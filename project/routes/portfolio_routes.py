from flask import Blueprint, request, jsonify
from models.portfolio import get_member_portfolio, update_portfolio

portfolio_routes = Blueprint('portfolio', __name__)

@portfolio_routes.route('/portfolio/<member_id>', methods=['GET'])
def get_portfolio(member_id):
    portfolio = get_member_portfolio(member_id)
    return jsonify(portfolio or {"error": "Not found"}), 404 if not portfolio else 200

@portfolio_routes.route('/portfolio/<member_id>', methods=['PUT'])
def edit_portfolio(member_id):
    data = request.get_json()
    update_portfolio(member_id, data['description'])
    return jsonify({"message": "Portfolio updated"})
