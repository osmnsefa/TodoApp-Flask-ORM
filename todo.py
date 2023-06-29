from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Asus/OneDrive/Masaüstü/python/python ders udemy/todo app/todo.db"
# initialize the app with the extension
db=SQLAlchemy(app)
@app.route("/")
def index():
    todos=Todo.query.all() #verileri alıp sözlük şeklinde todos'a gönderdik.
    return render_template("index.html",todos=todos)
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo=Todo.query.filter_by(id=id).first()#id'si gönderdiğimizi id'e eşit olan veriyi aldık.
    
    todo.complete=todo.complete=not todo.complete # burda değerimizi true ise false'a,false ise true'ya çevirdik.
    
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo=Todo.query.filter_by(id=id).first()#id'si gönderdiğimizi id'e eşit olan veriyi aldık.
    
    db.session.delete(todo)
    
    db.session.commit()
    return redirect(url_for("index"))
    
@app.route("/add",methods=["POST"])# Sadece post request almasını istedik.
def addTodo():
    title=request.form.get("title") #title name'ine sahip değeri aldık.
    newTodo=Todo(title=title,complete=False)
    db.session.add(newTodo) #objemizi databese'e ekledik.
    db.session.commit() # veri tabanına ekleme yaptığımız için commit ettik.
    return redirect(url_for("index"))
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    complete =db.Column(db.Boolean)
if __name__=="__main__":
    with app.app_context():
        db.create_all() # Tabloları veri tabanına kaydettik.
    app.run(debug=True) # Eğer tablo kayıtlı ise bir daha kaydetmez.
