import boto3
import os

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id='AKIA4JWJQEDWJAK4NKNS',
    aws_secret_access_key='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'
)

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

for obj in s3.Bucket('gpu-script-results').objects.all():
    print(obj.key)
    # Download file and read from disc
    key=obj.key
    filepath = './models/'+key
    s3.Bucket('gpu-script-results').download_file(Key=key, Filename=filepath)



# print(os.getcwd())

# filepath = './models/'+data_key
# s3.Bucket('gpu-script-results').download_file(Key=data_key, Filename=filepath)
