import React, { useState } from 'react';
import '../styles.css';

function CellModal({ children, onClose }) {

    const handleBackdropClick =(e)=>{
        if (e.target === e.currentTarget) {
            onClose();
          }
    }
  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content">
        {children}
        {/* <button onClick={onClose}>Close Modal</button> */}
      </div>
    </div>
  );
}

export default CellModal;