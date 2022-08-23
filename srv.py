from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import httpx
from configuration import WEBHOOK_URL, JIRA_BASE_URL

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        try:
            json_data = json.loads(post_data)
            if json_data['webhookEvent'] == 'jira:issue_created':
                title = f"{json_data['issue']['fields']['creator']['displayName']} created new task"
                issue_key = json_data['issue']['key']
                issue_summary = json_data['issue']['fields']['summary']
                jira_url = f"{JIRA_BASE_URL}/browse/{issue_key}"
                
                with open('team_json_base.json', 'r') as f:
                    json_data = json.load(f)

                json_data['sections'][0]['activityTitle'] = title
                
                for fact in json_data['sections'][0]['facts']:
                    if fact['name'] == 'Issue':
                        fact['value'] = issue_key
                    elif fact['name'] == 'Summary':
                        fact['value'] = issue_summary 

                json_data['potentialAction'][0]['targets'][0]['uri'] = jira_url 

                json_data = json.dumps(json_data)
                logging.info(json_data)
                httpx.post(WEBHOOK_URL, data=json_data)
        except Exception as e:
            logging.info(f"Exception occured: {e}")

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
