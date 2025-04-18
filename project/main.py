# from flask import Flask, render_template, redirect, url_for, session
# from routes.auth_routes import auth_routes
# from routes.file_routes import file_routes

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Replace with a secure key
# app.register_blueprint(auth_routes)  # Ensure this is registered
# app.register_blueprint(file_routes)

# @app.route('/')
# def home():
#     if 'user_id' in session:
#         return redirect(url_for('files.list_files'))
#     return redirect(url_for('auth.login'))

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')


from flask import Flask, render_template, redirect, url_for, session
from routes.auth_routes import auth_routes
from routes.file_routes import file_routes
from routes.upload_routes import upload_routes
from routes.portfolio_routes import portfolio_routes
from routes.dashboard_routes import dashboard_routes
from routes.member_routes import member_routes
from routes.folder_routes import folder_routes
from routes.share_routes import share_routes




from db import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.register_blueprint(auth_routes)
app.register_blueprint(upload_routes)
app.register_blueprint(file_routes)
app.register_blueprint(portfolio_routes)
app.register_blueprint(dashboard_routes)
app.register_blueprint(member_routes)
app.register_blueprint(folder_routes)
app.register_blueprint(share_routes)

@app.before_request
def create_hardcoded_admin():
    conn = get_connection()
    cursor = conn.cursor()
    # cursor.execute("INSERT INTO members (UserName, emailID) VALUES (%s, %s)", ('Admin123', 'admin@safedocs.com'))
    member_id = cursor.lastrowid
    # cursor.execute("INSERT INTO Login (MemberID, Password, Role) VALUES (%s, %s, %s)", (member_id, '1234', 'admin'))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('files.list_files'))
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')