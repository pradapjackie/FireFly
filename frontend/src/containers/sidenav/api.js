import { apiClient } from '../../utils/api-client';

export const api = {
    async getTestsFolders() {
        return apiClient.get('/autotest/root_folders/');
    },

    async getScriptsFolders() {
        return apiClient.get('/script/root_folders/');
    },

    async getLoadTestsFolders() {
        return apiClient.get('/load_test/root_folders/');
    },
};
