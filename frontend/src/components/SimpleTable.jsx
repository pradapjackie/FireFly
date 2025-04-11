import React from 'react';
import { Table, TableBody, TableCell, TableRow } from '@mui/material';
import { isEmpty } from 'lodash';

export const SimpleTableMemo = ({ data, stringify = true, firstRowSx = {} }) => {
    if (isEmpty(data)) return;

    return (
        <Table size="small">
            <TableBody>
                {Object.keys(data).map((param_name, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                        <TableCell sx={{ padding: 0, ...firstRowSx }}>{param_name}</TableCell>
                        <TableCell>{stringify ? JSON.stringify(data[param_name]) : data[param_name]}</TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    );
};

export const SimpleTable = React.memo(SimpleTableMemo);
