import React from "react";
import { useNavigate, Link } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/"); // Redirect to login page
  };

  return (
    <nav
      style={{
        marginBottom: "2rem",
        borderBottom: "1px solid #eee",
        paddingBottom: "1rem",
      }}
    >
      <ul>
        <li>
          <Link to="/home" style={{ textDecoration: "none", color: "inherit" }}>
            <h2>
              <strong>MyDailyTime</strong>
            </h2>
          </Link>
        </li>
      </ul>
      <ul>
        <li>
          <Link to="/home" className="secondary">
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/analytics" className="secondary">
            Analytics
          </Link>
        </li>
        <li>
          <button className="secondary outline" onClick={handleLogout}>
            Logout
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
