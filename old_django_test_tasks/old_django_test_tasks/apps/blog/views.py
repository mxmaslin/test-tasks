from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import Post
from .forms import PostCreateForm


class PostList(ListView):
    queryset = Post.objects.all().order_by('-created_on')[:10]
    template_name = 'index.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreate(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'
