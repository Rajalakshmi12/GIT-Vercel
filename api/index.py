# api/index.py
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Load the JSON file with student data
try:
    file_path = os.path.join(os.path.dirname(__file__), '../q-vercel-python.json')
    with open(file_path, 'r') as file:
        students = json.load(file)
        if not isinstance(students, list):  # Validate the JSON structure
            raise ValueError("Invalid JSON format: Expected a list of dictionaries.")
except FileNotFoundError:
    students = []
    logging.error("JSON file not found. Ensure 'q-vercel-python.json' is in the correct directory.")
except ValueError as e:
    students = []
    logging.error(f"Error parsing JSON file: {e}")
except Exception as e:
    students = []
    logging.error(f"Unexpected error loading JSON file: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse Query parameters
            query = parse_qs(urlparse(self.path).query)
            names = query.get('name', [])  # Get the 'name' parameter as a list

            if not names:
                raise ValueError("No 'name' parameter provided in the query string.")

            # Retrieve Marks from the JSON file
            marks = []
            for name in names:
                # Search for the name in the student data
                student = next((s for s in students if s["name"] == name), None)
                if student:
                    marks.append(student["marks"])
                else:
                    marks.append("Not Found")

            # Send a successful response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
            self.end_headers()

            # Send JSON response
            response = {"marks": marks}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except ValueError as ve:
            self._send_error_response(400, str(ve))  # Handle bad requests (400)
        except Exception as e:
            logging.error(f"Unexpected server error: {e}")
            self._send_error_response(500, "Internal Server Error")  # Handle unexpected errors

    def _send_error_response(self, code, message):
        """Helper method to send error responses."""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS for errors
        self.end_headers()
        error_response = {"error": message}
        self.wfile.write(json.dumps(error_response).encode('utf-8'))
