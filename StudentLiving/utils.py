import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name="secrets/production", region_name="eu-north-1"):
    """
    Retrieve a secret from AWS Secrets Manager.
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    try:
        # Retrieve the secret value
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Failed to retrieve secret: {e}")
        raise e

    # Extract and parse the secret string as JSON
    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

def get_database_settings():
    """
    Retrieve database settings from the secrets manager.
    """
    secrets = get_secret()
    return {
        "ENGINE": "django.db.backends.mysql",
        "NAME": secrets["DB_NAME"],
        "USER": secrets["DB_USER"],
        "PASSWORD": secrets["DB_PASSWORD"],
        "HOST": secrets["DB_HOST"],
        "PORT": "3306",  # Default MySQL port
    }

def get_email_settings():
    """
    Retrieve email backend settings from the secrets manager.
    """
    secrets = get_secret()
    return {
        "EMAIL_HOST_USER": secrets["EMAIL_HOST_USER"],
        "EMAIL_HOST_PASSWORD": secrets["EMAIL_HOST_PASSWORD"],
        "DEFAULT_FROM_EMAIL": secrets["DEFAULT_FROM_EMAIL"],
    }

def get_aws_settings():
    """
    Retrieve AWS storage settings from the secrets manager.
    """
    secrets = get_secret()
    return {
        "AWS_ACCESS_KEY_ID": secrets["AWS_ACCESS_KEY_ID"],
        "AWS_SECRET_ACCESS_KEY": secrets["AWS_SECRET_ACCESS_KEY"],
        "AWS_STORAGE_BUCKET_NAME": secrets["AWS_STORAGE_BUCKET_NAME"],
        "AWS_S3_REGION_NAME": secrets["AWS_S3_REGION_NAME"],
        "AWS_S3_SIGNATURE_NAME": secrets["AWS_S3_SIGNATURE_NAME"],
        "AWS_S3_FILE_OVERWRITE": secrets["AWS_S3_FILE_OVERWRITE"] == "False",  # Convert string to boolean
        "AWS_DEFAULT_ACL": secrets["AWS_DEFAULT_ACL"],
        "AWS_S3_VERIFY": secrets["AWS_S3_VERIFY"] == "True",  # Convert string to boolean
    }
