
from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver
from .models import CustomUser as User
from posts.models import Post, Comment
from .models import *
from .forms import EditProfileForm, CustomUserChangeForm, EditEducationForm, EditFamilyForm, PostAddForm
from posts.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.models import EmailAddress
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.account.utils import send_email_confirmation
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse







@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    users = CustomUser.objects.filter(email=email_address)
    # profile = Profile.objects.filter(user_id=users)
    # if profile:
    #     login_if_exists(users, profile,sociallogin)
    if users:
        perform_login(request, users[0], email_verification=settings.ACCOUNT_EMAIL_VERIFICATION)

    # users.is_active = True
    # users.save()
    return sociallogin

# @receiver(perform_login)
# def login_if_exists(request, users, sociallogin, **kwargs):
#     profile = Profile.objects.filter(user_id=users)



@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):

    if sociallogin:
        user.is_active = True
        user.save()
    else:
        user.is_active = False
        user.save()
        after_user_signed_up(request, user=user)

def after_user_signed_up(request, user, **kwargs):
    send_email_confirmation(request, user, True)


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    user = CustomUser.objects.get(email=email_address.email)
    user.is_active = True
    user.save()

# def info(request):
#     return render(request, 'profiles/information.html', {})


@login_required
def profile(request):

    myuser = CustomUser.objects.filter( id=request.user.id).first()
    profile = Profile.objects.filter(user_id=myuser).first()
    posts = Post.objects.filter(author_id=profile)
    context = {'posts': posts,
               'profile':profile}

    return render(request, 'profiles/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    user_id = user.id
    form = EditProfileForm(request.POST or None ,request.FILES or None,  instance=user.profile)
    if form.is_valid():
        # pic = Profile(avatar = request.FILES['avatar'])
        profile = form.save(commit=False)
        profile.user_id = user_id
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        return redirect('profile')
    return render(request, 'profiles/edit_profile.html',{'form':form})

@login_required
def education(request):
    myuser = CustomUser.objects.filter( id=request.user.id).first()
    education = Education.objects.filter(user_id=myuser)
    return render(request, 'profiles/education.html', {'education': education})

@login_required
def edit_education(request, pk, template_name = 'profiles/edit_education.html' ):

    edu = get_object_or_404(Education, pk=pk)
    form = EditEducationForm(request.POST or None, instance=edu)
    if form.is_valid():
        form.save()
        return redirect('education')
    return render(request, template_name, {'form':form})


@login_required
def add_education(request):
    form = EditEducationForm(request.POST)
    if form.is_valid():

        edu = form.save(commit=False)
        edu.user = request.user
        edu.save()
        return redirect('/education')
    else:
        args = {'form': form}
        return render(request, 'profiles/edit_education.html', args)

@login_required
def delete_education(request, pk):
    template = 'common/confirm_Delete.html'
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        edu.delete()
        return redirect('education')
    context = {'edu': edu}
    return render(request, template, context)


@login_required
def family(request):

    myuser = CustomUser.objects.filter( id=request.user.id).first()
    family = FamilyInfo.objects.filter(user_id=myuser)
    return render(request, 'profiles/family.html', {'family': family})
@login_required
def add_family(request):
    form = EditFamilyForm(request.POST)
    if form.is_valid():

        family = form.save(commit=False)
        family.user = request.user
        family.save()
        return redirect('/family')
    else:
        args = {'form': form}
        return render(request, 'profiles/edit_family.html', args)

@login_required
def edit_family(request, pk, template_name = 'profiles/edit_family.html' ):

    family = get_object_or_404(FamilyInfo, pk=pk)
    form = EditFamilyForm(request.POST or None, instance=family)
    if form.is_valid():
        form.save()
        return redirect('family')
    return render(request, template_name, {'form':form})

@login_required
def delete_family(request, pk):
    template = 'common/confirm_Delete.html'
    family = get_object_or_404(FamilyInfo, pk=pk)
    if request.method == 'POST':
        family.delete()
        return redirect('family')
    context = {'family': family}
    return render(request, template, context)

# def testing():
#     template = 'profiles/testing.html'
#     return HttpResponse(template)

def testing(request):
    user = request.user

    if user.is_authenticated:

        user_profile = Profile.objects.filter(user_id=user).first()  # it always has to be one user
        friend = Connection.objects.get(follower=user_profile)
        friends = friend.following.all()
        posts = Post.objects.all()

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.post_id = comment_form['post_id']
            comment.author = Profile.objects.filter(user_id = request.user.id).first()
            comment.save()
            return redirect('testing')


        form = PostAddForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = user.profile.id
            post.save()
            return redirect('testing')

        args = {'form': form,
                'posts': posts,
                'friends': friends,
                'comment_form': comment_form
                }
        return render(request, 'newsfeed.html', args)
    else:
        return render(request, 'login_screen.html')


# @login_required
def home(request):
    user = request.user
    num_of_user = CustomUser.objects.count()
    num_of_posts = Post.objects.count()

    if user.is_authenticated:

        user_profile = Profile.objects.filter(user_id=user).first()  # it always has to be one user
        # friend = get_object_or_404(Friend, follower=user_profile)
        following = Friend.objects.filter(following=user_profile)

        # friends = friend.following.all()
        all_posts = Post.objects.all().order_by('-created_date')

        page = request.GET.get('page', 1)
        paginator = Paginator(all_posts, 5)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        form = PostAddForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = user.profile.id
            post.save()
            return redirect('home')

        args = {
                'posts': posts,
                'following': following,
                'form': form,
                }
        return render(request, 'newsfeed.html', args)
    else:
        without_login = {
            'num_of_users': num_of_user,
            'num_of_posts':num_of_posts
        }
        return render(request, 'login_screen.html', without_login)

@login_required
def change_connection(request, operation, pk):
    friend = Profile.objects.get(pk=pk)
    friend = friend.id
    path = request.path_info
    current_user = request.user.profile.id
    if operation == 'follow':
        Connection.follow(current_user, friend)
        return HttpResponseRedirect(path)
    elif operation == 'unfollow':
        Connection.unfollow(current_user, friend)
    return HttpResponseRedirect(path)

@login_required
def timeline(request, pk):
    profile = Profile.objects.filter(pk = pk).first()
    followers = Friend.objects.filter(following=profile).count()
    posts = Post.objects.filter(author=profile).order_by('-created_date')
    post_form = PostAddForm(request.POST)
    auth_user_profile = Profile.objects.filter(user=request.user).first()
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = auth_user_profile
        post.save()
        return redirect('timeline' , auth_user_profile.id)

    args = {'profile': profile,
            'posts' : posts,
            'post_form': post_form,
            'auth_user_profile': auth_user_profile,
            'followers':followers
            }

    return render(request, 'profiles/timeline.html', args)


@login_required
def edit_basic_info(request,):
    user = request.user
    user_id = user.id
    user_profile = Profile.objects.filter(user = user).first()
    form = EditProfileForm(request.POST or None ,request.FILES or None,  instance=user_profile)
    if form.is_valid():
        # pic = Profile(avatar = request.FILES['avatar'])
        profile = form.save(commit=False)
        profile.user_id = user_id
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()

        return redirect('about', user_profile.id)
    return render(request, 'profiles/edit-profile-basic.html',{'form':form, 'profile':user_profile})

@login_required
def edu_work(request):
    user= request.user
    user_profile = Profile.objects.filter(user = user).first()

    edu_form = EditEducationForm(request.POST)
    if edu_form.is_valid():
        edu = edu_form.save(commit=False)
        edu.profile = user_profile
        edu.save()
        return redirect('add_edu_work', )
    else:
        args = {'edu_form': edu_form, 'profile': user_profile}
        return render(request, 'profiles/edit-profile-education.html', args)

@login_required
def add_family(request):
    user = request.user
    # profile = Profile.objects.filter(user=request.user).first()
    user_profile = Profile.objects.filter(user = user).first()

    family_form = EditFamilyForm(request.POST)
    if family_form.is_valid():

        family = family_form.save(commit=False)
        family.profile = user_profile
        family.save()
        return redirect('add_family' ,)
    else:
        args = {'family_form': family_form, 'profile': user_profile}
        return render(request, 'profiles/edit-profile-family.html', args)

@login_required()
def about(request,pk ):
    profile = Profile.objects.filter(pk=pk).first()
    user_edu = Education.objects.filter(profile_id=profile.id)
    family = FamilyInfo.objects.filter(profile_id=profile.id)

    arg = {'education' : user_edu,
            'profile' : profile,
           'family': family
           }

    return render(request, 'profiles/about.html', arg)

def get_followers(request, pk):
    curr_user = request.user.profile
    user_following = Friend.objects.filter(follower=curr_user).values_list('following', flat=True)
    profile = Profile.objects.filter(pk=pk).first()
    followers = Friend.objects.filter(following=profile)
    args = {
        'curr_user':curr_user,
        'user_following': user_following,
        'followers':followers,
        'profile':profile
    }
    return render(request, 'profiles/followers.html', args)


def get_following(request, pk):
    curr_user = request.user.profile
    profile = Profile.objects.filter(pk=pk).first()
    user_following = Friend.objects.filter(follower=curr_user).values_list('following', flat=True)
    following = Friend.objects.filter(follower=profile)

    args = {
        'curr_user':curr_user,
        'following':following,
        'profile':profile,
        'user_following':user_following
    }
    return render(request, 'profiles/following.html', args)

@login_required()
def follow(request, pk):
    path = request.path_info
    current_user = request.user.profile
    connection = Profile.objects.filter(pk=pk).first()
    if current_user and connection:
        friend_check = Friend.objects.filter(Q(following=connection) & Q(follower=current_user))
        if friend_check:
            messages.error(request, "You are already following %s" % (connection.user.first_name))
            return redirect('/')

        else:
            perform_follow = Friend(follower=current_user, following=connection)
            perform_follow.save()
            messages.success(request, "Successfully followed %s %s" % (connection.user.first_name, connection.user.last_name))
            return redirect('/')
        return redirect('/')

    else:
        messages.error(request, "something went wrong")
        return redirect('/')

def unfollow(request, pk):
    path = request.path_info
    current_user = request.user.profile
    connection = Profile.objects.filter(pk=pk).first()
    if current_user and connection:
        friend_check = Friend.objects.filter(Q(following=connection) & Q(follower=current_user))
        if friend_check:
            friend_check.delete()
            messages.success(request, "Unfollowed %s" % (connection.user.first_name))
            # return HttpResponseRedirect(request.path_info)
            return HttpResponseRedirect(reverse(path))

        else:
            messages.error(request, "You are not following %s" % (connection.user.first_name))
            return redirect('/')

    else:
        messages.error(request, "something went wrong")
        return redirect('/')

def friend_suggestions():
    pass