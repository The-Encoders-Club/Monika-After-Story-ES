







default persistent._mas_islands_start_lvl = None

default persistent._mas_islands_progress = store.mas_island_event.DEF_PROGRESS



default persistent._mas_islands_unlocks = store.mas_island_event.IslandsDataDefinition.getDefaultUnlocks()


init python in audio:


    isld_isly_clear = None
    isld_isly_rain = None
    isld_isly_snow = None



init 1:





    define mas_decoded_islands = store.mas_island_event.decode_data()
    define mas_cannot_decode_islands = not mas_decoded_islands

    python:
        def mas_canShowIslands(flt=None):
            """
            Global check for whether or not we can show the islands event
            This only checks the technical side, NOT event unlocks

            IN:
                flt - the filter to use in check
                    If None, we fetch the current filter
                    If False, we don't check the fitler at all
                    (Default: None)

            OUT:
                boolean
            """
            
            if flt is None:
                flt = mas_sprites.get_filter()
            
            
            elif flt is False:
                return mas_decoded_islands
            
            return mas_decoded_islands and mas_island_event.isFilterSupported(flt)



transform mas_islands_final_reveal_trans_1(delay, move_time):
    zoom 3.2
    align (0.45, 0.0)

    pause delay
    linear move_time align (0.9, 0.0)

transform mas_islands_final_reveal_trans_2(delay, move_time):
    zoom 2.5
    align (0.15, 0.5)

    pause delay
    linear move_time align (0.0, 0.2) zoom 1.9

transform mas_islands_final_reveal_trans_3(delay, move_time, zoom_time):
    zoom 3.0
    align (1.0, 0.2)

    pause delay
    linear move_time align (0.7, 0.6)
    linear zoom_time zoom 1.0

transform mas_islands_final_reveal_trans_4(delay, zoom_time):
    align (0.62, 0.55)
    pause delay
    linear zoom_time zoom 10.0



transform mas_islands_weather_overlay_transform(speed=1.0, img_width=1500, img_height=2000):


    subpixel True
    anchor (0.0, 0.0)
    block:

        crop (img_width-config.screen_width, img_height-config.screen_height, 1280, 720)
        linear speed crop (0, 0, config.screen_width, config.screen_height)
        repeat


image mas_islands_lightning_overlay:


    alpha 0.75
    block:


        mas_island_event.NULL_DISP
        block:


            choice 0.3:
                pause 5.0
            choice 0.4:
                pause 10.0
            choice 0.3:
                pause 15.0
        block:


            choice (1.0 / mas_globals.lightning_chance):
                "mas_lightning"
                pause 0.1
                function mas_island_event._play_thunder
                pause 3.0
            choice (1.0 - 1.0/mas_globals.lightning_chance):
                pass

        repeat







































