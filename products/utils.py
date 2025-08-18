import boto3 
from botocore.exceptions import NoCredentialsError
from decouple import config


s3 = boto3.client(
    's3',
    aws_access_key_id='AKIARDAYYYYNYSLU67PQ',
    aws_secret_access_key='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',
    region_name='eu-north-1'
)

def upload_image_to_s3(image_file, image_name):
    try:
        content_type = getattr(image_file, 'content_type', 'image/jpeg')
        encoded_image_name = image_name

        s3.upload_fileobj(
            image_file,
            'backendbt',
            encoded_image_name,
            ExtraArgs={'ContentType': content_type},
        )

        return f"https://{config('AWS_STORAGE_BUCKET_NAME')}.s3.{config('AWS_S3_REGION_NAME')}.amazonaws.com/{image_name}"
        
    except NoCredentialsError:
        print('No AWS Credentials found')
        return None
    except Exception as e:
        print(f'S3 upload error: {e}')
        return None
