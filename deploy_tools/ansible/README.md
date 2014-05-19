Ansible Deployment of Superlists
================================

This directory contains an Ansible approach to deploying the Superlists
application from the excellent book [Test-Driven Web Development with Python](http://chimera.labs.oreilly.com/books/1234000000754/ch20.html#_installing_jenkins).

I've mostly structured the setup  according to [Ansible best practices](http://docs.ansible.com/playbooks_best_practices.html),
and also decided to use a couple of existing roles from Ansible Galaxy to
speed things along:

- [Stouts.jenkins](https://galaxy.ansible.com/list#/roles/858) [(GitHub)](https://github.com/Stouts/Stouts.jenkins)
- [Stouts.nginx](https://galaxy.ansible.com/list#/roles/854) [(GitHub)](https://github.com/Stouts/Stouts.nginx)

They exist as local copies below roles/, without the "Stouts." prefix so
as to avoid distractions.

Briefly, this means that we've got the following structure:

    production          # Inventory for production system (incl. Jenkins)
    staging             # Inventory for staging system
    site.yml            # Top-level site playbook; includes..
    ciservers.yml       # ..playbook for Jenkins setup
    webservers.yml      # ..playbook for web server provisioning
    deploy.yml          # ..playbook for application deployment
    roles/              # Ansible roles
        web/            # - web; with provisioning steps for Superlists
        app/            # - app; with deployment steps for Superlists
        jenkins/        # - jenkins; for the CI server
        nginx/          # - nginx; for the CI server
    vars/               # Globally used variables, included in playbooks
       secrets.yml      # - SSH keys, credentials, etc.. encrypted!

To keep things safe for storing in source control, the `secrets.yml` file
mentioned above is encrypted using [Ansible Vault](http://docs.ansible.com/playbooks_vault.html).

In the top-level project directory there are wrapper scripts that will run
`site.yml` for either production or staging. Due to the use of encryption,
you must either tell Ansible that you want to be asked for the Vault password:

    ./deploy_prod.sh --ask-vault-pass
    ./deploy_staging.sh --ask-vault-pass

..or you can create a local file with the Vault password, and refer to it:

    ./deploy_prod.sh --vault-password-file=~/.ansible_vault_password
    ./deploy_staging.sh --vault-password-file=~/.ansible_vault_password

_**NOTE:** As indicated above, to install the CI server, you must run `site.yml`
for production; staging will only deal with the Superlists web server.

Opbeat
------

If you want to integrate with [Opbeat](https://opbeat.com/), make sure you have an account,
then add the following to `vars/secrets.yml`:

    opbeat_org_id: <YOUR_ORGANIZATION_ID>
    opbeat_app_id: <YOUR_APPLICATION_ID>
    opbeat_secret_key: <YOUR_SECRET_KEY>

Finally, set `opbeat_enable=true` in the inventory file (`production`).
