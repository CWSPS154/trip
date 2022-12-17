from flask import Flask ,render_template ,request ,session ,redirect
from DBConnection import Db
from datetime import date


app = Flask(__name__)
app.secret_key="xyss"


@app.route('/ssj/<a>')
def hello_world(a):
    print(a)
    return str(a)

@app.route('/test')
def test():
    a=10
    b=20
    c=int(a+b)
    print(c)
    return str(c)

@app.route('/login')
def login():
    return render_template("Admin/index.html")

@app.route('/forget1')
def forget1():
    name = request.args.get('uname')
    print(name)
    q="select username,password from login where username='"+str(name)+"'"
    ob=Db()
    un=ob.selectOne(q)
    if un is not None:
        return '''<script>alert('Check your email to login');window.location='/login'</script>'''
    else:
        return '''<script>alert('Incurrect email');window.location='/login'</script>'''

@app.route('/about_us')
def about_us():
    if session.get('login'):
      w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
      ob = Db()
      pic = ob.selectOne(w)
      return render_template("User/about us.html",pic=pic)
    else:
        return render_template("User/about us.html")

@app.route('/contact_us')
def contact_us():
    o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid order by date desc"
    ob = Db()
    cmp = ob.selectOne(o)
    w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' order by date desc"
    ob = Db()
    ntf = ob.selectOne(w)
    x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
    ob = Db()
    ag = ob.selectOne(x)
    return render_template("Agency/contacts.html",cmp=cmp,ntf=ntf,ag=ag)

@app.route('/')
def user():
    id = None
    type = None

    if session.get('login'):
        id = session['login']

    if session.get('type'):
        type = session['type']

    x = "select * from ad where type='posted' order by date desc"
    ob = Db()
    ad = ob.select(x)

    q = "select package.*,location.*,trending.*,agency.agency_name,agency.agency_id,round(avg(rating.rating),0) from package,trending,agency,location,rating where package.package_id=trending.package_id and agency.agency_id=package.agencyid and location.package_id=package.package_id and trending.package_id=rating.package_id group by rating.package_id"
    ob = Db()
    res = ob.select(q)
    if session.get('login'):
        w = "select type from login where Login_id='" + str(session['login']) + "'"
        ob = Db()
        ty = ob.selectOne(w)
        if ty['type'] == 'admin':
            return redirect('/h1')
        elif ty['type'] == 'agency':
            return redirect('/h2')
        elif ty['type'] == 'user':
            y = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
            ob = Db()
            pic = ob.selectOne(y)
            b = "select count(bk_id) from booking where user_id='" + str(session['login']) + "'"
            ob = Db()
            bk = ob.selectOne(b)
            return render_template("User/index.html", val=res, lid=id, tp=type, pic=pic, ad=ad,bk=bk)
    else:
      return render_template("User/index.html",val=res, lid=id, tp=type,ad=ad)

@app.route('/login1',methods=['POST'])
def login1():
    name = request.form['uname']
    pswd = request.form['passwd']
    q="select * from login where username='"+name+"' and password='"+pswd+"'"
    # print(q)
    ob=Db()
    res=ob.selectOne(q)
    print(res)
    if res is not None:
        session['login'] = res['Login_id']
        session['type'] = res['type']
        if res['type']=='admin':
            return redirect('/h1')
        elif res['type']=='agency':
            d=date.today()
            ob=Db()
            val=ob.selectOne("select * from validity where agency_id='"+str(session['login'])+"'")
            print(d)
            if val['exp_date']==d:
                ob=Db()
                ob.update("update validity set date=null,exp_date=null,status='Experied' where agency_id='"+str(session['login'])+"'")
                return redirect('/paynow')
            elif val['status']=='Not Payed' or val['status']=='Experied':
                 return '''<script>alert('Your Account is Not Payed Or Experied');window.location='/paynow'</script>'''
            else:
                return redirect('/h2')
        elif res['type']=='user':
            return redirect('/')
    if res is None:
     return '''<script>alert('Incurrect username or password');window.location='/login'</script>'''

@app.route('/log_out')
def log_out():
    session.clear()
    return login()


@app.route('/h1')
def h1():
    if session.get('login'):
        w = "select count(package_id) from package where type='pending'"
        ob = Db()
        npkg = ob.selectOne(w)
        a = "select count(package_id) from package where type='Approved'"
        ob = Db()
        pkg = ob.selectOne(a)
        x = "select count(Login_id) from login where type='pending'"
        ob = Db()
        nagcy = ob.selectOne(x)
        s = "select count(Login_id) from login where type='agency'"
        ob = Db()
        agcy = ob.selectOne(s)
        y = "select count(Login_id) from login where type='user'"
        ob = Db()
        usr = ob.selectOne(y)
        z = "select count(cmplt_id) from complaint where reply='pending'"
        ob = Db()
        fdbk = ob.selectOne(z)
        return render_template("Admin/home.html",npkg=npkg, nagcy=nagcy, usr=usr, fdbk=fdbk,agcy=agcy,pkg=pkg)
    else:
        return login()

@app.route('/h2')
def h2():
    if session.get('login'):
        # y="select count(cmplt_id) from complaint where agency_id='"+str(session['login'])+"'"
        # ob = Db()
        # ccmp = ob.selectOne(y)
        # z = "select count(fdbk_id) from feedback where agency_id='"+str(session['login'])+"'"
        # ob = Db()
        # fdk = ob.selectOne(z)
        q="select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob=Db()
        cmp=ob.selectOne(q)
        w="select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob=Db()
        ntf=ob.selectOne(w)
        x="select agency.agency_name,agency.cover from agency where agency_id='"+str(session['login'])+"'"
        ob=Db()
        ag=ob.selectOne(x)
        m = "select * from ad order by date desc"
        ob = Db()
        ad = ob.select(m)
        return render_template("Agency/home.html",ntf=ntf,cmp=cmp,ag=ag,ad=ad)
    else:
        return login()


@app.route('/register')
def register():
    return render_template("User/register.html")
@app.route('/registration',methods=['POST'])
def registion():
    uname=request.form['uname']
    place=request.form['Place']
    po=request.form['PO']
    pin=request.form['PIN']
    dob=request.form['age']
    mail=request.form['Email']
    mob=request.form['mobno']
    img=request.files['img']


    import time
    fname=time.strftime("%Y%m%d_%H%M%S")+".jpg"
    img.save(r"G:\trip\static\profilepic\\"+fname)

    pwd = request.form['Passwd']
    cpwd = request.form['cp']
    ob=Db()
    q="insert into login values(null, '" + mail + "','" + cpwd + "','user')"
    id=ob.insert(q)
    q = "insert into user values('"+str(id)+"','"+uname+"','"+place+"','"+po+"','"+pin+"','"+dob+"','"+mail+"','"+mob+"','"+fname+"','"+str(id)+"')"
    ob.insert(q)
    return login()

@app.route('/register1')
def register1():
    return render_template("Agency/Register.html")
