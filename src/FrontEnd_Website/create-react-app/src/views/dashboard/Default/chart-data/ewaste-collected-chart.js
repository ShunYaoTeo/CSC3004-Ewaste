// ===========================|| DASHBOARD - E-WASTE COLLECTED CHART ||=========================== //

const chartData = {
  type: 'area',
  height: 95,
  options: {
    chart: {
      id: 'ewaste-collected-chart',
      sparkline: {
        enabled: true
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: 1
    },
    tooltip: {
      fixed: {
        enabled: false
      },
      x: {
        show: false
      },
      y: {
        title: 'Kg '
      },
      marker: {
        show: false
      }
    }
  },
  series: [
    {
      // TODO: replace with dynamic data
      data: [0, 500, 600, 700, 1200, 1300, 1500]
    }
  ]
};

export default chartData;
