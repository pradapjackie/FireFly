import React, { useEffect, useRef } from 'react';
import ReactEcharts from 'echarts-for-react';
import { useTheme } from '@mui/styles';

const PieChartMemo = ({
  height,
  color = [],
  data: { success, fail, pending },
}) => {
  const { palette } = useTheme();
  let echartRef = useRef('echartRef');
  useEffect(() => {
    if (echartRef.current) {
      const echartInstance = echartRef.current.getEchartsInstance();
      echartInstance.dispatchAction({
        type: 'highlight',
        seriesName: 'Test Group History',
        name: 'Success',
      });
      echartInstance.on('mouseover', (e) => {
        if (e.dataIndex !== 0) {
          echartInstance.dispatchAction({
            type: 'downplay',
            seriesName: 'Test Group History',
            name: 'Success',
          });
        }
      });
      echartInstance.on('mouseout', () => {
        echartInstance.dispatchAction({
          type: 'highlight',
          seriesName: 'Test Group History',
          name: 'Success',
        });
      });
    }
  }, []);

  const option = {
    legend: { show: false },
    tooltip: { show: false },
    xAxis: [
      {
        axisLine: { show: false },
        splitLine: { show: false },
      },
    ],
    yAxis: [
      {
        axisLine: { show: false },
        splitLine: { show: false },
      },
    ],
    series: [
      {
        name: 'Test Group History',
        type: 'pie',
        radius: ['45%', '72.55%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: false,
        hoverOffset: 5,
        stillShowZeroSum: false,
        emphasis: {
          label: {
            show: true,
            fontSize: '14',
            fontWeight: 'normal',
            formatter: '{d}%\n{b}',
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
        label: {
          show: false,
          position: 'center',
          color: palette.text.secondary,
          fontSize: 13,
          fontFamily: 'roboto',
          formatter: '{a}',
        },
        labelLine: {
          show: false,
        },
        data: [
          {
            value: success,
            name: 'Success',
          },
          {
            value: pending,
            name: 'Pending',
          },
          {
            value: fail,
            name: 'Error',
          },
        ],
      },
    ],
  };

  return (
    <ReactEcharts
      ref={echartRef}
      style={{ height: height, width: '100%' }}
      option={{
        ...option,
        color: [...color],
      }}
    />
  );
};

export const PieChart = React.memo(PieChartMemo);
