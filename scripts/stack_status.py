import sys

import boto3
import botocore

stack_name = sys.argv[1]
client = boto3.client('cloudformation')

try:
    stacks = client.describe_stacks(StackName=stack_name)['Stacks']
except botocore.exceptions.ClientError:
    print(f'Stack "{stack_name}" does not exist')
    sys.exit()

for stack in stacks:
    print(f'Stack {stack_name} status: {stack["StackStatus"]}')
