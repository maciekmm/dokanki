from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators, FileField
from wtforms.validators import DataRequired


class InsertForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    id = IntegerField('id', validators=(validators.Optional(),))
    level = IntegerField('level', validators=(validators.Optional(),))
    steps = IntegerField('steps', validators=(validators.Optional(),))
    type = StringField('type', validators=(validators.Optional(),))
    out = StringField('out', validators=(validators.Optional(),))
    url = StringField('url', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    id = IntegerField('id', validators=(validators.Optional(),))
    level = IntegerField('level', validators=(validators.Optional(),))
    steps = IntegerField('steps', validators=(validators.Optional(),))
    type = StringField('type', validators=(validators.Optional(),))
    out = StringField('out', validators=(validators.Optional(),))
    file = FileField('file', validators=[DataRequired()])
    submit = SubmitField('Submit')