@app.route('/registration1',methods=['POST'])
def registion1():

    aname=request.form['Aname']
    place=request.form['Place']
    po=request.form['PO']
    pin=request.form['PIn']
    mail=request.form['E-mail']
    mob=request.form['mob']
    licno= request.form['lino']
    img=request.files['img']
    cvr = request.files['cvr']

    import time
    fname=time.strftime("%Y%m%d_%H%M%S")+".jpg"
    img.save(r"G:\trip\static\licence\\"+fname)
    cover = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
    cvr.save(r"G:\trip\static\licence\cover\\" +cover)

    pwd = request.form['passwd']
    cpwd = request.form['cp']
    ob=Db()
    q="insert into login values(null,'" + mail + "','" + cpwd + "','pending')"
    id=ob.insert(q)
    q = "insert into agency values('"+str(id)+"','"+aname+"','"+place+"','"+po+"','"+pin+"','"+mail+"','"+mob+"','"+licno+"','"+fname+"','"+cover+"')"
    ob.insert(q)
    ob = Db()
    w = "insert into validity values(null,'"+str(id)+"',null,null,null,'Not Payed')"
    ob.insert(w)
    ob = Db()
    x = "insert into account values(null,'" + str(id) + "',null,null,null,null,null,null,null,null,null,'0')"
    ob.insert(x)
    return '''<script>alert('You get confirmation through mail');window.location='/login'</script>'''



# <-------------------------ADMIN---------------------------------------------->


@app.route('/home')
def home():
    return render_template("Admin/Admin homepage.html")
@app.route('/Approve_Agency')
def Approve_Agency():
    if session.get('login'):
        q = "select agency.*,login.type,validity.* from login,agency left join validity on agency.agency_id=validity.agency_id where login.Login_id=agency.agency_id order by type='agency'"
        ob = Db()
        agcy = ob.select(q)
        ln = 0
        if len(agcy) == 0:
            ln = 1
        return render_template("Admin/Approve Agency.html",val=agcy,ln=ln)
    else:
        return redirect('login')
@app.route('/Approve_Agency1')
def Approve_Agency1():
    if session.get('login'):
        id=request.args.get('id')
        q="update login set type='agency' where Login_id="+str(id)+""
        ob=Db()
        ob.update(q)
        return Approve_Agency()
    else:
        return login()

@app.route('/Approve_Agency2',methods=['post'])
def Approve_Agency2():
    if session.get('login'):
        search = request.form['Search']
        q = "select agency.*,login.type,validity.* from login ,agency left join validity on agency.agency_id=validity.agency_id  where login.Login_id=agency.agency_id and agency_name like '%" + search + "%' order by type='agency'"
        ob = Db()
        agcy = ob.select(q)
        ln = 0
        if len(agcy) == 0:
            ln = 1
        print(agcy)
        return render_template("Admin/Approve Agency.html", val=agcy,ln=ln)
    else:
        return login()


@app.route('/Reject_Agency')
def Reject_Agency():
    if session.get('login'):
        id=request.args.get('id')
        q="delete from login where Login_id="+str(id)+""
        ob=Db()
        ob.delete(q)
        w="delete from agency where agency.agency_id="+str(id)+""
        ob = Db()
        ob.delete(w)
        x = "delete from package where package.agencyid=" + str(id) + ""
        ob = Db()
        ob.delete(x)
        r = "delete from guide where guide.agency_id=" + str(id) + ""
        ob = Db()
        ob.delete(r)
        return Approve_Agency()
    else:
        return login()
# @app.route('/Remove_Agency')
# def Remove_Agency():
#     id = request.args.get('id')
#     q = "update login set type='pending' where Login_id=" + str(id) + ""
#     ob = Db()
#     ob.update(q)
#     q = "delete from agency where agency.agency_id=" + str(id) + ""
#     ob.delete(q)
#     return '''<script>alert('Removed');window.location='/Approve_Agency'</script>'''

@app.route('/View_user')
def View_user():
    if session.get('login'):
        q = "select user.*,login.type from user,login where login.Login_id=user.userid "
        ob = Db()
        user = ob.select(q)
        ln = 0
        if len(user) == 0:
            ln = 1
        return render_template("Admin/Approve User.html",val=user,ln=ln)
    else:
        return login()

@app.route('/View_user1',methods=['post'])
def View_user1():
    if session.get('login'):
        search = request.form['Search']
        ob = Db()
        w = "select * from user where username like '%" + search + "%'"
        user = ob.select(w)
        ln = 0
        if len(user) == 0:
            ln = 1
        return render_template("Admin/Approve User.html",val=user,ln=ln)
    else:
        return login()


@app.route('/Remove_user')
def Remove_user():
    if session.get('login'):
        id = request.args.get('id')
        q = "delete from login where Login_id=" + str(id) + ""
        ob = Db()
        ob.delete(q)
        w = "delete from user where login_id=" + str(id) + ""
        ob.delete(w)
        return render_template("Admin/Approve User.html")
    else:
        return login()


@app.route('/Manage_Trending2',methods=['post'])
def Manage_Trending2():
    if session.get('login'):
        db = Db()
        search=request.form['Search']
        qry=db.select("select package.package_name,package.photo,package.package_id,package.agencyid,avg(rating.rating),rating.package_id,rating.status from package,rating where package.type='Approved' and package.package_id=rating.package_id and package.package_name like '%"+search+"%' group by rating.package_id ")
        ln = 0
        if len(qry) == 0:
            ln = 1
        return render_template("Admin/manage trending.html",val=qry,ln=ln)
    else:
        return login()

@app.route('/Manage_Trending')
def Manage_Trending():
    if session.get('login'):
        ob = Db()
        q = "select package.package_name,package.photo,package.package_id,package.agencyid,avg(rating.rating),rating.package_id,rating.status from package,rating where package.type='Approved' and package.package_id=rating.package_id group by rating.package_id order by rating.status='pending',avg(rating.rating) desc"
        trnd = ob.select(q)
        ln = 0
        if len(trnd) == 0:
            ln = 1
        return render_template("Admin/manage trending.html",val=trnd,ln=ln)
    else:
        return log_out()

# @app.route('/Manage_Trending1')
# def Manage_Trending1():
#     ob = Db()
#     category=request.form['ctgry']
#     print(category)
#     # x="select * from trending"
#     # res11=ob.select(x)
#     # print(res11)
#     w="select * from package"
#     res=ob.select(w)
#     q = "select package.package_name,package.photo,package.package_id,avg(rating.rating),rating.package_id,rating.status from package,rating where package.type='Approved' and package.package_id=rating.package_id and package.package_id='"+category+"'"
#     trnd = ob.select(q)
#     return render_template("Admin/manage trending.html",val=trnd,vall=res)

@app.route('/Post_Trending')
def Post_Trending():
    if session.get('login'):
        pid=request.args.get('id')
        aid = request.args.get('aid')
        ob = Db()
        q="Insert into trending values(null,'"+str(pid)+"')"
        ob.insert(q)
        ob = Db()
        w = "update rating set status='post' where package_id='" + str(pid) + "'"
        ob.update(w)
        ob = Db()
        pak = ob.selectOne("select package.package_name from package where package_id='" + str(pid) + "'")
        z = "insert into notification values(null,'Your package -" + str(pak['package_name']) + " - is now on trending ',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob = Db()
        ob.insert(z)
        return Manage_Trending()
    else:
        return login()

@app.route('/Reject_Trending')
def Reject_Trending():
    if session.get('login'):
        pid = request.args.get('id')
        aid = request.args.get('aid')
        ob = Db()
        q = "delete from trending where package_id='"+str(pid)+"'"
        ob.delete(q)
        ob = Db()
        w = "update rating set status='pending' where package_id='" + str(pid) + "'"
        ob.update(w)
        ob = Db()
        pak = ob.selectOne("select package.package_name from package where package_id='" + str(pid) + "'")
        z = "insert into notification values(null,'Your package -" + str(pak['package_name']) + " - is removed from trending ',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob = Db()
        ob.insert(z)
        return Manage_Trending()
    else:
        return login()

