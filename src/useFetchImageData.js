import { useState, useEffect } from 'react';

export function useFetchImageData() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchImages = async () => {
      setLoading(true);
      // Update this URL to your Flask app's endpoint
      const dataUrl = 'http://192.168.0.19:5000/image_data'; 
      const path = 'http://192.168.0.19:5000/';

      try {
        const response = await fetch(dataUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();

        // Map the JSON data to your images format
        const activeImageItems = jsonData.filter(entry => entry.active === 1).map(entry => ({
          ...entry,
          imageUrl: path + entry.path,
        }));

        setImages(activeImageItems);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, []); 

  return { images, loading, error };
}
