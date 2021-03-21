from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse, Http404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, 
    ListView, 
    TemplateView,
    UpdateView, 
    View,
)
from django.views.generic.edit import BaseCreateView

from .forms import GroupModelForm, TodosModelForm
from .models import GroupModel, TodosModel


# Create your views here.
class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "todo/index.html")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home_class"] = 'active'
        return context
    

class FeatureView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "todo/feature.html")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feature_class"] = 'active'
        return context


class GroupListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('user:login')
    template_name = "todo/group_list.html"

    def get_queryset(self):
        return GroupModel.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group_class"] = 'active'
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('user:login')
    form_class = GroupModelForm
    template_name = 'todo/show_form.html'
    success_url = reverse_lazy('todo:groups')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Group Successfully Created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Group"
        context["submit_icon"] = "fa-plus"
        context["submit_value"] = "Add"
        return context


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('user:login')
    form_class = GroupModelForm
    template_name = "todo/show_form.html"
    success_url = reverse_lazy('todo:groups')

    def get_queryset(self):
        return GroupModel.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Group Successfully Updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Group"
        context["submit_icon"] = "fa-save"
        context["submit_value"] = "Save"
        return context


class GroupDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy('todo:groups')
    login_url = reverse_lazy('user:login')

    def get_queryset(self):
        return GroupModel.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Group Successfully Deleted.")
        return redirect(self.success_url)


class TodoListView(LoginRequiredMixin, View):
    template_name = 'todo/todos_list.html'
    login_url = reverse_lazy('user:login')

    def get_queryset(self):
        return TodosModel.objects.filter(user=self.request.user, group__pk=self.kwargs.get('pk'))

    def get_object(self):
        return get_object_or_404(GroupModel, user=self.request.user, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = {}
        context["group"] = self.get_object()
        context["todos_list"] = self.get_queryset()
        return context
        
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        
        return render(request, self.template_name, context)
    

class TodosCreateView(LoginRequiredMixin, CreateView):
    template_name = 'todo/todos_list.html'
    login_url = reverse_lazy('user:login')
    template_name = "todo/show_form.html"
    form_class = TodosModelForm

    def get_success_url(self):
        return reverse('todo:todos_list', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.group = get_object_or_404(GroupModel, pk=self.kwargs.get('pk'))
        messages.success(self.request, "Todo Successfully Created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Todo"
        context["submit_icon"] = "fa-plus"
        context["submit_value"] = "Add"
        context["group_id"] = self.kwargs.get('pk')
        return context


class TodosEditView(LoginRequiredMixin, UpdateView):
    template_name = 'todo/show_form.html'
    login_url = reverse_lazy('user:login')
    template_name = "todo/show_form.html"
    form_class = TodosModelForm

    def get_success_url(self):
        return reverse('todo:todos_list', kwargs={'pk': self.kwargs.get('group_id')})

    def get_queryset(self):
        group = get_object_or_404(GroupModel, user=self.request.user, pk=self.kwargs.get('group_id'))
        lists = TodosModel.objects.filter(user=self.request.user, group=group)
        return lists

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.group = get_object_or_404(GroupModel, pk=self.kwargs.get('group_id'))
        messages.success(self.request, "Todo Successfully Updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Todo"
        context["submit_icon"] = "fa-save"
        context["submit_value"] = "Save"
        context["group_id"] = self.kwargs.get('group_id')
        return context


class TodosDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get_success_url(self):
        return reverse('todo:todos_list', kwargs={'pk': self.kwargs.get('group_id')})

    def get_queryset(self):
        group = get_object_or_404(GroupModel, pk=self.kwargs.get('group_id'))
        return TodosModel.objects.filter(user=self.request.user, group=group)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Todo Successfully Deleted.")
        return redirect(self.get_success_url())


class ChangeTodoStateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get_success_url(self):
        return reverse('todo:todos_list', kwargs={'pk': self.kwargs.get('group_id')})

    def get_queryset(self):
        group = get_object_or_404(GroupModel, pk=self.kwargs.get('group_id'))
        return TodosModel.objects.filter(user=self.request.user, group=group)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.completed = True if not self.object.completed else False
        self.object.save()
        messages.success(request, "Task Completed.")
        return redirect(self.get_success_url())