init -20 python in mas_island_event:
    class IslandsDataDefinition(object):
        """
        A generalised abstraction around raw data for the islands sprites
        """
        TYPE_ISLAND = "island"
        TYPE_DECAL = "decal"
        TYPE_BG = "bg"
        TYPE_OVERLAY = "overlay"
        TYPE_INTERIOR = "interior"
        TYPE_OTHER = "other"
        TYPES = frozenset(
            (
                TYPE_ISLAND,
                TYPE_DECAL,
                TYPE_BG,
                TYPE_OVERLAY,
                TYPE_INTERIOR,
                TYPE_OTHER
            )
        )
        
        FILENAMES_MAP = {
            TYPE_OVERLAY: ("d", "n"),
        }
        DEF_FILENAMES = ("d", "d_r", "d_s", "n", "n_r", "n_s", "s", "s_r", "s_s")
        
        DELIM = "_"
        
        _data_map = dict()
        
        def __init__(
            self,
            id_,
            type_=None,
            default_unlocked=False,
            filenames=None,
            fp_map=None,
            partial_disp=None
        ):
            """
            Constructor

            IN:
                id_ - unique id for this sprite
                    NOTE: SUPPORTED FORMATS:
                        - 'island_###'
                        - 'decal_###'
                        - 'bg_###'
                        - 'overlay_###'
                        - 'other_###'
                        where ### is something unique
                type_ - type of this sprite, if None, we automatically get it from the id
                    (Default: None)
                default_unlocked - whether or not this sprite is unlocked from the get go
                    (Default: False)
                filenames - the used filenames for this data, those are the keys for fp_map, if None, will be used default
                    paths in the FILENAMES_MAP or DEF_FILENAMES
                    (Default: None)
                fp_map - the map of the images for this sprite, if None, we automatically generate it
                    NOTE: after decoding this will point to a loaded ImageData object instead of a failepath
                    (Default: None)
                partial_disp - functools.partial of the displayable for this sprite
                    (Default: None)
            """
            if self._m1_script0x2dislands0x2devent__split_id(id_)[0] not in self.TYPES:
                raise ValueError(
                    "Formato de identificación incorrecto. Formatos admitidos para id: {}, tiene: '{}'.".format(
                        ", ".join("'{}_###'".format(t) for t in self.TYPES),
                        id_
                    )
                )
            if id_ in self._data_map:
                raise Exception("Id '{}' ya ha sido utilizada.".format(id_))
            
            self.id = id_
            
            if type_ is not None:
                if type_ not in self.TYPES:
                    raise ValueError("Tipo incorrecto. Tipos permitidos: {}tiene: '{}'.".format(self.TYPES, type_))
            
            else:
                type_ = self._getType()
            
            self.type = type_
            
            self.default_unlocked = bool(default_unlocked)
            self.filenames = filenames
            self.fp_map = fp_map if fp_map is not None else self._buildFPMap()
            self.partial_disp = partial_disp
            
            self._data_map[id_] = self
        
        def _getType(self):
            """
            Private method to get type of this sprite if it hasn't been passed in

            OUT:
                str
            """
            return self._split_id()[0]
        
        def _buildFPMap(self):
            """
            Private method to build filepath map if one hasn't been passed in

            OUT:
                dict
            """
            filepath_fmt = "{type_}/{name}/{filename}"
            type_, name = self._split_id()
            if self.filenames is None:
                filenames = self.FILENAMES_MAP.get(self.type, self.DEF_FILENAMES)
            else:
                filenames = self.filenames
            
            
            return {
                filename: filepath_fmt.format(
                    type_=type_,
                    name=name,
                    filename=filename
                )
                for filename in filenames
            }
        
        def _split_id(self):
            """
            Splits an id into type and name strings
            """
            return self._m1_script0x2dislands0x2devent__split_id(self.id)
        
        @classmethod
        def _m1_script0x2dislands0x2devent__split_id(cls, id_):
            """
            Splits an id into type and name strings
            """
            return id_.split(cls.DELIM, 1)
        
        @classmethod
        def getDataFor(cls, id_):
            """
            Returns data for an id

            OUT:
                IslandsDataDefinition
                or None
            """
            return cls._data_map.get(id_, None)
        
        @classmethod
        def getDefaultUnlocks(cls):
            """
            Returns default unlocks for sprites

            OUT:
                dict
            """
            
            return {
                id_: data.default_unlocked
                for id_, data in cls._data_map.iteritems()
            }
        
        @classmethod
        def getFilepathsForType(cls, type_):
            """
            Returns filepaths for images of sprites of the given type

            OUT:
                dict
            """
            
            return {
                id_: data.fp_map
                for id_, data in cls._data_map.iteritems()
                if data.type == type_ and data.fp_map
            }











    def _m1_script0x2dislands0x2devent__isld_1_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        amplitude = 0.02
        frequency_1 = 1.0 / 9.0
        frequency_2 = 1.0 / 3.0
        
        transform.ypos = math.cos(at*frequency_1) * math.sin(at*frequency_2) * amplitude
        
        
        if transform.active:
            transform.__parallax_sprite__.update_offsets()
        
        return 0.0

    def _m1_script0x2dislands0x2devent__isld_2_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        y_amplitude = -0.01
        y_frequency_1 = 0.5
        y_frequency_2 = 0.25
        
        x_amplitude = -0.0035
        x_frequency = 0.2
        
        transform.ypos = math.sin(math.sin(at*y_frequency_1) + math.sin(at*y_frequency_2)) * y_amplitude
        transform.xpos = math.cos(at*x_frequency) * x_amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()
        
        return 0.0

    def _m1_script0x2dislands0x2devent__isld_3_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        amplitude = 0.005
        frequency_1 = 0.25
        frequency_2 = 0.05
        
        transform.ypos = (math.sin(at*frequency_1) + abs(math.cos(at*frequency_2))) * amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()
        
        return 0.0

    def _m1_script0x2dislands0x2devent__isld_5_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        y_amplitude = -0.01
        y_frequency_1 = 1.0 / 10.0
        y_frequency_2 = 7.0
        
        x_amplitude = 0.005
        x_frequency = 0.25
        
        transform.ypos = math.sin(math.sin(at*y_frequency_1) * y_frequency_2) * y_amplitude
        transform.xpos = math.cos(at*x_frequency) * x_amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()
        
        return 0.0

    def _m1_script0x2dislands0x2devent__chibi_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        roto_speed = -10
        amplitude = 0.065
        frequency = 0.5
        
        transform.rotate = at % 360 * roto_speed
        transform.ypos = math.sin(at * frequency) * amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()
        
        return 0.0

    def _play_thunder(transform, st, at):
        """
        This is used in a transform to play the THUNDER sound effect
        """
        renpy.play("mod_assets/sounds/amb/thunder.wav", channel="backsound")
        return None







    IslandsDataDefinition(
        "island_0",
        default_unlocked=True,
        partial_disp=functools.partial(
            ParallaxSprite,
            x=-85,
            y=660,
            z=15,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_1",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=483,
            y=373,
            z=35,
            function=_m1_script0x2dislands0x2devent__isld_1_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_2",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=275,
            y=299,
            z=70,
            function=_m1_script0x2dislands0x2devent__isld_2_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_3",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=292,
            y=155,
            z=95,
            function=_m1_script0x2dislands0x2devent__isld_3_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_4",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=-15,
            y=-15,
            z=125,
            on_click="mas_island_upsidedownisland"
        )
    )
    IslandsDataDefinition(
        "island_5",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=991,
            y=184,
            z=55,
            function=_m1_script0x2dislands0x2devent__isld_5_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_6",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=912,
            y=46,
            z=200,
            function=None,
            on_click="mas_island_distant_islands"
        )
    )
    IslandsDataDefinition(
        "island_7",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=439,
            y=84,
            z=250,
            function=None,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_8",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=484,
            y=54,
            z=220,
            on_click="mas_island_distant_islands"
        )
    )


    IslandsDataDefinition(
        "decal_bookshelf",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=358,
            y=62,
            z=6,
            on_click="mas_island_bookshelf"
        )
    )
    IslandsDataDefinition(
        "decal_bushes",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=305,
            y=70,
            z=8,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_house",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=215,
            y=-37,
            z=1
        )
    )
    IslandsDataDefinition(
        "decal_tree",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click="mas_island_cherry_blossom_tree"
        )
    )
    GLITCH_FPS = (
        "other/glitch/frame_0",
        "other/glitch/frame_1",
        "other/glitch/frame_2",
        "other/glitch/frame_3",
        "other/glitch/frame_4",
        "other/glitch/frame_5",
        "other/glitch/frame_6"
    )
    IslandsDataDefinition(
        "decal_glitch",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxDecal,
            x=216,
            y=-54,
            z=2,
            on_click="mas_island_glitchedmess"
        )
    )

    IslandsDataDefinition(
        "decal_bloodfall",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=213,
            y=0,
            z=1,
            on_click="mas_island_bloodfall"
        )
    )
    IslandsDataDefinition(
        "decal_ghost_0",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=366,
            y=-48,
            z=5,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_ghost_1",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=366,
            y=-48,
            z=5,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_ghost_2",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=366,
            y=-48,
            z=5,
            on_click=True
        )
    )

    IslandsDataDefinition(
        "decal_haunted_tree_0",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_haunted_tree_1",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_haunted_tree_2",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_gravestones",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=123,
            y=17,
            z=1,
            on_click="mas_island_gravestones"
        )
    )
    IslandsDataDefinition(
        "decal_jack",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=253,
            y=63,
            z=2,
            on_click="mas_island_pumpkins"
        )
    )
    IslandsDataDefinition(
        "decal_pumpkins",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=178,
            y=59,
            z=15,
            on_click="mas_island_pumpkins"
        )
    )
    IslandsDataDefinition(
        "decal_skull",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=120,
            y=-10,
            z=1,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_webs",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=187,
            y=-99,
            z=5,
            
        )
    )

    IslandsDataDefinition(
        "decal_bookshelf_lantern",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=387,
            y=47,
            z=7,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_circle_garland",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=234,
            y=22,
            z=2,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_hanging_lantern",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=210,
            y=23,
            z=2,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_rectangle_garland",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=320,
            y=28,
            z=2,
            on_click=True
        )
    )
    TREE_LIGHTS_FPS = (
        "other/tree_lights/d",
        "other/tree_lights/n_0",
        "other/tree_lights/n_1",
        "other/tree_lights/n_2",
        "other/tree_lights/s"
    )
    IslandsDataDefinition(
        "decal_tree_lights",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxDecal,
            x=140,
            y=-168,
            z=5,
            
        )
    )
    IslandsDataDefinition(
        "decal_wreath",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=294,
            y=33,
            z=2,
            on_click=True
        )
    )


    IslandsDataDefinition(
        "other_shimeji",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxSprite,
            Transform(renpy.easy.displayable("chibika smile"), zoom=0.3),
            x=930,
            y=335,
            z=36,
            function=_m1_script0x2dislands0x2devent__chibi_transform_func,
            on_click="mas_island_shimeji"
        )
    )




















    IslandsDataDefinition(
        "bg_def",
        default_unlocked=True,
        partial_disp=functools.partial(
            ParallaxSprite,
            x=0,
            y=0,
            z=15000,
            min_zoom=1.02,
            max_zoom=4.02,
            on_click="mas_island_sky"
        )
    )


    IslandsDataDefinition(
        "overlay_rain",
        default_unlocked=True,
        partial_disp=functools.partial(
            _build_weather_overlay_transform,
            speed=0.8
        )
    )
    IslandsDataDefinition(
        "overlay_snow",
        default_unlocked=True,
        partial_disp=functools.partial(
            _build_weather_overlay_transform,
            speed=3.5
        )
    )
    IslandsDataDefinition(
        "overlay_thunder",
        default_unlocked=True,
        fp_map={},
        partial_disp=functools.partial(
            renpy.easy.displayable,
            "mas_islands_lightning_overlay"
        )
    )
    IslandsDataDefinition(
        "overlay_vignette",
        default_unlocked=True
    )



