import React from 'react';
import { Box } from '@mui/material';
import TestStatusIcon from 'components/TestStatusIcon';
import Typography from '@mui/material/Typography';
import { useTestRunTreeSelector } from '../../slice';

export const ItemContent = ({ itemId, testRunId }) => {
  const name = useTestRunTreeSelector(testRunId, state => state.items[itemId].name)
  const status = useTestRunTreeSelector(testRunId, state => state.items[itemId].status)

  return (
    <>
      <Box sx={{ display: 'flex' }}>
        <TestStatusIcon status={status} />
        <Typography variant="body1">{name}</Typography>
      </Box>
    </>
  );
};
