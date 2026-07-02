import json
import yaml

def load_prompts(file_path):
    """ Read a list of test prompts from a JSON file and return it. """
    with open(file_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
    return prompts


def run_test(prompts, client):
    """ Send each prompt to the model and collect all the results."""

    results = []

    for item in prompts:
        prompt_id = item['id']
        prompt_text = item['prompt']

        print(f"Running {prompt_id} ...")

        answer = client.send_prompt(prompt_text)

        results.append({
            "id": prompt_id,
            "prompt": prompt_text,
            "response": answer
        })

    return results


def save_results(results, file_path):
    """Write the list of results to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

    print(f"Saved {len(results)} results to {file_path}")