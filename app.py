from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from models import db, Ksb
import os

def create_app(config_name="default"):
      app = Flask(__name__)

      if config_name == "testing":
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            app.config['TESTING'] = True
      else:
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

      db.init_app(app)

      @app.get('/ksbs')
      def get_all_ksbs():
            ksbs = Ksb.query.all()
            return jsonify([k.to_dict() for k in ksbs]), 200

      @app.post('/ksbs')
      def post_ksb():
            data = request.json
            if 'code' not in data or 'description' not in data:
                  return {"error": "Missing required fields. Request must contain code and description."}, 400
            
            code = data["code"]
            description = data["description"]
            try:
                  new_ksb = Ksb(code=code, description=description)
                  db.session.add(new_ksb)
                  db.session.commit()
                  return jsonify(new_ksb.to_dict()), 201
            except IntegrityError:
                  db.session.rollback()
                  return {"error": "A KSB with this code already exists."}, 400
            except ValueError as e:
                  return {"error": str(e)}, 400
      
      @app.get('/ksbs/<string:id>')
      def get_ksb_by_id(id):
            ksb = Ksb.query.filter_by(id=id).first_or_404(description=f"Ksb with id {id} not found.")
            return jsonify(ksb.to_dict()), 200
      
      @app.delete('/ksbs/<string:id>')
      def delete_ksb_by_id(id):
            ksb = Ksb.query.filter_by(id=id).first_or_404(description=f"Ksb with id {id} not found.")
            db.session.delete(ksb)
            db.session.commit()     
            return "", 204
      
      @app.put('/ksbs/<string:id>')
      def put_ksb_by_id(id):
            data = request.json
            new_code = data["code"]
            new_description = data["description"]
            ksb = Ksb.query.filter_by(id=id).first_or_404(description=f"Ksb with id {id} not found.")
            ksb.update(new_code=new_code, new_description=new_description)
            db.session.commit()
            return jsonify(ksb.to_dict()), 200

      return app  

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

