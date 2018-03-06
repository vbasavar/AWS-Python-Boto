import boto3

users_list=dict()
iam=boto3.client('iam')

users=iam.list_users(MaxItems=800)  #You can set MaxItems to the total number of users under IAM

print "Does all users listed? :", users['IsTruncated']  # If it is False, then all the users are not listed , to fix this increase MaxItems value in the above line 

for key in users['Users']:
	list_user_policies=iam.list_groups_for_user(UserName=key['UserName']) #Will fetch the policies which are from AWS IAM Groups
	policies = [ gp['GroupName'] for gp in list_user_policies['Groups']]  # Will fetch embedded user policies
	policies.append(iam.list_user_policies(UserName=key['UserName'])['PolicyNames']) # Combining both together for a user
	users_list[key['UserName']]=policies
			
for user,policies in users_list.items():
	print user, policies
