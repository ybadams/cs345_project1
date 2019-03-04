import requests

def weather_data(query):
    res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
    return res.json();


def write_weather_data(result,zipcode):
    with open('weather_today.txt', 'w') as f:
        f.write("{}'s temperature: {}°C \n".format(zipcode,result['main']['temp']))
        f.write("Wind speed: {} m/s \n".format(result['wind']['speed']))
        f.write("Description: {} \n".format(result['weather'][0]['description']))
        f.write("Weather: {} \n".format(result['weather'][0]['main']))

    
def main():
    zipcode = 47374
    try:
        query='zip='+str(zipcode)+',us';
        w_data=weather_data(query);
        write_weather_data(w_data, zipcode)
        
    except:
        print('Zipcode not found...')

if __name__=='__main__':
    main()
  
