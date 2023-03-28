#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__=type

DOCUMENTATION = r'''
---
+ http://localhost:8080/manager/text/list
http://localhost:8080/manager/text/reload?path=/example
http://localhost:8080/manager/text/serverinfo
http://localhost:8080/manager/text/threaddump
http://localhost:8080/manager/text/vminfo
http://localhost:8080/manager/text/sessions?path=/example

+ http://localhost:8080/manager/text/start?path=/example
+ http://localhost:8080/manager/text/stop?path=/example

+ http://localhost:8080/manager/text/undeploy?path=/example
+ http://localhost:8080/manager/text/deploy?war=bar.war

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
    'output': output get reguest command
    'name': name tomcat wars 
    'state': /running/stopped/ state tomcat war after execute request command
'''

import requests
from requests.auth import HTTPBasicAuth
from ansible.module_utils.basic import AnsibleModule

'''
    Check status output tomcat request 
'''
def check_out(out):
    if out == "" or not out.startswith("OK"):
        return False
    else:
        return True

def call_request(req, auth):
    try:
        out = requests.get(req, auth=auth, timeout=10)
        if out.status_code != requests.codes.ok:
            return f'Failed Request status code: {out.status_code}'
        return out.text
    # except requests.exceptions.HTTPError as errh:
        # module.fail_json(msg=f'Error execute requests out: "{out}"' )
    # except requests.exceptions.ConnectionError as errc:
        # module.fail_json(msg=f'Error execute requests out: "{out}"',)
    # except requests.exceptions.Timeout as err:
        # module.fail_json(msg=f'Error execute requests out: "{out}"', )
    except requests.exceptions.RequestException as err:
        return f'Error request: {err}'

'''
    Find war module exists and get state module
'''
def status_tomcat(name, port, auth):
    war = {}
    # out_list = requests.get(f"http://localhost:{port}/manager/test/list", auth=auth, timeout=2)
    out_list = call_request(f"http://localhost:{port}/manager/test/list", auth)
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
def stop_start(port, name, state, auth):
    # out = requests.get(f"http://localhost:{port}/manager/{state}?path=/{name}", auth=auth)
    out = call_request(f"http://localhost:{port}/manager/{state}?path=/{name}", auth)
    return out

'''
    Undeploy tomcat module
'''
def undeploy(port, name, auth):
    out = call_request(f"http://localhost:{port}/manager/text/undeploy?path=/{name}", auth)
    return out

'''
    Deploy tomcat module
'''
def deploy(port, name, auth):
    out = call_request(f"http://localhost:{port}/manager/text/deploy?war={name}.war", auth)
    return out


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        state=dict(type='str', choices=['started', 'stopped', 'restarted', 'redeployed']),
        port=dict(type='str', required=False, default="8080"),
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
    port = module.params['port']
    name = module.params['name']
    auth = HTTPBasicAuth(module.params['username'], module.params['password'])
    status_war = status_tomcat(name, port, auth)
    # Check war module exists
    res = {}
    if status_war or state == "redeployed":
        state = module.params['state']
        out = ""
        state_check = ""
        if state == "started":
            if status_war['state'] == "stopped":
                out = stop_start(port, name, "start", auth)
            state_check = "running"
        elif state == "stopped":
            if status_war['state'] == "running":
                out = stop_start(port, name, "stop", auth)
            state_check = "stopped"
        elif state == "restarted":
            if status_war['state'] == "running":
                out = stop_start(port, name, "stop", auth)
            if check_out(out):
                out = stop_start(port, name, "start", auth)
            state_check = "running"
        elif state == "redeployed":
            if status_war:
                out = undeploy(port, name, auth)
                if check_out(out):
                    out = deploy(port, name, auth)
            state_check = "running"
        status_war = status_tomcat(name, port, auth)
        res['output'] = out
        res['name'] = name
        res['state'] = status_war['state']
        if check_out(out) and status_war['state'] == state_check:
            # Ok state war equal wanted
            module.exit_json(**res)
        else:
            # Error state not equal or command run failed
            if not check_out(out):
                module.fail_json(msg=f'Error execute requests out: "{out}"', **res)
            elif status_war['state'] != state_check:
                module.fail_json(msg=f'State not quals. State war module: {status_war["state"]}', **res)
        # Error?? 
        module.fail_json(msg=f'Error  out: {out}, state: {status_war["state"]}', **res)
    module.fail_json(msg=f'Error get state tomcat module', **res)

def main():
    run_module()

if __name__ == '__main__':
    main()
