from django.contrib import admin
from django.utils.html import format_html
from .models import HomepageImage, InfoPageContent, Project, ProjectImage


# -----------------------------------------------------
# HOMEPAGE CAROUSEL ADMIN
# -----------------------------------------------------

@admin.register(HomepageImage)
class HomepageImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order', 'is_active', 'preview')
    list_editable = ('order', 'is_active')
    readonly_fields = ('preview',)
    ordering = ('order', 'id')

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="140" style="border-radius:4px;">', obj.image.url)
        return "-"
    preview.short_description = "Preview"


# -----------------------------------------------------
# INFO PAGE ADMIN — SINGLETON
# -----------------------------------------------------

@admin.register(InfoPageContent)
class InfoPageContentAdmin(admin.ModelAdmin):
    list_display = ('contact_email', 'portrait_preview')
    readonly_fields = ('portrait_preview',)

    def portrait_preview(self, obj):
        if obj.portrait:
            return format_html('<img src="{}" width="120" style="border-radius:4px;">', obj.portrait.url)
        return "-"
    portrait_preview.short_description = "Portrait"

    def has_add_permission(self, request):
        # prevents more than 1 info page entry
        return not InfoPageContent.objects.exists()


# -----------------------------------------------------
# PROJECT IMAGES INLINE
# -----------------------------------------------------

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2
    fields = ('image', 'caption', 'order', 'preview')
    readonly_fields = ('preview',)
    ordering = ('order', 'id')

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="90" style="border-radius:4px;">', obj.image.url)
        return "-"
    preview.short_description = "Preview"


# -----------------------------------------------------
# PROJECT ADMIN
# -----------------------------------------------------

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'order', 'created_at')
    list_editable = ('order', 'is_published')
    inlines = [ProjectImageInline]
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-created_at')
