import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_BASE_URL = "http://127.0.0.1:8000/api"; // Ensure this matches your Django backend

const Login = ({ setIsAuthenticated }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(""); // Clear previous errors

        try {
            const response = await axios.post(
                `${API_BASE_URL}/token/`,
                { username, password },
                { headers: { "Content-Type": "application/json" } }
            );

            console.log("Login successful! Response:", response.data); // Debugging log
            localStorage.setItem("token", response.data.access);
            setIsAuthenticated(true);
            navigate("/dashboard");
        } catch (err) {
            console.error("Login error:", err);

            if (err.response) {
                console.log("Error response:", err.response.data);
                setError(err.response.data.detail || "Invalid credentials, please try again.");
            } else if (err.request) {
                console.log("No response received:", err.request);
                setError("No response from server. Is the backend running?");
            } else {
                console.log("Request error:", err.message);
                setError("Something went wrong. Please try again.");
            }
        }
    };

    return (
        <div style={{ textAlign: "center", padding: "50px" }}>
            <h1>🔐 Login to SOC</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <br />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <br />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
