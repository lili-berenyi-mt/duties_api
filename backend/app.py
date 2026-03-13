from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from backend.models import db, Ksb, Duty, Theme, User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import os

limiter = Limiter(key_func=get_remote_address,
                   default_limits=["200 per day", "10 per minute"],
                   storage_uri="memory://")


mode = os.getenv("APP_SETTINGS", "default")

def create_app(config_name=mode):
      app = Flask(__name__)
      app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
      limiter.init_app(app)

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
      
      @app.get('/duties')
      def get_all_duties():
            duties = Duty.query.all()
            return jsonify([d.to_dict() for d in duties]), 200

      @app.post('/duties')
      def post_duty():
            data = request.json or {}
            if 'code' not in data or 'description' not in data:
                  return {"error": "Missing required fields. Request must contain code and description."}, 400
            ksb_ids = data.get('ksb_ids', [])
            if not isinstance(ksb_ids, list):
                  return {"error": "ksb_ids must be a list of strings"}, 400
            
            code = data["code"]
            description = data["description"]
            try:
                  new_duty = Duty(code=code, description=description)
                  db.session.add(new_duty)
                  if 'ksb_ids' in data:
                        for ksb_id in data['ksb_ids']:
                              ksb = Ksb.query.filter_by(id=ksb_id).first()
                              if ksb:
                                    new_duty.ksbs.append(ksb)
                              else:
                                    return {"error": f"KSB with ID '{ksb_id}' not found"}, 400
                  db.session.commit()
                  return jsonify(new_duty.to_dict()), 201
            except IntegrityError:
                  db.session.rollback()
                  return {"error": "A duty with this code already exists."}, 409
            except ValueError as e:
                  return {"error": str(e)}, 400
            
      @app.get('/duties/<string:code>')
      def get_duty_by_code(code):
            duty = Duty.query.filter_by(code=code).first_or_404(description=f"Duty with code {code} not found.")
            return jsonify(duty.to_dict()), 200
      
      @app.delete('/duties/<string:code>')
      def delete_duty_by_code(code):
            duty = Duty.query.filter_by(code=code).first_or_404(description=f"Duty with code {code} not found.")
            db.session.delete(duty)
            db.session.commit()     
            return "", 204

      @app.get('/themes')
      def get_all_themes():
            themes = Theme.query.all()
            return jsonify([t.to_dict() for t in themes]), 200
      
      @app.post('/themes')
      def post_theme():
            data = request.json
            if 'name' not in data or 'description' not in data:
                  return {"error": "Missing required fields. Request must contain name and description."}, 400
            duty_ids = data.get('duty_ids', [])
            if not isinstance(duty_ids, list):
                  return {"error": "duty_ids must be a list of strings"}, 400
            try:
                  new_theme = Theme(name=data["name"], description=data["description"])
                  db.session.add(new_theme)
                  if 'duty_ids' in data:
                        for duty_id in data['duty_ids']:
                              duty = Duty.query.filter_by(id=duty_id).first()
                              if duty:
                                    new_theme.duties.append(duty)
                              else:
                                    return {"error": f"Duty with ID '{duty_id}' not found"}, 400
                  db.session.commit()
                  return jsonify(new_theme.to_dict()), 201
            except IntegrityError:
                  db.session.rollback()
                  return {"error": "A theme with this name already exists."}, 400
            except ValueError as e:
                  return {"error": str(e)}, 400

      
      @app.get('/themes/<string:id>')
      def get_theme_by_id(id):
            theme = Theme.query.filter_by(id=id).first_or_404(description=f"Theme with id '{id}' not found.")
            return jsonify(theme.to_dict()), 200

      @app.delete('/themes/<string:id>')
      def delete_theme_by_id(id):
            theme = Theme.query.filter_by(id=id).first_or_404(description=f"theme with id '{id}' not found.")
            db.session.delete(theme)
            db.session.commit()     
            return "", 204
      
      @app.get('/duties/search/<string:code>')
      def get_themes_by_duty_code(code):
            duty = Duty.query.filter_by(code=code).first_or_404(description=f"Duty with code '{code}' not found.")
            themes_data = [
                  {
                        "id": t.id, 
                        "name": t.name, 
                        "completed": t.completed
                  } for t in duty.themes
            ]
            return jsonify({"duty": code, "description": duty.description, "themes": themes_data}), 200
      
      @app.route('/themes/<string:id>', methods=['PUT'])
      def update_theme(id):
            theme = Theme.query.filter_by(id=id).first_or_404(description=f"Theme with id '{id}' not found.")
            data = request.get_json()
            if 'completed' in data:
                  theme.completed = data['completed']

            db.session.commit()
            return jsonify({"id": theme.id, "name": theme.name, "completed": theme.completed}), 200
      
      @app.route('/verify-login', methods = ["POST"])
      def verify_login():
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                  return jsonify({
                        "id": user.id,
                        "role": user.role,
                        "username": user.username
                  }), 200
            return jsonify({"error": "Invalid username or password"}), 401

      with app.app_context():
            db.create_all()

      return app  

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

