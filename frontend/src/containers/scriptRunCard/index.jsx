import React, { useCallback, useEffect } from 'react';
import Box from '@mui/material/Box';
import { Description } from './blocks/description';
import { Name } from './blocks/name';
import { ViewHistoryButton } from './blocks/viewHistoryButton';
import { InputParams } from './blocks/inputParams';
import { RunScriptButton } from './blocks/runButton';
import { useDispatch } from 'react-redux';
import { useScriptRunCardSelector, useScriptRunCardSlice } from './slice';
import { LocalLoading } from 'components/Loading/LocalLoading';

export const ScriptRunCard = ({ folder, scriptId, switchToHistory }) => {
    const { actions } = useScriptRunCardSlice();
    const dispatch = useDispatch();
    const { fetchStatus, ...script } = useScriptRunCardSelector(scriptId);

    useEffect(() => {
        dispatch(actions.fetch({ scriptId }));
    }, [scriptId]);

    const setResultConfig = useCallback(
        (paramName, paramValue) => {
            dispatch(actions.setScriptParamValue({ scriptId, paramName, paramValue }));
        },
        [scriptId],
    );

    if (fetchStatus !== 'success') return <LocalLoading />;

    return (
        <>
            <Box
                sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                }}
            >
                <Name name={script.displayName} />
                <ViewHistoryButton switchToHistory={switchToHistory} />
            </Box>
            <Description description={script.description} />
            <InputParams
                paramsConfig={script.params}
                paramsState={script.parametersValues}
                setParamsState={setResultConfig}
            />
            <RunScriptButton
                folder={folder}
                scriptId={scriptId}
                params={script.parametersValues}
                paramsConfig={script.params}
            />
        </>
    );
};
