from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    

username = 'mad1@gmail.com'
password = 'mad123'

@app.route('/health')
def hello():
    return 'Server is running fine.'

@app.route('/')
def index():
    return render_template('hello.html')

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
            return 'You are logged in successfully'
        else:
            return 'Login failed. Please check your email and password.'
        
        return "Form Submitted Successfully"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Registering user with Email: {email} and Password: {password}")
        new_user = User(email=email, password=password)
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