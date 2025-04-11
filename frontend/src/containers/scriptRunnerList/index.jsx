import React, { useEffect, useState } from 'react';
import Scrollbar from 'react-perfect-scrollbar';
import { useScriptRunnerListSelector, useScriptRunnerListSlice } from './slice';
import { useDispatch } from 'react-redux';
import { ScriptListSkeleton } from './skeleton';
import { ListScriptCard } from './blocks/listScriptCard';
import { ScriptSearch } from './blocks/search';

const inString = (searchArray, text) => {
    return text && searchArray.some((v) => text.toLowerCase().includes(v.toLowerCase()));
};

export const ScriptRunnerList = ({ folder, focusedId, setFocusedScript }) => {
    const { actions } = useScriptRunnerListSlice();
    const dispatch = useDispatch();
    const { status, scriptList } = useScriptRunnerListSelector(folder, (state) => state);
    const isSuccess = status === 'success';

    const [search, setSearch] = useState('');
    const [filteredScripts, setFilteredScripts] = useState(scriptList);

    useEffect(() => {
        if (!isSuccess) {
            dispatch(actions.fetch({ folder: folder }));
        }
    }, [folder, isSuccess]);

    useEffect(() => {
        let scriptsToShow = [];
        if (!search) {
            scriptsToShow = scriptList;
        } else {
            let searchArray = search.split('|');
            for (let script of scriptList) {
                if (inString(searchArray, script.displayName) || inString(searchArray, script.description)) {
                    scriptsToShow.push(script);
                }
            }
        }
        setFilteredScripts(scriptsToShow);
    }, [scriptList, search]);

    return (
        <>
            <ScriptSearch search={search} setSearch={setSearch} disabled={!isSuccess} />

            <Scrollbar style={{ maxHeight: 'calc(100vh - 185px)', position: 'relative' }}>
                {!isSuccess ? (
                    <ScriptListSkeleton />
                ) : (
                    <>
                        {filteredScripts.map((script) => (
                            <ListScriptCard
                                key={script.id}
                                scriptId={script.id}
                                name={script.displayName}
                                description={script.description}
                                isFocused={focusedId === script.id}
                                setFocused={setFocusedScript}
                            />
                        ))}
                    </>
                )}
            </Scrollbar>
        </>
    );
};
