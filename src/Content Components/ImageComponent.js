import React, { useState } from 'react';
import '../styles.css';
import CellModal from './CellModal'; // Import or define your Modal component

function ImageComponent({ item, alt, onImageClick }) {
  const [isCellModalOpen, setIsCellModalOpen] = useState(false);
  const [inputTag, setInputTag] = useState('');

  const handleImageClick = (e) => {
    e.stopPropagation(); // Stop propagation first
    onImageClick(e); // Now call the function passed from the parent with the event
    setIsCellModalOpen(true);
  };

  const handleInactivate = () => {
    console.log("Inactivate action", item);

    fetch('http://localhost:5000/deactivate_image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: item.id, // Assuming `item` has an `id` field
        active: 0,
        type: 'image'
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
  const handleTagChange = (event) => {
    setInputTag(event.target.value); // Only update the input value
  };

  const handleAddTag = () => {
    fetch('http://localhost:5000/add_tag', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: item.id,
        tag: inputTag // Use the state variable
      })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Tag added:', data);
        setIsCellModalOpen(false);
      })
      .catch(error => {
        console.error('Error adding tag:', error);
      });
    // Optionally reset the inputTag state here if needed
  };
  // const formattedColor = item.color_rgb ? `rgb(${item.color_rgb.replace(/[\(\)]/g, '')})` : 'rgb(0,0,0)';
  const formatColor = (colorRgb) => {
    return colorRgb ? `rgb(${colorRgb.replace(/[\(\)]/g, '')})` : 'rgb(0,0,0)';
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
          maxHeight: '80vh',
          cursor: 'pointer',
        }}
      />
      <button onClick={()=> handleInactivate()}>Inactivate</button>
      {isCellModalOpen && (
        <CellModal onClose={handleCloseCellModal}>


          <input
            type="text"
            value={inputTag} // Use the state variable
            onChange={handleTagChange}
            placeholder="Enter tag"
            style={{ marginRight: '10px' }}
          />
          <p />
          <button style={{ fontSize: '2vw' }} onClick={handleAddTag}>Add tag</button>
          <div>Tags:{item.tags}</div>
          <p/>
          <button style={{ fontSize: '2vw' }}  onClick={handleGenerateCellModal}>Generate</button>
             
          <p />
          <button style={{ fontSize: '2vw' }} onClick={handleInactivate}>Inactivate</button>
          <p/>
          <button style={{ fontSize: '2vw' }} onClick={handleCloseCellModal}>Close</button>
        </CellModal>
      )}
    </div>
  );
}

export default ImageComponent;
