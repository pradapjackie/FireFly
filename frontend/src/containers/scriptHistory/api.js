import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(scriptId) {
        return apiClient.get(`/script/${scriptId}/history/`);
    },
};
