from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap5


app=Flask(__name__)
Bootstrap5(app)
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
    list=[]
    for _ in range(20):
        list.append(_)
    return render_template('projects.html',projects=list)

if __name__ == "__main__":
    app.run(debug=True)