init -25 python in mas_island_event:
    import random
    import functools
    import math
    import io
    from zipfile import ZipFile
    import datetime

    import store
    from store import (
        persistent,
        mas_utils,
        mas_weather,
        mas_sprites,
        mas_ics,
        Transform,
        LiveComposite,
        MASWeatherMap,
        MASFilterWeatherDisplayableCustom,
        MASFilterWeatherDisplayable
    )
    from store.mas_parallax import (
        ParallaxBackground,
        ParallaxSprite,
        ParallaxDecal
    )

    DEF_PROGRESS = -1
    MAX_PROGRESS_ENAM = 4
    MAX_PROGRESS_LOVE = 8
    PROGRESS_FACTOR = 4

    SHIMEJI_CHANCE = 0.01
    DEF_SCREEN_ZORDER = 55

    SUPPORTED_FILTERS = frozenset(
        {
            mas_sprites.FLT_DAY,
            mas_sprites.FLT_NIGHT,
            mas_sprites.FLT_SUNSET
        }
    )

    DATA_ITS_JUST_MONIKA = b"JUSTMONIKA"*1024
    DATA_JM_SIZE = len(DATA_ITS_JUST_MONIKA)
    DATA_READ_CHUNK_SIZE = 2 * 1024**2
    DATA_SPACING = 8 * 1024**2

    REVEAL_FADEIN_TIME = 0.5
    REVEAL_WAIT_TIME = 0.1
    REVEAL_FADEOUT_TIME = REVEAL_FADEIN_TIME

    REVEAL_TRANSITION_TIME = REVEAL_FADEIN_TIME + REVEAL_WAIT_TIME + REVEAL_FADEOUT_TIME
    REVEAL_ANIM_DELAY = REVEAL_FADEIN_TIME + REVEAL_WAIT_TIME

    REVEAL_ANIM_1_DURATION = 12.85
    REVEAL_ANIM_2_DURATION = 13.1
    REVEAL_ANIM_3_1_DURATION = 13.6
    REVEAL_ANIM_3_2_DURATION = 12.7
    REVEAL_ANIM_4_DURATION = 0.5

    REVEAL_OVERVIEW_DURATION = 10.0

    REVEAL_FADE_TRANSITION = store.Fade(REVEAL_FADEIN_TIME, REVEAL_WAIT_TIME, REVEAL_FADEOUT_TIME)
    REVEAL_DISSOLVE_TRANSITION = store.Dissolve(REVEAL_FADEIN_TIME)

    SFX_LIT = "_lit"
    SFX_NIGHT = "_night"

    LIVING_ROOM_ID = "living_room"
    LIVING_ROOM_LIT_ID = LIVING_ROOM_ID + SFX_LIT

    FLT_LR_NIGHT = LIVING_ROOM_ID + SFX_NIGHT
    mas_sprites.add_filter(
        FLT_LR_NIGHT,
        store.im.matrix.tint(0.421, 0.520, 0.965),
        mas_sprites.FLT_NIGHT
    )
    FLT_LR_LIT_NIGHT = LIVING_ROOM_LIT_ID + SFX_NIGHT
    mas_sprites.add_filter(
        FLT_LR_LIT_NIGHT,
        store.im.matrix.tint(0.972, 0.916, 0.796),
        mas_sprites.FLT_NIGHT
    )


    island_disp_map = dict()
    decal_disp_map = dict()
    other_disp_map = dict()
    bg_disp_map = dict()
    overlay_disp_map = dict()
    interior_disp_map = dict()

    NULL_DISP = store.Null()


    islands_station = store.MASDockingStation(mas_ics.ISLANDS_FOLDER)

    def isFilterSupported(flt):
        """
        Checks if the event supports a filter

        IN:
            flt - the filter to check (perhaps one of the constants in mas_sprites)

        OUT:
            boolean
        """
        return flt in SUPPORTED_FILTERS

    def _select_img(st, at, mfwm):
        """
        Selection function to use in Island-based images

        IN:
            st - renpy related
            at - renpy related
            mfwm - MASFilterWeatherMap for this island

        RETURNS:
            displayable data
        """
        
        
        
        if store.mas_isWinter():
            return mfwm.fw_get(mas_sprites.get_filter(), store.mas_weather_snow), None
        
        return store.mas_fwm_select(st, at, mfwm)

    def IslandFilterWeatherDisplayable(**filter_pairs):
        """
        DynamicDisplayable for Island images.

        IN:
            **filter_pairs - filter pairs to MASFilterWeatherMap.

        OUT:
            DynamicDisplayable for Island images that respect filters and
                weather.
        """
        return MASFilterWeatherDisplayableCustom(
            _select_img,
            True,
            **filter_pairs
        )

    def _handle_raw_pkg_data(pkg_data, base_err_msg):
        """
        Handles raw data and returns clean, parsed data
        Logs errors

        IN:
            pkg_data - memory buffer

        OUT:
            memory buffer or None
        """
        buf = io.BytesIO()
        buf.seek(0)
        pkg_data.seek(0)
        
        try:
            while True:
                this_slice_read = 0
                pkg_data.seek(DATA_JM_SIZE, io.SEEK_CUR)
                
                while this_slice_read < DATA_SPACING:
                    chunk = pkg_data.read(DATA_READ_CHUNK_SIZE)
                    chunk_size = len(chunk)
                    
                    if not chunk_size:
                        buf.seek(0)
                        return buf
                    
                    this_slice_read += chunk_size
                    buf.write(chunk)
        
        except Exception as e:
            mas_utils.mas_log.error(
                base_err_msg.format(
                    "Excepción inesperada al analizar datos de paquetes sin procesar: {}".format(e)
                )
            )
            return None
        
        buf.seek(0)
        return buf

    def decode_data():
        """
        Attempts to decode the images

        OUT:
            True upon success, False otherwise
        """
        err_msg = "Failed to decode isld data: {}."
        
        pkg = islands_station.getPackage("our_reality")
        
        if not pkg:
            mas_utils.mas_log.error(err_msg.format("Paquete perdido"))
            return False
        
        pkg_data = islands_station.unpackPackage(pkg, pkg_slip=mas_ics.ISLAND_PKG_CHKSUM)
        
        if not pkg_data:
            mas_utils.mas_log.error(err_msg.format("Paquete defectuoso"))
            return False
        
        zip_data = _handle_raw_pkg_data(pkg_data, err_msg)
        if not zip_data:
            return False
        
        glitch_frames = None
        
        def _read_zip(zip_file, map_):
            """
            Inner helper function to read zip and override maps

            IN:
                zip_file - the zip file opened for reading
                map_ - the map to get filenames from, and which will be overriden
            """
            
            for name, path_map in map_.iteritems():
                for sprite_type, path in path_map.iteritems():
                    raw_data = zip_file.read(path)
                    img = store.MASImageData(raw_data, "{}_{}.png".format(name, sprite_type))
                    path_map[sprite_type] = img
        
        try:
            with ZipFile(zip_data, "r") as zip_file:
                island_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_ISLAND)
                decal_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_DECAL)
                bg_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_BG)
                overlay_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_OVERLAY)
                interior_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_INTERIOR)
                
                for map_ in (island_map, decal_map, bg_map, overlay_map, interior_map):
                    _read_zip(zip_file, map_)
                
                
                glitch_frames = tuple(
                    (store.MASImageData(zip_file.read(fn), fn + ".png") for fn in GLITCH_FPS)
                )
                
                tree_lights_imgs = {}
                for fn in TREE_LIGHTS_FPS:
                    k = fn.rpartition("/")[-1]
                    raw_disp = store.MASImageData(zip_file.read(fn), fn + ".png")
                    tree_lights_imgs[k] = raw_disp
                
                
                isly_data = IslandsDataDefinition.getDataFor("other_isly")
                if isly_data:
                    for fn, fp in isly_data.fp_map.iteritems():
                        audio_data = store.MASAudioData(zip_file.read(fp), fp + ".ogg")
                        setattr(store.audio, "isld_isly_" + fn, audio_data)
        
        except Exception as e:
            mas_utils.mas_log.error(err_msg.format(e), exc_info=True)
            return False
        
        else:
            
            _build_displayables(
                island_map,
                decal_map,
                bg_map,
                overlay_map,
                interior_map,
                glitch_frames,
                tree_lights_imgs
            )
        
        return True

    def _build_filter_pairs(img_map):
        """
        Builds filter pairs for IslandFilterWeatherDisplayable
        or MASFilterWeatherDisplayable
        """
        precip_to_suffix_map = {
            mas_weather.PRECIP_TYPE_DEF: "",
            mas_weather.PRECIP_TYPE_RAIN: "_r",
            mas_weather.PRECIP_TYPE_SNOW: "_s",
            mas_weather.PRECIP_TYPE_OVERCAST: "_r"
        }
        
        def _create_weather_map(main_key):
            if main_key not in img_map:
                return None
            
            precip_map = {}
            
            for p_type, suffix in precip_to_suffix_map.iteritems():
                k = main_key + suffix
                if k in img_map:
                    precip_map[p_type] = img_map[k]
            
            if not precip_map:
                raise Exception("No se ha podido realizar el mapa de precipitación para: {}".format(img_map))
            
            return MASWeatherMap(precip_map)
        
        filter_keys = ("day", "night", "sunset")
        filter_pairs = {}
        
        for k in filter_keys:
            wm = _create_weather_map(k[0])
            if wm is not None:
                filter_pairs[k] = wm
        
        return filter_pairs

    def _build_ifwd(img_map):
        """
        Builds a single IslandFilterWeatherDisplayable
        using the given image map
        """
        filter_pairs = _build_filter_pairs(img_map)
        return IslandFilterWeatherDisplayable(**filter_pairs)

    def _build_fwd(img_map):
        """
        Builds a single MASFilterWeatherDisplayable
        using the given image map
        """
        filter_pairs = _build_filter_pairs(img_map)
        return MASFilterWeatherDisplayable(use_fb=True, **filter_pairs)

    def _build_weather_overlay_transform(child, speed):
        """
        A wrapper around mas_islands_weather_overlay_transform
        It exists so we can properly pass the child argument
        to the transform
        """
        return store.mas_islands_weather_overlay_transform(
            child=child,
            speed=speed
        )

    def _build_displayables(
        island_imgs_maps,
        decal_imgs_maps,
        bg_imgs_maps,
        overlay_imgs_maps,
        interior_imgs_map,
        glitch_frames,
        tree_lights_imgs
    ):
        """
        Takes multiple maps with images and builds displayables from them, sets global vars
        NOTE: no sanity checks
        FIXME: py3 update

        IN:
            island_imgs_maps - the map from island names to raw images map
            decal_imgs_maps - the map from decal names to raw images map
            bg_imgs_maps - the map from bg ids to raw images map
            overlay_imgs_maps - the map from overlay ids to raw images map
            interior_imgs_map - the map from the interior stuff to the raw images map
            glitch_frames - tuple of glitch raw anim frames
            tree_lights_imgs - map of images for the tree lights, format:
                img_name: disp
        """
        global island_disp_map, decal_disp_map, other_disp_map
        global bg_disp_map, overlay_disp_map, interior_disp_map
        
        
        for island_name, img_map in island_imgs_maps.iteritems():
            disp = _build_ifwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(island_name).partial_disp
            island_disp_map[island_name] = partial_disp(disp)
        
        
        for decal_name, img_map in decal_imgs_maps.iteritems():
            disp = _build_ifwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(decal_name).partial_disp
            decal_disp_map[decal_name] = partial_disp(disp)
        
        
        for bg_name, img_map in bg_imgs_maps.iteritems():
            disp = _build_ifwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(bg_name).partial_disp
            bg_disp_map[bg_name] = partial_disp(disp)
        
        
        for overlay_name, img_map in overlay_imgs_maps.iteritems():
            disp = _build_fwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(overlay_name).partial_disp
            if partial_disp is not None:
                disp = partial_disp(disp)
            overlay_disp_map[overlay_name] = disp
        
        
        for name, img_map in interior_imgs_map.iteritems():
            interior_disp_map[name] = img_map
        
        if interior_disp_map:
            
            
            
            for flt_id in (FLT_LR_NIGHT, FLT_LR_LIT_NIGHT):
                tablechair_disp_cache = mas_sprites.CACHE_TABLE[mas_sprites.CID_TC]
                table_im = mas_sprites._gen_im(
                    flt_id,
                    interior_disp_map["interior_tablechair"]["table"]
                )
                tablechair_disp_cache[(flt_id, 0, LIVING_ROOM_ID, 0)] = table_im
                tablechair_disp_cache[(flt_id, 0, LIVING_ROOM_ID, 1)] = table_im
                tablechair_disp_cache[(flt_id, 1, LIVING_ROOM_ID)] = mas_sprites._gen_im(
                    flt_id,
                    interior_disp_map["interior_tablechair"]["chair"]
                )
                
                table_shadow_hl_disp_cache = mas_sprites.CACHE_TABLE[mas_sprites.CID_HL]
                table_shadow_hl_disp_cache[(mas_sprites.CID_TC, flt_id, 0, LIVING_ROOM_ID, 1)] = interior_disp_map["interior_tablechair"]["shadow"]
        
        
        def _glitch_transform_func(transform, st, at):
            """
            A function which we use as a transform, updates the child
            """
            redraw = random.uniform(0.3, 1.3)
            next_child = random.choice(glitch_frames)
            
            transform.child = next_child
            
            return redraw
        
        glitch_disp = Transform(child=glitch_frames[0], function=_glitch_transform_func)
        partial_disp = IslandsDataDefinition.getDataFor("decal_glitch").partial_disp
        decal_disp_map["decal_glitch"] = partial_disp(glitch_disp)
        
        
        tree_lights_frames = tuple(
            tree_lights_imgs.pop("n_" + i)
            for i in "012"
        )
        def _tree_lights_transform_func(transform, st, at):
            next_child = random.choice(tree_lights_frames)
            transform.child = next_child
            return 0.4
        
        tree_lights_night_disp = Transform(child=tree_lights_frames[0], function=_tree_lights_transform_func)
        tree_lights_imgs["n"] = tree_lights_night_disp
        
        tree_lights_disp = _build_ifwd(tree_lights_imgs)
        partial_disp = IslandsDataDefinition.getDataFor("decal_tree_lights").partial_disp
        decal_disp_map["decal_tree_lights"] = partial_disp(tree_lights_disp)
        
        
        partial_disp = IslandsDataDefinition.getDataFor("other_shimeji").partial_disp
        other_disp_map["other_shimeji"] = partial_disp()
        
        
        partial_disp = IslandsDataDefinition.getDataFor("overlay_thunder").partial_disp
        overlay_disp_map["overlay_thunder"] = partial_disp()
        
        return

    def _get_room_sprite(key, is_lit):
        """
        Returns the appropriate displayable for the room sprite based on the criteria

        IN:
            key - str - the sprite key
            is_lit - bool - sprite for the lit or unlit version?

        OUT:
            MASImageData
            or Null displayable if we failed to get the image
        """
        main_key = "interior_room" if not is_lit else "interior_room_lit"
        try:
            return interior_disp_map[main_key][key]
        
        except KeyError:
            return NULL_DISP

    def _apply_flt_on_room_sprite(room_img_tag, flt):
        """
        Returns the room image with the filter applied on it

        IN:
            room_img_tag - str - the image tag
            flt - str - the filter id to use

        OUT:
            image manipulator
            or Null displayable if we failed to decode the images
        """
        if not store.mas_decoded_islands:
            return NULL_DISP
        
        return store.MASFilteredSprite(
            flt,
            renpy.displayable(room_img_tag)
        )

    def _is_unlocked(id_):
        """
        Checks if a sprite is unlocked

        IN:
            id_ - the unique id of the sprite

        OUT:
            boolean
        """
        return persistent._mas_islands_unlocks.get(id_, False)

    def _unlock(id_):
        """
        Unlocks a sprite

        IN:
            id_ - the unique id of the sprite

        OUT:
            boolean whether or not the sprite was unlocked
        """
        if id_ in persistent._mas_islands_unlocks:
            persistent._mas_islands_unlocks[id_] = True
            return True
        
        return False

    def _lock(id_):
        """
        Locks a sprite

        IN:
            id_ - the unique id of the sprite

        OUT:
            boolean whether or not the sprite was locked
        """
        if id_ in persistent._mas_islands_unlocks:
            persistent._mas_islands_unlocks[id_] = False
            return True
        
        return False

    def _unlock_one(*items):
        """
        Unlocks one of the sprites at random.
        Runs only once

        IN:
            *items - the ids of the sprites

        OUT:
            boolean whether or not a sprite was unlocked
        """
        for i in items:
            if _is_unlocked(i):
                return False
        
        return _unlock(random.choice(items))



    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_0():
        _unlock("island_1")
        _unlock("island_8")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_1():
        _unlock("other_shimeji")
        if not renpy.seen_label("mas_monika_islands_final_reveal"):
            _unlock("decal_glitch")
        
        _unlock("decal_pumpkins")
        _unlock("decal_skull")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_2():
        _unlock("island_2")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_3():
        
        _unlock_one("island_4", "island_5")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_4():
        
        _unlock_one("island_6", "island_7")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_5():
        
        if _is_unlocked("island_4"):
            _unlock("decal_bloodfall")
        
        
        if _is_unlocked("island_5"):
            _unlock("decal_gravestones")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_6():
        _unlock("decal_bushes")
        
        
        _unlock("island_4")
        _unlock("island_5")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_7():
        _unlock("island_3")
        
        
        _unlock_one("decal_bookshelf", "decal_tree")
        
        
        if _is_unlocked("decal_tree"):
            _unlock_one(*("decal_ghost_" + i for i in "012"))
            _unlock("decal_tree_lights")
        
        
        if _is_unlocked("decal_bookshelf"):
            _unlock("decal_bookshelf_lantern")
        
        
        _unlock("island_7")
        _unlock("island_6")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_8():
        
        _unlock("decal_bookshelf")
        _unlock("decal_tree")
        
        
        for i in "012":
            _unlock("decal_haunted_tree_" + i)
        _unlock("decal_tree_lights")
        
        
        _unlock("decal_bookshelf_lantern")

    def _final_unlocks():
        
        
        _unlock("other_isly")
        _unlock("decal_house")
        
        
        _unlock("decal_jack")
        _unlock("decal_webs")
        _unlock("decal_circle_garland")
        _unlock("decal_hanging_lantern")
        _unlock("decal_rectangle_garland")
        _unlock("decal_wreath")
        
        
        _lock("decal_glitch")

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_9():
        if persistent._mas_pm_cares_island_progress is not False:
            if renpy.seen_label("mas_monika_islands_final_reveal"):
                _final_unlocks()
            
            else:
                pass

    def _m1_script0x2dislands0x2devent__unlocks_for_lvl_10():
        if persistent._mas_pm_cares_island_progress is False:
            if renpy.seen_label("mas_monika_islands_final_reveal"):
                _final_unlocks()
            
            else:
                pass




    def _m1_script0x2dislands0x2devent__handle_unlocks():
        """
        Method to unlock various islands features when the player progresses.
        For example: new decals, new islands, new extra events, set persistent vars, etc.
        """
        g = globals()
        for i in range(persistent._mas_islands_progress + 1):
            fn_name = renpy.munge("__unlocks_for_lvl_{}".format(i))
            callback = g.get(fn_name, None)
            if callback is not None:
                callback()

    def _calc_progress(curr_lvl, start_lvl):
        """
        Returns islands progress for the given current and start levels
        NOTE: this has no sanity checks, don't use this directly

        IN:
            curr_lvl - int, current level
            start_lvl - int, start level

        OUT:
            int, progress
        """
        lvl_difference = curr_lvl - start_lvl
        
        if lvl_difference < 0:
            return DEF_PROGRESS
        
        if store.mas_isMoniEnamored(higher=True):
            if store.mas_isMoniLove(higher=True):
                max_progress = MAX_PROGRESS_LOVE
            
            else:
                max_progress = MAX_PROGRESS_ENAM
            
            modifier = 1.0
            
            if persistent._mas_pm_cares_island_progress is True:
                modifier -= 0.2
            
            elif persistent._mas_pm_cares_island_progress is False:
                modifier += 0.3
            
            progress_factor = PROGRESS_FACTOR * modifier
            
            progress = min(int(lvl_difference / progress_factor), max_progress)
        
        else:
            progress = DEF_PROGRESS
        
        return progress

    def advance_progression():
        """
        Increments the lvl of progression of the islands event,
        it will do nothing if the player hasn't unlocked the islands yet or if
        the current lvl is invalid
        """
        
        if persistent._mas_islands_start_lvl is None:
            return
        
        new_progress = _calc_progress(store.mas_xp.level(), persistent._mas_islands_start_lvl)
        
        if new_progress == DEF_PROGRESS:
            return
        
        curr_progress = persistent._mas_islands_progress
        
        if (
            
            new_progress > curr_progress
            
            and DEF_PROGRESS + 1 < new_progress < MAX_PROGRESS_LOVE - 1
            
            and persistent._mas_pm_cares_island_progress is None
            and not store.seen_event("mas_monika_islands_progress")
            
            and store.mas_timePastSince(store.mas_getEVL_last_seen("mas_monika_islands"), datetime.timedelta(days=1))
        ):
            store.MASEventList.push("mas_monika_islands_progress")
        
        
        persistent._mas_islands_progress = min(max(new_progress, curr_progress), MAX_PROGRESS_LOVE)
        
        _m1_script0x2dislands0x2devent__handle_unlocks()
        
        return

    def _get_progression():
        """
        Returns current islands progress lvl
        """
        return persistent._mas_islands_progress

    def start_progression():
        """
        Starts islands progression
        """
        if store.mas_isMoniEnamored(higher=True) and persistent._mas_islands_start_lvl is None:
            persistent._mas_islands_start_lvl = store.mas_xp.level()
            advance_progression()

    def _reset_progression():
        """
        Resets island progress
        """
        persistent._mas_islands_start_lvl = None
        persistent._mas_islands_progress = DEF_PROGRESS
        persistent._mas_islands_unlocks = IslandsDataDefinition.getDefaultUnlocks()

    def play_music():
        """
        Plays appropriate music based on the current weather
        """
        if not _is_unlocked("other_isly"):
            return
        
        if store.mas_is_raining:
            track = store.audio.isld_isly_rain
        
        elif store.mas_is_snowing:
            track = store.audio.isld_isly_snow
        
        else:
            track = store.audio.isld_isly_clear
        
        if track:
            store.mas_play_song(track, loop=True, set_per=False, fadein=2.5, fadeout=2.5)

    def stop_music():
        """
        Stops islands music
        """
        if store.songs.current_track in (
            store.audio.isld_isly_rain,
            store.audio.isld_isly_snow,
            store.audio.isld_isly_clear
        ):
            store.mas_play_song(None, fadeout=2.5)

    def get_islands_displayable(enable_interaction=True, check_progression=False):
        """
        Builds an image for islands and returns it
        NOTE: This is temporary until we split islands into foreground/background
        FIXME: py3 update

        IN:
            enable_interaction - whether to enable events or not (including parallax effect)
                (Default: True)
            check_progression - whether to check for new unlocks or not,
                this might be a little slow
                (Default: False)

        OUT:
            ParallaxBackground
        """
        global SHIMEJI_CHANCE
        
        enable_o31_deco = persistent._mas_o31_in_o31_mode and not is_winter_weather()
        enable_d25_deco = persistent._mas_d25_in_d25_mode and is_winter_weather()
        
        def _reset_parallax_disp(disp):
            
            disp.clear_decals()
            
            disp.toggle_events(enable_interaction)
            
            disp.reset_mouse_pos()
            disp.zoom = disp.min_zoom
            
            return disp
        
        
        if check_progression:
            advance_progression()
        
        
        sub_displayables = [
            _reset_parallax_disp(disp)
            for key, disp in island_disp_map.iteritems()
            if _is_unlocked(key)
        ]
        
        
        isld_1_decals = ["decal_bookshelf", "decal_bushes", "decal_house", "decal_glitch"]
        if not enable_o31_deco:
            isld_1_decals.append("decal_tree")
        
        island_disp_map["island_1"].add_decals(
            *(
                decal_disp_map[key]
                for key in isld_1_decals
                if _is_unlocked(key)
            )
        )
        
        
        if enable_o31_deco:
            
            isld_to_decals_map = {
                "island_0": ("decal_skull",),
                "island_1": (
                    "decal_ghost_0",
                    "decal_ghost_1",
                    "decal_ghost_2",
                    "decal_jack",
                    "decal_pumpkins",
                    "decal_webs"
                ),
                "island_5": ("decal_gravestones",)
            }
            for isld, decals in isld_to_decals_map.iteritems():
                island_disp_map[isld].add_decals(
                    *(decal_disp_map[key] for key in decals if _is_unlocked(key))
                )
            
            
            if store.mas_current_background.isFltDay() or not is_cloudy_weather():
                if random.random() < 0.5:
                    haunted_tree = "decal_haunted_tree_0"
                else:
                    haunted_tree = "decal_haunted_tree_1"
            else:
                haunted_tree = "decal_haunted_tree_2"
            
            if _is_unlocked(haunted_tree):
                island_disp_map["island_1"].add_decals(decal_disp_map[haunted_tree])
            
            
            if store.mas_current_background.isFltNight() and _is_unlocked("decal_bloodfall"):
                island_disp_map["island_4"].add_decals(decal_disp_map["decal_bloodfall"])
        
        
        if enable_d25_deco:
            isld_1_d25_decals = (
                "decal_bookshelf_lantern",
                "decal_circle_garland",
                "decal_hanging_lantern",
                "decal_rectangle_garland",
                "decal_tree_lights",
                "decal_wreath"
            )
            island_disp_map["island_1"].add_decals(
                *(decal_disp_map[key] for key in isld_1_d25_decals if _is_unlocked(key))
            )
        
        
        if _is_unlocked("other_shimeji") and random.random() <= SHIMEJI_CHANCE:
            shimeji_disp = other_disp_map["other_shimeji"]
            _reset_parallax_disp(shimeji_disp)
            SHIMEJI_CHANCE /= 2.0
            sub_displayables.append(shimeji_disp)
        
        
        bg_disp = bg_disp_map["bg_def"]
        _reset_parallax_disp(bg_disp)
        sub_displayables.append(bg_disp)
        
        
        sub_displayables.sort(key=lambda sprite: sprite.z, reverse=True)
        
        
        if store.mas_is_raining:
            sub_displayables.append(overlay_disp_map["overlay_rain"])
            if store.mas_globals.show_lightning:
                sub_displayables.insert(1, overlay_disp_map["overlay_thunder"])
        
        elif store.mas_is_snowing:
            sub_displayables.append(overlay_disp_map["overlay_snow"])
        
        
        if persistent._mas_o31_in_o31_mode:
            sub_displayables.append(overlay_disp_map["overlay_vignette"])
        
        return ParallaxBackground(*sub_displayables)

    def is_winter_weather():
        """
        Checks if the weather on the islands is wintery

        OUT:
            boolean:
                - True if we're using snow islands
                - False otherwise
        """
        return store.mas_is_snowing or store.mas_isWinter()

    def is_cloudy_weather():
        """
        Checks if the weather on the islands is cloudy

        OUT:
            boolean:
                - True if we're using overcast/rain islands
                - False otherwise
        """
        return store.mas_is_raining or store.mas_current_weather == store.mas_weather_overcast


