import getpass
import glob
import sys
import os

import soundfile as sf
import wave
from PyQt5 import QtWidgets, uic


class DivideDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        _ui = "./UI/divide_dialog.ui"
        uic.loadUi(_ui, self)

        self.user_name = getpass.getuser()
        self.save_folder_name = "C:/Users/{}/Documents/SoundEditor/".format(self.user_name)
        self.current_file_names = []
        self.current_folder_name = ""
        self.total_file_counting = 0
        self.file_counting = 2
        self.file_role = True
        self.time_counting = 0.1
        self.preview_text = "2"
        self.mk_counting = False
        self.remove_role = False
        self.file_name_role = False

        self.loading_fuc()

    def loading_fuc(self):
        self.ui_init()
        self.button_init()
        self.function_init()
        self.setting_init()

    def button_init(self):
        self.findButton.clicked.connect(self.save_folder_find_fuc)
        self.loadFileButton.clicked.connect(self.load_file_fuc)
        self.loadFolderButton.clicked.connect(self.load_folder_fuc)
        self.doButton.clicked.connect(self.do_divide)
        self.closeButton.clicked.connect(self.close)

    def function_init(self):
        self.fileCountRadioButton.toggled.connect(self.count_setting)
        self.removeRoleCheckBox.stateChanged.connect(self.remove_role_setting)
        self.fileNameCheckBox.stateChanged.connect(self.file_name_role_setting)
        self.countingTextBrowser.textChanged.connect(self.counting_file_check)
        self.countingTextBrowser_2.textChanged.connect(self.counting_file_check)
        self.saveTextBrowser.textChanged.connect(self.save_locate_change)

    def ui_init(self):
        _qr = self.frameGeometry()
        _cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        _qr.moveCenter(_cp)
        self.fileLoadTableWidget.setColumnWidth(0, int(300 * 0.6))
        self.fileLoadTableWidget.setColumnWidth(1, int(300 * 0.25))

    def setting_init(self):
        self.setAcceptDrops(True)
        if not os.path.exists(self.save_folder_name):
            os.mkdir(self.save_folder_name)

    # Mouse Functions
    def dragEnterEvent(self, e):
        for url in e.mimeData().urls():
            if not (url.isEmpty()) or ".wav" in url.toLocalFile():
                e.accept()
            else:
                e.ignore()

    def dropEvent(self, e):
        self.current_file_names = []
        for url in e.mimeData().urls():
            if ".wav" in url.toLocalFile() or not (url.isEmpty()):
                e.accept()
                if url.toLocalFile()[-4:] == ".wav":
                    self.current_file_names.append(url.toLocalFile())
                else:
                    tmp_file_names = glob.glob(url.toLocalFile() + "/*.wav")
                    self.current_file_names.extend(tmp_file_names)
            else:
                e.ignore()
        self.load_to_table_widget_fuc()

    # Load Functions
    def save_folder_find_fuc(self):
        self.save_folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, '?????? ?????? ??????')
        self.saveTextBrowser.setText(self.save_folder_name)

    def load_file_fuc(self):
        filter_ = "*.wav"
        self.current_file_names, _ = QtWidgets.QFileDialog.getOpenFileNames(self, '?????? ????????? ??????', filter=filter_)
        self.load_to_table_widget_fuc()

    def load_folder_fuc(self):
        self.current_folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, "?????? ?????? ??????")
        self.current_file_names = glob.glob(self.current_folder_name + "/*.wav")
        self.load_to_table_widget_fuc()

    def load_to_table_widget_fuc(self):
        self.fileLoadTableWidget.setRowCount(len(self.current_file_names))
        if not self.current_file_names:
            self.fileCountRadioButton.setEnabled(False)
            self.timeCountRadioButton.setEnabled(False)
            self.removeRoleCheckBox.setEnabled(False)
            self.fileNameCheckBox.setEnabled(False)
            self.doButton.setEnabled(False)
        else:
            for i in range(len(self.current_file_names)):
                file_path = self.current_file_names[i].replace("\\", "/")
                audio = wave.open(file_path)
                frames = audio.getnframes()
                rate = audio.getframerate()
                duration = round(frames / rate, 3)
                file_name = file_path.split("/")[-1]
                self.fileLoadTableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(file_name))
                self.fileLoadTableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(duration)))
            self.fileCountRadioButton.setEnabled(True)
            self.countingTextBrowser.setEnabled(True)
            self.timeCountRadioButton.setEnabled(True)
            self.removeRoleCheckBox.setEnabled(True)
            self.fileNameCheckBox.setEnabled(True)
            self.check_row_and_text()

    # divideenate Expectancy Functions
    def calculate_expectancy(self):
        if self.file_role:
            self.total_file_counting = self.fileLoadTableWidget.rowCount() * int(self.preview_text)
            self.file_counting = int(self.preview_text)
        else:
            self.total_file_counting = 0
            for i in range(self.fileLoadTableWidget.rowCount()):
                time_item = self.fileLoadTableWidget.item(i, 1).text()
                self.total_file_counting += float(time_item) / round(float(self.preview_text), 3)
            self.time_counting = round(float(self.preview_text), 3)

    def show_result(self, bools):
        if bools:
            if self.file_role:
                self.msgLabel_1.setText(str(self.total_file_counting))
                self.msgLabel_2.setText(str(self.file_counting))
                self.show_file_name_fuc()
                self.mk_counting = True
            else:
                self.msgLabel_1.setText(str(int(self.total_file_counting)))
                self.msgLabel_2.setText(str(self.time_counting))
                self.show_file_name_fuc()
                self.mk_counting = True
        else:
            self.msgLabel_1.setText("0")
            self.msgLabel_2.setText("0")
            self.msgLabel_3.setText("---")
            self.mk_counting = False

    def show_file_name_fuc(self):
        if self.file_name_role:
            self.msgLabel_3.setText("?????? ?????????_****.wav")
        else:
            self.msgLabel_3.setText("Divide_wave_***_****.wav")

    # divide Setting Functions
    def count_setting(self, check_bool):
        if check_bool:
            self.file_role = True
            self.countingTextBrowser.setEnabled(True)
            self.countingTextBrowser.setText("2")
            self.countingTextBrowser_2.setEnabled(False)
            self.countingTextBrowser_2.setText("")
            self.changeLabel.setText("????????? ?????? ?????? ??????")
            self.changeLabel_2.setText("???")
        else:
            self.file_role = False
            self.countingTextBrowser.setEnabled(False)
            self.countingTextBrowser.setText("")
            self.countingTextBrowser_2.setEnabled(True)
            self.countingTextBrowser_2.setText("0.1")
            self.changeLabel.setText("???????????? ?????????")
            self.changeLabel_2.setText("???")

    def remove_role_setting(self, check_bool):
        if check_bool:
            self.remove_role = True
        else:
            self.remove_role = False

    def file_name_role_setting(self, check_bool):
        if check_bool:
            self.file_name_role = True
        else:
            self.file_name_role = False
        self.counting_file_check()

    # divide Functions
    def do_divide(self):
        self.check_before_divide()
        try:
            if self.mk_counting:
                to_file_dict = {}
                progress_value = 10
                if self.file_role:
                    up_value = 1 / len(self.current_file_names) * 50
                    for file_path in self.current_file_names:
                        file_path = file_path.replace("\\", "/")
                        file_name = file_path.split("/")[-1][:-4]
                        sound, sr = sf.read(file_path)
                        sound_datas = []
                        if sound.ndim == 1:
                            division = sound.shape[0] // self.file_counting
                            for i in range(self.file_counting):
                                if sound.shape[0] >= division:
                                    sound_datas.append(sound[:division])
                                    sound = sound[division:]
                                elif (sound.shape[0] < division) and (sound.shape[0] > (sr / 0.1)):
                                    sound_datas.append(sound)
                            to_file_dict[file_name] = sound_datas
                        else:
                            division = sound.shape[0] // self.file_counting
                            for i in range(self.file_counting):
                                if sound.shape[0] >= division:
                                    sound_datas.append(sound[:division, :])
                                    sound = sound[division:, :]
                                elif (sound.shape[0] < division) and (sound.shape[0] > (sr / 0.1)):
                                    sound_datas.append(sound)
                            to_file_dict[file_name] = sound_datas, sr
                        progress_value += up_value
                        self.progressBar.setValue(int(progress_value))

                    up_value = 1 / len(self.current_file_names) * 40
                    k = 1
                    for sound_name, value in to_file_dict.items():
                        if self.file_name_role:
                            sound_name = sound_name + "_{:04d}.wav"
                            path_ = os.path.join(self.save_folder_name, sound_name)
                            n = 1
                            for sound_data in value[0]:
                                sf.write(path_.format(n), sound_data, samplerate=value[1])
                                n += 1
                        else:
                            sound_name = "Divide_Wave" + "{:03d}" + "_{:04d}.wav"
                            path_ = os.path.join(self.save_folder_name, sound_name)
                            n = 1
                            for sound_data in value[0]:
                                sf.write(path_.format(k, n), sound_data, samplerate=value[1])
                                n += 1
                        k += 1
                        progress_value += up_value
                        self.progressBar.setValue(int(progress_value))
                else:
                    up_value = 1 / len(self.current_file_names) * 50
                    for file_path in self.current_file_names:
                        file_path = file_path.replace("\\", "/")
                        file_name = file_path.split("/")[-1][:-4]
                        sound, sr = sf.read(file_path)
                        sound_datas = []
                        if sound.ndim == 1:
                            division = int(sr / self.time_counting)
                            count = round(sound.shape[0] / division, 0)
                            for i in range(int(count)):
                                if sound.shape[0] >= division:
                                    sound_datas.append(sound[:division])
                                    sound = sound[division:]
                                elif (sound.shape[0] < division) and (sound.shape[0] > (sr / 0.1)):
                                    sound_datas.append(sound)
                            to_file_dict[file_name] = sound_datas
                        else:
                            division = int(sr * self.time_counting)
                            count = round(sound.shape[0] / division, 0)
                            for i in range(int(count)):
                                if sound.shape[0] >= division:
                                    sound_datas.append(sound[:division, :])
                                    sound = sound[division:, :]
                                elif (sound.shape[0] < division) and (sound.shape[0] > (sr / 0.1)):
                                    sound_datas.append(sound)

                            to_file_dict[file_name] = sound_datas, sr
                        progress_value += up_value
                        self.progressBar.setValue(int(progress_value))

                    up_value = 1 / len(self.current_file_names) * 50
                    k = 1
                    for sound_name, value in to_file_dict.items():
                        if self.file_name_role:
                            sound_name = sound_name + "_{:04d}.wav"
                            path_ = os.path.join(self.save_folder_name, sound_name)
                            n = 1
                            for sound_data in value[0]:
                                sf.write(path_.format(n), sound_data, samplerate=value[1])
                                n += 1
                        else:
                            sound_name = "Divide_Wave" + "{:03d}" + "_{:04d}.wav"
                            path_ = os.path.join(self.save_folder_name, sound_name)
                            n = 1
                            for sound_data in value[0]:
                                sf.write(path_.format(k, n), sound_data, samplerate=value[1])
                                n += 1
                        k += 1
                        progress_value += up_value
                        self.progressBar.setValue(int(progress_value))

            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setWindowTitle("????????? ??????")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.setText("???????????? ?????????????????????!")
            msgbox.exec_()
            self.progressBar.setValue(0)
            self.do_option()

        except:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setWindowTitle("????????? ??????")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.setText("???????????? ????????? ???????????? ???????????? ??????????????????...")
            msgbox.exec_()
            self.progressBar.setValue(0)



    def check_before_divide(self):
        if not os.path.exists(self.saveTextBrowser.toPlainText()):
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setWindowTitle("?????? ?????? ??????")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.setText("?????? ????????? ???????????? ????????????.")
            msgbox.exec_()
            self.mk_counting = False
            return
        if len(self.current_file_names) == 0:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setWindowTitle("?????? ?????? ??????")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.setText("?????? ????????? 2??? ??????????????? ?????????.")
            msgbox.exec_()
            self.mk_counting = False
            return
        if 0 <= self.file_counting <= 1:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Warning)
            msgbox.setWindowTitle("?????? ?????????")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.setText("0?????? 1??? ?????? ??? ????????????.")
            msgbox.exec_()
            self.mk_counting = False
            return
        self.progressBar.setValue(10)
        self.mk_counting = True

    def do_option(self):
        if self.remove_role:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setWindowTitle("?????? ??????")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.No)
            msgbox.setText("?????? ????????? ??????????????????????")
            ret = msgbox.exec_()
            if ret == QtWidgets.QMessageBox.Ok:
                for file_path in self.current_file_names:
                    os.remove(file_path)
                self.fileLoadTableWidget.clearContents()

    # Input UI Setting Functions
    def counting_file_check(self):
        if self.file_role:
            counting_num = self.countingTextBrowser.toPlainText()
            if len(counting_num) == 0:
                self.preview_text = counting_num
                self.msgLabel_4.setText("?????? ??????")
                self.doButton.setEnabled(False)
            else:
                for char_ in counting_num:
                    if not (48 <= ord(char_) <= 57):
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgbox.setWindowTitle("?????? ?????? ??????")
                        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        msgbox.setText("????????? ?????????????????????!")
                        msgbox.exec_()
                        self.countingTextBrowser.setText(self.preview_text)
                        return
                self.preview_text = counting_num
                self.check_row_and_text()
        else:
            counting_num = self.countingTextBrowser_2.toPlainText()
            if len(counting_num) == 0:
                self.preview_text = counting_num
                self.msgLabel_4.setText("?????? ??????")
                self.doButton.setEnabled(False)
            else:
                for char_ in counting_num:
                    if not (48 <= ord(char_) <= 57) and not (ord(char_) == 46):
                        msgbox = QtWidgets.QMessageBox()
                        msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                        msgbox.setWindowTitle("?????? ?????? ??????")
                        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        msgbox.setText("?????? ?????? ????????? ?????????????????????!")
                        msgbox.exec_()
                        self.countingTextBrowser_2.setText(self.preview_text)
                        return
                try:
                    float(counting_num)
                except:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgbox.setWindowTitle("?????? ?????? ??????")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgbox.setText("????????? ????????? ????????? ????????????!")
                    msgbox.exec_()
                    self.countingTextBrowser_2.setText(self.preview_text)
                    return
                self.preview_text = counting_num
                self.check_row_and_text()

    def check_row_and_text(self):
        if self.file_role:
            for i in range(self.fileLoadTableWidget.rowCount()):
                time_item = self.fileLoadTableWidget.item(i, 1).text()
                if float(time_item) / int(self.preview_text) < 0.1:
                    self.show_result(False)
                    self.msgLabel_4.setText("?????? ??????")
                    self.doButton.setEnabled(False)
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgbox.setWindowTitle("?????? ?????? ??????")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgbox.setText("?????? ????????? ?????? ????????? ???????????????.")
                    msgbox.exec_()
                    return
            if 1 >= int(self.preview_text) >= 0:
                self.show_result(False)
                self.msgLabel_4.setText("?????? ??????")
                self.doButton.setEnabled(False)
            else:
                self.calculate_expectancy()
                self.show_result(True)
                self.msgLabel_4.setText("?????? ??????")
                self.doButton.setEnabled(True)
        else:
            for i in range(self.fileLoadTableWidget.rowCount()):
                time_item = self.fileLoadTableWidget.item(i, 1).text()
                if float(self.preview_text) >= (float(time_item)-0.1):
                    self.show_result(False)
                    self.msgLabel_4.setText("?????? ??????")
                    self.doButton.setEnabled(False)
                    return
            if float(self.preview_text) < 0.1:
                self.show_result(False)
                self.msgLabel_4.setText("?????? ??????")
                self.doButton.setEnabled(False)
                msgbox = QtWidgets.QMessageBox()
                msgbox.setIcon(QtWidgets.QMessageBox.Warning)
                msgbox.setWindowTitle("?????? ?????? ??????")
                msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgbox.setText("0.1?????? ??? ?????? ??????????????????.")
                msgbox.exec_()
            else:
                self.calculate_expectancy()
                self.show_result(True)
                self.msgLabel_4.setText("?????? ??????")
                self.doButton.setEnabled(True)

    def save_locate_change(self):
        self.save_folder_name = self.saveTextBrowser.toPlainText()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = DivideDialog()
    main.show()
    sys.exit(app.exec_())
