import React from 'react';
import DoneIcon from "@mui/icons-material/Done";
import CloseIcon from '@mui/icons-material/Close';
import {CircularProgress} from "@mui/material";


const TestStatusIcon = ({status}) => {
  const Icon = ({status}) => {
    switch (status) {
      case 'success':
        return <DoneIcon
          sx={{
            height: '20px',
            paddingRight: '6px',
            color: '#08ad6c'
          }}
        />;
      case 'fail':
        return <CloseIcon
          sx={{
            height: '20px',
            paddingRight: '6px',
            color: 'error.main'
          }}
        />;
      case 'pending':
        return <CircularProgress
          sx={{
            height: '20px !important',
            width: '20px !important',
            marginRight: '6px',
            color: 'primary.main'
          }}
        />;
      default:
        return (
          <DoneIcon
            sx={{
              height: '20px',
              paddingRight: '6px',
              color: '#08ad6c'
            }}
          />
        );
    }
  }


  return (
    <Icon status={status}/>
  );
};

export default TestStatusIcon;
