






define persistent._mas_zz_lupd_ex_v = []


init -10 python:
    found_monika_ani = persistent.monika_anniversary is not None
    no_topics_list = persistent.monika_random_topics is None








init 4 python:


    if persistent.version_number != config.version:
        
        persistent.monika_topic = None
        
        
        persistent._mas_unsee_unseen = False





















init python:
    def removeTopicID(topicID):
        """
        Removes one topic from the _seen_ever variable topics list if it exists in either var
        (persistent is also checked for existence)

        IN:
            topicID - the topicID to remove

        ASSUMES:
            persistent._seen_ever
        """
        if renpy.seen_label(topicID):
            persistent._seen_ever.pop(topicID)

    def mas_eraseTopic(topicID, per_eventDB=persistent.event_database):
        """
        Erases an event from both lockdb and Event database
        This should also handle lockdb data as well.
        TopicIDs that are not in the given eventDB are silently ignored.
        (LockDB data will be erased if found)

        IN:
            topicID - topic ID / label
            per_eventDB - persistent database this topic is in
        """
        if topicID in per_eventDB:
            per_eventDB.pop(topicID)
        
        if topicID in Event.INIT_LOCKDB:
            Event.INIT_LOCKDB.pop(topicID)

    def mas_transferTopic(old_topicID, new_topicID, per_eventDB):
        """DEPREACTED

        NOTE: This can cause data corruption. DO NOT USE.

        Transfers a topic's data from the old topic ID to the new one int he
        given database as well as the lock database.

        NOTE: If the new topic ID already exists in the given databases,
        the data is OVERWRITTEN

        IN:
            old_topicID - old topic ID to transfer
            new_topicID - new topic ID to receieve
            per_eventDB - persistent databse this topic is in
        """
        if old_topicID in per_eventDB:
            
            
            
            old_data = list(per_eventDB.pop(old_topicID))
            old_data[0] = new_topicID
            per_eventDB[new_topicID] = tuple(old_data)
        
        if old_topicID in Event.INIT_LOCKDB:
            Event.INIT_LOCKDB[new_topicID] = Event.INIT_LOCKDB.pop(old_topicID)

    def mas_transferTopicSeen(old_topicID, new_topicID):
        """
        Tranfers persistent seen ever data. This is separate because of complex
        topic adjustments

        IN:
            old_topicID - old topic ID to tranfer
            new_topicID - new topic ID to receieve
        """
        if old_topicID in persistent._seen_ever:
            persistent._seen_ever.pop(old_topicID)
            persistent._seen_ever[new_topicID] = True

    def adjustTopicIDs(changedIDs,updating_persistent=persistent):
        """
        Changes labels in persistent._seen_ever
        to new IDs in the changedIDs dict

        IN:
            oldList - the list of old Ids to change
            changedIDs - dict of changed ids:
                key -> old ID
                value -> new ID

        ASSUMES:
            persistent._seen_ever
        """
        
        
        
        
        for oldTopic in changedIDs:
            if updating_persistent._seen_ever.pop(oldTopic,False):
                updating_persistent._seen_ever[changedIDs[oldTopic]] = True
        
        return updating_persistent

    def updateTopicIDs(version_number,updating_persistent=persistent):
        """
        Updates topic IDS between versions by performing a two step process: adjust exisitng IDS to match the new IDS
        then add newIDs to the persistent randomtopics

        IN:
            version_number - the version number we are updating to

        ASSUMES:
            persistent._seen_ever
            updates.topics
        """
        if version_number in updates.topics:
            changedIDs = updates.topics[version_number]
            
            
            if changedIDs is not None:
                adjustTopicIDs(changedIDs, updating_persistent)
        
        return updating_persistent

    def updateGameFrom(startVers):
        """
        Updates the game, starting at the given start version

        IN:
            startVers - the version number in the parsed format ('v#####')

        ASSUMES:
            updates.version_updates
        """
        
        while startVers in updates.version_updates:
            
            updateTo = updates.version_updates[startVers]
            
            
            if renpy.has_label(updateTo) and not renpy.seen_label(updateTo):
                renpy.call_in_new_context(updateTo, updateTo)
            startVers = updates.version_updates[startVers]

    def safeDel(varname):
        """
        Safely deletes variables from persistent

        IN:
            varname - name of the variable to delete from persistent as string

        NOTE: THIS SHOULD BE USED IN PLACE OF THE DEFAULT `del` KEYWORD WHEN DELETING VARIABLES FROM THE PERSISTENT
        """
        if varname in persistent.__dict__:
            persistent.__dict__.pop(varname)


init 7 python:
    def mas_transferTopicData(
        new_topic_evl,
        old_topic_evl,
        old_topic_ev_db,
        transfer_unlocked=True,
        transfer_shown_count=True,
        transfer_seen_data=True,
        transfer_last_seen=True,
        erase_topic=True
    ):
        """
        Transfers topic data from ev to ev

        IN:
            new_topic_evl - new topic's eventlabel
            old_topic_evl - old topic's eventlabel
            old_topic_ev_db - event database containing the old topic
            transfer_unlocked - whether or not we should transfer the unlocked property of the old topic
            (Default: True)
            transfer_shown_count - whether or not we should transfer the shown_count property of the old topic
            (Default: True)
            transfer_seen_data - whether or not we should transfer the _seen_ever state of the old topic
            (Default: True)
            transfer_last_seen - whether or not we should transfer the last_seen property of the old topic
            (Default: True)
            erase_topic - whether or not we should erase this topic after transferring data
            (Defualt: True)
        """
        
        new_ev = mas_getEV(new_topic_evl)
        
        
        if old_topic_evl in old_topic_ev_db:
            old_ev = Event(
                old_topic_ev_db,
                old_topic_evl
            )
        else:
            old_ev = None
        
        if new_ev is not None and old_ev is not None:
            if transfer_unlocked:
                
                new_ev.unlocked = old_ev.unlocked
            
            if transfer_shown_count:
                
                new_ev.shown_count += old_ev.shown_count
            
            if (
                transfer_last_seen
                and old_ev.last_seen is not None
                and (new_ev.last_seen is None or new_ev.last_seen <= old_ev.last_seen)
            ):
                
                new_ev.last_seen = old_ev.last_seen
            
            if transfer_seen_data:
                
                mas_transferTopicSeen(old_topic_evl, new_topic_evl)
            
            
            if erase_topic:
                mas_eraseTopic(old_topic_evl, old_topic_ev_db)



init 10 python:


    if persistent.version_number is None:
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        persistent.version_number = config.version
        
        
        mas_versions.clear()

    elif persistent.version_number != config.version:
        
        t_version = persistent.version_number
        if "-" in t_version:
            t_version = t_version[:t_version.index("-")]
        vvvv_version = "v"+"_".join(t_version.split("."))
        
        updateGameFrom(vvvv_version)
        
        
        persistent.version_number = config.version
        
        
        mas_versions.clear()



    def _mas_resetVersionUpdates():
        """
        Resets all version update script's seen status
        """
        late_updates = [
            "v0_8_3",
            "v0_8_4",
            "v0_8_10",
            "v0_12_0",
        ]
        
        store.mas_versions.init()
        ver_list = store.updates.version_updates.keys()
        
        if "-" in config.version:
            working_version = config.version[:config.version.index("-")]
        else:
            working_version = config.version
        
        ver_list.extend(["mas_lupd_" + x for x in late_updates])
        ver_list.append("v" + "_".join(
            working_version.split(".")
        ))
        
        for _version in ver_list:
            if _version in persistent._seen_ever:
                persistent._seen_ever.pop(_version)













label vgenericupdate(version="v0_2_2"):
label v0_6_1(version=version):
label v0_5_1(version=version):
label v0_3_3(version=version):
label v0_3_2(version=version):
label v0_3_1(version=version):
    python:

        updateTopicIDs(version)

    return




label v0_12_15(version="v0_12_15"):
    python hide:
        pass
    return


label v0_12_13(version="v0_12_13"):
    python hide:

        m_bday_nts = mas_getEV("mas_bday_postbday_notimespent")
        m_bday_hbd = mas_getEV("mas_bday_pool_happy_bday")
        today = datetime.date.today()
        curr_year = today.year
        corr_end_date = mas_monika_birthday+datetime.timedelta(days=8)


        if m_bday_nts.start_date.year != m_bday_nts.end_date.year:
            
            
            mas_rmallEVL("mas_bday_postbday_notimespent")
            
            
            if today > corr_end_date or (m_bday_nts.last_seen and m_bday_nts.last_seen.year == curr_year):
                mas_setEVLPropValues(
                    "mas_bday_postbday_notimespent",
                    start_date = datetime.datetime.combine(mas_monika_birthday.replace(year=curr_year+1)+datetime.timedelta(days=1), datetime.time(hour=1)),
                    end_date = mas_monika_birthday.replace(year=curr_year+1)+datetime.timedelta(days=8)
                )
            
            
            
            else:
                mas_setEVLPropValues(
                    "mas_bday_postbday_notimespent",
                    start_date = datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
                    end_date = mas_monika_birthday+datetime.timedelta(days=8)
                )




        else:
            mas_setEVLPropValues(
                "mas_bday_postbday_notimespent",
                start_date=datetime.datetime.combine(mas_monika_birthday.replace(year=m_bday_nts.end_date.year)+datetime.timedelta(days=1), datetime.time(hour=1))
            )


        if today <= mas_monika_birthday:
            mas_setEVLPropValues(
                "mas_bday_pool_happy_bday",
                start_date=mas_monika_birthday,
                end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1))
            )

        else:
            mas_setEVLPropValues(
                "mas_bday_pool_happy_bday",
                start_date=mas_monika_birthday.replace(year=curr_year+1),
                end_date=datetime.datetime.combine(mas_monika_birthday.replace(year=curr_year+1)+datetime.timedelta(days=1), datetime.time(hour=1))
            )


        isld_p_data = persistent._mas_islands_unlocks
        if isld_p_data is not None:
            keys = (
                "decal_bookshelf_lantern",
                "decal_circle_garland",
                "decal_hanging_lantern",
                "decal_rectangle_garland",
                "decal_tree_lights",
                "decal_wreath"
            )
            for k in keys:
                isld_p_data[k] = False

    return


label v0_12_12(version="v0_12_12"):
    python hide:
        isld_p_data = persistent._mas_islands_unlocks
        if isld_p_data is not None:
            isld_p_data["other_shimeji"] = isld_p_data.pop("obj_shimeji", False)
            
            for k in ("decal_ghost_", "decal_haunted_tree_"):
                for i in "012":
                    isld_p_data[k + i] = False
            
            for k in (
                "decal_bloodfall",
                "decal_gravestones",
                "decal_jack",
                "decal_pumpkins",
                "decal_skull",
                "decal_webs"
            ):
                isld_p_data[k] = False
            
            isld_p_data["overlay_vignette"] = True

    return


label v0_12_10(version="v0_12_10"):
    python hide:
        mas_hideEVL("monika_lastpoem", "EVE", derandom=True)

        if not mas_seenEvent("monika_lastpoem"):
            mas_setEVLPropValues(
                "monika_lastpoem",
                conditional="persistent.playthrough >= 2",
                action=EV_ACT_RANDOM
            )

        if mas_seenLabels(['monika_solipsism']):
            mas_protectedShowEVL("monika_materialism","EVE", _random=True)

        persistent._mas_affection_version = 1

        mas_affection._transfer_aff_2nd_gen()
        mas_affection._remove_backups()
        mas_affection._make_backup()


        if mas_getEVL_shown_count("mas_story_mindthegap") < 1:
            mas_lockEVL("mas_story_mindthegap", "STY")
    return