@app.route('/Manage_Package')
def Manage_Package():
    if session.get('login'):
        ob=Db()
        q="select * from package,location where package.package_id=location.package_id order by type='Approved'"
        pak=ob.select(q)
        ln = 0
        if len(pak) == 0:
            ln = 1
        ob = Db()
        w = "select agency.agency_name from package,agency where package.agencyid=agency.agency_id group by agency.agency_id"
        slct = ob.select(w)

        return render_template("Admin/Manage package.html",val=pak,slct=slct,ln=ln)
    else:
        return login()

@app.route('/Manage_Package1',methods=['post'])
def Manage_Package1():
    if session.get('login'):
        search = request.form['Search']
        ob = Db()
        q = "select package.*,agency.agency_name from package,agency where package.agencyid=agency.agency_id and agency.agency_name like '%"+search+"%'"
        pak = ob.select(q)
        ln = 0
        if len(pak) == 0:
            ln = 1
        ob = Db()
        q = "select agency.agency_name from package,agency where package.agencyid=agency.agency_id group by agency.agency_id"
        slct = ob.select(q)
        return render_template("Admin/Manage package.html", val=pak,slct=slct,ln=ln)
    else:
        return login()



@app.route('/Approve_Package')
def Approve_Package():
    if session.get('login'):
        id=request.args.get('id')
        aid = request.args.get('aid')
        ob = Db()
        q="update package set type='Approved' where package_id='"+str(id)+"'"
        ob.update(q)
        ob=Db()
        pak=ob.selectOne("select package.package_name from package where package_id='"+str(id)+"'")
        w = "insert into notification values(null,'Your package -"+str(pak['package_name'])+" - is approved',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob = Db()
        ob.insert(w)
        return Manage_Package()
    else:
        return login()

@app.route('/Reject_Package')
def Reject_Package():
    if session.get('login'):
        id=request.args.get('id')
        aid = request.args.get('aid')
        db = Db()
        pak = db.selectOne("select package.package_name from package where package_id='" + str(id) + "'")
        ob = Db()
        w = "insert into notification values(null,'Your package - " + str(pak['package_name']) + " - is Removed',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob.insert(w)
        ob = Db()
        q = "delete from package where package_id='" + str(id) + "'"
        ob.delete(q)
        return Manage_Package()
    else:
        return login()

@app.route('/View_feedbak')
def View_feedbak():
    if session.get('login'):
        ob=Db()
        q="select feedback.*,user.username,agency.agency_name from feedback,user,agency where feedback.user_id=user.login_id and agency.agency_id=feedback.agency_id order by  fdbk_id desc "
        res=ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        return render_template("Admin/Feedback.html",data=res,ln=ln)
    else:
        return login()


@app.route('/View_Complaints')
def View_Complaints():
    if session.get('login'):
        ob = Db()
        q = "select user.username,complaint.*,agency.agency_name,agency.agency_id from complaint,user,agency where complaint.user_id=user.login_id and agency.agency_id=complaint.agency_id order by cmplt_id desc "
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        return render_template("Admin/view complaints.html", data=res,ln=ln)
    else:
        return login()

@app.route('/reply')
def reply():
    if session.get('login'):
        id = request.args.get('id')
        aid = request.args.get('aid')
        return render_template("Admin/Replay.html",data=id,aid=aid)
    else:
        return login()

@app.route('/reply1/<a>/<aid>',methods=['post'])
def reply1(a,aid):
    if session.get('login'):
        reply = request.form['Reply']
        q = "update complaint set reply='"+reply+"',rdate=curdate() where cmplt_id='" + a+"'"
        ob = Db()
        ob.update(q)
        ob = Db()
        w = "insert into notification values(null,'Admin is gived the reply for the user complaint',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob.insert(w)
        return View_Complaints()
    else:
        return login()

@app.route('/rdlt')
def rdlt():
    if session.get('login'):
        id = request.args.get('id')
        q = "update complaint set reply='pending',rdate='pending' where cmplt_id='" +str(id)+"'"
        ob = Db()
        ob.update(q)
        return View_Complaints()
    else:
        return login()



@app.route('/Send_notification')
def Send_notification():
    if session.get('login'):
        return render_template("Admin/Notification.html")
    else:
        return login()

@app.route('/Send_notification1',methods=['POST'])
def Send_notification1():
    if session.get('login'):
       type=request.form['type']
       noti =request.form['ntfn']
       lid = session['login']
       q="insert into notification values(null,'"+noti+"',curdate(),'"+str(lid)+"','"+type+"')"
       ob=Db()
       ob.insert(q)
       return Send_notification()
    else:
        return log_out()

# @app.route('/view_notification')
# def view_notification():
#     ob = Db()
#     q = "select * from notification"
#     res = ob.select(q)
#     return render_template("Admin/View Notifications.html",data=res)
# @app.route('/view_notdlt')
# def view_notdlt():
#     id = request.args.get('id')
#     q = "delete from notification where notfcn_id='" +str(id)+"'"
#     ob=Db()
#     ob.delete(q)
#     return '''<script>alert('Deleted');window.location='/view_notification'</script>'''

@app.route('/ad_control')
def ad_control():
    if session.get('login'):
        ob = Db()
        q = "select ad.*,agency.agency_name,agency.agency_id from ad,agency where ad.agency_id=agency.agency_id order by type"
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        return render_template("Admin/Ad Control.html",data=res,ln=ln)
    else:
        return login()

@app.route('/ad_post')
def ad_post():
    if session.get('login'):
        id = request.args.get('id')
        aid = request.args.get('aid')
        ob=Db()
        q = "update ad set type='Posted' where ad_id='" + str(id) + "'"
        ob.update(q)
        ob = Db()
        w = "insert into notification values(null,'Your Advertisement is posted',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob.insert(w)
        return ad_control()
    else:
        return login()

@app.route('/ad_delete')
def ad_delete():
    if session.get('login'):
        id = request.args.get('id')
        aid = request.args.get('aid')
        ob = Db()
        q = "update ad set type='Removed' where ad_id='" + str(id) + "'"
        ob.update(q)
        ob = Db()
        w = "insert into notification values(null,'Your Advertisement is removed',curdate(),'" + str(session['login']) + "','" + str(aid) + "')"
        ob.insert(w)
        return ad_control()
    else:
        return login()


# <-------------------------AGENCY---------------------------------------------->



@app.route('/home2')
def home2():
    return render_template("Agency/Agency homepage.html")

@app.route('/paynow')
def paynow():
    if session.get('login'):
        ob=Db()
        res=ob.selectOne("select agency.agency_name,agency.mob_no from agency where agency_id='"+str(session['login'])+"'")
        return render_template("Agency/paynow.html",data=res)
    else:
        return login()

@app.route('/paynow1',methods=['post'])
def paynow1():
    if session.get('login'):
        cno=request.form['pname']
        cvc=request.form['accno']
        mm=request.form['exp']
        yy=request.form['yy']

        y = "insert into bank VALUES (NULL ,'" + cno + "','"+cvc+"','"+mm+"','"+yy+"','999')"
        ob = Db()
        bkid=ob.insert(y)
        w = "update validity set val_id='" + str(bkid) + "', date=curdate(),exp_date=DATE_ADD(date, INTERVAL 1 YEAR) ,amount='999', status='Payed' where agency_id='" + str(session['login']) + "'"
        ob.update(w)
        x = "update account set balance=balance+999 where login_id= '1'"
        ob.update(x)
        return '''<script>alert('Payment Successfull');window.location='/linkac'</script>'''
    else:
        return login()

@app.route('/linkac')
def linkac():
    if session.get('login'):
        ob=Db()
        res=ob.selectOne("select account.ac_no from account where login_id='"+str(session['login'])+"'")
        if res['ac_no']==None:
             return render_template("Agency/linkac.html")
        else:
            return redirect('/h2')
    else:
        return login()

