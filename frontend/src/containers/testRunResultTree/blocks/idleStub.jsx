import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import RefreshIcon from '@mui/icons-material/Refresh';
import { Button } from '@mui/material';

export const IdleStub = () => {
  const refreshPage = () => {
    window.location.reload();
  };

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
        FireFly imports tests and prepares a report...
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        Try refreshing the page in a couple of seconds.
      </Typography>
      <Button
        sx={{alignSelf: "center"}}
        onClick={refreshPage}
        variant="contained"
        endIcon={<RefreshIcon />}
      >
        Refresh page
      </Button>
    </Box>
  );
};
