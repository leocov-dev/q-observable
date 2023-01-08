import sys

import requests
from PySide2 import QtWidgets, QtCore
from requests import HTTPError

from qobservable.q_observable import QObservable
from qobservable.q_subscriber import QSubscriber


class RequestParagraph(QtCore.QRunnable):
    def __init__(self, count: int):
        super().__init__()
        self._count = count

    def run(self) -> None:
        response = requests.get("http://127.0.0.1:8000/paragraph/next")
        print(response.json())


class ParaSubscriber(QSubscriber):
    def __init__(self, count: int):
        super().__init__()
        self._count = count

    def run(self) -> None:
        for i in range(self._count):
            try:
                response = requests.get("http://127.0.0.1:8000/paragraph/next")
                self.next(response.json())
            except HTTPError as e:
                self.error(e)


class Application(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self._main_window = QtWidgets.QMainWindow()

        central = QtWidgets.QWidget(parent=self._main_window)
        self._main_window.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout()
        central.setLayout(layout)

        self._timer = QtCore.QBasicTimer()
        self._tick = 0
        self._direction = True

        prog_lab = QtWidgets.QLabel("Animation should be uninterrupted")
        layout.addWidget(prog_lab)

        self._tick_prog = QtWidgets.QProgressBar(parent=central)
        layout.addWidget(self._tick_prog)
        self._tick_prog.setMinimum(0)
        self._tick_prog.setMaximum(100)

        frame = QtWidgets.QFrame(parent=central)
        layout.addWidget(frame)
        frame.setMinimumHeight(100)

        action_ly = QtWidgets.QHBoxLayout()
        layout.addLayout(action_ly)

        self._count = QtWidgets.QSpinBox(parent=central)
        action_ly.addWidget(self._count)
        self._count.setMinimum(1)
        self._count.setMaximum(10)

        self._get = QtWidgets.QPushButton(text="Get Items", parent=central)
        action_ly.addWidget(self._get, stretch=2)
        self._get.clicked.connect(self.on_get)

    def on_get(self):
        print(self._count.value())

        obs = QObservable(ParaSubscriber(self._count.value()))
        obs.subscribe(self)

    def next(self, val) -> None:
        print(f"got value {val}")

    def timerEvent(self, event):
        if self._tick >= 100:
            self._direction = False
        elif self._tick <= 0:
            self._direction = True

        self._tick = (self._tick + 1) if self._direction else (self._tick - 1)
        self._tick_prog.setValue(self._tick)
        event.accept()

    def launch(self):
        self._timer.start(10, self)
        self._main_window.show()


if __name__ == "__main__":
    qt = QtWidgets.QApplication()

    app = Application()
    app.launch()

    sys.exit(qt.exec_())
