"""
UBX configuration container dialog

This is the pop-up dialog containing the various
UBX configuration widgets

Created on 19 Sep 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name, too-many-instance-attributes, too-many-ancestors

from tkinter import (
    Toplevel,
    Frame,
    Button,
    Label,
    StringVar,
    N,
    S,
    E,
    W,
    LEFT,
)
from PIL import ImageTk, Image
from .globals import (
    BGCOL,
    FGCOL,
    ICON_EXIT,
    UBX_MONVER,
    UBX_MONHW,
    UBX_CFGPRT,
    UBX_CFGRATE,
    UBX_CFGMSG,
    UBX_CFGVAL,
    UBX_PRESET,
)
from .strings import LBLUBXCONFIG, DLGUBXCONFIG
from .ubx_info_frame import UBX_INFO_Frame
from .ubx_port_frame import UBX_PORT_Frame
from .ubx_msgrate_frame import UBX_MSGRATE_Frame
from .ubx_preset_frame import UBX_PRESET_Frame
from .ubx_cfgval_frame import UBX_CFGVAL_Frame
from .ubx_solrate_frame import UBX_RATE_Frame


class UBXConfigDialog:
    """,
    UBXConfigDialog class.
    """

    def __init__(self, app, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Constructor.

        :param Frame app: reference to main tkinter application
        :param args: optional args to pass to parent class (not currently used)
        :param kwargs: optional kwargs to pass to parent class (not currently used)
        """

        self.__app = app  # Reference to main application class
        self.__master = self.__app.get_master()  # Reference to root class (Tk)
        self._dialog = Toplevel()
        self._dialog.transient(self.__app)
        self._dialog.resizable(False, False)
        self._dialog.title = DLGUBXCONFIG
        self._dialog.protocol("WM_DELETE_WINDOW", self.on_exit)
        # roughly center dialog in master window
        # NB: this works on Windows and MacOS but not on some Linux
        dw = 780
        dh = 470
        mx = self.__master.winfo_x()
        my = self.__master.winfo_y()
        mw = self.__master.winfo_width()
        mh = self.__master.winfo_height()
        self._dialog.geometry(f"+{int(mx + (mw/2 - dw/2))}+{int(my + (mh/2 - dh/2))}")
        self._img_exit = ImageTk.PhotoImage(Image.open(ICON_EXIT))
        self._cfg_msg_command = None
        self._pending_confs = {
            UBX_MONVER: (),
            UBX_MONHW: (),
            UBX_CFGPRT: (),
            UBX_CFGMSG: (),
            UBX_CFGVAL: (),
            UBX_PRESET: (),
            UBX_CFGRATE: (),
        }
        self._status = StringVar()
        self._status_cfgmsg = StringVar()

        self._body()
        self._do_layout()
        self._reset()

    def _body(self):
        """
        Set up frame and widgets.
        """

        self._frm_container = Frame(self._dialog, borderwidth=2, relief="groove")
        self._lbl_title = Label(
            self._frm_container,
            text=LBLUBXCONFIG,
            bg=BGCOL,
            fg=FGCOL,
            justify=LEFT,
            font=self.__app.font_md,
        )
        self._frm_status = Frame(self._frm_container, borderwidth=2, relief="groove")
        self._lbl_status = Label(
            self._frm_status, textvariable=self._status, anchor="w"
        )
        self._btn_exit = Button(
            self._frm_status,
            image=self._img_exit,
            width=50,
            fg="red",
            command=self.on_exit,
            font=self.__app.font_md,
        )
        # add configuration widgets
        self._frm_device_info = UBX_INFO_Frame(
            self.__app, self, borderwidth=2, relief="groove"
        )
        self._frm_config_port = UBX_PORT_Frame(
            self.__app, self, borderwidth=2, relief="groove"
        )
        self._frm_config_rate = UBX_RATE_Frame(
            self.__app, self, borderwidth=2, relief="groove"
        )
        self._frm_config_msg = UBX_MSGRATE_Frame(
            self.__app, self, borderwidth=2, relief="groove"
        )
        self._frm_configdb = UBX_CFGVAL_Frame(
            self.__app, self, borderwidth=2, relief="groove"
        )
        self._frm_preset = UBX_PRESET_Frame(
            self.__app, self, borderwidth=2, relief="groove"
        )

    def _do_layout(self):
        """
        Position widgets in frame.
        """

        # top of grid
        col = 0
        row = 0
        self._frm_container.grid(
            column=col,
            row=row,
            columnspan=12,
            rowspan=22,
            padx=3,
            pady=3,
            ipadx=5,
            ipady=5,
            sticky=(N, S, W, E),
        )
        self._lbl_title.grid(column=col, row=row, columnspan=12, ipadx=3, sticky=(W, E))
        # left column of grid
        rowsp = 1
        for frm in (
            self._frm_device_info,
            self._frm_config_port,
            self._frm_config_rate,
            self._frm_config_msg,
        ):
            row += rowsp
            (colsp, rowsp) = frm.grid_size()
            frm.grid(
                column=col,
                row=row,
                columnspan=colsp,
                rowspan=rowsp,
                sticky=(N, S, W, E),
            )
        # right column of grid
        row = 0
        rowsp = 1
        col += colsp
        for frm in (self._frm_configdb, self._frm_preset):
            row += rowsp
            (colsp, rowsp) = frm.grid_size()
            frm.grid(
                column=col,
                row=row,
                columnspan=colsp,
                rowspan=rowsp,
                sticky=(N, S, W, E),
            )
        # bottom of grid
        col = 0
        row += rowsp
        (colsp, rowsp) = self._frm_container.grid_size()
        self._frm_status.grid(column=col, row=row, columnspan=colsp, sticky=(W, E))
        self._lbl_status.grid(
            column=0, row=0, columnspan=colsp - 1, ipadx=3, ipady=3, sticky=(W, E)
        )
        self._btn_exit.grid(column=colsp - 1, row=0, ipadx=3, ipady=3, sticky=(E))

        for frm in (self._frm_container, self._frm_status):
            for i in range(colsp):
                frm.grid_columnconfigure(i, weight=1)
            for i in range(rowsp):
                frm.grid_rowconfigure(i, weight=1)

        self._frm_container.option_add("*Font", self.__app.font_sm)
        self._frm_status.option_add("*Font", self.__app.font_sm)

    def _reset(self):
        """
        Reset configuration widgets.
        """

        self._frm_config_rate.reset()
        self._frm_config_port.reset()
        self._frm_device_info.reset()

    def set_pending(self, key: int, val: list):
        """
        Set pending confirmation flag for configuration widget to
        signify that it's waiting for a confirmation message.

        :param int key: integer representing UBX configuration widget (0-6)
        :param list val: list of confirmation messages that widget is awaiting
        """

        self._pending_confs[key] = val

    def update_pending(self, cfgtype, **kwargs):
        """
        Receives polled confirmation message from the ubx_handler and
        updates the widget that is waiting for this confirmation.

        :param str cfgtype: identity of UBX message containing config info
        :param kwargs: status keywords and values from UBX config message
        """

        for (key, val) in self._pending_confs.items():
            if cfgtype in val:
                self.set_status(
                    f"{cfgtype} GET message received",
                    "red" if cfgtype == "ACK-NAK" else "green",
                )
                self._pending_confs[key] = ()  # reset awaiting conf flag
                if key == UBX_MONVER:
                    self._frm_device_info.update_status(cfgtype, **kwargs)
                elif key == UBX_MONHW:
                    self._frm_device_info.update_status(cfgtype, **kwargs)
                elif key == UBX_CFGPRT:
                    self._frm_config_port.update_status(cfgtype, **kwargs)
                elif key == UBX_CFGRATE:
                    self._frm_config_rate.update_status(cfgtype, **kwargs)
                elif key == UBX_CFGMSG:
                    self._frm_config_msg.update_status(cfgtype, **kwargs)
                elif key == UBX_CFGVAL:
                    self._frm_configdb.update_status(cfgtype, **kwargs)
                elif key == UBX_PRESET:
                    self._frm_preset.update_status(cfgtype, **kwargs)

    def set_status(self, message: str, color: str = "blue"):
        """
        Set status message.

        :param str message: message to be displayed
        :param str color: rgb color of text (blue)
        """

        message = (message[:120] + "..") if len(message) > 120 else message
        self._lbl_status.config(fg=color)
        self._status.set("  " + message)

    def on_exit(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Handle Exit button press.
        """

        self.__master.update_idletasks()
        self.__app.stop_config_thread()
        self._dialog.destroy()

    def get_size(self):
        """
        Get current frame size.

        :return: window size (width, height)
        :rtype: tuple
        """

        self.__master.update_idletasks()  # Make sure we know about any resizing
        return (self._dialog.winfo_width(), self._dialog.winfo_height())

    @property
    def container(self):
        """
        Getter for container frame.

        :return: reference to container frame
        :rtype: tkinter.Frame
        """

        return self._frm_container
