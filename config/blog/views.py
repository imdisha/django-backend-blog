# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render
# from .models import Post

# def post_list(request):
#     posts = Post.objects.all().order_by('-created_at')
#     return render(request, 'blog/post_list.html', {'posts': posts})
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import PostForm
from django.core.paginator import Paginator

from django.core.paginator import Paginator
from .models import Post

def post_list(request):
    posts = Post.objects.order_by('-created_at')  # ❗ NO FILTER HERE
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('post_list')

    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})
