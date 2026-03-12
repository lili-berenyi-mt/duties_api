from flask import Flask, render_template, request, redirect, url_for, session
from frontend.repo.duty_repo import DutyRepo
from frontend.services.duty_service import DutyService
from frontend.services.results import AddDutyResult
from frontend.services.theme_service import ThemeService
from frontend.repo.theme_repo import ThemeRepo
import os
import requests

duty_repo = DutyRepo()
duty_service = DutyService(duty_repo)
theme_repo = ThemeRepo()
theme_service = ThemeService(theme_repo)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret')
app.service = duty_service

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        number = request.form.get("number")
        number = int(number)
        description = request.form.get("description")

        result = duty_service.add(number, description)
        if result == AddDutyResult.EMPTY_DESCRIPTION:
            session["error"]="Error: Description cannot be empty"
        elif result == AddDutyResult.DUPLICATE:
            session["error"]="Error: Duty already exists"
        elif result == AddDutyResult.INVALID_INPUT:
            session["error"]="Error: Number must be a number"
        else:
            session["error"]=None

        duties = duty_service.get_all()
        return redirect(url_for('index'))

    duties = app.service.get_all()
    error_message = session.pop("error", None)
    return render_template('index.html', duties=duties, error_message=error_message)

@app.route("/duty/<code>")
def duty_detail(code):
    duty = duty_service.get_by_code(code)
    if not duty:
        return "Duty not found", 404
        
    return render_template("duty_detail.html", duty=duty)

@app.route("/theme/toggle/<string:theme_id>", methods=["POST"])
def toggle_theme(theme_id):
    current_status_str = request.form.get("current_status")
    current_status = current_status_str == 'True'
    
    duty_code = request.form.get("duty_code")
    
    theme_service.toggle_completion(theme_id, current_status)

    return redirect(url_for('duty_detail', code=duty_code))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        session["login-error"] = None

        try:
            resp = requests.post("http://backend:5000/verify-login", 
                                 json={"username": username, "password": password},
                                 timeout=5)

            if resp.status_code == 200:
                user_data = resp.json()
                session.clear()
                session['id'] = user_data['id']
                session['role'] = user_data['role']
                session['username'] = user_data['username']
                
                return redirect(url_for('index'))
            else:
                session["login-error"] = "Error: Invalid username or password"
                
        except requests.exceptions.ConnectionError:
            session["login-error"] = "Backend service is currently unavailable."

    error_message = session.pop("login-error", None)
    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
