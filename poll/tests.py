from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTest(TestCase):
    '''
    Here we have created a django.test.TestCase subclass with a method that creates a
    Question instance with a pub_date in the future.
    We then check the output of was_published_recently() - which ought to be False.
    '''
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently return False for questions whose pub_date in in future
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question= Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question= Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question= Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

