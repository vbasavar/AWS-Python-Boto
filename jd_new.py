#!/usr/bin/python
import boto3
import boto.cloudformation

stack_name=None
name=None

key=raw_input("Enter your aws_access_key_id:")
secret=raw_input("Enter your aws_secret_access_key:")

ec2conn = boto3.resource('ec2', aws_access_key_id=key,aws_secret_access_key=secret,region_name="eu-west-1",)
print "Ec2 instances info"
for i in ec2conn.instances.all():
        for tag in i.tags:
                if 'Name'in tag['Key']:
                        name=tag['Value']
                if 'aws:cloudformation:stack-name' in tag['Key']:
                        stack_name=tag['Value']
        print i.id,"|", i.state['Name'],"|", i.platform,"|", i.launch_time,"|", name,"|",stack_name
        stack_name=None
        name=None
cfn = boto.cloudformation.connect_to_region("eu-west-1")


print "Cloud formation stacks info"
for stack in cfn.describe_stacks():
        print stack.stack_name,"|", stack.stack_id,"|", stack.stack_status,"|",stack.creation_time
