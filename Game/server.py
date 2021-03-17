import http.server
import socketserver

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'World.html'
        if self.path == '/Add':
            text = open("players_test.json").read()
            f = open("players.json","w")
            f.write(text)
            f.seek(0)
            f.close
            self.path = 'World.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Start the server
print("Listening on Port 8000")
my_server.serve_forever()