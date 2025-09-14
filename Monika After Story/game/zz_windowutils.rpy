


default persistent._mas_enable_notifications = False


default persistent._mas_notification_sounds = True


default persistent._mas_windowreacts_windowreacts_enabled = False


default persistent._mas_windowreacts_database = dict()


default persistent._mas_windowreacts_no_unlock_list = list()


default persistent._mas_windowreacts_notif_filters = dict()

init -10 python in mas_windowreacts:

    can_show_notifs = True


    can_do_windowreacts = True


    windowreact_db = {}




    _groups_list = [
        "Alerta de temas",
        "Reacciones de ventana",
    ]

init python in mas_windowutils:
    import os

    import store
    from store import mas_utils



    MAS_WINDOW = None


    if renpy.windows:
        
        import sys
        sys.path.append(renpy.config.gamedir + '\\python-packages\\')
        
        
        try:
            
            import win32gui
            
            import win32api
            
            
            import balloontip
            
            
            from win32gui import GetWindowText, GetForegroundWindow
            
            
            _m1_zz_windowutils__tip = balloontip.WindowsBalloonTip()
            
            
            _m1_zz_windowutils__tip.hwnd = None
        
        except Exception as e:
            
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            
            
            store.mas_utils.mas_log.warning(
                "win32api/win32gui failed to be imported, disabling notifications: {}".format(e)
            )

    elif renpy.linux:
        
        session_type = os.environ.get("XDG_SESSION_TYPE")
        
        
        if session_type == "wayland":
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            store.mas_utils.mas_log.warning("Wayland is not yet supported, disabling notifications.")
        
        
        elif session_type == "x11":
            try:
                import Xlib
                
                from Xlib.display import Display
                from Xlib.error import BadWindow, XError
                
                _m1_zz_windowutils__display = Display()
                _m1_zz_windowutils__root = _m1_zz_windowutils__display.screen().root
            
            except Exception as e:
                store.mas_windowreacts.can_show_notifs = False
                store.mas_windowreacts.can_do_windowreacts = False
                
                store.mas_utils.mas_log.warning(
                    "Xlib failed to be imported, disabling notifications: {}".format(e)
                )
        
        else:
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            
            store.mas_utils.mas_log.warning("Cannot detect current session type, disabling notifications.")

    else:
        store.mas_windowreacts.can_do_windowreacts = False


    class MASWindowFoundException(Exception):
        """
        Custom exception class to flag a window found during a window enum

        Has the hwnd as a property
        """
        def __init__(self, hwnd):
            self.hwnd = hwnd
        
        def __str__(self):
            return self.hwnd


    DEF_MOUSE_POS_RETURN = (0, 0)



    def _m1_zz_windowutils__getActiveWindowObj_Linux():
        """
        Gets the active window object

        OUT:
            Xlib.display.Window, or None if errors occur (or not possible to get window obj)
        """
        
        if not store.mas_windowreacts.can_do_windowreacts:
            return None
        
        NET_ACTIVE_WINDOW = _m1_zz_windowutils__display.intern_atom("_NET_ACTIVE_WINDOW")
        
        
        active_winid_prop = _m1_zz_windowutils__root.get_full_property(NET_ACTIVE_WINDOW, 0)
        
        if active_winid_prop is None:
            return None
        
        active_winid = active_winid_prop.value[0]
        
        try:
            return _m1_zz_windowutils__display.create_resource_object("window", active_winid)
        except XError as e:
            mas_utils.mas_log.error("Failed to get active window object: {}".format(e))
            return None

    def _m1_zz_windowutils__getMASWindowLinux():
        """
        Funtion to get the MAS window on Linux systems

        OUT:
            Xlib.display.Window representing the MAS window

        ASSUMES: OS IS LINUX (renpy.linux)
        """
        
        if not store.mas_windowreacts.can_do_windowreacts:
            return None
        
        NET_CLIENT_LIST_ATOM = _m1_zz_windowutils__display.intern_atom('_NET_CLIENT_LIST', False)
        
        try:
            prop = _m1_zz_windowutils__root.get_full_property(NET_CLIENT_LIST_ATOM, 0)
            
            
            if prop is None:
                return
            
            winid_list = prop.value
            for winid in winid_list:
                win = _m1_zz_windowutils__display.create_resource_object("window", winid)
                transient_for = win.get_wm_transient_for()
                winname = win.get_wm_name()
                
                if transient_for is None and winname and store.mas_getWindowTitle() == winname:
                    return win
        
        except XError as e:
            mas_utils.mas_log.error("Failed to get MAS window object: {}".format(e))
            return None

    def _m1_zz_windowutils__getMASWindowHWND():
        """
        Gets the hWnd of the MAS window

        NOTE: Windows ONLY

        OUT:
            int - represents the hWnd of the MAS window
        """
        
        if not store.mas_windowreacts.can_do_windowreacts:
            return None
        
        def checkMASWindow(hwnd, lParam):
            """
            Internal function to identify the MAS window. Raises an exception when found to allow the main func to return
            """
            if store.mas_getWindowTitle() == win32gui.GetWindowText(hwnd):
                raise MASWindowFoundException(hwnd)
        
        try:
            win32gui.EnumWindows(checkMASWindow, None)
        
        except MASWindowFoundException as e:
            return e.hwnd
        
        mas_utils.mas_log.error("Failed to get MAS window hwnd")
        return None

    def _m1_zz_windowutils__getAbsoluteGeometry(win):
        """
        Returns the (x, y, height, width) of a window relative to the top-left
        of the screen.

        IN:
            win - Xlib.display.Window object representing the window we wish to get absolute geometry of

        OUT:
            tuple, (x, y, width, height) if possible, otherwise None
        """
        
        if win is None:
            
            win = _setMASWindow()
            if win is None:
                return None
        
        try:
            geom = win.get_geometry()
            (x, y) = (geom.x, geom.y)
            
            while True:
                parent = win.query_tree().parent
                pgeom = parent.get_geometry()
                x += pgeom.x
                y += pgeom.y
                if parent.id == _m1_zz_windowutils__root.id:
                    break
                win = parent
            
            return (x, y, geom.width, geom.height)
        
        except Xlib.error.BadDrawable:
            
            _setMASWindow()
        
        except XError as e:
            mas_utils.mas_log.error("Failed to get window geometry: {}".format(e))
        
        return None

    def _setMASWindow():
        """
        Sets the MAS_WINDOW global on Linux systems

        OUT:
            the window object
        """
        global MAS_WINDOW
        
        if renpy.linux:
            MAS_WINDOW = _m1_zz_windowutils__getMASWindowLinux()
        
        else:
            MAS_WINDOW = None
        
        return MAS_WINDOW


    def _getActiveWindowHandle_Windows():
        """
        Funtion to get the active window on Windows systems

        OUT:
            string representing the active window handle

        ASSUMES: OS IS WINDOWS (renpy.windows)
        """
        return unicode(GetWindowText(GetForegroundWindow()))

    def _getActiveWindowHandle_Linux():
        """
        Funtion to get the active window on Linux systems

        OUT:
            string representing the active window handle

        ASSUMES: OS IS LINUX (renpy.linux)
        """
        NET_WM_NAME = _m1_zz_windowutils__display.intern_atom("_NET_WM_NAME")
        active_winobj = _m1_zz_windowutils__getActiveWindowObj_Linux()
        
        if active_winobj is None:
            return ""
        
        try:
            
            active_winname_prop = active_winobj.get_full_property(NET_WM_NAME, 0)
            
            if active_winname_prop is not None:
                active_winname = unicode(active_winname_prop.value, encoding = "utf-8")
                return active_winname.replace("\n", "")
            
            else:
                return ""
        
        except BadWindow:
            return ""
        
        except XError as e:
            mas_utils.mas_log.error("Failed to get active window handle: {}".format(e))
        
        return ""

    def _getActiveWindowHandle_OSX():
        """
        Gets the active window on macOS

        NOTE: This currently just returns an empty string, this is because we do not have active window detection
        for MacOS
        """
        return ""


    def _tryShowNotification_Windows(title, body):
        """
        Tries to push a notification to the notification center on Windows.
        If it can't it should fail silently to the user.

        IN:
            title - notification title
            body - notification body

        OUT:
            bool. True if the notification was successfully sent, False otherwise
        """
        
        notif_success = _m1_zz_windowutils__tip.showWindow(title, body)
        
        
        store.destroy_list.append(_m1_zz_windowutils__tip.hwnd)
        return notif_success

    def _tryShowNotification_Linux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.

        IN:
            title - notification title
            body - notification body

        OUT:
            bool - True, representing the notification's success
        """
        
        
        
        body  = body.replace("'", "'\\''")
        title = title.replace("'", "'\\''") 
        os.system("notify-send '{0}' '{1}' -a 'Monika' -u low".format(title, body))
        return True

    def _tryShowNotification_OSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.

        IN:
            title - notification title
            body - notification body

        OUT:
            bool - True, representing the notification's success
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body, title))
        return True


    def _getAbsoluteMousePos_Windows():
        """
        Returns an (x, y) co-ord tuple for the mouse position

        OUT:
            tuple representing the absolute position of the mouse
        """
        if store.mas_windowreacts.can_do_windowreacts:
            
            try:
                cur_pos = win32gui.GetCursorPos()
            except Exception:
                cur_pos = DEF_MOUSE_POS_RETURN
        
        else:
            cur_pos = DEF_MOUSE_POS_RETURN
        
        return cur_pos

    def _getAbsoluteMousePos_Linux():
        """
        Returns an (x, y) co-ord tuple represening the absolute mouse position
        """
        mouse_data = _m1_zz_windowutils__root.query_pointer()._data
        return (mouse_data["root_x"], mouse_data["root_y"])


    def _getMASWindowPos_Windows():
        """
        Gets the window position for MAS as a tuple of (left, top, right, bottom)

        OUT:
            tuple representing window geometry or None if the window's hWnd could not be found
        """
        hwnd = _m1_zz_windowutils__getMASWindowHWND()
        
        if hwnd is None:
            return None
        
        rv = win32gui.GetWindowRect(hwnd)
        
        
        
        if rv[0] <= -32000 and rv[1] <= -32000:
            return None
        
        return rv

    def _getMASWindowPos_Linux():
        """
        Returns (x1, y1, x2, y2) relative to the top-left of the screen.

        OUT:
            tuple representing (left, top, right, bottom) of the window bounds, or None if not possible to get
        """
        geom = _m1_zz_windowutils__getAbsoluteGeometry(MAS_WINDOW)
        
        if geom is not None:
            return (
                geom[0],
                geom[1],
                geom[0] + geom[2],
                geom[1] + geom[3]
            )
        return None

    def getMousePosRelative():
        """
        Gets the mouse position relative to the MAS window.
        Returned as a set of coordinates (0, 0) being within the MAS window, (1, 0) being to the left, (0, 1) being above, etc.

        OUT:
            Tuple representing the location of the mouse relative to the MAS window in terms of coordinates
        """
        pos_tuple = getMASWindowPos()
        
        if pos_tuple is None:
            return (0, 0)
        
        left, top, right, bottom = pos_tuple
        
        mouse_x, mouse_y = getMousePos()
        
        if mouse_x == 0:
            mouse_x = 1
        if mouse_y == 0:
            mouse_y = 1
        
        half_mas_window_width = (right - left)/2
        half_mas_window_height = (bottom - top)/2
        
        
        
        if half_mas_window_width == 0 or half_mas_window_height == 0:
            return (0, 0)
        
        mid_mas_window_x = left + half_mas_window_width
        mid_mas_window_y = top + half_mas_window_height
        
        mas_window_to_cursor_x_comp = mouse_x - mid_mas_window_x
        mas_window_to_cursor_y_comp = mouse_y - mid_mas_window_y
        
        
        mas_window_to_cursor_x_comp = int(float(mas_window_to_cursor_x_comp)/half_mas_window_width)
        mas_window_to_cursor_y_comp = -int(float(mas_window_to_cursor_y_comp)/half_mas_window_height)
        
        
        return (
            mas_window_to_cursor_x_comp/abs(mas_window_to_cursor_x_comp) if mas_window_to_cursor_x_comp else 0,
            mas_window_to_cursor_y_comp/abs(mas_window_to_cursor_y_comp) if mas_window_to_cursor_y_comp else 0
        )

    def isCursorInMASWindow():
        """
        Checks if the cursor is within the MAS window

        OUT:
            True if cursor is within the mas window (within x/y), False otherwise
            Also returns True if we cannot get window position
        """
        return getMousePosRelative() == (0, 0)

    def isCursorLeftOfMASWindow():
        """
        Checks if the cursor is to the left of the MAS window (must be explicitly to the left of the left window bound)

        OUT:
            True if cursor is to the left of the window, False otherwise
            Also returns False if we cannot get window position
        """
        return getMousePosRelative()[0] == -1

    def isCursorRightOfMASWindow():
        """
        Checks if the cursor is to the right of the MAS window (must be explicitly to the right of the right window bound)

        OUT:
            True if cursor is to the right of the window, False otherwise
            Also returns False if we cannot get window position
        """
        return getMousePosRelative()[0] == 1

    def isCursorAboveMASWindow():
        """
        Checks if the cursor is above the MAS window (must be explicitly above the window bound)

        OUT:
            True if cursor is above the window, False otherwise
            False as well if we're unable to get a window position
        """
        return getMousePosRelative()[1] == 1

    def isCursorBelowMASWindow():
        """
        Checks if the cursor is above the MAS window (must be explicitly above the window bound)

        OUT:
            True if cursor is above the window, False otherwise
            False as well if we're unable to get a window position
        """
        return getMousePosRelative()[1] == -1


    def return_true():
        """
        Literally returns True
        """
        return True

    def return_false():
        """
        Literally returns False
        """
        return False


    if renpy.windows:
        _window_get = _getActiveWindowHandle_Windows
        _tryShowNotif = _tryShowNotification_Windows
        getMASWindowPos = _getMASWindowPos_Windows
        getMousePos = _getAbsoluteMousePos_Windows

    else:
        if renpy.linux:
            _window_get = _getActiveWindowHandle_Linux
            _tryShowNotif = _tryShowNotification_Linux
            getMASWindowPos = _getMASWindowPos_Linux
            getMousePos = _getAbsoluteMousePos_Linux
        
        else:
            _window_get = _getActiveWindowHandle_OSX
            _tryShowNotif = _tryShowNotification_OSX
            
            
            getMASWindowPos = store.dummy
            getMousePos = store.dummy
            
            
            isCursorAboveMASWindow = return_false
            isCursorBelowMASWindow = return_false
            isCursorLeftOfMASWindow = return_false
            isCursorRightOfMASWindow = return_false
            isCursorInMASWindow = return_true

init python:


    mas_win_notif_quips = [
        "[player], quiero hablar contigo de algo.",
        "¿Estás ahí, [player]?",
        "¿Puedes venir aquí un segundo?",
        "[player], ¿tienes un segundo?",
        "¡Tengo algo que decirte, [player]!",
        "¿Tienes un minuto [player]?",
        "¡Tengo algo de que hablar, [player]!",
    ]


    mas_other_notif_quips = [
        "¡Tengo algo de que hablar, [player]!",
        "¡Tengo algo que decirte [player]!",
        "Hey [player], quiero decirte algo.",
        "¿Tienes un minuto [player]?",
    ]


    destroy_list = list()


    def mas_canCheckActiveWindow():
        """
        Checks if we can check the active window (simplifies conditionals)
        """
        return (
            store.mas_windowreacts.can_do_windowreacts
            and (persistent._mas_windowreacts_windowreacts_enabled or persistent._mas_enable_notifications)
        )

    def mas_getActiveWindowHandle():
        """
        Gets the active window name

        OUT:
            The active window handle if found. If it is not possible to get, we return an empty string

        NOTE: THIS SHOULD NEVER RETURN NONE
        """
        if mas_windowreacts.can_show_notifs and mas_canCheckActiveWindow():
            return store.mas_windowutils._window_get()
        return ""

    def mas_display_notif(title, body, group=None, skip_checks=False):
        """
        Notification creation method

        IN:
            title - Notification heading text
            body - A list of items which would go in the notif body (one is picked at random)
            group - Notification group (for checking if we have this enabled)
                (Default: None)
            skip_checks - Whether or not we skips checks
                (Default: False)
        OUT:
            bool indicating status (notif shown or not (by check))

        NOTE:
            We only show notifications if:
                1. We are able to show notifs
                2. MAS isn't the active window
                3. User allows them
                4. And if the notification group is enabled
                OR if we skip checks. BUT this should only be used for introductory or testing purposes.
        """
        
        
        if persistent._mas_windowreacts_notif_filters.get(group) is None and not skip_checks:
            persistent._mas_windowreacts_notif_filters[group] = False
        
        if (
            skip_checks
            or (
                mas_windowreacts.can_show_notifs
                and ((renpy.windows and not mas_isFocused()) or not renpy.windows)
                and mas_notifsEnabledForGroup(group)
            )
        ):
            
            notif_success = mas_windowutils._tryShowNotif(
                renpy.substitute(title),
                renpy.substitute(renpy.random.choice(body))
            )
            
            
            if persistent._mas_notification_sounds and notif_success:
                renpy.sound.play("mod_assets/sounds/effects/notif.wav")
            
            
            return notif_success
        return False


    display_notif = mas_display_notif

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindowHandle() == store.mas_getWindowTitle()

    def mas_isInActiveWindow(regexp, active_window_handle=None):
        """
        Checks if ALL keywords are in the active window name
        IN:
            regexp:
                Regex pattern to identify the window

            active_window_handle:
                String representing the handle of the active window
                If None, it's fetched
                (Default: None)
        """
        
        
        if not store.mas_windowreacts.can_show_notifs:
            return False
        
        
        if active_window_handle is None:
            active_window_handle = mas_getActiveWindowHandle()
        
        return bool(re.findall(regexp, active_window_handle))

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows and store.mas_windowreacts.can_show_notifs:
            for index in range(len(destroy_list)-1,-1,-1):
                store.mas_windowutils.win32gui.DestroyWindow(destroy_list[index])
                destroy_list.pop(index)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        
        if not persistent._mas_windowreacts_windowreacts_enabled or not store.mas_windowreacts.can_show_notifs:
            return
        
        active_window_handle = mas_getActiveWindowHandle()
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if (
                Event._filterEvent(ev, unlocked=True, aff=store.mas_curr_affection)
                and ev.checkConditional()
                and mas_isInActiveWindow(ev.category[0], active_window_handle)
                and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                and mas_notifsEnabledForGroup(ev.rules.get("notif-group"))
            ):
                MASEventList.queue(ev_label)
                ev.unlocked = False
                
                
                if "no_unlock" in ev.rules:
                    mas_addBlacklistReact(ev_label)

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them
        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if ev_label not in excluded:
                ev.unlocked=True

    def mas_updateFilterDict():
        """
        Updates the filter dict with the groups in the groups list for the settings menu
        """
        for group in store.mas_windowreacts._groups_list:
            if persistent._mas_windowreacts_notif_filters.get(group) is None:
                persistent._mas_windowreacts_notif_filters[group] = False

    def mas_addBlacklistReact(ev_label):
        """
        Adds the given ev_label to the no unlock list
        IN:
            ev_label: eventlabel to add to the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label not in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.append(ev_label)

    def mas_removeBlacklistReact(ev_label):
        """
        Removes the given ev_label to the no unlock list if exists
        IN:
            ev_label: eventlabel to remove from the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.remove(ev_label)

    def mas_notifsEnabledForGroup(group):
        """
        Checks if notifications are enabled, and if enabled for the specified group
        IN:
            group: notification group to check
        """
        return persistent._mas_enable_notifications and persistent._mas_windowreacts_notif_filters.get(group,False)

    def mas_unlockFailedWRS(ev_label=None):
        """
        Unlocks a wrs again provided that it showed, but failed to show (failed checks in the notif label)
        NOTE: This should only be used for wrs that are only a notification
        IN:
            ev_label: eventlabel of the wrs
        """
        if (
            ev_label
            and renpy.has_label(ev_label)
            and ev_label not in persistent._mas_windowreacts_no_unlock_list
        ):
            mas_unlockEVL(ev_label,"WRS")

    def mas_prepForReload():
        """
        Handles clearing wrs notifs and unregistering the wndclass to allow 'reload' to work properly

        ASSUMES: renpy.windows
        """
        store.mas_clearNotifs()
        store.mas_windowutils.win32gui.UnregisterClass(_m1_zz_windowutils__tip.classAtom, _m1_zz_windowutils__tip.hinst)
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