label v0_12_8_6(version="v0_12_8_6"):
    python hide:

        if not isinstance(persistent._mas_chess_dlg_actions, defaultdict):
            replacement = defaultdict(int)
            replacement.update(persistent._mas_chess_dlg_actions)
            persistent._mas_chess_dlg_actions = replacement

    return


label v0_12_8_3(version="v0_12_8_3"):
    python hide:
        if seen_event("monika_otaku"):
            mas_protectedShowEVL("monika_conventions", "EVE", _random=True)
    return


label v0_12_8_1(version="v0_12_8_1"):
    python hide:
        mas_setEVLPropValues(
            "mas_bday_spent_time_with",
            action=EV_ACT_PUSH,
            conditional="mas_recognizedBday() and not mas_lastSeenInYear('mas_bday_spent_time_with_wrapup')"
        )














        if persistent._mas_nye_accomplished_resolutions is None:
            persistent._mas_nye_accomplished_resolutions = persistent._mas_pm_accomplished_resolutions
            store.mas_history._store_all(
                mas_HistLookup_all("pm.actions.did_new_years_resolutions"),
                "nye.actions.did_new_years_resolutions"
            )
            safeDel("_mas_pm_accomplished_resolutions")

        if persistent._mas_nye_has_new_years_res is None:
            persistent._mas_nye_has_new_years_res = persistent._mas_pm_has_new_years_res
            store.mas_history._store_all(
                mas_HistLookup_all("pm.actions.made_new_years_resolutions"),
                "nye.actions.made_new_years_resolutions"
            )
            safeDel("_mas_pm_has_new_years_res")


        mas_transferTopicData("monika_idle_brb", "monika_brb_idle", persistent.event_database)
        mas_transferTopicSeen("monika_brb_idle_callback", "monika_idle_brb_callback")
        mas_transferTopicData("monika_idle_writing", "monika_writing_idle", persistent.event_database)
        mas_transferTopicSeen("monika_writing_idle_callback", "monika_idle_writing_callback")
    return


label v0_12_8(version="v0_12_8"):
    python hide:
        sundress_white_data = store.mas_utils.pdget(
            "sundress_white",
            persistent._mas_selspr_clothes_db,
            validator=store.mas_ev_data_ver._verify_tuli_nn,
            defval=(False, )
        )
        if len(sundress_white_data) > 0 and sundress_white_data[0]:
            persistent._mas_selspr_acs_db["musicnote_necklace_gold"] = (True, True)

    return


label v0_12_7(version="v0_12_7"):
    python hide:







        credits_song_ev = mas_getEV('monika_credits_song')
        if (
                credits_song_ev
                and credits_song_ev.action
                and credits_song_ev.shown_count == 0 
        ):
            credits_song_ev.conditional = (
                "store.mas_anni.pastOneMonth() "
                "and seen_event('mas_unlock_piano')"
            )




        if "orcaramelo_twintails" in persistent._mas_selspr_hair_db:
            persistent._mas_selspr_hair_db["orcaramelo_twintails"] = (True, True)





        if (
                persistent._mas_grandfathered_nickname is None 
                and persistent._mas_monika_nickname != "Monika"
                and mas_awk_name_comp.search(persistent._mas_monika_nickname)
        ):
            persistent._mas_grandfathered_nickname = persistent._mas_monika_nickname




        if persistent._mas_called_moni_a_bad_name is not None: 
            persistent._mas_pm_called_moni_a_bad_name = persistent._mas_called_moni_a_bad_name
            safeDel("_mas_called_moni_a_bad_name")





        if not persistent._mas_penname:
            persistent._mas_penname = None




        if store.seen_event("monika_hamlet") and persistent.monika_kill:
            mas_showEVL("monika_tragic_hero", "EVE", _random=True)

    return


label v0_12_5(version="v0_12_5"):
    python hide:

        if store.seen_event("greeting_ourreality") and persistent._mas_current_background == store.mas_background.MBG_DEF:
            store.mas_unlockEVL("mas_monika_islands", "EVE")

        mas_setEVLPropValues(
            "bye_enjoyyourafternoon",
            conditional="mas_getSessionLength() <= datetime.timedelta(minutes=30)"
        )
        mas_setEVLPropValues(
            "bye_goodevening",
            conditional="mas_getSessionLength() >= datetime.timedelta(minutes=30)"
        )
        if seen_event("monika_affection_nickname"):
            mas_setEVLPropValues(
                "monika_affection_nickname",
                prompt="¿Puedo llamarte de otra manera?"
            )

        if datetime.date.today() < datetime.date(2021, 12, 31) and persistent._mas_nye_spent_nye:
            persistent._mas_nye_spent_nye = False
            mas_history._store(True, "nye.actions.spent_nye", 2020)
            
            date_count = persistent._mas_nye_nye_date_count
            persistent._mas_nye_nye_date_count = 0
            old_date_count = mas_HistLookup("nye.actions.went_out_nye", 2020)[1]
            if old_date_count is not None:
                date_count += old_date_count
            
            mas_history._store(date_count, "nye.actions.went_out_nye", 2020)

    return


label v0_12_4(version="v0_12_4"):
    python hide:
        mas_setEVLPropValues(
            'bye_trick_or_treat',
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3))
        )

        mas_setEVLPropValues(
            "greeting_ourreality",
            conditional="mas_canShowIslands(flt=False) and not mas_isSpecialDay()"
        )
    return


label v0_12_3_2(version="v0_12_3_2"):
    python hide:
        import os


        store.mas_utils.trydel(renpy.config.gamedir + "/00utils.rpy")
        store.mas_utils.trydel(renpy.config.gamedir + "/00utils.rpyc")


        def _rename_log_file(old_log_path, new_log_path):
            """
            Renames log files

            IN:
                old_log_path - the path to the old log
                new_log_path - the path to the new log
            """
            try:
                mas_utils.trydel(new_log_path)
                os.rename(old_log_path, new_log_path)
            except Exception as ex:
                mas_utils.mas_log.error("Failed to rename log at '{0}'. {1}".format(old_log_path, ex))

        log_dir = os.path.join(renpy.config.basedir, "log")

        migrating_logs = [
            mas_utils.mas_log,
            mas_affection.log,
            mas_submod_utils.submod_log
        ]
        non_migrating_logfiles = [
            "pnm.txt",
            "spj.txt"
        ]


        for mf_log_name in ("mfgen", "mfread"):
            if mas_logging.is_inited(mf_log_name):
                migrating_logs.append(mas_logging.logging.getLogger(mf_log_name))
            
            else:
                new_log_path = os.path.join(log_dir, mf_log_name + ".log")
                old_log_path = os.path.join(log_dir, mf_log_name + ".txt")
                
                _rename_log_file(old_log_path, new_log_path)

        for log in migrating_logs:
            new_log_path = os.path.join(log_dir, log.name + ".log")
            old_log_path = os.path.join(log_dir, log.name + ".txt")
            
            handlers = list(log.handlers)
            
            for handler in handlers:
                handler.close()
                log.removeHandler(handler)
            
            try:
                with open(old_log_path, "a") as mergeto, open(new_log_path, "r") as mergefrom:
                    for line in mergefrom:
                        mergeto.write(line)
            
            except Exception as ex:
                mas_utils.mas_log.error("Failed to update log at '{0}'. {1}".format(old_log_path, ex))
            
            else:
                _rename_log_file(old_log_path, new_log_path)
            
            for handler in handlers:
                
                log.addHandler(handler)

        for logfile in non_migrating_logfiles:
            mas_utils.trydel(os.path.join(log_dir, logfile))


    return


label v0_12_3_1(version="v0_12_3_1"):
    python:

        mas_setEVLPropValues(
            "greeting_ourreality",
            conditional="store.mas_decoded_islands"
        )



        persistent._mas_zz_lupd_ex_v.append(version)

    return


label v0_12_2_3(version="v0_12_2_3"):
    python:
        if seen_event("monika_fanfiction"):
            mas_protectedShowEVL('monika_ddlcroleplay', 'EVE', _random=True)

        if seen_event("monika_back_ups"):
            mas_protectedShowEVL("monika_murphys_law","EVE", _random=True)
    return


label v0_12_2_2(version="v0_12_2_2"):
    python:
        if seen_event("monika_nihilism"):
            mas_protectedShowEVL('monika_impermanence', 'EVE', _random=True)

    return


label v0_12_2(version="v0_12_2"):
    python:
        if persistent.ever_won:
            persistent._mas_ever_won.update(persistent.ever_won)

        if mas_getEVLPropValue("mas_compliment_chess", "conditional"):
            mas_setEVLPropValues(
                "mas_compliment_chess",
                conditional="persistent._mas_chess_stats.get('losses', 0) > 5"
            )



        mas_setEVLPropValues(
            'mas_d25_monika_christmas_eve',
            start_date = datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date = mas_d25
        )


        if persistent.has_merged is not None:
            persistent._mas_imported_saves = persistent.has_merged



        if persistent.clear is not None and any(persistent.clear):
            persistent._mas_imported_saves = True
        safeDel("has_merged")


        persistent.first_run = not persistent.first_run

    return


label v0_12_1_2(version="v0_12_1_2"):
    python:
        if mas_getEVLPropValue("monika_dystopias", "action"):
            mas_setEVLPropValues(
                "monika_dystopias",
                conditional="mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world', 'monika_we'], seen_all=True)"
            )

    return


label v0_12_1(version="v0_12_1"):
    python:
        missing_chess_persist_keys = [
            "practice_wins",
            "practice_losses",
            "practice_draws"
        ]

        for missing_key in missing_chess_persist_keys:
            if missing_key not in persistent._mas_chess_stats:
                persistent._mas_chess_stats[missing_key] = 0

    return


label v0_12_0(version="v0_12_0"):
    python:
        mas_setEVLPropValues(
            "mas_d25_monika_holiday_intro_upset",
            end_date=mas_d25
        )

        mas_setEVLPropValues(
            "mas_d25_monika_christmas",
            conditional="not mas_lastSeenInYear('mas_d25_monika_christmas')"
        )

        mas_setEVLPropValues(
            "mas_nye_monika_nye_dress_intro",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_PUSH
        )

        mas_setEVLPropValues(
            "mas_pf14_monika_lovey_dovey",
            random=False,
            conditional="not renpy.seen_label('mas_pf14_monika_lovey_dovey')",
            action=EV_ACT_QUEUE,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14
        )


        persistent._mas_zz_lupd_ex_v.append(version)

    return


label v0_11_9_3(version="v0_11_9_3"):
    python:
        if renpy.seen_label('mas_chess_dlg_qf_lost_ofcn_6'):
            persistent._mas_chess_timed_disable = True

        mas_setEVLPropValues(
            "mas_chess",
            conditional=(
                "persistent._mas_chess_timed_disable is not True "
                "and mas_games.is_platform_good_for_chess() "
                "and mas_timePastSince(persistent._mas_chess_timed_disable, datetime.timedelta(hours=1))"
            )
        )

        fps_to_delete = [
            "zz_windowreacts.rpy",
            "Submods/Enhanced Idle/enhanced idle.rpy"
        ]

        for fp in fps_to_delete:
            mas_utils.trydel(os.path.join(renpy.config.gamedir, fp).replace('\\', '/'))
            mas_utils.trydel(os.path.join(renpy.config.gamedir, fp + "c").replace('\\', '/'))

    return


