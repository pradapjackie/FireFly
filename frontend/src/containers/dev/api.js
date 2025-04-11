import { apiClient } from '../../utils/api-client';

export const api = {
    async recollectTests() {
        return apiClient.post('/autotest/dev/recollect/');
    },

    async recollectScripts() {
        return apiClient.post('/script/dev/recollect/');
    },

    async recollectLoadTests() {
        return apiClient.post('/load_test/dev/recollect/');
    },
};
