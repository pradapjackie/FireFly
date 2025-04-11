import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { useTheme } from '@mui/styles';
import {isEmpty} from "lodash";

export const MultiLineChart = ({ series }) => {
    const { palette } = useTheme();
    const colorMap = {
        pending: palette.text.secondary,
        setup: 'rgba(9, 182, 109, 0.5)',
        working: palette.success.main,
        teardown: 'rgba(106, 117, 201, 0.5)',
        finished: palette.primary.main,
        error: palette.error.main,
    };
    const statuses = isEmpty(series) ? [] : Object.keys(Object.values(series)[0]);
    const data = statuses.map((status) => ({
        name: status,
        type: 'line',
        symbol: 'circle',
        showSymbol: false,
        data: Object.entries(series).map(([ts, statusValues]) => [new Date(ts), statusValues[status]]),
        itemStyle: {
            color: colorMap[status],
        },
    }));

    const option = {
        legend: {
            show: true,
            textStyle: {
                color: palette.text.secondary,
                fontFamily: 'roboto',
            },
        },
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
            bottom: '20%',
            containLabel: true,
        },
        xAxis: {
            type: 'time',
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
        dataZoom: [
            {
                type: 'slider',
                show: true,
            },
            {
                type: 'inside',
                xAxisIndex: [0],
            },
        ],
        series: data,
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
