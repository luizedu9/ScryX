
import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

export function authenticate(userData) {
    return axios.post(`${API_URL}/login/`, userData);
}

export function register(userData) {
    return axios.post(`${API_URL}/register/`, userData);
}