@app.route('/linkac1',methods=['post'])
def linkac1():
    if session.get('login'):
        sname = request.form['surname']
        acno = request.form['accno']
        ifsc = request.form['ifsc']
        mob = request.form['telephoneNumber']
        mail = request.form['email']
        adrs = request.form['address']
        cty = request.form['city']
        state = request.form['state']
        pin = request.form['PIN']
        ob=Db()
        ob.update("update account set surename='"+sname+"',ac_no='"+acno+"',ifsc='"+ifsc+"',mob='"+mob+"',email='"+mail+"',adrs='"+adrs+"',city='"+cty+"',state='"+state+"',pin='"+pin+"' where login_id='"+str(session['login'])+"'")
        return '''<script>alert('Account Is Linked');window.location='/h2'</script>'''
    else:
        return login()

@app.route('/Add_Package')
def Add_Package():
    if session.get('login'):
        id = request.args.get('id')
        ob = Db()
        q = "select * from package,location where package.package_id='" + str(id) + "' and package.package_id=location.package_id"
        pak = ob.selectOne(q)
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/add package.html",pak=pak,cmp=cmp,ntf=ntf,ag=ag)
    else:
        return login()


@app.route('/Add_Package1',methods=['post'])
def Add_Package1():
    if session.get('login'):
        pname = request.form['PName']
        ctgry = request.form['ctgry']
        dscrptn = request.form['dscptn']
        amt = request.form['amount']
        img = request.files['img']
        lid=session['login']
        session['pname']=pname
        import time
        fname = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(r"G:\trip\static\pimages\\" + fname)

        ob=Db()
        q = "insert into package values(Null,'"+pname+"','" + ctgry + "','" + dscrptn + "','" + amt + "','"+fname+"','"+str(lid)+"','pending')"
        id=ob.insert(q)
        e = "insert into rating values(null,'" + str(lid) + "','0',curdate(),'" + str(id) + "','pending')"
        ob = Db()
        ob.insert(e)
        ob = Db()
        w ="update location set package_id='"+str(id)+"' where loc_id='"+str(session['lcid'])+"'"
        ob.insert(w)
        return View_Package()
    else:
        return login()

@app.route('/location')
def location():
    if session.get('login'):
     return render_template("Agency/gmaps.html")
    else:
        return login()

@app.route('/add_location')
def add_location():
    if session.get('login'):
        lat=request.args.get('lat')
        lon=request.args.get('lon')
        print(lat)
        print(lon)
        ob = Db()
        w = "insert into location values(Null,'" + lat + "','" + lon + "','" + str(id) + "')"
        lcid=ob.insert(w)
        session['lcid']=lcid
        return Add_Package()
    else:
        return login()

@app.route('/View_Package')
def View_Package():
    if session.get('login'):
        lid = session['login']
        ob=Db()
        q="select * from package,location where agencyid='"+str(lid)+"'and  package.package_id=location.package_id order by type='Approved'"
        pak=ob.select(q)
        ln = 0
        if len(pak) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/View Packages.html",val=pak,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()

@app.route('/Remove_Package')
def Remove_Package():
    if session.get('login'):
        id=request.args.get('id')
        ob = Db()
        q = "delete from package where package_id=" + str(id) + ""
        ob.delete(q)
        ob = Db()
        w = "delete from location where package_id=" + str(id) + ""
        ob.delete(w)
        return View_Package()
    else:
        return login()

# @app.route('/Update_Package')
# def Update_Package():
#     id = request.args.get('id')
#     pname = request.form['PName']
#     ctgry = request.form['ctgry']
#     dscrptn = request.form['dscptn']
#     amt = request.form['amount']
#     img = request.files['img']
#
#     import time
#     # if request.files is not None:
#     #     if img.filename != "":
#     fname = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
#     img.save(r"G:\trip\static\pimages\\" + fname)
#
#     q = "update Package set package_name='" + pname + "',ctgory='" + ctgry + "',Decptn='" + dscrptn + "',amount='" + amt + "',photo='" + fname + "',type='pending' where package_id='" + str(id) + "'"
#     ob = Db()
#     ob.update(q)
#     return '''<script>alert('Updated');window.location='/Update_profile'</script>'''
    #     else:
    #         q = "update Package set package_name='" + pname + "',ctgory='" + ctgry + "',Decptn='" + dscrptn + "',amount='" + amt + "',type='pending' where package_id='" + str(id) + "'"
    #         ob = Db()
    #         ob.update(q)
    #         return '''<script>alert('Updated');window.location='/Update_profile'</script>'''
    # else:
    #     q = "update Package set package_name='" + pname + "',ctgory='" + ctgry + "',Decptn='" + dscrptn + "',amount='" + amt + "',type='pending' where package_id='" + str(id) + "'"
    #     ob = Db()
    #     ob.update(q)
    #     return '''<script>alert('Package Updated');window.location='/Add_Package'</script>'''



@app.route('/Add_Guides')
def Add_Guides():
    if session.get('login'):
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/Add guide.html",cmp=cmp,ntf=ntf,ag=ag)
    else:
        return login()

@app.route('/Add_Guides1',methods=['post'])
def Add_Guides1():
    if session.get('login'):
        gname=request.form['gname']
        lid = session['login']
        eid=request.form['email']
        mob=request.form['cntct']
        gexp = request.form['gexp']
        klan = request.form['klan']
        img = request.files['img']
        import time
        fname = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(r"G:\trip\static\guidephoto\\" + fname)

        ob = Db()
        q = "insert into guide values(Null,'" + gname + "','" + str(lid) + "','" + eid+ "','" + mob + "','" + gexp + "','" + klan + "','"+fname+"','free','Null')"
        ob.insert(q)
        return View_Guides()
    else:
        return login()

@app.route('/Remove_Guide')
def Remove_Guide():
    if session.get('login'):
        id = request.args.get('id')
        ob = Db()
        q = "delete from guide where guide_id='" + str(id) + "'"
        ob.delete(q)
        return View_Guides()
    else:
        return login()

@app.route('/f_Guide')
def f_Guide():
    if session.get('login'):
        id = request.args.get('id')
        # ob = Db()
        # x = "delete from booking  where package_id=(select package_id from guide where guide_id='" + str(id) + "')"
        # ob.delete(x)
        ob = Db()
        q = "update guide set status='free',package_id=NULL where guide_id='" + str(id) + "'"
        ob.update(q)
        ob = Db()
        w = "delete from allocate_guide  where guide_id='" + str(id) + "'"
        ob.delete(w)
        ob=Db()
        n="select package_id from guide where guide_id='" + str(id) + "'"
        ob.selectOne(n)
        return View_Guides()
    else:
        return login()


@app.route('/Bookings')
def Bookings():
    if session.get('login'):
        ob = Db()
        q = "select package.*,booking.* from package,booking where package.package_id=booking.package_id and booking.status='Booking' and package.agencyid='"+str(session['login'])+"'"
        res = ob.select(q)
        ln=0
        if len(res)==0:
            ln=1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/booking1.html", data=res,ln=ln,cmp=cmp,ntf=ntf,ag=ag)
    else:
        return login()



@app.route('/Booking2')
def Booking2():
    if session.get('login'):
       pid=request.args.get('pid')
       print(pid)
       id = request.args.get('id')
       print(id )
       ob = Db()
       q = "select package.*,user.*,booking.*,guide.guide_id from user,booking,package left join guide on package.package_id=guide.package_id where package.package_id=booking.package_id and booking.user_id=user.userid and booking.bk_id='"+str(id)+"'"
       res = ob.selectOne(q)
       o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
       ob = Db()
       cmp = ob.selectOne(o)
       w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
       ob = Db()
       ntf = ob.selectOne(w)
       x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
       ob = Db()
       ag = ob.selectOne(x)
       return render_template("Agency/BOOKING2.html",data=res,pid=pid,cmp=cmp,ntf=ntf,ag=ag)
    else:
        return login()

