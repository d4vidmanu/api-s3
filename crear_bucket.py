import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extrae el nombre del bucket de la solicitud (suponiendo que el nombre se pasa en el cuerpo de la solicitud)
    body = json.loads(event.get("body", "{}"))
    bucket_name = body.get("bucket_name")
    
    if not bucket_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Bucket name is required"})
        }
    
    try:
        # Crear el bucket
        s3.create_bucket(Bucket=bucket_name)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Bucket '{bucket_name}' created successfully"})
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
