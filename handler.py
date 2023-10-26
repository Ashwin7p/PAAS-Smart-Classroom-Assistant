import boto3
import face_recognition
import pickle
import os
from face_recognition_util import FaceEncodingsLoader
import json

from s3Coms import S3FileManager

import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.INFO)



# s3 = boto3_client('s3')
# dynamodb = boto3.resource('dynamodb')


input_bucket = "inputbucket-cloudcomputing2"
output_bucket = "outputbucket-cloudcomputing2"


s3_input = S3FileManager(input_bucket)
s3_results = S3FileManager(output_bucket)

aws_access_key_id = 'AKIAQKMDBFTEDZAUQCG5'
aws_secret_access_key = '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'
aws_region = 'us-east-1' 

def save_frames(video_file_path, folder_name):
    # Check if the folder exists, and if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Generate the output image file names
    output_pattern = os.path.join(folder_name, "image-%3d.jpeg")

    # Use subprocess to run the ffmpeg command
    cmd = f"ffmpeg -i {video_file_path} -r 1 {output_pattern}"
    os.system(cmd)



def lambda_handler(event, context):
	# Get the S3 bucket and object information from the S3 event
	logger.info('## Function triggered')
	s3_event = event['Records'][0]['s3']
	object_key = s3_event['object']['key']

	downloaded_video_path = "/tmp/"
	video_file_path = downloaded_video_path+object_key
	folder_path = video_file_path.split(".")[0]
	s3_input.copy_video_to_file(object_key, video_file_path)
	logger.info(f'video {object_key} downloaded at {video_file_path}')
	logger.info(f"save_frames({video_file_path},{folder_path})")
	save_frames(video_file_path,folder_path)


	
	# unknown face

	encoding_file = "encoding"  # Replace with the path to your encoding file
	encodings_loader = FaceEncodingsLoader(encoding_file)
    
	# Get the loaded encodings
	loaded_encodings = encodings_loader.get_encodings()
	logger.info(f'encodings loaded')


		# List all files in the folder
	files = os.listdir(folder_path)

	results = "unknown face"

	# Process each file one by one
	for file in files:
		file_path = os.path.join(folder_path, file)

		# Check if the item is a file (not a subdirectory)
		if os.path.isfile(file_path):
			logger.info(f"Processing file: {file_path}")

			# print(f"Processing file: {file_path}")

		results  = encodings_loader.find_best_match(loaded_encodings["encoding"],file_path,loaded_encodings["name"])
		if results !=  "unknown face":
			break


	logger.info(f"found result: {results}")
	# aws_region = 'us-east-1'  # Replace with your desired AWS region
	# DynamoDB resource
	dynamodb = boto3.resource('dynamodb', 
							region_name=aws_region,
							aws_access_key_id=aws_access_key_id, 
                            aws_secret_access_key=aws_secret_access_key)

	table_name = 'Students'

	# Specify the column name and the value you want to filter on
	column_name = 'name'
	filter_value = results

	# Retrieve data from DynamoDB where "name" equals "president_obama"
	table = dynamodb.Table(table_name)

	dynamo_response = table.scan(
		FilterExpression=boto3.dynamodb.conditions.Attr(column_name).eq(filter_value)
	)

	response = dynamo_response["Items"][0]

	logger.info(f" response from dynamo {response}")
	final_string = f'{filter_value}, {response["major"]}, {response["year"]}'
	logger.info(f"final string generated: {final_string}")
	s3_results.upload_text(object_key.split(".")[0],final_string)


	print(results)



	# Create a DynamoDB table resource
	# table = dynamodb.Table(table_name)


	# Copy the image from S3 to a local file


	# Search DynamoDB for the record using the filename (object_key)
	# response = table.get_item(
	# 	Key={
	# 		'string': final_string
	# 	}
	# )

	return {
			'statusCode': 200,
			'body': json.dumps(final_string)
		}


event = {
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:*",
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "bcca404d-cb99-48f8-a05d-696eacf53c5b",
        "bucket": {
          "name": "inputbucket-cloudcomputing2",
          "ownerIdentity": {
            "principalId": "022286511304"
          },
          "arn": "arn:aws:s3:::inputbucket-cloudcomputing2"
        },
        "object": {
          "key": "test_0.mp4",
          "size": 322560,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}

lambda_handler(event,"asdasda")