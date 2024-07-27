#Modules

from tkinter import *
import mysql.connector
import random, math
from email.message import EmailMessage
import ssl,smtplib
import datetime

#Connection to MySQL

obj=mysql.connector.connect(host='localhost',user='root',password='7159')
obj.autocommit=True
c=obj.cursor()

#Check for Database

c.execute("SHOW DATABASES;")
db=c.fetchall()
if ("project",) not in db:
    c.execute('CREATE DATABASE PROJECT;')
    c.execute('USE PROJECT;')
    c.execute('CREATE TABLE SCHOOLS(INITIAL VARCHAR(10) PRIMARY KEY, SCHOOL VARCHAR(50), EMAIL VARCHAR(30), PASSWORD VARCHAR(50));')

#Credentials for Email

sender="pytech.ae@gmail.com"
password="nzhapwiviyhasokr"

#Font Configuration

def font(item,size):
    return item.configure(font=("Cormorant Garamond Regular",size))
def reportfont(item):
    return item.configure(font=("Courier New",15))

#Package Creation for School Account (Database, Teacher Record)

def package(user):
    
    c.execute("CREATE DATABASE {};".format(user))
    c.execute("USE {};".format(user))
    c.execute("CREATE TABLE TEACHERS(ID INT PRIMARY KEY, NAME VARCHAR(20), SUBJECT VARCHAR(3), PASSWORD INT, CLASS CHAR(3));")
    c.execute("CREATE TABLE STUDENTS(ID INT PRIMARY KEY, NAME VARCHAR(20), DOB DATE, CLASS CHAR(1), STREAM CHAR(4), S1 VARCHAR(3), S2 VARCHAR(3), S3 VARCHAR(3), S4 VARCHAR(3), S5 VARCHAR(3));")
    c.execute("CREATE TABLE MARKS(ID INT PRIMARY KEY, S1 INT, S2 INT, S3 INT, S4 INT, S5 INT);")

#Label Deletion

def del_label():
    global text
    try:
        if text.winfo_exists():
            text.destroy()
    except:
        print()

#OTP Generation

def otp(user,receiver):
    
    global otp
    
    subject="OTP - A+ Systems"
    otp=random.randint(1000,9999)
    body="Username: "+user+"\nOTP: "+str(otp)
    
    em=EmailMessage()
    em['From']=sender
    em['To']=receiver
    em['Subject']=subject
    em.set_content(body)
    
    context=ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,password)
        smtp.sendmail(sender,receiver,em.as_string())
    

#Forgot Password Instance
    
