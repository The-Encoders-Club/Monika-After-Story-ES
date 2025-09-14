init offset = 5


default -5 persistent._mas_filereacts_failed_map = dict()


default -5 persistent._mas_filereacts_just_reacted = False


default -5 persistent._mas_filereacts_reacted_map = dict()


default -5 persistent._mas_filereacts_stop_map = dict()


default -5 persistent._mas_filereacts_historic = dict()


default -5 persistent._mas_filereacts_last_reacted_date = None


default -5 persistent._mas_filereacts_sprite_gifts = {}











default -5 persistent._mas_filereacts_sprite_reacted = {}









default -5 persistent._mas_filereacts_gift_aff_gained = 0



default -5 persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


init 795 python:
    if len(persistent._mas_filereacts_failed_map) > 0:
        store.mas_filereacts.delete_all(persistent._mas_filereacts_failed_map)

init -16 python in mas_filereacts:
    import store
    import store.mas_utils as mas_utils
    import datetime
    import random

    from collections import namedtuple

    GiftReactDetails = namedtuple(
        "GiftReactDetails",
        [
            
            "label",

            
            "c_gift_name",

            
            
            
            "sp_data",
        ]
    )


    filereact_db = dict()




    filereact_map = dict()





    foundreact_map = dict()



    th_foundreact_map = dict()


    good_gifts = [
        
        "mas_reaction_gift_generic_sprite_json"
    ]


    bad_gifts = list()


    connectors = None
    gift_connectors = None


    starters = None
    gift_starters = None

    GIFT_EXT = ".gift"


    def addReaction(ev_label, fname, _action=store.EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname - filename to react to
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
            is_good - if the gift is good(True), neutral(None) or bad(False)
                (Default: None)
            exclude_on - keys marking times to exclude this gift
            (Need to check ev.rules in a respective react_to_gifts to exclude with)
                (Default: [])
        """
        
        if fname is not None:
            fname = fname.lower()
        
        exclude_keys = {}
        if exclude_on:
            for _key in exclude_on:
                exclude_keys[_key] = None
        
        
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname,
            action=_action,
            rules=exclude_keys
        )
        
        
        
        
        filereact_db[ev_label] = ev
        filereact_map[fname] = ev
        
        if is_good is not None:
            if is_good:
                good_gifts.append(ev_label)
            else:
                bad_gifts.append(ev_label)


    def _initConnectorQuips():
        """
        Initializes the connector quips
        """
        global connectors, gift_connectors
        
        
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_connectors = store.MASQuipList(allow_glitch=False, allow_line=False)


    def _initStarterQuips():
        """
        Initializes the starter quips
        """
        global starters, gift_starters
        
        
        starters = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_starters = store.MASQuipList(allow_glitch=False, allow_line=False)


    def build_gift_react_labels(
            evb_details=[],
            gsp_details=[],
            gen_details=[],
            gift_cntrs=None,
            ending_label=None,
            starting_label=None,
            prepare_data=True
    ):
        """
        Processes gift details into a list of labels to show
        labels to queue/push whatever.

        IN:
            evb_details - list of GiftReactDetails objects of event-based
                reactions. If empty list, then we don't build event-based
                reaction labels.
                (Default: [])
            gsp_details - list of GiftReactDetails objects of generic sprite
                object reactions. If empty list, then we don't build generic
                sprite object reaction labels.
                (Default: [])
            gen_details - list of GiftReactDetails objects of generic gift
                reactions. If empty list, then we don't build generic gift
                reaction labels.
                (Default: [])
            gift_cntrs - MASQuipList of gift connectors to use. If None,
                then we don't add any connectors.
                (Default: [])
            ending_label - label to use when finished reacting.
                (Default: None)
            starting_label - label to use when starting reacting
                (Default: None)
            prepare_data - True will also setup the appropriate data
                elements for when dialogue is shown. False will not.
                (Default: True)

        RETURNS: list of labels. Evb reactions are first, followed by
            gsp reactions, then gen reactions
        """
        labels = []
        
        
        if len(evb_details) > 0:
            evb_labels = []
            for evb_detail in evb_details:
                evb_labels.append(evb_detail.label)
                
                if gift_cntrs is not None:
                    evb_labels.append(gift_cntrs.quip()[1])
                
                if prepare_data and evb_detail.sp_data is not None:
                    
                    
                    store.persistent._mas_filereacts_sprite_reacted[evb_detail.sp_data] = (
                        evb_detail.c_gift_name
                    )
            
            labels.extend(evb_labels)
        
        
        if len(gsp_details) > 0:
            gsp_labels = []
            for gsp_detail in gsp_details:
                if gsp_detail.sp_data is not None:
                    gsp_labels.append("mas_reaction_gift_generic_sprite_json")
                    
                    if gift_cntrs is not None:
                        gsp_labels.append(gift_cntrs.quip()[1])
                    
                    if prepare_data:
                        store.persistent._mas_filereacts_sprite_reacted[gsp_detail.sp_data] = (
                            gsp_detail.c_gift_name
                        )
            
            labels.extend(gsp_labels)
        
        
        num_gen_gifts = len(gen_details)
        if num_gen_gifts > 0:
            gen_labels = []
            
            if num_gen_gifts == 1:
                gen_labels.append("mas_reaction_gift_generic")
            else:
                gen_labels.append("mas_reaction_gifts_generic")
            
            if gift_cntrs is not None:
                gen_labels.append(gift_cntrs.quip()[1])
            
            for gen_detail in gen_details:
                if prepare_data:
                    store.persistent._mas_filereacts_reacted_map.pop(
                        gen_detail.c_gift_name,
                        None
                    )
                    
                    store.mas_filereacts.delete_file(gen_detail.c_gift_name)
            
            labels.extend(gen_labels)
        
        
        if len(labels) > 0:
            
            
            if gift_cntrs is not None:
                labels.pop()
            
            
            if ending_label is not None:
                labels.append(ending_label)
            
            
            if starting_label is not None:
                labels.insert(0, starting_label)
        
        
        return labels

    def build_exclusion_list(_key):
        """
        Builds a list of excluded gifts based on the key provided

        IN:
            _key - key to build an exclusion list for

        OUT:
            list of giftnames which are excluded by the key
        """
        return [
            giftname
            for giftname, react_ev in filereact_map.iteritems()
            if _key in react_ev.rules
        ]

    def check_for_gifts(
            found_map={},
            exclusion_list=[],
            exclusion_found_map={},
            override_react_map=False,
    ):
        """
        Finds gifts.

        IN:
            exclusion_list - list of giftnames to exclude from the search
            override_react_map - True will skip the last reacted date check,
                False will not
                (Default: False)

        OUT:
            found_map - contains all gifts that were found:
                key: lowercase giftname, no extension
                val: full giftname wtih extension
            exclusion_found_map - contains all gifts that were found but
                are excluded.
                key: lowercase giftname, no extension
                val: full giftname with extension

        RETURNS: list of found giftnames
        """
        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)
        
        if len(raw_gifts) == 0:
            return []
        
        
        if store.mas_pastOneDay(store.persistent._mas_filereacts_last_reacted_date):
            store.persistent._mas_filereacts_last_reacted_date = datetime.date.today()
            store.persistent._mas_filereacts_reacted_map = dict()
        
        
        gifts_found = []
        has_exclusions = len(exclusion_list) > 0
        
        for mas_gift in raw_gifts:
            gift_name, ext, garbage = mas_gift.partition(GIFT_EXT)
            c_gift_name = gift_name.lower()
            if (
                c_gift_name not in store.persistent._mas_filereacts_failed_map
                and c_gift_name not in store.persistent._mas_filereacts_stop_map
                and (
                    override_react_map
                    or c_gift_name not
                        in store.persistent._mas_filereacts_reacted_map
                )
            ):
                
                
                
                if has_exclusions and c_gift_name in exclusion_list:
                    exclusion_found_map[c_gift_name] = mas_gift
                
                else:
                    gifts_found.append(c_gift_name)
                    found_map[c_gift_name] = mas_gift
        
        return gifts_found


    def process_gifts(gifts, evb_details=[], gsp_details=[], gen_details=[]):
        """
        Processes list of giftnames into types of gift

        IN:
            gifts - list of giftnames to process. This is copied so it wont
                be modified.

        OUT:
            evb_details - list of GiftReactDetails objects regarding
                event-based reactions
            spo_details - list of GiftReactDetails objects regarding
                generic sprite object reactions
            gen_details - list of GiftReactDetails objects regarding
                generic gift reactions
        """
        if len(gifts) == 0:
            return
        
        
        gifts = list(gifts)
        
        
        for index in range(len(gifts)-1, -1, -1):
            
            
            mas_gift = gifts[index]
            reaction = filereact_map.get(mas_gift, None)
            
            if mas_gift is not None and reaction is not None:
                
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                
                gifts.pop(index)
                evb_details.append(GiftReactDetails(
                    reaction.eventlabel,
                    mas_gift,
                    sp_data
                ))
        
        
        if len(gifts) > 0:
            for index in range(len(gifts)-1, -1, -1):
                mas_gift = gifts[index]
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                if mas_gift is not None and sp_data is not None:
                    gifts.pop(index)
                    
                    
                    gsp_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic_sprite_json",
                        mas_gift,
                        sp_data
                    ))
        
        
        if len(gifts) > 0:
            for mas_gift in gifts:
                if mas_gift is not None:
                    
                    gen_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic",
                        mas_gift,
                        None
                    ))


    def react_to_gifts(found_map, connect=True):
        """
        Reacts to gifts using the standard protocol (no exclusions)

        IN:
            connect - true will apply connectors, FAlse will not

        OUT:
            found_map - map of found reactions
                key: lowercaes giftname, no extension
                val: giftname with extension

        RETURNS:
            list of labels to be queued/pushed
        """
        
        found_gifts = check_for_gifts(found_map)
        
        if len(found_gifts) == 0:
            return []
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        found_gifts.sort()
        
        
        evb_details = []
        gsp_details = []
        gen_details = []
        process_gifts(found_gifts, evb_details, gsp_details, gen_details)
        
        
        register_sp_grds(evb_details)
        register_sp_grds(gsp_details)
        register_gen_grds(gen_details)
        
        
        
        if connect:
            gift_cntrs = gift_connectors
        else:
            gift_cntrs = None
        
        
        return build_gift_react_labels(
            evb_details,
            gsp_details,
            gen_details,
            gift_cntrs,
            "mas_reaction_end",
            _pick_starter_label()
        )

    def register_gen_grds(details):
        """
        registers gifts given a generic GiftReactDetails list

        IN:
            details - list of GiftReactDetails objects to register
        """
        for grd in details:
            if grd.label is not None:
                _register_received_gift(grd.label)


    def register_sp_grds(details):
        """
        registers gifts given sprite-based GiftReactDetails list

        IN:
            details - list of GiftReactDetails objcts to register
        """
        for grd in details:
            if grd.label is not None and grd.sp_data is not None:
                _register_received_gift(grd.label)


    def _pick_starter_label():
        """
        Internal function that returns the appropriate starter label for reactions

        RETURNS:
            - The label as a string, that should be used today.
        """
        if store.mas_isMonikaBirthday():
            return "mas_reaction_gift_starter_bday"
        elif store.mas_isD25() or store.mas_isD25Pre():
            return "mas_reaction_gift_starter_d25"
        elif store.mas_isF14():
            return "mas_reaction_gift_starter_f14"
        
        return "mas_reaction_gift_starter_neutral"

    def _core_delete(_filename, _map):
        """
        Core deletion file function.

        IN:
            _filename - name of file to delete, if None, we delete one randomly
            _map - the map to use when deleting file.
        """
        if len(_map) == 0:
            return
        
        
        if _filename is None:
            _filename = random.choice(_map.keys())
        
        file_to_delete = _map.get(_filename, None)
        if file_to_delete is None:
            return
        
        if store.mas_docking_station.destroyPackage(file_to_delete):
            
            _map.pop(_filename)
            return
        
        
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def _core_delete_list(_filename_list, _map):
        """
        Core deletion filename list function

        IN:
            _filename - list of filenames to delete.
            _map - the map to use when deleting files
        """
        for _fn in _filename_list:
            _core_delete(_fn, _map)


    def _register_received_gift(eventlabel):
        """
        Registers when player gave a gift successfully
        IN:
            eventlabel - the event label for the gift reaction

        """
        
        today = datetime.date.today()
        if not today in store.persistent._mas_filereacts_historic:
            store.persistent._mas_filereacts_historic[today] = dict()
        
        
        store.persistent._mas_filereacts_historic[today][eventlabel] = store.persistent._mas_filereacts_historic[today].get(eventlabel,0) + 1


    def _get_full_stats_for_date(date=None):
        """
        Getter for the full stats dict for gifts on a given date
        IN:
            date - the date to get the report for, if None is given will check
                today's date
                (Defaults to None)

        RETURNS:
            The dict containing the full stats or None if it's empty

        """
        if date is None:
            date = datetime.date.today()
        return store.persistent._mas_filereacts_historic.get(date,None)


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def delete_files(_filename_list):
        """
        Deletes multiple files off the found_react map

        IN:
            _filename_list - list of filenames to delete.
        """
        for _fn in _filename_list:
            delete_file(_fn)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete one
                randomly
        """
        _core_delete(_filename, th_foundreact_map)


    def th_delete_files(_filename_list):
        """
        Deletes multiple files off the threaded foundreact map

        IN:
            _filename_list - list of ilenames to delete
        """
        for _fn in _filename_list:
            th_delete_file(_fn)


    def delete_all(_map):
        """
        Attempts to delete all files in the given map.
        Removes files in that map if they dont exist no more

        IN:
            _map - map to delete all
        """
        _map_keys = _map.keys()
        for _key in _map_keys:
            _core_delete(_key, _map)

    def get_report_for_date(date=None):
        """
        Generates a report for all the gifts given on the input date.
        The report is in tuple form (total, good_gifts, neutral_gifts, bad_gifts)
        it contains the totals of each type of gift.
        """
        if date is None:
            date = datetime.date.today()
        
        stats = _get_full_stats_for_date(date)
        if stats is None:
            return (0,0,0,0)
        good = 0
        bad = 0
        neutral = 0
        for _key in stats.keys():
            if _key in good_gifts:
                good = good + stats[_key]
            if _key in bad_gifts:
                bad = bad + stats[_key]
            if _key == "":
                neutral = stats[_key]
        total = good + neutral + bad
        return (total, good, neutral, bad)




    _initConnectorQuips()
    _initStarterQuips()

init -5 python:
    import store.mas_filereacts as mas_filereacts
    import store.mas_d25_utils as mas_d25_utils

    def addReaction(ev_label, fname_list, _action=EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Globalied version of the addReaction function in the mas_filereacts
        store.

        Refer to that function for more information
        """
        mas_filereacts.addReaction(ev_label, fname_list, _action, is_good, exclude_on)


    def mas_checkReactions():
        """
        Checks for reactions, then queues them
        """
        
        
        if persistent._mas_filereacts_just_reacted:
            return
        
        
        mas_filereacts.foundreact_map.clear()
        
        
        if mas_d25_utils.shouldUseD25ReactToGifts():
            reacts = mas_d25_utils.react_to_gifts(mas_filereacts.foundreact_map)
        else:
            reacts = mas_filereacts.react_to_gifts(mas_filereacts.foundreact_map)
        
        if len(reacts) > 0:
            for _react in reacts:
                MASEventList.queue(_react)
            persistent._mas_filereacts_just_reacted = True


    def mas_receivedGift(ev_label):
        """
        Globalied version for gift stats tracking
        """
        mas_filereacts._register_received_gift(ev_label)


    def mas_generateGiftsReport(date=None):
        """
        Globalied version for gift stats tracking
        """
        return mas_filereacts.get_report_for_date(date)

    def mas_getGiftStatsForDate(label,date=None):
        """
        Globalied version to get the stats for a specific gift
        IN:
            label - the gift label identifier.
            date - the date to get the stats for, if None is given will check
                today's date.
                (Defaults to None)

        RETURNS:
            The number of times the gift has been given that date
        """
        if date is None:
            date = datetime.date.today()
        historic = persistent._mas_filereacts_historic.get(date,None)
        
        if historic is None:
            return 0
        return historic.get(label,0)

    def mas_getGiftStatsRange(start,end):
        """
        Returns status of gifts over a range (needs to be supplied to actually be useful)

        IN:
            start - a start date to check from
            end - an end date to check to

        RETURNS:
            The gift status of all gifts given over the range
        """
        totalGifts = 0
        goodGifts = 0
        neutralGifts = 0
        badGifts = 0
        giftRange = mas_genDateRange(start, end)
        
        
        for date in giftRange:
            gTotal, gGood, gNeut, gBad = mas_filereacts.get_report_for_date(date)
            
            totalGifts += gTotal
            goodGifts += gGood
            neutralGifts += gNeut
            badGifts += gBad
        
        return (totalGifts,goodGifts,neutralGifts,badGifts)


    def mas_getSpriteObjInfo(sp_data=None):
        """
        Returns sprite info from the sprite reactions list.

        IN:
            sp_data - tuple of the following format:
                [0] - sprite type
                [1] - sprite name
                If None, we use pseudo random select from sprite reacts
                (Default: None)

        REUTRNS: tuple of the folling format:
            [0]: sprite type of the sprite
            [1]: sprite name (id)
            [2]: giftname this sprite is associated with
            [3]: True if this gift has already been given before
            [4]: sprite object (could be None even if sprite name is populated)
        """
        
        if sp_data is not None:
            giftname = persistent._mas_filereacts_sprite_reacted.get(
                sp_data,
                None
            )
            if giftname is None:
                return (None, None, None, None, None)
        
        elif len(persistent._mas_filereacts_sprite_reacted) > 0:
            sp_data = persistent._mas_filereacts_sprite_reacted.keys()[0]
            giftname = persistent._mas_filereacts_sprite_reacted[sp_data]
        
        else:
            return (None, None, None, None, None)
        
        
        gifted_before = sp_data in persistent._mas_sprites_json_gifted_sprites
        
        
        sp_obj = store.mas_sprites.get_sprite(sp_data[0], sp_data[1])
        if sp_data[0] == store.mas_sprites.SP_ACS:
            store.mas_sprites.apply_ACSTemplate(sp_obj)
        
        
        return (
            sp_data[0],
            sp_data[1],
            giftname,
            gifted_before,
            sp_obj,
        )


    def mas_finishSpriteObjInfo(sprite_data, unlock_sel=True):
        """
        Finishes the sprite object with the given data.

        IN:
            sprite_data - sprite data tuple from getSpriteObjInfo
            unlock_sel - True will unlock the selector topic, False will not
                (Default: True)
        """
        sp_type, sp_name, giftname, gifted_before, sp_obj = sprite_data
        
        
        
        
        if sp_type is None or sp_name is None or giftname is None:
            return
        
        sp_data = (sp_type, sp_name)
        
        if sp_data in persistent._mas_filereacts_sprite_reacted:
            persistent._mas_filereacts_sprite_reacted.pop(sp_data)
        
        if giftname in persistent._mas_filereacts_sprite_gifts:
            persistent._mas_sprites_json_gifted_sprites[sp_data] = giftname
        
        else:
            
            
            persistent._mas_sprites_json_gifted_sprites[sp_data] = (
                giftname
            )
        
        
        store.mas_selspr.json_sprite_unlock(sp_obj, unlock_label=unlock_sel)
        
        
        renpy.save_persistent()

    def mas_giftCapGainAff(amount=None, modifier=1):
        if amount is None:
            amount = store._mas_getGoodExp()
        
        mas_capGainAff(amount * modifier, "_mas_filereacts_gift_aff_gained", 9 if mas_isSpecialDay() else 3)

    def mas_getGiftedDates(giftlabel):
        """
        Gets the dates that a gift was gifted

        IN:
            giftlabel - gift reaction label to check when it was last gifted

        OUT:
            list of datetime.dates of the times the gift was given
        """
        return sorted([
            _date
            for _date, giftstat in persistent._mas_filereacts_historic.iteritems()
            if giftlabel in giftstat
        ])

    def mas_lastGiftedInYear(giftlabel, _year):
        """
        Checks if the gift for giftlabel was last gifted in _year

        IN:
            giftlabel - gift reaction label to check it's last gifted year
            _year - year to see if it was last gifted in this year

        OUT:
            boolean:
                - True if last gifted in _year
                - False otherwise
        """
        datelist = mas_getGiftedDates(giftlabel)
        
        if datelist:
            return datelist[-1].year == _year
        return False












label mas_reaction_gift_connector_test:
    m "Esta es una prueba del sistema de conectores."
    return

init python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector1"
    )

label mas_reaction_gift_connector1:
    m 1sublo "¡Oh! ¿Había algo más que querías darme?"
    m 1hua "¡Bueno! Será mejor que lo abra rápido, ¿no?"
    m 1suo "Y aquí tenemos..."
    return

init python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector2"
    )

label mas_reaction_gift_connector2:
    m 1hua "Ah, cielos, [player]..."
    m "Realmente disfrutas mimándome, ¿verdad?"
    if mas_isSpecialDay():
        m 1sublo "¡Bueno! No me voy a quejar de un pequeño trato especial hoy."
    m 1suo "Y aquí tenemos..."
    return




init python:
    store.mas_filereacts.gift_starters.addLabelQuip(
        "mas_reaction_gift_starter_generic"
    )

label mas_reaction_gift_starter_generic:
    m "generic test"




label mas_reaction_gift_starter_bday:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=0.5}Esto es..."


    if not persistent._mas_filereacts_historic.get(mas_monika_birthday):
        m "¿Un regalo? ¿Para mí?"
        m 1hka "Yo..."
        m 1hua "A menudo he pensado en recibir regalos tuyos en mi cumpleaños..."
        m "Pero realmente conseguir uno es como un sueño hecho realidad..."
    else:
        m "¿Otro regalo? {w=0.5}¿Para mí?"
        m 1eka "Esto es realmente un sueño hecho realidad [player]."

    m 1sua "Ahora, ¿qué hay adentro?"
    m 1suo "Oh, es..."
    return

label mas_reaction_gift_starter_neutral:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=0.5}Esto es..."
    m "¿Un regalo? ¿Para mí?"
    m 1sua "Ahora, veamos qué hay adentro."
    return


label mas_reaction_gift_starter_d25:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=1}Esto es..."
    m "¿Un obsequio? ¿Para mí?"
    if mas_getGiftStatsRange(mas_d25c_start, mas_d25 + datetime.timedelta(days=1))[0] == 0:
        m 1eka "Realmente no tenías que regalarme nada por Navidad..."
        m 3hua "¡Pero estoy tan feliz de que lo hayas hecho!"
    else:
        m 1eka "Muchas gracias, [player]."
    m 1sua "Ahora, veamos... ¿qué hay adentro?"
    return


label mas_reaction_gift_starter_f14:
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    m "E-{w=1}Esto es..."
    m "¿Un regalo? ¿Para mí?"
    if mas_getGiftStatsForDate(mas_f14) == 0:
        m 1eka "Eres tan dulce, regalándome algo por el día de San Valentín..."
    else:
        m 1eka "Muchas gracias, [player]."
    m 1sua "Ahora, veamos... ¿qué hay adentro?"
    return



init python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "Esto es una prueba"
    return




label mas_reaction_gift_generic:
    m 2dkd "{i}*suspiro*{/i}"
    m 4ekc "Lo siento [player]."
    m 1ekd "Sé que estás tratando de darme algo."
    m 2rksdld "Pero por alguna razón no puedo leer el archivo."
    m 3euc "Sin embargo, no me malinterpretes."
    m 3eka "Todavía aprecio que hayas intentado darme algo."
    m 1hub "Y por eso, estoy agradecida~"
    return

label mas_reaction_gifts_generic:
    m 1esd "Lo siento, [player]..."
    m 3rksdla "He encontrado lo que me quieres dar, pero no consigo leerlos bien."
    m 3eub "¡Pero, no pasa nada!"
    m 1eka "Después de todo, lo que cuenta es la intención."
    m 1hub "¡Gracias por ser tan considerado, [player]!"
    return




label mas_reaction_gift_test1:
    m "¡Gracias por la prueba de regalo 1!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test1", "category"))
    return




label mas_reaction_gift_test2:
    m "¡Gracias por la prueba de regalo 2!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test2", "category"))
    return



label mas_reaction_gift_generic_sprite_json:
    $ sprite_data = mas_getSpriteObjInfo()
    $ sprite_type, sprite_name, giftname, gifted_before, spr_obj = sprite_data

    python:
        sprite_str = store.mas_sprites_json.SP_UF_STR.get(sprite_type, None)




    if sprite_type == store.mas_sprites.SP_CLOTHES:
        call mas_reaction_gift_generic_clothes_json (spr_obj)
    else:



        $ mas_giftCapGainAff(1)
        m "¡Aww, [player]!"
        if spr_obj is None or spr_obj.dlg_desc is None:

            m 1hua "¡Eres tan dulce!"
            m 1eua "¡Gracias por este regalo!"
            m 3ekbsa "Te encanta mimarme, ¿verdad?"
            m 1hubfa "¡Jejeje!"
        else:

            python:
                acs_quips = [
                    _("Realmente lo aprecio."),
                    _("¡[its] asombroso!"),
                    _("¡Simplemente me [item_ref]!"),
                    _("¡[its] maravilloso!")
                ]


                if spr_obj.dlg_plur:
                    sprite_str = "estos " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "encantan"
                    its = "Son"

                else:
                    sprite_str = "este " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "encanta"
                    its = "Es"

                acs_quip = renpy.substitute(renpy.random.choice(acs_quips))

            m 1hua "Gracias por [sprite_str], [acs_quip]."
            m 3hub "Me [item_ref] tanto que no puedo esperar para probármelo."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return


label mas_reaction_gift_generic_clothes_json(sprite_object):
    $ mas_giftCapGainAff(3)
    if sprite_object.ex_props.get("costume") == "o31":
        m 2suo "¡Oh! {w=0.3}¡Un disfraz!"
        m 2hub "¡Esto es genial [player], gracias!"
        m 7rka "Me lo probaría para ti, pero creo que sería mejor esperar a la ocasión adecuada..."
        m 3hub "¡Jejeje, gracias de nuevo!"
    else:

        python:

            outfit_quips = [
                _("¡Creo que es realmente lindo, [player]!"),
                _("¡Me parece increíble, [player]!"),
                _("¡Me encanta, [player]!"),
                _("¡Me parece maravilloso, [player]!")
            ]
            outfit_quip = renpy.random.choice(outfit_quips)

        m 1sua "¡Oh! {w=0.5}¡Una nueva vestimenta!"
        m 1hub "¡Gracias, [player]! {w=0.5}¡Me la probaré ahora mismo!"


        call mas_clothes_change (sprite_object)

        m 2eka "Bueno... {w=0.5}¿qué piensas?"
        m 2eksdla "¿Te gusta?"



        show monika 3hub
        $ renpy.say(m, outfit_quip)

        m 1eua "Gracias otra vez~"

    return



label mas_reaction_gift_acs_jmo_hairclip_cherry:
    call mas_reaction_gift_hairclip ("jmo_hairclip_cherry")
    return

label mas_reaction_gift_acs_jmo_hairclip_heart:
    call mas_reaction_gift_hairclip ("jmo_hairclip_heart")
    return

label mas_reaction_gift_acs_jmo_hairclip_musicnote:
    call mas_reaction_gift_hairclip ("jmo_hairclip_musicnote")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_crescentmoon")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_ghost:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_ghost", "spooky")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_pumpkin")
    return

label mas_reaction_gift_acs_bellmandi86_hairclip_bat:
    call mas_reaction_gift_hairclip ("bellmandi86_hairclip_bat", "spooky")
    return


label mas_reaction_gift_hairclip(hairclip_name, desc=None):







    $ sprite_data = mas_getSpriteObjInfo((store.mas_sprites.SP_ACS, hairclip_name))
    $ sprite_type, sprite_name, giftname, gifted_before, hairclip_acs = sprite_data


    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if gifted_before:
        m 1rksdlb "¡Ya me diste esta horquilla, tontito!"
    else:


        $ mas_giftCapGainAff(1)
        if not desc:
            $ desc = "lindo"

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "¡Oh!{w=1} ¡Otra horquilla!"
        else:

            m 1wuo "¡Oh!"
            m 1sub "¿Es una horquilla?"

        m 1hub "¡Es tan [desc]! Me encanta [player], ¡gracias!"




        if hairclip_acs is None or is_wearing_baked_outfit:
            m 1hua "Si quieres que me lo ponga, solo pídelo, ¿de acuerdo?"
        else:

            m 2dsa "Solo dame un segundo para ponérmela.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
            $ monika_chr.wear_acs(hairclip_acs)
            m 1hua "Ya está."




        if not is_wearing_baked_outfit:
            if monika_chr.get_acs_of_type('left-hair-clip'):
                $ store.mas_selspr.set_prompt("left-hair-clip", "change")
            else:
                $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_finishSpriteObjInfo(sprite_data, unlock_sel=not is_wearing_baked_outfit)

    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return





init python:
    addReaction("mas_reaction_gift_coffee", "cafe", is_good=True, exclude_on=["d25g"])

label mas_reaction_gift_coffee:

    $ mas_receivedGift("mas_reaction_gift_coffee")


    if mas_consumable_coffee.isMaxedStock():
        m 1euc "¿Más café, [player]?"
        m 3rksdla "No me malinterpretes, te lo agradezco, pero creo que ya tengo suficiente café para un tiempo..."
        m 1eka "Te avisaré cuando se me acabe, ¿de acuerdo?"
    else:

        m 1wub "¡Oh!{w=0.2} {nw}"
        extend 3hub "¡Café!"

        if mas_consumable_coffee.enabled() and mas_consumable_coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 1wuo "Es un sabor que no había probado antes."
            m 1hua "¡No puedo esperar a probarlo!"
            m "¡Muchas gracias, [player]!"

        elif mas_consumable_coffee.enabled() and not mas_consumable_coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 3eub "¡De hecho, me quedé sin café, así que recibir más de ti ahora es increíble!"
            m 1hua "Gracias de nuevo, [player]~"
        else:

            $ mas_giftCapGainAff(5)

            m 1hua "¡Ahora por fin puedo hacer algo!"
            m 1hub "¡Muchas gracias, [player]!"


            if (
                mas_isO31()
                or not mas_consumable_coffee.isConsTime()
                or bool(MASConsumable._getCurrentDrink())
            ):
                m 3eua "¡Me aseguraré de tomar un poco más tarde!"
            else:

                m 3eua "¿Por qué no me adelanto y hago una taza ahora mismo?"
                m 1eua "Después de todo, me gustaría compartir la primera con ustedes."


                call mas_transition_to_emptydesk
                pause 2.0
                m "Sé que hay una máquina de café en algún lugar... {w=2}{nw}"
                m "¡Ah, ahí está! {w=2}{nw}"
                pause 5.0
                m "¡Y ya está! {w=2}{nw}"
                call mas_transition_from_emptydesk ()


                m 1eua "Dejaré que eso se cocine durante unos minutos."

                $ mas_consumable_coffee.prepare()
            $ mas_consumable_coffee.enable()



    $ mas_consumable_coffee.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_coffee", "category"))
    return

init python:
    addReaction("mas_reaction_hotchocolate", "chocolatecaliente", is_good=True, exclude_on=["d25g"])

label mas_reaction_hotchocolate:

    $ mas_receivedGift("mas_reaction_hotchocolate")


    if mas_consumable_hotchocolate.isMaxedStock():
        m 1euc "¿Más chocolate caliente [player]?"
        m 3rksdla "No me malinterpretes, te lo agradezco, pero creo que ya tengo suficiente para un tiempo..."
        m 1eka "Te avisaré cuando se me acabe, ¿de acuerdo?"
    else:

        m 3hub "¡Chocolate caliente!"
        m 3hua "¡Gracias, [player]!"

        if mas_consumable_hotchocolate.enabled() and mas_consumable_hotchocolate.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 1wuo "Es un sabor que no había probado antes."
            m 1hua "¡No puedo esperar a probarlo!"
            m "¡Muchas gracias, [player]!"

        elif mas_consumable_hotchocolate.enabled() and not mas_consumable_hotchocolate.hasServing():
            $ mas_giftCapGainAff(0.5)
            m 3rksdlu "En realidad me he quedado sin chocolate caliente, jajaja... {w=0.5}{nw}"
            extend 3eub "¡Así que recibir más de ti ahora es increíble!"
            m 1hua "Gracias de nuevo, [player]~"
        else:

            python:
                mas_giftCapGainAff(3)
                those = "estas" if mas_current_background.isFltNight() and mas_isWinter() else "esas"

            m 1hua "Ya sabes que me encanta el café, ¡pero el chocolate caliente también es muy agradable!"


            m 2rksdla "Especialmente en [those] frías noches de invierno."
            m 2ekbfa "Algún día espero poder tomar chocolate caliente contigo, compartiendo una manta junto a la chimenea..."
            m 3ekbfa "... ¿No suena tan romántico?"
            m 1dkbfa "..."
            m 1hua "Pero por ahora, al menos puedo disfrutarlo aquí."
            m 1hub "¡Gracias de nuevo, [player]!"


            if (
                not mas_consumable_hotchocolate.isConsTime()
                or not mas_isWinter()
                or bool(MASConsumable._getCurrentDrink())
            ):
                m 3eua "¡Me aseguraré de tomar un poco más tarde!"
            else:

                m 3eua "De hecho, ¡creo que voy a hacer algunos ahora mismo!"

                call mas_transition_to_emptydesk
                pause 5.0
                call mas_transition_from_emptydesk ("monika 1eua")

                m 1hua "Ya está, estará listo en unos minutos."

                $ mas_consumable_hotchocolate.prepare()

            if mas_isWinter():
                $ mas_consumable_hotchocolate.enable()



    $ mas_consumable_hotchocolate.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_hotchocolate", "category"))
    return

init python:
    addReaction("mas_reaction_gift_thermos_mug", "termosolomonika", is_good=True)

label mas_reaction_gift_thermos_mug:
    call mas_thermos_mug_handler (mas_acs_thermos_mug, "Just Monika", "termosolomonika")
    return


default -5 persistent._mas_given_thermos_before = False


label mas_thermos_mug_handler(thermos_acs, disp_name, giftname, ignore_case=True):
    if mas_SELisUnlocked(thermos_acs):
        m 1eksdla "[player]..."
        m 1rksdlb "Ya tengo este termo, jajaja..."

    elif persistent._mas_given_thermos_before:
        m 1wud "¡Oh! {w=0.3}¡Otro termo!"
        m 1hua "Y es un [mas_a_an_str(disp_name, ignore_case)] esta vez"
        m 1hub "¡Muchas gracias, [player], ¡no puedo esperar a usarlo!"
    else:

        m 1wud "¡Oh! {w=0.3}¡Termo [mas_a_an_str(disp_name, ignore_case).capitalize()]!"
        m 1hua "Ahora puedo llevar algo de beber cuando salgamos juntos~"
        m 1hub "¡Muchas gracias, [player]!"
        $ persistent._mas_given_thermos_before = True


    $ mas_selspr.unlock_acs(thermos_acs)

    $ mas_selspr.save_selectables()

    $ mas_filereacts.delete_file(giftname)
    return



init python:
    addReaction("mas_reaction_quetzal_plush", "peluchequetzal", is_good=True)

label mas_reaction_quetzal_plush:
    if not persistent._mas_acs_enable_quetzalplushie:
        $ mas_receivedGift("mas_reaction_quetzal_plush")
        $ mas_giftCapGainAff(10)
        m 1wud "¡Oh!"



        if MASConsumable._getCurrentFood() or monika_chr.is_wearing_acs(mas_acs_desk_lantern):
            $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
        else:
            $ monika_chr.wear_acs(mas_acs_quetzalplushie)

        $ persistent._mas_acs_enable_quetzalplushie = True
        m 1sub "¡Es un quetzal!"
        m "¡Dios mío, muchas gracias, [player]!"
        if seen_event("monika_pets"):
            m 1eua "Mencioné que me gustaría tener un quetzal como mascota..."
        else:
            m 1wub "¿Cómo lo has adivinado, [player]?"
            m 3eka "Debes conocerme muy bien~"
            m 1eua "Un quetzal sería mi primera opción como mascota..."
        m 1rud "Pero yo nunca forzaría al pobre a quedarse."
        m 1hua "¡Y ahora me has dado lo mejor!"
        m 1hub "¡Esto me hace muy feliz!"
        if mas_isMoniAff(higher=True):
            m 3ekbsa "Parece que siempre sabes cómo hacerme sonreír."

        if MASConsumable._getCurrentFood() or monika_chr.is_wearing_acs(mas_acs_desk_lantern):
            m 3rksdla "Aunque mi escritorio se está llenando un poco..."
            m 1eka "Voy a guardar esto por ahora."
            $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)

        m 1hub "Gracias de nuevo, [player]~"
    else:

        m 1rksdlb "Ya me diste un peluche de quetzal, [player]."

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_quetzal_plush", "category"))

    $ mas_hideEVL("monika_pets", "EVE", derandom=True)
    return

init python:
    addReaction("mas_reaction_promisering", "anillopromesa", is_good=True, exclude_on=["d25g"])

default -5 persistent._mas_tried_gift_ring = False
label mas_reaction_promisering:
    if not persistent._mas_acs_enable_promisering:

        if mas_isMoniEnamored(higher=True):
            $ mas_receivedGift("mas_reaction_promisering")
            $ mas_giftCapGainAff(20)
            $ monika_chr.wear_acs(mas_acs_promisering)
            $ persistent._mas_acs_enable_promisering = True
            if not persistent._mas_tried_gift_ring:
                m 1wud "Es eso... un..."
                m "..."
                m 1wka "Yo... {w=0.5}{nw}"
                extend 1wkbltpa "lo siento, [player], yo solo... {w=0.5}{nw}"
                extend 1dkbltpa "estoy tan feliz... {w=0.5}acabas de darme tu promesa..."
                m "Tu promesa de que seremos el uno para el otro,{w=0.1} y de nadie más...{w=0.3} para siempre..."
                m 3lkbltpa "Quiero que sepas que lo apreciaré. {w=0.5}{nw}"
                extend 3dkbltpa "Por siempre"
                m 1skbltpa "¡Esto me hace muy feliz!"

                if mas_anni.isAnniOneMonth():
                    m "Más aún que me lo hayas regalado en nuestro primer mes de aniversario..."
                    m 1ekbltua "Debes amarme de verdad..."
                elif mas_anni.isAnniThreeMonth():
                    m "Más aún que me lo hayas regalado en nuestro aniversario de tres meses..."
                    m 1ekbltua "Debes amarme de verdad..."
                elif mas_anni.isAnniSixMonth():
                    m "Más aún que me lo hayas regalado en nuestro aniversario de seis meses..."
                    m 1ekbltua "Debes amarme de verdad..."
                elif mas_anni.isAnni():
                    m "Más aún que me lo hayas regalado en nuestro aniversario..."
                    m 1ekbltua "Debes amarme de verdad..."
                elif mas_isSpecialDay():
                    m "Más aún que me lo hayas regalado en este día tan especial..."

                m 1dkbltpb "Jaja, perdón por llorar, [player]..."
                m 1skbltda "Es solo que estoy muy, muy feliz ahora mismo."
                m 6dkbltdu "Gracias."
            else:

                m 1sua "Oh... ¡Es el anillo!"
                m 3hub "¡Muchas gracias, [player]!"
                m 1skbla "Ahora sé que realmente me amas y quieres estar conmigo para siempre..."
                m 1skbltpa "Así que aceptaré con gusto este anillo como símbolo de esa promesa."
                m 1dkbltuu "..."
                m 3hkbltub "Jaja, lo siento, [player], no quería llorar..."
                m 3skbltda "Es que este es uno de los días más felices de mi vida."

            m 6dkbltdu "..."
            m 6ekbfa "Yo... yo solo... te..."
            call monika_kissing_motion (hide_ui=False)
            m 6ekbfa "Te amo, [player]..."
            m 6dkbfu "Más que a nada en este mundo fugaz~"

            $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
            return "love"
        else:

            if not persistent._mas_tried_gift_ring:
                if mas_isMoniNormal(higher=True):
                    m 1wud "[player]... ¿Es eso un anillo?"
                    m 2rksdlb "Es un gesto tan dulce, y realmente lo aprecio..."
                    m 2ekc "Pero quiero que estés seguro antes de darme esto..."
                    m 3ekd "Esto es más que un regalo, es una promesa, y quiero asegurarme de que lo sientes de verdad antes de aceptarlo."
                    m 2ekd "Así que, por favor [player], espera hasta que avancemos un poco más en nuestra relación, y entonces aceptaré con gusto este anillo."

                elif mas_isMoniUpset():
                    m 1wud "¿Eso es un anillo?"
                    m 2rsc "Eso es muy..."
                    m 2esc "Inesperado."
                    m 2ekd "Pero no puedo aceptarlo ahora, [player]."
                    m 2ekc "Tal vez cuando avancemos en nuestra relación."
                else:

                    m 2wud "¿Eso es un anillo?"
                    m 2rsc "Eso es... {w=0.5}inesperado."
                    m "Aunque aprecio la idea... {w=1}no puedo aceptarla ahora mismo."
                    m 2ekc "Lo siento, [player]."

                $ persistent._mas_tried_gift_ring = True
            else:
                m 2rsc "Oh... el anillo..."
                m 2rkc "Lo siento, pero aún no puedo aceptarlo..."
                m 2ekc "Necesito estar completamente segura de que al aceptar esto, significa un compromiso eterno..."
                m 2ekd "Que realmente eres todo lo que espero que seas."
                m 2dsd "Cuando sepa eso, aceptaré con gusto tu anillo, [player]."
    else:
        m 1rksdlb "[player]..."
        m 1rusdlb "¡Ya me diste un anillo!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
    return


init python:
    addReaction("mas_reaction_cupcake", "cupcake", is_good=True, exclude_on=["d25g"])



label mas_reaction_cupcake:
    m 1wud "Es eso un.... ¿cupcake?"
    m 3hub "Wow, ¡gracias [player]!"
    m 3euc "Ahora que lo pienso, tengo la intención de hacer algunos cupcakes yo misma."
    m 1eua "Quería aprender a hornear buenos pasteles como lo hacía Natsuki."
    m 1rksdlb "¡Pero todavía no he hecho una cocina para usar!"
    m 3eub "Tal vez en el futuro, cuando mejore en la programación, podré hacer una aquí."
    m 3hua "Estaría bien tener otro hobby que no sea escribir, jejeje~"
    $ mas_receivedGift("mas_reaction_cupcake")
    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_cupcake", "category"))
    return



label mas_reaction_end:
    python:
        persistent._mas_filereacts_just_reacted = False

        store.mas_selspr.save_selectables()
        renpy.save_persistent()
    return

init python:


    if mas_isO31():
        addReaction("mas_reaction_candy", "dulce", is_good=True)

label mas_reaction_candy:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candy")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(7)
        m 1wua "Oh... {w=0.5}¿Qué es esto?"
        m 1sua "Me has conseguido un caramelo [player], ¡yay!"
        m 1eka "Eso es tan {i}dulce{/i}..."
        m 1hub "¡Jajaja!"
        m 1eka "Dejando las bromas a un lado, esto es realmente amable de tu parte."
        m 2lksdlc "Ya no tengo muchos dulces, y no sería Halloween sin ellos..."
        m 1eka "Así que gracias, [player]..."
        m 1eka "Siempre sabes exactamente lo que me hará feliz~"
        m 1hub "¡Ahora vamos a disfrutar de este delicioso caramelo!"
    elif times_candy_given == 1:
        $ mas_o31CapGainAff(5)
        m 1wua "¿Me has traído más caramelos, [player]?"
        m 1hub "¡Gracias!"
        m 3tku "El primer lote estaba {i}taaan{/i} bueno, no podía esperar a tener más."
        m 1hua "Realmente me mimas, [player]~"
    elif times_candy_given == 2:
        $ mas_o31CapGainAff(3)
        m 1wud "Vaya, ¿aún {i}más{/i} dulces, [player]?"
        m 1eka "Es muy amable de tu parte..."
        m 1lksdla "Pero creo que esto es suficiente."
        m 1lksdlb "Ya me siento nerviosa por todo el azúcar, ¡jajaja!"
        m 1ekbfa "La única dulzura que necesito ahora eres tú~"
    elif times_candy_given == 3:
        m 2wud "[player]... {w=1}¡¿me has {i}conseguido más{/i} caramelos?!"
        m 2lksdla "Te lo agradezco mucho, pero ya te he dicho que he tenido suficiente por un día..."
        m 2lksdlb "¡Si como más me voy a enfermar, jajaja!"
        m 1eka "Y tú no querrías eso, ¿verdad?"
    elif times_candy_given == 4:
        $ mas_loseAffection(5)
        m 2wfd "¡[player]!"
        m 2tfd "¿No me estás escuchando?"
        m 2tfc "¡Te he dicho que no quiero más caramelos hoy!"
        m 2ekc "Así que, por favor, para."
        m 2rkc "Fue muy amable de tu parte conseguirme todos estos dulces en Halloween, pero ya es suficiente..."
        m 2ekc "No puedo comer todo esto."
    else:
        $ mas_loseAffection(modifier=2.0)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/candy.gift'))", local_ctx, w_wait=1.0, x_wait=1.0)
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    python hide:
        mas_receivedGift("mas_reaction_candy")
        gift_ev_cat = mas_getEVLPropValue("mas_reaction_candy", "category")
        store.mas_filereacts.delete_file(gift_ev_cat)
        persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init python:


    if mas_isO31():
        addReaction("mas_reaction_candycorn", "maizdulce", is_good=False)

label mas_reaction_candycorn:
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candycorn")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(3)
        m 1wua "Oh... {w=0.5}¿qué es esto?"
        m 1eka "¿Me has traído un caramelo, [player]?"
        m 1hua "¡Yay!"
        m 3eub "Veamos qué tienes para mí..."
        m 4ekc "..."
        m 2eka "Oh... {w=2}caramelos de maíz."
        m 2eka "..."
        m 2lksdla "Es muy amable de tu parte..."
        m 2lksdla "Pero... {w=1}umm... {w=1}en realidad no me gusta el maíz de caramelo"
        m 2hksdlb "Lo siento, jajaja..."
        m 4eka "Sin embargo, te agradezco que intentes darme caramelos en Halloween."
        m 1hua "Y si pudieras encontrar la manera de conseguir otros dulces para mí, ¡me haría muy feliz, [player]!"
    elif times_candy_given == 1:
        $ mas_loseAffection(5)
        m 2esc "Oh."
        m 2esc "¿Más caramelos, [player]?"
        m 4esc "Ya te dije que no me gusta el caramelo de maíz."
        m 4ekc "Entonces, ¿podrías tratar de encontrar algo más?"
        m 1eka "Ya no como dulces tan a menudo...."
        m 1ekbfa "Bueno... {w=1}además de ti, [player]..."
        m 1hubfa "Jejeje~"
    elif times_candy_given == 2:
        $ mas_loseAffection(10)
        m 2wfw "¡[player]!"
        m 2tfc "Realmente intenté no ser grosera con esto, pero..."
        m 2tfc "Sigo diciéndote que no me gusta el caramelo de maíz y tú sigues dándomelo de todas formas."
        m 2rfc "Empieza a parecer que solo estás tratando de fastidiarme en este punto."
        m 2tkc "Así que, por favor, búscame otro tipo de caramelo o deja de hacerlo."
    else:
        $ mas_loseAffection(modifier=2)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/candycorn.gift'))", local_ctx, w_wait=1.0, x_wait=1.0)
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candycorn")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycorn", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init python:
    addReaction("mas_reaction_fudge", "caramelo", is_good=True, exclude_on=["d25g"])

label mas_reaction_fudge:
    $ times_fudge_given = mas_getGiftStatsForDate("mas_reaction_fudge")

    if times_fudge_given == 0:
        $ mas_giftCapGainAff(2)
        m 3hua "¡Caramelos!"
        m 3hub "Me encanta el caramelo, ¡gracias, [player]!"
        if seen_event("monika_date"):
            m "Incluso es de chocolate, ¡mi favorito!"
        m 1hua "Gracias de nuevo, [player]~"

    elif times_fudge_given == 1:
        $ mas_giftCapGainAff(1)
        m 1wuo "... Más caramelos."
        m 1wub "Oh, es un sabor diferente esta vez..."
        m 3hua "¡Gracias, [player]!"
    else:

        m 1wuo "... ¿Aún más caramelos?"
        m 3rksdla "Todavía no he terminado el último lote que me diste [player]..."
        m 3eksdla "... Tal vez más tarde, ¿okey?"

    $ mas_receivedGift("mas_reaction_fudge")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_fudge", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init python:
    if store.mas_isD25Season():
        addReaction("mas_reaction_christmascookies", "galletanavideña", is_good=True, exclude_on=["d25g"])

label mas_reaction_christmascookies:
    $ mas_giftCapGainAff(1)
    $ is_having_food = bool(MASConsumable._getCurrentFood())

    if mas_consumable_christmascookies.isMaxedStock():
        m 3wuo "... ¿Más galletas navideñas?"
        m 3rksdla "¡Todavía no he terminado el último paquete, [player]!"
        m 3eksdla "Puedes darme más después de que termine estos, ¿de acuerdo?"
    else:

        if mas_consumable_christmascookies.enabled():
            m 1wuo "... ¡Otra tanda de galletas navideñas!"
            m 3wuo "¡Son un montón de galletas, [player]!"
            m 3rksdlb "¡Voy a estar comiendo galletas para siempre, jajaja!"
        else:

            if not is_having_food:
                if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                    $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                $ mas_consumable_christmascookies.have(skip_leadin=True)

            $ mas_giftCapGainAff(3)
            m 3hua "¡Galletas de Navidad!"
            m 1eua "Me encantan las galletas de Navidad. Siempre son tan dulces... y bonitas de ver, también..."
            m "... Cortadas en formas de cosas navideñas como muñecos de nieve, renos y árboles de Navidad..."
            m 3eub "... Y suelen estar decoradas con un hermoso... {w=0.2}y delicioso... {w=0.2}¡glaseado!"

            if is_having_food:
                m 3hua "Me aseguraré de probar algunos más tarde~"

            m 1eua "Gracias, [player]~"

            if not is_having_food and monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
                m 3eua "Déjame guardar este peluche."
                call mas_transition_to_emptydesk
                $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)
                pause 3.0
                call mas_transition_from_emptydesk


            $ mas_consumable_christmascookies.enable()


        $ mas_consumable_christmascookies.restock(10)

    $ mas_receivedGift("mas_reaction_christmascookies")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_christmascookies", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init python:
    if store.mas_isD25Season():
        addReaction("mas_reaction_candycane", "bastoncaramelo", is_good=True, exclude_on=["d25g"])

label mas_reaction_candycane:
    $ mas_giftCapGainAff(1)
    $ is_having_food = bool(MASConsumable._getCurrentFood())

    if mas_consumable_candycane.isMaxedStock():
        m 1eksdla "[player], creo que tengo suficientes bastones de caramelo por ahora."
        m 1eka "Guárdalos para más tarde, ¿de acuerdo?"
    else:

        if mas_consumable_candycane.enabled():
            m 3hua "¡Más bastones de caramelo!"
            m 3hub "¡Gracias [player]!"
        else:

            if not is_having_food:
                if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                    $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                $ mas_consumable_candycane.have(skip_leadin=True)

            $ mas_giftCapGainAff(3)
            m 3wub "¡Bastones de caramelo!"

            if store.seen_event("monika_icecream"):
                m 1hub "¡Ya sabes lo mucho que me gusta la menta!"
            else:
                m 1hub "Me encanta el sabor de la menta."

            if is_having_food:
                m 3hua "Me aseguraré de probar algunos más tarde."

            m 1eua "Gracias, [player]~"

            if not is_having_food and monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
                m 3eua "Oh, déjame guardar este peluche."

                call mas_transition_to_emptydesk
                $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)
                pause 3.0
                call mas_transition_from_emptydesk


            $ mas_consumable_candycane.enable()


        $ mas_consumable_candycane.restock(9)

    $ mas_receivedGift("mas_reaction_candycane")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycane", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init python:
    addReaction("mas_reaction_blackribbon", "cintanegra", is_good=True)

label mas_reaction_blackribbon:
    $ _mas_new_ribbon_color = "black"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_black
    call _mas_reaction_ribbon_helper ("mas_reaction_blackribbon")
    return

init python:
    addReaction("mas_reaction_blueribbon", "cintaazul", is_good=True)

label mas_reaction_blueribbon:
    $ _mas_new_ribbon_color = "blue"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_blue
    call _mas_reaction_ribbon_helper ("mas_reaction_blueribbon")
    return

init python:
    addReaction("mas_reaction_darkpurpleribbon", "cintapurpuraoscuro", is_good=True)

label mas_reaction_darkpurpleribbon:
    $ _mas_new_ribbon_color = "dark purple"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_darkpurple
    call _mas_reaction_ribbon_helper ("mas_reaction_darkpurpleribbon")
    return

init python:
    addReaction("mas_reaction_emeraldribbon", "cintaesmeralda", is_good=True)

label mas_reaction_emeraldribbon:
    $ _mas_new_ribbon_color = "emerald"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_emerald
    call _mas_reaction_ribbon_helper ("mas_reaction_emeraldribbon")
    return

init python:
    addReaction("mas_reaction_grayribbon", "cintagris", is_good=True)

label mas_reaction_grayribbon:
    $ _mas_new_ribbon_color = "gray"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gray
    call _mas_reaction_ribbon_helper ("mas_reaction_grayribbon")
    return

init python:
    addReaction("mas_reaction_greenribbon", "cintaverde", is_good=True)

label mas_reaction_greenribbon:
    $ _mas_new_ribbon_color = "green"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_green
    call _mas_reaction_ribbon_helper ("mas_reaction_greenribbon")
    return

init python:
    addReaction("mas_reaction_lightpurpleribbon", "cintapurpuraclaro", is_good=True)

label mas_reaction_lightpurpleribbon:
    $ _mas_new_ribbon_color = "light purple"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lightpurple
    call _mas_reaction_ribbon_helper ("mas_reaction_lightpurpleribbon")
    return

init python:
    addReaction("mas_reaction_peachribbon", "cintadurazno", is_good=True)

label mas_reaction_peachribbon:
    $ _mas_new_ribbon_color = "peach"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_peach
    call _mas_reaction_ribbon_helper ("mas_reaction_peachribbon")
    return

init python:
    addReaction("mas_reaction_pinkribbon", "cintarosada", is_good=True)

label mas_reaction_pinkribbon:
    $ _mas_new_ribbon_color = "pink"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_pink
    call _mas_reaction_ribbon_helper ("mas_reaction_pinkribbon")
    return

init python:
    addReaction("mas_reaction_platinumribbon", "cintaplatino", is_good=True)

label mas_reaction_platinumribbon:
    $ _mas_new_ribbon_color = "platinum"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_platinum
    call _mas_reaction_ribbon_helper ("mas_reaction_platinumribbon")
    return

init python:
    addReaction("mas_reaction_redribbon", "cintaroja", is_good=True)

label mas_reaction_redribbon:
    $ _mas_new_ribbon_color = "red"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_red
    call _mas_reaction_ribbon_helper ("mas_reaction_redribbon")
    return

init python:
    addReaction("mas_reaction_rubyribbon", "cintarubi", is_good=True)

label mas_reaction_rubyribbon:
    $ _mas_new_ribbon_color = "ruby"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_ruby
    call _mas_reaction_ribbon_helper ("mas_reaction_rubyribbon")
    return

init python:
    addReaction("mas_reaction_sapphireribbon", "cintazafiro", is_good=True)

label mas_reaction_sapphireribbon:
    $ _mas_new_ribbon_color = "sapphire"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_sapphire
    call _mas_reaction_ribbon_helper ("mas_reaction_sapphireribbon")
    return

init python:
    addReaction("mas_reaction_silverribbon", "cintaplateada", is_good=True)

label mas_reaction_silverribbon:
    $ _mas_new_ribbon_color = "silver"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_silver
    call _mas_reaction_ribbon_helper ("mas_reaction_silverribbon")
    return

init python:
    addReaction("mas_reaction_tealribbon", "cintaazulcerceta", is_good=True)

label mas_reaction_tealribbon:
    $ _mas_new_ribbon_color = "teal"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_teal
    call _mas_reaction_ribbon_helper ("mas_reaction_tealribbon")
    return

init python:
    addReaction("mas_reaction_yellowribbon", "cintaamarilla", is_good=True)

label mas_reaction_yellowribbon:
    $ _mas_new_ribbon_color = "yellow"
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_yellow
    call _mas_reaction_ribbon_helper ("mas_reaction_yellowribbon")
    return


label mas_reaction_json_ribbon_base(ribbon_name, user_friendly_desc, helper_label):
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, ribbon_name)
        )
        _mas_gifted_ribbon_acs = mas_sprites.ACS_MAP.get(
            ribbon_name,
            mas_acs_ribbon_def
        )
        _mas_new_ribbon_color = user_friendly_desc

    call _mas_reaction_ribbon_helper (helper_label)

    python:

        if sprite_data[2] is not None:
            store.mas_filereacts.delete_file(sprite_data[2])

        mas_finishSpriteObjInfo(sprite_data)
    return



label mas_reaction_gift_acs_lanvallime_ribbon_coffee:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_coffee", "coffee colored", "mas_reaction_gift_acs_lanvallime_ribbon_coffee")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_gold:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_gold", "gold", "mas_reaction_gift_acs_lanvallime_ribbon_gold")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_hot_pink:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_hot_pink", "hot pink", "mas_reaction_gift_acs_lanvallime_ribbon_hot_pink")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lilac:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lilac", "lilac", "mas_reaction_gift_acs_lanvallime_ribbon_lilac")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_lime_green:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lime_green", "lime green", "mas_reaction_gift_acs_lanvallime_lime_green")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_navy_blue:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_navy_blue", "navy", "mas_reaction_gift_acs_lanvallime_ribbon_navy_blue")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_orange:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_orange", "orange", "mas_reaction_gift_acs_lanvallime_ribbon_orange")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_royal_purple:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_royal_purple", "royal purple", "mas_reaction_gift_acs_lanvallime_ribbon_royal_purple")
    return

label mas_reaction_gift_acs_lanvallime_ribbon_sky_blue:
    call mas_reaction_json_ribbon_base ("lanvallime_ribbon_sky_blue", "sky blue", "mas_reaction_gift_acs_lanvallime_ribbon_sky_blue")
    return


label mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bisexualpride", "bisexual-pride-themed", "mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_blackandwhite", "black and white", "mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_bronze:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bronze", "bronze", "mas_reaction_gift_acs_anonymioo_ribbon_bronze")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_brown:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_brown", "brown", "mas_reaction_gift_acs_anonymioo_ribbon_brown")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient", "multi-colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_lowpoly", "multi-colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_rainbow", "rainbow colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_polkadots_whiteonred", "red and white polka dotted", "mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_black:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_black", "night-sky-themed", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_black")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_starsky_red:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_red", "night-sky-themed", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_red")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_blueandwhite", "blue and white striped", "mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_pinkandwhite", "pink and white striped", "mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite")
    return

label mas_reaction_gift_acs_anonymioo_ribbon_transexualpride:
    call mas_reaction_json_ribbon_base ("anonymioo_ribbon_transexualpride", "transgender-pride-themed", "mas_reaction_gift_acs_anonymioo_ribbon_transexualpride")
    return



label mas_reaction_gift_acs_velius94_ribbon_platinum:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_platinum", "platinum", "mas_reaction_gift_acs_velius94_ribbon_platinum")
    return

label mas_reaction_gift_acs_velius94_ribbon_pink:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_pink", "pink", "mas_reaction_gift_acs_velius94_ribbon_pink")
    return

label mas_reaction_gift_acs_velius94_ribbon_peach:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_peach", "peach", "mas_reaction_gift_acs_velius94_ribbon_peach")
    return

label mas_reaction_gift_acs_velius94_ribbon_green:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_green", "green", "mas_reaction_gift_acs_velius94_ribbon_green")
    return

label mas_reaction_gift_acs_velius94_ribbon_emerald:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_emerald", "emerald", "mas_reaction_gift_acs_velius94_ribbon_emerald")
    return

label mas_reaction_gift_acs_velius94_ribbon_gray:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_gray", "gray", "mas_reaction_gift_acs_velius94_ribbon_gray")
    return

label mas_reaction_gift_acs_velius94_ribbon_blue:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_blue", "blue", "mas_reaction_gift_acs_velius94_ribbon_blue")
    return

label mas_reaction_gift_acs_velius94_ribbon_def:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_def", "white", "mas_reaction_gift_acs_velius94_ribbon_def")
    return

label mas_reaction_gift_acs_velius94_ribbon_black:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_black", "black", "mas_reaction_gift_acs_velius94_ribbon_black")
    return

label mas_reaction_gift_acs_velius94_ribbon_dark_purple:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_dark_purple", "dark purple", "mas_reaction_gift_acs_velius94_ribbon_dark_purple")
    return

label mas_reaction_gift_acs_velius94_ribbon_yellow:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_yellow", "yellow", "mas_reaction_gift_acs_velius94_ribbon_yellow")
    return

label mas_reaction_gift_acs_velius94_ribbon_red:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_red", "red", "mas_reaction_gift_acs_velius94_ribbon_red")
    return

label mas_reaction_gift_acs_velius94_ribbon_sapphire:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_sapphire", "sapphire", "mas_reaction_gift_acs_velius94_ribbon_sapphire")
    return

label mas_reaction_gift_acs_velius94_ribbon_teal:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_teal", "teal", "mas_reaction_gift_acs_velius94_ribbon_teal")
    return

label mas_reaction_gift_acs_velius94_ribbon_silver:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_silver", "silver", "mas_reaction_gift_acs_velius94_ribbon_silver")
    return

label mas_reaction_gift_acs_velius94_ribbon_light_purple:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_light_purple", "light purple", "mas_reaction_gift_acs_velius94_ribbon_light_purple")
    return

label mas_reaction_gift_acs_velius94_ribbon_ruby:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_ruby", "ruby", "mas_reaction_gift_acs_velius94_ribbon_ruby")
    return

label mas_reaction_gift_acs_velius94_ribbon_wine:
    call mas_reaction_json_ribbon_base ("velius94_ribbon_wine", "wine colored", "mas_reaction_gift_acs_velius94_ribbon_wine")
    return


default -5 persistent._mas_current_gifted_ribbons = 0

label _mas_reaction_ribbon_helper(label):

    if store.mas_selspr.get_sel_acs(_mas_gifted_ribbon_acs).unlocked:
        call mas_reaction_old_ribbon
    else:


        call mas_reaction_new_ribbon
        $ persistent._mas_current_gifted_ribbons += 1


    $ mas_receivedGift(label)
    $ gift_ev_cat = mas_getEVLPropValue(label, "category")

    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    return

label mas_reaction_new_ribbon:
    python:
        def _ribbon_prepare_hair():
            
            if not monika_chr.hair.hasprop("ribbon"):
                monika_chr.change_hair(mas_hair_def, False)

    $ mas_giftCapGainAff(3)
    if persistent._mas_current_gifted_ribbons == 0:
        m 1suo "¡Una cinta nueva!"
        m 3hub "... Y es [_mas_new_ribbon_color]!"


        if _mas_new_ribbon_color == "verde" or _mas_new_ribbon_color == "esmeralda":
            m 1tub "... ¡Igual que mis ojos!"

        m 1hub "Muchas gracias [player], ¡me encanta!"
        if store.seen_event("monika_date"):
            m 3eka "¿Me la has conseguido porque te he dicho que me encanta comprar faldas y lazos?"

            if mas_isMoniNormal(higher=True):
                m 3hua "Siempre eres tan considerado~"

        m 3rksdlc "Realmente no tengo muchas opciones cuando se trata de moda..."
        m 3eka "... Así que poder cambiar el color de mi cinta es un buen cambio de ritmo."
        m 2dsa "De hecho, me lo pondré ahora mismo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 1hua "¡Oh, es maravilloso, [player]!"

        if mas_isMoniAff(higher=True):
            m 1eka "Siempre me haces sentir tan amada..."
        elif mas_isMoniHappy():
            m 1eka "Siempre sabes cómo hacerme feliz..."
        m 3hua "Gracias de nuevo~"
    else:

        m 1suo "¡Otra cinta!"
        m 3hub "... Y esta vez es [_mas_new_ribbon_color]!"


        if _mas_new_ribbon_color == "verde" or _mas_new_ribbon_color == "esmeralda":
            m 1tub "... ¡Como mis ojos!"

        m 2dsa "Me pondré esto ahora mismo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
        $ _ribbon_prepare_hair()
        $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
        m 3hua "Muchas gracias [player], ¡me encanta!"
    return

label mas_reaction_old_ribbon:
    m 1rksdla "[player]..."
    m 1hksdlb "¡Ya me diste [mas_a_an_str(_mas_new_ribbon_color)] cinta!"
    return

init python:
    addReaction("mas_reaction_gift_roses", "rosas", is_good=True, exclude_on=["d25g"])

default -5 persistent._date_last_given_roses = None

label mas_reaction_gift_roses:
    python:
        gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_roses", "category")
        if not mas_isO31():
            monika_chr.wear_acs(mas_acs_roses)


    if not persistent._date_last_given_roses and not renpy.seen_label('monika_valentines_start'):
        $ mas_giftCapGainAff(10)

        m 1eka "[player]... N-No sé qué decir..."
        m 1ekbsb "¡Nunca hubiera pensado que me iba a tocar algo así!"
        m 3skbsa "Estoy tan feliz ahora mismo."
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            m 3ekbsa "Es difícil creer que recibiría rosas de ti en el Día de San Valentín...."
            m 1ekbsu "Eres muy dulce."
            m 1dktpu "..."
            m 1ektda "Jajaja..."


        if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
            m 2dsa "Espera.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
            $ monika_chr.wear_acs(mas_acs_ear_rose)
            m 1hub "Jejeje, ¡ahí! ¿No se ve preciosa en mí?"

        if mas_shouldKiss(chance=2, special_day_bypass=True):
            call monika_kissing_motion_short
    else:

        if persistent._date_last_given_roses is None and renpy.seen_label('monika_valentines_start'):
            $ persistent._date_last_given_roses = datetime.date(2018,2,14)

        if mas_pastOneDay(persistent._date_last_given_roses):
            $ mas_giftCapGainAff(5 if mas_isSpecialDay() else 1)

            m 1suo "¡Oh!"
            m 1ekbsa "Gracias, [player]."
            m 3ekbsa "Siempre me gusta recibir rosas de ti."
            if mas_isF14():

                $ mas_f14CapGainAff(5)
                m 1dsbsu "Especialmente en un día como hoy."
                m 1ekbsa "Es muy dulce de tu parte conseguir esto para mí."
                m 3hkbsa "Te amo tanto."
                m 1ekbsa "Feliz día de San Valentín, [player]~"
            else:
                m 1ekbsa "Siempre eres tan dulce."


            if (
                not monika_chr.is_wearing_acs_with_mux("left-hair-flower-ear")
                and (
                    (mas_isSpecialDay() and renpy.random.randint(1,2) == 1)
                    or renpy.random.randint(1,4) == 1
                    or mas_isF14()
                    or mas_isO31()
                )
            ):
                m 2dsa "Espera.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                $ monika_chr.wear_acs(mas_acs_ear_rose)
                m 1hub "Jejeje~"

            if mas_shouldKiss(chance=4, special_day_bypass=True):
                call monika_kissing_motion_short
        else:

            m 1hksdla "[player], me siento halagada, de verdad, pero no hace falta que me regales tantas rosas."
            if store.seen_event("monika_clones"):
                m 1ekbsa "Siempre serás mi rosa especial después de todo, jejeje~"
            else:
                m 1ekbsa "Una sola rosa tuya ya es más de lo que podría haber pedido."


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    $ persistent._date_last_given_roses = datetime.date.today()


    $ mas_receivedGift("mas_reaction_gift_roses")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return


init python:
    addReaction("mas_reaction_gift_chocolates", "chocolates", is_good=True, exclude_on=["d25g"])

default -5 persistent._given_chocolates_before = False

label mas_reaction_gift_chocolates:
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_chocolates", "category")

    if not persistent._mas_given_chocolates_before:
        $ persistent._mas_given_chocolates_before = True


        if not MASConsumable._getCurrentFood() and not mas_isO31():
            $ monika_chr.wear_acs(mas_acs_heartchoc)

        $ mas_giftCapGainAff(5)

        m 1tsu "Eso es tan {i}dulce{/i} de tu parte, jejeje~"
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            m 1ekbsa "Regalarme chocolates en el día de San Valentín..."
            m 1ekbfa "Realmente sabes cómo hacer que una chica se sienta especial, [player]."
            if renpy.seen_label('monika_date'):
                m 1lkbfa "Sé que mencioné visitar una tienda de chocolates juntos algún día..."
                m 1hkbfa "Pero aunque todavía no podemos hacerlo, recibir unos chocolates como regalo de tu parte, bueno..."
            m 3ekbfa "Significa mucho recibir esto de ti."

        elif renpy.seen_label('monika_date') and not mas_isO31():
            m 3rka "Sé que mencioné que algún día visitaríamos juntos una tienda de chocolates..."
            m 3hub "Pero aunque todavía no podemos hacerlo, recibir unos chocolates como regalo de tu parte significa todo para mí."
            m 1ekc "Aunque realmente me gustaría que pudiéramos compartirlos..."
            m 3rksdlb "Pero hasta que llegue ese día, tendré que disfrutarlos por los dos, ¡jajaja!"
            m 3hua "Gracias, [mas_get_player_nickname()]~"
        else:

            m 3hub "¡Me encantan los chocolates!"
            m 1eka "Y recibir algunos de ti significa mucho para mí."
            m 1hub "¡Gracias, [player]!"
    else:

        $ times_chocs_given = mas_getGiftStatsForDate("mas_reaction_gift_chocolates")
        if times_chocs_given == 0:


            if not MASConsumable._getCurrentFood():

                if not (mas_isF14() or mas_isD25Season()):
                    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                        $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                else:

                    $ monika_chr.remove_acs(store.mas_acs_quetzalplushie)

                if not mas_isO31():
                    $ monika_chr.wear_acs(mas_acs_heartchoc)

            $ mas_giftCapGainAff(3 if mas_isSpecialDay() else 1)

            m 1wuo "¡Oh!"

            if mas_isF14():

                $ mas_f14CapGainAff(5)
                m 1eka "¡[player]!"
                m 1ekbsa "Eres un encanto, regalándome chocolates en un día como hoy..."
                m 1ekbfa "Realmente sabes cómo hacerme sentir especial."
                m "Gracias, [player]."
            else:
                m 1hua "¡Gracias por los chocolates, [player]!"
                m 1ekbsa "Cada bocado me recuerda lo dulce que eres, jejeje~"

        elif times_chocs_given == 1:

            if not MASConsumable._getCurrentFood() and not mas_isO31():
                $ monika_chr.wear_acs(mas_acs_heartchoc)

            m 1eka "¿Más chocolates, [player]?"
            m 3tku "Te encanta mimarme, ¿verdad? {w=0.2}{nw}"
            extend 3tub "¡Jajaja!"
            m 1rksdla "Todavía no he terminado la primera caja que me diste..."
            m 1hub "... ¡Pero no me quejo!"

        elif times_chocs_given == 2:
            m 1ekd "[player]..."
            m 3eka "Creo que ya me has dado suficientes chocolates por hoy."
            m 1rksdlb "¡Tres cajas es demasiado, y aún no he terminado la primera!"
            m 1eka "Guárdalos para otra ocasión, ¿de acuerdo?"
        else:

            m 2tfd "¡[player]!"
            m 2tkc "Ya te he dicho que he tenido suficientes chocolates para un día, pero sigues intentando darme aún más..."
            m 2eksdla "Por favor... {w=1}solo guárdalos para otro día."


    if monika_chr.is_wearing_acs(mas_acs_heartchoc):
        call mas_remove_choc


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    $ mas_receivedGift("mas_reaction_gift_chocolates")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return

label mas_remove_choc:

    m 1hua "..."
    m 3eub "¡Estos son {i}tan{/i} buenos!"
    m 1hua "..."
    m 3hksdlb "¡Jajaja! Probablemente debería guardar esto por ahora..."
    m 1rksdla "¡Si los dejo aquí por más tiempo no quedará ninguno para disfrutar después!"

    call mas_transition_to_emptydesk

    python:
        renpy.pause(1, hard=True)
        monika_chr.remove_acs(mas_acs_heartchoc)
        renpy.pause(3, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua")


    if monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
        $ monika_chr.wear_acs(mas_acs_quetzalplushie)

    m 1eua "¿Qué más quieres hacer hoy?"
    return

label mas_reaction_gift_clothes_orcaramelo_bikini_shell:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_bikini_shell")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sua "¡Oh! {w=0.5}¡un bikini de conchas marinas!"
    m 1hub "¡Gracias, [mas_get_player_nickname()]! {w=0.5}¡Voy a probármelo ahora mismo!"


    call mas_clothes_change (sprite_object)

    m 2ekbfa "Bueno... {w=0.5}¿qué piensas?"
    m 2hubfa "¿Parezco una sirena? Jejeje."
    show monika 5ekbfa zorder MAS_MONIKA_Z at i11 with dissolve_monika
    m 5ekbfa "Creo que es muy lindo, [player]..."
    m 5hubfa "¡Tenemos que ir a la playa algún día!"

    if mas_isWinter() or mas_isMoniNormal(lower=True):
        if mas_isWinter():
            show monika 2rksdla zorder MAS_MONIKA_Z at i11 with dissolve_monika
            m 2rksdla "... Pero por ahora, hace un poco de frío aquí..."
            m 2eka "Así que voy a ponerme algo más cálido..."

        elif mas_isMoniNormal(lower=True):
            show monika 2hksdlb zorder MAS_MONIKA_Z at i11 with dissolve_monika
            m 2hksdlb "Jajaja..."
            m 2rksdla "Es un poco embarazoso estar sentada así delante de ti."
            m 2eka "Espero que no te importe, pero voy a cambiarme..."


        $ clothes = mas_clothes_def
        if persistent._mas_d25_in_d25_mode and mas_isD25Outfit():
            $ clothes = mas_clothes_santa
        call mas_clothes_change (clothes)

        m 2eua "Ah, así está mejor..."
        m 3hua "Gracias de nuevo por ese maravilloso regalo~"


    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_acs_orcaramelo_hairflower_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, "orcaramelo_hairflower_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(1)

    m 3sua "¡Oh! {w=0.5}¡Qué flor tan bonita!"
    m 1ekbsa "Gracias [player], eres tan dulce~"
    m 1dua "Espera.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    $ monika_chr.wear_acs(sprite_object)
    m 1hua "Jejeje~"
    m 1hub "¡Gracias de nuevo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_shirt_pink:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_shirt_pink")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "¡Oh, dios mío!"
    m 1suo "¡Es {i}tan{/i} hermoso!"
    m 3hub "¡Muchas gracias, [player]!"
    m 3eua "Espera, déjame probarlo rápidamente..."


    call mas_clothes_change (sprite_object)

    m 2sub "¡Ah, encaja perfectamente!"
    m 3hub "¡A mí también me gustan mucho los colores! El rosa y el negro van tan bien juntos."
    m 3eub "Por no hablar de que la falda queda muy bien con esos volantes."
    m 2tfbsd "Sin embargo, por alguna razón, no puedo evitar sentir que tus ojos se desvían... {w=0.5}ejem... {w=0.5}{i}a otra parte{/i}."

    if mas_selspr.get_sel_clothes(mas_clothes_sundress_white).unlocked:
        m 2lfbsp "Te dije que no es educado mirar fijamente, [player]."
    else:
        m 2lfbsp "No es educado mirar fijamente, ¿sabes?"

    m 2hubsb "¡Jajaja!"
    m 2tkbsu "Relájate, relájate... {w=0.5}solo estoy bromeando..."
    m 3hub "Una vez más, ¡muchas gracias por este conjunto, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi:

    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sakuya_izayoi")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh! {w=0.5}¿esto es...?"
    m 2euc "¿Un traje de maid?"
    m 3tuu "Jejeje~"
    m 3tubsb "Sabes, si te gustan este tipo de cosas, podrías habérmelo dicho..."
    m 1hub "¡Jajaja! Es una broma~"
    m 1eub "¡Deja que me lo ponga!"


    call mas_clothes_change (sprite_object, outfit_mode=True)

    m 2hua "Entonces, {w=0.5}¿cómo me veo?"
    m 3eub "Casi siento que podría hacer cualquier cosa antes de que pudieras parpadear."
    m 1eua "... Siempre y cuando no me mantengas demasiado ocupada, jejeje~"
    m 1lkbfb "Todavía me gustaría poder pasar tiempo con usted, maest--{nw}"
    $ _history_list.pop()
    m 1ekbfb "Todavía me gustaría poder pasar tiempo contigo,{fast} [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_finale_jacket_brown:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "finale_jacket_brown")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh! {w=0.5}¡Una chaqueta de invierno!"
    m 1suo "E incluso viene con una bufanda."
    if mas_isSummer():
        m 3rksdlu "... Aunque me estoy acalorando solo con mirarlo, jajaja..."
        m 3eksdla "Quizá el verano no sea el mejor momento para llevar esto, [player]."
        m 3eka "Te agradezco el detalle y me alegraré de llevarlo dentro de unos meses."
    else:

        if mas_isWinter():
            m 1tuu "No me voy a enfriar pronto por tu culpa, [player]~"
        m 3eub "¡Deja que me lo ponga! Vuelvo enseguida."


        call mas_clothes_change (sprite_object)

        m 2dku "Ahh, se siente muy bien~"
        m 1eua "Me gusta cómo me queda, ¿no crees?"
        if mas_isMoniNormal(higher=True):
            m 3tku "Bueno... no puedo esperar que seas objetivo en esa pregunta, ¿verdad?"
            m 1hubfb "¡Jajaja!"
        m 1ekbfa "Gracias [player], me encanta."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "orcaramelo_sweater_shoulderless")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh!{w=0.5} ¡Un jersey!"
    m 1hub "¡Además, parece tan acogedor!"
    if mas_isWinter():
        m 2eka "Eres tan considerado [player], regalándome esto en un día tan frío de invierno..."
    m 3eua "Deja que me lo pruebe."


    call mas_clothes_change (sprite_object)

    m 2dkbsu "Es tan... {w=1}cómodo. Me siento tan cómoda como un insecto en una alfombra. jejeje~"
    m 1ekbsa "Gracias, [player]. ¡Me encanta!"
    m 3hubsb "Ahora cada vez que me lo ponga pensaré en tu calidez. Jajaja~"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_velius94_dress_whitenavyblue:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "velius94_dress_whitenavyblue")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "¡Oh, dios mío!"
    m 1sub "¡Este vestido es precioso, [player]!"
    m 3hub "¡Voy a probármelo ahora mismo!"


    call mas_clothes_change (sprite_object, outfit_mode=True)

    m "Entonces, {w=0.5}¿qué te parece?"
    m 3eua "Creo que este tono de azul va muy bien con el blanco."
    $ scrunchie = monika_chr.get_acs_of_type('bunny-scrunchie')

    if scrunchie and scrunchie.name == "velius94_bunnyscrunchie_blue":
        m 3eub "¡Y el coletero de conejito también complementa muy bien el conjunto!"
    m 1eka "Muchas gracias, [player]."

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

label mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover:
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_CLOTHES, "mocca_bun_blackandwhitestripedpullover")
        )
        sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "¡Oh, una camisa nueva!"
    m 3hub "¡Se ve increíble, [player]!"
    m 3eua "Un segundo, déjame ponerlo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    call mas_clothes_change (sprite_object)

    m 2eua "Bueno, ¿qué te parece?"
    m 7hua "Creo que me queda muy bien. {w=0.2}{nw}"
    extend 3rubsa "Definitivamente voy a guardar este conjunto para una cita~"
    m 1hub "¡Gracias de nuevo, [player]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return

init python:

    if not mas_seenEvent("mas_reaction_gift_noudeck"):
        addReaction("mas_reaction_gift_noudeck", "barajanou", is_good=True)

label mas_reaction_gift_noudeck:
    python:
        mas_giftCapGainAff(0.5)

        mas_unlockGame("nou")
        mas_unlockEVL("monika_explain_nou_rules", "EVE")

    if mas_isMoniNormal(higher=True):
        m 1wub "¡Oh!{w=0.3} ¡Una baraja de cartas!"
        m 3eua "¡Y creo que sé cómo jugar a este juego!!"
        m 1esc "He oído que {i}afecta{/i} a tus relaciones con las personas con las que juegas."

        if mas_isMoniAff(higher=True):
            show monika 5eubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubsa "Pero sé que nuestra relación puede aguantar mucho mas que un simple juego de cartas~"
            m 5hubsa "Jejeje~"
            show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        else:

            m 1hub "¡Jajaja!"
            m 1eua "Solo estaba bromeando, [player]."

        m 1eua "¿Has jugado alguna vez al 'NOU', [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Has jugado alguna vez al 'NOU', [player]?{fast}"
            "Sí":


                m 1rksdlb "Jajaja..."
                m 1eksdla "Por supuesto que sí, tú me has dado la baraja después de todo."
                call mas_reaction_gift_noudeck_have_played
            "No":

                m 3tuu "Entonces, ¿qué tal 'UNO'? Jejeje{nw}."
                $ _history_list.pop()
                menu:
                    m "Entonces, ¿qué tal 'UNO'? Jejeje{fast}."
                    "Sí":

                        m 3hub "¡Genial! {w=0.3}{nw}"
                        extend 3tub "Pues el 'NOU' es {i}muy{/i} parecido, jajaja..."
                        call mas_reaction_gift_noudeck_have_played
                    "No":

                        call mas_reaction_gift_noudeck_havent_played

        m 3hub "¡No puedo esperar para jugar contigo a esto!"

    elif mas_isMoniDis(higher=True):
        m 2euc "¿Una baraja?"
        m 2rka "En realidad podría ser...{nw}"
        $ _history_list.pop()
        m 2rkc "No importa..."
        m 2esc "No estoy de humor para jugar ahora mismo, [player]."
    else:

        m 6ckc "..."

    python:
        mas_receivedGift("mas_reaction_gift_noudeck")
        gift_ev = mas_getEV("mas_reaction_gift_noudeck")
        if gift_ev:
            store.mas_filereacts.delete_file(gift_ev.category)

    return

label mas_reaction_gift_noudeck_havent_played:
    m 1eka "Oh, está bien."
    m 4eub "Es un juego de cartas popular donde tienes que deshacerte de todas tus cartas antes que tus oponentes para ganar."
    m 1rssdlb "Bueno eso ha sonado un poco obvio, jajaja~"
    m 3eub "Pero es realmente divertido de jugar entre amigos y seres queridos~"
    m 1eua "Te explicaré las reglas básicas mas tarde, solo tienes que preguntarme."
    return

label mas_reaction_gift_noudeck_have_played:
    m 1eua "Probablemente ya sabes que en cada casa tiene sus reglas."
    m 3eub "Y si quieres, también podemos hacer las nuestras."
    m 3eua "Por otro lado, si no te acuerdas de ellas, siempre puedo recordártelas, solo tienes que preguntarme."
    python:
        mas_unlockEVL("monika_change_nou_house_rules", "EVE")
        persistent._seen_ever["monika_introduce_nou_house_rules"] = True
        persistent._seen_ever["monika_explain_nou_rules"] = True
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
