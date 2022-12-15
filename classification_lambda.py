import json
import base64
#from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2022-12-15-11-03-18-834' ## TODO: fill in
import boto3



def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']["image_data"])
    bucket = event['body']["s3_bucket"]
    key = event['body']["s3_key"]
    

    runtime= boto3.client('runtime.sagemaker')
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,
                                           ContentType='image/png',
                                           Body=image)
        
    # Make a prediction:
    predictions = json.loads(response['Body'].read().decode()) ## TODO: fill in
    #print(predictions)
    
    # We return the data back to the Step Function    
    event["inferences"] = predictions
    print(event)
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['body']["image_data"],
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": predictions
        }
    }