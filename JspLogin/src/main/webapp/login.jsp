<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JSP Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
        }
        .box {
            background: white;
            width: 320px;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 12px #ccc;
        }
        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 11px;
            margin: 10px 0;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>Login Page</h2>

        <form action="authenticate.jsp" method="post">
            <label>Username</label>
            <input type="text" name="username" required>

            <label>Password</label>
            <input type="password" name="password" required>

            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
