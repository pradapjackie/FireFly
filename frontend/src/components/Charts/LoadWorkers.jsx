import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { useTheme } from '@mui/styles';
import {toTitle} from "../../utils/to-camel-case";

export const LoadWorkers = ({ workers }) => {
    const { palette } = useTheme();
    const columnLength = 10;
    const numberOfColumns = Math.floor((Object.keys(workers).length - 1) / columnLength) + 1
    const height = `${numberOfColumns * 50}px`
    const colorMap = {
        pending: palette.text.secondary,
        setup: 'rgba(9, 182, 109, 0.5)',
        working: palette.success.main,
        proceed_finish: 'rgba(106, 117, 201, 0.5)',
        teardown: 'rgba(106, 117, 201, 0.5)',
        finished: palette.primary.main,
        error: palette.error.main,
    };

    const data = [];
    for (let i = 0; i < Object.keys(workers).length; i++) {
        const column = Math.floor(i / columnLength) + 1;
        const row = i % columnLength;
        const status = workers[i] || "pending"
        data.push([row, column, colorMap[status], toTitle(status)]);
    }

    const option = {
        legend: { show: false },
        tooltip: {
            show: true,
            formatter: function (param) {
                return param.value[3];
            },
            textStyle: {
                color: palette.background.default,
                fontFamily: 'roboto',
            },
        },
        grid: {
            left: 0,
            right: 0,
            top: 0,
            bottom: 0,
        },
        xAxis: {
            show: false,
            type: 'category',
            data: new Array(10).fill(' '),
        },
        yAxis: {
            show: false,
            type: 'category',
            inverse: true,
        },
        series: [
            {
                type: 'scatter',
                data: data,
                symbolSize: 20,
                itemStyle: {
                    color: function (param) {
                        return param.data[2];
                    },
                },
            },
        ],
    };

    return (
        <ReactEcharts
            style={{ height: height, width: '100%' }}
            option={{
                ...option,
            }}
        />
    );
};
