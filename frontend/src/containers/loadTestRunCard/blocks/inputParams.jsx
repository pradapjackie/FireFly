import React from 'react';
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import { DynamicForm } from 'components/DynamicForm';
import { isEmpty } from 'lodash';

export const InputParams = ({ paramsConfig, paramsState, setParamsState }) => {
    if (isEmpty(paramsConfig)) return;

    return (
        <Box sx={{ paddingTop: '1rem' }}>
            <Typography sx={{ fontWeight: '700' }} variant={'subtitle1'}>
                Input parameters:
            </Typography>
            <DynamicForm
                requiredConfig={paramsConfig}
                resultConfig={paramsState}
                setResultConfig={setParamsState}
                numberOfColumns={2}
            />
        </Box>
    );
};
