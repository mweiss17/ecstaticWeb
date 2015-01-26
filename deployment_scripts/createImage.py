   

import boto
import boto.utils
import time
import datetime


instance_id = boto.utils.get_instance_metadata()['instance-id']
timestamp = time.time()
value = datetime.datetime.fromtimestamp(timestamp)
humanreadabledate = value.strftime('%Y-%m-%d_%H.%M.%S')
name = 'productionImage'+humanreadabledate
print name
conn = boto.connect_ec2()
conn.create_image(instance_id, name, description=None, no_reboot=False, block_device_mapping=None, dry_run=False)

