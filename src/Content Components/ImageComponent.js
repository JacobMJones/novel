import React, { useState } from 'react';
import '../styles.css';
import CellModal from './CellModal'; // Import or define your Modal component

function ImageComponent({ item, alt }) {
  const [isCellModalOpen, setIsCellModalOpen] = useState(false);

  const handleImageClick = () => {
    setIsCellModalOpen(true);
  };

  const handleInactivate = () => {
    console.log("Inactivate action", item);
  
    fetch('http://localhost:5000/update_excel', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: item.id, // Assuming `item` has an `id` field
        active: 0,
        type:'image'
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Row updated:', data);
      setIsCellModalOpen(false);
    })
    .catch(error => {
      console.error('Error updating row:', error);
    });
    setIsCellModalOpen(false);
  };

  const handleGenerateCellModal = () => {
    console.log("Inactivate action");
    setIsCellModalOpen(false);
  };

  const handleCloseCellModal = () => {
    setIsCellModalOpen(false);
  };

  return (
    <div className='sharedSize'>
      <img
        // key={'imgid-' + item.id}
        onClick={handleImageClick}
        src={item.imageUrl}
        alt={alt}
        loading="lazy"
        style={{
          maxWidth: '100%',
          maxHeight: '100%',
          cursor: 'pointer',
        }}
      />
      {isCellModalOpen && (
        <CellModal onClose={handleCloseCellModal}>
        <button style={{fontSize:'5vw'}} onClick={handleInactivate}>Inactivate</button>
        <p/>
        <button onClick={handleGenerateCellModal}>Generate</button>
        <p/>
        <button onClick={handleCloseCellModal}>Close</button>
      </CellModal>
      )}
    </div>
  );
}

export default ImageComponent;
