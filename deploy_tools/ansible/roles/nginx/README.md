Stouts.nginx
============

[![Build Status](https://travis-ci.org/Stouts/Stouts.nginx.png)](https://travis-ci.org/Stouts/Stouts.nginx)

Ansible role which simple manage nginx

#### Variables

```yaml
nginx_enabled: yes                  # The role in enabled
nginx_dir: /etc/nginx               # Nginx config directory
nginx_user: www-data                # -------------------
nginx_worker_processes: 4           #   See nginx docs
nginx_worker_connections: 1024      # -------------------
nginx_sendfile: yes
nginx_keepalive_timeout: 65
nginx_gzip: yes
nginx_server_names_hash_bucket_size: 128
nginx_access_log: /var/log/nginx/access.log
nginx_error_log: /var/log/nginx/error.log
nginx_http_options:                 # Additional http options
                                    # Ex: nginx_http_options:
                                    #       name: value
                                    #       name: value

nginx_servers:                      # Setup servers (simplest interface, use cfg files for large configurations)
                                    # Ex: nginx_servers:
                                    #     -
                                    #       - listen 80;
                                    #       - server_name localhost;
                                    #       - location / { root html; index index.html; }
                                    #     -
                                    #       - listen 80;
                                    #       - server_name test.com;
                                    #       - location / { root /test; index index.html; }
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.nginx/issues)!

