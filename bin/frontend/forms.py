from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class InsertForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    id = IntegerField('id')
    level = IntegerField('level')
    steps = IntegerField('steps')
    type = StringField('type')
    out = StringField('out')
    url = StringField('url', validators=[DataRequired()])
    submit = SubmitField('Submit')