label v0_11_9_1(version="v0_11_9_1"):
    python:
        mas_bookmarks_derand.removeDerand("monika_twitter")

        mas_setEVLPropValues(
            "monika_twitter",
            random=False,
            conditional="renpy.seen_label('monika_clones')",
            action=EV_ACT_RANDOM
        )

        if seen_event("monika_boardgames"):
            mas_protectedShowEVL("monika_boardgames_history", "EVE", _random=True)


        safeDel("chess_strength")

        for story_type, story_last_seen in persistent._mas_last_seen_new_story.iteritems():
            if story_last_seen is not None:
                persistent._mas_last_seen_new_story[story_type] = datetime.datetime.combine(
                    story_last_seen, datetime.time()
                )

        if seen_event("monika_asimov_three_laws"):
            mas_protectedShowEVL("monika_foundation", "EVE", _random=True)
    return


label v0_11_9(version="v0_11_9"):
    python:

        dropfixes = (
            "zz_delactfix",
            "zz_dropfix",
            "ev_dropfix",
            "bookderanddropfix",
            "christmas_gifts_drop"
        )
        extensions = (
            ".rpy",
            ".rpyc"
        )

        for df in dropfixes:
            for ext in extensions:
                mas_utils.trydel(
                    os.path.join(config.gamedir, df+ext).replace("\\", "/")
                )
    return


label v0_11_7(version="v0_11_7"):
    python:
        with MAS_EVL("monika_whispers") as whispers_ev:
            if (
                not persistent.clearall
                and store.mas_anni.pastOneMonth()
                and not persistent._mas_pm_cares_about_dokis
            ):
                whispers_ev.conditional = None
                whispers_ev.action = None
            
            else:
                whispers_ev.conditional = "not persistent.clearall"
                whispers_ev.action = EV_ACT_RANDOM
            
            whispers_ev.random = False
            whispers_ev.unlocked = False

        mas_setEVLPropValues(
            'mas_d25_spent_time_monika',
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=17)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=3))
        )

        mas_setEVLPropValues(
            'monika_nye_year_review',
            action=EV_ACT_QUEUE,
            start_date=mas_nye,
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23))
        )

        mas_setEVLPropValues(
            'mas_nye_monika_nye_dress_intro',
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_SELisUnlocked(mas_clothes_dress_newyears)"
            )
        )

        mas_setEVLPropValues(
            'mas_d25_monika_christmaslights',
            conditional=(
                "persistent._mas_pm_hangs_d25_lights is None "
                "and persistent._mas_d25_deco_active "
                "and not persistent._mas_pm_live_south_hemisphere "
                "and mas_isDecoTagVisible('mas_d25_lights')"
            )
        )

        safeDel("_mas_d25_gifted_cookies")

    return


label v0_11_6(version="v0_11_6"):
    python:

        mas_lockEVL("monika_daydream", "EVE")


        if mas_seenLabels(["mas_monika_plays_yr", "mas_monika_plays_or"]):
            mas_unlockEVL("monika_piano_lessons", "EVE")


        if seen_event("monika_debate"):
            mas_showEVL('monika_taking_criticism', 'EVE', _random=True)
            mas_showEVL('monika_giving_criticism', 'EVE', _random=True)

        if seen_event("monika_vn"):
            mas_unlockEVL("monika_kamige","EVE")


        filenames_to_delete = [
            "sprite-chart-00.rpyc",
            "sprite-chart-01.rpyc",
            "sprite-chart-02.rpyc",
            "sprite-chart-10.rpyc",
            "sprite-chart-20.rpyc",
            "sprite-chart-21.rpyc"
        ]

        for fn in filenames_to_delete:
            mas_utils.trydel(os.path.join(renpy.config.gamedir, fn))

    return


label v0_11_5(version="v0_11_5"):
    python:

        game_evls = (
            ("mas_hangman", "mas_unlock_hangman"),
            ("mas_chess", "mas_unlock_chess",),
            ("mas_piano", "mas_unlock_piano"),
        )

        for game_evl, unlock_evl in game_evls:
            
            if (
                    renpy.seen_label(unlock_evl)
                    or mas_getEVL_shown_count(unlock_evl) > 0
            ):
                mas_unlockEVL(game_evl, "GME")
                persistent._seen_ever[unlock_evl] = True
                
                
                
                
                unlock_ev = mas_getEV(unlock_evl)
                if unlock_ev:
                    mas_rmEVL(unlock_evl)
                    unlock_ev.conditional = None
                    unlock_ev.action = None
                    unlock_ev.unlocked = False
                    unlock_ev.shown_count = 1



        mas_unlockEVL("bye_illseeyou", "BYE")

        if seen_event("monika_veggies"):
            mas_unlockEVL("monika_eating_meat","EVE")


        for _key in ("hangman", "piano"):
            if _key not in persistent.ever_won:
                persistent.ever_won[_key] = False


        steam_install_detected_ev = mas_getEV("mas_steam_install_detected")
        if (
            steam_install_detected_ev is not None
            and steam_install_detected_ev.conditional is not None
        ):
            steam_install_detected_ev.conditional = "store.mas_globals.is_steam"


        new_stats = {
            "practice_wins": 0,
            "practice_losses": 0,
            "practice_draws": 0
        }

        persistent._mas_chess_stats.update(new_stats)

        mas_setEVLPropValues(
            'mas_bday_spent_time_with',
            start_date = datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date = datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3))
        )

    return


label v0_11_4(version="v0_11_4"):
    python:

        mas_eraseTopic("mas_mood_lucky", persistent._mas_mood_database)


        OLD_NEW_RANDCHAT_MAP = {
            0: 6,
            1: 5,
            2: 4,
            3: 3,
            4: 2,
            5: 1,
            6: 0
        }

        persistent._mas_randchat_freq = OLD_NEW_RANDCHAT_MAP.get(persistent._mas_randchat_freq, mas_randchat.NORMAL)


        if seen_event('monika_japan'):
            mas_unlockEVL("monika_remembrance", "EVE")


        bad_topic_derand_list = [
            "monika_fear",
            "monika_soft_rains",
            "monika_whispers",
            "monika_eternity",
            "monika_dying_same_day"
        ]








        mas_unlockEVL("bye_illseeyou", "BYE")

        if seen_event("monika_veggies"):
            mas_unlockEVL("monika_eating_meat","EVE")


        for _key in ("hangman", "piano"):
            if _key not in persistent.ever_won:
                persistent.ever_won[_key] = False


        steam_install_detected_ev = mas_getEV("mas_steam_install_detected")
        if (
            steam_install_detected_ev is not None
            and steam_install_detected_ev.conditional is not None
        ):
            steam_install_detected_ev.conditional = "store.mas_globals.is_steam"


        new_stats = {
            "practice_wins": 0,
            "practice_losses": 0,
            "practice_draws": 0
        }

        persistent._mas_chess_stats.update(new_stats)

        mas_setEVLPropValues(
            'mas_bday_spent_time_with',
            start_date = datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date = datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3))
        )

    return


label v0_11_3(version="v0_11_3"):
    python:

        for song_ev in mas_songs.song_db.itervalues():
            if (
                song_ev.eventlabel not in ["mas_song_aiwfc", "mas_song_merry_christmas_baby"]
                and mas_songs.TYPE_LONG not in song_ev.category
            ):
                song_ev.random=True


        if mas_isFirstSeshPast(datetime.date(2020, 4, 4)):
            
            
            
            
            persistent._mas_pool_unlocks += store.mas_xp.level() * 4


        for consumable_id in persistent._mas_consumable_map.iterkeys():
            cons = mas_getConsumable(consumable_id)
            
            if cons and cons.getStock() > cons.max_stock_amount:
                persistent._mas_consumable_map[cons.consumable_id]["servings_left"] = cons.max_stock_amount


        mas_unlockEVL("monika_kiss", "EVE")


        tod_list = [
            "monika_gtod_tip002",
            "monika_gtod_tip003",
            "monika_gtod_tip004",
            "monika_gtod_tip005",
            "monika_gtod_tip006",
            "monika_gtod_tip007",
            "monika_gtod_tip008",
            "monika_gtod_tip009",
            "monika_gtod_tip010",
            "monika_ptod_tip002",
            "monika_ptod_tip003",
            "monika_ptod_tip005",
            "monika_ptod_tip006",
            "monika_ptod_tip008",
            "monika_ptod_tip009"
        ]

        for tod_label in tod_list:
            tod_ev = mas_getEV(tod_label)
            
            if tod_ev is not None:
                if tod_ev.pool:
                    tod_ev.unlocked = True
                
                else:
                    tod_ev.pool = True
                    tod_ev.action = EV_ACT_UNLOCK


        filenames_to_rename = [
            "losiento",
            "losiento.txt",
            "perdoname.txt",
            "puedes oirme.txt",
            "por favor escucha.txt",
            "sorpresa.txt",
            "jejeje.txt",
            "secreto.txt",
            "para ti.txt",
            "Mi unico amor.txt"
        ]

        for fn in filenames_to_rename:
            try:
                os.rename(
                    renpy.config.basedir + "/{0}".format(fn),
                    renpy.config.basedir + "/characters/{0}".format(fn)
                )
            except:
                pass


        try:
            os.rename(
                renpy.config.basedir + "/jejeje.txt",
                renpy.config.basedir + "/characters/ehehe.txt"
            )
        except:
            mas_utils.trydel(renpy.config.basedir + "/jejeje.txt")


        pool_unlock_list = [
            "monika_meta",
            "monika_difficulty",
            "monika_ddlc",
            "monika_justification",
            "monika_girlfriend",
            "monika_herself",
            "monika_birthday",
            "monika_sayhappybirthday"
        ]

        for pool_label in pool_unlock_list:
            mas_unlockEVL(pool_label,"EVE")


        if not seen_event("monika_player_appearance"):
            player_appearance_ev = mas_getEV("monika_player_appearance")
            if player_appearance_ev:
                player_appearance_ev.random = False
                player_appearance_ev.conditional = "seen_event('mas_gender')"
                player_appearance_ev.action = EV_ACT_RANDOM


        if not mas_isWinter() and not seen_event("greeting_ourreality"):
            mas_unlockEVL("greeting_ourreality", "GRE")


        gender_ev = mas_getEV("mas_gender")
        if gender_ev:
            
            gender_ev.conditional = None
            
            preferredname_ev = mas_getEV("mas_preferredname")
            if preferredname_ev:
                
                preferredname_ev.conditional = None
            
            
            
            if gender_ev.last_seen:
                if preferredname_ev and not preferredname_ev.last_seen:
                    preferredname_ev.start_date = gender_ev.last_seen + datetime.timedelta(hours=2)
            
            
            else:
                gender_ev.start_date = mas_getFirstSesh() + datetime.timedelta(minutes=30)


        if persistent._mas_pm_do_smoke:
            mas_unlockEVL("monika_smoking_quit","EVE")


        leaving_already_ev = mas_getEV("bye_leaving_already")
        if leaving_already_ev:
            leaving_already_ev.random = True
            leaving_already_ev.conditional = "mas_getSessionLength() <= datetime.timedelta(minutes=20)"

        if not mas_isWinter():
            mas_lockEVL("monika_snowballfight", "EVE")
    return