@app.route('/View_Guides')
def View_Guides():
    if session.get('login'):
        ob = Db()
        pid = request.args.get('pid')
        id = request.args.get('bid')
        uid=None
        if pid is not None :
         q = "select * from guide where package_id='"+str(pid)+"' and status='Requested'"
         res = ob.select(q)
         uid = request.args.get('uid')
         ln = 0
         if len(res) == 0:
             ln = 1
        else:
          q = "select * from guide where agency_id='" + str(session['login']) + "'order by status='free' "
          res = ob.select(q)
          ln = 0
          if len(res) == 0:
              ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/View Guides.html",data=res,data1=id,cmp=cmp,ntf=ntf,ag=ag,ln=ln,uid=uid)
    else:
        return login()

# @app.route('/View_Guides1')
# def View_Guides1():
#     ob = Db()
#     id = request.args.get('bid')
#     pid = request.args.get('pid')
#     print(pid)
#     session['bid']=id
#     q = "select * from guide where agency_id='"+str(session['login'])+"' and package_id='"+str(pid)+"' and status='Requested'"
#     res = ob.select(q)
#     return render_template("Agency/View Guides.html",data=res,data1=id)

@app.route('/Allocate')
def Allocate():
    if session.get('login'):
        gid=request.args.get('gid')
        bid=request.args.get('bid')
        uid = request.args.get('uid')
        ob = Db()
        q = "insert into allocate_guide values(Null,'" + str(gid)+"','"+str(uid)+"')"
        ob.insert(q)
        w = "update booking set status='Payment pending' where bk_id='"+str(bid)+"'"
        ob.update(w)
        z = "update guide set status='Allocated' where guide_id='" + str(gid) + "'"
        ob.update(z)
        ob=Db()
        pak=ob.selectOne("select package.package_name from package,booking where package.package_id=booking.package_id and booking.bk_id='"+str(bid)+"'")
        ob = Db()
        x = "insert into notification values(null,'You Booked " + str(pak['package_name']) + " is accepted and now you can pay the amount for the package through card payment',curdate(),'" + str(session['login']) + "','" + str(uid) + "')"
        ob.insert(x)
        return '''<script>alert('Allocated Succesfully');window.location='/View_Bookings'</script>'''
    else:
        return login()

@app.route('/View_Bookings')
def View_Bookings():
    if session.get('login'):
        db = Db()
        res = db.select("select user.*,package.*,booking.*,guide.guide_name,guide.email_id,guide.mob_no,agency.agency_id from user,package join agency on package.agencyid=agency.agency_id,booking left join guide on booking.package_id=guide.package_id where user.userid=booking.user_id and booking.package_id=package.package_id  and package.agencyid='"+str(session['login'])+"' and booking.status!='booking' group by booking.bk_id")
        ln = 0
        if len(res) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/View Bookings.html",data=res,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()

@app.route('/receipt')
def receipt():
    id=request.args.get('uid')
    pid=request.args.get('pid')
    bid = request.args.get('bid')
    ob=Db()
    res=ob.selectOne("select user.*,package.package_name,package.amount as amt,booking.*,payment.payment_id,round(payment.amount,1) as amount,payment.date from user,package,payment,booking where user.userid='"+str(id)+"' and package.package_id='"+str(pid)+"' and payment.user_id=user.userid and payment.package_id=package.package_id and booking.bk_id='"+str(bid)+"'")
    ob=Db()
    pic=ob.selectOne("select agency.* from agency where agency_id='"+str(session['login'])+"'")
    tamount = ((int(res['kids']) + int(res['adults'])) * int(res['amt']))
    aamt=round(float(res['amount'])*(5/100),1)
    aa = round(float(res['amount'])* (95 / 100), 1)
    return render_template("Agency/receipt.html",data=res,tamt=tamount,aamt=aamt,agmt=aa,pic=pic)

@app.route('/cbooking')
def cbooking():
    if session.get('login'):
        bid=request.args.get('bid')
        gid = request.args.get('gid')
        uid = request.args.get('uid')
        ob = Db()
        pak = ob.selectOne("select package.package_name from package,booking where package.package_id=booking.package_id and booking.bk_id='" + str(bid) + "'")
        ob = Db()
        q="delete from booking where bk_id='"+str(bid)+"'"
        ob.update(q)
        ob = Db()
        x = "insert into notification values(null,'You Booked " + str(pak['package_name']) + " is Rejected by the agency due to some reasons,Please book again the package with proper arguments for your trip',curdate(),'" + str(session['login']) + "','" + str(uid) + "')"
        ob.insert(x)
        ob = Db()
        y="update guide set status='free',package_id=NULL where guide_id='"+str(gid)+"'"
        ob.update(y)
        return '''<script>alert('Booking Canceled');window.location='/Bookings'</script>'''
    else:
        return login()

@app.route('/Complaints')
def Complaints():
    if session.get('login'):
        ob = Db()
        q = "select user.username,complaint.* from complaint,user where complaint.user_id=user.login_id and complaint.agency_id='"+str(session['login'])+"' "
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/Complaints.html", data=res,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()

# @app.route('/reply')
# def reply():
#     id = request.args.get('id')
#     return render_template("Agency/Replay.html",data=id)
#
# @app.route('/reply1/<a>',methods=['post'])
# def reply1(a):
#     reply = request.form['Reply']
#     q = "update complaint set reply='"+reply+"',rdate=curdate() where cmplt_id='" + a+"'"
#     ob = Db()
#     ob.update(q)
#     return Complaints()



@app.route('/Feedback')
def Feedback():
    if session.get('login'):
        ob = Db()
        q = "select * from feedback,user where feedback.user_id=user.login_id and feedback.agency_id='"+str(session['login'])+"' order by date desc"
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/View Feedbacks.html",data=res,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()


@app.route('/Add_ads')
def Add_ads():
    if session.get('login'):
        ob = Db()
        q = "select * from ad where agency_id='"+str(session['login'])+"'"
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/Add ads.html",data=res,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()

@app.route('/Add_ads1',methods={'post'})
def Add_ads1():
    if session.get('login'):
        img = request.files['img']
        lid = session['login']

        import time
        fname = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(r"G:\trip\static\ads\\" + fname)

        ob = Db()
        q = "insert into ad values(Null,'"+str(lid)+"','" + fname + "',curdate(),'pending')"
        ob.insert(q)
        return Add_ads()
    else:
        return login()

@app.route('/ad_dlt')
def ad_dlt():
    if session.get('login'):
        id = request.args.get('id')
        ob=Db()
        q = "delete from ad where ad_id='" + str(id) + "'"
        ob.delete(q)
        return Add_ads()
    else:
        return login()



@app.route('/Send_Notification')
def Send_Notification():
    if session.get('login'):
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/Notification.html",cmp=cmp,ntf=ntf,ag=ag)
    else:
        return login()

@app.route('/Send_Notification1',methods=['POST'])
def Send_Notification1():
    if session.get('login'):
       noti =request.form['ntfn']
       lid = session['login']

       q="insert into notification values(null,'"+noti+"',curdate(),'"+str(lid)+"','User')"
       ob=Db()
       ob.insert(q)
       return Send_Notification()
    else:
        return login()

