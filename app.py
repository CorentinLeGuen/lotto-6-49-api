from flask import Flask, request, jsonify

from db import LottoDB

app = Flask(__name__)

db = LottoDB()


@app.errorhandler(400)
def page_error_400(e):
    return jsonify(error=400, text=str(e)), 400


@app.errorhandler(404)
def page_error_404(e):
    return jsonify(error=404, text=str(e)), 404


@app.errorhandler(405)
def page_error_405(e):
    return jsonify(error=405, text=str(e)), 405


@app.errorhandler(500)
def page_error_500(e):
    return jsonify(error=500, text=str(e)), 500


@app.route('/', methods=['GET'])
def get_draws():
    return jsonify(db.get_all()), 200


@app.route('/date', methods=['GET'])
def get_date():
    date = request.args.get('full')
    if date:
        result = db.get_by_date(date)
        if result:
            return jsonify(result), 200
        return jsonify(error=404, text=f"Nothing found for date {date}"), 404
    date = request.args.get('starting')
    if date:
        result = db.get_by_date_wc(date)
        if result:
            return jsonify(result), 200
        return jsonify(error=404, text=f"Nothing found for date starting by {date}"), 404
    return jsonify(error=400, text="'full' or 'starting' parameter expected"), 400


@app.route('/stats', methods=['GET'])
def get_stats():
    result = db.get_stats()
    return jsonify({'date_start': result[1], 'date_last': result[0], 'total': result[2], 'stats': result[3]}), 200


@app.route('/total', methods=['GET'])
def get_total():
    result = db.get_total_records()
    return jsonify({'total': result}), 200


@app.route('/number', methods=['GET'])
def get_number():
    n = request.args.get('all')
    if n and n.isnumeric():
        result = db.get_by_number(int(n))
        if result and len(result) != 0:
            return jsonify(result), 200
        return jsonify(error=404, text=f"No result found for number {n}."), 404
    n = request.args.get('comp')
    if n and n.isnumeric():
        result = db.get_by_complementary_number(int(n))
        if result and len(result) != 0:
            return jsonify(result), 200
        return jsonify(error=404, text=f"No result found for complementary number {n}."), 404
    return jsonify(error=400, text="'all' or 'comp' parameter expected"), 400
