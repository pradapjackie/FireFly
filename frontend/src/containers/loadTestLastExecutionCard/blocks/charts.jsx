import React from 'react';
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import { isEmpty } from 'lodash';
import { DynamicChart } from '../../../components/DynamicChart';

export const Charts = ({ chartConfig, chartsData }) => {
    return (
        <Box sx={{ borderRadius: '4px' }}>
            <Typography sx={{ fontWeight: '700' }} variant={'subtitle1'}>
                Charts:
            </Typography>
            {!isEmpty(chartConfig) ? (
                Object.entries(chartConfig).map(([chartName, chartType]) => (
                    <DynamicChart key={chartName} type={chartType} series={chartsData?.[chartName]} />
                ))
            ) : (
                <></>
            )}
        </Box>
    );
};
