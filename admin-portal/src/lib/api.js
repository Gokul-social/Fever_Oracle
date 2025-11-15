import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      return Promise.reject({
        message: error.response.data?.error || error.response.data?.message || 'An error occurred',
        status: error.response.status,
        data: error.response.data,
      })
    } else if (error.request) {
      // Request made but no response
      return Promise.reject({
        message: 'Network error. Please check your connection.',
        status: 0,
      })
    } else {
      // Something else happened
      return Promise.reject({
        message: error.message || 'An unexpected error occurred',
        status: 0,
      })
    }
  }
)

// Admin API endpoints
export const adminAPI = {
  // Get dashboard stats
  getStats: () => api.get('/admin/stats'),
  
  // Get hospitals list
  getHospitals: () => api.get('/admin/hospitals'),
  
  // Get predicted hotspots
  getHotspots: () => api.get('/admin/hotspots'),
  
  // Get alerts
  getAlerts: () => api.get('/admin/alerts'),
}

export default api

