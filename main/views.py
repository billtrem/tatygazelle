from django.shortcuts import render, get_object_or_404
from .models import HomepageImage, InfoPageContent, Project


# -------------------------------------------------------
# LANDING PAGE (full screen intro)
# -------------------------------------------------------
def landing(request):
    # Landing uses ONLY the first homepage image as hero
    hero_image = HomepageImage.objects.filter(is_active=True).order_by('order').first()
    return render(request, "main/landing.html", {"hero_image": hero_image})


# -------------------------------------------------------
# HOME PAGE — CAROUSEL OF IMAGES
# -------------------------------------------------------
def home(request):
    # Load all active homepage images, in order
    images = HomepageImage.objects.filter(is_active=True).order_by('order', 'id')

    return render(request, 'main/home.html', {
        'images': images,
    })


# -------------------------------------------------------
# INFO PAGE (singleton)
# -------------------------------------------------------
def info(request):
    info = InfoPageContent.objects.first()
    return render(request, 'main/info.html', {'info': info})


# -------------------------------------------------------
# PROJECT LIST
# -------------------------------------------------------
def project_list(request):
    projects = Project.objects.filter(is_published=True).order_by('order', '-created_at')
    return render(request, 'main/projects.html', {'projects': projects})


# -------------------------------------------------------
# PROJECT DETAIL
# -------------------------------------------------------
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'main/project_detail.html', {'project': project})
