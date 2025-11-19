# Chatbot con PDF usando Ollama

Este proyecto es una aplicación de chatbot interactiva construida con Streamlit que permite cargar un archivo PDF y hacer preguntas sobre su contenido. Utiliza Ollama para generar embeddings y respuestas basadas en modelos de lenguaje grandes (LLM).

## Características
- Carga de archivos PDF
- Procesamiento de texto con divisiones inteligentes
- Búsqueda semántica usando embeddings
- Respuestas generadas por IA basadas únicamente en el contenido del PDF
- Interfaz de chat intuitiva

## Requisitos Previos
- Python 3.8 o superior instalado
- Ollama instalado en tu sistema (o Docker para alternativa)

## Pasos para Ejecutar el Proyecto

### 1. Instalar Ollama
Descarga e instala Ollama desde el sitio oficial: [https://ollama.ai/](https://ollama.ai/)

### 2. Iniciar Sesión en Ollama (Necesario)
Debes iniciar sesión con tu cuenta de Ollama para acceder a modelos en la nube y evitar el uso de recursos locales. Esto es requerido para el modelo "gpt-oss:120b-cloud" utilizado en el proyecto:
```bash
ollama signin
```

### 3. Descargar los Modelos Necesarios
Este proyecto utiliza dos modelos específicos de Ollama. Descárgalos ejecutando:
```bash
ollama pull embeddinggemma
ollama pull gpt-oss:120b-cloud
```

### 4. Instalar las Dependencias del Proyecto
Clona o descarga este repositorio. Crea un entorno virtual y activa, luego instala las dependencias:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Iniciar el Servidor de Ollama
Antes de ejecutar la aplicación, asegúrate de que Ollama esté corriendo en segundo plano:
```bash
ollama serve
```
Esto iniciará el servidor en `http://localhost:11434`.

### 6. Ejecutar el Proyecto
Una vez que Ollama esté corriendo, ejecuta la aplicación Streamlit:
```bash
streamlit run embedding-ollama.py
```

La aplicación se abrirá en tu navegador web predeterminado. Sube un PDF desde la barra lateral y comienza a hacer preguntas sobre su contenido.

## Alternativa: Ejecutar con Docker (Sin Instalar Ollama Localmente)

Si prefieres no instalar Ollama en tu sistema, puedes usar Docker para ejecutar Ollama y los modelos.

### Requisitos Adicionales
- Docker instalado y ejecutándose en tu sistema

### Pasos Alternativos

#### 1. Ejecutar Ollama en Docker
Ejecuta el contenedor de Ollama en segundo plano:
```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
```

#### 2. Iniciar Sesión en Ollama (Necesario)
Desde el contenedor, inicia sesión:
```bash
docker exec -it ollama ollama signin
```

#### 3. Descargar los Modelos Necesarios
Descarga los modelos dentro del contenedor:
```bash
docker exec -it ollama ollama pull embeddinggemma
docker exec -it ollama ollama pull gpt-oss:120b-cloud
```

#### 4. Instalar las Dependencias del Proyecto
Clona o descarga este repositorio e instala las dependencias usando pip:
```bash
pip install -r requirements.txt
```

#### 5. Ejecutar el Proyecto
Ejecuta la aplicación Streamlit (el servidor de Ollama ya está corriendo en Docker):
```bash
streamlit run embedding-ollama.py
```

## Notas Adicionales
- Asegúrate de que el puerto 11434 no esté ocupado por otra aplicación.
- Si encuentras problemas con los modelos, verifica que Ollama esté actualizado y que los modelos se hayan descargado correctamente.
- La aplicación procesa el PDF al cargarlo por primera vez y crea embeddings en memoria para búsquedas rápidas.

## Solución de Problemas
- Si Streamlit no se ejecuta, verifica que Python esté en tu PATH.
- Si hay errores de conexión con Ollama, confirma que `ollama serve` esté ejecutándose.
- Para modelos grandes como "gpt-oss:120b-cloud", asegúrate de tener suficiente espacio en disco y memoria RAM.