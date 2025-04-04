from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import cross_origin
from dotenv import load_dotenv
import os
from services.firebase_service import init_firebase

# Initialize Firebase
init_firebase()

from features.email_notification import ContractNotificationManager
from features.send_email_to_users import process_all_users_contracts
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Register Blueprints for authentication and dashboard routes
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/notifications123', methods=["GET"])
@cross_origin()  # Allow cross-origin requests
def notifications():
    try:
        process_all_users_contracts()
        obj = ContractNotificationManager()
        obj.send_scheduled_notifications()
        return jsonify({"message": "Notifications processed successfully", "status": "success"})
    except Exception as e:
        # Log the error as needed
        return jsonify({"message": f"Error processing notifications: {str(e)}", "status": "error"}), 500



if __name__ == '__main__':
    app.run(debug=True)
