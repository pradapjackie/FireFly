import React, { useState } from 'react';
import Box from '@mui/material/Box';
import { Button } from '@mui/material';
import { actions, useEnvSliceSelector } from '../slice';
import { v4 as uuid } from 'uuid';
import { useDispatch } from 'react-redux';
import { EnvWarningPopup } from './WarningPopup';

const ActionButtonsM = ({ env, ids }) => {
    const dispatch = useDispatch();
    const [warningPopupOpen, setWarningPopupOpen] = useState(false);
    const [warningPopupData, setWarningPopupData] = useState({
        updated: [],
        deleted: [],
    });
    const entities = useEnvSliceSelector((state) => state?.entities[env]?.entities);

    function addRow() {
        dispatch(actions.addParam({ env: env, param: uuid() }));
    }

    function saveAll(confirmed = false) {
        setWarningPopupOpen(false);
        const newParams = [];
        const removedParams = [];
        const updatedParams = [];
        const overwriteEnv = {};
        ids.forEach((id) => {
            // Global
            const item = entities[id];
            if (item.isNew) {
                newParams.push({
                    env: env,
                    param: item.newName,
                    value: item.secure ? 'REPLACE_THIS' : item.value,
                    secure: item.secure,
                });
            } else if (item.toRemove) {
                removedParams.push(id);
            } else if (item.valueChanged) {
                updatedParams.push({
                    env: env,
                    param: id,
                    value: item.secure ? 'REPLACE_THIS' : item.value,
                    secure: item.secure,
                    initial: item.initial,
                });
            }
            // Local
            const newName = item.newName;
            const newId = newName ? newName : id;
            overwriteEnv[newId] = {
                value: item.overwrite,
                secure: item.secure,
            };
        });
        if (
            !confirmed &&
            !process.env.REACT_APP_TEST_DEV_MODE &&
            (updatedParams.length > 0 || removedParams.length > 0)
        ) {
            setWarningPopupData({
                updated: updatedParams,
                deleted: removedParams,
            });
            setWarningPopupOpen(true);
        } else {
            dispatch(
                actions.saveGlobalEnv({
                    env: env,
                    updatedEnv: {
                        new: newParams,
                        removed: removedParams,
                        updated: updatedParams,
                    },
                }),
            );
            dispatch(actions.saveLocalEnv({ env: env, overwriteEnv: overwriteEnv }));
        }
    }

    return (
        <>
            <Box>
                <Button sx={{ marginTop: '1rem' }} color="secondary" variant="outlined" onClick={addRow}>
                    + Add New Variable
                </Button>
            </Box>
            <Box>
                <Button
                    sx={{
                        marginTop: '1rem',
                        marginLeft: '1rem',
                        minWidth: '200px',
                        textTransform: 'uppercase',
                    }}
                    color="secondary"
                    variant="contained"
                    onClick={() => saveAll(false)}
                >
                    Save
                </Button>
            </Box>
            <EnvWarningPopup
                open={warningPopupOpen}
                setOpen={setWarningPopupOpen}
                save={() => saveAll(true)}
                data={warningPopupData}
            />
        </>
    );
};
export const ActionButtons = React.memo(ActionButtonsM);
