// StudentData.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const StudentData = () => {
  const [studentInfo, setStudentInfo] = useState(null);
  const [selectedWeek, setSelectedWeek] = useState(1);
  const [selectedStudent, setSelectedStudent] = useState(null);

  useEffect(() => {
    // Realizar solicitud para obtener datos del estudiante desde la API
    axios.get('https://girapi.bladimirchipana.repl.co/alumnos?_idUsuario=6531d08612ec096c58717b97&_idRiesgo=65754cdbd6a61db3295d8f3b')
      .then(response => setStudentInfo(response.data))
      .catch(error => console.error('Error fetching student data:', error));
  }, []);

  const weeks = Array.from({ length: 16 }, (_, index) => index + 1); // Generar semanas del 1 al 16

  const handleWeekChange = (week) => {
    setSelectedWeek(week);
  };


  const handleSaveAttendance = () => {
    // Filtrar estudiantes que han marcado asistencia para la semana seleccionada
    const studentsWithAttendance = studentInfo.filter(student => student[`sem${selectedWeek}`] !== undefined);
  
    // Crear el objeto que se enviará a la API
    const dataToSend = {
      _idUsuario: "6531d08612ec096c58717b97",
      _idRiesgo: "65754cdbd6a61db3295d8f3b",
      alumnoId: studentsWithAttendance.map(student => student._id),
      [`sem${selectedWeek}`]: studentsWithAttendance.map(student => student[`sem${selectedWeek}`]),
    };
  
    axios.post('https://girapi.bladimirchipana.repl.co/listalumno', dataToSend)
      .then(response => console.log('Attendance data saved:', response.data))
      .catch(error => console.error('Error saving attendance data:', error));
  };
  
  
 

  const handleStudentClick = (student) => {
    setSelectedStudent(student);
  };

  const handleCheckboxChange = (studentIndex, attended) => {
    const updatedStudentInfo = [...studentInfo];
  
    if (attended) {
      updatedStudentInfo[studentIndex][`sem${selectedWeek}`] = 1;
    } else {
      // Si el checkbox no está marcado, desmarcarlo (valor 0)
      updatedStudentInfo[studentIndex][`sem${selectedWeek}`] = 0;
    }
  
    console.log('Updated Student Info:', updatedStudentInfo);
    setStudentInfo(updatedStudentInfo);
  };
  
  

  return (
    <div>
      <h2>Datos del Estudiante</h2>
      {selectedStudent && (
        <div>
          <p>Nombre: {selectedStudent.nombre}</p>
          <p>Curso: {selectedStudent.curso}</p>
          <p>Correo: {selectedStudent.correo}</p>
          <p>Número de Whatsapp: {selectedStudent.wasap}</p>
        </div>
      )}

      <div>
        <h3>Semanas</h3>
        <div style={{ display: 'flex' }}>
          {weeks.map((week) => (
            <div key={week} style={{ marginRight: '10px' }}>
              <button onClick={() => handleWeekChange(week)}>
                Semana {week}
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedWeek && studentInfo && studentInfo.length > 0 && (
        <div>
          <h3>Asistencias para la Semana {selectedWeek}</h3>
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Asistió</th>
                <th>No asistió</th>
              </tr>
            </thead>
            <tbody>
              {studentInfo.map((student, index) => (
                <tr key={index}>
                  <td onClick={() => handleStudentClick(student)}>{student.nombre}</td>
                  <td>
                    <input
                      type="checkbox"
                      checked={student[`sem${selectedWeek}`] === 1}
                      onChange={() => handleCheckboxChange(index, true)}
                    />
                  </td>
                  <td>
                    <input
                      type="checkbox"
                      checked={student[`sem${selectedWeek}`] === 0}
                      onChange={() => handleCheckboxChange(index, false)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <button onClick={handleSaveAttendance}>Guardar Asistencias</button>
        </div>
      )}
    </div>
  );
};

export default StudentData;
