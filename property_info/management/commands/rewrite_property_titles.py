from django.core.management.base import BaseCommand
from property_info.models import Property
from property_info.ollama_service import rewrite_property_title

class Command(BaseCommand):
    help = 'Rewrite property titles using Ollama'

    def handle(self, *args, **kwargs):
        properties = Property.objects.all()
        for property in properties:
            new_title = rewrite_property_title(property.title)
            if new_title:
                property.rewritten_title = new_title
                property.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully updated title for {property.title}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to rewrite title for {property.title}"))
