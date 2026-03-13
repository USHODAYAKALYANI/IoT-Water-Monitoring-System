import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Prediction from "./pages/Prediction";

function Home() {
  return (
    <div style={{ padding: "40px" }}>
      <h1>IoT Water Monitoring System</h1>
      <p>Welcome to the dashboard</p>

      <Link to="/prediction">
        Go to Prediction Page
      </Link>
    </div>
  );
}

function App() {
  return (
    <Router>

      <div>

        <nav
          style={{
            background: "#1976D2",
            padding: "15px"
          }}
        >

          <Link
            to="/"
            style={{
              color: "white",
              marginRight: "20px",
              textDecoration: "none"
            }}
          >
            Home
          </Link>

          <Link
            to="/prediction"
            style={{
              color: "white",
              textDecoration: "none"
            }}
          >
            Prediction
          </Link>

        </nav>

        <Routes>

          <Route path="/" element={<Home />} />

          <Route path="/prediction" element={<Prediction />} />

        </Routes>

      </div>

    </Router>
  );
}

export default App;