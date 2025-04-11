import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export const FailedStub = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        flexWrap: 'wrap',
        alignItems: 'flex-start',
        padding: '20px',
      }}
    >
      <Typography variant="subtitle1" color="textSecondary">
        Test run failed outside of auto tests scope.
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        Address test run error for details.
      </Typography>
    </Box>
  );
};
