import React, { useEffect, useState } from 'react';
import * as Data from '../Data';

import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import './lista.css'

const Lista = () => {
    const getAlumnos = Data.getAlumnos;
    const postLista = Data.postLista;

    const [alumnos, setAlumnos] = useState([]);
    const [diccionario, setDiccionario] = useState({});
    const [chekf1, setChekf1] = useState('1');
    const [nsemana, setNsemana] = useState('1');
    const [semanaActual, setSemanaActual] = useState(1);



    useEffect(() => {
        const obtenerdata = async () => {
            try {
                const alumnosData = await getAlumnos(setAlumnos);

                // Construye el diccionario con la clave _id
                const diccionarioAsistencia = {};
                alumnosData.forEach((alumno) => {
                    diccionarioAsistencia[alumno._id] = chekf1; // Puedes inicializar el valor como desees
                });

                setDiccionario(diccionarioAsistencia);
            } catch (error) {
                console.log(error);
            }
        };

        obtenerdata();
    }, []);

    const handleCheckboxChangeAsistio = (alumnoId) => {
        setDiccionario((prevDiccionario) => ({
            ...prevDiccionario,
            [alumnoId]: '0',
        }));
    };

    const handleCheckboxChangeFalto = (alumnoId) => {
        setDiccionario((prevDiccionario) => ({
            ...prevDiccionario,
            [alumnoId]: '1',
        }));
    };

    const handleCheckboxChange = (alumnoId) => {
        // Cambia el estado del checkbox actual
        setDiccionario((prevDiccionario) => ({
            ...prevDiccionario,
            [alumnoId]: prevDiccionario[alumnoId] === '0' ? '1' : '0',
        }));

        // Encuentra el ID del otro checkbox
        const otroAlumnoId = Object.keys(diccionario).find((id) => id !== alumnoId);

        // Desmarca el otro checkbox
        if (otroAlumnoId) {
            setDiccionario((prevDiccionario) => ({
                ...prevDiccionario,
                [otroAlumnoId]: '',
            }));
        }
    };

    const df = () => {
        console.log(diccionario);
    };

    const tomarAsistencia = async () => {
        //const nsemana = '1'
        try {

            for (const alumnoId in diccionario) {
                if (diccionario.hasOwnProperty(alumnoId)) {
                    const valor = diccionario[alumnoId];
                    await postLista(alumnoId, nsemana, valor);
                }
            }
            toast.success('¡Asistencia guardada correctamente!');

        } catch (error) {
            console.log(error)
        }
    };



    return (
        <div className='alumnos'>
            <ToastContainer />
            <h2>Lista de Alumnos Tecsup 2023 curso AWS</h2>
            <div className='semanas'>
                <button onClick={() => { setNsemana('1') }}  >Semana 1</button>
                <button onClick={() => { setNsemana('2') }} >Semana 2</button>
                <button onClick={() => { setNsemana('3') }} >Semana 3</button>
                <button onClick={() => { setNsemana('4') }} >Semana 4</button>
                <button onClick={() => { setNsemana('5') }} >Semana 5</button>
                <button onClick={() => { setNsemana('6') }} >Semana 6</button>
                <button onClick={() => { setNsemana('7') }} >Semana 7</button>
                <button onClick={() => { setNsemana('8') }}>Semana 8</button>
                <button onClick={() => { setNsemana('9') }}>Semana 9</button>
                <button onClick={() => { setNsemana('10') }}>Semana 10</button>
                <button onClick={() => { setNsemana('11') }}>Semana 11</button>
                <button onClick={() => { setNsemana('12') }}>Semana 12</button>
                <button onClick={() => { setNsemana('13') }}>Semana 13</button>
                <button onClick={() => { setNsemana('14') }}>Semana 14</button>
                <button onClick={() => { setNsemana('15') }}>Semana 15</button>
                <button onClick={() => { setNsemana('16') }}>Semana 16</button>
            </div>

            <div className='regis'>
                <button onClick={tomarAsistencia}>Confirmar registro de Asistencia</button>
            </div>

            <div className='tablecontaine'>
                <h3>Asistencia Semana {nsemana}</h3>
                <table className='mitable'>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Asistió</th>
                            <th>No Asistió</th>
                        </tr>
                    </thead>
                    <tbody>
                        {alumnos.map((alumno) => (
                            <tr key={alumno._id}>
                                <td>{alumno.nombre}</td>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={diccionario[alumno._id] === '0'}
                                        onChange={() => handleCheckboxChangeAsistio(alumno._id)}
                                    />
                                </td>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={diccionario[alumno._id] === '1'}
                                        onChange={() => handleCheckboxChangeFalto(alumno._id)}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

        </div>
    );
};

export default Lista;
