from django.shortcuts import render, get_object_or_404
from .models import HomepageImage, InfoPageContent, Project

def home(request):
    images = HomepageImage.objects.all()
    return render(request, 'main/home.html', {'images': images})

def info(request):
    info = InfoPageContent.objects.first()
    return render(request, 'main/info.html', {'info': info})

def project_list(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, 'main/projects.html', {'projects': projects})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'main/project_detail.html', {'project': project})

def landing(request):
    # optional hero image (take first from homepage images)
    hero_image = HomepageImage.objects.first()
    return render(request, "main/landing.html", {"hero_image": hero_image})
