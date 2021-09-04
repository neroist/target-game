from PySide6.QtGui import QFont
from PySide6.QtCore import (
	QCoreApplication,
	QPropertyAnimation,
	Qt
)
from PySide6.QtWidgets import (
	QWidget,
	QFrame,
	QLabel,
	QPushButton,
	QVBoxLayout,
	QGraphicsOpacityEffect
)


class RestartFrame(QFrame):
	def __init__(self, parent: QWidget = None):
		super().__init__(parent)
		
		self.score = 0
		self.hscore = 0
		self.tscore = 0
		self.time = 0
		self.ttime = 0
		
		self.setObjectName(u"Frame")
		self.resize(400, 300)
		self.setStyleSheet("background-color: rgb(220, 220, 220)")
		
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setObjectName(u"verticalLayout")
		
		self.titleLabel = QLabel(self.tr(u"You misclicked, try again!"), self)
		self.titleLabel.setObjectName(u"titleLabel")
		
		self.titleLabel.setFont(QFont(u"Segoe UI", 18))
		
		self.verticalLayout.addWidget(self.titleLabel)
		
		self.line = QFrame(self)
		self.line.setObjectName(u"line")
		self.line.setFrameShadow(QFrame.Plain)
		self.line.setFrameShape(QFrame.HLine)
		
		self.verticalLayout.addWidget(self.line)
		
		self.statsLabel = QLabel(self.tr(u"Stats:"), self)
		self.statsLabel.setObjectName(u"statsLabel")
		self.statsLabel.setFont(QFont(u"Segoe UI Semibold", 16, QFont.Bold))
		
		self.verticalLayout.addWidget(self.statsLabel)
		
		self.scoreLabel = QLabel(self)
		self.scoreLabel.setObjectName(u"scoreLabel")
		self.scoreLabel.setFont(font2 := QFont(u"Segoe UI", 10))
		self.scoreLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.scoreLabel)
		
		self.hscoreLabel = QLabel(self)
		self.hscoreLabel.setObjectName(u"hscoreLabel")
		self.hscoreLabel.setFont(font2)
		self.hscoreLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.hscoreLabel)
		
		self.tscoreLabel = QLabel(self)
		self.tscoreLabel.setObjectName(u"tscoreLabel")
		self.tscoreLabel.setFont(font2)
		self.tscoreLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.tscoreLabel)
		
		self.timeLabel = QLabel(self)
		self.timeLabel.setObjectName(u"timeLabel")
		self.timeLabel.setFont(font2)
		self.timeLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.timeLabel)
		
		self.ttimeLabel = QLabel(self)
		self.ttimeLabel.setObjectName(u"ttimeLabel")
		self.ttimeLabel.setFont(font2)
		self.ttimeLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.ttimeLabel)
		
		self.restartButton = QPushButton(self.tr(u"Restart"), self)
		self.restartButton.setObjectName(u"restartButton")
		self.restartButton.clicked.connect(self.fadeOut)
		
		self.verticalLayout.addWidget(self.restartButton)
		
		self.retranslateUi()
	
	def fadeOut(self):
		effect = QGraphicsOpacityEffect(self)
		
		animation = QPropertyAnimation(effect, b'opacity', self)
		animation.setStartValue(1.0)
		animation.setEndValue(0.0)
		effect.opacityChanged.connect(lambda _: self.setGraphicsEffect(effect))
		animation.start(QPropertyAnimation.KeepWhenStopped)
		
		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
		self.parent().centralwidget.setEnabled(True)
		self.parent().scoreLabel.setText("Score: 0")
		self.parent().timeLabel.setText("Time: 0:00")
	
	def retranslateUi(self):
		# self.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
		self.scoreLabel.setText(QCoreApplication.translate("Frame", f"Score: {self.score}", None))
		self.hscoreLabel.setText(QCoreApplication.translate("Frame", f"High Score: {self.hscore}", None))
		self.tscoreLabel.setText(QCoreApplication.translate("Frame", f"Total Score: {self.tscore}", None))
		self.timeLabel.setText(QCoreApplication.translate("Frame", f"Time: {self.time}", None))
		self.ttimeLabel.setText(QCoreApplication.translate("Frame", f"Total Time: {self.ttime}", None))
		self.restartButton.setText(QCoreApplication.translate("Frame", u"Restart", None))
