inputs vars
----------------
- ntp_pool - ntp servers. example: `ntp.debian.org`
- sources_list - list apt sources. example: 
```  |
   deb ftp://127.0.0.1/main smolensk main contrib non-free
   deb ftp://127.0.0.1/devel smolensk main contrib non-free
   deb ftp://127.0.0.1/update smolensk main contrib non-free
   deb ftp://127.0.0.1/update-devel smolensk main contrib non-free
   ```
- resolv_conf - dns resolv. example:
``` |
  nameserver 8.8.8.8
  nameserver 1.1.1.1
```
- fonts_dirs - fonts directory. see vars/main.yaml
- packages - list deb packages to install. see vars/main.yml
- nfs_dir - nfs directory for exchange files. see vars/main.yaml
- remote_package_dir - directory for deb packages
- admin_packages - aditional list packages for install. see vars/main.yaml
- domain_project - domain name project for /etc/hosts 
- add_name - additional name hosts /etc/hosts
