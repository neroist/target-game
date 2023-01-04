import random, secrets

from PySide6.QtCore import (
	QPropertyAnimation,
	QVariantAnimation,
	QEasingCurve,
	QSettings,
	QTimer,
	QPoint,
	QRect,
	QSize,
	Qt
)
from PySide6.QtGui import (
	QResizeEvent,
	QMouseEvent,
	QIcon,
	QFont
)
from PySide6.QtWidgets import (
	QGraphicsOpacityEffect,
	QApplication,
	QMainWindow,
	QPushButton,
	QSpacerItem,
	QSizePolicy,
	QHBoxLayout,
	QWidget,
	QLabel
)

import resources
from frame import RestartFrame


# ------ window -------
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.score = 0      
		self.time = 0
		self.newHighScore = False
		self.afterRestart = False
		
		self.settings = QSettings("Alice", "Target Game", self)
		
		self.setObjectName(u"MainWindow")
		if self.settings.contains("last_pos"): self.move(self.settings.value("last_pos"))
		self.resize(800, 600)
		self.setMinimumSize(300, 300)
		self.setWindowTitle("Target Game")
		self.setWindowIcon(QIcon('://target_wi.png'))
		
		self.centralwidget = QWidget(self)
		self.centralwidget.setObjectName(u"centralwidget")
		
		self.headerLayoutWidget = QWidget(self.centralwidget)
		self.headerLayoutWidget.setObjectName(u"horizontalLayoutWidget")
		self.headerLayoutWidget.setGeometry(QRect(9, 9, 780, 30))
		
		self.headerLayout = QHBoxLayout(self.headerLayoutWidget)
		self.headerLayout.setObjectName(u"headerLayout")
		self.headerLayout.setContentsMargins(0, 0, 0, 0)
		
		self.scoreLabel = QLabel(self.tr(u"Score: 0"), self.headerLayoutWidget)
		self.scoreLabel.setObjectName(u"scoreLabel")
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setHeightForWidth(self.scoreLabel.sizePolicy().hasHeightForWidth())
		self.scoreLabel.setSizePolicy(sizePolicy)
		self.scoreLabel.setFont(QFont(u"Segoe UI", 16))
		self.scoreLabel.setAlignment(Qt.AlignCenter)
		self.scoreLabel.setAttribute(Qt.WA_TransparentForMouseEvents)
		self.headerLayout.addWidget(self.scoreLabel)
		
		self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.headerLayout.addItem(self.horizontalSpacer)
		
		self.timeLabel = QLabel(self.tr(u"Time: 0:00"), self.headerLayoutWidget)
		self.timeLabel.setObjectName(u"timeLabel")
		sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
		self.timeLabel.setSizePolicy(sizePolicy)
		self.timeLabel.setFont(QFont(u"Segoe UI", 16))
		self.timeLabel.setAlignment(Qt.AlignCenter)
		self.timeLabel.setAttribute(Qt.WA_TransparentForMouseEvents)
		self.headerLayout.addWidget(self.timeLabel)
		
		self.targetButton = QPushButton(self.centralwidget)
		self.targetButton.setObjectName(u"targetButton")
		self.targetButton.setGeometry(
			QRect(
				(self.size().width() - 80) // 2, (self.size().height() - 80) // 2, 80, 80
			)
		)
		icon = QIcon()
		icon.addFile(u"://target_bi.png", QSize(), QIcon.Normal, QIcon.Off)
		self.targetButton.setIcon(icon)
		self.targetButton.setIconSize(QSize(80, 80))
		self.targetButton.setFlat(True)
		# so the player can't just focus onto the target button and spam the space bar to farm points
		self.targetButton.setFocusPolicy(Qt.NoFocus)
		self.targetButton.clicked.connect(self.moveTargetButton)
		
		self.rf = RestartFrame(self)
		self.rf.setObjectName(u"restartFrame")
		self.center(self.rf)
		rf_opacity = QGraphicsOpacityEffect(self.rf)
		rf_opacity.setOpacity(0)
		self.rf.setGraphicsEffect(rf_opacity)
		self.rf.setAttribute(Qt.WA_TransparentForMouseEvents)
		
		self.setCentralWidget(self.centralwidget)
		
		# timer to increment self.time var
		# update time label
		# and increment total time
		self.timeTimer = QTimer(self)
		self.timeTimer.timeout.connect(self.incrementTime)
		self.timeTimer.timeout.connect(
			lambda: self.timeLabel.setText(
				self.tr(f"Time: {self.secsToTime(self.time)}")
			)
		)
		self.timeTimer.timeout.connect(
			lambda: self.settings.setValue(
				"total_time", self.settings.value("total_time", 0, int) + 1
			)
		)
		self.timeTimer.start(1000)
		
		self.show()
		
	@staticmethod
	def center(widget: QWidget):
		parent = widget.parent()
		
		widget.move(
			(parent.width() - widget.width()) // 2,
			(parent.height() - widget.height()) // 2
		)
	
	@staticmethod
	def secsToTime(secs: int):
		return f"{secs // 60}:{(secs % 60):02d}"
	
	def incrementTime(self):
		self.time += 1
	
	def moveTargetButton(self) -> None:
		# generate random point
		x = random.randint(0, self.width() - 80)  # subtract 80 to make up for button width
		y = random.randint(0, self.height() - 80)  # same for the height
		
		# move button to random point on window
		ani = QVariantAnimation(self.targetButton)
		ani.setDuration(150)
		ani.setStartValue(self.targetButton.pos())
		ani.setEndValue(QPoint(x, y))
		ani.valueChanged.connect(lambda pos: self.targetButton.move(pos))
		ani.setEasingCurve(QEasingCurve.OutSine)  # Alternatives: NCurveTypes, TCBSpline, BezierSpline, "Out*"
		ani.start()
		
		# self.targetButton.move(QPoint(x, y))
		
		# increment score and update label and total score
		self.score += 2 if secrets.randbelow(50) == 0 else 1  # a 1/50 chance to get 2 points instead of 1
		self.scoreLabel.setText(self.tr(f"Score: {self.score}"))
		self.settings.setValue("total_score", self.settings.value("total_score", self.score, int) + 1)
		
		if self.afterRestart:
			# reconnect timer slots / "resume" timer
			self.timeTimer.timeout.connect(
				self.incrementTime
			)
			self.timeTimer.timeout.connect(
				lambda: self.timeLabel.setText(
					self.tr(f"Time: {self.secsToTime(self.time)}")
				)
			)
			self.timeTimer.timeout.connect(
				lambda: self.settings.setValue(
					"total_time", self.settings.value("total_time", 0, int) + 1
				)
			)
			self.timeTimer.start(1000)
			
			self.afterRestart = False
			
	def fadeInRF(self):
		effect = QGraphicsOpacityEffect(self.rf)
		
		ani = QPropertyAnimation(effect, b"opacity", self.rf)
		ani.setStartValue(0.0)
		ani.setEndValue(1.0)
		
		self.rf.setGraphicsEffect(effect)
		ani.start()
		
		self.rf.setAttribute(Qt.WA_TransparentForMouseEvents, False)
		
	def closeEvent(self, event):
		self.settings.setValue("last_pos", self.pos())
		
		self.settings.sync()
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		# center target button if game has not started yet
		if not self.score:
			self.center(self.targetButton)
			
		if self.afterRestart:
			self.center(self.rf)
		
		widget = self.headerLayoutWidget
		widget.resize(self.geometry().width() - 20, 30)
	
	def mousePressEvent(self, event: QMouseEvent) -> None:
		self.settings.setValue("total_misses", self.settings.value("total_misses", 0, int) + 1)
		self.afterRestart = True
		
		if self.score > self.settings.value("high_score", 0, int):
			self.settings.setValue("high_score", self.score)
		
		# if restart frame is visible ignore clicks
		if not self.centralwidget.isEnabled():
			event.ignore()
			return
		
		# set high score if score is higher than current high score
		if self.score > self.settings.value("high_score", 0, int):
			self.newHighScore = True
			self.settings.setValue("high_score", self.score)
			
		# center target button and restart frame in window
		self.center(self.targetButton)
		self.center(self.rf)
		
		# sync settings so stats are accurate
		self.settings.sync()
		
		# get user stats
		total_score = self.settings.value('total_score', self.score, int)
		total_misses = self.settings.value('total_misses', 1, type=int)
		total_time = self.settings.value('total_time', 1, type=int)
		high_score = self.settings.value('high_score', self.score, int)
		
		# set restart frame stats
		self.rf.timeLabel.setText(
			self.tr(self.timeLabel.text())
		)
		self.rf.ttimeLabel.setText(
			self.tr(f"Total Time: {self.secsToTime(total_time)}")
		)
		self.rf.scoreLabel.setText(
			self.tr(self.scoreLabel.text())
		)
		self.rf.tscoreLabel.setText(
			self.tr(f"Total Score: {total_score}")
		)
		self.rf.SPSLabel.setText(
			self.tr(
				f"Score Per Second: {round(self.score / (self.time if self.time else 1), 2)}"  # to avoid division by zero error
			)  
		)
		self.rf.tSPSLabel.setText(
			self.tr(
				f"Total Score Per Second: {round(total_score / (total_time if total_time else 1), 2)}"  # here aswell
			)
		)
		self.rf.taccuracyLabel.setText(
			self.tr(f"Accuracy: {round(total_score / total_misses, 2)}")
		)
		
		if not self.newHighScore:
			self.rf.hscoreLabel.setText(
				self.tr(f"High Score: {high_score}")
			)
		else:
			self.rf.hscoreLabel.setText(
				self.tr(f'High Score: {high_score} <b><span style="color: red">*NEW*</span></b>')  # QLabels support HTML
			)
			
		self.newHighScore = False
		
		# reset score
		self.score = 0
		
		# reset time
		self.time = 0
		
		# and "pause" time timer
		try: self.timeTimer.timeout.disconnect()
		except Exception as err: print(err)
		
		# fade in/show restart frame
		self.fadeInRF()
		
		self.centralwidget.setDisabled(True)
		

if __name__ == '__main__':
	from sys import argv, exit
	import ctypes
	
	app = QApplication(argv)
	app.setApplicationName("Target Game")
	app.setApplicationVersion("1.1.0")
	app.setApplicationDisplayName("Target Game")
	
	# show window icon on taskbar. see https://stackoverflow.com/a/1552105/14586140 for details
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'jasmine.target_game.v1.1.0')  # arbitrary string
	
	# initialize main window and set a variable to it so doesnt get garbage collected
	window = MainWindow()
	
	# run app and exit with proper error code
	exit(app.exec())
	
	# TODO add "+1" animation when target button is clicked
	# TODO add pause feature
	# TODO have a random chance to gain 2 points when target button is clicked
	# TODO when the target button moves to a new position, its movement should be animated
