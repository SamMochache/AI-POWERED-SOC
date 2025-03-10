import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api"; // Adjust based on your backend URL

// Function to get the authentication token
const getAuthToken = () => localStorage.getItem("token");

// Axios instance with authorization headers
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// Request interceptor to attach the token before each request
axiosInstance.interceptors.request.use(
    (config) => {
        const token = getAuthToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Fetch Logs
export const fetchLogs = async () => {
    try {
        const response = await axiosInstance.get("/logs/");
        return response.data;
    } catch (error) {
        console.error("Error fetching logs:", error);
        throw error;
    }
};

// Fetch Alerts
export const fetchAlerts = async () => {
    try {
        const response = await axiosInstance.get("/alerts/");
        return response.data;
    } catch (error) {
        console.error("Error fetching alerts:", error);
        throw error;
    }
};

// Fetch Threats
export const fetchThreats = async () => {
    try {
        const response = await axiosInstance.get("/threats/");
        return response.data;
    } catch (error) {
        console.error("Error fetching threats:", error);
        throw error;
    }
};

// Login Function
export const loginUser = async (username, password) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/token/`, {
            username,
            password,
        });

        localStorage.setItem("token", response.data.access); // Store token
        return response.data;
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
};

// Logout Function
export const logoutUser = () => {
    localStorage.removeItem("token");
};
