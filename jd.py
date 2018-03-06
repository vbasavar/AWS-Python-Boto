import boto3
import boto


ec2=boto3.resources("ec2")
for i in ec2.instances.all():
	for tag in i.tags:
		if 'Name'in tag['Key']:
			name=tag['Value']
		if 'aws:cloudformation:stack-name' tag['Key']:
			stack_name=tag['Value']
	print i.id, i.state['Name'], i.platform, i.launch_time, name,stack_name

cfn = boto.cloudformation.connect_to_region("eu-west-1")

for stack in cfn.describe_stacks():
	print stack.stack_name, stack.stack_id, stack.stack_status,stack.creation_time,stack.LastUpdatedTime
	