import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TestInfoIcons from 'components/TestInfoIcons';
import { useTestRunTreeSelector } from '../../slice';

export const GroupContent = ({ groupId, testRunId }) => {
  const name = useTestRunTreeSelector(testRunId, state => state.groups[groupId].name)
  const resultByStatus = useTestRunTreeSelector(testRunId, state => state.groups[groupId].resultByStatus)

  return (
    <>
      <Box>
        <Typography variant="body1">{name}</Typography>
      </Box>
      <TestInfoIcons resultByStatus={resultByStatus} />
    </>
  );
};
