from flask import Flask,session,render_template,request,url_for,redirect
from flask_socketio import SocketIO, send
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

    # habarlarni yuborish
    print(request.sid,message)
    send(message, broadcast=True)


@app.route('/')
def home():
    print('user' in session)
    return  render_template('home.html')

@app.route('/get-messages/<chat_id>')
def getMessages(user_id):
    chat_db.getPersonalChats(user=user_id)
    print('user' in session)
    return  render_template('home.html')

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
        check_user = chat_db.checkUser(username,password)
        if len(check_user)==1:
            print(check_user[0])
            if check_user[2]== username and check_user[3]==password:
                print('login succes')
                current_user = {
                    'name':check_user[0][1],
                    'username':username,
                    'password':password,
                    'id': check_user[0][0],
                    'created_at':check_user[0][4]
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
            'password':password
        }
        user['id'] = chat_db.createUser(user)
        print(user)
        print('register  succes !')
        session['user'] = user
        return redirect(url_for('home'))
    return  render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return  'logout'

@app.route('/message-page')
def messagePage():
    return render_template('message-test.html')

@app.route('/create-personal-chat',methods=['POST'])
def createChat():
    if request.method == 'POST' and 'user' in session:
        
        print()
        

if __name__=='__main__':
    # app.run(debug=False)
    socketio.run(app,host='localhost',debug=True)