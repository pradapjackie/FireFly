import { apiClient } from 'utils/api-client';

export const api = {
    async fetch_test_runs(folder, env) {
        return apiClient.get('/autotest/test_runs/', { params: { root_folder: folder, env: env } });
    },
};
