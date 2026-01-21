from flask import Flask, jsonify, request
from models import db
import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"

db.init_app(app)

@app.route('/ksbs', methods = ["GET"])
def handle_ksbs():
        return "ksbs", 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)