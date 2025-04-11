import React from 'react';
import { Skeleton } from '@mui/material';
import Box from '@mui/material/Box';

export const TestResultTreeSkeleton = () => {
  const stepLeft = [1, 2, 3, 4];
  const randomSteps = Array.from(
    { length: 11 },
    () => stepLeft[Math.floor(Math.random() * stepLeft.length)],
  );
  const skeletonsEls = randomSteps.map((el, idx) => (
    <Skeleton
      animation="wave"
      variant="rectangular"
      height="20px"
      key={idx}
      width={`calc(100% - ${16 * el}px)`}
      sx={{
        marginBottom: '16px',
        borderRadius: '5px',
        marginLeft: `${16 * el}px`,
        marginRight: '16px',
      }}
    />
  ));
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        flexWrap: 'wrap',
        alignItems: 'flex-start',
        paddingRight: '20px',
      }}
    >
      <Skeleton
        animation="wave"
        variant="rectangular"
        height="20px"
        width="calc(100% - 16px)"
        sx={{
          marginBottom: '16px',
          borderRadius: '5px',
          marginLeft: '16px',
          marginRight: '16px',
        }}
      />
      {skeletonsEls}
    </Box>
  );
};
