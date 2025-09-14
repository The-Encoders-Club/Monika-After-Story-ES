





default persistent._mas_curr_eli_data = None


default persistent._mas_pool_unlocks = 0



image monika_waiting_img:
    "monika 1eua"
    1.0
    "monika 1euc"
    1.0
    "monika 1esc"
    1.0
    "monika 1lksdlc"
    1.0
    "monika 1ekd"
    1.0
    repeat


transform prompt_monika:
    tcommon(950,z=0.8)


init -999 python in mas_ev_data_ver:



    import __builtin__


    import datetime
    import renpy


    def _strict_can_pickle(val):
        """
        Checks if this value can be pickled safely into persistent.

        This is VERY strict. we only allow types, not isinstance checks.
        no ducks here

        This will check structures recursively and will catch recursion errors.

        IN:
            val - value to check

        RETURNS: tuple of the following format:
            [0] - True if the value can be safely pickled, False if recursion
                error or not picklable.
            [1] - True if recursion error, False otherwise
        """
        try:
            return _m1_event0x2dhandler__strict_can_pickle(val), False
        except RuntimeError as re:
            
            
            
            if "maximum recursion depth exceeded" not in re.args[0]:
                raise
            return False, True


    def _m1_event0x2dhandler__strict_can_pickle(val):
        """
        Recursive strict pickle check. See _strict_can_pickle for more info.

        Will raise recursion error if appropriate.

        IN:
            val - value to check

        RETURNS: True if value can be safely pickled, False otherwise.
        """
        if val is None:
            return True
        
        
        val_type = type(val)
        if val_type in (
                str,
                unicode,
                bool,
                int,
                float,
                long,
                complex,
                datetime.timedelta,
                datetime.date,
        ):
            return True
        
        
        if val_type in (datetime.datetime, datetime.time):
            return val.tzinfo is None
        
        
        if val_type in (
                __builtin__.list,
                renpy.python.RevertableList,
                __builtin__.set,
                __builtin__.frozenset,
                renpy.python.RevertableSet,
                tuple,
        ):
            for sub_val in val:
                if not _m1_event0x2dhandler__strict_can_pickle(sub_val):
                    return False
            return True
        
        
        if val_type in (__builtin__.dict, renpy.python.RevertableDict):
            for sub_key in val:
                if (
                        not _m1_event0x2dhandler__strict_can_pickle(sub_key)
                        or not _m1_event0x2dhandler__strict_can_pickle(val[sub_key])
                ):
                    return False
            return True
        
        
        return False




    def _verify_bool(val, allow_none=True):
        return _verify_item(val, bool, allow_none)


    def _verify_dict(val, allow_none=True):
        return _verify_item(val, __builtin__.dict, allow_none)


    def _verify_list(val, allow_none=True):
        return _verify_item(val, __builtin__.list, allow_none)


    def _verify_dt(val, allow_none=True):
        if (
                isinstance(val, datetime.datetime)
                and val.year < 1900
            ):
            return False
        return _verify_item(val, datetime.datetime, allow_none)


    def _verify_dt_nn(val):
        return _verify_dt(val, False)


    def _verify_evact(val, allow_none=True):
        if val is None:
            return allow_none
        
        return val in store.EV_ACTIONS


    def _verify_int(val, allow_none=True):
        return _verify_item(val, int, allow_none)


    def _verify_int_nn(val):
        return _verify_int(val, False)


    def _verify_str(val, allow_none=True):
        if val is None:
            return allow_none
        
        return isinstance(val, str) or isinstance(val, unicode)


    def _verify_td(val, allow_none=True):
        if val is None:
            return allow_none
        return _verify_item(val, datetime.timedelta, allow_none)


    def _verify_td_nn(val):
        return _verify_td(val, False)


    def _verify_tuli(val, allow_none=True):
        if val is None:
            return allow_none
        
        return isinstance(val, __builtin__.list) or isinstance(val, tuple)


    def _verify_tuli_nn(val):
        return _verify_tuli(val, False)


    def _verify_tuli_aff(val, allow_none=True):
        if val is None:
            return allow_none
        
        return isinstance(val, tuple) and len(val) == 2


    def _verify_item(val, _type, allow_none=True):
        """
        Verifies the given value has the given type/instance

        IN:
            val - value to verify
            _type - type to check
            allow_none - If True, None should be considered good value,
                false means bad value
                (Default: True)

        RETURNS: True if the given value has the given type/instance,
            false otherwise
        """
        if val is None:
            return allow_none
        
        
        return isinstance(val, _type)


    class MASCurriedVerify(object):
        """
        Allows for currying of a verification function
        """
        
        def __init__(self, verifier, allow_none):
            """
            Constructor

            IN:
                verifier - the verification function we want to use
                allow_none - True if we should pass True for allow_none,
                    false for False
            """
            self.verifier = verifier
            self.allow_none = allow_none
        
        
        def __call__(self, value):
            """
            Callable override

            IN:
                value - the value we want to verify

            RETURNS: True if the value passes verification, False otherwise
            """
            return self.verifier(value, self.allow_none)


init -998 python in mas_ev_data_ver:
    import time
    import renpy
    import store

    def _verify_per_mtime():
        """
        verifies persistent data and ensure mod times are not in the future
        """
        curr_time = time.time()
        
        
        if renpy.persistent.persistent_mtime > curr_time:
            renpy.persistent.persistent_mtime = curr_time
        
        
        if renpy.loadsave.location is not None:
            locs = renpy.loadsave.location.locations
            if locs is not None and len(locs) > 0 and locs[0] is not None:
                if locs[0].persistent_mtime > curr_time:
                    locs[0].persistent_mtime = curr_time
        
        
        for varkey in store.persistent._changed:
            if store.persistent._changed[varkey] > curr_time:
                store.persistent._changed[varkey] = curr_time


    try:
        _verify_per_mtime()
        valid_times = True
    except:
        valid_times = False
        store.mas_utils.mas_log.error("[EARLY]: Failed to verify mtimes")

init -950 python in mas_ev_data_ver:
    import store


    _verify_map = {
        0: MASCurriedVerify(_verify_str, False), 
        1: MASCurriedVerify(_verify_str, True), 
        2: MASCurriedVerify(_verify_str, True), 
        

        4: MASCurriedVerify(_verify_bool, True), 
        5: MASCurriedVerify(_verify_bool, True), 
        6: MASCurriedVerify(_verify_bool, True), 
        7: MASCurriedVerify(_verify_str, True), 
        8: MASCurriedVerify(_verify_evact, True), 
        9: MASCurriedVerify(_verify_dt, True), 
        10: MASCurriedVerify(_verify_dt, True), 
        11: MASCurriedVerify(_verify_dt, True), 
        12: MASCurriedVerify(_verify_int, False), 
        
        14: MASCurriedVerify(_verify_dt, True), 
        15: MASCurriedVerify(_verify_tuli, True), 
        16: MASCurriedVerify(_verify_bool, True), 
        17: MASCurriedVerify(_verify_tuli_aff, True), 
        18: MASCurriedVerify(_verify_bool, True), 
    }


    def _verify_data_line(ev_line):
        """
        Verifies event data for a single tuple of data.

        IN:
            ev_line - single line of data to verify

        RETURNS:
            True if passed verification, False if not
        """
        
        for index in range(len(ev_line)):
            
            verify = _verify_map.get(index, None)
            if verify is not None and not verify(ev_line[index]):
                
                return False
        
        return True


    def verify_event_data(per_db):
        """
        Verifies event data of the given persistent data. Entries that are
        invalid are removed. We only check the bits of data that we have, so
        data lines with smaller sizes are only validated for what they have.

        IN:
            per_db - persistent database to verify
        """
        if per_db is None:
            return
        
        for ev_label in per_db.keys():
            
            ev_line = per_db[ev_label]
            
            if not _verify_data_line(ev_line):
                
                store.mas_utils.mas_log.error(
                    "bad data found in {0}".format(ev_label)
                )
                per_db.pop(ev_label)


init -895 python in mas_ev_data_ver:



    for _dm_db in store._mas_dm_dm.per_dbs:
        verify_event_data(_dm_db)

    _dm_db = None









init -500 python:





    mas_init_lockdb_template = (
        True, 
        False, 
        False, 
        False, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        True, 
        False, 
        True, 
        False, 
        False, 
        False, 
        False, 
    )













    if persistent._mas_event_init_lockdb is None:
        persistent._mas_event_init_lockdb = dict()

    for ev_key in persistent._mas_event_init_lockdb:
        stored_lock_row = persistent._mas_event_init_lockdb[ev_key]
        
        if len(mas_init_lockdb_template) != len(stored_lock_row):
            
            lock_row = list(mas_init_lockdb_template)
            lock_row[0:len(stored_lock_row)] = list(stored_lock_row)
            persistent._mas_event_init_lockdb[ev_key] = tuple(lock_row)


    persistent._mas_event_init_lockdb_template = mas_init_lockdb_template






    Event.INIT_LOCKDB = persistent._mas_event_init_lockdb



init 4 python:











    mas_all_ev_db_map = {
        "EVE": store.evhand.event_database,
        "BYE": store.evhand.farewell_database,
        "GRE": store.evhand.greeting_database,
        "MOO": store.mas_moods.mood_db,
        "STY": store.mas_stories.story_database,
        "CMP": store.mas_compliments.compliment_database,
        "FLR": store.mas_filereacts.filereact_db,
        "APL": store.mas_apology.apology_db,
        "WRS": store.mas_windowreacts.windowreact_db,
        "FFF": store.mas_fun_facts.fun_fact_db,
        "SNG": store.mas_songs.song_db,
        "GME": store.mas_games.game_db
    }


