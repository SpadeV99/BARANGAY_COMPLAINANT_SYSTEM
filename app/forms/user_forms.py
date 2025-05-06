from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RoleForm(FlaskForm):
    role = SelectField('Role', choices=[('resident', 'Resident'), ('staff', 'Staff'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class DeleteUserForm(FlaskForm):
    confirmation = StringField('Type DELETE to confirm', validators=[DataRequired()])
    submit = SubmitField('Delete User')

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact_number = StringField('Contact Number')
    address = TextAreaField('Address')
    role = SelectField('Role', choices=[
        ('resident', 'Resident'), 
        ('staff', 'Staff'), 
        ('admin', 'Admin')
    ], validators=[DataRequired()])
    submit = SubmitField('Create User')