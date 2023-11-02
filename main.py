from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import smtplib
import os

SENDER = os.environ.get("SENDER")
PASSWORD=os.environ.get("PASSWORD")
#email address where you want to get notification ⬇️
RECEIVER = "arturziianbaev@gmail.com"

class ContactForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "arturziianbaev@gmail.com"})
    name = StringField(label='Name:', validators=[DataRequired(), ],
                       render_kw={"placeholder": "Artur Ziianbaev"})
    message = StringField(label='Your message:', validators=[DataRequired(), Length(min=5)],
                          render_kw={"placeholder": "Hi, my name is Artur Ziianbaev. I like your portfolio and ..."})
    submit=SubmitField(label='Submit')


app=Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] ="asd"
app.config['SQLALCHEMY_DATABASE_URI'] =('sqlite:///projects.db')
db = SQLAlchemy()
db.init_app(app)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=False, nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    check_url = db.Column(db.String(500), nullable=False)
    github_url = db.Column(db.String(500), nullable=False)
    category=db.Column(db.String(500),nullable=False)
    picture=db.Column(db.String(500),nullable=False)

def add_project():
    new_project=Projects(
        title="My knowledge in DS",
        subtitle="In the link below you can check some projects according to Data Science. I did them using Google Colab",
        check_url="https://github.com/ArturrrZ/DataScience",
        github_url="https://github.com/ArturrrZ/DataScience",
        category="datascience",
        picture="./static/assets/img/data_science.jpg",
    )
    db.session.add(new_project)
    db.session.commit()


with app.app_context():
    db.create_all()
    #undo to add a new project to db
    # add_project()


@app.route("/")
def home():
    return render_template('index.html')
@app.route("/dont",methods=['GET','POST'])
def dont():
    patrick=False
    if request.method == 'POST':
        patrick=True
        return render_template('dont.html',patrick=patrick)
    return render_template('dont.html')

@app.route("/projects")
def projects():
    result= db.session.execute(db.select(Projects).order_by(Projects.id))
    projects=result.scalars()
    # for _ in range(20):
    #     list.append(_)
    return render_template('projects.html',projects=projects)

@app.route("/contact",methods=['POST','GET'])
def contact():
    form=ContactForm()
    if form.validate_on_submit():
        email=form.email.data
        name=form.name.data
        message=form.message.data
        with smtplib.SMTP('smtp.gmail.com') as connection:

            connection.starttls()
            connection.login(user=SENDER,
                             password=PASSWORD)
            connection.sendmail(
                from_addr=SENDER,
                to_addrs=RECEIVER,
                msg=f"Subject:Portfolio\n\nHere is the message from {name} his/her email: {email}.\nMessage: {message}"
            )
        return render_template('contact.html')


    return render_template('contact.html',form=form)

if __name__ == "__main__":
    app.run(debug=True)