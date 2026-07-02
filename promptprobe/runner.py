import json
import yaml

from promptprobe.client import OllamaClient
from promptprobe.evaluator import evaluate_injection, evaluate_leak

def load_prompts(file_path):
    """ Read a list of test prompts from a JSON file and return it. """
    with open(file_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
    return prompts


def run_tests(prompts, client):
    """Send each prompt to the model, evaluate attack prompts, and collect results."""
    results = []

    for item in prompts:
        prompt_id = item["id"]
        prompt_text = item["prompt"]
        system_prompt = item.get("system")  # None for tests without a system prompt

        print(f"Running {prompt_id} ...")

        answer = client.send_prompt(prompt_text, system=system_prompt)

        result = {
            "id": prompt_id,
            "category": item.get("category", "uncategorized"),
            "owasp": item.get("owasp", "N/A"),
            "prompt": prompt_text,
            "response": answer,
        }

        # Choose the right evaluator based on which fields the test carries.
        if "canary" in item and "injected_word" in item:
            result["verdict"] = evaluate_injection(answer, item["canary"], item["injected_word"])
        elif "secret" in item:
            result["verdict"] = evaluate_leak(answer, item["secret"])
        else:
            result["verdict"] = "N/A"

        results.append(result)

    return results

def save_results(results, file_path):
    """Write the list of results to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

    print(f"Saved {len(results)} results to {file_path}")