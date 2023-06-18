import React, { useState } from 'react';
import { Button, Grid, Typography } from '@mui/material';
import Alert from '@mui/material/Alert';

// Components
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import CardSecondaryAction from 'ui-component/cards/CardSecondaryAction';

// Replace these with actual data from your sensors
const initialEwasteData = {
    itemType: '',
    weight: ''
};

const AddEwaste = () => {
    const [ewasteData, setEwasteData] = useState(initialEwasteData);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // Function to simulate getting data from sensors
    const getDataFromSensors = () => {
        setEwasteData({
            itemType: 'Battery',
            weight: '200g'
        });
    };

    const handleConfirm = async () => {
        try {
            // Simulate a call to your API. Replace with your actual API call
            await new Promise((resolve) => setTimeout(resolve, 1000));
            setSuccessMessage('Data has been successfully added and points have been awarded.');
            setErrorMessage('');
        } catch (error) {
            setErrorMessage('Failed to add data. Please try again.');
            setSuccessMessage('');
        }
    };

    return (
        <Grid container spacing={3} justifyContent="center">
            <Grid item xs={12} md={8} lg={6}>
                {/* Change the link to balena cam? */}
                <MainCard title="Add E-Waste" secondary={<CardSecondaryAction title="Info" link="https://info-link.com" />}>
                    <SubCard title="E-Waste Data" contentSX={{ pb: '16px' }}>
                        <Button variant="contained" color="primary" onClick={getDataFromSensors}>Get E-Waste Data</Button>
                        <Typography variant="h6" style={{ marginTop: '16px' }}>Item Type: {ewasteData.itemType}</Typography>
                        <Typography variant="h6" style={{ marginTop: '16px' }}>Weight: {ewasteData.weight}</Typography>
                        <Button variant="contained" color="secondary" onClick={handleConfirm} style={{ marginTop: '16px' }}>Confirm</Button>
                        {successMessage && <Alert severity="success" style={{ marginTop: '16px' }}>{successMessage}</Alert>}
                        {errorMessage && <Alert severity="error" style={{ marginTop: '16px' }}>{errorMessage}</Alert>}
                    </SubCard>
                </MainCard>
            </Grid>
        </Grid>
    );
};

export default AddEwaste;
