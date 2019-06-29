from django.shortcuts import render
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from users.models import CustomUser, Profile
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, PostAddForm


# Create your views here.



def user_posts(request):
    myuser = CustomUser.objects.filter(id=request.user.id).first()
    profile = Profile.objects.filter(user_id=myuser)
    posts = Post.objects.all(author_id=profile)
    return render(request, 'profiles/profile.html', {'posts': posts})



def add_post(request):
    user = request.user
    profile = Profile.objects.filter(user_id=user.id).first()

    if request.method == "POST":
        id_post = request.POST.get('id_post')
        form = PostAddForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post = Post(text='id_post')
            post.author = profile
            post.save()
            return redirect('testing')
    else:
        form = PostAddForm()
    return render(request, 'mayoforce/newsfeed.html', {'form': form})


def add_comment_to_post(request ,pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    comment_author = Profile.objects.filter(user_id=user).first()
    comment_author = comment_author


    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = comment_author
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'newsfeed.html', {'form': form})

def get_post(request, pk):
    post = Post.objects.filter(pk=pk).first()
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment_form.post_id = post.id
        comment_form.save()
        return redirect(request, 'get_post')
    return redirect(request, 'get_post')
