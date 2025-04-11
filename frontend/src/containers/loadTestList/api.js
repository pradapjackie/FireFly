import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(folder) {
        return apiClient.get('/load_test/', { params: { root_folder: folder } });
    },
};
