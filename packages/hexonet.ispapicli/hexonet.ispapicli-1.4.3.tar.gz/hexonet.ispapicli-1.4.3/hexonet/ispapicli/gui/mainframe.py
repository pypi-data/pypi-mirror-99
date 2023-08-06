from typing import Text
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from modules.core import Core
from modules.scrap import Scrap
from gui.login import LoginWindow
import textwrap
import sys
from io import StringIO
from collections import defaultdict
import re
import subprocess
import os

__version__ = "1.0.3"


class MainFrame(QWidget):

    BATCH_COMMANDLINE_ID = 300
    BATCH_PARAMETER_ID = 400
    BATCH_LIST_ID = 500
    BATCH_PARAMS = [
        "Select",
        "CONTACT",
        "DNSZONE",
        "DOMAIN",
        "DOMAINAUTH",
        "HOST",
        "NAMESERVER",
        "OBJECTID",
        "SSLCERTID",
    ]

    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)

        # intialize the gui
        self.originalPalette = QApplication.palette()
        self.createTopGroupBox()
        self.createLeftGroupBox()
        self.createMiddleTabWidget()
        self.createProgressBar()
        self.createMenubar()
        self.createToolbar()

        # set gui layout
        mainLayout = QGridLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.toolbar, 0, 0, 1, 3)
        mainLayout.addWidget(self.topBox, 1, 0, 1, 3)
        mainLayout.addWidget(self.leftGroupBox, 2, 0)
        mainLayout.addWidget(self.middleGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 3)
        mainLayout.setRowStretch(2, 2)
        mainLayout.setColumnStretch(0, 2)
        mainLayout.setColumnStretch(1, 6)
        self.setLayout(mainLayout)
        self.setWindowTitle("ISPAPI-CLI Tool")

        # set app gui style
        QApplication.setStyle(QStyleFactory.create("Fusion"))

        # create core login instnace
        self.coreLogic = Core()

        # scrap instance
        self.scrap = Scrap()

        # check user session upon start
        self.checkLogin()

        # set focus on command input field
        self.cmdTxt.setFocus()

        # initilaize command line completer
        self.initialiseCommandCompleter()

        # initialize subuser completer
        self.initialiseSubuserCompleter()

        # command to execute
        self.commandToExecute = ""

        # set app icon
        self.setWindowIcon(QIcon(self.getIcon("logo-bgw.jpg")))

    def checkLogin(self):
        result = self.coreLogic.checkSession()
        if result == "valid":
            self.sessionTime.setText("Your session is valid. ")
            self.sessionTime.setStyleSheet("color:green")
            self.loginBtn.setIcon(QIcon(self.getIcon("logout.png")))
            self.loginBtn.setText("Logout")
            self.loginBtn.clicked.connect(self.logout)
            self.reconnectBtnAction(self.loginBtn.clicked, self.logout)
            # enable gui
            self.disableEnableGui("enable")

        else:
            self.sessionTime.setText("Session expired! ")
            self.sessionTime.setStyleSheet("color:red")
            self.loginBtn.setIcon(QIcon(self.getIcon("login.png")))
            self.loginBtn.setText("Login")
            self.reconnectBtnAction(self.loginBtn.clicked, self.openLoginWindow)
            # diable gui
            self.disableEnableGui("disable")

    def reconnectBtnAction(self, signal, newhandler=None, oldhandler=None):
        """
        Reconnecting login btn action to either login or logout
        """
        while True:
            try:
                if oldhandler is not None:
                    signal.disconnect(oldhandler)
                else:
                    signal.disconnect()
            except TypeError:
                break
        if newhandler is not None:
            signal.connect(newhandler)

    def logout(self):
        msg = self.coreLogic.logout()
        alert = QMessageBox()
        alert.setText(msg)
        alert.exec_()
        # update login
        self.checkLogin()

    def disableEnableGui(self, status=None):
        """
        If session is expired then disable gui
        """
        if status is not None:
            if status == "enable":
                self.leftGroupBox.setEnabled(True)
                self.topBox.setEnabled(True)
                # focus on command input field
                self.cmdTxt.setFocus()
            else:
                self.leftGroupBox.setDisabled(True)
                self.topBox.setDisabled(True)
        else:
            pass

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        if curVal <= 99:
            self.progressBar.setValue(curVal + 1)
        else:
            self.timer.stop()
            self.progressBar.setValue(0)

    def createProgressBar(
        self,
    ):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setMaximumHeight(5)
        self.progressBar.setTextVisible(False)

        # create a timer for the progress bar

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advanceProgressBar)

        # call timer with speed of 5
        self.progressBarSpeed(5)

    def progressBarSpeed(self, speed):
        self.timer.start(speed)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def executeCommand(self):
        # start progressbar
        self.progressBarSpeed(5)
        # get args from the GUI
        commandToExecute = self.commandText.toPlainText().lower()
        if commandToExecute.startswith("-", 0, 1):
            original_args = commandToExecute.splitlines()
        else:
            original_args = ("--" + commandToExecute).splitlines()
        original_args = " ".join(original_args)
        # remove extra spaces around the = cases are ' =', '= ', ' = '
        original_args = original_args.replace(" = ", "=")
        original_args = original_args.replace(" =", "=")
        original_args = original_args.replace("= ", "=")
        splitted_args = original_args.split()
        # intialize the parser
        core_obj = self.coreLogic
        parser = core_obj.initParser()
        # overwrite defualt error function with our local function to show on the GUI
        parser.error = self.errorFunction

        try:
            args = vars(parser.parse_args(splitted_args))
            reminderargs = args["args"]
            # parse command args
            result, data = core_obj.parseArgs(args)
            # case gui started
            if result == "gui":
                self.plainResponse.setText("GUI already started")
            # case of help command
            elif result == "help":
                helpText = ""
                preHelp = textwrap.dedent(
                    """\
                    ISPAPI - Commandline Tool
                    ------------------------------------------------------------
                    The tool can be used in two modes:
                    - By using '=' sign e.g. --command=QueryDomainList limit=5
                    - By using spaces e.g. --command QueryDomainList limit 5
                    ------------------------------------------------------------

                    """
                )
                # redirect stdout
                stringio = StringIO()
                previous_stdout = sys.stdout
                sys.stdout = stringio

                # trigger parser help
                parser.print_help()

                # set back stdout
                sys.stdout = previous_stdout
                stdoutValue = stringio.getvalue()

                # show output on the GUI
                helpText = preHelp + stdoutValue
                self.plainResponse.setText(helpText)

            elif result == "cmd":
                # append reminder args with the command
                params_list = core_obj.parseParameters(reminderargs)
                cmd = data
                # add them to data which is the command list
                cmd.update(params_list)
                # check if subuser
                subuser = self.subuser.text()
                if len(subuser) > 1:
                    core_obj.cl.setUserView(subuser)  # set subuser
                else:
                    core_obj.cl.resetUserView()  # remove subuser
                # check for batches
                batch_param = self.batchParams.currentText()
                batch_params_list = self.batchParamsList.toPlainText()
                if batch_param != "Select" and batch_params_list != "":
                    lines = batch_params_list.split("\n")
                    for line in lines:
                        if line != "":
                            cmd[batch_param] = line
                            # request call
                            self.response = core_obj.request(cmd)
                            # set reult values to gui
                            self.populateResults(self.response)
                else:
                    # request call
                    self.response = core_obj.request(cmd)
                    # set reult values to gui
                    self.populateResults(self.response)

            # case update commands
            elif result == "update":
                # create scrap object
                # msg = "Please run this command in the terminal, use: ./ispapicli --update"
                # self.plainResponse.setText(msg)
                self.showUpdating()
            else:
                self.plainResponse.setText(data)

            # 1 end the progress bar
            # self.progressBarSpeed(5)
            # 2
            # check user session, in case of sesssion is expired
            self.checkLogin()
        except Exception as e:
            self.plainResponse.setText("Command failed due to: " + str(e))

    def errorFunction(self, message):
        self.plainResponse.setText("An error happend: " + message + "\n")

    def updateCommandView(self, e):
        cmdTxt = self.cmdTxt.text()
        # check if the command is related to other actions
        if cmdTxt.startswith("-", 0, 1):
            self.commandText.setText(cmdTxt)
            self.commandToExecute = cmdTxt
            return 0
        else:
            args = "command "
            args += cmdTxt
            args = args.split()
            # clean extra spaces, leave only single spaces among commands
            original_args = " ".join(args)
            # remove extra spaces around the = cases are ' =', '= ', ' = '
            original_args = original_args.replace(" = ", "=")
            original_args = original_args.replace(" =", "=")
            original_args = original_args.replace("= ", "=")
            # split args in an array
            parameters = original_args.split()
            # split commands if = used
            params_len = len(parameters)
            params = {}
            try:
                if params_len > 1:
                    i = 0
                    while i < params_len:
                        if "=" in parameters[i]:
                            key, value = parameters[i].split("=")
                            params[key] = value
                        else:
                            key = parameters[i]
                            i += 1
                            value = parameters[i]
                            params[key] = value
                        i += 1
                    self.commandText.setText()
            except Exception as e:
                pass
            commandView = "\n".join(("{}={}".format(*i) for i in params.items()))
            self.commandText.setText(commandView)
            self.commandToExecute = "--" + commandView

    def createToolbar(self):
        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setIconSize(QSize(20, 20))
        saveAction = QAction(
            QIcon(self.getIcon("save.png")), "Save results to a file", self
        )
        saveAction.triggered.connect(lambda: self.saveCommandToFile())

        copyAction = QAction(
            QIcon(self.getIcon("copy.png")), "Copy the results to clipboard", self
        )
        copyAction.triggered.connect(self.copyToClipboard)

        helpAction = QAction(
            QIcon(self.getIcon("help.png")), "See help documentation", self
        )
        helpAction.triggered.connect(self.showHelp)

        updateAction = QAction(
            QIcon(self.getIcon("refresh.png")), "Update the tool API's commands", self
        )
        updateAction.triggered.connect(self.showUpdating)

        self.sessionTime = QLabel("Checking your session... ")
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.loginBtn = QPushButton("Login")
        self.loginBtn.setIcon(QIcon(self.getIcon("login.png")))
        self.loginBtn.setStyleSheet("padding: 2px; padding-left: 6px")
        self.loginBtn.setIconSize(QSize(12, 12))
        self.loginBtn.setLayoutDirection(Qt.RightToLeft)

        seperator = QAction(self)
        seperator.setSeparator(True)
        # create a new window -TODO
        # self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(seperator)
        self.toolbar.addAction(copyAction)
        self.toolbar.addAction(seperator)
        self.toolbar.addAction(helpAction)
        self.toolbar.addAction(seperator)
        self.toolbar.addAction(updateAction)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.sessionTime)
        self.toolbar.addWidget(self.loginBtn)

    def createMenubar(self):

        self.menuBar = QMenuBar()
        file = self.menuBar.addMenu("File")
        new = QAction("New window", self)
        new.setShortcut("Ctrl+n")
        save = QAction("Save to file", self)
        save.setShortcut("Ctrl+S")
        quit = QAction("Quit", self)
        quit.setShortcut("Ctrl+q")

        # create a new window - TODO
        # file.addAction(new)
        file.addAction(save)
        file.addAction(quit)

        edit = self.menuBar.addMenu("Edit")
        copy = QAction("Copy", self)
        copy.setShortcut("Ctrl+c")

        edit.addAction(copy)

        help = self.menuBar.addMenu("Help")
        help.addAction("About ISPAPI tool")
        help.addAction("How to start?")

        file.triggered[QAction].connect(self.menuBarActions)
        edit.triggered[QAction].connect(self.menuBarActions)
        help.triggered[QAction].connect(self.menuBarActions)

    def createTopGroupBox(self):
        self.topBox = QGroupBox((""))
        executeBtn = QPushButton("Execute")
        executeBtn.setIcon(QIcon(self.getIcon("execute.png")))
        executeBtn.clicked.connect(self.executeCommand)
        executeBtn.setIconSize(QSize(14, 14))
        # executeBtn.setLayoutDirection(Qt.RightToLeft)

        clearBtn = QPushButton("Clear")
        clearBtn.setIcon(QIcon(self.getIcon("cross.png")))
        clearBtn.setIconSize(QSize(14, 14))
        # clearBtn.setLayoutDirection(Qt.RightToLeft)
        clearBtn.clicked.connect(self.__clearCMDfield)

        self.cmdTxt = QLineEdit()
        self.cmdTxt.setPlaceholderText("Enter command here...")
        self.cmdTxt.textEdited.connect(self.updateCommandView)
        # qSpaceEvent = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace, Qt.NoModifier)
        # self.cmdTxt.keyPressEvent(qSpaceEvent)
        self.cmdTxt.installEventFilter(self)
        self.cmdTxt.returnPressed.connect(self.executeCommand)

        # set command completer
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.cmdTxt.setCompleter(self.completer)

        # subuser
        self.subuser = QLineEdit()
        self.subuser.setPlaceholderText("Type a subuser")

        self.subuser.returnPressed.connect(self.executeCommand)

        # set command completer
        self.subUsercompleter = QCompleter()
        self.subUsercompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.subuser.setCompleter(self.subUsercompleter)

        self.minParameter = QLabel(self)
        self.minParameter.setText("Min parameters: ")
        self.minParameter.setStyleSheet("color:gray")
        f = QFont("Arial", 9)
        self.minParameter.setFont(f)

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.cmdTxt, 0, 1, 1, 1)
        gridLayout.addWidget(self.subuser, 0, 2, 1, 1)
        gridLayout.addWidget(executeBtn, 0, 3, 1, 1)
        gridLayout.addWidget(clearBtn, 0, 4, 1, 1)
        gridLayout.addWidget(self.minParameter, 1, 1, 1, 1)
        gridLayout.setColumnStretch(1, 6)
        gridLayout.setColumnStretch(2, 2)
        gridLayout.setColumnStretch(3, 1)
        gridLayout.setColumnStretch(4, 1)
        gridLayout.setContentsMargins(5, 0, 5, 10)
        self.topLayout = gridLayout
        self.topBox.setLayout(gridLayout)

    def createLeftGroupBox(self):
        self.leftGroupBox = QGroupBox("Command")
        leftTabWidget = QTabWidget()
        leftTabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tab1 = QWidget()
        self.commandText = QTextEdit()
        self.commandText.setPlaceholderText("Extracted command will be shown here")
        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.commandText)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        # params label
        self.batchParamsLabel = QLabel()
        self.batchParamsLabel.setText("Select parameter:")
        # params list
        self.batchParams = QComboBox()
        self.batchParams.addItems(self.BATCH_PARAMS)
        self.batchParams.setEditable(True)
        # params text label
        self.batchParamsListLabel = QLabel()
        self.batchParamsListLabel.setText("Insert the list:")
        self.batchParamsListLabel.setContentsMargins(0, 10, 0, 0)

        # params text
        self.batchParamsList = QTextEdit()
        self.batchParamsList.setPlaceholderText("Enter each item in new line")
        self.batchParamsList.setFrameStyle(QFrame.Box)
        tableLayout = QGridLayout()
        tableLayout.setContentsMargins(15, 5, 5, 5)
        tableLayout.addWidget(self.batchParamsLabel, 0, 0)
        tableLayout.addWidget(self.batchParams, 1, 0)
        tableLayout.addWidget(self.batchParamsListLabel, 2, 0)
        tableLayout.addWidget(self.batchParamsList, 3, 0)
        tab2.setLayout(tableLayout)

        leftTabWidget.addTab(tab1, "Extracted Command")
        leftTabWidget.addTab(tab2, "Batch")

        layout = QGridLayout()
        layout.addWidget(leftTabWidget, 0, 0, 1, 1)

        self.leftGroupBox.setLayout(layout)

    def createMiddleTabWidget(self):
        self.middleGroupBox = QGroupBox("Results")
        middleTabWidget = QTabWidget()
        middleTabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tab1 = QWidget()
        self.plainResponse = QTextEdit()
        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.plainResponse)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        self.tableResponse = QTableWidget(1, 2)
        self.tableResponse.setHorizontalHeaderLabels(["Property", "Value"])
        self.tableResponse.horizontalHeader().setStretchLastSection(True)
        tableLayout = QGridLayout()
        tableLayout.setContentsMargins(5, 5, 5, 5)
        tableLayout.addWidget(self.tableResponse, 0, 0)
        tab2.setLayout(tableLayout)

        tab3 = QWidget()
        self.listResponse = QTextEdit()
        tab3hbox = QHBoxLayout()
        tab3hbox.addWidget(self.listResponse)
        tab3.setLayout(tab3hbox)

        middleTabWidget.addTab(tab1, "Plain")
        middleTabWidget.addTab(tab2, "Properties")
        middleTabWidget.addTab(tab3, "List")

        layout = QGridLayout()
        layout.addWidget(middleTabWidget, 0, 0, 1, 1)

        self.middleGroupBox.setLayout(layout)

    def openLoginWindow(self):
        """
        Start login window
        """
        loginGui = LoginWindow(self)
        loginGui.startGui()

    def menuBarActions(self, q):
        action = q.text()
        if action == "New Window":
            pass
        if action == "Save to file":
            self.saveCommandToFile()
        if action == "Quit":
            self.closeApplication()
        if action == "Copy":
            self.copyToClipboard()
        if action == "Help":
            self.showHelp()
        if action == "About ISPAPI tool":
            self.showAbout()
        if action == "How to start?":
            self.showHelp()

    def closeApplication(self):
        print("exiting")
        sys.exit()

    def startNewWindow(self):
        app = QApplication(sys.argv)
        appGui = MainFrame()
        appGui.startGui()
        sys.exit(app.exec_())

    def startGui(self):
        geo = QDesktopWidget().availableGeometry()

        screenWidth = geo.width()
        screenHeight = geo.height()
        width = int(screenWidth * 0.5)
        height = int(screenHeight * 0.5)
        self.resize(width, height)

        frameGeo = self.frameGeometry()
        cp = geo.center()
        frameGeo.moveCenter(cp)
        self.move(frameGeo.topLeft())

        # start gui
        self.show()

    def initialiseCommandCompleter(self):
        model = QStringListModel()
        # get all possible autocomplete strings
        stringsSuggestion = []
        stringsSuggestion = (self.coreLogic.getCommandList()).splitlines()
        # set suggestion to the model
        model.setStringList(stringsSuggestion)
        # set model to the completer
        self.completer.setModel(model)

    def initialiseSubuserCompleter(self):
        model = QStringListModel()
        # get all possible autocomplete strings
        stringsSuggestion = []
        stringsSuggestion = (self.coreLogic.getSubUserList()).splitlines()
        # set suggestion to the model
        model.setStringList(stringsSuggestion)
        # set model to the completer
        self.subUsercompleter.setModel(model)

    def __clearCMDfield(self):
        self.cmdTxt.clear()
        self.cmdTxt.setFocus(True)

    def populateResults(self, response, mode="normal"):
        # get reulsts
        plainResult = response.getPlain()
        listResult = response.getListHash()

        # set plain results
        if mode == "iterative":
            self.plainResponse.append(plainResult)
            print("iternative")
        else:
            self.plainResponse.setText(plainResult)
            # delete any previous content of the list
            self.listResponse.setText("")

        # set properties and list
        resultLists = listResult["LIST"]
        counter = 0
        for row in resultLists:
            for col in row:
                counter += 1
        # set the number of rows
        self.tableResponse.setRowCount(counter)

        # populate the table
        rownumber = 0
        for row in resultLists:
            for i, (key, value) in enumerate(row.items()):
                keyWidget = QTableWidgetItem(key)
                valueWidget = QTableWidgetItem(value)
                self.tableResponse.setItem(rownumber, 0, keyWidget)
                self.tableResponse.setItem(rownumber, 1, valueWidget)
                # update the list
                if key not in ("TOTAL", "FIRST", "LAST", "LIMIT", "COUNT"):
                    self.listResponse.append(value)
                # incerate rownumber
                rownumber += 1
        # order table content
        self.tableResponse.sortItems(Qt.AscendingOrder)

    def saveCommandToFile(self):
        try:
            textToWrite = self.commandAndResponsePlain()
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog # Qt's builtin File Dialogue
            fileName, _ = QFileDialog.getSaveFileName(
                self, "Open", "report.txt", "All Files (*.*)", options=options
            )
            if fileName:
                try:
                    with open(fileName, "w") as file:
                        file.write(textToWrite)
                    alert = QMessageBox()
                    alert.setText("'" + fileName + "' \n\nFile Saved Successfully!")
                    alert.setIcon(QMessageBox.Information)
                    alert.exec_()
                except Exception as e:
                    alert = QMessageBox()
                    alert.setIcon(QMessageBox.Critical)
                    alert.setText("Couldn't save the file due to: " + str(e))
                    alert.exec_()
        except Exception as e:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Critical)
            alert.setText("Request a command first!")
            alert.setWindowTitle("Error")
            alert.exec_()

    def commandAndResponsePlain(self):
        result = self.plainResponse.toPlainText()
        command = self.response.getCommandPlain()
        textToWrite = command + "\n" + result
        return textToWrite

    def copyToClipboard(self):
        try:
            newText = self.commandAndResponsePlain()
            clipboard = QApplication.clipboard()
            clipboard.setText(newText)
        except Exception as e:
            print(e)
            pass  # in the case where there is not command requested

    def showHelp(self):
        box = QMessageBox(self)
        msg = """<p align='center'>
        <b style='font-size:20px'>Help Information</b>. <br><br><br>
        This window provides a simple help view, more detailed help can be found at: 
        <a href="https://hexonet.github.io/ispapicli/">ISPAPI CLI Tool Documentation</a>
        <br><br>
        Quick start:
        <br>
        To show help, type the command: -h | --help
        <br>
        From there you will find all information about using the command line in both the GUI and terminal
        <br><br>
        <span style="color:orange">Note</span>: Commands executed in terminal are similar to commands used in the GUI, except for the "--update" command which is only possible to trigger in the terminal
        <br><br><br>
        Copyright 2020 @Hexonet
        <br><br>
        </p>
        """
        box.setStandardButtons(QMessageBox.Ok)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle("Help")
        box.setText(msg)
        box.show()

    def showUpdating(self):
        box = QMessageBox(self)
        msg = """
        <p>Updating is done!</p>
        """
        box.setStandardButtons(QMessageBox.Ok)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle("Updating...")
        box.setText(msg)
        box.show()
        self.scrap.scrapCommands()
        # init tool dropdown autocomplete
        self.initialiseCommandCompleter()

    def showAbout(self):

        box = QMessageBox(self)
        msg = """<p align='center'>
        <b style='font-size:20px'>ISPAPI Tool</b>. <br><br><br>
        Version: %s <br><br>
        A simple command line interface to connect you to your account on Hexonet
        <br><br>
        Technical Support:
        <br>
        Email: support@hexonet.net 
        <br>
        Website: <a href="https://hexonet.github.io/ispapicli/">ISPAPI CLI Tool</a>
        <br><br><br>
        Copyright 2020 @Hexonet
        <br><br>
        </p>
        """

        box.setStandardButtons(QMessageBox.Ok)
        # box.setIcon(QMessageBox.Information)
        box.setWindowTitle("About")
        box.setText(msg % __version__)
        box.show()

    def eventFilter(self, source, event):

        # this function to handle autocomplete for command line
        if event.type() == QEvent.KeyRelease and source is self.cmdTxt:
            if event.key() == Qt.Key_Space:
                # show min paramters suggestions
                try:
                    cmd = self.cmdTxt.text()
                    m = re.match("^(\w+)\s$", cmd)
                    if m:
                        minParams = self.coreLogic.getMinParameters(cmd.strip())
                        if len(minParams) > 0:
                            minParamsLabel = ", ".join(minParams)
                            minParamsInput = "= ".join(minParams)
                            cursorPosition = (
                                len(self.cmdTxt.text() + minParams[0]) + 1
                            )  # for the '=' char
                            self.cmdTxt.setText(cmd + minParamsInput + "=")
                            self.minParameter.setText(
                                "Min parameters: " + minParamsLabel
                            )
                            self.cmdTxt.setCursorPosition(cursorPosition)
                        else:
                            self.minParameter.setText("Min parameters:")
                except Exception as e:
                    print(e)
        # must return bool value
        return super(MainFrame, self).eventFilter(source, event)

    def getIcon(self, iconName):
        ##
        # This function checks if the app is executable or in development and return the path

        if getattr(sys, "frozen", False):
            self.absolute_dirpath = os.path.dirname(sys.executable)
            try:
                self.absolute_dirpath = sys._MEIPASS
            except Exception:
                self.absolute_dirpath = os.path.abspath(".")
            path = self.command_path = os.path.join(
                self.absolute_dirpath, "data/icons/" + iconName
            )
        elif __file__:
            self.absolute_dirpath = os.path.dirname(__file__)
            path = self.command_path = os.path.join(
                self.absolute_dirpath, "../icons/" + iconName
            )
        return path
