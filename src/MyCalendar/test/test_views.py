from django.test import TestCase, Client
from MyCalendar.models import Event


class EventListViewTest(TestCase):
    def test_get_events(self):
        resp = self.client.get('/events')
        self.assertEqual(resp.status_code, 200)

    def test_add_new_event(self):
        resp = self.client.post('/events', {
            'name': 'event',
            'description': 'event',
            'start_time': '2022-12-30 17:00:00+00:00',
            'end_time': '2022-12-30 19:00:00+00:00'
        })
        self.assertEqual(resp.status_code, 200)

    def test_change_event(self):
        Event.objects.create(pk='7', name='Dinner', description='Dinner with my family',
                             start_time='2022-12-30 17:00:00+00:00', end_time='2022-12-30 19:00:00+00:00',
                             hidden_event=True)
        resp = self.client.put('/events/7', {'name': 'event2'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_delete_event(self):
        Event.objects.create(pk='5', name='Dinner', description='Dinner with my family',
                             start_time='2022-12-30 17:00:00+00:00', end_time='2022-12-30 19:00:00+00:00',
                             hidden_event=True)
        resp = self.client.delete('/events/5')
        self.assertEqual(resp.status_code, 200)


