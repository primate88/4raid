import click
from modules.filter_data import filter_data
from modules.sample import print_sample
from modules.download import download_data

@click.group()
def cli():
    """A CLI tool for performing operations: filter, sample, download."""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def filter(file_path):
    """Filter the dataset."""
    # Since we're now dealing with a single file path argument, we pass it directly
    filter_data(file=file_path)

@cli.command()
@click.option('-R', '--random', is_flag=True, help='Print a random sample from the dataset.')
@click.option('-n', '--number', type=int, help='Number of samples to print.')
def sample(random, number):
    """Print a sample from the dataset."""
    print_sample(random=random, number=number)

@cli.command()
@click.option('--url', type=str, default=None, help='URL to download the file from.')
@click.option('--md5', type=str, default=None, help='MD5 checksum for the file.')
@click.option('-y', '--confirm', is_flag=True, default=False, help='Skip confirmation and download the file.')
def download(url, md5, yes):
    """Download the dataset."""
    download_data(url, md5, yes)

if __name__ == '__main__':
    cli()
