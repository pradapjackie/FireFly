import {apiClient} from 'utils/api-client';

export const api = {

  async fetch(test_id) {
    return apiClient.get(`/autotest/stat/${test_id}`);
  },

}
