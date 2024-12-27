import requests

def rewrite_property_title(title):
    url = "http://ollama:11434/v1/llama"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual API key
    data = {
        "input": title,
        "model": "llama-2",  # Replace with your chosen model
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('output')
    else:
        return None