def forgot_pass(win):
    
    #Password Change Instance
    
    def fchange(win):

        def ch():
            c.execute("USE PROJECT;")
            c.execute("SELECT INITIAL,EMAIL,PASSWORD FROM SCHOOLS;")
            d=c.fetchall()
            for i in d:
                if i1==i[0]:
                    if new.get()!=confirm.get():
                        del_label()
                        text=Label(f,text="New passwords are not matching",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
                    elif new.get() in [""," "] or confirm.get() in [""," "]:
                        del_label()
                        text=Label(f,text="Fields cannot be empty.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
                    elif new.get()==confirm.get():
                        c.execute("UPDATE SCHOOLS SET PASSWORD='{}' WHERE INITIAL='{}';".format(new.get(),i1))
                        text=Label(f,text="Password updated.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
            
        win.destroy()
        f=Tk()
        f.title("A+ Student Management Systems (Academic) - Forgot Password")
        f.resizable(0,0)
        
        bg=PhotoImage(file="bg/fchangepw.png")
        lbg=Label(f,i=bg)
        lbg.pack()
        lbg.image=bg
        
        new=Entry(f,bd=0,width=26,justify="center",show="*")
        font(new,20)
        new.place(x=788,y=352)
        
        confirm=Entry(f,bd=0,width=26,justify="center",show="*")
        font(confirm,20)
        confirm.place(x=788,y=442)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(f,image=sub,command=lambda:ch(),bd=0)
        sub_b.place(x=964,y=538)
        sub_b.button=sub
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(f,image=back,command=lambda:[login_school(f)],bd=0)
        back_b.place(x=70,y=70)
        back_b.button=back
        
        f.mainloop()
        
    #Verification Instance
    
    def veri():
        if o.get()==str(otp):
            fchange(forgot)
        else:
            del_label()
            text=Label(forgot,text="Incorrect OTP!",background="#F1EBE5")
            font(text,10)
            text.place(x=732,y=590)
    
    def send_otp():
        
        del_label()
        
        c.execute("USE PROJECT;")
        c.execute("SELECT INITIAL,EMAIL FROM SCHOOLS;")
        d=c.fetchall()
        
        emails={}
        flag=False
        
        for i in d:
            e={i[0]:i[1]}
            emails.update(e)
        for i in emails:
            if emails[i]!=email.get():
                continue
            else:
                flag=True
                global i1
                i1=i
                break
        if flag==False:
            del_label()
            text=Label(forgot,text="Account not found",background="#F1EBE5")
            font(text,10)
            text.place(x=732,y=590)
        else:
            otp("User",email.get())
            text=Label(forgot,text="OTP Sent!",background="#F1EBE5")
            font(text,10)
            text.place(x=732,y=590)
    
    win.destroy()
    forgot=Tk()
    forgot.title("A+ Student Management Systems (Academic) - Forgot Password")
    forgot.resizable(0,0)
    
    bg=PhotoImage(file="bg/forgot.png")
    lbg=Label(forgot,i=bg)
    lbg.pack()
    lbg.image=bg
    
    email=Entry(forgot,bd=0,width=26,justify="center")
    font(email,20)
    email.place(x=788,y=352)
    
    o=Entry(forgot,bd=0,width=26,justify="center")
    font(o,20)
    o.place(x=788,y=442)
    
    send=PhotoImage(file="buttons/send.png")
    send_b=Button(forgot,image=send,command=lambda:send_otp(),bd=0)
    send_b.place(x=788,y=538)
    send_b.button=send
    
    sub=PhotoImage(file="buttons/submit.png")
    sub_b=Button(forgot,image=sub,command=lambda:[veri()],bd=0)
    sub_b.place(x=964,y=538)
    sub_b.button=sub
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(forgot,image=back,command=lambda:[login_school(forgot)],bd=0)
    back_b.place(x=70,y=70)
    back_b.button=back
    
    forgot.mainloop()


#School Menu Instance

def menu_school(win,name):
    
    def add_teacher():
        
        def add():
            
            c.execute("USE {};".format(name))
            c.execute("SELECT * FROM TEACHERS;")
            d=c.fetchall()
                
            if len(d)==0:
                i=1
            else:
                i=d[-1][0]+1
            pw=random.randint(10000,99999)
            if nam.get() in [""," "] or subj.get() in [""," "] or cl.get() in [""," "]:
                text=Label(at,text="Record cannot be empty.")
                font(text,10)
                text.place(x=732,y=590)
            else:
                c.execute("INSERT INTO TEACHERS VALUES ({},'{}','{}',{},'{}');".format(i,nam.get(),subj.get(),pw,cl.get()))
                text=Label(at,text="Record Added")
                font(text,10)
                text.place(x=732,y=590)

        schmenu.destroy()
        at=Tk()
        at.title("A+ Student Management Systems (Academic)")
        at.resizable(0,0)
        
        bg=PhotoImage(file="bg/addteacher.png")
        lbg=Label(at,i=bg)
        lbg.pack()
        lbg.image=bg
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(at,image=sub,command=lambda:add(),bd=0)
        sub_b.place(x=876,y=540)
            
        cl=Entry(at,bd=0,width=13,justify="center",borderwidth=1)
        font(cl,20)
        cl.place(x=791,y=318)
        
        subj=Entry(at,bd=0,width=13,justify="center",borderwidth=1)
        font(subj,20)
        subj.place(x=954,y=318)
        
        nam=Entry(at,bd=1,width=26,justify="center")
        font(nam,20)
        nam.place(x=788,y=396)
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(at,image=back,command=lambda:[menu_school(at,name)],bd=0)
        back_b.place(x=70,y=70)
        
        at.mainloop()
    
    def view_teacher(name):
        
        def search(x):
            
            del_label()
            
            c.execute("USE {};".format(name))
            c.execute("SELECT * FROM TEACHERS;")
            d=c.fetchall()
            for i in d:
                if str(i[0])==x:
                    text=Label(vt,text=str(i),background="#F1EBE5")
                    font(text,20)
                    text.place(x=757,y=310)
                    break
            else:
                text=Label(vt,text="Record not found.",background="#F1EBE5")
                font(text,20)
                text.place(x=757,y=310)
        
        def modify(win,x):
            
            def mod():
                if nam.get() not in [""," "]:
                    c.execute("UPDATE TEACHERS SET NAME='{}' WHERE ID={};".format(nam.get(),x))
                elif subj.get() not in [""," "]:
                    c.execute("UPDATE TEACHERS SET SUBJECT='{}' WHERE ID={};".format(subj.get(),x))
                elif cl.get() not in [""," "]:
                    c.execute("UPDATE TEACHERS SET CLASS='{}' WHERE ID={};".format(cl.get(),x))
                text=Label(vt,text="Record Updated",background="#F1EBE5")
                font(text,10)
                text.place(x=732,y=590)
            
            win.destroy()
            vt=Tk()
            vt.title("A+ Student Management Systems (Academic) - {}".format(name))
            vt.resizable(0,0)
            
            bg=PhotoImage(file="bg/addteacher.png")
            lbg=Label(vt,i=bg)
            lbg.pack()
            lbg.image=bg
            
            sub=PhotoImage(file="buttons/submit.png")
            sub_b=Button(vt,image=sub,command=lambda:mod(),bd=0)
            sub_b.place(x=876,y=540)
            sub_b.button=sub
                
            cl=Entry(vt,bd=0,width=13,justify="center",borderwidth=1)
            font(cl,20)
            cl.place(x=791,y=318)
            
            subj=Entry(vt,bd=0,width=13,justify="center",borderwidth=1)
            font(subj,20)
            subj.place(x=954,y=318)
            
            nam=Entry(vt,bd=1,width=26,justify="center")
            font(nam,20)
            nam.place(x=788,y=396)
            
            back=PhotoImage(file="buttons/back.png")
            back_b=Button(vt,image=back,command=lambda:[menu_school(vt,name)],bd=0)
            back_b.place(x=70,y=70)
            back_b.button=back
            
            vt.mainloop()
        
        schmenu.destroy()
        vt=Tk()
        vt.title("A+ Student Management Systems (Academic) - {}".format(name))
        vt.resizable(0,0)
        
        bg=PhotoImage(file="bg/viewteacher.png")
        lbg=Label(vt,i=bg)
        lbg.pack()
        lbg.image=bg
        
        ID=Entry(vt,bd=1,width=26,justify="center")
        font(ID,20)
        ID.place(x=788,y=396)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(vt,image=sub,command=lambda:search(ID.get()),bd=0)
        sub_b.place(x=876,y=540)
        
        mod=PhotoImage(file="buttons/modify.png")
        modi=Button(vt,image=mod,command=lambda:modify(vt,ID.get()),bd=0)
        modi.place(x=876,y=489)
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(vt,image=back,command=lambda:[menu_school(vt,name)],bd=0)
        back_b.place(x=70,y=70)
        
        vt.mainloop()
        
    def change_pass(win):
        
        def ch():
            c.execute("USE PROJECT;")
            c.execute("SELECT INITIAL,PASSWORD FROM SCHOOLS;")
            d=c.fetchall()
            for i in d:
                if i[0]==name:
                    if old.get()!=i[1]:
                        del_label()
                        text=Label(change,text="Old password incorrect.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
                    elif new.get()!=confirm.get():
                        del_label()
                        text=Label(change,text="New passwords are not matching",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
                    elif old.get() in [""," "] or new.get() in [""," "] or confirm.get() in [""," "]:
                        del_label()
                        text=Label(change,text="Fields cannot be empty.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
                    elif i[1]==old.get() and new.get()==confirm.get():
                        c.execute("UPDATE SCHOOLS SET PASSWORD='{}' WHERE INITIAL='{}';".format(new.get(),name))
                        text=Label(change,text="Password updated.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
        
        win.destroy()
        change=Tk()
        change.title("A+ Student Management Systems (Academic) - Change Password")
        change.resizable(0,0)
        
        bg=PhotoImage(file="bg/changepw.png")
        lbg=Label(change,i=bg)
        lbg.pack()
        lbg.image=bg
        
        old=Entry(change,bd=0,width=26,justify="center",show='*')
        font(old,20)
        old.place(x=788,y=317)
        
        new=Entry(change,bd=0,width=26,justify="center",show='*')
        font(new,20)
        new.place(x=788,y=395)
        
        confirm=Entry(change,bd=0,width=26,justify="center",show='*')
        font(confirm,20)
        confirm.place(x=788,y=471)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(change,image=sub,command=ch,bd=0)
        sub_b.place(x=876,y=540)
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(change,image=back,command=lambda:[menu_school(change,name)],bd=0)
        back_b.place(x=70,y=70)
        
        change.mainloop()
    
    def generate_loc():
            
        c.execute("USE {};".format(name))
        c.execute("SELECT S.ID,S.NAME,S.CLASS,(M.S1+M.S2+M.S3+M.S4+M.S5)/5 FROM STUDENTS S,MARKS M WHERE S.ID=M.ID ORDER BY S.CLASS,S.NAME;")
        filename="LOC - "+name+".txt"
        loc=open(filename,"w")
        data=c.fetchall()
        lines=["List of Candidates\n","\n","ID\tName\t\t\t\tClass\tAgg%\t\tSignature\n"]
        for i in data:
            line=str(i[0])+"\t"+i[1]+"\t\t"+"12"+i[2]+"\t"+str(i[3])+"\t__________________________\n"
            lines.append(line)
        lines.append("\n")
        lines.append("\n_______________________")
        lines.append("\nSignature of Principal")
        loc.writelines(lines)
        text=Label(schmenu,text="LOC has been saved to local file.",background="#F1EBE5")
        font(text,10)
        text.place(x=732,y=590)

    win.destroy()
    schmenu=Tk()
    schmenu.title("A+ Student Management Systems (Academic) - {}".format(name))
    schmenu.resizable(0,0)
    
    bg=PhotoImage(file="bg/school menu.png")
    lbg=Label(schmenu,i=bg)
    lbg.pack()
    lbg.image=bg
    
    #Button: Add Teacher

    addteach=PhotoImage(file="buttons/addteach.png")
    addt=Button(schmenu,image=addteach,command=lambda:add_teacher(),bd=0)
    addt.place(x=752,y=228)

    #Button: View Teacher

    viewteach=PhotoImage(file="buttons/viewteach.png")
    viewt=Button(schmenu,image=viewteach,command=lambda:view_teacher(name),bd=0)
    viewt.place(x=752,y=333)

    #Button: Generate LOC

    dclass=PhotoImage(file="buttons/loc.png")
    class_b=Button(schmenu,image=dclass,command=generate_loc,bd=0)
    class_b.place(x=752,y=440)

    #Button: Change Password

    changepw=PhotoImage(file="buttons/changepw.png")
    cpw=Button(schmenu,image=changepw,command=lambda:change_pass(schmenu),bd=0)
    cpw.place(x=752,y=546)
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(schmenu,image=back,command=lambda:[schmenu.destroy(),start()],bd=0)
    back_b.place(x=70,y=70)
    
    schmenu.mainloop()

#Teacher Menu Instance
    
def menu_teacher(win,name,tchr):
    
    def add_student():
        
        def add():
            
            c.execute("USE {};".format(name))
            c.execute("SELECT CLASS FROM TEACHERS WHERE ID={};".format(tchr))
            classes=c.fetchall()
            for x in classes:
                if cl.get() not in x[0]:
                    text=Label(ast,text="You don't teach this division.",background="#F1EBE5")
                    font(text,10)
                    text.place(x=732,y=590)
                else:
                    c.execute("SELECT * FROM STUDENTS;")
                    d=c.fetchall()
                        
                    if len(d)==0:
                        i=1
                    else:
                        i=d[-1][0]+1
                    
                    if nam.get() in [""," "] or clicked.get() in ["Select Stream"] or cl.get() in [""," "] or dob.get() in [""," "]:
                        text=Label(at,text="Record cannot be empty.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)
                    else:
                        s1="ENG"
                        if clicked.get()=="pcmc":
                            s2='PHY'
                            s3='CHE'
                            s4='MAT'
                            s5='COS'
                        elif clicked.get()=="pcmb":
                            s2='PHY'
                            s3='CHE'
                            s4='MAT'
                            s5='BIO'
                        elif clicked.get()=="pcme":
                            s2='PHY'
                            s3='CHE'
                            s4='MAT'
                            s5='ECO'
                        elif clicked.get()=="pcbp":
                            s2='PHY'
                            s3='CHE'
                            s4='BIO'
                            s5='PSY'
                        c.execute("INSERT INTO STUDENTS VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(i,nam.get(),dob.get(),cl.get(),clicked.get(),s1,s2,s3,s4,s5))
                        text=Label(ast,text="Record Added.",background="#F1EBE5")
                        font(text,10)
                        text.place(x=732,y=590)

        tmenu.destroy()
        ast=Tk()
        ast.title("A+ Student Management Systems (Academic)")
        ast.resizable(0,0)
        
        bg=PhotoImage(file="bg/addstudent.png")
        lbg=Label(ast,i=bg)
        lbg.pack()
        lbg.image=bg
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(ast,image=sub,command=lambda:add(),bd=0)
        sub_b.place(x=876,y=540)
            
        cl=Entry(ast,bd=0,width=13,justify="center",borderwidth=1)
        font(cl,20)
        cl.place(x=791,y=318)
        
        clicked=StringVar()
        clicked.set("Select Stream")
        options=["pcmc","pcmb","pcbp","pcme"]
        stream=OptionMenu(ast,clicked, *options)
        font(stream,15)
        stream.config(width=12)
        stream.place(x=954,y=318)
        
        nam=Entry(ast,bd=1,width=26,justify="center")
        font(nam,20)
        nam.place(x=788,y=396)
        
        dob=Entry(ast,bd=1,width=13,justify="center")
        font(dob,20)
        dob.place(x=872,y=484)
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(ast,image=back,command=lambda:[menu_teacher(ast,name,tchr)],bd=0)
        back_b.place(x=70,y=70)
        
        ast.mainloop()
        
    def view_student(name):
        
        def search(x):
            
            c.execute("USE {};".format(name))
            c.execute("SELECT * FROM STUDENTS;")
            d=c.fetchall()
            for i in d:
                if str(i[0])==x:
                    del_label()
                    rec=i[1]+"\t12"+i[3]+"\tDOB: "+i[2].strftime("%d/%m/%Y")+"\t"+i[4]
                    text=Label(vs,text=rec,background="#F1EBE5")
                    font(text,10)
                    text.place(x=757,y=310)
                    global cn
                    cn=i[3]
                    break
            else:
                del_label()
                text=Label(vs,text="Record not found.",background="#F1EBE5")
                font(text,20)
                text.place(x=757,y=310)
        
        def modify(win,x):
            
            def mod():
                if nam.get() not in [""," "]:
                    c.execute("UPDATE STUDENTS SET NAME='{}' WHERE ID={};".format(nam.get(),x))
                elif clicked.get() not in ["Select Stream"]:
                    c.execute("UPDATE STUDENTS SET STREAM='{}' WHERE ID={};".format(clicked.get(),x))
                    if clicked.get()=="pcmc":
                            s2='PHY'
                            s3='CHE'
                            s4='MAT'
                            s5='COS'
                    elif clicked.get()=="pcmb":
                        s2='PHY'
                        s3='CHE'
                        s4='MAT'
                        s5='BIO'
                    elif clicked.get()=="pcme":
                        s2='PHY'
                        s3='CHE'
                        s4='MAT'
                        s5='ECO'
                    elif clicked.get()=="pcbp":
                        s2='PHY'
                        s3='CHE'
                        s4='BIO'
                        s5='PSY'
                    c.execute("UPDATE STUDENTS SET S2='{}',S3='{}',S4='{}',S5='{}' WHERE ID={};".format(s2,s3,s4,s5,x))
                elif cl.get() not in [""," "]:
                    c.execute("UPDATE STUDENTS SET CLASS='{}' WHERE ID={};".format(cl.get(),x))
                elif dob.get() not in [""," "]:
                    c.execute("UPDATE STUDENTS SET DOB='{}' WHERE ID={};".format(dob.get(),x))
                text=Label(vs,text="Record Updated.",background="#F1EBE5")
                font(text,10)
                text.place(x=732,y=590)
                
            c.execute("SELECT CLASS FROM TEACHERS WHERE ID='{}';".format(tchr))
            d=c.fetchall()
            for i in d:
                if cn not in i[0]:
                    text=Label(win,text="You don't teach this division.",background="#F1EBE5")
                    font(text,10)
                    text.place(x=732,y=590)
                else:
            
                    win.destroy()
                    vs=Tk()
                    vs.title("A+ Student Management Systems (Academic) - {}".format(name))
                    vs.resizable(0,0)
                    
                    bg=PhotoImage(file="bg/addstudent.png")
                    lbg=Label(vs,i=bg)
                    lbg.pack()
                    lbg.image=bg
                    
                    sub=PhotoImage(file="buttons/submit.png")
                    sub_b=Button(vs,image=sub,command=lambda:mod(),bd=0)
                    sub_b.place(x=876,y=540)
                        
                    cl=Entry(vs,bd=0,width=13,justify="center",borderwidth=1)
                    font(cl,20)
                    cl.place(x=791,y=318)
                    
                    clicked=StringVar()
                    clicked.set("Select Stream")
                    options=["pcmc","pcmb","pcbp","pcme"]
                    stream=OptionMenu(vs,clicked, *options)
                    font(stream,15)
                    stream.config(width=12)
                    stream.place(x=954,y=318)
                    
                    nam=Entry(vs,bd=1,width=26,justify="center")
                    font(nam,20)
                    nam.place(x=788,y=396)
                    
                    dob=Entry(vs,bd=1,width=13,justify="center")
                    font(dob,20)
                    dob.place(x=872,y=484)
                    
                    back=PhotoImage(file="buttons/back.png")
                    back_b=Button(vs,image=back,command=lambda:[menu_teacher(vs,name,tchr)],bd=0)
                    back_b.place(x=70,y=70)
                    back_b.button=back
                    
                    vs.mainloop()
        
        tmenu.destroy()
        vs=Tk()
        vs.title("A+ Student Management Systems (Academic) - {}".format(name))
        vs.resizable(0,0)
        
        bg=PhotoImage(file="bg/viewstudent.png")
        lbg=Label(vs,i=bg)
        lbg.pack()
        lbg.image=bg
        
        ID=Entry(vs,bd=1,width=26,justify="center")
        font(ID,20)
        ID.place(x=788,y=396)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(vs,image=sub,command=lambda:search(ID.get()),bd=0)
        sub_b.place(x=876,y=540)
        
        mod=PhotoImage(file="buttons/modify.png")
        modi=Button(vs,image=mod,command=lambda:modify(vs,ID.get()),bd=0)
        modi.place(x=876,y=489)
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(vs,image=back,command=lambda:[menu_teacher(vs,name,tchr)],bd=0)
        back_b.place(x=70,y=70)
        
        vs.mainloop()
        
    #def marks_entry():
        
    def report():
        
        def search(x):
            
            def create_report(win,ID):
                
                win.destroy()
                rep=Tk()
                rep.title("A+ Student Management Systems (Academic) - {} - Student Report for {}".format(name,ID))
                rep.resizable(0,0)
                
                bg=PhotoImage(file="bg/report.png")
                lbg=Label(rep,i=bg)
                lbg.pack()
                lbg.image=bg
                
                c.execute("SELECT * FROM STUDENTS S,MARKS M WHERE S.ID=M.ID;")
                data=c.fetchall()
                c.execute("USE PROJECT;")
                c.execute("SELECT SCHOOL FROM SCHOOLS WHERE INITIAL='{}';".format(name))
                school=c.fetchall()
                for s in school:
                    school=s[0]
                for i in data:
                    if str(i[0])==str(ID):
                        
                        def rep_subject(x):
                            if x=="ENG":
                                return "ENGLISH CORE"
                            elif x=="PHY":
                                return "PHYSICS"
                            elif x=="CHE":
                                return "CHEMISTRY"
                            elif x=="MAT":
                                return "MATHEMATICS"
                            elif x=="COS":
                                return "COMPUTER SCIENCE"
                            elif x=="BIO":
                                return "BIOLOGY"
                            elif x=="PSY":
                                return "PSYCHOLOGY"
                            elif x=="ECO":
                                return "ECONOMICS"
                            
                        def grade(x):
                            if x>=91:
                                return "A1"
                            elif x>=81 and x<91:
                                return "A2"
                            elif x>=71 and x<81:
                                return "B1"
                            elif x>=61 and x<71:
                                return "B2"
                            elif x>=51 and x<61:
                                return "C1"
                            elif x>=41 and x<51:
                                return "C2"
                            elif x>=33 and x<51:
                                return "D"
                            elif x>=21 and x<33:
                                return "E2"
                            elif x>=0 and x<21:
                                return "E2"
                        
                        def result(x):
                            if x=="A1":
                                return "PASS - DIST."
                            elif x in ['E1','E2']:
                                return "FAIL"
                            else:
                                return "PASS"
                        
                        
                        
                        Name=Label(rep,text=i[1],background="#F1EBE5",foreground="grey")
                        reportfont(Name)
                        Name.place(x=213,y=210)
                        School=Label(rep,text=school,background="#F1EBE5",foreground="grey")
                        reportfont(School)
                        School.place(x=213,y=276)
                        DOB=Label(rep,text=i[2].strftime("%d/%m/%Y"),background="#F1EBE5",foreground="grey")
                        reportfont(DOB)
                        DOB.place(x=239,y=342)
                        Class=Label(rep,text=i[3],background="#F1EBE5",foreground="grey")
                        reportfont(Class)
                        Class.place(x=548,y=337)
                        IDf=Label(rep,text=name.upper()+"-S-"+ID,background="#F1EBE5",foreground="red")
                        reportfont(IDf)
                        IDf.place(x=190,y=408)
                        Stream=Label(rep,text=i[4].upper(),background="#F1EBE5",foreground="grey")
                        reportfont(Stream)
                        Stream.place(y=408,x=516)
                        
                        S1=Label(rep,text=rep_subject(i[5]),background="#F1EBE5",foreground="grey")
                        reportfont(S1)
                        S1.place(x=770,y=256)
                        S2=Label(rep,text=rep_subject(i[6]),background="#F1EBE5",foreground="grey")
                        reportfont(S2)
                        S2.place(x=770,y=311)
                        S3=Label(rep,text=rep_subject(i[7]),background="#F1EBE5",foreground="grey")
                        reportfont(S3)
                        S3.place(x=770,y=366)
                        S4=Label(rep,text=rep_subject(i[8]),background="#F1EBE5",foreground="grey")
                        reportfont(S4)
                        S4.place(x=770,y=419)
                        S5=Label(rep,text=rep_subject(i[9]),background="#F1EBE5",foreground="grey")
                        reportfont(S5)
                        S5.place(x=770,y=473)
                        
                        m1=Label(rep,text=i[11],background="#F1EBE5",foreground="grey")
                        reportfont(m1)
                        m1.place(x=1087,y=256)
                        m2=Label(rep,text=i[12],background="#F1EBE5",foreground="grey")
                        reportfont(m2)
                        m2.place(x=1087,y=311)
                        m3=Label(rep,text=i[13],background="#F1EBE5",foreground="grey")
                        reportfont(m3)
                        m3.place(x=1087,y=366)
                        m4=Label(rep,text=i[14],background="#F1EBE5",foreground="grey")
                        reportfont(m4)
                        m4.place(x=1087,y=419)
                        m5=Label(rep,text=i[15],background="#F1EBE5",foreground="grey")
                        reportfont(m5)
                        m5.place(x=1087,y=473)
                        
                        g1=Label(rep,text=grade(i[11]),background="#F1EBE5",foreground="grey")
                        reportfont(g1)
                        g1.place(x=1176,y=256)
                        g2=Label(rep,text=grade(i[12]),background="#F1EBE5",foreground="grey")
                        reportfont(g2)
                        g2.place(x=1176,y=311)
                        g3=Label(rep,text=grade(i[13]),background="#F1EBE5",foreground="grey")
                        reportfont(g3)
                        g3.place(x=1176,y=366)
                        g4=Label(rep,text=grade(i[14]),background="#F1EBE5",foreground="grey")
                        reportfont(g4)
                        g4.place(x=1176,y=419)
                        g5=Label(rep,text=grade(i[15]),background="#F1EBE5",foreground="grey")
                        reportfont(g5)
                        g5.place(x=1176,y=473)
                        
                        total=i[11]+i[12]+i[13]+i[14]+i[15]
                        obt=Label(rep,text=str(total),background="#F1EBE5",foreground="grey")
                        reportfont(obt)
                        obt.place(x=1087,y=527)
                        
                        g=Label(rep,text=grade(total/5),background="#F1EBE5",foreground="grey")
                        reportfont(g)
                        g.place(x=1176,y=527)
                        
                        ptage=Label(rep,text=str(total/5),background="#F1EBE5",foreground="grey")
                        reportfont(ptage)
                        ptage.place(x=751,y=604)
                        
                        res=Label(rep,text=result(grade(total/5)),background="#F1EBE5",foreground="grey")
                        reportfont(res)
                        res.place(x=910,y=604)
                        
                        dte=Label(rep,text=datetime.date.today(),background="#F1EBE5",foreground="grey")
                        reportfont(dte)
                        dte.place(x=1090,y=604)
                        
                        fname=name.upper()+"-S"+i[0]+" - "+str(datetime.date.today())+".png"
                        
                        
                        back=PhotoImage(file="buttons/back.png")
                        back_b=Button(rep,image=back,command=report,bd=0)
                        back_b.place(x=70,y=45)                        
                
                rep.mainloop()
            
            c.execute("USE {};".format(name))
            c.execute("SELECT * FROM STUDENTS;")
            d=c.fetchall()
            for i in d:
                if str(i[0])==x:
                    create_report(vs,x)
                    break
            else:
                del_label()
                text=Label(vs,text="Record not found.",background="#F1EBE5")
                font(text,20)
                text.place(x=757,y=310)

        
        tmenu.destroy()
        vs=Tk()
        vs.title("A+ Student Management Systems (Academic) - {}".format(name))
        vs.resizable(0,0)
        
        bg=PhotoImage(file="bg/genrep.png")
        lbg=Label(vs,i=bg)
        lbg.pack()
        lbg.image=bg
        
        ID=Entry(vs,bd=1,width=26,justify="center")
        font(ID,20)
        ID.place(x=788,y=396)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(vs,image=sub,command=lambda:search(ID.get()),bd=0)
        sub_b.place(x=876,y=540)
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(vs,image=back,command=lambda:[menu_teacher(vs,name,tchr)],bd=0)
        back_b.place(x=70,y=70)
        
        vs.mainloop()
        
    def marks_entry(name):
        
        def search(x):
            
            def mark(y):
                
                def positive():
                    text=Label(ent,text="Marks entered.",background="#F1EBE5")
                    font(text,10)
                    text.place(x=732,y=590)
                
                c.execute("SELECT * FROM STUDENTS S,MARKS M WHERE S.ID=M.ID;")
                d=c.fetchall()
                if len(d)==0:
                    c.execute("INSERT INTO MARKS (ID) VALUES ({});".format(y))
                    c.execute("SELECT * FROM STUDENTS S,MARKS M WHERE S.ID=M.ID;")
                    d=c.fetchall()
                    for i in d:
                        if i[5]==s:
                            q="UPDATE MARKS SET S1={} WHERE ID={};".format(marks.get(),y)
                            c.execute(q)
                            positive()
                        elif i[6]==s:
                            c.execute("UPDATE MARKS SET S2={} WHERE ID={};".format(marks.get(),y))
                            positive()
                        elif i[7]==s:
                            c.execute("UPDATE MARKS SET S3={} WHERE ID={};".format(marks.get(),y))
                            positive()
                        elif i[8]==s:
                            c.execute("UPDATE MARKS SET S4={} WHERE ID={};".format(marks.get(),y))
                            positive()
                        elif i[9]==s:
                            c.execute("UPDATE MARKS SET S5={} WHERE ID={};".format(marks.get(),y))
                            positive()
                else:
                    for i in d:
                        if str(y)==str(i[0]):
                            if i[5]==s:
                                c.execute("UPDATE MARKS SET S1={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[6]==s:
                                c.execute("UPDATE MARKS SET S2={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[7]==s:
                                c.execute("UPDATE MARKS SET S3={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[8]==s:
                                c.execute("UPDATE MARKS SET S4={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[9]==s:
                                c.execute("UPDATE MARKS SET S5={} WHERE ID={};".format(marks.get(),y))
                                positive()
                        elif str(y)!=str():
                            c.execute("INSERT INTO MARKS (ID) VALUES ({});".format(y))
                            if i[5]==s:
                                c.execute("UPDATE MARKS SET S1={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[6]==s:
                                c.execute("UPDATE MARKS SET S2={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[7]==s:
                                c.execute("UPDATE MARKS SET S3={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[8]==s:
                                c.execute("UPDATE MARKS SET S4={} WHERE ID={};".format(marks.get(),y))
                                positive()
                            elif i[9]==s:
                                c.execute("UPDATE MARKS SET S5={} WHERE ID={};".format(marks.get(),y))
                                positive()

                
                
            c.execute("USE {};".format(name))
            c.execute("SELECT ID,CLASS FROM STUDENTS;")
            d=c.fetchall()
            c.execute("SELECT SUBJECT,CLASS FROM TEACHERS WHERE ID={};".format(tchr))
            data=c.fetchall()
            cl=data[0][1]
            s=data[0][0]
            for i in d:
                if str(i[0])==ID.get():
                    for j in cl:
                        if j==i[1]:
                            mark(ID.get())
                            break
                    else:
                        text=Label(ent,text="You don't teach this division.",background="#F1EBE5")
                        font(text,20)
                        text.place(x=757,y=310)
                    break
            else:
                text=Label(ent,text="Student doesn't exist.",background="#F1EBE5")
                font(text,20)
                text.place(x=757,y=310)
                
        
        tmenu.destroy()
        ent=Tk()
        ent.title("A+ Student Management Systems (Academic) - Marks Entry - {}".format(name))
        ent.resizable(0,0)
        
        bg=PhotoImage(file="bg/me.png")
        lbg=Label(ent,i=bg)
        lbg.pack()
        lbg.image=bg
        
        ID=Entry(ent,bd=1,width=26,justify="center")
        font(ID,20)
        ID.place(x=788,y=396)
        
        marks=Entry(ent,bd=1,width=26,justify="center")
        font(marks,20)
        marks.place(x=788,y=471)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(ent,image=sub,command=lambda:search(ID.get()),bd=0)
        sub_b.place(x=876,y=540)
        sub_b.button=sub
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(ent,image=back,command=lambda:[menu_teacher(ent,name,tchr)],bd=0)
        back_b.place(x=70,y=70)
        back_b.button=back
        
        ent.mainloop
        
    win.destroy()
    tmenu=Tk()
    tmenu.title("A+ Student Management Systems (Academic) - Teachers")
    tmenu.resizable(0,0)
    
    bg=PhotoImage(file="bg/school menu.png")
    lbg=Label(tmenu,i=bg)
    lbg.pack()
    lbg.image=bg
    
    #Button: Add Student

    addstud=PhotoImage(file="buttons/addstud.png")
    adds=Button(tmenu,image=addstud,command=lambda:add_student(),bd=0)
    adds.place(x=752,y=228)

    #Button: View Student

    viewstud=PhotoImage(file="buttons/viewstud.png")
    views=Button(tmenu,image=viewstud,command=lambda:view_student(name),bd=0)
    views.place(x=752,y=333)

    #Button: Marks Entry

    me=PhotoImage(file="buttons/me.png")
    meb=Button(tmenu,image=me,command=lambda:marks_entry(name),bd=0)
    meb.place(x=752,y=440)

    #Button: Reports

    rep=PhotoImage(file="buttons/viewrep.png")
    reports=Button(tmenu,image=rep,command=lambda:report(),bd=0)
    reports.place(x=752,y=546)
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(tmenu,image=back,command=lambda:[tmenu.destroy(),start()],bd=0)
    back_b.place(x=70,y=70)
    back_b.button=back
    
    tmenu.mainloop()

#School Login Instance
    
def login_school(win):
    
    def login(user,pw):
        
        del_label()
                
        c.execute("USE PROJECT;")
        c.execute("SELECT INITIAL,PASSWORD FROM SCHOOLS;")
        creds=c.fetchall()
        for i in creds:
            if i[0]==user and i[1]==pw:
                c.execute("USE {};".format(i[0]))
                menu_school(school,i[0])
            elif user in [""," "] or pw in [""," "]:
                alert=Label(school,text="Username or Password cannot be blank.",background="#F1EBE5")
                font(alert,10)
                alert.place(x=732,y=590)
            else:
                alert=Label(school,text="Incorrect Credentials.",background="#F1EBE5")
                font(alert,10)
                alert.place(x=732,y=590)
    
    win.destroy()
    school=Tk()
    school.title("A+ Student Management Systems (Academic) - Login for Schools")
    school.resizable(0,0)
    
    bg=PhotoImage(file="bg/school login.png")
    lbg=Label(school,i=bg)
    lbg.pack()
    lbg.image=bg
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(school,image=back,command=lambda:[school.destroy(),start()],bd=0)
    back_b.place(x=70,y=70)
    
    ini=Entry(school,bd=0,width=26,justify="center")
    font(ini,20)
    ini.place(x=788,y=352)
    
    pwsch=Entry(school,bd=0,width=26,show="*",justify="center")
    font(pwsch,20)
    pwsch.place(x=788,y=442)
    
    forg=PhotoImage(file="buttons/forgot.png")
    forgot_b=Button(school,image=forg,command=lambda:forgot_pass(school),bd=0)
    forgot_b.place(x=964,y=537)
    forgot_b.button=forg
    
    sub=PhotoImage(file="buttons/submit.png")
    sub_b=Button(school,image=sub,command=lambda:[login(ini.get(),pwsch.get())],bd=0)
    sub_b.place(x=787,y=537)    
    
    school.mainloop()

#Teacher Login Instance
    
def login_teacher(win):
    
    def login(user,pw):
        
        del_label()
        
        if user in [""," "] or pw in [""," "]:
                text=Label(teacher,text="Username or Password cannot be blank.",background="#F1EBE5")
                font(text,10)
                text.place(x=732,y=590)
        else:
        
            for i in range(len(user)):
                if user[i]==".":
                    user1=user[i+1:]
                    school=user[0:i]
        
            c.execute("USE {};".format(school))
            c.execute("SELECT ID,PASSWORD FROM TEACHERS;")
            creds=c.fetchall()
            for i in creds:
                if str(i[0])==user1 and str(i[1])==pw:
                    menu_teacher(teacher,school,i[0])
                else:
                    text=Label(teacher,text="Incorrect Credentials.",background="#F1EBE5")
                    font(text,10)
                    text.place(x=732,y=590)
    
    def cntct():
        
        text=Label(teacher,text="Contact your administrator.",background="#F1EBE5")
        font(text,10)
        text.place(x=732,y=590)
    
    win.destroy()
    teacher=Tk()
    teacher.title("A+ Student Management Systems (Academic) - Login for Teachers")
    teacher.resizable(0,0)
    
    bg=PhotoImage(file="bg/teacher login.png")
    lbg=Label(teacher,i=bg)
    lbg.pack()
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(teacher,image=back,command=lambda:[teacher.destroy(),start()],bd=0)
    back_b.place(x=70,y=70)
    
    user=Entry(teacher,bd=0,width=26,justify="center")
    font(user,20)
    user.place(x=788,y=352)
    
    pw=Entry(teacher,bd=0,width=26,show="*",justify="center")
    font(pw,20)
    pw.place(x=788,y=442)
    
    sub=PhotoImage(file="buttons/submit.png")
    sub_b=Button(teacher,image=sub,command=lambda:[login(user.get(),pw.get())],bd=0)
    sub_b.place(x=787,y=537)
    
    forg=PhotoImage(file="buttons/forgot.png")
    forgot_b=Button(teacher,image=forg,command=lambda:[cntct()],bd=0)
    forgot_b.place(x=964,y=537)
    
    teacher.mainloop()

#Account Creation Instance

def create_account():
    
    #OTP Submission+Verification Instance

    def otp_verify(win):
        
        #Verification
        
        def veri():
            if o.get()==str(otp):
                login_school(verify)
            else:
                text=Label(verify,text="Incorrect OTP!",background="#F1EBE5")
                font(text,10)
                text.place(x=732,y=590)
        
        win.destroy()
        verify=Tk()
        verify.title("A+ Student Management Systems (Academic) - Verify")
        verify.resizable(0,0)
        
        bg=PhotoImage(file="bg/otp.png")
        lbg=Label(verify,i=bg)
        lbg.pack()
        lbg.image=bg
        
        back=PhotoImage(file="buttons/back.png")
        back_b=Button(verify,image=back,command=lambda:[login_school(verify)],bd=0)
        back_b.place(x=70,y=70)
        back_b.button=back
        
        o=Entry(verify,bd=0,width=26,justify="center")
        font(o,20)
        o.place(x=788,y=438)
        
        sub=PhotoImage(file="buttons/submit.png")
        sub_b=Button(verify,image=sub,command=veri,bd=0)
        sub_b.place(x=875,y=537)
        sub_b.button=sub
    
    #Final Submission of Form
    
    def submit():
        
        data=[]
        x=school.get()
        ini=x[0].upper()
        if x[-1]==" ":
            x=x.rstrip()
        for i in range(len(x)):
            if x[i]==" ":
                ini+=x[i+1].upper()
        data.append(ini)
        data.append(school.get())
        data.append(email.get())
        data.append(pw.get())
        c.execute("USE PROJECT;")
        c.execute("SELECT INITIAL FROM SCHOOLS;")
        d=c.fetchall()
        for i in d:
            if i[0]==data[0]:
                data[0]+="1"
        otp(data[0],data[2])
        otp_verify(create)
        c.execute("INSERT INTO SCHOOLS VALUES ('{}','{}','{}','{}');".format(data[0],data[1],data[2],data[3]))
        package(data[0])
    
    #Form Validation
        
    def validate():
        
        if pw.get() in [""," "] or school.get() in [""," "] or email.get() in [""," "] or confirm.get() in [""," "]:
            text2=Label(create,text="All fields must be filled!")
            font(text2,10)
            text2.place(x=911,y=590)
            x1=False
        else:
            x1=True
        if "@" not in email.get():
            text3=Label(create,text="Invalid Email")
            font(text3,10)
            text3.place(x=1100,y=590)
            x2=False
        else:
            x2=True
        if pw.get()!=confirm.get() or len(pw.get())==0 or len(confirm.get())==0:
            text1=Label(create,text="Password doesn't match!")
            font(text1,10)
            text1.place(x=732,y=590)
            x3=False
        else:
            x3=True
        
        if x1 and x2 and x3:
            return submit()
        
    root.destroy()
    create=Tk()
    create.title("A+ Student Management Systems (Academic) - Create School Account")
    create.resizable(0,0)
    
    bg=PhotoImage(file="bg/create.png")
    lbg=Label(create,i=bg)
    lbg.pack()
    
    sub=PhotoImage(file="buttons/submit.png")
    sub_b=Button(create,image=sub,command=lambda:validate(),bd=0)
    sub_b.place(x=876,y=540)
        
    school=Entry(create,bd=0,width=13,justify="center",borderwidth=1)
    font(school,20)
    school.place(x=791,y=318)
    
    email=Entry(create,bd=0,width=13,justify="center",borderwidth=1)
    font(email,20)
    email.place(x=954,y=318)
    
    pw=Entry(create,bd=1,width=26,show="*",justify="center")
    font(pw,20)
    pw.place(x=788,y=396)
    
    confirm=Entry(create,bd=1,width=26,show="*",justify="center")
    font(confirm,20)
    confirm.place(x=788,y=470)
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(create,image=back,command=lambda:[create.destroy(),start()],bd=0)
    back_b.place(x=70,y=70)
    back_b.button=back
    
    create.mainloop()

#About Us Instance
    
def about_us():
    
    root.destroy()
    about=Tk()
    about.title("About A+ Student Management Systems (Academic)")
    about.resizable(0,0)
    
    bg=PhotoImage(file="bg/about.png")
    lbg=Label(about,i=bg)
    lbg.pack()
    
    back=PhotoImage(file="buttons/back.png")
    back_b=Button(about,image=back,command=lambda:[about.destroy(),start()],bd=0)
    back_b.place(x=70,y=70)
    
    about.mainloop()

#Onloading Screen 

def start():
    global root
    root=Tk()
    root.resizable(0,0)
    root.title("A+ Student Management Systems (Academic)")

    #Loading Page

    loading=PhotoImage(file="bg/loading.png")
    l_load=Label(root,i=loading)
    l_load.pack()

    #Button: Login - Students

    logsch=PhotoImage(file="buttons/logsch.png")
    logsch_b=Button(root,image=logsch,command=lambda:[login_school(root)],bd=0)
    logsch_b.place(x=752,y=228)

    #Button: Login - Teachers

    logt=PhotoImage(file="buttons/logt.png")
    logt_b=Button(root,image=logt,command=lambda:[login_teacher(root)],bd=0)
    logt_b.place(x=752,y=333)

    #Button: Create Student Account

    create=PhotoImage(file="buttons/create.png")
    create_b=Button(root,image=create,command=create_account,bd=0)
    create_b.place(x=752,y=440)

    #Button: Login - Teachers

    about=PhotoImage(file="buttons/about.png")
    about_b=Button(root,image=about,command=about_us,bd=0)
    about_b.place(x=752,y=546)

    root.mainloop()

start() #Program Start