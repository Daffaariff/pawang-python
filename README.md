# 🧠 PawangPython — Interactive Quiz Web App

Welcome to **PawangPython**, an engaging, youth-oriented web app designed to help users test and improve their Python knowledge — with weather-based theming and gamified quizzes! Built using Flask, this app combines user authentication, weather API integration, and a clean modern UI.

---

## 🚀 Features

- 🔐 **User Registration & Login**
- 📍 **City-aware Weather Forecast Integration**
- 📝 **Multiple Python Quiz Topics**
- 🧑‍🎓 **Leaderboard for Top Coders**
- 🎨 **Cool, responsive UI design for youth**
- 🧠 **Encourages learning through interaction**

---

## 🧰 Tech Stack

| Layer       | Technology        |
|-------------|-------------------|
| Backend     | Python (Flask)    |
| Database    | SQLite (default)  |
| Frontend    | HTML, CSS, Jinja2 |
| API         | WeatherAPI (OpenWeatherMap, etc.) |
| Auth        | Flask sessions    |

---

## 📸 Screenshots

| Login UI                        | Home Page w/ Weather                  |
|----------------------------------|----------------------------------------|
| ![Login](screenshots/login.png) | ![Home](screenshots/home-weather.png) |

> Screenshots are located in the `/screenshots` folder.

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/PawangPython-quiz.git
cd PawangPython-quiz

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# edit .env with your SECRET_KEY and WEATHER_API_KEY

# 5. Run the app
python app.py
