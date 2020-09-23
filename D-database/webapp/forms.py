from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,Length
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired


class Upload(FlaskForm):
	name = StringField("",validators=[DataRequired()])
	file = FileField("",[FileAllowed(['jpg','jpeg'])])
	submit = SubmitField("Upload",render_kw={"id":"login","class":"btn btn-success"})

class SignUp(FlaskForm):
	email = StringField("",validators=[DataRequired(),Email()],render_kw={"placeholder":"E-mail","id":"ip"})
	username = StringField("",validators=[DataRequired()],render_kw={"placeholder":"Username","id":"ip"})
	password= PasswordField("",validators=[DataRequired(),Length(min=8,max=32,message=('Password length must be min of 8 characters and maximum of 32 characters and must contain minimum of 1 Upeer case,1 digit and must include special characters'))],render_kw={"placeholder":"Password","id":"ip"})
	submit = SubmitField("Sign Up",render_kw={"placeholder":"Sign Up","id":"su","class":"btn btn-primary"})

class Editor(FlaskForm):
    code=TextAreaField("")
    compitle=SubmitField("Submit")
