// App.js
// Main entry point of application

import React from 'react'; // Foundation of react native application
import { StyleSheet, View } from 'react-native'; // Allows styling components from StyleSheet, and View is a container tag
// View has flexbox, style, touch handling, and accessibility controls

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
