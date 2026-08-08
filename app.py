from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock Data
STATE = {
    "districts_affected": 12,
    "people_affected": 284500,
    "relief_camps": 186,
    "evacuated": 42100
}

DISTRICTS = [
    {
        "id": 1,
        "name": "Dibrugarh",
        "risk_level": "High",
        "people_affected": 45000,
        "relief_camps": 23,
        "trend": "Rising"
    },
    {
        "id": 2,
        "name": "Barpeta",
        "risk_level": "Severe",
        "people_affected": 82000,
        "relief_camps": 45,
        "trend": "Stable"
    },
    {
        "id": 3,
        "name": "Dhubri",
        "risk_level": "Moderate",
        "people_affected": 15000,
        "relief_camps": 8,
        "trend": "Falling"
    },
    {
        "id": 4,
        "name": "Majuli",
        "risk_level": "Severe",
        "people_affected": 32000,
        "relief_camps": 12,
        "trend": "Rising"
    }
]

UPDATES = [
    {"time": "17:40", "message": "Relief supplies dispatched to Majuli district."},
    {"time": "16:55", "message": "River levels monitored at Dibrugarh; water level rising."},
    {"time": "15:30", "message": "Shelter capacity updated in Barpeta."}
]

RELIEF_DATA = {
    "camps": 186,
    "capacity": 50000,
    "evacuated": 42100,
    "supplies_dispatched": 120,
    "food_packets": 150000,
    "water_bottles": 300000
}


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home_page():
    return render_template("home.html", state=STATE)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'admin@assamflood.local' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard_page'))
        else:
            error = "Invalid credentials."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home_page'))

@app.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html", state=STATE, districts=DISTRICTS, relief=RELIEF_DATA)

@app.route("/districts")
def districts_page():
    return render_template("districts.html", districts=DISTRICTS)

@app.route("/relief")
def relief_page():
    return render_template("relief.html", relief=RELIEF_DATA)

@app.route("/updates")
def updates_page():
    return render_template("updates.html", updates=UPDATES)

@app.route("/donate", methods=['GET', 'POST'])
def donate_page():
    if request.method == 'POST':
        amount = request.form.get('amount')
        name = request.form.get('name')
        # In a real app, process payment here.
        return render_template("donate.html", success=True, amount=amount, name=name)
    return render_template("donate.html", success=False)

@app.route("/about")
def about_page():
    return render_template("about.html")

# APIs
@app.route("/api/summary")
def api_summary():
    return jsonify(STATE)

@app.route("/api/districts")
def api_districts():
    q = request.args.get('q', '').lower()
    if q:
        filtered = [d for d in DISTRICTS if q in d['name'].lower()]
        return jsonify(filtered)
    return jsonify(DISTRICTS)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
