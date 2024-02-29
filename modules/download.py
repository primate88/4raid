import os
import requests
import hashlib
import tarfile
from pyzstd import decompress
import shutil
import click

default_data_url = "https://zenodo.org/records/3606810/files/pol_0616-1119_labeled.tar.zst"
default_data_md5 = "3ad65640bf590d77af0f931045aef2e0"

def download_file(url, target_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(target_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def verify_md5(file_path, expected_md5):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest() == expected_md5

def extract_tar_zst(file_path, destination):
    tar_path = file_path[:-4]  # Remove .zst extension
    with open(tar_path, 'wb') as tar_f, open(file_path, 'rb') as zst_f:
        decompressed = decompress(zst_f.read())
        tar_f.write(decompressed)

    with tarfile.open(tar_path) as tar:
        tar.extractall(path=destination)

@click.command()
@click.option('--url', default=default_data_url, help='URL to download the file from.')
@click.option('--md5', default=default_data_md5, help='MD5 checksum for the file.')
@click.option('-y', '--confirm', is_flag=True, help='Skip confirmation and download the file.')
def download_data(url, md5, confirm):
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not url:
        url = default_data_url

    file_name = os.path.join(data_dir, url.split('/')[-1])

    if os.path.exists(file_name):
        if not confirm:
            click.confirm(f'The file {file_name} already exists. Do you want to overwrite it?', abort=True)
        else:
            click.echo(f'Overwriting existing file {file_name}...')

    if not confirm:
        click.confirm(f'Do you want to download {file_name}?', abort=True)
    else:
        click.echo(f'Downloading {file_name}...')

    download_file(url, file_name)

    if md5 and verify_md5(file_name, md5):
        click.echo('MD5 checksum matches. Proceeding with extraction...')
        extract_tar_zst(file_name, data_dir)
        os.remove(file_name)
        os.remove(file_name[:-4])
        click.echo('Extraction completed.')
    elif md5:
        click.echo('MD5 checksum does not match after download. Exiting.')
        os.remove(file_name)
    else:
        click.echo('Skipping MD5 verification.')
        extract_tar_zst(file_name, data_dir)
        os.remove(file_name)
        os.remove(file_name[:-4])
        click.echo('Extraction completed.')

if __name__ == "__main__":
    download_data()
