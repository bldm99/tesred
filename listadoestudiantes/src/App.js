// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './login/Login'; // Asegúrate de tener el archivo CSS en la misma carpeta

import StudentData from './studenData/StudentData';
import Lista from './studenData/Lista';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Lista />} />
      </Routes>
    </Router>
  );
}

export default App;