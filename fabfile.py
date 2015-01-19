from fabric import api as fab
from fabric.network import ssh
import boto

LOAD_BALANCER_NAME = 'SDSLiveLoadBalancer'
SERVER_USER = 'ec2-user'
SSH_KEY_FILE = '~/.ssh/martin.pem'

def aws_hosts():
    # Get a list of instance IDs for the ELB.
    instances = []
    conn = boto.connect_elb()
    for elb in conn.get_all_load_balancers(LOAD_BALANCER_NAME):
        instances.extend(elb.instances)
 
    # Get the instance IDs for the reservations.
    conn = boto.connect_ec2()
    reservations = conn.get_all_instances([i.id for i in instances])
    instance_ids = []
    for reservation in reservations:
        for i in reservation.instances:
            instance_ids.append(i.id)
 
    # Get the public CNAMES for those instances.
    hosts = []
    for host in conn.get_all_instances(instance_ids):
        hosts.extend([i.public_dns_name for i in host.instances])
    hosts.sort() # Put them in a consistent order, so that calling code can do hosts[0] and hosts[1] consistently.
 
    return hosts

def aws():
    fab.env.hosts = aws_hosts()
    print fab.env.hosts
    fab.env.key_filename = SSH_KEY_FILE
    fab.env.user = SERVER_USER
    fab.env.parallel = False 
aws()

def prepare_deploy_dev(branch_name):
    with fab.settings(warn_only=True):
	fab.env.hosts = ['ec2-user@54.173.246.101:22']
        fab.local('python manage.py schemamigration sds --auto')
        fab.local('python manage.py migrate sds')
	fab.local("git add -p --all :/ && git commit -a")
        fab.local('git checkout master && git merge ' + branch_name)

def prepare_deploy_preprod(branch_name):
    with fab.settings(warn_only=True):
        fab.local('python manage.py schemamigration sds --auto')
        fab.local('python manage.py migrate sds')
        fab.local("git add -p --all :/ && git commit -a")
        fab.local('git checkout master && git merge ' + branch_name)

def deploy_preprod():
    with fab.settings(warn_only=True):
        with fab.cd('/home/ec2-user/sds'):
            fab.local('git push')
            fab.run('git pull')
            fab.run('python manage.py schemamigration sds --auto')
            fab.run('python manage.py migrate sds')
            fab.run('sudo /etc/init.d/httpd restart')


def deploy_dev():
    with fab.settings(warn_only=True):
        with fab.cd('/home/ec2-user/sds'):
            fab.env.hosts = ['ec2-user@54.173.246.101:22']
	    print "here"
	    fab.local('git push')
            fab.run('git pull')
            fab.run('python manage.py schemamigration sds --auto')
            fab.run('python manage.py migrate sds')
            fab.run('sudo /etc/init.d/httpd restart')

def reset_migrations():
    #navigate into the production database and run:  'drop table south_migrationhistory;'
    #Make sure that the Django Models.py schema is identical to the database. Check with "\d+ TABLENAME"
    #ALTER TABLE sds_photos DROP COLUMN test;

    local('rm -r sds/migrations')
    local('python manage.py schemamigration sds --initial')
    local('python manage.py syncdb')
    local('python manage.py migrate sds 0001 --fake --delete-ghost-migrations')
    local('sudo /etc/init.d/httpd restart')
    with cd('/home/ec2-user/sds'):
        run('rm -r sds/migrations')
        run('python manage.py schemamigration sds --initial')
        run('python manage.py syncdb')
        run('python manage.py migrate sds 0001 --fake --delete-ghost-migrations')
        sudo('/etc/init.d/httpd restart')