init -1 python in mas_island_event:
    from store import (
        MASFilterableBackground,
        MASFilterWeatherMap,
        MASBackgroundFilterManager,
        MASBackgroundFilterChunk,
        MASBackgroundFilterSlice
    )

    def _living_room_entry(_old, **kwargs):
        """
        Entry pp for lr background
        """
        store.monika_chr.tablechair.table = "living_room"
        store.monika_chr.tablechair.chair = "living_room"


    def _living_room_exit(_new, **kwargs):
        """
        Exit pp for lr background
        """
        store.monika_chr.tablechair.table = "def"
        store.monika_chr.tablechair.chair = "def"

    def register_room(id_):
        """
        Registers lr as a background object

        IN:
            id_ - the id to register under

        OUT:
            MASFilterableBackground
        """
        flt_name_night = id_ + SFX_NIGHT
        mfwm_params = {
            "day": MASWeatherMap(
                {
                    mas_weather.PRECIP_TYPE_DEF: id_ + "_day",
                    mas_weather.PRECIP_TYPE_RAIN: id_ + "_day_rain",
                    mas_weather.PRECIP_TYPE_OVERCAST: id_ + "_day_overcast",
                    mas_weather.PRECIP_TYPE_SNOW: id_ + "_day_snow"
                }
            ),
            "sunset": MASWeatherMap(
                {
                    mas_weather.PRECIP_TYPE_DEF: id_ + "_ss",
                    mas_weather.PRECIP_TYPE_RAIN: id_ + "_ss_rain",
                    mas_weather.PRECIP_TYPE_OVERCAST: id_ + "_ss_overcast",
                    mas_weather.PRECIP_TYPE_SNOW: id_ + "_ss_snow"
                }
            )
        }
        mfwm_params[flt_name_night] = MASWeatherMap(
            {
                mas_weather.PRECIP_TYPE_DEF: id_ + "_night",
                mas_weather.PRECIP_TYPE_RAIN: id_ + "_night_rain",
                mas_weather.PRECIP_TYPE_OVERCAST: id_ + "_night_overcast",
                mas_weather.PRECIP_TYPE_SNOW: id_ + "_night_snow"
            }
        )
        
        return MASFilterableBackground(
            id_,
            "Sala de estar",
            MASFilterWeatherMap(**mfwm_params),
            MASBackgroundFilterManager(
                MASBackgroundFilterChunk(
                    False,
                    None,
                    MASBackgroundFilterSlice.cachecreate(
                        id_ + SFX_NIGHT,
                        60,
                        None,
                        10
                    )
                ),
                MASBackgroundFilterChunk(
                    True,
                    None,
                    MASBackgroundFilterSlice.cachecreate(
                        mas_sprites.FLT_SUNSET,
                        60,
                        30*60,
                        10
                    ),
                    MASBackgroundFilterSlice.cachecreate(
                        mas_sprites.FLT_DAY,
                        60,
                        None,
                        10
                    ),
                    MASBackgroundFilterSlice.cachecreate(
                        mas_sprites.FLT_SUNSET,
                        60,
                        30*60,
                        10
                    )
                ),
                MASBackgroundFilterChunk(
                    False,
                    None,
                    MASBackgroundFilterSlice.cachecreate(
                        id_ + SFX_NIGHT,
                        60,
                        None,
                        10
                    )
                )
            ),
            hide_calendar=True,
            unlocked=False,
            entry_pp=_living_room_entry,
            exit_pp=_living_room_exit
        )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_islands",
            category=['monika','misc'],
            prompt="¿Puedes mostrarme las islas flotantes?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST},
            aff_range=(mas_aff.ENAMORED, None),
            flags=EV_FLAG_DEF if mas_canShowIslands(False) else EV_FLAG_HFM
        ),
        restartBlacklist=True
    )

