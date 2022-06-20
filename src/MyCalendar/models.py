from django.db import models


class Event(models.Model):
    name = models.CharField('Title', max_length=200)
    description = models.TextField('Event description', max_length=400)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    hidden = models.BooleanField('Hidden event', default=False)

    def __str__(self):
        return f"{self.name} {self.description} {self.start_time} {self.end_time} {self.hidden}"
