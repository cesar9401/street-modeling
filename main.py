import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from geneticalgorithm import generic_algorithm
from ui import main_widget

if __name__ == '__main__':
    print('hello there')
    # algorithm
    algorithm = generic_algorithm.GenericAlgorithm()

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create('gtk'))
    window = main_widget.MainWidget(algorithm)
    algorithm.window = window
    window.show()
    sys.exit(app.exec_())
