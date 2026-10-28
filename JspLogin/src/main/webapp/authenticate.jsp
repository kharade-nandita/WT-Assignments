<%@ page import="java.sql.*" %>
<%@ page import="org.mindrot.jbcrypt.BCrypt" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Login Result</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 100px;">

<%
    request.setCharacterEncoding("UTF-8");

    String username = request.getParameter("username");
    String password = request.getParameter("password");

    boolean valid = false;

    if (username != null && password != null) {
        String url = "jdbc:mariadb://localhost:3306/login_db";
        String dbUser = "root";
        String dbPassword = "";

        try {
            Class.forName("org.mariadb.jdbc.Driver");

            try (Connection con = DriverManager.getConnection(url, dbUser, dbPassword);
                 PreparedStatement ps = con.prepareStatement(
                     "SELECT password FROM users WHERE username = ?")) {

                ps.setString(1, username);

                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        String storedPassword = rs.getString("password");

                        if (storedPassword != null &&
                            (storedPassword.startsWith("$2a$") ||
                             storedPassword.startsWith("$2b$") ||
                             storedPassword.startsWith("$2y$"))) {

                            if (storedPassword.startsWith("$2y$")) {
                                storedPassword = "$2a$" + storedPassword.substring(4);
                            }

                            valid = BCrypt.checkpw(password, storedPassword);
                        } else {
                            valid = password.equals(storedPassword);
                        }
                    }
                }
            }

            if (valid) {
%>
                <h2 style="color: green;">Login Successful!</h2>
                <p>Welcome, <%= username.replace("&", "&amp;")
                                         .replace("<", "&lt;")
                                         .replace(">", "&gt;")
                                         .replace("\"", "&quot;")
                                         .replace("'", "&#39;") %>!</p>
<%
            } else {
%>
                <h2 style="color: red;">Invalid Username or Password</h2>
<%
            }

        } catch (Exception e) {
            application.log("Database login error", e);
%>
            <h2 style="color: red;">Unable to verify login.</h2>
            <p>Check that MySQL is running and the database settings are correct.</p>
<%
        }
    } else {
%>
        <h2>Please enter your username and password.</h2>
<%
    }
%>

    <p><a href="login.jsp">Back to Login</a></p>
</body>
</html>
