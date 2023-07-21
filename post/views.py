from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.http import require_POST





def Home(request):

    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.published.filter(title__icontains = search_query)
    else:
        posts = Post.published.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/home.html', context)





def post_detail(request, day, month, year, slug):
    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED,
        publish__day = day,
        publish__month = month,
        publish__year = year,
        slug=slug
        )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'post/post_detail.html', context)




def Post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends your read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"

            send_mail(
                subject,
                message,
                'atabekdemurtaza@gmail.com',
                [cd['to']],
            )
            sent = True

    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent
    }
    return  render(request, 'post/share.html', context)


def logout(request):
    return render(request, 'registration/logout.html')


def password_change(request):
    return render(request, 'registration/password_change__form.html')

def password_change_done(request):
    return render(request, 'registration/password_change__done.html')

@require_POST
def Post_comment(request, post_id):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = { 
        'post': post,
        'comment': comment,
        'form': form
    }
    return render(request, 'post/post_comment.html', context)





def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if  form.is_valid():
            cd=form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Такого аккаунта не существует')
            else:
                return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form
    }   
    return render(request, 'registration/login.html', context)





#РЕГИСТРАЦИЯ
def Register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():

            new_user = user_form.save(commit=False)

            new_user.set_password(
            user_form.cleaned_data['password'])

            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)

            context = {
                'new_user': new_user,
                'user_form':user_form
            }
            return render(request, 'registration/register_done.html', context)
    else:
        user_form = UserRegisterForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/register.html', context)







@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно редактирован')
        else:
    
            messages.success(request, 'Ошибка при редактировании')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {

        'user_form': user_form,
        'profile_form': profile_form
        }
    return render(request, 'registration/edit.html', context)


def contact(request):
    return render(request, 'post/contact.html')