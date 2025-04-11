export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token) => localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

export const saveEnvOverwriteData = (env, data) => localStorage.setItem(`${env}_overwrite_data`, data);

export const getEnvOverwriteData = (env) => localStorage.getItem(`${env}_overwrite_data`) || "{}";

export const saveActiveEnv = (env) => localStorage.setItem('selected_env', env);

export const getActiveEnv = () => localStorage.getItem('selected_env');
