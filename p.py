from flask import Flask
from flask import request,render_template,redirect,url_for
import sqlite3
import datetime
app=Flask(__name__)

@app.route("/",methods=["GET"])
def func():
   connect=sqlite3.connect('p.db')
   cursor=connect.cursor() 
   cursor.execute("""CREATE TABLE IF NOT EXISTS user(
    id integer primary key,
    name text,
    password integer)
    ;""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS poll(
id integer primary key,
name text,
user_id integer,
choice_1 text,
choice_2 text,
choice_3 text,
c1 integer,
c2 integer,
c3 integer,
result text,
dt datetime default current_timestamp,
foreign key(user_id)references user(id)
)
    ;""")
   return render_template("index.html")
 
def max(a,b,c):
 if(a>=b and a>=c):
  return a
 elif(b>=a and b>=c):
  return b
 elif(c>=a and c>=b):
  return c
 return 1
 
d=dict()

@app.route("/signin", methods=["POST"])
def fun():
   return render_template("login.html")

@app.route("/<poll>/result",methods=["GET","POST"])
def result(poll):
   connect=sqlite3.connect('p.db')
   cursor=connect.cursor()
   cursor.execute("""select choice_1,choice_2,choice_3,c1,c2,c3,result,dt from POLL where name=?""",[poll])
   p=cursor.fetchone()
   choice_1,choice_2,choice_3,c1,c2,c3,result,t=p;
   print(p)
   return render_template("v.html",name=poll,c1=c1,c2=c2,c3=c3,choice_1=choice_1,choice_2=choice_2,choice_3=choice_3,result=result,t=t)
   
@app.route("/<poll>/result_",methods=["GET","POST"])
def result_(poll):
   connect=sqlite3.connect('p.db')
   cursor=connect.cursor()
   cursor.execute("""select dt from POLL where name=?""",[poll])
   p=cursor.fetchone()
   l=p
   print(str(l[0]))
   print(str(datetime.date.today()))
   if str(datetime.date.today())>str(l[0]):
     return render_template("Time.html")
   c=request.form['c']
   print(c)
   d[c]=d[c]+1
   print(d)
   l=list(d)
   c1=d[l[0]]
   c2=d[l[1]]
   c3=d[l[2]]
   k=max(c1,c2,c3)
   for i in range(0,3):
    if(d[l[i]]==k):
     result=l[i]
   cursor.execute("""UPDATE POLL set c1=?,c2=?,c3=?,result=? where name=?""",[c1,c2,c3,result,poll])
   connect.commit()
   cursor.execute("""select name,choice_1,choice_2,choice_3,c1,c2,c3,result from POLL where name=?""",[poll])
   p=cursor.fetchone()
   name,choice_1,choice_2,choice_3,c1,c2,c3,result=p
   return render_template("Thank.html")
   
@app.route("/<id_>/c",methods=["GET","POST"])
def c(id_):
 print(id_)
 return render_template("create.html",id_=id_)  
 
@app.route("/<id_>/v",methods=["GET","POST"])
def f(id_):
   connect=sqlite3.connect('p.db')
   cursor=connect.cursor()
   cursor.execute("""select name from POLL where user_id=?""",[id_])
   p=cursor.fetchall()
   print(p)
   return render_template("view.html",poll=p)
   
@app.route("/<poll>/share" ,methods=["GET"])
def share(poll):
   connect=sqlite3.connect('p.db')
   cursor=connect.cursor()
   cursor.execute("""select choice_1,choice_2,choice_3,dt from POLL where name=?""",[poll])
   p=cursor.fetchone()
   c1,c2,c3,l=p
   print(str(l))
   if str(datetime.date.today())>str(l):
    return """TIME FOR POLL ENDED"""
   return render_template("create1.html",c1=c1,c2=c2,c3=c3,poll=poll)
  
@app.route("/<id_>/create",methods=["GET","POST"])
def create_poll(id_):
   pollname=request.form['name']
   choice1=request.form['c1']
   choice2=request.form['c2']
   choice3=request.form['c3']
   t=request.form['t']
   id_=request.form['id_']
   connect=sqlite3.connect('p.db')
   cursor=connect.cursor()
   cursor.execute("""INSERT INTO POLL(name,user_id,choice_1,choice_2,choice_3,dt)values(?,?,?,?,?,?)""",[pollname,id_,choice1,choice2,choice3,t])
   connect.commit()
   d.clear()
   d[choice1]=0
   d[choice2]=0
   d[choice3]=0
   return render_template("create1.html",c1=choice1,c2=choice2,c3=choice3,poll=pollname)
   
@app.route("/signup",methods=["GET","POST"])
def signup():
       return render_template("signup.html")
       
@app.route("/signup_",methods=["POST"])
def signup_():
       connect=sqlite3.connect('p.db')
       cursor=connect.cursor()
       username = request.form['name'] 
       password = request.form['pass'] 
       cursor.execute("""INSERT INTO USER(name,password)values(?,?)""",[username,password])
       connect.commit()
       cursor.execute("""select id from user where name=? and password=?""",[username,password])
       q=cursor.fetchone()
       return render_template('display.html',name=username,pass_=password,id_=q[0])
     


@app.route("/login", methods=["POST"])
def login() :    
       connect=sqlite3.connect('p.db')
       cursor=connect.cursor()
       username = request.form['name'] 
       password = request.form['pass'] 
       cursor.execute("""select name from user where name=? and password=?""",[username,password])
       p=cursor.fetchall()
       cursor.execute("""select id from user where name=? and password=?""",[username,password])
       q=cursor.fetchone()
       if (len(p)):
         return render_template('display.html',name=username,pass_=password,id_=q[0])
       else:
         return redirect('signup')



  
if __name__=='__main__':
  app.run()


