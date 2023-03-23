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
      user: tomuser
      pass: tompass
      state: restarted
  - name: Redeploy module
    tomcat:
      name: example
      port: 8080
      user: tomuser
      pass: tompass
      state: redeploy
  state = restarted/started/stopped/redeploy
'''
RETURN = r'''
'''

import requests
from ansible.module_utils.basic import AnsibleModule

def list_tomcat():
    '''
    List tomcat modules and status
    '''
    out_list = requests.get('http://localhost:8080/manager/test/list')

def restart():
    '''
    Stop tomcat module
    Start tomcat module
    '''
    out_stop = requests.get('http://localhost:8080/manager/stop?path=/example')
    out_start = requests.get('http://localhost:8080/manager/start?path=/example')

def deploy():
    '''
    Undeploy tomcat module
    Deploy tomcat module
    '''
    out_udep = requests.get('http://localhost:8080/manager/text/undeploy?path=/example')
    out_dep = requests.get('http://localhost:8080/manager/text/deploy?war=bar.war')


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
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
    result['original_message'] = module.params['name']
    result['message'] = 'goodbay'
    if module.params['new']:
        result['changed'] = True
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
