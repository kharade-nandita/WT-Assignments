const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "login_db"
});

db.connect((err) => {
    if (err) {
        console.error("Database connection failed:", err.message);
        process.exit(1);
    }
    console.log("Connected to MySQL!");
});

app.post("/login", (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({
            success: false,
            message: "Enter username and password."
        });
    }

    const sql = "SELECT id, username FROM users WHERE username = ? AND password = ?";

    db.query(sql, [username, password], (err, results) => {
        if (err) {
            console.error(err.message);
            return res.status(500).json({
                success: false,
                message: "Database query failed."
            });
        }

        if (results.length > 0) {
            return res.json({
                success: true,
                message: "Welcome, " + results[0].username + "!"
            });
        }

        return res.status(401).json({
            success: false,
            message: "Invalid username or password."
        });
    });
});

app.listen(5000, () => {
    console.log("Backend running at http://localhost:5000");
});
