from django.db import models

class Property(models.Model):
    title = models.CharField(max_length=255)
    rewritten_title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
