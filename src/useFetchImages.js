import { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';
export function useFetchImages() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchImages = async () => {
      setLoading(true);
      const imageData = 'http://192.168.0.19:5000/image_data.xlsx';
      const imagePath = 'http://192.168.0.19:5000/images/'
      try {
        const response = await fetch(imageData);
        const arrayBuffer = await response.arrayBuffer();
        const workbook = XLSX.read(arrayBuffer, { type: 'buffer' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        console.log('slice', jsonData.slice(1)[0]);
        
        // Filter the entries where 'active' equals 1 before mapping
        const activeImageItems = jsonData.slice(1).filter(entry => entry[10] === 1).map((entry) => ({
          id: entry[0],
          file: entry[1],
          width: entry[2],
          height: entry[3],
          size: entry[4],
          format: entry[5],
          type: entry[6],
          subtype: entry[7],
          tags: entry[8],
          votes: entry[9],
          active: entry[10],
          timestamp: entry[11],
          imageUrl: imagePath + entry[1],
        }));
        
        console.log('active image items', activeImageItems);
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
