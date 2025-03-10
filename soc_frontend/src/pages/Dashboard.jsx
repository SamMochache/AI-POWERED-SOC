import React, { useEffect, useState } from "react";
import { fetchLogs, fetchAlerts, fetchThreats } from "../api/api";
import { useNavigate } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const Dashboard = ({ setIsAuthenticated }) => {
    const [logs, setLogs] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [threats, setThreats] = useState([]);
    const [anomalyData, setAnomalyData] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const logsData = await fetchLogs();
                const alertsData = await fetchAlerts();
                const threatsData = await fetchThreats();
                
                setLogs(logsData.reverse());
                setAlerts(alertsData.reverse());
                setThreats(threatsData.reverse());
                
                // Process anomaly data
                const anomalyCounts = {};
                logsData.forEach(log => {
                    const timestamp = new Date(log.timestamp).toLocaleTimeString();
                    anomalyCounts[timestamp] = (anomalyCounts[timestamp] || 0) + 1;
                });
                
                const formattedData = Object.keys(anomalyCounts).map(time => ({
                    time,
                    anomalies: anomalyCounts[time]
                }));
                
                setAnomalyData(formattedData);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("token");
        setIsAuthenticated(false);
        navigate("/");
    };

    if (loading) return <h2 style={{ textAlign: "center" }}>Loading data... ⏳</h2>;

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1 style={{ textAlign: "center", color: "#4CAF50" }}>🚀 AI-Powered SOC Dashboard</h1>
            <button onClick={handleLogout} style={{ float: "right", padding: "10px 20px", background: "#f44336", color: "white", border: "none", cursor: "pointer" }}>Logout</button>
            
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px", marginTop: "20px" }}>
                <div style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "5px" }}>
                    <h2>📊 Anomaly Trends</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={anomalyData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="time" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="anomalies" stroke="#ff7300" />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                <div style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "5px", overflowY: "auto", maxHeight: "500px" }}>
                    <h2>📌 Logs ({logs.length})</h2>
                    <table border="1" width="100%">
                        <thead style={{ position: "sticky", top: 0, background: "#333", color: "white" }}>
                            <tr>
                                <th>Source IP</th>
                                <th>Destination IP</th>
                                <th>Protocol</th>
                            </tr>
                        </thead>
                        <tbody>
                            {logs.map((log) => (
                                <tr key={log.id}>
                                    <td>{log.source_ip}</td>
                                    <td>{log.destination_ip}</td>
                                    <td>{log.protocol}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "5px", overflowY: "auto", maxHeight: "500px" }}>
                    <h2>⚠️ Alerts ({alerts.length})</h2>
                    <table border="1" width="100%">
                        <thead style={{ position: "sticky", top: 0, background: "#d9534f", color: "white" }}>
                            <tr>
                                <th>Message</th>
                                <th>Created At</th>
                            </tr>
                        </thead>
                        <tbody>
                            {alerts.map((alert) => (
                                <tr key={alert.id}>
                                    <td>{alert.message}</td>
                                    <td>{new Date(alert.created_at).toLocaleString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "5px", overflowY: "auto", maxHeight: "500px" }}>
                    <h2>🔍 Threats ({threats.length})</h2>
                    <table border="1" width="100%">
                        <thead style={{ position: "sticky", top: 0, background: "#f0ad4e", color: "white" }}>
                            <tr>
                                <th>Type</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            {threats.map((threat) => (
                                <tr key={threat.id}>
                                    <td>{threat.type}</td>
                                    <td>{threat.description}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
