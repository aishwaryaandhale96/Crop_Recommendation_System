from flask import Flask, render_template, request, jsonify
import requests
import joblib
import os

app = Flask(__name__)

class Website():
    def __init__(self):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home2', self.home2)
        self.app.add_url_rule('/get_location', 'get_location', self.get_weather, methods=['POST'])
        self.app.add_url_rule('/home2', 'home2', self.home2)
        self.app.add_url_rule('/final2', 'final2', self.final2)
        self.app.add_url_rule('/about2', 'about', self.about)
        self.app.add_url_rule('/run_function', 'run_function', self.run_function, methods=['POST'])
        self.app.add_url_rule('/soil_prediction2', 'soil_prediction', self.soil_prediction)
        self.app.add_url_rule('/submit_form', 'submit_form', self.submit_form, methods=['POST'])

    def home2(self):
        return render_template('home2.html')

    def about(self):
        return render_template('about2.html')

    def run_function(self):
        print("Function executed successfully")
        return 'Function executed'

    def soil_prediction(self):
        return render_template('soil_prediction2.html')

    def submit_form(self):
        self.soil_type = request.form['soilColor']
        self.nitrogen = float(request.form['nitrogen'])
        self.phosphorus = float(request.form['phosphorus'])
        self.potassium = float(request.form['potassium'])
        self.water = int(request.form['water'])
        self.temperature = float(request.form['temperature'])
        self.crop_arr = [[self.soil_type,self.nitrogen,self.phosphorus,self.potassium,self.temperature,self.water]]
        crop_output ,fertilizer_output = self.final2()
        return render_template('final2.html', crop_output=crop_output, fertilizer_output=fertilizer_output)

    def final2(self):
        current_directory = os.getcwd()
        print(current_directory)
        crop = joblib.load(current_directory+'/crop.pkl')
        grip = int(crop.predict(self.crop_arr))
        crop_output = self.crop_perticular(grip)

        self.crop_arr2=[[self.soil_type,self.nitrogen,self.phosphorus,self.potassium,self.temperature,self.water,grip]]
        fertilizer = joblib.load(current_directory+'/fertilizer2311.pkl')
        find = fertilizer.predict(self.crop_arr2)
        fertilizer_output = self.fer_perticular(find)
        return crop_output ,fertilizer_output

    def crop_perticular(self,crop):
        if crop == 0:
            crop_find = 'Cotton'
        elif crop == 1:
            crop_find = 'Ginger'
        elif crop == 2:
            crop_find = 'Gram'
        elif crop == 3:
            crop_find = 'Grapes'
        elif crop == 4:
            crop_find = 'Groundnut'
        elif crop == 5:
            crop_find = 'Jowar'
        elif crop == 6:
            crop_find = 'Maize'
        elif crop ==7 :
            crop_find = 'Masoor'
        elif crop == 8:
            crop_find = 'Moong'
        elif crop == 9:
            crop_find = 'Rice'
        elif crop == 10:
            crop_find = 'Sugarcane'
        elif crop == 11:
            crop_find = 'Tur'
        elif crop == 12:
            crop_find= 'Turmeric'
        elif crop == 13:
            crop_find = 'Rice'
        else:
            crop_find = 'Sugarcane'

        return crop_find

    def fer_perticular(self,fer):
        if fer==0:
            fer_na= "10:10:10 NPK"
        elif fer==1:
            fer_na="10:26:26 NPK"
        elif fer==2:
            fer_na='12:32:16 NPK'
        elif fer==3:
            fer_na='13:32:26 NPK'
        elif fer==4:
            fer_na='19:19:19 NPK'
        elif fer==5:
            fer_na='50:26:26 NPK'
        elif fer==6:
            fer_na='Ammonium Sulphate'
        elif fer==7:
            fer_na='Chilated Micronutrient'
        elif fer==8:
            fer_na='DAP'
        elif fer==9:
            fer_na='Ferrous Sulphate'
        elif fer==10:
            fer_na='MOP'
        elif fer==11:
            fer_na='Magnesium Sulphate'
        elif fer==12:
            fer_na='SSP'
        else:
            fer_na='Urea'

        return fer_na

    def get_weather(self):
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        print(latitude)
        api_key = "1e92e74cf6380f493c062773f324d611"
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            self.temperature = round(temperature - 273,1)
            print("help")
            return jsonify({'temperature': self.temperature})
        else:
            return jsonify({'error': 'Failed to retrieve weather data'})

if __name__ == '__main__':
    website = Website()
    website.app.run(host='0.0.0.0', port=8000,debug=True)