label v0_11_1(version="v0_11_1"):
    python:

        mas_eraseTopic("monika_careful")


        safeDel("game_unlocks")

        chess_unlock_ev = mas_getEV("mas_unlock_chess")
        if chess_unlock_ev and chess_unlock_ev.action:
            chess_unlock_ev.conditional = (
                "store.mas_xp.level() >= 8 "
                "or store.mas_games._total_games_played() > 99"
            )

        hangman_unlock_ev = mas_getEV("mas_unlock_hangman")
        if hangman_unlock_ev and hangman_unlock_ev.action:
            hangman_unlock_ev.conditional = (
                "store.mas_xp.level() >= 4 "
                "or store.mas_games._total_games_played() > 49"
            )

        piano_unlock_ev = mas_getEV("mas_unlock_piano")
        if piano_unlock_ev and piano_unlock_ev.action:
            piano_unlock_ev.conditional="store.mas_xp.level() >= 12"


        if (
            persistent._mas_chess_stats["wins"]
            or persistent._mas_chess_stats["losses"]
            or persistent._mas_chess_stats["draws"]
        ):
            mas_unlockGame("chess")
            mas_stripEVL("mas_unlock_chess", list_pop=True)
            persistent._seen_ever["mas_unlock_chess"] = True
            chess_unlock_ev = mas_getEV("mas_unlock_chess")
            if chess_unlock_ev:
                chess_unlock_ev.shown_count = 1


        session_count = mas_getTotalSessions()
        if mas_isFirstSeshPast(datetime.date(2020, 4, 4)) and session_count > 0:
            
            
            
            
            ahs = (
                store.mas_utils.td2hr(mas_getTotalPlaytime())
                / float(session_count)
            )
            
            
            if ahs < 2:
                lvls_gained, xptnl = store.mas_xp._grant_on_pt()
                
                
                
                
                if persistent._mas_xp_lvl < lvls_gained or lvls_gained == 0:
                    
                    
                    persistent._mas_pool_unlocks += (
                        lvls_gained - persistent._mas_xp_lvl
                    )
                    
                    
                    persistent._mas_xp_tnl = xptnl
                    persistent._mas_xp_lvl = lvls_gained

        credits_song_ev = mas_getEV('monika_credits_song')
        if credits_song_ev and credits_song_ev.action:
            credits_song_ev.conditional = (
                "store.mas_anni.pastOneMonth() "
                "and seen_event('mas_unlock_piano')"
            )

        if "orcaramelo_twintails" in persistent._mas_selspr_hair_db:
            persistent._mas_selspr_hair_db["orcaramelo_twintails"] = (True, True)




        if persistent._mas_monika_nickname != "Monika" and mas_awk_name_comp.search(persistent._mas_monika_nickname):
            persistent._mas_grandfathered_nickname = persistent._mas_monika_nickname


        persistent._mas_pm_called_moni_a_bad_name = persistent._mas_called_moni_a_bad_name


        safeDel("_mas_called_moni_a_bad_name")


        if not persistent._mas_penname:
            persistent._mas_penname = None

    return


label v0_11_0(version="v0_11_0"):
    python:

        for cons_id in persistent._mas_consumable_map.iterkeys():
            persistent._mas_consumable_map[cons_id]["has_restock_warned"] = False



        coffee_cons = mas_getConsumable("coffee")
        if coffee_cons and persistent._mas_acs_enable_coffee:
            
            if not coffee_cons.enabled():
                coffee_cons.restock(renpy.random.randint(40, 60))
                
                
                coffee_cons.enable()
            
            
            
            if persistent._mas_coffee_cups_drank:
                persistent._mas_consumable_map["coffee"]["times_had"] += persistent._mas_coffee_cups_drank
            
            
            safeDel("_mas_coffee_cups_drank")
            safeDel("_mas_acs_enable_coffee")
            safeDel("_mas_coffee_been_given")

        hotchoc_cons = mas_getConsumable("hotchoc")
        if hotchoc_cons and seen_event("mas_reaction_hotchocolate"):
            hotchoc_cons.restock(renpy.random.randint(40, 60))
            
            
            if persistent._mas_c_hotchoc_cups_drank:
                persistent._mas_consumable_map["hotchoc"]["times_had"] += persistent._mas_c_hotchoc_cups_drank
            
            
            safeDel("_mas_c_hotchoc_cups_drank")
            safeDel("_mas_acs_enable_hotchoc")
            safeDel("_mas_c_hotchoc_been_given")


        song_pool_ev = mas_getEV("monika_sing_song_pool")
        if song_pool_ev:
            song_pool_ev.conditional = None
            song_pool_ev.action = None
            song_pool_ev.unlocked = mas_songs.hasUnlockedSongs()


        persistent._mas_acs_bab_list = None


        if mas_o31CostumeWorn(mas_clothes_marisa):
            persistent._mas_selspr_clothes_db["marisa"] = (True, False)
            persistent._mas_selspr_acs_db["marisa_witchhat"] = (True, False)
            persistent._mas_selspr_hair_db["downtiedstrand"] = (True, True)


        new_greetings_conditions = {
            "greeting_back": "store.mas_getAbsenceLength() >= datetime.timedelta(hours=12)",
            "greeting_back2": "store.mas_getAbsenceLength() >= datetime.timedelta(hours=20)",
            "greeting_back3": "store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            "greeting_back4": "store.mas_getAbsenceLength() >= datetime.timedelta(hours=10)",
            "greeting_visit3": "store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            "greeting_back5": "store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            "greeting_visit4": "store.mas_getAbsenceLength() <= datetime.timedelta(hours=3)",
            "greeting_visit9": "store.mas_getAbsenceLength() >= datetime.timedelta(hours=1)",
            "greeting_hamlet": "store.mas_getAbsenceLength() >= datetime.timedelta(days=7)"
        }

        for gr_label, conditional in new_greetings_conditions.iteritems():
            gr_ev = mas_getEV(gr_label)
            if gr_ev:
                gr_ev.conditional = conditional


        changename_ev = mas_getEV("monika_changename")
        if changename_ev:
            changename_ev.pool=True



        mas_eraseTopic("monika_morning")
        mas_eraseTopic("monika_evening")



        topic_transfer_map = {
            "monika_gender_redo": "gender_redo",
            "mas_gender": "gender",
            "mas_preferredname": "preferredname",
            "mas_unlock_hangman": "unlock_hangman",
            "mas_unlock_chess": "unlock_chess",
            "mas_unlock_piano": "unlock_piano"
        }


        game_evl_map = {
            "mas_unlock_hangman": "hangman",
            "mas_unlock_chess": "chess",
            "mas_unlock_piano": "piano"
        }


        intro_topic_map = {
            "monika_gender_redo": "mas_gender",
            "monika_changename": "mas_preferredname"
        }

        for new_evl, old_evl in topic_transfer_map.iteritems():
            mas_transferTopicData(new_evl, old_evl, persistent.event_database)
            
            
            
            if seen_event(new_evl) or mas_isGameUnlocked(game_evl_map.get(new_evl, "")):
                mas_stripEVL(new_evl, list_pop=True)
                
                
                persistent._seen_ever[new_evl] = True
                
                
                if mas_isGameUnlocked(game_evl_map.get(new_evl, "")):
                    mas_getEV(new_evl).shown_count = 1
            
            
            
            if new_evl in intro_topic_map and mas_getEV(new_evl).unlocked:
                prereq_evl = intro_topic_map[new_evl]
                
                persistent._seen_ever[prereq_evl] = True
                
                mas_getEV(prereq_evl).shown_count = 1
                
                mas_stripEVL(prereq_evl, list_pop=True)


        if mas_getEV("monika_changename").unlocked:
            persistent._seen_ever[intro_topic_map["monika_changename"]] = True
            mas_getEV(intro_topic_map["monika_changename"]).shown_count = 1
            mas_stripEVL(intro_topic_map["monika_changename"], list_pop=True)


        cave_ev = mas_getEV("monika_allegory_of_the_cave")
        if cave_ev and cave_ev.shown_count > 0:
            perspective_ev = mas_getEV("monika_multi_perspective_approach")
            if perspective_ev:
                perspective_ev.random = True

        credits_ev = mas_getEV("monika_credits_song")
        if credits_ev:
            credits_ev.random = False
            
            
            credits_ev.conditional = "store.mas_anni.pastOneMonth()"
            credits_ev.action = EV_ACT_QUEUE
            credits_ev.unlocked = False


        if renpy.seen_label("greeting_tears"):
            beingvirtual_ev = mas_getEV("monika_being_virtual")
            
            if beingvirtual_ev:
                beingvirtual_ev.start_date = datetime.datetime.now() + datetime.timedelta(days=2)


        concert_ev = mas_getEV("monika_concerts")
        if concert_ev and concert_ev.action is not None:
            concert_ev.conditional = "mas_seenLabels(['monika_jazz', 'monika_orchestra', 'monika_rock', 'monika_vocaloid', 'monika_rap'], seen_all=True)"


        if persistent.playerxp is not None:
            lvls_gained, xptnl = store.mas_xp._grant_on_pt()
            
            
            persistent._mas_xp_tnl = xptnl
            persistent._mas_xp_lvl = lvls_gained
            persistent._mas_pool_unlocks = lvls_gained
            
            persistent.playerxp = None


        mas_unlockEVL("monika_good_tod", "EVE")

        dystopias_ev = mas_getEV("monika_dystopias")
        if dystopias_ev and dystopias_ev.action is not None:
            dystopias_ev.conditional= "mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world'], seen_all=True)"

        if persistent._mas_pm_have_fam is None:
            mas_hideEVL("monika_familygathering","EVE",derandom=True)
    return


label v0_10_7(version="v0_10_7"):
    python:

        if renpy.seen_label("monika_valentines_start"):
            persistent._mas_history_archives[2018]["f14.actions.spent_f14"] = True


        f14_spent_time_ev = mas_getEV("mas_f14_monika_spent_time_with")
        if f14_spent_time_ev:
            f14_spent_time_ev.conditional = "persistent._mas_f14_spent_f14"

        vday_spent_ev = mas_getEV("mas_f14_monika_spent_time_with")
        if vday_spent_ev:
            vday_spent_ev.start_date = datetime.datetime.combine(mas_f14, datetime.time(hour=18))
            vday_spent_ev.end_date = datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=3))


        vday_origins_ev = mas_getEV('mas_f14_monika_vday_origins')
        if vday_origins_ev:
            vday_origins_ev.action = EV_ACT_UNLOCK
            vday_origins_ev.pool = True
            
            if not mas_isF14():
                vday_origins_ev.unlocked=False


        mistletoe_ev = mas_getEV("mas_d25_monika_mistletoe")
        carolling_ev = mas_getEV("mas_d25_monika_carolling")

        if mistletoe_ev:
            mistletoe_ev.action = EV_ACT_RANDOM

        if carolling_ev:
            carolling_ev.action = EV_ACT_RANDOM
    return


label v0_10_6(version="v0_10_6"):
    python:


        if persistent._mas_likes_rain:
            safeDel("_mas_likes_rain")


        mas_eraseTopic("mas_topic_unbookmark")

        seen_bday_surprise = False

        bday_list = [
            'mas_player_bday_listen',
            'mas_player_bday_knock_no_listen',
            'mas_player_bday_opendoor',
            'mas_player_bday_surprise'
        ]


        for bday_label in bday_list:
            if renpy.seen_label(bday_label):
                seen_bday_surprise = True

        if seen_bday_surprise:
            
            other_bday_list = [
                'mas_player_bday_ret_on_bday',
                'mas_player_bday_no_restart',
                'mas_player_bday_upset_minus',
                'mas_player_bday_other_holiday'
            ]
            
            
            years_list = []
            
            
            for other_bday_label in other_bday_list:
                if mas_getEV(other_bday_label) is not None and mas_getEV(other_bday_label).last_seen is not None:
                    years_list.append(mas_getEV(other_bday_label).last_seen.year)
            
            
            if persistent._mas_player_bday is not None and persistent._mas_player_confirmed_bday:
                bdate_ev = mas_getEV('mas_birthdate')
                if bdate_ev is not None and bdate_ev.last_seen is not None:
                    seen_date = bdate_ev.last_seen.date()
                    if seen_date == mas_player_bday_curr().replace(year=seen_date.year):
                        years_list.append(seen_date.year)
            
            
            if persistent._mas_player_bday_spent_time and datetime.date.today().year not in years_list:
                persistent._mas_player_bday_saw_surprise = True
            
            spent_time_hist = mas_HistVerify("player_bday.spent_time",True)
            
            if spent_time_hist[0]:
                for year in spent_time_hist[1]:
                    if year not in years_list:
                        persistent._mas_history_archives[year]["player_bday.saw_surprise"] = True


        for ev in mas_fun_facts.fun_fact_db.itervalues():
            if ev.shown_count:
                ev.unlocked = True


        birthdate_ev = mas_getEV("mas_birthdate")
        bday = persistent._mas_player_bday
        if (
                birthdate_ev is not None
                and birthdate_ev.last_seen is not None
                and bday is not None
        ):
            seen_year = birthdate_ev.last_seen.year
            
            
            
            
            
            if renpy.seen_label("v0_9_0") and seen_year - bday.year < 5:
                mas_addDelayedAction(16)


        safeDel("_mas_mood_bday_last")
        safeDel("_mas_mood_bday_lies")
        safeDel("_mas_mood_bday_locked")
    return


