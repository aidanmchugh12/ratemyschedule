import React, { useEffect, useState } from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from './components/Home';
import InputData from './components/InputData';
import GradeOutput from './components/GradeOutput';

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/input" element={<InputData />} />
      <Route path="/output" element={<GradeOutput />} />
    </Routes>
  </Router>
  );
}

export default App;

