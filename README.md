# Serverless Neural Network for Image Classification - Demo

## Pre-Requisites
1. This demo uses the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html). If the AWS CLI isn't installed,  follow [these](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) instructions. The CLI [configuration](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) needs `PowerUserAccess` and `IAMFullAccess` [IAM policies](http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) associated. To verify that the AWS CLI is installed and up to date, run the following:
```console
    $ aws --version
```
2. Clone the repo.
```console
    $ git clone https://github.com/darkreapyre/itsacat
``` 

## Deployment

```shell
    Enter the AWS Region to use > "AWS REGION"
    Enter the S3 bucket to create > "UNIQUE S3 BUCKET"
    Enter the name of the Stack to deploy > "UNIQUE STACK NAME"
    Enter the e-mail address to send training update > "E-MAIL ADDRESS"
```

```shell
    "Successfully created/updated stack - <Stack Name>"
```

**Confirm Subscription**

## Integration with SakeMaker Notebook Instance

1. Create notebook instance
2. Notebook instance settings
    - Notebook instance name
    - Notebook instance type -> ml.t2.medium
    - IAM Role -> Create new role
    - Specific S3 Bucket -> "UNIQUE BUCKET NAME" -> Create Role
    - VPC -> "UNIQUE STACK NAME"
    - Subnet -> "Private subnet"
    - Security group(s) -> HostSecurityGroup
    - Create notebook instance
3. Status -> Pending
4. Configure Service Access role
    - IAM -> Role -> "AmazonSageMaker-ExecutionRole-..."
    - Policy name -> "AmazonSageMaker-ExecutionPolicy-..." -> Edit policy
    - Visual editor tab -> Add additional permissions
        - Service -> Choose a service -> ElastiCache
        - Action -> Select and action -> All ElastiCache actions (elasticache:*) 
        - Review Policy
        - Save changes
    - The final Policy should look similar to this:
    ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:DeleteObject"
                    ],
                    "Resource": "arn:aws:s3:::*"
                },
                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": "elasticache:*",
                    "Resource": "*"
                }
            ]
        }
    ```
5. Actions -> Open
6. Configure Libraries
    - Conda -> Conda environments -> python3
    - Available packages -> Search -> "redis"
        - redis
        - redis-py
    - "Right Arrow" -> Install ??(pop-up)??
7. Download Code
    - Files Tab -> New -> Terminal
    - ```shell
        $ cd SageMaker
        $ git clone https://github.com/darkreapyre/itsacat
        $ exit
    ```
    - Files -> itsacat -> Codebooks -> Codebook.ipynb


## Codebook Overview


>**Note:** Good idea to close the SageMaker Notebook instance until training is complete by openning the SageMaker console -> Noetbook instances -> Select the instance Name -> Actions -> Stop.

## Training the Classifier

- Sample e-mail:
```text
    Training update!
    Cost after epoch 0 = 0.7012303687667679
```

## Analyzing the Results

## Troubleshooting

```python
    list index out of range: IndexError
    Traceback (most recent call last):
    File "/var/task/trainer.py", line 484, in lambda_handler
    A = vectorizer(Outputs='a', Layer=layer-1)
    File "/var/task/trainer.py", line 235, in vectorizer
    key_list.append(result[0])
    IndexError: list index out of range
```

## Cleanup