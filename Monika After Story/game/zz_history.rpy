














































































default persistent._mas_pm_has_went_back_in_time = False

init -860 python in mas_history:
    import store
    import datetime


    if store.persistent._mas_history_archives is None:
        store.persistent._mas_history_archives = dict()


    for year in range(2017, datetime.date.today().year + 1):
        if year not in store.persistent._mas_history_archives:
            store.persistent._mas_history_archives[year] = dict()



    if store.persistent._mas_history_mhs_data is None:
        store.persistent._mas_history_mhs_data = dict()


    mhs_db = dict()


    mhs_sorted_list = list()





    L_FOUND = 0


    L_NO_YEAR = 1


    L_NO_KEY = 2



    def lookup(key, year):
        """
        Looks up data in the historical archives.

        IN:
            key - data key to lookup
            year - year to look up data

        RETURNS: a tuple of the following format:
            [0]: Lookup constant
            [1]: retrieved data (which may be None). This is always None if
                we could not find year or key
        """
        archives = store.persistent._mas_history_archives
        
        
        data_file = archives.get(year, None)
        if data_file is None:
            return (L_NO_YEAR, None)
        
        
        if key not in data_file:
            return (L_NO_KEY, None)
        
        
        return (L_FOUND, data_file[key])


    def lookup_ot(key, *years):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to lookup
            years - years to look up data

        RETURNS: SEE lookup_ot_l
        """
        return lookup_otl(key, years)


    def lookup_otl(key, years_list):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years_list - list of years to lookup data

        RETURNS: dict of the following format:
            year: tuple (SEE lookup)
        """
        found_data = dict()
        
        for year in years_list:
            found_data[year] = lookup(key, year)
        
        return found_data


    def verify(key, _verify, years_list):
        """
        Internali version of mas_HistVerify
        """
        if len(years_list) == 0:
            years_list = _valid_year_range()
        
        found_data = lookup_otl(key, years_list)
        years_found = []
        
        for year, data_tuple in found_data.iteritems():
            status, _data = data_tuple
            
            if status == L_FOUND and _data == _verify:
                years_found.append(year)
        
        return (len(years_found) > 0, years_found)


    def _valid_year_range():
        """
        generates the range of years that are valid for historical lookups.

        RETURNS: range of years from 2017 to todays year.
        """
        return range(2017, datetime.date.today().year + 1)



    def _store(value, key, year):
        """
        Stores data in the historical archives.

        NOTE: will OVERWRITE data that already exists.

        IN:
            value - value to store
            key - data key to store value
            year - year to store value
        """
        store.persistent._mas_history_archives[year][key] = value


    def _store_all(year_data, key):
        """
        Stores multiple year's worth of data in the historical archives.

        NOTE: will OVERWRITE data that already exists.

        IN:
            year_data - dictionary of the following format:
                year: data tuple from mas_HistLookup
            key - data key to store values
        """
        for year in year_data:
            lookup_const, data = year_data[year]
            if lookup_const == L_FOUND:
                _store(data, key, year)



    def loadMHSData():
        """
        Loads persistent MASHistorySaver data into the mhs_db

        Also adds MHS to the sorted list and sorts it.

        ASSUMES: the mhs database is already filled
        """
        for mhs_id, mhs_data in store.persistent._mas_history_mhs_data.iteritems():
            mhs = mhs_db.get(mhs_id, None)
            if mhs is not None:
                mhs.fromTuple(mhs_data)
                mhs_sorted_list.append(mhs)
        
        mhs_sorted_list.sort(key=store.MASHistorySaver.getSortKey)


    def saveMHSData():
        """
        Saves MASHistorySaver data from mhs_db into persistent
        """
        for mhs_id, mhs in mhs_db.iteritems():
            store.persistent._mas_history_mhs_data[mhs_id] = mhs.toTuple()



    def addMHS(mhs):
        """
        Adds the given mhs to the database.

        IN:
            mhs - MASHistorySaver object to add

        ASSUMES that the given mhs does not conflict with existing
        """
        mhs_db[mhs.id] = mhs


    def getMHS(mhs_id):
        """
        Gets the MASHistorySaver object with the given id

        IN:
            mhs_id - id of the MASHistorySaver object to get

        RETURNS: MASHistorySaver object, or None if not found
        """
        return mhs_db.get(mhs_id, None)


