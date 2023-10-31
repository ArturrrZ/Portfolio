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

if __name__ == "__main__":
    app.run(debug=True)