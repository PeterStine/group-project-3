// App.js
// Main entry point of application

import React from 'react';
import './App.css';
import LeafletMap from './LeafletMap';
import TextStack from './TextStack';

function App() {
  return (
    <div className="App">
      <header className="App-header">
          <TextStack />
          <LeafletMap />
      </header>
    </div>
  );
}

export default App;
