import sys
from typing import Dict, List

import requests
from PySide2 import QtWidgets, QtCore
from requests import RequestException

from q_observable import QObservable, QSubscriberInterface, QSubscription
from q_observable.q_observable_thread_pool import wait_for_running_observables


class Application(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self._main_window = QtWidgets.QMainWindow()
        self._main_window.setMinimumWidth(400)

        central = QtWidgets.QWidget(parent=self._main_window)
        self._main_window.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout()
        central.setLayout(layout)

        self._observables_created = 0
        self._results = 0
        self._subscriptions: List[QSubscription] = []

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

        obs_counter = QtWidgets.QLabel("Observables Created: -")
        layout.addWidget(obs_counter)
        self._result_counter = QtWidgets.QLabel("Results: -")
        layout.addWidget(self._result_counter)

        action_ly = QtWidgets.QHBoxLayout()
        layout.addLayout(action_ly)

        self._count_lb = QtWidgets.QLabel("Per Obs")
        action_ly.addWidget(self._count_lb)

        self._count = QtWidgets.QSpinBox(parent=central)
        action_ly.addWidget(self._count)
        self._count.setMinimum(1)
        self._count.setMaximum(10)
        self._count.setValue(5)

        self._get = QtWidgets.QPushButton(text="Get Items", parent=central)
        action_ly.addWidget(self._get, stretch=2)
        self._get.clicked.connect(self.on_clicked)
        self._get.clicked.connect(
            lambda: obs_counter.setText(
                f"Observables Created: {self._observables_created}"
            )
        )

        self._unsub = QtWidgets.QPushButton(text="UnSub All", parent=central)
        action_ly.addWidget(self._unsub, stretch=1)
        self._unsub.clicked.connect(self._cancel_all_subs)

    def on_clicked(self):
        self._observables_created += 1

        print(QtCore.QThread.currentThread())
        print(f"getting {self._count.value()} paragraphs...")

        def _get_paragraphs(subscriber: QSubscriberInterface) -> None:
            for i in range(self._count.value()):
                try:
                    response = requests.get("http://127.0.0.1:8000/paragraph/next")
                    subscriber.next(response.json())
                except RequestException as e:
                    subscriber.error(e)

        obs = QObservable[Dict](_get_paragraphs)

        def on_next(val: Dict) -> None:
            print(val)
            self._results += 1
            self._result_counter.setText(f"Results: {self._results}")

        def on_error(err: Exception) -> None:
            print(f"Error: {err}")

        subscription = obs.subscribe(next_fn=on_next, error_fn=on_error)
        self._subscriptions.append(subscription)

    def _cancel_all_subs(self):
        if not self._subscriptions:
            return

        for sub in self._subscriptions:
            # stop listening for THIS class
            # other situations might have multiple subscribers that keep listening
            # threads are not canceled here
            sub.unsubscribe()

        self._subscriptions = []

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

    qt.aboutToQuit.connect(wait_for_running_observables)

    app = Application()
    app.launch()

    sys.exit(qt.exec_())
