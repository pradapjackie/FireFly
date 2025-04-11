import React, { useCallback } from 'react';
import { RunButton } from 'components/RunButton';
import { useSelectedEnv, useSelectedEnvName } from '../../enviroment/slice';
import { actions } from '../slice';
import { useDispatch } from 'react-redux';
import { Box } from '@mui/material';
import { validateDynamicForm } from '../../../components/DynamicForm/validate';

export const RunScriptButton = ({ folder, scriptId, params, paramsConfig }) => {
    const dispatch = useDispatch();
    const selectedEnv = useSelectedEnvName();
    const envData = useSelectedEnv();

    const validate = useCallback(() => {
        const invalidParams = validateDynamicForm(params, paramsConfig);
        if (invalidParams.length) {
            dispatch(actions.markParamAsInvalid({ scriptId, paramNames: invalidParams }));
        }
        return !invalidParams.length;
    }, [params, paramsConfig]);

    const runScript = useCallback(() => {
        if (validate()) {
            dispatch(actions.runScript({ folder, selectedEnv, envData, scriptId, params }));
        }
    }, [folder, selectedEnv, envData, scriptId, params]);

    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <RunButton text={'Run script'} isDisabled={false} runCallback={runScript} />
        </Box>
    );
};