@app.route('/View_Notification')
def View_Notification():
    if session.get('login'):
        ob = Db()
        q = "select * from notification where Type='Agency' or Type='All' or type='"+str(session['login'])+"' order by notfcn_id desc"
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/View Notifications.html",data=res,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()

@app.route('/view_notdlt1')
def view_notdlt1():
    if session.get('login'):
        id = request.args.get('id')
        q = "delete from notification where notfcn_id='" +str(id)+"'"
        ob=Db()
        ob.delete(q)
        return '''<script>alert('Deleted');window.location='/View_Notification'</script>'''
    else:
        return login()

@app.route('/view_Enquiry')
def view_Enquiry():
    if session.get('login'):
        db = Db()
        res = db.select("select package.package_name,enquiry.* from enquiry inner join package on enquiry.pid = package.package_id and package.agencyid = '"+str(session['login'])+"'")
        ln = 0
        if len(res) == 0:
            ln = 1
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='"+str(session['login'])+"' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/View Enquiry.html", data = res,cmp=cmp,ntf=ntf,ag=ag,ln=ln)
    else:
        return login()

@app.route('/Enquired')
def Enquired():
    if session.get('login'):
        id = request.args.get('id')
        uid = request.args.get('uid')
        ob = Db()
        q = "update enquiry set status='Enquired' where eid='" + str(id) + "'"
        ob.update(q)
        ob = Db()
        w = "insert into notification values(null,'Your Enquiry is checked and we will contact you soon',curdate(),'" + str(session['login']) + "','" + str(uid) + "')"
        ob.insert(w)
        return view_Enquiry()
    else:
        return login()

@app.route('/Edelete')
def Edelete():
    if session.get('login'):
        id = request.args.get('id')
        uid = request.args.get('uid')
        ob = Db()
        q = "delete from enquiry where eid='" + str(id) + "'"
        ob.delete(q)
        ob = Db()
        w = "insert into notification values(null,'Your Enquiry is deleted',curdate(),'" + str(session['login']) + "','" + str(uid) + "')"
        ob.insert(w)
        return view_Enquiry()
    else:
        return login()

@app.route('/profile')
def profile():
    if session.get('login'):
        d = date.today()
        ob=Db()
        val=ob.selectOne("select * from agency,validity where agency.agency_id=validity.agency_id and agency.agency_id='"+str(session['login'])+"'")
        o = "select complaint.cmplt,complaint.date,user.username,user.profile_pic from user,complaint where complaint.user_id=user.userid and complaint.agency_id='" + str(session['login']) + "' order by cmplt_id desc"
        ob = Db()
        cmp = ob.selectOne(o)
        w = "select notification.notfcn_ctnt,notification.date from notification where type='All' or type='Agency' or type='" + str(session['login']) + "' order by notfcn_id desc"
        ob = Db()
        ntf = ob.selectOne(w)
        x = "select agency.agency_name,agency.cover from agency where agency_id='" + str(session['login']) + "'"
        ob = Db()
        ag = ob.selectOne(x)
        return render_template("Agency/agency profile.html",cmp=cmp,ntf=ntf,ag=ag,val=val,d=d)
    else:
        return login()

@app.route('/profile1', methods=['POST'])
def profile1():
        if session.get('login'):
            place = request.form['place']
            po = request.form['po']
            pin = request.form['pin']
            mob = request.form['mob']
            img = request.files['img']

            import time
            if request.files is not None:
                if img.filename != "":
                    fname = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
                    img.save(r"G:\trip\static\licence\cover\\" + fname)

                    q = "update agency set place='" + place + "',postoffice='" + po + "',pin='" + pin + "',mob_no='" + mob + "',cover='" + fname + "' where agency_id='" + str(session['login']) + "'"
                    ob = Db()
                    ob.update(q)
                    return profile()
                else:
                    q = "update agency set place='" + place + "',postoffice='" + po + "',pin='" + pin + "',mob_no='" + mob + "' where agency_id='" + str(session['login']) + "'"
                    ob = Db()
                    ob.update(q)
                    return profile()
            else:
                q = "update agency set place='" + place + "',postoffice='" + po + "',pin='" + pin + "',mob_no='" + mob + "' where agency_id='" + str(session['login']) + "'"
                ob = Db()
                ob.update(q)
                return profile()
        else:
            return login()
# <-------------------------USER---------------------------------------------->


@app.route('/home3')
def home3():
    return render_template("User/User homepage.html")
@app.route('/Update_profile')
def Update_profile():
    if session.get('login'):
        lid = session['login']
        q="select * from user where login_id='"+str(lid)+"'"
        ob = Db()
        res=ob.selectOne(q)
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/Upadet profile.html",data=res,pic=pic)
    else:
        return login()

@app.route('/Update/<a>',methods=['POST'])
def Update(a):
    if session.get('login'):
        place = request.form['Place']
        po = request.form['PO']
        pin = request.form['PIN']
        # dob = request.form['dob']
        mob = request.form['Mob']
        img = request.files['img']

        import time
        if request.files is not None:
            if img.filename!="":
                fname = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
                img.save(r"G:\trip\static\profilepic\\" + fname)

                q="update user set place='"+place+"',postoffice='"+po+"',pin='"+pin+"',mobile_number='"+mob+"',profile_pic='"+fname+"' where login_id='"+str(a)+"'"
                ob=Db()
                ob.update(q)
                return Update_profile()
            else:
                q = "update user set place='" + place + "',postoffice='" + po + "',pin='" + pin + "',mobile_number='" + mob + "' where login_id='" + str(a) + "'"
                ob = Db()
                ob.update(q)
                return Update_profile()
        else:
            q = "update user set place='" + place + "',postoffice='" + po + "',pin='" + pin + "',mobile_number='" + mob + "' where login_id='" + str(a) + "'"
            ob = Db()
            ob.update(q)
            return Update_profile()
    else:
        return login()


@app.route('/Trending')
def Trending():
    id = None
    type= None


    if session.get('login'):

       id=session['login']

    if session.get('type'):

       type=session['type']

    q = "select package.*,location.*,trending.*,agency.agency_name,agency.agency_id,round(avg(rating.rating),0) from package,trending,agency,location,rating where package.package_id=trending.package_id and agency.agency_id=package.agencyid and location.package_id=package.package_id and trending.package_id=rating.package_id group by rating.package_id"
    ob = Db()
    res=ob.select(q)
    ln = 0
    if len(res) == 0:
        ln = 1
    if session:
      w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
      ob = Db()
      pic = ob.selectOne(w)
      return render_template("User/view trending.html",val=res,lid=id,tp=type,pic=pic,ln=ln)
    else:
        return render_template("User/view trending.html", val=res, lid=id, tp=type,ln=ln)

@app.route('/Enquiry')
def Enquiry():
    res = None
    pid = request.args.get('pid')
    d=date.today()
    if session:
       id=session['login']
       qry = "select user.username,user.mail,user.mobile_number,user.login_id from user,login where login.Login_id = user.login_id and login.type='user' and user.login_id = '"+str(id)+"'"
       ob = Db()
       res = ob.selectOne(qry)
       w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
       ob = Db()
       pic = ob.selectOne(w)
       return render_template("User/Enquiry&book.html",val=res,pid=str(pid),pic=pic,d=d)
    else:
        return render_template("User/Enquiry&book.html", val=res, pid=str(pid),d=d)



