


define mas_spring_equinox = datetime.date(datetime.date.today().year,3,21)
define mas_summer_solstice = datetime.date(datetime.date.today().year,6,21)
define mas_fall_equinox = datetime.date(datetime.date.today().year,9,23)
define mas_winter_solstice = datetime.date(datetime.date.today().year,12,21)

default persistent._mas_current_season = 0







init -1 python:

    def mas_isSpring(_date=None):
        """
        Checks if given date is during spring
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's spring right now
        """
        if _date is None:
            _date = datetime.date.today()
        
        _date = _date.replace(datetime.date.today().year)
        
        if persistent._mas_pm_live_south_hemisphere:
            return mas_fall_equinox <= _date < mas_winter_solstice
        else:
            return mas_spring_equinox <= _date < mas_summer_solstice

    def mas_isSummer(_date=None):
        """
        Checks if given date is during summer
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's summer right now
        """
        if _date is None:
            _date = datetime.date.today()
        
        _date = _date.replace(datetime.date.today().year)
        
        if persistent._mas_pm_live_south_hemisphere:
            return mas_winter_solstice <= _date or _date < mas_spring_equinox
        else:
            return mas_summer_solstice <= _date < mas_fall_equinox

    def mas_isFall(_date=None):
        """
        Checks if given date is during fall
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's fall right now
        """
        if _date is None:
            _date = datetime.date.today()
        
        _date = _date.replace(datetime.date.today().year)
        
        if persistent._mas_pm_live_south_hemisphere:
            return mas_spring_equinox <= _date < mas_summer_solstice
        else:
            return mas_fall_equinox <= _date < mas_winter_solstice

    def mas_isWinter(_date=None):
        """
        Checks if given date is during winter
        iff none passed in, then we assume today

        Note: If persistent._mas_pm_live_north_hemisphere is none, we assume northern hemi

        RETURNS:
            boolean showing whether or not it's winter right now
        """
        if _date is None:
            _date = datetime.date.today()
        
        _date = _date.replace(datetime.date.today().year)
        
        if persistent._mas_pm_live_south_hemisphere:
            return mas_summer_solstice <= _date < mas_fall_equinox
        else:
            return mas_winter_solstice <= _date or _date < mas_spring_equinox


init 10 python in mas_seasons:
    import store

    PLUGIN_PP_SPRING = "pp_spring"
    PLUGIN_PP_SUMMER = "pp_summer"
    PLUGIN_PP_FALL = "pp_fall"
    PLUGIN_PP_WINTER = "pp_winter"












    def _pp_spring():
        """
        Programming point for spring
        """
        
        store.mas_protectedShowEVL("monika_enjoyingspring", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_outdoors", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_backpacking", "EVE", _random=True)
        
        
        if store.persistent._mas_pm_would_like_mt_peak is None:
            store.mas_protectedShowEVL("monika_mountain", "EVE", _random=True)
        
        
        store.mas_hideEVL("monika_snow", "EVE", derandom=True)
        store.mas_hideEVL("monika_sledding", "EVE", derandom=True)
        store.mas_hideEVL("monika_snowcanvas", "EVE", derandom=True)
        store.mas_hideEVL("monika_cozy", "EVE", derandom=True)
        store.mas_hideEVL("monika_winter", "EVE", derandom=True)
        store.mas_hideEVL("monika_winter_dangers", "EVE", derandom=True)
        store.mas_hideEVL("monika_snowmen", "EVE", derandom=True)
        store.mas_lockEVL("monika_snowballfight", "EVE")
        
        
        store.mas_consumable_hotchocolate.disable()
        
        
        store.mas_submod_utils.getAndRunFunctions(key=PLUGIN_PP_SPRING)
        
        
        
        
        if not renpy.seen_label("greeting_ourreality"):
            store.mas_unlockEVL("greeting_ourreality", "GRE")


    def _pp_summer():
        """
        Programming point for summer
        """
        
        store.mas_hideEVL("monika_enjoyingspring", "EVE", derandom=True)
        
        
        store.mas_protectedShowEVL("monika_fireworks", "EVE", _random=True)
        
        
        store.mas_submod_utils.getAndRunFunctions(key=PLUGIN_PP_SUMMER)

    def _pp_fall():
        """
        Programming point for fall
        """
        
        store.mas_hideEVL("monika_fireworks", "EVE", derandom=True)
        
        
        store.mas_submod_utils.getAndRunFunctions(key=PLUGIN_PP_FALL)


    def _pp_winter():
        """
        Programming point for winter
        """
        
        if not renpy.seen_label("monika_snow"):
            store.mas_protectedShowEVL("monika_snow", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_sledding", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_snowcanvas", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_cozy", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_winter", "EVE", _random=True)
        store.mas_protectedShowEVL("monika_winter_dangers", "EVE", _random=True)
        store.mas_unlockEVL("monika_snowballfight", "EVE")
        
        
        if store.persistent._mas_pm_gets_snow is not False:
            store.mas_protectedShowEVL("monika_snowmen", "EVE", _random=True)
        
        
        store.mas_hideEVL("monika_outdoors", "EVE", derandom=True)
        store.mas_hideEVL("monika_backpacking", "EVE", derandom=True)
        store.mas_hideEVL("monika_mountain", "EVE", derandom=True)
        
        
        if store.seen_event("mas_reaction_hotchocolate"):
            store.mas_consumable_hotchocolate.enable()
        
        
        store.mas_submod_utils.getAndRunFunctions(key=PLUGIN_PP_WINTER)
        
        
        
        store.mas_lockEVL("greeting_ourreality", "GRE")



    _season_pp_map = {
        1: _pp_spring,
        2: _pp_summer,
        3: _pp_fall,
        4: _pp_winter
    }




    _progression_map = {
        1: 2,
        2: 3,
        3: 4,
        4: 1
    }




    _season_logic_map = {
        1: store.mas_isSpring,
        2: store.mas_isSummer,
        3: store.mas_isFall,
        4: store.mas_isWinter
    }


    def _currentSeason():
        """
        Determins the current season and returns appropriate season ID
        """
        for _id, logic in _season_logic_map.iteritems():
            if logic():
                return _id
        
        
        return 3


    def _seasonalCatchup(prev_season):
        """
        Runs through seasonal programming points from the given prevoius
        season to now. Returns the ID of the current season.

        IN:
            prev_season - previously saved season

        RETURNS: current season ID
        """
        curr_season = _currentSeason()
        
        if prev_season == curr_season:
            
            _season_pp_map[curr_season]()
            return curr_season
        
        
        while prev_season != curr_season:
            prev_season = _progression_map.get(prev_season, curr_season)
            
            if prev_season in _season_pp_map:
                _season_pp_map[prev_season]()
        
        return curr_season


init 900 python:

    persistent._mas_current_season = store.mas_seasons._seasonalCatchup(
        persistent._mas_current_season
    )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
