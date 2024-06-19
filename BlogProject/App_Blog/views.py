from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import CreateView,UpdateView,ListView,DetailView,View,TemplateView,DeleteView
from django.urls import reverse,reverse_lazy
from .models import Blog,Comment,Likes
import uuid
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
# def BlogList(request):
    # return render(request,'App_Blog/blog_list.html')
class MyBlog(LoginRequiredMixin,TemplateView):
    template_name='App_Blog/my_blog.html'



class CreateBlog(LoginRequiredMixin,CreateView):
    model=Blog
    template_name="App_Blog/create_blog.html"
    fields=('blog_title','blog_content','blog_image')
    def form_valid(self,form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug=title.replace(' ','-')+"-"+str(uuid.uuid4)
        print(type(blog_obj.slug))
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))
    
class BlogList(ListView):
    context_object_name='blogs'
    model=Blog
    template_name='App_Blog/blog_list.html'


@login_required
def blog_details(request,pk):
    blog = Blog.objects.get(pk=pk)
    comment_form = CommentForm()
    already_liked= Likes.objects.filter(blog=blog,user =request.user)
    if already_liked:
        Liked = True
    else:
        Liked = False
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            context = {'blog': blog, 'comment': comment}  # Pass comment only if saved
            print(comment_form)
            return HttpResponseRedirect(reverse('App_Blog:details_blog', kwargs={'pk': pk}))
    context = {'blog': blog, 'comment_form': comment_form,'Liked':Liked}  # Pass only form for GET requests
    return render(request, 'App_Blog/blog_details.html', context)

@login_required
def liked(request,pk):
    blog= Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        like_post =Likes(blog=blog,user=user)
        like_post.save()
    return HttpResponseRedirect(reverse('App_Blog:details_blog',kwargs={'pk':blog.pk}))

@login_required
def unLiked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked =Likes.objects.filter(blog=blog,user=user)
    already_liked.delete()

    return HttpResponseRedirect(reverse('App_Blog:details_blog',kwargs={'pk':blog.pk}))

from django.contrib import messages
class UpdateBlog(LoginRequiredMixin,UpdateView):
    model= Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = 'App_Blog/edit_blog.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Updated Successfully')
        return reverse('App_Blog:details_blog', args=(self.kwargs['pk'],))

    