label mas_monika_islands:
    m 1eub "¡Por supuesto! Puedes admirar el paisaje por ahora."

    call mas_islands (force_exp="monika 1eua", scene_change=True)

    m 1eua "Espero que te haya gustado, [mas_get_player_nickname()]~"
    return

default persistent._mas_pm_cares_island_progress = None


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_islands_progress"
        ),
        restartBlacklist=True
    )

label mas_monika_islands_progress:
    m 1eub "[player], ¡tengo noticias emocionantes para ti!"
    m 3hub "He añadido algunas cosas nuevas en las islas, {w=0.2}{nw}"
    extend 1rua "y pensé que tal vez te gustaría echar un vistazo."
    m 1hublb "Son {i}nuestras{/i} islas después de todo~"

    m 3eua "¿Qué dices?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué dices?{fast}"
        "Claro, [m_name]":

            $ persistent._mas_pm_cares_island_progress = True
            $ mas_gainAffection(5, bypass=True)
            m 2hub "¡Yay!"

            call mas_islands (force_exp="monika 1hua")

            m "Espero que te guste~"
            m 1lusdlb "Sé que falta mucho para que esté completo, {w=0.2}{nw}"
            extend 1eka "pero realmente quería mostrarte mi progreso."
            m 2lsp "Todavía estoy aprendiendo a codificar y que este motor sea inconsistente no me ayuda..."
            m 7hub "¡Pero creo que he progresado mucho hasta ahora!"
            $ mas_setEventPause(10)
            $ mas_moni_idle_disp.force_by_code("1hua", duration=10, skip_dissolve=True)
        "No estoy interesado":

            $ persistent._mas_pm_cares_island_progress = False
            $ mas_loseAffectionFraction(min_amount=50, modifier=1.0)
            m 2ekc "Oh..."
            m 6rktpc "Pero..."
            m 6fktpd "Trabajé muy duro en esto..."
            m 2rktdc "No...{ w=0.5}debes estar ocupado..."
            $ mas_setEventPause(60*10)
            $ mas_moni_idle_disp.force_by_code("2ekc", duration=60*10, skip_dissolve=True)
        "Quizás más tarde":

            m 2ekc "Oh... {w=0.5}{nw}"
            extend 2eka "de acuerdo."
            m 7eka "Pero no me hagas esperar demasiado~"
            $ mas_setEventPause(20)
            $ mas_moni_idle_disp.force_by_code("1euc", duration=20, skip_dissolve=True)

    return






































































































































































