'''Generate data about the countries of Europe'''

# All our imports
from os import path
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required
from flask_login import logout_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

# All data is stored in a global variable.
COUNTRY_LIST = [
    {'country':'Albania', 'population':2877797, 'capital':'Tirana',\
     'language':'Albanian','city-pop':557000,'elevation':'104m',\
     'country_var':'albania', 'city_var':'tirana'},
    {'country':'Andorra', 'population':77265, 'capital':'Andorra la Vella',\
     'language':'Catalan','city-pop':23000,'elevation':'1023m',\
     'country_var':'andorra', 'city_var':'andorra_la_vella'},
    {'country':'Austria', 'population':9006398, 'capital':'Vienna',\
     'language':'German','city-pop':1897500,'elevation':'170m',\
     'country_var':'austria', 'city_var':'vienna'},
    {'country':'Belarus', 'population':9449323, 'capital':'Minsk',\
     'language':'Belarusian','city-pop':2020000,'elevation':'198m',\
     'country_var':'belarus', 'city_var':'minsk'},
    {'country':'Belgium', 'population':11589623, 'capital':'Brussels',\
     'language':'Dutch','city-pop':1200000,'elevation':'76m',\
     'country_var':'belgium', 'city_var':'brussels'},
    {'country':'Bosnia and Herzegovina', 'population':3280819, 'capital':'Sarajevo',\
     'language':'Bosnian','city-pop':280000,'elevation':'518m',\
     'country_var':'bosnia_and_herzegovina', 'city_var':'sarajevo'},
    {'country':'Bulgaria', 'population':6948445, 'capital':'Sofia',\
     'language':'Bulgarian','city-pop':1241000,'elevation':'580m',\
     'country_var':'bulgaria', 'city_var':'sofia'},
    {'country':'Croatia', 'population':4105267, 'capital':'Zagreb',\
     'language':'Croatian','city-pop':820000,'elevation':'130m',\
     'country_var':'croatia', 'city_var':'zagreb'},
    {'country':'Czech Republic', 'population':10708981, 'capital':'Prague',\
     'language':'Czech','city-pop':1324000,'elevation':'244m',\
     'country_var':'czech_republic', 'city_var':'prague'},
    {'country':'Denmark', 'population':5792202, 'capital':'Copenhagen',\
     'language':'Danish','city-pop':632300,'elevation':'5m',\
     'country_var':'denmark', 'city_var':'copenhagen'},
    {'country':'Estonia', 'population':1326535, 'capital':'Tallinn',\
     'language':'Estonian','city-pop':437000,'elevation':'37m',\
     'country_var':'estonia', 'city_var':'tallinn'},
    {'country':'Finland', 'population':5540720, 'capital':'Helsinki',\
     'language':'Finnish','city-pop':653800,'elevation':'25m',\
     'country_var':'finland', 'city_var':'helsinki'},
    {'country':'France', 'population':65273511, 'capital':'Paris',\
     'language':'French','city-pop':2148000,'elevation':'34m',\
     'country_var':'france', 'city_var':'paris'},
    {'country':'Germany', 'population':83783942, 'capital':'Berlin',\
     'language':'German','city-pop':3770000,'elevation':'34m',\
     'country_var':'germany', 'city_var':'berlin'},
    {'country':'Greece', 'population':10423054, 'capital':'Athens',\
     'language':'Greek','city-pop':664000,'elevation':'153m',\
     'country_var':'greece', 'city_var':'athens'},
    {'country':'Holy See', 'population':801, 'capital':'Vatican City',\
     'language':'Latin and Italian','city-pop':453,'elevation':'41m',\
     'country_var':'holy_see', 'city_var':'vatican_city'},
    {'country':'Hungary', 'population':9660351, 'capital':'Budapest',\
     'language':'Hungarian','city-pop':1750000,'elevation':'102m',\
     'country_var':'hungary', 'city_var':'budapest'},
    {'country':'Iceland', 'population':341243, 'capital':'Reykjavik',\
     'language':'Icelandic','city-pop':131000,'elevation':'15m',\
     'country_var':'iceland', 'city_var':'reykjavik'},
    {'country':'Ireland', 'population':4937786, 'capital':'Dublin',\
     'language':'Irish Gaelic','city-pop':554000,'elevation':'8m',\
     'country_var':'ireland', 'city_var':'dublin'},
    {'country':'Italy', 'population':60461826, 'capital':'Rome',\
     'language':'Italian','city-pop':2860000,'elevation':'14m',\
     'country_var':'italy', 'city_var':'rome'},
    {'country':'Latvia', 'population':1886198, 'capital':'Riga',\
     'language':'Latvian','city-pop':632600,'elevation':'8m',\
     'country_var':'latvia', 'city_var':'riga'},
    {'country':'Liechtenstein', 'population':38128, 'capital':'Vaduz',\
     'language':'German','city-pop':5670,'elevation':'455m',\
     'country_var':'liechtenstein', 'city_var':'vaduz'},
    {'country':'Lithuania', 'population':2722289, 'capital':'Vilnius',\
     'language':'Lithuanian','city-pop':580000,'elevation':'124m',\
     'country_var':'lithuania', 'city_var':'vilnius'},
    {'country':'Luxembourg', 'population':625978, 'capital':'Luxembourg',\
     'language':'Luxembourgish','city-pop':122200,'elevation':'273m',\
     'country_var':'luxembourg', 'city_var':'luxembourg'},
    {'country':'Malta', 'population':441543, 'capital':'Valletta',\
     'language':'Maltese','city-pop':6000,'elevation':'54m',\
     'country_var':'malta', 'city_var':'valletta'},
    {'country':'Moldova', 'population':4033963, 'capital':'Chisinau',\
     'language':'Moldovan','city-pop':686000,'elevation':'80m',\
     'country_var':'moldova', 'city_var':'chisinau'},
    {'country':'Monaco', 'population':39242, 'capital':'Monaco',\
     'language':'French','city-pop':38300,'elevation':'0m',\
     'country_var':'monaco', 'city_var':'monaco'},
    {'country':'Montenegro', 'population':628066, 'capital':'Podgorica',\
     'language':'Serbo-Croatian','city-pop':199000,'elevation':'61m',\
     'country_var':'montenegro', 'city_var':'podgorica'},
    {'country':'Netherlands', 'population':17134872, 'capital':'Amsterdam',\
     'language':'Dutch','city-pop':872000,'elevation':'-2m',\
     'country_var':'netherlands', 'city_var':'amsterdam'},
    {'country':'North Macedonia', 'population':2083374, 'capital':'Skopje',\
     'language':'0','city-pop':560000,'elevation':'243m',\
     'country_var':'north_macedonia', 'city_var':'skopje'},
    {'country':'Norway', 'population':5421241, 'capital':'Oslo',\
     'language':'Norwegian','city-pop':693500,'elevation':'12m',\
     'country_var':'norway', 'city_var':'oslo'},
    {'country':'Poland', 'population':37846611, 'capital':'Warsaw',\
     'language':'Polish','city-pop':1783000,'elevation':'93m',\
     'country_var':'poland', 'city_var':'warsaw'},
    {'country':'Portugal', 'population':10196709, 'capital':'Lisbon',\
     'language':'Portuguese','city-pop':505500,'elevation':'15m',\
     'country_var':'portugal', 'city_var':'lisbon'},
    {'country':'Romania', 'population':19237691, 'capital':'Bucharest',\
     'language':'Romanian','city-pop':1820000,'elevation':'70m',\
     'country_var':'romania', 'city_var':'bucharest'},
    {'country':'San Marino', 'population':33931, 'capital':'San Marino',\
     'language':'Italian','city-pop':4000,'elevation':'328m',\
     'country_var':'san_marino', 'city_var':'san_marino'},
    {'country':'Serbia', 'population':8737371, 'capital':'Belgrade',\
     'language':'Serbian','city-pop':1200000,'elevation':'116m',\
     'country_var':'serbia', 'city_var':'belgrade'},
    {'country':'Slovakia', 'population':5459642, 'capital':'Bratislava',\
     'language':'Slovak','city-pop':437700,'elevation':'131m',\
     'country_var':'slovakia', 'city_var':'bratislava'},
    {'country':'Slovenia', 'population':2078938, 'capital':'Ljubljana',\
     'language':'Slovenian','city-pop':284300,'elevation':'281m',\
     'country_var':'slovenia', 'city_var':'ljubljana'},
    {'country':'Spain', 'population':46754778, 'capital':'Madrid',\
     'language':'Spanish','city-pop':3266000,'elevation':'667m',\
     'country_var':'spain', 'city_var':'madrid'},
    {'country':'Sweden', 'population':10099265, 'capital':'Stockholm',\
     'language':'Swedish','city-pop':975000,'elevation':'15m',\
     'country_var':'sweden', 'city_var':'stockholm'},
    {'country':'Switzerland', 'population':8654622, 'capital':'Bern',\
     'language':'German','city-pop':134000,'elevation':'542m',\
     'country_var':'switzerland', 'city_var':'bern'},
    {'country':'Ukraine', 'population':43733762, 'capital':'Kyiv',\
     'language':'Ukranian','city-pop':2952000,'elevation':'168m',\
     'country_var':'ukraine', 'city_var':'kyiv'},
    {'country':'United Kingdom', 'population':67886011, 'capital':'London',\
     'language':'English','city-pop':8900000,'elevation':'14m',\
     'country_var':'united_kingdom', 'city_var':'london'},
]

