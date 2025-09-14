


init -700 python in mas_deco:
    deco_def_db = {}


    vis_store = {}





init -20 python in mas_deco:
    import store

    deco_name_db = {}




    deco_db = {}





    LAYER_FRONT = 5
    LAYER_MID = 6
    LAYER_BACK = 7

    LAYERS = (
        LAYER_FRONT,
        LAYER_MID,
        LAYER_BACK,
    )


    DECO_PREFIX = "mas_deco_"


    def add_deco(s_name, obj):
        """
        Adds deco object to the deco db. Raises an exception if there are
        duplicates. All deco objects get prefixed wtih text to prevent
        collisions with standard sprite objects.

        IN:
            s_name - shorthand name to apply to this deco object
            obj - MASDecoration object to add to the deco db
        """
        if s_name in deco_name_db:
            raise Exception("Deco object '{0}' already exists".format(s_name))
        
        
        
        new_deco_name = DECO_PREFIX + s_name
        obj.name = new_deco_name
        
        deco_name_db[s_name] = new_deco_name
        deco_db[new_deco_name] = obj


    def _add_it_deco(obj):
        """
        Adds a MASImageTagDecoration object to the deco db. Raises exceptions
        if a duplicate was found OR if the object is not a
        MASImageTagDecoration.

        IN:
            obj - MASImageTagDecoration object to add to the deco db
        """
        if not isinstance(obj, store.MASImageTagDecoration):
            raise Exception("{0} is not MASImageTagDecoration".format(obj))
        
        
        
        if obj.name in deco_db:
            raise Exception("Deco object '{0}' already exists".format(
                obj.name)
            )
        
        deco_db[obj.name] = obj


    def get_deco(name):
        """
        Gets a deco object by name. This accepts shortname or regular deco name

        IN:
            name - can either be shortname or actual deco name

        RETURNS: MASDecoration object, or None if not valid name
        """
        if not name.startswith(DECO_PREFIX):
            name = deco_name_db.get(name, name)
        
        if name:
            return deco_db.get(name, None)
        
        return None


