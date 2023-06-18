import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://ewaste-management.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

const getToken = () => localStorage.getItem('token');

export const login = async (username, password) => {
    try {
      const token = btoa(`${username}:${password}`);
      const response = await apiClient.post('/login', {}, {
        headers: {
          'Authorization': `Basic ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error Sending Request: ', error);
    }
  }
  

export const addEwaste = async (item_type, weight) => {
  try {
    const response = await apiClient.post(`/addEwaste?item_type=${item_type}&weight=${weight}`, {}, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error Sending Request: ', error);
  }
}

export const getUserEwaste = async () => {
  try {
    const response = await apiClient.get('/getUserEwaste', {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error Sending Request: ', error);
  }
}

export const getUserEwasteStats = async () => {
  try {
    console.log(getToken())
    const response = await apiClient.get('/getUserEwasteStats', {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error Sending Request: ', error);
  }
}

export const getReward = async () => {
  try {
    const response = await apiClient.get('/getReward', {
      headers: { Authorization: `Bearer ${getToken()}` },
    });

    return response.data.map((reward, index) => ({
      ...reward,
      id: `${reward.reward_id}-${index}`
    }));
  } catch (error) {
    console.error('Error Sending Request: ', error);
  }
}

export const getUserRewards = async () => {
  try {
    const response = await apiClient.get('/getUserRewards', {
      headers: { Authorization: `Bearer ${getToken()}` },
    });

    return response.data.map((reward, index) => ({
      ...reward,
      id: `${reward.reward_id}-${index}`
    }));
  } catch (error) {
    console.error('Error Sending Request: ', error);
  }
}


export const redeemReward = async (reward_id) => {
  try {
    const response = await apiClient.post(`/redeemReward?reward_id=${reward_id}`, {}, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
      return response.data;
  } catch (error) {
    console.error('Error Sending Request: ', error);
    return error.message;
  }
}


export const getUserPoints = async () => {
  try {
    const response = await apiClient.get('/getUserPoints', {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.data;
  } catch (error) {
    console.error('Error Sending Request: ', error);
  }
}