label v0_10_5(version="v0_10_5"):
    python:

        ev = mas_getEV("mas_bday_surprise_party_hint")
        if ev:
            ev.start_date = mas_monika_birthday - datetime.timedelta(days=7)
            ev.end_date = mas_monika_birthday - datetime.timedelta(days=2)
            ev.action = EV_ACT_RANDOM

        ev = mas_getEV("mas_bday_pool_happy_bday")
        if ev:
            ev.start_date = mas_monika_birthday
            ev.end_date = mas_monika_birthday + datetime.timedelta(days=1)
            ev.action = EV_ACT_UNLOCK

        ev = mas_getEV("mas_bday_spent_time_with")
        if ev:
            ev.start_date = datetime.datetime.combine(mas_monika_birthday, datetime.time(20))
            ev.end_date = datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1))
            ev.conditional = "mas_recognizedBday()"
            ev.action = EV_ACT_QUEUE

        ev = mas_getEV("mas_bday_postbday_notimespent")
        if ev:
            ev.start_date = mas_monika_birthday + datetime.timedelta(days=1)
            ev.end_date = mas_monika_birthday + datetime.timedelta(days=8)
            ev.conditional = (
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            )
            ev.action = EV_ACT_PUSH


        fun_facts_evls = {
            
            "mas_fun_facts_1": "mas_fun_fact_librocubiculartist",
            "mas_fun_facts_2": "mas_fun_fact_menu_currency",
            "mas_fun_facts_3": "mas_fun_fact_love_you",
            "mas_fun_facts_4": "mas_fun_fact_morpheus",
            "mas_fun_facts_5": "mas_fun_fact_otter_hand_holding",
            "mas_fun_facts_6": "mas_fun_fact_chess",
            "mas_fun_facts_7": "mas_fun_fact_struck_by_lightning",
            "mas_fun_facts_8": "mas_fun_fact_honey",
            "mas_fun_facts_9": "mas_fun_fact_vincent_van_gone",
            "mas_fun_facts_10": "mas_fun_fact_king_snakes",
            "mas_fun_facts_11": "mas_fun_fact_strength",
            "mas_fun_facts_12": "mas_fun_fact_reindeer_eyes",
            "mas_fun_facts_13": "mas_fun_fact_bananas",
            "mas_fun_facts_14": "mas_fun_fact_pens",
            "mas_fun_facts_15": "mas_fun_fact_density",
            "mas_fun_facts_16": "mas_fun_fact_binky",
            "mas_fun_facts_17": "mas_fun_fact_windows_games",
            "mas_fun_facts_18": "mas_fun_fact_mental_word_processing",
            "mas_fun_facts_19": "mas_fun_fact_I_am",
            "mas_fun_facts_20": "mas_fun_fact_low_rates",

            
            "mas_bad_facts_1": "mas_bad_fact_10_percent",
            "mas_bad_facts_2": "mas_bad_fact_taste_areas",
            "mas_bad_facts_3": "mas_bad_fact_antivaxx",
            "mas_bad_facts_4": "mas_bad_fact_tree_moss",
        }

        for old_evl, new_evl in fun_facts_evls.iteritems():
            mas_transferTopicData(
                new_evl,
                old_evl,
                persistent._mas_fun_facts_database,
                transfer_unlocked=False
            )

        islands_evs = {
            "mas_monika_upsidedownisland": "mas_island_upsidedownisland",
            "mas_monika_glitchesmess": "mas_island_glitchedmess",
            "mas_monika_cherry_blossom_tree": "mas_island_cherry_blossom_tree",
            "mas_monika_cherry_blossom1": "mas_island_cherry_blossom1",
            "mas_monika_cherry_blossom2": "mas_island_cherry_blossom2",
            "mas_monika_cherry_blossom3": "mas_island_cherry_blossom3",
            "mas_monika_cherry_blossom4": "mas_island_cherry_blossom4",
            "mas_monika_sky": "mas_island_sky",
            "mas_monika_day1": "mas_island_day1",
            "mas_monika_day2": "mas_island_day2",
            "mas_monika_day3": "mas_island_day3",
            "mas_monika_night1": "mas_island_night1",
            "mas_monika_night2": "mas_island_night2",
            "mas_monika_night3": "mas_island_night3",
            "mas_monika_daynight1": "mas_island_daynight1",
            "mas_monika_daynight2": "mas_island_daynight2"
        }

        for old_label, new_label in islands_evs.iteritems():
            mas_transferTopicSeen(old_label, new_label)


        persistent._mas_pm_plays_instrument = persistent.instrument
        persistent._mas_pm_likes_rain = persistent._mas_likes_rain


        safeDel("instrument")
        safeDel("_mas_likes_rain")


        mas_eraseTopic("mas_topic_unbookmark")



        seen_bday_surprise = False

        bday_list = [
            'mas_player_bday_listen',
            'mas_player_bday_knock_no_listen',
            'mas_player_bday_opendoor',
            'mas_player_bday_surprise'
        ]


        for bday_label in bday_list:
            if renpy.seen_label(bday_label):
                seen_bday_surprise = True

        if seen_bday_surprise:
            
            other_bday_list = [
                'mas_player_bday_ret_on_bday',
                'mas_player_bday_no_restart',
                'mas_player_bday_upset_minus',
                'mas_player_bday_other_holiday'
            ]
            
            
            years_list = []
            
            
            for other_bday_label in other_bday_list:
                if mas_getEV(other_bday_label) is not None and mas_getEV(other_bday_label).last_seen is not None:
                    years_list.append(mas_getEV(other_bday_label).last_seen.year)
            
            
            if persistent._mas_player_bday is not None and persistent._mas_player_confirmed_bday:
                bdate_ev = mas_getEV('mas_birthdate')
                if bdate_ev is not None and bdate_ev.last_seen is not None:
                    seen_date = bdate_ev.last_seen.date()
                    if seen_date == mas_player_bday_curr().replace(year=seen_date.year):
                        years_list.append(seen_date.year)
            
            
            if persistent._mas_player_bday_spent_time and datetime.date.today().year not in years_list:
                persistent._mas_player_bday_saw_surprise = True
            
            spent_time_hist = mas_HistVerify("player_bday.spent_time",True)
            
            if spent_time_hist[0]:
                for year in spent_time_hist[1]:
                    if year not in years_list:
                        persistent._mas_history_archives[year]["player_bday.saw_surprise"] = True
    return


label v0_10_4(version="v0_10_4"):
    python:

        mas_eraseTopic("monika_scary_stories", persistent.event_database)

        if renpy.seen_label("monika_aiwfc"):
            
            mas_unlockEVL("mas_song_aiwfc", "SNG")
            mas_lockEVL("monika_aiwfc", "EVE")
            aiwfc_ev = mas_getEV("monika_aiwfc")
            
            if aiwfc_ev:
                aiwfc_ev.action = EV_ACT_QUEUE
                aiwfc_ev.pool = False
                
                
                aiwfc_sng_ev = mas_getEV("mas_song_aiwfc")
                if aiwfc_sng_ev:
                    aiwfc_sng_ev.shown_count += aiwfc_ev.shown_count
                    aiwfc_sng_ev.last_seen = aiwfc_ev.last_seen
                    
                    
                    aiwfc_ev.last_seen = None


        ev = mas_getEV("mas_d25_monika_holiday_intro")
        if ev:
            ev.conditional=(
                "not persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday() "
                "and not persistent._mas_d25_intro_seen"
            )

        ev = mas_getEV("mas_d25_monika_holiday_intro_upset")
        if ev:
            ev.conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday()"
            )
            ev.action = EV_ACT_QUEUE

        islands_ev = store.mas_getEV("mas_monika_islands")
        if (
                islands_ev is not None
                and islands_ev.shown_count > 0
            ):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

        ev = mas_getEV("mas_d25_postd25_notimespent")
        if ev:
            ev.end_date = mas_d25p + datetime.timedelta(days=6)

        ev = mas_getEV("mas_d25_monika_christmas")
        if ev:
            ev.conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_lastSeenInYear('mas_d25_monika_christmas')"
            )






        if persistent._mas_first_kiss and persistent._mas_first_kiss.date().replace(year=mas_d25.year) == mas_d25:
            persistent._mas_poems_seen["poem_d25_1"] = 1


        if renpy.seen_label("monika_valentines_start"):
            persistent._mas_poems_seen["poem_f14_1"] = 1
            
            
            if mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
                persistent._mas_poems_seen["poem_f14_2"] = 1


        elif mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
            persistent._mas_poems_seen["poem_f14_1"] = 1


        if renpy.seen_label("mas_player_bday_cake") or renpy.seen_label("mas_player_bday_card"):
            persistent._mas_poems_seen["poem_pbday_1"] = 1


        push_list = [
            "mas_d25_monika_christmas_eve",
            "mas_nye_monika_nyd",
            "mas_f14_no_time_spent",
            "mas_bday_postbday_notimespent"
        ]

        for ev_label in push_list:
            ev = mas_getEV(ev_label)
            if ev:
                ev.action = EV_ACT_PUSH

        ev = mas_getEV("mas_monikai_detected")
        if ev:
            ev.action = EV_ACT_QUEUE


        ev = mas_getEV("monika_backpacking")
        if ev:
            ev.random = not mas_isWinter()

        ev = mas_getEV("monika_outdoors")
        if ev:
            ev.random = not mas_isWinter()


        if persistent._mas_pm_would_like_mt_peak is None:
            ev = mas_getEV("monika_mountain")
            if ev:
                ev.random = not mas_isWinter()


        mas_weather_snow.unlocked=True
        mas_weather_thunder.unlocked=True
        mas_weather.saveMWData()


        if persistent._mas_pm_got_a_fresh_start:
            persistent._mas_history_archives[2018]["pm.actions.monika.got_fresh_start"] = True
            
            
            if not persistent._mas_aff_before_fresh_start:
                persistent._mas_aff_before_fresh_start = mas_HistLookup("aff.before_fresh_start", 2018)
    return


label v0_10_3(version="v0_10_3"):
    python:

        if isinstance(persistent._mas_player_bookmarked, dict):
            persistent._mas_player_bookmarked = persistent._mas_player_bookmarked.keys()

        if isinstance(persistent._mas_player_derandomed, dict):
            persistent._mas_player_derandomed = persistent._mas_player_derandomed.keys()

    return


