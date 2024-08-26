from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CreateForm
from blog.models import Post, Category


# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = CreateForm
    #fields = ['title', 'content', 'category']

def create_post(request):
    if request.method == 'GET': categories = Category.objects.all()
    return render(request, 'post_create_function.html', {'categories': categories})
    title = request.POST.get('title')
    content = request.POST.get('title')
    category_id  = request.POST.get('category_id')
    category = request.POST.get('category')
    author_id = request.POST.get('author_id')
    author = request.POST.get('author')
    Post.objects.create(title=title, content=content, category=category, author=author)
    return render(request, 'post_create_function.html')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'post_update.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'

    def get_success_url(self):
        return reverse_lazy('home')

