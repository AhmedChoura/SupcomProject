# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse ,HttpResponseRedirect,Http404
from django.shortcuts import render , get_object_or_404 , redirect 
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.
from .models import Post
from .forms import PostForm

def post_list (request):
    today = timezone.now().date()
    queryset =Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset =Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "contacts":queryset,
        "today":today,
    }
    return render(request,"post_list.html",context)

def post_detail (request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    if instance.draft or instance.publish > timezone.now().date() :
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    # get the comment releated to the post
    comments = instance.comments

    initial_data = {
        "content_type" :instance.get_content_type,
        "object_id" : instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
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
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    if instance.file:
        t0,t1,t2,t4 = instance.file.url.split('/')
    else:
        t4 = ''
    context = {
        "title": instance.title,
        "instance": instance,
        "pdf_name": t4,
        "comments":comments,
        "comment_form":form,
    }
    return render(request,"comment_style.html",context)
    
@login_required(login_url='/login/')
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Post created.')
        return redirect("posts:list")
    else :
        messages.error(request, 'Post Not created.')
    context={
        "form":form,
    }
    return render(request,"post_form.html",context)

@login_required(login_url='/login/')
def post_edit(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404 (Post , slug =slug)
    form = PostForm(request.POST or None ,request.FILES or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit =False)
        instance.save()
        messages.success(request, 'Post details updated.')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title" : instance.title,
        "instance" : instance,
        'form' : form,
    }
    return render(request,"post_form.html",context)

@login_required(login_url='/login/')
def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        instance.delete()
        messages.success(request,"succsessfuly deleted")
        return redirect("posts:list")
    context ={
        "object":instance
    }
    return render(request,"confirm_delete.html",context)
