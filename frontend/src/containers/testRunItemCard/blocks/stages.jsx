import React from 'react';
import { Box, Typography } from '@mui/material';
import { CustomTreeView } from 'components/TreeView';

const Stage = ({ stageName, stage }) => {
  return (
    <CustomTreeView
      key={stageName}
      steps={[{ name: stageName, status: stage.status, inner: stage.steps_data }]}
    />
  );
};

export const Stages = ({ stages }) => {
  return (
    <Box sx={{ paddingTop: '1rem' }}>
      <Typography
        sx={{ paddingBottom: '0.5rem', fontWeight: '700' }}
        variant={'subtitle1'}
      >
        Stages:
      </Typography>
      {Object.entries(stages).map(([stageName, stage]) => (
        <Stage key={stageName} stageName={stageName} stage={stage} />
      ))}
    </Box>
  );
};
