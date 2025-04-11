import React, { useEffect } from 'react';
import { PieChart } from 'components/PieChart';
import { useTheme } from '@mui/styles';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { SimpleTable } from 'components/SimpleTable';
import { useTestRunStatisticSelector, useTestRunStatisticSlice } from './slice';
import { useDispatch } from 'react-redux';
import { TestRunStatisticSkeleton } from './blocks/skeleton';
import { FireFlyError } from '../../components/FireflyError';
import { isEmpty } from 'lodash';

export function TestRunStatistic({ testRunId }) {
  const { actions } = useTestRunStatisticSlice();
  const dispatch = useDispatch();
  const { fetchStatus, status, ...data } =
    useTestRunStatisticSelector(testRunId);

  const { palette } = useTheme();

  useEffect(() => {
    dispatch(actions.fetch({ testRunId }));
  }, [testRunId]);

  return (
    <>
      <Typography
        variant="h6"
        color="textSecondary"
        sx={{ alignSelf: 'center' }}
      >
        Test Run Statistic
      </Typography>
      {fetchStatus === 'success' ? (
        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
          {['primed', 'running', 'success'].includes(status) && (
            <PieChart
              height="300px"
              color={[
                palette.success.main,
                palette.text.secondary,
                palette.error.main,
              ]}
              data={data.resultByStatus}
            />
          )}
          <SimpleTable
            data={{
              'Status:': status,
              Version: data.version,
              Start: data.startTime,
              User: data.user.fullName,

              // 'Tests with warnings': `${data.withWarnings} (${Math.round(
              //   (withWarnings / total) * 100,
              // )}%)`,
            }}
            stringify={false}
          />
          {!isEmpty(data.error) && (
            <Box sx={{ marginTop: '1rem' }}>
              <FireFlyError
                errorName={data.error.name}
                errorMessage={data.error.message}
                errorTrace={data.error.traceback}
              />
            </Box>
          )}
        </Box>
      ) : (
        <TestRunStatisticSkeleton />
      )}
    </>
  );
}
