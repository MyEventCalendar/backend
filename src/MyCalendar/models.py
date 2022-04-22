from django.db import models


class Event(models.Model):
    name = models.CharField('Title', max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    deleted_event = models.BooleanField("deleted", default=False)

    def __str__(self):
        return self.name + " " + self.description, self.end_time, self.end_time
