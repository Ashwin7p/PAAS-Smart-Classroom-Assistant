import boto3
import face_recognition
import pickle
import os
from face_recognition_util import FaceEncodingsLoader

from s3Coms import S3FileManager





# s3 = boto3_client('s3')
dynamodb = boto3.resource('dynamodb')


input_bucket = "inputbucket-cloudcomputing2"
output_bucket = "outputbucket-cloudcomputing2"


s3_input = S3FileManager(input_bucket)
s3_results = S3FileManager(output_bucket)



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
	s3_event = event['Records'][0]['s3']
	object_key = s3_event['object']['key']

	downloaded_video_path = "/tmp/"
	folder_path = downloaded_video_path.split(".")[0]
	s3_input.S3FileManager(object_key, downloaded_video_path)
	save_frames(downloaded_video_path,folder_path)


	
	# unknown face

	encoding_file = "encoding"  # Replace with the path to your encoding file
	encodings_loader = FaceEncodingsLoader(encoding_file)
    
	# Get the loaded encodings
	loaded_encodings = encodings_loader.get_encodings()


		# List all files in the folder
	files = os.listdir(folder_path)

	results = "unknown face"

	# Process each file one by one
	for file in files:
		file_path = os.path.join(folder_path, file)

		# Check if the item is a file (not a subdirectory)
		if os.path.isfile(file_path):
			print(f"Processing file: {file_path}")

		results  = encodings_loader.find_best_match(loaded_encodings["encoding"],file_path,loaded_encodings["name"])
		if results !=  "unknown face":
			break


	
	aws_region = 'us-east-1'  # Replace with your desired AWS region
	# DynamoDB resource
	dynamodb = boto3.resource('dynamodb', 
							region_name=aws_region)

	table_name = 'Students'

	# Specify the column name and the value you want to filter on
	column_name = 'name'
	filter_value = results

	# Retrieve data from DynamoDB where "name" equals "president_obama"
	table = dynamodb.Table(table_name)

	response = table.scan(
		FilterExpression=boto3.dynamodb.conditions.Attr(column_name).eq(filter_value)
	)

	final_string = f'{filter_value}, {response["major"]}, {response["year"]}'

	s3_results.upload_text(object_key,final_string)


	print(results)



	# Create a DynamoDB table resource
	table = dynamodb.Table(table_name)


	# Copy the image from S3 to a local file


	# Search DynamoDB for the record using the filename (object_key)
	response = table.get_item(
		Key={
			'filename': object_key
		}
	)

	if 'Item' in response:
		# If the record is found, return it
		item = response['Item']
		return {
			'statusCode': 200,
			'body': json.dumps(item)
		}
	else:
		# If the record is not found, you can return an appropriate response
		return {
			'statusCode': 404,
			'body': json.dumps('Record not found')
		}


# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):	
	print("Processing video file...")

	# Ensure the input and output buckets exist
	if not s3.head_bucket(Bucket=input_bucket) or not s3.head_bucket(Bucket=output_bucket):
		print("Input or output bucket does not exist.")
		return

	# Get the name of the input video file from the event
	input_key = event['Records'][0]['s3']['object']['key']

	# Generate the output video file key
	output_key = os.path.join('output', os.path.basename(input_key))
	# video path
	# download
	# convert from video to frames, save frames in local
	# for each frame run face recognition: break if face
	# pull data from dynamo for that face 
	# put data into csv 
	# delete local video/frames

	# Download the input video file from the input S3 bucket
	s3.download_file(input_bucket, input_key, '/tmp/input_video.mp4')

	# Load face encodings (assuming you have a file named 'encodings.pickle')
	face_encodings = open_encoding('/tmp/encoding.pickle')

	

	# Load the input video

	input_video = face_recognition.load_image_file('/tmp/input_video.mp4')

	# Perform face recognition on the input video (replace this with your face recognition logic)
	# results = perform_face_recognition(input_video, face_encodings)

	# Process the video and save the results (replace this with your processing logic)
	# processed_video = process_video(input_video, results)

	# Save the processed video to a file
	# face_recognition.api.batch_save_faces('/tmp/processed_video.mp4', processed_video)

	# Upload the processed video to the output S3 bucket
	s3.upload_file('/tmp/processed_video.mp4', output_bucket, output_key)

	print(f"Processed video saved to {output_bucket}/{output_key}")

	# Clean up temporary files
	os.remove('/tmp/input_video.mp4')
	# os.remove('/tmp/processed_video.mp4')

	print("Processing complete.")


    


    