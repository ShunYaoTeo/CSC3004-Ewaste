// import PropTypes from 'prop-types';
import { useEffect, useState } from 'react';

// material-ui
import { useTheme, styled } from '@mui/material/styles';
import { Avatar, Box, Button, Grid, Typography } from '@mui/material';

// third-party
import Chart from 'react-apexcharts';
import { groupBy, size } from 'lodash';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SkeletonTotalOrderCard from 'ui-component/cards/Skeleton/EarningCard';
import { getUserEwaste } from 'api/api'

// assets
import LocalMallOutlinedIcon from '@mui/icons-material/LocalMallOutlined';
import generateMonthChartData from './chart-data/total-order-month-line-chart';
import generateYearChartData from './chart-data/total-order-year-line-chart';

const CardWrapper = styled(MainCard)(({ theme }) => ({
  backgroundColor: theme.palette.primary.dark,
  color: '#fff',
  overflow: 'hidden',
  position: 'relative',
  '&>div': {
    position: 'relative',
    zIndex: 5
  },
  '&:after': {
    content: '""',
    position: 'absolute',
    width: 210,
    height: 210,
    background: theme.palette.primary[800],
    borderRadius: '50%',
    zIndex: 1,
    top: -85,
    right: -95,
    [theme.breakpoints.down('sm')]: {
      top: -105,
      right: -140
    }
  },
  '&:before': {
    content: '""',
    position: 'absolute',
    zIndex: 1,
    width: 210,
    height: 210,
    background: theme.palette.primary[800],
    borderRadius: '50%',
    top: -125,
    right: -15,
    opacity: 0.5,
    [theme.breakpoints.down('sm')]: {
      top: -155,
      right: -70
    }
  }
}));

// ==============================|| DASHBOARD - TOTAL ORDER LINE CHART CARD ||============================== //

const TotalOrderLineChartCard = () => {
  const theme = useTheme();
  const [isLoading, setIsLoading] = useState(true);
  const [timeValue, setTimeValue] = useState(false);
  const [monthlyDonationCounts, setMonthlyDonationCounts] = useState([]);
  const [yearlyDonationCounts, setYearlyDonationCounts] = useState([]);

  useEffect(() => {
    // Fetch data when component mounts
    setIsLoading(true);
    const fetchData = async () => {
      const data = await getUserEwaste();
      console.log(data)

      const donationsGroupedByMonth = groupBy(data, (donation) =>
        new Date(donation.date_added).getMonth()
      );

      const donationsGroupedByYear = groupBy(data, (donation) =>
        new Date(donation.date_added).getFullYear()
      );

      console.log('donationsGroupedByMonth:', donationsGroupedByMonth);
      console.log('donationsGroupedByYear:', donationsGroupedByYear);

      // Count donations per month and year
      const monthlyCounts = Object.values(donationsGroupedByMonth).map(size);
      const yearlyCounts = Object.values(donationsGroupedByYear).map(size);

      console.log('monthlyCounts:', monthlyCounts);
      console.log('yearlyCounts:', yearlyCounts);

      setMonthlyDonationCounts(monthlyCounts);
      setYearlyDonationCounts(yearlyCounts);
      setIsLoading(false);
    };

    fetchData();
  }, []);

  const handleChangeTime = (event, newValue) => {
    setTimeValue(newValue);
  };

  const monthData = generateMonthChartData(monthlyDonationCounts);
  const yearData = generateYearChartData(yearlyDonationCounts)

  return (
    <>
      {isLoading ? (
        <SkeletonTotalOrderCard />
      ) : (
        <CardWrapper border={false} content={false}>
          <Box sx={{ p: 2.25 }}>
            <Grid container direction="column">
              <Grid item>
                <Grid container justifyContent="space-between">
                  <Grid item>
                    <Avatar
                      variant="rounded"
                      sx={{
                        ...theme.typography.commonAvatar,
                        ...theme.typography.largeAvatar,
                        backgroundColor: theme.palette.primary[800],
                        color: '#fff',
                        mt: 1
                      }}
                    >
                      <LocalMallOutlinedIcon fontSize="inherit" />
                    </Avatar>
                  </Grid>
                  <Grid item>
                    <Button
                      disableElevation
                      variant={timeValue ? 'contained' : 'text'}
                      size="small"
                      sx={{ color: 'inherit' }}
                      onClick={(e) => handleChangeTime(e, true)}
                    >
                      Month
                    </Button>
                    <Button
                      disableElevation
                      variant={!timeValue ? 'contained' : 'text'}
                      size="small"
                      sx={{ color: 'inherit' }}
                      onClick={(e) => handleChangeTime(e, false)}
                    >
                      Year
                    </Button>
                  </Grid>
                </Grid>
              </Grid>
              <Grid item sx={{ mb: 0.75 }}>
                <Grid container alignItems="center">
                  <Grid item xs={6}>
                    <Grid container alignItems="center">
                      <Grid item>
                        {timeValue ? (
                          <Typography sx={{ fontSize: '2.125rem', fontWeight: 500, mr: 1, mt: 1.75, mb: 0.75 }}>
                            {monthlyDonationCounts.reduce((a, b) => a + b, 0)} times
                          </Typography>
                        ) : (
                          <Typography sx={{ fontSize: '2.125rem', fontWeight: 500, mr: 1, mt: 1.75, mb: 0.75 }}>
                            {yearlyDonationCounts.reduce((a, b) => a + b, 0)} times
                          </Typography>
                        )}
                      </Grid>
                    </Grid>
                  </Grid>
                  <Grid item xs={6}>
                    {timeValue && monthlyDonationCounts ? 
                        <Chart {...monthData} /> : 
                        yearlyDonationCounts ? 
                        <Chart {...yearData} /> :
                        null
                    }
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Box>
        </CardWrapper>
      )}
    </>
  );
};

// TotalOrderLineChartCard.propTypes = {
//   isLoading: PropTypes.bool,
// };

export default TotalOrderLineChartCard;