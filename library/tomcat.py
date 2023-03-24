#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__=type

DOCUMENTATION = r'''
---
http://localhost:8080/manager/text/list
http://localhost:8080/manager/text/reload?path=/example
http://localhost:8080/manager/text/serverinfo
http://localhost:8080/manager/text/threaddump
http://localhost:8080/manager/text/vminfo
http://localhost:8080/manager/text/sessions?path=/example

http://localhost:8080/manager/text/start?path=/example
http://localhost:8080/manager/text/stop?path=/example

http://localhost:8080/manager/text/undeploy?path=/example
http://localhost:8080/manager/text/deploy?war=bar.war

'''
EXAMPLES = r'''
tasks:
  - name: Restart module
    tomcat:
      name: example
      port: 8080
      username: tomuser
      password: tompass
      state: restarted
  - name: Redeploy module
    tomcat:
      name: example
      port: 8080
      username: tomuser
      password: tompass
      state: redeploy
  state = restarted/started/stopped/redeploy
'''
RETURN = r'''
'''

import requests
from requests.auth import HTTPBasicAuth
from ansible.module_utils.basic import AnsibleModule

'''
    List tomcat modules and status
'''
def list_tomcat(name, port, auth):
    war = {}
    out_list = requests.get(f"http://localhost:{port}/manager/test/list", auth=auth, timeout=2)
    for line in out_list:
        sp_line = line.split(':')
        if len(sp_line) > 1:
            war_name = sp_line[0].replace("/", "", 1) 
            if name == war_name:
                war['name'] = sp_line[0]
                war['status'] = sp_line[1]
    return war

'''
    Stop tomcat module
    Start tomcat module
'''
def restart(port, name, auth):
    out_stop = requests.get(f"http://localhost:{port}/manager/stop?path=/{name}", auth=auth)
    if out_stop == "" or not out_stop.startswith("OK"):
        return False
    out_start = requests.get(f"http://localhost:{port}/manager/start?path=/{name}", auth=auth)
    if out_start == "" or not out_start.startswith("OK"):
        return False
    return True

'''
    Undeploy tomcat module
    Deploy tomcat module
'''
def deploy(port, name, auth):
    out_undep = requests.get(f"http://localhost:{port}/manager/text/undeploy?path=/{name}", auth=auth)
    if out_undep == "" or not out_undep.startswith("OK"):
        return False
    out_dep = requests.get(f"http://localhost:{port}/manager/text/deploy?war={name}.war", auth=auth)
    if out_dep == "" or not out_dep.startswith("OK"):
        return False
    return True


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        state=dict(type='str', required=True),
        port=dict(type='str', required=False, default="8080"),
        new=dict(type='bool', required=False, default=False),
    )
    result = dict(
        changed=False,
        original_message='',
        message=''
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    if module.check_mode:
        module.exit_json(**result)
    auth = HTTPBasicAuth(module.params['username'], module.params['password'])
    tomcat_war = list_tomcat(module.params['name'], module.params['port'], auth)
    # Check war module exists
    if tomcat_war:
        '''
        check state and chouse use functions
        call function
        check status tomcat module
        check state module with param state
        '''

    # result['original_message'] = module.params['name']
    # result['message'] = 'goodbay'
    # if module.params['new']:
        # result['changed'] = True
    # if module.params['name'] == 'fail me':
        # module.fail_json(msg='You requested this to fail', **result)
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
