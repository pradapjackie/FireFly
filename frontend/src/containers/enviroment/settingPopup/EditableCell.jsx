import React from 'react';
import {TableCell, TextField} from "@mui/material";

export const EditableCell = ({value, isEdit, setEnvironment, onChange, select, children, ...cellParams}) => {

  return (
    <TableCell {...cellParams}>
      {
        isEdit ?
          <TextField
            variant="standard"
            select={select}
            sx={{width: '100%'}}
            color="secondary"
            value={value}
            onChange={onChange}
          >
            {children}
          </TextField> : <>{value}</>
      }
    </TableCell>
  )
};
