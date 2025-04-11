import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(scriptId) {
        return apiClient.get(`/script/${scriptId}/`);
    },
    async runScript(folder, selectedEnv, filteredEnvData, scriptId, params) {
        return apiClient.post('/script/run/', {
            root_folder: folder,
            env_name: selectedEnv,
            setting_overwrite: filteredEnvData,
            script_id: scriptId,
            params: params,
        });
    },
};
