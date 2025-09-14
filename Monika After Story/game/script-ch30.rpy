default persistent.monika_reload = 0


default persistent.tried_skip = None



default persistent.monika_kill = None

default persistent.first_run = True
default persistent.rejected_monika = None
default initial_monika_file_check = None
define modoorg.CHANCE = 20
define mas_battery_supported = False
define mas_in_intro_flow = False


default persistent._mas_disable_animations = False

init -998 python:

    if "unstable" in config.version and not persistent.sessions:
        raise Exception(
            _("Hay archivos del modo inestable en la instalación. Esto puede causar problemas.\n"
            "Por favor, reinstale la última versión estable de Monika After Story para asegurar que no haya problemas de datos.")
        )

init -890 python in mas_globals:
    import datetime
    import store


    tt_detected = (
        store.mas_getLastSeshEnd() - datetime.datetime.now()
            > datetime.timedelta(hours=30)
    )

    if tt_detected:
        store.persistent._mas_pm_has_went_back_in_time = True


    is_r7 = renpy.version(True)[0] == 7


    is_steam = "steamapps" in renpy.config.basedir.lower()

init -1 python in mas_globals:



    dlg_workflow = False

    show_vignette = False


    show_lightning = False


    lightning_chance = 16
    sayori_lightning_chance = 10


    show_sayori_lightning = False


    text_speed_enabled = False


    in_idle_mode = False


    late_farewell = False


    last_minute_dt = datetime.datetime.now()


    last_hour = last_minute_dt.hour


    last_day = last_minute_dt.day


    time_of_day_4state = None


    time_of_day_3state = None


    returned_home_this_sesh = bool(store.persistent._mas_moni_chksum)


    this_ev = None



    event_unpause_dt = None

init 970 python:
    import store.mas_filereacts as mas_filereacts



    if persistent._mas_moni_chksum is not None:
        
        
        
        store.mas_dockstat.init_findMonika(mas_docking_station)


init -10 python:

    class MASIdleMailbox(store.MASMailbox):
        """
        Spaceroom idle extension of the mailbox

        PROPERTIES:
            (no additional)

        See MASMailbox for properties
        """
        
        
        REBUILD_EV = 1
        
        
        DOCKSTAT_GRE_TYPE = 2
        
        
        IDLE_MODE_CB_LABEL = 3
        
        
        SKIP_MID_LOOP_EVAL = 4
        
        
        SCENE_CHANGE = 5
        
        
        DISSOLVE_ALL = 6
        
        
        FORCED_EXP = 7
        
        
        
        
        def __init__(self):
            """
            Constructor for the idle mailbox
            """
            super(MASIdleMailbox, self).__init__()
        
        
        def send_rebuild_msg(self):
            """
            Sends the rebuild message to the mailbox
            """
            self.send(self.REBUILD_EV, True)
        
        def get_rebuild_msg(self):
            """
            Gets rebuild message
            """
            return self.get(self.REBUILD_EV)
        
        def send_ds_gre_type(self, gre_type):
            """
            Sends greeting type to mailbox
            """
            self.send(self.DOCKSTAT_GRE_TYPE, gre_type)
        
        def get_ds_gre_type(self, default=None):
            """
            Gets dockstat greeting type

            RETURNS: None by default
            """
            result = self.get(self.DOCKSTAT_GRE_TYPE)
            if result is None:
                return default
            return result
        
        def send_idle_cb(self, cb_label):
            """
            Sends idle callback label to mailbox
            """
            self.send(self.IDLE_MODE_CB_LABEL, cb_label)
        
        def get_idle_cb(self):
            """
            Gets idle callback label
            """
            return self.get(self.IDLE_MODE_CB_LABEL)
        
        def send_skipmidloopeval(self):
            """
            Sends skip mid loop eval message to mailbox
            """
            self.send(self.SKIP_MID_LOOP_EVAL, True)
        
        def get_skipmidloopeval(self):
            """
            Gets skip midloop eval value
            """
            return self.get(self.SKIP_MID_LOOP_EVAL)
        
        def send_scene_change(self):
            """
            Sends scene change message to mailbox
            NOTE: only do this if a scene is acutally necessary
            """
            self.send(self.SCENE_CHANGE, True)
        
        def get_scene_change(self):
            """
            Gets scene change value
            """
            return self.get(self.SCENE_CHANGE)
        
        def send_dissolve_all(self):
            """
            Sends dissolve all message to mailbox
            """
            self.send(self.DISSOLVE_ALL, True)
        
        def get_dissolve_all(self):
            """
            Gets dissolve all value
            """
            return self.get(self.DISSOLVE_ALL)
        
        def send_forced_exp(self, exp):
            """
            Sends forced exp message to mailbox

            IN:
                exp - full exp code to force (None to use idle disp)
            """
            self.send(self.FORCED_EXP, exp)
        
        def get_forced_exp(self):
            """
            Gets forced exp value
            """
            return self.get(self.FORCED_EXP)

    mas_idle_mailbox = MASIdleMailbox()


image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"

image monika_body_glitch1:
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    1.00
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"

image monika_body_glitch2:
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    1.00
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"

image room_glitch = "images/cg/monika/monika_bg_glitch.png"



define MAS_PRONOUN_GENDER_MAP = {
    "his": {"M": "su", "F": "her", "X": "their"},
    "he": {"M": "él", "F": "she", "X": "they"},
    "hes": {"M": "él es", "F": "she's", "X": "they're"},
    "heis": {"M": "él es", "F": "she is", "X": "they are"},
    "bf": {"M": "novio", "F": "girlfriend", "X": "partner"},
    "man": {"M": "hombre", "F": "woman", "X": "person"},
    "boy": {"M": "chico", "F": "girl", "X": "person"},
    "guy": {"M": "chico", "F": "girl", "X": "person"},
    "him": {"M": "él", "F": "her", "X": "them"},
    "himself": {"M": "él mismo", "F": "herself", "X": "themselves"},
    "hero": {"M": "héroe", "F": "heroine", "X": "hero"}
}

