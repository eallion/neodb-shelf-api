# -*- coding: UTF-8 -*-
import requests
import re
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_data(neo_page, neo_cate=None):
    allowed_categories = ['book', 'movie', 'tv', 'music', 'game', 'podcast']
    
    if neo_cate and neo_cate not in allowed_categories:
        raise ValueError(f"Invalid category. Allowed categories are: {', '.join(allowed_categories)}")

    if neo_cate:
        url = f'https://neodb.social/api/me/shelf/complete?page={neo_page}&category={neo_cate}'
    else:
        url = f'https://neodb.social/api/me/shelf/complete?page={neo_page}'
    
    headers = {'Authorization': 'Bearer QuhZZpr8bE7wllpoJ3Wd0X2OPaSRKU', 'Accept': 'application/json'}
    
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    
    return json_data

class Handler(BaseHTTPRequestHandler): 
    def do_GET(self):
        path = self.path
        neo_page = re.findall(r'page=([^&]*)', path)[0]
        neo_cate = re.findall(r'category=([^&]*)', path)
        neo_cate = neo_cate[0] if neo_cate else None

        try:    
            data = get_data(neo_page, neo_cate) 
        except Exception as e:  
            self.send_error(500, str(e))
            return
       
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        return
    
def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()