import React from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { isEmpty } from 'lodash';

export const MultiTableMemo = ({ data, stringify = true }) => {
    if (isEmpty(data)) {
        return <></>;
    }

    const header = Object.keys(data[0]);

    return (
        <Table size="small">
            <TableHead>
                <TableRow>
                    {header.map((label, index) => (
                        <TableCell sx={{ textTransform: 'capitalize', fontWeight: '900' }} key={index}>
                            {label}
                        </TableCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody>
                {data.map((row, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                        {Object.values(row).map((value, index) => (
                            <TableCell key={index}>{stringify ? JSON.stringify(value) : value}</TableCell>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    );
};

export const MultiTable = React.memo(MultiTableMemo);
