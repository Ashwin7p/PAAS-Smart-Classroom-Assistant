from s3Coms import S3FileManager
import pandas as pd
from io import BytesIO
import csv

output_bucket = "outputbucket-cloudcomputing2"

s3_results = S3FileManager(output_bucket)

# List all objects in the S3 bucket
bucket_objects = s3_results.list_all_objects()

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Define the CSV file name
csv_file_name = "student_data.csv"

# Check if the file exists, and if not, create it with headers
file_exists = False
try:
    with open(csv_file_name, 'a', newline='') as file:
        file_exists = True
        writer = csv.writer(file)
        writer.writerow(['file name', 'name', 'major', 'year'])
except FileNotFoundError:
    pass

# Loop through the objects in the S3 bucket
for obj in bucket_objects.get('Contents', []):
    object_key = obj['Key']
    

    # Download the CSV file from S3
    response = s3_results.get_object(object_key)
    csv_string = response['Body'].read().decode('utf-8')
    name, major, year = csv_string.split(', ')

    # Write the data to the CSV file, appending or creating as needed
    with open(csv_file_name, 'a', newline='') as file:
        writer = csv.writer(file)

        # if not file_exists:
        #     # Write the headers if the file is newly created
        #     writer.writerow(['name', 'major', 'year'])

        # Write the student data
        writer.writerow([object_key, name, major, year])
    

