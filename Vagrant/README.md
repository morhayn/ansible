### Config virtual mashine for testing ansible playbooks
Install vagrant
```
yum install vagrant
```
- Create Vmbox
```
-- Create VM in VirtualBox
-- Run VM and first initial
-- Off VM
cd Vagrant
vagrant package --base vm-name --out vm01.box
vagrant box add vm01.box --name vm01
```
- Run virtual mashine
```
 vagrant up
```
- SSH Connect to virtual mashine
```
 vagrant ssh
```
- Stop virtual mashine
```
 vagrant destroy
```