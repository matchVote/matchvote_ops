import os
import sys
import time

import boto3

from utils import log

stack_name = sys.argv[1]
template_bucket = os.getenv('TEMPLATE_BUCKET')
master_username = os.getenv('MASTER_USERNAME')
master_password = os.getenv('MASTER_PASSWORD')

template_file = f'{stack_name}.yaml'
cloudformation = boto3.client('cloudformation')
s3 = boto3.client('s3')

with log('Uploading template to S3...'):
    s3.upload_file(
        f'cloudformation_templates/{template_file}',
        template_bucket,
        template_file)

with log('Stack creation in progress...'):
    stack_parameters = [
        {'ParameterKey': 'KeyName', 'ParameterValue': os.getenv('SSH_KEY_NAME')},
        {'ParameterKey': 'IpRangeAllowedForSSH', 'ParameterValue': os.getenv('ALLOWED_SSH_CIDR_IP')},
        {'ParameterKey': 'DBMasterUsername', 'ParameterValue': master_username},
        {'ParameterKey': 'DBMasterPassword', 'ParameterValue': master_password},
        ]
    cloudformation.create_stack(
        StackName=stack_name,
        TemplateURL=f'https://s3.amazonaws.com/{template_bucket}/{template_file}',
        Parameters=stack_parameters,
        Capabilities=['CAPABILITY_NAMED_IAM'],
        Tags=[{'Key': 'system', 'Value': stack_name}])

    stack = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]
    while stack['StackStatus'] != 'CREATE_COMPLETE':
        time.sleep(20)
        print('.', end='')
        sys.stdout.flush()
        stack = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]

print(f'\nStack {stack_name} created successfully!')
print('Now would be the time to set up the default web app DB user')
