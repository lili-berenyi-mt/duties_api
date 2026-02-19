from flask import Flask, render_template, request, redirect, url_for, session
from repo.duty_repo import DutyRepo
from services.duty_service import DutyService
from services.results import AddDutyResult
import os

#type hints
#linting - ruff an mypy
#Add basic stuff to readme, like create venv
#pycharm - IDE python instead of vs code
#pip's garbage
#use interface for differrnt repos
#flask blueprints for endpoints

repo = DutyRepo()
service = DutyService(repo)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.service = service

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        number = request.form.get("number")
        number = int(number)
        description = request.form.get("description")

        result = service.add(number, description)
        if result == AddDutyResult.EMPTY_DESCRIPTION:
            session["error"]="Error: Description cannot be empty"
        elif result == AddDutyResult.DUPLICATE:
            session["error"]="Error: Duty already exists"
        else:
            session["error"]=None

        duties = service.get_all()
        return redirect(url_for('index'))

    duties = app.service.get_all()
    error_message = session.pop("error", None)
    return render_template('index.html', duties=duties, error_message=error_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
