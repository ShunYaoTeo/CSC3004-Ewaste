import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { Grid, Typography } from '@mui/material';
import ApexCharts from 'apexcharts';
import Chart from 'react-apexcharts';
import SkeletonTotalGrowthBarChart from 'ui-component/cards/Skeleton/TotalGrowthBarChart';
import MainCard from 'ui-component/cards/MainCard';
import { gridSpacing } from 'store/constant';
import { getUserEwaste } from 'api/api';

const TotalGrowthBarChart = ({ isLoading }) => {
  const [ewasteData, setEwasteData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [chartData, setChartData] = useState({ options: {}, series: [] });
  const customization = useSelector((state) => state.customization);
  const { navType } = customization;

  const fetchEwasteData = async () => {
    try {
      const response = await getUserEwaste();
      console.log(response);
      setEwasteData(response);
    } catch (error) {
      console.error('Error Fetching eWaste Data: ', error);
    }
  };

  useEffect(() => {
    fetchEwasteData();
  }, []);

  useEffect(() => {
    const now = new Date();
    const thisYear = now.getFullYear();
    const dataToUse = ewasteData.filter(item => (new Date(item.date_added)).getFullYear() === thisYear);
    setFilteredData(dataToUse);
  }, [ewasteData]);
  

  useEffect(() => {
    const groupedData = filteredData.reduce((acc, item) => {
      const month = (new Date(item.date_added)).getMonth();
      if (!acc[item.item_type]) {
        acc[item.item_type] = Array(12).fill(0);
      }
      acc[item.item_type][month] += item.weight;
      return acc;
    }, {});

    const newSeries = Object.entries(groupedData).map(([itemType, data]) => {
      return {
        name: itemType,
        data: data.map(weight => parseFloat(weight.toFixed(2)))
      };
    });

    const newChartData = {
      series: newSeries,
      options: {
        chart: {
          type: 'bar',
          id: 'ewaste-collected-chart'
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        },
        dataLabels: {
          enabled: false
        },
        tooltip: {
          y: {
            title: 'Kg '
          },
        }
      }
    };

    if (!isLoading) {
      ApexCharts.exec('ewaste-collected-chart', 'updateOptions', newChartData);
    }

    setChartData(newChartData);
  }, [navType, isLoading, filteredData]);

  return (
    <>
      {isLoading ? (
        <SkeletonTotalGrowthBarChart />
      ) : (
        <MainCard>
          <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
              <Grid container direction="column" spacing={1}>
                <Grid item>
                  <Typography variant="subtitle2">Total Growth</Typography>
                </Grid>
                <Grid item>
                  <Typography variant="h3">
                    {filteredData.reduce((sum, item) => parseFloat((sum + item.weight).toFixed(2)), 0)} Kg
                  </Typography>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12}>
              <Chart
                options={chartData.options}
                series={chartData.series}
                type="bar"
                height={378}
                id="ewaste-collected-chart"
              />
            </Grid>
          </Grid>
        </MainCard>
      )}
    </>
  );
};

TotalGrowthBarChart.propTypes = {
  isLoading: PropTypes.bool
};

export default TotalGrowthBarChart;
