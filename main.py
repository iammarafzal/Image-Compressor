import sys
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Enable for creating EXE file
# import sys, os
# os.chdir(sys._MEIPASS)


class App (QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 600
        self.statusBar().showMessage("Message:")
        self.statusBar().setObjectName("status")
        self.image_width = 0
        self.compress_width = 0
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        stylesheet = ""
        with open("design.css", "r") as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # ---------------------------- Main Window ----------------------------
        self.single_bubble = QFrame(self)
        self.single_bubble.setObjectName("bubble")
        self.single_bubble.move(50, 100)
        self.single_bubble.mousePressEvent = self.single_bubble_clicked

        self.single_bubble_heading = QLabel(self.single_bubble)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(90, 8)

        self.single_bubble_para = QLabel(self.single_bubble)
        self.single_bubble_para.setObjectName("bubble_para")
        self.single_bubble_para.setText("Click here to compress single image")
        self.single_bubble_para.move(25, 32)


        self.dir_bubble = QFrame(self)
        self.dir_bubble.setObjectName("bubble")
        self.dir_bubble.setGeometry(50, 275, 300, 100)
        self.dir_bubble.mousePressEvent = self.dir_bubble_clicked

        self.dir_bubble_heading = QLabel(self.dir_bubble)
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.setText("Compress Multiple Images")
        self.dir_bubble_heading.move(55, 8)

        self.dir_bubble_para = QLabel(self.dir_bubble)
        self.dir_bubble_para.setObjectName("bubble_para")
        self.dir_bubble_para.setText("Want to compress multiple images at once? Select the folder and get compressed images in another folder")
        self.dir_bubble_para.setWordWrap(True)
        self.dir_bubble_para.setGeometry(15, 32, 270, 60)
        
        # ---------------------------- Single Bubble Expanded ----------------------------
        self.single_bubble_expanded = QFrame(self)
        self.single_bubble_expanded.setObjectName("bubble_expanded")
        self.single_bubble_expanded.move(50, 100)
        self.single_bubble_expanded.setVisible(False)

        self.back_arrow_s = QLabel(self.single_bubble_expanded)
        self.back_arrow_s.setObjectName("back_arrow")
        self.back_arrow_s.move(20, 5)
        self.back_arrow_s.setTextFormat(Qt.RichText)
        self.back_arrow_s.setText("&#8592")
        self.back_arrow_s.mousePressEvent = self.back_arrow_clicked

        self.single_bubble_heading = QLabel(self.single_bubble_expanded)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(90, 8)

        self.select_image_label = QLabel(self.single_bubble_expanded)
        self.select_image_label.setObjectName("bubble_para")
        self.select_image_label.setText("Choose Image")
        self.select_image_label.move(30, 50)

        self.image_path = QLineEdit(self.single_bubble_expanded)
        self.image_path.setObjectName("path_text")
        self.image_path.move(60, 85)

        self.browse_button = QPushButton(self.single_bubble_expanded)
        self.browse_button.setText("...")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.move(240, 85)

        self.select_image_quality = QLabel(self.single_bubble_expanded)
        self.select_image_quality.setObjectName("bubble_para")
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.move(30, 130)

        self.quality_path = QLineEdit(self.single_bubble_expanded)
        self.quality_path.setObjectName("quality_path_text")
        self.quality_path.move(60, 160)

        self.quality_combo = QComboBox(self.single_bubble_expanded)
        self.quality_combo.setObjectName("quality_combo")
        self.quality_combo.addItem("High")
        self.quality_combo.addItem("Medium")
        self.quality_combo.addItem("Low")
        self.quality_combo.currentIndexChanged.connect(self.quality_current_value)
        self.quality_combo.move(170, 160)

        self.compress_image = QPushButton(self.single_bubble_expanded)
        self.compress_image.setText("Compress")
        self.compress_image.setObjectName("compress_button")
        self.compress_image.clicked.connect(self.resize_pic)
        self.compress_image.move(110, 240)

        # ---------------------------- End Single Bubble Expanded ----------------------------
        # ---------------------------- Dir Bubble Expanded -----------------------------------
        self.dir_bubble_expanded = QFrame(self)
        self.dir_bubble_expanded.setObjectName("bubble_expanded")
        self.dir_bubble_expanded.move(50, 100)
        self.dir_bubble_expanded.setVisible(False)

        self.back_arrow_d = QLabel(self.dir_bubble_expanded)
        self.back_arrow_d.setObjectName("back_arrow")
        self.back_arrow_d.move(10, 10)
        self.back_arrow_d.setTextFormat(Qt.RichText)
        self.back_arrow_d.setText("&#8592")
        self.back_arrow_d.mousePressEvent = self.back_arrow_clicked

        self.single_bubble_heading = QLabel(self.dir_bubble_expanded)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Multiple Images")
        self.single_bubble_heading.move(60, 8)

        self.select_source_label = QLabel(self.dir_bubble_expanded)
        self.select_source_label.setObjectName("bubble_para")
        self.select_source_label.setText("Choose Folder")
        self.select_source_label.move(30, 50)

        self.source_path = QLineEdit(self.dir_bubble_expanded)
        self.source_path.setObjectName("path_text")
        self.source_path.move(60, 85)

        self.browse_source_button = QPushButton(self.dir_bubble_expanded)
        self.browse_source_button.setText("...")
        self.browse_source_button.setObjectName("browse_button")
        self.browse_source_button.clicked.connect(self.select_folder_source)
        self.browse_source_button.move(240, 85)

        self.select_dest_label = QLabel(self.dir_bubble_expanded)
        self.select_dest_label.setObjectName("bubble_para")
        self.select_dest_label.setText("Choose Destination Folder")
        self.select_dest_label.move(30, 130)

        self.dest_path = QLineEdit(self.dir_bubble_expanded)
        self.dest_path.setObjectName("path_text")
        self.dest_path.move(60, 160)

        self.browse_dest_button = QPushButton(self.dir_bubble_expanded)
        self.browse_dest_button.setText("...")
        self.browse_dest_button.setObjectName("browse_button")
        self.browse_dest_button.clicked.connect(self.select_folder_dest)
        self.browse_dest_button.move(240, 160)

        self.select_dir_quality = QLabel(self.dir_bubble_expanded)
        self.select_dir_quality.setObjectName("bubble_para")
        self.select_dir_quality.setText("Choose Quality")
        self.select_dir_quality.move(30, 205)

        self.quality_dir_path = QLineEdit(self.dir_bubble_expanded)
        self.quality_dir_path.setObjectName("quality_path_text")
        self.quality_dir_path.move(60, 235)

        self.quality_dir_combo = QComboBox(self.dir_bubble_expanded)
        self.quality_dir_combo.setObjectName("quality_combo")
        self.quality_dir_combo.addItem("High")
        self.quality_dir_combo.addItem("Medium")
        self.quality_dir_combo.addItem("Low")
        self.quality_dir_combo.currentIndexChanged.connect(self.quality_dir_current_value)
        self.quality_dir_combo.move(170, 235)

        self.compress_dir = QPushButton(self.dir_bubble_expanded)
        self.compress_dir.setText("Compress")
        self.compress_dir.setObjectName("compress_button")
        self.compress_dir.clicked.connect(self.resize_dir)
        self.compress_dir.move(110, 290)

        # ---------------------------- End Dir Bubble Expanded ----------------------------

        # ---------------------------- End Main Window -----------------------------------

        self.show()

        # ---------------------------- Functions -----------------------------------------

    def single_bubble_clicked(self, event):
        print("singal bubble clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(True)
        self.dir_bubble_expanded.setVisible(False)

    def dir_bubble_clicked(self, event):
        print("dir bubble clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(True)

    def back_arrow_clicked(self, event):
        self.single_bubble.setVisible(True)
        self.dir_bubble.setVisible(True)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(False)

    def select_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;JPEG (*.jpeg)")
        if fileName:
            print(fileName, _)
            self.image_path.setText(fileName)
            img = Image.open(fileName)
            self.image_width = img.width
            self.quality_path.setText(str(self.image_width))

    def quality_current_value(self):
        # Handle the quality for individual images
        if self.quality_combo.currentText() == "High":
            self.quality_path.setText(str(self.image_width))
            self.compress_width = self.image_width
        elif self.quality_combo.currentText() == "Medium":
            self.quality_path.setText(str(int(self.image_width / 2)))
            self.compress_width = int(self.image_width/2)
        elif self.quality_combo.currentText() == "Low":
            self.quality_path.setText(str(int(self.image_width / 4)))
            self.compress_width = int(self.image_width/4)


    def quality_dir_current_value(self):
        # Handle the quality for directories
        if self.quality_dir_combo.currentText() == "High":
            self.quality_dir_path.setText(str(self.image_width))
            self.compress_width = int(self.image_width)
        elif self.quality_dir_combo.currentText() == "Medium":
            self.quality_dir_path.setText(str(int(self.image_width / 2)))
            self.compress_width = int(self.image_width/2)
        elif self.quality_dir_combo.currentText() == "Low":
            self.quality_dir_path.setText(str(int(self.image_width / 4)))
            self.compress_width = int(self.image_width/4)



    def select_folder_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        self.source_path.setText(folder)
        files = os.listdir(folder)
        first_pic = folder + "/" + files[0]


        for file in files:
            print(file)

        img = Image.open(first_pic)
        self.image_width = img.width
        self.quality_dir_path.setText(str(self.image_width))


    def select_folder_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        self.dest_path.setText(folder)

    def resize_pic(self):
        old_pic = self.image_path.text()

        if old_pic == "":
            self.statusBar().showMessage("Message: Please choose an image")
            return
        print("Original Image Path:", old_pic)
        print("Compressed Width:", self.compress_width)
        directories = old_pic.split("/")
        print("Directories:", directories)
        new_pic = ""

        # Prompting the user for the new image name
        new_pic_name, okPressed = QInputDialog.getText(self, "Save Image as", "Image Name", QLineEdit.Normal, "")
        
        if okPressed and new_pic_name != "":
            # Determining the file extension based on the original image
            if old_pic.lower().endswith(".jpeg"):
                new_pic_name += ".jpeg"
            elif old_pic.lower().endswith(".png"):
                new_pic_name += ".png"
            elif old_pic.lower().endswith(".jpg"):
                new_pic_name += ".jpg"
            else:
                new_pic_name += ".jpeg"  # Default to .jpeg if unknown

            for directory in directories[:-1]:
                new_pic = new_pic + directory + "/"

            new_pic += new_pic_name
            
            print("New Image Path:", new_pic)

            self.compression_code(old_pic, new_pic, int(self.quality_path.text()))
            self.statusBar().showMessage("Message: Compressed")



    def resize_dir(self):
        source_directory = self.source_path.text()
        dest_directory = self.dest_path.text()

        if source_directory == "":
            self.statusBar().showMessage("Message: Please select source directory")
            return
        elif dest_directory == "":
            self.statusBar().showMessage("Message: Please select destination directory")
            return
        
        files = os.listdir(source_directory)
        total_images = len([file for file in files if file.lower().endswith((".jpg", ".png", ".jpeg"))])
        i = 0

        for file in files:
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                i += 1
                old_pic = os.path.join(source_directory, file)
                new_pic = os.path.join(dest_directory, file)

                # Resize and compress the image
                self.compression_code(old_pic, new_pic, self.compress_width)

                # Update the percentage in the status bar
                percentage = int((i / total_images) * 100)
                self.statusBar().showMessage(f"Message: Compressed {percentage}%")
                
                # Allow the UI to update
                QApplication.processEvents()

        self.statusBar().showMessage("Message: Compression Completed")



    def compression_code(self, old_pic, new_pic, mywidth):
        try:
            img = Image.open(old_pic)
            wpercent = (mywidth / float(img.size[0]))
            hsize = int(float(img.size[1]) * float(wpercent))
            img = img.resize((mywidth, hsize), Image.LANCZOS)
            img.save(new_pic)

        except Exception as e:
            self.statusBar().showMessage("Message: " + str(e))


    def entire_dir(self, source_dir, dest_dir, width):
        files = os.listdir(source_dir)

        i = 0
        for file in files:
            i += 1

            old_pic = os.path.join(source_dir, file)
            new_pic = os.path.join(dest_dir, file)
            self.resize_pic(old_pic, new_pic, width)
            print(i, "Done")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())