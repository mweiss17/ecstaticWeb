import boto, boto.utils, time, datetime, os
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup

#Create an Image of the current server
def create_image():
    instance_id = boto.utils.get_instance_metadata()['instance-id']
    timestamp = time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    humanreadabledate = value.strftime('%Y-%m-%d_%H.%M.%S')
    image_name = 'productionImage'+humanreadabledate
    conn = boto.connect_ec2()
    img = conn.create_image(instance_id, name, description=None, no_reboot=False, block_device_mapping=None, dry_run=False)

#Create a new Autoscaling Configuration
def create_autoscaling_conf():
    conn = AutoScaleConnection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
    autoscale = boto.ec2.autoscale.connect_to_region('us-east-1')
    print conn.get_all_groups()
    timestamp = time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    humanreadabledate = value.strftime('%Y-%m-%d_%H.%M.%S')
    config_name = 'live_launch_config'+humanreadabledate
    lc = LaunchConfiguration(name=config_name, image_id=img,
                             key_name='SDSEastKey',
                             security_groups=['sg-a7afb1c2'])
    conn.create_launch_configuration(lc)

#Create new Autoscaling Group
def create_autoscaling_group():
    ag = AutoScalingGroup(group_name=config_name, load_balancers=['SDSLiveLoadBalancer'], availability_zones=['us-east-1a'], launch_config=lc, min_size=2, max_size=2, connection=conn)
    conn.create_auto_scaling_group(ag)

conn = AutoScaleConnection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
print conn.get_all_groups()
old_autoscaling_group = conn.get_all_groups()
old_config_group = conn.get_all_groups()
create_image()
create_autoscaling_conf()
create_autoscaling_group()
print "Wait 5 minutes"
time.sleep(300)
print "wake up and kill the old AG group."


#old_autoscaling_group.shutdown_instances()
#old_autoscaling_group.delete()
#old_config_group.delete()
