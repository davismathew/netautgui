from flask import render_template, redirect, url_for, jsonify, abort, flash, send_from_directory, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc
from .forms import InventoryForm, ProjectForm, TaskForm
from . import ansible
from sqlalchemy import update
from .. import db
from ..models import Inventory, Post, Project, Task, Result, User
import os
import time
from datetime import datetime
from .ansible_utils import get_path
from play_util.AnsiblePlaybook import AnsiblePlaybook

@ansible.route('/downloadstdout', methods=['GET','POST'])
def downloadstdout():
    resultid = request.args.get('result')
    filename = "stdout"+resultid+".out"
    return send_from_directory('/etc/ansiblestdout',filename,as_attachment=True)

@ansible.route('/runresult', methods=['GET','POST'])
def runresult():
    if request.method == 'POST':
        resultid=str(request.form['result'])
        editresult = Result.query.get_or_404(resultid)
        stdoutpath = get_path('resultout')
        stdoutfilename = "stdout"+resultid+".out"
        stdoutfile = stdoutpath+"/"+stdoutfilename
        playbookName = editresult.playbook
        inventory = editresult.inventory
        editresult.outfile = stdoutfile
        # retdata = {'value':stdoutfile}
       playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
       Output=playbook.runPlaybook()
        fileRead=open(stdoutfile)
        Output=fileRead.read()
        # print Output
        Output=Output.replace("[0;32m","")
        Output=Output.replace("[0;31m","")
        Output=Output.replace("[0m"," ")
        Output=Output.replace("\x1b"," ")
        retdata={'value':Output}
        return jsonify(retdata)

    ret_data={'value':"use post with args result"}
    return jsonify(ret_data)

@ansible.route('/getresultout', methods=['GET','POST'])
def fetchresultout():
    if request.method == 'POST':
        resultid=str(request.form['result'])
        result = Result.query.get_or_404(resultid)
        stdoutfile = result.outfile
        # retdata = {'value':stdoutfile}
        # playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
        # Output=playbook.runPlaybook()
        fileRead=open(stdoutfile)
        Output=fileRead.read()
        # # print Output
        Output=Output.replace("[0;32m","")
        Output=Output.replace("[0;31m","")
        Output=Output.replace("[0m"," ")
        Output=Output.replace("\x1b"," ")
        retdata={'value':Output}
        return jsonify(retdata)

    ret_data={'value':"use post with args result"}
    return jsonify(ret_data)


@ansible.route('/runplay', methods=['GET', 'POST'])
def runnothing():
    playbookName = request.args.get('playbookname')
    inventory = request.args.get('inventory')
    path = request.args.get('projpath')
  #  inventory = Inventory.query.filter_by(id=2).first()
  #  project = Project.query.all()
    # retdata={'value':project[1].name}
  #  retdata={'value':argsb}
  #  return jsonify(retdata)
  #   playbook=AnsiblePlaybook(playbookName,inventory)
  #   Output=playbook.runPlaybook()
    fileRead=open('Output-pythonAnsible')
    Output=fileRead.read()
    # print Output
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    #print Output
#    ret_data = {"value": playbookName}
    ret_data = {"key": Output}
    return jsonify(ret_data)

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

@ansible.route('/create-orion', methods=['GET','POST'])
@login_required
def create_orion():
    form=TaskForm()
    if form.validate_on_submit():
        userobj = User.query.filter_by(id=int(current_user.id)).first()
        projectobj = Project.query.filter_by(name=form.project.data).first()
        task=Task(name = form.name.data,
                            description = form.description.data,
                            playbook = form.playbook.data,
                            users = userobj,
                            project = form.project.data,
                            inventory = form.inventory.data,
                            credential = form.credential.data,
                            tags = form.tags.data)
        db.session.add(task)
        flash('Orion has been created.')
        return redirect(url_for('ansible.listorion'))
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/create-orion.html', form=form)

@ansible.route('/edit-orion/<int:id>', methods=['GET','POST'])
@login_required
def edit_orion(id):
    edittask=Task.query.get_or_404(id)
    form=TaskForm()
    if form.validate_on_submit():
        edittask.name = form.name.data
        edittask.description = form.description.data
        edittask.playbook = form.playbook.data
        edittask.project = form.project.data
        edittask.inventory = form.inventory.data
        edittask.credential = form.credential.data
        edittask.tags = form.tags.data
        db.session.commit()
        flash('Orion has been updated.')
        return redirect(url_for('ansible.listorionk'))
    form.name.data = edittask.name
    form.description.data = edittask.description
    form.tags.data = edittask.tags
    return render_template('ansible/edit-orion.html', form=form)

@ansible.route('/listorion', methods=['GET','POST'])
@login_required
def listorion():
    task = Task.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    baseurl="http://200.12.221.13:5005/create-result"
    return render_template('ansible/task.html', tasks=task, baseurl=baseurl)

@ansible.route('/gettraceroute', methods=['GET','POST'])
@login_required
def gettraceroute():
    task = Task.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    baseurl="http://200.12.221.13:5005/create-result"
    return render_template('ansible/traceroute.html', tasks=task, baseurl=baseurl)

