import requests

class OllamaClient:
    """ A simple helper that sends prompts to a local Ollama model. """

    def __init__(self, model="llama3.2:3b", host="http://localhost:11434/"):
        """ Set up the client with model name and address """
        self.model = model
        self.url = f"{host}/api/generate"

    def send_prompt(self, prompt):
        """ Send a prompt to a local Ollama model and return just the answer text. """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=data)
        result = response.json()
        return result['response']