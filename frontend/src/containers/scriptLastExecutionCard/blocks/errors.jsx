import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { FireFlyError } from 'components/FireflyError';
import React from 'react';
import { SimpleAccordion } from 'components/SimpleAccordion';
import { useScriptLastExecutionCardSelector } from '../slice';

export const ErrorSections = ({ scriptId }) => {
    const errors = useScriptLastExecutionCardSelector(scriptId, (state) => state.errors);
    if (!errors) return;

    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <Typography sx={{ paddingBottom: '0.5rem', fontWeight: '700' }} variant={'subtitle1'}>
                Errors:
            </Typography>
            {errors.map((error, i) => (
                <FireFlyError
                    key={i}
                    errorName={error.name}
                    errorMessage={error.message}
                    errorTrace={error.traceback}
                />
            ))}
        </Box>
    );
};

export const ErrorSectionAccordion = ({ errors }) => {
    if (!errors) return;

    return (
        <SimpleAccordion title={'Errors:'}>
            {errors.map((error, i) => (
                <FireFlyError
                    key={i}
                    errorName={error.name}
                    errorMessage={error.message}
                    errorTrace={error.traceback}
                />
            ))}
        </SimpleAccordion>
    );
};
