import sys
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
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
    new_pic_name, okPressed = QInputDialog.getText(self, "Save Image as", "Image Name", QLineEdit.Normal, "")
        
    if okPressed and new_pic_name != "":
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

            self.compression_code(old_pic, new_pic, self.compress_width)
            percentage = int((i / total_images) * 100)
            self.statusBar().showMessage(f"Message: Compressed {percentage}%")
                
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