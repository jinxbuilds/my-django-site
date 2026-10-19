from django.contrib import admin
from django.utils import timezone

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_date", "published_date", "is_published")
    list_filter = ("published_date", "created_date", "author")
    search_fields = ("title", "text")
    date_hierarchy = "created_date"
    raw_id_fields = ("author",)
    actions = ("make_published",)

    @admin.display(boolean=True, description="Published")
    def is_published(self, obj):
        return obj.is_published

    @admin.action(description="Publish selected posts now")
    def make_published(self, request, queryset):
        updated = queryset.filter(published_date__isnull=True).update(
            published_date=timezone.now()
        )
        self.message_user(request, f"{updated} post(s) published.")
