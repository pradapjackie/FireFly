export const validateDynamicForm = (params, paramsConfig) => {
    let invalidParams = [];
    for (let paramName in paramsConfig) {
        const config = paramsConfig[paramName];
        const value = params[paramName] || config.defaultValue;
        if (value === null && !config.optional) {
            invalidParams.push(paramName);
        }
    }
    return invalidParams;
};
