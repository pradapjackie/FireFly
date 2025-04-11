import React from 'react';
import { Box, Typography } from '@mui/material';
import { isEmpty } from 'lodash';
import { SimpleTable } from 'components/SimpleTable';
import { SimpleAccordion } from 'components/SimpleAccordion';
import { useScriptLastExecutionCardSelector } from '../slice';

export const EnvUsed = ({ scriptId }) => {
    const envUsed = useScriptLastExecutionCardSelector(scriptId, (state) => state.envUsed);
    if (isEmpty(envUsed)) return;

    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <Typography sx={{ paddingBottom: '0.5rem', fontWeight: '700' }} variant={'subtitle1'}>
                Environment used:
            </Typography>
            <Box sx={{ paddingLeft: '0.5rem', paddingRight: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
                <SimpleTable data={envUsed} />
            </Box>
        </Box>
    );
};

export const EnvUsedAccordion = ({ envUsed }) => {
    if (isEmpty(envUsed)) return;

    return (
        <SimpleAccordion title={'Environment used:'}>
            <Box sx={{ paddingLeft: '0.5rem', paddingRight: '0.5rem', background: 'rgba(var(--primary), 0.15)' }}>
                <SimpleTable data={envUsed} />
            </Box>
        </SimpleAccordion>
    );
};
