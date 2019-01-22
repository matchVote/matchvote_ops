#!/bin/bash

REGION=us-east-1
APP=$1
VERSION=$2

if [ -z "$APP" ]; then
  echo "App name missing"
  exit 1
elif [ -z "$VERSION" ]; then
  echo "Version argument missing"
  exit 1
fi

SOURCE_IMAGE=$APP:$VERSION
TARGET_IMAGE=788332838494.dkr.ecr.$REGION.amazonaws.com/$SOURCE_IMAGE

# Login to AWS EC2 Container Registry
$(aws --profile mv ecr get-login --no-include-email)

echo "Building image..."
docker build -t $SOURCE_IMAGE ../$APP
docker tag $SOURCE_IMAGE $TARGET_IMAGE

echo "Pushing image..."
docker push $TARGET_IMAGE

echo "Deployment successful"
