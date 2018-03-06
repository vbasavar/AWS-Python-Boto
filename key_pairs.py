#!/usr/bin/env python

import boto.ec2

region="eu-west-1"

key=raw_input("Enter your aws_access_key_id:")
secret=raw_input("Enter your aws_secret_access_key:")

ec2=boto.ec2.connect_to_region(region_name=region,aws_access_key_id=key,aws_secret_access_key=secret)
live_keys=set()  ## To avoid duplicates as many instance may have a same have same key pair
unused_keys=list()

reservations=ec2.get_all_instances()

for res in reservations:
	for s in res.instances:
		live_keys.add(s.key_name)

key_pairs=ec2.get_all_key_pairs()

key_pairs_present=[ str(key_pairs[n]).replace("KeyPair:","") for n in range(len(key_pairs))]

unused_keys=[key for key in key_pairs_present if key not in live_keys]

print unused_keys


# Below will remove all the unused key pairs.

"""
for k in unused_keys:
	ec2.delete_key_pair(k)
"""
