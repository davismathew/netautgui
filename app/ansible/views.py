from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from .forms import InventoryForm, ProjectForm, TaskForm
from . import ansible
from .. import db
from ..models import Inventory, Post, Project, Task, Result


@ansible.route('/create-inventory', methods=['GET','POST'])
@login_required
def create_inventory():
    form=InventoryForm()
    if form.validate_on_submit():
        inventory=Inventory(name = form.name.data,
                            description = form.description.data,
                            file = form.file.data,
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
                            variables = form.variables.data)
        db.session.add(inventory)
        flash('Inventory has been updated.')
        return redirect(url_for('ansible.listinventory'))
    form.name.data = editinventory.name
    form.description.data = editinventory.description
    form.file.data = editinventory.file
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
        project=Project(name = form.name.data,
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
        task=Task(name = form.name.data,
                            description = form.description.data,
                            path = form.path.data,
                            playbook = form.playbook.data,
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
    return render_template('ansible/task.html', tasks=task)

@ansible.route('/listresult', methods=['GET','POST'])
@login_required
def listresult():
    result = Result.query.all()
    # form.name.data = current_user.name
    # form.description.data = current_user.location
    # form.file.data = current_user.about_me
    return render_template('ansible/result.html', results=result)


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
