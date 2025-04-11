import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import {
    useLoadTestLastExecutionCardSelector,
    useLoadTestLastExecutionCardSlice,
    useCurrentLoadTestSubscribeIdSelector,
} from './slice';
import { LocalLoading } from 'components/Loading/LocalLoading';
import { Name } from './blocks/name';
import { Workers } from './blocks/workers';
import { Grid } from '@mui/material';
import { Tasks } from './blocks/tasks';
import { Charts } from './blocks/charts'
import {useLoadTestChartConfigSelector} from "../loadTestRunCard/slice";

export const LoadTestLastExecutionCard = ({ loadTestId }) => {
    const { actions } = useLoadTestLastExecutionCardSlice();
    const dispatch = useDispatch();
    const currentSubscribeId = useCurrentLoadTestSubscribeIdSelector();
    const { fetchStatus, ...history } = useLoadTestLastExecutionCardSelector(loadTestId);
    const chartConfig = useLoadTestChartConfigSelector(loadTestId);
    const executionId = history?.executionId;

    useEffect(() => {
        dispatch(actions.fetch({ loadTestId }));
    }, [loadTestId]);

    useEffect(() => {
        dispatch(actions.initWS());

        return function cleanup() {
            dispatch(actions.closeWS());
        };
    }, []);

    useEffect(() => {
        if (fetchStatus === 'success' && executionId !== currentSubscribeId) {
            dispatch(actions.subscribe({ executionId, loadTestId }));
        }
    }, [fetchStatus, executionId, currentSubscribeId]);

    if (fetchStatus !== 'success') return <LocalLoading />;

    return (
        <>
            <Name name={'Last load test data'} status={history.status} />
            <Grid container spacing={3} sx={{ paddingTop: '1rem' }}>
                <Grid item sm={8} xs={12}>
                    <Workers workers={history.workers} />
                </Grid>
                <Grid item sm={4} xs={12}></Grid>
            </Grid>
            <Tasks series={history.taskStatusHistory} />
            <Charts chartConfig={chartConfig} chartsData={history.charts}/>
        </>
    );
};
