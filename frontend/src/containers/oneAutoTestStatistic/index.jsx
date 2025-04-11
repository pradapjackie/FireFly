import React, { useEffect } from 'react';
import {
  Card,
  Fade,
  Table,
  TableBody,
  TableRow,
  TableCell,
  Box,
} from '@mui/material';
import { PieChart } from 'components/PieChart';
import { format } from 'date-fns';
import { useTheme } from '@mui/styles';
import {
  useOneAutoTestStatisticSlice,
  useOneAutoTestStatisticSliceSelector,
} from './slice';
import { useDispatch } from 'react-redux';
import {SmallStatusChip} from "components/StatusChip";

export function OneAutoTestStatistic({ test_id }) {
  const { actions } = useOneAutoTestStatisticSlice();
  const { palette } = useTheme();
  const dispatch = useDispatch();

  const { status, fullName, resultByStatus, statistic } =
    useOneAutoTestStatisticSliceSelector((state) => state);
  const isSuccess = status === 'success';

  useEffect(() => {
    dispatch(actions.fetch({ test_id }));
  }, [test_id]);

  return (
    <Fade in timeout={100}>
      <Card
        sx={{
          paddingLeft: '1.5rem',
          paddingRight: '1.5rem',
          paddingTop: '1rem',
          paddingBottom: '1rem',
          marginBottom: '1.5rem',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
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
          {fullName}
        </Box>
        {isSuccess ? (
          <PieChart
            height="300px"
            color={[
              palette.success.main,
              palette.text.secondary,
              palette.error.main,
            ]}
            data={resultByStatus}
          />
        ) : (
          <></>
        )}
        {isSuccess ? (
          <Table size={'small'}>
            <TableBody>
              {statistic.map((autoTest, index) => (
                <TableRow key={index}>
                  <TableCell align="left" sx={{ padding: 0 }}>
                    {format(new Date(autoTest.date), 'dd.MM.yyyy HH:mm')}
                  </TableCell>
                  <TableCell
                    sx={{ padding: 0, textTransform: 'capitalize' }}
                    align="right"
                  >
                    <SmallStatusChip status={autoTest.status}/>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <></>
        )}
      </Card>
    </Fade>
  );
}
