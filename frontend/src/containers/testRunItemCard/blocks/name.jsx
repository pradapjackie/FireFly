import React from 'react';
import {Box} from "@mui/material";
import Typography from "@mui/material/Typography";
import {StatusChip} from "components/StatusChip";


export const Name = ({status, name}) => {

  return (
    <Box sx={{display: 'flex', borderRadius: '4px'}}>
      <StatusChip status={status}/>
      <Typography variant="h6" color="textSecondary">
        {name}
      </Typography>
    </Box>
  );
};
