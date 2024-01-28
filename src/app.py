from flask import Flask, jsonify, request

from src.db.db import DB

app = Flask(__name__)

# Configure the database connection
db = DB()
db.connect()


# Route to get all segments
@app.route('/segments', methods=['GET'])
def get_segments():
    data = db.query_data("segments")
    return jsonify(data)


# Route to get all companies in a specific segment
@app.route('/companies/<int:segment_id>', methods=['GET'])
def get_companies_by_segment(segment_id: int):
    data = db.query_data("companies", condition=f"segmentid = {segment_id}")
    return jsonify(data)


# Route to get leads for a specific company
@app.route('/leads/<int:company_id>', methods=['GET'])
def get_leads_by_company(company_id: int):
    data = db.query_data("leads", condition=f"companyid = {company_id}")
    return jsonify(data)


# Route to search for companies by name
@app.route('/search', methods=['GET'])
def search_companies():
    query = request.args.get('query')
    data = db.query_data("companies", condition=f"name ILIKE '%{query}%'")
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
