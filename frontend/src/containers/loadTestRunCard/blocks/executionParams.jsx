import React from 'react';
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import { DynamicForm } from 'components/DynamicForm';
import { isEmpty } from 'lodash';
import { toTitle } from '../../../utils/to-camel-case';

export const ExecutionParams = ({ paramsConfig, paramsState, setParamsState }) => {
    if (isEmpty(paramsConfig)) return;

    const fields = Object.fromEntries(
        Object.entries(paramsConfig).map(([label, paramValue]) => [
            label,
            {
                label: toTitle(label),
                defaultValue: paramValue,
                type: 'number',
                valid: true,
                value: null,
                placeholder: null,
                optional: false,
            },
        ]),
    );

    return (
        <Box
            sx={{
                paddingTop: '1rem',
                borderLeft: '5px solid var(--bg-default)',
                paddingBottom: '1rem',
                paddingLeft: '1rem',
            }}
        >
            <Typography sx={{ fontWeight: '700' }} variant={'subtitle1'}>
                Execution parameters:
            </Typography>
            <DynamicForm requiredConfig={fields} resultConfig={paramsState} setResultConfig={setParamsState} />
        </Box>
    );
};
