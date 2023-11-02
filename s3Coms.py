import boto3

aws_access_key_id = 'AKIAQKMDBFTEDZAUQCG5'
aws_secret_access_key = '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'
aws_region = 'us-east-1' 


class S3FileManager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', region_name=aws_region, 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key)

    def upload_image(self, key, image_file):
        """
        Upload an image file to S3.

        Args:
            key (str): The object key (S3 filename).
            image_file (str): The local path to the image file.
        """
        self.s3.upload_file(image_file, self.bucket_name, key)

    def upload_text(self, key, text):
        """
        Upload text content to S3.

        Args:
            key (str): The object key (S3 filename).
            text (str): The text content to upload.
        """
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=text)

    def copy_video_to_file(self, key, file_path):
        """
        Copy an image from S3 to a local file.

        Args:
            key (str): The object key (S3 filename).
            file_path (str): The local path where the image should be copied.
        """
        self.s3.download_file(self.bucket_name, key, file_path)

    def get_object(self, object_key):
        return self.s3.get_object(Bucket=self.bucket_name, Key=object_key)

    def list_all_objects(self):
        return self.s3.list_objects(Bucket=self.bucket_name)

# Example usage:
if __name__ == "__main__":
    bucket_name = "your-bucket-name"
    s3_manager = S3FileManager(bucket_name)
    
    # Upload an image to S3
    s3_manager.upload_image("image.jpg", "local_image.jpg")

    # Upload text content to S3
    s3_manager.upload_text("text.txt", "This is a text file.")

    # Copy an image from S3 to a local file
    s3_manager.copy_image_to_file("image.jpg", "downloaded_image.jpg")