label v0_10_2(version="v0_10_2"):
    python:


        if renpy.seen_label("greeting_o31_marisa"):
            mas_o31SetCostumeWorn_n("marisa", 2018)
        if renpy.seen_label("greeting_o31_rin"):
            mas_o31SetCostumeWorn_n("rin", 2018)


        ev_label_list = [
            ("monika_song_lover_boy", "mas_song_lover_boy"),
            ("monika_song_need_you", "mas_song_need_you"),
            ("monika_song_i_will", "mas_song_i_will"),
            ("monika_song_belong_together", "mas_song_belong_together"),
            ("monika_song_your_song", "mas_song_your_song"),
            ("monika_song_with_you", "mas_song_with_you"),
            ("monika_song_dream", "mas_song_dream"),
        ]

        for old_ev_label, new_ev_label in ev_label_list:
            new_ev = mas_getEV(new_ev_label)
            
            if old_ev_label in persistent.event_database:
                old_ev = Event(
                    persistent.event_database,
                    old_ev_label
                )
            else:
                old_ev = None
            
            if new_ev is not None and old_ev is not None:
                
                new_ev.unlocked = old_ev.unlocked
                
                
                new_ev.shown_count += old_ev.shown_count
                
                
                if old_ev.shown_count > 0:
                    new_ev.random = False
                
                
                if old_ev.last_seen is not None and (new_ev.last_seen is None or new_ev.last_seen <= old_ev.last_seen):
                    new_ev.last_seen = old_ev.last_seen
                
                
                mas_transferTopicSeen(old_ev_label, new_ev_label)
                
                
                mas_eraseTopic(old_ev_label, persistent.event_database)

        if 'monika_clothes_select' in persistent._seen_ever:
            persistent._seen_ever['monika_event_clothes_select'] = True

        trick_treat = mas_getEV('bye_trick_or_treat')
        if trick_treat is not None:
            trick_treat.unlocked = False
            trick_treat.start_date = mas_o31
            trick_treat.end_date = mas_o31+datetime.timedelta(days=1)
            trick_treat.action = action=EV_ACT_UNLOCK
            trick_treat.years = []



        d25_ev_label_list = [
            ("mas_d25_monika_holiday_intro", mas_d25),
            ("mas_d25_monika_holiday_intro_upset", mas_d25p),
            ("mas_d25_monika_carolling", mas_d25p),
            ("mas_d25_monika_mistletoe", mas_d25p),
            ("monika_aiwfc", mas_d25p)
        ]

        for ev_label, end_date in d25_ev_label_list:
            ev = mas_getEV(ev_label)
            
            if ev:
                ev.start_date = mas_d25c_start
                ev.end_date = end_date
                
                MASUndoActionRule.adjust_rule(
                    ev,
                    datetime.datetime.combine(mas_d25c_start, datetime.time()),
                    ev.end_date
                )
    return


label v0_10_1(version="v0_10_1"):

    if datetime.date.today() < mas_monika_birthday:
        $ persistent._mas_bday_no_time_spent = True
        $ persistent._mas_bday_no_recognize = True


    python:
        ev_label_list = [
            
            ("mas_d25_monika_holiday_intro", "not persistent._mas_d25_started_upset"),
            ("mas_d25_monika_holiday_intro_upset", "persistent._mas_d25_started_upset"),
            ("mas_d25_monika_christmas", "persistent._mas_d25_in_d25_mode"),
            ("mas_d25_monika_carolling", "persistent._mas_d25_in_d25_mode"),
            ("mas_d25_monika_mistletoe", "persistent._mas_d25_in_d25_mode"),
            ("monika_aiwfc", "persistent._mas_d25_in_d25_mode"),

            
            ("mas_pf14_monika_lovey_dovey", None),
            ("mas_f14_monika_valentines_intro", None),
            ("mas_f14_no_time_spent", "not persistent._mas_f14_spent_f14"),

            
            ("mas_bday_spent_time_with", "mas_recognizedBday()"),
            ("mas_bday_postbday_notimespent", "not mas_recognizedBday() and not persistent._mas_bday_gone_over_bday"),
            ("mas_bday_surprise_party_hint", None),
            ("mas_bday_pool_happy_bday", None),
        ]

        for ev_label, conditional in ev_label_list:
            ev = mas_getEV(ev_label)
            
            if ev:
                ev.conditional = conditional



        mas_getEV("mas_bday_postbday_notimespent").action=EV_ACT_QUEUE


        cond_str = " and not mas_isMonikaBirthday() "

        ev_list_1 = [
            ("mas_player_bday_upset_minus", cond_str),
            ('mas_player_bday_ret_on_bday', cond_str),
            ('mas_player_bday_no_restart', cond_str)
        ]

        for ev_label, conditional in ev_list_1:
            ev = mas_getEV(ev_label)
            
            if ev and ev.conditional:
                ev.conditional += conditional

    return


label v0_10_0(version="v0_10_0"):
    python:
        ev_label_list = [
            ("monika_whatwatching","mas_wrs_youtube", persistent._mas_windowreacts_database),
            ("monika_lookingat","mas_wrs_r34m", persistent._mas_windowreacts_database),
            ("monika_monikamoddev","mas_wrs_monikamoddev", persistent._mas_windowreacts_database),
            ("mas_scary_story_o_tei","mas_story_o_tei", persistent._mas_story_database)
        ]


        for old_ev_label, new_ev_label, ev_db in ev_label_list:
            ev = mas_getEV(new_ev_label)
            if old_ev_label in ev_db:
                old_ev = Event(
                    ev_db,
                    old_ev_label
                )
            else:
                old_ev = None
            
            if ev is not None and old_ev is not None:
                ev.unlocked = old_ev.unlocked
                
                ev.shown_count += old_ev.shown_count
                
                if old_ev.last_seen is not None and (ev.last_seen is None or ev.last_seen <= old_ev.last_seen):
                    ev.last_seen = old_ev.last_seen
                
                mas_transferTopicSeen(old_ev_label, new_ev_label)
                
                
                mas_eraseTopic(old_ev_label, ev_db)


        if not renpy.seen_label("greeting_tears"):
            mas_unlockEVL("greeting_tears", "GRE")


        family_ev = mas_getEV("monika_family")
        if family_ev is not None:
            family_ev.pool = True


        concert_ev = mas_getEV("monika_concerts")
        if concert_ev is not None and concert_ev.shown_count == 0:
            concert_ev.random = False
            concert_ev.conditional = (
                "renpy.seen_label('monika_jazz') "
                "and renpy.seen_label('monika_orchestra') "
                "and renpy.seen_label('monika_rock') "
                "and renpy.seen_label('monika_vocaloid') "
                "and renpy.seen_label('monika_rap')"
            )
            concert_ev.action = EV_ACT_RANDOM


        dt_now = datetime.datetime.now()



        mhs_922 = store.mas_history.getMHS("922")
        if (
                mhs_922 is not None
                and mhs_922.trigger.month == 9
                and mhs_922.trigger.day == 30
        ):
            
            mhs_922.setTrigger(datetime.datetime(dt_now.year + 1, 1, 6))
            
            
            mhs_922.use_year_before = True

        mhs_pbday = store.mas_history.getMHS("player_bday")
        if (
                mhs_pbday is not None
                and mhs_pbday.trigger.month == 1
                and mhs_pbday.trigger.day == 1
                and persistent._mas_player_bday is not None
        ):
            store.mas_player_bday_event.correct_pbday_mhs(
                persistent._mas_player_bday
            )
            
            now_dt = datetime.datetime.now()
            trig_now = mhs_pbday.trigger.replace(year=now_dt.year)
            if trig_now < now_dt:
                
                
                mhs_pbday.trigger = trig_now
                mhs_pbday.save() 
                renpy.save_persistent()

        mhs_o31 = store.mas_history.getMHS("o31")
        if (
                mhs_o31 is not None
                and mhs_o31.trigger.month == 11
                and mhs_o31.trigger.day == 2
        ):
            
            mhs_o31.setTrigger(datetime.datetime(dt_now.year + 1, 1, 6))
            
            
            mhs_o31.use_year_before = True


        store.mas_history.saveMHSData()


        clothes_sel_ev = mas_getEV("monika_clothes_select")
        if clothes_sel_ev is not None:
            clothes_sel_ev.unlocked = True

    return


label v0_9_5(version="v0_9_5"):
    python:

        if persistent._mas_likes_rain:
            mas_unlockEVL("monika_rain_holdme", "EVE")


        why_ev = mas_getEV('monika_why')
        if why_ev is not None:
            why_ev.pool = False
            if not renpy.seen_label('monika_why') or not mas_anni.pastOneMonth():
                why_ev.random = True
    return


label v0_9_4(version="v0_9_4"):
    python:

        if persistent._mas_greeting_type != store.mas_greetings.TYPE_LONG_ABSENCE:
            
            persistent._mas_long_absence = False


        if mas_getEV('monika_ptod_tip001').unlocked:
            
            mas_hideEVL("monika_ptod_tip000", "EVE", lock=True)


        outfit_ev = mas_getEV("monika_outfit")
        if outfit_ev is not None and renpy.seen_label(outfit_ev.eventlabel):
            outfit_ev.unlocked = True

    return


label v0_9_2(version="v0_9_2"):
    python:


        mas_eraseTopic("monika_szs", persistent.event_database)


        if persistent._mas_pm_have_fam is False:
            mas_hideEVL("monika_familygathering", "EVE", derandom=True)







        sleigh_ev = mas_getEV("monika_sleigh")
        if "mas_d25_monika_sleigh" in persistent.event_database:
            old_sleigh_ev = Event(
                persistent.event_database,
                "mas_d25_monika_sleigh"
            )
        else:
            old_sleigh_ev = None
        if sleigh_ev is not None and old_sleigh_ev is not None:
            sleigh_ev.unlock_date = old_sleigh_ev.unlock_date
            sleigh_ev.shown_count = old_sleigh_ev.shown_count
            sleigh_ev.last_seen = old_sleigh_ev.last_seen
            mas_transferTopicSeen("mas_d25_monika_sleigh", "monika_sleigh")
            
            
            mas_eraseTopic("mas_d25_monika_sleigh", persistent.event_database)


        mas_lockEVL("mas_pf14_monika_lovey_dovey","EVE")


        def fix_tip(tip_ev, prev_tip_ev):
            
            tip_ev.random = False
            
            if renpy.seen_label(tip_ev.eventlabel):
                
                tip_ev.unlocked = True
                tip_ev.conditional = None
                tip_ev.pool = True
                tip_ev.action = None
                
                if tip_ev.shown_count <= 0:
                    tip_ev.shown_count = 1
                
                if tip_ev.unlock_date is None:
                    tip_ev.unlock_date = datetime.datetime.now()
                
                
                if prev_tip_ev is not None:
                    persistent._seen_ever[prev_tip_ev.eventlabel] = True
            
            else:
                
                tip_ev.unlocked = False
                tip_ev.shown_count = 0
                
                if prev_tip_ev is None:
                    
                    tip_ev.pool = True
                    tip_ev.conditional = None
                    tip_ev.action = None
                    tip_ev.unlock_date = datetime.datetime.now()
                
                else:
                    
                    tip_ev.conditional = (
                        "seen_event('" + prev_tip_ev.eventlabel + "')"
                    )
                    tip_ev.pool = False
                    tip_ev.action = EV_ACT_POOL
                    tip_ev.unlock_date = None


        wt_5 = mas_getEV("monika_writingtip5")
        wt_4 = mas_getEV("monika_writingtip4")
        wt_3 = mas_getEV("monika_writingtip3")
        wt_2 = mas_getEV("monika_writingtip2")
        wt_1 = mas_getEV("monika_writingtip1")
        if wt_5 is not None:
            fix_tip(wt_5, wt_4)

        if wt_4 is not None:
            fix_tip(wt_4, wt_3)

        if wt_3 is not None:
            fix_tip(wt_3, wt_2)

        if wt_2 is not None:
            fix_tip(wt_2, wt_1)

        if wt_1 is not None:
            fix_tip(wt_1, None)


    return


