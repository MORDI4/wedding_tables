from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired

class TableForm(FlaskForm):
    table_num = IntegerField('table_num', validators=[DataRequired()])
    guests = TextAreaField('guest', validators=[DataRequired()])