from django.test import TestCase
from MyCalendar.models import Event


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.event = Event.objects.create(name='Dinner', description='Dinner with my family',
                                         start_time='2022-12-30 17:00:00+00:00', end_time='2022-12-30 19:00:00+00:00',
                                         hidden_event=True)

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.event.name, str)
        self.assertIsInstance(self.event.description, str)

    def test_name_max_length(self):
        event = Event.objects.get(id=1)
        max_length = event._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_description_max_length(self):
        event = Event.objects.get(id=1)
        max_length = event._meta.get_field('description').max_length
        self.assertEquals(max_length, 400)

    def test_verbose_name(self):
        event = Event.objects.get(id=1)
        field_verbose = {
            'name': 'Title',
            'description': 'Event description',
            'start_time': 'Start time',
            'end_time': 'End time',
            'hidden_event': 'Hidden event',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    event._meta.get_field(field).verbose_name, expected_value)

    def test_object_name_presentation(self):
        event = Event.objects.get(id=1)
        expected_object_name = f"{event.name} {event.description} {event.start_time} " \
                               f"{event.end_time} {event.hidden_event}"
        self.assertEquals(expected_object_name, str(self.event))