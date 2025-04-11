import React from 'react';
import { RunAutotestWidget } from '../containers/runAutotest';

const RunAutotestPage = ({
    match: {
        params: { folder },
    },
}) => {
    return <RunAutotestWidget folder={folder} />;
};

export default RunAutotestPage;
