import React, { useEffect, useRef, useState } from 'react';
import { Icon, IconButton, TableCell, TableRow, Box, Checkbox } from '@mui/material';
import { EditableCell } from './EditableCell';
import { useDispatch } from 'react-redux';
import { actions, useEnvSliceSelector } from '../slice';

export const EnvTableRowT = ({ env, param, removeRow }) => {
    const dispatch = useDispatch();
    const [isEdit, setEdit] = useState(false);
    const { value, overwrite, secure, isNew, newName, toRemove } = useEnvSliceSelector(
        (state) => state?.entities[env].entities[param],
    );

    const bottomRef = useRef(null);

    useEffect(() => {
        if (isNew) {
            bottomRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [isNew]);

    function handleNewNameEdit(event) {
        dispatch(actions.editNewName({ env: env, param: param, newName: event.target.value }));
    }

    function handleValueEdit(valueName, value) {
        dispatch(actions.editValue({ env: env, param: param, valueName: valueName, value: value }));
    }

    function handleOverwriteEdit(e) {
        dispatch(actions.editOverwriteValue({ env: env, param: param, value: e.target.value }));
    }

    function handleRowRemove() {
        if (isNew && newName === '') {
            removeRow(param);
        } else {
            dispatch(actions.markRowToRemove({ env: env, param: param }));
        }
    }

    function handleRowRestore() {
        dispatch(actions.markRowToRestore({ env: env, param: param }));
    }

    return (
        <>
            <TableRow hover key={param} sx={[toRemove && { background: 'rgba(0, 0, 0, 0.15) !important' }]}>
                <EditableCell
                    value={isNew ? newName : param}
                    onChange={handleNewNameEdit}
                    isEdit={isNew}
                    sx={[
                        toRemove && { color: 'rgba(255, 255, 255, 0.54)' },
                        { paddingLeft: '1.25rem', paddingTop: 0, paddingBottom: 0 },
                    ]}
                    align="left"
                />
                <EditableCell
                    value={value}
                    onChange={(e) => handleValueEdit('value', e.target.value)}
                    isEdit={isNew || isEdit}
                    sx={[
                        toRemove && { color: 'rgba(255, 255, 255, 0.54)' },
                        { paddingLeft: 0, paddingRight: '1.25rem', paddingTop: 0, paddingBottom: 0 },
                    ]}
                    align="left"
                />
                <EditableCell
                    value={overwrite ? overwrite : ''}
                    onChange={handleOverwriteEdit}
                    isEdit={isNew || isEdit}
                    sx={[
                        toRemove && { color: 'rgba(255, 255, 255, 0.54)' },
                        { paddingLeft: 0, paddingRight: '1.25rem', paddingTop: 0, paddingBottom: 0 },
                    ]}
                    align="left"
                />
                <TableCell
                    sx={[
                        toRemove && { color: 'rgba(255, 255, 255, 0.54)' },
                        { paddingLeft: 0, paddingRight: '1.25rem', paddingTop: 0, paddingBottom: 0 },
                    ]}
                    align="center"
                >
                    <Checkbox
                        checked={secure}
                        color="secondary"
                        onChange={(e) => handleValueEdit('secure', e.target.checked)}
                        disabled={!(isNew || isEdit)}
                    />
                </TableCell>
                <TableCell
                    sx={{ paddingLeft: 0, paddingRight: '0.5rem', paddingTop: 0, paddingBottom: 0 }}
                    align="right"
                >
                    <Box sx={{ display: 'flex' }}>
                        <IconButton disabled={toRemove} onClick={() => setEdit(!isEdit)} size="large">
                            <Icon fontSize="small">edit</Icon>
                        </IconButton>
                        {toRemove ? (
                            <IconButton onClick={handleRowRestore} size="large">
                                <Icon fontSize="small">restore</Icon>
                            </IconButton>
                        ) : (
                            <IconButton onClick={handleRowRemove} size="large">
                                <Icon color="error" fontSize="small">
                                    clear
                                </Icon>
                            </IconButton>
                        )}
                    </Box>
                </TableCell>
            </TableRow>
            <tr>
                <td ref={bottomRef} />
            </tr>
        </>
    );
};
export const EnvTableRow = React.memo(EnvTableRowT);
