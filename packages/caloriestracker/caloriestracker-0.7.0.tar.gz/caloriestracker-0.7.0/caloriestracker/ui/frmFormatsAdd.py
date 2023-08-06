from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmFormatsAdd import Ui_frmFormatsAdd
from caloriestracker.objects.format import Format, FormatPersonal
from datetime import datetime

class frmFormatsAdd(QDialog, Ui_frmFormatsAdd):
    def __init__(self, mem, product,  format=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.product=product
        self.format=format
        if self.format==None:
            self.__insert=True
        else:
            self.__insert=False
            self.txtName.setText(self.format.name)
            self.spnAmount.setValue(self.format.amount)

    def on_bb_accepted(self):
        if self.format==None:
            if self.mem.isProductsMaintainerMode(): 
                format_class=Format
            else:
                format_class=FormatPersonal
            self.format=format_class(self.mem,  self.txtName.text(), self.product, self.product.system_product, self.spnAmount.value(), datetime.now(), None)
            self.product.formats.append(self.format)
        else:
            self.format.name=self.txtName.text()
            self.format.amount=self.spnAmount.value()
            self.format.last=datetime.now()
        self.format.save()
        if self.mem.isProductsMaintainerMode():
            if self.__insert==True:
                self.mem.insertFormats.append(self.format)
            else:
                self.mem.updateFormats.append(self.format)
        else:#Not mantainer mode
            if self.__insert==True:
                self.mem.con.commit()
        self.product.needStatus(1, downgrade_to=0)
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


