from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from datetime import timedelta

engine = create_engine("mysql+pymysql://root:stea1chamalie@localhost/register?host=localhost?port=3306")

db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        
        req = request.form

        username = request.form.get("username")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT username FROM officer WHERE username=:username",{"username":username}).fetchone()
        passworddata = db.execute("SELECT password FROM officer WHERE username=:username",{"username":username}).fetchone()
        admindata = db.execute("SELECT role FROM officer WHERE username=:username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("No username","danger")
            return render_template("login.html")
         
        elif username == usernamedata['username'] and password == passworddata['password'] and admindata['role'] == 'admin':
            session["USERNAME"] = usernamedata["username"]
            
            flash("you are loggin as an admin","success")
            return redirect (url_for('admin')) 

        elif username == usernamedata['username'] and password == passworddata['password'] and admindata['role'] == 'idcard':
            flash("you are loggin as an officer in the identification card department","success")
            return redirect (url_for('idcard'))

        elif username == usernamedata['username'] and password == passworddata['password'] and admindata['role'] == 'passport':
            flash("you are loggin as an officer the passport department","success")
            return redirect (url_for('passport'))
        elif username == usernamedata['username'] and password == passworddata['password'] and admindata['role'] == 'permit':
            flash("you are loggin as an officer in the permit department","success")
            return redirect (url_for('permit'))
        elif username == usernamedata['username'] and password == passworddata['password'] and admindata['role'] == 'visa':
            flash("you are loggin as an officer in the visa department","success")
            return redirect (url_for('visa'))
                     
        else:
            flash("incorrect password")
            return render_template("login.html")
  
    return render_template("login.html")

#ADMIN
@app.route("/admin",methods=["GET","POST"])
def admin():
    if session.get('USERNAME', None) is not None:
        username = session.get("USERNAME")
        user = username
        return render_template("admin.html", user=user)
    else:
        print("user not found in session")
        return redirect(url_for('login'))

@app.route("/reg_officer", methods=["GET","POST"])
def reg_officer():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        password = request.form.get("password")
        address = request.form.get("address")
        role = request.form.get("role")
        phone_number = request.form.get("phone_number")

        db.execute("INSERT INTO officer(fname, lname, username, password, address, role, phone_number) VALUES(:fname, :lname, :username, :password, :address, :role, :phone_number)",{"fname":fname,"lname":lname,"username":username,"password":password,"address":address,"role":role,"phone_number":phone_number,})
        data = db.commit()
        flash("you have successfully registerd the officer ","success")

    return render_template("reg_officer.html", data = officers)

@app.route("/officers",methods=["GET","POST"])
def officers():
    cur = db.execute("SELECT * FROM officer")
    data = cur.fetchall()
    cur.close()

    return render_template("officers.html", officer = data)

@app.route("/idcard",methods=["GET","POST"])
def idcard():
    cur = db.execute("SELECT * FROM national_id")
    data = cur.fetchall()
    cur.close()

    return render_template("idcard.html", national_id = data)

@app.route("/passport",methods=["GET","POST"])
def passport():  
    cur = db.execute("SELECT * FROM passport")
    data = cur.fetchall()
    cur.close()

    return render_template("passport.html", passport = data)

@app.route("/permit",methods=["GET","POST"])
def permit():  
    cur = db.execute("SELECT * FROM permit")
    data = cur.fetchall()
    cur.close()

    return render_template("permit.html", permit = data)

@app.route("/visa",methods=["GET","POST"])
def visa():  
    cur = db.execute("SELECT * FROM visa")
    data = cur.fetchall()
    cur.close()

    return render_template("visa.html", visa = data)

@app.route("/update_password",methods=["GET","POST"])
def update_password():
    if request.method == 'POST':

       oldpassword = request.form.get("oldpassword")
       newpassword = request.form.get("newpassword")
       confirmpassword = request.form.get("confirmpassword")

       if newpassword == confirmpassword:

            cur = db.execute("UPDATE password FROM users WHERE  password=:oldpassword",{"password":oldpassword}).fetchone()
            data = db.commit()
            flash("you have successfully registerd the officer ","success")
        
    return render_template("update_password.html", users = data)

#LOGOUT
@app.route("/logout")
def logout():
    session.pop("USERNAME", None)
    flash("you are now logout","success")
    return redirect(url_for('login'))

if __name__=='__main__':
    app.secret_key="123stea"
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.run(debug=True)