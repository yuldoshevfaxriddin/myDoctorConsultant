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

@app.route('/doctors')
def doctors():
    doctors = chat_db.getDoctors()
    return  render_template('doctors.html',doctors=doctors)

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

@app.route('/register',methods=['GET','POST'])
def register():
    if 'user' in session:
        return redirect(url_for('home'))
    if request.method =='POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        check_user = chat_db.checkUser(username,password)
        if len(check_user) != 0:
            error = 'username bor'
            return  render_template('register.html',error=error)
        user = {
            'name':name,
            'username':username,
            'password':password,
            'user_bio':'Tizim foydalanuvchisi',
            'user_image':'images/default-person.png'
        }
        user['id'] = chat_db.createUser(user)
        print(user)
        print('register  succes !')
        session['user'] = user
        # users = chat_db.getAllUsers()
        return redirect(url_for('home'))
    return  render_template('register.html')

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