import os
import sys
import subprocess
from PIL import Image
import multiprocessing
import concurrent.futures

# imporitng noises from the noises folder
from noises.impulse import *
from noises.anisotropic import *
from noises.exponential import *
from noises.flimgrain import *
from noises.gamma import *
from noises.gaussian import *
from noises.pepper import *
from noises.periodic import *
from noises.poisson import *
from noises.rayleigh import *
from noises.speckle import *
from noises.uniform import *
from video.vimpulse import *
from video.vanisotropic import *
from video.vexponential import *
from video.vflimgrain import *
from video.vgamma import *
from video.vgaussian import *
from video.vpepper import *
from video.vperiodic import *
from video.vpoisson import *
from video.vrayleigh import *
from video.vspeckle import *
from video.vuniform import *

# importing libraries for PyQt5

from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
from PIL import Image
from collections import Counter

# data for the project
flag_hover = False
show_name = False
folder_dir = "/output"
open_folder_when_done = False
show_preview = True
last_refreshed = 0
width = 256
height = 512
get_current_label = {}
sepearator = "-"


def count_files():
    """
    Counts the number of files in a specified directory and stores the count in a global variable.
    """
    try:
        os.mkdir(os.getcwd() + "/output")
        os.mkdir(os.getcwd() + "/output/thumbnail_dir/")

    except:
        pass
    lis = []
    for image in os.listdir(os.getcwd() + folder_dir):
        image = str(image)
        k = image[: image.rfind(sepearator)]
        lis.append(k)
    get_current_label = Counter(lis)


count_files()


def save_image_generated(generated_image, label):
    """
    Saves the generated image with a specific label and updates the count of images for that label.
    """
    get_current_label[label] = get_current_label.get(label, 0) + 1
    output_filename = f"output/{label}{sepearator}{get_current_label[label]}.jpg"
    cv2.imwrite(output_filename, generated_image)


