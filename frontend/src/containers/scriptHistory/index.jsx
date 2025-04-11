import React, { useEffect } from 'react';
import Scrollbar from 'react-perfect-scrollbar';
import { ListHistoryCard } from './blocks/historyCard';
import { Card, Box } from '@mui/material';
import { Name } from './blocks/name';
import { ReturnToScriptButton } from './blocks/returnToScriptButton';
import { useScriptHistorySelector, useScriptHistorySlice } from './slice';
import { useDispatch } from 'react-redux';
import { LocalLoading } from 'components/Loading/LocalLoading';

export const ScriptHistoryList = ({ scriptId, switchToScript }) => {
    const { actions } = useScriptHistorySlice();
    const dispatch = useDispatch();
    const { fetchStatus, scriptName, history } = useScriptHistorySelector(scriptId);

    useEffect(() => {
        dispatch(actions.fetch({ scriptId }));
    }, [scriptId]);

    if (fetchStatus !== 'success') return <LocalLoading />;

    return (
        <Card
            sx={{
                paddingLeft: '1.5rem',
                paddingRight: '1.5rem',
                paddingTop: '1rem',
                paddingBottom: '1rem',
                display: 'flex',
                flexDirection: 'column',
                maxHeight: 'calc(100vh - 140px)',
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                }}
            >
                <Name name={scriptName} />
                <ReturnToScriptButton switchToScript={switchToScript} />
            </Box>
            <Scrollbar style={{ position: 'relative', marginTop: '1rem' }}>
                <Card
                    sx={{
                        paddingLeft: '1rem',
                        paddingRight: '1rem',
                        paddingTop: '1rem',
                        backgroundColor: 'background.default',
                    }}
                >
                    {history &&
                        history.map((historyItem, index) => <ListHistoryCard key={index} historyItem={historyItem} />)}
                </Card>
            </Scrollbar>
        </Card>
    );
};
