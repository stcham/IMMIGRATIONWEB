from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt as sha256_crypt

engine = create_engine("mysql+pymysql://root:stea1chamalie@localhost/register?host=localhost?port=3306")

db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")
#REGISTER
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("INSERT INTO users(name, username, password) VALUES(:name,:username,:password)",{"name":name,"username":username,"password":password})
            db.commit()
            flash("you are now registered and can login","success")
            return redirect(url_for('login'))
        else:
            flash("password does not match","danger")
            return render_template("register.html")    


    return render_template("register.html")
#LOGIN
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passworddata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("No username","danger")
            return render_template("login.html")
        else:
            for password_data in passworddata:
                if sha256_crypt.verify(password, password_data):
                    session["log"] = True

                    flash("you are now login","success")
                    return redirect(url_for('options'))
                else:
                   flash("incorrect password","danger")
                   return render_template("login.html")
    return render_template("login.html")
#OPTIONS
@app.route("/options")
def options():
    return render_template("options.html")

#LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    flash("you are now logout","success")
    return redirect(url_for('login'))

#NATIONAL ID
@app.route("/nationalid",methods=["GET","POST"])
def nationalid():
    if request.method == "POST":
        title = request.form.get("title")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        number = request.form.get("number")
        address = request.form.get("address")
        DoB = request.form.get("DoB")
        PoB = request.form.get("PoB")
        file = request.form.get("file")

        db.execute("INSERT INTO national_id(title, fname, lname, number, address, DoB, PoB, file) VALUES(:title, :fname, :lname, :number, :address, :DoB, :PoB, :file)",{"title":title,"fname":fname,"lname":lname,"number":number,"address":address,"DoB":DoB,"PoB":PoB,"file":file,})
        db.commit()
        flash("you have successfully submitted your application for national ID","success")

    return render_template("nationalid.html")

#PASSPORT
@app.route("/passport",methods=["GET","POST"])
def passport():
    if request.method == "POST":
        title = request.form.get("title")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        number = request.form.get("number")
        address = request.form.get("address")
        DoB = request.form.get("DoB")
        PoB = request.form.get("PoB")
        file = request.form.get("file")

        db.execute("INSERT INTO passport(title, fname, lname, number, address, DoB, PoB, file) VALUES(:title, :fname, :lname, :number, :address, :DoB, :PoB, :file)",{"title":title,"fname":fname,"lname":lname,"number":number,"address":address,"DoB":DoB,"PoB":PoB,"file":file,})
        db.commit()
        flash("you have successfully submitted your application for passport","success")
    return render_template("passport.html")

#PERMIT
@app.route("/permit",methods=["GET","POST"])
def permit():
    if request.method == "POST":
        title = request.form.get("title")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        number = request.form.get("number")
        address = request.form.get("address")
        DoB = request.form.get("DoB")
        PoB = request.form.get("PoB")
        file = request.form.get("file")

        db.execute("INSERT INTO permit(title, fname, lname, number, address, DoB, PoB, file) VALUES(:title, :fname, :lname, :number, :address, :DoB, :PoB, :file)",{"title":title,"fname":fname,"lname":lname,"number":number,"address":address,"DoB":DoB,"PoB":PoB,"file":file,})
        db.commit()
        flash("you have successfully submitted your application for permit","success")

    return render_template("permit.html")

#VISA
@app.route("/visa",methods=["GET","POST"])
def visa():
    if request.method == "POST":
        title = request.form.get("title")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        number = request.form.get("number")
        address = request.form.get("address")
        DoB = request.form.get("DoB")
        PoB = request.form.get("PoB")
        file = request.form.get("file")
    

        db.execute("INSERT INTO visa(title, fname, lname, number, address, DoB, PoB, file) VALUES(:title, :fname, :lname, :number, :address, :DoB, :PoB, :file)",{"title":title,"fname":fname,"lname":lname,"number":number,"address":address,"DoB":DoB,"PoB":PoB,"file":file,})
        db.commit()
        flash("you have successfully submitted your application for enterance visa","success")

    return render_template("visa.html")

if __name__=='__main__':
    app.secret_key="12345stea"
    app.run(debug=True)
