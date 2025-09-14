















































































































































































































































































































































































































default persistent._mas_sprites_json_gifted_sprites = {}










init -21 python in mas_sprites_json:
    import __builtin__
    import json
    import store
    import store.mas_utils as mas_utils
    import traceback
    from collections import defaultdict
    import logging


    SP_JSON_VER = 4
    VERSION_TXT = "version"


    FILENAME_FMT_VER = 3


    from store.mas_ev_data_ver import _verify_bool, _verify_str, \
        _verify_int, _verify_list, _verify_dict


    class SpriteJsonLogAdapter(store.mas_logging.MASNewlineLogAdapter):
        """
        Speciality logger for sprite jsons.
        This defaults some props for all log record objects created from this
        logger.

        accepts newlines in logging.
        """
        
        def __init__(self, logger):
            """
            IN:
                logger - the logger to adapt
            """
            super(SpriteJsonLogAdapter, self).__init__(
                logger,
                extra_props={
                    "indent_lvl": 0,
                }
            )


    class SpriteJsonFormatter(store.mas_logging.MASNewlineLogFormatter):
        """
        Specialty formatter for sprite jsons
        """
        
        def format(self, record):
            """
            override of logging.Formatter.format

            IN:
                record - LogRecord object

            RETURNS: string to be logged
            """
            self.update_levelname(record)
            return self.replace_lf(
                self.apply_newline_prefix(
                    record,
                    "[{0}]:  {1}{2}".format(
                        record.levelname,
                        " " * (record.indent_lvl * 2),
                        record.msg
                    )
                )
            )


    log = store.mas_logging.init_log(
        "spj",
        append=False,
        formatter=SpriteJsonFormatter(),
        adapter_ctor=SpriteJsonLogAdapter
    )

    py_list = __builtin__.list
    py_dict = __builtin__.dict

    sprite_station = store.MASDockingStation(
        renpy.config.basedir + "/game/mod_assets/monika/j/"
    )





    hm_key_delayed_veri = {}


    hm_val_delayed_veri = {}




    def _add_hair_to_verify(hairname, verimap, name):
        
        if hairname not in verimap:
            verimap[hairname] = []
        
        verimap[hairname].append(name)





    giftname_map = {
        "__testing": (0, "__testing"),
    }











    namegift_map = {
        (0, "__testing"): "__testing",
    }




    @store.mas_utils.deprecated(use_instead="log.info, log.warning, log.error, log.exception")
    def writelog(msg):
        
        log.info(msg)

    @store.mas_utils.deprecated()
    def writelogs(msgs):
        
        for msg in msgs:
            writelog(msg)
        
        
        msgs[:] = []



    READING_FILE = "reading JSON at '{0}'..."
    SP_LOADING = "loading {0} sprite object '{1}'..."
    SP_SUCCESS = "{0} sprite object '{1}' loaded successfully!"
    SP_SUCCESS_DRY = "{0} sprite object '{1}' loaded successfully! DRY RUN"
    VER_NOT_FOUND = "version not found"
    VER_BAD = "version mismatch. expected '{0}', found '{1}'"
    FILENAME_FMT = "using filename-based structure - consider updating to folder-based structure"

    BAD_TYPE = "property '{0}' - expected type {1}, got {2}"
    EXTRA_PROP = "extra property '{0}' found"
    REQ_MISS = "    required property '{0}' not found"
    BAD_SPR_TYPE = "    invalid sprite type '{0}'"
    BAD_ACS_LAYER = "invalid ACS layer '{0}'"
    BAD_LIST_TYPE = "property '{0}' index '{1}' - expected type {2}, got {3}"
    EMPTY_LIST = "property '{0}' cannot be an empty list"

    DUPE_GIFTNAME = "giftname '{0}' already exists"
    MATCH_GIFT = (
        "cannot associate giftname '{0}' with sprite object type {1} name "
        "'{2}' - sprite object already associated with giftname '{3}'"
    )
    NO_GIFT = "without 'giftname', this cannot be natively unlocked"

    NO_DLG_DESC = "'dlg_desc' not found, ignoring 'dlg_plural'"
    NO_DLG_PLUR = "'dlg_plural' not found, ignoring 'dlg_desc'"


    MPM_LOADING = "loading Pose Map in '{0}'..."
    MPM_SUCCESS = "Pose Map '{0}' loaded successfully!"
    MPM_BAD_TYPE = "invalid mpm_type '{0}'"
    MPM_TYPE_MISS = "expected mpm_type in {0}, got '{1}'"
    MPM_BAD_POSE = "property '{0}' - invalid pose '{1}'"
    MPM_FB_DEF = "in fallback mode but default not set"
    MPM_FB_DEF_L = "in fallback mode but leaning default not set"
    MPM_ACS_DEF = "acs default pose not set"
    MPM_ACS_DEF_L = "acs leaning default pose not set"
    MPM_DEF = "default not set"
    MPM_DEF_L = "leaning default not set"
    MPM_BAD_POSE_TYPE = "property '{0}' - expected type {1}, got {2}"
    MPM_AS_BAD_TYPE = "property '{0}' - expected {1}, got {2}"
    MPM_AS_EXTRA = "arm_split cannot be used with rec_layer '{0}'"
    MPM_PA_BAD_TYPE = "property '{0}' - expected object, got {1}"


    MHM_LOADING = "loading Highlight object..."
    MHM_SUCCESS = "Highlight object loaded successfully!"
    MHM_S_LOADING = "loading Highlight Split object..."
    MHM_S_SUCCESS = "Highlight Split object loaded successfully!"
    MHM_SK_LOADING = "loading Highlight object for key '{0}'..."
    MHM_SK_SUCCESS = "Highlight object for key '{0}' loaded successfully!"
    MHM_LOADING_MAPPING = "loading mapping..."
    MHM_SUCCESS_MAPPING = "mapping loaded successfully!"
    MHM_NO_DATA = "No data in Highlight object, ignoring"
    MHM_S_NO_DATA = "No data in Highlight Split object, ignoring"
    MHM_KEY_BAD_TYPE = "key '{0}' - expected type {1} got {2}"
    MHM_NOT_DICT = "Highlight object must be of type {0}. got {1}"
    MHM_S_NOT_DICT = "Highlight split object must be of type {0}. got {1}"


    MFM_LOADING = "loading Filter object in '{0}'..."
    MFM_SUCCESS = "Filter object '{0}' loaded successfully!"
    MFM_NONE_FLT = "filter '{0}' set to null, ignoring"
    MFM_BAD_TYPE = "filter '{0}' - expected type str, got {1}"
    MFM_NO_DATA = "No data in Filter object, ignoring"


    MPA_LOADING = "loading Pose Arms in '{0}'..."
    MPA_SUCCESS = "Pose Arms '{0}' loaded successfully!"
    MPA_BAD_TYPE = "Arm ID: {0} - expected type {1} got {2}"
    MPA_NO_DATA = "No Pose Arms data found"


    MA_LOADING = "loading Arm in '{0}'..."
    MA_SUCCESS = "Arm '{0}' loaded successfully!"
    MA_INVALID_LAYER = "invalid layer '{0}' found, ignoring"
    MA_NO_LAYERS = "Arm must have valid layers set"


    HM_LOADING = "loading hair_map..."
    HM_SUCCESS = "hair_map loaded successfully!"
    HM_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    HM_BAD_V_TYPE = "value for key '{0}' - expected type {1}, got {2}"
    HM_MISS_ALL = "hair_map does not have key 'all' set. Using default for 'all'."
    HM_FOUND_CUST = (
        "'custom' hair cannot be used in JSON hair maps. "
        "Outfits using 'custom' hair must be created manually."
    )
    HM_VER_ALL = "verifying hair maps..."
    HM_VER_SUCCESS = "hair map verification complete!"
    HM_NO_KEY = (
        "hair '{0}' does not exist - found in hair_map keys of these "
        "sprites: {1}"
    )
    HM_NO_VAL = (
        "hair '{0}' does not exist - found in hair_map values of these "
        "sprites: {1}. replacing with defaults."
    )


    EP_LOADING = "loading ex_props..."
    EP_SUCCESS = "ex_props loaded successfully!"
    EP_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    EP_BAD_V_TYPE = "value for key '{0}' - expected type int/str/bool, got {1}"


    SI_LOADING = "loading select_info..."
    SI_SUCCESS = "sel_info loaded successfully!"


    PP_MISS = "'{0}' progpoint not found"
    PP_NOTFUN = "'{0}' progpoint not callable"


    IL_NOTLOAD = "image at '{0}' is not loadable"


    GR_LOADING = "creating reactions for gifts..."
    GR_SUCCESS = "gift reactions created successfully!"
    GR_FOUND = "reaction label found for {0} sprite '{1}', giftname '{2}'"
    GR_GEN = "using generic reaction for {0} sprite '{1}', giftname '{2}'"


    OE_LOADING = "loading outfit mode data..."
    OE_SUCCESS = "outfit mode data loaded successfully!"
    OE_INVALID_HAIR = "hair '{0}' does not exist, ignoring for clothes '{1}'"
    OE_INVALID_ACS = "ACS '{0}' does not exist, ignoring for clothes '{1}'"



    SP_ACS = 0
    SP_HAIR = 1
    SP_CLOTHES = 2

    SP_CONSTS = (
        SP_ACS,
        SP_HAIR,
        SP_CLOTHES,
    )

    SP_STR = {
        SP_ACS: "ACS",
        SP_HAIR: "HAIR",
        SP_CLOTHES: "CLOTHES",
    }

    SP_UF_STR = {
        SP_ACS: "accessory",
        SP_HAIR: "hairstyle",
        SP_CLOTHES: "outfit",
    }

    SP_PP = {
        SP_ACS: "store.mas_sprites._acs_{0}_{1}",
        SP_HAIR: "store.mas_sprites._hair_{0}_{1}",
        SP_CLOTHES: "store.mas_sprites._clothes_{0}_{1}",
    }

    SP_RL = {
        SP_ACS: "mas_reaction_gift_acs_{0}",
        SP_HAIR: "mas_reaction_gift_hair_{0}",
        SP_CLOTHES: "mas_reaction_gift_clothes_{0}",
    }

    SP_RL_GEN = "{0}|{1}|{2}"

    def _verify_sptype(val, allow_none=True):
        if val is None:
            return allow_none
        return val in SP_CONSTS








    HLITE = "highlight"



    REQ_SHARED_PARAM_NAMES = {
        

        "name": (str, _verify_str),
        "img_sit": (str, _verify_str),
        

    }

    OPT_SHARED_PARAM_NAMES = {
        "stay_on_start": (bool, _verify_bool),

        



    }

    OPT_AC_SHARED_PARAM_NAMES = {
        "giftname": (str, _verify_str),
    }

    OPT_HA_SHARED_PARAM_NAMES = {
    }

    OPT_ACS_PARAM_NAMES = {
        



        "priority": (int, _verify_int),
        "acs_type": (str, _verify_str),
        "dlg_desc": (str, _verify_str),
        "dlg_plural": (str, _verify_bool),
        "keep_on_desk": (bool, _verify_bool),
    }
    OPT_ACS_PARAM_NAMES.update(OPT_AC_SHARED_PARAM_NAMES)
    OPT_ACS_PARAM_NAMES.update(OPT_HA_SHARED_PARAM_NAMES)

    OPT_HC_SHARED_PARAM_NAMES = {

    }

    OPT_HAIR_PARAM_NAMES = {
        

        "unlock": (bool, _verify_bool),
        "use_numeric_layer_ids": (bool, _verify_bool),
    }
    OPT_HAIR_PARAM_NAMES.update(OPT_HA_SHARED_PARAM_NAMES)

    OPT_CLOTH_PARAM_NAMES = {
        
        "outfit_hair": (str, _verify_str),
        "outfit_acs": (list, _verify_list),
    }
    OPT_CLOTH_PARAM_NAMES.update(OPT_AC_SHARED_PARAM_NAMES)


    OBJ_BASED_PARAM_NAMES = (
        "pose_map",
        "ex_props",
        "select_info",
        "split",
        "hair_map",
        "arm_split",
        "pose_arms",
        HLITE,
        "mid_hair_map",
    )


    SEL_INFO_REQ_PARAM_NAMES = {
        "display_name": (str, _verify_str),
        "thumb": (str, _verify_str),
        "group": (str, _verify_str),
    }

    SEL_INFO_OPT_PARAM_NAMES = {
        "visible_when_locked": (bool, _verify_bool),
    }


    PAD_REQ_PARAM_NAMES = {
        "tag": (str, _verify_str),
        "layers": (str, _verify_str),
    }



    DRY_RUN = "dryrun"


