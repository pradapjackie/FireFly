import { apiClient } from 'utils/api-client';
import { createWebSocketConnection } from 'utils/ws-client';

export const api = {
    async fetch(scriptId) {
        return apiClient.get(`/script/${scriptId}/last/`);
    },
    async openScriptEventChannel() {
        return createWebSocketConnection(`/script/ws/history/`);
    },
};
