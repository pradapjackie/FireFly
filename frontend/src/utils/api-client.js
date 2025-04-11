import axios from 'axios';
import {getLocalToken} from "./local-storage";

const params = {
  baseURL: typeof process.env.REACT_APP_OUT_DOCKER === 'undefined' ? '/api' : 'http://localhost/api'
};

export const bareApiClient = axios.create(params);
const apiClient = axios.create(params);
apiClient.defaults.headers.common.Authorization = `Bearer ${getLocalToken()}`;
export {apiClient};