# Global variable for database
DB_NAME = "userlist.db"

# Call the app with the database configs
app = Flask(__name__)
app.config['SECRET_KEY'] = 'IMustNotFearFearIsTheMindKiller'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

# Call the db.
db = SQLAlchemy(app)

# Define the User class model to hold the logged in user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(50))
    full_name = db.Column(db.String(100))

    def __init__(self, email, password, full_name):
        self.email = email
        self.password = password
        self.full_name = full_name

# Hold all the login manager
login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

# User Loader for Login Manaager
@login_manager.user_loader
def load_user(id):
    '''User Loader '''
    return User.query.get(id)

# Ingest password and spit out results
def check_password(password_var):
    ''' Check Password function'''
    output_msg = ''
    good_pass = True
    special_char = '!@#$%^&*()?'

    # Statement to loop through all the pass checks.
    while True:
        if len(password_var) < 12:
            output_msg = output_msg + 'Password is too short. '
            good_pass = False
        if not any(char.isdigit() for char in password_var):
            output_msg = output_msg + 'Password must include a number. '
            good_pass = False
        if not any(char.isupper() for char in password_var):
            output_msg = output_msg + 'Password must include uppercase letter. '
            good_pass = False
        if not any(char.islower() for char in password_var):
            output_msg = output_msg + 'Password must include lowercase letter. '
            good_pass = False
        if not any(char in special_char for char in password_var):
            output_msg = output_msg + 'Password must include a special character. '
            good_pass = False
        break

    # Return values
    return output_msg, good_pass

