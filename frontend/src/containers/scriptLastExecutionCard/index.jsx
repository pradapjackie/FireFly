import React, { useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { useScriptLastExecutionCardSelector, useScriptLastExecutionCardSlice } from './slice';
import { LocalLoading } from 'components/Loading/LocalLoading';
import { Name } from './blocks/name';
import { ErrorSections } from './blocks/errors';
import { ScriptResult } from './blocks/result';
import { Log } from './blocks/log';
import { EnvUsed } from './blocks/envUsed';

export const ScriptLastExecutionCard = ({ scriptId }) => {
    const { actions } = useScriptLastExecutionCardSlice();
    const dispatch = useDispatch();
    const status = useScriptLastExecutionCardSelector(scriptId, (state) => state.status);
    const fetchStatus = useScriptLastExecutionCardSelector(scriptId, (state) => state.fetchStatus);
    const executionId = useScriptLastExecutionCardSelector(scriptId, (state) => state.executionId);
    const currentExecutionId = useRef(executionId);

    useEffect(() => {
        dispatch(actions.fetch({ scriptId }));
    }, [scriptId]);

    useEffect(() => {
        dispatch(actions.initWS());

        return function cleanup() {
            dispatch(actions.closeWS());
        };
    }, []);

    useEffect(() => {
        if (fetchStatus === 'success' && executionId && currentExecutionId.current !== executionId) {
            dispatch(actions.subscribe(executionId));
        }
        currentExecutionId.current = executionId;
    }, [fetchStatus, executionId]);

    if (fetchStatus !== 'success') return <LocalLoading />;

    return (
        <>
            <Name name={'Last script data'} status={status} />
            <ScriptResult scriptId={scriptId} />
            <ErrorSections scriptId={scriptId} />
            <Log status={status} scriptId={scriptId} />
            <EnvUsed scriptId={scriptId} />
        </>
    );
};
