import React from 'react';
import { Box } from '@mui/material';

const TestInfoIcons = ({ resultByStatus }) => {
  const spacingStyle = {
    borderRadius: '4px !important',
    paddingLeft: '0.5rem',
    paddingRight: '0.5rem',
    paddingTop: '2px',
    paddingBottom: '2px',
    marginRight: '2px',
    marginLeft: '2px',
  };

  const StatusChips = ({ resultByStatus: { success, pending, fail } }) => {
    return (
      <>
        {success !== 0 && (
          <Box
            component={'small'}
            sx={{
              color: '#08ad6c',
              backgroundColor: 'rgba(8, 173, 108,.1)',
              borderColor: '#08ad6c',
              ...spacingStyle,
            }}
          >
            {success}
          </Box>
        )}
        {pending !== 0 && (
          <Box
            component={'small'}
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              borderColor: 'rgba(255, 255, 255, 0.7)',
              ...spacingStyle,
            }}
          >
            {pending}
          </Box>
        )}
        {fail !== 0 && (
          <Box
            component={'small'}
            sx={{
              color: '#ec412c',
              backgroundColor: 'rgba(236,65,44,.1)',
              borderColor: '#ec412c',
              ...spacingStyle,
            }}
          >
            {fail}
          </Box>
        )}
      </>
    );
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'row',
      }}
    >
      {resultByStatus && <StatusChips resultByStatus={resultByStatus} />}
    </Box>
  );
};

export default TestInfoIcons;
