import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls.models import Poll


def create_poll(question, days):
    return Poll.objects.create(question=question, pub_date=timezone.now()+datetime.timedelta(days=days))

class PollViewsTests(TestCase):
    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        create_poll(question="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                response.context['latest_poll_list'],
                ['<Poll: Past poll.>']
        )

    def test_index_view_a_future_poll(self):
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        create_poll(question="Past poll.", days=-30)
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'],
                ['<Poll: Past poll.>']
        )

    def test_index_view_with_two_past_polls(self):
        create_poll(question="Past poll 1", days=-30)
        create_poll(question="Past poll 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                response.context['latest_poll_list'],
                ['<Poll: Past poll 2>', '<Poll: Past poll 1>']
        )


# Create your tests here.
