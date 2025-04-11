import { apiClient } from 'utils/api-client';

export const api = {
  async fetch(testRunId, itemId) {
    return apiClient.get(`/autotest/test_run/${testRunId}/test/${itemId}`);
  },
};
