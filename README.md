# DynamoDB CLI 
![Workflow](https://github.com/dotnetmentor/dynamocli/actions/workflows/ci.yml/badge.svg)
![Coverage Badge](https://github.com/dotnetmentor/dynamocli/blob/main/coverage.svg)


## Introduction
A simple lightweight command line interface for interacting with an Amazon DynamoDB instance. 

Mainly intended to work with a local instance, since current tools often struggles to work with a larger local database, but also works with AWS hosted instances.


## Setup
In order to set up your connection you may use the command
> dynamocli set-config

or edit the configuration file directly. The file is located in the user configuration folder  
  - *~/Library/Application Support/dynamocli* for Mac OS
  - *~/.local/share/dynamocli* for linux

The required configurations are

 - Authentication - Supports three different options
   - local - Connect to local dynamoDB
   - env - Connect to AWS instance using environment values
   - credentials - Connect to AWS instance using .credentials file
 - TableName - Name of the table in the database
 - Port - Port of the instance, only required if Authentication = local
 - Profile - AWS profile to use. Only required if Authentication = credentials
 - Region - AWS region for the instance. Not needed if Authentication = local

## Usage

`dynamocli [-h] [--index INDEX] [--pk PK] [--sk SK] {describe,query,get-config,set-config}`

>`positional arguments:`
>>  `{describe,query,get-config,set-config}`

>`optional arguments:`
>>`  -h, --help            show this help message and exit`
>>`  --verbose, -v         increase output verbosity`
>>`  --index INDEX, -i INDEX  apecify name of index to use. Omit "pk"` 
>>`  --pk PK               partition key value of the index to query`
>> ` --sk SK              sort key value. Defaults to --pk`
