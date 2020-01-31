from django.test import TestCase
from django.urls import reverse
from .models import Board


class LoginRequiredNewTopicTests(TestCase):

    def setup(self):
        Board.objects.create(name="Django" ,description="django dj")
        