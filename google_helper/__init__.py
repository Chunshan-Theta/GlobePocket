import datetime

import requests
from bs4 import BeautifulSoup

def get_place_by_text(text) -> dict:
    google_map_responds = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={text}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry,type&key=AIzaSyA3fN27gbdKTelvniFWyrpMpEH6nka1sIg")
    places = google_map_responds.json()
    return places

def get_weather(Latitude, Longitude):
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={Latitude}&lon={Longitude}&appid=a8f1a35148b9d49f4bd8d2fa2a9d5764").json()

    return {
        "forecast": {(datetime.datetime.today()+datetime.timedelta(days=idx)).strftime("%m/%d"): val for idx,val in enumerate(weather['daily'])}
    }

def get_weather_dep(Latitude, Longitude):
    content = requests.get(
        f"https://weather.com/weather/tenday/l/{Latitude},{Longitude}?par=google")
    htmlsoup = BeautifulSoup(content.text, 'html.parser')
    print(content.text)
    # area
    class_name = "_-_-components-src-molecule-DaypartDetails-DaypartDetails--Content--2Yg3_ _-_-components-src-molecule-DaypartDetails-DaypartDetails--contentGrid--2_szQ"

    area = htmlsoup.findAll("h1", {"class": class_name})
    #area = title_area[0].findAll('span')[0].text[1:]

    area = None

    #
    class_name = "_-_-components-src-molecule-DaypartDetails-DaypartDetails--Content--2Yg3_ _-_-components-src-molecule-DaypartDetails-DaypartDetails--contentGrid--2_szQ"
    days_forecast_10 = {}
    a_tags = htmlsoup.findAll("div", {"class": class_name})
    for tag in a_tags:
        # print("\n"*3)
        for b in tag.findAll("h3"):
            combine_dict = {}
            # print("\n"*1)
            datetime = b.text.split(" | ")
            # print(datetime)

            #{'TemperatureValue': '22°', 'PercentageValue': '30%', 'Wind': 'WNW 4 km/h'}
            span_dict = {}
            for s in b.parent.findAll("span"):
                if s.get("data-testid") is not None:
                    span_dict.update({s.get("data-testid"): s.text})
            #print(span_dict)
            combine_dict.update(span_dict)

            # {'content': 'Cloudy early with partial clearing expected late. Low 22C. Winds light and variable.'}
            p_dict = {"content": b.parent.find("p").text}
            #print(p_dict)
            combine_dict.update(p_dict)

            # {'PercentageValue': '96%', 'UVIndexValue': '0 of 10', 'MoonriseTime': '10:30 pm', 'MoonsetTime': '11:19 am'}
            li_dict = {}
            uls = b.parent.parent.findAll("ul")
            if datetime[1] == "Day":
                ul = uls[0]
            elif datetime[1] == "Night":
                ul = uls[-1]
            else:
                continue
            for li in ul.findAll("li"):
                element = li.find("span", {
                    "class": "_-_-components-src-molecule-DaypartDetails-DetailsTable-DetailsTable--value--2YD0-"})
                li_dict.update({element.get("data-testid"): element.text})
            #print(li_dict)
            combine_dict.update(li_dict)

            if datetime[0] not in days_forecast_10:
                days_forecast_10[datetime[0]] = {}
            days_forecast_10[datetime[0]][datetime[1]] = combine_dict

    return {
        "forecast": days_forecast_10,
        "area": area
    }
"""
import json
print(json.dumps(get_weather("23.5", "121.3")))
"""
