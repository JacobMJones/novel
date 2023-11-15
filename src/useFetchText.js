import { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';

export function useFetchText() {
  
  const [texts, setTexts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchText = async () => {
      setLoading(true);
      try {
        // Replace this URL with the URL of your Flask server's route for downloading the Excel file
        const fileUrl = 'http://192.168.0.19:5000/text_data.xlsx';
        
        const response = await fetch(fileUrl);
        const arrayBuffer = await response.arrayBuffer();
        const workbook = XLSX.read(arrayBuffer, { type: 'buffer' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        
        // Exclude the first row which contains header data
        const textItems = jsonData.slice(1).map((entry) => ({
          id:entry[0],
          type: entry[2],
          subtype: entry[3],
          content: entry[1],
          active:entry[4],
          tags:entry[5]
        }));
        setTexts(textItems);
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
