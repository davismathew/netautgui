from flask import render_template, redirect, url_for, jsonify, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from .forms import InventoryForm, ProjectForm, TaskForm
from . import ansible
from .. import db
from ..models import Inventory, Post, Project, Task, Result, User
import os
import time
from datetime import datetime

@ansible.route('/files', methods=['GET','POST'])
def fileslist():
    if request.method == 'POST':
        inventory = Inventory.query.filter_by(id=2).first()
        project = Project.query.all()
        retdata={'value':project[1].name}
        return jsonify(retdata)

    files=os.listdir("/etc/ansible/")
    inventory = Inventory.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    # return render_template('ansible/files.html', files=files)
    time.sleep(5)
    fileRead=open('/home/davis/Documents/flasky/app/ansible/Output-pythonAnsible')
    Output=fileRead.read()
           # print Output
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
            #print Output
    ret_data = {"key": files}
    return jsonify(ret_data)

@ansible.route('/run', methods=['GET', 'POST'])
def runnothing():
    args = request.args.get('a')
    argsb = request.args.get('b')
    inventory = Inventory.query.filter_by(id=2).first()
    project = Project.query.all()
    # retdata={'value':project[1].name}
    retdata={'value':argsb}
    return jsonify(retdata)

@ansible.route('/runplay', methods=['GET', 'POST'])
def runplay():
    error = None
    inv=['test']
    play=[]
    if request.method == 'GET':
        for file in os.listdir("/var/lib/emc/networkaut"):
            if file.endswith(".yml"):
                play.append(file)
                print(file)
            # inv=['dev','host']
            #play=['cisco.yml','cisco_ce.yml']
    return render_template('Playoutput.html',Inventory=inv,Playbook=play)

# @ansible.route('/runplaybook', methods=['GET','POST'])
# @login_required
# def runplaybook():
#     # Output=''
#     # ret_data={}
#     if request.method == 'GET':
#             # name : name, desc : desc, jobTags : jobTags,  inventory : inventory, playbookName:playbookName
#             # name=str(request.form['name'])
#             # desc=str(request.form['desc'])
#             # jTags=str(request.form['jobTags'])
#             # inventory=str(request.form['inventory'])
#             # playbookName=str(request.form['playbookName'])
#             # playbook=AnsiblePlaybook(playbookName,inventory)
#             # Output=playbook.runPlaybook()
#             fileRead=open('/home/davis/Documents/flasky/app/ansible/Output-pythonAnsible')
#             Output=fileRead.read()
#            # print Output
#             Output=Output.replace("[0;32m","")
#             Output=Output.replace("[0;31m","")
#             Output=Output.replace("[0m"," ")
#             Output=Output.replace("\x1b"," ")
#             Output=Output.replace('\n', '<br>')
#             #print Output
#             ret_data = {"value": Output}
#             # return jsonify(ret_data)
#             return render_template('ansible/runplay.html',ret_data=ret_data)

    #return render_template('Inventory.html',Output=Output)



@ansible.route('/create-inventory', methods=['GET','POST'])
@login_required
def create_inventory():
    form=InventoryForm()
    if form.validate_on_submit():
        userobj = User.query.filter_by(id=int(current_user.id)).first()
        inventory=Inventory(name = form.name.data,
                            description = form.description.data,
                            file = form.file.data,
                            users = userobj,
                            tags = form.tags.data,
                            variables = form.variables.data)
        db.session.add(inventory)
        flash('Inventory has been updated.')
        return redirect(url_for('ansible.listinventory'))
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/create-inventory.html', form=form)

