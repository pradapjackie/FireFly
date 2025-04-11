import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import {Box} from "@mui/material";


export const LocalLoading = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        width: '100%',
        justifyContent: 'center',
        margin: '0.5rem'
      }}
    >
      <CircularProgress/>
    </Box>
  );
};
