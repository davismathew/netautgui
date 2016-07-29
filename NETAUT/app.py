from flask import Flask,render_template, request,jsonify
from AnsiblePlaybook import AnsiblePlaybook
import os
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	print request.form['username'] 
        if request.form['username'] != 'network' or request.form['password'] != '0$net!!123':
	    print "came"
            error = 'Invalid Credentials. Please try again.'
        else:
	    play=[]
	    for file in os.listdir("/home/davis/Documents/Network-automation"):
		if file.endswith(".yml"):
		    play.append(file)    
		    print(file)	    
	    inv=['dev','host']
	    #play=['cisco.yml','cisco_ce.yml']
            return render_template('Inventory.html',Inventory=inv,Playbook=play)
    return render_template('login.html', error=error)


@app.route('/runAnsiblePlaybook',methods=['GET', 'POST', 'DELETE','OPTIONS'])
def runAnsiblePlaybook():
    if request.method == 'POST':
	    # name : name, desc : desc, jobTags : jobTags,  inventory : inventory, playbookName:playbookName
	    name=str(request.form['name'])
	    desc=str(request.form['desc'])
	    jTags=str(request.form['jobTags'])
	    inventory=str(request.form['inventory'])
	    playbookName=str(request.form['playbookName'])
	    playbook=AnsiblePlaybook(playbookName,inventory)
	    Output=playbook.runPlaybook()
	    fileRead=open('Output-pythonAnsible')
	    Output=fileRead.read()
	   # print Output
	    Output=Output.replace("[0;32m","")
            Output=Output.replace("[0;31m","")
	    Output=Output.replace("[0m"," ")
	    Output=Output.replace("\x1b"," ")
	    #print Output
	    ret_data = {"value": Output}
	    return jsonify(ret_data)
    #return render_template('Inventory.html',Output=Output)
	    

    

		  

if __name__ =='__main__':
    app.run(host='200.12.221.13',port=5000)
    #app.run()
