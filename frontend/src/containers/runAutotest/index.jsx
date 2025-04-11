import React, { useEffect } from 'react';
import { ClickAwayListener, Grid } from '@mui/material';
import { TestRunCarousel } from '../testRunCarousel/testRunCarousel';
import { useRunAutotestSlice, useRunAutotestSliceSelector } from './slice';
import { useDispatch } from 'react-redux';
import { RunAutotestButtons } from './sections/runAutotestButtons';
import { SelectTestsTree } from './sections/selectTestsTree';
import { useSelectedEnvName } from '../enviroment/slice';
import TestHistory from './sections/testHistory';

export const RunAutotestWidget = ({ folder }) => {
    const { actions } = useRunAutotestSlice();
    const dispatch = useDispatch();
    const selectedEnv = useSelectedEnvName();
    const status = useRunAutotestSliceSelector(folder, (state) => state.status);
    const isSuccess = status === 'success';

    const testUnfocused = () => {
        dispatch(actions.testFocused({ testId: '', folder: folder }));
    };

    useEffect(() => {
        if (!isSuccess) {
            dispatch(actions.fetch({ folder: folder }));
        }
    }, [folder, isSuccess]);

    return (
        <ClickAwayListener onClickAway={testUnfocused}>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <TestRunCarousel folder={folder} />
                </Grid>

                <Grid item sm={8} xs={12}>
                    {isSuccess ? (
                        <>
                            <RunAutotestButtons folder={folder} selectedEnv={selectedEnv} />
                            <SelectTestsTree folder={folder} />
                        </>
                    ) : (
                        <></>
                    )}
                </Grid>

                <Grid item sm={4} xs={12}>
                    <TestHistory folder={folder} selectedEnv={selectedEnv} />
                </Grid>
            </Grid>
        </ClickAwayListener>
    );
};
