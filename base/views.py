from lib2to3.fixes.fix_input import context
from re import search
from venv import create

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import TaskForm


from .models import Task

class CustomSigninView(LoginView):
    template_name = 'base/signin.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class SignUpView(FormView):
    template_name = 'base/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(SignUpView, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort-by') or 'due_date'
        queryset = Task.objects.filter(user=self.request.user)
        if sort_by == 'due_date':
            queryset = queryset.order_by('complete', 'due_date')
        elif sort_by == 'create':
            queryset = queryset.order_by('complete', 'create')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Підрахунок кількості неповних задач
        context['count'] = context['object_list'].filter(complete=False).count()

        # Обробка пошукового запиту
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['object_list'] = context['object_list'].filter(title__icontains=search_input)
        context['search_input'] = search_input

        # Обробка сортування
        sort_input = self.request.GET.get('sort-by') or 'due_date'
        context['sort_input'] = sort_input

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
