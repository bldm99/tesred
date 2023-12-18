
import axios from 'axios';

const URLdesrrollo = "https://girapi.bladimirchipana.repl.co/listalumno"
const alumnos = 'https://girapi.bladimirchipana.repl.co/alumnos?_idUsuario=6531d08612ec096c58717b97&_idRiesgo=657f1edfb8453f2c73ddf88c'

const apiURL = "http://api:5000"; 
//const apiURL = "http://ip172-18-0-15-clvp0fdnp9tg008ijs50-5000.direct.labs.play-with-docker.com/"; 


export const helloword = async () => {
    try {
        const response = await axios.get(apiURL);
        console.log(response.data)
        return response.data
    } catch (error) {
        console.log(error)
    }
}


export const getAlumnos = async (xset) => {
    try {
        const response = await axios.get(alumnos);
        xset(response.data)
        return response.data
    } catch (error) {
        console.log(error)
    }

}

export const postLista = async (alumnoId ,numero, valor) => {
    try {
        const semana = "sem";
        const data = {
            _idUsuario: "6531d08612ec096c58717b97",
            _idRiesgo: "65754cdbd6a61db3295d8f3b",
            alumnoId,
        };

        // Crear la propiedad dinámica nombresemana + numero
        data[semana + numero] = valor;

        const response = await axios.post(`${URLdesrrollo}`, data);

        // Puedes imprimir la respuesta si es necesario
        console.log('Asistencia guardada correctamente');
    } catch (error) {
        console.log('Error en la solicitud:', error.message);
        console.log('Respuesta del servidor:', error.response.data);
    }
};
