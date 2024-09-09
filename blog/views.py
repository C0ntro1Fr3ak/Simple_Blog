import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from blog.forms import CreateForm
from blog.models import Post, Category, Profile
from blog.utils import create_user_profile


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
    # fields = ['title', 'content', 'category']


def create_post(request):
    if request.method == 'GET': categories = Category.objects.all()
    return render(request, 'post_create_function.html', {'categories': categories})
    title = request.POST.get('title')
    content = request.POST.get('title')
    category_id = request.POST.get('category_id')
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


def likes_or_not(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('post_detail', pk=post.id)


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'


def create_profile(request):
    if request.method == 'GET':
        return render(request, template_name='create_profile.html')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    github = request.POST.get('github')
    email = request.POST.get('email')
    user = User.objects.get(id=request.user.id)
    Profile.objects.create(user=user, phone=phone, address=address, email=email, github=github)
    return render(request, template_name='profile.html', context={'object': user})


def register_user(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    username = request.POST.get('username')
    if username in User.objects.values_list('username', flat=True):
        return render(request, 'register.html',
                      {'error': 'Username already exists'})
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if password1 != password2:
        return render(request, 'register.html',
                      {'error': 'Passwords do not match'})
    if User.objects.create_user(username=username, email=email,
                                first_name=first_name,
                                last_name=last_name):
        user = User.objects.get(username=username)
        user.set_password(password1)
        user.save()
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        github = request.POST.get('github')
        create_user_profile(username, password1, first_name, last_name, phone, email, address, github, 3)

        Profile.objects.create(user=user,
                               phone=phone,
                               address=address,
                               github=github)
        return render(request, 'registration/login.html')
    else:
        return render(request, 'register.html',
                      {'error': 'Something went wrong'})


def load_user_from_file(request):
    if request.method == 'GET':
        return render(request, 'load_user_from_file.html')
    file = request.FILES.get('users_file')
    print(file)
    if file:
        excel_file = pd.read_excel(file)
        data = pd.DataFrame(excel_file)
        usernames = data['Username'].values.tolist()
        first_names = data['FirstName'].values.tolist()
        last_names = data['LastName'].values.tolist()
        emails = data['Email'].values.tolist()
        dobs = data['DoB'].values.tolist()
        phones = data['Phone'].values.tolist()
        addresses = data['Address'].values.tolist()
        githubs = data['Github'].values.tolist()
        for i in range(len(usernames)):
            print("user", i)
            username = usernames[i]
            first_name = first_names[i]
            last_name = last_names[i]
            email = emails[i]
            dob = dobs[i]
            print(dob)
            phone = phones[i]
            address = addresses[i]
            github = githubs[i]
            print(username)
            print(first_name)
            password1 = str(pd.to_datetime(dob, utc=True).date()).replace("-", "")
            create_user_profile(username, password1, first_name, last_name, phone, email, address, github, 1)
        return render(request, 'home.html')
