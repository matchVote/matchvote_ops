import sys
import time

import boto3
from botocore.exceptions import ClientError

from utils import log


def describe_stack(stack_name):
    try:
        return cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]
    except ClientError:
        return {}


def delete_repo_images():
    try:
        ecr.batch_delete_image(
            repositoryName='matchvote',
            imageIds=[{'imageTag': 'latest'}])
    except Exception:
        pass


if __name__ == '__main__':
    stack_name = sys.argv[1]
    cloudformation = boto3.client('cloudformation')
    ecr = boto3.client('ecr')

    with log('Deleting repository images...'):
        delete_repo_images()

    with log('Deleting stack...'):
        cloudformation.delete_stack(StackName=stack_name)

        stack = describe_stack(stack_name)
        while stack.get('StackStatus') == 'DELETE_IN_PROGRESS':
            time.sleep(20)
            print('.', end='')
            sys.stdout.flush()
            stack = describe_stack(stack_name)

    print(f'\nStack {stack_name} deleted successfully!')
