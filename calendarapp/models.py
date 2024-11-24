from django.db import models

class CalendarEvent(models.Model):
    date = models.DateField();
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__ (self):
        return f"Event on {self.date}: {self.description}"
