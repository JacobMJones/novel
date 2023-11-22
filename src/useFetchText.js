import { useState, useEffect } from 'react';

export function useFetchText() {
  
  const [texts, setTexts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchText = async () => {
      setLoading(true);
      try {
        const apiUrl = 'http://192.168.0.19:5000/texts';
        const response = await fetch(apiUrl, {
          method: 'GET'
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setTexts(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchText();
  }, []); 

  return { texts, loading, error };
}