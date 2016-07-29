#!/home/davis/Documents/netautgui/flask/bin/python2.7
from play_util.AnsiblePlaybook import AnsiblePlaybook

playbookName='cisco_xe.yml'
inventory='dev'
playbook=AnsiblePlaybook(playbookName,inventory)
Output=playbook.runPlaybook()
fileRead=open('Output-pythonAnsible')
Output=fileRead.read()
           # print Output
#Output=Output.replace("[0;32m","")
#Output=Output.replace("[0;31m","")
#Output=Output.replace("[0m"," ")
#Output=Output.replace("\x1b"," ")
print Output

