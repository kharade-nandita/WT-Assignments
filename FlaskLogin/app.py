from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps

app = Flask(__name__)
app.secret_key = "flask-login-assignment-secret-key"

# Connect to the existing XAMPP MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login_db",
        port=3306
    )

# Require login before opening the dashboard
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()

            # Supports hashed passwords and existing plain-text assignment passwords
            if user:
                stored_password = user["password"]
                password_matches = False

                if stored_password.startswith(("pbkdf2:", "scrypt:")):
                    from werkzeug.security import check_password_hash
                    password_matches = check_password_hash(stored_password, password)
                else:
                    password_matches = (stored_password == password)

                if password_matches:
                    session.clear()
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    return redirect(url_for("dashboard"))

            flash("Invalid username or password.", "error")

        except mysql.connector.Error:
            app.logger.exception("Database error during login")
            flash("Unable to connect to the database. Check XAMPP MySQL.", "error")

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
