import React, { useCallback, useState } from 'react';
import { Box, IconButton } from '@mui/material';
import { actions, useRunAutotestSliceSelector } from '../../slice';
import { useSelectedEnv } from 'containers/enviroment/slice';
import { useDispatch } from 'react-redux';
import { createDeepEqualSelector } from 'utils/reselect-helpers';
import { Tune } from '@mui/icons-material';
import { RunConfigPopup } from './RunConfigPopup';
import { isEmpty, isEqual } from 'lodash';
import { RunButton } from 'components/RunButton';

export const selectedTests = createDeepEqualSelector([(state) => Object.values(state.items.entities)], (tests) =>
    tests.filter((test) => test.selected),
);

export const selectedTestIds = createDeepEqualSelector([selectedTests], (tests) => tests.map((test) => test.id));

export const requiredRunConfig = createDeepEqualSelector([selectedTests], (tests) => {
    const requiredRunConfig = tests.map((test) => test.requiredRunConfig);
    let mergedRequiredRunConfig = {};
    !isEmpty(requiredRunConfig) && Object.assign(mergedRequiredRunConfig, ...requiredRunConfig);
    return mergedRequiredRunConfig;
});

const ConfigButton = React.memo(
    ({ setOpen, mergedRequiredRunConfig }) => {
        return (
            <IconButton
                size="medium"
                color="secondary"
                disabled={isEmpty(mergedRequiredRunConfig)}
                onClick={() => setOpen(true)}
                sx={{ marginTop: '-12px', marginBottom: '-12px', marginRight: '-12px' }}
            >
                <Tune fontSize="large" />
            </IconButton>
        );
    },
    (prevProps, nextProps) => isEqual(prevProps.mergedRequiredRunConfig, nextProps.mergedRequiredRunConfig),
);

export const RunAutotestButtons = ({ folder, selectedEnv }) => {
    const dispatch = useDispatch();
    const envData = useSelectedEnv();
    const testIds = useRunAutotestSliceSelector(folder, (state) => selectedTestIds(state));
    const mergedRequiredRunConfig = useRunAutotestSliceSelector(folder, (state) => requiredRunConfig(state));
    const runConfig = useRunAutotestSliceSelector(folder, (state) => state.runConfig);

    const [isOpen, setOpen] = useState(false);

    const runAutotest = useCallback(() => {
        dispatch(actions.run({ folder, testIds, selectedEnv, envData, runConfig }));
    }, [folder, testIds, selectedEnv, envData, runConfig]);

    const setRunConfig = useCallback(
        (name, value) => {
            dispatch(actions.setRunConfig({ name, value, folder }));
        },
        [folder],
    );

    const fetchDynamicData = useCallback(
        (alias, callbackUrl) => {
            dispatch(actions.fetchDynamicData({ alias, callbackUrl, folder }));
        },
        [folder],
    );

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
            <RunButton
                text={'Run selected tests: '.toUpperCase() + testIds.length}
                isDisabled={testIds.length === 0}
                runCallback={runAutotest}
            />
            <ConfigButton setOpen={setOpen} mergedRequiredRunConfig={mergedRequiredRunConfig} />
            <RunConfigPopup
                isOpen={isOpen}
                setOpen={setOpen}
                requiredRunConfig={mergedRequiredRunConfig}
                runConfig={runConfig}
                setRunConfig={setRunConfig}
                fetchDynamicData={fetchDynamicData}
            />
        </Box>
    );
};
