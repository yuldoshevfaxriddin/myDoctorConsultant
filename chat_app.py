from flask import Flask,session,render_template,request,url_for,redirect
from flask_socketio import SocketIO, send, emit
import datetime
import settings
import json
import chat_db

app = Flask(__name__)
app.secret_key=settings.SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*",)

@socketio.on('connect')
def socketConnect():
    if 'user' in session:
        user = session['user']
        user['request_session'] = request.sid 
        result = chat_db.checkUserSession(user)
        print(result)
        print(user)
        print('user login home')
    else:
        print('user not login')
    print(session)
     
@socketio.on("sendMessage")
def sendMessage(message):
    print(message)
    data = json.loads(message)
    user_id_1 = data['user_id_1'] # client 
    user_id_2 = data['user_id_2'] # current user
    text = data['text']
    data['user_img_1'] = chat_db.getUser(user_id=user_id_1)[0][4]
    data['user_img_2'] = chat_db.getUser(user_id=user_id_2)[0][4]
    data['user_name_1'] = chat_db.getUser(user_id=user_id_1)[0][1]
    data['user_name_2'] = chat_db.getUser(user_id=user_id_2)[0][1]
    data['user_bio_1'] = chat_db.getUser(user_id=user_id_1)[0][5]
    data['user_bio_2'] = chat_db.getUser(user_id=user_id_2)[0][5]
    data['time'] = datetime.datetime.timestamp(datetime.datetime.now())
    chat_info = chat_db.checkPersonalChat(user_id_1,user_id_2)[0]
    chat_id = chat_info[0]
    chat_db.insertPersonalMessage(chat_id,user_id_2,text)
    print("chat insert yakunlandi")
    user_request_id = chat_db.getUserRequestId(user_id_1)
    print(user_request_id)
    # habarlarni yuborish
    # print(request.sid,message)
    print(user_request_id,chat_info)
    # send(message, broadcast=True,to=user_request_id)
    emit('sendMessage',json.dumps(data), broadcast=True,to=user_request_id)

@app.route('/')
def home():
    print('user' in session)
    return  render_template('home.html')

@app.route('/about')
def about():
    return  render_template('about.html')

@app.route('/services')
def services():
    return  render_template('services.html')

@app.route('/news')
def news():
    return  render_template('news.html')

@app.route('/contact')
def contact():
    return  render_template('contact.html')

@app.route('/doctors',methods=['GET','POST'])
def doctors():
    regions = chat_db.getRegions()
    mutaxasislik = chat_db.getMutaxaslik()
    doctors = None
    if request.method == 'POST':
        region_id = request.form.get('region',None)
        m_id = request.form.get('mutaxasislik',None)
        t1 = (region_id == None) and (m_id == None) # ikkalasi ham kiritilmasa 
        t2 = (region_id != None) and (m_id == None) # m_id kiritilmasa
        t3 = (region_id == None) and (m_id != None) # region kiritilmasa
        t4 = (region_id != None) and (m_id != None) # ikkalasi ham kiritsa
        doctors = chat_db.getDoctorsFilter(t1=t1,t2=t2,t3=t3,t4=t4,r_id=region_id,m_id=m_id)
    else:
        doctors = chat_db.getDoctors()
    return  render_template('doctors.html',doctors=doctors,regions=regions,mutaxasislik=mutaxasislik)

@app.route('/doctor/<doctor_id>')
def doctorProfile(doctor_id):
    respons = chat_db.getUser(doctor_id)
    if len(respons)==0:
        return redirect(url_for('doctors'))
    doctor = respons[0]
    role_key = 'doctor'
    if doctor[6] != role_key:
        return  redirect(url_for('doctors'))
    return  render_template('doctor/profile.html',doctor=doctor)


@app.route('/get-messages')
def getMessages():
    user_1 = request.args.get('user_1')
    user_2 = request.args.get('user_2')
    chat_id = chat_db.checkPersonalChat(user_1,user_2)[0][0]
    data = chat_db.getPersonalChatsMessages(chat_id)
    print('data',data)
    return json.dumps(data)

