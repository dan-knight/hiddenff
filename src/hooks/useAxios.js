import React, { useState } from 'react';
import axios from 'axios';

export default function useAxios(initialData) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  async function request({ url, method='get', params={} }) {
    setLoading(true);
    
    let error = false;
    let data;

    try {
      const response = await axios({
        method: method,
        url: url,
        params: params
      });

      data = response?.data;
    } catch (e) {
      error = true;
    };
    
    setError(error);
    setLoading(false)

    return data;
  };

  return [loading, error, request];
};