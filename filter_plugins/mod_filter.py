#!/usr/bin/python
'''
Filter modify input array:
--------------------
[
server1:
  mops:
   - module1.war
   - module2.war
server2:
  mods:
   - module1.war
   - module3.war
   - module4.war
]

in Output array:
-------------
[
  - upstream: upstream1
    servers: [server1, server2]
    mods: [module1]
  - upstream: upstream2
    servers: [server1]
    mods: [module2]
  - upstream: upstream3
    servers: [server2]
    mods: [module3, module4]
]
'''
def filtermod(things):
#   seen = set()
  my_things = []
  result = []
  for app in things:
    for thing in app['instance']:
      host = f"{app['host']}:{thing['tomcat_port']}"
      for war in thing['mods']:
        if war == 'mod-chatbot.war':
            found = True
            break
        found = False
        for my in my_things:
          if my['mod'] == war and my['server'].find(host) == -1:
            my['server'] = f"{my['server']},{host}"
            found = True
            break
        if found == False:
          my_things.append({'war': war, 'server': host})
  for my in my_things:
    found = False
    for res in result:
      if res['servers'] == my['server'] and res['mods'].find(my['mod']) == -1:
        res['mods'] = f"{res['mods']}|{my['mod']}"
        found = True
        break
      if res['servers'] == my['server'] and res['mods'].find(my['mod']) != -1:
        found = True
        break
    if found == False:
      result.append({'wars': my['mod'], 'servers': my['server']})
  for index, res in enumerate(result):
    res['servers'] = res['servers'].split(',')
    res['mods'] = res['mods'].replace(".war", "")
    res['upstream'] = f"wap-upstream{index}"
  return result

class FilterModule(object):
    def filters(self):
        return { 'filtermod': filtermod }