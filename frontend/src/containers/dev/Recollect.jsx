import React from 'react';
import { CircularProgress, Fab, Icon, IconButton } from '@mui/material';
import { useDispatch } from 'react-redux';
import { useRootFolderFromLocation } from '../../utils/hooks/useRootFolderFromLocation';
import { useDevSlice, useDevSliceSelector } from './slice';
import { useModuleFromLocation } from '../../utils/hooks/useModuleFromLocation';

export const Recollect = () => {
    const { actions } = useDevSlice();
    const dispatch = useDispatch();
    const status = useDevSliceSelector((state) => state.status);
    const rootFolderFromLocation = useRootFolderFromLocation();
    const moduleFromLocation = useModuleFromLocation();
    const isLoading = status === 'loading';

    function handleClick() {
        dispatch(actions.reCollect({ folder: rootFolderFromLocation, module: moduleFromLocation }));
    }

    return (
        <>
            <Fab
                color="primary"
                component="span"
                size="medium"
                sx={{
                    boxShadow: 'none',
                    transition: 'all 250ms',
                    '&:hover': {
                        background: 'background.paper',
                        color: '#ffffff',
                        backgroundColor: 'background.paper',
                        fallbacks: [{ color: 'white !important' }],
                    },
                }}
                onClick={handleClick}
            >
                <IconButton size="medium" color="secondary">
                    <Icon>update</Icon>
                </IconButton>
                {isLoading && (
                    <CircularProgress size={48} sx={{ position: 'absolute', color: 'rgba(255, 255, 255, 0.87)' }} />
                )}
            </Fab>
        </>
    );
};
