import http.server as srv;
import os;
from urllib.parse import parse_qs as dc;

page = """
<!DOCTYPE html>
<html>
	<head>
		<title>QSA – QuickShellAccess</title>
		<meta charset="utf-8">
		<style>
			input, textarea {
				font-family: monospace;
			}
		</style>
	</head>
	<body>
		<input id="directory" placeholder="Working directory"><br>
		<input id="command" placeholder="Command"><br>
		<input type="submit" onclick="execute()">
		<br>
		<textarea readonly id="output"> </textarea>
		<script>
			function execute(){
				fetch("/", {
					"body": "command=" + encodeURIComponent(document.getElementById("command").value) + "&working_dir=" + document.getElementById("directory").value,
					"method": "POST"
				}).catch(() => {
					alert("Error!");
				}).then(res => res.text()).then(res => {
					document.getElementById("output").value = res;
				});
			}
		</script>
	</body>
</html>
"""

class MainHandler(srv.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200);
		self.send_header("Content-Type", "text/html");
		self.end_headers();
		self.wfile.write(bytes(page, encoding = "utf-8"));
	def do_POST(self):
		data = dc(self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8"));
		data = {k: v[0] for k, v in data.items()};
		os.chdir(data["working_dir"]);
		self.send_response(200);
		self.send_header("Content-Type", "text/plain");
		self.end_headers();
		self.wfile.write(bytes(os.popen(data["command"]).read(), "utf-8"));

def run(server_class = srv.HTTPServer, handler_class = MainHandler):
	httpd = server_class(("", 48474), handler_class);
	httpd.serve_forever();
run();
