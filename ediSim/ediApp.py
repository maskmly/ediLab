import os
import sys
import pickle
from edisim import edisim
from PyQt5.QtWidgets import (
    QApplication, QDialog, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QProgressBar
)

scriptDir = os.path.dirname(os.path.realpath(__file__))

class ediApp(QDialog):

    def __init__(self):
        super(ediApp, self).__init__()
        self.createFormGroupBox()

        self.progBar = QProgressBar(self)

        simButton = QPushButton(self)
        simButton.setText('Simulate')
        simButton.clicked.connect(self.simulate)

        closeButton = QPushButton(self)
        closeButton.setText('Close')
        closeButton.clicked.connect(self.close)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox0)
        mainLayout.addWidget(self.formGroupBox1)
        mainLayout.addWidget(self.formGroupBox2)
        mainLayout.addWidget(self.formGroupBox3)
        mainLayout.addWidget(self.progBar)
        mainLayout.addWidget(simButton)
        mainLayout.addWidget(closeButton)
        
        self.setLayout(mainLayout)

        self.setWindowTitle('EDI Form Layout')
        self.show()

    def errorMsg(self, msg):
        errorReply = QMessageBox.question(self, 'Attention!', msg, QMessageBox.Close)
        self.show()

    def waitMsg(self, msg):
        waitReply = QMessageBox.about(self, 'Attention!', msg)
        self.show()

    def createFormGroupBox(self):
        # First form
        self.formGroupBox0 = QGroupBox('Simulation Parameters')
        self.simNum = QLineEdit()
        self.spanNum = QLineEdit()
        layout0 = QFormLayout()
        layout0.addRow(QLabel('Number of Simulations:'), self.simNum)
        layout0.addRow(QLabel('Number of 3-month time spans:'), self.spanNum)
        self.formGroupBox0.setLayout(layout0)

        # Second form
        self.formGroupBox1 = QGroupBox('Simulation Info')
        self.faculty = QLineEdit()
        self.ORG = QLineEdit()
        self.URG = QLineEdit()
        layout1 = QFormLayout()
        layout1.addRow(QLabel('Total Faculty Population:'), self.faculty)
        layout1.addRow(QLabel('ORG Population in Faculty:'), self.ORG)
        layout1.addRow(QLabel('URG Population in Faculty:'), self.URG)
        self.formGroupBox1.setLayout(layout1)


        # Third form
        self.formGroupBox2 = QGroupBox('Over Represented Group Info')
        self.orgApp = QLineEdit()
        self.maxOrgScore = QLineEdit()
        self.minOrgScore = QLineEdit()
        layout2 = QFormLayout()
        layout2.addRow(QLabel('ORG Applicant Population:'), self.orgApp)
        layout2.addRow(QLabel('Maximum Score:'), self.maxOrgScore)
        layout2.addRow(QLabel('Minimum Score:'), self.minOrgScore)
        self.formGroupBox2.setLayout(layout2)

        # First sub-fourth form
        self.subGroupBox3_0 = QGroupBox('Before 15 Years')
        self.urgApp_0 = QLineEdit()
        self.maxUrgScore_0 = QLineEdit()
        self.minUrgScore_0 = QLineEdit()
        subLayout3_0 = QFormLayout()
        subLayout3_0.addRow(QLabel('Applicant Population:'), self.urgApp_0)
        subLayout3_0.addRow(QLabel('Maximum Score:'), self.maxUrgScore_0)
        subLayout3_0.addRow(QLabel('Minimum Score:'), self.minUrgScore_0)
        # Second sub-fourth form
        self.subGroupBox3_1 = QGroupBox('After 15 Years')
        self.urgApp_1 = QLineEdit()
        self.maxUrgScore_1 = QLineEdit()
        self.minUrgScore_1 = QLineEdit()
        subLayout3_1 = QFormLayout()
        subLayout3_1.addRow(QLabel('Applicant Population:'), self.urgApp_1)
        subLayout3_1.addRow(QLabel('Maximum Score:'), self.maxUrgScore_1)
        subLayout3_1.addRow(QLabel('Minimum Score:'), self.minUrgScore_1)
        # Fourth form
        self.formGroupBox3 = QGroupBox('Under Represented Group Info')
        layout3 = QFormLayout()
        layout3.addRow(self.subGroupBox3_0)
        layout3.addRow(self.subGroupBox3_1)
        self.subGroupBox3_0.setLayout(subLayout3_0)
        self.subGroupBox3_1.setLayout(subLayout3_1)
        self.formGroupBox3.setLayout(layout3)

        self.loadForm()

    def checkForm(self, aVar):
        if '' in aVar.values():
            self.errorMsg('Form is incomplete! Please fill out all information.')
            return False
        elif int(aVar['faculty']) == 0:
            self.errorMsg('Simulation Info Error! Total faculty population cannot be zero.')
            return False
        elif int(aVar['orgApp']) == 0:
            self.errorMsg('ORG Info Error! ORG applicant population cannot be zero.')
            return False
        elif int(aVar['urgApp_0']) == 0 or int(aVar['urgApp_1']) == 0:
            self.errorMsg('URG Info Error! URG applicant population cannot be zero.')
            return False
        elif int(aVar['ORG']) + int(aVar['URG']) != int(aVar['faculty']):
            self.errorMsg('Simulation Info Error! ORG & URG sum must equal total Faculty.')
            return False
        elif self.checkNegative(aVar):
            self.errorMsg('Attention! Negative values are invalid.')
            return False
        else:
            self.saveForm()
            return True
    
    def checkNegative(self, aVar):
        for vv in aVar.values():
            if int(vv) < 0:
                return True
        return False

    def saveForm(self):
        with open(f'{scriptDir}/formData.pkl', 'wb') as ff:
            pickle.dump(self.formVar, ff)

    def loadForm(self):
        try:
            with open(f'{scriptDir}/formData.pkl', 'rb') as ff:
                self.formVar = pickle.load(ff)
            self.setFrom()
        except:
            pass

    def setFrom(self):
        self.simNum.setText(self.formVar['simNum'])
        self.spanNum.setText(self.formVar['spanNum'])
        self.faculty.setText(self.formVar['faculty'])
        self.ORG.setText(self.formVar['ORG'])
        self.URG.setText(self.formVar['URG'])
        self.orgApp.setText(self.formVar['orgApp'])
        self.minOrgScore.setText(self.formVar['minOrgScore'])
        self.maxOrgScore.setText(self.formVar['maxOrgScore'])
        self.urgApp_0.setText(self.formVar['urgApp_0'])
        self.minUrgScore_0.setText(self.formVar['minUrgScore_0'])
        self.maxUrgScore_0.setText(self.formVar['maxUrgScore_0'])
        self.urgApp_1.setText(self.formVar['urgApp_1'])
        self.minUrgScore_1.setText(self.formVar['minUrgScore_1'])
        self.maxUrgScore_1.setText(self.formVar['maxUrgScore_1'])

    def updateFormVar(self):
        self.formVar = {
            'simNum': self.simNum.text(),
            'spanNum': self.spanNum.text(),
            'faculty': self.faculty.text(),
            'ORG': self.ORG.text(),
            'URG': self.URG.text(),
            'orgApp': self.orgApp.text(),
            'minOrgScore': self.minOrgScore.text(),
            'maxOrgScore': self.maxOrgScore.text(),
            'urgApp_0': self.urgApp_0.text(),
            'minUrgScore_0': self.minUrgScore_0.text(),
            'maxUrgScore_0': self.maxUrgScore_0.text(),
            'urgApp_1': self.urgApp_1.text(),
            'minUrgScore_1': self.minUrgScore_1.text(),
            'maxUrgScore_1': self.maxUrgScore_1.text(),
        }

    def simulate(self):
        self.updateFormVar()
    
        if self.checkForm(self.formVar):
            self.progBar.setRange(0, int(self.formVar['simNum']) - 1)
            sim = edisim(self.formVar)
            sim.main(self.progBar)
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ediApp()
    sys.exit(app.exec_())