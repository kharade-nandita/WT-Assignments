from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from html import escape
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Add your MySQL password if you have one
    "database": "python_login_db"
}


def check_login(username, password):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, username FROM users WHERE username = %s AND password = %s",
        (username, password)
    )
    user = cursor.fetchone()

    cursor.close()
    connection.close()
    return user


class LoginHandler(BaseHTTPRequestHandler):
    def send_page(self, content, status=200):
        page = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_GET(self):
        if self.path == "/":
            with open("templates/login.html", "r", encoding="utf-8") as file:
                self.send_page(file.read())

        elif self.path == "/dashboard":
            self.send_page("""
                <!DOCTYPE html>
                <html><head><title>Dashboard</title>
                <link rel="stylesheet" href="/static/style.css"></head>
                <body><div class="box">
                <h1>Login Successful!</h1>
                <p>Welcome to the dashboard.</p>
                <a href="/">Back to Login</a>
                </div></body></html>
            """)

        elif self.path == "/static/style.css":
            with open("static/style.css", "r", encoding="utf-8") as file:
                css = file.read().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(css)))
            self.end_headers()
            self.wfile.write(css)

        else:
            self.send_page("<h1>404 - Page Not Found</h1>", 404)

    def do_POST(self):
        if self.path != "/login":
            self.send_page("<h1>404 - Page Not Found</h1>", 404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)

        username = form.get("username", [""])[0].strip()
        password = form.get("password", [""])[0]

        try:
            user = check_login(username, password)

            if user:
                self.send_page("""
                    <!DOCTYPE html>
                    <html><head><title>Welcome</title>
                    <link rel="stylesheet" href="/static/style.css"></head>
                    <body><div class="box">
                    <h1>Login Successful!</h1>
                    <p>Welcome, """ + escape(user[1]) + """!</p>
                    <a href="/dashboard">Open Dashboard</a><br><br>
                    <a href="/">Logout / Back to Login</a>
                    </div></body></html>
                """)
            else:
                self.send_page("""
                    <!DOCTYPE html>
                    <html><head><title>Login Failed</title>
                    <link rel="stylesheet" href="/static/style.css"></head>
                    <body><div class="box">
                    <h1>Login Failed</h1>
                    <p>Invalid username or password.</p>
                    <a href="/">Try Again</a>
                    </div></body></html>
                """, 401)

        except mysql.connector.Error as error:
            print("MySQL error:", error)
            self.send_page("""
                <h1>Database connection failed</h1>
                <p>Check MySQL status and DB_CONFIG in app.py.</p>
                <a href="/">Back</a>
            """, 500)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), LoginHandler)
    print("Python login server running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
