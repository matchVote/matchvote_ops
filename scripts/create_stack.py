import os
import sys
import time

import boto3
import yaml

from utils import log

if __name__ == '__main__':
    stack_name = sys.argv[1]
    template_bucket = os.getenv('TEMPLATE_BUCKET')
    template_file = f'{stack_name}.yaml'
    stack_parameters = []
    with open(f'config/{stack_name}-parameters.yaml') as f:
        for key, value in yaml.load(f.read())['params'].items():
            param = {'ParameterKey': key, 'ParameterValue': str(value)}
            stack_parameters.append(param)

    cloudformation = boto3.client('cloudformation')
    s3 = boto3.client('s3')

    with log('Uploading template to S3...'):
        s3.upload_file(
            f'cloudformation_templates/{template_file}',
            template_bucket,
            template_file)

    with log('Stack creation in progress...'):
        cloudformation.create_stack(
            StackName=stack_name,
            TemplateURL=f'https://s3.amazonaws.com/{template_bucket}/{template_file}',
            Parameters=stack_parameters,
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Tags=[{'Key': 'system', 'Value': stack_name}])

        stack = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]
        while stack['StackStatus'] == 'CREATE_IN_PROGRESS':
            time.sleep(20)
            print('.', end='')
            sys.stdout.flush()
            stack = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]

    print(f'\nStack {stack_name} created successfully!')
