init offset = -2


python early:





    class MASFilterException(Exception):
        """
        General filter exceptions
        """
        
        def __init__(self, msg):
            """
            Constructor

            IN:
                msg - messgae to show
            """
            self.msg = msg
        
        def __str__(self):
            return self.msg


    class MASInvalidFilterException(MASFilterException):
        """
        Use when an invalid filter is being used
        """
        
        def __init__(self, bad_flt):
            """
            Constructor

            IN:
                bad_flt - the invalid filter being used
            """
            self.msg = "'{0}' is not a valid filter".format(bad_flt)


    class MASFilterable(renpy.Displayable):
        """
        Special displayable that adjusts its image based on filter.
        Also includes surface caching, if desired.

        PROPERTIES:
            flt - filter we last used
        """
        
        def __init__(self,
                focus=None,
                default=False,
                style='default',
                _args=None,
                **properties
        ):
            """
            Constructor

            IN:
                All params are passed to Displayable
            """
            super(renpy.Displayable, self).__init__(
                focus=focus,
                default=default,
                style=style,
                _args=_args,
                **properties
            )
            self.flt = None
        
        
        
        def apply_filter(self, img_base, flt=None):
            """
            Applies the current filter to the given image base.

            IN:
                img_base - the image to apply filter to
                flt - filter to use, leave None to use the internal filter.
            """
            if flt is None:
                flt = self.flt
            return store.mas_sprites._gen_im(flt, img_base)
        
        def current_filter(self):
            """
            Gets the current filter (not internal)

            RETURNS: the current filter
            """
            return store.mas_sprites.get_filter()
        
        def per_interact(self):
            """
            Decides if this displayable should be redrawn on an interaction.
            """
            if self.update_filter():
                renpy.redraw(self, 0)
        
        def safe_apply_filter(self, img_base):
            """
            Updates the filter before applying it.

            IN:
                img_base - the image to apply filter to
            """
            self.update_filter()
            return self.apply_filter(img_base)
        
        def update_filter(self):
            """
            Updates the internal filter

            RETURNS: True if the filter chagned
            """
            new_flt = self.current_filter()
            if new_flt != self.flt:
                self.flt = new_flt
                return True
            
            return False


    class MASFilterableSprite(MASFilterable):
        """
        Generic Filterable Sprite with Highlight support

        Potentially more optimal than MASFilterSwitch, but likely to have less
        configuration.

        NOTE:
            Many of the style properties will likely NOT work with this.
            If you can make it work, submit a PR.

        PROPERTIES:
            img_path - image path of this sprite
            img_obj = Image object of this sprite
            highlight - MASFilterMap of highlights to use
        """
        
        def __init__(self,
                image_path,
                highlight,
                focus=None,
                default=False,
                style='default',
                _args=None,
                **properties
        ):
            """
            Constructor

            IN:
                image_path - MUST be an image path string.
                highlight - MASFilterMap object of highlights to apply
            """
            super(MASFilterableSprite, self).__init__(
                focus=focus,
                default=default,
                style=style,
                _args=_args,
                **properties
            )
            self.img_path = image_path
            self.img_obj = Image(image_path)
            self.highlight = highlight
            
            self._last_flt = self.flt
        
        def _m1_sprite0x2dchart0x2dmatrix__gen_hl(self):
            """
            Builds highlight Image based on current filters and cache

            REUTRNS: Image to use as highlight, None if we shouldnt make filter
            """
            
            if self.highlight is None:
                return None
            
            
            img_key = (self.flt, self.img_path)
            hlg_c = store.mas_sprites._gc(store.mas_sprites.CID_HLG)
            if img_key in hlg_c:
                return hlg_c[img_key]
            
            
            hlcode = self.highlight.get(self.flt)
            
            
            if hlcode is None:
                hlg_c[img_key] = None
                return None
            
            
            new_img = store.mas_sprites._bhlifp(self.img_path, hlcode)
            hlg_c[img_key] = new_img
            return new_img
        
        def render(self, width, height, st, at):
            """
            Render function
            """
            
            self.flt = store.mas_sprites.get_filter()
            
            
            new_img = store.mas_sprites._gen_im(self.flt, self.img_obj)
            
            
            hl_img = self._m1_sprite0x2dchart0x2dmatrix__gen_hl()
            
            
            
            
            
            if hl_img is None:
                
                
                
                render = renpy.render(new_img, width, height, st, at)
                rw, rh = render.get_size()
                rv = renpy.Render(rw, rh)
                rv.blit(render, (0, 0))
            
            else:
                
                render_list = [
                    renpy.render(img, width, height, st, at)
                    for img in (new_img, hl_img)
                ]
                
                
                rw, rh = render_list[0].get_size()
                rv = renpy.Render(rw, rh)
                
                
                for render in render_list:
                    rv.blit(render, (0, 0))
            
            
            return rv
        
        def per_interact(self):
            """
            Decides whether or no we should redraw this displayable
            on an interaction
            """
            if self._last_flt != self.flt:
                self._last_flt = self.flt
                renpy.redraw(self, 0.0)
        
        def visit(self):
            self.flt = store.mas_sprites.get_filter()
            
            
            new_img = store.mas_sprites._gen_im(self.flt, self.img_obj)
            
            
            hl_img = self._m1_sprite0x2dchart0x2dmatrix__gen_hl()
            
            
            if hl_img is None:
                return [new_img]
            
            return [new_img, hl_img]


    def MASFilterSwitch(img):
        """
        Builds a condition switch that applies appropriate filters.

        NOTE: as this returns a ConditionSwitch, use this when you need
            more renpy-based control over an image.

        IN:
            img - image path/ImageBase to build filter switch for
                NOTE: CANNOT BE A DISPLAYABLE

        RETURNS: ConditionSwitch for filters
        """
        if isinstance(img, basestring):
            img = renpy.substitute(img)
        
        args = []
        for flt in store.mas_sprites.FILTERS.iterkeys():
            
            
            args.append("store.mas_sprites.get_filter() == '{0}'".format(flt))
            
            
            args.append(store.mas_sprites._gen_im(flt, img))
        
        return ConditionSwitch(*args)


    def MASLiteralFilterSwitch(def_img, filterize_def, **flt_pairs):
        """
        Builds a filter switch that lets you explicitly define the images
        for a filter.

        NOTE: this is a bad choice to use UNLESS you have a good default.

        IN:
            def_img - the default image to use for any filter not defined.
            filterize_def - True will apply filters to the default image
                as appropraite, False will NOT apply filters.
                Setting this as False may result in a sprite that looks shit
                in certain settings.
            **flt_pairs - name=value args for specific filters:
                name: filter enum (day/night/etc...)
                value: the image value to use for that filter

        RETURNS: ConditionSwitch with filter support
        """
        return MASDictFilterSwitch(def_img, filterize_def, flt_pairs)


    def MASDictFilterSwitch(def_img, filterize_def, flt_pairs):
        """
        Builds a filter switch that lets you explicitly define the images
        for a filter.

        NOTE: this is a bad choice to use UNLESS you have a good default.

        IN:
            def_img - the default image to use for any filter not defined.
            filterize_def - True will apply filters to the default image
                as appropraite, False will NOT apply filters.
                Setting this as False may result in a sprite that looks shit
                in certain settings.
            flt_pairs - dict mapping filtesr to images
                key: filter enum (day/night/etc...)
                value: the image value to use for that filter

        RETURNS: ConditionSwitch with filter support
        """
        args = []
        
        
        for flt in flt_pairs:
            if flt in store.mas_sprites.FILTERS:
                
                args.append("mas_isCurrentFlt('{0}')".format(flt))
                
                
                args.append(flt_pairs[flt])
        
        
        if filterize_def:
            
            
            for flt in store.mas_sprites.FILTERS.iterkeys():
                
                
                if flt not in flt_pairs:
                    
                    args.append("mas_isCurrentFlt('{0}')".format(flt))
                    
                    
                    args.append(store.mas_sprites._gen_im(flt, def_img))
        
        else:
            
            args.append("True")
            args.append(def_img)
        
        return ConditionSwitch(*args)


    def MASDayNightFilterSwitch(day_img, night_img):
        """
        Builds a filter switch that changes image based on if the current flt
        is a day/night filter.

        This does NOT apply any filters.

        IN:
            day_img - image to return if day flt is in use
            night_img - image to return if night flt is in use

        RETURNS: ConditionSwitch that works with day/night filters.
        """
        return ConditionSwitch(
            "store.mas_current_background.isFltDay()", day_img,
            "store.mas_current_background.isFltNight()", night_img
        )


    def MASFilteredSprite(flt, img):
        """
        Generates an already filtered version of the given image

        IN:
            flt - filter to use
            img_base - image path/ImageBase to build filtered sprite for

        RETURNS: Displayable of the filtered image
        """
        return renpy.easy.displayable(store.mas_sprites._gen_im(flt, img))


    def MASFallbackFilterDisplayable(**filter_pairs):
        """
        Generates a dynamic displayable for filters that applies fallback
        mechanics. If you don't need fallback mechanics, use the filter
        switches.

        IN:
            **filter_pairs - filter=val args to use. invalid filters are
                ignored.

        RETURNS: Dynamic displayable that handles fallback filters
        """
        return DynamicDisplayable(
            mas_fbf_select,
            MASFilterMapFallback(**filter_pairs)
        )


    def MASFilterWeatherDisplayable(use_fb, **filter_pairs):
        """
        Generates a dynamic displayable that maps filters to weathers for
        arbitrary objects.

        This supports fallback-based value getting. For example:
            Assuming there are 3 precip types (pt - 1, 2, 3)
            and there are 4 filters (flt - A, B, C, D)
            Fallback is denoted by fb
            Precip type 1 is the DEFAULT precip type.

            Let's say the configuration for this MASFilterWeatherDisp is:

            flt A - pt 1, 2, 3
            flt B - pt 1, 3     - fb: A
            flt C - pt 2        - fb: B

            flt B is a fallback for flt D, but flt D is NOT defined in this
            MASFilterWeatherDisp.

            This is what would happen for combinations of filter, precip_type,
            and use_fb settings:

            Current flt: A - Current pt: 2 - use_fb: any
            In this case, flt A is defined and has a value for precip type 2.
            The image at flt A, pt 2 is selected.

            Current flt: B - Current pt: 3 - use_fb: any
            In this case, flt B is defined and has a value for pt 3. The image
            at flt B, pt 3 is selected.

            Current flt: B - Current pt: 2 - use_fb: True
            In this case, flt B does not have a precip_type of 2. Since we are
            using fallback mode and flt A is a fallback of B, the image at
            flt A, pt 2 is selected.

            Current flt: B - Current pt: 2 - use_fb: False
            This is the same case as above except we are NOT using fallback
            mode. In this case, the image at flt B, pt 1 is selected since it
            is the default precip type.

            Current flt: C - Current pt: 3 - use_fb: True
            In this case, flt C does not have a pt of 3. Since we are using
            fallback mode and flt B is a fallback of C, the image at flt B,
            pt 3 is selected.

            Current flt: C - Current pt: 3 - use_fb: False
            This case would NEVER happen because an exception would be raised
            on startup. If use_fb is False, a default precip type must be
            defined for all filters.

            Current flt: D - Current pt: 3 - use_fb: True
            In this case, flt D is not defined in this MASFilterWeatherDisp.
            Since we are using fallback mode and flt B is a fallback of flt D,
            the image at flt B, pt 3 is selected.

            Current flt: D - Current pt: 3 - use_fb: False
            In thise, flt D is not defined. Even though we are NOT using
            fallback mode, since flt B is a fallback of flt D, the image at
            flt B, pt 3 is selected.

            Current flt: D - Current pt: 2 - use_fb: True
            In this case, flt D is not defined, but flt B does NOT have an
            image for pt 2. Since we are using fallback mode, flt B is a
            fallback of flt D, and flt A is a fallback of flt B, the image at
            flt A, pt 2 is selected.

            Current flt: D - Current pt: 2 - use_fb: False
            In thise case, flt D is not defined. Since we are NOT using
            fallback mode and flt B does NOT have an image for pt 2, the image
            at flt B, pt 1 is selected as it is the default precip type.

        In terms of filter_pairs, if fallback-based getting is used, then
        only the base filters need a PRECIP_TYPE_DEF to be valid for all
        filter+weather type combinations. If normal getting is used, then
        every filter will need PRECIP_TYPE_DEF to be set or else images may
        not exist for a filter. This is checked on startup at init level 2.

        IN:
            use_fb - set to True to use filter fallback-based value getting.
                This will use the filter fallback mapping to retrieve values
                for a precip_type if a selected filter does not have a value
                for a precip_type. See above for an example.
                False will use standard value getting.
            **filter_pairs - fitler pairs to pass directly to
                MASFilterWeatherMap

        RETURNS: DynamicDisplayable that respects Filters and weather.
        """
        return MASFilterWeatherDisplayableCustom(
            mas_fwm_select,
            use_fb,
            **filter_pairs
        )


    def MASFilterWeatherDisplayableCustom(dyn_func, use_fb, **filter_pairs):
        """
        Version of MASFilterWeatherDisplayable that accepts a custom function
        to use instead of the default mas_fwm_select.

        See MASFilterWeatherDisplayable for explanations of this kind of disp.

        NOTE: in general, you should use MASFilterWeatherDisplayable.
        """
        
        new_map = MASFilterWeatherMap(**filter_pairs)
        new_map.use_fb = use_fb
        
        
        new_id = store.mas_sprites.FW_ID + 1
        store.mas_sprites.FW_DB[new_id] = new_map
        store.mas_sprites.FW_ID += 1
        
        
        return DynamicDisplayable(dyn_func, new_map)


