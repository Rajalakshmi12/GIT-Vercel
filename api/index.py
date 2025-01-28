@app.route('/api', methods=['GET'])
def api():
    try:
        # Your logic here
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
