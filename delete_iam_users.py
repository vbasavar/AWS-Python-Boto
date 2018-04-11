import boto.iam
import boto.ses
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from boto.regioninfo import RegionInfo
import sys

today = datetime.now()
conn=boto.iam.connect_to_region("eu-west-1")
s_msg=list()
count=0
groups=list()
msg1="was inactive in last 60 days. Last login was on"
msg2=""
test_users=list()
#value=""

def main():
	count=0
	users=conn.get_all_users()
	for key,values in users.items():
		 for item in values['list_users_result'].values():
				for n in item:
					if len(n) > 1:
						last_active=n.get('password_last_used', 'Never')
						if last_active is not "Never":
							password_last_used=(( today - datetime.strptime(last_active,  '%Y-%m-%dT%H:%M:%SZ')).days)
							password_last_used=int(password_last_used)
							if password_last_used > 60 :
								count = count + 1	
								msg="%s) User:%s  is inactive since 60 days. Last login was %s days ago. %s"%(count, n['user_name'], password_last_used, get_user_policies(n['user_name']))
								test_users.append(n['user_name'])
								s_msg.append(msg)
						else:	
								count = count+1
								msg="%s) User:%s was never logged into console.%s"%(count, n['user_name'], get_user_policies(n['user_name']))
								s_msg.append(msg)
								test_users.append(n['user_name'])
						
	s_msg.insert(0,"\t------USERS WHO WERE INACTIVE IN LAST 60 DAYS ARE AS BELOW. PLEASE TAKE A LOOK AND DELETE REDUNDANT USERS----- \n")
	for item in s_msg:
		print item

#	print "test_users-----\n", test_users
	print ("\nDo you Want to remove Any of the above user (Y/N)\n")
        value=raw_input()
        if value == "Y":
           print ("Please enter the USER ID")
           user_id=raw_input()
           groups=[conn.get_groups_for_user(user_id)['list_groups_for_user_response']['list_groups_for_user_result']['groups'][i]['group_name'] for i in range(len(conn.get_groups_for_user(user_id)["list_groups_for_user_response"]["list_groups_for_user_result"]["groups"]))]
	   for gp in groups:
		conn.remove_user_from_group(user_name=user_id,group_name=gp)
           if user_id in test_users:
		    ac_key=str()
		    ac_key=conn.get_all_access_keys(user_name=user_id)
		    keys=ac_key['list_access_keys_response']['list_access_keys_result']['access_key_metadata']
		    for i in range(len(keys)):
	            	key=keys[i]['access_key_id']
			print "Deleting key:", key
			conn.delete_access_key(key,user_name=user_id)
		    try:
			conn.delete_login_profile(user_id)
		    except:
			pass
	            conn.delete_user(user_id)
       		    print "User has been Removed Succesfully"
       	   else:
           	       print "Failed to remove user %s"%(user_id)

def get_user_policies(username):
	
	policies_attached=[conn.get_groups_for_user(username)["list_groups_for_user_response"]["list_groups_for_user_result"]["groups"][i]["group_name"] for i in range(len(conn.get_groups_for_user(username)["list_groups_for_user_response"]["list_groups_for_user_result"]["groups"])) ]
	policies_attached.extend(conn.get_all_user_policies(username)["list_user_policies_response"]["list_user_policies_result"]["policy_names"])

	if policies_attached:	
		return "Groups/Policies attached are:",policies_attached
	else:
		return "and no polices were attached"
			


(__name__ == '__main__' and main())