init 6 python:




    mas_all_ev_db = {}
    for code,ev_db in mas_all_ev_db_map.iteritems():
        mas_all_ev_db.update(ev_db)

    del code, ev_db


    class MAS_EVL(object):
        """
        Context manager wrapper for Event objects via event labels.
        This has handling for when an eventlabel doesn't return an actual
        event object via mas_getEV.

        Use as follows:
            with MASev('some event label') as ev:
                ev.<property name> = new_value
                curr_value ev.<property_name>

        property names should be same as used on Event object.
        functions can also be used.
        additionally, the resulting context object can be compared with
        other event objects like normal.

        In cases where the Event does not exist, the following occurs:
            - Event properties return their defaults (see below)
            - property set operations do nothing
            - functions calls do nothing
            - The Event class is used as fallback
        """
        _default_values = {
            "eventlabel": "",
            "prompt": None,
            "label": None,
            "category": None,
            "unlocked": False,
            "random": False,
            "pool": False,
            "conditional": None,
            "action": None,
            "start_date": None,
            "end_date": None,
            "unlock_date": None,
            "shown_count": 0,
            "last_seen": None,
            "years": None,
            "sensitive": False,
            "aff_range": None,
            "show_in_idle": False,
            "flags": 0,
        }
        
        _null_dicts = {
            "per_eventdb": 0,
            "rules": 0,
        }
        
        def __init__(self, evl):
            """
            Constructor

            IN:
                evl - event label to build context manager for
            """
            self._ev = mas_getEV(evl)
        
        def __repr__(self):
            return repr(self._ev)
        
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            return False 
        
        def __getattr__(self, name):
            if self._ev is None:
                
                
                if name in MAS_EVL._default_values:
                    return MAS_EVL._default_values.get(name)
                
                
                if name in MAS_EVL._null_dicts:
                    return {}
                
                if callable(Event.__dict__.get(name)):
                    
                    return MASDummyClass()
                
                
                return getattr(Event, name)
            
            return getattr(self._ev, name)
        
        def __setattr__(self, name, value):
            if name == "_ev":
                self.__dict__["_ev"] = value
            
            elif self._ev is None:
                return
            
            elif self._ev is not None:
                setattr(self._ev, name, value)
            
            else:
                super(self, MAS_EVL).__setattr__(name, value)
        
        def __eq__(self, other):
            if self._ev is None:
                return False
            if isinstance(other, Event):
                return self._ev == other
            return False
        
        def __ne__(self, other):
            if self._ev is None:
                return False
            return not self.__eq__(other)


    def mas_getEV(ev_label):
        """
        Global get function that retreives an event given the label

        Designed to be used as a wrapper around the mas_all_ev_db dict
        NOTE: only available at RUNTIME

        IN:
            ev_label - eventlabel to find event for

        RETURNS:
            the event object you were looking for, or None if not found
        """
        return mas_all_ev_db.get(ev_label, None)

    def mas_checkEVL(ev_label, predicate):
        """
        Checks event properties using a lambda

        IN:
            ev_label - ev_label representing the event to check properties for
            predicate - predicate function (accepting an ev as the argument) for the test(s)

        OUT:
            True if predicate function returns True, False otherwise

        NOTE: Does nothing if the ev does not exist
        """
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return False
        
        return predicate(ev)

    def mas_getEVLPropValue(ev_label, prop, default=None):
        """
        Safely gets an ev prop value

        IN:
            ev_label - eventlabel corresponding to the event object to get the property from
            prop - property name to get
            default - default value to return if ev not found/prop not found
                (Default: None)

        OUT:
            Value of the given property name, or default if not found/no ev exists
        """
        ev = mas_getEV(ev_label)
        
        return getattr(ev, prop, default)

    def mas_setEVLPropValues(ev_label, **kwargs):
        """
        Sets ev prop values in bulk if the ev exists

        IN:
            ev_label - ev_label representing the event to set properties for
            kwargs - propname=new_value. Represents the value to set to the property

        OUT:
            True if the property/ies was/were set
            False if not (ev does not exist)
        """
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return False
        
        for attr, new_value in kwargs.iteritems():
            setattr(ev, attr, new_value)
        
        return True

    def mas_isPoolEVL(ev_label):
        """
        Checks if the event for the given event label is pool

        IN:
            ev_label - eventlabel corresponding to the event we wish to check if is pooled

        OUT:
            True if the ev is pooled, False if not, or the ev doesn't exist
        """
        return mas_getEVLPropValue(ev_label, "pool", False)

    def mas_isRandomEVL(ev_label):
        """
        Checks if the event for the given event label is random

        IN:
            ev_label - eventlabel corresponding to the event we wish to check if is random

        OUT:
            True if the ev is random, False if not, or the ev doesn't exist
        """
        return mas_getEVLPropValue(ev_label, "random", False)

    def mas_isUnlockedEVL(ev_label):
        """
        Checks if the event for the given event label is unlocked

        IN:
            ev_label - eventlabel corresponding to the event we wish to check if is unlocked

        OUT:
            True if the ev is unlocked, False if not, or the ev doesn't exist
        """
        return mas_getEVLPropValue(ev_label, "unlocked", False)

    def mas_getEVL_last_seen(ev_label, default=None):
        """
        Gets the last_seen from the event corresponding to the given eventlabel

        If the event doesn't exist, the default is returned

        IN:
            ev_label - eventlabel for the event we wish to get last_seen from
            default - value to return if the event object doesn't exist

        OUT:
            The last_seen of the ev, or the default if the event doesn't exist
        """
        return mas_getEVLPropValue(ev_label, "last_seen", default)

    def mas_getEVL_shown_count(ev_label, default=0):
        """
        Gets the shown_count from the event corresponding to the given eventlabel

        If the event doesn't exist, the default is returned

        IN:
            ev_label - eventlabel for the event we wish to get shown_count from
            default - value to return if the event object doesn't exist

        OUT:
            The shown_count of the ev, or the default if the event doesn't exist
        """
        return mas_getEVLPropValue(ev_label, "shown_count", default)

    def mas_inRulesEVL(ev_label, *args):
        """
        Checks if keys are in the event's rules dict

        IN:
            ev_label - eventlabel for the event we wish to check rule keys for
            *args - rule keys

        OUT:
            True if all rule keys provided are in an event object's rules dict
            False if the event doesn't exist or any provided keys aren't present in the rules dict
        """
        ev_rules = mas_getEVLPropValue(ev_label, "rules", dict())
        
        if not ev_rules:
            return False
        
        for rule_key in args:
            if rule_key not in ev_rules:
                return False
        return True

    def mas_assignModifyEVLPropValue(ev_label, propname, operation, value):
        """
        Does an assign-modify operation

        IN:
            ev_label - eventlabel representing the event that will have a property assign/modified
            propname - property name to do the assign-modify operation on
            operation - operator to assign/modify with. (Any of the following: +=, -=, *=, /= (as a string))
            value - value to use in the operation

        OUT:
            True if event values were assign/modified successfully
            False otherwise
        """
        ev = mas_getEV(ev_label)
        if not ev:
            return False
        
        else:
            try:
                exec("ev.{0} {1} {2}".format(propname, operation, value))
            except:
                return False
        return True

    def mas_getEVCL(ev_label):
        """
        Global get function that retrieves the calendar label for an event
        given the eventlabel. This is mainly to help with calendar.

        IN:
            ev_label - eventlabel to find calendar label for

        RETURNS:
            the calendar label you were looking for, or "Unknown Event" if
            not found.
        """
        ev = mas_getEV(ev_label)
        if ev is None:
            return "Unknown Event"
        else:
            return ev.label


    def mas_hideEVL(
            ev_label,
            code,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Hides an event given label and code.

        IN:
            ev_label - label of event to hide
            code - string code of the db this ev_label belongs to
            lock - True if we want to lock this event
                (Default: False)
            derandom - True if we want to de random this event
                (Default: False)
            depool - True if we want to de pool this event
                (Default: False)
            decond - True if we want to remove conditoinal for this event
                (Default: False)
        """
        store.evhand._hideEvent(
            mas_all_ev_db_map.get(code, {}).get(ev_label, None),
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def mas_showEVL(
            ev_label,
            code,
            unlock=False,
            _random=False,
            _pool=False,
        ):
        """
        Shows an event given label and code.

        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
            unlock - True if we want to unlock this Event
                (Default: False)
            _random - True if we want to random this event
                (Default: False)
            _pool - True if we want to random thsi event
                (Default: False)

        NOTE:
            if using this to random, it does not protect labels that are in persistent._mas_player_derandomed
            and thus will remove the label from that list if present.

            if the label should not be randomed if it's in persistent._mas_player_derandomed
            use mas_protectedShowEVL
        """
        
        if _random:
            store.mas_bookmarks_derand.removeDerand(ev_label)
        
        store.mas_showEvent(
            mas_all_ev_db_map.get(code, {}).get(ev_label, None),
            unlock=unlock,
            _random=_random,
            _pool=_pool
        )

    def mas_protectedShowEVL(
            ev_label,
            code,
            unlock=False,
            _random=False,
            _pool=False,
        ):
        """
        Shows an event given label and code.

        Does checking if the actions should happen
        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
            unlock - True if we want to unlock this Event
                (Default: False)
            _random - True if we want to random this event
                (Default: False)
            _pool - True if we want to random thsi event
                (Default: False)
        """
        mas_showEVL(
            ev_label=ev_label,
            code=code,
            unlock=unlock,
            _random=_random and store.mas_bookmarks_derand.shouldRandom(ev_label),
            _pool=_pool
        )

    def mas_lockEVL(ev_label, code):
        """
        Locks an event given label and code.

        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
        """
        mas_hideEVL(ev_label, code, lock=True)


    def mas_unlockEVL(ev_label, code):
        """
        Unlocks an event given label and code.

        IN:
            ev_label - label of event to show
            code - string code of the db this ev_label belongs to
        """
        mas_showEVL(ev_label, code, unlock=True)


    def mas_stripEVL(ev_label, list_pop=False, remove_dates=True):
        """
        Strips the conditional and action properties from an event given its label
        start_date and end_date will be removed if remove_dates is True
        Also removes the event from the event list if present (optional)

        IN:
            ev_label - label of event to strip
            list_pop - True if we want to remove the event from the event list
                (Default: False)
            remove_dates - True if we want to remove start/end_dates from the event
                (Default: True)
        """
        if remove_dates:
            mas_setEVLPropValues(
                ev_label,
                conditional=None,
                action=None,
                start_date=None,
                end_date=None
            )
        
        else:
            mas_setEVLPropValues(
                ev_label,
                conditional=None,
                action=None
            )
        
        if list_pop:
            mas_rmEVL(ev_label)


    def mas_flagEVL(ev_label, code, flags):
        """
        Applies flags to the given event

        IN:
            ev_label - label of the event to flag
            code - string code of the db this ev_label belongs to
            flags - flags to apply
        """
        ev = mas_all_ev_db_map.get(code, {}).get(ev_label, None)
        if ev is not None:
            ev.flag(flags)


    def mas_unflagEVL(ev_label, code, flags):
        """
        Unflags flags from the given event

        IN:
            ev_label - label of the event to unflag
            code - string code of the db this ev_label belongs to
            flags - flags to unset
        """
        ev = mas_all_ev_db_map.get(code, {}).get(ev_label, None)
        if ev is not None:
            ev.unflag(flags)


init 4 python:
    def mas_lastSeenInYear(ev_label, year=None):
        """
        Checks whether or not the even was last seen in the year provided

        IN:
            ev_label - label of the event we want to check
            year - the year we want to check if it's been last seen in

        OUT:
            boolean - True if last seen this year, False otherwise

        NOTE: if no year provided, we assume this year
        """
        
        try:
            
            ev = mas_getEV(ev_label)
        except:
            ev = None
        
        
        if not ev or not ev.last_seen:
            return False
        
        
        if year is None:
            year = datetime.date.today().year
        
        
        return ev.last_seen.year == year

    def mas_lastSeenLastYear(ev_label):
        """
        Checks if the event corresponding to ev_label was last seen last year
        """
        return mas_lastSeenInYear(ev_label, datetime.date.today().year-1)


    store.evhand.cleanYearsetBlacklist()


python early:







    MAS_FC_INIT = 1


    MAS_FC_START = 2


    MAS_FC_END = 4


    MAS_FC_IDLE_ROUTINE = 8



    MAS_FC_IDLE_ONCE = 16


    MAS_FC_IDLE_HOUR = 32


    MAS_FC_IDLE_DAY = 64

    MAS_FC_CONSTANTS = [
        MAS_FC_INIT,
        MAS_FC_START,
        MAS_FC_END,
        MAS_FC_IDLE_ROUTINE,
        MAS_FC_IDLE_ONCE,
        MAS_FC_IDLE_HOUR,
        MAS_FC_IDLE_DAY,
    ]


init -880 python:





    if persistent._mas_delayed_action_list is None:
        
        
        
        persistent._mas_delayed_action_list = list()




    mas_delayed_action_map = dict()

    class MASDelayedAction(object):
        """
        A Delayed action consists of the following:

        All exceptions are logged

        id - the unique ID of this DelayedAction
        ev - the event this action is associated with
        conditional - the logical conditional we want to check before performing
            action
            NOTE: this is not checked for correctness
            If cond_is_callable is True, then this is called instead of eval'd.
            In that case, the event object in question is passed into the
            callable.
        action - EV_ACTION constant this delayed action will perform
            NOTE: this is not checked for existence
            NOTE: this can also be a callable
                the event would be passd in as ev
                if callable, make this return True upon success and false
                    othrewise
        flowcheck - FC constant saying when this delayed action should be
            checked
            NOTE: this is not checked for existence
        been_checked - True if this action has been checked this game session
        executed - True if this delayed action has been executed
            - Delayed actions that have been executed CANNOT be executed again
        cond_is_callable - True if the conditional is a callable instead of
            a eval check.
            NOTE: we do not check callable for correctness
        """
        ERR_COND = "delayed action has bad conditional '{0}' | {1}"
        
        
        def __init__(self,
                _id,
                ev,
                conditional,
                action,
                flowcheck,
                cond_is_callable=False
            ):
            """
            Constructor

            NOTE: MAY raise exceptions
            NOTE: also logs exceptions.

            IN:
                _id - id of this delayedAction
                ev - event this action is related to
                conditional - conditional to check to do this action
                    NOTE: if this is a callable, then event is passed in
                action - EV_ACTION constant for this delayed action
                    NOTE: this can also be a callable
                        ev would be passed in as ev
                    If callable, make this return True on success, False
                        otherwise
                flowcheck - FC constant saying when this delaeyd action should
                    be checked
                cond_is_callable - True if the conditional is actually a
                    callable.
                    If this True and None is passed into the conditional, then
                    we just return False (aka never run the delayedaction)
                    (Default: False)
            """
            if not cond_is_callable:
                try:
                    eval(conditional)
                except Exception as e:
                    store.mas_utils.mas_log.error(self.ERR_COND.format(
                        conditional,
                        str(e)
                    ))
                    raise e
            
            self.cond_is_callable = cond_is_callable
            self.conditional = conditional
            self.action = action
            self.flowcheck = flowcheck
            self.been_checked = False
            self.executed = False
            self.ev = ev
            self.id = _id
        
        
        def __call__(self):
            """
            Checks if the conditional passes then performs the action

            NOTE: logs exceptions

            RETURNS:
                True on successful action performed, False otherwise
            """
            
            if self.ev is None or self.executed or self.action is None:
                return False
            
            
            try:
                
                
                if self.cond_is_callable:
                    
                    if self.conditional is None:
                        
                        return False
                    
                    condition_passed = self.conditional(ev=self.ev)
                
                else:
                    condition_passed = eval(self.conditional)
                
                
                if condition_passed:
                    if self.action in Event.ACTION_MAP:
                        Event.ACTION_MAP[self.action](
                            self.ev, unlock_time=datetime.datetime.now()
                        )
                        self.executed = True
                    
                    else:
                        
                        self.executed = self.action(ev=self.ev)
            
            except Exception as e:
                store.mas_utils.mas_log.error(self.ERR_COND.format(
                    self.conditional,
                    str(e)
                ))
            
            
            return self.executed
        
        
        @staticmethod
        def makeWithLabel(
                _id,
                ev_label,
                conditional,
                action,
                flowcheck,
                cond_is_callable=False
            ):
            """
            Makes a MASDelayedAction using an eventlabel instead of an event

            IN:
                _id - id of this delayedAction
                ev_label - label of the event this action is related to
                conditional - conditional to check to do to tihs action
                action - EV_ACTION constant for this delayed action
                    NOTE: this can also be a cllable
                        ev would be passed in as ev
                    If callable, make this return True on success, False
                        otherwise
                flowcheck - FC constant saying when this delayed action should
                    be checked
                cond_is_callable - True if the conditional is actually a
                    callable.
                    If this True and None is passed into the conditional, then
                    we just return False (aka never run the delayedaction)
                    (Default: False)
            """
            return MASDelayedAction(
                _id,
                mas_getEV(ev_label),
                conditional,
                action,
                flowcheck,
                cond_is_callable
            )



    def mas_removeDelayedAction(_id):
        """
        Removes a delayed action with the given ID

        NOTE: this removes from both persistent and the runtime lists

        IN:
            _id - id of the delayed action to remove
        """
        if _id in persistent._mas_delayed_action_list:
            persistent._mas_delayed_action_list.remove(_id)
        
        if _id in mas_delayed_action_map:
            mas_delayed_action_map.pop(_id)


    def mas_removeDelayedActions_list(_ids):
        """
        Removes a list of delayed actions with given Ids

        IN:
            _ids - list of Ids to remove
        """
        for _id in _ids:
            mas_removeDelayedAction(_id)


    def mas_removeDelayedActions(*args):
        """
        Multiple argument delayed action removal

        Assumes all given args are IDS
        """
        mas_removeDelayedActions_list(args)


    def mas_runDelayedActions(flow):
        """
        Attempts to run currently held delayed actions for the given flow mode

        Delayed actions that are successfully completed are removed from the
        list

        IN:
            flow - FC constant for the current flow
        """
        if flow not in MAS_FC_CONSTANTS:
            return
        
        
        for action_id in list(mas_delayed_action_map):
            action = mas_delayed_action_map[action_id]
            
            
            if (action.flowcheck & flow) > 0:
                if action():
                    
                    mas_removeDelayedAction(action_id)
                
                
                action.been_checked = True


    def mas_addDelayedAction(_id):
        """
        Creates a delayed action with the given ID and adds it to the delayed
        action map (runtime)

        NOTE: this handles duplicates, so its better to use this

        NOTE: this also adds to persistent, just in case

        IN:
            _id - id of the delayed action to create
        """
        if _id in mas_delayed_action_map:
            return
        
        
        make_action = store.mas_delact.MAP.get(_id, None)
        if make_action is None:
            return
        
        
        mas_delayed_action_map[_id] = make_action()
        
        
        if _id not in persistent._mas_delayed_action_list:
            persistent._mas_delayed_action_list.append(_id)


    def mas_addDelayedActions_list(_ids):
        """
        Creates delayed actions given a list of Ids

        IN:
            _ids - list of IDS to add
        """
        for _id in _ids:
            mas_addDelayedAction(_id)


    def mas_addDelayedActions(*args):
        """
        Creates delayed actions given ids as args

        assumes each arg is a valid id
        """
        mas_addDelayedActions_list(args)


init 995 python:

    mas_runDelayedActions(MAS_FC_INIT)

init -880 python in mas_delact:

    import store

    def _MDA_safeadd(*ids):
        """
        Adds MASDelayedAction ids to the persistent mas delayed action list.

        NOTE: this is only meant for code that runs super early yet needs to
        add MASDelayedActions.

        NOTE: This will NOT add duplicates.

        IN:
            ids - ids to add to the delayed action list
        """
        for _id in ids:
            if _id not in store.persistent._mas_delayed_action_list:
                store.persistent._mas_delayed_action_list.append(_id)


    def _MDA_saferm(*ids):
        """
        Removes MASDelayedActions from the persistent mas delayed action list.

        NOTE: this is only meant for code that runs super early yet needs to
        remove MASDelayedActions

        NOTE: this will check for existence before removing

        IN:
            ids - ids to remove from the delayed action list
        """
        for _id in ids:
            if _id in store.persistent._mas_delayed_action_list:
                store.persistent._mas_delayed_action_list.remove(_id)


init -875 python in mas_delact:

    import datetime 






    MAP = {
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        16: _mas_birthdate_bad_year_fix,
    }


init 994 python in mas_delact:


    def loadDelayedActionMap():
        """
        Checks the persistent delayed action list and generates the
        runtime map of delayed actions
        """
        store.mas_addDelayedActions_list(
            store.persistent._mas_delayed_action_list
        )


    def saveDelayedActionMap():
        """
        Checks the runtime map of delayed actions and saves them into the
        persistent value.

        NOTE: this does not ADD to the persistent's list. This recreates it
            entirely.
        """
        store.persistent._mas_delayed_action_list = [
            action_id for action_id in store.mas_delayed_action_map
        ]



    loadDelayedActionMap()


default persistent._mas_ev_yearset_blacklist = {}



init -1 python in evhand:
    import store
    import re


    event_database = dict()
    farewell_database = dict()
    greeting_database = dict()


    from collections import namedtuple




    _NT_CAT_PANE = namedtuple("_NT_CAT_PANE", "menu cats")



    RIGHT_X = 1020

    RIGHT_Y = 15 + 55

    RIGHT_W = 250
    RIGHT_H = 572

    RIGHT_XALIGN = -0.10
    RIGHT_AREA = (RIGHT_X, RIGHT_Y, RIGHT_W, RIGHT_H)



    LEFT_X = 740

    LEFT_Y = RIGHT_Y

    LEFT_W = RIGHT_W
    LEFT_H = RIGHT_H

    LEFT_XALIGN = -0.10
    LEFT_AREA = (LEFT_X, LEFT_Y, LEFT_W, LEFT_H)
    LEFT_EXTRA_SPACE = 68


    import datetime
    LAST_SEEN_DELTA = datetime.timedelta(hours=6)


    RESTART_BLKLST = []


    IDLE_WHITELIST = [
        "unlock_prompt",
    ]



    RET_KEY_PATTERN_BASE = (
        r"(?:(?<=\|)|(?<=^))\s*"
        r"{key}"
        r"\s*:\s*"
        r"{value}"
        r"\s*(?:(?=\|)|(?=$))"
    )

    RET_KEY_PATTERN_IDLE_EXP = re.compile(
        RET_KEY_PATTERN_BASE.format(
            key=r"idle_exp",
            value=r"(?:(?P<exp>\d[a-z]{3,13})\s*,\s*(?P<duration>\d+)|(?P<tag>\w+))"
        )
    )

    RET_KEY_PATTERN_PAUSE = re.compile(
        RET_KEY_PATTERN_BASE.format(
            key=r"pause",
            value=r"(?P<duration>\d+)"
        )
    )


    class EventListItem(object):
        """
        Representation of an EventListItem (ELI)
        """
        
        
        DEFAULT_VALUES = (
            False, 
            None, 
        )
        
        ITEM_LEN = len(DEFAULT_VALUES) + 1 
        
        IDX_EVENT_LABEL = 0
        IDX_NOTIFY = 1
        IDX_CONTEXT = 2
        
        def __init__(self, data):
            """
            Constructor

            IN:
                data - the data directly from event list
            """
            self._eli = data
        
        def __repr__(self):
            return "<{}: (data: {})>".format(
                type(self).__name__,
                self._eli
            )
        
        @staticmethod
        def build(evl, *args):
            """
            Builds an ELI.

            IN:
                evl - event label
                *args - the other args for an EventListItem.

            RETURNS: EventListItem object
            """
            return EventListItem(EventListItem._build_raw(evl, *args))
        
        @staticmethod
        def _build_raw(evl, *args):
            """
            Builds raw data for an ELI.

            args are same as EventListItem.build

            RETURNS: raw data
            """
            data = list(
                (evl, ) + args + EventListItem.DEFAULT_VALUES[len(args):]
            )
            
            
            ctx = data[EventListItem.IDX_CONTEXT]
            if isinstance(ctx, store.MASEventContext):
                data[EventListItem.IDX_CONTEXT] = ctx._to_dict()
            
            return tuple(data)
        
        def _raw(self):
            """
            Gets the data for this EventListItem that is ready for
            the actual event list.

            RETURNS: raw event list data
            """
            return self._eli
        
        @property
        def event_label(self):
            """
            Gets the event label from this EventListItem

            Aliases: ev_label, evl

            RETURNS: event label
            """
            return self._eli[self.IDX_EVENT_LABEL]
        
        
        eventlabel = event_label 
        ev_label = event_label
        evl = event_label
        
        @property
        def notify(self):
            """
            Gets the notify value from this EventListItem

            RETURNS: notify
            """
            return self._eli[self.IDX_NOTIFY]
        
        @property
        def context(self):
            """
            Gets the context from this EventListItem

            Aliases: ctx

            RETURNS: context (MASEventContext object)
            """
            return store.MASEventContext(self._eli[self.IDX_CONTEXT])
        
        
        ctx = context



    def addIfNew(items, pool):
        
        
        
        
        
        
        
        
        
        
        
        for item in items:
            if item not in pool:
                pool.append(item)
        return pool

    def tuplizeEventLabelList(key_list, db):
        
        
        
        
        
        
        
        
        
        
        
        
        return [(db[x].prompt, x) for x in key_list]


    def _isFuture(ev, date=None):
        """INTERNAL
        Checks if the start_date of the given event happens after the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's start_date is in the future, False otherwise
        """
        
        
        if ev is None:
            return False
        
        
        if date is None:
            date = datetime.datetime.now()
        
        start_date = ev.start_date
        
        
        if start_date is None:
            return False
        
        return date < start_date


    def _isPast(ev, date=None):
        """INTERNAL
        Checks if the end_date of the given event happens before the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's end_date is in the past, False otherwise
        """
        
        
        if ev is None:
            return False
        
        
        if date is None:
            date = datetime.datetime.now()
        
        end_date = ev.end_date
        
        
        if end_date is None:
            return False
        
        return end_date < date


    def _isPresent(ev):
        """INTERNAL
        Checks if current date falls within the given event's start/end date
        range

        IN:
            ev - Event to check the start_time and end_time

        RETURNS:
            True if current time is inside the  Event's start_date/end_date
            interval, False otherwise
        """
        
        if ev is None:
            return False
        
        start_date = ev.start_date
        end_date = ev.end_date
        
        current = datetime.datetime.now()
        
        
        if start_date is None or end_date is None:
            return False
        
        return start_date <= current <= end_date


    def _hideEvent(
            event,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Internalized hideEvent
        """
        if event:
            
            if lock:
                event.unlocked = False
            
            if derandom:
                event.random = False
            
            if depool:
                event.pool = False
            
            if decond:
                event.conditional = None


    def _hideEventLabel(
            eventlabel,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=event_database
        ):
        """
        Internalized hideEventLabel
        """
        ev = eventdb.get(eventlabel, None)
        
        _hideEvent(
            ev,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def _lockEvent(ev):
        """
        Internalized lockEvent
        """
        _hideEvent(ev, lock=True)


    def _lockEventLabel(evlabel, eventdb=event_database):
        """
        Internalized lockEventLabel
        """
        _hideEventLabel(evlabel, lock=True, eventdb=eventdb)


    def _unlockEvent(ev):
        """
        Internalized unlockEvent
        """
        if ev:
            ev.unlocked = True


    def _unlockEventLabel(evlabel, eventdb=event_database):
        """
        Internalized unlockEventLabel
        """
        _unlockEvent(eventdb.get(evlabel, None))


    def addYearsetBlacklist(evl, expire_dt):
        """
        Adds the given evl to the yearset blacklist, with the given expiration
        dt

        IN:
            evl - event label
            expire_dt - when the evl should be removed from the blacklist
        """
        if expire_dt > datetime.datetime.now():
            store.persistent._mas_ev_yearset_blacklist[evl] = expire_dt


    def cleanYearsetBlacklist():
        """
        Goes through the year setblacklist and removes expired entries
        """
        now_dt = datetime.datetime.now()
        for evl in store.persistent._mas_ev_yearset_blacklist.keys():
            if store.persistent._mas_ev_yearset_blacklist[evl] <= now_dt:
                store.persistent._mas_ev_yearset_blacklist.pop(evl)


    def isYearsetBlacklisted(evl):
        """
        Checks if the given evl is yearset blacklisted. Also checks expiration
        date and removes if needed.

        IN:
            evl - event label

        RETURNS: True if blacklisted, false if not
        """
        if evl not in store.persistent._mas_ev_yearset_blacklist:
            return False
        
        expire_dt = store.persistent._mas_ev_yearset_blacklist[evl]
        if expire_dt <= datetime.datetime.now():
            store.persistent._mas_ev_yearset_blacklist.pop(evl)
            return False
        
        return True


init python:
    import store.evhand as evhand
    import datetime


    class MASEventContext(mas_utils.IsolatedFlexProp):
        """
        Context for events. Supports flexible attributes (like persistent).

        However, only picklable primitive datatypes are allowed.
        See mas_ev_data_ver._strict_can_pickle for more info.
        In general, DO NOT USE OBJECTS - they will be denied entry.

        To get the current event context, call MASEventContext.get.
        """
        _this_ev_ctx = None 
        
        
        _m1_event0x2dhandler__CTX_CTX = "current event: {0}"
        _m1_event0x2dhandler__ERR_NON_PICKLE = (
            "object of type '{0}' cannot be added to context | {1}"
        )
        _m1_event0x2dhandler__ERR_RECUR = (
            "recursion error hit while adding object of type '{0}' to context "
            "| {1}"
        )
        
        def __init__(self, ctx_data=None):
            """
            Constructor

            IN:
                ctx_data - context data directly from event list. Optional.
                    (Default: None)
            """
            super(MASEventContext, self).__init__()
            if ctx_data is not None:
                self._from_dict(ctx_data)
        
        def __setattr__(self, name, value):
            """
            We don't allow types that cannot be saved to persistent
            """
            if MASEventContext.is_allowed_data(value):
                super(MASEventContext, self).__setattr__(name, value)
        
        @classmethod
        def is_allowed_data(cls, thing):
            """
            Checks if the given thing is allowed to be used in context.

            IN:
                thing - thing to check

            RETURNS: True if the thing can be used, False otherwise
            """
            can_pickle, recur_error = store.mas_ev_data_ver._strict_can_pickle(thing)
            if can_pickle:
                return True
            
            
            
            if store.mas_globals.this_ev is None:
                context = ""
            else:
                context = cls._m1_event0x2dhandler__CTX_CTX.format(
                    store.mas_globals.this_ev.eventlabel
                )
            
            if recur_error:
                
                store.mas_utils.mas_log.error(cls._m1_event0x2dhandler__ERR_RECUR.format(
                    type(thing).__name__,
                    context
                ))
            
            else:
                
                store.mas_utils.mas_log.error(cls._m1_event0x2dhandler__ERR_NON_PICKLE.format(
                    type(thing).__name__,
                    context
                ))
        
        @classmethod
        def get(cls):
            """
            Gets current event context.
            """
            if cls._this_ev_ctx is None:
                cls._this_ev_ctx = cls()
            
            return cls._this_ev_ctx
        
        @classmethod
        def _set(cls, eli):
            """
            Sets current event context - only for internal use.

            IN:
                eli - EventListItem object. Use None to clear.
            """
            if eli is None:
                cls._this_ev_ctx = None
            else:
                cls._this_ev_ctx = eli.ctx


    class MASEventList(object):
        """
        representation of persistent.event_list*

        *not literally, this should be considered an abstraction layer with
        unified naming.
        """
        
        
        
        @staticmethod
        def clear_current():
            """
            Clears the current event aka persistent eli data.
            """
            MASEventList._set_current(None)
        
        @staticmethod
        def load_current():
            """
            Loads the current event as an EventListItem, which is stored in
            persistent eli data.

            RETURNS: EventListItem of the current event, or None if no current
                event.
            """
            if persistent._mas_curr_eli_data is None:
                return None
            
            return evhand.EventListItem.build(*persistent._mas_curr_eli_data)
        
        @staticmethod
        def _set_current(eli):
            """
            Sets the current event aka persistent eli data using the given
            EventListItem object.

            Also sets persistent.current_monikatopic.

            IN:
                eli - the EventListItem object to set as the current one.
                    pass None to clear the current event data.
            """
            if eli is None:
                new_eli_data = None
                new_curr_moni_topic = None
            else:
                new_eli_data = eli._raw()
                new_curr_moni_topic = eli.evl
            
            persistent._mas_curr_eli_data = new_eli_data
            persistent.current_monikatopic = new_curr_moni_topic
        
        @staticmethod
        def sync_current():
            """
            Syncs the current event persistent vars, aka:
                - current_monikatopic
                - _mas_curr_eli_data
            """
            curr_eli = MASEventList.load_current()
            
            if curr_eli is None:
                
                if renpy.has_label(str(persistent.current_monikatopic)):
                    
                    
                    MASEventList._set_current(evhand.EventListItem.build(
                        str(persistent.current_monikatopic)
                    ))
                
                else:
                    MASEventList.clear_current()
            
            else:
                MASEventList._set_current(curr_eli)
        
        
        
        @staticmethod
        def clean():
            """
            Cleans the event list and makes sure all events are of the
            appropriate length and have a valid label.
            """
            for index in MASEventList.rev_idx_iter():
                item_raw = persistent.event_list[index]
                
                
                if not isinstance(item_raw, tuple):
                    
                    new_item = evhand.EventListItem.build(item_raw)
                
                elif len(item_raw) < evhand.EventListItem.ITEM_LEN:
                    
                    new_item = evhand.EventListItem.build(*item_raw)
                
                else:
                    
                    new_item = evhand.EventListItem(item_raw)
                
                
                if renpy.has_label(new_item.evl):
                    persistent.event_list[index] = new_item._raw()
                
                else:
                    persistent.event_list.pop(index)
        
        @staticmethod
        def iter():
            """
            an iterable over event list that yields EventListITem objects

            ASSUMES event list data is valid

            RETURNS: generator/iterable over persistent.event_list
            """
            for data in persistent.event_list:
                yield evhand.EventListItem(data)
        
        @staticmethod
        def is_paused():
            """
            Checks if events are paused - also updates the event pause dt vars.

            RETURNS: True if events are paused, False otherwise.
            """
            if mas_globals.event_unpause_dt is None:
                return False
            
            if datetime.datetime.utcnow() < mas_globals.event_unpause_dt:
                return True
            
            mas_globals.event_unpause_dt = None
            return False
        
        @staticmethod
        def _next():
            """
            Gets the next event's data and its location in the event_list.
            This takes event restrictions into account, aka pausing and idle.

            RETURNS: tuple of the following format:
                [0] - EventListItem of the next event, or None if no next event
                [1] - the index of the event, or -1 if no next event
            """
            if len(persistent.event_list) < 1:
                return None, -1
            
            is_paused = MASEventList.is_paused()
            
            for index, item in MASEventList.rev_enum_iter():
                ev = mas_getEV(item.evl)
                
                if (
                        not is_paused
                        or ev is None 
                        or "skip_pause" in ev.rules
                ):
                    
                    if mas_globals.in_idle_mode:
                        
                        
                        if (
                                (ev is not None and ev.show_in_idle)
                                or item.evl in evhand.IDLE_WHITELIST
                        ):
                            return item, index
                    
                    else:
                        return item, index
            
            
            return None, -1
        
        @staticmethod
        def peek():
            """
            Gets the EventListItem for the next event on the event list, but
            does NOT remove it.

            This will respect pausing and other next event restrictions.

            Does NOT set additional vars that pop does - please use pop
            when actually planning to execute an event.

            RETURNS: EventListItem object for the next event, or None if no
            next event.
            """
            return MASEventList._next()[0]
        
        @staticmethod
        def pop():
            """
            Gets the EventListItem for the next event on the event list and
            removes the event from the event list.

            This will respect pausing and other next event restrictions.

            Also sets:
                persistent.current_monikatopic
                persistent._mas_eli_data

            RETURNS: EventListItem object for the next event
            """
            item, loc = MASEventList._next()
            
            if item is None:
                return None
            
            if 0 <= loc < len(persistent.event_list): 
                persistent.event_list.pop(loc)
            
            MASEventList._set_current(item)
            
            return item
        
        @staticmethod
        def push(event_label, skipeval=False, notify=False, context=None):
            """
            Pushes an event to the list - this will make the event trigger
            next unless something else is pushed.

            IN:
                @event_label - a renpy label for the event to be called
                skipmidloopeval - do we want to skip the mid loop eval to
                    prevent other rogue events from interrupting.
                    (Defaults: False)
                notify - True will trigger a notification if appropriate. False
                    will not
                    (Default: False)
                context - set to a MASEventContext object to supply extra
                    context to the event
                    (accessible via MASEventContext.get())
                    (Default: None)
            """
            MASEventList._push_eli(evhand.EventListItem.build(
                event_label,
                notify,
                context
            ))
            
            if skipeval:
                mas_idle_mailbox.send_skipmidloopeval()
        
        @staticmethod
        def _push_eli(eli):
            """
            Pushes an EventListItem directly. only for internal use.

            IN:
                eli - EventListItem to push
            """
            persistent.event_list.append(eli._raw())
        
        @staticmethod
        def queue(event_label, notify=False, context=None):
            """
            Queues an event to the list - this will make the event trigger,
            but not right away unless the list is empty.

            IN:
                @event_label - a renpy label for the event to be called
                notify - True will trigger a notification if appropriate, False
                    will not
                    (Default: False)
                context - set to a MASEventContext object to supply extra
                    context to the event
                    (accessible via MASEventContext.get())
                    (Default: None)
            """
            MASEventList._queue_eli(evhand.EventListItem.build(
                event_label,
                notify,
                context
            ))
        
        @staticmethod
        def _queue_eli(eli):
            """
            Queues an EventListItem directly, only for internal use.

            IN:
                eli - EventListItem to queue
            """
            persistent.event_list.insert(0, eli._raw())
        
        @classmethod
        def rev_enum_iter(cls):
            """
            Reverse enumerated iterable for event list.

            ASSUMES persistent.event_list is valid

            RETURNS: reverse enumerated iterable:
                [0] - index
                [1] - EventListItem
            """
            for index in cls.rev_idx_iter():
                yield (index, evhand.EventListItem(persistent.event_list[index]))
        
        @staticmethod
        def rev_idx_iter():
            """
            Reverse index iterable. If you want index iterable, please use
            enumerate with iter.

            RETURNS: reverse index iterable for event list
            """
            return range(len(persistent.event_list)-1, -1, -1)


    def addEvent(
        event,
        eventdb=None,
        skipCalendar=True,
        restartBlacklist=False,
        markSeen=False,
        code="EVE"
    ):
        """
        Adds an event object to the given eventdb dict
        Properly checksfor label and conditional statements
        This function ensures that a bad item is not added to the database

        NOTE: this MUST be ran after init level 4.

        IN:
            event - the Event object to add to database
            eventdb - The Event databse (dict) we want to add to
                NOTE: DEPRECATED. Use code instead.
                NOTE: this can still be used for custom adds.
                (Default: None)
            skipCalendar - flag that marks wheter or not calendar check should
                be skipped
                (Default: True)

            restartBlacklist - True if this topic should be added to the restart blacklist
                (Default: False)

            markSeen - True if this topic should be `True` in persistent._seen_ever.
                (Default: False)

            code - code of the event database to add to.
                (Default: EVE) - event database
        """
        if eventdb is None:
            eventdb = mas_all_ev_db_map.get(code, None)
        
        if type(eventdb) is not dict:
            raise EventException("Given db is not of type dict")
        if type(event) is not Event:
            raise EventException("'" + str(event) + "' is not an Event object")
        if not renpy.has_label(event.eventlabel):
            raise EventException("'" + event.eventlabel + "' does NOT exist")
        
        
        
        
        
        
        
        
        if not skipCalendar and type(event.start_date) is datetime.datetime:
            
            store.mas_calendar.addEvent(event)
        
        
        
        if not store.evhand.isYearsetBlacklisted(event.eventlabel):
            Event._verifyAndSetDatesEV(event)
        
        
        if restartBlacklist:
            evhand.RESTART_BLKLST.append(event.eventlabel)
        
        if markSeen:
            persistent._seen_ever[event.eventlabel] = True
        
        
        eventdb.setdefault(event.eventlabel, event)

    @store.mas_utils.deprecated(use_instead="mas_hideEVL", should_raise=True)
    def hideEventLabel(
            eventlabel,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=evhand.event_database
        ):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        mas_hideEventLabel(eventlabel, lock, derandom, depool, decond, eventdb)

    @store.mas_utils.deprecated(use_instead="mas_hideEvent")
    def hideEvent(
            event,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        mas_hideEvent(event, lock, derandom, depool, decond)


    def mas_hideEvent(
            ev,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Hide an event by Falsing its unlocked/random/pool props

        IN:
            ev - event object we want to hide
            lock - True if we want to lock this event, False if not
                (Default: False)
            derandom - True fi we want to unrandom this Event, False if not
                (Default: False)
            depool - True if we want to unpool this event, Flase if not
                (Default: False)
            decond - True if we want to remove the conditional, False if not
                (Default: False)
        """
        evhand._hideEvent(
            ev,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def mas_hideEventLabel(
            ev_label,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=evhand.event_database
        ):
        """
        Hide an event label by Falsing its unlocked/random/pool props

        NOTE: use this with custom eventdbs

        IN:
            ev_label - label of the event we wnat to hide
            lock - True if we want to lock this event, False if not
                (Default: False)
            derandom - True fi we want to unrandom this Event, False if not
                (Default: False)
            depool - True if we want to unpool this event, Flase if not
                (Default: False)
            decond - True if we want to remove the conditional, False if not
                (Default: False)
            eventdb - event databsae ev_label is in
                (Default: evhand.event_database)
        """
        evhand._hideEventLabel(
            ev_label,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond,
            eventdb=eventdb
        )


    def mas_showEvent(
            ev,
            unlock=False,
            _random=False,
            _pool=False
        ):
        """
        Show an event by Truing its unlock/ranomd/pool props

        IN:
            ev - event to show
            unlock - True if we want to unlock this event, False if not
                (Default: False)
            _random - True if we want to random this event, Flase otherwise
                (Default: False)
            _pool - True if we want to pool this event, False otherwise
                (Default: False)
        """
        if ev:
            if unlock:
                ev.unlocked = True
            
            if _random:
                ev.random = True
            
            if _pool:
                ev.pool = True


    def mas_showEventLabel(
            ev_label,
            unlock=False,
            _random=False,
            _pool=False,
            eventdb=evhand.event_database
        ):
        """
        Shows an event label, by Truing the unlocked, random, and pool
        properties.

        NOTE: use this for custom event dbs

        IN:
            ev_label - label of event to show
            unlock - True if we want to unlock this event, False if not
                (DEfault: False)
            _random - True if we want to random this event, False if not
                (Default: False)
            _pool - True if we want to pool this event, False if not
                (Default: False)
            eventdb - eventdatabase this label belongs to
                (Default: evhannd.event_database)
        """
        mas_showEvent(eventdb.get(ev_label, None), unlock, _random, _pool)

    @store.mas_utils.deprecated(use_instead="mas_lockEvent", should_raise=True)
    def lockEvent(ev):
        """
        NOTE: DEPRECATED
        Locks the given event object

        IN:
            ev - the event object to lock
        """
        mas_lockEvent(ev)

    @store.mas_utils.deprecated(use_instead="mas_lockEventLabel", should_raise=True)
    def lockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        NOTE: DEPRECATED
        Locks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        mas_lockEventLabel(evlabel, eventdb)


    def mas_lockEvent(ev):
        """
        Locks the given event object

        IN:
            ev - the event object to lock
        """
        evhand._lockEvent(ev)


    def mas_lockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Locks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        evhand._lockEventLabel(evlabel, eventdb=eventdb)


    @store.mas_utils.deprecated(use_instead="MASEventList.push")
    def pushEvent(event_label, skipeval=False, notify=False):
        """
        This pushes high priority or time sensitive events onto the top of
        the event list

        IN:
            @event_label - a renpy label for the event to be called
            skipmidloopeval - do we want to skip the mid loop eval to
                prevent other rogue events from interrupting.
                (Defaults: False)
            notify - True will trigger a notification if appropriate. False
                will not
                (Default: False)

        ASSUMES:
            persistent.event_list
        """
        MASEventList.push(event_label, skipeval, notify)


    @store.mas_utils.deprecated(use_instead="MASEventList.queue")
    def queueEvent(event_label, notify=False):
        """
        This adds low priority or order-sensitive events onto the bottom of
        the event list. This is slow, but rarely called and list should be
        small.

        IN:
            @event_label - a renpy label for the event to be called
            notify - True will trigger a notification if appropriate, False
                will not
                (Default: False)

        ASSUMES:
            persistent.event_list
        """
        MASEventList.queue(event_label, notify)


    @store.mas_utils.deprecated(use_instead="mas_unlockEvent", should_raise=True)
    def unlockEvent(ev):
        """
        NOTE: DEPRECATED
        Unlocks the given evnet object

        IN:
            ev - the event object to unlock
        """
        mas_unlockEvent(ev)

    @store.mas_utils.deprecated(use_instead="mas_unlockEventLabel")
    def unlockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        NOTE: DEPRECATED
        Unlocks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        mas_unlockEventLabel(evlabel, eventdb)


    def mas_unlockEvent(ev):
        """
        Unlocks the given evnet object

        IN:
            ev - the event object to unlock
        """
        evhand._unlockEvent(ev)


    def mas_unlockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Unlocks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        evhand._unlockEventLabel(evlabel, eventdb=eventdb)


    def isFuture(ev, date=None):
        """
        Checks if the start_date of the given event happens after the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's start_date is in the future, False otherwise
        """
        return evhand._isFuture(ev, date=date)


    def isPast(ev, date=None):
        """
        Checks if the end_date of the given event happens before the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's end_date is in the past, False otherwise
        """
        return evhand._isPast(ev, date=date)


    def isPresent(ev):
        """
        Checks if current date falls within the given event's start/end date
        range

        IN:
            ev - Event to check the start_time and end_time

        RETURNS:
            True if current time is inside the  Event's start_date/end_date
            interval, False otherwise
        """
        return evhand._isPresent(ev)


    @store.mas_utils.deprecated(use_instead="MASEventList.pop", should_raise=True)
    def popEvent(remove=True):
        """
        DO NOT USE.

        Use MASEventList.pop instead (not exactly the same)
        """
        pass


    def seen_event(event_label):
        """
        Please use mas_seenEvent, this function hasn't been deprecated
        only because it's used a lot in event conditionals
        and I don't want to update them all
        """
        return mas_seenEvent(event_label)

    def mas_seenEvent(event_label):
        """
        This checks if an event has either been seen or is already in the
        event list.

        IN:
            event_lable = The label for the event to be checked

        ASSUMES:
            persistent.event_list
        """
        return renpy.seen_label(event_label) or mas_inEVL(event_label)


    def mas_findEVL(event_label):
        """
        Finds index of the given event label in the even tlist

        IN:
            event_label - event lable to check

        RETURNS: index of the event in teh even tlist, -1 if not found
        """
        for index, item in enumerate(MASEventList.iter()):
            if item.evl == event_label:
                return index
        
        return -1


    def mas_inEVL(event_label):
        """
        This checks if an event is in the event list

        IN:
            event_label - event lable to check

        RETURNS: True if in event list, False if not
        """
        return mas_findEVL(event_label) > -1


    def mas_rmEVL(event_label):
        """
        REmoves an event from the event list if it exists

        IN:
            event label to remove
        """
        position = mas_findEVL(event_label)
        if position >= 0:
            persistent.event_list.pop(position)


    def mas_rmallEVL(event_label):
        """
        Removes all events with athe given label

        IN:
            event label to remove
        """
        position = mas_findEVL(event_label)
        while position >= 0:
            mas_rmEVL(event_label)
            position = mas_findEVL(event_label)


    def restartEvent():
        """
        This checks if there is a persistent topic, and if there was push it
        back on the stack with a little comment.
        """
        curr_eli = MASEventList.load_current()
        
        if curr_eli is None:
            return
        
        
        if not mas_isRstBlk(curr_eli.evl):
            MASEventList._push_eli(curr_eli)
            MASEventList.push('continue_event', skipeval=True)
        
        MASEventList.clear_current()


    def mas_isRstBlk(topic_label):
        """
        Checks if the event with the current label is blacklistd from being
        restarted

        IN:
            topic_label - label of the event we are trying to restart
        """
        if not topic_label:
            return True
        
        if topic_label.startswith("greeting_"):
            return True
        
        if topic_label.startswith("bye"):
            return True
        
        if topic_label.startswith("i_greeting"):
            return True
        
        if topic_label.startswith("ch30_reload"):
            return True
        
        
        if topic_label in evhand.RESTART_BLKLST:
            return True
        
        return False

    def mas_cleanEventList():
        """
        Iterates through the event list and removes items which shouldn't be restarted
        """
        for index, item in MASEventList.rev_enum_iter():
            if mas_isRstBlk(item.evl):
                mas_rmEVL(item.evl)

    def mas_cleanJustSeen(eventlist, db):
        """
        Cleans the given event list of just seen items (withitn the THRESHOLD)
        retunrs not just seen items

        IN:
            eventlist - list of event labels to pick from
            db - database these events are tied to

        RETURNS:
            cleaned list of events (stuff not in the time THREASHOLD)
        """
        import datetime
        now = datetime.datetime.now()
        cleanlist = list()
        
        for evlabel in eventlist:
            ev = db.get(evlabel, None)
            
            if ev:
                if ev.last_seen:
                    if now - ev.last_seen >= store.evhand.LAST_SEEN_DELTA:
                        cleanlist.append(evlabel)
                
                else:
                    cleanlist.append(evlabel)
        
        return cleanlist


    def mas_cleanJustSeenEV(ev_list):
        """
        Cleans the given event list (of events) of just seen items
        (within the THRESHOLD). Returns not just seen items.
        Basically the same as mas_cleanJustSeen, except for Event object lists

        IN:
            ev_list - list of event objects

        RETURNS:
            cleaned list of events (stuff not in the tiem THRESHOLD)
        """
        import datetime
        now = datetime.datetime.now()
        cleaned_list = list()
        
        for ev in ev_list:
            if ev.last_seen is not None:
                
                if now - ev.last_seen >= store.evhand.LAST_SEEN_DELTA:
                    cleaned_list.append(ev)
            
            else:
                
                cleaned_list.append(ev)
        
        return cleaned_list


    def mas_unlockPrompt(count=1):
        """
        Unlocks a pool event

        IN:
            count - number of pool events to unlock
                (Default: 1)

        RETURNS:
            True if an event was unlocked. False otherwise
        """
        
        pool_evs = [
            ev
            for ev in evhand.event_database.itervalues()
            if (
                Event._filterEvent(ev, unlocked=False, pool=True)
                and "no_unlock" not in ev.rules
            )
        ]
        u_count = count
        
        
        while len(pool_evs) > 0 and u_count > 0:
            ev_index = renpy.random.randint(0, len(pool_evs)-1)
            ev = pool_evs.pop(ev_index)
            mas_unlockEvent(ev)
            ev.unlock_date = datetime.datetime.now()
            u_count -= 1
        
        
        if u_count > 0:
            persistent._mas_pool_unlocks += u_count
        
        
        
        return u_count != count


init 1 python in evhand:






    import store
    import datetime

    def actionPush(ev, **kwargs):
        """
        Runs Push Event action for the given event

        IN:
            ev - event to push to event stack
        """
        store.MASEventList.push(ev.eventlabel, notify=True)


    def actionQueue(ev, **kwargs):
        """
        Runs Queue event action for the given event

        IN:
            ev - event to queue to event stack
        """
        store.MASEventList.queue(ev.eventlabel, notify=True)


    def actionUnlock(ev, **kwargs):
        """
        Unlocks an event. Also setse the unlock_date to the given
            unlock time

        IN:
            ev - event to unlock
            unlock_time - time to set unlock_date to
        """
        ev.unlocked = True
        ev.unlock_date = kwargs.get("unlock_time", datetime.datetime.now())


    def actionRandom(ev, **kwargs):
        """
        Randos an event.

        IN:
            ev - event to random
            rebuild_ev - True if we wish to notify idle to rebuild events
        """
        ev.random = True
        if kwargs.get("rebuild_ev", False):
            store.mas_idle_mailbox.send_rebuild_msg()


    def actionPool(ev, **kwargs):
        """
        Pools an event.

        IN:
            ev - event to pool
        """
        ev.pool = True



    store.Event.ACTION_MAP = {
        store.EV_ACT_UNLOCK: actionUnlock,
        store.EV_ACT_QUEUE: actionQueue,
        store.EV_ACT_PUSH: actionPush,
        store.EV_ACT_RANDOM: actionRandom,
        store.EV_ACT_POOL: actionPool
    }





label call_next_event:
    python:
        _ev_list_item = MASEventList.pop()



        renpy.save_persistent()

    if _ev_list_item and renpy.has_label(_ev_list_item.evl):







        $ mas_RaiseShield_dlg()

        $ ev = mas_getEV(_ev_list_item.evl)

        if (
            _ev_list_item.notify
            and (ev is None or ("skip alert" not in ev.rules))
        ):

            if renpy.windows:
                $ mas_display_notif(m_name, mas_win_notif_quips, "Alerta de Temas")
            else:
                $ mas_display_notif(m_name, mas_other_notif_quips, "Alerta de Temas")


        if ev is not None and "keep_idle_exp" not in ev.rules:
            $ mas_moni_idle_disp.unforce_all(skip_dissolve=True)


        $ mas_globals.this_ev = ev
        $ MASEventContext._set(_ev_list_item)

        call expression _ev_list_item.evl from _call_expression


        $ MASEventList.clear_current()
        $ MASEventContext._set(None)
        $ mas_globals.this_ev = None


        $ mas_moni_idle_disp.do_after_topic_logic()


        $ ev = mas_getEV(_ev_list_item.evl)

        if ev is not None:


            if (
                    ev.eventlabel in evhand.event_database
                    and ev.random and not ev.unlocked
            ):
                python:
                    ev.unlocked=True
                    ev.unlock_date=datetime.datetime.now()


            $ ev.shown_count += 1
            $ ev.last_seen = datetime.datetime.now()

        if _return is not None:
            $ ret_items = _return.split("|")

            if "derandom" in ret_items:
                $ ev.random = False

            if "no_unlock" in ret_items:
                $ ev.unlocked = False
                $ ev.unlock_date = None

            if "unlock" in ret_items:
                $ ev.unlocked = True
                if ev.unlock_date is None:
                    $ ev.unlock_date = ev.last_seen

            if "rebuild_ev" in ret_items:
                $ mas_rebuildEventLists()

            if "idle" in ret_items:
                $ mas_setupIdleMode(brb_label=ev.eventlabel)

            if "love" in ret_items:
                $ mas_ILY()

            if "quit" in ret_items:
                $ persistent.closed_self = True
                $ mas_clearNotifs()
                jump _quit


            if "idle_exp" in _return:
                python:
                    _match = re.search(evhand.RET_KEY_PATTERN_IDLE_EXP, _return)
                    if _match is not None:
                        if _match.group("exp") is not None and _match.group("duration") is not None:
                            mas_moni_idle_disp.force_by_code(
                                _match.group("exp"),
                                duration=int(_match.group("duration"))
                            )
                        
                        elif _match.group("tag") is not None:
                            _exp = MASMoniIdleExp.weighted_choice(
                                MASMoniIdleExp.exp_tags_map.get(
                                    _match.group("tag"),
                                    tuple()
                                )
                            )
                            if _exp is not None:
                                mas_moni_idle_disp.force(_exp)


            if "pause" in _return:
                python:
                    _match = re.search(evhand.RET_KEY_PATTERN_PAUSE, _return)
                    if _match is not None and _match.group("duration") is not None:
                        mas_setEventPause(int(_match.group("duration")))

            if "prompt" in ret_items:
                show monika idle
                jump prompt_menu


        if len(persistent.event_list) > 0:
            jump call_next_event

    if store.mas_globals.in_idle_mode:

        $ mas_dlgToIdleShield()
    else:

        $ mas_DropShield_dlg()


    if not renpy.showing("monika idle"):
        show monika idle zorder MAS_MONIKA_Z at t11 with dissolve_monika

    return False





label prompt_menu:

    $ mas_RaiseShield_dlg()

    if store.mas_globals.in_idle_mode:



        $ cb_label = mas_idle_mailbox.get_idle_cb()









        if cb_label is not None and renpy.has_label(cb_label):
            call expression cb_label
        else:


            $ _return = None


        if _return != "idle":
            $ mas_resetIdleMode()


            $ persistent._mas_greeting_type = None


        elif cb_label is not None:
            $ mas_idle_mailbox.send_idle_cb(cb_label)


        if not renpy.showing("monika idle"):
            show monika idle zorder MAS_MONIKA_Z at t11 with dissolve_monika



        $ store.mas_hotkeys.music_enabled = True

        jump prompt_menu_end

    python:

        mas_setTODVars()

        unlocked_events = Event.filterEvents(
            evhand.event_database,
            unlocked=True,
            aff=mas_curr_affection
        )
        sorted_event_labels = Event.getSortedKeys(unlocked_events,include_none=True)



        unseen_event_labels = [
            ev_label
            for ev_label in sorted_event_labels
            if not seen_event(ev_label) and ev_label != "mas_show_unseen"
        ]

        if len(unseen_event_labels) > 0 and persistent._mas_unsee_unseen:
            mas_showEVL('mas_show_unseen','EVE',unlock=True)
            unseen_num = len(unseen_event_labels)
            mas_setEVLPropValues(
                "mas_show_unseen",
                prompt="Quisiera ver 'Texto no visto' ([unseen_num]) de nuevo"
            )
        else:
            mas_hideEVL('mas_show_unseen','EVE',lock=True)

        repeatable_events = Event.filterEvents(
            evhand.event_database,
            unlocked=True,
            pool=False,
            aff=mas_curr_affection
        )





    show monika at t21

    python:
        talk_menu = []
        if len(unseen_event_labels)>0 and not persistent._mas_unsee_unseen:
            
            talk_menu.append((_("{b}Texto no visto{/b}"), "unseen"))
        if mas_hasBookmarks():
            talk_menu.append((_("Marcadores"),"bookmarks"))
        talk_menu.append((_("Hey, [m_name]..."), "prompt"))
        if len(repeatable_events)>0:
            talk_menu.append((_("Repetir conversación"), "repeat"))
        if _mas_getAffection() > -50:
            if mas_passedILY(pass_time=datetime.timedelta(0,10)):
                talk_menu.append((_("¡Yo también te amo!"),"love_too"))
            else:
                talk_menu.append((_("¡Te amo!"), "love"))
        talk_menu.append((_("Me siento..."), "moods"))
        talk_menu.append((_("Adiós"), "goodbye"))
        talk_menu.append((_("No importa"),"nevermind"))

        renpy.say(m, store.mas_affection.talk_quip()[1], interact=False)
        madechoice = renpy.display_menu(talk_menu, screen="talk_choice")

    if madechoice == "unseen":
        call show_prompt_list (unseen_event_labels)

    elif madechoice == "bookmarks":
        call mas_bookmarks

    elif madechoice == "prompt":
        call prompts_categories (True)

    elif madechoice == "repeat":
        call prompts_categories (False)

    elif madechoice == "love":
        $ MASEventList.push("monika_love", skipeval=True)
        $ _return = True

    elif madechoice == "love_too":
        $ MASEventList.push("monika_love_too", skipeval=True)
        $ _return = True

    elif madechoice == "moods":
        call mas_mood_start

    elif madechoice == "goodbye":
        call mas_farewell_start
    else:

        $ _return = None


    if _return is False:
        jump prompt_menu

label prompt_menu_end:
    show monika at t11
    if store.mas_globals.in_idle_mode:
        $ mas_dlgToIdleShield()
    else:
        $ mas_DropShield_dlg()
    jump ch30_visual_skip

label show_prompt_list(sorted_event_labels):
    $ import store.evhand as evhand


    python:
        prompt_menu_items = [
            (mas_getEVLPropValue(ev_label, "prompt"), ev_label, False, False)
            for ev_label in sorted_event_labels
        ]

        hide_unseen_event = mas_getEV("mas_hide_unseen")

        final_items = (
            (_("No quiero ver más este menú"), "mas_hide_unseen", False, False, 20),
            (_("No importa"), False, False, False, 0)
        )

    call screen mas_gen_scrollable_menu(prompt_menu_items, mas_ui.SCROLLABLE_MENU_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)

    if _return:
        $ mas_setEventPause(None)
        $ MASEventList.push(_return, skipeval=True)

    return _return

label prompts_categories(pool=True):



    $ cat_lists = list()

    $ current_category = list()
    $ import store.evhand as evhand
    $ picked_event = False
    python:


        unlocked_events = Event.filterEvents(
            evhand.event_database,


            unlocked=True,
            pool=pool,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )


        main_cat_list = list()
        no_cat_list = list() 
        for key in unlocked_events:
            if unlocked_events[key].category:
                evhand.addIfNew(unlocked_events[key].category, main_cat_list)
            else:
                no_cat_list.append(unlocked_events[key])


        main_cat_list.sort()
        no_cat_list.sort(key=Event.getSortPrompt)




        dis_cat_list = [(x.capitalize() + "...",x) for x in main_cat_list]



        no_cat_list = [(x.prompt, x.eventlabel) for x in no_cat_list]


        dis_cat_list.extend(no_cat_list)


        cat_lists.append(evhand._NT_CAT_PANE(dis_cat_list, main_cat_list))

    while not picked_event:
        python:
            prev_items, prev_cats = cat_lists[len(cat_lists)-1]


            if len(current_category) == 0:
                main_items = None

            else:
                
                
                
                
                
                
                unlocked_events = Event.filterEvents(
                    evhand.event_database,

                    category=(False,current_category),
                    unlocked=True,
                    pool=pool,
                    aff=mas_curr_affection,
                    flag_ban=EV_FLAG_HFM
                )
                
                
                
                
                
                
                
                no_cat_list = sorted(
                    unlocked_events.values(),
                    key=Event.getSortPrompt
                )
                
                
                no_cat_list = [(x.prompt, x.eventlabel) for x in no_cat_list]
                
                
                
                
                
                main_cats = []
                
                
                main_items = no_cat_list
                
                """ KEEP this for legacy purposes
#            sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

            prompt_category_menu = []
            #Make a list of categories

            #Make a list of all categories
            subcategories=set([])
            for event in sorted_event_keys:
                if unlocked_events[event].category is not None:
                    new_categories=set(unlocked_events[event].category).difference(set(current_category))
                    subcategories=subcategories.union(new_categories)

            subcategories = list(subcategories)
            for category in sorted(subcategories, key=lambda s: s.lower()):
                #Don't list additional subcategories if adding them wouldn't change the same you are looking at
                test_unlock = Event.filterEvents(evhand.event_database,full_copy=True,category=[False,current_category+[category]],unlocked=True)

                if len(test_unlock) != len(sorted_event_keys):
                    prompt_category_menu.append([category.capitalize() + "...",category])


            #If we do have a category picked, make a list of the keys
            if sorted_event_keys is not None:
                for event in sorted_event_keys:
                    prompt_category_menu.append([unlocked_events[event].prompt,event])
                """

        call screen twopane_scrollable_menu(prev_items, main_items, evhand.LEFT_AREA, evhand.LEFT_XALIGN, evhand.RIGHT_AREA, evhand.RIGHT_XALIGN, len(current_category)) nopredict



        if _return in prev_cats:

            python:
                if len(current_category) > 0:
                    current_category.pop()
                current_category.append(_return)











        elif _return == -1:
            if len(current_category) > 0:
                $ current_category.pop()
        else:

            $ picked_event = True

            if _return is not False:
                $ mas_setEventPause(None)
                $ MASEventList.push(_return, skipeval=True)

    return _return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="mas_bookmarks",unlocked=False,rules={"no_unlock":None}))


label mas_bookmarks:
    show monika idle
    python:


        prompt_suffix_map = {
            "mas_song_": store.mas_songs.getPromptSuffix
        }


        bookmarks_items = []
        for ev in mas_get_player_bookmarks(persistent._mas_player_bookmarked):
            
            if Event._filterEvent(ev, flag_ban=EV_FLAG_HFM):
                label_prefix = mas_bookmarks_derand.getLabelPrefix(ev.eventlabel)
                
                
                suffix_func = prompt_suffix_map.get(label_prefix)
                
                
                prompt_suffix = suffix_func(ev) if suffix_func else ""
                
                
                bookmarks_items.append(
                    (renpy.substitute(ev.prompt + prompt_suffix), ev.eventlabel, False, False)
                )

        bookmarks_items.sort()

        bk_menu_final_items = (
            (_("Me gustaría eliminar un marcador"), "remove_bookmark", False, False, 20),
            (_("No importa"), "nevermind", False, False, 0)
        )



label mas_bookmarks_loop:
    if not bookmarks_items:
        show monika idle
        return True

    show monika at t21
    call screen mas_gen_scrollable_menu(bookmarks_items, mas_ui.SCROLLABLE_MENU_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *bk_menu_final_items)

    $ topic_choice = _return

    if topic_choice == "nevermind":

        return False

    elif topic_choice == "remove_bookmark":

        call mas_bookmarks_unbookmark (bookmarks_items)
        show monika idle

        $ bookmarks_items = _return
    else:


        show monika at t11
        $ mas_setEventPause(None)
        $ MASEventList.push(topic_choice, skipeval=True)
        return True

    jump mas_bookmarks_loop









label mas_bookmarks_unbookmark(bookmarks_items):
    python:
        def _convert_items(items, convert_into):
            """
            A local func to convert items from
            gen scrollable menu format into check scrollable one
            and vice versa

            IN:
                items - list of items to convert
                convert_into - type of conversion
                    either "CHECK_ITEMS"
                    or "GEN_ITEMS"

            OUT:
                list of converted items
            """
            if convert_into == "CHECK_ITEMS":
                new_items = []
                
                for item in items:
                    prompt = item[0]
                    
                    if item[2]:
                        prompt = "{0}{1}{2}".format("{i}", prompt, "{/i}")
                    
                    
                    if item[3]:
                        prompt = "{0}{1}{2}".format("{b}", prompt, "{/b}")
                    
                    new_items.append(
                        (prompt, item[1], False, True, False)
                    )
            
            else:
                new_items = [
                    (item[0], item[1], False, False)
                    for item in items
                ]
            
            return new_items

        bookmarks_items = _convert_items(bookmarks_items, "CHECK_ITEMS")

    show monika 1eua at t21


    if len(bookmarks_items) > 1:
        $ renpy.say(m, "¿Qué marcadores quieres eliminar?", interact=False)
    else:

        $ renpy.say(m, "Solo selecciona el marcador si estás seguro de que quieres quitarlo", interact=False)

    call screen mas_check_scrollable_menu(bookmarks_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Remove selected")

    $ bookmarks_to_remove = _return
    $ bookmarks_items = _convert_items(bookmarks_items, "GEN_ITEMS")


    if bookmarks_to_remove:
        python:
            for ev_label in bookmarks_to_remove.iterkeys():
                
                if ev_label in persistent._mas_player_bookmarked:
                    persistent._mas_player_bookmarked.remove(ev_label)


            bookmarks_items = filter(lambda item: item[1] not in bookmarks_to_remove, bookmarks_items)

        show monika at t11
        m 1dsa "Okey, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
        m 3hua "¡Todo listo!"

    return bookmarks_items
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
