from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def published(self):
        """Posts whose publish date has been set and is not in the future."""
        return self.filter(published_date__isnull=False, published_date__lte=timezone.now())


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_date", "-created_date"]
        indexes = [models.Index(fields=["published_date"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})

    @property
    def is_published(self):
        return self.published_date is not None and self.published_date <= timezone.now()

    def publish(self):
        self.published_date = timezone.now()
        self.save(update_fields=["published_date"])
