from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import City, Searchhistory, Favouritecity, Forecastday
import requests
from datetime import datetime
table_bp = Blueprint("table",__name__,url_prefix="/table")
API_KEY = "6b35acecf0f18c39200a27b46d68b971"
BASE_URL = "https://api.openweathermap.org/data/2.5"
def get_weather_icon(condition :str):
    mapping = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Thunderstorm": "⛈️",
        "Drizzle": "🌦️",
        "Mist": "🌫️"
    }
    return mapping.get(condition.capitalize(),"🌍")
def get_current_weather(city:str):
    response = requests.get(f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric")
    data = response.json()
    if data.get("cod")!= 200:
        return None
    return {
        "city":data["name"],
        "date":datetime.utcnow().strftime("%d %b %Y"),
        "condition":data["weather"][0]["main"],
        "temp":data["main"]["temp"],
        "feel_like":data["main"]["feels_like"],
        "icon": get_weather_icon(data["weather"][0]["main"]),
    }
def get_forecast(city :str):
    response = requests.get(f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric")
    data = response.json()
    if data.get("cod") != "200":
        return []
    forecast_list = []
    for i in range(0, len(data["list"]), 8): 
        item = data["list"][i]
        forecast_list.append({
            "day": datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%a"),
            "date": datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%d %b"),
            "condition": item["weather"][0]["main"],
            "temp_min": item["main"]["temp_min"],
            "temp_max": item["main"]["temp_max"],
            "icon": get_weather_icon(item["weather"][0]["main"]),
        })
    return forecast_list
def get_user_searchhistory(user_id: int): 
    return Searchhistory.query.filter_by(user_id=user_id).order_by(Searchhistory.searched_at.desc()).all()
def get_user_favorites(user_id: int):
    return Favouritecity.query.filter_by(user_id=user_id).all()
def save_search(user_id: int, city: str, temp: float):
    new_search = Searchhistory(
        user_id=user_id,
        city_name=city,
        searched_at=datetime.utcnow(),
        summary_temp=temp
    )
    db.session.add(new_search)
    db.session.commit()
    
@table_bp.route("/search",methods = ["POST"])
@login_required
def search_city():
    city = request.form.get("search_city")
    if not city:
        flash("please enter the name of city","warning")
        return redirect(url_for("table.dashboard"))
    current_weather = get_current_weather(city)
    forecast = get_forecast(city)
    if current_weather:
        save_search(current_user.id,city,current_weather["temp"])
    else:
        flash("city not found. Try again","danger")
    history = get_user_searchhistory(current_user.id)
    favorites = get_user_favorites(current_user.id)
    return render_template(
        "dashboard.html",
        current_weather=current_weather,
        forecast=forecast,
        history=history,
        favorites=favorites,
    )
@table_bp.route("/add_favorite/<city>")
@login_required
def add_favorite(city):
    exists = Favouritecity.query.filter_by(user_id=current_user.id, city_name=city).first()
    if not exists:
        fav = Favouritecity(user_id=current_user.id, city_name=city)
        db.session.add(fav)
        db.session.commit()
        flash(f"{city} added to favorites.", "success")
    else:
        flash(f"{city} is already in favorites.", "info")
    return redirect(url_for("table.dashboard"))
@table_bp.route("/remove_favorite/<city>")
@login_required
def remove_favorite(city):
    fav = Favouritecity.query.filter_by(user_id=current_user.id, city_name=city).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        flash(f"{city} removed from favorites.", "info")
    return redirect(url_for("table.dashboard"))
@table_bp.route("/dashboard")
@login_required
def dashboard():
    """Show dashboard with weather, forecast, history, favorites"""
    history = get_user_searchhistory(current_user.id)
    favorites = get_user_favorites(current_user.id)

    current_weather = None
    forecast = None

    if history:
        last_city = history[0].city_name
        current_weather = get_current_weather(last_city)
        forecast = get_forecast(last_city)

    return render_template(
        "dashboard.html",
        current_weather=current_weather,
        forecast=forecast,
        history=history,
        favorites=favorites,
    )



    