


init -1 python in mas_db_merging:
    import store

    def merge_db(source, dest):
        """
        Merges the given source database into the given destination db

        IN:
            source - source database to merge from
            dest - destination database to merge into
        """
        dest.update(source)


    def merge_post0810():
        """
        Runs a specific set of merges, particularly for the merge that
        happend after version 0.8.10.
        """
        
        
        if store.persistent._mas_compliments_database is not None:
            merge_db(
                store.persistent._mas_compliments_database,
                store.persistent.event_database
            )



init -1 python:
    @store.mas_utils.deprecated(use_instead="mas_versions.clear", should_raise=True)
    def clearUpdateStructs():
        """DEPRECATED
        Use mas_versions.clear instead
        """
        store.mas_versions.clear()


init 9 python:
    store.mas_versions.init()



define updates.version_updates = mas_versions.version_updates
define updates.topics = mas_versions.topics


init -2 python in mas_versions:
    import store
    import store.mas_utils as mas_utils
    from store.mas_ev_data_ver import _verify_str


    version_updates = {}




    topics = {}


    def add_steps(version_struct):
        """
        Adds versions to the version updates dict.

        IN:
            version_struct - dict with versions in special version notation.
                Keys: version to update to, as string
                Vals: versions to update from, as string or tuple of strings
        """
        for to_ver, from_vers in version_struct.items(): 
            to_ver_str = _vdot2vstr(to_ver)
            if _verify_str(from_vers, False):
                version_updates[_vdot2vstr(from_vers)] = to_ver_str
            else:
                
                for from_ver in from_vers:
                    version_updates[_vdot2vstr(from_ver)] = to_ver_str


    def clear():
        """
        Clears the update data structures
        """
        version_updates.clear()
        topics.clear()


    def init():
        """
        Initializes the update data structures
        """
        
        
        
        
        
        
        
        add_steps({
            
            "0.12.13": "0.12.12",
            "0.12.12": ("0.12.11", "0.12.10"),
            "0.12.10": ("0.12.9", "0.12.8.6"),
            "0.12.8.6": ("0.12.8.5", "0.12.8.4", "0.12.8.3"),
            "0.12.8.3": ("0.12.8.2", "0.12.8.1"),
            "0.12.8.1": "0.12.8",
            "0.12.8": "0.12.7",
            "0.12.7": ("0.12.6", "0.12.5"),
            "0.12.5": "0.12.4",
            "0.12.4": ("0.12.3.3", "0.12.3.2"),
            "0.12.3.2": "0.12.3.1",
            "0.12.3.1": ("0.12.3", "0.12.2.4", "0.12.2.3"),
            "0.12.2.3": "0.12.2.2",
            "0.12.2.2": ("0.12.2.1", "0.12.2"),
            "0.12.2": "0.12.1.2",
            "0.12.1.2": ("0.12.1.1", "0.12.1"),
            "0.12.1": "0.12.0",
            "0.12.0": "0.11.9.3",
            "0.11.9.3": ("0.11.9.2", "0.11.9.1"),
            "0.11.9.1": "0.11.9",
            "0.11.9": ("0.11.8", "0.11.7"),
            "0.11.7": "0.11.6",
            "0.11.6": "0.11.5",
            "0.11.5": "0.11.4",
            "0.11.4": "0.11.3",
            "0.11.3": ("0.11.2", "0.11.1"),
            "0.11.1": "0.11.0",
            "0.11.0": "0.10.7",

            "0.10.7": "0.10.6",
            "0.10.6": "0.10.5",
            "0.10.5": "0.10.4",
            "0.10.4": "0.10.3",
            "0.10.3": "0.10.2",
            "0.10.2": "0.10.1",
            "0.10.1": "0.10.0",
            "0.10.0": "0.9.5",

            "0.9.5": "0.9.4",
            "0.9.4": ("0.9.3", "0.9.2"),
            "0.9.2": "0.9.1",
            "0.9.1": "0.9.0",
            "0.9.0": "0.8.14",

            "0.8.14": "0.8.13",
            "0.8.13": ("0.8.12", "0.8.11"),
            "0.8.11": "0.8.10",
            "0.8.10": "0.8.9",
            "0.8.9": ("0.8.8", "0.8.7", "0.8.6"),
            "0.8.6": ("0.8.5", "0.8.4"),
            "0.8.4": "0.8.3",
            "0.8.3": "0.8.2",
            "0.8.2": "0.8.1",
            "0.8.1": "0.8.0",
            "0.8.0": "0.7.4",

            "0.7.4": ("0.7.3", "0.7.2"),
            "0.7.2": "0.7.1",
            "0.7.1": "0.7.0",
            "0.7.0": ("0.6.3", "0.6.2", "0.6.1"),
            "0.6.1": ("0.6.0", "0.5.1"),
            "0.5.1": ("0.5.0", "0.4.0", "0.3.3"),
            "0.3.3": "0.3.2",
            "0.3.2": "0.3.1",
            "0.3.1": "0.3.0",
            "0.3.0": "0.2.2",
        })
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        updates = store.updates
        
        
        updates.topics[_vdot2vstr("0.8.11")] = {
            "monika_snowman": None,
            "monika_relax": None,
            "monika_hypothermia": None,
            "monika_whatiwant": None
        }
        
        
        updates.topics[_vdot2vstr("0.8.4")] = {
            "monika_bestgirl": "mas_compliment_bestgirl"
        }
        
        
        updates.topics[_vdot2vstr("0.8.1")] = {
            "monika_write": "monika_writingtip3",
            "mas_random_ask": None,
            "monika_ravel": "mas_story_ravel"
        }
        
        
        updates.topics[_vdot2vstr("0.8.0")] = {
            "monika_love2": None
        }
        
        
        updates.topics[_vdot2vstr("0.7.4")] = {
            "monika_playerhappy": None,
            "monika_bad_day": None
        }
        
        
        changedIDs = {
            "monika_deleted": None,
            "monika_whatever": None,
            "monika_games": None,
            "monika_chess": None,
            "monika_pong": None,
            "monika_vulgarity": None,
            "monika_goodbye": None,
            "monika_night": None
        }
        updates.topics[_vdot2vstr("0.7.0")] = changedIDs
        
        
        changedIDs = {
            "monika_piano": None
        }
        updates.topics[_vdot2vstr("0.6.1")] = changedIDs
        
        
        changedIDs = dict()
        changedIDs["monika_music"] = None
        changedIDs["monika_keitai"] = None
        changedIDs["monika_subahibi"] = None
        changedIDs["monika_reddit"] = None
        changedIDs["monika_shill"] = None
        changedIDs["monika_dracula"] = None
        changedIDs["monika_undertale"] = None
        changedIDs["monika_recursion"] = None
        changedIDs["monika_lain"] = None
        changedIDs["monika_kyon"] = None
        changedIDs["monika_water"] = None
        changedIDs["monika_computer"] = None
        updates.topics[_vdot2vstr("0.5.1")] = changedIDs
        
        
        changedIDs = dict()
        changedIDs["monika_monika"] = None
        updates.topics[_vdot2vstr("0.3.2")] = changedIDs
        
        
        changedIDs = dict()
        changedIDs["monika_ghosts"] = "monika_whispers"
        updates.topics[_vdot2vstr("0.3.1")] = changedIDs
        
        
        
        
        changedIDs = None
        changedIDs = dict()
        changedIDs["ch30_1"] = "monika_god"
        changedIDs["ch30_2"] = "monika_death"
        changedIDs["ch30_3"] = "monika_bad_day"
        changedIDs["ch30_4"] = "monika_sleep"
        changedIDs["ch30_5"] = "monika_sayori"
        changedIDs["ch30_6"] = "monika_japan"
        changedIDs["ch30_7"] = "monika_high_school"
        changedIDs["ch30_8"] = "monika_nihilism"
        changedIDs["ch30_9"] = "monika_piano"
        changedIDs["ch30_10"] = "monika_twitter"
        changedIDs["ch30_11"] = "monika_portraitof"
        changedIDs["ch30_12"] = "monika_veggies"
        changedIDs["ch30_13"] = "monika_saved"
        changedIDs["ch30_14"] = "monika_secrets"
        changedIDs["ch30_15"] = "monika_color"
        changedIDs["ch30_16"] = "monika_music"
        changedIDs["ch30_17"] = "monika_listener"
        changedIDs["ch30_18"] = "monika_spicy"
        changedIDs["ch30_19"] = "monika_why"
        changedIDs["ch30_20"] = "monika_okayeveryone"
        changedIDs["ch30_21"] = "monika_ghosts"
        changedIDs["ch30_22"] = "monika_archetype"
        changedIDs["ch30_23"] = "monika_tea"
        changedIDs["ch30_24"] = "monika_favoritegame"
        changedIDs["ch30_25"] = "monika_smash"
        
        changedIDs["ch30_27"] = "monika_lastpoem"
        changedIDs["ch30_28"] = "monika_anxious"
        changedIDs["ch30_29"] = "monika_friends"
        changedIDs["ch30_30"] = "monika_college"
        changedIDs["ch30_31"] = "monika_middleschool"
        changedIDs["ch30_32"] = "monika_outfit"
        changedIDs["ch30_33"] = "monika_horror"
        changedIDs["ch30_34"] = "monika_rap"
        changedIDs["ch30_35"] = "monika_wine"
        changedIDs["ch30_36"] = "monika_date"
        changedIDs["ch30_37"] = "monika_kiss"
        changedIDs["ch30_38"] = "monika_yuri"
        changedIDs["ch30_39"] = "monika_writingtip"
        changedIDs["ch30_40"] = "monika_habits"
        changedIDs["ch30_41"] = "monika_creative"
        changedIDs["ch30_42"] = "monika_deleted"
        changedIDs["ch30_43"] = "monika_keitai"
        changedIDs["ch30_44"] = "monika_simulated"
        changedIDs["ch30_45"] = "monika_rain"
        changedIDs["ch30_46"] = "monika_closeness"
        changedIDs["ch30_47"] = "monika_confidence"
        changedIDs["ch30_48"] = "monika_carryme"
        changedIDs["ch30_49"] = "monika_debate"
        changedIDs["ch30_50"] = "monika_internet"
        changedIDs["ch30_51"] = "monika_lazy"
        changedIDs["ch30_52"] = "monika_mentalillness"
        changedIDs["ch30_53"] = "monika_read"
        changedIDs["ch30_54"] = "monika_festival"
        changedIDs["ch30_55"] = "monika_tsundere"
        changedIDs["ch30_56"] = "monika_introduce"
        changedIDs["ch30_57"] = "monika_cold"
        changedIDs["ch30_58"] = "monika_housewife"
        changedIDs["ch30_59"] = "monika_route"
        changedIDs["monika_literatureclub"] = "monika_ddlc"
        changedIDs["monika_religion"] = None
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        updates.topics[_vdot2vstr("0.3.0")] = changedIDs
        
        
        changedIDs = None


    def _vdot2vstr(version_str):
        """
        Converts a version string that uses dots to the v#_#_# notation

        IN:
            version_str - version string with dots #.#.#.#

        RETURNS: version string in the standard version notation:
            v#_#_#_#
        """
        return "v" + "_".join(version_str.split("."))
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
