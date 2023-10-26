# steps to create a new docker

```bash
docker build --platform linux/amd64 -t video-image-fixed:test .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 022286511304.dkr.ecr.us-east-1.amazonaws.com

aws ecr create-repository --repository-name video-image-fixed --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE


```

## Now you would have a repo with a response similar to this:
```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:022286511304:repository/video-image-fixed",
        "registryId": "022286511304",
        "repositoryName": "video-image-fixed",
        "repositoryUri": "022286511304.dkr.ecr.us-east-1.amazonaws.com/video-image-fixed",
        "createdAt": "2023-10-25T21:01:23-07:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

- next tag and push the image

```bash
docker tag video-image-fixed:test 022286511304.dkr.ecr.us-east-1.amazonaws.com/video-image-fixed:latest

# push
docker push 022286511304.dkr.ecr.us-east-1.amazonaws.com/video-image-fixed:latest
```


### testing the function

```bash

aws lambda create-function --function-name video-proc-fixed --package-type Image --code ImageUri=022286511304.dkr.ecr.us-east-1.amazonaws.com/video-processing-image:latest --role arn:aws:iam::022286511304:role/LambdaAccess --region us-east-1 

aws s3api put-bucket-notification-configuration --bucket inputbucket-cloudcomputing2 --notification-configuration "{\"LambdaFunctionConfigurations\":[{\"LambdaFunctionArn\":\"arn:aws:lambda:us-east-1:022286511304:function:video-proc-fixed\",\"Events\":[\"s3:ObjectCreated:*\"]}]}"


aws lambda invoke --function-name hello-world response.json --region us-east-1


aws configure
# upload: .\test_7.mp4 to s3://inputbucket-cloudcomputing2/test_7.mp4

aws s3 cp test_2.mp4 s3://inputbucket-cloudcomputing2/

```