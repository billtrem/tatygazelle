from django.urls import path
from . import views

urlpatterns = [
    # LANDING PAGE (root)
    path("", views.landing, name="landing"),

    # OPTIONAL home page (if you still want it)
    path("home/", views.home, name="home"),

    # Info/About
    path("info/", views.info, name="info"),

    # Project List + Detail
    path("projects/", views.project_list, name="project_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
]
