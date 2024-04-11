from flask import Flask,session,render_template,request,url_for,redirect

app = Flask(__name__)
app.secret_key='Faxriddin Yuldoshev'

@app.route('/')
def home():
    print('user' in session)
    return  render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        user = {
            'username':'admin',
            'password':'password'
        }
        # if user['username']== username and user['password']==password:
        if user['username']!= username and user['password']!=password:
            print('login succes')
            current_user = {
                'username':username,
                'password':password
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
        user = {
            'name':name,
            'username':username,
            'password':password
        }
        print('register  succes !')
        session['user'] = user
        return redirect(url_for('home'))
    return  render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return  'logout'

if __name__=='__main__':
    app.run(debug=False)