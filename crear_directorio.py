import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extrae el nombre del bucket y del "directorio" de la solicitud
    body = json.loads(event.get("body", "{}"))
    bucket_name = body.get("bucket_name")
    directory_name = body.get("directory_name")
    
    if not bucket_name or not directory_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Bucket name and directory name are required"})
        }
    
    try:
        # Crear un objeto "vacío" con el nombre del directorio
        s3.put_object(Bucket=bucket_name, Key=f"{directory_name}/")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Directory '{directory_name}' created in bucket '{bucket_name}'"})
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
