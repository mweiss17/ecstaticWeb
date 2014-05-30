from fabric.api import *
from fabric.network import ssh

env.key_filename = '~/.ssh/martin.pem'
env.hosts = ['ec2-user@silentdiscosquad.com:22']

def commit():
    local("git add -p -A * && git commit")

def prepare_deploy(branch_name):
    commit()
    local('git checkout master && git merge ' + branch_name)
    local('git pull')

def deploy():
    with cd('/home/ec2-user/sds'):
    	local('git push')
        run('git pull')
        run('python manage.py migrate sds')
        run('sudo /etc/init.d/httpd restart')

def restart_live():
    sudo('/etc/init.d/httpd restart')

def restart_local():
    local('sudo /etc/init.d/httpd restart')
