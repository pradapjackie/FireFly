import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(folder) {
        return apiClient.get('/script/', { params: { root_folder: folder } });
    },
};
