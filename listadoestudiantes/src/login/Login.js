// Login.js
import './Login.css'; // Asegúrate de tener el archivo CSS en la misma carpeta

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
  
    try {
      const response = await axios.get(
        `https://girapi.bladimirchipana.repl.co/alumnos?_idUsuario=${username}`
      );
      console.log(response.data);  // Agrega esta línea
  
      // Verifica si la API devuelve datos de usuario
      if (response.data && response.data.length > 0) {
        // Encuentra el primer objeto con el nombre de usuario proporcionado
        const usuarioEncontrado = response.data.find(
          (usuario) => usuario.nombre === username
        );
  
        // Si se encuentra el usuario, redirige a la página de datos del estudiante
        if (usuarioEncontrado) {
          navigate(`/student-data/${username}`);
        } else {
          setError('Credenciales inválidas');
        }
      } else {
        setError('Credenciales inválidas');
      }
    } catch (error) {
      console.error('Error de autenticación:', error);
      setError('Error de autenticación');
    }
  };
  

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form className="login-form" onSubmit={handleLogin}>
        <label>
          Usuario:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        {error && <p className="error-message">{error}</p>}
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  );
};

export default Login;
