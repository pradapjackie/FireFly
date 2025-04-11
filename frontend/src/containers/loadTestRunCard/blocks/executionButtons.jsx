import React, { useCallback } from 'react';
import { RunButton } from 'components/RunButton';
import { useSelectedEnv, useSelectedEnvName } from '../../enviroment/slice';
import { actions } from '../slice';
import { useDispatch } from 'react-redux';
import { Box } from '@mui/material';
import { validateDynamicForm } from '../../../components/DynamicForm/validate';

export const LoadTestExecutionButton = ({
    folder,
    loadTestId,
    params,
    paramsConfig,
    configValues,
    numberOfTasks,
    chartConfig,
    currentExecutionId,
    currentExecutionStatus,
}) => {
    const dispatch = useDispatch();
    const selectedEnv = useSelectedEnvName();
    const envData = useSelectedEnv();

    const validate = useCallback(() => {
        const invalidParams = validateDynamicForm(params, paramsConfig);
        if (invalidParams.length) {
            dispatch(actions.markParamAsInvalid({ loadTestId, paramNames: invalidParams }));
        }
        return !invalidParams.length;
    }, [params, paramsConfig]);

    const startLoadTest = useCallback(() => {
        if (validate()) {
            dispatch(
                actions.startLoadTest({
                    folder,
                    selectedEnv,
                    envData,
                    loadTestId,
                    params,
                    configValues,
                    numberOfTasks,
                    chartConfig,
                }),
            );
        }
    }, [folder, selectedEnv, envData, loadTestId, params, configValues, numberOfTasks]);

    const stopLoadTest = useCallback(() => {
        dispatch(actions.stopLoadTest({ loadTestId }));
    }, [loadTestId]);

    const changeNumberOfWorkers = useCallback(() => {
        dispatch(
            actions.changeNumberOfWorkers({ loadTestId, executionId: currentExecutionId, configValues, numberOfTasks }),
        );
    }, [loadTestId, currentExecutionId, configValues, numberOfTasks]);

    return (
        <Box
            sx={{
                display: 'flex',
                paddingTop: '1rem',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                gap: '2rem',
            }}
        >
            {currentExecutionStatus !== 'running' ? (
                <RunButton text={'Start load'} isDisabled={false} runCallback={startLoadTest} />
            ) : (
                <RunButton text={'Change number of workers'} isDisabled={false} runCallback={changeNumberOfWorkers} />
            )}
            <RunButton
                text={'Stop load'}
                isDisabled={currentExecutionStatus === 'finished'}
                runCallback={stopLoadTest}
                isSuccess={false}
            />
        </Box>
    );
};
