import React from 'react';
import { useRunAutotestSliceSelector } from '../../slice';
import { AutoTestStatistic } from '../../../autoTestStatistic';
import { OneAutoTestStatistic } from '../../../oneAutoTestStatistic';

const TestHistory = ({ folder, selectedEnv }) => {
    const focusedTest = useRunAutotestSliceSelector(folder, (state) => state.focusedTest);

    return (
        <>
            {focusedTest ? (
                <OneAutoTestStatistic test_id={focusedTest} />
            ) : (
                <AutoTestStatistic folder={folder} env={selectedEnv} />
            )}
        </>
    );
};

export default TestHistory;
