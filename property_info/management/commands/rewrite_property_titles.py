# this is property_info/management/commands/rewrite_property_titles.py
########################################


import requests
from django.core.management.base import BaseCommand
from property_info.models import Property  # Corrected import
from django.db import connections

class Command(BaseCommand):
    help = "Rewrite property titles using Ollama model"

    def handle(self, *args, **options):
        # Connect to the ecommerce database and fetch property titles
        with connections['ecommerce'].cursor() as cursor:
            cursor.execute("SELECT id, title FROM properties LIMIT 5")
            properties = cursor.fetchall()

        # Iterate over each property and send it to Ollama for rewriting
        for prop_id, title in properties:
            try:
                # Rewrite the title with Ollama
                rewritten_title = self.rewrite_title_with_ollama(title)
                
                # Save the rewritten title back to the property model
                property_instance = Property.objects.get(id=prop_id)
                property_instance.rewritten_title = rewritten_title
                property_instance.save()

                self.stdout.write(f"Processed property: {title} -> {rewritten_title}")
            except Property.DoesNotExist:
                self.stdout.write(f"Property with ID {prop_id} not found.")

    def rewrite_title_with_ollama(self, title):
        # Prepare the prompt for Ollama
        prompt = f"Rewrite the following property title using Phi3: {title}"

        # Make the API request to Ollama
        response = requests.post(
            "http://ollama:11434/api/generate",  # The Ollama endpoint
            json={"prompt": prompt, "model": "phi3"}  # Specify using phi3 model
        )

        # Handle the response and return the rewritten title
        if response.status_code == 200:
            return response.json().get("rewritten_title", title)
        else:
            self.stdout.write(f"Error rewriting title: {response.text}")
            return title
    
        

##########################################
# Run with:
# docker-compose exec django python manage.py rewrite_property_titles