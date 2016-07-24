from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Inventory, Post, Project, Task, Result
import os

class InventoryForm(Form):
    name = StringField('Inventory Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    file = StringField('Inventory File', validators=[Length(0, 64)])
    variables = TextAreaField('Variables')
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')


class ProjectForm(Form):
    files=os.listdir("/var/lib/emc")
    name = StringField('Project Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    projectdir = SelectField('Projects', choices=[(file,file) for file in files])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')


class TaskForm(Form):
    files=[]
    temp=os.listdir("/var/lib/emc/networkaut")
    for file in temp:
        if file.endswith(".yml"):
            files.append(file)
    name = StringField('Task Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    path = StringField('Path File', validators=[Length(0, 64)])
    playbook = TextAreaField('Playbook')
    taskdir = SelectField('Tasks', choices=[(file,file) for file in files])
    tags = TextAreaField('Tags')
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')
