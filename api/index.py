# import json
# from http.server import BaseHTTPRequestHandler

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps({"message": "Hello!"}).encode('utf-8'))
#         return

# api/index.py
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load the Json file with student data
try:
    with open('q-vercel-python.json','r') as file:
        students = json.load(file)
except Exception as e:
    students = {}
    print(f"Error loading students.json: {e}")
        
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        #Parse Query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', []) #Get the name parameter as a list   
            
        #Retrieve Marks from the json file with the name parsed from the URL
        marks = []
        for name in names:
            # Search for the name in the student data
            student = next((s for s in students if s["name"] == name), None)
            if student:
                marks.append(student["marks"])
            else:
                marks.append("Not Found")
                
        #Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # This is enabling CORS
        self.end_headers()
        
        #Send JSON response
        response = {"marks": marks}
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
            