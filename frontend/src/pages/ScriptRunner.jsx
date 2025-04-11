import React, { useCallback, useState } from 'react';
import { Card, Grid } from '@mui/material';
import Box from '@mui/material/Box';
import { ScriptRunnerList } from '../containers/scriptRunnerList';
import { ScriptRunCard } from '../containers/scriptRunCard';
import Scrollbar from 'react-perfect-scrollbar';
import { ScriptLastExecutionCard } from '../containers/scriptLastExecutionCard';
import { ScriptHistoryList } from '../containers/scriptHistory';
import history from '../history';
import {useGetParams} from "../utils/hooks/useGetParameters";

const ScriptRunnerPage = ({
    match: {
        params: { folder },
    },
}) => {
    const search = useGetParams();
    const focusedId = search.get("scriptId") || ""
    const [viewHistory, setViewHistory] = useState(false);

    const setFocusedScript = useCallback((scriptId) => {
        const params = new URLSearchParams({ scriptId: scriptId });
        history.replace({ pathname: history.location.pathname, search: params.toString() });
    }, []);

    const switchToHistory = useCallback(() => {
        setViewHistory(true);
    }, []);

    const switchToScript = useCallback(() => {
        setViewHistory(false);
    }, []);

    return (
        <Grid container spacing={3}>
            <Grid item sm={3} xs={12}>
                <Box>
                    <ScriptRunnerList folder={folder} focusedId={focusedId} setFocusedScript={setFocusedScript} />
                </Box>
            </Grid>
            <Grid item sm={9} xs={12}>
                {viewHistory ? (
                    <ScriptHistoryList scriptId={focusedId} switchToScript={switchToScript} />
                ) : (
                    <Scrollbar style={{ maxHeight: 'calc(100vh - 140px)', position: 'relative' }}>
                        <Card
                            sx={{
                                paddingLeft: '1.5rem',
                                paddingRight: '1.5rem',
                                paddingTop: '1rem',
                                paddingBottom: '1rem',
                                marginBottom: '20px',
                                display: 'flex',
                                flexDirection: 'column',
                            }}
                        >
                            {focusedId && (
                                <ScriptRunCard folder={folder} scriptId={focusedId} switchToHistory={switchToHistory} />
                            )}
                        </Card>
                        <Card
                            sx={{
                                paddingLeft: '1.5rem',
                                paddingRight: '1.5rem',
                                paddingTop: '1rem',
                                paddingBottom: '1rem',
                                display: 'flex',
                                flexDirection: 'column',
                                minHeight: 'calc(50vh)',
                            }}
                        >
                            {focusedId && <ScriptLastExecutionCard scriptId={focusedId} />}
                        </Card>
                    </Scrollbar>
                )}
            </Grid>
        </Grid>
    );
};

export default ScriptRunnerPage;
