from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError

class InventoryForm(Form):
    name = StringField('Inventory Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    file = StringField('Inventory File', validators=[Length(0, 64)])
    variables = TextAreaField('Variables')
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')


class ProjectForm(Form):
    name = StringField('Project Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')

class TaskForm(Form):
    name = StringField('Task Name', validators=[Length(0, 64)])
    description = StringField('Description', validators=[Length(0, 64)])
    path = StringField('Path File', validators=[Length(0, 64)])
    playbook = TextAreaField('Playbook')
    tags = TextAreaField('Tags')
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')
