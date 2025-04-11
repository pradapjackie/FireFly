import React from 'react';
import {Box} from "@mui/material";


export const VerticalNavLabel = ({sidebarMode, label}) => {
  return sidebarMode === 'compact' ? (
    <Box
      component={"p"}
      sx={{
        paddingLeft: '1rem',
        paddingRight: '1rem',
        marginBottom: '0.5rem',
        marginTom: '1.5rem',
        textTransform: 'uppercase',
        fontSize: '12px',
        display: 'none',
      }}
      className="sidenavHoverShow"
    >
      {label}
    </Box>
  ) : (
    <Box
      component={"p"}
      sx={{
        paddingLeft: '1rem',
        paddingRight: '1rem',
        marginBottom: '0.5rem',
        marginTom: '1.5rem',
        textTransform: 'uppercase',
        fontSize: '12px',
        color: 'text.secondary'
      }}
    >
      {label}
    </Box>
  );
};
