import { useState } from "react";
import "./App.css";

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      const data = await response.json();
      setMessage(data.message);
    } catch {
      setMessage("Cannot connect to server. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="login-card">
        <div className="logo">L</div>
        <h1>Welcome Back</h1>
        <p className="subtitle">Login to your account</p>

        <form onSubmit={handleLogin}>
          <label htmlFor="username">Username</label>
          <input id="username" value={username}
            onChange={e => setUsername(e.target.value)}
            placeholder="Enter your username" required />

          <label htmlFor="password">Password</label>
          <input id="password" type="password" value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Enter your password" required />

          <button disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {message && <p className={message.startsWith("Welcome") ? "success" : "error"}>{message}</p>}
        <p className="footer">Secure Login Portal</p>
      </section>
    </main>
  );
}
