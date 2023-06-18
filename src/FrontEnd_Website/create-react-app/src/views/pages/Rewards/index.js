import React, { useEffect, useState } from 'react';
import { Button, Typography } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import Alert from '@mui/material/Alert';
import { getReward, getUserRewards, redeemReward, getUserPoints } from 'api/api';

const Rewards = () => {
  const [rewards, setRewards] = useState([]);
  const [userRewards, setUserRewards] = useState([]);
  const [points, setPoints] = useState(0);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const columns = [
    { field: 'reward_name', headerName: 'Reward', width: 200 },
    { field: 'cost', headerName: 'Cost', width: 200 },
    { field: 'redeem', headerName: 'Redeem', renderCell: (params) => (
      <Button variant="contained" color="primary" onClick={() => handleRedeem(params.row.reward_id)}>Redeem</Button>
    )},
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const rewardsData = await getReward();
      setRewards(rewardsData);

      const userRewardsData = await getUserRewards();
      setUserRewards(userRewardsData);

      const pointsData = await getUserPoints();
      setPoints(pointsData.points);

    } catch (error) {
      console.error('Error Fetching Data: ', error);
    }
  }

  const handleRedeem = async (rewardId) => {
    try {
      const response = await redeemReward(rewardId);
      if (response && response.success) { 
        setSuccessMessage(response.message);
        setErrorMessage('');
        fetchData();
      } else if (response) {
        setErrorMessage(response.message);
        setSuccessMessage('');
      }
    } catch (error) {
      console.error('Error Redeeming Reward: ', error);
    }
  }
  return (
    <div style={{ height: 320, width: '100%' }}>
      <Typography variant="h6">Available Points: {points}</Typography>
      <Typography variant="h5">Available Rewards:</Typography>
      <DataGrid rows={rewards} columns={columns} hideFooter hideFooterSelectedRowCount/>
      <Typography variant="h5" style={{ marginTop: '16px' }}>Your Rewards:</Typography>
      <DataGrid rows={userRewards} columns={columns.slice(0, 2)} hideFooter/>
      {successMessage && <Alert severity="success" style={{ marginTop: '16px' }}>{successMessage}</Alert>}
      {errorMessage && <Alert severity="error" style={{ marginTop: '16px' }}>{errorMessage}</Alert>}
    </div>
  );
}

export default Rewards;
