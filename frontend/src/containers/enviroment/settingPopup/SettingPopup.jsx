import React, { useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Paper, CircularProgress, Box } from '@mui/material';
import { useDispatch } from 'react-redux';
import { actions, useEnvSliceSelector } from '../slice';
import { ActionButtons } from './ActionButtons';
import { EnvTable } from './EnvTable';

export const SettingPopupT = ({ open, setOpen, env }) => {
    const dispatch = useDispatch();
    const status = useEnvSliceSelector((state) => state?.entities[env].status);
    const ids = useEnvSliceSelector((state) => state?.entities[env].ids);

    useEffect(() => {
        dispatch(actions.fetchByEnv({ env: env }));
    }, [env]);

    return (
        <Dialog
            open={open}
            sx={{ '& .MuiDialog-paper': { height: '100%' } }}
            onClose={() => setOpen(false)}
            maxWidth="xl"
            fullWidth={true}
        >
            <DialogTitle>{`${env} environment settings`}</DialogTitle>
            <DialogContent sx={{ paddingBottom: '0px' }}>
                {status === 'success' ? (
                    <Paper sx={{ width: '100%' }}>
                        <EnvTable ids={ids} env={env} />
                    </Paper>
                ) : (
                    <Box
                        sx={{
                            width: '100%',
                            height: '100%',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                        }}
                    >
                        <CircularProgress color="secondary" />
                    </Box>
                )}
            </DialogContent>
            <DialogActions sx={{ paddingLeft: '1.5rem', paddingRight: '1.5rem', justifyContent: 'space-between' }}>
                <ActionButtons env={env} ids={ids} />
            </DialogActions>
        </Dialog>
    );
};
export const SettingPopup = React.memo(SettingPopupT);