init -19 python:


    class MASRegImgSameDecoTagDefNotFoundException(Exception):
        """
        Exception for when a deco tag definition is not found while regisering
        an image using `register_img_same`
        """
        MSG = (
            "Cannot register tag '{0}' for BG '{1}'. \n"
            "Tag definition for source BG '{2}' does not exist. \n"
            "Try registering at a later init level."
        )
        
        def __init__(self, tag, bg_id_src, bg_id_dest):
            """
            Constructor

            IN:
                tag - the tag being registered
                bg_id_src - the ID of the source BG that the deco tag
                    definition could not be located for
                bg_id_dest - the ID of the destination BG being registered
            """
            super(MASRegImgSameDecoTagDefNotFoundException, self).__init__(
                self.MSG.format(tag, bg_id_dest, bg_id_src)
            )


    class MASDecorationBase(MASExtraPropable):
        """
        Base class for decortaions objects.

        INHERITED PROPS:
            ex_props- arbitrary properties associated with this deco object

        PROPERTIES:
            name - unique identifier of this deco object
        """
        
        def __init__(self, name, ex_props=None):
            """
            Constructor for base decoration objets

            IN:
                name - unique identifier to use for this deco object
                ex_props - dict of aribtrary properties associated with this
                    deco object.
                    (Default: None)
            """
            self.name = name
            super(MASDecorationBase, self).__init__(ex_props)
        
        def __eq__(self, other):
            if isinstance(other, MASDecorationBase):
                return self.name == other.name
            return NotImplemented
        
        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result


    class MASDecoration(MASDecorationBase):
        """
        Decoration object. Does NOT know positioning.

        PROPERTIES:
            name - unique identifier of this deco object
            ex_props - arbitrary properties associated with tihs deco object
        """
        
        def __init__(self, s_name, img=None, fwm=None, ex_props=None):
            """
            constructor for MASDecoration. this will auto add the
            deco object to the deco_db.

            IN:
                s_name - shortname for this deco object. This should be
                    unique.
                    NOTE: this object's real name will be set to something
                        different. To lookup deco objects,
                        see mas_deco.get_deco.
                img - image filepath associated with this deco object. If None,
                    then we assume fwm is set.
                    (Default: None)
                fwm - MASFilterWeatherMap to use for this deco object. pass
                    None to mark the deco object as a "simple" object that
                    gets the standard filters applied.
                    (Default: None)
                ex_props - dict of arbitrary properties associated with this
                    deco object.
                    (Default: None)
            """
            super(MASDecoration, self).__init__("", ex_props)
            
            
            store.mas_deco.add_deco(s_name, self)
            
            
            if img is None and fwm is None:
                raise Exception(
                    (
                        "Deco object '{0}' does not contain image or "
                        "MASFilterWeatherMap"
                    ).format(s_name)
                )
            
            self._img = img
            self._fwm = fwm 
            
            
            
            self._simple = fwm is None
        
        def __repr__(self):
            return "<MASDecoration: (name: {0}, img: {1})>".format(
                self.name,
                self.img
            )
        
        def is_simple(self):
            """
            Returns True if this is a simple deco object.
            Simple Deco objects do not have custom filter settings.

            RETURNS: True if simple deco object, False otherwise
            """
            return self._simple


    class MASImageTagDecoration(MASDecorationBase):
        """
        Variation of MASDecoration meant for images already defined as image
        tags in game.

        PROPERTIES:
            See MASDecorationBase
        """
        
        def __init__(self, tag, ex_props=None):
            """
            Constructor for MASImageTagDecoration

            IN:
                tag - image tag to build this decoration for. This is also
                    used as the decoration name.
                ex_props - arbitraary props to assocaitd with this deco object
                    (Default: None)
            """
            super(MASImageTagDecoration, self).__init__(tag, ex_props)
            
            
            
            store.mas_deco._add_it_deco(self)
        
        def __repr__(self):
            return "<MASImageTagDecoration: (tag: {0})>".format(self.name)
        
        @staticmethod
        def create(tag, ex_props=None):
            """
            Creates a MASImageTagDecoration and returns it. Will return an
            existing one if we find one with the same tag.

            IN:
                tag - tag to create MASImageTagDecoration for
                ex_props - passed to the MASImageTagDecoration constructor.
                    NOTE: will be ignored if an existing MASImageTagDecoration
                    exists.
                    (Default: None)

            RETURNS: MASImageTagDecoration to use
            """
            it_deco = store.mas_deco.get_deco(tag)
            if it_deco is not None:
                return it_deco
            
            return MASImageTagDecoration(tag, ex_props)


    class MASDecoFrame(object):
        """
        Contains position, scale, and rotation info about a decoration

        PROPERTIES:
            priority - integer priority that this deco frame should be shown.
                Smaller numbers are rendered first, and therefore can be hidden
                behind deco frames with higher priorities.
            pos - (x, y) coordinates of the top left of the decoration
            scale - (ws, hs) scale values to apply to the image's width and
                height. This is fed directly to FactorScale.
                    ws - multiplied to the decoration's image's width
                    hs - multiplied to the decoration's images' height
                Both scale values have a precision limit of 2 decimal places
            rotation - radians/degrees to rotate the decoration.
                NOTE: CURRENTLY UNUSED
        """
        
        def __init__(self, priority, pos, scale, rotation):
            """
            Constructor for a MASDecoFrame

            IN:
                priority - integer priority that this deco frame should be shown.
                pos - initial (x, y) coordinates to show the decoration on
                scale - (ws, hs) scale values to apply to the image's width and
                    height. This is fed directly to FactorScale.
                        ws - multiplied to the decoration's image's width
                        hs - multiplied to the decoration's images' height
                    Both scale values have a precision limit of 2 decimal places
            """
            self.priority = priority
            self.pos = pos
            self.scale = scale
            self.rotation = 0
        
        def __setattr__(self, name, value):
            """
            Set attr override for MASDecoFrame. This does very specific checks
            for all numerical values to ensure compliance. This is important
            since these are directly responsible for image appearance.
            """
            if name == "pos":
                
                value = (int(value[0]), int(value[1]))
            
            elif name == "scale":
                
                
                ws, hs = value
                
                if store.mas_utils.eqfloat(abs(ws), ws, 2):
                    ws = abs(ws)
                else:
                    ws = store.mas_utils.truncround(ws, 2)
                
                if store.mas_utils.eqfloat(abs(hs), hs, 2):
                    hs = abs(hs)
                else:
                    hs = store.mas_utils.truncround(hs, 2)
                
                value = (ws, hs)
            
            
            
            
            super(MASDecoFrame, self).__setattr__(name, value)
        
        def __repr__(self):
            return (
                "<MASDecoFrame: (pty: {0}, pos: {1}, scale: {2}, rot: {3})>"
            ).format(
                self.priority,
                self.pos,
                self.scale,
                self.rotation
            )
        
        def fromTuple(self, data):
            """
            Loads data from a tuple into this deco frame's propeties.

            IN:
                data - tuplized data of a MASDecoFrame. See toTuple for format

            RETURNS: True if successful, false otherwise
            """
            if len(data) < 5:
                
                return False
            
            
            self.pos = data[0]
            self.scale = (
                store.mas_utils.floatcombine_i(data[1], 2),
                store.mas_utils.floatcombine_i(data[2], 2),
            )
            self.rotation = data[3]
            self.priority = data[4]
            
            return True
        
        def toTuple(self):
            """
            Creates a tuple of this deco's properties for saving.

            RETURNS: tuple of the following format:
                [0]: position (x, y)
                [1]: width scale (integer, float part as integer)
                [2]: height scale (integer, float part as integer)
                [3]: rotation
                [4]: priority
            """
            return (
                self.pos,
                store.mas_utils.floatsplit_i(self.scale[0], 2),
                store.mas_utils.floatsplit_i(self.scale[1], 2),
                self.rotation,
                self.priority,
            )


    class MASAdvancedDecoFrame(object):
        """
        Advanced deco frame. Basically an interface around
        renpy.show params.

        Equivalence is supported, but only in positionig AND tag.

        PROPERTIES: NOTE: refer to renpy.show for info
            name - set when this is shown
            at_list
            layer
            what
            zorder
            tag - used as the decoration tag in deco db, if given
            behind
            real_tag - tag this image ends up being shown with.
        """
        
        def __init__(self,
                at_list=None,
                layer="master",
                what=None,
                zorder=0,
                tag=None,
                behind=None
        ):
            """
            Constructor.
            NOTE: all parameter doc is copied from renpy.show

            at_list - list of tranforms applyed to the image
                Equivalent of the `at` property
                (Default: None)
            layer - string, giving name of layer on which image will be shown
                Equivalent of the `onlayer` property
                (Default: None)
            what - if not None, displaybale that will be shown
                Equivalent of `show expression`.
                If provided, name will be the tag for the image
                (Default: None)
            zorder - integer for zorder
                if None, zorder is preserved, otherwise set to 0.
                Equivalent of `zorder` property
                (Default: 0)
            tag - ignored - do not use
            behind - list of strings, giving image tags that this image is
                shown behind.
                Equivalent of the `behind` property
            """
            if at_list is None:
                at_list = []
            if behind is None:
                behind = []
            
            self.at_list = at_list
            self.layer = layer
            self.what = what
            self.zorder = zorder
            self.tag = None
            self.behind = behind
            self.real_tag = None
            self.name = None
        
        def __eq__(self, other):
            if isinstance(other, MASAdvancedDecoFrame):
                return (
                    self.at_list == other.at_list
                    and self.layer == other.layer
                    and self.what == other.what
                    and self.zorder == other.zorder
                    and self.tag == other.tag
                    and self.behind == other.behind
                )
            
            return NotImplemented
        
        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result
        
        def hide(self):
            """
            Hides this image
            """
            if self.real_tag is not None:
                renpy.hide(self.real_tag, layer=self.layer)
                self.real_tag = None
                self.name = None
        
        def show(self, name):
            """
            Shows image at this deco frame

            IN:
                name - tag of the image to show
            """
            if name is None:
                return
            self.name = name
            
            
            if self.tag is None:
                self.real_tag = name
            else:
                self.real_tag = self.tag
            
            renpy.show(
                self.name,
                at_list=self.at_list,
                layer=self.layer,
                what=self.what,
                zorder=self.zorder,
                tag=self.tag,
                behind=self.behind
            )
        
        def showing(self, layer=None):
            """
            Analogus to renpy.showing

            IN:
                layer - layer to check, if None, uses the default layer for
                    the tag.
                    (Default: None)

            RETURNS: True if this deco frame is showing on the layer, False
                if not
            """
            return self.name is not None and renpy.showing(self.name, layer)


    class MASImageTagDecoDefinition(MASExtraPropable):
        """
        Class that defines bg-based properties for image tags.

        The Primary purpose of these is for auto image management when
        dealing with backgrounds. You can define position position information
        for every image for specific backgrounds (NOTE: this is via
        MASAdvancedDecoFrame)

        Defaults cannot be defined because of the general issues.
        Custom BGs should run the staticmethod register_img to setup
        their custom mapping (or override)

        PROPERTIES:
            deco - MASImageTagDecoration object associated with this definition
            bg_map - mapping of background ids to tuple:
                [0] - tag to use, or None to use the known tag
                [1] - adv deco frame
        """
        
        def __init__(self, deco):
            """
            Constructor

            IN:
                deco - MASImageTagDefintion object to use
            """
            self.deco = deco
            self.bg_map = {}
            
            if deco.name in store.mas_deco.deco_def_db:
                raise Exception("duplicate deco definition found")
            
            store.mas_deco.deco_def_db[deco.name] = self
        
        @staticmethod
        def get_adf(bg_id, tag):
            """
            Gets MASAdvancedDecoFrame for a bg for a given tag.

            IN:
                bg_id - background ID to get deco frame for
                tag - tag to get deco frame for

            RETURNS: MASAdvancedDecoFrame, or None if not found
            """
            deco_def = store.mas_deco.deco_def_db.get(tag, None)
            if deco_def is None:
                return None
            
            return deco_def.bg_map.get(bg_id, None)
        
        def get_img(self, bg_id):
            """
            Gets the tag and MASAdvancedDecoFrame to use for a bg for this
            definition.

            IN:
                bg_id - background ID to get img info for
                tag - tag to get img info for

            RETURNS: tuple (or None if not found)
                [0] - tag to use
                [1] - MASAdvancedDecoFrame to use
            """
            img_info = self.bg_map.get(bg_id, None)
            if img_info is None:
                return None
            
            tag, adf = img_info
            if tag is None:
                tag = self.deco.name
            
            return tag, adf
        
        @staticmethod
        def get_img_for_bg(bg_id, tag):
            """
            Gets the tag and MASAdvancedDecoFrame to use for a bg for a
            given main tag.

            IN:
                bg_id - backgroud ID to get img info for
                tag - tag to get img info for

            RETURNS: tuple (or None if not found)
                [0] - tag to use
                [1] - MASAdvancedDecoFrame to use
            """
            deco_def = store.mas_deco.deco_def_db.get(tag, None)
            if deco_def is None:
                return None
            
            return deco_def.get_img(bg_id)
        
        @staticmethod
        def get_img_setting(bg_id, tag):
            """
            Gets the tag and MASAdvancedDecoFrame setting to use for a bg for
            a given main tag.
            NOTE: do not use this for render. Use this for getting raw
            settings.

            IN:
                bg_id - background ID to get img info for
                tag - tag to get img info for

            RETURNS: tuple (or None if not found)
                [0] - tag used in the setting
                [1] - MASAdvancedDecoFrame used in the setting
            """
            deco_def = store.mas_deco.deco_def_db.get(tag, None)
            if deco_def is None:
                return None
            
            return deco_def.bg_map.get(bg_id, None)
        
        def register_bg(self, bg_id, adv_deco_frame, replace_tag=None):
            """
            Registers the given MASAdvanecdDecoFrame to this definition for
            a bg id.

            IN:
                bg_id - MASBackgroundID
                adv_deco_frame - MASAdvancedDecoFrame to register
                replace_tag - tag to use instead of the known tag
                    if None, then we use the known tag instead.
                    (Default: None)
            """
            self.bg_map[bg_id] = (replace_tag, adv_deco_frame)
        
        def register_bg_same(self, bg_id_src, bg_id_dest):
            """
            Register that a bg for this tag should use the same
            MASAdvancedDecoFrame + tag info as another bg.

            IN:
                bg_id_src - bg ID of the background to copy deco frame from
                bg_id_dest - bg ID of the background to use deco frame for
            """
            adf = self.bg_map.get(bg_id_src, None)
            if adf is not None:
                self.bg_map[bg_id_dest] = adf
        
        @staticmethod
        def register_img(tag, bg_id, adv_deco_frame, replace_tag=None):
            """
            Registers MASAdvancedDecoFrame for a BG and tag.
            Will create a new entry if the tag does not have a definition yet.
            NOTE: this will basically create a dummy MASImageTagDecoration
            object. Use store.mas_deco.get_deco to get the decoration object.

            IN:
                tag - tag to register decoframe for bg
                bg_id - id of teh bg to register decoframe for
                adv_dec_frame - the decoframe to register
                replace_tag - tag to use instead of the known tag for this bg
                    if None, then we use the known tag instead.
                    (Default: None)
            """
            deco_def = store.mas_deco.deco_def_db.get(tag, None)
            if deco_def is None:
                deco_def = MASImageTagDecoDefinition(
                    MASImageTagDecoration(tag)
                )
            
            deco_def.register_bg(bg_id, adv_deco_frame, replace_tag=replace_tag)
        
        @staticmethod
        def register_img_same(tag, bg_id_src, bg_id_dest):
            """
            Registers that a bg for a tag should use the same
            MASAdvancedDecoFRame + tag info as another bg for that tag.
            Will create a new entry if the tag does not have a definition yet.

            IN:
                tag - tag to register decoframe for
                bg_id_src - bg ID of the background to copy deco frame from
                bg_id_dest - bg ID of the background to use deco frame for
            """
            img_info = MASImageTagDecoDefinition.get_img_setting(
                bg_id_src,
                tag
            )
            
            
            if img_info is None:
                raise MASRegImgSameDecoTagDefNotFoundException(
                    tag,
                    bg_id_src,
                    bg_id_dest
                )
            
            replace_tag, adf = img_info
            MASImageTagDecoDefinition.register_img(
                tag,
                bg_id_dest,
                adf,
                replace_tag=replace_tag
            )


    class MASDecoManager(object):
        """
        Decoration manager for a background.
        Manages decoration objects and their assocation with layers.

        GETTING:
            This supports getting via bracket notation []
            If a tag does not exist, None is returned.

        PROPERTIES:
            changed - set when the decorations have changed and spaceroom
                will need to show new things. (should be set by callers)
        """
        
        def __init__(self):
            """
            Constructor
            """
            self._decos = {}
            
            
            
            
            self._adv_decos = {}
            
            
            
            
            self._deco_layer_map = {}
            
            
            
            self._deco_frame_map = {}
            
            
            
            self._deco_tag_override = {}
            
            
            
            self._deco_tag_override_r = {}
            
            
            
            self._deco_render_map = {
                store.mas_deco.LAYER_BACK: [],
                store.mas_deco.LAYER_MID: [],
                store.mas_deco.LAYER_FRONT: [],
            }
            
            
            
            self.changed = False
        
        def __getitem__(self, item):
            item = self.get_override_name(item)
            
            if item in self._adv_decos:
                return self._adv_decos[item]
            
            if item in self._decos:
                return self._decos[item]
            
            return None
        
        def _add_deco(self, layer, deco_obj, deco_frame):
            """
            Adds a decoration object to the deco manager.
            NOTE: if decoration has already been added, the existing decoration
            object is instead updated to the given layer and decoframe.

            NOTE: this should only be used for non-advanced decos

            IN:
                layer - layer to add deco object to
                deco_obj - MASDecoration object to add
                deco_frame - MASDecoFrame to associated with deco object
            """
            if deco_obj.name in self._decos:
                
                
                old_layer = self._deco_layer_map,get(deco_obj.name, None)
                if old_layer is not None:
                    decos = self._deco_render_map.get(old_layer, [])
                    if deco_obj in decos:
                        decos.remove(deco_obj)
        
        
        
        
        
        
        
        
        def _adv_add_deco(self, deco_obj, adv_deco_frame, override_tag=None):
            """
            Adds a decoration object to teh deco manager.
            This is meant for Advanced DecoFrames

            IN:
                deco_obj - MASDecoration object to add
                adv_deco_frame - MASAdvancedDecoFRame to associate with deco
                    object.
                override_tag - tag to use as the "name" for this deco
            """
            self._adv_decos[deco_obj.name] = deco_obj
            self._deco_frame_map[deco_obj.name] = adv_deco_frame
            
            if override_tag is not None:
                self._deco_tag_override[override_tag] = deco_obj.name
                self._deco_tag_override_r[deco_obj.name] = override_tag
        
        def add_back(self, deco_obj, deco_frame):
            """
            Adds a decoration object to the back deco layer
            """
        
        
        
        def add_front(self, deco_obj, deco_frame):
            """
            Adds a decoration object to the front deco layer
            """
        
        
        
        def add_mid(self, deco_obj, deco_frame):
            """
            Adds a decoration object to the middle deco layer
            """
        
        
        
        def deco_iter(self):
            """
            Generator that yields deco objects and their frames

            TODO: probably should return more than this

            YIELDS: tuple contianing deco object and frame
            """
        
        
        def deco_iter_adv(self):
            """
            Generates iter of advanced deco objects and their frames

            RETURNS: iter of tuple:
                [0] - deco object
                [1] - adv deco frame
                [2] - the override tag (will be the same as deco object's name
                    if no override tag given)
            """
            for deco_name, deco_obj in self._adv_decos.items():
                yield (
                    deco_obj,
                    self._deco_frame_map[deco_name],
                    self._deco_tag_override_r.get(deco_name, deco_name)
                )
        
        def diff_deco_adv(self, deco, adv_df):
            """
            Checks diffs between the given deco + frame and the the same deco
            in this manager.

            IN:
                deco - deco to check
                adv_df - MASAdvancedDecoFrame to check

            RETURNS: integer code:
                0 - the given deco and equivalent frame exist in this
                    deco manager.
                1 - the given deco exists but has a different frame in this
                    deco manager.
                -1 - the given deco does NOT exist in this deco manager.
            """
            df = self._deco_frame_map.get(deco.name, None)
            if df is None:
                return -1
            
            if df == adv_df:
                return 0
            
            return 1
        
        def get_override_name(self, name):
            """
            Gets the tag name that is actually being used for the given name

            IN:
                name - name to get real tag name for

            RETURNS: the real tag name
            """
            return self._deco_tag_override.get(name, name)
        
        def rm_deco(self, name):
            """
            REmoves all instances of the deco with the given name from this
            deco manager.

            IN:
                name - tag, either deco name or image tag, of the deco object
                    to remove
            """
            name = self.get_override_name(name)
            
            deco_obj = None
            if name in self._decos:
                deco_obj = self._decos.pop(name)
            
            if name in self._adv_decos:
                deco_obj = self._adv_decos.pop(name)
            
            if name in self._deco_frame_map:
                self._deco_frame_map.pop(name)
            
            deco_lst = self._deco_render_map.get(
                self._deco_layer_map.get(name, None),
                []
            )
            if deco_obj in deco_lst:
                deco_lst.remove(deco_obj)



    def mas_showDecoTag(tag, show_now=False):
        """
        Shows a decoration object that is an image tag.

        NOTE: this should be called when you want to show a decoration-based
        image, regardless of background. This will refer to the image tag
        definition to determine how the object will be shown.

        To hide an image shown this way, see mas_hideDecoTag.

        IN:
            tag - the image tag to show
            show_now - set to True to show immediately
                (Deafult: False)
        """
        
        store.mas_deco.vis_store[tag] = None
        mas_current_background._deco_add(tag=tag)
        
        if show_now:
            deco_info = mas_current_background.get_deco_info(tag)
            if deco_info is not None:
                real_tag, adf = deco_info
                if adf is not None:
                    adf.show(real_tag)
        else:
            mas_current_background._deco_man.changed = True


    def mas_hideDecoTag(tag, hide_now=False):
        """
        Hides a decoration object that is an image tag

        NOTE: this should be called when you want to hide a decoration-based
        image, regardless of background.

        This is primarily for hiding images shown with the mas_showDecoTag
        function.

        IN:
            tag - the image tag to hide
            hide_now - set to True to hide immediately
                (Default: False)
        """
        if tag in store.mas_deco.vis_store:
            store.mas_deco.vis_store.pop(tag)
        
        if hide_now:
            deco_info = mas_current_background.get_deco_info(tag)
            if deco_info is not None:
                ignore, adf = deco_info
                if adf is not None:
                    adf.hide()
        else:
            mas_current_background._deco_man.changed = True


    def mas_isDecoTagEnabled(tag):
        """
        Checks if the given deco tag is in the vis store, which means its
        slated to be visible if it can be.

        IN:
            tag - the image tag to check

        RETURNS: True if the deco is slated to be visible, False if not
        """
        return tag in store.mas_deco.vis_store


    def mas_isDecoTagVisible(tag):
        """
        Checks if this deco is showing - as in the image associated with
        this tag is being rendered (including replace tag depending on bg)

        IN:
            tag - the image tag to check

        RETURNS: True if the deco is being shown, false if not
        """
        deco_info = mas_current_background.get_deco_info(tag)
        if deco_info is None:
            return False
        
        real_tag, adf = deco_info
        if adf is None:
            return False
        
        return adf.showing()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