init python:
    import subprocess
    import os
    import eliza      
    import datetime   
    import battery    
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    import store.mas_globals as mas_globals
    therapist = eliza.eliza()
    process_list = []
    currentuser = None 
    if renpy.windows:
        try:
            process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
        except:
            pass
        try:
            for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    currentuser = user
        except:
            pass

    try:
        renpy.file("../characters/monika.chr")
        initial_monika_file_check = True
    except:
        
        pass



    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    else:
        mcname = persistent.mcname


    mas_battery_supported = battery.is_supported()



    renpy.music.register_channel(
        "background",
        mixer="amb",
        loop=True,
        stop_on_mute=True,
        tight=True
    )


    renpy.music.register_channel(
        "backsound",
        mixer="amb",
        loop=False,
        stop_on_mute=True
    )


    def show_dialogue_box():
        """
        Jumps to the topic promt menu
        """
        renpy.jump('prompt_menu')


    def pick_game():
        """
        Jumps to the pick a game workflow
        """
        renpy.jump("mas_pick_a_game")


    def mas_getuser():
        """
        Attempts to get the current user

        RETURNS: current user if found, or None if not found
        """
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
        
        return None


    def mas_enable_quitbox():
        """
        Enables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = True


    def mas_disable_quitbox():
        """
        Disables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = False


    def mas_enable_quit():
        """
        Enables quitting without monika knowing
        """
        persistent.closed_self = True
        mas_disable_quitbox()


    def mas_disable_quit():
        """
        Disables quitting without monika knowing
        """
        persistent.closed_self = False
        mas_enable_quitbox()


    def mas_drawSpaceroomMasks(dissolve_masks=True):
        """
        Draws the appropriate masks according to the current state of the
        game.

        IN:
            dissolve_masks - True will dissolve masks, False will not
                (Default; True)
        """
        
        mask = mas_current_weather.get_mask()
        
        
        renpy.show(mask, tag="rm")
        
        if dissolve_masks:
            renpy.with_statement(Dissolve(1.0))


    def mas_validate_suntimes():
        """
        Validates both persistent and store suntimes are in a valid state.
        Sunrise is always used as the lead if a reset is needed.
        """
        if (
            mas_suntime.sunrise > mas_suntime.sunset
            or persistent._mas_sunrise > persistent._mas_sunset
        ):
            mas_suntime.sunset = mas_suntime.sunrise
            persistent._mas_sunset = persistent._mas_sunrise


    def show_calendar():
        """RUNTIME ONLY
        Opens the calendar if we can
        """
        mas_HKBRaiseShield()
        
        if not persistent._mas_first_calendar_check:
            renpy.call('_first_time_calendar_use')
        
        renpy.call_in_new_context("mas_start_calendar_read_only")
        
        if store.mas_globals.in_idle_mode:
            
            store.hkb_button.talk_enabled = True
            store.hkb_button.extra_enabled = True
            store.hkb_button.music_enabled = True
        
        else:
            mas_HKBDropShield()


    dismiss_keys = config.keymap['dismiss']
    renpy.config.say_allow_dismiss = store.mas_hotkeys.allowdismiss

    def slow_nodismiss(event, interact=True, **kwargs):
        """
        Callback for whenever monika talks

        IN:
            event - main thing we can use here, lets us now when in the pipeline
                we are for display text:
                begin -> start of a say statement
                show -> right before dialogue is shown
                show_done -> right after dialogue is shown
                slow_done -> called after text finishes showing
                end -> end of dialogue (user has interacted)
                    NOTE: dismiss needs to be possible for end to be reached
                        when mouse is clicked after an interaction ends.
        """
        
        
        
        
        
        
        
        
        if event == "show" or event == "begin":
            store.mas_hotkeys.set_dismiss(False)
        
        
        
        elif event == "slow_done":
            store.mas_hotkeys.set_dismiss(True)



    @store.mas_utils.deprecated(use_instead="mas_isDayNow", should_raise=True)
    def mas_isMorning():
        """DEPRECATED
        Checks if it is day or night via suntimes

        NOTE: the wording of this function is bad. This does not literally
            mean that it is morning. USE mas_isDayNow

        RETURNS: True if day, false if not
        """
        return mas_isDayNow()


    def mas_progressFilter():
        """
        Changes filter according to rules.

        Call this when you want to update the filter.

        RETURNS: True upon a filter change, False if not
        """
        curr_flt = store.mas_sprites.get_filter()
        new_flt = mas_current_background.progress()
        store.mas_sprites.set_filter(new_flt)
        
        return curr_flt != new_flt

    @store.mas_utils.deprecated(should_raise=True)
    def mas_shouldChangeTime():
        """DEPRECATED
        This no longer makes sense with the filtering system.
        """
        return False


    def mas_shouldRain():
        """
        Rolls some chances to see if we should make it rain

        RETURNS:
            rain weather to use, or None if we dont want to change weather
        """
        
        chance = random.randint(1,100)
        if mas_isMoniNormal(higher=True):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if mas_isSpring():
                return mas_weather._determineCloudyWeather(
                    40,
                    15,
                    15,
                    rolled_chance=chance
                )
            
            elif mas_isSummer():
                return mas_weather._determineCloudyWeather(
                    10,
                    6,
                    5,
                    rolled_chance=chance
                )
            
            elif mas_isFall():
                return mas_weather._determineCloudyWeather(
                    30,
                    12,
                    15,
                    rolled_chance=chance
                )
            
            else:
                
                if chance <= 50:
                    return mas_weather_snow
                elif chance <= 70:
                    return mas_weather_overcast
        
        
        elif mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
            return mas_weather_overcast
        
        elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
            return mas_weather_rain
        
        elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
            return mas_weather_thunder
        
        return None


    def mas_lockHair():
        """
        Locks all hair topics
        """
        mas_lockEVL("monika_hair_select")


    def mas_seasonalCheck():
        """
        Determines the current season and runs an appropriate programming
        point.

        If the global for season is currently None, then we instead set the
        current season.

        NOTE: this does NOT do progressive programming point execution.
            This is intended for runtime usage only.

        ASSUMES:
            persistent._mas_current_season
        """
        _s_tag = store.mas_seasons._currentSeason()
        
        if persistent._mas_current_season != _s_tag:
            
            _s_pp = store.mas_seasons._season_pp_map.get(_s_tag, None)
            if _s_pp is not None:
                
                
                _s_pp()
                
                
                persistent._mas_current_season = _s_tag


    def mas_enableTextSpeed():
        """
        Enables text speed
        """
        style.say_dialogue = style.normal
        store.mas_globals.text_speed_enabled = True


    def mas_disableTextSpeed():
        """
        Disables text speed
        """
        style.say_dialogue = style.default_monika
        store.mas_globals.text_speed_enabled = False


    def mas_resetTextSpeed(ignoredev=False):
        """
        Sets text speed to the appropriate one depending on global settings

        Rules:
        1 - developer always gets text speed (unless ignoredev is True)
        2 - text speed enabled if affection above happy
        3 - text speed disabled otherwise
        """
        if config.developer and not ignoredev:
            mas_enableTextSpeed()
        
        elif (
                mas_isMoniHappy(higher=True)
                and persistent._mas_text_speed_enabled
            ):
            mas_enableTextSpeed()
        
        else:
            mas_disableTextSpeed()


    def mas_isTextSpeedEnabled():
        """
        Returns true if text speed is enabled
        """
        return store.mas_globals.text_speed_enabled

    def mas_check_player_derand():
        """
        Checks the player derandom lists for events that are not random and derandoms them
        """
        
        derand_list = store.mas_bookmarks_derand.getDerandomedEVLs()
        
        
        for ev_label in derand_list:
            
            ev = mas_getEV(ev_label)
            if ev and ev.random:
                ev.random = False

    def mas_get_player_bookmarks(bookmarked_evls):
        """
        Gets topics which are bookmarked by the player
        Also cleans events which no longer exist

        NOTE: Will NOT add events which fail the aff range check

        IN:
            bookmarked_evls - appropriate persistent variable holding the bookmarked eventlabels

        OUT:
            List of bookmarked topics as evs
        """
        bookmarkedlist = []
        
        
        for index in range(len(bookmarked_evls)-1,-1,-1):
            
            ev = mas_getEV(bookmarked_evls[index])
            
            
            if not ev:
                bookmarked_evls.pop(index)
            
            
            elif ev.unlocked and ev.checkAffection(mas_curr_affection):
                bookmarkedlist.append(ev)
        
        return bookmarkedlist

    def mas_get_player_derandoms(derandomed_evls):
        """
        Gets topics which are derandomed by the player (in check-scrollable-menu format)
        Also cleans out events which no longer exist

        IN:
            derandomed_evls - appropriate variable holding the derandomed eventlabels

        OUT:
            List of player derandomed topics in mas_check_scrollable_menu form
        """
        derandlist = []
        
        
        for index in range(len(derandomed_evls)-1,-1,-1):
            
            ev = mas_getEV(derandomed_evls[index])
            
            
            if not ev:
                derandomed_evls.pop(index)
            
            
            elif ev.unlocked:
                derandlist.append((renpy.substitute(ev.prompt), ev.eventlabel, False, True, False))
        
        return derandlist


    def mas_safeToRefDokis():
        """
        Checks if it is safe for us to reference the dokis in a potentially
        sensitive matter. The user must have responded to the question
        regarding dokis - if the user hasn't responded, then we assume it is
        NEVER safe to reference dokis.

        RETURNS: True if safe to reference dokis
        """
        return store.persistent._mas_pm_cares_about_dokis is False

    def mas_set_pronouns(key=None):
        """
        Sets gender specific word replacements

        Few examples:
            "It is his pen." (if the player's gender is declared as male)
            "It is her pen." (if the player's gender is declared as female)
            "It is their pen." (if player's gender is not declared)

        For all available pronouns/words check the keys in MAS_PRONOUN_GENDER_MAP

        IN:
            key - Optional[Literal["M", "F", "X"]] - key (perhaps current gender) to set the pronouns for
                If None, uses persistent.gender
        """
        store = renpy.store
        
        if key is None:
            key = store.persistent.gender
        
        for word, sub_map in store.MAS_PRONOUN_GENDER_MAP.items():
            if key in sub_map:
                value = sub_map[key]
            else:
                value = sub_map["X"]
            setattr(store, word, value)


