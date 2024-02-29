import click
from filter import perform_filtering
from sample import perform_sampling
from download import perform_downloading

@click.group()
def cli():
    """A CLI tool for performing operations: filter, sample, download."""
    pass

@cli.command()
def filter():
    """Filter the dataset."""
    perform_filtering()

@cli.command()
@click.option('-R', '--random', is_flag=True, help='Print a random sample from the dataset.')
@click.option('-n', '--number', type=int, help='Number of samples to print.')
def sample(random, number):
    """Print a sample from the dataset."""
    perform_sampling(random=random, number=number)

@cli.command()
@click.option('--url', default="https://zenodo.org/records/3606810/files/pol_0616-1119_labeled.tar.zst", help='URL to download the file from.')
@click.option('--md5', default="3ad65640bf590d77af0f931045aef2e0", help='MD5 checksum for the file.')
def download(md5, url):
    """Download the dataset."""
    perform_downloading(md5=md5, url=url)

if __name__ == '__main__':
    cli()
