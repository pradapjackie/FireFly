import React from 'react';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { SimpleTable } from 'components/SimpleTable';
import { MultiTable } from 'components/MultiTable';
import { SimpleAccordion } from 'components/SimpleAccordion';
import { FileResult, FilesResult } from './fileResult';
import { useScriptLastExecutionCardSelector } from '../slice';

export const DefaultField = ({ type }) => {
    return `Unsupported on UI result type: "${type}"`;
};

const StringResult = ({ data }) => {
    return (
        <Typography sx={{ whiteSpace: 'pre-wrap', padding: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
            {data}
        </Typography>
    );
};

const ObjectResult = ({ data }) => {
    return (
        <Box sx={{ paddingLeft: '0.5rem', paddingRight: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
            <SimpleTable
                data={data}
                firstRowSx={{ textTransform: 'capitalize', fontWeight: '900' }}
                stringify={false}
            />
        </Box>
    );
};

const TableResult = ({ data }) => {
    return (
        <Box sx={{ paddingLeft: '0.5rem', paddingRight: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
            <MultiTable data={data} stringify={false} />
        </Box>
    );
};

const MultiResult = ({ data }) => {
    const results = [];
    for (const [key, value] of Object.entries(data)) {
        const ResultComponent = availableComponents[value.type] || availableComponents.default;
        results.push(<ResultComponent key={key} data={value.object} type={value.type} />);
    }
    return <Box sx={{ display: 'flex', gap: '0.25rem', flexDirection: 'column' }}>{results}</Box>;
};

const availableComponents = {
    string: StringResult,
    object: ObjectResult,
    table: TableResult,
    multi: MultiResult,
    file: FileResult,
    files: FilesResult,
    default: DefaultField,
};

export const ScriptResult = ({ scriptId }) => {
    const result = useScriptLastExecutionCardSelector(scriptId, (state) => state.result);
    if (!result) return;

    const ResultComponent = availableComponents[result.type] || availableComponents.default;

    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <Typography sx={{ paddingBottom: '0.5rem', fontWeight: '700' }} variant={'subtitle1'}>
                {result.type === 'multi' ? 'Results:' : 'Result:'}
            </Typography>
            <ResultComponent data={result.object} type={result.type} />
        </Box>
    );
};

export const ScriptResultAccordion = ({ result }) => {
    if (!result) return;

    const ResultComponent = availableComponents[result.type] || availableComponents.default;
    return (
        <SimpleAccordion title={'Result:'}>
            <ResultComponent data={result.object} type={result.type} />
        </SimpleAccordion>
    );
};
