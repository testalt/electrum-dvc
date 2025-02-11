from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import os
import qrcode

import electrum_dvc
from electrum_dvc import bmp
from electrum_dvc.i18n import _


class QRCodeWidget(QWidget):

    def __init__(self, data = None, fixedSize=False):
        QWidget.__init__(self)
        self.data = None
        self.qr = None
        self.fixedSize=fixedSize
        if fixedSize:
            self.setFixedSize(fixedSize, fixedSize)
        self.setData(data)


    def setData(self, data):
        if self.data != data:
            self.data = data
        if self.data:
            self.qr = qrcode.QRCode()
            self.qr.add_data(self.data)
            if not self.fixedSize:
                k = len(self.qr.get_matrix())
                self.setMinimumSize(k*5,k*5)
        else:
            self.qr = None

        self.update()
 

    def paintEvent(self, e):
        if not self.data:
            return

        black = QColor(0, 0, 0, 255)
        white = QColor(255, 255, 255, 255)

        if not self.qr:
            qp = QtGui.QPainter()
            qp.begin(self)
            qp.setBrush(white)
            qp.setPen(white)
            r = qp.viewport()
            qp.drawRect(0, 0, r.width(), r.height())
            qp.end()
            return

        matrix = self.qr.get_matrix()
        k = len(matrix)
        qp = QtGui.QPainter()
        qp.begin(self)
        r = qp.viewport()

        margin = 10
        framesize = min(r.width(), r.height())
        boxsize = int( (framesize - 2*margin)/k )
        size = k*boxsize
        left = (r.width() - size)/2
        top = (r.height() - size)/2

        # Make a white margin around the QR in case of dark theme use
        qp.setBrush(white)
        qp.setPen(white)
        qp.drawRect(left-margin, top-margin, size+(margin*2), size+(margin*2))

        for r in range(k):
            for c in range(k):
                if matrix[r][c]:
                    qp.setBrush(black)
                    qp.setPen(black)
                else:
                    qp.setBrush(white)
                    qp.setPen(white)
                qp.drawRect(left+c*boxsize, top+r*boxsize, boxsize, boxsize)
        qp.end()
        


class QRDialog(QDialog):

    def __init__(self, data, parent=None, title = "", show_text=False):
        QDialog.__init__(self, parent)

        d = self
        d.setWindowTitle(title)
        vbox = QVBoxLayout()
        qrw = QRCodeWidget(data)
        vbox.addWidget(qrw, 1)
        if show_text:
            text = QTextEdit()
            text.setText(data)
            text.setReadOnly(True)
            vbox.addWidget(text)
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        config = electrum.get_config()
        if config:
            filename = os.path.join(config.path, "qrcode.bmp")

            def print_qr():
                bmp.save_qrcode(qrw.qr, filename)
                QMessageBox.information(None, _('Message'), _("QR code saved to file") + " " + filename, _('OK'))

            def copy_to_clipboard():
                bmp.save_qrcode(qrw.qr, filename)
                self.parent().app.clipboard().setImage(QImage(filename))
                QMessageBox.information(None, _('Message'), _("QR code saved to clipboard"), _('OK'))

            b = QPushButton(_("Copy"))
            hbox.addWidget(b)
            b.clicked.connect(copy_to_clipboard)

            b = QPushButton(_("Save"))
            hbox.addWidget(b)
            b.clicked.connect(print_qr)

        b = QPushButton(_("Close"))
        hbox.addWidget(b)
        b.clicked.connect(d.accept)
        b.setDefault(True)

        vbox.addLayout(hbox)
        d.setLayout(vbox)