label v0_9_1(version="v0_9_1"):
    python:

        if (
                persistent._mas_pm_likes_spoops
                and not renpy.seen_label("greeting_ghost")
            ):
            mas_unlockEVL("greeting_ghost", "GRE")


        plush_ev = mas_getEV("monika_plushie")
        if plush_ev is not None:
            plush_ev.unlocked = False
            plush_ev.category = None
            plush_ev.prompt = "monika_plushie"

        if renpy.seen_label("monika_driving"):
            mas_unlockEVL("monika_vehicle","EVE")

    return


label v0_9_0(version="v0_9_0"):
    python:

        if persistent._mas_called_moni_a_bad_name:
            nickname_ev = mas_getEV("monika_affection_nickname")
            if nickname_ev is not None:
                nickname_ev.unlocked = True





        d25e_ev = mas_getEV("mas_d25_monika_christmas_eve")
        if d25e_ev is not None:
            d25e_ev.conditional = (
                "persistent._mas_d25_in_d25_mode "
            )
            d25e_ev.action = EV_ACT_QUEUE

        d25_hi_ev = mas_getEV("mas_d25_monika_holiday_intro")
        if d25_hi_ev is not None:
            d25_hi_ev.conditional = (
                "not persistent._mas_d25_intro_seen "
                "and not persistent._mas_d25_started_upset "
            )
            d25_hi_ev.action = EV_ACT_PUSH

        d25_ev = mas_getEV("mas_d25_monika_christmas")
        if d25_ev is not None:
            d25_ev.conditional = (
                "persistent._mas_d25_in_d25_mode "
                "and not persistent._mas_d25_spent_d25"
            )
            d25_ev.action = EV_ACT_PUSH

        d25p_nts = mas_getEV("mas_d25_postd25_notimespent")
        if d25p_nts is not None:
            d25p_nts.conditional = (
                "not persistent._mas_d25_spent_d25"
            )
            d25p_nts.action = EV_ACT_PUSH

        d25_hiu_ev = mas_getEV("mas_d25_monika_holiday_intro_upset")
        if d25_hiu_ev is not None:
            d25_hiu_ev.conditional = (
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
            )
            d25_hiu_ev.action = EV_ACT_PUSH

        d25_stm_ev = mas_getEV("mas_d25_spent_time_monika")
        if d25_stm_ev is not None:
            d25_stm_ev.conditional = (
                "persistent._mas_d25_in_d25_mode "
            )
            d25_stm_ev.action = EV_ACT_QUEUE
            d25_stm_ev.start_date = datetime.datetime.combine(
                mas_d25,
                datetime.time(hour=20)
            )
            d25_stm_ev.end_date = datetime.datetime.combine(
                mas_d25p,
                datetime.time(hour=1)
            )
            d25_stm_ev.years = []
            Event._verifyAndSetDatesEV(d25_stm_ev)


        nye_yr_ev = mas_getEV("monika_nye_year_review")
        if nye_yr_ev is not None:
            nye_yr_ev.action = EV_ACT_PUSH

        nyd_ev = mas_getEV("mas_nye_monika_nyd")
        if nyd_ev is not None:
            nyd_ev.action = EV_ACT_QUEUE

        res_ev = mas_getEV("monika_resolutions")
        if res_ev is not None:
            res_ev.action = EV_ACT_QUEUE


        if (
                persistent._mas_player_bday is not None
                and not persistent._mas_player_confirmed_bday
            ):
            mas_bd_ev = mas_getEV("mas_birthdate")
            if mas_bd_ev is not None:
                mas_bd_ev.conditional = "True"
                mas_bd_ev.action = EV_ACT_QUEUE


        for gre_label, gre_ev in store.evhand.greeting_database.iteritems():
            
            gre_ev.random = False


        if renpy.seen_label("monika_rain"):
            mas_unlockEVL("monika_rain", "EVE")


        if not renpy.seen_label("greeting_ourreality"):
            mas_unlockEVL("greeting_ourreality", "GRE")


        if persistent._mas_acs_enable_quetzalplushie:
            mas_hideEVL("monika_pets", "EVE", derandom=True)


        d25_mis_ev = mas_getEV("mas_d25_monika_mistletoe")
        if d25_mis_ev is not None:
            
            mas_addDelayedAction(10)

    return


label v0_8_14(version="v0_8_14"):
    python:

        rain_ev = mas_getEV("monika_rain")
        if rain_ev is not None and not rain_ev.random:
            rain_ev.unlocked = True

    return


label v0_8_13(version="v0_8_13"):
    python:


        d25_sp_tm = mas_getEV("mas_d25_spent_time_monika")
        if d25_sp_tm is not None:
            if (
                    d25_sp_tm.start_date.hour != 20
                    or d25_sp_tm.end_date.hour != 1
                ):
                d25_sp_tm.start_date = datetime.datetime.combine(
                    mas_d25,
                    datetime.time(hour=20)
                )
                
                
                d25_sp_tm.end_date = datetime.datetime.combine(
                    mas_d25p,
                    datetime.time(hour=1)
                )
                
                Event._verifyAndSetDatesEV(d25_sp_tm)

        d25_ce = mas_getEV("mas_d25_monika_christmas_eve")
        if d25_ce is not None:
            if d25_ce.start_date.hour != 20:
                d25_ce.start_date = datetime.datetime.combine(
                    mas_d25e,
                    datetime.time(hour=20)
                )
                
                d25_ce.end_date = mas_d25
                
                Event._verifyAndSetDatesEV(d25_ce)

        nye_re = mas_getEV("monika_nye_year_review")
        if nye_re is not None:
            if (
                    nye_re.start_date.hour != 19
                    or nye_re.end_date.hour != 23
                ):
                nye_re.start_date = datetime.datetime.combine(
                    mas_nye,
                    datetime.time(hour=19)
                )
                
                nye_re.end_date = datetime.datetime.combine(
                    mas_nye,
                    datetime.time(hour=23)
                )
                
                Event._verifyAndSetDatesEV(nye_re)


        bday_sp = mas_getEV("mas_bday_spent_time_with")
        if bday_sp is not None:
            if (
                    bday_sp.start_date.hour != 22
                    or bday_sp.end_date.hour != 23
                ):
                bday_sp.start_date = datetime.datetime.combine(
                    mas_monika_birthday,
                    datetime.time(hour=22)
                )
                
                bday_sp.end_date = datetime.datetime.combine(
                    mas_monika_birthday,
                    datetime.time(hour=23, minute=59)
                )
                
                Event._verifyAndSetDatesEV(bday_sp)

    return


label v0_8_11(version="v0_8_11"):
    python:
        import store.mas_compliments as mas_comp
        import store.evhand as evhand


        thanks_ev = mas_comp.compliment_database.get(
            "mas_compliment_thanks",
            None
        )
        if thanks_ev:
            
            thanks_ev.conditional = None
            thanks_ev.action = None
            
            
            if not renpy.seen_label(thanks_ev.eventlabel):
                thanks_ev.unlocked = True


        if not persistent._mas_called_moni_a_bad_name:
            mas_unlockEventLabel("monika_affection_nickname")

        if (
                not persistent._mas_pm_taken_monika_out
                and len(persistent._mas_dockstat_checkin_log) > 0
            ):
            persistent._mas_pm_taken_monika_out = True

    return


label v0_8_10(version="v0_8_10"):
    python:
        import store.evhand as evhand
        import store.mas_history as mas_history


        if persistent.sessions is not None:
            first_sesh = persistent.sessions.get("first_session", None)
            if first_sesh:
                store.mas_anni.reset_annis(first_sesh)
                store.mas_anni.unlock_past_annis()


        if (
                persistent._mas_bday_sbd_aff_given is not None
                and persistent._mas_bday_sbd_aff_given > 0
            ):
            persistent._mas_history_archives[2018][
                "922.actions.surprise.aff_given"
            ] = persistent._mas_bday_sbd_aff_given


        unlockEventLabel(
            "i_greeting_monikaroom",
            store.evhand.greeting_database
        )
        if not persistent._mas_hair_changed:
            unlockEventLabel(
                "greeting_hairdown",
                store.evhand.greeting_database
            )


        changename_ev = evhand.event_database.get("monika_changename", None)
        if changename_ev and renpy.seen_label("preferredname"):
            changename_ev.unlocked = True
            changename_ev.pool = True
            persistent._seen_ever["monika_changename"] = True


        family_ev = evhand.event_database.get("monika_family", None)
        if family_ev:
            family_ev.random = False


        persistent._mas_zz_lupd_ex_v.append(version)

    return


label v0_8_9(version="v0_8_9"):
    python:
        import store.evhand as evhand


        mas_eraseTopic("monika_weddingring", persistent.event_database)



        horror_ev = evhand.event_database.get("monika_horror", None)
        if horror_ev:
            horror_ev.conditional = (
                "datetime.date(2018, 10, 26) <= datetime.date.today() "
                "<= datetime.date(2018, 10, 30)"
            )
            horror_ev.action = EV_ACT_QUEUE

    return



label v0_8_6(version="v0_8_6"):
    python:
        import store.evhand as evhand
        import datetime


        genderredo_ev = evhand.event_database.get("gender_redo", None)
        if genderredo_ev and renpy.seen_label("gender"):
            genderredo_ev.unlocked = True
            genderredo_ev.pool = True
            
            
            persistent._seen_ever["gender_redo"] = True


        new_char_ev = evhand.event_database.get("mas_new_character_file", None)
        if new_char_ev and not renpy.seen_label("mas_new_character_file"):
            new_char_ev.conditional = "True"
            new_char_ev.action = EV_ACT_PUSH

    return


label v0_8_4(version="v0_8_4"):
    python:

        import store.evhand as evhand
        import store.mas_stories as mas_stories


        updateTopicIDs(version)









        best_evlabel = "monika_bestgirl"
        best_comlabel = "mas_compliment_bestgirl"
        best_ev = Event(persistent.event_database, eventlabel=best_evlabel)
        best_compliment = mas_compliments.compliment_database.get(best_comlabel, None)
        best_lockdata = None


        if best_evlabel in Event.INIT_LOCKDB:
            best_lockdata = Event.INIT_LOCKDB.pop(best_evlabel)

        if best_compliment:
            
            best_compliment.shown_count = best_ev.shown_count
            best_compliment.last_seen = best_ev.last_seen
            
            if best_lockdata:
                
                Event.INIT_LOCKDB[best_comlabel] = best_lockdata


        if best_evlabel in persistent.event_database:
            persistent.event_database.pop(best_evlabel)


        persistent._mas_zz_lupd_ex_v.append(version)


    return


label v0_8_3(version="v0_8_3"):
    python:
        import datetime
        import store.evhand as evhand


        ex_ev = evhand.event_database.get("monika_explain", None)
        if ex_ev is not None:
            ex_ev.random = False
            ex_ev.pool = True


        kiz_ev = evhand.event_database.get("monika_kizuna", None)
        if kiz_ev is not None and not renpy.seen_label(kiz_ev.eventlabel):
            kiz_ev.action = EV_ACT_POOL
            kiz_ev.unlocked = False
            kiz_ev.pool = False
            kiz_ev.conditional = "seen_event('greeting_hai_domo')"


        curr_level = store.mas_xp.level()
        if curr_level > 25:
            persistent._mas_pool_unlocks = int(curr_level / 2)


        derandomable = [
            "monika_natsuki_letter",
            "monika_prom",
            "monika_beach",
            "monika_asks_family",
            "monika_smoking",
            "monika_otaku",
            "monika_jazz",
            "monika_orchestra",
            "monika_meditation",
            "monika_sports",
            "monika_weddingring",
            "monika_icecream",
            "monika_japanese",
            "monika_haterReaction",
            "monika_cities",
            "monika_images",
            "monika_rain",
            "monika_selfesteem",
            "monika_yellowwp",
            "monika_familygathering"
        ]
        for topic in derandomable:
            ev = evhand.event_database.get(topic, None)
            if renpy.seen_label(topic) and ev:
                ev.unlocked = True
                ev.unlock_date = datetime.datetime.now()



        persistent._mas_zz_lupd_ex_v.append(version)

    return


