from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from food_cordoba.models import Post, Profile, Mensaje
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    context = {'posts': Post.objects.all()}
    return render(request,"food_cordoba/index.html", context)
    
def about(request):
    return render(request,"food_cordoba/about.html")

class PostList(ListView):
    model = Post

class PostDetail(DetailView):
    model = Post

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy("post-list")
    fields = '__all__'

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    success_url = reverse_lazy("post-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(publicador=user_id, id=post_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "food_cordoba/not_found.html")


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post-list")

    def test_func(self):
        user_id = self.request.user.id
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(publicador=user_id, id=post_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "food_cordoba/not_found.html")

class SignUp(CreateView):
       form_class = UserCreationForm
       template_name = 'registration/signup.html'
       success_url =    reverse_lazy('index')

class Login(LoginView):
    next_page = reverse_lazy('index')

class Logout(LogoutView):
    template_name = 'registration/logout.html'

class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Profile
    fields = '__all__'
    success_url =    reverse_lazy('index')

    def test_func(self):
        user_id = self.request.user.id
        profile_id = self.kwargs.get('pk')
        return Profile.objects.filter(user=user_id, id=profile_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "food_cordoba/not_found.html")

class ProfileCreate(CreateView): 
    model = Profile
    fields = '__all__'
    success_url =    reverse_lazy('index')

class MensajeCreate(CreateView):
    model = Mensaje
    fields = '__all__'
    success_url =    reverse_lazy('index')

class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"

    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user.id).all()

class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mensaje
    success_url =    reverse_lazy('index')

    def test_func(self):
        user_id = self.request.user.id
        mensaje_id = self.kwargs.get('pk')
        return Mensaje.objects.filter(destinatario=user_id, id=mensaje_id).exists()
    
    def handle_no_permission(self):
        return render(self.request, "food_cordoba/not_found.html")
