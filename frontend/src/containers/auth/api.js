import {apiClient, bareApiClient} from 'utils/api-client';

export const api = {

  async authorize(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return bareApiClient.post('/login/access-token', params);
  },

  async getMe(token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    return apiClient.get('/users/me');
  },

  async signUp(email, password, fullName) {
    return bareApiClient.post('/login/signup', {
      email: email,
      password: password,
      full_name: fullName
    });
  }

}
