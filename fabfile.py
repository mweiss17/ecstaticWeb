from fabric.api import *
from fabric.network import ssh

env.key_filename = '~/.ssh/martin.pem'
env.hosts = ['ec2-user@silentdiscosquad.com:22']

def prepare_deployment(branch_name):
    #local('python manage.py test sds')
    local('git add -p && git commit') 

def restart_webserver():
    sudo('sudo /etc/init.d/httpd restart')
