import sys
from utilities import Utility
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import urllib3
import json
import vlc
from math import pi, sin
import struct
import glob


class MusicUI(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Music Widget'
        self.left = 10
        self.top = 10
        self.width = 100
        self.height = 100
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

    def createGridLayout(self):

        m_format = QAudioFormat()
        m_format.setChannelCount(1)
        # m_format.setFrequency(22050)
        m_format.setSampleRate(22050)
        m_format.setSampleSize(16)
        m_format.setCodec("audio/pcm")
        m_format.setByteOrder(QAudioFormat.LittleEndian)
        m_format.setSampleType(QAudioFormat.SignedInt)
        self.output = QAudioOutput(m_format, self)

        self.frequency = 440
        self.volume = 10000
        self.buffer = QBuffer()
        self.data = QByteArray()

        self.deviceLineEdit = QLineEdit()
        self.deviceLineEdit.setReadOnly(True)
        self.deviceLineEdit.setText(QAudioDeviceInfo.defaultOutputDevice().deviceName())

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximum(32767)
        self.volumeSlider.setPageStep(1024)

        self.volumeSlider.setValue(self.volume)

        self.playButton = QPushButton(self.tr("&Play"))

        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.playButton.clicked.connect(self.play)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("Device:"), self.deviceLineEdit)
        formLayout.addRow(self.tr("&Volume:"), self.volumeSlider)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addStretch()

        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.addLayout(formLayout)
        horizontalLayout.addLayout(buttonLayout)

        self.files = self.getAllFiles()
        self.num_songs = len(self.files)
        self.cur_song = 0
        self.isPlaying = False 
        self.cur_seek=0


    def getAllFiles(self):
        return glob.glob("/Users/shubham/Music/*.mp3")

    def getCurrentSong(self):
        self.song_file = QFile()
        self.song_file.setFileName(self.files[self.cur_song])
        self.song_file.open(QIODevice.ReadOnly)
        self.data.clear()
        self.data.append(self.song_file.readAll())
        return self.data

    def nextSong(self):
        self.cur_song = (self.cur_song+1)%self.num_songs


    def play(self):

        if not self.isPlaying:
            self.isPlaying = True
            self.playButton.setText("Pause")
        else:
            self.isPlaying = False
            self.playButton.setText("Play")


        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
            self.cur_seek=self.output.getSeek()
        elif self.output.state() == QAudio.IdleState:
            self.data.clear()
            self.song_file.close()
            self.nextSong()
            self.cur_seek=0

        if self.buffer.isOpen():
            self.buffer.close()

        self.getCurrentSong()
        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(self.cur_seek)

        self.output.start(self.buffer)

    def changeVolume(self, value):
        self.volume = value

    def createData(self):
        # Create 2 seconds of data with 22050 samples per second, each sample
        # being 16 bits (2 bytes).

        self.data.clear()
        for i in range(2 * 22050):
            t = i / 22050.0
            value = int(self.volume * sin(2 * pi * self.frequency * t))
            self.data.append(struct.pack("<h", value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MusicUI()
    window.show()
    sys.exit(app.exec_())

        