"""
      ██╗███╗   ███╗ ██████╗
      ██║████╗ ████║██╔════╝
      ██║██╔████╔██║██║
 ██   ██║██║╚██╔╝██║██║    
 ╚█████╔╝██║ ╚═╝ ██║╚██████╗
  ╚════╝ ╚═╝     ╚═╝ ╚═════╝
"""
import sys
import os
import time
import numpy as np

# Interfaz gráfica
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox)
from PyQt5.QtCore import Qt

# Motores 3D y BIM
import pyvista as pv
from pyvistaqt import QtInteractor
import ifcopenshell
import ifcopenshell.geom

class VisorIFC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor BIM - IFC")
        self.setGeometry(100, 100, 1024, 768) # Tamaño inicial de la ventana

        # Contenedor principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout(self.central_widget)

        # --- BARRA SUPERIOR (Botones) ---
        self.layout_botones = QHBoxLayout()

        self.btn_cargar = QPushButton("📂 Cargar IFC")
        self.btn_cargar.setMinimumHeight(40)
        self.btn_cargar.clicked.connect(self.cargar_ifc)
        self.layout_botones.addWidget(self.btn_cargar)

        self.btn_fondo = QPushButton("🌗 Alternar Fondo (B/N)")
        self.btn_fondo.setMinimumHeight(40)
        self.btn_fondo.clicked.connect(self.alternar_fondo)
        self.btn_fondo.setEnabled(False) # Desactivado hasta que haya un modelo
        self.layout_botones.addWidget(self.btn_fondo)

        self.btn_captura = QPushButton("📸 Captura de Pantalla")
        self.btn_captura.setMinimumHeight(40)
        self.btn_captura.clicked.connect(self.tomar_captura)
        self.btn_captura.setEnabled(False)
        self.layout_botones.addWidget(self.btn_captura)

        self.layout_principal.addLayout(self.layout_botones)

        # --- BARRA DE METADATOS ---
        self.label_info = QLabel("Esperando archivo... Haz clic en 'Cargar IFC'.")
        self.label_info.setStyleSheet("font-weight: bold; color: #333; padding: 5px;")
        self.label_info.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(self.label_info)

        # --- VISOR 3D ---
        # Añadimos el visor de PyVista a la interfaz
        self.plotter = QtInteractor(self.central_widget)
        self.layout_principal.addWidget(self.plotter.interactor)
        self.fondo_es_blanco = True
        self.plotter.set_background('white')

    def alternar_fondo(self):
        """Cambia el fondo del visor 3D entre blanco y gris oscuro"""
        if self.fondo_es_blanco:
            self.plotter.set_background('#222222') # Gris muy oscuro (mejor que negro puro)
            self.fondo_es_blanco = False
        else:
            self.plotter.set_background('white')
            self.fondo_es_blanco = True

    def tomar_captura(self):
        """Abre un diálogo para guardar una imagen de lo que se ve en pantalla"""
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Captura", "captura_modelo.png", "Imágenes PNG (*.png)")
        if ruta_archivo:
            self.plotter.screenshot(ruta_archivo)
            QMessageBox.information(self, "Éxito", f"Captura guardada en:\n{ruta_archivo}")

    def extraer_metadatos(self, archivo_ifc, ruta_archivo):
        """Extrae la información general del modelo IFC"""
        nombre_archivo = os.path.basename(ruta_archivo)
        esquema = archivo_ifc.schema
        
        # Extraer Nombre del Proyecto
        proyectos = archivo_ifc.by_type("IfcProject")
        nombre_proyecto = proyectos[0].Name if (proyectos and proyectos[0].Name) else "Desconocido"

        # Extraer Autor y Fecha de la cabecera (Header) del archivo si existe
        autor = "Desconocido"
        fecha = "Desconocida"
        try:
            cabecera = archivo_ifc.wrapped_data.header.file_name
            if cabecera.author: autor = cabecera.author[0]
            if cabecera.time_stamp: fecha = cabecera.time_stamp
        except:
            pass # Si falla, nos quedamos con los datos por defecto

        info = f"📄 Archivo: {nombre_archivo} | 🏗️ Proyecto: {nombre_proyecto} | ⚙️ Versión: {esquema} | 👤 Autor: {autor} | 📅 Fecha: {fecha}"
        self.label_info.setText(info)

    def cargar_ifc(self):
        """Abre el archivo, extrae datos y renderiza la geometría"""
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo IFC", "", "IFC Files (*.ifc)")
        if not ruta_archivo:
            return

        self.label_info.setText("⏳ Cargando y procesando volúmenes del modelo... Esto puede tardar unos segundos.")
        QApplication.processEvents() # Fuerza a la interfaz a actualizar el texto

        try:
            # 1. Leer el archivo IFC
            archivo_ifc = ifcopenshell.open(ruta_archivo)
            
            # 2. Mostrar datos generales
            self.extraer_metadatos(archivo_ifc, ruta_archivo)

            # 3. Limpiar visor anterior y preparar el bloque 3D
            self.plotter.clear()
            bloques_3d = pv.MultiBlock() # Agrupamos las mallas para mayor rendimiento

            # 4. Configurar el motor de geometría de IfcOpenShell
            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True)

            # 5. Extraer y convertir la geometría de cada producto
            productos = archivo_ifc.by_type("IfcProduct")
            for producto in productos:
                if producto.Representation: # Si el elemento tiene volumen/geometría
                    try:
                        forma = ifcopenshell.geom.create_shape(settings, producto)
                        
                        # Extraer vértices y caras
                        v = np.array(forma.geometry.verts).reshape((-1, 3))
                        f = np.array(forma.geometry.faces).reshape((-1, 3))
                        
                        # PyVista requiere que cada cara indique cuántos puntos tiene (3 para triángulos)
                        caras_pv = np.hstack([np.full((f.shape[0], 1), 3), f]).flatten()
                        
                        malla = pv.PolyData(v, caras_pv)
                        bloques_3d.append(malla)
                    except Exception:
                        pass # Ignoramos elementos abstractos que no se puedan triangular

            # 6. Añadir los volúmenes al visor
            # Color platinium, mostrando las aristas (bordes) para que se parezca a un software BIM real
            self.plotter.add_mesh(bloques_3d, color="#d3d3d3", show_edges=True, edge_color="gray")
            self.plotter.reset_camera()

            # Activar botones
            self.btn_fondo.setEnabled(True)
            self.btn_captura.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar el IFC:\n{str(e)}")
            self.label_info.setText("Error al cargar el archivo.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    visor = VisorIFC()
    visor.show()
    sys.exit(app.exec_())
