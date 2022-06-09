from django.test import TestCase
from MyCalendar.models import Event
from MyCalendar.serializers import EventSerializer


class EventSerializerTestCase(TestCase):
    def test_main(self):
        event_1 = Event.objects.create(name='Dinner', description='Dinner with my family',
                                       start_time='2022-12-30 17:00:00+00:00', end_time='2022-12-30 19:00:00+00:00')
        data = EventSerializer(event_1).data
        expected_data = {
            'pk': event_1.pk,
            'name': 'Dinner',
            'description': 'Dinner with my family',
            'start_time': '2022-12-30 17:00:00+00:00',
            'end_time': '2022-12-30 19:00:00+00:00'
        }
        self.assertEqual(expected_data, data)

