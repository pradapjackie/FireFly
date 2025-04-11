import {apiClient} from 'utils/api-client';

export const api = {

  async fetch(folder, env) {
    return apiClient.get('/autotest/stat/', {params: {root_folder: folder, env: env}});
  },

}
