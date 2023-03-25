### example my playbooks

Vagrant - config vagrant for simple test apnsible playbooks

filter_plugin - my filter for convert list tomcat modules in configure nginx streams

library - my module for start/stop/redeploy tomcat wars

------------------------------------
Playbooks
------------------------------------
- astra-cassandra - install database cassandra. use role astra-cassandra-config
- astra-elasticsearch - install batanase elasticsearch. use role astra-elastic-conf
- astra-kafka - install queue brocker kafka and zookeeper. use role astra-kafka
- astra-nginx - install web server nginx. use role astra-nginx
- astra - initial setup astra linux. use role astra-init
- local-mon_confug - coverted inventory to config file for diaginfra
- local_nginx_vars - test configure nginx stream to tomcat modules
- local_remmina - add to rammina servers from output remmina.py
- telegraf - install telegraf for agregate tomcat logs files
- test_local_memmory - test get total memory and math operation
- test - testing create /etc/host from inventory servers
- upload_nginx - update nginx site. 
- upload_tomcat - updtae tomcat modules. use tasks/upload_tomcat_in 
------------------------------------
Roles
------------------------------------
- astra-cassandra-config - install cassandra.  config template/cassandra.j2
- astra-elastic-conf - install elsactic.  config tamplate/elasticsearch.j2
- astra-influxdb2 - empty 
- astra-init - initinal system. file - deb packages, vars - list programs
- astra-kafka - install kafka. file/kafka.tgz and configs template/*
- astra-nginx - install nginx.  configs site template/*
- astra-openjdk8 - install java openjdk8
- astra-telegraf - install telegraf. file/telegraf.deb confug template/telegraf.j2
- centos-initial - initial system centos7
- centos-jenkins - install jenkins in docker swarm on centos7
- centos_service - initial docker swarm