Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv


## Templates:

Configuration templates are provided. Replace the following as needed:

`{{ site_fqdn }}` - Name of the site; eg. staging.my-domain.com
`{{ deployment_user }}` - User account on the server
`{{ django_project_name }}` - Name of the Django project; eg. superlists


### Nginx Virtual Host config

* see nginx.conf.j2
* replace `{{ site_fqdn }}` with, eg, staging.my-domain.com


### Upstart Job

* see gunicorn-upstart.conf.j2
* replace `{{ site_fqdn }}` with, eg, staging.my-domain.com


## Folder structure:

Assume we have a user account at /home/`{{ deployment_user }}`

    /home/{{ deployment_user }}
    └── sites
        └── {{ site_fqdn }} (checked out from git repo)
             ├── database
             ├── static
             ├── virtualenv
             └── ..other stuff

## Setup:

    # prepare the system
    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

    # set up project environment
    mkdir -p /home/{{ deployment_user }}/sites
    cd /home/{{ deployment_user }}/sites
    git clone git@bitbucket.org:jwarlander/superlists.git {{ site_fqdn }}
    cd {{ site_fqdn }}
    virtualenv --python=python3 virtualenv
    virtualenv/bin/pip install -r requirements-prod.txt
    virtualenv/bin/python manage.py migrate --noinput
    virtualenv/bin/python manage.py collectstatic --noinput

    # deploy configuration files
    sudo cp deploy_tools/nginx.conf.j2 /etc/nginx/sites-available/{{ site_fqdn }}
    ## ..modify /etc/nginx/sites-available/{{ site_fqdn }} as needed
    sudo ln -s ../sites-available/{{ site_fqdn }} /etc/nginx/sites-enabled/
    sudo cp deploy_tools/gunicorn-upstart.conf.j2 /etc/init/gunicorn-{{ site_fqdn }}.conf
    ## ..modify /etc/init/gunicorn-{{ site_fqdn }}.conf as needed

    # start services
    sudo service nginx restart
    sudo start gunicorn-{{ site_fqdn }}

## Deployment using Ansible

The project contains a playbook that will automatically do all of the above.

### Requirements

-   server exists, the IP is known, and you have root access
-   currently assumes Ubuntu 13.x

### USAGE

The playbook can be executed from anywhere, as long as you have Ansible
installed and can connect to the server as `root` over SSH.

To do a staging deployment:

-   Copy `deploy_tools/ansible/hosts-staging.template` to
    `deploy_tools/ansible/hosts-staging` and replace SERVER_IP,
    SITE_NAME, SITE_USER and REPO_URL
-   Run the playbook; either with password-based access:

        ansible-playbook deploy_tools/ansible/site.yml \
                         -i deploy_tools/ansible/hosts-staging \
                         --ask-pass

    ..or, if you have an SSH key:

        ansible-playbook deploy_tools/ansible/site.yml \
                         -i deploy_tools/ansible/hosts-staging \
                         --private-key=<PATH_TO_KEYFILE>

For a production deployment, repeat the above with `hosts-prod` instead of
`hosts-staging`.
