# Utiliza una imagen base con Node.js
FROM node:14

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación al directorio de trabajo
COPY . .

# Instala las dependencias
RUN npm install

# Construye la aplicación React para producción
RUN npm run build



# Expone el puerto 3000 en el contenedor
EXPOSE 3000

# Comando para ejecutar la aplicación al iniciar el contenedor
CMD ["npm", "start"]
