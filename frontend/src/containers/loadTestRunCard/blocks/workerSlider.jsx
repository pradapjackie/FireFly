import React from 'react';
import { Box, Slider } from '@mui/material';
import Typography from '@mui/material/Typography';

export const WorkerSlider = ({ config, configState, numberOfTasks, changeNumberOfTasks }) => {
    const values = { ...config, ...configState };

    const workerMax = parseInt(values['maximum_number_of_workers']);
    const workerStep = parseInt(values['concurrency_within_a_single_worker']);

    return (
        <Box>
            <Typography sx={{ fontWeight: '700' }} variant={'subtitle1'}>
                Number of tasks:
            </Typography>
            <Slider
                value={numberOfTasks}
                onChange={changeNumberOfTasks}
                defaultValue={workerStep}
                valueLabelDisplay="auto"
                step={workerStep}
                marks
                min={0}
                max={workerMax * workerStep}
            />
        </Box>
    );
};