@app.route('/login',methods=['GET','POST'])
def login():
    print(session)
    if 'user' in session: 
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username',None)
        password = request.form.get('password',None)

        print(username,password)
        check_user = chat_db.checkUser(username,password)
        print('chekuser',check_user)
        if len(check_user)==1:
            check_user = check_user[0]
            print(check_user)
            if check_user[2]== username and check_user[3]==password:
                print('login succes')
                current_user = {
                    'name':check_user[1],
                    'username':username,
                    'password':password,
                    'id': check_user[0],
                    'created_at':check_user[7],
                    'user_role':check_user[6],
                    'user_bio':check_user[5],
                    'user_image':check_user[4]
                }
                session['status'] = 'Tizimga kirildi'
                session['user'] = current_user
                if 'nextUrl' in session:
                    nextUrl = session['nextUrl']
                    session.pop('nextUrl')
                    return redirect(nextUrl)
                return redirect(url_for('home'))
        print('not login')
    return render_template('login.html')

@app.route('/register-user',methods=['GET','POST'])
def registerUser():
    if 'user' in session:
        return redirect(url_for('home'))
    if request.method =='POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        check_user = chat_db.checkUser(username,password)
        if password != password_confirm:
            error = 'Parolar xar hil'
            return  render_template('register_user.html',error=error)
        if len(check_user) != 0:
            error = 'Foydalanuvchi nomi mavjud'
            return  render_template('register_user.html',error=error)
        user = {
            'name':name,
            'username':username,
            'password':password,
            'user_bio':'Tizim foydalanuvchisi',
            'user_image':'images/default-person.png',
            'user_role':'bemor'
        }
        user['id'] = chat_db.createUser(user)
        print(user)
        print('register  succes !')
        session['user'] = user
        # users = chat_db.getAllUsers()
        return redirect(url_for('home'))
    return  render_template('register_user.html')
@app.route('/register-doctor',methods=['GET','POST'])
def registerDoctor():
    regions = chat_db.getRegions()
    m = chat_db.getMutaxaslik()

    if 'user' in session:
        return redirect(url_for('home'))
    if request.method =='POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        region_id = request.form.get('region')
        mut_id = request.form.get('mut')
        if password != password_confirm:
            error = 'Parollar xar hil'
            return  render_template('register_doctor.html',error=error,regions=regions,mut=m)
        check_user = chat_db.checkUser(username,password)
        if len(check_user) != 0:
            error = 'Foydalanuvchi nomi mavjud'
            return  render_template('register_doctor.html',error=error,regions=regions,mut=m)
        user = {
            'name':name,
            'username':username,
            'password':password,
            'user_bio':'Tizim foydalanuvchisi',
            'user_image':'images/default-person.png',
            'user_role':'doctor'
        }
        user['id'] = chat_db.createUser(user)
        chat_db.insertRegionUser(user['id'],region_id)
        chat_db.insertMutaxasislik(user['id'],mut_id)
        print(user)
        print('register  succes !')
        session['user'] = user
        # users = chat_db.getAllUsers()
        return redirect(url_for('home'))
    return  render_template('register_doctor.html',regions=regions,mut=m)

@app.route('/logout')
def logout():
    session.pop('user')
    return  redirect(url_for('home'))

@app.route('/message-page')
def messagePage():
    # status = session['status'] if 'status' in session else None 
    status = None
    if 'status' in session:
        status = session['status']
        session.pop('status')
    if 'user' not in session:
        session['nextUrl'] = url_for('messagePage')
        return redirect(url_for('login'))
    user = session['user']
    users = chat_db.getPersonalChats(user)
    doctor = None
    # users = chat_db.getAllUsers()
    return render_template('message-test.html',users=users,current_user=user,status=status,client_doctor=doctor)
@app.route('/message-page/<id>/')
def messagePage_2(id):
    # status = session['status'] if 'status' in session else None 
    status = None
    if 'status' in session:
        status = session['status']
        session.pop('status')
    if 'user' not in session:
        session['nextUrl'] = url_for('messagePage_2',id=id)
        return redirect(url_for('login'))
    user = session['user']
    if str(user['id']) == str(id):
        return redirect(url_for('messagePage'))
    users = chat_db.getPersonalChats(user)
    doctor = None
    if id :
        doctor = chat_db.getUser(id)[0]
    # users = chat_db.getAllUsers()
    return render_template('message-test.html',users=users,current_user=user,status=status,client_doctor=doctor)

@app.route('/create-personal-chat',methods=['POST'])
def createChat():
    if request.method == 'POST' and 'user' in session:
        
        print()
        

if __name__=='__main__':
    # app.run(debug=False)
    socketio.run(app=app,host=settings.HOST_SERVER,debug=settings.DEBUG,port=settings.PORT)