#!/usr/bin/env python3

import argparse
import subprocess
import requests
import json
import sys
import os
import requests
import uuid
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed, wait_exponential
import urllib3
import urllib3.exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://kf-key-manager.kf-strides.org'
file_url = 'https://data.kidsfirstdrc.org/user/data/download'
drs_url = 'https://data.kidsfirstdrc.org/ga4gh/drs/v1/objects'

def main():
    parser = argparse.ArgumentParser(description='Download a file from GMKF from AWS.')
    parser.add_argument('--token')
    parser.add_argument('--fileid')
    parser.add_argument('--outputdir')
    args = parser.parse_args()
    if len(sys.argv) < 6:
        parser.print_help()
    if args.token and args.fileid:
        # get the access token
        access_token = get_access_token(args.token)
        # get the signed URL
        signed_url = get_signed_url(args.fileid, access_token)
        # get the filename
        filename = get_filename(args.fileid)
        # now download the file with retries
        download_file(url=signed_url, path=args.outputdir+"/"+filename)

def download_file(outputdir, signed_url):
    print("downloading file")

# TODO: it's not clear if I should call this for each file or if I should
# try to cache the access token for a certain amount of time...
def get_access_token(token):
    print("getting access token")
    headers = {
        'authorization': 'Bearer ' + token,
        'authority': 'kf-key-manager.kf-strides.org',
        'content-length': '0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'origin': 'https://portal.kidsfirstdrc.org',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://portal.kidsfirstdrc.org/',
        'accept-language': 'en-US,en;q=0.9'
    }
    r = requests.post(url+'/refresh?fence=gen3', headers=headers, verify=False, data={})
    json_response = r.json()
    return(json_response['access_token'])

def get_signed_url(fileid, access_token):
    print("getting signed URL")
    headers = {
        'connection': 'keep-alive',
        'accept': '*/*',
        'authorization': 'Bearer ' + access_token,
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'origin': 'https://portal.kidsfirstdrc.org',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://portal.kidsfirstdrc.org/',
        'accept-language': 'en-US,en;q=0.9'
    }
    r = requests.get(file_url+'/'+fileid, headers=headers, verify=False)
    json_response = r.json()
    return(json_response['url'])

def get_filename(fileid):
    print("getting filename from DRS server")
    r = requests.get(drs_url+'/'+fileid, headers={}, verify=False)
    json_response = r.json()
    return(json_response['name'])

# taken from excellent blog post here: https://alexwlchan.net/2020/04/downloading-files-with-python/
# see https://tenacity.readthedocs.io/en/latest/ for docs on the retry
@retry(
    retry=(
        retry_if_exception_type(httpx.HTTPError) |
        retry_if_exception_type(urllib3.exceptions.HTTPError)
    ),
    stop=stop_after_attempt(10),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
def download_file(*, url, path, client=None):
    """
    Atomically download a file from ``url`` to ``path``.

    If ``path`` already exists, the file will not be downloaded again.
    This means that different URLs should be saved to different paths.

    This function is meant to be used in cases where the contents of ``url``
    is immutable -- calling it more than once should always return the same bytes.

    Returns the download path.

    """
    # If the URL has already been downloaded, we can skip downloading it again.
    if os.path.exists(path):
        return path

    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    if client is None:
        client = httpx.Client()

    try:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()

            # Download to a temporary path first.  That way, we only get
            # something at the destination path if the download is successful.
            #
            # We download to a path in the same directory so we can do an
            # atomic ``os.rename()`` later -- atomic renames don't work
            # across filesystem boundaries.
            tmp_path = f"{path}.{uuid.uuid4()}.tmp"

            with open(tmp_path, "wb") as out_file:
                for chunk in resp.iter_raw():
                    out_file.write(chunk)

    # If something goes wrong, it will probably be retried by tenacity.
    # Log the exception in case a programming bug has been introduced in
    # the ``try`` block or there's a persistent error.
    except Exception as exc:
        print(exc, file=sys.stderr)
        raise

    os.rename(tmp_path, path)
    return path

if __name__ == '__main__':
    main()
