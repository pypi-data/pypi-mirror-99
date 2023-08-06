from logging import getLogger

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from Rare.Components.Dialogs.InstallDialog import InstallDialog
from Rare.utils.Models import InstallOptions

logger = getLogger("Uninstalled")


class BaseUninstalledWidget(QWidget):
    install_game = pyqtSignal(InstallOptions)

    def __init__(self, game, core, pixmap):
        super(BaseUninstalledWidget, self).__init__()
        self.game = game
        self.core = core
        self.pixmap = pixmap

    def install(self):
        infos = InstallDialog().get_information()
        if infos != 0:
            path, max_workers = infos
            self.install_game.emit(InstallOptions(app_name=self.game.app_name, max_workers=max_workers, path=path))
