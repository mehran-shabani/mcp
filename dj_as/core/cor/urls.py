from django.urls import path
from .views import Ping, WaitMany, FetchMany, TaskListCreate

urlpatterns = [
    path("ping/", Ping.as_view(), name="ping"),
    path("wait/", WaitMany.as_view(), name="wait-many"),
    path("fetch/", FetchMany.as_view(), name="fetch-many"),
    path("tasks/", TaskListCreate.as_view(), name="tasks"),
]