@app.route('/Enquiry_now',methods=['post'])
def Enquiry_now():
    id=request.form['pid']
    session['pid']=id
    name=request.form['name']
    mail=request.form['mail']
    phno=request.form['phno']
    adults=request.form['Adults']
    kids=request.form['kids']
    date=request.form['date']
    details=request.form['add']
    uid = 'null'
    if session.get('login'):
        uid = session['login']
    q="insert into enquiry values(null,'"+str(id)+"','"+name+"','"+mail+"','"+phno+"','"+adults+"','"+kids+"','"+date+"','"+details+"','pending',curdate(),'"+str(uid)+"')"
    ob=Db()
    ob.insert(q)
    if session.get('login'):
     return rating()
    else:
        return '''<script>alert('Enquiry is Submited,For Booking Login your Account');window.location='/login'</script>'''

@app.route('/Book_Enquiry')
def Book_Enquiry():
    if session.get('login'):
           res = None
           pid = request.args.get('pid')
           d = date.today()
           id=session['login']
           qry = "select user.username,user.mail,user.mobile_number,user.login_id from user,login where login.Login_id = user.login_id and login.type='user' and user.login_id = '"+str(id)+"'"
           ob = Db()
           res = ob.selectOne(qry)
           w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
           ob = Db()
           pic = ob.selectOne(w)
           return render_template("User/Book enquiry.html",val=res,pid=str(pid),pic=pic,d=d)
    else:
        return login()

@app.route('/Book_Enquiry_Now',methods=['post'])
def Book_Enquiry_Now():
    if session.get('login'):
        id=request.form['pid']
        session['pid']=id
        lid = session['login']
        adults=request.form['Adults']
        kids=request.form['kids']
        date=request.form['date']
        details=request.form['add']
        q="insert into booking values(null,'"+str(id)+"','"+str(lid)+"',curdate(),'"+adults+"','"+kids+"','"+date+"','"+details+"','Booking')"
        ob=Db()
        ob.insert(q)
        return '''<script>var r = confirm("Do You Want Guide");
                if (r == true)
                 {
                     window.location='/view_Guides'
                 } 
                 else 
                 {
                         window.location='/rating'
                 }</script>'''
    else:
        return login()

@app.route('/view_enquiries')
def view_enquiries():
    if session.get('login'):
        db = Db()
        res = db.select("select user.*,agency.agency_id,agency.agency_name,package.*,enquiry.*,location.* from user,package,agency,location,enquiry  where user.userid=enquiry.user_id and enquiry.user_id='" + str(session['login']) + "' and enquiry.pid=package.package_id  and package.agencyid=agency.agency_id and location.package_id=package.package_id group by enquiry.eid order by enquiry.eid desc")
        ln = 0
        if len(res) == 0:
            ln = 1
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/View Enquiries.html",data=res,pic=pic,ln=ln)
    else:
        return login()

@app.route('/view_bookings')
def view_bookings():
    if session.get('login'):
        db = Db()
        res = db.select("select user.*,agency.agency_id,agency.agency_name,package.*,booking.*,guide.guide_id,guide.guide_name,guide.email_id,guide.mob_no,location.* from user,package,agency,location,booking left join guide on booking.package_id=guide.package_id  where user.userid=booking.user_id and booking.user_id='" + str(session['login']) + "' and booking.package_id=package.package_id  and package.agencyid=agency.agency_id and location.package_id=package.package_id group by booking.bk_id order by booking.bk_id desc")
        ln = 0
        if len(res) == 0:
            ln = 1
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/view bookings.html",data=res,pic=pic,ln=ln)
    else:
        return login()

@app.route('/view_Guides')
def view_Guides():
    if session.get('login'):
        id = session['pid']
        ob = Db()
        q = "select * from guide where status='free' and agency_id=(SELECT agencyid from package where package_id='"+str(id)+"')"
        res = ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/View Guides.html",data=res,pid=id,pic=pic,ln=ln)
    else:
        return login()

@app.route('/Guides/<i>/<j>')
def Guides(i,j):
    if session.get('login'):
        # id=request.args.get('id')
        print(i)
        # pid = request.args.get('pid')
        print(j)
        session['pid'] = j
        ob=Db()
        q="update guide set status='Requested',package_id='"+str(j)+"' where guide_id='"+str(i)+"'"
        ob.update(q)
        return '''<script>alert('Booking Successfull');window.location='/rating'</script>'''
    else:
        return login()

@app.route('/Book_now')
def Book_now():
    if session.get('login'):
        pid = request.args.get('pid')
        bid = request.args.get('id')
        aid = request.args.get('aid')
        session['bkid'] = bid
        session['aid'] = aid
        q = "select package.*,user.*,booking.adults,booking.kids from package,user,booking where package.package_id='"+str(pid)+"' and booking.package_id=package.package_id and user.userid='"+str(session['login'])+"'"
        ob = Db()
        res=ob.selectOne(q)
        tamount=((int(res['kids'])+int(res['adults']))*int(res['amount']))
        if int(res['kids'])>=10 and int(res['adults'])>=25:
            kamount=round((int(res['kids'])*int(res['amount']))*(80/100),1)
            aamount = round((int(res['adults']) * int(res['amount'])) * (90 / 100),1)
        elif int(res['kids'])<=10 and int(res['adults'])>=25:
            kamount = round((int(res['kids']) * int(res['amount'])) * (95 / 100),1)
            aamount=round((int(res['adults'])*int(res['amount']))*(90/100),1)
        elif int(res['kids'])>=10 and int(res['adults'])<=25:
            kamount = round((int(res['kids']) * int(res['amount'])) * (80 / 100),1)
            aamount=round((int(res['adults'])*int(res['amount']))*(95/100),1)
        else:
            kamount=round((int(res['kids'])*int(res['amount']))*(95/100),1)
            aamount=round((int(res['adults'])*int(res['amount'])) * (95 / 100),1)

        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/booking.html",data=res,pic=pic,k=kamount,a=aamount,t=tamount)
    else:
        return login()

@app.route('/Book_now1')
def Book_now1():
    if session.get('login'):
        id=request.args.get('pid')
        q = "select package.*,user.*,booking.bk_id from package,user where package.package_id='"+str(id)+"' and user.userid='"+str(session['login'])+"' and booking.pa"
        ob = Db()
        res=ob.selectOne(q)
        return render_template("User/booking.html",data=res)
    else:
        return login()

@app.route('/Pay',methods=['post'])
def Pay():
    if session.get('login'):
        # pid=request.args.get['pid']
        # amount=request.args.get['amt']
        pid = request.form['pkid']
        amount = request.form['amt']
        cno=request.form['pname']
        cvc=request.form['accno']
        mm=request.form['exp']
        yy=request.form['yy']
        lid = session['login']
        session['pid']=pid

        # adamount=(amount)*(90/100)
        # agamount=amount-adamount
        ob = Db()
        pak = ob.selectOne("select package.package_name,user.username from package,booking,user where package.package_id=booking.package_id and booking.bk_id='" + str(session['bkid']) + "' and user.userid='" + str(session['login']) + "'")
        ob = Db()
        d = "insert into notification values(null,'"+str(pak['username'])+" is payed amount for "+str(pak['package_name'])+"' ,curdate(),'" + str(session['login']) + "','" + str(session['aid']) + "')"
        ob.insert(d)
        y = "insert into bank VALUES (NULL ,'" + cno + "','"+cvc+"','"+mm+"','"+yy+"','"+amount+"')"
        ob = Db()
        bkid=ob.insert(y)
        w = "update booking set status='Payed' where bk_id='" + str(session['bkid']) + "'"
        ob.update(w)
        z = "insert into payment VALUES ('" + str(bkid) + "','" + amount + "',curdate(),'" + str(lid) + "','" + str(pid) + "')"
        ob = Db()
        ob.insert(z)
        ob=Db()
        x = "update account set balance=balance + ('"+amount+"'*(5/100)) where login_id='1'"
        ob.update(x)
        ob = Db()
        m = "update account set balance=balance + ('"+amount+"'*(95/100)) where login_id='"+str(session['aid'])+"'"
        ob.update(m)
        return '''<script>alert('Payment Successfull');window.location='/invoice'</script>'''
    else:
        return login()

