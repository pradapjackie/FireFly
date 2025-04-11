import React, { useEffect, useState } from 'react';
import Scrollbar from 'react-perfect-scrollbar';
import { useLoadTestListSlice, useLoadTestListSelector } from './slice';
import { useDispatch } from 'react-redux';
import { LoadTestListSkeleton } from './skeleton';
import { LoadTestCard } from './blocks/loadTestCard';
import { LoadTestSearch } from './blocks/search';

const inString = (searchArray, text) => {
    return text && searchArray.some((v) => text.toLowerCase().includes(v.toLowerCase()));
};

export const LoadTestList = ({ folder, focusedId, setFocusedTest }) => {
    const { actions } = useLoadTestListSlice();
    const dispatch = useDispatch();
    const { status, loadTestList } = useLoadTestListSelector(folder, (state) => state);
    const isSuccess = status === 'success';

    const [search, setSearch] = useState('');
    const [filteredTests, setFilteredTests] = useState(loadTestList);

    useEffect(() => {
        if (!isSuccess) {
            dispatch(actions.fetch({ folder: folder }));
        }
    }, [folder, isSuccess]);

    useEffect(() => {
        let testToShow = [];
        if (!search) {
            testToShow = loadTestList;
        } else {
            let searchArray = search.split('|');
            for (let test of loadTestList) {
                if (inString(searchArray, test.displayName) || inString(searchArray, test.description)) {
                    testToShow.push(test);
                }
            }
        }
        setFilteredTests(testToShow);
    }, [loadTestList, search]);

    return (
        <>
            <LoadTestSearch search={search} setSearch={setSearch} disabled={!isSuccess} />

            <Scrollbar style={{ maxHeight: 'calc(100vh - 185px)', position: 'relative' }}>
                {!isSuccess ? (
                    <LoadTestListSkeleton />
                ) : (
                    <>
                        {filteredTests.map((test) => (
                            <LoadTestCard
                                key={test.id}
                                loadTestId={test.id}
                                name={test.displayName}
                                description={test.description}
                                isFocused={focusedId === test.id}
                                setFocused={setFocusedTest}
                            />
                        ))}
                    </>
                )}
            </Scrollbar>
        </>
    );
};
