#!/usr/bin/env python3
"""
s3_ops.py
Simple S3 operations: upload, download, list.
Supports AWS_PROFILE (env var) or --profile argument.

Usage examples:
  python s3_ops.py --profile myprofile --bucket my-bucket --upload ./local.txt --key folder/remote.txt
  python s3_ops.py --bucket my-bucket --list
  python s3_ops.py --bucket my-bucket --download folder/remote.txt --destination ./local_copy.txt
"""

import os
import argparse
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def get_session(profile_name: str | None):
    """Return a boto3 Session, honoring profile_name or AWS_PROFILE env var."""
    env_profile = os.environ.get("AWS_PROFILE")
    profile = profile_name or env_profile
    if profile:
        return boto3.Session(profile_name=profile)
    return boto3.Session()

def upload_file(session: boto3.Session, bucket: str, local_path: str, key: str):
    s3 = session.resource('s3')
    try:
        print(f"Uploading {local_path} -> s3://{bucket}/{key}")
        s3.Bucket(bucket).upload_file(local_path, key)
        print("Upload completed.")
    except FileNotFoundError:
        print(f"Local file not found: {local_path}")
    except NoCredentialsError:
        print("ERROR: No AWS credentials found.")
        raise
    except ClientError as e:
        print(f"Upload failed: {e}")
        raise

def download_file(session: boto3.Session, bucket: str, key: str, destination: str):
    s3 = session.client('s3')
    try:
        print(f"Downloading s3://{bucket}/{key} -> {destination}")
        s3.download_file(bucket, key, destination)
        print("Download completed.")
    except NoCredentialsError:
        print("ERROR: No AWS credentials found.")
        raise
    except ClientError as e:
        code = getattr(e.response, "get", lambda k, d=None: d)("Error", {}).get("Code", "")
        if code == "404":
            print("ERROR: Object not found (404).")
        else:
            print(f"Download failed: {e}")
        raise

def list_objects(session: boto3.Session, bucket: str, prefix: str | None = None):
    s3 = session.client('s3')
    try:
        paginator = s3.get_paginator('list_objects_v2')
        params = {'Bucket': bucket}
        if prefix:
            params['Prefix'] = prefix
        print(f"Listing objects in s3://{bucket}/{'' if not prefix else prefix}")
        for page in paginator.paginate(**params):
            contents = page.get('Contents', [])
            if not contents:
                continue
            for obj in contents:
                print(f" - {obj['Key']}    (Size: {obj['Size']})")
    except NoCredentialsError:
        print("ERROR: No AWS credentials found.")
        raise
    except ClientError as e:
        print(f"List failed: {e}")
        raise

def parse_args():
    p = argparse.ArgumentParser(description="Simple S3 operations.")
    p.add_argument("--profile", help="Named AWS profile to use (overrides AWS_PROFILE env var).")
    p.add_argument("--bucket", required=True, help="S3 bucket name.")
    p.add_argument("--upload", help="Local file path to upload.")
    p.add_argument("--download", help="S3 key to download.")
    p.add_argument("--destination", help="Local destination path for download (required if --download).")
    p.add_argument("--key", help="S3 key for upload (required if --upload).")
    p.add_argument("--list", action="store_true", help="List objects in bucket.")
    p.add_argument("--prefix", help="Optional prefix to filter listing.")
    return p.parse_args()

def main():
    args = parse_args()
    session = get_session(args.profile)
    # Basic sanity:
    try:
        if args.upload:
            if not args.key:
                raise SystemExit("Error: --key is required when using --upload")
            upload_file(session, args.bucket, args.upload, args.key)

        if args.download:
            if not args.destination:
                raise SystemExit("Error: --destination is required when using --download")
            download_file(session, args.bucket, args.download, args.destination)

        if args.list:
            list_objects(session, args.bucket, args.prefix)

        if not any([args.upload, args.download, args.list]):
            print("No operation specified. Use --upload, --download, or --list.")
    except NoCredentialsError:
        print("NoCredentialsError: Check your AWS credentials. Try 'aws configure' or set AWS_PROFILE.")
    except ClientError as e:
        print(f"AWS ClientError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