@app.route('/invoice')
def invoice():
    ob=Db()
    res=ob.selectOne("select agency.agency_name,agency.place as aplace,agency.postoffice as apo,agency.pin as apin,agency.email,agency.mob_no,user.username,user.place,user.postoffice,user.pin,user.mail,user.mobile_number,booking.adults,booking.kids,booking.status,package.package_name,package.amount as amt,payment.payment_id,round(payment.amount,1) as amount,payment.date from agency,user,booking,package,payment where agency.agency_id='"+str(session['aid'])+"' and user.userid='"+str(session['login'])+"' and package.package_id='"+str(session['pid'])+"' and booking.bk_id='"+str(session['bkid'])+"' and payment.package_id=booking.package_id")
    tamount = ((int(res['kids']) + int(res['adults'])) * int(res['amt']))
    damt=round(tamount-float(res['amount']),1)
    return render_template("User/receipt.html",data=res,tamt=tamount,damt=damt)

@app.route('/cancel_booking/<bkid>/<gid>')
def cancel_booking(bkid,gid):
    if session.get('login'):
        ob = Db()
        pak = ob.selectOne("select package.package_name,user.username from package,booking,user where package.package_id=booking.package_id and booking.bk_id='" +str(bkid) + "' and user.userid='" + str(session['login']) + "'")
        ob = Db()
        d = "insert into notification values(null,'" + str(pak['username']) + " is canceled  " + str(pak['package_name']) + "',curdate(),'" + str(session['login']) + "','" + str(session['aid']) + "')"
        ob.insert(d)
        ob = Db()
        q="delete from booking where bk_id='"+str(bkid)+"'"
        ob.delete(q)
        ob = Db()
        y="update guide set status='free',package_id=NULL where guide_id='"+str(gid)+"'"
        ob.update(y)
        return '''<script>alert('Booking Canceled');window.location='/view_bookings'</script>'''
    else:
        return login()

@app.route('/rating2')
def rating2():
    if session.get('login'):
        pid = request.args.get('pid')
        session['pid']=pid
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/Review.html",pic=pic)
    else:
        return login()


@app.route('/rating')
def rating():
    if session.get('login'):
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/Review.html",pic=pic)
    else:
        return login()

@app.route('/rating1',methods=['post'])
def rating1():
    if session.get('login'):
        rvw=request.form['Review']
        pid=session['pid']
        id=session['login']
        q = "insert into rating values(null,'" + str(id) + "','" + str(rvw) + "',curdate(),'" + str(pid) + "','pending')"
        ob = Db()
        ob.insert(q)
        # w="insert into review values(null,'" + str(rvw) + "',curdate(),'" + str(id) + "','User')"
        # ob=Db()
        # ob.insert(w)
        return '''<script>alert('Thank You');window.location='/'</script>'''
    else:
        return login()

@app.route('/View_Packages')
def View_Packages():
    q="select package.*,location.*,agency.agency_name,agency.agency_id,round(avg(rating.rating),0) from package,agency,location,rating where package.type='Approved' and agency.agency_id=package.agencyid and location.package_id=package.package_id and package.package_id=rating.package_id group by rating.package_id"
    ob=Db()
    res=ob.select(q)
    ln = 0
    if len(res) == 0:
        ln = 1
    if session:
      w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
      ob = Db()
      pic = ob.selectOne(w)
      return render_template("User/View & search package.html",val=res,pic=pic,ln=ln)
    else:
        return render_template("User/View & search package.html", val=res,ln=ln)

@app.route('/View_Packages1',methods=['post'])
def View_Packages1():
    search = request.form['Search']
    ob = Db()
    q = "select package.*,location.*,agency.agency_name,agency.agency_id,round(avg(rating.rating),0) from package,agency,location,rating where package.type='Approved' and agency.agency_id=package.agencyid and location.package_id=package.package_id and package.package_id=rating.package_id and package_name like '%"+search+"%' group by rating.package_id"
    res = ob.select(q)
    ln = 0
    if len(res) == 0:
        ln = 1
    if session:
      w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
      ob = Db()
      pic = ob.selectOne(w)
      return render_template("User/View & search package.html", val=res,pic=pic,ln=ln)
    else:
        return render_template("User/View & search package.html", val=res,ln=ln )


@app.route('/Send_Complaints')
def Send_Complaints():
    if session.get('login'):
        id = request.args.get('id')
        session['id']=id
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/complaints.html",pic=pic)
    else:
        return login()

@app.route('/Send_Complaints1',methods=['POST'])
def Send_Complaints1():
    if session.get('login'):
       cmplt =request.form['cmplts']
       lid = session['login']
       id = session['id']
       q="insert into complaint values(null,'"+str(lid)+"','"+cmplt+"',curdate(),'pending','pending','"+str(id)+"')"
       ob=Db()
       ob.insert(q)
       return '''<script>alert('Complaint Sended');window.location='/ '</script>'''
    else:
        return login()

@app.route('/View_Reply')
def View_Reply():
    if session.get('login'):
        lid = session['login']
        q="select complaint.*,agency.agency_name from complaint,agency where complaint.user_id='"+str(lid)+"' and complaint.agency_id=agency.agency_id group by complaint.cmplt_id order by cmplt_id desc"
        ob=Db()
        res=ob.select(q)
        ln = 0
        if len(res) == 0:
            ln = 1
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/view replay.html",val=res,pic=pic,ln=ln)
    else:
        return login()

@app.route('/feedback')
def feedback():
    if session.get('login'):
        id = request.args.get('id')
        session['id'] = id
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/Feedback.html",pic=pic)
    else:
        return login()

@app.route('/Send_feedback',methods=['POST'])
def Send_feedback():
    if session.get('login'):
       fdbk =request.form['fedbkncmplt']
       lid = session['login']
       id = session['id']
       q="insert into feedback values(null,'"+str(lid)+"',curdate(),'"+fdbk+"','"+str(id)+"')"
       ob=Db()
       ob.insert(q)
       return '''<script>alert('Feedback Sended');window.location='/ '</script>'''
    else:
        return login()

@app.route('/Notification')
def Notification():
    if session.get('login'):
        q = "select notfcn_ctnt,day(date),month(date),year(date) from notification where type='User' or type='All' or type='"+str(session['login'])+"' order by notfcn_id desc"
        ob = Db()
        res = ob.select(q)
        w = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(w)
        return render_template("User/Notifications.html",val=res,pic=pic)
    else:
        return login()

@app.route('/View_agency')
def View_agency():
    id = request.args.get('id')
    q = "select * from agency where agency_id='"+str(id)+"'"
    ob = Db()
    res = ob.selectOne(q)
    w = "select * from package where type='Approved' and agencyid='" + str(id) + "'"
    ob = Db()
    pk = ob.select(w)
    x = "select * from ad where agency_id='" + str(id) + "' order by date desc"
    ob = Db()
    ad = ob.select(x)
    ob = Db()
    g = "select * from guide where agency_id='" + str(id) + "'"
    gud = ob.select(g)
    if session:
        z = "select userid,profile_pic from user where login_id='" + str(session['login']) + "'"
        ob = Db()
        pic = ob.selectOne(z)
        return render_template("User/agency profile.html", val=res,data=pk,ad=ad,pic=pic,gud=gud,id=id)
    return render_template("User/agency profile.html", val=res, data=pk,ad=ad,gud=gud)



if __name__ == '__main__':
    app.run(debug=True)
