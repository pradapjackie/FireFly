import React from 'react';
import {Box} from "@mui/material";

const Dashboard = () => (
  <Box sx={{margin: {'xs': '14px', 'sm': '14px', 'md': '16px', 'lg': '30px', 'xl': '30px'}}}>
    <Box sx={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'
    }}
    >
      <Box component={"h3"} sx={{margin: 0}}>There will be a great dashboard here</Box>
    </Box>
  </Box>
);

export default Dashboard;
