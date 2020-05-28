# Script to delete tweets every day

Leave only your high quality tweets.
Run daily with AWS Lambda.

- Tweet to be deleted
  - No RT Tweets
  - No Favorite Tweets
  - No Reply Tweets

## How to deploy
- Precondition
  - Python
  - AWS CLI
  - Twitter API Key

- Includes tweepy(External module) in package

```Powershell
pip install tweepy --target ./code
```

- Packaging

```Powershell
aws cloudformation package --s3-bucket $YourBucketName `
--template-file lambda.yml `
--output-template-file lambda-packaged.yml
```

- Deploy

```Powershell
aws cloudformation deploy `
--template-file lambda-packaged.yml `
--stack-name $YourStackName `
--parameter-overrides AccessSecret=$YourAccessSecret `
ConsumerKey=$YourConsumerKey ` 
ConsumerSecret=$YourConsumerSecret ` 
AccessKey=$YourAccessKey `
--capabilities CAPABILITY_NAMED_IAM
```