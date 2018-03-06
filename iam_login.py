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
users=conn.get_all_users()

for key,values in users.items():
     for item in values['list_users_result'].values():
            for n in item:
                    if len(n) > 1:
                        #print n.get('user_name', 'Unknown_User'), n.get('password_last_used', 'Unknown_Date')
			last_active=n.get('password_last_used', 'Unknown_Date')
			if last_active is not "Unknown_Date":
				password_last_used=(( today - datetime.strptime(last_active,  '%Y-%m-%dT%H:%M:%SZ')).days)
				#print password_last_used
				password_last_used=int(password_last_used)
				if password_last_used > 60 :
					count = count + 1
					s_msg.append( str(count) +") "+n['user_name'] + ": was inactive in last 60 days. Last login was on :" + last_active + " which is " + str(password_last_used) + " days ago" )
			else:	
			 	count = count + 1	
				s_msg.append(str(count) +") "+n['user_name'] + ": Dont have password set so suggest to delete such user if not required ")

s_msg.insert(0,"User who were inactive in last 60 days are as below ")
print s_msg
						
msg = str()
for el in s_msg:
	if el != None:
		msg =  msg + el + "\n"

if len(msg) != 0:
	print (msg)
	# Send message via AWS SES
	region = RegionInfo(None, "eu-west-1", "email.eu-west-1.amazonaws.com")
	r_msg = MIMEMultipart()
	r_msg['Subject'] = "Login report from environment <env> "
	r_msg['From'] = "saltmaster@<env>.odinfra.com"
	r_msg['To'] = "<your_email>@thbs.com"
	r_msg.attach(MIMEText(msg))
	conn = boto.ses.SESConnection(region=region)
	result = conn.send_raw_email(r_msg.as_string())
else:
	sys.exit(logging.info("No garbage found. Exiting."))