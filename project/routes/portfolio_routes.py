from flask import Blueprint, jsonify
from db import get_connection

portfolio_routes = Blueprint('portfolio', __name__)

@portfolio_routes.route('/portfolio', methods=['GET'])
def get_portfolio():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.name, m.email, d.filename, d.upload_date
        FROM members m
        JOIN documents d ON m.id = d.uploaded_by
    """)
    portfolio = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(portfolio)