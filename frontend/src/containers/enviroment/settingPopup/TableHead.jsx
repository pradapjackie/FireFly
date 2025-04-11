import React from 'react';
import { MenuItem, TableCell, TableHead, TableRow } from '@mui/material';
import { CellWithFilter } from './CellWithFilter';

export const EnvTableHeadT = ({
    paramFilter,
    setParamFilter,
    valueFilter,
    setValueFilter,
    overwriteFilter,
    setOverwriteFilter,
    secureFilter,
    setSecureFilter,
}) => {
    return (
        <TableHead>
            <TableRow>
                <CellWithFilter
                    title="Param"
                    value={paramFilter}
                    onChange={(e) => {
                        setParamFilter(e.target.value);
                    }}
                    sx={{ paddingLeft: '1.25rem', paddingRight: '1.25rem', width: '28%' }}
                />
                <CellWithFilter
                    title="Default"
                    value={valueFilter}
                    onChange={(e) => {
                        setValueFilter(e.target.value);
                    }}
                    sx={{ paddingRight: '1.25rem', paddingLeft: 0, width: '27%' }}
                />
                <CellWithFilter
                    title="Current"
                    value={overwriteFilter}
                    onChange={(e) => {
                        setOverwriteFilter(e.target.value);
                    }}
                    sx={{ paddingRight: '1.25rem', paddingLeft: 0, width: '27%' }}
                />
                <CellWithFilter
                    select={true}
                    title="Secure"
                    value={secureFilter}
                    onChange={(e) => setSecureFilter(e.target.value)}
                    sx={{ paddingRight: '1.25rem', paddingLeft: 0, width: '10%' }}
                >
                    {['All', 'True', 'False'].map((item) => (
                        <MenuItem value={item} key={item}>
                            {item}
                        </MenuItem>
                    ))}
                </CellWithFilter>
                <TableCell cx={{ paddingLeft: 0, paddingRight: 0, width: '9%' }} />
            </TableRow>
        </TableHead>
    );
};
export const EnvTableHead = React.memo(EnvTableHeadT);
