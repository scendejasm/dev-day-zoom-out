# Track 1: Build Workflows

## Overview
Welcome to Track 1: Build Workflows, designed for individuals that are new to Prefect who want to create resilient and efficient workflows. Whether you're a data engineer at a professional sports team or simply exploring workflow orchestration for the first time, this track is for you!

Each example is an iteration of a data pipeline that fetches and analyzes MLB game statistics using the MLB Stats API.

## Project Contents
- `session_1_basic_workflows`: This folder contains A basic Python script that is converted into a Prefect workflow. There is an example which shows how to run this flow as a micro-service.
- `session_2_resilent_workflows`: This folder contains a series of workflows that demonstrate how to use Prefect for implementing error handling, data quality checks, and automated retries.
- `session_3_smart_workflows`: This folder contains a series of examples that demonstrate how to use idempotency and caching in Prefect.   


## Prerequisites
- Complete the instructions in the README.md file in the root of the dev-day-zoom-out directory to set up your environment.
- Sign up for an AWS account 
- Create an AWS IAM user with programmatic access, and save the access key and secret access key to a Prefect AWS credentials block.
- Create an S3 bucket in AWS, and store the bucket name in a Prefect S3 bucket block.
- Sign up for a free account at MotherDuck to get access to setup your database.
- Create a MotherDuck access token, and save it to a Prefect Secret block.

The instructions for satisfying these prerequisites are below.

## Instructions for creating AWS resources and Prefect blocks
- This guide will help you set up the necessary AWS resources and Prefect blocks for your workflow.

### How to create an AWS IAM user
1. Navigate to IAM service in AWS Console
2. Click "Users" in the left sidebar
3. Click "Create user"
4. Enter a username (e.g., "prefect-s3")
5. Select "Attach policies directly" from the Permissions options, and choose "AmazonS3FullAccess" from the Permissions policy list
6. Create the user
7. Once the user is created, click on the new user record
8. Click "Create access key"
9. From the "Access key best practices & alternatives" menu, select "Local code"
10. Click "Next"
11. Set a description tag for the access key (e.g., "Prefect S3 Access Key")
12. Click "Create access key"
13. **Important**: Save the Access Key ID and Secret Access Key - you'll need these to create a Prefect AWS credentials block

### How to create a Prefect AWS credentials block
1. Using the Python SDK:
```
from prefect_aws import AwsCredentials


AwsCredentials(
    aws_access_key_id="PLACEHOLDER",
    aws_secret_access_key="PLACEHOLDER",
    region_name="us-east-2" # replace this with your region
).save("BLOCK-NAME-PLACEHOLDER")

``` 
 
2. Using the UI:
   - Go to Blocks → + Add Block
   - Select "AWS Credentials"
   - Enter your Access Key ID and Secret Access Key
   - Enter your region
   - Name the block (e.g., "prefect-s3-credentials")
   - Click "Create"

### How to create an S3 Bucket in AWS
1. Sign in to the AWS Management Console
2. Navigate to S3 service
3. Click "Create bucket"
4. Enter a unique bucket name (e.g., "my-prefect-flows")
5. Select your desired region
6. Keep default settings for:
   - Object Ownership (ACLs disabled)
   - Block Public Access settings
   - Bucket Versioning
   - Tags
7. Click "Create bucket"

### How to create a Prefect S3 bucket block
1. Using the Python SDK:
```
from prefect_aws import S3Bucket, AwsCredentials

aws_credentials = AwsCredentials.load("NAME-OF-YOUR-AWS-CREDENTIALS-BLOCK")

S3Bucket(
    bucket_name="YOUR-S3-BUCKET-NAME",
    credentials=aws_credentials
).save("BLOCK-NAME-PLACEHOLDER")
``` 

2. Using the UI:
   - Go to Blocks → + Add Block
   - Select "S3 Bucket"
   - Enter your bucket name
   - Select your AWS credentials block
   - Name the block (e.g., "s3-bucket")
   - Click "Create"

## Instructions for creating a MotherDuck account, access token, and Prefect block
- This guide will help you set up your MotherDuck account, access token, and Prefect block.

### Create a MotherDuck account
Sign up for a free account at [MotherDuck](https://motherduck.com/).

### Create an access token
- From the MotherDuck UI, click on organization name in the top left
- Click on Settings
- Click + Create token
- Name the token (e.g., "prefect-duckdb")
- Specify that the token is for Read/Write (this should be the default)
- Choose whether you want the token to expire and then click on Create token
- Copy the access token token to your clipboard by clicking on the copy icon
- **Important**: Save the token - you'll need this to create a Prefect Secret block

### Create a Prefect Secret block to store the MotherDuck access token
1. Using the Python SDK:
```
from prefect_secrets import Secret

Secret(
    value="YOUR-MOTHERDUCK-TOKEN",
    name="motherduck-access-token"
).save("BLOCK-NAME-PLACEHOLDER")
``` 

1. Using the UI:
   - Go to Blocks → + Add Block
   - Select "Secret"
   - Enter your access token
   - Name the block (e.g., "md-access-token")
   - Click "Create"
