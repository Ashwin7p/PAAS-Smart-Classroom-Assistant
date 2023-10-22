import boto3
import json

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Specify the table name
table_name = 'Students'

# Load the student data from the JSON file
with open('student_data.json', 'r') as json_file:
    student_data = json.load(json_file)

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)

# Iterate through the student data and put each item into the DynamoDB table
for student in student_data:
    response = table.put_item(Item=student)
    print(f"Added student: {student['id']}")