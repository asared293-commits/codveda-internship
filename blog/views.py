from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Post
from .forms import RegisterForm, PostForm


def home(request):
    posts = Post.objects.all()
    return render(request, "blog/home.html", {"posts": posts})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(
        request,
        "blog/post_detail.html",
        {"post": post}
    )


def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_staff
    )(view_func)


@login_required
@staff_required
def create_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("post_detail", pk=post.pk)

    else:
        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "title": "Create Post"
        }
    )


@login_required
@staff_required
def edit_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "title": "Edit Post"
        }
    )


@login_required
@staff_required
def delete_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(
        request,
        "blog/post_confirm_delete.html",
        {"post": post}
    )