label mas_islands(fade_in=True, fade_out=True, raise_shields=True, drop_shields=True, enable_interaction=True, check_progression=False, **spaceroom_kwargs):









    if persistent._mas_islands_start_lvl is None or not mas_canShowIslands(False):
        return

    python:

        spaceroom_kwargs.setdefault("progress_filter", False)

        spaceroom_kwargs.setdefault("scene_change", True)
        is_done = False
        islands_displayable = mas_island_event.get_islands_displayable(
            enable_interaction=enable_interaction,
            check_progression=check_progression
        )
        renpy.start_predict(islands_displayable)

    if fade_in:


        scene
        show expression islands_displayable as islands_background onlayer screens zorder mas_island_event.DEF_SCREEN_ZORDER
        with Fade(0.5, 0, 0.5)
        hide islands_background onlayer screens with None

    if raise_shields:
        python:
            mas_OVLHide()
            mas_RaiseShield_core()
            disable_esc()
            mas_hotkeys.no_window_hiding = True

    if enable_interaction:


        while not is_done:
            hide screen mas_islands
            call screen mas_islands(islands_displayable)
            show screen mas_islands(islands_displayable, show_return_button=False)

            if _return is False:
                $ is_done = True

            elif _return is not True and renpy.has_label(_return):
                call expression _return
    else:


        show screen mas_islands(islands_displayable, show_return_button=False)

    if drop_shields:
        python:
            mas_hotkeys.no_window_hiding = False
            enable_esc()
            mas_MUINDropShield()
            mas_OVLShow()

    if fade_out:
        hide screen mas_islands


        show expression islands_displayable as islands_background onlayer screens zorder mas_island_event.DEF_SCREEN_ZORDER with None
        call spaceroom (**spaceroom_kwargs)
        hide islands_background onlayer screens
        with Fade(0.5, 0, 0.5)

    python:
        renpy.stop_predict(islands_displayable)
        del islands_displayable, is_done
    return