# Create database function
def create_db(app):
    ''' Function that builds the database'''
    if not path.exists('/' + DB_NAME):
        db.create_all(app=app)

# Figured a function would be the best way to handle this
# Since I had to do it more than once.
def convert_num(population):
    '''A function to convert the population values to numbers'''

    # The best way to test for an integer is with a try block
    try:
        converted_pop = int(population)
        # If the conversion was successful, flags it for
        # True, meaning it will go the through f-string
        # to get comma seperators at the 1,000 marks.
        convert_check = True
    except ValueError:
        converted_pop = population
        convert_check = False

    # If successfully converted to integer, adds the commma
    # formatting to the variable and returns it.
    if convert_check:
        converted_pop = f'{converted_pop:,}'

    return converted_pop

# Route for the main page.
@app.route('/index.html', methods=['GET','POST'])
def home():
    '''Function for the homepage and the initial login'''

    # Gather password info
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # HASHED PASSWORD FUNCTION DIDN'T WORK
        # hashed_pass = sha256_crypt.hash(password)
        log_user = User.query.filter_by(email=email).first()

        # Check for existing user before logging in
        if log_user:
            if log_user.password == password:
                login_user(log_user, remember=True)
                return redirect(url_for('front'))
            else:
                flash('Incorrect Password')
        else:
            flash('User Not Found')

    # The date has to be added to each function so that it refreshes.
    date_time = (datetime.now()).strftime('%H:%M:%S %d/%m/%Y')

    # Returns simply the date and feeds the whole country list in the the main page.
    return render_template('index.html',date_time = date_time)

