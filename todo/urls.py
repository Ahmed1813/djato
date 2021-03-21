from django.urls import path

from .views import (
    GroupCreateView, 
    GroupDeleteView, 
    GroupListView,
    GroupUpdateView, 
    HomeView, 
    FeatureView, 
    TodoListView,
    TodosCreateView,
    TodosEditView,
    TodosDeleteView,
    ChangeTodoStateView,
)

app_name = "todo"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("feature/", FeatureView.as_view(), name="features"),
    path("groups/", GroupListView.as_view(), name="groups"),
    path("groups/add/", GroupCreateView.as_view(), name="add_group"),
    path("groups/edit/<int:pk>/", GroupUpdateView.as_view(), name="update_group"),
    path("groups/delete/<int:pk>/", GroupDeleteView.as_view(), name="delete_group"),
    path("groups/list/<int:pk>/", TodoListView.as_view(), name="todos_list"),
    path("groups/list/<int:pk>/add/", TodosCreateView.as_view(), name="add_todo"),
    path("groups/list/<int:group_id>/edit/<int:pk>/", TodosEditView.as_view(), name="edit_todo"),
    path("groups/list/<int:group_id>/delete/<int:pk>/", TodosDeleteView.as_view(), name="delete_todo"),
    path("groups/list/<int:group_id>/change/<int:pk>/", ChangeTodoStateView.as_view(), name="change_todo_state"),
]