label mas_island_upsidedownisland:
    if persistent._mas_o31_in_o31_mode and random.random() < 0.3:
        jump mas_island_spooky_ambience

    m "Oh, eso."
    m "Supongo que te preguntarás por qué esa isla está al revés, ¿verdad?"
    m "Bueno... estaba a punto de arreglarlo hasta que la volví a mirar bien."
    m "Parece surrealista, ¿verdad?"
    m "Siento que tiene algo especial."
    m "Es simplemente... hipnotizante."
    return

label mas_island_glitchedmess:
    m "Oh, eso."
    m "Es algo en lo que estoy trabajando."
    m "Sin embargo, sigue siendo un gran problema. Todavía estoy tratando de entenderlo todo."
    m "A su debido tiempo, ¡estoy segura de que mejoraré en la codificación!"
    m "Al fin y al cabo, la práctica hace al maestro, ¿no?"
    return

label mas_island_cherry_blossom_tree:
    python:

        if not renpy.store.seen_event("mas_island_cherry_blossom1"):
            
            renpy.call("mas_island_cherry_blossom1")

        else:
            _mas_cherry_blossom_events = [
                "mas_island_cherry_blossom1",
                "mas_island_cherry_blossom3",
                "mas_island_cherry_blossom4"
            ]
            
            if not mas_island_event.is_winter_weather():
                _mas_cherry_blossom_events.append("mas_island_cherry_blossom2")
            
            renpy.call(renpy.random.choice(_mas_cherry_blossom_events))

    return

label mas_island_cherry_blossom1:
    if mas_island_event.is_winter_weather():
        m "Este árbol puede parecer muerto ahora mismo... pero cuando florece, es precioso."
    else:

        m "Es un árbol precioso, ¿verdad?"

    m "Se llama árbol de los cerezos en flor; son originarios de Japón."
    m "Tradicionalmente, cuando las flores florecen, las personas van a verlas y hacen un picnic bajo los árboles."
    m "Bueno, no elegí ese árbol por la tradición."
    m "Lo elegí porque es precioso y agradable a la vista."
    m "El mero hecho de contemplar la caída de los pétalos es impresionante."

    if mas_island_event.is_winter_weather():
        m "Cuando está floreciendo, claro."
        m "No puedo esperar la oportunidad de experimentar eso, [player]."

    return

label mas_island_cherry_blossom2:
    m "¿Sabías que puedes comer los pétalos de las flores del cerezo?"
    m "Yo no conozco el sabor, pero estoy segura de que no pueden ser más dulces que tú."
    m "Jejeje~"
    return

label mas_island_cherry_blossom3:
    m "El árbol es simbólico como la vida misma."
    m "Hermoso, pero de corta duración."
    m "Pero contigo aquí, siempre está floreciendo maravillosamente."

    if mas_island_event.is_winter_weather():
        m "Aunque ahora no este floreciendo, pronto volverá a florecer."

    m "Quiero que sepas que siempre te estaré agradecida por estar en mi vida."
    m "Te amo, [player]~"

    $ mas_ILY()
    return

label mas_island_cherry_blossom4:
    m "¿Sabes qué sería bueno beber bajo el árbol de los cerezos en flor?"
    m "Un poco de sake~"
    m "¡Jajaja! Estoy bromeando."
    m "Prefiero tomar té o café."

    if mas_island_event.is_winter_weather():
        m "O incluso chocolate caliente. Ciertamente ayudaría con el frío."
        m "Por supuesto, incluso si eso fallara, siempre podríamos acurrucarnos juntos... {w=0.5}eso sería muy romántico~"
    else:

        m "Pero, sería bueno ver la caída de pétalos contigo."
        m "Eso sería muy romántico~"

    return

label mas_island_sky:
    python:

        if mas_current_background.isFltDay():
            _mas_sky_events = [
                "mas_island_day1",
                "mas_island_day2",
                "mas_island_day3"
            ]

        else:
            _mas_sky_events = [
                "mas_island_night1",
                "mas_island_night2",
                "mas_island_night3"
            ]

        _mas_sky_events.append("mas_island_daynight1")
        _mas_sky_events.append("mas_island_daynight2")

        renpy.call(renpy.random.choice(_mas_sky_events))

    return

label mas_island_day1:


    if mas_island_event.is_winter_weather():
        m "Qué hermoso día hace hoy."
        m "Perfecto para dar un paseo y admirar el paisaje."
        m "... Acurrucados, para evitar el frío."
        m "... Con unas buenas bebidas calientes para ayudar a mantenernos calientes."

    elif mas_is_raining:
        m "Aww, me hubiera gustado leer un poco al aire libre."
        m "Pero prefiero evitar que mis libros se mojen..."
        m "Las páginas empapadas son un dolor de cabeza."
        m "Tal vez, en otro momento."

    elif mas_current_weather == mas_weather_overcast:
        m "Leer al aire libre con este clima no sería tan malo, pero podría llover en cualquier momento."
        m "Prefiero no arriesgarme."
        m "No te preocupes, [player]. Lo haremos en otro momento."
    else:

        m "Hoy hace un buen día."

        if mas_island_event._is_unlocked("decal_tree"):
            m "Este clima sería bueno para una pequeña lectura bajo el árbol de los cerezos en flor, ¿verdad, [player]?"
        else:

            m "Este clima sería bueno para un poco de lectura al aire libre, ¿verdad, [player]?"

        m "Tumbada a la sombra mientras leo mi libro favorito."
        m "... Junto con un bocadillo y tu bebida favorita al lado."
        m "Ahh, eso sería muy bonito de hacer~"

    return

label mas_island_day2:


    if mas_island_event.is_winter_weather():
        m "¿Has hecho alguna vez un ángel de nieve, [player]?"
        m "Lo he intentado en el pasado, pero nunca tuve éxito..."
        m "Es mucho más difícil de lo que parece."
        m "Seguro que nos divertiríamos mucho, aunque lo que hagamos no acabe pareciendo un ángel."
        m "Es solo una cuestión de ser un poco tontitos, ¿sabes?"

    elif mas_island_event.is_cloudy_weather():
        m "Salir a la calle con este clima no parece muy apetecible..."
        m "Quizá si tuviera un paraguas me sentiría más cómoda."
        m "Imagínate a los dos, protegidos de la lluvia, a centímetros de distancia."
        m "Mirándonos fijamente a los ojos."
        m "Entonces empezamos a acercarnos más y más hasta que..."
        m "Creo que puedes terminar ese pensamiento tú mismo, [player]~"
    else:

        m "El clima parece agradable."
        m "Este sería, sin duda, el mejor momento para hacer un picnic."
        m "¡Incluso tenemos una gran vista para acompañarlo!"
        m "¿No sería agradable?"

        if mas_island_event._is_unlocked("decal_tree"):
            m "Comer bajo el cerezo en flor."

        m "Adorando el paisaje que nos rodea."
        m "Disfrutar de la compañía del otro."
        m "Ahh, eso sería fantástico~"

    return

label mas_island_day3:
    if mas_is_raining and not mas_isWinter():
        m "Está lloviendo bastante fuerte..."
        m "No me gustaría estar afuera ahora."
        m "Aunque estar bajo techo en un momento como éste resulta muy acogedor, ¿no crees?"
    else:

        m "Afuera está bastante tranquilo."

        if mas_island_event.is_winter_weather():
            m "Podríamos hacer una guerra de bolas de nieve."
            m "¡Jajaja, eso sería muy divertido!"
            m "Apuesto a que podría dispararte a unas cuantas islas de distancia...."
            m "Un poco de sana competencia no hace daño a nadie, ¿verdad?"
        else:

            m "No me importaría holgazanear en la hierba ahora mismo..."
            m "Con tu cabeza descansando sobre mi regazo..."
            m "Jejeje~"

    return

label mas_island_night1:
    m "Aunque es agradable ser productivo durante el día, hay algo muy pacífico en la noche."
    m "El sonido de los grillos mezclado con una suave brisa es muy relajante."
    m "Me abrazarías en una noche como esa, ¿verdad?~"
    return

