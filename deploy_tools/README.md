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

Servers:

-   servers for web + CI exist, the IPs are known, and you have root access
-   currently assumes Ubuntu 13.x (app) / 14.x (CI) but may work for others

Inventory files:

-   Copy `deploy_tools/ansible/staging.template` to
    `deploy_tools/ansible/staging` and replace APP_HOSTNAME,
    APP_SERVER_IP, APP_USER, CI_HOSTNAME, CI_SERVER_IP and REPO_URL
-   Copy `deploy_tools/ansible/production.template` to
    `deploy_tools/ansible/production` and replace APP_HOSTNAME,
    APP_SERVER_IP, APP_USER, CI_HOSTNAME, CI_SERVER_IP and REPO_URL

SSH keys:

-   Create an SSH key set for Jenkins:

        # Use an empty password, when asked..
        ssh-keygen -t rsa -f jenkins -q

-   Create the vars file for SSH keys:

        ansible-vault create deploy_tools/ansible/vars/secrets.yml

The last step above will ask for a password (make it a good one, and
remember it!), then put you in edit mode. Here, you'll be using copy-paste
to end up with something like this:

    ---
    jenkins_private_key: |
        -----BEGIN RSA PRIVATE KEY-----
        MIIEowIBAAKCAQEA3Bf2AZ68qx/APWThYtMj8qSuUKrwLk6M1FBArouWQY+9uvMs
        D4N5EgS3p2TIECurgya4VivFMlTpblOP4SDr2cOM4HSnvNgUQ93Qb9uXfOaemzPs
        <...more lines...>
        leLhPke0/ZBJURhMUa51hIKuXA81coe2tWpVQ3W+Qc7uQc62jGyw
        -----END RSA PRIVATE KEY-----

    jenkins_public_key: |-
        ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcF/YBnryrH8A9ZOFi0yPypK5QqvAuTozUUECui5ZBj7268ywPg3kSBLenZMgQK6uDJrhWK8UyVOluU4/hIOvZw4zgdKe82BRD3dBv25d85p6bM+zqdVNyP4+CfoETiu6voEUOx5NYKWgRBPRGeyHng3jV79u7oQCpIBQBYBVa18dMRHcDVLvuGuxN+b32EOu9ptyB1hJBpeFiTp4hg94AZAiJO250mRnsv75fFQWY7paMecCXK4L49ciZ1aKagAGXa1mTBFaO0TRudQkPWalxQQZ2TlDcCfkvFvy0c6/Nm5XdTm2IUwibiy6vIozJxe9L52UCN+DYL8qFljODGydH jenkins

Note that the public key should be all on one line, and that the YAML entry for
it must use '|-' to properly strip the ending newline.

### USAGE

The playbook can be executed from anywhere, as long as you have Ansible
installed and can connect to the server as `root` over SSH.

#### Deploying with ansible-playbook

To do a staging deployment:

-   Run the playbook; either with password-based access:

        ansible-playbook deploy_tools/ansible/site.yml \
                         -i deploy_tools/ansible/staging \
                         --ask-pass \
                         --ask-vault-pass

    ..or, if you have an SSH key, and a pw file for the Vault:

        ansible-playbook deploy_tools/ansible/site.yml \
                         -i deploy_tools/ansible/staging \
                         --private-key=<PATH_TO_KEYFILE> \
                         --vault-password-file=<PATH_TO_VAULTPW_FILE>

For a production deployment, repeat the above with `production` instead of
`staging` for the inventory file.

#### Deploying with wrapper scripts

If you have an SSH key saved as `~/.ssh/id_rsa` that's valid for server
access, use the top-level wrapper scripts:

    ./deploy_staging.sh --ask-vault-pass
    ./deploy_prod.sh --ask-vault-pass

Similarly, with a Vault password file:

    ./deploy_staging.sh --vault-password-file=<PATH_TO_VAULTPW_FILE>
    ./deploy_prod.sh --vault-password-file=<PATH_TO_VAULTPW_FILE>

