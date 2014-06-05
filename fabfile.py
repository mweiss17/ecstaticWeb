from fabric.api import *
from fabric.network import ssh

env.key_filename = '~/.ssh/martin.pem'
env.hosts = ['ec2-user@silentdiscosquad.com:22']

def prepare_deploy(branch_name):
    local('python manage.py schemamigration sds --auto')
    local('python manage.py migrate sds')
    local("git add -p -A * && git commit")
    local('git checkout master && git merge ' + branch_name)

def deploy():
    with cd('/home/ec2-user/sds'):
        local('git push')
        run('git pull')
        run('python manage.py schemamigration sds --auto')
        run('python manage.py migrate sds')
        run('sudo /etc/init.d/httpd restart')

def reset_migrations():
    #navigate into the production database and run:  'drop table south_migrationhistory;'
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
