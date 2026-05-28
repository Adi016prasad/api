from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Constants - In a real app, keep these in environment variables!
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfbmFtZSI6IkNvblZPemVuLkFpIiwiaWF0IjoxNzU1NDk3OTcyLCJleHAiOjE3NTU1ODQzNzIsImp0aSI6IjE3NTU0OTc5NzIifQ.oGnN-BapKjY2i0kbV5x-gpwofeDJ7VCh6urafQTgy_Y"
BASE_URL = "https://mockingjay-mcp.convozen.ai/convozen"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/fetch-policy', methods=['POST'])
def fetch_policy():
    data = request.json
    env = data.get('env')           # hdfc_policy_prod or hdfc_policy_prod_new
    action = data.get('action')     # get-optimized-result or get-contact-details
    policy_id = data.get('policy_id')

    if not all([env, action, policy_id]):
        return jsonify({"error": "Missing parameters"}), 400

    # Build the target URL dynamically
    target_url = f"{BASE_URL}/{env}/{action}?policy_id={policy_id}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        response = requests.get(target_url, headers=headers)
        # Return the actual response from the server to our frontend
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