# Route for the homepage that is just a redirect.
@app.route('/')
def homepage():
    '''Just a redirect back the home function.'''

    # Takes the user back to the home function/home page.
    return redirect(url_for('home'))

# Sign up route
@app.route('/signup.html', methods=['GET','POST'])
def signup():
    '''Route for the sign up of the initial account'''

    #Gather info from the form
    credentials = request.form

    # Pull data out of the form
    if request.method == 'POST':
        cred_email = request.form.get('email')
        cred_name = request.form.get('realname')
        cred_pass1 = request.form.get('password1')
        cred_pass2 = request.form.get('password2')

        # Call the function to check the password
        pass_msg, pass_check = check_password(cred_pass1)

        # Do all the account setting checks.
        exist_user = User.query.filter_by(email=cred_email).first()
        if exist_user:
            flash('User already exists')
        elif len(cred_email) < 10:
            flash('Email must be at least 10 characters')
        elif len(cred_name) < 5 or len(cred_name) > 50:
            flash('Name must be between 5 and 50 characters.')
        elif cred_pass1 != cred_pass2:
            flash('Passwords do not match.')
        elif not pass_check:
            flash(pass_msg)
        else:
            # HASHED PASSWORD NOT WORKING
            # hashed_pass = sha256_crypt.hash(cred_pass1)
            new_user = User(email=cred_email, full_name=cred_name, password=cred_pass1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('front'))

    # The date has to be added to each function so that it refreshes.
    date_time = (datetime.now()).strftime('%H:%M:%S %d/%m/%Y')

    # Returns simply the date and feeds the whole country list in the the main page.
    return render_template('signup.html',date_time = date_time)

# Logout function
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    '''log out function'''
    logout_user()
    return redirect(url_for('home'))

# Front page function
@app.route('/front.html')
@login_required
def front():
    '''Function for the initial country landing page'''

    # The date has to be added to each function so that it refreshes.
    date_time = (datetime.now()).strftime('%H:%M:%S %d/%m/%Y')

    # Returns simply the date and feeds the whole country list in the the main page.
    return render_template('front.html',date_time = date_time, country_list = COUNTRY_LIST)

# Route for the country page.
@app.route('/country/<country_url>')
@login_required
def country_name(country_url):
    '''Gathers all the data to pass to the country page'''

    # The date has to be added to each function so that it refreshes.
    date_time = (datetime.now()).strftime('%H:%M:%S %d/%m/%Y')

    # For loop to gather the relevant data from the dictionary to pass to the
    # country page. Gets the name of the country to query from the URL entered.
    for c_list in COUNTRY_LIST:
        if c_list['country_var'] == country_url:
            coun_val = c_list['country']
            pop_val = convert_num(c_list['population'])
            cap_val = c_list['capital']
            coun_var = c_list['country_var']
            city_var = c_list['city_var']

    # Returns the loop results into the country page.
    return render_template('country.html', country_name = coun_val, \
                           population = pop_val, capital = cap_val, \
                           country_tech_name = coun_var, \
                           city_tech_name = city_var, date_time = date_time)

# Route for the capital city page.
@app.route('/city/<city_url>')
@login_required
def city_name(city_url):
    '''Gathers all the data to pass to the city page'''

    # The date has to be added to each function so that it refreshes.
    date_time = (datetime.now()).strftime('%H:%M:%S %d/%m/%Y')

    # For loop to gather the relevant data from the dictionary to pass to the
    # country page. Gets the name of the country to query from the URL entered.
    for c_list in COUNTRY_LIST:
        if c_list['city_var'] == city_url:
            coun_val = c_list['country']
            cap_val = c_list['capital']
            coun_var = c_list['country_var']
            city_var = c_list['city_var']
            main_lang = c_list['language']
            city_pop = convert_num(c_list['city-pop'])
            city_elev = c_list['elevation']

    # Returns the loop results into the country page.
    return render_template('city.html', country_name = coun_val, \
                           capital = cap_val, language = main_lang, \
                           population = city_pop, elevation = city_elev, \
                           country_tech_name = coun_var, \
                           city_tech_name = city_var, date_time = date_time)

# Runs the application!
if __name__ == '__main__':
    create_db(app)
    app.run()
