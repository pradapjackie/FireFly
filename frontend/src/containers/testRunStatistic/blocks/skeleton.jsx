import { Skeleton } from '@mui/material';
import Box from '@mui/material/Box';
import React from 'react';

export const TestRunStatisticSkeleton = () => {
  return (
    <>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: '50px'
        }}
      >
        <Skeleton
          animation="wave"
          variant="circular"
          height="250px"
          width="250px"
        />
      </Box>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {Array(5).fill(1).map((_, id) => (
          <Skeleton
            key={id}
            animation="wave"
            variant="rectangular"
            height="40px"
            width="100%"
            sx={{ margin: '3px', borderRadius: '5px' }}
          />
        ))}
      </Box>
    </>
  );
};
