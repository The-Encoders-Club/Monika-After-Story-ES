

init -999 python in _mas_dm_dm:
    import store


    dm_data_version = 2






    per_dbs = [

        
        store.persistent.event_database,
        store.persistent._mas_compliments_database,
        store.persistent.farewell_database,
        store.persistent.greeting_database,
        store.persistent._mas_mood_database,
        store.persistent._mas_story_database,
        store.persistent._mas_apology_database
    ]


    lock_db = store.persistent._mas_event_init_lockdb



    def _m1_zz_dm__add_idxs(_db, _key, _exp_len, idx_d_list):
        """INTERNAL ONLY
        adds indexes to the given key to the given db
        """
        
        ignore_len = _exp_len < 0
        
        _data = list(_db[_key])
        
        if ignore_len or len(_data) == _exp_len:
            for idx, idx_data in idx_d_list:
                _data.insert(idx, idx_data)
            
            _db[_key] = tuple(_data)


    def _m1_zz_dm__rm_idxs(_db, _key, _exp_len, idx_list):
        """INTERNAL ONLY
        removes indexes off the given key off the given db
        """
        
        ignore_len = _exp_len <= 0
        
        _data = list(_db[_key])
        
        if ignore_len or len(_data) == _exp_len:
            for idx in idx_list:
                _data.pop(idx)
            
            _db[_key] = tuple(_data)




    def add_idxs(_db, _key, _exp_len, *idxs_d):
        """
        Adds indexes to the given key

        NOTE: indxs_d is added in reverse order.

        IN:
            _db - database to add indexes to
            _key - key of the item to add indexes to
            _exp_len - the length the item should have prior to addition
                Pass in less than 0 to ignore length checks
            *idxs_d - tuples of the following format:
                [0]: index to add
                [1]: data to add at index
        """
        if len(idxs_d) < 1:
            return
        
        _m1_zz_dm__add_idxs(_db, _key, _exp_len, sorted(idxs_d, reverse=True))


    def add_idxs_db(_db, _exp_len, *idxs_d):
        """
        Adds indexes to items in the given db

        IN:
            _db - database to add indexes to
            _exp_len - the length the item shoudl have prior to additoin
                Pass in 0 or less to ignore length checks
            *idxs_d - tuples of the following format:
                [0]: index to add
                [1]: data to add at index
        """
        
        if len(idxs_d) < 1:
            return
        
        idxs_d_rev = sorted(idxs_d, reverse=True)
        
        for item in _db:
            _m1_zz_dm__add_idxs(_db, item, _exp_len, idxs_d_rev)


    def rm_idxs(_db, _key, _exp_len, *idxs):
        """
        removes indexes off the given key off the given db

        IN:
            _db - database to remove indexes off of
            _key - key of the item to remove indexes off of
            _exp_len - the length the item should have prior to removal.
                Pass in 0 or less to ignore length checks.
            *idxs - indexes to remove
                If nothing is passed, nothing happens.
        """
        
        if len(idxs) < 1:
            return
        
        _m1_zz_dm__rm_idxs(_db, _key, _exp_len, sorted(idxs, reverse=True))


    def rm_idxs_db(_db, _exp_len, *idxs):
        """
        Removes indexes off items in the given db

        IN:
            _db - database to remove indexes off of
            _exp_len - the length the item should have prior to removal
                Pass in 0 or less to ignore length checks
            *idxs - indexes to remove
                if Nothing is passsed, nothing happens
        """
        if len(idxs) < 1 or _db is None:
            return
        
        idxs_rev = sorted(idxs, reverse=True)
        
        for item in _db:
            _m1_zz_dm__rm_idxs(_db, item, _exp_len, idxs_rev)




    def _m1_zz_dm__dm_1_to_2_helper(curr_len):
        
        rules_index = 14
        
        
        
        
        for _db in per_dbs:
            rm_idxs_db(_db, curr_len, rules_index)
        
        
        rm_idxs_db(lock_db, curr_len, rules_index)


    def _dm_1_to_2():
        """
        Data migration from version 1 to 2

        GOALS:
            - remove rules property from events and shrink the tuples.
        """
        
        _m1_zz_dm__dm_1_to_2_helper(20)


    def _dm_0811_to_2():
        """
        Data migration from version 0811-0814 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        
        _m1_zz_dm__dm_1_to_2_helper(19)


    def _dm_089_to_2():
        """
        Data migration from version 089-0810 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        
        _m1_zz_dm__dm_1_to_2_helper(18)


    def _dm_082_to_2():
        """
        Data migration from version 082-088 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        
        _m1_zz_dm__dm_1_to_2_helper(17)


    def _dm_080_to_2():
        """
        Data migration from version 080-081 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        
        _m1_zz_dm__dm_1_to_2_helper(16)


    def _dm_073_to_2():
        """
        Data migration from version 073-074 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        
        _m1_zz_dm__dm_1_to_2_helper(15)


    def _dm_2_to_1():
        """
        Data migration from version 2 to 1

        GOALS:
            - add rules property to events, expand tuples
        """
        
        rules_index = 14
        rules_data = {}
        curr_len = 19 
        
        
        
        
        for _db in per_dbs:
            add_idxs_db(_db, curr_len, (rules_index, rules_data))
        
        
        add_idxs_db(lock_db, curr_len, (rules_index, False))







    dm_map = {
        
        (-1, 2): _dm_0811_to_2,
        (-2, 2): _dm_089_to_2,
        (-3, 2): _dm_082_to_2,
        (-4, 2): _dm_080_to_2,
        (-5, 2): _dm_073_to_2,

        
        (1, 2): _dm_1_to_2,
        (2, 1): _dm_2_to_1,
    }



    def _determine_version():
        """
        This returns an  appropriate dm version based on version
        NOTE: this should only be used if migrating from versions 0814 and
        below.
        """
        
        
        
        version, sp, ignore = store.persistent.version_number.partition("-")
        maj_ver, mid_ver, min_ver = version.split(".")
        
        mid_ver = int(mid_ver)
        min_ver = int(min_ver)
        
        if mid_ver == 8:
            if 11 <= min_ver <= 14:
                return -1
            
            elif 9 <= min_ver <= 10:
                return -2
            
            elif 2 <= min_ver <= 8:
                return -3
            
            else:
                
                return -4
        
        elif mid_ver == 7 and 3 <= min_ver <= 4:
            
            return -5
        
        
        return dm_data_version


    def _m1_zz_dm__lessthan(val_a, val_b):
        return val_a < val_b


    def _m1_zz_dm__morethan(val_a, val_b):
        return val_a > val_b


    def _find_dm_fun(piv_ver, adj_ver, direction):
        """
        Iterates until we find a dm function and returns it.

        IN:
            piv_ver - the verion number we dont want to change when searching
            adj_ver - the verison number we change when searching
            direction - the direction to change adj_ver

        RETURNS tuple of the following format:
            [0]: data migration function found, Or none if not found
            [1]: value of adj_ver when data migration found
        """
        if direction < 0:
            
            
            ver_not_passed = _m1_zz_dm__lessthan
        else:
            
            
            ver_not_passed = _m1_zz_dm__morethan
        
        
        dm_found = dm_map.get((piv_ver, adj_ver), None)
        while dm_found is None and ver_not_passed(piv_ver, adj_ver):
            adj_ver += direction
            dm_found = dm_map.get((piv_ver, adj_ver), None)
        
        return (dm_found, adj_ver)


    def run(start_ver, end_ver):
        """
        Runs the data migration algorithms.

        ASSUMES: start_ver != end_ver

        IN:
            start_ver - start version to start
            end_ver - ending version number
        """
        _dm_fun = dm_map.get((start_ver, end_ver), None)
        
        if _dm_fun == -1:
            
            return
        
        if _dm_fun is not None:
            
            _dm_fun()
            return
        
        
        
        
        
        if start_ver < end_ver:
            direction = -1
        else:
            direction = 1
        
        curr_ver = start_ver
        while curr_ver != end_ver:
            _dm_fun, new_ver = _find_dm_fun(curr_ver, end_ver, direction)
            
            if _dm_fun is None:
                raise Exception(
                    "DATA MIGRATION FAILURE. {0} to {1}".format(
                        curr_ver, end_ver
                    )
                )
            
            
            _dm_fun()
            curr_ver = new_ver


init -897 python:





    if persistent.version_number is None:
        persistent._mas_dm_data_version = store._mas_dm_dm.dm_data_version

    elif persistent._mas_dm_data_version is None:
        persistent._mas_dm_data_version = store._mas_dm_dm._determine_version()

    if persistent._mas_dm_data_version != store._mas_dm_dm.dm_data_version:
        store._mas_dm_dm.run(
            persistent._mas_dm_data_version,
            store._mas_dm_dm.dm_data_version
        )
        
        
        persistent._mas_dm_data_version = store._mas_dm_dm.dm_data_version
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
