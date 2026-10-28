const express = require("express");
const mysql = require("mysql2/promise");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, "public")));

const pool = mysql.createPool({
    host: "localhost",
    user: "root",
    password: "",
    database: "login_db",
    port: 3306,
    waitForConnections: true,
    connectionLimit: 10
});

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "login.html"));
});

app.post("/login", async (req, res) => {
    const username = (req.body.username || "").trim();
    const password = req.body.password || "";

    try {
        const [rows] = await pool.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            [username, password]
        );

        if (rows.length > 0) {
            return res.send(`
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Login Successful</title>
                </head>
                <body style="font-family:Arial;text-align:center;padding-top:100px">
                    <h1>Login Successful!</h1>
                    <h2>Welcome, ${escapeHtml(rows[0].username)}!</h2>
                    <a href="/">Back to Login</a>
                </body>
                </html>
            `);
        }

        return res.status(401).send(`
            <!DOCTYPE html>
            <html lang="en">
            <head><meta charset="UTF-8"><title>Login Failed</title></head>
            <body style="font-family:Arial;text-align:center;padding-top:100px">
                <h2>Invalid username or password!</h2>
                <a href="/">Try Again</a>
            </body>
            </html>
        `);
    } catch (error) {
        console.error("Database error:", error.message);
        return res.status(500).send(
            "Database connection failed. Check XAMPP MySQL and database settings."
        );
    }
});

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

async function startServer() {
    try {
        const connection = await pool.getConnection();
        console.log("MySQL connected successfully to login_db");
        connection.release();

        app.listen(PORT, () => {
            console.log(`Server running at http://localhost:${PORT}`);
        });
    } catch (error) {
        console.error("Could not connect to MySQL:", error.message);
        process.exit(1);
    }
}

startServer();
