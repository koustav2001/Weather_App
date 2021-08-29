import requests as requests
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities=City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    weather_data=[]
    for city in cities:
        #city = 'Las Vegas'
        r = requests.get(url.format(city.name)).json()
        #print(r)

        weather={
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    #print(weather)

    return render_template('weather.html',weather_data=weather_data)
