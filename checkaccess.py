import boto3

session = boto3.Session(profile_name="default")  # or your profile name
bedrock_client = session.client(service_name="bedrock", region_name="us-west-2")

sts = boto3.client("sts")
print(sts.get_caller_identity())