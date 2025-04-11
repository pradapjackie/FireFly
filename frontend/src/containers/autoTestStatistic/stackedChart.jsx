import React from 'react';
import ReactEcharts from 'echarts-for-react';
import {useTheme} from '@mui/styles';
import {format} from "date-fns";

export const StackedHistoryChart = ({color = [], testRuns}) => {
  const {palette} = useTheme();

  let dates = []
  let success = []
  let fail = []
  let pending = []

  for (const testRun of testRuns) {
    dates.push(format(new Date(testRun.startTime), 'dd.MM.yyyy HH:mm'))
    if (testRun.resultByStatus.success !== 0) {
      success.push(testRun.resultByStatus.success)
    } else {
      success.push('-')
    }
    if (testRun.resultByStatus.fail !== 0) {
      fail.push(testRun.resultByStatus.fail)
    } else {
      fail.push('-')
    }
    if (testRun.resultByStatus.pending !== 0) {
      pending.push(testRun.resultByStatus.pending)
    } else {
      pending.push('-')
    }
  }

  const height = `${dates.length * 25 + 25}px`

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {type: 'shadow'},
      textStyle: {
        color: palette.background.default,
        fontFamily: 'roboto',
      },
    },
    legend: {show: false},
    grid: {
      top: '0%',
      left: '0%',
      right: '0%',
      bottom: '0%',
      containLabel: true,
    },
    xAxis: [{
      show: false,
      type: 'value',
      axisLine: {show: false},
      splitLine: {show: false},
    }],
    yAxis: [{
      type: 'category',
      data: dates,
      inverse: true,
      axisLine: {show: false},
      axisTick: {show: false},
      splitLine: {show: false},
      axisLabel: {
        color: palette.text.secondary,
        fontSize: 13,
        fontFamily: 'roboto',
      },
    }],
    series: [
      {
        name: 'Success',
        type: 'bar',
        stack: 'total',
        label: {
          show: true,
        },
        emphasis: {
          focus: 'series',
        },
        data: success,
      },
      {
        name: 'Pending',
        type: 'bar',
        stack: 'total',
        label: {
          show: true,
        },
        emphasis: {
          focus: 'series',
        },
        data: pending,
      },
      {
        name: 'Error',
        type: 'bar',
        stack: 'total',
        label: {
          show: true,
        },
        emphasis: {
          focus: 'series',
        },
        data: fail,
      },
    ],
  };

  return (
    <ReactEcharts
      style={{height: height}}
      option={{
        ...option,
        color: [...color],
      }}
    />
  );
};
