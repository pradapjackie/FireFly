import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { useTheme } from '@mui/styles';
import { isEmpty } from 'lodash';

export const BoxPlotChart = ({ series }) => {
    const { palette } = useTheme();
    const data = isEmpty(series)
        ? []
        : Object.keys(series).map((key) => [new Date(key + 'Z'), ...series[key]]);

    const option = {
        legend: { show: false },
        tooltip: {
            trigger: 'axis',
            textStyle: {
                color: palette.background.default,
                fontFamily: 'roboto',
            },
        },
        grid: {
            left: 0,
            right: 0,
            top: '10%',
            bottom: 0,
            containLabel: true,
        },
        xAxis: {
            type: 'time',
            boundaryGap: ['10%', '10%'],
            splitLine: {
                show: false,
            },
        },
        yAxis: {
            type: 'value',
            splitLine: {
                show: false,
            },
        },
        dataset: {
            source: data,
        },
        series: [
            {
                name: 'boxplot',
                type: 'boxplot',
                itemStyle: {
                    color: palette.primary.main,
                },
                encode: {
                    x: [0],
                    y: [1, 2, 3, 4, 5],
                },
            },
        ],
    };

    return (
        <ReactEcharts
            style={{ height: '300px', width: '100%' }}
            option={{
                ...option,
            }}
        />
    );
};
