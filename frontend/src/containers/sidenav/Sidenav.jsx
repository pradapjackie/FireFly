import React, { useEffect } from 'react';
import Scrollbar from 'react-perfect-scrollbar';
import { VerticalNav } from './VerticalNav/VerticalNav';
import { Box } from '@mui/material';
import {useMenuSlice} from './slice';
import { useDispatch } from 'react-redux';

const Sidenav = ({ sidebarMode, setSidebarMode, children }) => {
    const { actions } = useMenuSlice();
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(actions.startMenuLoad());
    }, []);

    return (
        <>
            <Scrollbar
                options={{ suppressScrollX: true }}
                style={{
                    position: 'relative',
                    paddingLeft: '1rem',
                    paddingRight: '1rem',
                }}
            >
                {children}
                <VerticalNav sidebarMode={sidebarMode} />
            </Scrollbar>

            <Box
                onClick={() => setSidebarMode('close')}
                sx={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    width: '100vw',
                    background: 'rgba(0, 0, 0, 0.54)',
                    zIndex: -1,
                    display: { lg: 'none', xl: 'none' },
                }}
            />
        </>
    );
};

export default Sidenav;
