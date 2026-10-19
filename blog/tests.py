from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Post


class PostTestMixin:
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_user(username="author", password="x" * 20)
        now = timezone.now()
        cls.published = Post.objects.create(
            author=cls.author, title="Published", text="Hello", published_date=now
        )
        cls.draft = Post.objects.create(author=cls.author, title="Draft", text="WIP")
        cls.scheduled = Post.objects.create(
            author=cls.author,
            title="Scheduled",
            text="Later",
            published_date=now + timedelta(days=1),
        )


class PostModelTests(PostTestMixin, TestCase):
    def test_str(self):
        self.assertEqual(str(self.published), "Published")

    def test_published_queryset_excludes_drafts_and_future_posts(self):
        self.assertQuerySetEqual(Post.objects.published(), [self.published])

    def test_publish_sets_date(self):
        self.draft.publish()
        self.draft.refresh_from_db()
        self.assertTrue(self.draft.is_published)

    def test_absolute_url(self):
        self.assertEqual(
            self.published.get_absolute_url(),
            reverse("blog:post_detail", kwargs={"pk": self.published.pk}),
        )


@override_settings(SECURE_SSL_REDIRECT=False)
class PostViewTests(PostTestMixin, TestCase):
    def test_list_shows_only_published(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published")
        self.assertNotContains(response, "Draft")
        self.assertNotContains(response, "Scheduled")

    def test_detail_published(self):
        response = self.client.get(self.published.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")

    def test_detail_draft_is_404(self):
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)

    def test_detail_scheduled_is_404(self):
        self.assertEqual(self.client.get(self.scheduled.get_absolute_url()).status_code, 404)

    def test_post_text_is_escaped(self):
        post = Post.objects.create(
            author=self.author,
            title="XSS",
            text="<script>alert(1)</script>",
            published_date=timezone.now(),
        )
        response = self.client.get(post.get_absolute_url())
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")
