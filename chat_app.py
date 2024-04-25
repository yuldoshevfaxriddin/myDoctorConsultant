from flask import Flask,session,render_template,request,url_for,redirect
from flask_socketio import SocketIO, send, emit
import datetime
import json
import chat_db

app = Flask(__name__)
app.secret_key='Faxriddin Yuldoshev'
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
    # data['user_1'] = chat_db.getUser(user_id_1)[0]
    # data['user_2'] = chat_db.getUser(user_id_2)[0]
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

@app.route('/open-chat')
def openChat():
    return  "open chat"

@app.route('/doctors')
def doctors():
    return  render_template('doctors.html')

@app.route('/doctor/<doctor>')
def doctorProfile(doctor):
    print(doctor)
    return  render_template('doctor/profile.html')


@app.route('/get-messages')
def getMessages():
    user_1 = request.args.get('user_1')
    user_2 = request.args.get('user_2')
    print(user_1,request.form)
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
        user = {
            'username':'admin',
            'password':'password'
        }
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
                    'created_at':check_user[4]
                }
                session['user'] = current_user
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
    return  'logout'

@app.route('/message-page')
def messagePage():
    users = chat_db.getAllUsers()
    user = session['user']
    return render_template('message-test.html',users=users,current_user=user)

@app.route('/create-personal-chat',methods=['POST'])
def createChat():
    if request.method == 'POST' and 'user' in session:
        
        print()
        

if __name__=='__main__':
    # app.run(debug=False)
    socketio.run(app,host='localhost',debug=True)