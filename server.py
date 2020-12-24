from flask import Flask, request, send_from_directory
import main
import requests, json
import os, sys
import datetime
from time import gmtime, strftime

cur_time = strftime("%H:%M")

now = datetime.datetime.now()
day = now.strftime("%A")[:3].upper()
date = now.strftime("%B %d").upper()



app = Flask('server')

def get_city_id(s_city_name):
	try:
		res = requests.get("http://api.openweathermap.org/data/2.5/find",
					 params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
		data = res.json()
		cities = ["{} ({})".format(d['name'], d['sys']['country'])
				  for d in data['list']]
		print("city:", cities)
		city_id = data['list'][0]['id']
		print('city_id=', city_id)
	except Exception as e:
		print("Exception (find):", e)
		pass
	assert isinstance(city_id, int)
	return city_id

@app.route('/index.html')
def index():
	appid = '9a0e4ffe23b84856975e1e4a72d739bb'
	city_id = 1508291
	res_now = requests.get(f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&lang=ru&appid={appid}")
	#
	data_now = res_now.json()
	arr_now = [
	data_now['weather'][0]['description'], 
	data_now['main']['temp'],
	data_now['weather'][0]['icon']
	   ]
	F_CONST = 9/5
	fahr = int(arr_now[1])*F_CONST+32





	res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})	
	data = res.json()

	
	#print('Город:', data['city']['name'], data['city']['country'])
	arr = []
	res = 0
	for i in data["list"]:
		res += 1
		if res == 8:
			arr.append(
			[i['dt_txt'][:16], 
			i['main']['temp'],
			i['weather'][0]['description'],
			i['weather'][0]['icon']])
			res = 0
		#print(arr_now)
		# print("Состояние:", data['weather'][0]['description'])
		# print("Температура сейчас:", data['main']['temp'])
		# print("Минимальная температура:", data['main']['temp_min'])
		# print("Максимальная температура:", data['main']['temp_max'])
		# print("data:", data)
	# TOKEN = 'b23c002d4c85f6a9829d3b7ae142d6f2'
	# lat = '55.24363508145407'
	# lon = '61.380813446477845'
	# cnt = 1 # by default
	# link = f'https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={TOKEN}'
	# response = requests.get(link)
	# token = '0f518a13b76643c315b33323ffffc8c4'
	

	return '''
<!DOCTYPE html>
<html lang="ru" style="width:600px; height:1530px;">
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400&display=swap" rel="stylesheet">
<style>
html{
	font-family: 'Montserrat', sans-serif;
	margin: 0px;
	color:#FEFFFF;
	background: linear-gradient(45deg, #5D6B74, #B3C2CE);
}

body{
	
}

.tiles{
	margin-top: 10px;
	width: 50%;
	height: 100%;
	margin:auto;
}

.tile_lower{
	display: inline-block;
	width: 192px;
	height: 200px;
	margin:auto;
	border: 3px solid #9EACB5;
}

.lower{
	margin:auto;

}

.tile-1{
	display: block;
	width: 80%;
	height: 300px;
	background-color: #415860;
	text-align: center;
	margin: auto;
}

#date{
	font-size:32px;

}

#time{
	padding-right: 300px;
	font-size: 30px;
}

#p_1{
	padding-top: 100px;
	padding-right: 300px;
	font-size: 30px;
}

#icon{
	position: relative;
	bottom: 130px;
	left: 30px;

}

.tile_2{
	margin-left:75px;
	
{

.img_2{
	
    position: relative;
    left: 80px;
    bottom: 70px;


}
.tile_3{
	position:absolute;
}

.tile_4{
	position: relative;
    left: 202px;
}

</style>
<head>
	<title>Проектная работа</title>
	<meta charset="utf-8">
</head>
<body>
	<div class="header">
		
	</div>
	<div class="main">
		<div class="tiles">
			<div class="tile tile-1">
				<p id="date">'''+day+","+date+'''</p>
				<p id="p_1">'''+str(arr_now[1])+'''°C/'''+str(round(fahr))+'''°F</p>
				<p id="time">'''+str(cur_time)+'''</p>
				<img id="icon" src="'''"http://openweathermap.org/img/wn/"+arr_now[2]+"@2x.png"'''">
			</div>
			<div class="lower">
				<div class="tile tile_2 tile_lower">
					<p id="day_2">'''+str((datetime.date.today() + datetime.timedelta(days=1)).strftime('%A')[:3].upper())+'''</p>
					<p id="temp_2">'''+str(round(arr[0][1]))+'''°C</p>
					<img style="width:50px;height:50px;position:relative;left: 80px;bottom: 70px;" class="img_2"  src="'''"http://openweathermap.org/img/wn/"+arr[0][3]+".png"'''">
				</div>
				<div class="tile_3 tile tile_lower" style="position:absolute;">
					<p id="day_3">'''+str((datetime.date.today() + datetime.timedelta(days=2)).strftime('%A')[:3].upper())+'''</p>
					<p id="temp_3">'''+str(round(arr[1][1]))+'''°C</p>
					<img style="width:50px;height:50px; position:relative;left: 80px;bottom: 70px;" class="img_3"  src="'''"http://openweathermap.org/img/wn/"+arr[1][3]+".png"'''">
				</div>
				<div class="tile tile_4 tile_lower" style="position: relative; left: 203px;">
					<p id="day_4">'''+str((datetime.date.today() + datetime.timedelta(days=3)).strftime('%A')[:3].upper())+'''</p>
					<p id="temp_4">'''+str(round(arr[2][1]))+'''°C</p>
					<img style="width:50px;height:50px; position:relative;left: 80px;bottom: 70px; " class="img_4"  src="'''"http://openweathermap.org/img/wn/"+arr[2][3]+".png"'''">
				</div>
			</div>
		</div>
	</div>
	<div class="footer">
		<p>
	</div>
</body>
</html>

'''

# print(day)
# print(now)
#print(data)
app.run(port=3000, host='0.0.0.0')


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')


#position:relative;left: 80px;bottom: 70px;