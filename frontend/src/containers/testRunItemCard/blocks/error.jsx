import React, { Fragment } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { FireFlyError } from '../../../components/FireflyError';

export const ErrorSections = ({ errors }) => {
    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <Typography sx={{ paddingBottom: '0.5rem', fontWeight: '700' }} variant={'subtitle1'}>
                Errors:
            </Typography>
            {Object.entries(errors).map(([stageName, errors]) => (
                <Fragment key={stageName}>
                    {errors.map((error, i) => (
                        <FireFlyError
                            key={stageName + i}
                            errorName={`${stageName} stage error: ${error.name}`}
                            errorMessage={error.message}
                            errorTrace={error.traceback}
                        />
                    ))}
                </Fragment>
            ))}
        </Box>
    );
};
