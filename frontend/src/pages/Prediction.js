import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from "recharts";

import logo from "../assets/logo.png";

/* -----------------------------
BACKEND URL
----------------------------- */

const API_BASE =
  "https://iot-water-monitoring-system-backend.onrender.com/api/v1";


/* -----------------------------
Tank Visualization Component
----------------------------- */

function Tank({ level }) {

  const percent = Math.min(100, Math.max(0, level));

  return (
    <div
      style={{
        width: "120px",
        height: "220px",
        border: "3px solid black",
        position: "relative"
      }}
    >

      <div
        style={{
          position: "absolute",
          bottom: 0,
          width: "100%",
          height: `${percent}%`,
          backgroundColor: "#3498db",
          transition: "height 1s"
        }}
      />

      <div
        style={{
          position: "absolute",
          width: "100%",
          textAlign: "center",
          top: "50%",
          fontWeight: "bold"
        }}
      >
        {percent.toFixed(0)}%
      </div>

    </div>
  );
}


/* -----------------------------
Main Prediction Component
----------------------------- */

function Prediction() {

  const [distance, setDistance] = useState("");
  const [temperature, setTemperature] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [sensorData, setSensorData] = useState([]);


  /* -----------------------------
  Activity Statistics
  ----------------------------- */

  const activityStats = () => {

    const stats = {};

    history.forEach(item => {

      if (!stats[item.prediction]) {
        stats[item.prediction] = 0;
      }

      stats[item.prediction] += 1;

    });

    return Object.keys(stats).map(key => ({
      name: key,
      value: stats[key]
    }));
  };

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#AA00FF"];


  /* -----------------------------
  Manual Prediction
  ----------------------------- */

  const predict = async () => {

    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        distance: Number(distance),
        temperature: Number(temperature)
      })
    });

    const data = await res.json();
    setPrediction(data);

    loadHistory();
  };


  /* -----------------------------
  Load Prediction History
  ----------------------------- */

  const loadHistory = async () => {

    const res = await fetch(`${API_BASE}/history`);
    const data = await res.json();

    setHistory(data);
  };


  /* -----------------------------
  Auto Sensor Data
  ----------------------------- */

  const loadSensor = async () => {

    const res = await fetch(`${API_BASE}/auto-predict`);
    const data = await res.json();

    setSensorData(prev => [
      ...prev.slice(-9),
      {
        time: data.time,
        distance: data.distance,
        temperature: data.temperature
      }
    ]);

    setPrediction(data);

    loadHistory();
  };


  useEffect(() => {

    loadHistory();
    loadSensor();

    const interval = setInterval(() => {
      loadSensor();
    }, 5000);

    return () => clearInterval(interval);

  }, []);


  return (
    <div style={{ padding: "20px" }}>

      {/* -----------------------------
      Header Section
      ----------------------------- */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

        <img
          src={logo}
          alt="College Logo"
          style={{ width: "70px" }}
        />

        <div>
          <h2>IOT WATER MONITORING SYSTEM</h2>
          <p>by Ushodaya Kalyani K</p>
        </div>

      </div>


      {/* -----------------------------
      Input Section
      ----------------------------- */}

      <input
        type="number"
        placeholder="Distance"
        value={distance}
        onChange={(e) => setDistance(e.target.value)}
      />

      <input
        type="number"
        placeholder="Temperature"
        value={temperature}
        onChange={(e) => setTemperature(e.target.value)}
      />

      <button onClick={predict}>Predict</button>


      {/* -----------------------------
      Prediction Result
      ----------------------------- */}

      {prediction && (
        <div style={{ marginTop: "20px" }}>

          <h3>Prediction Result</h3>

          <p>Activity: {prediction.prediction}</p>
          <p>Confidence: {prediction.confidence}</p>

          <h3>Tank Status</h3>

          <div style={{ display: "flex", alignItems: "center", gap: "40px" }}>

            <Tank level={prediction.water_level} />

            <div>
              <p>Water Level: {prediction.water_level} cm</p>
              <p>Water Volume: {prediction.volume_liters} Liters</p>
            </div>

          </div>

        </div>
      )}


      {/* -----------------------------
      Real Time Graph
      ----------------------------- */}

      <h2 style={{ marginTop: "40px" }}>Real Time Sensor Graph</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={sensorData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="distance" stroke="#8884d8" />
          <Line type="monotone" dataKey="temperature" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>


      {/* -----------------------------
      Prediction History
      ----------------------------- */}

      <h2 style={{ marginTop: "40px" }}>Prediction History</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Time</th>
            <th>Distance</th>
            <th>Temperature</th>
            <th>Prediction</th>
            <th>Confidence</th>
          </tr>
        </thead>

        <tbody>
          {history.map((item, index) => (
            <tr key={index}>
              <td>{item.time}</td>
              <td>{item.distance}</td>
              <td>{item.temperature}</td>
              <td>{item.prediction}</td>
              <td>{item.confidence}</td>
            </tr>
          ))}
        </tbody>
      </table>


      {/* -----------------------------
      Activity Distribution Chart
      ----------------------------- */}

      <h2 style={{ marginTop: "40px" }}>Activity Distribution</h2>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={activityStats()}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label
          >
            {activityStats().map((entry, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>

    </div>
  );
}

export default Prediction;