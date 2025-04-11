import React from 'react';
import {Box, Button} from '@mui/material';
import {Link} from 'react-router-dom';

const NotFound = () => (
  <Box
    sx={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      width: '100%'
    }}
  >
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        maxWidth: '320px'
      }}
    >
      <Box
        component={"img"}
        sx={{marginBottom: '2rem', width: '100%'}}
        src="/assets/images/illustrations/404.svg"
        alt=""
      />
      <Link to="/">
        <Button sx={{textTransform: 'capitalize'}} variant="contained" color="primary">
          Back to Dashboard
        </Button>
      </Link>
    </Box>
  </Box>
);

export default NotFound;
