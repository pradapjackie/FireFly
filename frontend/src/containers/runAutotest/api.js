import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(folder) {
        return apiClient.get('/autotest/', { params: { root_folder: folder } });
    },

    async run(folder, testIds, selectedEnv, filteredEnvData, runConfig) {
        return apiClient.post('/autotest/run/', {
            root_folder: folder,
            env_name: selectedEnv,
            test_ids: testIds,
            setting_overwrite: filteredEnvData,
            run_config: runConfig,
        });
    },

    async fetchDynamicData(callback) {
        return apiClient.get(callback);
    },
};
