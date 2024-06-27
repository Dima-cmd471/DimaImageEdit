#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout,
    QApplication, QWidget,
    QPushButton, QLabel, QListWidget,
    QFileDialog, QMessageBox
    )
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageEnhance

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.savedir = 'modifided/'
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        text.hide()
        pixmapimage = QPixmap(path)
        w, h = text.width(), text.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        text.setPixmap(pixmapimage)
        text.show()
    def saveImage(self, file_format='.jpg'): #extentions = ['.jpg','.jpeg','.png','.bmp','.gif','.svg','.pdf', '.webp']
        global file_i
        file_i += 1
        path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        new_filename = self.filename.split('.')
        try:
            new_filename = new_filename[0].split('(#')
        except:
            pass
        self.filename = new_filename[0]+'(#'+str(file_i)+')'+file_format
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
                    


def showChoosenImage():
    if images_list.currentRow() >= 0:
        filename = images_list.currentItem().text()
        image_processor.loadImage(filename)
        image_path = os.path.join(workdir, image_processor.filename)
        image_processor.showImage(image_path)

def filter(files, extentions):
    result = list()
    for name in files:
        for ext in extentions:
            if name.endswith(ext):
                result.append(name)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extentions = ['.jpg','.jpeg','.png','.bmp','.gif','.svg','.pdf', '.webp']
    chooseWorkdir()
    files = list()
    try:
        files = os.listdir(workdir)
    except:
        error_message = QMessageBox()
        error_message.setText('Dirrectory isn`t definded')
    filenames = filter(files, extentions)
    images_list.clear()
    for filename in filenames:
        images_list.addItem(filename)

file_i = 0
workdir = ''
image_processor = ImageProcessor()

app = QApplication([])
main_win = QWidget()
main_win.resize(700, 400)
main_win.setWindowTitle('Easy Editor')

dir_button = QPushButton('Папка')
images_list = QListWidget()
bw_button = QPushButton('Ч/Б')
sharpness_button = QPushButton('Контраст')
mirror_button = QPushButton('Зеркало')
text = QLabel('Здесь будет картинка')
left_button = QPushButton('Лево')
right_button = QPushButton('Право')

main_layout = QHBoxLayout()
leftside_layout = QVBoxLayout()
rightside_layout = QVBoxLayout()
buttons_layout = QHBoxLayout()

buttons_layout.addWidget(left_button, alignment=Qt.AlignBottom)
buttons_layout.addWidget(right_button, alignment=Qt.AlignBottom)
buttons_layout.addWidget(mirror_button, alignment=Qt.AlignBottom)
buttons_layout.addWidget(sharpness_button, alignment=Qt.AlignBottom)
buttons_layout.addWidget(bw_button, alignment=Qt.AlignBottom)
leftside_layout.addWidget(dir_button)
leftside_layout.addWidget(images_list, alignment=Qt.AlignLeft)
rightside_layout.addWidget(text, 100)

rightside_layout.addLayout(buttons_layout)
main_layout.addLayout(leftside_layout, 20)
main_layout.addLayout(rightside_layout, 80)
main_win.setLayout(main_layout)

dir_button.clicked.connect(showFilenamesList)
images_list.currentRowChanged.connect(showChoosenImage)

left_button.clicked.connect(image_processor.do_left)
right_button.clicked.connect(image_processor.do_right)
bw_button.clicked.connect(image_processor.do_bw)
mirror_button.clicked.connect(image_processor.do_flip)
sharpness_button.clicked.connect(image_processor.do_contrast)

main_win.show()
app.exec_()