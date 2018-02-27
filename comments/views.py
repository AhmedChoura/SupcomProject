# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render , get_object_or_404
from .models import Comment
from .forms import CommentForm
# Create your views here.

def comment_thread(request, id):
    comment = get_object_or_404(Comment,id=id)
    initial_data = {
        "content_type" :comment.content_type,
        "object_id" : comment.object_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid()and request.user.is_authenticated():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get('object_id')
        content = form.cleaned_data.get('content')
        parent_obj = None
        # cheack if there is a parent id
        try:
            parent_id =int(request.POST.get('parent_id'))
        except:
            parent_id =None
        # cheack if it exist in the db
        if parent_id :
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj= parent_qs.first()
        new_comment,created = Comment.objects.get_or_create(
                                  user = request.user,
                                  content_type = content_type,
                                  object_id = object_id,
                                  content = content, 
                                  parent = parent_obj,
                                )
        return HttpResponseRedirect(comment.get_comment_url())
    context = {
        "comment":comment,
        "comment_form":form
    }
    return render(request, 'comment_thread.html',context)

@login_required(login_url='/login/')
def comment_delete(request, id):
    instance = get_object_or_404(Comment, id=id)
    if instance.user != request.user:
        reponse = HttpResponse('you do not have permission to do this.')
        reponse.status_code = 403
        return reponse
    obj_url = instance.content_object.get_absolute_url()
    if not instance.is_parent:
        parent_instance = get_object_or_404(Comment, id=instance.parent_id)
        obj_url = parent_instance.get_comment_url()
    instance.delete()
    messages.success(request,"succsessfuly deleted")
    return HttpResponseRedirect(obj_url)

@login_required(login_url='/login/')
def comment_delete_from_post(request, id):
    instance = get_object_or_404(Comment, id=id)
    obj_url = instance.content_object.get_absolute_url()
    instance.delete()
    messages.success(request,"succsessfuly deleted")
    return HttpResponseRedirect(obj_url)