label v0_8_2(version="v0_8_2"):
    python:
        import store.mas_anni as mas_anni


        mas_anni.reset_annis(persistent.sessions["first_session"])

    return


label v0_8_1(version="v0_8_1"):
    python:
        import store.evhand as evhand
        import store.mas_stories as mas_stories



        m_ff = evhand.event_database.get("monika_fastfood", None)
        if m_ff:
            hideEvent(m_ff, derandom=True)
            m_ff.pool = True


        updateTopicIDs(version)




        writ_5 = evhand.event_database.get("monika_writingtip5", None)
        if writ_5 and not renpy.seen_label(writ_5.eventlabel):
            writ_5.pool = False
            writ_5.conditional = "seen_event('monika_writingtip4')"
            writ_5.action = EV_ACT_POOL


        writ_4 = evhand.event_database.get("monika_writingtip4", None)
        if writ_4 and not renpy.seen_label(writ_4.eventlabel):
            writ_4.pool = False
            writ_4.conditional = "seen_event('monika_writingtip3')"
            writ_4.action = EV_ACT_POOL



        writ_3_old = persistent.event_database.get("monika_write", None)

        if writ_3_old is not None:
            persistent.event_database.pop("monika_write")

        writ_3 = evhand.event_database.get("monika_writingtip3", None)

        if writ_3_old is not None and writ_3 is not None:
            writ_3.unlocked = writ_3_old[Event.T_EVENT_NAMES["unlocked"]]
            writ_3.unlock_date = writ_3_old[Event.T_EVENT_NAMES["unlock_date"]]

        if writ_3 and not renpy.seen_label(writ_3.eventlabel):
            writ_3.pool = False
            writ_3.conditional = "seen_event('monika_writingtip2')"
            writ_3.action = EV_ACT_POOL


        zero_t = "monika_writingtip"
        old_t = "monika_writingtip1"
        new_t = "monika_writingtip2"
        if zero_t in persistent.event_database:
            
            
            
            mas_transferTopicSeen(old_t, new_t)
            old_t_ev = mas_getEV(old_t)
            new_t_ev = mas_getEV(new_t)
            
            if old_t_ev is not None and new_t_ev is not None:
                new_t_ev.unlocked = old_t_ev.unlocked
                new_t_ev.unlock_date = old_t_ev.unlock_date
            
            if new_t_ev and not renpy.seen_label(new_t):
                new_t_ev.conditional = "seen_event('monika_writingtip1')"
                new_t_ev.pool = False
                new_t_ev.action = EV_ACT_POOL
            
            
            zero_t_d = persistent.event_database.pop(zero_t)
            mas_transferTopicSeen(zero_t, old_t)
            if old_t_ev is not None:
                old_t_ev.unlocked = zero_t_d[Event.T_EVENT_NAMES["unlocked"]]
                old_t_ev.unlock_date = zero_t_d[
                    Event.T_EVENT_NAMES["unlock_date"]
                ]


        persistent._mas_enable_random_repeats = None
        persistent._mas_monika_repeated_herself = None


        annis = (
            "anni_1week",
            "anni_1month",
            "anni_3month",
            "anni_6month"
        ) 
        for anni in annis:
            anni_ev = evhand.event_database.get(anni, None)
            
            if anni_ev and isPast(anni_ev):
                
                persistent._seen_ever[anni] = True
                anni_ev.unlocked = True


        music_ev = Event(persistent.event_database, eventlabel="monika_music2")
        music_ev.unlocked = False
        music_ev.random = False









        ravel_evlabel = "monika_ravel"
        ravel_stlabel = "mas_story_ravel"
        ravel_ev = Event(persistent.event_database, eventlabel=ravel_evlabel)
        ravel_story = mas_stories.story_database.get(ravel_stlabel, None)
        ravel_lockdata = None


        if ravel_evlabel in Event.INIT_LOCKDB:
            ravel_lockdata = Event.INIT_LOCKDB.pop(ravel_evlabel)

        if ravel_story:
            
            ravel_story.shown_count = ravel_ev.shown_count
            ravel_story.last_seen = ravel_ev.last_seen
            
            if ravel_lockdata:
                
                Event.INIT_LOCKDB[ravel_stlabel] = ravel_lockdata


        if ravel_evlabel in persistent.event_database:
            persistent.event_database.pop(ravel_evlabel)


    return


label v0_8_0(version="v0_8_0"):
    python:
        import store.evhand as evhand


        if (
                renpy.seen_label("monika_changename")
                or renpy.seen_label("preferredname")
            ):
            evhand.event_database["monika_changename"].unlocked = True

        annis = (
            "anni_1week",
            "anni_1month",
            "anni_3month",
            "anni_6month"
        ) 
        for anni in annis:
            if isPast(evhand.event_database[anni]):
                persistent._seen_ever[anni] = True

        persistent = updateTopicIDs(version)


        for k in updates.topics["v0_8_0"]:
            mas_eraseTopic(k, persistent.event_database)



        for k in updates.topics["v0_7_4"]:
            mas_eraseTopic(k, persistent.event_database)


        m_ff = evhand.event_database.get("monika_fastfood", None)
        if m_ff:
            hideEvent(m_ff, derandom=True)
            m_ff.pool = True

    return



label v0_7_4(version="v0_7_4"):
    python:



        import os
        try: os.remove(config.basedir + "/game/valentines.rpyc")
        except: pass


        try: os.remove(config.basedir + "/game/white-day.rpyc")
        except: pass



        import store.evhand as evhand
        import store.mas_utils as mas_utils
        import datetime
        fullday = datetime.timedelta(days=1)
        threeday = datetime.timedelta(days=3)
        week = datetime.timedelta(days=7)
        month = datetime.timedelta(days=30)
        year = datetime.timedelta(days=365)
        def _month_adjuster(key, months, span):
            new_anni_date = mas_utils.add_months(
                mas_utils.sod(persistent.sessions["first_session"]),
                months
            )
            evhand.event_database[key].start_date = new_anni_date
            evhand.event_database[key].end_date = new_anni_date + span


        _month_adjuster("anni_1month", 1, fullday)
        _month_adjuster("anni_3month", 3, fullday)
        _month_adjuster("anni_6month", 6, fullday)
        _month_adjuster("anni_1", 12, fullday)
        _month_adjuster("anni_2", 24, fullday)
        _month_adjuster("anni_3", 36, threeday)
        _month_adjuster("anni_4", 48, week)
        _month_adjuster("anni_5", 60, week)
        _month_adjuster("anni_10", 120, month)
        _month_adjuster("anni_20", 240, year)
        evhand.event_database["anni_100"].start_date = mas_utils.add_months(
            mas_utils.sod(persistent.sessions["first_session"]),
            1200
        )



        for k in evhand.farewell_database:
            
            evhand.farewell_database[k].unlocked = True

        updateTopicIDs(version)



        for k in updates.topics["v0_7_4"]:
            mas_eraseTopic(k, persistent.event_database)

    return


label v0_7_2(version="v0_7_2"):
    python:
        import store.evhand as evhand


        for k in evhand.event_database:
            event = evhand.event_database[k]
            if (renpy.seen_label(event.eventlabel)
                and (event.random or event.action == EV_ACT_RANDOM)):
                event.unlocked = True
                event.conditional = None




    return


label v0_7_1(version="v0_7_1"):
    python:

        if persistent.you is not None:
            persistent._mas_you_chr = persistent.you

        if persistent.pnml_data is not None:
            persistent._mas_pnml_data = persistent.pnml_data

        if renpy.seen_label("zz_play_piano"):
            removeTopicID("zz_play_piano")
            persistent._seen_ever["mas_piano_start"] = True

    return


label v0_7_0(version="v0_7_0"):
    python:

        import os
        try: os.remove(config.basedir + "/game/christmas.rpyc")
        except: pass


        updateTopicIDs(version)

        temp_event_list = list(persistent.event_list)

        import store.evhand as evhand
        for k in evhand.event_database:
            event = evhand.event_database[k]
            if (renpy.seen_label(event.eventlabel)
                and (event.pool
                    or event.random
                    or event.action == EV_ACT_POOL
                    or event.action == EV_ACT_RANDOM
                )):
                event.unlocked = True
                event.conditional = None


        persistent.event_list = temp_event_list


        if seen_event('game_chess'):
            mas_unlockGame("chess")


        if seen_event('preferredname'):
            evhand.event_database["monika_changename"].unlocked = True

    return


label v0_4_0(version="v0_4_0"):
    python:

        persistent.monika_random_topics = None




    return


label v0_3_0(version="v0_3_0"):
    python:

        removeTopicID("monika_piano")
        removeTopicID("monika_college")


        updateTopicIDs(version)
    return



























































label mas_lupd_v0_12_3_1:
    python:

        if seen_event("mas_monika_islands"):
            mas_island_event.start_progression()
            
            
            persistent._mas_islands_start_lvl = 0
            mas_island_event.advance_progression()

    return

label mas_lupd_v0_12_0:
    python:

        first_sesh = mas_getFirstSesh()
        if first_sesh.month == 2 and first_sesh.day == 29:
            mas_anni.reset_annis(first_sesh)

    return

label mas_lupd_v0_8_10:
    python:
        import store.mas_selspr as mas_selspr


        if persistent._mas_hair_changed:
            mas_selspr.unlock_hair(mas_hair_down)
            unlockEventLabel("monika_hair_select")


        if persistent._mas_o31_seen_costumes is not None:
            if persistent._mas_o31_seen_costumes.get("marisa", False):
                mas_selspr.unlock_clothes(mas_clothes_marisa)




        mas_selspr.save_selectables()

    return

label mas_lupd_v0_8_4:
    python:

        import store.evhand as evhand
        import datetime

        aff_to_grant = 0

        if renpy.seen_label('monika_christmas'):
            aff_to_grant += 10

        if renpy.seen_label('monika_newyear1'):
            aff_to_grant += 5

        if renpy.seen_label('monika_valentines_chocolates'):
            aff_to_grant += 15

        if renpy.seen_label('monika_found'):
            aff_to_grant += 10

        moni_love = evhand.event_database.get("monika_love", None)

        if moni_love is not None:
            aff_to_grant += (moni_love.shown_count * 7) / 100

        aff_to_grant += (datetime.datetime.now() - persistent.sessions["first_session"]).days / 3

        if aff_to_grant > 200:
            aff_to_grant = 200

        _mas_AffLoad()
        store.mas_gainAffection(aff_to_grant,bypass=True)
        _mas_AffSave()

    return

label mas_lupd_v0_8_3:
    python:

        if persistent.sessions:
            first_sesh = persistent.sessions.get("first_session", None)
            if first_sesh:
                store.mas_anni.reset_annis(first_sesh)

    return


init 999 python:
    for _m1_updates__temp_version in persistent._mas_zz_lupd_ex_v:
        _m1_updates__lupd_v = "mas_lupd_" + _m1_updates__temp_version
        if renpy.has_label(_m1_updates__lupd_v) and not renpy.seen_label(_m1_updates__lupd_v):
            renpy.call_in_new_context(_m1_updates__lupd_v)

    persistent._mas_zz_lupd_ex_v = list()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
