from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
Bootstrap5(app)

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

@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)