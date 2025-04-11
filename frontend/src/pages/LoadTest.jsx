import { Card, Grid } from '@mui/material';
import React, { useCallback } from 'react';
import { LoadTestList } from 'containers/loadTestList';
import { useGetParams } from '../utils/hooks/useGetParameters';
import history from '../history';
import Scrollbar from 'react-perfect-scrollbar';
import { LoadTestRunCard } from '../containers/loadTestRunCard';
import { LoadTestLastExecutionCard } from '../containers/loadTestLastExecutionCard';

const LoadTestPage = ({
    match: {
        params: { folder },
    },
}) => {
    const search = useGetParams();
    const focusedId = search.get('loadTestId') || '';

    const setFocusedTest = useCallback((loadTestId) => {
        const params = new URLSearchParams({ loadTestId: loadTestId });
        history.replace({ pathname: history.location.pathname, search: params.toString() });
    }, []);

    return (
        <Grid container spacing={3}>
            <Grid item sm={3} xs={12}>
                <LoadTestList folder={folder} focusedId={focusedId} setFocusedTest={setFocusedTest} />
            </Grid>
            <Grid item sm={9} xs={12}>
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
                        {focusedId && <LoadTestRunCard folder={folder} loadTestId={focusedId} />}
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
                        {focusedId && <LoadTestLastExecutionCard loadTestId={focusedId} />}
                    </Card>
                </Scrollbar>
            </Grid>
        </Grid>
    );
};

export default LoadTestPage;
