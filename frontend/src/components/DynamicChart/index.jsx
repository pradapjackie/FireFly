import { BoxPlotChart } from '../Charts/BoxPlot';
import { DefaultChart } from './defaultChart';

const availableCharts = {
    BoxPlot: BoxPlotChart,
    default: DefaultChart,
};

export const DynamicChart = ({ type, ...props }) => {
    const ChartComponent = availableCharts[type] || availableCharts.default;
    return <ChartComponent type={type} {...props} />;
};
