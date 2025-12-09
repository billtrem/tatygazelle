from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


# ---------------------------------------------------
# HOMEPAGE CAROUSEL IMAGES (UNLIMITED)
# ---------------------------------------------------

class HomepageImage(models.Model):
    image = CloudinaryField('image')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.caption or f"Homepage Image {self.id}"


# ---------------------------------------------------
# INFO / ABOUT PAGE (Singleton editable entry)
# ---------------------------------------------------

class InfoPageContent(models.Model):
    portrait = CloudinaryField('image', blank=True, null=True)
    bio = models.TextField()
    contact_email = models.EmailField(blank=True, null=True)

    # Ensures only ONE row exists — prevents duplicates in admin
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Info Page Content"

    class Meta:
        verbose_name = "Info Page Content"
        verbose_name_plural = "Info Page Content"


# ---------------------------------------------------
# PROJECT MODEL
# ---------------------------------------------------

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# ---------------------------------------------------
# PROJECT IMAGES (Unlimited gallery)
# ---------------------------------------------------

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.project.title} Image {self.pk}"
