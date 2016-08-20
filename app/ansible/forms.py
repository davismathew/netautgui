from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Inventory, Post, Project, Task, Result
import os
from .ansible_utils import project_path

class InventoryForm(Form):
    name = StringField('Inventory Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    tags = StringField('Tags', validators=[Length(0, 64)])
    file = StringField('Inventory File', validators=[Length(0, 64)])
    variables = TextAreaField('Variables')
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')


class ProjectForm(Form):
    files=project_path('project')
    name = StringField('Project Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    tags = StringField('Tags', validators=[Length(0, 64)])
    projectdir = SelectField('Projects', choices=[(file,file) for file in files])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')


class TaskForm(Form):
    inventories = Inventory.query.all()
    projects = Project.query.all()
    files=[]
    temp=os.listdir("/home/davis/Documents/Network-automation")
    for file in temp:
        if file.endswith(".yml"):
            files.append(file)
    name = StringField('Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    tags = StringField('factfile', validators=[Length(0, 64)])
    playbook = SelectField('Playbook', choices=[(file,file) for file in files])
    project = QuerySelectField(get_label='name',query_factory=lambda : Project.query.all())
    # project = SelectField('Project', choices=[(pro.name,pro.name) for pro in projects])
    inventory = QuerySelectField(get_label='name',query_factory=lambda : Inventory.query.all())
    # inventory = SelectField('Inventory', choices=[(inv.name,inv.name) for inv in inventories])
    credential = QuerySelectField(get_label='name',query_factory=lambda : Inventory.query.all())
    credential = SelectField('Credentials', choices=[(inv.name,inv.name) for inv in inventories])
    submit = SubmitField('Submit')
    Run = SubmitField('Run')
