import React, { useCallback, useEffect } from 'react';
import Box from '@mui/material/Box';
import { useDispatch } from 'react-redux';
import { LocalLoading } from '../../components/Loading/LocalLoading';
import { useLoadTestRunCardSelector, useLoadTestRunCardSlice } from './slice';
import { Name } from './blocks/name';
import { ViewHistoryButton } from './blocks/viewHistoryButton';
import { Description } from './blocks/description';
import { InputParams } from './blocks/inputParams';
import { ExecutionParams } from './blocks/executionParams';
import { Grid } from '@mui/material';
import { LoadTestExecutionButton } from './blocks/executionButtons';
import { WorkerSlider } from './blocks/workerSlider';
import {
    useLoadTestLastExecutionIdSelector,
    useLoadTestLastExecutionStatusSelector,
} from '../loadTestLastExecutionCard/slice';

export const LoadTestRunCard = ({ folder, loadTestId }) => {
    const { actions } = useLoadTestRunCardSlice();
    const dispatch = useDispatch();
    const { fetchStatus, ...loadTest } = useLoadTestRunCardSelector(loadTestId);
    const currentExecutionStatus = useLoadTestLastExecutionStatusSelector(loadTestId);
    const currentExecutionId = useLoadTestLastExecutionIdSelector(loadTestId);

    useEffect(() => {
        dispatch(actions.fetch({ loadTestId }));
    }, [loadTestId]);

    const setResultConfig = useCallback(
        (paramName, paramValue) => {
            dispatch(actions.setLoadTestParamValue({ loadTestId, paramName, paramValue }));
        },
        [loadTestId],
    );

    const setExecutionConfigResult = useCallback(
        (paramName, paramValue) => {
            dispatch(actions.setLoadTestExecutionParamValue({ loadTestId, paramName, paramValue }));
        },
        [loadTestId],
    );

    const changeNumberOfTasks = useCallback(
        (_, numberOfTasks) => {
            dispatch(actions.setNumberOfTasks({ loadTestId, numberOfTasks }));
        },
        [loadTestId],
    );

    if (fetchStatus !== 'success') return <LocalLoading />;

    return (
        <>
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                }}
            >
                <Name name={loadTest.displayName} />
                <ViewHistoryButton switchToHistory={undefined} />
            </Box>
            <Description description={loadTest.description} />
            <Grid container spacing={3} sx={{ paddingTop: '1rem' }}>
                <Grid item sm={8} xs={12}>
                    <InputParams
                        paramsConfig={loadTest.params}
                        paramsState={loadTest.parametersValues}
                        setParamsState={setResultConfig}
                    />
                </Grid>
                <Grid item sm={4} xs={12}>
                    <ExecutionParams
                        paramsConfig={loadTest.config}
                        paramsState={loadTest.executionConfigValues}
                        setParamsState={setExecutionConfigResult}
                    />
                </Grid>
            </Grid>
            <WorkerSlider
                config={loadTest.config}
                configState={loadTest.executionConfigValues}
                numberOfTasks={loadTest.numberOfTasks}
                changeNumberOfTasks={changeNumberOfTasks}
            />
            <LoadTestExecutionButton
                folder={folder}
                loadTestId={loadTestId}
                params={loadTest.parametersValues}
                paramsConfig={loadTest.params}
                configValues={loadTest.executionConfigValues}
                numberOfTasks={loadTest.numberOfTasks}
                chartConfig={loadTest.charts}
                currentExecutionId={currentExecutionId}
                currentExecutionStatus={currentExecutionStatus}
            />
        </>
    );
};
