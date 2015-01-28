import boto, boto.utils, time, datetime, os, re
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup

#Couldn't get this script to work.
#The main goal was to delete the old autoscaling group, and turn of the old instances
#The issue was that I wanted this script to WAIT until we had confirmation that the new autoscaling group was live
#Couldn't get AWS to give me that


#get instances from an autoscaling group
def get_instances_from_group(group):
    instance_ids = [i.instance_id for i in group.instances]
    #get the actual instances in each group
    reservations = ec2_conn.get_all_instances(instance_ids=instance_ids, filters=None, dry_run=False, max_results=None)
    instances = []
    for r in reservations:
        instances.extend(r.instances)
    return instances

#Check Instance Health
def check_instance_health(instances):
    all_healthy = False
    for i in instances:
        i.update()
        print i
        print i.state
        #if the instance is running, set all healthy to true
        if i.state == "running":
            all_healthy = True
            #if any instance is not running, set all_healthy to false and break out to the group level
        else:
            all_healthy = False
            break
    return all_healthy 

def check_group_health(group_activities):
    all_healthy = False
    for g in group_activities:
        print g 
        if int(g.progress) == 100:
            all_healthy = True
        else:
            all_healthy = False
            break
    return all_healthy

#make connections
autoscaling_conn = AutoScaleConnection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
ec2_conn = boto.ec2.connect_to_region('us-east-1') 

#get the autoscaling groups
a_groups = autoscaling_conn.get_all_groups()
for group in a_groups:
    instances = get_instances_from_group(group)

time.sleep(30)    
#wait until all groups have all healthy instances
while(True):
    all_healthy = False
    #go through all the groups
    for group in a_groups:
        #check if the group is ready
        group.update()
        #if the group is live
        if check_group_health(group.get_activities()):             
            print "Group Passes"
            print group
            #iterate over all instances in each group, updating them
            if check_instance_health(get_instances_from_group(group)):
                print "Instances Pass"
                all_healthy = True
            else:
                print "Instances Failed"
                all_healthy = False
                break
        #else the group isn't live
        else:
            print "Group Failed"
            print group
            all_healthy = False
            break
    time.sleep(5) 
    if all_healthy:
        break
print "YAY"



#delete the old autoscaling groups that had healthy instances initially
#for old_group in healthy_groups:
#    print "killing old group:"
#    print old_group
    #old_group.shutdown_instances()
    #old_group.delete()

#delete the config groups
#old_config_groups = autoscaling_conn.get_all_groups()
#for old_config_group in old_config_groups:
#    old_config_group.delete()

