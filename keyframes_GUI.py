import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, 
                             QMessageBox, QCheckBox, QComboBox)
import subprocess
import os

class KeyframeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_paths = []
        self.output_folder = ""
        self.create_keyframes_folder = False
        self.analize_option = False
        self.linux_option = False

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Generador de Keyframes")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        self.dependencies_button = QPushButton("Comprobar dependencias")
        self.dependencies_button.clicked.connect(self.check_dependencies)
        main_layout.addWidget(self.dependencies_button)

        self.video_label = QLabel("Videos cargados:")
        main_layout.addWidget(self.video_label)

        self.video_list = QListWidget()
        main_layout.addWidget(self.video_list)

        button_layout = QHBoxLayout()
        self.video_button = QPushButton("Agregar")
        self.video_button.clicked.connect(self.browse_videos)
        button_layout.addWidget(self.video_button)

        self.delete_button = QPushButton("Borrar")
        self.delete_button.clicked.connect(self.delete_selected_video)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)

        self.output_layout = QHBoxLayout()
        self.output_label = QLabel("Guardar en:")
        self.output_layout.addWidget(self.output_label)

        self.output_entry = QLineEdit()
        self.output_layout.addWidget(self.output_entry)

        self.output_button = QPushButton("Examinar")
        self.output_button.clicked.connect(self.browse_output)
        self.output_layout.addWidget(self.output_button)
        main_layout.addLayout(self.output_layout)

        self.keyframes_layout = QHBoxLayout()
        self.keyframes_checkbox = QCheckBox("Crear carpeta 'Keyframes'")
        self.keyframes_layout.addWidget(self.keyframes_checkbox)
        main_layout.addLayout(self.keyframes_layout)

        self.metodo_layout = QHBoxLayout()
        self.metodo_label = QLabel("Método:")
        self.metodo_layout.addWidget(self.metodo_label)

        self.metodo_combobox = QComboBox()
        self.metodo_combobox.addItem("Usar WWXD (default)")
        self.metodo_combobox.addItem("Usar Scxvid")
        self.metodo_combobox.addItem("Usar WWXD y Scxvid (recomendado)")
        self.metodo_layout.addWidget(self.metodo_combobox)
        main_layout.addLayout(self.metodo_layout)

        self.autismo_layout = QHBoxLayout()
        self.autismo_label = QLabel("Nivel de autismo:")
        self.autismo_layout.addWidget(self.autismo_label)

        autismo_resolutions = {
            "Automático": 0,
            "640x360p": 1,
            "720x480p": 2,
            "1280x720p": 3,
            "1440x810p": 4,
            "1600x900p": 5,
            "1920x1080p": 6,
            "3840x2160p": 7
        }

        self.autismo_combobox = QComboBox()
        for resolution, level in autismo_resolutions.items():
            self.autismo_combobox.addItem(resolution, level)
        self.autismo_layout.addWidget(self.autismo_combobox)
        main_layout.addLayout(self.autismo_layout)

        analyze_linux_rescribir_layout = QHBoxLayout()

        analyze_layout = QVBoxLayout()
        self.analyze_checkbox = QCheckBox("Analizar")
        analyze_layout.addWidget(self.analyze_checkbox)

        linux_layout = QVBoxLayout()
        self.linux_checkbox = QCheckBox("Linux")
        linux_layout.addWidget(self.linux_checkbox)

        rescribir_layout = QVBoxLayout()
        self.rescribir_checkox = QCheckBox("Reescribir")
        rescribir_layout.addWidget(self.rescribir_checkox)

        analyze_linux_rescribir_layout.addLayout(analyze_layout)
        analyze_linux_rescribir_layout.addLayout(linux_layout)
        analyze_linux_rescribir_layout.addLayout(rescribir_layout)
        main_layout.addLayout(analyze_linux_rescribir_layout)

        generate_layout = QHBoxLayout()
        self.generate_button = QPushButton("¡GENERAR!")
        self.generate_button.clicked.connect(self.start_generation)
        generate_layout.addWidget(self.generate_button)
        main_layout.addLayout(generate_layout)

        main_layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Conectar la señal 'activated' del ComboBox de autismo a la función de manejo
        self.autismo_combobox.activated.connect(self.handle_autismo_combobox)

    def handle_autismo_combobox(self):
        # Obtener el nivel de autismo seleccionado del ComboBox de autismo
        selected_index = self.autismo_combobox.currentIndex()
        autismo_level = self.autismo_combobox.itemData(selected_index)

        # Actualizar la variable autismo_param
        self.autismo_param = ["--autismo", str(autismo_level)]

    def browse_videos(self):
        video_paths, _ = QFileDialog.getOpenFileNames(self, "Seleccione videos", "", "Archivos de video (*.mp4 *.m2ts *.mkv)")
        for video_path in video_paths:
            self.video_paths.append(video_path)
            item = QListWidgetItem(os.path.basename(video_path))
            self.video_list.addItem(item)

    def delete_selected_video(self):
        selected_items = self.video_list.selectedItems()
        for item in selected_items:
            row = self.video_list.row(item)
            self.video_list.takeItem(row)
            del self.video_paths[row]

    def browse_output(self):
        output_folder = QFileDialog.getExistingDirectory(self, "Seleccione una carpeta de salida")
        self.output_entry.setText(output_folder)
        self.output_folder = output_folder

    def check_dependencies(self):
        programs = ['ffmpeg', 'ffprobe', 'python']
        missing_programs = []

        for program in programs:
            try:
                subprocess.run([program, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FileNotFoundError:
                missing_programs.append(program)

        vs_modules = ['wwxd', 'scxvid', 'ffms2', 'fmtc', 'resize', 'lsmas']
        missing_modules = []

        for module in vs_modules:
            try:
                import vapoursynth as vs
                getattr(vs.core, module)
            except (ImportError, AttributeError):
                missing_modules.append(module)

        error_message = ""

        if missing_programs:
            error_message += f"Los siguientes programas no están en el PATH: {', '.join(missing_programs)}\n"

        if missing_modules:
            error_message += f"Los siguientes módulos de VapourSynth no están disponibles: {', '.join(missing_modules)}"

        if error_message:
            QMessageBox.critical(self, "Dependencias faltantes", error_message)
        else:
            QMessageBox.information(self, "Dependencias", "Todas las dependencias están presentes.")

    def start_generation(self):
        if not self.video_paths:
            QMessageBox.critical(self, "Error", "Seleccione al menos un video.")
            return

        self.create_keyframes_folder = self.keyframes_checkbox.isChecked()
        self.output_folder = self.output_entry.text()

        metodo = self.metodo_combobox.currentText()
        if metodo == "Usar Scxvid":
            metodo_params = "--use-scxvid"
        elif metodo == "Usar WWXD y Scxvid (recomendado)":
            metodo_params = "--use-doble"
        else:
            metodo_params = ""

        autismo_level = self.autismo_combobox.currentData()  # Obtener el nivel de autismo seleccionado

        for video_path in self.video_paths:
            video_name = os.path.basename(video_path)

            if self.create_keyframes_folder:
                if not self.output_folder:
                    self.output_folder = os.path.dirname(video_path)
                keyframes_folder_path = os.path.join(self.output_folder, "Keyframes")
                os.makedirs(keyframes_folder_path, exist_ok=True)
                output_file_path = os.path.join(keyframes_folder_path, f"{os.path.splitext(video_name)[0]}_keyframes.txt")
            else:
                if not self.output_folder:
                    self.output_folder = os.path.dirname(video_path)
                output_file_path = os.path.join(self.output_folder, f"{os.path.splitext(video_name)[0]}_keyframes.txt")

            command = ["python", "keyframes.py", "--clip", video_path]

            if self.output_folder:
                command.extend(["--out-file", output_file_path])

            if self.analyze_checkbox.isChecked():
                command.append("--analize")

            if self.linux_checkbox.isChecked():
                command.append("--linux")

            if self.rescribir_checkox.isChecked():
                command.append("--reescribir")

            if metodo_params != "":
                command.append(metodo_params)

            command.extend(["--autismo", str(autismo_level)])
                
              
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Error al generar keyframes para '{video_name}': {e}")
                return

        QMessageBox.information(self, "Generación de keyframes completa", "La generación de keyframes se completó exitosamente.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyframeGeneratorApp()
    window.show()
    sys.exit(app.exec_())
