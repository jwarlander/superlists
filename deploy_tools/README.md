Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv


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
        └── {{ site_fqdn }}
             ├── database
             ├── source
             ├── static
             └── virtualenv

