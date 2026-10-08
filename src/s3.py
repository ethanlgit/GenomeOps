import boto3
import os

# BUCKET_NAME = "genomeops-clinvar-0801"

def download_from_s3(bucket_name: str, s3_key: str, loc_path: str):
    if os.path.exists(loc_path):
        print(f"File already exists: {loc_path}")
        return

    s3 = boto3.client("s3")
    s3.download_file(bucket_name, s3_key, loc_path)

    print(f"Success. Downloaded {s3_key} to {loc_path}")


# EXPERIMENTAL, OPTIONAL
def upload_to_s3(loc_path: str, bucket_name: str, s3_key: str):
    s3 = boto3.client("s3")
    s3.upload_file(loc_path, bucket_name, s3_key)

    print(f"Successfully uploaded {loc_path} to {bucket_name}/{s3_key}")