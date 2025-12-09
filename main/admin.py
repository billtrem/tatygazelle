from django.contrib import admin
from django.utils.html import format_html
from .models import HomepageImage, InfoPageContent, Project, ProjectImage

@admin.register(HomepageImage)
class HomepageImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="140">', obj.image.url)
        return "-"
    preview.short_description = "Preview"

@admin.register(InfoPageContent)
class InfoPageContentAdmin(admin.ModelAdmin):
    list_display = ('contact_email', 'portrait_preview')
    readonly_fields = ('portrait_preview',)

    def portrait_preview(self, obj):
        if obj.portrait:
            return format_html('<img src="{}" width="120">', obj.portrait.url)
        return "-"
    portrait_preview.short_description = "Portrait"

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'order', 'created_at')
    list_editable = ('order',)
    inlines = [ProjectImageInline]
    prepopulated_fields = {'slug': ('title',)}
