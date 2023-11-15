import React, { useState, useEffect } from 'react';
import InfiniteScrollComponent from './InfiniteScrollComponent';
import './App.css'
function App() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(()=>{
    setScrollY(window.scrollY)
  })
  return (
    <div className="App">
      
      <h1>Novelty and Self Reflection Generator</h1>
      <InfiniteScrollComponent />
    </div>
  );
}

export default App;