init 189 python in mas_sprites_json:
    from store.mas_sprites import _verify_pose, HAIR_MAP, CLOTH_MAP, ACS_MAP
    from store.mas_logging import (
        JSON_LOAD_FAILED,
        FILE_LOAD_FAILED,
        LOAD_TRY,
        LOAD_SUCC,
        LOAD_FAILED,
        NAME_BAD
    )


    import store.mas_sprites as sms
    import store.mas_selspr as sml


    MSG_INFO_T = 0
    MSG_WARN_T = 1
    MSG_ERR_T = 2

    MSG_SEVERITY_MAP = {
        MSG_INFO_T: log.info,
        MSG_WARN_T: log.warning,
        MSG_ERR_T: log.error
    }




    def parsewritelog(msg_data):
        """
        write log using specially formatted data.

        IN:
            msg_data - tuple of the following format:
                [0] - log constant
                [1] - indentation level
                [2] - msg to write

        RETURNS: True if an ERR constant was found, False if not
        """
        log_con, indent, msg = msg_data
        log_func = MSG_SEVERITY_MAP.get(log_con, None)
        if log_func is None:
            return True
        
        log_func(msg, indent_lvl=indent)
        return log_con == MSG_ERR_T


    def parsewritelogs(msgs_data):
        """
        Write logs using specially formatted data

        IN:
            msgs_data - list of tuples of the following format:
                [0] - log constant
                [1] - indentation level
                [2] - msg to write

        RETURNS: True if an ERR constnat was found, False if not
        """
        is_bad = False
        for msg_data in msgs_data:
            if parsewritelog(msg_data):
                is_bad = True
        
        return is_bad


    def _replace_hair_map(sp_name, hair_to_replace):
        """
        Replaces the hair vals of the given sprite object with the given name
        of the given hair with defaults.

        IN:
            sp_name - name of the clothing sprite object to replace hair
                map values in
            hair_to_replace - hair name to replace with defaults
        """
        
        sp_obj = CLOTH_MAP.get(sp_name, None)
        if sp_obj is None or sp_obj.hair_map is None:
            return
        
        
        for hair_key in sp_obj.hair_map:
            if sp_obj.hair_map[hair_key] == hair_to_replace:
                sp_obj.hair_map[hair_key] = store.mas_hair_def.name


    def _remove_sel_list(name, sel_list):
        """
        Removes selectable from selectbale list

        Only intended for json usage. DO not use elsewhere. In general, you
        should NEVER need to remove a selectable from the selectable list.
        """
        for index in range(len(sel_list)-1, -1, -1):
            if sel_list[index].name == name:
                sel_list.pop(index)


    def _reset_sp_obj(sp_obj):
        """
        Uninits the given sprite object. This is meant only for json
        sprite usage if we need to back out.

        IN:
            sp_obj - sprite object to remove
        """
        sp_type = sp_obj.gettype()
        sp_name = sp_obj.name
        
        
        if sp_type not in SP_CONSTS:
            return
        
        if sp_type == SP_ACS:
            _item_map = sms.ACS_MAP
            _sel_map = sml.ACS_SEL_MAP
            _sel_list = sml.ACS_SEL_SL
        
        elif sp_type == SP_HAIR:
            _item_map = sms.HAIR_MAP
            _sel_map = sml.HAIR_SEL_MAP
            _sel_list = sml.HAIR_SEL_SL
        
        else:
            
            _item_map = sms.CLOTH_MAP
            _sel_map = sml.CLOTH_SEL_MAP
            _sel_list = sml.CLOTH_SEL_SL
        
        
        if sp_name in _item_map:
            _item_map.pop(sp_name)
        
        if sml.get_sel(sp_obj) is not None:
            
            if sp_name in _sel_map:
                _sel_map.pop(sp_name)
            
            
            _remove_sel_list(sp_name, _sel_list)


    def _build_loadstrs(sp_obj, sel_obj=None):
        """
        Builds list of strings that need to be verified via loadable.

        IN:
            sp_obj - sprite object to build strings from
            sel_obj - selectable to build thumb string from.
                Ignored if None
                (Default: None)

        RETURNS: list of strings that would need to be loadable verified
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        if sp_obj.gettype() == SP_ACS:
            prefix = [sms.A_MAIN]
        
        elif sp_obj.gettype() == SP_HAIR:
            prefix = [sms.H_MAIN]
        
        elif sp_obj.gettype() == SP_CLOTHES:
            prefix = [sms.C_MAIN]
        
        else:
            return []
        
        
        to_verify = [
            "".join(str_tup)
            for str_tup in sp_obj.build_loadstrs(prefix)
        ]
        
        
        if sel_obj is not None:
            to_verify.append(sel_obj._build_thumbstr())
        
        return to_verify


    def _check_giftname(giftname, sp_type, sp_name, msg_log, ind_lvl):
        """
        Initializes the giftname with the sprite info

        IN:
            giftname - giftname we want to use
            sp_type - sprite type we want to init
            sp_name - name of the sprite object to associated with this gift
                (use the sprite's name property == ID)
            ind_lvl - indentation level to use

        OUT:
            msg_log - list to log messages to
        """
        
        if giftname in giftname_map:
            msg_log.append((
                MSG_ERR_T,
                ind_lvl,
                DUPE_GIFTNAME.format(giftname)
            ))
            return
        
        
        sp_value = (sp_type, sp_name)
        if sp_value in namegift_map:
            msg_log.append((
                MSG_ERR_T,
                ind_lvl,
                MATCH_GIFT.format(
                    giftname,
                    SP_STR[sp_type],
                    sp_name,
                    namegift_map[sp_value]
                )
            ))
            return


    def _init_giftname(giftname, sp_type, sp_name):
        """
        Initializes the giftname with the sprite info
        does not check for valid giftname.

        IN:
            giftname - giftname we want to use
            sp_type - sprite type we want to init
            sp_name - name of the sprite object to associate with this gift
        """
        
        giftname_map[giftname] = (sp_type, sp_name)
        namegift_map[(sp_type, sp_name)] = giftname


    def _process_giftname():
        """
        Process the gift maps by cleaning the persistent vars
        """
        
        for fr_sp_gn in store.persistent._mas_filereacts_sprite_gifts:
            if fr_sp_gn not in giftname_map:
                store.persistent._mas_filereacts_sprite_gifts.pop(fr_sp_gn)
        
        
        for j_sp_data in store.persistent._mas_sprites_json_gifted_sprites:
            if j_sp_data not in namegift_map:
                store.persistent._mas_sprites_json_gifted_sprites.pop(j_sp_data)


    def _process_progpoint(
            sp_type,
            name,
            save_obj,
            msg_log,
            ind_lvl,
            progname
        ):
        """
        Attempts to find a prop point for a sprite object with the given
        sp_type and name

        IN:
            sp_type - sprite object type
            name - name of sprite object
            ind_lvl - indent level
            progname - name of progpoint (do not include suffix)

        OUT:
            save_obj - dict to save progpoint to
            msg_log - list to save messages to
        """
        
        e_pp_str = SP_PP[sp_type].format(name, progname)
        
        
        try:
            e_pp = eval(e_pp_str)
        
        except:
            
            e_pp = None
        
        
        if e_pp is None:
            msg_log.append((
                MSG_INFO_T,
                ind_lvl,
                PP_MISS.format(progname)
            ))
        
        elif not callable(e_pp):
            msg_log.append((
                MSG_WARN_T,
                ind_lvl,
                PP_NOTFUN.format(progname)
            ))
        
        else:
            
            save_obj[progname + "_pp"] = e_pp


    def _test_loadables(sp_obj, msg_log, ind_lvl):
        """
        Tests loadable images and errs if an image is not loadable.

        IN:
            sp_obj - sprite object to test
            ind_lvl - indentation level

        OUT:
            msg_log - list to add messages to
        """
        sel_obj = sml.get_sel(sp_obj)
        
        
        to_verify = _build_loadstrs(sp_obj, sel_obj)
        
        
        for imgpath in to_verify:
            if not renpy.loadable(imgpath):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl,
                    IL_NOTLOAD.format(imgpath)
                ))


    def _validate_type(json_obj, msg_log, ind_lvl):
        """
        Validates the type of this json object.

        Logs errors. Also pops type off

        IN:
            json_obj - json object to validate
            ind_lvl - indentation level

        OUT:
            msg_log - list to add messages to

        RETURNS: SP constant if valid type, None otherwise
        """
        
        if "type" not in json_obj:
            msg_log.append((
                MSG_ERR_T,
                ind_lvl,
                REQ_MISS.format("type")
            ))
            return None
        
        
        type_val = json_obj.pop("type")
        if not _verify_sptype(type_val, False):
            msg_log.append((
                MSG_ERR_T,
                ind_lvl,
                BAD_SPR_TYPE.format(type_val)
            ))
            return None
        
        
        return type_val


    def _validate_mux_type(json_obj, msg_log, indent_lvl):
        """
        Validates mux_type of this json object

        IN:
            json_obj - json object to validate
            indent_lvl - indtenation lvl to use

        OUT:
            msg_log - list to save error messages to
                if nothing was addeed to this list, the mux_type is valid

        RETURNS: mux_type found. May be None
        """
        if "mux_type" not in json_obj:
            return None
        
        
        mux_type = json_obj.pop("mux_type")
        
        if not _verify_list(mux_type):
            
            msg_log.append((
                MSG_ERR_T,
                indent_lvl,
                BAD_TYPE.format(
                    "mux_type",
                    py_list,
                    type(mux_type)
                )
            ))
            return None
        
        
        for index in range(len(mux_type)):
            acs_type = mux_type[index]
            if not _verify_str(acs_type):
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    BAD_LIST_TYPE.format(
                        "mux_type",
                        index,
                        str,
                        type(acs_type)
                    )
                ))
        
        
        
        
        return mux_type


    def _validate_iterstr(
            jobj,
            save_obj,
            propname,
            required,
            allow_none,
            msg_log,
            indent_lvl
        ):
        """
        Validates an iterable if it consists solely of strings

        an empty list is considered bad.

        IN:
            jobj - json object to parse
            propname - property name for error messages
            required - True if this property is required, False if not
            allow_none - True if None is valid value, False if not
            indent_lvl - indentation level

        OUT:
            save_obj - dict to save to
            msg_log - list to save messages to

        RETURNS: True if good, False if bad
        """
        
        if propname not in jobj:
            if required:
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    REQ_MISS.format(propname)
                ))
                return False
            return True
        
        
        iterval = jobj.pop(propname)
        
        
        if iterval is None:
            if not allow_none:
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    BAD_TYPE.format(propname, py_list, type(iterval))
                ))
                return False
            return True
        
        
        if len(iterval) <= 0:
            msg_log.append((
                MSG_ERR_T,
                indent_lvl,
                EMPTY_LIST.format(propname)
            ))
            return False
        
        
        is_bad = False
        for index in range(len(iterval)):
            item = iterval[index]
            
            if not _verify_str(item):
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    BAD_LIST_TYPE.format(propname, index, str, type(item))
                ))
                is_bad = True
        
        if is_bad:
            return False
        
        
        save_obj[propname] = iterval
        return True


    def _validate_params(
            jobj,
            save_obj,
            param_dict,
            required,
            msg_log,
            indent_lvl,
        ):
        """
        Validates a list of parameters, while also saving said params into
        given save object.

        Errors/Warnings are logged to given lists

        IN:
            jobj - json object to parse
            param_dict - dict of params + verification functiosn
            required - True if the given params are required, False otherwise.
            indent_lvl - indentation level to use

        OUT:
            save_obj - dict to save data to
            msg_log - log to save messages to

        RETURNS: True if success, False if not
        """
        
        allow_none = not required
        is_bad = False
        
        for param_name, verifier_info in param_dict.iteritems():
            if param_name in jobj:
                param_val = jobj.pop(param_name)
                desired_type, verifier = verifier_info
                
                if not verifier(param_val, allow_none):
                    
                    msg_log.append((
                        MSG_ERR_T,
                        indent_lvl,
                        BAD_TYPE.format(
                            param_name,
                            desired_type,
                            type(param_val)
                        )
                    ))
                    is_bad = True
                
                
                
                save_obj[param_name] = param_val
            
            elif required:
                
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    REQ_MISS.format(param_name)
                ))
                is_bad = True
        
        return not is_bad


    def _validate_acs(jobj, save_obj, obj_based, msg_log, indent_lvl):
        """
        Validates ACS-specific properties, as well as acs pose map

        Props validated:
            - rec_layer
            - priority
            - acs_type
            - dlg_desc
            - dlg_plural
            - mux_type
            - pose_map
            - giftname
            - arm_split
            - highlight

        IN:
            jobj - json object to pasrse
            obj_based - dict of object-based items
                (contains pose_map)
            indent_lvl - indentation lvl to use

        OUT:
            save_obj - dict to save data to
            msg_log - list to add messages to

        RETURNS: True if validation success, False if not
        """
        
        
        
        
        
        
        if not _validate_params(
            jobj,
            save_obj,
            OPT_ACS_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl
        ):
            return False
        
        
        if "dlg_desc" in save_obj:
            dlg_desc = save_obj.pop("dlg_desc")
            
            
            if "dlg_plural" in save_obj:
                
                
                save_obj["dlg_data"] = (dlg_desc, save_obj.pop("dlg_plural"))
            
            else:
                
                msg_log.append((MSG_WARN_T, indent_lvl, NO_DLG_PLUR))
        
        elif "dlg_plural" in save_obj:
            
            msg_log.append((MSG_WARN_T, indent_lvl, NO_DLG_DESC))
            save_obj.pop("dlg_plural")
        
        
        if "rec_layer" in jobj:
            rec_layer = jobj.pop("rec_layer")
            
            if not store.MASMonika._verify_rec_layer(rec_layer):
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    BAD_ACS_LAYER.format(rec_layer)
                ))
                return False
            
            
            save_obj["rec_layer"] = rec_layer
        
        
        err_log = []
        mux_type = _validate_mux_type(jobj, err_log, indent_lvl)
        if len(err_log) > 0:
            msg_log.extend(err_log)
            return False
        
        
        save_obj["mux_type"] = mux_type
        
        
        msg_log.append((
            MSG_INFO_T,
            indent_lvl,
            MPM_LOADING.format("pose_map")
        ))
        
        
        
        mpm_obj = obj_based.pop("pose_map")
        mpm_obj["mpm_type"] = store.MASPoseMap.MPM_TYPE_IC
        mpm_msg_log = []
        pose_map = store.MASPoseMap.fromJSON(
            mpm_obj,
            mpm_msg_log,
            indent_lvl + 1
        )
        msg_log.extend(mpm_msg_log)
        if pose_map is None:
            return False
        
        
        msg_log.append((
            MSG_INFO_T,
            indent_lvl,
            MPM_SUCCESS.format("pose_map")
        ))
        save_obj["pose_map"] = pose_map
        
        
        arm_split = None
        if store.MASMonika._verify_spl_layer(rec_layer):
            
            if "arm_split" not in obj_based:
                
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl,
                    REQ_MISS.format("arm_split")
                ))
                return False
            
            
            
            msg_log.append((
                MSG_INFO_T,
                indent_lvl,
                MPM_LOADING.format("arm_split")
            ))
            
            
            mpm_obj = obj_based.pop("arm_split")
            mpm_obj["mpm_type"] = store.MASPoseMap.MPM_TYPE_AS
            mpm_msg_log = []
            arm_split = store.MASPoseMap.fromJSON(
                mpm_obj,
                mpm_msg_log,
                indent_lvl + 1
            )
            msg_log.extend(mpm_msg_log)
            if arm_split is None:
                return False
            
            
            msg_log.append((
                MSG_INFO_T,
                indent_lvl,
                MPM_SUCCESS.format("arm_split")
            ))
            save_obj["arm_split"] = arm_split
        
        elif "arm_split" in obj_based:
            
            obj_based.pop("arm_split")
            msg_log.append((
                MSG_WARN_T,
                indent_lvl,
                MPM_AS_EXTRA.format(rec_layer)
            ))
        
        
        
        if HLITE in obj_based:
            
            
            hl_keys = pose_map.unique_values()
            
            if arm_split:
                
                
                hl_data = store.MASSplitAccessory.fromJSON_hl_data(
                    obj_based.pop(HLITE),
                    msg_log,
                    indent_lvl,
                    hl_keys,
                    rec_layer
                )
                
                
                if hl_data is False:
                    return False
                
                
                if hl_data is not None:
                    save_obj["hl_data"] = hl_data
            
            else:
                
                
                if not _validate_highlight(
                        obj_based,
                        save_obj,
                        msg_log,
                        indent_lvl,
                        hl_keys
                ):
                    return False
        
        return True


    def _validate_fallbacks(jobj, save_obj, obj_based, msg_log, indent_lvl):
        """
        Validates fallback related properties and pose map

        Props validated:
            - fallback
            - pose_map

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains pose_map)
            indent_lvl - indentation lvl to use

        OUT:
            save_obj - dict to save data to
            msg_log - list to save messages to

        RETURNS: True if success, False if not
        """
        
        if not _validate_params(
            jobj,
            save_obj,
            OPT_HC_SHARED_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl
        ):
            return False
        
        
        fallback = save_obj.get("fallback", False)
        
        
        msg_log.append((
            MSG_INFO_T,
            indent_lvl,
            MPM_LOADING.format("pose_map")
        ))
        mpm_msg_log = []
        pose_map = store.MASPoseMap.fromJSON(
            obj_based.pop("pose_map"),
            mpm_msg_log,
            indent_lvl + 1,
            valid_types=(
                store.MASPoseMap.MPM_TYPE_ED,
                store.MASPoseMap.MPM_TYPE_FB
            )
        )
        msg_log.extend(mpm_msg_log)
        if pose_map is None:
            return False
        
        
        msg_log.append((
            MSG_INFO_T,
            indent_lvl,
            MPM_SUCCESS.format("pose_map")
        ))
        save_obj["pose_map"] = pose_map
        return True


    def _validate_hair(jobj, save_obj, obj_based, msg_log, indent_lvl):
        """
        Validates HAIR related properties

        Props validated:
            - unlock
            - use_numeric_layer_ids
            - highlight

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
            indent_lvl - indentation lvl

        OUT:
            save_obj - dict to save data to
            msg_log - list to save messagse to

        RETURNS: True on success, False if not
        """
        
        if not _validate_params(
            jobj,
            save_obj,
            OPT_HAIR_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl
        ):
            return False
        
        
        if "use_numeric_layer_ids" not in save_obj:
            save_obj["use_numeric_layer_ids"] = False
        
        
        if "mid_hair_map" in obj_based:
            msg_log.append((
                MSG_INFO_T,
                indent_lvl,
                MPM_LOADING.format("mid_hair_map")
            ))
            mpm_msg_log = []
            mid_hair_map = store.MASPoseMap.fromJSON(
                obj_based.pop("mid_hair_map"),
                mpm_msg_log,
                indent_lvl + 1,
                valid_types=(
                    store.MASPoseMap.MPM_TYPE_ED,
                )
            )
            msg_log.extend(mpm_msg_log)
            if mid_hair_map is None:
                return False
            
            
            msg_log.append((
                MSG_INFO_T,
                indent_lvl,
                MPM_SUCCESS.format("mid_hair_map")
            ))
            save_obj["mpm_mid"] = mid_hair_map
        
        
        if HLITE in obj_based:
            
            
            if not _validate_highlight(
                    obj_based,
                    save_obj,
                    msg_log,
                    indent_lvl,
                    store.MASHair.hl_keys_c()
            ):
                return False
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        return True


    def _validate_clothes(
            jobj,
            save_obj,
            obj_based,
            sp_name,
            dry_run,
            msg_log,
            indent_lvl,
            post_proc_data
        ):
        """
        Validates CLOTHES related properties

        Props validated:
            - hair_map
            - giftname
            - pose_arms
            - highlight
            - outfit_hair
            - outfit_acs

        IN:
            jobj - json object to parse
            obj_based - dict of objected-baesd items
                (contains split)
            sp_name - name of the clothes we are validating
            dry_run - true if we are dry running, False if not
            indent_lvl - indentation lvl

        OUT:
            save_obj - dict to save data to
            msg_log - list to save messages to
            post_proc_data - dict to store data for post proccessing

        RETURNS: True if good, False if not
        """
        
        if not _validate_params(
            jobj,
            save_obj,
            OPT_CLOTH_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl
        ):
            return
        
        
        if "outfit_hair" in save_obj:
            post_proc_data["outfit_extras"][sp_name]["hair"] = save_obj.pop(
                "outfit_hair"
            )
        if "outfit_acs" in save_obj:
            post_proc_data["outfit_extras"][sp_name]["acs"] = save_obj.pop(
                "outfit_acs"
            )
        
        
        if "hair_map" in obj_based:
            
            
            msg_log.append((MSG_INFO_T, indent_lvl, HM_LOADING))
            hair_map = obj_based.pop("hair_map")
            is_bad = False
            
            for hair_key,hair_value in hair_map.iteritems():
                
                
                
                if _verify_str(hair_key):
                    if (
                            not dry_run
                            and hair_key != "all"
                            and hair_key not in HAIR_MAP
                        ):
                        _add_hair_to_verify(
                            hair_key,
                            hm_key_delayed_veri,
                            sp_name
                        )
                else:
                    msg_log.append((
                        MSG_ERR_T,
                        indent_lvl + 1,
                        HM_BAD_K_TYPE.format(hair_key, str, type(hair_key))
                    ))
                    is_bad = True
                
                
                if _verify_str(hair_value):
                    if hair_value == "custom":
                        msg_log.append((
                            MSG_ERR_T,
                            indent_lvl + 1,
                            HM_FOUND_CUST
                        ))
                        is_bad = True
                    
                    elif not dry_run and hair_value not in HAIR_MAP:
                        _add_hair_to_verify(
                            hair_value,
                            hm_val_delayed_veri,
                            sp_name
                        )
                
                else:
                    msg_log.append((
                        MSG_ERR_T,
                        indent_lvl + 1,
                        HM_BAD_V_TYPE.format(hair_key, str, type(hair_value))
                    ))
                    is_bad = True
            
            
            if "all" not in hair_map:
                msg_log.append((MSG_WARN_T, indent_lvl + 1, HM_MISS_ALL))
                hair_map["all"] = "def"
            
            
            if is_bad:
                return False
            
            
            msg_log.append((MSG_INFO_T, indent_lvl, HM_SUCCESS))
            save_obj["hair_map"] = hair_map
        
        
        if "pose_arms" in obj_based:
            
            msg_log.append((
                MSG_INFO_T,
                indent_lvl,
                MPA_LOADING.format("pose_arms")
            ))
            
            
            pa_obj = obj_based.pop("pose_arms")
            if not _verify_dict(pa_obj, False):
                msg_log.append((
                    MSG_ERR_T,
                    indent_lvl + 1,
                    BAD_TYPE.format("pose_arms", dict, type(pa_obj))
                ))
                return False
            
            
            pose_arms = store.MASPoseArms.fromJSON(
                pa_obj,
                msg_log,
                indent_lvl + 1
            )
            
            
            if pose_arms is False:
                return False
            
            
            msg_log.append((
                MSG_INFO_T,
                indent_lvl,
                MPA_SUCCESS.format("pose_arms")
            ))
            
            if pose_arms is not None:
                save_obj["pose_arms"] = pose_arms
        
        
        if HLITE in obj_based:
            
            if not _validate_highlight(
                    obj_based,
                    save_obj,
                    msg_log,
                    indent_lvl,
                    store.MASClothes.hl_keys_c()
            ):
                return False
        
        return True


    def _validate_ex_props(jobj, save_obj, obj_based, msg_log, ind_lvl):
        """
        Validates ex_props proprety

        Props validated:
            - ex_props

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains ex_props)
            ind_lvl - indentation level

        OUT:
            save_obj - dict to save data to
            msg_log - list to save messages to
        """
        
        if "ex_props" not in obj_based:
            return
        
        
        msg_log.append((MSG_INFO_T, ind_lvl, EP_LOADING))
        ex_props = obj_based.pop("ex_props")
        
        isbad = False
        for ep_key,ep_val in ex_props.iteritems():
            if not _verify_str(ep_key):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    EP_BAD_K_TYPE.format(ep_key, str, type(ep_key))
                ))
                isbad = True
            
            if not (
                    _verify_str(ep_val)
                    or _verify_bool(ep_val)
                    or _verify_int(ep_val)
                ):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    EP_BAD_V_TYPE.format(ep_key, type(ep_val))
                ))
                isbad = True
        
        
        if isbad:
            return
        
        
        msg_log.append((MSG_INFO_T, ind_lvl, EP_SUCCESS))
        save_obj["ex_props"] = ex_props


    def _validate_highlight(obj_based, save_obj, msg_log, ind_lvl, hl_keys):
        """
        Validates highlight objects

        Props validated:
            - highlight

        IN:
            obj_based - dict of object-based props
            hl_keys - the keys that this highlight object should be using
            ind_lvl - indentation level

        OUT:
            save_obj - dict to save data to
            msg_log - list to add messages to

        RETURNS: True if valid, False if not
        """
        
        msg_log.append((MSG_INFO_T, ind_lvl, MHM_LOADING))
        
        
        if not _validate_highlight_core(
                obj_based.pop(HLITE),
                save_obj,
                msg_log,
                ind_lvl + 1,
                hl_keys
        ):
            
            return False
        
        
        msg_log.append((MSG_INFO_T, ind_lvl, MHM_SUCCESS))
        return True


    def _validate_highlight_core(jobj, save_obj, msg_log, ind_lvl, hl_keys):
        """
        Primary portion of highlight validation. This is so it can be
        used seamlessly with highlight split object validation logs.

        Props validated:
            - highlight

        IN:
            jobj - json object to parse
            hl_keys - the keys this highlight object should be using

        OUT:
            save_obj - dict to save data to
            msg_log - list to add messages to

        RETURNS: True if valid, False if not
        """
        
        if not _verify_dict(jobj, allow_none=False):
            msg_log.append((
                MSG_ERR_T,
                ind_lvl,
                MHM_NOT_DICT.format(dict, type(jobj))
            ))
            return False
        
        
        hl_def = None
        hl_mapping = {}
        
        
        if "default" in jobj:
            hl_def = store.MASFilterMap.fromJSON(
                jobj.pop("default"),
                msg_log,
                ind_lvl,
                "default"
            )
        
        
        
        has_map_data = False
        if "mapping" in jobj:
            mapobj = jobj.pop("mapping")
            
            
            msg_log.append((MSG_INFO_T, ind_lvl, MHM_LOADING_MAPPING))
            
            
            if not _verify_dict(mapobj, allow_none=False):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    BAD_TYPE.format("mapping", dict, type(mapobj))
                ))
                return False
            
            
            isbad = False
            for hl_key in hl_keys:
                if hl_key in mapobj:
                    flt_obj = store.MASFilterMap.fromJSON(
                        mapobj.pop(hl_key),
                        msg_log,
                        ind_lvl + 1,
                        hl_key
                    )
                    
                    
                    if flt_obj is False:
                        isbad = True
                    else:
                        if flt_obj is not None:
                            
                            has_map_data = True
                        
                        hl_mapping[hl_key] = flt_obj
            
            
            for extra_prop in mapobj:
                msg_log.append((
                    MSG_WARN_T,
                    ind_lvl + 1,
                    EXTRA_PROP.format(extra_prop)
                ))
            
            
            
            if isbad:
                return False
            
            
            msg_log.append((MSG_INFO_T, ind_lvl, MHM_SUCCESS_MAPPING))
        
        
        if hl_def is None and (len(hl_mapping) == 0 or not has_map_data):
            
            msg_log.append((MSG_WARN_T, ind_lvl, MHM_NO_DATA))
        
        else:
            
            save_obj["hl_data"] = (hl_def, hl_mapping)
        
        return True


    def _validate_selectable(jobj, save_obj, obj_based, msg_log, indent_lvl):
        """
        Validates selectable

        Props validated:
            - select_info

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains select_info)
            indent_lvl - indentation level

        OUT:
            save_obj - dict to save data to
            msg_log - list to write messages to

        RETURNS: True if success, false if failure
        """
        
        msg_log.append((MSG_INFO_T, indent_lvl, SI_LOADING))
        select_info = obj_based.pop("select_info")
        
        
        if not _validate_params(
            select_info,
            save_obj,
            SEL_INFO_REQ_PARAM_NAMES,
            True,
            msg_log,
            indent_lvl + 1
        ):
            return False
        
        
        if not _validate_params(
            select_info,
            save_obj,
            SEL_INFO_OPT_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl + 1
        ):
            return False
        
        
        if "hover_dlg" in select_info:
            select_info.pop("hover_dlg")
        
        
        
        
        
        
        
        
        
        
        
        if "select_dlg" in select_info:
            if not _validate_iterstr(
                select_info,
                save_obj,
                "select_dlg",
                False,
                True,
                msg_log,
                indent_lvl + 1
            ):
                return False
        
        
        for extra_prop in select_info:
            msg_log.append((
                MSG_WARN_T,
                indent_lvl + 1,
                EXTRA_PROP.format(extra_prop)
            ))
        
        
        msg_log.append((MSG_INFO_T, indent_lvl, SI_SUCCESS))
        
        
        return True


    def addSpriteObject(filepath, post_proc_data):
        """
        Adds a sprite object, given its json filepath

        NOTE: most exceptions logged
        NOTE: may raise exceptions

        IN:
            filepath - filepath to the JSON we want to load

        OUT:
            post_proc_data - dict to store post processing data in
        """
        dry_run = False
        jobj = None
        obj_based_params = {}
        sp_obj_params = {}
        sel_params = {}
        unlock_hair = True
        giftname = None
        indent_lvl = 0
        
        log.info(READING_FILE.format(filepath), pfx_newline=True)
        
        
        with open(filepath, "r") as jsonfile:
            jobj = json.load(jsonfile)
        
        
        if jobj is None:
            log.error(JSON_LOAD_FAILED.format(filepath))
            return
        
        if DRY_RUN in jobj:
            jobj.pop(DRY_RUN)
            dry_run = True
        
        
        for jkey in jobj.keys():
            if jkey.startswith("__"):
                jobj.pop(jkey)
        
        
        if VERSION_TXT not in jobj:
            log.error(VER_NOT_FOUND)
            return
        
        
        version = jobj.pop(VERSION_TXT)
        
        
        if not _verify_int(version, allow_none=False):
            
            log.error(VER_BAD.format(SP_JSON_VER, version))
            return
        
        
        if version == FILENAME_FMT_VER:
            
            sp_obj_params["use_folders"] = False 
            log.warning(FILENAME_FMT)
        
        elif version != SP_JSON_VER:
            log.error(VER_BAD.format(SP_JSON_VER, version))
            return
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        msg_log = []
        sp_type = _validate_type(jobj, msg_log, indent_lvl)
        if parsewritelogs(msg_log):
            return
        
        
        if sp_type not in (SP_ACS, SP_HAIR):
            sp_obj_params.pop("use_folders", None) 
        
        
        msg_log = []
        _validate_params(
            jobj,
            sp_obj_params,
            REQ_SHARED_PARAM_NAMES,
            True,
            msg_log,
            indent_lvl
        )
        if parsewritelogs(msg_log):
            return
        
        
        sp_name = sp_obj_params["name"]
        
        
        log.info(SP_LOADING.format(
            SP_STR.get(sp_type),
            sp_name
        ))
        indent_lvl = 1
        
        
        
        if "pose_map" not in jobj:
            parsewritelog((MSG_ERR_T, indent_lvl, REQ_MISS.format("pose_map")))
            return
        
        
        for param_name in OBJ_BASED_PARAM_NAMES:
            if param_name in jobj:
                obj_val = jobj.pop(param_name)
                
                
                if not _verify_dict(obj_val, allow_none=False):
                    parsewritelog((
                        MSG_ERR_T,
                        indent_lvl,
                        BAD_TYPE.format(param_name, dict, type(obj_val))
                    ))
                    return
                
                obj_based_params[param_name] = obj_val
        
        
        msg_log = []
        _validate_params(
            jobj,
            sp_obj_params,
            OPT_SHARED_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl
        )
        if parsewritelogs(msg_log):
            return
        
        
        if sp_type == SP_ACS:
            
            msg_log = []
            _validate_acs(
                jobj,
                sp_obj_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return
        
        else:
            
            msg_log = []
            _validate_fallbacks(
                jobj,
                sp_obj_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return
            
            if sp_type == SP_HAIR:
                msg_log = []
                _validate_hair(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    msg_log,
                    indent_lvl
                )
                if parsewritelogs(msg_log):
                    return
            
            else:
                
                msg_log = []
                _validate_clothes(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    sp_name,
                    dry_run,
                    msg_log,
                    indent_lvl,
                    post_proc_data
                )
                if parsewritelogs(msg_log):
                    return
        
        
        msg_log = []
        _validate_ex_props(
            jobj,
            sp_obj_params,
            obj_based_params,
            msg_log,
            indent_lvl
        )
        if parsewritelogs(msg_log):
            return
        
        
        if "select_info" in obj_based_params:
            msg_log = []
            _validate_selectable(
                jobj,
                sel_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return
        
        
        
        
        for extra_prop in jobj:
            parsewritelog((
                MSG_WARN_T,
                indent_lvl,
                EXTRA_PROP.format(extra_prop)
            ))
        
        
        if "unlock" in sp_obj_params:
            unlock_hair = sp_obj_params.pop("unlock")
            giftname = None
        
        elif "giftname" in sp_obj_params:
            giftname = sp_obj_params.pop("giftname")
            
            
            msg_log = []
            _check_giftname(giftname, sp_type, sp_name, msg_log, indent_lvl)
            if parsewritelogs(msg_log):
                return
        
        elif sp_type != SP_HAIR:
            parsewritelog((MSG_WARN_T, indent_lvl, NO_GIFT))
            giftname = None
        
        
        msg_log = []
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msg_log,
            indent_lvl,
            "entry"
        )
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msg_log,
            indent_lvl,
            "exit"
        )
        parsewritelogs(msg_log)
        
        
        try:
            
            if sp_type == SP_ACS:
                
                if "arm_split" in sp_obj_params:
                    
                    sp_obj = store.MASSplitAccessory(**sp_obj_params)
                
                else:
                    
                    sp_obj = store.MASAccessory(**sp_obj_params)
                
                sms.init_acs(sp_obj)
                sel_obj_name = "acs"
            
            elif sp_type == SP_HAIR:
                sp_obj = store.MASHair(**sp_obj_params)
                sms.init_hair(sp_obj)
                sel_obj_name = "hair"
            
            else:
                
                sp_obj = store.MASClothes(**sp_obj_params)
                sms.init_clothes(sp_obj)
                sel_obj_name = "clothes"
        
        except Exception as e:
            
            log.exception(e)
            return
        
        
        msg_log = []
        _test_loadables(sp_obj, msg_log, 0)
        if parsewritelogs(msg_log):
            _reset_sp_obj(sp_obj)
            return
        
        
        
        if len(sel_params) > 0:
            sel_params[sel_obj_name] = sp_obj
            
            try:
                if sp_type == SP_ACS:
                    sml.init_selectable_acs(**sel_params)
                
                elif sp_type == SP_HAIR:
                    sml.init_selectable_hair(**sel_params)
                    if unlock_hair:
                        sml.unlock_hair(sp_obj)
                
                else:
                    
                    sml.init_selectable_clothes(**sel_params)
            
            except Exception as e:
                
                log.error(e.message)
                
                
                _reset_sp_obj(sp_obj)
                return
        
        
        if giftname is not None and not dry_run:
            _init_giftname(giftname, sp_type, sp_name)
        
        
        if dry_run:
            _reset_sp_obj(sp_obj)
            log.info(SP_SUCCESS_DRY.format(
                SP_STR.get(sp_type),
                sp_name
            ))
        
        else:
            sp_obj.is_custom = True
            log.info(SP_SUCCESS.format(
                SP_STR.get(sp_type),
                sp_name
            ))


    def addSpriteObjects(post_proc_data):
        """
        Adds sprite objects if we find any

        Also does delayed validation rules:
            - hair

        OUT:
            post_proc_data - data to be used in post processing code
                (should be a dict)
        """
        json_files = sprite_station.getPackageList(".json")
        
        if len(json_files) < 1:
            return
        
        
        for j_obj in json_files:
            j_path = sprite_station.station + j_obj
            try:
                addSpriteObject(j_path, post_proc_data)
            except Exception as e:
                
                log.exception(e)


    def initSpriteObjectProc():
        """
        Prepares internal data for sprite object processing
        """
        pass

    def verifyHairs():
        """
        Verifies all hair items that we encountered
        """
        log.info(HM_VER_ALL, pfx_newline=True)
        
        
        for hkey in hm_key_delayed_veri:
            if hkey not in HAIR_MAP:
                parsewritelog((
                    MSG_WARN_T,
                    1,
                    HM_NO_KEY.format(hkey, hm_key_delayed_veri[hkey])
                ))
        
        
        for hval in hm_val_delayed_veri:
            if hval not in HAIR_MAP:
                sp_name_list = hm_val_delayed_veri[hval]
                parsewritelog((
                    MSG_WARN_T,
                    1,
                    HM_NO_VAL.format(hval, sp_name_list)
                ))
                
                
                for sp_name in sp_name_list:
                    _replace_hair_map(sp_name, hval)
        
        log.info(HM_VER_SUCCESS)


    def processOutfitExtras(post_proc_data):
        """
        Processes outfit extras for sprites

        IN:
            post_proc_data - data set by the sprite object add alg
        """
        outfit_extras = post_proc_data["outfit_extras"]
        if len(outfit_extras) == 0:
            return
        
        log.info(OE_LOADING, pfx_newline=True)
        
        for sp_name in outfit_extras:
            outfit_hair = outfit_extras.get(sp_name, {}).get("hair", None)
            outfit_acs = outfit_extras.get(sp_name, {}).get("acs", None)
            
            if outfit_hair is not None:
                if outfit_hair in HAIR_MAP:
                    CLOTH_MAP[sp_name].outfit_hair = HAIR_MAP[outfit_hair]
                else:
                    parsewritelog((
                        MSG_WARN_T,
                        1,
                        OE_INVALID_HAIR.format(outfit_hair, sp_name),
                    ))
            
            if outfit_acs is not None:
                actual_acs = {}
                for acs_name in outfit_acs:
                    if acs_name in ACS_MAP:
                        actual_acs[acs_name] = ACS_MAP[acs_name]
                    else:
                        parsewritelog((
                            MSG_WARN_T,
                            1,
                            OE_INVALID_ACS.format(acs_name, sp_name),
                        ))
                
                if len(actual_acs) > 0:
                    CLOTH_MAP[sp_name].outfit_acs = actual_acs
        
        log.info(OE_SUCCESS)


    def _addGift(giftname, indent_lvl):
        """
        Adds the reaction for this gift, using the correct label depending on
        gift label existence.

        IN:
            giftname - giftname to add reaction for
            indent_lvl - indentation level to use
        """
        namegift = giftname_map.get(giftname, None)
        if namegift is None:
            return
        
        gifttype, spname = namegift
        rlstr = SP_RL.get(gifttype,  None)
        if rlstr is None:
            return
        
        
        reaction_label = rlstr.format(spname)
        if renpy.has_label(reaction_label):
            store.addReaction(reaction_label, giftname, is_good=True)
            parsewritelog((
                MSG_INFO_T,
                indent_lvl,
                GR_FOUND.format(SP_STR.get(gifttype), spname, giftname)
            ))
        
        else:
            parsewritelog((
                MSG_INFO_T,
                indent_lvl,
                GR_GEN.format(SP_STR.get(gifttype), spname, giftname)
            ))


    def processGifts():
        """
        Processes giftnames that were loaded, adding/removing them from
        certain dicts.
        """
        log.info(GR_LOADING, pfx_newline=True)
        
        frs_gifts = store.persistent._mas_filereacts_sprite_gifts
        msj_gifts = store.persistent._mas_sprites_json_gifted_sprites
        
        for giftname in frs_gifts.keys():
            if giftname in giftname_map:
                
                frs_gifts[giftname] = giftname_map[giftname]
            
            else:
                
                frs_gifts.pop(giftname)
        
        
        
        for giftname in giftname_map:
            if not giftname.startswith("__"):
                sp_data = giftname_map[giftname]
                
                
                if sp_data in msj_gifts:
                    
                    msj_gifts[sp_data] = giftname
                
                
                frs_gifts[giftname] = sp_data
                
                
                _addGift(giftname, 1)
        
        log.info(GR_SUCCESS)


init 190 python in mas_sprites_json:

    import store

    def runSpriteObjAlg():
        
        initSpriteObjectProc()
        post_proc_data = mas_utils.nested_defaultdict(levels=3)
        
        
        addSpriteObjects(post_proc_data)
        
        
        verifyHairs()
        processGifts()
        processOutfitExtras(post_proc_data)
        store.MASClothes.process_delayed_outfits()


    runSpriteObjAlg()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
