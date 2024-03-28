from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(message="This field cannot be empty")])
    password = PasswordField(label="Password", validators=[DataRequired(message="This field cannot be empty")])
    name = StringField(label="Name", validators=[DataRequired(message="This field cannot be empty")])
    submit = SubmitField("SIGN ME UP!")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(message="This field cannot be empty")])
    password = PasswordField(label="Password", validators=[DataRequired(message="This field cannot be empty")])
    submit = SubmitField("LET ME IN!")


# TODO: Create a CommentForm so users can leave comments below posts

class CommentForm(FlaskForm):
    comment_text = CKEditorField(label='Comment', validators=[DataRequired(message="This field cannot be empty")])
    submit = SubmitField("SUBMIT COMMENT")