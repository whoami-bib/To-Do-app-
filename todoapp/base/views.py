
from django.shortcuts import render,redirect
from .models import Task
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class customUserLogin(LoginView):
    template_name='base/login.html'
    fields = '__all__'
    redirect_authenticated_user= True
    

    def get_success_url(self):
        return reverse_lazy('todolist')

    def get(self, *args, **kwargs):
        return super(customUserLogin,self).get(*args, **kwargs)
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todolist')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todolist')
        return super(RegisterPage,self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model = Task
    ordering=['created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list']=context['object_list'].filter(user=self.request.user)
        context['count']=context['object_list'].filter(completed=False).count()
        

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['object_list'] = context['object_list'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context
class TaskDetail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name ='task'

class CreateTask(LoginRequiredMixin, CreateView):
    model  = Task
    fields = ['title', 'description','completed']
    success_url= reverse_lazy('todolist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask,self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    model= Task
    fields = ['title', 'description','completed']
    success_url= reverse_lazy('todolist')

class DeleteTask(DeleteView):
    model= Task
    template_name= 'base/delete.html'
    success_url= reverse_lazy('todolist')