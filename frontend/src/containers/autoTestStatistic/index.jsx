import React, { useEffect } from 'react';
import { Box, Card, Fade } from '@mui/material';
import { PieChart } from 'components/PieChart';
import { StackedHistoryChart } from './stackedChart';
import { useTheme } from '@mui/styles';
import { useDispatch } from 'react-redux';
import { useAutoTestStatisticSlice, useAutoTestStatisticSliceSelector } from './slice';

export function AutoTestStatistic({ folder, env }) {
    const { actions } = useAutoTestStatisticSlice();
    const { palette } = useTheme();
    const dispatch = useDispatch();

    const { status, stat, testRuns } = useAutoTestStatisticSliceSelector(folder, (state) => state);
    const isSuccess = status === 'success';

    useEffect(() => {
        dispatch(actions.fetch({ folder: folder, env: env }));
    }, [folder, env]);

    return (
        <Fade in timeout={300}>
            <Card
                sx={{
                    paddingLeft: '1.5rem',
                    paddingRight: '1.5rem',
                    paddingTop: '1rem',
                    paddingBottom: '1rem',
                    overflowY: 'auto',
                    maxHeight: 'calc(100vh - 252px)',
                }}
            >
                <Box
                    sx={{
                        fontSize: '1rem',
                        textTransform: 'capitalize',
                        fontWeight: '500',
                        textAlign: 'center',
                    }}
                >
                    Last 3 month stat
                </Box>
                {isSuccess ? (
                    <PieChart
                        height="300px"
                        color={[palette.success.main, palette.text.secondary, palette.error.main]}
                        data={stat}
                    />
                ) : (
                    <></>
                )}
                {isSuccess ? (
                    <StackedHistoryChart
                        color={[palette.success.main, palette.secondary.main, palette.error.main]}
                        testRuns={testRuns}
                    />
                ) : (
                    <></>
                )}
            </Card>
        </Fade>
    );
}