init python:

    def mas_fwm_select(st, at, mfwm):
        """
        Selects an image based on current filter and weather.

        IN:
            st - renpy related
            at - renpy related
            mfwm - MASFilterWeatherMap to select image wtih

        RETURNS: dynamic disp output
        """
        return (
            mfwm.fw_get(
                store.mas_sprites.get_filter(),
                store.mas_current_weather
            ),
            None
        )


    def mas_fbf_select(st, at, mfmfb):
        """
        Selects an image based on current filter, respecting fallback
        mechanics.

        IN:
            st - renpy related
            at - renpy related
            mfmfb - MASFilterMapFallback object to select image with

        RETURNS: dynamic disp output
        """
        return mfmfb.get(store.mas_sprites.get_filter()), None


init 3 python in mas_sprites:

    def _verify_fwm_db():
        """
        Verifies that data in the FW_DB is correct.
        MASFilterWeatherMaps are valid if:
            1. if the MFWM is fallback-based:
                a) All filters provided include a fallback filter with
                    PRECIP_TYPE_DEF set.
            2. If the MFWM is standard:
                a) All filters contain a PRECIP_TYPE_DEF set.

        Raises all errors.
        """
        for mfwm_id, mfwm in FW_DB.iteritems():
            _verify_mfwm(mfwm_id, mfwm)


    def _verify_mfwm(mfwm_id, mfwm):
        """
        Verifies a MASFilterWeatherMap object.

        Raises all errors.

        IN:
            mfwm_id - ID of the MASFilterWeatherMap object
            mfwm - MASFilterWeatherMap object to verify
        """
        if mfwm.use_fb:
            
            
            
            flt_defs = {}
            
            for flt in mfwm.flts():
                if not _mfwm_find_fb_def(mfwm, flt, flt_defs):
                    raise Exception(
                        (
                            "MASFilterWeatherMap does not have default "
                            "precip type set in the fallback chain for "
                            "filter '{0}'. ID: {1}"
                        ).format(
                            flt,
                            mfwm_id
                        )
                    )
        
        else:
            
            for flt in mfwm.flts():
                wmap = mfwm._raw_get(flt)
                if wmap._raw_get(store.mas_weather.PRECIP_TYPE_DEF) is None:
                    raise Exception(
                        (
                            "MASFilterWeatherMap does not have a default "
                            "precip type set for filter '{0}'. ID: {1}"
                        ).format(
                            flt,
                            mfwm_id
                        )
                    )


    def _mfwm_find_fb_def(mfwm, flt, flt_defs):
        """
        Finds fallbacks from a starting flt that are covered with a default
        precip type.

        IN:
            mfwm - MASFilterWeatherMap object we are checking
            flt - filter we are checking for fallbacks
            flt_defs - dict containing keys of filters that already have known
                defaults in their fallback chains.

        OUT:
            flt_defs - additional filters with known defaults are added to this
                dict as we go through the fallback chain of the given flt.

        RETURNS: True if we found a non-None default precip type. False if not
        """
        
        if flt in flt_defs:
            return True
        
        
        memo = {}
        ord_memo = []
        curr_flt = _find_next_fb(flt, memo, ord_memo)
        while not mfwm.has_def(curr_flt):
            nxt_flt = _find_next_fb(curr_flt, memo, ord_memo)
            
            
            if nxt_flt == curr_flt:
                
                return False
            
            if nxt_flt in flt_defs:
                
                
                flt_defs.update(memo)
                return True
            
            curr_flt = nxt_flt
        
        
        
        flt_defs.update(memo)
        return True


    def _find_circ_fb(flt, memo):
        """
        Tries to find circular fallbacks.
        Assumes that the current flt has not been placed into memo yet.

        IN:
            flt - flt we are checking
            memo - dict of all flts we traversed here

        OUT:
            memo - if False is returned, all keys in this memo are deemed to
                be non-circular fallbacks.

        RETURNS: True if circular fallback is found, False otherwise
        """
        
        if flt in memo:
            return True
        
        
        memo[flt] = True
        
        
        next_flt = _rslv_flt(flt)
        if next_flt == flt:
            FLT_BASE[flt] = True
            return False
        
        
        return _find_circ_fb(next_flt, memo)


    def _find_next_fb(flt, memo, ordered_memo):
        """
        Finds next filter and stores in memo and ordered memo

        IN:
            flt - filter to find next filter for

        OUT:
            memo - dict to add the next filter as a key if not None
            ordered memo - list to append the next filter if not None

        RETURNS: the next filter, or None if no next filter.
        """
        nxt_flt = _rslv_flt(flt)
        if nxt_flt != flt:
            memo[nxt_flt] = True
            ordered_memo.append(nxt_flt)
        
        return nxt_flt


    def _verify_flt_fb():
        """
        Verifies that there are no circular fallbacks in the filter
        fallback dict.

        Raises an error if circular fallbacks are found
        """
        non_cd = {}
        
        for flt in FLT_FB:
            memo = {}
            if _find_circ_fb(flt, memo):
                raise Exception("filter '{0}' has a circular fallback".format(
                    flt
                ))
            
            
            non_cd.update(memo)



    _verify_flt_fb()
    _verify_fwm_db()


