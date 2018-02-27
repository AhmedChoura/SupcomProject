# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models 
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your models here.
# create a manger to filter the posts
class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte = timezone.now())
# define the location of the images and files with a specific names
def upload_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)
class Post (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True,blank=True, width_field = "width_field", height_field = "height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)           
    file = models.FileField(upload_to=upload_location,null=True,blank=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False)
    Created_At = models.DateTimeField(auto_now_add = True)
    Updated_At = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"slug":self.slug})
    def get_absolute_url_edit(self):
        return reverse("posts:edit",kwargs={"slug":self.slug})
    def get_absolute_url_delete(self):
        return reverse("posts:delete",kwargs={"slug":self.slug})   
    
    # this function will get the pagedown content and markedown to a html form "with the balise staff" and then make it safe to disply correctly
    def get_markdown(self):
        content= self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
    # get the comments for a specific posts 
    @property
    def comments(self):
        return Comment.objects.filter_by_instance(self)
    
    # get the Post class
    @property
    def get_content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    class Meta:
        ordering = ["-Created_At","-Updated_At"]
    #initialize the postmanager
    objects = PostManager()

def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug 
    qs = Post.objects.filter(slug = slug).order_by("-id")
    exists = qs.exists()
    if exists :
        new_slug = "%s-%s" %(slug,qs.first().id) 
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post,sender=Post)