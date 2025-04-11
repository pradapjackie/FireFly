import React from 'react';
import {Box} from "@mui/material";
import Typography from "@mui/material/Typography";


export const Description = ({description}) => {

  return (
    <Box sx={{paddingTop: '1rem'}}>
      <Typography sx={{paddingBottom: '0.5rem', fontWeight: '700'}} variant={'subtitle1'}>
        Description:
      </Typography>
      <Typography sx={{whiteSpace: 'pre-wrap', padding: '0.5rem', background: 'rgba(var(--primary), 0.15)'}}>
        {description}
      </Typography>
    </Box>
  );
};