def get_first_frame(video_path, output_path):
    """
    Extracts the first frame from a video file and saves it to a specified path.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
        cap.release()
        print(f"First frame saved as {output_path}")
        return
    else:
        print("Error: Could not read the first frame")
    cap.release()


def create_thumbnail(input_file, output_filename):
    """
    Creates a thumbnail for an input file (image or video) and saves it with a specified filename.
    """
    if not os.path.exists(output_filename):
        if isimage(input_file):
            image = Image.open(input_file)
            MAX_SIZE = (height, width)
            image.thumbnail(MAX_SIZE)
            image.save(output_filename)
        elif isvideo(input_file):
            m = output_filename.find(".mp4")
            output_filename = output_filename[:m] + "__vid__.jpg"
            # create_thumbnail(input_file,output_filename)
            get_first_frame(input_file, output_filename)


def isimage(image):
    """
    Checks if the file is an image based on its extension.
    """
    return image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")


def isvideo(video):
    """
    Checks if the file is a video based on its extension.
    """
    return video.endswith(".mp4")


class HoverLabel(QLabel):
    def __init__(self, parent=None):
        """
        Initializes a label that changes appearance on hover.
        """
        QLabel.__init__(self, parent)
        self.setStyleSheet(
            "QLabel:hover { border: 2px solid #e94560; border-radius: 8px; }"
        )
        self.setAlignment(Qt.AlignCenter)

    def enterEvent(self, event):
        """
        Handles the mouse entering the label area, enlarging the label.
        """
        if flag_hover:
            pixmap = self.pixmap()
            global width, height
            if pixmap:
                scaled_pixmap = pixmap.scaled(
                    width * 2, height * 2, Qt.KeepAspectRatio, Qt.FastTransformation
                )
                self.setPixmap(scaled_pixmap)
                self.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            self.setFixedSize(width * 2, height * 2)

    def leaveEvent(self, event):
        """
        Handles the mouse leaving the label area, restoring the label size.
        """
        if flag_hover:
            pixmap = QPixmap()
            pixmap = self.pixmap()
            global width, height
            if pixmap:
                scaled_pixmap = pixmap.scaled(
                    width, height, Qt.KeepAspectRatio, Qt.FastTransformation
                )
                self.setPixmap(scaled_pixmap)
                self.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            self.setFixedSize(width, height)


class ImageLabel(QLabel):
    def __init__(self):
        """
        Initializes a label designed for displaying images with a specific style.
        """
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n")
        self.setStyleSheet(
            "color: #e0e0e0;"
            "width: 500px;"
            "background-color: #1a1a2e;"
            "border-style: dashed;"
            "border-width: 3px;"
            "border-color: #0f3460;"
            "border-radius: 12px"
        )

    def setPixmap(self, image):
        """
        Sets the pixmap of the label to the provided image.
        """
        super().setPixmap(image)


noises = [
    "Impulse",
    "Gaussian",
    "Periodic",
    "Speckle",
    "Anisotropic",
    "Exponential",
    "Flimgrain",
    "Gamma",
    "Pepper",
    "Poisson",
    "Rayleigh",
    "Uniform",
]


class Project(QWidget):
    def test_multi_processing(self):
        """
        Prints the number of CPU cores available for multiprocessing.
        """
        print("Using", multiprocessing.cpu_count(), "CPU cores")

    def __getstate__(self):
        """
        Returns the state of the object for serialization.
        """
        return {"some_data": self.addedimages}

    def __setstate__(self, state):
        """
        Restores the state of the object from serialization.
        """
        self.addedimages = state["some_data"]

    def __init__(self):
        """
        Initializes the main project widget, setting up UI and accepting drops.
        """
        super().__init__()
        self.intitalizeUI()
        self.setAcceptDrops(True)

    def intitalizeUI(self):
        """
        Initializes the user interface of the project widget.

        List of items in the function:
        Initialize the main container layout
        Create and configure the 'Generate' button
        Connect button click to submit function
        Create and configure the 'Add images' button
        Connect button click to add_image function
        Create and configure the 'Identify' button
        Connect button click to on_stateChanged function
        Store buttons in a list for future reference or manipulation
        Set up layout for buttons using QHBoxLayout for horizontal alignment
        Add 'Generate' button to layout
        Add 'Add images' button to layout
        Add 'Identify' button to layout
        Add button layout to the main container layout
        Finalize UI setup by setting the main layout of the widget
        Set window title
        Set window size and position
        """
        self.test_multi_processing()
        self.setWindowTitle("Image Augment")
        self.addedimages = []
        self.chkbxs = []
        self.labels = []
        self.buttons = []
        self.d_label = {}
        self.d_lab = {}
        # self.move(0,0)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        slider_one = {
            "Gaussian",
            "Gamma",
            "Flimgrain",
            "Pepper",
            "Poisson",
            "Speckle",
            "Uniform",
        }
        slider_two = {"Anisotropic", "Periodic"}
        slider_no = {"Impulse", "Rayleigh"}

        self.main_container = QHBoxLayout()

        self.photoViewer = ImageLabel()
        self.photoViewer.setMinimumWidth(300)
        self.labels.append(self.photoViewer)
        self.main_container.addWidget(self.photoViewer)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        self.gird_generated = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setStyleSheet("background-color: #16213e; border-radius: 8px;")

        self.add_image_grid()

        self.main_container.addWidget(self.scrollArea)

        self.scrollArea.setMinimumWidth(1000)

        button_gen = QPushButton("Generate", self)
        self.labels.append(button_gen)
        button_gen.clicked.connect(self.submit)
        self.buttons.append(button_gen)

        button_add = QPushButton("Add images", self)
        self.labels.append(button_add)
        button_add.clicked.connect(self.add_image)
        self.buttons.append(button_add)

        button_iden = QPushButton("Add all noises", self)
        self.labels.append(button_iden)
        button_iden.clicked.connect(self.on_stateChanged)
        button_iden.setStyleSheet("background-color : white")

        button_inv = QPushButton("Invert Selection", self)
        self.labels.append(button_inv)
        button_inv.clicked.connect(self.invertSelection)
        button_inv.setStyleSheet("background-color : white")

        self.b1 = QCheckBox("Hover over preview")
        self.b1.stateChanged.connect(lambda: self.settings(self.b1))
        self.b2 = QCheckBox("Show preview name")
        self.b2.stateChanged.connect(lambda: self.settings(self.b2))
        self.b4 = QCheckBox("Open Output folder when done")
        self.b4.stateChanged.connect(lambda: self.settings(self.b4))
        show_preview = True

        self.buttons.append(button_iden)
        self.buttons.append(button_inv)

        title_h_box_a = QHBoxLayout()
        title_h_box_a.addWidget(button_gen)
        title_h_box_a.addWidget(button_add)
        title_h_box_b = QHBoxLayout()
        title_h_box_b.addWidget(button_iden)
        title_h_box_b.addWidget(button_inv)

        title_h_box_c = QVBoxLayout()
        title_h_box_c.addWidget(self.b1)
        title_h_box_c.addWidget(self.b2)
        title_h_box_c.addWidget(self.b4)

        title_v_box = QVBoxLayout()
        title_v_box.setAlignment(Qt.AlignCenter)
        title_text_lable = QHBoxLayout()
        text_noise = QLabel(self)
        text_noise.setText("Select noises to add")
        self.labels.append(text_noise)
        refresh_image = QPushButton("Refresh preview")
        self.buttons.append(refresh_image)
        refresh_image.clicked.connect(self.refresh)
        title_text_lable.addWidget(text_noise)
        title_text_lable.addWidget(refresh_image)

        title_v_box.addLayout(title_text_lable)
        title_v_box.addStretch(10)

        def valuechange(self, size, clabel):
            mm = self.d_lab[clabel]
            size = round(size / 100, 2)
            self.d_label[mm.lower()] = size
            size = str(size)
            clabel.setText(size)

        for label in noises:
            layout = QHBoxLayout()
            cslider = QSlider(Qt.Horizontal)
            cslider.setRange(1, 100)
            cslider.setValue(50)
            cslider.setTickPosition(QSlider.TicksBelow)
            cslider.setTickInterval(1)
            clabel = QLabel("")

            checkbox = QCheckBox(label, self)
            self.labels.append(checkbox)
            self.chkbxs.append(checkbox)

            self.d_lab[clabel] = label
            cslider.valueChanged.connect(
                lambda value, clabel=clabel: valuechange(self, value, clabel)
            )
            layout.addWidget(checkbox)
            layout.addWidget(cslider)
            layout.addWidget(clabel)

            title_v_box.addLayout(layout)
            title_v_box.setStretchFactor(layout, 0)
            title_v_box.addStretch(10)
            liders = {}

            def updateLabel(label, value):
                # print(liders)
                # print(liders[label])
                liders[label].setText(str(value))

        title_v_box.addLayout(title_h_box_a)
        title_v_box.addLayout(title_h_box_b)
        title_v_box.addLayout(title_h_box_c)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #0f3460;
                border-radius: 8px;
                background-color: #16213e;
                text-align: center;
                color: #e0e0e0;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e94560, stop:1 #0f3460);
                border-radius: 6px;
            }
        """)
        title_v_box.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(
            "color: #e94560; font-size: 12pt; padding: 5px;"
        )
        self.status_label.setAlignment(Qt.AlignCenter)
        title_v_box.addWidget(self.status_label)

        title_v_box.setStretchFactor(title_h_box_a, 1)
        title_v_box.setStretchFactor(title_h_box_b, 1)
        title_v_box.setStretchFactor(title_h_box_c, 1)
        self.main_container.setStretchFactor(title_v_box, 1)
        title_v_box.setStretchFactor(title_h_box_b, 1)
        title_v_box.setStretchFactor(title_h_box_c, 1)
        self.main_container.setStretchFactor(title_v_box, 1)

        self.main_container.addLayout(title_v_box)
        self.main_container.setStretchFactor(title_v_box, 1)

        self.styles()
        self.setLayout(self.main_container)
        self.show()

    def settings(self, b):
        m = b.text()
        global show_preview, flag_hover, show_name
        if m == "Hover over preview":
            flag_hover = b.isChecked()
        elif m == "Show preview name":
            show_name = b.isChecked()
        elif m == "Show preview":
            show_preview = b.isChecked()
        elif m == "Open Output folder when done":
            open_folder_when_done = b.isChecked()

    def refresh(self):
        global last_refreshed
        if time.time() - last_refreshed > 2:
            self.add_image_grid()
            last_refreshed = time.time()

    def identify(self):
        self.file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "/Users/user_name/Desktop/",
            "All Files (*);;Text Files (*.txt)",
        )

    def submit(self):
        """
                Handles the 'Generate' button click event.
        This function should contain the logic to initiate whatever process is intended to be triggered by the 'Generate' button.
        For example, if this is part of an image processing application, this function could start the process of generating new images based on user inputs or selected parameters.
        """
        if len(self.addedimages) == 0:
            self.status_label.setText("⚠️ Please add images first!")
            ret = QMessageBox.question(
                self, "Critical", "Add Images!", QMessageBox.Ok, QMessageBox.Cancel
            )
            return

        import timeit

        start = timeit.default_timer()

        # Count selected noises and total operations
        selected_noises = [w.text().lower() for w in self.chkbxs if w.isChecked()]
        total_ops = len(selected_noises) * len(self.addedimages)

        if total_ops == 0:
            self.status_label.setText("⚠️ Select at least one noise type!")
            return

        self.progress_bar.setMaximum(total_ops)
        self.progress_bar.setValue(0)
        current_op = 0

        for noise_name in selected_noises:
            value_im = self.d_label.get(noise_name, 0.50)

            for idx, image in enumerate(self.addedimages):
                if len(image) > 0:
                    self.status_label.setText(
                        f"Processing {noise_name} on image {idx + 1}/{len(self.addedimages)}..."
                    )
                    QApplication.processEvents()

                    if isimage(image):
                        result = globals()[noise_name](image, value_im)
                        save_image_generated(result, noise_name)
                    else:
                        globals()["v" + noise_name](image, idx + 1, value_im)

                    current_op += 1
                    self.progress_bar.setValue(current_op)
                    QApplication.processEvents()

        stop = timeit.default_timer()
        elapsed = stop - start
        self.status_label.setText(f"✓ Completed in {elapsed:.2f}s ({total_ops} images)")
        self.progress_bar.setValue(total_ops)

        if open_folder_when_done:
            to_open = os.path.abspath(folder_dir)
            subprocess.Popen(r"explorer " + to_open)
        self.refresh()

    def on_stateChanged(self, state):
        """
        Handles the 'Add all noises' button click event.
        """
        for widget in self.chkbxs:
            widget.setChecked(True)

    def invertSelection(self, state):
        for widget in self.chkbxs:
            if widget.isChecked():
                widget.setChecked(False)
            else:
                widget.setChecked(True)

    def styles(self):
        try:
            font_loc = "fonts/GothamMedium_1.ttf"
            font_id = QFontDatabase.addApplicationFont(font_loc)
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            font.setPointSize(8)
            font.setItalic(True)

            self.setStyleSheet(
                "background-color: #1a1a2e;"
                "color: #e0e0e0;"
                "font-size: 14pt; font-family: {}; font-weight: normal;".format(
                    font_family
                )
            )
            for widget in self.labels:
                widget.setFont(font)

        except:
            self.setStyleSheet(
                "background-color: #1a1a2e;color: #e0e0e0;font-size: 14pt;"
            )
        finally:
            for widget in self.buttons:
                widget.setStyleSheet("""
            QPushButton {
                background-color: #0f3460;
                color: #e0e0e0;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #e94560;
                color: white;
            }
            """)

    def add_image_grid(self):
        """
        Populates the grid with image placeholders or thumbnails.
        """
        if show_preview:
            isExist = os.path.exists(folder_dir)
            if not isExist:
                os.makedirs(folder_dir)

            while self.gird_generated.count():
                child = self.gird_generated.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            try:
                i = 0
                c = 0
                max_r = 3
                r = 0
                for image in os.listdir(os.getcwd() + folder_dir):
                    output_loc = os.getcwd() + "/" + f"output/thumbnail_dir/{image}"
                    if not os.path.exists(output_loc):
                        thumb_dir = os.getcwd() + folder_dir + "thumbnail_dir"
                        label_name = os.getcwd() + folder_dir + "/" + str(image)
                        try:
                            create_thumbnail(label_name, output_loc)
                        except Exception as e:
                            print(e, "Unable to add thumbnail for", image)
                for image in os.listdir(os.getcwd() + "/output/thumbnail_dir/"):
                    k = ""
                    if image.find("__vid__") > 0:
                        k = image.replace("__vid__", "")
                        k = k.replace(".jpg", ".mp4")

                    if os.path.exists(os.getcwd() + "/output/" + image) or k:
                        small_grid = QGridLayout()
                        self.name_image = os.path.join(
                            os.getcwd() + "/output/thumbnail_dir/", image
                        )
                        # print(image)
                        if image.find("__vid__") > 0:
                            k = image.replace("__vid__", "")
                            image = k.replace(".jpg", ".mp4")

                        self.text_def = QLabel(self)
                        self.word_image = HoverLabel()
                        self.labels.append(self.word_image)
                        pixmap = QPixmap(self.name_image)
                        self.text_def.setText(image)
                        self.text_def.setFixedHeight(40)
                        self.text_def.setStyleSheet(
                            "background-color:#6096B4;"
                            "font-size: 10pt; font-weight: italic;"
                        )
                        self.word_image.setPixmap(pixmap)

                        def create_image_handler(image_name):
                            def handler(event):
                                self.openImage(os.getcwd() + "/output/" + image_name)

                            return handler

                        self.word_image.mousePressEvent = create_image_handler(image)

                        small_grid.addWidget(self.word_image, 0, 0)
                        if show_name:
                            small_grid.addWidget(self.text_def, 1, 0)
                        self.gird_generated.addLayout(small_grid, r, i)

                        i = i + 1
                        if i == max_r:
                            r += 1
                            i = 0

                        self.gird_generated.update()
                        self.gird_generated.activate()
                    self.gird_generated.update()
                    self.gird_generated.activate()
                self.gird_generated.update()
                self.gird_generated.activate()
            except Exception as e:
                print("Image not found.", e)
        else:
            self.deleteItemsOfLayout(self.gird_generated)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def add_image(self):
        """
        Handles the 'Add images' button click event.
        """
        self.file_names, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            "/Users/user_name/Desktop/",
            "All Files (*);;Text Files (*.txt)",
        )
        if len(self.file_names) == 0:
            self.addedimages.append(self.file_names)
        else:
            self.addedimages += self.file_names

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handle drop event to add dropped images to the grid.

        Parameters:
        - event (QDropEvent): The drop event.
        """
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.addedimages.append(file_path)
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(
            self.photoViewer.width(),
            self.photoViewer.height(),
            Qt.KeepAspectRatio,
            Qt.FastTransformation,
        )
        pixmap.mousePressEvent = self.openImage
        self.photoViewer.setPixmap(pixmap)

    def openImage(self, file_dir):
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_dir))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        id = QFontDatabase.addApplicationFont("fonts/Cubano.ttf")
        families = QFontDatabase.applicationFontFamilies(id)[0]
    except:
        pass
    window = Project()
    sys.exit(app.exec_())