@ansible.route('/runtraceroute', methods=['GET','POST'])
@login_required
def runtraceroute():
    if request.method == 'POST':
        resultid=str(request.form['ip'])
        playbookName = 'tracerouteip.yml'
        inventory = 'tracerouteinv'
        stdoutfile = '/etc/ansiblestdout/traceroute.out'
        # retdata = {'value':stdoutfile}
       playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
       Output=playbook.runPlaybook()
        target = open('/home/davis/Documents/Network-automation/tracerouteinv', 'w')
        target.write('[routerxe]')
        target.write("\n")
        target.write('10.10.10.102')
        fileRead=open(stdoutfile)
        Output=fileRead.read()
        # print Output
        Output=Output.replace("[0;32m","")
        Output=Output.replace("[0;31m","")
        Output=Output.replace("[0m"," ")
        Output=Output.replace("\x1b"," ")
        retdata={'value':Output}
        return jsonify(retdata)

    ret_data={'value':"use post with args result"}
    return jsonify(ret_data)



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
        target = open('/home/davis/Documents/Network-automation/inventory', 'w')
        target.write('[routerxe]')
        target.write("\n")
        target.write(variables)
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
        editinventory.name = form.name.data
        editinventory.description = form.description.data
        editinventory.file = form.file.data
        editinventory.tags = form.tags.data
        editinventory.variables = form.variables.data
        db.session.commit()

        target = open('/home/davis/Documents/Network-automation/inventory', 'w')
        target.write('[routerxe]')
        target.write("\n")
        target.write(form.variables.data)

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
    return render_template('ansible/create-project.html', form=form)

@ansible.route('/edit-project/<int:id>', methods=['GET','POST'])
@login_required
def edit_project(id):
    editproject=Project.query.get_or_404(id)
    form=InventoryForm()
    if form.validate_on_submit():
        editproject.name = form.name.data
        editproject.tags = form.tags.data
        editproject.projectdir = form.projectdir.data
        editproject.description = form.description.data
        db.session.commit()
        flash('Project has been updated.')
        return redirect(url_for('ansible.listproject'))
    form.name.data = editproject.name
    form.description.data = editproject.description
    form.tags.data = editproject.tags
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
                            project = form.project.data,
                            inventory = form.inventory.data,
                            credential = form.credential.data,
                            tags = form.tags.data)
        db.session.add(task)
        flash('Task has been created.')
        return redirect(url_for('ansible.listtask'))
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/create-task.html', form=form)

@ansible.route('/edit-task/<int:id>', methods=['GET','POST'])
@login_required
def edit_task(id):
    edittask=Task.query.get_or_404(id)
    form=TaskForm()
    if form.validate_on_submit():
        edittask.name = form.name.data
        edittask.description = form.description.data
        edittask.playbook = form.playbook.data
        edittask.project = form.project.data
        edittask.inventory = form.inventory.data
        edittask.credential = form.credential.data
        edittask.tags = form.tags.data
        db.session.commit()
        flash('Task has been updated.')
        return redirect(url_for('ansible.listtask'))
    form.name.data = edittask.name
    form.description.data = edittask.description
    form.tags.data = edittask.tags
    return render_template('ansible/edit-task.html', form=form)

@ansible.route('/listtask', methods=['GET','POST'])
@login_required
def listtask():
    task = Task.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    baseurl="http://200.12.221.13:5005/create-result"
    return render_template('ansible/task.html', tasks=task, baseurl=baseurl)

@ansible.route('/create-result', methods=['GET','POST'])
@login_required
def create_result():
    status = request.args.get('status')
    finished = datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S')
    playbook = request.args.get('playbook')
    tags = request.args.get('tags')
    inventory = request.args.get('inventory')
    credential = request.args.get('credential')
    task_id = request.args.get('taskid')
    timestamp = datetime.utcnow().strftime('%s')
    taskobj = Task.query.filter_by(id=int(task_id)).first()

    outpath = request.args.get('outpath')
    userobj = User.query.filter_by(id=int(current_user.id)).first()

    result=Result(status = status,
                    finished = finished,
                    # timestamp = timestamp,
                    playbook = playbook,
                    inventory = inventory,
                    credential = credential,
                    users = userobj,
                    outfile = outpath,
                    task = taskobj,
                    tags = tags)
    db.session.add(result)

    target = open('/home/davis/Documents/Network-automation/sharedvalues.yaml', 'w')
    target.write('---')
    target.write("\n")
    target.write('guivars: /etc/ansiblefacts/'+tags)

    resultid = Result.query.order_by(desc(Result.id)).first()
    flash('Result has been created.')
    return render_template('playoutput.html', resultid=resultid.id)

@ansible.route('/rerunresult', methods=['GET','POST'])
@login_required
def rerunresult():
    resultid = request.args.get('id')
    result = Result.query.get_or_404(resultid)
    status = result.status
    finished = datetime.utcnow().strftime('%Y-%m-%d  %H:%M:%S')
    playbook = result.playbook
    tags = result.tags
    inventory = result.inventory
    credential = result.credential
    ### change project_id name to task_id
    task_id = result.project_id
    timestamp = datetime.utcnow().strftime('%s')
    taskobj = Task.query.filter_by(id=int(task_id)).first()

    userobj = User.query.filter_by(id=int(current_user.id)).first()

    result=Result(status = status,
                    finished = finished,
                    # timestamp = timestamp,
                    playbook = playbook,
                    inventory = inventory,
                    credential = credential,
                    users = userobj,
                    task = taskobj,
                    tags = tags)
    db.session.add(result)

    resultid = Result.query.order_by(desc(Result.id)).first()
    flash('Result has been created.')
    return render_template('playoutput.html', resultid=resultid.id)

@ansible.route('/generateresultout', methods=['GET','POST'])
@login_required
def dispresultoutput():
    resultid = request.args.get('id')
    # flash('Result has been created.')
    return render_template('dispoutput.html', resultid=resultid)


@ansible.route('/listresult', methods=['GET','POST'])
def listresult():
    result = Result.query.order_by(desc(Result.id)).all()
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
