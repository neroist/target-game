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
		
		self.scoreLabel = QLabel(self.tr(u"Score: 0"), self)
		self.scoreLabel.setObjectName(u"scoreLabel")
		self.scoreLabel.setFont(font2 := QFont(u"Segoe UI", 10))
		self.scoreLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.scoreLabel)
		
		self.hscoreLabel = QLabel(self.tr(u"High Score: 0"), self)
		self.hscoreLabel.setObjectName(u"hscoreLabel")
		self.hscoreLabel.setFont(font2)
		self.hscoreLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.hscoreLabel)
		
		self.tscoreLabel = QLabel(self.tr(u"Total Score: 0"), self)
		self.tscoreLabel.setObjectName(u"tscoreLabel")
		self.tscoreLabel.setFont(font2)
		self.tscoreLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.tscoreLabel)
		
		self.SPSLabel = QLabel(self.tr(u"Score Per Second: 0"), self)
		self.SPSLabel.setObjectName(u"accuracyLabel")
		self.SPSLabel.setFont(font2)
		self.SPSLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.SPSLabel)
		
		self.tSPSLabel = QLabel(self.tr(u"Total Score Per Second: 0"), self)
		self.tSPSLabel.setObjectName(u"taccuracyLabel")
		self.tSPSLabel.setFont(font2)
		self.tSPSLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.tSPSLabel)
		
		self.taccuracyLabel = QLabel(self.tr(u"Total Accuracy: 0"), self)
		self.taccuracyLabel.setObjectName(u"taccuracyLabel")
		self.taccuracyLabel.setFont(font2)
		self.taccuracyLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.taccuracyLabel)
		
		self.timeLabel = QLabel(self.tr(u"Time: 0"), self)
		self.timeLabel.setObjectName(u"timeLabel")
		self.timeLabel.setFont(font2)
		self.timeLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.timeLabel)
		
		self.ttimeLabel = QLabel(self.tr(u"Total Time: 0"), self)
		self.ttimeLabel.setObjectName(u"ttimeLabel")
		self.ttimeLabel.setFont(font2)
		self.ttimeLabel.setIndent(10)
		
		self.verticalLayout.addWidget(self.ttimeLabel)
		
		for i in (
				self.scoreLabel,
				self.hscoreLabel,
				self.tscoreLabel,
				self.SPSLabel,
				self.tSPSLabel,
				self.taccuracyLabel,
				self.timeLabel,
				self.ttimeLabel
		): i.setTextInteractionFlags(Qt.TextBrowserInteraction)
		
		self.restartButton = QPushButton(self.tr(u"Restart"), self)
		self.restartButton.setObjectName(u"restartButton")
		self.restartButton.setDefault(True)
		self.restartButton.setCursor(Qt.PointingHandCursor)
		self.restartButton.clicked.connect(self.fadeOut)
		
		self.verticalLayout.addWidget(self.restartButton)
	
	def fadeOut(self):
		effect = QGraphicsOpacityEffect(self)
		
		animation = QPropertyAnimation(effect, b'opacity', self)
		animation.setStartValue(1.0)
		animation.setEndValue(0.0)
		#effect.opacityChanged.connect(lambda _: self.setGraphicsEffect(effect))
		self.setGraphicsEffect(effect)
		animation.start(QPropertyAnimation.KeepWhenStopped)
		
		self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
		self.parent().centralwidget.setEnabled(True)
		self.parent().scoreLabel.setText(self.tr(u"Score: 0"))
		self.parent().timeLabel.setText(self.tr(u"Time: 0:00"))
