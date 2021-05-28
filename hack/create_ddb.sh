#!/bin/bash

set -eo pipefail

DDB_TABLE_NAME=${DDB_TABLE_NAME:-repostatus_cache}

# Create DDB table
aws dynamodb create-table --table-name $DDB_TABLE_NAME \
  --attribute-definitions AttributeName=repoSlug,AttributeType=S \
  --key-schema AttributeName=repoSlug,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Wait for the table to exist
aws dynamodb wait table-exists --table-name $DDB_TABLE_NAME

# Update table TTL
aws dynamodb update-time-to-live --table-name $DDB_TABLE_NAME \
  --time-to-live-specification Enabled=true,AttributeName=ttl
