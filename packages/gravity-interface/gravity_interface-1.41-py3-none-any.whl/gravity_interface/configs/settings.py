from tkinter import *
from glob import glob
import sys, os
from PIL import Image
from PIL import ImageTk


class Settings:
    ''' Модуль для всех настроек терминала'''

    def __init__(self, root, dirpath):
        self.project_name = 'Gravity interface'
        # SCREEN SIZES#
        # self.screenwidth = root.winfo_screenwidth()
        self.screenwidth = 1366
        w = self.screenwidth
        # self.screenheight = root.winfo_screenheight()
        self.screenheight = 768
        h = self.screenheight
        print(w, h)
        self.screensize = (self.screenwidth, self.screenheight)
        self.screencenter = (self.screenwidth / 2, self.screenheight / 2)
        self.w = w
        self.h = h
        self.exit_gate = 'exit_gate_arrow'
        self.entry_gate = 'entry_gate_arrow'
        self.orup_enter_comm = 'orup_extended'
        self.orup_exit_comm = 'orup_short'
        # GATEICONS#
        self.bw = 1320
        self.bh = 653
        self.bwS = 450
        self.bhS = 600
        self.weight_show_posses = (w / 1.8699520876112252, h / 1.0924608819345663)
        # DIRPATHS#
        self.rootdir = dirpath
        self.imgsysdir = os.path.join(dirpath, 'imgs') + os.sep

        self.settingsfile = os.path.join(dirpath, 'settings.py')

        self.slideanimpath = os.path.join(dirpath, 'slideanim')
        self.mainscreenpath = r'%s\imgs\mainscreen.png' % dirpath
        # SCREENS#
        self.frontscreen = ('frontscreen.png', 80, 0,
                            PhotoImage(file=self.imgsysdir + 'frontscreen.png'))
        self.shadow = ('shadow.png', w / 2, h / 2,
                       PhotoImage(file=self.imgsysdir + 'shadow.png'))
        self.backscreen = ('backscreen.png', w / 2, h / 2,
                           PhotoImage(file=self.imgsysdir + 'backscreen.png'))
        self.accessscreen = [('access.png', 1600, 900)]
        self.blockwinB = ('dellwin.png', 0, 0,
                          PhotoImage(file=self.imgsysdir + 'blockwinB.png'))
        self.blockwinS = ('dellwin.png', 0, 0,
                          PhotoImage(file=self.imgsysdir + 'blockwinS.png'))
        self.toolbar = ('toolbar.png', self.w / 19.104895, self.h / 2.0026,
                        PhotoImage(file=self.imgsysdir + 'toolbar.png'))
        self.road = ('road.png', w / 2, h / 1.1327767780760494,
                     PhotoImage(file=self.imgsysdir + 'road.png'))
        self.disputs = ('disputs.png', w / 1.4, h / 2,
                        PhotoImage(file=self.imgsysdir + 'disputswin.png'))
        self.calendarModer = ('calendar.png', w / 3.7, h / 1.53,
                              PhotoImage(file=self.imgsysdir + 'calendarwin.png'))
        self.calendarUsual = ('calendar.png', w / 3.7, h / 2.9,
                              PhotoImage(file=self.imgsysdir + 'calendarwin.png'))
        self.choosePolWin = ('choosePolWin.png', w / 3.7, h / 4.82,
                             PhotoImage(file=self.imgsysdir + 'choosePol.png'))
        self.order = ('order', w / 4.599326, h / 3.09054,
                      PhotoImage(file=self.imgsysdir + 'order.png'))
        self.currentEvents = ('order', w / 1.504405, h / 3.090543,
                              PhotoImage(file=self.imgsysdir + 'currentEvents.png'))
        # self.auth_logo = ('auth_logo',w/2,h/2,
        #	PhotoImage(file=self.imgsysdir + 'auth_logo.png'))
        self.statisticwin = ('statisticwin', w / 1.9, h / 2,
                             PhotoImage(file=self.imgsysdir + 'statisticwin.png'))
        self.orupWinUs = ('orupwinus', w / 1.9486447931526392, h / 2,
                          PhotoImage(file=self.imgsysdir + 'orupwinus.png'))
        self.record_change_win = ('record_change_win', w / 1.9486447931526392, h / 2,
                                  PhotoImage(file=self.imgsysdir + 'record_change_win.png'))
        self.orupWinEx = ('orupwinex', w / 2, h / 2,
                          PhotoImage(file=self.imgsysdir + 'orupwinex.png'))
        self.lateConfirmWin = ('lateConfirmWin', w / 2, h / 2,
                               PhotoImage(file=self.imgsysdir + 'lateconfirmwin.png'))
        self.redbg = ('redbg', w / 2, h / 2,
                      PhotoImage(file=self.imgsysdir + 'redbg.png'))
        self.redbgEx = ('redbgEx', w / 2, h / 2,
                        PhotoImage(file=self.imgsysdir + 'redbgOrupEx.png'))
        self.check_off = ('check_off', w / 2, h / 2,
                          PhotoImage(file=self.imgsysdir + 'check_off.gif'))
        self.check_on = ('check_on', w / 2, h / 2,
                         PhotoImage(file=self.imgsysdir + 'check_on.gif'))

        # OTHER OBJECTS#
        self.exit_gate_arrow = ('exit_gate_arrow', w / 2.51, h / 1.24,
                                PhotoImage(file=self.imgsysdir + 'gate_arrow.png'))
        self.entry_gate_arrow = ('entry_gate_arrow', w / 1.418, h / 1.24,
                                 PhotoImage(file=self.imgsysdir + 'gate_arrow.png'))
        self.car_in_icon = ('car_in', w / 2, h / 2,
                            PhotoImage(file=self.imgsysdir + 'car_in.png'))
        self.car_out_icon = ('car_out', w / 2, h / 2,
                             PhotoImage(file=self.imgsysdir + 'car_out.png'))
        self.logo = ('logo', w / 2, h / 2.8,
                     PhotoImage(file=self.imgsysdir + 'logo.png'))
        self.lateCars = ('lateCars', w / 1.9, h / 3.17,
                         PhotoImage(file=self.imgsysdir + 'latecarswin.png'))
        self.forbWin = ('forbwin', w / 1.9, h / 2,
                        PhotoImage(file=self.imgsysdir + 'forbwin.png'))
        self.sysNot = ('sysNot', w / 1.9, h / 2,
                       PhotoImage(file=self.imgsysdir + 'sysnotwin.png'))
        self.gradient = ('gradient', 0, 0,
                         PhotoImage(file=self.imgsysdir + 'gradient.png'))
        self.login = ('login', w / 2, h / 2,
                      PhotoImage(file=self.imgsysdir + 'login.png'))
        self.password = ('password', w / 2, h / 1.63,
                         PhotoImage(file=self.imgsysdir + 'pw.png'))
        self.chatwin = ('chatwin', self.w / 2, self.h / 2,
                        PhotoImage(file=self.imgsysdir + 'chatwin.png'))
        self.ensureCloseRec = ('ensureCloseRec', w / 2, self.h / 2,
                               PhotoImage(file=self.imgsysdir + 'ensureCloseRec.png'))
        self.exitwin = ('chatwin', w / 2, self.h / 2,
                        PhotoImage(file=self.imgsysdir + 'exitwin.png'))
        self.pw = (w / 2, h / 2.8, Entry(root, bd=5, width=20, show="*"))
        self.picker = PhotoImage(file=self.imgsysdir + 'picker.png')


        self.notifIconAlert = ('notifAlert.png',w / 18.871, h / 1.6781, 'operator.sysNot.openWin()',
                         PhotoImage(file=self.imgsysdir + 'sysnotAlert.png'), 25, 25, 'toolbarBtn.TButton',
                         PhotoImage(file=self.imgsysdir + 'sysnotAlertZ.png'))
        self.mailIconUs = ('mailUs', w / 30, h / 3.491, 'operator.mailroom.openWin()',
                           PhotoImage(file=self.imgsysdir + 'mail.png'), 25, 25)
        self.mailIconAlert = ('mailAlert.png', w / 30, h / 3.491, 'operator.mailroom.openWin()',
                              PhotoImage(file=self.imgsysdir + 'mailAlert.png'), 25, 25)
        # BUTTONS#
        self.mainLogoBtn = ('mainL.png', w / 19.0609, h / 2.5282, 'operator.mainPage.openWin()',
                            PhotoImage(file=self.imgsysdir + 'mainL.png'), 25, 25, 'toolbarBtn.TButton',
                            PhotoImage(file=self.imgsysdir + 'mainLZ.png'))
        self.exitBtn = ('exit.png', w / 1.02429, h / 19.893796, 'self.drawExitWin()',
                        PhotoImage(file=self.imgsysdir + 'exit.png'), 25, 25, 'onGreyBtn.TButton',
                        PhotoImage(file=self.imgsysdir + 'exitZ.png'))
        self.forbListBtn = ('forblist.png', w / 30, 476,
                            'operator.forbList.openWin()',
                            PhotoImage(file=self.imgsysdir + 'forblist.png'), 25, 25, 'toolbarBtn.TButton',
                            PhotoImage(file=self.imgsysdir + 'forblistZ.png'))
        self.statisticBtn = ('statistic.png', w / 18.9669, h / 2.01619,
                             'operator.statP.openWin()',
                             PhotoImage(file=self.imgsysdir + 'statistic.png'), 25, 25, 'toolbarBtn.TButton',
                             PhotoImage(file=self.imgsysdir + 'statisticZ.png'))
        self.notifBtn = ('notifUs', w / 18.871, h / 1.6781, 'operator.sysNot.openWin()',
                         PhotoImage(file=self.imgsysdir + 'sysnot.png'), 25, 25, 'toolbarBtn.TButton',
                         PhotoImage(file=self.imgsysdir + 'sysnotZ.png'))
        self.lockBtn = ('lock.png', w / 1.0459778, h / 19.893796, 'operator.authWin.openWin()',
                        PhotoImage(file=self.imgsysdir + 'lock.png'), 25, 25, 'onGreyBtn.TButton',
                        PhotoImage(file=self.imgsysdir + 'lockZ.png'))
        self.toolBarBtns = [
            self.mainLogoBtn,
            self.statisticBtn,
            self.notifBtn,
        ]
        self.statBtns = [
            ('Ок', w / 1.12, h / 4.91, 'operator.statP.showStat()',
             PhotoImage(file=self.imgsysdir + 'ok.png'), 25, 25, "toolbarBtn.TButton",
             PhotoImage(file=self.imgsysdir + 'okZ.png')),
            ('Сбросить', w / 1.12, h / 3.78, 'operator.statP.abortFiltres()',
             PhotoImage(file=self.imgsysdir + 'abortFiltres.png'), 25, 25, "toolbarBtn.TButton",
             PhotoImage(file=self.imgsysdir + 'abortFiltresZ.png'))]
        self.disputsBtns = []
        # ('Выбрать',w/3.7,h/3.5,'operator.mailroom.upLowNow()',
        # hotoImage(file=self.imgsysdir + 'choose.png'),25,25),]

        orupAct = 'self.orupAct(call_method="manual")'
        orupActExit = 'self.orupActExit(call_method="manual")'
        self.orupEnterBtns = [
            ('accept.png', w / 1.6032, h / 1.4,
             'self.initOrupAct()',
             PhotoImage(file=self.imgsysdir + 'accept.png'), 100, 25, "onORUPbtn.TButton",
             PhotoImage(file=self.imgsysdir + 'acceptZ.png')),
            ('abort.png', w / 2.4927, h / 1.4,
             'self.destroyORUP(mode="decline")',
             PhotoImage(file=self.imgsysdir + 'abort.png'), 100, 25, "onORUPbtn.TButton",
             PhotoImage(file=self.imgsysdir + 'abortZ.png'))]
        self.orupExitBtns = [('newcar.png', w / 1.55, h / 2.30,
                              'self.big_orup_exit()',
                              PhotoImage(file=self.imgsysdir + 'newCar.png'), 40, 25, "onORUPbtn.TButton"),
                             ('accept.png', w / 1.7, h / 1.6,
                              'self.launchExitProtocol()',
                              PhotoImage(file=self.imgsysdir + 'accept.png'), 80, 25, "onORUPbtn.TButton",
                              PhotoImage(file=self.imgsysdir + 'acceptZ.png')),
                             ('abort.png', w / 2.45, h / 1.6,
                              'self.destroyORUP(mode="decline")',
                              PhotoImage(file=self.imgsysdir + 'abort.png'), 80, 25, "onORUPbtn.TButton",
                              PhotoImage(file=self.imgsysdir + 'abortZ.png'))]
        self.yesCloseAppBtn = [('yes.png', w / 2.3, h / 1.85,
                                'operator.closeApp()',
                                PhotoImage(file=self.imgsysdir + 'yes.png'), 40, 25, "onORUPbtn.TButton",
                                PhotoImage(file=self.imgsysdir + 'yesZ.png'))]
        self.yesCloseRecBtn = [('yes.png', w / 2.3, h / 1.85,
                                'operator.mainPage.closeRecord(self.record_id)',
                                PhotoImage(file=self.imgsysdir + 'yes.png'), 40, 25, "onORUPbtn.TButton",
                                PhotoImage(file=self.imgsysdir + 'yesZ.png'))]
        self.manual_control_info_bar = ('manual_control_info_bar.png', w / 1.85, h / 2.5,
                                        PhotoImage(file=self.imgsysdir + 'manual_control_info_bar.png'))
        self.manual_gate_control_btn = [('open.png', w / 9, h / 1.0477489768076398,
                                         'operator.manual_gate_control.openWin()',
                                         PhotoImage(file=self.imgsysdir + 'manual_gate_control.png'), 150, 25,
                                         "onORUPbtn.TButton",
                                         PhotoImage(file=self.imgsysdir + 'manual_gate_controlZ.png'))]

        self.manual_open_internal_gate_btn = [('open.png', w / 2.887949260042283, h / 1.0477489768076398,
                                               'operator.manual_gate_control.send_gate_comm("exit", "open")',
                                               PhotoImage(file=self.imgsysdir + 'open.png'), 60, 25,
                                               'onGreyBtn.TButton',
                                               PhotoImage(file=self.imgsysdir + 'openZ.png'))]
        self.manual_close_internal_gate_btn = [('close.png', w / 4.087949260042283, h / 1.0477489768076398,
                                                'operator.manual_gate_control.send_gate_comm("exit", "close")',
                                                PhotoImage(file=self.imgsysdir + 'close.png'), 60, 25,
                                                'onGreyBtn.TButton',
                                                PhotoImage(file=self.imgsysdir + 'closeZ.png'))]
        self.manual_open_external_gate_btn = [('open.png', w / 1.3742454728370221, h / 1.0477489768076398,
                                               'operator.manual_gate_control.send_gate_comm("entry", "open")',
                                               PhotoImage(file=self.imgsysdir + 'open.png'), 60, 25,
                                               'onGreyBtn.TButton',
                                               PhotoImage(file=self.imgsysdir + 'openZ.png'))]
        self.manual_close_external_gate_btn = [('close.png', w / 1.2042454728370221, h / 1.0477489768076398,
                                                'operator.manual_gate_control.send_gate_comm("entry", "close")',
                                                PhotoImage(file=self.imgsysdir + 'close.png'), 60, 25,
                                                'onGreyBtn.TButton',
                                                PhotoImage(file=self.imgsysdir + 'closeZ.png'))]

        self.auto_gate_control_btn = [('auto_gate_control', w / 9, h / 1.0477489768076398,
                                       'operator.mainPage.openWin()',
                                       PhotoImage(file=self.imgsysdir + 'auto_gate_control.png'), 150, 25,
                                       "onORUPbtn.TButton",
                                       PhotoImage(file=self.imgsysdir + 'auto_gate_controlZ.png'))]
        self.record_change_btns = [('change.png', w / 1.6032, h / 1.4, 'self.change_record()',
                                    PhotoImage(file=self.imgsysdir + 'change.png'), 100, 25, "onORUPbtn.TButton",
                                    PhotoImage(file=self.imgsysdir + 'changeZ.png')),

                                   ('cancel.png', self.w / 2.4927, self.h / 1.4, 'self.destroyORUP(mode="decline")',
                                    PhotoImage(file=self.imgsysdir + 'cancel.png'), 100, 25, "onORUPbtn.TButton",
                                    PhotoImage(file=self.imgsysdir + 'cancelZ.png'))]
        self.noCloseBlockImg = [('no.png', w / 1.75, h / 1.85, 'self.destroyBlockImg(mode="total")',
                                 PhotoImage(file=self.imgsysdir + 'no.png'), 40, 25, "onORUPbtn.TButton",
                                 PhotoImage(file=self.imgsysdir + 'noZ.png'))]
        self.exitBtns = self.yesCloseAppBtn + self.noCloseBlockImg
        self.closeRecBtns = self.yesCloseRecBtn + self.noCloseBlockImg
        self.entry_gate_base = ('gate_base.png', w / 2.619367209971237, h / 1.1574981160512434,
                                PhotoImage(file=self.imgsysdir + 'gate_base.png'))
        self.exit_gate_base = ('gate_base.png', w / 1.4501061571125264, h / 1.1574981160512434,
                               PhotoImage(file=self.imgsysdir + 'gate_base.png'))
        # self.entry_gate_base = ('gate_base.png',w/2.82,h/1.211,
        #	PhotoImage(file=self.imgsysdir + 'gate_base.png'))
        self.gateBtns = [
            ('open_internal.png', w / 2.887949260042283, h / 1.0477489768076398, orupActExit,
             PhotoImage(file=self.imgsysdir + 'open.png'), 60, 25, 'onGreyBtn.TButton',
             PhotoImage(file=self.imgsysdir + 'openZ.png')),
            ('open_external.png', w / 1.3742454728370221, h / 1.0477489768076398, orupAct,
             PhotoImage(file=self.imgsysdir + 'open.png'), 60, 25, 'onGreyBtn.TButton',
             PhotoImage(file=self.imgsysdir + 'openZ.png'))]
        self.authBtns = [
            ('exit.png', w / 1.04, h / 30, 'operator.closeApp()',
             PhotoImage(file=self.imgsysdir + 'exit.png'), 25, 25, 'authWinBtn.TButton',
             PhotoImage(file=self.imgsysdir + 'exitZ.png')),
            ('enter.png', w / 2, h / 1.40, 'self.tryLogin()',
             PhotoImage(file=self.imgsysdir + 'enter.png'), 25, 25, 'authWinBtn.TButton',
             PhotoImage(file=self.imgsysdir + 'enterZ.png'))]
        self.blockWinBtns = [('close.png',
                              PhotoImage(file=self.imgsysdir + 'close.png'), self.bw / 2,
                              self.bh / 1.1, 'operator.destroyBlockWin()')]
        self.closeAuto = [('close.png',
                           PhotoImage(file=self.imgsysdir + 'close.png'), self.bw / 2,
                           self.bh / 1.1, 'operator.lateCars.drawConfirmWin()')]

        self.addComm = ('addComm', self.w / 2, self.h / 2,
                        PhotoImage(file=self.imgsysdir + 'addComm.png'))
        self.addCommAccept = ('accept.png', self.w / 1.71, self.h / 1.6,
                              'self.add_comm()', PhotoImage(file=self.imgsysdir + 'accept.png'), 80, 25,
                              "onORUPbtn.TButton",
                              PhotoImage(file=self.imgsysdir + 'acceptZ.png'))
        self.addCommAbort = ('cancel.png', self.w / 2.41, self.h / 1.6, 'self.destroyBlockImg(mode="total")',
                             PhotoImage(file=self.imgsysdir + 'cancel.png'), 80, 25, "onORUPbtn.TButton",
                             PhotoImage(file=self.imgsysdir + 'cancelZ.png'))
        self.addCommBtns = [self.addCommAccept, self.addCommAbort]

        self.lateConfirmBtns = [('yes.png', w / 2.3, h / 1.85,
                                 'operator.closeAuto()', PhotoImage(file=self.imgsysdir + 'yes.png'), 40, 25),
                                ('no.png', w / 1.75, h / 1.85,
                                 'operator.lateCars.destroyBlockImg(mode="total"")',
                                 PhotoImage(file=self.imgsysdir + 'no.png'), 40, 25)]
        self.blockWinBtnsS = [('close.png',
                               PhotoImage(file=self.imgsysdir + 'close.png'), self.bwS / 2,
                               self.bhS / 1.1, 'operator.destroyBlockWin()')]
        self.entry = [('entry.png', w / 3.879, h / 3.303, '...')]
        self.copybtn = [('copy.png', w / 1.707, h / 1.407,
                         'operator.current.admincopy()')]
        self.copyherebtn = [('copyhere.png', w / 1.347, h / 1.407,
                             'operator.current.determine_dway("admin")')]
        # List generators for ojects #

        self.slanimimgs = [PhotoImage(file=x) for x in
                           glob(self.slideanimpath + '//*')]
        self.clomimgs = [PhotoImage(file=x) for x in
                         glob(self.slideanimpath + '//*')]

        # Данные для рисовки мультика
        self.right_pos = self.w / 1.34581, self.h / 1.29729
        self.center_pos = self.w / 2.25, self.h / 1.4014
        self.left_pos = self.w / 5.4859, self.h / 1.29729
        self.car_poses = {'r': self.right_pos, 'c': self.center_pos, 'l': self.left_pos}
        self.car_face_info = {'enter': 'car_out_icon', 'exit': 'car_in_icon'}

    def getImgPath(self, rootdir, imgname):
        dir = os.path.join(rootdir, imgname)
        ph = os.path.join(dir, imgname)
        return ph
