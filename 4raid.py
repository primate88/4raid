import json
import click
from pathlib import Path

def filter_single_file(file_path):
    """
    Filters and transforms data from a single file.
    """
    output_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                # Assuming you have a specific filtering condition based on the data structure
                if data['posts'][0]['replies'] > 0 and (data['posts'][0]['replies'] != 1 or data['posts'][0]['com'] != "."):
                    output_data.append(data)
            except json.JSONDecodeError:
                pass
    return output_data

def process_file(file_path):
    """
    Process a single file.
    """
    output_path = f"{Path(file_path).stem}_filtered.jsonl"
    filtered_data = filter_single_file(file_path)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for data in filtered_data:
            json.dump(data, output_file)
            output_file.write('\n')

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def filter_data(file_path):
    """
    Filter the dataset.
    """
    process_file(file_path)
    click.echo(f"Dataset filtered: {file_path} -> {Path(file_path).stem}_filtered.jsonl")

if __name__ == "__main__":
    filter_data()