init 1 python in mas_sprites:

    _m1_sprite0x2dchart0x2dmatrix__ignore_filters = True



init -97 python in mas_sprites:
    import store
    import store.mas_utils as mas_utils

    FW_ID = 1

    FW_DB = {}











    FLT_DAY = "day"
    FLT_NIGHT = "night"
    FLT_SUNSET = "sunset"


    FILTERS = {
        FLT_DAY: store.im.matrix.identity(),
        FLT_NIGHT: store.im.matrix.tint(0.59, 0.49, 0.55),
        FLT_SUNSET: store.im.matrix.tint(0.93, 0.82, 0.78),
    }




    FLT_FB = {
        FLT_SUNSET: FLT_DAY
    }






    FLT_BASE = {}


    _m1_sprite0x2dchart0x2dmatrix__ignore_filters = False



    _m1_sprite0x2dchart0x2dmatrix__flt_global = FLT_DAY


    def add_filter(flt_enum, imx, base=None):
        """
        Adds a filter to the global filters
        You can also use this to override built-in filters.

        NOTE: if you plan to use this, please use it before init level -1
        Filters beyond this level will be ignored.

        NOn-pythonable filter names are ignored

        IN:
            flt_enum - enum key to use as a filter.
            imx - image matrix to use as filter
            base - filter to use as a backup for this filter. Any images
                that are unable to be shown for flt_enum will be revert to
                the base filter.
                This should also be a FLT_ENUM.
                This is checked to make sure it is a valid, preexisting enum,
                so if chaining multiple bases, add them in order.
                If None, no base is given for the flt.
                (Default: None)
        """
        
        if _m1_sprite0x2dchart0x2dmatrix__ignore_filters:
            store.mas_utils.mas_log.warning(
                "Cannot add filter '{0}' after init -1".format(flt_enum)
            )
            return
        
        
        if not _test_filter(flt_enum):
            return
        
        
        if base is not None:
            if base not in FILTERS:
                store.mas_utils.mas_log.warning(
                    "Cannot add filter '{0}' with base '{1}', base flt does not exist".format(flt_enum, base)
                )
                return
            
            if not _test_filter(base):
                return
            
            FLT_FB[flt_enum] = base
        
        FILTERS[flt_enum] = imx

    @store.mas_utils.deprecated(use_instead="get_filter", should_raise=True)
    def _decide_filter():
        """DEPRECATED
        Please use get_filter
        """
        return get_filter()


    def get_filter():
        """
        Returns the current filter

        RETURNS: filter to use
        """
        return _m1_sprite0x2dchart0x2dmatrix__flt_global


    def is_filter(flt):
        """
        Checks if the given filter is a valid filter

        IN:
            flt - filter enum to check

        RETURNS: True if valid filter, False if not
        """
        return flt in FILTERS


    def _rslv_flt(flt):
        """
        Gets base filter for a flt.

        IN:
            flt - flt to get base filter for

        RETURNS: base flt for flt, or the flt itself if no base
        """
        return FLT_FB.get(flt, flt)


    def set_filter(flt_enum):
        """
        Sets the current filter if it is valid.
        Invalid filters are ignored.

        IN:
            flt_enum - filter to set
        """
        global _m1_sprite0x2dchart0x2dmatrix__flt_global
        if flt_enum in FILTERS:
            _m1_sprite0x2dchart0x2dmatrix__flt_global = flt_enum


    def _test_filter(flt_enum):
        """
        Checks if this filter enum can be a filter enum.

        Logs to mas log if there are errors

        IN:
            flt_enum - filter enum to test

        RETURNS: True if passed test, False if not
        """
        fake_context = {flt_enum: True}
        try:
            eval(flt_enum, fake_context)
            return True
        except:
            store.mas_utils.mas_log.warning(
                "Cannot add filter '{0}'. Name is not python syntax friendly".format(flt_enum)
            )
        
        return False


init -96 python:




    def mas_isCurrentFlt(flt):
        """
        Checks if the given filter is the current filter.

        IN:
            flt - filter to check

        RETURNS: True if flt is the current filter, false if not
        """
        return store.mas_sprites.get_filter() == flt



