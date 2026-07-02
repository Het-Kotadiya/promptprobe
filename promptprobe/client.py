import requests

class OllamaClient:
    """A simple helper that sends prompts to a local Ollama model."""

    def __init__(self, model="llama3.2:3b"):
        """Set up the client with a server address and a model name."""
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def send_prompt(self, prompt, system=None):
        """Send one prompt to the model and return just the answer text.

        Optionally include a system prompt (hidden instructions) via `system`.
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        # Only add a system prompt if one was provided.
        if system is not None:
            data["system"] = system

        response = requests.post(self.url, json=data)
        result = response.json()
        return result["response"]