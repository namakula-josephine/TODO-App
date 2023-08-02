from django.utils import timezone
from django.shortcuts import redirect
from .models import Task
from django.views.generic.list import ListView
from django.contrib.auth import login
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewUserForm
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
import calendar
from datetime import datetime



# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
       return reverse_lazy ('tasks')



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = super().get_queryset()
        tasks = tasks.filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            tasks = tasks.filter(title__icontains=search_input)
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area', '')
        
        
        context['calendar'] = self.get_calendar_html()

        return context

    def get_calendar_html(self):
        
        year = datetime.now().year
        month = datetime.now().month
        calendar_html = self.generate_calendar(year, month)
        return mark_safe(calendar_html)

    def generate_calendar(self, year, month):

        cal = calendar.HTMLCalendar().formatmonth(year, month)
        return cal


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due', 'time']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PendingTaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/pending.html'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user, complete=False)


class FinishedTaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/finished.html'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user, complete=True)


class SkippedTaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/skipped.html'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user, complete=False, due__lt=timezone.now())


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'due', 'time']
    success_url = reverse_lazy('tasks')


class  DeleteView(LoginRequiredMixin,DeleteView):
     model= Task
     context_object_name='task'
     success_url= reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = NewUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(*args, **kwargs)
    
class CalendarView(TemplateView):
    template_name = 'base/calendar.html'    

