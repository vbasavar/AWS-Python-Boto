#!/usr/bin/env python
import boto.ec2

region="eu-west-1"

print "For Account prod:"

key=raw_input("Enter your aws_access_key_id:")
secret=raw_input("Enter your aws_secret_access_key:")

live_keys1=set()

ec2=boto.ec2.connect_to_region(region_name=region,aws_access_key_id=key,aws_secret_access_key=secret)
reservations=ec2.get_all_instances()

for res in reservations:
        for s in res.instances:
                live_keys1.add(s.key_name)


print "For Account preprod:"

key=raw_input("Enter your aws_access_key_id:")
secret=raw_input("Enter your aws_secret_access_key:")

live_keys2=set()
ec2=boto.ec2.connect_to_region(region_name=region,aws_access_key_id=key,aws_secret_access_key=secret)

reservations=ec2.get_all_instances()

for res in reservations:
        for s in res.instances:
                live_keys2.add(s.key_name)

print "Keys common accross both are : \n", live_keys1 & live_keys2