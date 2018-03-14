from datetime import timedelta,datetime
import boto3
import sys


ec2_vols=boto3.client("ec2")
ec2_cloudwatch=boto3.client("cloudwatch")
Available_vols=list()
idle_interval=7
today = datetime.now()

def get_volumes(idle_interval):

	volumes=ec2_vols.describe_volumes()	
	suspicious_vols=[v[i]['VolumeId'] for k,v in volumes.items() if k == "Volumes" for i in range(len(v)) if v[i]['State'] == "available"]
	candidate_vols = [ vol_id for vol_id in suspicious_vols if vol_is_candidate(vol_id, idle_interval) ]
	print candidate_vols

def vol_is_candidate(vol_id, idle_interval):
    """Make sure vols has not been used past idle_interval days"""

    metrics = get_vol_metrics(vol_id, idle_interval)
    if len(metrics):
        for metric in metrics:
            # idle time is 5 minute interval aggregate so we use
            # 299 seconds to test if we're lower than that
            # if the volume had no metrics lower than 299 it's probably not
            # actually being used for anything so we can include it as
            # a candidate for deletion
 		if metrics['Datapoints']:
			if metrics['Datapoints'][len(metrics['Datapoints']-1)]['Minimum'] < 299:
				return False
    # if volume has no metrics at all, it was definitely not used
    return True

def get_vol_metrics(vol_id, idle_interval):
    """Get metrics related to vol activity"""

    stime = today + timedelta(days=1)
    gap = timedelta(days = idle_interval)
    start_date = stime - gap
    metrics = ec2_cloudwatch.get_metric_statistics(Namespace = 'AWS/EBS',
                                       MetricName = 'VolumeIdleTime',
                                       Dimensions = [{ 'Name' : 'VolumeId' , 'Value': vol_id }],
                                       Period = 3600,
                                       StartTime = start_date,
                                       EndTime = today,
                                       Statistics = [ 'Minimum' ],
                                       Unit = 'Seconds')
    return metrics

	
get_volumes(7)
