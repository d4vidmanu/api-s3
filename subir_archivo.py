import json
import boto3
import base64
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extrae los detalles del bucket, directorio y archivo de la solicitud
    body = json.loads(event.get("body", "{}"))
    bucket_name = body.get("bucket_name")
    directory_name = body.get("directory_name", "")
    file_name = body.get("file_name")
    file_content = body.get("file_content")
    
    if not bucket_name or not file_name or not file_content:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Bucket name, file name, and file content are required"})
        }
    
    try:
        # Decodificar el contenido del archivo de Base64 y subirlo
        file_data = base64.b64decode(file_content)
        s3.put_object(Bucket=bucket_name, Key=f"{directory_name}/{file_name}", Body=file_data)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"File '{file_name}' uploaded successfully to '{directory_name}' in bucket '{bucket_name}'"})
        }
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
