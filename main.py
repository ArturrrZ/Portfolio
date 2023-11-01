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
        title="Atari Breakout",
        subtitle="Breakout is an arcade video game developed and published by Atari, Inc. and released on May 13, 1976.",
        check_url="https://replit.com/@ArturZiianbaev1/6BreakoutGame?v=1",
        github_url="https://github.com/ArturrrZ/Project_6_AtariBreakout_Game",
        category="arcade",
        picture="./static/assets/img/atari.jpg",
    )
    db.session.add(new_project)
    db.session.commit()


with app.app_context():
    db.create_all()
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

if __name__ == "__main__":
    app.run(debug=True)