init 995 python in mas_reset:


    import store.mas_submod_utils as mas_submod_utils

    def ch30_reset(priority=0):
        """
        decorator that marks function to run as part of ch30_reset.

        IN:
            func - function to register
            priority - priority to run function
                Default: 0
                PLEASE USE POSITIVE PRIORITIES. If you need to slip
                something between existing reset code, be mindful of where you
                plugin your reset code. Take a look at the reset functions
                below for the correct placement.
        """
        return mas_submod_utils.functionplugin("ch30_reset", priority=priority)


init 999 python in mas_reset:




    import datetime
    import random

    import store
    import store.mas_background as mas_background
    import store.mas_egg_manager as mas_egg_manager
    import store.mas_dockstat as mas_dockstat
    import store.mas_games as mas_games
    import store.mas_globals as mas_globals
    import store.mas_island_event as mas_island_event
    import store.mas_randchat as mas_randchat
    import store.mas_selspr as mas_selspr
    import store.mas_songs as mas_songs
    import store.mas_sprites as mas_sprites
    import store.mas_utils as mas_utils
    import store.mas_windowutils as mas_windowutils
    import store.mas_xp as mas_xp


    from store import persistent

    @ch30_reset(-980)
    def start():
        """
        Reset code that should always be first
        """
        
        
        store.MASEventList.sync_current()


    @ch30_reset(-960)
    def xp():
        """
        Runs reset code specific for xp stuff
        """
        
        if persistent._mas_xp_lvl < 0:
            persistent._mas_xp_lvl = 0 
        
        if persistent._mas_xp_tnl < 0:
            persistent._mas_xp_tnl = mas_xp.XP_LVL_RATE
        elif int(persistent._mas_xp_tnl) > (2* int(mas_xp.XP_LVL_RATE)):
            
            persistent._mas_xp_tnl = 2 * mas_xp.XP_LVL_RATE
        
        if persistent._mas_xp_hrx < 0:
            persistent._mas_xp_hrx = 0.0
        
        
        mas_xp.set_xp_rate()
        mas_xp.prev_grant = store.mas_getCurrSeshStart()


    @ch30_reset(-940)
    def name_eggs():
        """
        Runs reset code specific for name eggs
        """
        
        if mas_egg_manager.sayori_enabled() or store.mas_isO31():
            mas_globals.show_sayori_lightning = True


    @ch30_reset(-920)
    def topic_lists():
        """
        Runs reset code specific for topic lists
        """
        
        if not store.mas_events_built:
            store.mas_rebuildEventLists()
        
        
        if len(store.mas_rev_unseen) == 0:
            
            
            
            store.random_seen_limit = 1000


    @ch30_reset(-900)
    def rpy_file_check():
        """
        Runs reset code specific for the rpy file check
        """
        if not persistent._mas_pm_has_rpy:
            if store.mas_hasRPYFiles():
                if not store.mas_inEVL("monika_rpy_files"):
                    store.MASEventList.queue("monika_rpy_files")
            
            else:
                if persistent.current_monikatopic == "monika_rpy_files":
                    persistent.current_monikatopic = 0
                store.mas_rmallEVL("monika_rpy_files")


    @ch30_reset(-880)
    def games():
        """
        Runs reset code specific for games
        """
        
        game_unlock_db = {
            "chess": "mas_unlock_chess",
            "hangman": "mas_unlock_hangman",
            "piano": "mas_unlock_piano"
        }
        
        store.mas_unlockGame("pong")
        
        if renpy.seen_label("mas_reaction_gift_noudeck"):
            store.mas_unlockGame("nou")
        else:
            store.mas_lockGame("nou")
        
        for game_name, game_startlabel in game_unlock_db.iteritems():
            
            if store.mas_getEVL_shown_count(game_startlabel) > 0:
                store.mas_unlockGame(game_name)
            
            else:
                store.mas_lockGame(game_name)


    @ch30_reset(-860)
    def sprites():
        """
        Runs reset code for sprites
        """
        _sprites_init()
        
        
        store.monika_chr.load(startup=True)
        
        _sprites_fixes()
        
        _sprites_setup()


    def _sprites_init():
        """
        Runs reset code for initializing sprites
        """
        
        mas_sprites.apply_ACSTemplates()
        
        
        
        mas_selspr.unlock_hair(store.mas_hair_def)
        
        mas_selspr.unlock_clothes(store.mas_clothes_def)
        
        
        mas_selspr.unlock_acs(store.mas_acs_ribbon_def)
        
        
        mas_selspr._validate_group_topics()


    def _sprites_fixes():
        """
        Runs reset code for fixing sprite issues
        """
        
        if (
                store.monika_chr.clothes != store.mas_clothes_def
                and (
                    store.mas_isMoniDis(lower=True)
                    or (
                        store.mas_isMoniNormal(lower=True)
                        and not store.mas_hasSpecialOutfit()
                    )
                )
        ):
            store.MASEventList.push("mas_change_to_def",skipeval=True)
        
        
        if not store.mas_hasSpecialOutfit():
            store.mas_lockEVL("monika_event_clothes_select", "EVE")
        
        
        
        
        if persistent._mas_acs_enable_promisering and not store.monika_chr.is_wearing_clothes_with_exprop("hide-ring"):
            
            store.monika_chr.wear_acs(store.mas_acs_promisering)


    def _sprites_setup():
        """
        Runs other sprite setup that is not init or fixes
        """
        
        now = datetime.datetime.now()
        if (
                persistent._mas_dev_ahoge
                or store.mas_isMNtoSR(now.time())
                or store.mas_isSRtoN(now.time())
        ):
            
            
            
            
            
            if (
                    persistent._mas_dev_ahoge
                    or (
                        store.mas_getAbsenceLength() >= datetime.timedelta(minutes=30)
                        and random.randint(1, 2) == 1
                    )
            ):
                
                store.monika_chr.ahoge()
        
        else:
            
            store.monika_chr._set_ahoge(None)
        
        
        store.mas_startupPlushieLogic(4)
        
        
        mas_selspr.startup_prompt_check()


    @ch30_reset(-840)
    def random_chatter():
        """
        Runs reset code for random chatter
        """
        
        mas_randchat.adjustRandFreq(persistent._mas_randchat_freq)


    @ch30_reset(-820)
    def returned_home():
        """
        Runs reset code for returned home
        """
        
        if persistent._mas_monika_returned_home is not None:
            _rh = persistent._mas_monika_returned_home.date()
            if datetime.date.today() > _rh:
                persistent._mas_monika_returned_home = None


    @ch30_reset(-800)
    def playtime():
        """
        Runs reset code for playtime
        """
        
        
        
        
        
        
        
        
        if persistent.sessions is not None:
            tp_time = store.mas_getTotalPlaytime()
            max_time = store.mas_maxPlaytime()
            if tp_time > max_time:
                
                persistent.sessions["total_playtime"] = max_time // 100
                
                
                store.mas_dockstat.setMoniSize(
                    persistent.sessions["total_playtime"]
                )
            
            elif tp_time < datetime.timedelta(0):
                
                persistent.sessions["total_playtime"] = datetime.timedelta(0)
                
                
                store.mas_dockstat.setMoniSize(
                    persistent.sessions["total_playtime"]
                )


    @ch30_reset(-780)
    def affection():
        """
        Runs reset code for affection
        """
        
        store.mas_affection._withdraw_aff()


    @ch30_reset(-760)
    def deco():
        """
        Runs reset code for deco
        """
        _deco_bday()












    def _deco_bday():
        """
        Runs reset code for bday deco
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        if (
                not store.mas_isMonikaBirthday()
                and not store.mas_isMonikaBirthday(yesterday)
        ):
            persistent._mas_bday_visuals = False
        
        
        if (
            not store.mas_isplayer_bday()
            and not store.mas_isplayer_bday(yesterday, use_date_year=True)
            and not persistent._mas_player_bday_left_on_bday
        ):
            persistent._mas_player_bday_decor = False


    def _deco_d25():
        """
        Runs reset code for d25 deco
        """
        
        
        
        
        
        mod_d25c_start = store.mas_d25c_start - datetime.timedelta(days=28)
        mod_d25c_end = store.mas_d25c_end + datetime.timedelta(days=28)
        today = datetime.date.today()
        
        if store.mas_isInDateRange(today, mod_d25c_end, mod_d25c_start, True, True):
            
            store.mas_d25HideVisuals()


    def _deco_o31():
        """
        Runs reset code for o31 deco
        """
        
        
        mod_o31_start = store.mas_o31 - datetime.timedelta(days=7)
        mod_o31_end = store.mas_o31 + datetime.timedelta(days=7)
        today = datetime.date.today()
        
        if not store.mas_isInDateRange(today, mod_o31_start, mod_o31_end, True, True):
            
            store.mas_o31HideVisuals()


    @ch30_reset(-740)
    def farewells():
        """
        Runs reset code for farewells
        """
        
        
        if persistent.mas_late_farewell:
            mas_globals.late_farewell = True
            persistent.mas_late_farewell = False


    @ch30_reset(-720)
    def file_reactions():
        """
        Runs reset code for file reactions
        """
        today = datetime.date.today()
        
        
        if persistent._mas_filereacts_just_reacted:
            store.MASEventList.queue("mas_reaction_end")
        
        
        
        if (
            persistent._mas_filereacts_reacted_map
            and store.mas_pastOneDay(
                persistent._mas_filereacts_last_reacted_date
            )
        ):
            persistent._mas_filereacts_reacted_map = dict()
        
        
        if persistent._mas_filereacts_last_aff_gained_reset_date > today:
            persistent._mas_filereacts_last_aff_gained_reset_date = today
        
        
        if persistent._mas_filereacts_last_aff_gained_reset_date < today:
            persistent._mas_filereacts_gift_aff_gained = 0
            persistent._mas_filereacts_last_aff_gained_reset_date = today


    @ch30_reset(-700)
    def events():
        """
        Runs reset code for general events + events list stuff
        """
        
        store.mas_check_player_derand()
        
        
        for index in range(len(persistent.event_list)-1, -1, -1):
            item = persistent.event_list[index]
            
            
            if type(item) != tuple:
                new_data = (item, False)
            else:
                new_data = item
            
            
            if store.renpy.has_label(new_data[0]):
                persistent.event_list[index] = new_data
            
            else:
                persistent.event_list.pop(index)
        
        
        store.MASUndoActionRule.check_persistent_rules()
        
        store.MASStripDatesRule.check_persistent_rules(
            persistent._mas_strip_dates_rules
        )
        
        if store.seen_event('mas_gender'):
            store.mas_unlockEVL("monika_gender_redo","EVE")
        
        if store.seen_event('mas_preferredname'):
            store.mas_unlockEVL("monika_changename","EVE")


    @ch30_reset(-680)
    def songs():
        """
        Runs reset code for songs
        """
        
        mas_songs.checkRandSongDelegate()
        
        
        mas_songs.checkSongAnalysisDelegate()


    @ch30_reset(-660)
    def holidays():
        """
        Runs reset code for holidays that do not fall under the other
        categories.
        """
        
        store.mas_confirmedParty()
        
        
        
        if (
            persistent._mas_d25_gifts_given
            and not store.mas_isD25GiftHold()
            and not mas_globals.returned_home_this_sesh
        ):
            store.mas_d25SilentReactToGifts()


    @ch30_reset(-640)
    def backgrounds():
        """
        Runs reset code for backgrounds
        """
        
        store.mas_setTODVars()
        
        
        store.mas_checkBackgroundChangeDelegate()
        
        
        
        store.mas_validate_suntimes()
        
        
        mas_background.buildupdate()


    @ch30_reset(-620)
    def window_reactions():
        """
        Runs reset code for window reactions
        """
        
        mas_windowutils._setMASWindow()


    @ch30_reset(-600)
    def islands():
        """
        Runs reset code for islands
        """
        
        mas_island_event.advance_progression()


    @ch30_reset(-580)
    def bath_cleanup():
        """
        Cleanup code for bath stuff
        """
        
        bath_cleanup_ev = store.mas_getEV("mas_after_bath_cleanup")
        if (
            bath_cleanup_ev is not None
            and bath_cleanup_ev.start_date is not None
        ):
            
            
            if (
                mas_dockstat.retmoni_status is None
                and store.mas_getAbsenceLength() >= datetime.timedelta(minutes=10)
                and bath_cleanup_ev.start_date > datetime.datetime.now()
            ):
                store.mas_after_bath_cleanup_change_outfit()
                store.mas_stripEVL("mas_after_bath_cleanup", list_pop=True, remove_dates=True)

    @ch30_reset(-560)
    def chr_removal():
        """
        Remove .chr files in the characters folder
        """
        
        if renpy.seen_label("introduction"):
            store.mas_delete_all_chrs()


    @ch30_reset(-560)
    def backups():
        """
        Runs reset for backup code
        """
        if persistent._mas_is_backup:
            store.MASEventList.push("mas_backup_restored")
            mas_utils.mas_log.info("Detectada una copia de seguridad restaurada")
            persistent._mas_is_backup = False


    def final():
        """
        Runs reset code that should run after everythign else
        """
        if mas_dockstat.retmoni_status is not None:
            store.monika_chr.remove_acs(store.mas_acs_quetzalplushie)
            
            
            
            store.MASConsumable._reset()
            
            
            if not store.mas_inEVL("mas_consumables_remove_thermos"):
                store.MASEventList.queue("mas_consumables_remove_thermos")
        
        
        
        store.MASEventList.clean()












































label spaceroom(start_bg=None, hide_mask=None, hide_monika=False, dissolve_all=False, dissolve_masks=False, scene_change=False, force_exp=None, hide_calendar=None, day_bg=None, night_bg=None, show_emptydesk=True, progress_filter=True, bg_change_info=None):

    with None


    if hide_mask is None:
        $ hide_mask = store.mas_current_background.hide_masks
    if hide_calendar is None:
        $ hide_calendar = store.mas_current_background.hide_calendar





    python:
        if progress_filter and mas_progressFilter():
            dissolve_all = True

        day_mode = mas_current_background.isFltDay()

    if scene_change:
        scene black

        if not hide_calendar:
            $ mas_calShowOverlay()
    else:

        if hide_mask:
            hide rm


        if hide_calendar:
            $ mas_calHideOverlay()
        else:
            $ mas_calShowOverlay()

    python:
        monika_room = mas_current_background.getCurrentRoom()


        if persistent._mas_auto_mode_enabled:
            if (
                    mas_globals.dark_mode is None 
                    or day_mode == mas_globals.dark_mode
            ):
                
                
                
                mas_darkMode(day_mode)
        else:
            if mas_globals.dark_mode != persistent._mas_dark_mode_enabled:
                
                
                mas_darkMode(not persistent._mas_dark_mode_enabled)


        if hide_monika:
            if not scene_change:
                renpy.hide("monika")
            
            if show_emptydesk:
                store.mas_sprites.show_empty_desk()

        else:
            if force_exp is None:
                force_exp = "monika idle"
            
            
            
            
            
            
            if not renpy.showing(force_exp):
                
                
                renpy.show(force_exp, tag="monika", at_list=[t11], zorder=MAS_MONIKA_Z)
                
                if not dissolve_all:
                    renpy.with_statement(None)


        if not dissolve_all and not hide_mask:
            mas_drawSpaceroomMasks(dissolve_masks)



        if start_bg:
            if not renpy.showing(start_bg):
                renpy.show(start_bg, tag="sp_mas_room", zorder=MAS_BACKGROUND_Z)

        elif monika_room is not None:
            if not renpy.showing(monika_room):
                renpy.show(
                    monika_room,
                    tag="sp_mas_room",
                    zorder=MAS_BACKGROUND_Z
                )




        if scene_change:
            if bg_change_info is None or len(bg_change_info) < 1:
                bg_change_info = store.mas_background.MASBackgroundChangeInfo()
                mas_current_background._entry_deco(None, bg_change_info)

        elif mas_current_background._deco_man.changed:
            
            
            bg_change_info = store.mas_background.MASBackgroundChangeInfo()
            mas_current_background._exit_deco(None, bg_change_info)
            mas_current_background._entry_deco(None, bg_change_info)
            mas_current_background._deco_man.changed = False


        if bg_change_info is not None:
            if not scene_change:
                for h_adf in bg_change_info.hides.itervalues():
                    h_adf.hide()
            
            for s_tag, s_info in bg_change_info.shows.iteritems():
                s_tag_real, s_adf = s_info
                s_adf.show(s_tag_real)
            
            if len(bg_change_info) > 0 and not dissolve_all:
                renpy.with_statement(Dissolve(1.0))
            
            bg_change_info = None
            mas_current_background._deco_man.changed = False


    if store.mas_globals.show_vignette:
        show vignette zorder 70
    elif renpy.showing("vignette"):
        hide vignette


    if persistent._mas_bday_visuals:

        $ store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)



    if persistent._mas_player_bday_decor:
        $ store.mas_surpriseBdayShowVisuals()


    if not persistent._mas_bday_visuals and not persistent._mas_player_bday_decor:
        $ store.mas_surpriseBdayHideVisuals(cake=True)

    if datetime.date.today() == persistent._date_last_given_roses and not mas_isO31():
        $ monika_chr.wear_acs(mas_acs_roses)


    if dissolve_all and not hide_mask:
        $ mas_drawSpaceroomMasks(dissolve_all)
    elif dissolve_all:
        $ renpy.with_statement(Dissolve(1.0))


    if not hide_monika and not show_emptydesk:
        hide emptydesk

    return


label ch30_main:
    $ mas_skip_visuals = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = persistent._mas_monika_nickname
    $ delete_all_saves()
    $ persistent.clear[9] = True


    call ch30_reset


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_in_intro_flow = True



    $ mas_RaiseShield_core()


    $ store.hkb_button.enabled = False



    call spaceroom (scene_change=True, dissolve_all=True, force_exp="monika 6dsc_static")




    call introduction



    $ mas_DropShield_core()


    $ mas_in_intro_flow = False


    $ store._mas_root.initialSessionData()


    $ skip_setting_weather = True


    if not mas_events_built:
        $ mas_rebuildEventLists()

    jump ch30_preloop

label continue_event:
    m "Ahora, donde estaba..."
    return

label ch30_noskip:
    show screen fake_skip_indicator
    m 1esc "... ¿Estás intentando avanzar rápido?"
    m 1ekc "No te estoy aburriendo, ¿verdad?"
    m "Oh, dios..."
    m 2esa "... Bueno, para que lo sepas, no hay nada que adelantar, [player]."
    m "Después de todo, solo somos nosotros dos..."
    m 1eua "Pero aparte de eso, el tiempo ya no existe realmente, así que ni siquiera va a funcionar."
    m "Ahora, voy a seguir adelante y apagaré eso por ti..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m 1hua "¡Ya está!"
    m 1esa "Serás un encanto y me escucharás a partir de ahora, ¿verdad?"
    m "Gracias~"
    hide screen fake_skip_indicator


    $ restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:

    jump ch30_autoload


label ch30_autoload:


    python:
        import store.evhand as evhand

        m.display_args["callback"] = slow_nodismiss
        m.what_args["slow_abortable"] = config.developer

        if not config.developer:
            config.allow_skipping = False

        mas_resetTextSpeed()
        quick_menu = True
        startup_check = True 
        mas_skip_visuals = False


        skip_setting_weather = False

        mas_cleanEventList()


    call mas_set_gender


    call ch30_reset



    python:
        if (
            persistent._mas_pm_got_a_fresh_start
            and _mas_getAffection() <= -50
        ):
            persistent._mas_load_in_finalfarewell_mode = True
            persistent._mas_finalfarewell_poem_id = "ff_failed_promise"

        elif _mas_getAffection() <= -115:
            persistent._mas_load_in_finalfarewell_mode = True
            persistent._mas_finalfarewell_poem_id = "ff_affection"



    if persistent._mas_load_in_finalfarewell_mode:
        jump mas_finalfarewell_start


    $ selected_greeting = None


    $ mas_startupBackground()













    if store.mas_dockstat.retmoni_status is not None:

        $ store.mas_dockstat.triageMonika(False)

label mas_ch30_post_retmoni_check:



    if mas_isO31() or persistent._mas_o31_in_o31_mode:
        jump mas_o31_autoload_check

    elif (
        mas_isD25Season()
        or persistent._mas_d25_in_d25_mode
        or (mas_run_d25s_exit and not mas_lastSeenInYear("mas_d25_monika_d25_mode_exit"))
    ):
        jump mas_holiday_d25c_autoload_check

    elif mas_isF14() or persistent._mas_f14_in_f14_mode:
        jump mas_f14_autoload_check



    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    if mas_isMonikaBirthday() or persistent._mas_bday_in_bday_mode:
        jump mas_bday_autoload_check



label mas_ch30_post_holiday_check:



    if _mas_getAffection() <= -50 and seen_event("mas_affection_apology"):




        if persistent._mas_affection_should_apologise and not is_apology_present():
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True)
            jump mas_affection_noapology


        elif persistent._mas_affection_should_apologise and is_apology_present():
            $ persistent._mas_affection_should_apologise = False
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True)
            jump mas_affection_yesapology


        elif not persistent._mas_affection_should_apologise and not is_apology_present():
            $ persistent._mas_affection_should_apologise = True
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True)
            jump mas_affection_apologydeleted


    $ gre_cb_label = None
    $ just_crashed = False
    $ forced_quit = False


    if store.mas_egg_manager.yuri_enabled():
        call yuri_name_scare from _call_yuri_name_scare


        jump ch30_post_greeting_check

    elif not persistent._mas_game_crashed:

        $ forced_quit = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RELOAD

    elif not persistent.closed_self:

        $ just_crashed = True
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CRASHED


        $ persistent.closed_self = True




    python:


        persistent._mas_greeting_type = store.mas_greetings.checkTimeout(
            persistent._mas_greeting_type
        )


        sel_greeting_ev = store.mas_greetings.selectGreeting(
            persistent._mas_greeting_type
        )


        persistent._mas_greeting_type = None

        if sel_greeting_ev is None:
            
            
            if persistent._mas_in_idle_mode:
                
                mas_resetIdleMode()
            
            if just_crashed:
                
                
                
                
                sel_greeting_ev = mas_getEV("mas_crashed_start")
            
            elif forced_quit:
                
                
                
                sel_greeting_ev = mas_getEV("ch30_reload_delegate")




        if sel_greeting_ev is not None:
            selected_greeting = sel_greeting_ev.eventlabel
            
            
            mas_skip_visuals = MASGreetingRule.should_skip_visual(
                event=sel_greeting_ev
            )
            
            
            setup_label = MASGreetingRule.get_setup_label(sel_greeting_ev)
            if setup_label is not None and renpy.has_label(setup_label):
                gre_cb_label = setup_label
            
            
            mas_idle_mailbox.send_forced_exp(MASGreetingRule.get_forced_exp(sel_greeting_ev))


    if gre_cb_label is not None:
        call expression gre_cb_label

label ch30_post_greeting_check:



    $ restartEvent()

label ch30_post_restartevent_check:



    python:
        if persistent.sessions['last_session_end'] is not None and persistent.closed_self:
            away_experience_time = datetime.datetime.now()-persistent.sessions['last_session_end']
            
            if away_experience_time.total_seconds() >= times.REST_TIME:
                
                mas_gainAffection(current_evlabel="[rested]")
            
            
            while persistent._mas_pool_unlocks > 0 and mas_unlockPrompt():
                persistent._mas_pool_unlocks -= 1

        else:
            
            mas_loseAffection(modifier=2, reason=4)

label ch30_post_exp_check:




    $ mas_checkReactions()



    python:
        startup_events = {}
        for evl in evhand.event_database:
            ev = evhand.event_database[evl]
            if ev.action != EV_ACT_QUEUE:
                startup_events[evl] = ev

        Event.checkEvents(startup_events)


    $ mas_checkAffection()


    $ mas_checkApologies()


    if (
            store.mas_per_check.is_per_corrupt()
            and not renpy.seen_label("mas_corrupted_persistent")
    ):
        $ MASEventList.push("mas_corrupted_persistent")


    if selected_greeting:

        if persistent._mas_in_idle_mode:
            $ MASEventList.push("mas_idle_mode_greeting_cleanup")

        $ MASEventList.push(selected_greeting)


    $ MASConsumable._checkConsumables(startup=not mas_globals.returned_home_this_sesh)








label ch30_preloop:


    window auto

    python:


        mas_HKRaiseShield()
        mas_HKBRaiseShield()
        set_keymaps()

        persistent.closed_self = False


        persistent._mas_game_crashed = True
        startup_check = False
        mas_checked_update = False
        mas_globals.last_minute_dt = datetime.datetime.now()
        mas_globals.last_hour = mas_globals.last_minute_dt.hour
        mas_globals.last_day = mas_globals.last_minute_dt.day


        mas_runDelayedActions(MAS_FC_IDLE_ONCE)


        mas_resetWindowReacts()


        mas_updateFilterDict()


        renpy.save_persistent()


        if mas_idle_mailbox.get_rebuild_msg():
            mas_rebuildEventLists()

    if mas_skip_visuals:
        $ mas_OVLHide()
        $ mas_skip_visuals = False
        $ quick_menu = True
        jump ch30_visual_skip


    $ mas_idle_mailbox.send_scene_change()
    $ mas_idle_mailbox.send_dissolve_all()


    $ mas_startupWeather()


    $ skip_setting_weather = False


    $ mas_startup_song()

    jump ch30_loop

label ch30_loop:
    $ quick_menu = True





    python:
        should_dissolve_masks = (
            mas_weather.weatherProgress()
            and mas_isMoniNormal(higher=True)
        )

        force_exp = mas_idle_mailbox.get_forced_exp()
        should_dissolve_all = mas_idle_mailbox.get_dissolve_all()
        scene_change = mas_idle_mailbox.get_scene_change()

    call spaceroom (scene_change=scene_change, force_exp=force_exp, dissolve_all=should_dissolve_all, dissolve_masks=should_dissolve_masks)







    if not mas_checked_update:
        $ mas_backgroundUpdateCheck()
        $ mas_checked_update = True

label ch30_visual_skip:

    $ persistent.autoload = "ch30_autoload"






    if store.mas_dockstat.abort_gen_promise:
        $ store.mas_dockstat.abortGenPromise()

    if mas_idle_mailbox.get_skipmidloopeval():
        jump ch30_post_mid_loop_eval






    $ now_check = datetime.datetime.now()


    if now_check.day != mas_globals.last_day:
        call ch30_day
        $ mas_globals.last_day = now_check.day


    if now_check.hour != mas_globals.last_hour:
        call ch30_hour
        $ mas_globals.last_hour = now_check.hour


    $ time_since_check = now_check - mas_globals.last_minute_dt
    if now_check.minute != mas_globals.last_minute_dt.minute or time_since_check.total_seconds() >= 60:
        call ch30_minute (time_since_check)
        $ mas_globals.last_minute_dt = now_check



label ch30_post_mid_loop_eval:


    call call_next_event from _call_call_next_event_1


    if not mas_globals.in_idle_mode:
        if not mas_HKIsEnabled():
            $ mas_HKDropShield()
        if not mas_HKBIsEnabled():
            $ mas_HKBDropShield()



    $ MASEventList.clear_current()


    if not _return:

        window hide(config.window_hide_transition)


        if (
            store.mas_globals.show_lightning
            and renpy.random.randint(1, store.mas_globals.lightning_chance) == 1
        ):
            $ light_zorder = MAS_BACKGROUND_Z - 1
            if (
                (mas_egg_manager.sayori_enabled() or (store.mas_globals.show_sayori_lightning and not persistent._mas_pm_cares_about_dokis))
                and mas_current_background.background_id == store.mas_background.MBG_DEF
                and renpy.random.randint(1, store.mas_globals.sayori_lightning_chance) == 1
            ):
                $ renpy.show("mas_lightning_s", zorder=light_zorder)
            else:
                $ renpy.show("mas_lightning", zorder=light_zorder)

            $ pause(0.1)
            play backsound "mod_assets/sounds/amb/thunder.wav"





        $ mas_randchat.wait()

        if not mas_randchat.waitedLongEnough():
            jump post_pick_random_topic
        else:
            $ mas_randchat.setWaitingTime()

        window auto










        if (
            store.mas_globals.in_idle_mode
            or (
                mas_globals.event_unpause_dt is not None
                and mas_globals.event_unpause_dt > datetime.datetime.utcnow()
            )
        ):
            jump post_pick_random_topic



        label pick_random_topic:


            if not persistent._mas_enable_random_repeats:
                jump mas_ch30_select_unseen


            $ chance = random.randint(1, 100)

            if chance <= store.mas_topics.UNSEEN:

                jump mas_ch30_select_unseen

            elif chance <= store.mas_topics.SEEN:

                jump mas_ch30_select_seen


            jump mas_ch30_select_mostseen




label post_pick_random_topic:

    $ _return = None

    jump ch30_loop


label mas_ch30_select_unseen:


    if len(mas_rev_unseen) == 0:

        if not persistent._mas_enable_random_repeats:

            if mas_timePastSince(mas_getEVL_last_seen("mas_random_limit_reached"), datetime.timedelta(weeks=2)):
                $ MASEventList.push("mas_random_limit_reached")

            jump post_pick_random_topic


        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_unseen)

    jump post_pick_random_topic


label mas_ch30_select_seen:


    if len(mas_rev_seen) == 0:

        $ mas_rev_seen, mas_rev_mostseen = mas_buildSeenEventLists()

        if len(mas_rev_seen) == 0:
            if len(mas_rev_mostseen) > 0:

                jump mas_ch30_select_mostseen


            if (
                len(mas_rev_mostseen) == 0
                and mas_timePastSince(mas_getEVL_last_seen("mas_random_limit_reached"), datetime.timedelta(days=1))
            ):
                $ MASEventList.push("mas_random_limit_reached")
                jump post_pick_random_topic


            jump post_pick_random_topic

    $ mas_randomSelectAndPush(mas_rev_seen)

    jump post_pick_random_topic


label mas_ch30_select_mostseen:


    if len(mas_rev_mostseen) == 0:
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_mostseen)

    jump post_pick_random_topic




label ch30_end:
    jump ch30_main




label ch30_minute(time_since_check):
    python:


        mas_checkAffection()


        mas_checkApologies()


        Event.checkEvents(evhand.event_database, rebuild_ev=False)


        mas_runDelayedActions(MAS_FC_IDLE_ROUTINE)


        mas_checkReactions()


        mas_seasonalCheck()


        mas_clearNotifs()


        mas_checkForWindowReacts()


        if mas_idle_mailbox.get_rebuild_msg():
            mas_rebuildEventLists()


        _mas_AffSave()


        mas_songs.checkRandSongDelegate()


        renpy.save_persistent()

    return





label ch30_hour:
    python:
        mas_runDelayedActions(MAS_FC_IDLE_HOUR)


        MASConsumable._checkConsumables()


        now_t = datetime.datetime.now().time()
        if mas_isNtoSS(now_t) or mas_isSStoMN(now_t):
            monika_chr._set_ahoge(None)


        store.mas_xp.grant()


        mas_setTODVars()


        with MAS_EVL("monika_holdrequest") as holdme_ev:
            
            if holdme_ev.allflags(EV_FLAG_HFRS):
                chance = max(mas_getSessionLength().total_seconds() / (4*3600.0), 0.2)
                if chance >= 1 or random.random() < chance:
                    holdme_ev.unflag(EV_FLAG_HFRS)

    return




label ch30_day:
    python:

        MASUndoActionRule.check_persistent_rules()

        MASStripDatesRule.check_persistent_rules(persistent._mas_strip_dates_rules)



        persistent._mas_filereacts_gift_aff_gained = 0
        persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


        mas_ret_long_absence = False


        mas_runDelayedActions(MAS_FC_IDLE_DAY)

        if mas_isMonikaBirthday():
            persistent._mas_bday_opened_game = True


        if (
            persistent._mas_filereacts_reacted_map
            and mas_pastOneDay(persistent._mas_filereacts_last_reacted_date)
        ):
            persistent._mas_filereacts_reacted_map = dict()


        if (
            not persistent._mas_d25_intro_seen
            and mas_isD25Outfit()
            and mas_isMoniUpset(lower=True)
        ):
            persistent._mas_d25_started_upset = True


        store.mas_island_event.advance_progression()


        mas_affection._withdraw_aff()


        if store.mas_can_import.certifi():
            store.mas_can_import.certifi.ch30_day_cert_update()

    return



label ch30_reset:





    $ store.mas_reset.final()

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
