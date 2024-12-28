from django.core.management.base import BaseCommand
from django.db import connections
import requests

class Command(BaseCommand):
    help = "Rewrites property titles using the Ollama model"

    def handle(self, *args, **kwargs):
        # Fetch data from scraper_db
        with connections['scraper_db'].cursor() as cursor:
            cursor.execute("SELECT id, title FROM properties LIMIT 10;")
            properties = cursor.fetchall()

        # Call the Ollama API for each title
        rewritten_titles = []
        for prop_id, title in properties:
            prompt = f"Rewrite this property title: '{title}'"
            response = requests.post(
                "http://ollama:11434/api/generate",  # Use the Ollama container URL
                json={"model": "llama2", "prompt": prompt},
            )
            rewritten_title = response.json().get("response", "").strip()
            rewritten_titles.append((prop_id, rewritten_title))

        # Save rewritten titles into property_info_property
        with connections['default'].cursor() as cursor:
            for prop_id, rewritten_title in rewritten_titles:
                cursor.execute(
                    "INSERT INTO property_info_property (property_id, title) VALUES (%s, %s);",
                    [prop_id, rewritten_title]
                )
        self.stdout.write(self.style.SUCCESS("Rewritten titles saved successfully."))
