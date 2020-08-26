import requests

def get_place_by_text(text) -> dict:
    google_map_responds = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={text}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyA3fN27gbdKTelvniFWyrpMpEH6nka1sIg")
    places = google_map_responds.json()
    return places