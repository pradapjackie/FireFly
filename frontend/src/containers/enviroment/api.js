import {apiClient} from "../../utils/api-client";

export const api = {

  async fetch() {
    return apiClient.get("/autotest/env");
  },
  async fetchByEnv(env) {
    return apiClient.get(`/autotest/env/${env}`);
  },
  async updateEnv(env, data) {
    return apiClient.patch(`/autotest/env/${env}`, data);
  },
}
