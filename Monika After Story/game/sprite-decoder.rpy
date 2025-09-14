
init python in mas_sprite_decoder:
    import json
    import store

    EYEBROW_MAP = dict()
    EYE_MAP = dict()
    MOUTH_MAP = dict()
    ARM_MAP = dict()







    HEAD_MAP = dict()
    SIDES_MAP = dict()

    SINGLE_MAP = dict()
    BLUSH_MAP = dict()
    TEAR_MAP = dict()
    SWEAT_MAP = dict()
    MOD_MAP = {}

    class MASSpriteException(Exception):
        def __init__(self, message):
            self.message = message
        
        def __str__(self):
            return self.message

    def _m1_sprite0x2ddecoder__loadSpriteMapData():
        """
        Loads sprite map data from the sprite map json file
        """
        global EYEBROW_MAP, EYE_MAP, MOUTH_MAP, ARM_MAP, HEAD_MAP
        global SIDES_MAP, SINGLE_MAP, BLUSH_MAP, TEAR_MAP, SWEAT_MAP
        global MOD_MAP
        
        jobj = None
        
        try:
            with open(store.os.path.join(renpy.config.gamedir, "mod_assets", "sprite_map.json"), "r") as jsonfile:
                jobj = json.load(jsonfile)
            
            EYEBROW_MAP = jobj["eyebrows"]
            EYE_MAP = jobj["eyes"]
            MOUTH_MAP = jobj["mouth"]
            ARM_MAP = jobj["arms"]
            HEAD_MAP = jobj["head"]
            SIDES_MAP = jobj["sides"]
            SINGLE_MAP = jobj["single"]
            BLUSH_MAP = jobj["blush"]
            TEAR_MAP = jobj["tears"]
            SWEAT_MAP = jobj["sweat"]
            MOD_MAP = jobj["MOD_MAP"]
            
            for sub_map in MOD_MAP.itervalues():
                for key, value in sub_map.iteritems():
                    sub_map[key] = set(value)
            
            
            ARM_MAP["5"] = tuple(ARM_MAP["5"])
            
            for side_key, side_list in SIDES_MAP.iteritems():
                SIDES_MAP[side_key] = tuple(side_list)
        
        
        except Exception as e:
            raise MASSpriteException(repr(e) + "\n\nPLEASE REINSTALL MAS TO CORRECT THIS ERROR")

    def _m1_sprite0x2ddecoder__process_blush(spcode, index, export_dict, *prefixes):
        """
        Processes a blush off the given sprite code at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the blush was valid, False if not
                [1] - the number of spots to increase the index by
        """
        
        fullcode = list(prefixes)
        fullcode.append(spcode[index])
        
        blush = BLUSH_MAP.get("".join(fullcode), None)
        
        if blush is None:
            return False, 0
        
        
        export_dict["blush"] = blush
        return True, 1

    def _m1_sprite0x2ddecoder__process_s(spcode, index, export_dict, *prefixes):
        """
        Processes the s-prefixed spcodes at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the processes were valid, False if not
                [1] - the number of spots to increase the index by
        """
        midfix = spcode[index]
        index += 1
        sprite_added = False
        
        processor = SUB_PROCESS_MAP["s"].get(midfix, None)
        
        if processor is not None:
            fullcode = list(prefixes)
            fullcode.append(midfix)
            
            sprite_added, increaseby = processor(
                spcode,
                index,
                export_dict,
                *fullcode
            )
        
        
        if not sprite_added:
            return False, 0
        
        
        return True, 1 + increaseby

    def _m1_sprite0x2ddecoder__process_sweatdrop(spcode, index, export_dict, *prefixes):
        """
        Processes a sweatdrop off the given spcode at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the sweatdrops were valid, False if not
                [1] - the number of spots to increase the index by
        """
        
        fullcode = list(prefixes)
        fullcode.append(spcode[index])
        
        sweatdrop = SWEAT_MAP.get("".join(fullcode), None)
        
        if sweatdrop is None:
            return False, 0
        
        
        export_dict["sweat"] = sweatdrop
        return True, 1

    def _m1_sprite0x2ddecoder__process_tears(spcode, index, export_dict, *prefixes):
        """
        Processes a tear off the given spcode at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the tears were valid, False if not
                [1] - the number of spots to increase the index by
        """
        
        fullcode = list(prefixes)
        fullcode.append(spcode[index])
        
        tears = TEAR_MAP.get("".join(fullcode), None)
        
        if tears is None:
            return False, 0
        
        
        tm_set = MOD_MAP.get("tears", {}).get(tears, None)
        eyes = export_dict["eyes"]
        if tm_set is not None and eyes in tm_set:
            tears += eyes
        
        
        export_dict["tears"] = tears
        return (True, 1)

    PROCESS_MAP = {
        "b": _m1_sprite0x2ddecoder__process_blush,
        "s": _m1_sprite0x2ddecoder__process_s,
        "t": _m1_sprite0x2ddecoder__process_tears,
    }

    SUB_PROCESS_MAP = {
        "s": {
            "d": _m1_sprite0x2ddecoder__process_sweatdrop,
        },
    }

    def parse_exp_to_kwargs(exp):
        """
        Converts exp codes to kwargs to pass into mas_drawmonika_rk

        IN:
            exp - spritecode to convert

        OUT:
            dict representing the exp as kwargs for mas_drawmonika_rk

        ASSUMES:
            exp is not in the staticsprite format (not exp_static)

        RAISES:
            - KeyError if pose, eyes, eyebrows, or mouth is invalid
            - Exception if optional sprite is invalid
        """
        full_code = exp
        kwargs = dict()
        
        
        arms = ARM_MAP[exp[0]]
        
        
        if isinstance(arms, tuple):
            
            kwargs["lean"], arms = arms
            
            
            kwargs["single"] = SINGLE_MAP.get(exp[-1], "3b")
        
        else:
            
            kwargs["left"], kwargs["right"] = SIDES_MAP[exp[0]]
        
        
        kwargs["arms"] = arms
        
        
        kwargs["head"] = HEAD_MAP.get("".join((exp[1], exp[2], exp[-1])), "")
        
        
        kwargs["eyes"] = EYE_MAP[exp[1]]
        
        
        kwargs["eyebrows"] = EYEBROW_MAP[exp[2]]
        
        
        kwargs["mouth"] = MOUTH_MAP[exp[-1]]
        
        
        exp = exp[3:-1]
        
        
        kwargs["nose"] = "def"
        
        index = 0
        while index < len(exp):
            prefix = exp[index]
            index += 1
            sprite_added = False
            
            
            processor = PROCESS_MAP.get(prefix, None)
            if processor is not None:
                sprite_added, increaseby = processor(
                    exp,
                    index,
                    kwargs,
                    prefix
                )
            
            
            if not sprite_added:
                raise Exception("Invalid sprite used: {0}".format(full_code))
            
            
            index += increaseby
        
        return kwargs

    def isValidSpritecode(exp):
        """
        Spritecode validity tester

        IN:
            exp - exp to check validity

        OUT:
            boolean:
                - True if code is valid
                - False otherwise
        """
        
        exp = exp.replace("_static", "")
        
        
        try:
            parse_exp_to_kwargs(exp)
            
            
            return True
        
        
        except:
            return False

    _m1_sprite0x2ddecoder__loadSpriteMapData()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
