from flask import Flask, jsonify, request
from models import db, Ksb
import config
import uuid

def create_app(config_name="default"):
      app = Flask(__name__)

      if config_name == "testing":
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            app.config['TESTING'] = True
      else:
            app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"

      db.init_app(app)

      @app.get('/ksbs')
      def get_all_ksbs():
            ksbs = Ksb.query.all()
            return jsonify([k.to_dict() for k in ksbs]), 200

      @app.post('/ksbs')
      def post_ksb():
            data = request.json
            code = data["code"]
            description = data["description"]
            new_ksb = Ksb(code=code, description=description)
            db.session.add(new_ksb)
            db.session.commit()
            return jsonify(new_ksb.to_dict()), 201
      
      @app.route('/ksbs/<string:id>', methods=["POST"])
      def get_ksb_by_id(id):
            ksb = Ksb.query.filter_by(id=id).first_or_404(description=f"Ksb with id {id} not found.")
            return jsonify(ksb.to_dict())

      
      return app  

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

