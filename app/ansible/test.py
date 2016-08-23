from play_util.AnsiblePlaybook import AnsiblePlaybook

playbook=AnsiblePlaybook('hostname.yml','dev','stdout100.out')
Output=playbook.runPlaybook()
fileRead=open('stdout100.out')
Output=fileRead.read()
print Output

