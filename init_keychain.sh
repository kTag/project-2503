#!/bin/bash

# Name of the Keychain item
KEYCHAIN_ITEM1="consumer_key"
KEYCHAIN_ITEM2="consumer_secret"
KEYCHAIN_ITEM3="access_token"
KEYCHAIN_ITEM4="access_token_secret"
# Name of the environment variable to set
ENV_VAR_NAME1="TWITTER_CONSUMER_KEY"
ENV_VAR_NAME2="TWITTER_CONSUMER_SECRET"
ENV_VAR_NAME3="TWITTER_ACCESS_TOKEN"
ENV_VAR_NAME4="TWITTER_ACCESS_TOKEN_SECRET"
# Retrieve the password from Keychain
PASSWORD1=$(security find-generic-password -w -s "$KEYCHAIN_ITEM1")


# Check if the password was successfully retrieved
if [ $? -eq 0 ]; then
    # Set the environment variable
    export $ENV_VAR_NAME1="$PASSWORD1"
    echo "Password successfully retrieved and set to $ENV_VAR_NAME1"
else
    echo "Failed to retrieve password1 from Keychain"
    exit 1
fi

PASSWORD2=$(security find-generic-password -w -s "$KEYCHAIN_ITEM2")
if [ $? -eq 0 ]; then
    # Set the environment variable
    export $ENV_VAR_NAME2="$PASSWORD2"
    echo "Password successfully retrieved and set to $ENV_VAR_NAME2"
else
    echo "Failed to retrieve password2 from Keychain"
    exit 1
fi
PASSWORD3=$(security find-generic-password -w -s "$KEYCHAIN_ITEM3")

if [ $? -eq 0 ]; then
    # Set the environment variable
    export $ENV_VAR_NAME3="$PASSWORD3"
    echo "Password successfully retrieved and set to $ENV_VAR_NAME3"
else
    echo "Failed to retrieve password3 from Keychain"
    exit 1
fi

PASSWORD4=$(security find-generic-password -w -s "$KEYCHAIN_ITEM4")

if [ $? -eq 0 ]; then
    # Set the environment variable
    export $ENV_VAR_NAME4="$PASSWORD4"
    echo "Password successfully retrieved and set to $ENV_VAR_NAME4"
else
    echo "Failed to retrieve password4 from Keychain"
    exit 1
fi
