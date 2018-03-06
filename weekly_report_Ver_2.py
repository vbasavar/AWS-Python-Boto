#!/usr/bin/python
import boto3
import boto.cloudformation
import datetime

stack_name=None
name=None

key=raw_input("Enter your aws_access_key_id:")
secret=raw_input("Enter your aws_secret_access_key:")

ec2conn = boto3.resource('ec2', aws_access_key_id=key,aws_secret_access_key=secret,region_name="eu-west-1",)
print "Ec2 instances info"
print "Instance_id | Status | Platform | Launch_time | Instance Name | Stack Name"
for i in ec2conn.instances.all():
	for tag in i.tags:
		if 'Name'in tag['Key']:
			name=tag['Value']
		if 'aws:cloudformation:stack-name' in tag['Key']:
			stack_name=tag['Value']
	print i.id,"|", i.state['Name'],"|", i.platform,"|", i.launch_time,"|", name,"|", stack_name
	stack_name=None
	name=None


cfn = boto.cloudformation.connect_to_region("eu-west-1")


#print "Cloudformation stacks info"

print "stack_name | stack_id | stack_status | creation_date | creation_time | Last update since"
for stack in cfn.describe_stacks():

	if "LastUpdatedTime" in stack.__dict__:
		t=datetime.date.today()
		lupdate=str(stack.LastUpdatedTime)[0:10]
		ldate=datetime.date(int(lupdate[0:4]), int(lupdate[5:7]), int(lupdate[8:10]))
	else:
		today=datetime.date.today()
		t=datetime.datetime(today.year,today.month,today.day)
		ldate=stack.creation_time		
	
	delta=t-ldate
	print stack.stack_name,"|", stack.stack_id,"|", stack.stack_status,"|",stack.creation_time, "|",'{:%b %d %H:%M:%S}'.format(stack.creation_time), "|", delta.days," day/s ago" 
	
	
"Rds instance info"


rds=boto3.client('rds')
response=rds.describe_db_instances()
print "DBParameterGroupName | InstanceCreateTime | Endpoint | DBInstanceArn"
for instance in response['DBInstances']:
	for db in instance['DBParameterGroups']:
		print db['DBParameterGroupName'], "|", instance['InstanceCreateTime'], "|", instance['Endpoint']['Address'], "|", instance['DBInstanceArn']
	