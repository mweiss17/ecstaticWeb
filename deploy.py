import boto, boto.utils, time, datetime, os
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup


#Create an Image of the current server
instance_id = boto.utils.get_instance_metadata()['instance-id']
timestamp = time.time()
value = datetime.datetime.fromtimestamp(timestamp)
humanreadabledate = value.strftime('%Y-%m-%d_%H.%M.%S')
name = 'productionImage'+humanreadabledate
print name
conn = boto.connect_ec2()
img = conn.create_image(instance_id, name, description=None, no_reboot=False, block_device_mapping=None, dry_run=False)

#Create a new Autoscaling Group
conn = AutoScaleConnection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
autoscale = boto.ec2.autoscale.connect_to_region('us-east-1')
print conn.get_all_groups()
timestamp = time.time()
value = datetime.datetime.fromtimestamp(timestamp)
humanreadabledate = value.strftime('%Y-%m-%d_%H.%M.%S')
name = 'live_launch_config'+humanreadabledate
lc = LaunchConfiguration(name=name, image_id=img,
                             key_name='SDSEastKey',
                             security_groups=['sg-a7afb1c2'])
conn.create_launch_configuration(lc)