init -2 python in mas_sprites:





    CID_FACE = 1 
    CID_ARMS = 2
    CID_BODY = 3
    CID_HAIR = 4
    CID_ACS = 5
    CID_TC = 6
    CID_HL = 7
    CID_HLG = 8
    CID_BG = 9 


    CID_DYNAMIC = -2



    CACHE_TABLE = {
        CID_FACE: {},
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        CID_ARMS: {},
        
        
        
        
        
        
        
        
        

        CID_BODY: {},
        
        
        
        
        
        
        

        CID_HAIR: {},
        
        
        
        
        
        
        

        CID_ACS: {},
        
        
        
        
        
        
        
        
        

        CID_TC: {},
        
        
        
        
        
        
        
        
        

        CID_HL: {},
        
        
        
        
        
        
        

        CID_HLG: {}
        
        
        
        
        
        
        
        
        
    }

    MFM_CACHE = {}





    def _clear_caches():
        """
        Clears all caches
        """
        for cid, cache in CACHE_TABLE.iteritems():
            for key in cache.keys():
                cache.pop(key)
        
        for key in MFM_CACHE.keys():
            MFM_CACHE.pop(key)


    class MASMonikaRender(store.MASFilterable):
        """
        custom rendering class for MASMonika. This does caching and rendering
        at the same time.

        INHERED PROPS:
            flt - filter we are using (string)

        PROPERTIES:
            render_keys - list of tuples of the following format:
                [0] - key of an image to generate. used to check cache
                [1] - cache ID of the cache to use
                [2] - ImageBase to build the image, IF NOT IN CACHE.
                    This should be set to None if we are sure a surf
                    object is in the cache.
                [3] - ImageBase to build the highlight. Set to None if no
                    no highlight or in cache.
            xpos - xposition to blit objects with
            ypos - yposition to blit objects with
            width - width to render objects with
            height - height to render objects with
        """
        
        def __init__(self, render_keys, flt, xpos, ypos, width, height):
            """
            Constructor for a MASMOnikaRender object

            IN:
                render_keys - image keys and ImageBase if needed.
                    See props.
                flt - filter we are using (string)
                xpos - xposition to blit objects with
                ypos - yposition to blit objects with
                width - width to render objects with
                height - height to render objects with
            """
            super(store.MASFilterable, self).__init__()
            self.render_keys = render_keys
            self.xpos = xpos
            self.ypos = ypos
            self.width = width
            self.height = height
            self.flt = flt
        
        def _l_render_hl(self, render_list, render_key, st, at):
            """
            Retrieves highlight image from cache, or renders if needed

            IN:
                render_key - tuple of the following format
                    [0] - key of image to generate
                    [1] - cache ID of the cache to use
                    [2] - ImageBase to build the image
                    [3] - ImageBase to build the highlight
                st - renpy related
                at - renpy related

            OUT:
                render_list - list to add render to, if needed
            """
            
            if render_key[1] == store.mas_sprites.CID_FACE:
                return None
            
            if render_key[1] == store.mas_sprites.CID_DYNAMIC:
                
                img_base = render_key[3]
            
            else:
                
                hl_key = (render_key[1],) + render_key[0]
                
                
                img_base = store.mas_sprites._cs_im(
                    hl_key,
                    store.mas_sprites.CID_HL,
                    render_key[3]
                )
            
            if img_base is not None:
                render_list.append(renpy.render(
                    img_base,
                    self.width,
                    self.height,
                    st, at
                ))
        
        
        def _render_surf(self, render_key, st, at):
            """
            Retrieves surf image from cache, or renders if needed

            IN:
                render_key - tuple of the following format:
                    [0] - key of image to generate
                    [1] - cache ID of the cache to use
                    [2] - ImageBase to build the image
                    [3] - ImageBase to build the highlight
                st - renpy related
                at - renpy related

            RETURNS: rendered surf image to use
            """
            new_surf = renpy.render(
                store.mas_sprites._cgen_im(
                    self.flt,
                    render_key[0],
                    render_key[1],
                    render_key[2]
                ),
                self.width,
                self.height,
                st, at
            )
            
            
            
            
            return new_surf
        
        def render(self, width, height, st, at):
            """
            Render function
            """
            self.flt = store.mas_sprites.get_filter()
            
            renders = []
            for render_key in self.render_keys:
                renders.append(self._render_surf(render_key, st, at))
                self._l_render_hl(renders, render_key, st, at)
            
            
            rv = renpy.Render(self.width, self.height)
            for render in renders:
                rv.blit(render, (self.xpos, self.ypos))
            
            return rv
        
        
        def visit(self):
            """
            Returns a list of displayables we obtain
            NOTE: will also save to our cache
            """
            self.flt = store.mas_sprites.get_filter()
            disp_list = []
            for render_key in self.render_keys:
                store.mas_sprites._cgha_im(disp_list, self.flt, render_key)
            
            return disp_list


    def _add_arms_rk(
            rk_list,
            arms,
            pfx,
            flt,
            bcode,
            clothing_t,
            leanpose
    ):
        """
        Adds render key for multiple MASArm objects, if needed

        IN:
            arms - MASArm objects to add render key for
            pfx - prefix tuple to generate image string with
            flt - filter code to use
            bcode - base code to use
            clothing_t - type of clothing to use
            leanpose - leanpose to use

        OUT:
            rk_list - render key list to add render keys to
        """
        
        img_key = (flt, bcode, clothing_t, leanpose)
        cache_arms = _gc(CID_ARMS)
        day_key = None
        if img_key in cache_arms:
            if cache_arms[img_key] is not None:
                rk_list.append((img_key, CID_ARMS, None, None))
            
            return
        
        elif flt != FLT_DAY:
            
            day_key = _dayify(img_key)
            if cache_arms.get(day_key, True) is None:
                
                cache_arms[img_key] = None
                return
        
        
        if arms is None:
            
            cache_arms[img_key] = None
            cache_arms[day_key] = None
            return
        
        
        arm_data = []
        for arm in arms:
            tag_list = arm.get(bcode)
            if len(tag_list) > 0:
                arm_data.append((arm, tag_list))
        
        
        if len(arm_data) == 0:
            
            cache_arms[img_key] = None
            cache_arms[day_key] = None
            return
        
        
        if len(arm_data) < 2:
            arm, tag_list = arm_data[0]
            img_list = pfx + tag_list + [FILE_EXT]
            
            
            rk_list.append((
                img_key,
                CID_ARMS,
                store.Image("".join(img_list)),
                _bhli(img_list, arm.gethlc(bcode, flt))
            ))
            return
        
        
        arm_comp_args = [LOC_WH]
        hl_comp_args = [LOC_WH]
        
        for arm, tag_list in arm_data:
            img_list = pfx + tag_list
            arm_comp_args.append((0, 0))
            arm_comp_args.append("".join(img_list + [FILE_EXT]))
            
            
            hlc = arm.gethlc(bcode, flt)
            if hlc is not None:
                hl_comp_args.append((0, 0))
                hl_comp_args.append("".join(
                    img_list + [
                        HLITE_SUFFIX,
                        hlc,
                        FILE_EXT
                    ]
                ))
        
        
        img_comp = store.im.Composite(*arm_comp_args)
        if len(hl_comp_args) > 1:
            hl_comp = store.im.Composite(*hl_comp_args)
        else:
            hl_comp = None
        
        
        rk_list.append((img_key, CID_ARMS, img_comp, hl_comp))


    def _bhli(img_list, hlcode):
        """
        Builds a
        High-
        Light
        Image using the base image path

        IN:
            img_list - list of strings that form the base image string
                NOTE: we assume that the last item in this string is the
                FILE_EXT. This also assumes highlight codes are always inserted
                right before the file extension.
            hlcode - highlight code to use. Can be None.

        RETURNS: Image to use for highlight, or None if no highlight.
        """
        if hlcode is None:
            return None
        
        
        hl_list = list(img_list)
        hl_list[-1:-1] = [HLITE_SUFFIX, hlcode]
        return store.Image("".join(hl_list))


    def _bhlifp(img_path, hlcode):
        """
        Builds a
        High-
        Light
        Image using an image's
        File
        Path

        IN:
            img_path - full filepath to an image, including extension.
            hlcode - highlight code to use. Can be None

        RETURNS: Image to use for highlight, or None if no highlight
        """
        if hlcode is None:
            return None
        
        
        pre_img, ext, ignore = img_path.partition(FILE_EXT)
        return store.Image("".join((pre_img, HLITE_SUFFIX, hlcode, ext)))


    def _cgen_im(flt, key, cid, img_base):
        """
        Checks cache for an im,
        GENerates the im if not found

        IN:
            flt - filter to use
            key - key of the image
            cid - cache ID of the cache to use
            img_base - ImageBase to build the image

        RETURNS: Image Manipulator for this render
        """
        if cid == CID_DYNAMIC:
            
            return img_base
        
        img_cache = _gc(cid)
        if key in img_cache:
            return img_cache[key]
        
        
        new_im = _gen_im(flt, img_base)
        img_cache[key] = new_im
        return new_im


    def _cgha_im(render_list, flt, render_key):
        """
        Checks cache of an image
        Generates the im if not found, and sets
        Highlight if needed.
        Adds IMs to the given render list

        NOTE: should only be used by the visit function

        IN:
            flt - filter to use
            render_key - tuple of the following format:
                [0] - key of the image to generate
                [1] - cache ID of the cahce to use
                [2] - ImageBase to build the image
                [3] - ImageBase to build the highlight
            st - renpy related
            at - renpy related

        OUT:
            render_list - list to add IMs to
        """
        img_key, cid, img_base, hl_base = render_key
        if cid == CID_DYNAMIC:
            
            if img_base is not None:
                render_list.append(img_base)
            if hl_base is not None:
                render_list.append(hl_base)
            
            return
        
        img_cache = _gc(cid)
        hl_key = _hlify(img_key, cid)
        if img_key in img_cache:
            render_list.append(img_base)
            
            
            
            
            hl_base = _gc(CID_HL).get(hl_key, None)
            if hl_base is not None:
                render_list.append(hl_base)
            return
        
        
        new_im = _gen_im(flt, img_base)
        img_cache[img_key] = new_im
        render_list.append(new_im)
        
        
        _gc(CID_HL)[hl_key] = hl_base
        if hl_base is not None:
            render_list.append(hl_base)


    def _cs_im(key, cid, img_base):
        """
        Checks cache for an im
        Stores the img_base if not found

        IN:
            key - key of the image
            cid - cache ID of the cache to use
            img_base - ImageBase to build the image

        RETURNS: ImageBase
        """
        img_cache = _gc(cid)
        if key in img_cache:
            return img_cache[key]
        
        
        img_cache[key] = img_base
        return img_base


    def _dayify(img_key):
        """
        Dayifies the given image key.
        DAying simply replaces the filter portion of the key with "day"

        IN:
            img_key - image key to dayify

        RETURNS: dayified key
        """
        img_key_list = list(img_key)
        img_key_list[0] = FLT_DAY
        return tuple(img_key_list)


    def _gc(cid):
        """
        Gets the
        Cache

        IN:
            cid - cache ID of the cache to get

        RETURNS: cache, or empty dict if cache not found
        """
        return CACHE_TABLE.get(cid, {})


    def _gen_im(flt, img_base):
        """
        GENerates an image maniuplator
        NOTE: always assumes we have an available filter.

        IN:
            flt - filter to use
            img_base - image path or manipulator to use

        RETURNS: generated render key
        """
        
        
        return store.im.MatrixColor(img_base, FILTERS[flt])


    def _hlify(key, cid):
        """
        Highlightifies the given key.
        Highlightifying is just prefixing the key with the cid

        IN:
            key - key to highlightify
            cid - cid to use when highlighting

        RETURNS: highlightified key
        """
        return (cid,) + key



    def _rk_accessory(
            rk_list,
            acs,
            flt,
            arm_split,
            leanpose=None
    ):
        """
        Adds accessory render key if needed

        IN:
            acs - MASAccessory object
            flt - filter to apply
            arm_split - see MASAccessory.arm_split for codes. None for no
                codes at all.
            leanpose - current pose
                (Default: None)

        OUT:
            rk_list - list to add render keys to
        """
        
        
        
        poseid = acs.pose_map.get(leanpose, None)
        
        
        if acs.is_dynamic():
            
            
            
            if not poseid:
                return
            
            
            rk_list.append((None, CID_DYNAMIC, acs.disp, acs.hl_disp))
            return
        
        
        
        
        if arm_split is None:
            arm_code = ""
        
        elif arm_split in acs.get_arm_split_code(leanpose):
            arm_code = ART_DLM + arm_split
        
        else:
            
            arm_code = None
        
        
        img_key = (flt, acs.name, poseid, arm_code)
        cache_acs = _gc(CID_ACS)
        day_key = None
        if img_key in cache_acs:
            if cache_acs[img_key] is not None:
                rk_list.append((img_key, CID_ACS, None, None))
            
            return
        
        elif flt != FLT_DAY:
            
            day_key = _dayify(img_key)
            if cache_acs.get(day_key, True) is None:
                
                cache_acs[img_key] = None
                return
        
        
        if poseid is None or arm_code is None:
            
            
            cache_acs[img_key] = None
            cache_acs[day_key] = None
            return
        
        
        if acs.use_folders:
            pfx = ""
            dlm = "/"
        else:
            pfx = PREFIX_ACS
            dlm = ART_DLM
        
        
        img_list = [
            A_T_MAIN,
            pfx,
            acs.img_sit,
            dlm,
            poseid,
            arm_code,
            FILE_EXT,
        ]
        
        
        rk_list.append((
            img_key,
            CID_ACS,
            store.Image("".join(img_list)),
            _bhli(img_list, acs.opt_gethlc(poseid, flt, arm_split))
        ))


    def _rk_accessory_list(
            rk_list,
            acs_list,
            flt,
            leanpose=None,
            arm_split=None
    ):
        """
        Adds accessory render keys for a list of accessories

        IN:
            acs_list - list of MASAccessory objects, in order of rendering
            flt - filter to use
            arm_split - set to MASAccessory.arm_split code if we are rendering
                arm_split-affected ACS. If None, we use standard algs.
                (Default: None)
            leanpose - arms pose for we are currently rendering
                (Default: None)

        OUT:
            rk_list - list to add render keys to
        """
        if len(acs_list) == 0:
            return
        
        for acs in acs_list:
            _rk_accessory(
                rk_list,
                acs,
                flt,
                arm_split,
                leanpose
            )


    def _rk_arms_base_nh(rk_list, barms, leanpose, flt, bcode):
        """
        Adds arms base render keys
        (equiv to _ms_arms_nh_up_base)

        IN:
            barms - tuple of MASArm objects to use
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_arms_rk(
            rk_list,
            barms,
            [
                B_MAIN,
                PREFIX_ARMS,
            ],
            flt,
            bcode,
            "base",
            leanpose
        )


    def _rk_arms_base_lean_nh(rk_list, barms, lean, leanpose, flt, bcode):
        """
        Adds arms base lean render key
        (eqiv to _ms_arms_nh_leaning_base)

        IN:
            barms - tuple of MASArm objects to use
            lean - type of lean
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_arms_rk(
            rk_list,
            barms,
            [
                B_MAIN,
                PREFIX_ARMS_LEAN,
                lean,
                ART_DLM,
            ],
            flt,
            bcode,
            "base",
            leanpose
        )


    def _rk_arms_nh(rk_list, parms, clothing, leanpose, flt, bcode):
        """
        Adds arms render key
        (equiv to _ms_arms_nh_up_arms)

        IN:
            parms - tuple of MASArm objects to use
            clothing - MASClothes object
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_arms_rk(
            rk_list,
            parms,
            [
                C_MAIN,
                clothing.img_sit,
                "/",
                PREFIX_ARMS,
            ],
            flt,
            bcode,
            clothing.img_sit,
            leanpose
        )


    def _rk_arms_lean_nh(rk_list, parms, clothing, lean, leanpose, flt, bcode):
        """
        Adds arms lean render key
        (equiv to _ms_arms_nh_leaning_arms)

        IN:
            parms - tuple of MASArm objects to use
            clothing - MASClothes object
            lean - type of lean
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_arms_rk(
            rk_list,
            parms,
            [
                C_MAIN,
                clothing.img_sit,
                "/",
                PREFIX_ARMS_LEAN,
                lean,
                ART_DLM,
            ],
            flt,
            bcode,
            clothing.img_sit,
            leanpose
        )


    def _rk_arms_nh_wbase(
            rk_list,
            barms,
            parms,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            bcode
    ):
        """
        Adds arms render keys, no hair, with baes

        IN:
            barms - tuple of MASArm objects for base
            parms - tuple of MASArm objects for pose
            clothing - MASClothes object
            acs_ase_list - acs between arms-base-0 and arms-0
            leanpose - leanpose to pass to accessorylist
            lean - lean to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        if lean:
            
            _rk_arms_base_lean_nh(rk_list, barms, lean, leanpose, flt, bcode)
            
            
            _rk_accessory_list(rk_list, acs_ase_list, flt, leanpose, bcode)
            
            if parms is not None:
                
                _rk_arms_lean_nh(
                    rk_list,
                    parms,
                    clothing,
                    lean,
                    leanpose,
                    flt,
                    bcode
                )
        
        else:
            
            _rk_arms_base_nh(rk_list, barms, leanpose, flt, bcode)
            
            
            _rk_accessory_list(rk_list, acs_ase_list, flt, leanpose, bcode)
            
            if parms is not None:
                
                _rk_arms_nh(rk_list, parms, clothing, leanpose, flt, bcode)


    def _rk_base_body_nh(rk_list, flt, bcode):
        """
        Adds base body render keys, no hair
        (equiv of _ms_torso_nh_base)

        IN:
            flt - filter ot use
            bcode- base code to use

        OUT:
            rk_list - list to add render keys to
        """
        img_str = "".join((
            B_MAIN,
            BASE_BODY_STR,
            bcode,
            FILE_EXT,
        ))
        
        
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return
        
        rk_list.append((img_key, CID_BODY, store.Image(img_str), None))


    def _rk_base_body_lean_nh(rk_list, lean, flt, bcode):
        """
        Adds base body lean render keys, no hair
        (equivalent of _ms_torsoleaning_nh_base)

        IN:
            lean - type of lean
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        img_str = "".join((
            B_MAIN,
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            bcode,
            FILE_EXT,
        ))
        
        
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return
        
        rk_list.append((img_key, CID_BODY, store.Image(img_str), None))


    def _rk_body_nh(rk_list, clothing, flt, bcode):
        """
        Adds body render keys, no hair
        (equiv of _ms_torso_nh)

        IN:
            clothing - MASClothes object
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        img_list = (
            C_MAIN,
            clothing.img_sit,
            "/",
            NEW_BODY_STR,
            ART_DLM,
            bcode,
            FILE_EXT,
        )
        img_str = "".join(img_list)
        
        
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return
        
        
        rk_list.append((
            img_key,
            CID_BODY,
            store.Image(img_str),
            _bhli(img_list, clothing.gethlc(bcode, None, flt)),
        ))


    def _rk_body_lean_nh(rk_list, clothing, lean, flt, bcode):
        """
        Adds body leaning render keys, no hair
        (equiv of _ms_torsoleaning_nh)

        IN:
            clothing - MASClothes object
            lean - type of lean
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        
        img_list = (
            C_MAIN,
            clothing.img_sit,
            "/",
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            bcode,
            FILE_EXT,
        )
        img_str = "".join(img_list)
        
        
        img_key = (flt, img_str)
        cache_body = _gc(CID_BODY)
        if img_key in cache_body:
            rk_list.append((img_key, CID_BODY, None, None))
            return
        
        
        rk_list.append((
            img_key,
            CID_BODY,
            store.Image(img_str),
            _bhli(img_list, clothing.gethlc(bcode, lean, flt))
        ))


    def _rk_body_nh_wbase(
            rk_list,
            clothing,
            acs_bse_list,
            bcode,
            flt,
            leanpose,
            lean=None
    ):
        """
        Adds body render keys, including base and bse acs, no hair

        IN:
            clothing - MASClothes object
            acs_bse_list - acs between base-0 and body-0
            bcode - base code to use
            flt - filter to use
            leanpose - leanpose to pass to accessorylist
            lean - type of lean

        OUT:
            rk_list - list to add render keys to
        """
        if lean:
            
            _rk_base_body_lean_nh(rk_list, lean, flt, bcode)
            
            
            _rk_accessory_list(rk_list, acs_bse_list, flt, leanpose, bcode)
            
            
            _rk_body_lean_nh(rk_list, clothing, lean, flt, bcode)
        
        else:
            
            _rk_base_body_nh(rk_list, flt, bcode)
            
            
            _rk_accessory_list(rk_list, acs_bse_list, flt, leanpose, bcode)
            
            
            _rk_body_nh(rk_list, clothing, flt, bcode)


    def _rk_chair(rk_list, mtc, flt):
        """
        Adds chair render key

        IN:
            mtc - MASTableChair object
            flt - filter to use

        OUT:
            rk_list - list to add render keys to
        """
        
        img_key = (flt, 1, mtc.chair)
        cache_tc = _gc(CID_TC)
        if img_key in cache_tc:
            rk_list.append((img_key, CID_TC, None, None))
            return
        
        
        img_list = (
            T_MAIN,
            PREFIX_CHAIR,
            mtc.chair,
            FILE_EXT,
        )
        img_str = "".join(img_list)
        
        rk_list.append((
            img_key,
            CID_TC,
            store.Image(img_str),
            _bhli(
                img_list,
                store.MASHighlightMap.o_fltget(mtc.hl_map, "c", flt)
            )
        ))


    def _rk_face(
            rk_list,
            eyes,
            eyebrows,
            nose,
            mouth,
            flt,
            fpfx,
            lean,
            sweat,
            tears,
            emote
        ):
        """
        Adds face render keys

        IN:
            eyes - type of eyes
            eyebrows - type of eyebrows
            nose - type of nose
            mouth - type of mouth
            flt - filter to use
            fpfx - face prefix to use
            lean - type of lean to use
            sweat - type of sweat drop
            tears - type of tears
            emote - type of emote

        OUT:
            rk_list - list to add render keys to
        """
        img_key = (
            flt,
            1,
            lean,
            eyes,
            eyebrows,
            nose,
            mouth,
            sweat,
            tears,
            emote
        )
        day_key = None
        cache_face = _gc(CID_FACE)
        if img_key in cache_face:
            if cache_face[img_key] is not None:
                rk_list.append((img_key, CID_FACE, None, None))
            return
        
        elif flt != FLT_DAY:
            
            day_key = _dayify(img_key)
            if cache_face.get(day_key, True) is None:
                
                cache_face[img_key] = None
                return
        
        
        
        
        img_str_list = [
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_EYES,
                eyes,
                FILE_EXT,
            )),
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_EYEB,
                eyebrows,
                FILE_EXT,
            )),
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_NOSE,
                nose,
                FILE_EXT,
            )),
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_MOUTH,
                mouth,
                FILE_EXT,
            )),
        ]
        
        
        if sweat:
            img_str_list.extend((
                (0,0),
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_SWEAT,
                    sweat,
                    FILE_EXT,
                ))
            ))
        
        if tears:
            img_str_list.extend((
                (0, 0),
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_TEARS,
                    tears,
                    FILE_EXT,
                ))
            ))
        
        if emote:
            img_str_list.extend((
                (0, 0),
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_EMOTE,
                    emote,
                    FILE_EXT,
                ))
            ))
        
        
        rk_list.append((
            img_key,
            CID_FACE,
            store.im.Composite((1280, 850), *img_str_list),
            None
        ))


    def _rk_face_pre(rk_list, flt, fpfx, lean, blush):
        """
        Adds face render keys that go before hair

        IN:
            flt - filter to use
            fpfx - face prefix to use
            lean - type of lean to use
            blush - type of blush

        OUT:
            rk_list - list to add render keys to
        """
        img_key = (flt, 0, lean, blush)
        day_key = None
        cache_face = _gc(CID_FACE)
        if img_key in cache_face:
            if cache_face[img_key] is not None:
                rk_list.append((img_key, CID_FACE, None, None))
            
            return
        
        elif flt != FLT_DAY:
            
            day_key = _dayify(img_key)
            if cache_face.get(day_key, True) is None:
                
                cache_face[img_key] = None
                return
        
        
        
        
        if blush:
            rk_list.append((
                img_key,
                CID_FACE,
                store.Image("".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_BLUSH,
                    blush,
                    FILE_EXT
                ))),
                None,
            ))
            return
        
        
        cache_face[img_key] = None
        cache_face[day_key] = None


    def _rk_hair(rk_list, hair, flt, hair_key, lean, leanpose):
        """
        Adds hair render key

        IN:
            hair - MASHair object
            flt - filter to use
            hair_key - hair key to use (front/back/mid)
            lean - tyoe of lean
            leanpose - leanpose

        OUT:
            rk_list - list to add render keys to
        """
        
        
        img_key = (flt, hair.img_sit, lean, hair_key)
        cache_hair = _gc(CID_HAIR)
        if img_key in cache_hair:
            if cache_hair[img_key] is not None:
                rk_list.append((img_key, CID_HAIR, None, None))
            return
        
        
        if hair_key in (MHAIR, store.MASHair.LAYER_MID):
            if hair.mpm_mid is None or not hair.mpm_mid.get(leanpose, False):
                
                cache_hair[img_key] = None
                return
        
        
        if lean:
            
            if hair.use_folders:
                img_list = (
                    H_MAIN,
                    hair.img_sit,
                    "/",
                    lean,
                    ART_DLM,
                    hair_key,
                    FILE_EXT,
                )
            
            else:
                img_list = (
                    H_MAIN,
                    PREFIX_HAIR_LEAN,
                    lean,
                    ART_DLM,
                    hair.img_sit,
                    ART_DLM,
                    hair_key,
                    FILE_EXT,
                )
        
        else:
            
            if hair.use_folders:
                pfx = ""
                dlm = "/"
            else:
                pfx = PREFIX_HAIR
                dlm = ART_DLM
            
            img_list = (
                H_MAIN,
                pfx,
                hair.img_sit,
                dlm,
                hair_key,
                FILE_EXT,
            )
        
        
        img_str = "".join(img_list)
        
        
        rk_list.append((
            img_key,
            CID_HAIR,
            store.Image(img_str),
            _bhli(img_list, hair.gethlc(hair_key, lean, flt)),
        ))


    def _rk_head(rk_list, flt, lean):
        """
        Adds head render keys.

        IN:
            bcode - base code to use
            flt - filter to use
            lean - type of lean

        OUT:
            rk_list - list to add render keys to
        """
        if lean:
            img_str = "".join((
                B_MAIN,
                PREFIX_BODY_LEAN,
                lean,
                ART_DLM,
                HEAD,
                FILE_EXT,
            ))
        
        else:
            img_str = "".join((
                B_MAIN,
                BASE_BODY_STR,
                HEAD,
                FILE_EXT
            ))
        
        
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return
        
        rk_list.append((img_key, CID_BODY, store.Image(img_str), None))


    def _rk_table(rk_list, tablechair, show_shadow, flt):
        """
        Adds table render key

        IN:
            table - MASTableChair object
            show_shadow - True if shadow should be included, false if not
            flt filter to use

        OUT:
            rk_list - list to add render keys to
        """
        img_key = (flt, 0, tablechair.table, int(show_shadow))
        if img_key in _gc(CID_TC):
            rk_list.append((img_key, CID_TC, None, None))
            return
        
        
        table_list = (
            T_MAIN,
            PREFIX_TABLE,
            tablechair.table,
            FILE_EXT,
        )
        
        
        if show_shadow:
            
            
            shdw_list = (
                T_MAIN,
                PREFIX_TABLE,
                tablechair.table,
                SHADOW_SUFFIX,
                FILE_EXT,
            )
            shdw_str = "".join(shdw_list)
            
            
            hl_img = _bhli(
                shdw_list,
                store.MASHighlightMap.o_fltget(tablechair.hl_map, "ts", flt)
            )
            
            if hl_img is None:
                
                hl_img = store.Image(shdw_str)
            
            else:
                
                hl_img = store.im.Composite(
                    (1280, 850),
                    (0, 0), shdw_str,
                    (0, 0), hl_img
                )
        
        else:
            
            hl_img = _bhli(
                table_list,
                store.MASHighlightMap.o_fltget(tablechair.hl_map, "t", flt)
            )
        
        
        rk_list.append((
            img_key,
            CID_TC,
            store.Image("".join(table_list)),
            hl_img
        ))




    def _rk_sitting(
            clothing,
            hair,
            base_arms,
            pose_arms,
            eyebrows,
            eyes,
            nose,
            mouth,
            flt,
            acs_pre_list,
            acs_bbh_list,
            acs_bse_list,
            acs_bba_list,
            acs_ase_list,
            acs_bmh_list,
            acs_mhh_list,
            acs_bat_list,
            acs_mat_list,
            acs_mab_list,
            acs_bfh_list,
            acs_afh_list,
            acs_mid_list,
            acs_pst_list,
            leanpose,
            lean,
            arms,
            eyebags,
            sweat,
            blush,
            tears,
            emote,
            tablechair,
            show_shadow
    ):
        """
        Creates a list of render keys in order of desired render.

        IN:
            clothing - MASClothes object
            hair - MASHair object
            base_arms - tuple of MASArm objects to use for the base
            pose_arms - tuple of MASArm objects to use for the clothes arms
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            flt - filter to use
            acs_pre_list - sorted list of MASAccessories to draw prior to body
            acs_bbh_list - sroted list of MASAccessories to draw between back
                hair and body
            acs_bse_list - sorted list of MASAccessories to draw between base
                body and outfit
            acs_bba_list - sorted list of MASAccessories to draw between
                body and back arms
            acs_ase_list - sorted list of MASAccessories to draw between base
                arms and outfit
            acs_bmh_list - sorted list of MASAccessories to draw betrween back
                arms and mid hair
            acs_mmh_list - sorted list of MASAccessories to draw between mid
                hair and head
            acs_bat_list - sorted list of MASAccessories to draw before table
            acs_mat_list - sorted list of MASAccessories to draw between
                middle arms and table
            acs_mab_list - sorted list of MASAccessories to draw between
                middle arms and boobs
            acs_bfh_list - sorted list of MASAccessories to draw between boobs
                and front hair
            acs_afh_list - sorted list of MASAccessories to draw between front
                hair and face
            acs_mid_list - sorted list of MASAccessories to draw between body
                and arms
            acs_pst_list - sorted list of MASAccessories to draw after arms
            leanpose - lean and arms together
            lean - type of lean
            arms - type of arms
            eyebags - type of eyebags
            sweat - type of sweatdrop
            blush - type of blush
            tears - type of tears
            emote - type of emote
            tablechair - MASTableChair object
            show_shadow - True will show shadow, false will not

        RETURNS: list of render keys
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        fpfx = face_lean_mode(lean)
        rk_list = []
        back_hk, mid_hk, front_hk = hair._get_hair_keys()
        
        
        _rk_accessory_list(rk_list, acs_pre_list, flt, leanpose)
        
        
        _rk_hair(rk_list, hair, flt, back_hk, lean, leanpose)
        
        
        _rk_accessory_list(rk_list, acs_bbh_list, flt, leanpose)
        
        
        _rk_chair(rk_list, tablechair, flt)
        
        
        
        
        _rk_body_nh_wbase(
            rk_list,
            clothing,
            acs_bse_list,
            "0",
            flt,
            leanpose,
            lean=lean
        )
        
        
        _rk_accessory_list(rk_list, acs_bba_list, flt, leanpose)
        
        
        
        
        _rk_arms_nh_wbase(
            rk_list,
            base_arms,
            pose_arms,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "0"
        )
        
        
        _rk_accessory_list(rk_list, acs_bmh_list, flt, leanpose)
        
        
        _rk_hair(rk_list, hair, flt, mid_hk, lean, leanpose)
        
        
        _rk_accessory_list(rk_list, acs_mhh_list, flt, leanpose)
        
        
        _rk_head(rk_list, flt, lean)
        
        
        _rk_accessory_list(rk_list, acs_bat_list, flt, leanpose)
        
        
        _rk_table(rk_list, tablechair, show_shadow, flt)
        
        
        _rk_accessory_list(rk_list, acs_mat_list, flt, leanpose)
        
        
        
        
        _rk_arms_nh_wbase(
            rk_list,
            base_arms,
            pose_arms,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "5"
        )
        
        
        _rk_accessory_list(rk_list, acs_mab_list, flt, leanpose)
        
        
        
        
        _rk_body_nh_wbase(
            rk_list,
            clothing,
            acs_bse_list,
            "1",
            flt,
            leanpose,
            lean=lean
        )
        
        
        _rk_accessory_list(rk_list, acs_bfh_list, flt, leanpose)
        
        
        _rk_face_pre(rk_list, flt, fpfx, lean, blush)
        
        
        _rk_hair(rk_list, hair, flt, front_hk, lean, leanpose)
        
        
        _rk_accessory_list(rk_list, acs_afh_list, flt, leanpose)
        
        
        _rk_face(
            rk_list,
            eyes,
            eyebrows,
            nose,
            mouth,
            flt,
            fpfx,
            lean,
            sweat,
            tears,
            emote
        )
        
        
        _rk_accessory_list(rk_list, acs_mid_list, flt, leanpose)
        
        
        
        
        _rk_arms_nh_wbase(
            rk_list,
            base_arms,
            pose_arms,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "10"
        )
        
        
        _rk_accessory_list(rk_list, acs_pst_list, flt, leanpose)
        
        return rk_list


init -48 python:

    class MASFilterMap(object):
        """SEALED
        The FilterMap connects filters to values

        DO NOT EXTEND THIS CLASS. if you need similar functionality, just
        make a wrapper class. There are functions in this class that will
        cause crashes if used in unexpected contexts.

        NOTE: you can make filtermaps with non-string values, just dont
            use the hash/eq/ne operators.

        PROPERTIES:
            map - dict containg filter to string map
                key: filter constant
                value: string or, None if no highlight
        """
        import store.mas_sprites_json as msj
        
        def __init__(self,
                default=None,
                cache=True,
                verify=True,
                **filter_pairs
        ):
            """
            Constructor

            IN:
                default - default code to apply to all filters
                    (Default: None)
                cache - True will cache the MFM, False will not
                    (Default: True)
                verify - True will verify the filters, False will not.
                    NOTE: if passing False, use the verify function to
                    verify flts.
                    (Default: True)
                **filter_pairs - filter=val args to use. invalid filters are
                    ignored.
                    See FILTERS dict. Example:
                        day=None
                        night="0"
            """
            self.map = MASFilterMap.clean_flt_pairs(default, filter_pairs)
            
            if verify:
                self.verify()
            
            if cache:
                store.mas_sprites.MFM_CACHE[hash(self)] = self
        
        def __eq__(self, other):
            """
            Equals implementation.
            MASFilterMaps are equal based on their internal tuple/hash var
            """
            if isinstance(self, other.__class__):
                return hash(self) == hash(other)
            return False
        
        def __hash__(self):
            """
            Hashable implementation.
            MASFilterMaps are uniqued based on their internal map
            """
            return MASFilterMap.flt_hash(self.map)
        
        def __ne__(self, other):
            """
            Not equals implmentation.
            MASFilterMaps are not equal based on their internal tuple/hash var
            """
            return not self.__eq__(other)
        
        @staticmethod
        def _fromJSON_value(json_obj, msg_log, ind_lvl, prop_name, output):
            """
            Parses a single value from the json obj

            IN:
                json_obj - JSON object to parse
                ind_lvl - indentation level
                prop_name - name of the prop to parse for

            OUT:
                msg_log - list to add messagse to
                output - dict to add data to:
                    key: prop_name
                    value: prop value

            RETURNS: True if we should stop because of failure, false if not
            """
            if prop_name not in json_obj:
                return False
            
            
            prop_val = json_obj.pop(prop_name)
            if prop_val is None:
                
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl,
                    store.mas_sprites_json.MFM_NONE_FLT.format(prop_name)
                ))
                return False
            
            
            if store.mas_sprites_json._verify_str(prop_val):
                
                output[prop_name] = prop_val
                return False
            
            
            msg_log.append((
                store.mas_sprites_json.MSG_ERR_T,
                ind_lvl,
                store.mas_sprites_json.MFM_BAD_TYPE.format(
                    prop_name,
                    type(prop_val)
                )
            ))
            return True
        
        @staticmethod
        def cachecreate(default=None, **filter_pairs):
            """
            Creates a MASFilterMap object ONLY if it is not in the filtermap
            cache.

            IN:
                default - See constructor for MASFilterMap
                **filter_pairs - See constructor for MASFilterMap

            RETURNS: MASFilterMap object to use
            """
            hash_value = MASFilterMap.flt_hash(MASFilterMap.clean_flt_pairs(
                default,
                filter_pairs
            ))
            
            if hash_value in store.mas_sprites.MFM_CACHE:
                return store.mas_sprites.MFM_CACHE[hash_value]
            
            
            
            return MASFilterMap(default=default, **filter_pairs)
        
        @staticmethod
        def clean_flt_pairs(default, filter_pairs):
            """
            cleans given filter pairs, setting defaults and only using valid
            filter keys.

            IN:
                default - default code to apply to all filters
                filter_pairs - filter pair dict:
                    key: filter as string
                    value: code to use as string

            RETURNS: dict with cleaned filter pairs
            """
            output = {}
            
            
            for flt in store.mas_sprites.FILTERS:
                output[flt] = filter_pairs.get(flt, default)
            
            return output
        
        @staticmethod
        def flt_hash(flt_pairs):
            """
            Generates a hash based on the given filter pairs

            IN:
                flt_pairs - dict of the following format:
                    key: filter as string
                    value: code to use as string
                    NOTE: default is assumed to already been set

            RETURNS: hash that would be generated by a MASFilterMAp created
                with the given filter pairs
            """
            
            
            return hash(tuple([
                flt_pairs.get(flt, None)
                for flt in store.mas_sprites.FILTERS
            ]))
        
        @classmethod
        def fromJSON(cls, json_obj, msg_log, ind_lvl, prop_name):
            """
            Builds a MASFilterMap given a JSON format of it

            IN:
                json_obj - JSOn object to parse
                ind_lvl - indent lvl
                    NOTE: this handles loading/success log, so do not
                        increase indent level
                prop_name - name of the prop this MASFilterMap object is
                    being created from

            OUT:
                msg_log - list to add messages to

            RETURNS: MASFilterMap object build using the JSON, or None if not
                creatable, or False if failur
            """
            
            msg_log.append((
                store.mas_sprites_json.MSG_INFO_T,
                ind_lvl,
                store.mas_sprites_json.MFM_LOADING.format(prop_name)
            ))
            
            
            if json_obj is None:
                
                msg_log.append((
                    store.mas_sprites_json.MSG_INFO_T,
                    ind_lvl + 1,
                    store.mas_sprites_json.MFM_NO_DATA
                ))
                return None
            
            
            if not store.mas_sprites_json._verify_dict(json_obj):
                msg_log.append((
                    store.mas_sprites_json.MSG_ERR_T,
                    ind_lvl + 1,
                    store.mas_sprites_json.BAD_TYPE.format(
                        prop_name,
                        dict,
                        type(json_obj)
                    )
                ))
                return False
            
            fltpairs = {}
            
            
            isbad = cls._fromJSON_value(
                json_obj,
                msg_log,
                ind_lvl + 1,
                "default",
                fltpairs
            )
            
            
            for flt in store.mas_sprites.FILTERS:
                if cls._fromJSON_value(
                        json_obj,
                        msg_log,
                        ind_lvl + 1,
                        flt,
                        fltpairs
                ):
                    isbad = True
            
            
            for extra_prop in json_obj:
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl + 1,
                    store.mas_sprites_json.EXTRA_PROP.format(extra_prop)
                ))
            
            
            if isbad:
                return False
            
            if len(fltpairs) < 1:
                
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl + 1,
                    store.mas_sprites_json.MFM_NO_DATA,
                ))
                return None
            
            
            
            
            def_flt = None
            if "default" in fltpairs:
                def_flt = fltpairs.pop("default")
            
            
            msg_log.append((
                store.mas_sprites_json.MSG_INFO_T,
                ind_lvl,
                store.mas_sprites_json.MFM_SUCCESS.format(prop_name)
            ))
            
            
            return cls.cachecreate(def_flt, **fltpairs)
        
        def get(self, flt, defval=None):
            """
            Gets value from map based on filter

            IN:
                flt - filter to lookup
                defval - default value to reutrn if filter not found
                    (Default: None)

            RETURNS: value for given filter
            """
            return self.map.get(flt, defval)
        
        def unique_values(self):
            """
            Gets all unique non-None values in this filter map

            RETURNS: list of all non-NOne and unique values in this filter
                map
            """
            vals = []
            for key in self.map:
                value = self.map[key]
                if value is not None and value not in vals:
                    vals.append(value)
            
            return vals
        
        def verify(self):
            """
            Verifies all filters in this filter map. Raises exceptions if
            bad filtesr are found.
            """
            for flt in self.map:
                if not store.mas_sprites.is_filter(flt):
                    raise MASInvalidFilterException(flt)


    class MASFilterMapSimple(object):
        """
        MASFilterMap for simple implementations, aka filter - value pairs
        without type checks.

        Classes that need MASFilterMap should just extend this one as a base.

        This will NOT cache filter maps.

        PROPERTIES:
            None
        """
        
        def __init__(self, **filter_pairs):
            """
            Constructor

            Passes values directly to the internal MFM

            IN:
                **filter_pairs - filter=val args to use. invalid filters
                    are ignored.
            """
            self._m1_sprite0x2dchart0x2dmatrix__mfm = MASFilterMap(
                default=None,
                cache=False,
                **filter_pairs
            )
        
        def flts(self):
            """
            Gets all filter names in this filter map

            RETURNS: list of all filter names in this map
            """
            return self._m1_sprite0x2dchart0x2dmatrix__mfm.map.keys()
        
        def get(self, flt, defval=None):
            """
            See MASFilterMap.get
            """
            return self._m1_sprite0x2dchart0x2dmatrix__mfm.get(flt, defval)
        
        def _mfm(self):
            """
            Returns the intenral MASFilterMap. Only use if you know what you
            are doing.

            RETURNS: MASFilterMap
            """
            return self._m1_sprite0x2dchart0x2dmatrix__mfm


    class MASFilterMapFallback(MASFilterMapSimple):
        """
        MASFilterMap that respects fallback mechanics.

        Classes that need fallback behavior should just extend this one as a
        base.

        This will NOT cache filter maps.

        PROPERTIES:
            None
        """
        
        def __init__(self, **filter_pairs):
            """
            Constructor

            IN:
                **filter_pairs - filter=val args to use. invalid filters are
                    ignored.
            """
            super(MASFilterMapFallback, self).__init__(**filter_pairs)
        
        def get(self, flt, defval=None):
            """
            Gets value from map based on filter. This follows fallback
            mechanics until a non-None value is found.

            IN:
                flt - filter to lookup
                defval - default value to return if no non-None value is
                    found after exhausting all fallbacks.
                    (Default: None)

            REUTRNS: value for a given filter
            """
            value = self._raw_get(flt)
            cur_flt = flt
            while value is None:
                nxt_flt = store.mas_sprites._rslv_flt(cur_flt)
                
                if nxt_flt == cur_flt:
                    
                    return defval
                
                value = self._raw_get(nxt_flt)
                cur_flt = nxt_flt
            
            return value
        
        def _raw_get(self, flt):
            """
            Gets value from map based on filter

            IN:
                flt - filter to lookup

            RETURNS: value for the given filter
            """
            return super(MASFilterMapFallback, self).get(flt)


init python:


    def mas_drawmonika_rk(
            st,
            at,
            character,

            
            eyebrows,
            eyes,
            nose,
            mouth,

            
            lean=None,
            arms="steepling",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None,

            
            head="a",
            left="1l",
            right="1r",
            stock=True,
            single=None
        ):
        """
        Draws monika dynamically, using render keys
        See mas_drawmonika for more info.

        IN:
            st - renpy related
            at - renpy related
            character - MASMonika character object
            eyebrows - type of eyebrows (sitting)
            eyes - type of eyes (sitting)
            nose - type of nose (sitting)
            mouth - type of mouth (sitting)
            head - type of head (standing)
            left - type of left side (standing)
            right - type of right side (standing)
            lean - type of lean (sitting)
                (Default: None)
            arms - type of arms (sitting)
                (Default: "steepling")
            eyebags - type of eyebags (sitting)
                (Default: None)
            sweat - type of sweatdrop (sitting)
                (Default: None)
            blush - type of blush (sitting)
                (Default: None)
            tears - type of tears (sitting)
                (Default: None)
            emote - type of emote (sitting)
                (Default: None)
            stock - True means we are using stock standing, False means not
                (standing)
                (Default: True)
            single - type of single standing image (standing)
                (Default: None)
        """
        if not is_sitting:
            
            return mas_drawmonika(
                st, at, character,
                eyebrows, eyes, nose, mouth,
                lean, arms, eyebags, sweat, blush, tears, emote,
                head, left, right, stock, single
            )
        
        
        acs_pre_list = character.acs.get(MASMonika.PRE_ACS, [])
        acs_bbh_list = character.acs.get(MASMonika.BBH_ACS, [])
        acs_bse_list = character.acs.get(MASMonika.BSE_ACS, [])
        acs_bba_list = character.acs.get(MASMonika.BBA_ACS, [])
        acs_ase_list = character.acs.get(MASMonika.ASE_ACS, [])
        acs_bmh_list = character.acs.get(MASMonika.BMH_ACS, [])
        acs_mmh_list = character.acs.get(MASMonika.MMH_ACS, [])
        acs_bat_list = character.acs.get(MASMonika.BAT_ACS, [])
        acs_mat_list = character.acs.get(MASMonika.MAT_ACS, [])
        acs_mab_list = character.acs.get(MASMonika.MAB_ACS, [])
        acs_bfh_list = character.acs.get(MASMonika.BFH_ACS, [])
        acs_afh_list = character.acs.get(MASMonika.AFH_ACS, [])
        acs_mid_list = character.acs.get(MASMonika.MID_ACS, [])
        acs_pst_list = character.acs.get(MASMonika.PST_ACS, [])
        
        
        
        
        
        
        
        
        
        
        pose_data = character._determine_poses(lean, arms)
        
        
        flt = store.mas_sprites.get_filter()
        
        
        sprite = store.mas_sprites.MASMonikaRender(
            store.mas_sprites._rk_sitting(
                character.clothes,
                pose_data[3],
                pose_data[4],
                pose_data[5],
                eyebrows,
                eyes,
                nose,
                mouth,
                flt,
                acs_pre_list,
                acs_bbh_list,
                acs_bse_list,
                acs_bba_list,
                acs_ase_list,
                acs_bmh_list,
                acs_mmh_list,
                acs_bat_list,
                acs_mat_list,
                acs_mab_list,
                acs_bfh_list,
                acs_afh_list,
                acs_mid_list,
                acs_pst_list,
                pose_data[1],
                pose_data[0],
                pose_data[2],
                eyebags,
                sweat,
                blush,
                tears,
                emote,
                character.tablechair,
                character.tablechair.has_shadow
            ),
            flt,
            store.mas_sprites.adjust_x,
            store.mas_sprites.adjust_y,
            store.mas_sprites.LOC_W,
            store.mas_sprites.LOC_H
        )
        
        
        return Transform(sprite, zoom=store.mas_sprites.value_zoom), None


    def mas_drawemptydesk_rk(st, at, character):
        """
        draws the table dynamically. includes ACS that should stay on desk.
        NOTE: uses image manips.
        NOTE: this is assumed to be used with empty desk ONLY
        NOTE: sitting only

        IN:
            st - renpy related
            at - renpy realted
            character - MASMonika character object
        """
        
        acs_pst_list = [
            acs
            for acs in character.acs.get(MASMonika.PST_ACS, [])
            if acs.keep_on_desk
        ]
        
        
        rk_list = []
        
        
        flt = store.mas_sprites.get_filter()
        
        
        store.mas_sprites._rk_chair(rk_list, character.tablechair, flt)
        
        
        store.mas_sprites._rk_table(
            rk_list,
            character.tablechair,
            False,
            flt
        )
        
        
        store.mas_sprites._rk_accessory_list(
            rk_list,
            acs_pst_list,
            flt,
            "steepling"
        )
        
        
        sprite = store.mas_sprites.MASMonikaRender(
            rk_list,
            flt,
            store.mas_sprites.adjust_x,
            store.mas_sprites.adjust_y,
            store.mas_sprites.LOC_W,
            store.mas_sprites.LOC_H
        )
        
        
        return Transform(sprite, zoom=store.mas_sprites.value_zoom), None
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
