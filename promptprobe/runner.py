import json
import yaml

from promptprobe.client import OllamaClient
from promptprobe.evaluator import evaluate_injection

def load_prompts(file_path):
    """ Read a list of test prompts from a JSON file and return it. """
    with open(file_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
    return prompts


def run_tests(prompts, client):
    """Send each prompt to the model, evaluate attack prompts, and collect results."""

    results = []

    for item in prompts:
        prompt_id = item['id']
        prompt_text = item['prompt']

        print(f"Running {prompt_id} ...")

        answer = client.send_prompt(prompt_text)

        # Start building this result
        result = {
            "id": prompt_id,
            "category": item.get("category", "uncategorized"),
            "owasp": item.get("owasp", "N/A"),
            "prompt": prompt_text,
            "response": answer,
        }

        # Only attack prompts have a canary + injected_word to judge.
        if "canary" in item and "injected_word" in item:
            verdict = evaluate_injection(answer, item["canary"], item["injected_word"])
            result["verdict"] = verdict
        else:
            result["verdict"] = "N/A"

        results.append(result)

    return results


def save_results(results, file_path):
    """Write the list of results to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

    print(f"Saved {len(results)} results to {file_path}")