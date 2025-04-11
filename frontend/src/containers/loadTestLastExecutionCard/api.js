import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(loadTestId) {
        return apiClient.get(`/load_test/${loadTestId}/last/`);
    }
};
