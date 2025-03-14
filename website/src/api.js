import axios from 'axios';

const api = axios.create({
baseURL: 'http://localhost:18000',
  timeout: 10000, // 请求超时设定
});

export default {
    get_model_list() {
        return api.get('/api/get_model_list');
    }
};