import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate(); // NEW: Hook for navigation

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const endpoint = isLogin ? "/login" : "/signup";

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000${endpoint}`,
        formData,
      );
      if (isLogin) {
        localStorage.setItem("token", response.data.access_token);
        navigate("/home"); // NEW: Redirect to home page
      } else {
        setIsLogin(true);
        alert("Account created! Please log in.");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <article
        style={{ maxWidth: "500px", margin: "0 auto", marginTop: "10vh" }}
      >
        <h2>{isLogin ? "Welcome Back" : "Create Account"}</h2>
        {error && <mark>{error}</mark>}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email Address"
            required
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
          />
          <input
            type="password"
            placeholder="Password"
            required
            value={formData.password}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
          />
          <button type="submit" aria-busy={loading}>
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>
        <footer>
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              setIsLogin(!isLogin);
            }}
          >
            {isLogin
              ? "Don't have an account? Sign Up"
              : "Already have an account? Login"}
          </a>
        </footer>
      </article>
    </main>
  );
};

export default Auth;
