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
        Raises a clear RuntimeError if something goes wrong with the request.
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        if system is not None:
            data["system"] = system

        try:
            response = requests.post(self.url, json=data, timeout=120)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Could not connect to Ollama. Is it running? "
                "Start it (e.g. run 'ollama serve' or open the Ollama app) and try again."
            )
        except requests.exceptions.Timeout:
            raise RuntimeError(
                f"The request to Ollama timed out. The model '{self.model}' may be too "
                "slow on this machine. Try a smaller model (e.g. llama3.2:1b)."
            )
        except requests.exceptions.HTTPError:
            raise RuntimeError(
                f"Ollama returned an error. Is the model '{self.model}' installed? "
                f"Check with 'ollama list' and pull it with 'ollama pull {self.model}'."
            )

        result = response.json()
        return result["response"]