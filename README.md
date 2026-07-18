# Visor IFC Ligero (PyQt5 + PyVista) 🏗️👀

![Role](https://img.shields.io/badge/Role-BIM%20%26%20ConTech-007ACC?logo=bim360&style=flat-square)
![Location](https://img.shields.io/badge/Location-A%20Coru%C3%B1a%20%F0%9F%8C%8A-005B94?logo=lighthouse&logoColor=white&style=flat-square)
![Sector](https://img.shields.io/badge/Sector-ConTech%20%7C%20AECO-E65100?logo=construct3&style=flat-square)
![BIM](https://img.shields.io/badge/BIM-IFC%20%2F%20openBIM-009688?style=flat-square)
![Maker](https://img.shields.io/badge/Maker-Software-red?logo=makerbot&style=flat-square)
![Hardware](https://img.shields.io/badge/Hardware---grey?style=flat-square)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&style=flat-square)
![Language](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white&style=flat-square)
![Stars](https://img.shields.io/github/stars/jmcaamanog/visor-ifc-pyvista-COATAC?style=flat-square&color=yellow&logo=github)
![License](https://img.shields.io/github/license/jmcaamanog/visor-ifc-pyvista-COATAC?style=flat-square&color=green)

(Arquitecto Técnico_JMC) Visor BIM ultraligero construido con PyQt5 y PyVista. Carga modelos IFC, extrae metadatos de proyecto y renderiza geometría 3D de alto rendimiento con opciones para capturas de pantalla y temas de fondo.

## 🚀 Características Principales

* **Extracción de Metadatos:** Lee la cabecera del archivo para mostrar instantáneamente el nombre del proyecto, versión del esquema IFC, autor y fecha de exportación.
* **Motor 3D de Alto Rendimiento:** Utiliza `pyvista` combinando las mallas en un `MultiBlock` para renderizar modelos fluidamente, mostrando la geometría en un acabado platino ("#d3d3d3") con las aristas remarcadas para un look BIM profesional.
* **Interfaz Nativa Integrada:** Ventana construida con `PyQt5` que incrusta el visor interactivo (`QtInteractor`) directamente en la aplicación sin abrir ventanas secundarias.
* **Herramientas de Visualización:** Permite alternar el color de fondo del espacio 3D (entre blanco y gris oscuro) para mejorar el contraste visual de los modelos.
* **Captura Rápida:** Función nativa para tomar capturas de pantalla del modelo renderizado y guardarlas directamente en formato PNG.

## 🛠️ Stack Tecnológico

* **PyQt5:** Framework principal para la creación de la interfaz gráfica de usuario y gestión de eventos.
* **PyVista & PyVistaQt:** Motor de renderizado 3D basado en VTK, altamente optimizado para análisis espacial e integración en interfaces Qt.
* **IfcOpenShell:** Librería principal encargada de parsear el archivo IFC y convertir los elementos paramétricos en datos geométricos puros.
* **NumPy:** Procesamiento rápido de matrices para reconstruir y adaptar los vértices y caras a la estructura requerida por PyVista.

## ⚙️ Instalación y Uso

1. Clona este repositorio en tu equipo:
   ```bash
   cd visor-ifc-pyvista

2. Accede al directorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/visor-ifc-pyvista.git](https://github.com/TU_USUARIO/visor-ifc-pyvista.git)

3. Instala las dependencias necesarias:
   ```bash
   pip install PyQt5 pyvista pyvistaqt ifcopenshell numpy

4. Ejecuta el programa:
   ```bash
   python nombre_del_archivo.py

## 👨‍💻 Autor

Jose Manuel Caamaño González | Arquitecto Técnico & BIM Manager.
Digital Product Lead | ConTech & Digital Twin SaaS | BIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)

Hecho con código y café desde A Coruña. ☕

Jose Manuel Caamaño González | [LinkedIn](https://www.linkedin.com/in/jmcaamanog/)