@ansible.route('/edit-inventory/<int:id>', methods=['GET','POST'])
@login_required
def edit_inventory(id):
    editinventory=Inventory.query.get_or_404(id)
    form=InventoryForm()
    if form.validate_on_submit():
        inventory=Inventory(name = form.name.data,
                            description = form.description.data,
                            file = form.file.data,
                            tags = form.tags.data,
                            variables = form.variables.data)
        db.session.add(inventory)
        flash('Inventory has been updated.')
        return redirect(url_for('ansible.listinventory'))
    form.name.data = editinventory.name
    form.description.data = editinventory.description
    form.file.data = editinventory.file
    form.tags.data = editinventory.tags
    form.variables.data = editinventory.variables
    return render_template('ansible/edit-inventory.html', form=form)


@ansible.route('/listinventory', methods=['GET','POST'])
@login_required
def listinventory():
    inventory = Inventory.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/inventory.html', inventories=inventory)

@ansible.route('/create-project', methods=['GET','POST'])
@login_required
def create_project():
    form=ProjectForm()
    if form.validate_on_submit():
        userobj = User.query.filter_by(id=int(current_user.id)).first()
        project=Project(name = form.name.data,
                        users = userobj,
                        tags = form.tags.data,
                        projectdir = form.projectdir.data,
                        description = form.description.data
                        )
        db.session.add(project)
        flash('Project has been created.')
        return redirect(url_for('ansible.listproject'))
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/edit-project.html', form=form)

@ansible.route('/listproject', methods=['GET','POST'])
@login_required
def listproject():
    project = Project.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/project.html', projects=project)


@ansible.route('/create-task', methods=['GET','POST'])
@login_required
def create_task():
    form=TaskForm()
    if form.validate_on_submit():
        userobj = User.query.filter_by(id=int(current_user.id)).first()
        projectobj = Project.query.filter_by(name=form.project.data).first()
        task=Task(name = form.name.data,
                            description = form.description.data,
                            playbook = form.playbook.data,
                            users = userobj,
                            project = projectobj,
                            inventory = form.inventory.data,
                            credential = form.credential.data,
                            tags = form.tags.data)
        db.session.add(task)
        flash('Task has been created.')
        return redirect(url_for('ansible.listtask'))
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/edit-task.html', form=form)

@ansible.route('/listtask', methods=['GET','POST'])
@login_required
def listtask():
    task = Task.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    baseurl="http://localhost:5000/create-result"
    return render_template('ansible/task.html', tasks=task, baseurl=baseurl)

@ansible.route('/create-result', methods=['GET','POST'])
@login_required
def create_result():
    status = request.args.get('status')
    finished = datetime.utcnow()
    playbook = request.args.get('playbook')
    tags = request.args.get('tags')
    inventory = request.args.get('inventory')
    credential = request.args.get('credential')
    task_id = request.args.get('taskid')

    taskobj = Task.query.filter_by(id=int(task_id)).first()

    outpath = request.args.get('outpath')
    userobj = User.query.filter_by(id=int(current_user.id)).first()

    result=Result(status = status,
                    finished = finished,
                    playbook = playbook,
                    inventory = inventory,
                    credential = credential,
                    users = userobj,
                    outfile = outpath,
                    task = taskobj,
                    tags = tags)
    db.session.add(result)
    flash('Result has been created.')
    return redirect(url_for('ansible.listresult'))

@ansible.route('/listresult', methods=['GET','POST'])
def listresult():
    result = Result.query.all()
    # task = Task.query.filter_by(id=int(result[0].project_id)).first()
    # user = User.query.filter_by(id=int(result[0].user_id)).first()
    # timestamp = str(result[0]).finished.strftime("%Y-%m-%d")
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    user = current_user
    # form.file.data = current_user.about_me
    return render_template('ansible/result.html', results=result, user=user)

# @ansible.route('/run-playbook', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         current_user.name = form.name.data
#         current_user.location = form.location.data
#         current_user.about_me = form.about_me.data
#         db.session.add(current_user)
#         flash('Your profile has been updated.')
#         return redirect(url_for('.user', username=current_user.username))
#     form.name.data = current_user.name
#     form.location.data = current_user.location
#     form.about_me.data = current_user.about_me
#     return render_template('edit_profile.html', form=form)
