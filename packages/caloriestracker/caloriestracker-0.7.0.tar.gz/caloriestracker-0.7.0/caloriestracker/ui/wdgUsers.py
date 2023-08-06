from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.ui.Ui_wdgUsers import Ui_wdgUsers

class wdgUsers(QWidget, Ui_wdgUsers):
    def __init__(self, mem,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblUsers.setSettings(self.mem.settings, "wdgUsers", "tblUsers")
        self.tblUsers.table.customContextMenuRequested.connect(self.on_tblUsers_customContextMenuRequested)
        self.update()

    def update(self):
        self.mem.data.users.qtablewidget(self.tblUsers)
        self.lblFound.setText(self.tr("{} products found").format(self.mem.data.users.length()))

    @pyqtSlot() 
    def on_actionUserDelete_triggered(self):
        if self.tblUsers.selected.is_deletable()==False:
            qmessagebox(self.tr("This product can't be removed, because is marked as not remavable"))
            return
            
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.tblUsers.selected.delete()
            self.mem.con.commit()
            self.mem.data.users.remove(self.tblUsers.selected)
            self.update()

    @pyqtSlot() 
    def on_actionUserNew_triggered(self):
        from caloriestracker.ui.frmUsersAdd import frmUsersAdd
        w=frmUsersAdd(self.mem, None, self)
        w.exec_()
        self.update()

    @pyqtSlot() 
    def on_actionUserEdit_triggered(self):
        from caloriestracker.ui.frmUsersAdd import frmUsersAdd
        w=frmUsersAdd(self.mem, self.tblUsers.selected, self)
        w.exec_()
        self.update()

    def on_tblUsers_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionUserNew)
        menu.addAction(self.actionUserDelete)
        menu.addAction(self.actionUserEdit)
        
        #Enabled disabled  
        if self.tblUsers.selected is None:
            self.actionUserDelete.setEnabled(False)
            self.actionUserEdit.setEnabled(False)
        else:
            self.actionUserDelete.setEnabled(True)
            self.actionUserEdit.setEnabled(True)
        menu.addSeparator()
        menu.addMenu(self.tblUsers.qmenu())
        menu.exec_(self.tblUsers.mapToGlobal(pos))