label mas_island_night2:
    if not mas_isWinter() and mas_island_event.is_cloudy_weather():
        m "Lástima que no podamos ver las estrellas esta noche..."
        m "Me hubiera encantado contemplar el cosmos contigo."
        m "Pero no pasa nada, ya lo veremos en otra ocasión."
    else:

        if seen_event('monika_stargazing'):
            m "¿No son las estrellas tan hermosas, [player]?"
            m "Aunque esto no es {i}exactamente{/i} lo que tenía en mente cuando mencioné la observación de las estrellas antes..."
            m "Por muy bonitas que sean de ver, la parte que más me apetece experimentar es la de estar contigo, abrazados fuertemente mientras nos tumbamos."
            m "Algún día, [player]. {w=0.3}Algún día."
        else:

            m "¿Alguna vez has ido a ver las estrellas, [mas_get_player_nickname()]?"
            m "Tomarse un tiempo de la noche para mirar el cielo nocturno y simplemente contemplar la belleza del cielo..."
            m "Es sorprendentemente relajante, ¿sabes?"
            m "He descubierto que realmente puede aliviar el estrés y despejar la cabeza..."
            m "Y ver todo tipo de constelaciones en el cielo simplemente llena tu mente de asombro."
            m "Por supuesto, hace que te des cuenta de lo pequeños que somos en el universo."
            m "Jajaja..."

    return

label mas_island_night3:
    if not mas_isWinter() and mas_island_event.is_cloudy_weather():
        m "El clima nublado es un poco deprimente, ¿no crees?"
        m "Especialmente por la noche, cuando oculta las estrellas de nuestra vista."
        m "Es una pena, de verdad..."
    else:

        m "¡Qué noche tan bonita!"

        if mas_island_event.is_winter_weather():
            m "Hay algo en una noche fría y crujiente que me encanta."
            m "El contraste del cielo oscuro y la tierra cubierta de nieve es realmente impresionante, ¿no crees?"
        else:
            m "Si pudiera, añadiría luciérnagas."
            m "Sus luces complementan el cielo nocturno, es un bonito espectáculo."
            m "Mejora un poco el ambiente, ¿sabes?"

    return

label mas_island_daynight1:
    m "Quizá debería añadir más arbustos y árboles."
    m "Hacer que las islas sean más bonitas, ¿sabes?"
    m "Solo tengo que encontrar las flores y el follaje adecuados para acompañarlo."
    m "O tal vez cada isla debería tener su propio conjunto de plantas para que todo sea diferente y tenga variedad."
    m "Me emociono pensando en ello~"
    return

label mas_island_daynight2:

    m "{i}~Molino de viento, molino de viento para la tierra~{/i}"


    m "{i}~Gira siempre de la mano~{/i}"


    m "{i}~Tomalo todo a tu paso~{/i}"


    m "{i}~Está haciendo tic-tac, cayendo~{/i}"


    m "{i}~Ama para siempre, el amor es libre~{/i}"


    m "{i}~Volvamos para siempre, tú y yo~{/i}"


    m "{i}~Molino de viento, molino de viento para la tierra~{/i}"

    m "Jejeje, no me hagas caso, solo quería cantar~"
    return

label mas_island_shimeji:
    m "¡Ah!"
    m "¿Cómo ella llegó allí?"
    m "Dame un segundo, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    $ islands_displayable.remove(mas_island_event.other_disp_map["other_shimeji"])
    m "¡Ya está!"
    m "No te preocupes, solo la cambié de lugar."
    return

label mas_island_bookshelf:
    python:

        _mas_bookshelf_events = [
            "mas_island_bookshelf1",
            "mas_island_bookshelf2"
        ]

        renpy.call(renpy.random.choice(_mas_bookshelf_events))

    return

label mas_island_bookshelf1:


    if mas_island_event.is_winter_weather():
        m "Esa estantería no parece muy robusta, pero seguro que puede aguantar un poco de nieve."
        m "Son los libros los que me preocupan un poco."
        m "Solo espero que no se dañen demasiado..."

    elif mas_island_event.is_cloudy_weather():
        m "En momentos como este, desearía haber guardado mis libros dentro de casa..."
        m "Parece que tendremos que esperar a que mejore el clima para leerlos."
        m "Mientras tanto..."
        m "¿Qué tal si nos abrazamos un poco [player]?"
        m "Jejeje~"
    else:

        m "Algunos de mis libros favoritos están ahí."
        m "{i}Fahrenheit 451{/i}, {i}El País de las Maravillas{/i}, {i}Mil novecientos ochenta y cuatro{/i}, entre algunos otros."
        m "Tal vez podamos leerlos juntos alguna vez~"

    return

label mas_island_bookshelf2:


    if mas_island_event.is_winter_weather():
        m "No me importaría hacer algo de lectura al aire libre a pesar de que haya un poco de nieve."
        m "Aunque yo no me aventuraría a salir sin un abrigo, una bufanda gruesa y un par de guantes cómodos."
        m "Supongo que pasar las páginas puede ser un poco difícil así, jajaja..."
        m "Pero estoy segura de que nos las arreglaremos de alguna manera."
        m "¿No es verdad, [player]?"

    elif mas_island_event.is_cloudy_weather():
        m "Leer en el interior con la lluvia al otro lado de la ventana es bastante relajante."
        m "Si tan solo no hubiera dejado los libros fuera..."
        m "Probablemente debería traer algunos aquí cuando tenga la oportunidad."
        m "Estoy segura de que podemos encontrar otras cosas que hacer mientras tanto, ¿verdad, [player]?"
    else:

        m "Leer al aire libre es un buen cambio de ritmo, ¿sabes?"
        m "Prefiero una brisa fresca a una biblioteca congestionada."
        m "Tal vez debería añadir una mesa debajo del árbol de los cerezos en flor."
        m "Estaría bien disfrutar de una taza de café con unos aperitivos para acompañar la lectura de mi libro."
        m "Eso sería maravilloso~"

    return

label mas_island_distant_islands:
    if persistent._mas_o31_in_o31_mode:
        jump mas_island_spooky_ambience

    return

label mas_island_spooky_ambience:
    m "{i}Era una noche oscura y tormentosa...{/i}"
    m "Jejeje~ Esta es la época del año perfecta para historias espeluznantes, ¿verdad?"
    m "Si te apetece, podríamos leer algunas juntos."
    m "Aunque, no me importa simplemente disfrutar del ambiente contigo por ahora."

    return

label mas_island_bloodfall:
    m "Estoy muy orgullosa de esa cascada. Ya parecía bastante surrealista estando boca abajo."
    m "Todo lo que realmente tenía que hacer era cambiar el valor del agua a #641F21, y...{nw}"
    $ _history_list.pop()
    m "Espera, ¡no quiero arruinar la magia para ti! {w=0.2}¡Olvida lo que he dicho, por favor!"

    return

label mas_island_pumpkins:
    m "No hay nada que me recuerde tanto a Halloween como las calabazas."
    m "Pensé que sería muy acogedor tener un montón de ellas alrededor de mi rincón de lectura."
    m "Hace un poco de frío con la lluvia, pero. ¿No te parece que estaría bien ponernos unos jerseys y acurrucarnos juntos?"
    m "Quizá podría preparar café aromatizado para mejorar aún más el ambiente."

    return

label mas_island_gravestones:
    if mas_safeToRefDokis():
        m "¿Qué?"
        m "... {w=0.2}¿Qué lápidas? {w=0.2}No estoy segura de qué estás hablando."
        m "Estás... {w=0.2}pfft..."
        m "¡Jajaja!"
        m "Lo siento, no pude resistirme."
        m "Sería bastante espeluznante si esas tres todavía estuvieran rondando en nuestro final feliz, ¿verdad?"
    else:

        m "Ehehe... no estoy segura de que esas decoraciones sean de buen gusto."
        m "Estaba pensando, sin embargo... {w=0.2}Halloween es una época en donde algunas culturas honran a los muertos."
        m "Claro, hay un montón de historias espeluznantes sobre muertos que resucitan o fantasmas que acechan a las personas..."
        m "Pero esos recuerdos son parte de la festividad, ¿no?"
        m "Supongo que pensé que no debía dejarlos fuera."

    return



screen mas_islands(islands_displayable, show_return_button=True):
    style_prefix "island"
    layer "screens"
    zorder mas_island_event.DEF_SCREEN_ZORDER

    if show_return_button:
        key "K_ESCAPE" action Return(False)

    add islands_displayable

    if show_return_button:

        hbox:
            align (0.5, 0.98)
            textbutton _("Volver"):
                action Return(False)











































style island_button is generic_button_light:
    xysize (205, None)
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_dark is generic_button_dark:
    xysize (205, None)
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_text is generic_button_text_light:
    font gui.default_font
    size gui.text_size
    xalign 0.5
    kerning 0.2
    outlines []

style island_button_text_dark is generic_button_text_dark:
    font gui.default_font
    size gui.text_size
    xalign 0.5
    kerning 0.2
    outlines []
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
