import React, { useState } from 'react';
import '../styles.css';
import CellModal from './CellModal'; // Import or define your Modal component

function TextComponent({ item }) {
  const [isCellModalOpen, setIsCellModalOpen] = useState(false);

  const handleTextClick = () => {
    console.log("clicked");
    setIsCellModalOpen(true);
  };

  const handleGenerateCellModal = (e) => {
    if (e) {
      e.stopPropagation();
    }
    console.log("generate action");
    setIsCellModalOpen(false);
  };

  const handleCloseCellModal = (e) => {
    if (e) {
      e.stopPropagation();
    }
    console.log("clicked close cell", isCellModalOpen);
    setIsCellModalOpen(false);
  };

  const handleInactivate = (e) => {
    console.log("Inactivate action", item);
    if (e) {
      e.stopPropagation();
    }
    fetch('http://localhost:5000/update_excel', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: item.id, // Assuming `item` has an `id` field
        active: 0,
        type: 'text'
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

  // Function to determine the style based on item subtype
  const getStyleBySubtype = () => {
    switch (item.subtype) {
      case 'reminder':
        return 'reminderStyle';
      case 'memory':
        return 'memoryStyle';
      case 'poem':
        return 'poemStyle';
      default:
        return 'defaultStyle';
    }
  };

  // Function to render different elements based on subtype
  const renderContentBySubtype = () => {
    console.log("Rendering content for subtype:", item.subtype, "Content:", item.content);

    switch (item.subtype) {
      case 'reminder':
        return <span className="reminderElement">{item.content}</span>;
      case 'memory':
        return <div className="memoryElement">{item.content}</div>;
      case 'rumi':
        return <p className="poemElement">{item.content}</p>;
      default:
        return <span>{item.content}</span>;
    }
  };

  return (
    <div className={`sharedSize ${getStyleBySubtype()}`} onClick={handleTextClick}>
      {renderContentBySubtype()}
      {isCellModalOpen && (
        <CellModal onClose={handleCloseCellModal}>
          <button onClick={handleInactivate}>Inactivate</button>
          <p />
          <button onClick={handleGenerateCellModal}>Generate</button>
          <p />
          <button onClick={handleCloseCellModal}>Close</button>
        </CellModal>
      )}
    </div>
  );
}

export default TextComponent;
