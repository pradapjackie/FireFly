import { apiClient } from 'utils/api-client';

export const api = {
    async fetch(scriptId) {
        return apiClient.get(`/load_test/${scriptId}/`);
    },
    async start(folder, selectedEnv, filteredEnvData, loadTestId, params, configValues, numberOfTasks, chartConfig) {
        return apiClient.post('/load_test/start/', {
            root_folder: folder,
            env_name: selectedEnv,
            setting_overwrite: filteredEnvData,
            load_test_id: loadTestId,
            params: params,
            config_values: configValues,
            number_of_tasks: numberOfTasks,
            chart_config: chartConfig,
        });
    },
    async stop(loadTestId) {
        return apiClient.post('/load_test/stop/', {
            load_test_id: loadTestId,
        });
    },
    async changeNumberOfWorkers(loadTestId, executionId, configValues, numberOfTasks) {
        return apiClient.post('/load_test/change_number_of_workers/', {
            load_test_id: loadTestId,
            execution_id: executionId,
            config_values: configValues,
            number_of_tasks: numberOfTasks,
        });
    },
};
