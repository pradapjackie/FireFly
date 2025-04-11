export const filterOnlyOverwrite = (envData) => {
    const filteredEnvData = {};
    envData.ids.forEach((id) => {
        if (envData.entities[id].overwrite) {
            filteredEnvData[id] = {
                value: envData.entities[id].overwrite,
                secure: envData.entities[id].secure,
            };
        }
    });
    return filteredEnvData;
};
