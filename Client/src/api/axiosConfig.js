import axios from 'axios';


const api = axios.create({
  baseURL: 'http://defrontaback-8181a176203ccdac.elb.us-east-1.amazonaws.com:5000' || 'http://127.0.0.1:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      console.error('Error de respuesta:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('Error de solicitud:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;