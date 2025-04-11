import { apiClient } from 'utils/api-client';

export const api = {
  async fetch(testRunId) {
    return apiClient.get(`/autotest/test_run/tree/${testRunId}`);
  },
};
