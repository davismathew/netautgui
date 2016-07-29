from flask import jsonify

fileRead=open('/home/davis/Documents/flasky/app/ansible/Output-pythonAnsible')
Output=fileRead.read()
           # print Output
Output=Output.replace("[0;32m","")
Output=Output.replace("[0;31m","")
Output=Output.replace("[0m"," ")
Output=Output.replace("\x1b"," ")
print jsonify(Output)