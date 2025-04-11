import React from 'react';
import { Box } from '@mui/material';
import { MultiLineChart } from '../../../components/Charts/MultiLineChart';
import Typography from '@mui/material/Typography';

const TasksMemo = ({ series }) => {
    return (
        <Box sx={{ borderRadius: '4px' }}>
            <Typography sx={{ fontWeight: '700' }} variant={'subtitle1'}>
                Task status:
            </Typography>
            <MultiLineChart series={series} />
        </Box>
    );
};

function compareSeries(oldProps, newProps) {
    const obj1 = oldProps.series;
    const obj2 = newProps.series;
    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    for (const key of keys1) {
        if (!obj2.hasOwnProperty(key)) {
            return false;
        }
        if (obj1[key].length !== obj2[key].length) {
            return false;
        }
    }

    return true;
}

export const Tasks = React.memo(TasksMemo, compareSeries);
