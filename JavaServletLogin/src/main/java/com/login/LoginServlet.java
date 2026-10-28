
package com.login;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();

        out.println("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Java Servlet Login</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #f2f2f2;
                        display: flex;
                        justify-content: center;
                        padding-top: 80px;
                    }
                    .box {
                        background: white;
                        padding: 30px;
                        width: 320px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px #ccc;
                    }
                    input, button {
                        box-sizing: border-box;
                        width: 100%;
                        padding: 10px;
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
                    <h2>Login</h2>
                    <form method="post" action="login">
                        <label>Username</label>
                        <input type="text" name="username" required>

                        <label>Password</label>
                        <input type="password" name="password" required>

                        <button type="submit">Login</button>
                    </form>
                </div>
            </body>
            </html>
            """);
    }

    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");
        response.getWriter().println(
            "<h2>Login form submitted successfully!</h2>"
            + "<p>Database authentication will be connected next.</p>"
            + "<a href='login'>Back to Login</a>"
        );
    }
}
