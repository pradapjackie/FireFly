import React from 'react';
import {Divider, InputAdornment, TableCell, TextField} from "@mui/material";
import FilterListIcon from "@mui/icons-material/FilterList";

const CellWithFilterM = ({title, value, onChange, children, select, ...cellParams}) => {
  return (
    <TableCell {...cellParams}>
      <>{title}</>
      <Divider/>
      <TextField
        variant="standard"
        select={select}
        sx={{width: '100%'}}
        color="secondary"
        value={value}
        onChange={onChange}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <FilterListIcon/>
            </InputAdornment>
          ),
        }}
      >
        {children}
      </TextField>
    </TableCell>
  )
};

export const CellWithFilter = React.memo(CellWithFilterM);
