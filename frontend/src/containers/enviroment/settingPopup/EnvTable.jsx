import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableContainer } from '@mui/material';
import { useDispatch } from 'react-redux';
import { actions, useEnvSliceSelector } from '../slice';
import { EnvTableRow } from './TableRow';
import { EnvTableHead } from './TableHead';

const inString = (search, text) => {
    return text && text.toLowerCase().includes(search.toLowerCase());
};

export const EnvTableMemo = ({ ids, env }) => {
    const dispatch = useDispatch();
    const entities = useEnvSliceSelector((state) => state?.entities[env]?.entities);
    const [filteredIds, setFilteredIds] = useState(ids);

    function removeRow(param) {
        const newIds = filteredIds.filter((item) => item !== param);
        setFilteredIds(newIds);
        dispatch(actions.removeNewRow({ env: env, param: param }));
    }

    const [paramFilter, setParamFilter] = useState('');
    const [valueFilter, setValueFilter] = useState('');
    const [overwriteFilter, setOverwriteFilter] = useState('');
    const [secureFilter, setSecureFilter] = useState('All');

    useEffect(() => {
        if (ids) {
            const idsToShow = [];
            for (let id of ids) {
                const item = entities[id];
                if (entities[id].isNew) {
                    idsToShow.push(id);
                    continue;
                }
                if (paramFilter && !inString(paramFilter, id)) continue;
                if (valueFilter && !inString(valueFilter, item.value)) continue;
                if (overwriteFilter && !inString(overwriteFilter, item.overwrite)) continue;
                if (secureFilter !== 'All' && item.secure !== (secureFilter === 'True')) continue;
                idsToShow.push(id);
            }
            setFilteredIds(idsToShow);
        }
    }, [ids, paramFilter, valueFilter, overwriteFilter, secureFilter]);

    return (
        <TableContainer>
            <Table stickyHeader size="small">
                <EnvTableHead
                    paramFilter={paramFilter}
                    setParamFilter={setParamFilter}
                    valueFilter={valueFilter}
                    setValueFilter={setValueFilter}
                    overwriteFilter={overwriteFilter}
                    setOverwriteFilter={setOverwriteFilter}
                    secureFilter={secureFilter}
                    setSecureFilter={setSecureFilter}
                />
                {filteredIds && (
                    <TableBody>
                        {filteredIds.map((id, ind) => (
                            <EnvTableRow key={ind} env={env} param={id} removeRow={removeRow} />
                        ))}
                    </TableBody>
                )}
            </Table>
        </TableContainer>
    );
};
export const EnvTable = React.memo(EnvTableMemo);
