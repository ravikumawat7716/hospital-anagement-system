from flask import Flask, render_template, request, redirect
from models import db, User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user





app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

    

username = 'mad1@gmail.com'
password = 'mad123'

@app.route('/health')
def hello():
    return 'Server is running fine.'

@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/vipaccess')
@login_required
def vipacess():
    return 'This is a VIP Acess Page'

@app.route('/dashboard')
def dashboard():
    logged_in_user = current_user
    print("========================")
    print(logged_in_user)
    print("========================")
    if logged_in_user.is_anonymous == False:
        print(logged_in_user.email)
        return render_template('userdashboard.html', email=logged_in_user.email)
    else:
        return redirect('/login')


@app.route('/admindashboard')
@login_required
def admindashboard():
    who = current_user
    if who.role == 'admin':
        return render_template('admindashboard.html')
    if who.role == 'user':
        return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("We received a post request")
        print("===========================")
        print("Email : ", request.form.get('email'))
        print("Password : ", request.form.get('password'))
        print("===========================")
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            if user.role == 'user':
                login_user(user)
                print("We need to do something here.")
                return redirect('/dashboard')
            if user.role == 'doctor':
                return 'You are logged in as a doctor'
            if user.role == 'admin':
                return redirect('/admindashboard')
        else:
            return 'Login failed. Please check your email and password.'
        
        return "Form Submitted Successfully"
    logged_in_user = current_user
    if logged_in_user.is_anonymous == False:
        if logged_in_user.role == 'admin':
            return redirect('/admindashboard')
        if logged_in_user.role == 'user':
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        print(f"Registering user with Email: {email} and Password: {password} and Role: {role}")
        new_user = User(email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        print("User registered successfully!")
        return 'User registered successfully!'
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
        # lets add some users
        # user1 = User(email=username, password=password)
        # db.session.add(user1)
        # db.session.commit()
        print("Users added successfully!")

    app.run(debug=True)