init -850 python:


    def mas_HistLookup(key, year):
        """
        Looks up data in the historical archives.

        IN:
            key - data key to look up
            year - year to look up data

        RETURNS: a tuple of the following format:
            [0]: mas_history lookup constant
            [1]: retrieved data (which may be None). This is always None if
                we could not find year or key
        """
        return store.mas_history.lookup(key, year)


    def mas_HistLookup_all(key):
        """
        Looks up all historical data for a specific key.

        IN:
            key - data key to look up

        RETURNS: dictionary of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(
            key,
            store.mas_history._valid_year_range()
        )


    def mas_HistLookup_k(year, *keys):
        """
        Looks up data in the historical archives
        NOTE: this accepts keys as string pieces that are put together

        IN:
            year - year to look up data
            keys - string pieces of a key to search for

        RETURNS: same as mas_HistLookup
        """
        return store.mas_history.lookup(".".join(keys), year)


    def mas_HistLookup_ot(key, *years):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years - years to look updata

        RETURNS: dict of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(key, years)


    def mas_HistLookup_otl(key, years_list):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years_list - list of years to lookup data

        RETURNS: dict of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(key, years_list)


    def mas_HistLookup_otl_k(years_list, *keys):
        """
        Looks up data overtime in the historical archives

        IN:
            years_list - list of years to lookup data
            *keys - string pieces of a key to search for

        RETURNS: See mas_HistLookup_otl
        """
        return store.mas_history.lookup_otl(".".join(keys), years_list)


    def mas_HistVerify(key, _verify, *years):
        """
        Verifies if data at the given key matches the verification value.

        IN:
            key - data key to lookup
            _verify - the data we want to match to
            years - years to look up data (as args)
                Dont pass in anything if you want to lookup all years since
                2017

        RETURNS: tuple of the following format:
            [0]: true/False if we found data that matched the verification
            [1]: list of years that matched the verification
        """
        return store.mas_history.verify(key, _verify, years)


    def mas_HistVerify_k(years_list, _verify, *keys):
        """
        Verifies if data at the given key matches the verification value.

        IN:
            years_list - list of years to look up data (as args)
                Pass an empty list if you want to lookup all years since
                2017.
            _verify - the data we want to match to
            *keys - string pieces of a key to search for

        RETURNS: see mas_HistVerify
        """
        return store.mas_history.verify(".".join(keys), _verify, years_list)

    def mas_HistWasFirstValueIn(_verify, year, *keys):
        """
        Checks if the first year that _verify was found for the keys provided in history
        matches the year provided

        IN:
            _verify - Value to check for
            year - year to match
            *keys - string pieces to make a key for history

        OUT:
            boolean:
                - True if the first year matches the year provided
                - False otherwise
        """
        return mas_HistGetFirstYearOfValue(_verify, *keys) == year

    def mas_HistGetFirstYearOfValue(_verify, *keys):
        """
        Gets the first year which has the entry of _verify in the keys provided

        IN:
            _verify - value to check for
            *keys - string pieces of a key to search for

        OUT:
            If there's a point where the value we're checking for is found, we return the first year that is met.
            If not found, we return None
        """
        archive_value = mas_HistVerify_k([],_verify, *keys)
        
        
        if archive_value[0]:
            return archive_value[1][0]
        return None

    def mas_HistVerifyAll_k(_verify, *keys):
        """
        Checks if the value of _verify for the keys is in history at any point

        IN:
            _verify - value to check for
            *keys - string pieces of a key to search for

        OUT:
            boolean:
                - True if _verify is in the key built by the provided pieces at all
                - False otherwise
        """
        return mas_HistVerify_k([],_verify, *keys)[0]

    def mas_HistVerifyLastYear_k(_verify, *keys):
        """
        Checks history for the value of _verify in the key provided last year

        IN:
            _verify - value to check for
            *keys - string pieces of a key to search for

        OUT:
            boolean:
                - True if _verify is in the key built by the provided pieces last year
                - False otherwise
        """
        return mas_HistVerify_k([datetime.date.today().year-1], _verify, *keys)[0]



    class MASHistorySaver(object):
        """
        Class designed to represent mapping of historial data that we need to
        save over certain intervals.

        PROPERTIES:
            id - identifier of this MASHistorySaver object
                NOTE: Must be unique
            trigger - datetime to trigger the saving
                NOTE: this is changed automatically when saving is done
                NOTE: the trigger's year is what we use to determine where to
                    save the historical data
            mapping - mapping of persistent variable names to historical data
                keys
            use_year_before - True means that when saving data, we should use
                trigger.year - 1 as the year to determine where to save
                historical data. This is mainly for year-end events like
                d31 and new years
            dont_reset - True means we do NOT reset the persistent var
                when doing the save.
            entry_pp - programming point called before saving data
                self is passed to this
            exitpp - programming point called after saving data
                self is passed to this
            trigger_pp - programming point called to update trigger with
                instead of the default year+1
            start_dt - datetime that this MHS starts covering
            end_dt - datetime that this MHS stops covering (exclusive)
        """
        import store.mas_history as mas_history
        
        
        first_sesh = -1
        
        def __init__(self,
                mhs_id,
                trigger,
                mapping,
                use_year_before=False,
                dont_reset=False,
                entry_pp=None,
                exit_pp=None,
                trigger_pp=None,
                start_dt=None,
                end_dt=None
            ):
            """
            Constructor

            Throws exception if mhs_id is NOT unique

            IN:
                mhs_id - identifier of this MASHistorySaver object
                    NOTE: Must be unique
                trigger - datetime of when to trigger data saving for this
                    NOTE: if the year of this datetime is 2 years ahead of the
                        current year, we reset this to 1 year ahead of the
                        current year.
                    NOTE: this is changed every time we execute the saveing
                        routine
                    NOTE: trigger.year is used when saving historical data
                mapping - mapping of the persistent variable names to
                    historical data keys
                use_year_before - True will use trigger.year-1 when saving
                    historical data instead of trigger.year.
                    (Default: False)
                dont_reset - True will NOT reset the persistent var after
                    saving.
                    (Default: False)
                entry_pp - programming point called before saving data
                    self is passed to this
                    (Default: None)
                exit_pp - programming point called after saving data
                    self is passed to this
                    (Default: None)
                trigger_pp - if not None, this pp is called with the current
                    trigger when updating trigger, and the returned datetime
                    is used as the new trigger.
                    (Default: None)
                start_dt - datetime that this MHs starts covering
                    if None, then we assume this MHs is continuous
                end_dt - datetime that this MHS stops covering
                    if None, then we assume this MHS is continous
            """
            
            if mhs_id in self.mas_history.mhs_db:
                raise Exception(
                    "History object '{0}' already exists".format(mhs_id)
                )
            
            if MASHistorySaver.first_sesh == -1:
                if persistent.sessions is not None:
                    MASHistorySaver.first_sesh = persistent.sessions.get(
                        "first_session",
                        None
                    )
                
                else:
                    MASHistorySaver.first_sesh = None
            
            self.id = mhs_id
            self.start_dt = start_dt
            self.end_dt = end_dt
            self.use_year_before = use_year_before
            self.setTrigger(trigger)  
            self.mapping = mapping
            self.dont_reset = dont_reset
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            self.trigger_pp = trigger_pp
            self._was_triggered = False
        
        @staticmethod
        def getSortKey(_mhs):
            """
            Gets the sort key for this MASHistorySaver

            IN:
                _mhs - MASHistorSaver to get sort key

            RETURNS the sort key, which is trigger datetime
            """
            return _mhs.trigger
        
        @staticmethod
        def correctTriggerYear(_trigger):
            """
            Determines the correct year to set trigger to.

            A triggers with a correct year are basically triggers that have not
            passed yet. It's not as simple as increasing year since we have to
            account for triggers that have yet to execute this year.

            IN:
                _trigger - trigger we are trying to change

            RETURNS: _trigger with the correct year
            """
            _now = datetime.datetime.now()
            _temp_trigger = _trigger.replace(year=_now.year)
            
            if _now > _temp_trigger:
                
                return _trigger.replace(year=_now.year + 1)
            
            
            return _temp_trigger
        
        def fromTuple(self, data_tuple):
            """
            Loads data from the data tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: datetime to set the trigger property
                    [1]: use_year_before
                        - check for existence before loading
            """
            
            if len(data_tuple) > 1:
                self.use_year_before = data_tuple[1]
            
            self.setTrigger(data_tuple[0])
        
        def isActive(self, check_dt):
            """
            Checks if the given dt is within range of this MHS's range time
            NOTE: if an MHS is continuous, then we are ALWAYS in range
            NOTE: we are also currently only checking the month/day props
                If we want to take year into acct, then this function will need
                to be changed

            IN:
                check_dt - dateime to check

            RETURNS: True if in range, False if not
            """
            if self.isContinuous():
                return True
            
            if self.start_dt.year != self.end_dt.year:
                return (
                    (self.start_dt.replace(year=check_dt.year) <= check_dt)
                    or (check_dt < self.end_dt.replace(year=check_dt.year))
                )
            
            
            return (
                self.start_dt.replace(year=check_dt.year)
                <= check_dt
                < self.end_dt.replace(year=check_dt.year)
            )
        
        def isActiveWithin(self, start_dt, end_dt):
            """
            Checks if this MHS would have been active within the given range
            of dt. NOTE: if an MHS is continuous, then we are ALWAYS within
            range.

            IN:
                start_dt - start of the range to check (inclusive)
                end_dt - end of the range to check (inclusive)

            RETURNS: True if this MHS would hav ebeen active in teh given
                range, False ifnot
            """
            if self.isContinuous():
                return True
            
            return (
                self.isActive(start_dt)
                or self.isActive(end_dt)
                or (self.isFuture(start_dt) and self.isPassed(end_dt))
            )
        
        def isContinuous(self):
            """
            Checks if this MHS is continuous.
            An MHS is continuous if it does not have datetime ranges.

            RETURNS: True if continuos, False if npt
            """
            return self.start_dt is None or self.end_dt is None
        
        def isFuture(self, check_dt):
            """
            Checks if the given dt is before the active range of this MHS

            IN:
                check_dt - dateime to check

            RETURNS: True if future, False if not
            """
            if self.isContinuous():
                return False
            
            return check_dt < self.start_dt.replace(year=check_dt.year)
        
        def isPassed(self, check_dt):
            """
            Checks if the given dt is past the active range of this MHS, aka
            bigger than the end dt

            NOTE: if an MHS is continuous, it is NEVER passed

            IN:
                check_dt - datetime to check

            RETURNS: True if passed, False if not
            """
            if self.isContinuous():
                return False
            
            return self.end_dt.replace(year=check_dt.year) <= check_dt
        
        def resetData(self):
            """
            Resets data in teh mapping. This is highly dangerous.
            """
            
            for p_key in self.mapping:
                persistent.__dict__[p_key] = None
        
        def setTrigger(self, _trigger):
            """
            Sets the trigger of this object. This function does cleansing of
            bad trigger dates.

            IN:
                _trigger - trigger to change to
            """
            _now = datetime.datetime.now()
            
            
            
            
            first_sesh = MASHistorySaver.first_sesh
            if first_sesh is None:
                first_sesh = _now
            
            trigger_year_ahead = _trigger.year - _now.year > 1
            tt_happen_mhs_future = (
                mas_TTDetected()
                and not self.isContinuous()
                and (self.isFuture(_now) or self.isActive(_now))
            )
            impossible_trigger = _trigger <= first_sesh
            
            if (
                    tt_happen_mhs_future
                    or trigger_year_ahead
                    or impossible_trigger
            
            
            ):
                
                
                
                
                
                
                
                
                
                
                
                
                self.trigger = MASHistorySaver.correctTriggerYear(_trigger)
                
                
                
                
                if (
                        self.use_year_before
                        and not tt_happen_mhs_future
                        and not impossible_trigger
                ):
                    self.trigger = self.trigger.replace(year=self.trigger.year + 1)
            
            else:
                
                self.trigger = _trigger
        
        def save(self):
            """
            Runs the saving routine

            NOTE: does NOT check trigger.

            NOTE: will CHANGE trigger
            """
            if self.entry_pp is not None:
                self.entry_pp(self)
            
            
            source = persistent.__dict__
            dest = self.mas_history
            save_year = self.trigger.year
            
            if self.use_year_before:
                save_year -= 1
            
            
            for p_key, data_key in self.mapping.iteritems():
                
                
                dest._store(source.get(p_key, None), data_key, save_year)
                
                
                if not self.dont_reset:
                    source[p_key] = None
            
            
            if self.trigger_pp is not None:
                self.trigger = self.trigger_pp(self.trigger)
            
            else:
                self.trigger = MASHistorySaver.correctTriggerYear(self.trigger)
            
            if self.exit_pp is not None:
                self.exit_pp(self)
            
            
            self._was_triggered = True
        
        def toTuple(self):
            """
            Converts this MASHistorySaver object into a tuple

            RETURNS tuple of the following format:
                [0]: trigger - the trigger property of this object
                [1]: use_year_before - the use_year_before property of this obj
                    NOTE: needed for ease of migrations
            """
            return (self.trigger, self.use_year_before)
        
        def was_triggered(self):
            """
            RETURNS: True if this MHS was triggered during this session
            """
            return self._was_triggered


init -800 python in mas_history:


    def _runMHSAlg():
        """
        Runs the historical data saving algorithm

        ASSUMES:
            - mhs_db is filled with MASHistorySaver objects
        """
        
        
        _now = datetime.datetime.now()
        
        
        for mhs in mhs_sorted_list:
            
            
            if mhs.trigger <= _now:
                mhs.save()

    def _runMHSResetAlg():
        """
        Runs special resets in the case of TT. Do NOT call if TT not detected.
        """
        
        
        
        
        
        
        
        
        
        
        
        
        now_dt = datetime.datetime.now()
        now_ahead = now_dt.replace(year=now_dt.year + 1)
        lse = store.mas_getLastSeshEnd()
        
        same_cal_year = now_dt.year == lse.year
        lse_within_year = lse < now_ahead
        
        for mhs in mhs_sorted_list:
            if not mhs.isContinuous():
                reset = False
                
                if same_cal_year:
                    reset = mhs.isActiveWithin(now_dt, lse)
                
                elif lse_within_year:
                    reset = mhs.isActive(lse) or mhs.isPassed(lse)
                
                else:
                    reset = True
                
                if reset:
                    mhs.resetData()



    loadMHSData()


    _runMHSAlg()


    if store.mas_TTDetected():
        _runMHSResetAlg()


    saveMHSData()


init -816 python in mas_delact:

    nothing = "temp"

init -816 python in mas_history:
    from store.mas_delact import _MDA_safeadd, _MDA_saferm


init -815 python in mas_history:



    def _bday_exit_pp(mhs):
        
        
        
        
        pass



    def _pm_holdme_adj_times(elapsed):
        """
        Sets the appropraite persistent vars according to the elasped time
        for the hold me topic
        """
        
        if store.persistent._mas_pm_longest_held_monika is None:
            store.persistent._mas_pm_longest_held_monika = elapsed
            store.persistent._mas_pm_total_held_monika = elapsed
            return
        
        
        if elapsed > store.persistent._mas_pm_longest_held_monika:
            store.persistent._mas_pm_longest_held_monika = elapsed
        
        
        store.persistent._mas_pm_total_held_monika += elapsed


init -810 python:


























    store.mas_history.addMHS(MASHistorySaver(
        "pm",
        datetime.datetime(2019, 1, 1),
        {
            
            "_mas_pm_religious": "pm.lifestyle.religious",
            "_mas_pm_like_playing_sports": "pm.lifestyle.plays_sports",
            "_mas_pm_like_playing_tennis": "pm.lifestyle.plays_tennis",
            "_mas_pm_meditates": "pm.lifestyle.meditates",
            "_mas_pm_see_therapist": "pm.lifestyle.sees_therapist",
            "_mas_pm_driving_can_drive": "pm.lifestyle.can_drive",
            "_mas_pm_driving_learning": "pm.lifestyle.learning_to_drive",
            "_mas_pm_driving_post_accident": "pm.lifestyle.driving_post_accident",
            "_mas_pm_is_fast_reader": "pm.lifestyle.reads_fast",
            "_mas_pm_is_trans": "pm.lifestyle.is_trans",
            "_mas_pm_social_personality": "pm.lifestyle.social_personality",
            "_mas_pm_swear_frequency": "pm.lifestyle.swear_frequency",
            "_mas_pm_bakes": "pm.lifestyle.bakes",

            
            "_mas_pm_wearsRing": "pm.lifestyle.ring.wears_one",

            
            "_mas_pm_plays_instrument": "pm.lifestyle.play_instrument",
            "_mas_pm_play_jazz": "pm.lifestyle.music.play_jazz",

            
            "_mas_pm_do_smoke": "pm.lifestyle.smoking.smokes",
            "_mas_pm_do_smoke_quit": "pm.lifestyle.smoking.trying_to_quit",
            "_mas_pm_do_smoke_quit_succeeded_before": "pm.lifestyle.smoking.successfully_quit_before",

            
            "_mas_pm_eat_fast_food": "pm.lifestyle.food.eats_fast_food",
            "_mas_pm_drinks_soda": "pm.lifestyle.food.drinks_soda",

            
            "_mas_pm_works_out": "pm.lifestyle.works_out",

            
            "_mas_pm_had_relationships_many": "pm.lifestyle.had_many_relationships",
            "_mas_pm_had_relationships_just_one": "pm.lifestyle.had_one_relationship",

            
            "_mas_pm_last_promoted_d": "pm.lifestyle.last_promoted",

            
            "_mas_pm_love_yourself": "pm.emotions.love_self",
            "_mas_pm_feels_lonely_sometimes": "pm.emotions.lonely_sometimes",

            
            "_mas_pm_have_fam": "pm.family.have_family",
            "_mas_pm_have_fam_sibs": "pm.family.have_siblings",
            "_mas_pm_no_fam_bother": "pm.family.bothers_you",
            "_mas_pm_have_fam_mess": "pm.family.is_mess",
            "_mas_pm_have_fam_mess_better": "pm.family.will_get_better",
            "_mas_pm_no_talk_fam": "pm.family.no_talk_about",
            "_mas_pm_fam_like_monika": "pm.family.likes_monika",

            
            "_mas_pm_has_friends": "pm.friends.has_friends",
            "_mas_pm_few_friends": "pm.friends.few_friends",

            
            "_mas_pm_drawn_art": "pm.actions.drawn_art",
            "_mas_pm_has_bullied_people": "pm.actions.bullied_people",
            "_mas_pm_has_been_to_amusement_park": "pm.actions.been_to_amusement_park",

            
            "_mas_pm_hangs_d25_lights": "pm.actions.hangs_d25_lights",

            
            "_mas_pm_gamed_late": "pm.actions.games.gamed_late",

            
            "_mas_pm_ate_breakfast_times": "pm.actions.food.breakfast_times",
            "_mas_pm_ate_lunch_times": "pm.actions.food.lunch_times",
            "_mas_pm_ate_dinner_times": "pm.actions.food.dinner_times",
            "_mas_pm_ate_snack_times": "pm.actions.food.snack_times",
            "_mas_pm_ate_late_times": "pm.actions.food.late_times",

            
            "_mas_pm_d25_mistletoe_kiss": "pm.actions.monika.mistletoe_kiss",
            "_mas_pm_taken_monika_out": "pm.actions.monika.taken_out_of_sp",
            "_mas_pm_longest_held_monika": "pm.actions.monika.longest_held_time",
            "_mas_pm_total_held_monika": "pm.actions.monika.total_held_time",
            "_mas_pm_listened_to_grad_speech": "pm.actions.monika.listened_to_grad_speech",
            "_mas_pm_got_a_fresh_start": "pm.actions.monika.got_fresh_start",
            "_mas_pm_failed_fresh_start": "pm.actions.monika.failed_fresh_start",
            "_mas_pm_called_moni_a_bad_name": "pm.actions.monika.called_bad_name",

            
            "_mas_pm_gone_to_prom": "pm.actions.prom.went",
            "_mas_pm_prom_good": "pm.actions.prom.good",
            "_mas_pm_had_prom_date": "pm.actions.prom.had_date",
            "_mas_pm_prom_monika": "pm.actions.prom.wanted_monika",
            "_mas_pm_prom_not_interested": "pm.actions.prom.no_interest",
            "_mas_pm_prom_shy": "pm.actions.prom.too_shy",
            "_mas_pm_no_prom": "pm.actions.prom.no_prom",

            
            "_mas_pm_read_yellow_wp": "pm.actions.books.read_yellow_wp",
            "_mas_pm_read_jekyll_hyde": "pm.actions.books.read_jekyll_hyde",

            
            "_mas_pm_donate_charity": "pm.actions.charity.donated",
            "_mas_pm_donate_volunteer_charity": "pm.actions.charity.volunteered",

            
            "_mas_pm_gone_to_comic_con": "pm.actions.gone_to_comic_con",

            
            "_mas_pm_gone_to_anime_con": "pm.actions.gone_to_anime_con",

            
            "_mas_pm_has_went_back_in_time": "pm.actions.mas.went_back_in_time",
            "_mas_pm_snitched_on_chibika": "pm.actions.mas.snitched_on_chibika",

            
            "_mas_pm_added_custom_bgm": "pm.actions.mas.music.added_custom_bgm",

            
            "_mas_pm_zoomed_out": "pm.actions.mas.zoom.out",
            "_mas_pm_zoomed_in": "pm.actions.mas.zoom.in",
            "_mas_pm_zoomed_in_max": "pm.actions.mas.zoom.in_max",

            
            "_mas_pm_will_change": "pm.actions.mas.opendoor.will_change",

            
            "_mas_pm_has_rpy": "pm.actions.mas.dev.has_rpy",
            "_mas_pm_has_contributed_to_mas": "pm.actions.mas.dev.has_contributed",
            "_mas_pm_wants_to_contribute_to_mas": "pm.actions.mas.dev.wants_to_contribute",

            
            "_mas_pm_live_in_city": "pm.location.live_in_city",
            "_mas_pm_live_near_beach": "pm.location.live_near_beach",
            "_mas_pm_live_south_hemisphere": "pm.location.south_hemi",
            "_mas_pm_gets_snow": "pm.location.snows",

            
            "_mas_pm_likes_horror": "pm.likes.horror",
            "_mas_pm_likes_spoops": "pm.likes.spooks",
            "_mas_pm_watch_mangime": "pm.likes.manga_and_anime",
            "_mas_pm_would_like_mt_peak": "pm.likes.reach_mt_peak",
            "_mas_pm_likes_rain": "pm.likes.rain",
            "_mas_pm_likes_travelling": "pm.likes.travelling",
            "_mas_pm_likes_poetry" : "pm.likes.poetry",
            "_mas_pm_likes_board_games": "pm.likes.board_games",
            "_mas_pm_likes_nature": "pm.likes.nature",

            
            "_mas_pm_likes_singing_d25_carols": "pm.likes.d25.singing_carols",

            
            "_mas_pm_a_hater": "pm.likes.monika.not",
            "_mas_pm_liked_grad_speech": "pm.likes.monika.grad_speech",
            "_mas_pm_cares_island_progress": "pm.likes.monika.island.progress",
            

            
            "_mas_pm_like_rap": "pm.likes.music.rap",
            "_mas_pm_like_vocaloids": "pm.likes.music.vocaloids",
            "_mas_pm_like_rock_n_roll": "pm.likes.music.rock_n_roll",
            "_mas_pm_like_orchestral_music": "pm.likes.music.orchestral",
            "_mas_pm_like_jazz": "pm.likes.music.jazz",
            "_mas_pm_like_other_music": "pm.likes.music.other",

            
            "_mas_pm_like_mint_ice_cream": "pm.likes.food.mint_ice_cream",

            
            "_mas_pm_likes_panties": "pm.likes.clothes.panties",
            "_mas_pm_no_talk_panties": "pm.likes.clothes.panties.no_talk",

            
            "_mas_pm_cares_about_dokis": "pm.likes.dokis.cares_about_them",

            
            
            "_mas_pm_lang_other": "pm.know.lang.other",
            "_mas_pm_lang_jpn": "pm.know.lang.jpn",

            
            "_mas_pm_given_false_justice": "pm.exp.given_false_justice",
            "_mas_pm_driving_been_in_accident": "pm.exp.been_in_car_accident",
            "_mas_pm_is_bullying_victim": "pm.exp.victim_of_bullying",
            "_mas_pm_currently_bullied": "pm.exp.currently_being_bullied",
            "_mas_pm_has_code_experience": "pm.exp.code_experience",

            
            
            "_mas_pm_monika_deletion_justice": "pm.op.monika.delmoni_justified",
            "_mas_pm_monika_evil": "pm.op.monika.is_evil",
            "_mas_pm_monika_evil_but_ok": "pm.op.monika.is_evil_but_it_ok",
            "_mas_pm_monika_cute_as_natsuki": "pm.op.monika.is_cute_as_natsuki",

            
            "_mas_pm_shared_appearance": "pm.looks.shared_looks",

            
            "_mas_pm_eye_color": "pm.looks.eyes.color",
            "_mas_pm_has_heterochromia": "pm.looks.eyes.heterochromia",

            
            "_mas_pm_hair_color": "pm.looks.hair.color",
            "_mas_pm_hair_length": "pm.looks.hair.length",
            "_mas_pm_shaved_hair": "pm.looks.hair.shaved",
            "_mas_pm_no_hair_no_talk": "pm.looks.hair.no_talk",

            
            "_mas_pm_skin_tone": "pm.looks.skin.tone",

            
            "_mas_pm_height": "pm.looks.dims.height",
            "_mas_pm_units_height_metric": "pm.looks.dims.height_is_metric",

            
            "_mas_pm_would_come_to_spaceroom": "pm.future.goto_spaceroom",

            
            "_mas_pm_owns_car": "pm.owns.car",
            "_mas_pm_owns_car_type": "pm.owns.car_type",

        },
        use_year_before=True,
        dont_reset=True
    ))


    store.mas_history.addMHS(MASHistorySaver(
        "aff",
        datetime.datetime(2019, 1, 2),
        {
            "_mas_aff_before_fresh_start": "aff.before_fresh_start"
        },
        use_year_before=True,
        dont_reset=True
    ))
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
