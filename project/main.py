from flask import Flask
from routes.member_routes import member_routes
from routes.portfolio_routes import portfolio_routes

app = Flask(__name__)
app.register_blueprint(member_routes)
app.register_blueprint(portfolio_routes)

@app.route('/')
def home():
    return {"message": "Welcome to the File Access System"}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
