import React from 'react';
import { Box } from '@mui/material';
import { Warning as WarningIcon } from '@mui/icons-material';
import Typography from '@mui/material/Typography';

const Warning = ({ warning }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        padding: '0.5rem',
        backgroundColor: 'secondary.main',
        alignItems: 'center',
      }}
    >
      <WarningIcon
        sx={{ marginRight: '0.5rem', color: 'rgba(0, 0, 0, 0.87)' }}
      />
      <Typography
        sx={{
          whiteSpace: 'pre-wrap',
          color: 'rgba(0, 0, 0, 0.87)',
          width: '100%',
        }}
      >
        {warning}
      </Typography>
    </Box>
  );
};

export const Warnings = ({ warnings }) => {
  return (
    <Box sx={{ paddingTop: '1rem' }}>
      {warnings.map((warning, index) => (
        <Warning key={index} warning={warning} />
      ))}
    </Box>
  );
};
