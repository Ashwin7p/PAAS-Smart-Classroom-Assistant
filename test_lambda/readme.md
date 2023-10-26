# steps to create a new docker

```bash
docker build --platform linux/amd64 -t test-hello-world:test .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 022286511304.dkr.ecr.us-east-1.amazonaws.com

aws ecr create-repository --repository-name test-hello-world --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE


```

## Now you would have a repo with a response similar to this:
```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:022286511304:repository/test-hello-world",
        "registryId": "022286511304",
        "repositoryName": "test-hello-world",
        "repositoryUri": "022286511304.dkr.ecr.us-east-1.amazonaws.com/test-hello-world",
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
docker tag test-hello-world:test 022286511304.dkr.ecr.us-east-1.amazonaws.com/test-hello-world:latest

# push
docker push 022286511304.dkr.ecr.us-east-1.amazonaws.com/test-hello-world:latest
```


### testing the function



```bash
aws lambda create-function --function-name hello-world --package-type Image --code ImageUri=022286511304.dkr.ecr.us-east-1.amazonaws.com/test-hello-world:latest --role arn:aws:iam::022286511304:role/LambdaAccess --region us-east-1 

aws lambda invoke --function-name hello-world response.json --region us-east-1```


```bash
aws configure

```