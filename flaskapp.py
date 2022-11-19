from cgitb import html
from flask import Flask, render_template, request , redirect
# from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Loaddata.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Loaddata(db.Model):
    slno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    # date_Time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.slno} - {self.title}"

@app.route('/', methods = ['GET','POST'])

def hello():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']    
        ld = Loaddata(title = title, desc = desc)
        db.session.add(ld)
        db.session.commit()
        
    
    allld = Loaddata.query.all()
    return render_template("index.html", allld = allld)

@app.route('/delete/<int:slno>')

def delete(slno):
    ld = Loaddata.query.filter_by(slno = slno).first()
    db.session.delete(ld)
    db.session.commit()

    return redirect("/")


@app.route('/update/<int:slno>',methods = ['GET','POST'])
def update(slno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        ld = Loaddata.query.filter_by(slno = slno).first()
        ld.title = title
        ld.desc = desc
        db.session.add(ld)
        db.session.commit()

        return redirect("/")

    ld = Loaddata.query.filter_by(slno = slno).first()
    return  render_template("update.html",ld = ld)

@app.route('/deleteit', methods = ['GET','POST'])

def deleteit():
    if request.method == "POST":
        slno = request.form['slno']
        try:  
            ld  = Loaddata.query.filter_by(slno = slno).first()
            db.session.delete(ld)
            db.session.commit()
        except Exception as e:
            print(f"No slno exist. {e}")
        finally:
            return redirect("/")

    return render_template("deleteit.html")


if __name__ == "__main__":
    app.run(debug = True,port=8000)