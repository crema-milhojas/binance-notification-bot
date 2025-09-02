FROM python:3.13.3

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto usado por la aplicación
EXPOSE 9001

# Establece el comando por defecto (comentado si lo manejarás desde GitHub Actions)
# CMD ["python", "main.py"]
