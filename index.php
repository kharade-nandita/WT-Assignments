<?php
session_start();

$error = "";
$success = "";

$conn = new mysqli("localhost", "root", "", "login_db");

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

$conn->set_charset("utf8mb4");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = trim($_POST["username"] ?? "");
    $password = $_POST["password"] ?? "";

    $stmt = $conn->prepare(
        "SELECT id, username, password FROM users WHERE username = ?"
    );

    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($user = $result->fetch_assoc()) {
        // Supports the existing demo password and password_hash() accounts.
        $validPassword = password_verify($password, $user["password"])
            || hash_equals($user["password"], $password);

        if ($validPassword) {
            session_regenerate_id(true);
            $_SESSION["username"] = $user["username"];
            $success = "Login successful! Welcome, " .
                htmlspecialchars($user["username"], ENT_QUOTES, "UTF-8") . ".";
        } else {
            $error = "Invalid username or password.";
        }
    } else {
        $error = "Invalid username or password.";
    }

    $stmt->close();
}

$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #eef2ff;
            font-family: Arial, sans-serif;
        }

        .login-box {
            width: 350px;
            max-width: 92%;
            padding: 30px;
            background: white;
            border-radius: 14px;
            box-shadow: 0 8px 25px #00000018;
        }

        h1 { text-align: center; color: #242b50; }

        label {
            display: block;
            margin: 15px 0 6px;
        }

        input {
            width: 100%;
            padding: 11px;
            border: 1px solid #ccd0df;
            border-radius: 6px;
        }

        button {
            width: 100%;
            margin-top: 22px;
            padding: 12px;
            border: 0;
            border-radius: 6px;
            background: #4f46e5;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        .message { text-align: center; overflow-wrap: anywhere; }
        .error { color: #c62828; }
        .success { color: #16803d; }
    </style>
</head>
<body>
    <main class="login-box">
        <h1>Welcome Back</h1>
        <p class="message">Login to your account</p>

        <?php if ($error !== ""): ?>
            <p class="message error">
                <?= htmlspecialchars($error, ENT_QUOTES, "UTF-8") ?>
            </p>
        <?php endif; ?>

        <?php if ($success !== ""): ?>
            <p class="message success"><?= $success ?></p>
            <p class="message">
                <a href="logout.php">Logout</a>
            </p>
        <?php else: ?>
            <form method="POST" action="">
                <label for="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    required
                    autocomplete="username"
                >

                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    required
                    autocomplete="current-password"
                >

                <button type="submit">Login</button>
            </form>
        <?php endif; ?>
    </main>
</body>
</html>
