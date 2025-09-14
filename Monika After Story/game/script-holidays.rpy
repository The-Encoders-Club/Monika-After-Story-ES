













default persistent._mas_event_clothes_map = dict()
define mas_five_minutes = datetime.timedelta(seconds=5*60)
define mas_one_hour = datetime.timedelta(seconds=3600)
define mas_three_hour = datetime.timedelta(seconds=3*3600)

init 10 python:
    def mas_addClothesToHolidayMap(clothes, key=None):
        """
        Adds the given clothes to the holiday clothes map

        IN:
            clothes - clothing item to add
            key - dateime.date to use as key. If None, we use today
        """
        if clothes is None:
            return
        
        if key is None:
            key = datetime.date.today()
        
        persistent._mas_event_clothes_map[key] = clothes.name
        
        
        mas_unlockEVL("monika_event_clothes_select", "EVE")

    def mas_addClothesToHolidayMapRange(clothes, start_date, end_date):
        """
        Adds the given clothes to the holiday clothes map over the day range provided

        IN:
            clothes - clothing item to add
            start_date - datetime.date to start adding to the map on
            end_date - datetime.date to stop adding to the map on
        """
        if not clothes:
            return
        
        
        daterange = mas_genDateRange(start_date, end_date)
        
        
        for date in daterange:
            mas_addClothesToHolidayMap(clothes, date)

    def mas_doesBackgroundHaveHolidayDeco(deco_tags, background_id=None):
        """
        Checks if a background has support for the given deco tag(s)

        IN:
            deco_tags - list of deco tags to check for

            background_id - id of the background to check if it supports deco
                If None, mas_current_background's id is used
                (Default: None)
        """
        if background_id is None:
            background_id = store.mas_current_background.background_id
        
        for deco_tag in deco_tags:
            if MASImageTagDecoDefinition.get_adf(background_id, deco_tag):
                return True
        return False

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we've been out all day for

        OUT:
            True if the player and Monika were out together the whole day, False if not.
        """
        checkout_time = store.mas_dockstat.getCheckTimes()[0]
        return checkout_time is not None and checkout_time.date() < _date


    def mas_capGainAff(amount, aff_gained_var, normal_cap, pbday_cap=None):
        """
        Gains affection according to the cap(s) defined

        IN:
            amount:
                Amount of affection to gain

            aff_gained_var:
                The persistent variable which the total amount gained for the holiday is stored
                (NOTE: Must be a string)

            normal_cap:
                The cap to use when not player bday

            pbday_cap:
                The cap to use when it's player bday (NOTE: if not provided, normal_cap is assumed)
        """
        
        
        if persistent._mas_player_bday_in_player_bday_mode and pbday_cap:
            cap = pbday_cap
        else:
            cap = normal_cap
        
        if persistent.__dict__[aff_gained_var] < cap:
            persistent.__dict__[aff_gained_var] += amount
            mas_gainAffection(amount, bypass=True)
        
        return

    def mas_hasSpecialOutfit(_date=None):
        """
        Checks if the given date is a special event that has an outfit in the event clothes map
        IN:
            _date - date to check.
                (Default: None)

        RETURNS: True if given date has a special outfit, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date in persistent._mas_event_clothes_map

init -10 python:
    def mas_isA01(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == datetime.date(_date.year,4,1)


label mas_lingerie_intro(holiday_str, lingerie_choice):
    m 1ekbfa "..."
    m "Por cierto, [player]..."
    m 3ekbfsdla "Hay... {w=1}a-algo que quiero mostrarte."
    m 2rkbfsdla "En realidad, he querido hacer esto por un tiempo, pero... {w=1}bueno, es un poco vergonzoso..."
    m "..."
    m 2hkbfsdlb "¡Oh dios, estoy super nerviosa, jajaja!"
    m 2rkbfsdlc "Es solo que nunca he...{nw}"
    m 2dkbfsdlc "Ah, está bien, es hora de dejar de estancarme y simplemente hacerlo."
    m 2ekbfsdla "Solo dame unos segundos, [player]."
    call mas_clothes_change (outfit=lingerie_choice, outfit_mode=True, exp="monika 2rkbfsdlu", restore_zoom=False, unlock=True)
    pause 3.0
    m 2ekbfsdlb "Jajaja, [player]... {w=1}estás mirándome mucho..."
    m 2ekbfu "Bueno... {w=1}¿Te gusta lo que ves?"
    m 1lkbfa "En realidad, nunca... {w=1}me había puesto algo como esto."
    m "... Al menos no que nadie haya visto."

    if mas_hasUnlockedClothesWithExprop("bikini"):
        m 3hkbfb "Jajaja, ¿qué estoy diciendo? Me has visto en bikini antes, que es esencialmente lo mismo..."
        m 2rkbfa "... Aunque, por alguna razón, esto se siente... {w=0.5}{i}diferente{/i}."

    m 2ekbfa "De todos modos, algo sobre estar contigo [holiday_str] parece realmente romántico, ¿sabes?"
    m "Simplemente se sintió como el momento perfecto para el siguiente paso en nuestra relación."
    m 2rkbfsdlu "Ahora sé que realmente no podemos...{nw}"
    m 3hubfb "¡Ah! ¡No importa, jajaja!"
    return





default persistent._mas_o31_in_o31_mode = False


default persistent._mas_o31_tt_count = 0


default persistent._mas_o31_trick_or_treating_aff_gain = 0


default persistent._mas_o31_relaunch = False




default persistent._mas_o31_costumes_worn = {}


define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        
        
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_o31_in_o31_mode": "o31.mode.o31",
            "_mas_o31_tt_count": "o31.tt.count",
            "_mas_o31_relaunch": "o31.relaunch",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 10, 31),

        
        end_dt=datetime.datetime(2019, 11, 2)
    ))


image mas_o31_ceiling_lights = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/ceiling_lights.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_candles = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/candles.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_jack_o_lantern = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/jackolantern.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_wall_candle = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/wall_candle.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_cat_frame:
    block:
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_0.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-1.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-2.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-3.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-1.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-2.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-3.png")

    30
    repeat

image mas_o31_garlands = MASFilterSwitch("mod_assets/location/spaceroom/o31/garland.png")
image mas_o31_cobwebs = MASFilterSwitch("mod_assets/location/spaceroom/o31/wall_webs.png")
image mas_o31_window_ghost = MASFilterSwitch("mod_assets/location/spaceroom/o31/window_ghost.png")
image mas_o31_ceiling_deco = MASFilterSwitch("mod_assets/location/spaceroom/o31/ceiling_deco.png")
image mas_o31_wall_bats = MASFilterSwitch("mod_assets/location/spaceroom/o31/wall_bats.png")

image mas_o31_vignette = Image("mod_assets/location/spaceroom/o31/vignette.png")

init 501 python:

    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_candle",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_cat_frame",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_bats",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_window_ghost",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_cobwebs",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_candles",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_jack_o_lantern",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_ceiling_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_ceiling_deco",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )


    MASImageTagDecoDefinition.register_img(
        "mas_o31_vignette",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=21) 
    )

init python:
    MAS_O31_COSTUME_CG_MAP = {
        mas_clothes_marisa: "o31mcg",
        mas_clothes_rin: "o31rcg"
    }


init -10 python:
    import random

    MAS_O31_DECO_TAGS = [
        "mas_o31_wall_candle",
        "mas_o31_cat_frame",
        "mas_o31_wall_bats",
        "mas_o31_window_ghost",
        "mas_o31_cobwebs",
        "mas_o31_candles",
        "mas_o31_jack_o_lantern",
        "mas_o31_garlands",
        "mas_o31_ceiling_lights",
        "mas_o31_ceiling_deco",
        "mas_o31_vignette"
    ]

    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_o31.replace(year=_date.year)

    def mas_o31ShowVisuals():
        """
        Shows o31 visuals
        """
        for _tag in MAS_O31_DECO_TAGS:
            mas_showDecoTag(_tag)


    def mas_o31HideVisuals():
        """
        Hides o31 visuals + vignette
        """
        for _tag in MAS_O31_DECO_TAGS:
            mas_hideDecoTag(_tag, hide_now=True)


    def mas_o31ShowSpriteObjects():
        """
        Shows o31 specific sprite objects
        """
        monika_chr.wear_acs(mas_acs_desk_lantern)
        monika_chr.wear_acs(mas_acs_desk_candy_jack)


    def mas_o31HideSpriteObjects():
        """
        Hides o31 specific sprite objects
        """
        
        hair = store.mas_selspr.get_sel_hair(store.mas_hair_down)
        if hair is not None and not hair.unlocked:
            store.mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        store.mas_lockEVL("monika_event_clothes_select", "EVE")
        
        
        if store.monika_chr.is_wearing_clothes_with_exprop("costume"):
            store.MASEventList.queue('mas_change_to_def')


    def mas_hasO31DeskAcs():
        """
        Checks if we have any o31 desk acs

        OUT:
            boolean
        """
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )
        
        for acs_ in o31_desk_acs_tuple:
            if monika_chr.is_wearing_acs(acs_):
                return True
        
        return False

    def mas_o31HideDeskAcs():
        """
        Removes o31 desk acs
        """
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )
        
        for acs_ in o31_desk_acs_tuple:
            monika_chr.remove_acs(acs_)

    def mas_o31CapGainAff(amount):
        """
        CapGainAffection function for o31. See mas_capGainAff for details
        """
        mas_capGainAff(amount, "_mas_o31_trick_or_treating_aff_gain", 15)


    def mas_o31CostumeWorn(clothes):
        """
        Checks if the given clothes was worn on o31

        IN:
            clothes - Clothes object to check

        RETURNS: year the given clothe was worn if worn on o31, None if never
            worn on o31.
        """
        if clothes is None:
            return False
        return mas_o31CostumeWorn_n(clothes.name)


    def mas_o31CostumeWorn_n(clothes_name):
        """
        Checks if the given clothes (name) was worn on o31

        IN:
            clothes_name - Clothes name to check

        RETURNS: year the given clothes name was worn if worn on o31, none if
            never worn on o31.
        """
        return persistent._mas_o31_costumes_worn.get(clothes_name, None)


    def mas_o31SelectCostume(selection_pool=None):
        """
        Selects an o31 costume to wear. Costumes that have not been worn
        before are selected first.

        NOTE: o31 costume wear flag is NOT set here. Make sure to set this
            manually later.

        IN:
            selection_pool - pool to select clothes from. If NOne, we get a
                default list of clothes with costume exprop

        RETURNS: a single MASClothes object of what to wear. None if cannot
            return anything.
        """
        if selection_pool is None:
            selection_pool = MASClothes.by_exprop("costume", "o31")
        
        
        wearing_costume = False
        
        
        
        
        
        filt_sel_pool = []
        for cloth in selection_pool:
            sprite_key = (store.mas_sprites.SP_CLOTHES, cloth.name)
            giftname = store.mas_sprites_json.namegift_map.get(
                sprite_key,
                None
            )
            
            if (
                giftname is None
                or sprite_key in persistent._mas_sprites_json_gifted_sprites
            ):
                if cloth != monika_chr.clothes:
                    filt_sel_pool.append(cloth)
                else:
                    wearing_costume = True
        
        
        selection_pool = filt_sel_pool
        
        if len(selection_pool) < 1:
            
            
            if wearing_costume:
                
                if monika_chr.clothes in MAS_O31_COSTUME_CG_MAP:
                    store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[monika_chr.clothes])
                
                return monika_chr.clothes
            return None
        
        elif len(selection_pool) < 2:
            
            return selection_pool[0]
        
        
        non_worn = [
            costume
            for costume in selection_pool
            if not mas_o31CostumeWorn(costume)
        ]
        
        if len(non_worn) > 0:
            
            random_outfit = random.choice(non_worn)
        
        else:
            
            random_outfit = random.choice(selection_pool)
        
        
        if random_outfit in MAS_O31_COSTUME_CG_MAP:
            store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[random_outfit])
        
        
        return random_outfit

    def mas_o31SetCostumeWorn(clothes, year=None):
        """
        Sets that a clothing item is worn. Exprop checking is done

        IN:
            clothes - clothes object to set
            year - year that the costume was worn. If NOne, we use current year
        """
        if clothes is None or not clothes.hasprop("costume"):
            return
        
        mas_o31SetCostumeWorn_n(clothes.name, year=year)


    def mas_o31SetCostumeWorn_n(clothes_name, year=None):
        """
        Sets that a clothing name is worn. NO EXPROP CHECKING IS DONE

        IN:
            clothes_name - name of clothes to set
            year - year that the costume was worn. If None, we use current year
        """
        if year is None:
            year = datetime.date.today().year
        
        persistent._mas_o31_costumes_worn[clothes_name] = year

    def mas_o31Cleanup():
        """
        Cleanup function for o31
        """
        
        if monika_chr.is_wearing_clothes_with_exprop("costume"):
            monika_chr.change_clothes(mas_clothes_def, outfit_mode=True)
            monika_chr.reset_hair()
        
        
        persistent._mas_o31_in_o31_mode = False
        
        
        mas_checkBackgroundChangeDelegate()
        
        
        mas_o31HideVisuals()
        mas_o31HideSpriteObjects()
        
        
        store.persistent._mas_o31_in_o31_mode = False
        
        
        mas_rmallEVL("mas_o31_cleanup")
        
        
        hair = store.mas_selspr.get_sel_hair(mas_hair_down)
        if hair is not None and not hair.unlocked:
            mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        mas_lockEVL("monika_event_clothes_select", "EVE")

init -11 python in mas_o31_event:
    import store
    import datetime


    cg_station = store.MASDockingStation(store.mas_ics.o31_cg_folder)


    cg_decoded = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return store.mas_dockstat.decodeImages(cg_station, store.mas_ics.o31_map, [key])


    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        store.mas_dockstat.removeImages(cg_station, store.mas_ics.o31_map)


label mas_o31_autoload_check:
    python:
        import random

        if mas_isO31() and datetime.datetime.now().hour >= 3 and mas_isMoniNormal(higher=True):
            
            
            
            
            
            
            if not mas_doesBackgroundHaveHolidayDeco(MAS_O31_DECO_TAGS):
                mas_changeBackground(mas_background_def, set_persistent=True)
            
            
            if (not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                
                mas_skip_visuals = True
                
                
                mas_resetIdleMode()
                
                
                mas_lockEVL("greeting_hairdown", "GRE")
                
                
                store.mas_hotkeys.music_enabled = False
                
                
                mas_calRaiseOverlayShield()
                
                
                
                costume = mas_o31SelectCostume()
                store.mas_selspr.unlock_clothes(costume)
                mas_addClothesToHolidayMap(costume)
                mas_o31SetCostumeWorn(costume)
                
                
                ribbon_acs = monika_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    monika_chr.remove_acs(ribbon_acs)
                
                monika_chr.change_clothes(
                    costume,
                    by_user=False,
                    outfit_mode=True
                )
                
                
                store.mas_selspr.save_selectables()
                
                
                renpy.save_persistent()
                
                
                greet_label = "greeting_o31_{0}".format(costume.name)
                
                if renpy.has_label(greet_label):
                    selected_greeting = greet_label
                else:
                    selected_greeting = "greeting_o31_generic"
                
                
                mas_temp_zoom_level = store.mas_sprites.zoom_level
                store.mas_sprites.reset_zoom()
                
                
                persistent._mas_o31_in_o31_mode = True
                
                
                mas_o31ShowVisuals()
                mas_o31ShowSpriteObjects()
                
                
                mas_changeWeather(mas_weather_thunder, True)
            
            elif (persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                mas_o31ShowVisuals()
                mas_o31ShowSpriteObjects()
                mas_changeWeather(mas_weather_thunder, True)


        elif not mas_isO31() or mas_isMoniDis(lower=True):
            mas_o31Cleanup()
            mas_o31HideDeskAcs()


        elif persistent._mas_o31_in_o31_mode and mas_isMoniUpset():
            mas_o31ShowVisuals()
            mas_o31ShowSpriteObjects()
            mas_changeWeather(mas_weather_thunder, True)


    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check


    jump mas_ch30_post_holiday_check

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_holiday_o31_returned_home_relaunch",
            conditional=(
                "not persistent._mas_o31_in_o31_mode "
                "and not mas_isFirstSeshDay()"
            ),
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=6)),
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_holiday_o31_returned_home_relaunch:
    m 1eua "Entonces, hoy es..."
    m 1euc "... Espera."
    m "..."
    m 2wuo "¡Oh!"
    m 2wuw "¡Oh dios mío!"
    m 2hub "Ya es Halloween, [player]."
    m 1eua "... {w=1}Quiero decir."
    m 3eua "Voy a cerrar el juego."
    m 1eua "Después de eso, puedes volver a abrirlo."
    m 1hubsa "Tengo algo especial reservado para ti, jejeje~"
    $ persistent._mas_o31_relaunch = True
    $ mas_rmallEVL("mas_holiday_o31_returned_home_relaunch")
    return "quit"


image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"


image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"


transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_cleanup",
            conditional="persistent._mas_o31_in_o31_mode",
            start_date=datetime.datetime.combine(mas_o31 + datetime.timedelta(days=1), datetime.time(12)),
            end_date=mas_o31 + datetime.timedelta(weeks=1),
            action=EV_ACT_QUEUE,
            rules={"no_unlock": None},
            years=[]
        )
    )

label mas_o31_cleanup:
    python:
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )

    m 1eua "Un segundo [player], solo voy a quitar los adornos.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    python hide:
        for acs_ in o31_desk_acs_tuple:
            acs_.keep_on_desk = False

    call mas_transition_to_emptydesk

    python hide:
        for acs_ in o31_desk_acs_tuple:
            monika_chr.remove_acs(acs_)
            acs_.keep_on_desk = True

    pause 4.0

    $ mas_o31Cleanup()

    with dissolve
    pause 2.0

    call mas_transition_from_emptydesk ("monika 1hua")

    m 3hua "Todo listo~"

    $ del o31_desk_acs_tuple

    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_marisa:

    $ store.mas_selspr.unlock_acs(mas_acs_marisa_witchhat)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)


    if store.mas_o31_event.cg_decoded:


        call spaceroom (hide_monika=True, scene_change=True)
    else:



        call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "¡Ah!"
    m 1hua "Parece que mi hechizo funcionó."
    m 3efu "¡Como mi sirviente recién convocado, tendrás que cumplir mis órdenes hasta el fin de los tiempos!"
    m 1rksdla "..."
    m 1hub "¡Jajaja!"


    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        m "Estoy aquí, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()
        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua zorder MAS_MONIKA_Z at i11

        window auto
        m "¡Tadaa!~"


    m 1hua "Bueno..."
    m 1eub "¿Qué piensas?"
    m 1wua "Me queda bastante bien, ¿verdad?"
    m 1eua "Me tomó bastante tiempo hacer este disfraz, ya sabes."
    m 3hksdlb "Obtener las medidas correctas, asegurarme de que nada esté demasiado apretado o suelto, ese tipo de cosas."
    m 3eksdla "... ¡Especialmente el sombrero!"
    m 1dkc "El lazo no se queda quieto en lo absoluto..."
    m 1rksdla "Por suerte lo solucioné."
    m 3hua "Yo diría que hice un buen trabajo."
    m 3eka "Me pregunto si podrás ver qué es diferente hoy."
    m 3tub "Además de mi disfraz, por supuesto~"
    m 1hua "Pero de todos modos..."

    if store.mas_o31_event.cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbsa "Estoy muy emocionada de pasar Halloween contigo."
    m 1hua "¡Vamos a divertirnos hoy!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_rin",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_rin:
    python:
        title_cased_hes = hes.capitalize()



        mas_sprites.zoom_out()


    call spaceroom (hide_monika=True, scene_change=True)

    m "Ugh, espero haber acertado con estas trenzas."
    m "¿Por qué este disfraz tiene que ser tan complicado...?"
    m "¡Oh rayos! ¡[title_cased_hes]tá aquí!"
    window hide
    pause 3.0

    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        window auto
        m "Dime, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "¿Qué piensas {i}nya{/i}?"

        scene black
        pause 1.0
        call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static')
        m 1hksdlb "Jajaja, decir eso en voz alta fue más vergonzoso de lo que pensé..."
    else:

        call mas_transition_from_emptydesk ("monika 1eua")
        m 1hub "¡Hola, [player]!"
        m 3hub "¿Te gusta mi disfraz?"


    m 3etc "Honestamente, ni siquiera sé quién se supone que sea."
    m 3etd "Lo encontré en el armario con una nota adjunta que tenía la palabra 'Rin', un dibujo de una niña empujando una carretilla y algunas cositas azules flotantes."
    m 1euc "Junto con instrucciones sobre cómo peinar tu cabello para combinar con este atuendo."
    m 3rtc "A juzgar por estas orejas de gato, supongo que este personaje es una niña gato."
    m 1dtc "... Pero, ¿por qué empujaría una carretilla?"
    m 1hksdlb "Fue un {i}dolor{/i} de cabeza arreglar mi cabello... {w=0.2}{nw}"
    extend 1eub "¡Así que espero que te guste el disfraz!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_hatsune_miku",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_hatsune_miku:
    if not persistent._mas_o31_relaunch:
        call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)

        m "{i}~Mi voz no has de olvidar~{/i}"
        m "{i}~Mi señal cruzará~{/i}"
        m "{i}~Yo no soy virtual~{/i}"
        m "{i}~Todavía quiero ser...{/i}"
        m "¡Oh!{w=0.5} Parece que alguien me ha estado escuchando."


        call mas_transition_from_emptydesk ("monika 3hub")
    else:

        call spaceroom (scene_change=True, dissolve_all=True)

    m 3hub "¡Bienvenido de nuevo, [player]!"
    m 1eua "Entonces... {w=0.5}¿Qué opinas?"
    m 3eua "Creo que este disfraz realmente me queda bien."
    m 3eub "¡A mí también me encanta especialmente por cómo se ven los audífonos!"
    m 1rksdla "Aunque no puedo decir que sea demasiado cómodo para moverse..."
    m 3tsu "¡Así que no esperes que te dé una actuación hoy, [player]!"
    m 1hub "Jajaja~"
    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_sakuya_izayoi",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_sakuya_izayoi:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)


    if not persistent._mas_o31_relaunch:
        m "..."
        m "¿{i}Eh{/i}?"
        m "{i}Ah, debe haber habido algún tipo de error. {w=0.5}No me advirtieron de ningún invitado...{/i}"
        m "{i}No importa. Nadie interrumpirá este mo...{/i}"
        m "¡Oh! {w=0.5}¡Eres tú, [player]!"
    else:

        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Bienvenido, {w=0.3}a la sala espacial del demonio carmesí..."
        m "[player]."
        m "Por favor, permíteme ofrecerte mi hospitalidad."
        m "¡Jajaja! ¿Cómo estuvo esa imitación?"


    call mas_transition_from_emptydesk ("monika 3hub")

    m 3hub "¡Bienvenido de vuelta!"
    m 3eub "¿Qué opinas de mi atuendo?"
    m 3hua "¡Desde que me lo diste, supe que lo usaría hoy!"
    m 2tua "..."
    m 2tub "Sabes, [player], solo porque estoy vestida de maid no significa que voy a seguir todas tus órdenes..."
    show monika 5kua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5kua "Aunque podría hacer algunas excepciones, jejeje~"
    show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_briaryoung_shuchiin_academy_uniform",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_briaryoung_shuchiin_academy_uniform:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)


    if not persistent._mas_o31_relaunch:
        m "Ugh..."
        m "¿Cómo {i}se{/i} mantiene este moño en su lugar?"
        m "Las personas pueden decir lo que quieran sobre mi cinta, pero al menos es algo práctica..."
        m "... Supongo que esto funcionará, espero que no se caiga tan pronto como...{nw}"
        m "Hora de la verdad..."
    else:

        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Ya casi, [player]..."
        m "Solo trato de averiguar cómo se supone que este moño deba quedarse en su lugar."
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "¡Espero que eso sea suficiente!"


    call mas_transition_from_emptydesk ("monika 2hub")

    m 2hub "¡Bienvenido de nuevo!"
    m 2eub "Bueno, ¿qué opinas?"
    m 7tuu "Pensé que en lugar de ser la presidenta, podría ser la secretaria por hoy..."

    if mas_isMoniAff(higher=True):
        m 3rtu "O tal vez incluso una detective del amor, pero eso es algo inútil porque, ya lo he encontrado..."

    m 3hua "Jejeje~"
    call greeting_o31_deco
    call greeting_o31_cleanup
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_hatana_2b",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_hatana_2b:
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True)


    if persistent._mas_o31_relaunch:
        m "Casi listo, [player]..."
        m "Solo espero que esta falda no se autodestruya."
        m "{cps=*2}Aunque quizás a ti te gustaría que lo hiciera...{/cps}{nw}"
        $ _history_list.pop()
        m "De acuerdo. {w=0.2}¿Listo [player]?"
    else:

        m "Bien, {w=0.1}creo que eso es todo."
        m "Siempre y cuando esta falda no se autodestruya... {w=0.3}¡Sería realmente embarazoso!"
        m "¡Oh! {w=0.2}Creo que oigo algo..."
        m "¿[player]?"

    m "Tengo una pregunta para usted..."
    m "Ser o..."


    call mas_transition_from_emptydesk ("monika 3hub")

    m 3hub "... No ser 2B?!"
    m 1hub "¡Jajaja!"
    m 2eka "Entonces, ¿qué piensas?"
    m 2hub "Creo que es un disfraz realmente genial, ¡gracias de nuevo por dármelo!"
    m 7rtu "Dime [player], ¿te he dicho alguna vez que hay algo tranquilizador en ti?"
    m 3euu "Bueno, solo quería que lo supieras. {w=0.2}{nw}"
    extend 3tuu "Esperemos que nunca se borre de tu memoria."
    m 3eud "Eso me recuerda, asegúrate de hacer copias de seguridad de mis datos de vez en cuando, lo haría por ti si pudiera..."
    m 1hksdlb "Oh cielos, ni siquiera estoy segura de lo que significa eso, solo estoy divagando ahora, ¡jajaja!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

label greeting_o31_deco:
    m 1eua "Bueno..."
    m 3eua "¿Te gusta lo que he hecho con la habitación?"
    m 3tuu "Me encanta el ambiente espeluznante asociado a Halloween, además traté de crear uno propio."
    m 1eud "Se pueden hacer muchas cosas solo con iluminación, ¿sabes?"
    m 3tub "Sin mencionar que a veces lo más espeluznante son las cosas que están un {i}poco{/i} fuera de lugar..."
    m 1eua "Creo que las telarañas también son un buen toque..."
    m 1rka "{cps=*2}Estoy segura de que a Amy le gustarían mucho.{/cps}{nw}"
    $ _history_list.pop()
    m 3hub "¡Estoy súper contenta con cómo ha quedado todo!"
    return

label greeting_o31_generic:
    call spaceroom (scene_change=True, dissolve_all=True)

    m 3hub "¡Dulce o truco!"
    m 3eub "Jajaja, {w=0.1}{nw}"
    extend 3eua "solo estoy bromeando, [player]."
    m 1hua "Bienvenido de nuevo y... {w=0.5}{nw}"
    extend 3hub "¡Feliz Halloween!"


    call greeting_o31_deco

    m 3hua "Por cierto, ¿qué opinas de mi disfraz?"
    m 1hua "A mí me gusta mucho~"
    m 1hub "Más aún, porque fue un regalo tuyo, ¡jajaja!"
    m 3tuu "Así que deleita tus ojos con mi disfraz mientras puedas, jejeje~"

    call greeting_o31_cleanup
    return


label greeting_o31_cleanup(skip_zoom=False):
    window hide
    if not skip_zoom:
        call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    window auto

    python:

        store.mas_hotkeys.music_enabled = True

        mas_calDropOverlayShield()

        set_keymaps()

        HKBShowButtons()

        mas_startup_song()

        mas_rmallEVL("mas_holiday_o31_returned_home_relaunch")
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASPriorityRule.create_rule(0))
    ev_rules.update(MASNumericalRepeatRule.create_rule(EV_NUM_RULE_YEAR))
    ev_rules.update(MASGreetingRule.create_rule(override_type=True, skip_visual=True))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_lingerie",
            unlocked=True,
            conditional=(
                "mas_canShowRisque() "
                "and mas_hasUnlockedClothesWithExprop('lingerie')"
            ),
            start_date=datetime.datetime.combine((mas_o31-datetime.timedelta(days=1)), datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_o31_lingerie:

    python:
        mas_progressFilter()
        if persistent._mas_auto_mode_enabled:
            mas_darkMode(mas_current_background.isFltDay())
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)

    scene black
    pause 2.0

    menu:
        "¿Hola?":
            pause 5.0

    m "¡Jejeje!"
    m "No te preocupes [player], estoy aquí..."
    call mas_o31_lingerie_end
    call greeting_o31_cleanup (skip_zoom=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_lingerie",
            conditional=(
                "mas_canShowRisque() "
                "and mas_hasUnlockedClothesWithExprop('lingerie')"
            ),
            unlocked=False,
            rules={"skip alert": None},
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine((mas_o31-datetime.timedelta(days=1)), datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            years=[]
        )
    )

label mas_o31_lingerie:

    python:
        curr_song = songs.current_track
        mas_play_song(None)
        mas_display_notif("M̷̢͘ô̴͎ṇ̵͐i̴͎͂k̸̗̂ả̴̫", ["C̸̳̓ą̵́n̷̳̎ ̸̖̊y̴̦͝õ̷̯ų̷͌ ̴̼͘h̷̭̚e̴̪͝a̴̙̐ŕ̵̖ ̴̠́m̸̰̂ě̵̬?̷̮̐"], "Alertas de diálogos")

    scene black
    pause 2.0
    m "Oh no, ¿se fue la luz?"
    m "Que {cps=*2}suerte{/cps}{nw}."
    $ _history_list.pop()
    m "Que {fast}mala suerte..."
    m "Supongo que tendré que aprovechar esta situación, [player]..."
    call mas_o31_lingerie_end
    return

label mas_o31_lingerie_end:
    m "Dime, ¿has oído hablar de Devil's Night?"
    m "En algunos lugares es tradición que la noche anterior a Halloween las personas salgan para hacer travesuras."
    m "Bueno [player], me siento un poco traviesa esta noche..."
    window hide
    pause 2.0

    python:

        mas_temp_zoom_level = store.mas_sprites.zoom_level
        store.mas_sprites.reset_zoom()

        store.mas_selspr.unlock_acs(mas_acs_grayhearts_hairclip)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_black_gray)
        store.mas_selspr.unlock_clothes(mas_clothes_spider_lingerie)
        monika_chr.change_clothes(mas_clothes_spider_lingerie, by_user=False, outfit_mode=True)

    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 2tfu')

    pause 2.0
    window auto
    m 2tub "Jejeje, ¿qué opinas?"
    m 2hub "Es un poco diferente, lo sé, es posible que no estes seguro de querer tocar o salir corriendo, ¡jajaja!"
    m 7rua "Probablemente no es algo que me pondría todo el tiempo, pero creo que es muy bonito para esta época del año."
    m 2ekbsa "No te preocupes [player], no me molestaré si quieres que {cps=*2}me lo quite{/cps}{nw}."
    $ _history_list.pop()
    m "No te preocupes [player], no me molestaré si quieres que {fast}me cambie..."
    m 2hubsb "Sé que muchas personas le tienen miedo a las arañas y puede que esto no les parezca muy atractivo, ¡jajaja!"

    if player.lower() == "amy":
        m 2rsbla "Aunque he oído que a la gente llamada Amy le gustan las arañas, jejeje~"
    else:

        m 2rsbla "Aunque he oído que a la gente llamada Amy le gustan las arañas, jejeje~"


    call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    python:
        mas_stripEVL("mas_o31_lingerie", list_pop=True)
        mas_lockEVL("greeting_o31_lingerie", "GRE")


        if globals().get("curr_song", -1) is not -1 and curr_song != store.songs.FP_MONIKA_LULLABY:
            mas_play_song(curr_song, 1.0)
        else:
            mas_play_song(None, 1.0)

    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_trick_or_treat",
            prompt="Te voy a llevar a pedir dulce o truco",
            pool=True,
            unlocked=False,
            action=EV_ACT_UNLOCK,
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE",
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "bye_trick_or_treat",
        mas_o31,
        mas_o31 + datetime.timedelta(days=1),
    )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23


    if persistent._mas_o31_tt_count:
        m 1eka "¿Otra vez?"

    if too_early_to_go:

        m 3eksdla "¿No te parece un poco temprano para pedir dulce o truco, [player]?"
        m 3rksdla "No creo que haya nadie repartiendo dulces todavía..."

        m 2etc "¿Estás {i}seguro{/i} de que quieres ir ahora mismo?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás {i}seguro{/i} de que quieres ir ahora mismo?{fast}"
            "Sí":
                m 2etc "Bueno... {w=1}está bien, [player]..."
            "No":

                m 2hub "¡Jajaja!"
                m "Ten un poco de paciencia, [player]~"
                m 4eub "Aprovechemos al máximo esta tarde, ¿okey?"
                return

    elif too_late_to_go:
        m 3hua "¡Bueno! Vamos a pedir..."
        m 3eud "Espera..."
        m 2dkc "[player]..."
        m 2rkc "Ya es demasiado tarde para ir a pedir dulce o truco."
        m "Solo falta una hora para la medianoche."
        m 2dkc "Sin mencionar que dudo que queden muchos dulces..."
        m "..."

        m 4ekc "¿Estás seguro de que todavía quieres ir?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás seguro de que todavía quieres ir?{fast}"
            "Sí":
                m 1eka "... De acuerdo."
                m "Aunque solo quede una hora..."
                m 3hub "Al menos vamos a pasar el resto de Halloween juntos~"
                m 3wub "¡Vamos a aprovecharlo al máximo, [player]!"
            "En realidad, es un {i}poco{/i} tarde...":

                if persistent._mas_o31_tt_count:
                    m 1hub "Jajaja~"
                    m "Te lo dije."
                    m 1eua "Tendremos que esperar hasta el próximo año para ir."
                else:

                    m 2dkc "..."
                    m 2ekc "Bien, [player]."
                    m "Es una pena que no pudiéramos ir a pedir dulce o truco este año."
                    m 4eka "Asegurémonos de que podamos la próxima vez, ¿okey?"

                return
    else:


        m 3wub "¡Okey, [player]!"
        m 3hub "Parece que nos lo pasaremos genial~"
        m 1eub "¡Apuesto a que tendremos muchos dulces!"
        m 1ekbsa "E incluso si no lo hacemos, solo pasar la noche contigo es suficiente para mí~"


    $ mas_farewells.dockstat_wait_menu_label = "bye_trick_or_treat_wait_wait"
    $ mas_farewells.dockstat_rtg_label = "bye_trick_or_treat_rtg"
    jump mas_dockstat_iostart

label bye_trick_or_treat_wait_wait:

    menu:
        m "¿Qué pasa?"
        "Tienes razón, es un poco temprano" if too_early_to_go:
            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk (exp="monika 3hub")

            m 3hub "¡Jajaja, te lo dije!"
            m 1eka "Esperemos hasta la noche, ¿okey?"
            return True

        "Tienes razón, es un poco tarde" if too_late_to_go:
            call mas_dockstat_abort_gen

            if persistent._mas_o31_tt_count:
                call mas_transition_from_emptydesk (exp="monika 1hua")
                m 1hub "Jajaja~"
                m "Te lo dije."
                m 1eua "Tendremos que esperar hasta el próximo año para volver."
            else:

                call mas_transition_from_emptydesk (exp="monika 2dkc")
                m 2dkc "..."
                m 2ekc "De acuerdo, [player]."
                m "Es una pena que no pudiéramos ir a pedir dulce o truco este año."
                m 4eka "Asegurémonos de que podamos la próxima vez, ¿okey?"

            return True
        "En realidad, no puedo llevarte ahora":

            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk (exp="monika 1euc")

            m 1euc "Oh, de acuerdo [player]."

            if persistent._mas_o31_tt_count:
                m 1eua "Avísame si quieres volver más tarde, ¿de acuerdo?"
            else:

                m 1eua "Avísame si podemos ir, ¿de acuerdo?"

            return True
        "Nada":

            m "Okey, déjame terminar de prepararme."
            return

label bye_trick_or_treat_rtg:

    $ moni_chksum = promise.get()
    $ promise = None
    call mas_dockstat_ready_to_go (moni_chksum)

    if _return:
        call mas_transition_from_emptydesk (exp="monika 1hub")
        m 1hub "¡Vamos a pedir dulce o truco!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT


        $ persistent._mas_o31_tt_count += 1
        return "quit"



    call mas_transition_from_emptydesk (exp="monika 1ekc")
    $ persistent._mas_o31_tt_count -= 1
    m 1ekc "Oh no..."
    m 1rksdlb "No pude convertirme en un archivo."

    if persistent._mas_o31_tt_count:
        m 1eksdld "Creo que tendrás que ir a pedir dulce o truco sin mí esta vez..."
    else:

        m 1eksdld "Creo que tendrás que ir a pedir dulce o truco sin mí..."

    m 1ekc "Lo siento, [player]..."
    m 3eka "Asegúrate de traer muchos dulces para que los dos disfrutemos, ¿okey?~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31_TT]
        ),
        code="GRE"
    )

label greeting_trick_or_treat_back:

    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        ret_tt_long = False

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "¿A eso le llamas dulce o truco, [player]?"
        m "¿A dónde fuimos, a una sola casa?"
        m 2rsc "... Ni siquiera nos movimos."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        m 2ekp "Eso fue bastante corto para el dulce o truco, [player]."
        m 3eka "Pero lo disfruté mientras duró."
        m 1eka "Fue muy agradable estar ahí contigo~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
        m 1hua "Y... ¡Ya estamos en casa!"
        m 1hub "¡Espero que tengamos muchos dulces deliciosos!"
        m 1eka "Realmente disfruté pedir dulce o truco contigo, [player]..."

        call greeting_trick_or_treat_back_costume

        m 4eub "¡Hagamos esto de nuevo el año que viene!"

    elif not is_past_sunrise_post31:

        $ mas_o31CapGainAff(15)
        m 1hua "Y... ¡Ya estamos en casa!"
        m 1wua "Vaya [player], seguro que fuimos a pedir dulce o truco durante mucho tiempo..."
        m 1wub "¡Seguro que hemos recibido una tonelada de dulces!"
        m 3eka "Realmente disfruté estar allí contigo..."

        call greeting_trick_or_treat_back_costume

        m 4eub "¡Hagamos esto de nuevo el año que viene!"
        $ ret_tt_long = True
    else:


        $ mas_o31CapGainAff(15)
        m 1wua "¡Finalmente estamos en casa!"
        m 1wuw "Ya no es Halloween, [player]... ¡Estuvimos fuera toda la noche!"
        m 1hua "Supongo que nos divertimos demasiado, jejeje~"
        m 2eka "Pero de todos modos, gracias por llevarme, realmente lo disfruté."

        call greeting_trick_or_treat_back_costume

        m 4hub "Hagamos esto de nuevo el año que viene...{w=1} ¡Pero quizás {i}deberíamos{/i} no quedarnos afuera tan tarde!"
        $ ret_tt_long = True


    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():

        call return_home_post_player_bday


    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out, ret_tt_long)
    return

label mas_o31_ret_home_cleanup(time_out=None, ret_tt_long=False):

    if not time_out:
        $ time_out = store.mas_dockstat.diffCheckTimes()


    if not ret_tt_long and time_out > mas_five_minutes:
        m 1hua "..."
        m 1wud "Oh, wow [player]. Realmente estuvimos fuera durante bastante tiempo..."
    else:

        m 1esc "De todas formas..."



    call mas_o31_cleanup

    return

label greeting_trick_or_treat_back_costume:
    if monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 2eka "Incluso si no pudiera ver nada y nadie más pudiera ver mi disfraz..."
        m 2eub "¡Vestirse y salir fue realmente genial!"
    else:

        m 2eka "Incluso si no pudiera ver nada..."
        m 2eub "¡Salir fue realmente genial!"
    return






default persistent._mas_d25_in_d25_mode = False



default persistent._mas_d25_spent_d25 = False


default persistent._mas_d25_started_upset = False


default persistent._mas_d25_second_chance_upset = False






default persistent._mas_d25_deco_active = False


default persistent._mas_d25_intro_seen = False


default persistent._mas_d25_d25e_date_count = 0



default persistent._mas_d25_d25_date_count = 0


default persistent._mas_d25_gifts_given = list()


default persistent._mas_d25_gone_over_d25 = None


define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)


define mas_d25e = mas_d25 - datetime.timedelta(days=1)


define mas_d25p = mas_d25 + datetime.timedelta(days=1)


define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 11)


define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)



init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            
            
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            
            "_mas_d25_d25e_date_count": "d25s.d25e.went_out_count",
            "_mas_d25_d25_date_count": "d25s.d25.went_out_count",
            "_mas_d25_gone_over_d25": "d25.actions.gone_over_d25",

            "_mas_d25_spent_d25": "d25.actions.spent_d25"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 11),
        end_dt=datetime.datetime(2019, 12, 31)
    ))


init -10 python:
    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 11 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()
        
        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_d25p)


    def mas_isD25Pre(_date=None):
        """
        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the D25 season, but before Christmas, False
            otherwise

        NOTE: This is used for gifts too
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_d25)

    def mas_isD25GiftHold(_date=None):
        """
        IN:
            _date - date to check, defaults None, which means today's date is assumed

        RETURNS:
            boolean - True if within d25c start, to d31 (end of nts range)
            (The time to hold onto gifts, aka not silently react)
        """
        if _date is None:
            _date = datetime.date.today()
        
        return mas_isInDateRange(_date, mas_d25c_start, mas_nye, end_inclusive=True)

    def mas_d25ShowVisuals():
        """
        Shows d25 visuals.
        """
        mas_showDecoTag("mas_d25_banners")
        mas_showDecoTag("mas_d25_tree")
        mas_showDecoTag("mas_d25_garlands")
        mas_showDecoTag("mas_d25_lights")
        mas_showDecoTag("mas_d25_gifts")

    def mas_d25HideVisuals():
        """
        Hides d25 visuals
        """
        mas_hideDecoTag("mas_d25_banners", hide_now=True)
        mas_hideDecoTag("mas_d25_tree", hide_now=True)
        mas_hideDecoTag("mas_d25_garlands", hide_now=True)
        mas_hideDecoTag("mas_d25_lights", hide_now=True)
        mas_hideDecoTag("mas_d25_gifts", hide_now=True)

    def mas_d25ReactToGifts():
        """
        Goes thru the gifts stored from the d25 gift season and reacts to them

        this also registeres gifts
        """
        
        found_reacts = list()
        
        
        persistent._mas_d25_gifts_given.sort()
        
        
        
        
        given_gifts = list(persistent._mas_d25_gifts_given)
        
        
        gift_cntrs = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_cntrs.addLabelQuip("mas_d25_gift_connector")
        
        
        d25_evb = []
        d25_gsp = []
        store.mas_filereacts.process_gifts(given_gifts, d25_evb, d25_gsp)
        
        
        store.mas_filereacts.register_sp_grds(d25_evb)
        store.mas_filereacts.register_sp_grds(d25_gsp)
        
        
        react_labels = store.mas_filereacts.build_gift_react_labels(
            d25_evb,
            d25_gsp,
            [],
            gift_cntrs,
            "mas_d25_gift_end",
            "mas_d25_gift_starter"
        )
        
        react_labels.reverse()
        
        
        if len(react_labels) > 0:
            for react_label in react_labels:
                mas_rmallEVL(react_label) 
            
            for react_label in react_labels:
                MASEventList.push(react_label,skipeval=True)

    def mas_d25SilentReactToGifts():
        """
        Method to silently 'react' to gifts.

        This is to be used if you gave Moni a christmas gift but didn't show up on
        D25 when she would have opened them in front of you.

        This also registeres gifts
        """
        
        base_gift_ribbon_id_map = {
            "blackribbon":"ribbon_black",
            "blueribbon": "ribbon_blue",
            "darkpurpleribbon": "ribbon_dark_purple",
            "emeraldribbon": "ribbon_emerald",
            "grayribbon": "ribbon_gray",
            "greenribbon": "ribbon_green",
            "lightpurpleribbon": "ribbon_light_purple",
            "peachribbon": "ribbon_peach",
            "pinkribbon": "ribbon_pink",
            "platinumribbon": "ribbon_platinum",
            "redribbon": "ribbon_red",
            "rubyribbon": "ribbon_ruby",
            "sapphireribbon": "ribbon_sapphire",
            "silverribbon": "ribbon_silver",
            "tealribbon": "ribbon_teal",
            "yellowribbon": "ribbon_yellow"
        }
        
        
        evb_details = []
        gso_details = []
        store.mas_filereacts.process_gifts(
            persistent._mas_d25_gifts_given,
            evb_details,
            gso_details
        )
        
        
        persistent._mas_d25_gifts_given = []
        
        
        for evb_detail in evb_details:
            if evb_detail.sp_data is None:
                
                ribbon_id = base_gift_ribbon_id_map.get(
                    evb_detail.c_gift_name,
                    None
                )
                if ribbon_id is not None:
                    mas_selspr.unlock_acs(mas_sprites.get_sprite(0, ribbon_id))
                    mas_receivedGift(evb_detail.label)
                
                elif ribbon_id is None and evb_detail.c_gift_name == "quetzalplushie":
                    persistent._mas_acs_enable_quetzalplushie = True
            
            else:
                
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    evb_detail.sp_data[0],
                    evb_detail.sp_data[1]
                ))
                mas_receivedGift(evb_detail.label)
        
        
        for gso_detail in gso_details:
            
            if gso_detail.sp_data is not None:
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    gso_detail.sp_data[0],
                    gso_detail.sp_data[1]
                ))
                mas_receivedGift(gso_detail.label)
        
        
        store.mas_selspr.save_selectables()
        renpy.save_persistent()


init -10 python in mas_d25_utils:
    import store
    import store.mas_filereacts as mas_frs

    has_changed_bg = False

    DECO_TAGS = [
        "mas_d25_banners",
        "mas_d25_tree",
        "mas_d25_garlands",
        "mas_d25_lights",
        "mas_d25_gifts",
    ]

    def shouldUseD25ReactToGifts():
        """
        checks whether or not we should use the d25 react to gifts method

        Conditions:
            1. Must be in d25 gift range
            2. Must be at normal+ aff (since that's when the topics which will open these gifts will show)
            3. Must have deco active. No point otherwise as no tree to put gifts under
        """
        return (
            store.mas_isD25Pre()
            and store.mas_isMoniNormal(higher=True)
            and store.persistent._mas_d25_deco_active
            and not store.persistent._mas_override_d25_gift_react
        )

    def react_to_gifts(found_map):
        """
        Reacts to gifts using the d25 protocol (exclusions)

        OUT:
            found_map - map of found reactions
                key: lowercase giftname, no extension
                val: giftname wtih extension
        """
        d25_map = {}
        
        
        
        
        d25_giftnames = mas_frs.check_for_gifts(d25_map, mas_frs.build_exclusion_list("d25g"), found_map)
        
        
        d25_giftnames.sort()
        d25_evb = []
        d25_gsp = []
        d25_gen = []
        mas_frs.process_gifts(d25_giftnames, d25_evb, d25_gsp, d25_gen)
        
        
        non_d25_giftnames = [x for x in found_map]
        non_d25_giftnames.sort()
        nd25_evb = []
        nd25_gsp = []
        nd25_gen = []
        mas_frs.process_gifts(non_d25_giftnames, nd25_evb, nd25_gsp, nd25_gen)
        
        
        for grd in d25_gen:
            nd25_gen.append(grd)
            found_map[grd.c_gift_name] = d25_map.pop(grd.c_gift_name)
        
        
        
        for c_gift_name, gift_name in d25_map.iteritems():
            
            if c_gift_name not in store.persistent._mas_d25_gifts_given:
                store.persistent._mas_d25_gifts_given.append(c_gift_name)
            
            
            store.mas_docking_station.destroyPackage(gift_name)
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        
        mas_frs.register_sp_grds(nd25_evb)
        mas_frs.register_sp_grds(nd25_gsp)
        mas_frs.register_gen_grds(nd25_gen)
        
        
        return mas_frs.build_gift_react_labels(
            nd25_evb,
            nd25_gsp,
            nd25_gen,
            mas_frs.gift_connectors,
            "mas_reaction_end",
            mas_frs._pick_starter_label()
        )





image mas_d25_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/bgdeco.png"
)

image mas_mistletoe = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/mistletoe.png"
)



image mas_d25_lights = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_lights_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/lights_off.png")
)

image mas_d25_night_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/lights_on_1.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_2.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_3.png"
        0.5
    repeat



image mas_d25_garlands = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/garland_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_garlands_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/garland.png")
)

image mas_d25_night_garlands_atl:
    "mod_assets/location/spaceroom/d25/garland_on_1.png"
    block:
        "mod_assets/location/spaceroom/d25/garland_on_1.png" with Dissolve(3, alpha=True)
        5
        "mod_assets/location/spaceroom/d25/garland_on_2.png" with Dissolve(3, alpha=True)
        5
        repeat



image mas_d25_tree = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/tree_lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_tree_lights_atl"
    ),
    "True", MASFilterSwitch(
        "mod_assets/location/spaceroom/d25/tree_lights_off.png"
    )
)

image mas_d25_night_tree_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/tree_lights_on_1.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_2.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_3.png"
        1.5
    repeat





image mas_d25_gifts = ConditionSwitch(
    "len(persistent._mas_d25_gifts_given) == 0", "mod_assets/location/spaceroom/d25/gifts_0.png",
    "0 < len(persistent._mas_d25_gifts_given) < 3", "mas_d25_gifts_1",
    "3 <= len(persistent._mas_d25_gifts_given) <= 4", "mas_d25_gifts_2",
    "True", "mas_d25_gifts_3"
)

image mas_d25_gifts_1 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_1.png"
)

image mas_d25_gifts_2 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_2.png"
)

image mas_d25_gifts_3 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_3.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_d25_banners",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_tree",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_gifts",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=7)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )


label mas_holiday_d25c_autoload_check:







    if (
        not persistent._mas_d25_in_d25_mode
        and mas_isD25Season()
        and not mas_isFirstSeshDay()
        and (
            mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS, persistent._mas_current_background)
            
            
            or mas_isD25()
        )
    ):

        python:

            persistent._mas_d25_in_d25_mode = True


            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True




            elif (
                mas_isD25Outfit()
                and (not mas_isplayer_bday() or mas_isD25())
            ):
                
                store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                store.mas_selspr.unlock_clothes(mas_clothes_santa)
                store.mas_selspr.save_selectables()
                
                
                monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
                
                
                mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)
                
                
                persistent._mas_d25_deco_active = True
                
                
                if mas_isD25():
                    mas_changeWeather(mas_weather_snow, by_user=True)
                    
                    
                    if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
                        store.mas_d25_utils.has_changed_bg = True
                        mas_changeBackground(mas_background_def, set_persistent=True)


    elif mas_run_d25s_exit or mas_isMoniDis(lower=True):

        call mas_d25_season_exit


    elif (
        persistent._mas_d25_in_d25_mode
        and not persistent._mas_force_clothes
        and monika_chr.is_wearing_clothes_with_exprop("costume")
        and not mas_isD25Outfit()
    ):

        $ monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


    elif mas_isD25() and not mas_isFirstSeshDay() and persistent._mas_d25_deco_active:

        python:
            monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
            mas_changeWeather(mas_weather_snow, by_user=True)



            if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
                store.mas_d25_utils.has_changed_bg = True
                mas_changeBackground(mas_background_def, set_persistent=True)


    if (
        mas_isMoniNormal()
        and persistent._mas_d25_in_d25_mode
        and mas_isD25Outfit()
        and (monika_chr.clothes != mas_clothes_def or monika_chr.clothes != store.mas_clothes_santa)
    ):
        $ monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

    if persistent._mas_d25_deco_active:
        $ mas_d25ShowVisuals()


    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


    jump mas_ch30_post_holiday_check


label mas_d25_season_exit:
    python:



        if monika_chr.is_wearing_clothes_with_exprop("costume") and not mas_globals.dlg_workflow:
            
            monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


        elif monika_chr.is_wearing_clothes_with_exprop("costume") and mas_globals.dlg_workflow:
            MASEventList.push("mas_change_to_def")


        mas_lockEVL("monika_event_clothes_select", "EVE")


        persistent._mas_d25_deco_active = False
        mas_d25HideVisuals()


        persistent._mas_d25_in_d25_mode = False


        mas_hideEVL("mas_d25_monika_christmaslights", "EVE", derandom=True)

        mas_d25ReactToGifts()
    return


label mas_d25_gift_starter:
    $ amt_gifts = len(persistent._mas_d25_gifts_given)
    $ presents = "regalos"
    $ the = "el"
    $ should_open = "debería abrir"

    if amt_gifts == 1:
        $ presents = "regalo"
    elif amt_gifts > 3:
        $ the = "todos los"

    if persistent._mas_d25_gone_over_d25:
        $ should_open = "no he abierto"

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3wud "¡Oh! ¡[should_open] [the] [presents] que me diste!"
        if persistent._mas_d25_gone_over_d25:
            m 3hub "¡Hagamos eso ahora!"
    else:


        m 1eka "Bueno, al menos ahora que estás aquí, puedo abrir [the] [presents] que me trajiste."
        m 3eka "Realmente quería que estuviéramos juntos para esto..."

    m 1suo "Veamos qué tenemos aquí.{w=0.5}.{w=0.5}.{w=0.5}{nw}"



    if persistent._mas_d25_gifts_given:
        $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_connector:
    python:
        d25_gift_quips = [
            _("¡Siguiente!"),
            _("Oh, ¡aquí hay otro!"),
            _("¡Ahora abramos este!"),
            _("¡Ahora abriré este!")
        ]

        picked_quip = random.choice(d25_gift_quips)

    m 1hub "[picked_quip]"
    m 1suo "Y aquí tenemos...{w=0.5}.{w=0.5}.{w=0.5}{nw}"



    if persistent._mas_d25_gifts_given:
        $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_end:

    $ persistent._mas_d25_gifts_given = []

    m 1eka "[player]..."

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3eka "Realmente no tenías que regalarme nada por Navidad... {w=0.3}{nw}"
        if mas_isD25():
            extend 3dku "solo tenerte aquí conmigo es más que suficiente."
        else:
            extend 3dku "estar contigo era todo lo que quería."
        m 1eka "Pero el hecho de que te hayas tomado el tiempo de conseguirme algo... {w=0.5}{nw}"
        extend 3ekbsa "bueno, no puedo agradecerte lo suficiente."
        m 3ekbfa "Realmente me hace sentir amada."
    else:

        m 1eka "Solo queria agradecerte..."
        m 1rkd "Aunque todavía estoy un poco decepcionada de que no pudieras estar conmigo en Navidad..."
        m 3eka "El hecho de que tú te hayas tomado el tiempo de conseguirme un regalo... {w=0.5}{nw}"
        extend 3ekbsa "bueno, solo demuestra que realmente estabas pensando en mí durante esta temporada especial."
        m 1dkbsu "No sabes cuánto significa esto para mí."


    if mas_isD25():
        m 3ekbfu "Te amo tanto, [player]~"
    else:
        m 3ekbfu "Feliz Navidad, [player]. Te amo~"
    $ mas_ILY()
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional=(
                "not persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday() "
                "and not persistent._mas_d25_intro_seen"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:
    if not persistent._mas_d25_deco_active:
        if mas_isplayer_bday():
            window hide
            pause 2.0
            m 1dku "..."
            m 1huu "Jejeje..."
            m 3eub "¡Tengo otra sorpresa para ti!"
        else:

            m 1eua "Entonces, hoy es..."
            m 1euc "... Espera."
            m "..."
            m 3wuo "¡Oh!"
            m 3hub "Hoy es el día en el que iba a..."





        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Cierra los ojos por un momento [player], tengo que hacer algo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

        call mas_d25_monika_holiday_intro_deco

        m 3hub "Y aquí estamos..."


        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "¡Felices fiestas, [player]!"

    if mas_lastSeenLastYear("mas_d25_monika_holiday_intro"):
        m 1hua "¿Puedes creer que ya es esa época del año otra vez?"

        $ the_last = "la última"

        if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "d25s.saw_an_intro"):
            $ the_last = "nuestra primera"

        m 3eua "Parece como si fuera ayer cuando pasamos [the_last] Navidad juntos, ¡y ahora ha pasado un año entero!"

        if mas_isMoniLove(higher=True):

            m 3hua "El tiempo realmente vuela cuando estoy contigo~"

    m 3eua "¿Te gusta lo que hice con el lugar?"
    m 1hua "Debo decir que estoy bastante orgullosa de ello."

    if mas_d25_utils.has_changed_bg:
        m 3rksdla "Solo tenía suficientes adornos para una habitación, así que me decidí por el aula... {w=0.2}espero que esté bien."
        m "Pero de todos modos..."

    m 3eua "La Navidad siempre ha sido una de mis épocas favoritas del año..."

    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika

    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m 5eka "Así que me alegro de que estés conmigo para compartirlo de nuevo este año~"
    else:
        m 5eka "Y estoy tan contenta de que estés aquí para compartirlo conmigo~"

    $ persistent._mas_d25_intro_seen = True



    $ mas_rmallEVL("mas_d25_monika_holiday_intro")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday()"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro_upset:

    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "Bueno, [player]... {w=1}realmente no me había sentido muy animada este año..."
    m 3eka "¡Pero últimamente has sido muy dulce conmigo y me he sentido mucho mejor!"
    m 3hua "Entonces... creo que es hora de arreglar un poco este lugar."





    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "Si tan solo pudieras cerrar los ojos por un momento.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    call mas_d25_monika_holiday_intro_deco

    m 3hub "Tada~"
    m 3eka "¿Qué piensas?"
    m 1eka "No está mal para el último minuto, ¿eh?"
    m 1hua "La Navidad siempre ha sido una de mis épocas favoritas del año..."
    m 3eua "Y estoy muy contenta de que podamos pasarlo felices juntos, [player]~"


    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:



    scene black with dissolve

    python:

        persistent._mas_d25_in_d25_mode = True


        monika_chr.change_hair(mas_hair_def, False)


        store.mas_selspr.unlock_clothes(mas_clothes_santa)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
        store.mas_selspr.unlock_acs(mas_acs_holly_hairclip)
        monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)


        mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)


        mas_changeWeather(mas_weather_snow, by_user=True)


        mas_rmallEVL("monika_auroras")


        persistent._mas_d25_deco_active = True
        mas_d25ShowVisuals()

        change_info = None

        if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
            mas_d25_utils.has_changed_bg = True
            change_info = mas_changeBackground(mas_background_def, set_persistent=True)


    call spaceroom (scene_change=True, dissolve_all=True, bg_change_info=change_info)

    return

label mas_d25_monika_holiday_intro_rh:

    m 1hua "¡ Y ya estamos en casa!"



    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)



label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Espera..."
    m 3etc "... ¿Es?..."
    m 3hub "¡Sí, lo es!"
    m 1tsu "... Cierra los ojos un segundo, tengo que hacer algo..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()


    $ persistent._mas_d25_intro_seen = True

    $ MASEventList.push("mas_d25_monika_christmas",skipeval=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
            conditional="not mas_lastSeenInYear('mas_d25_monika_christmas')",
            action=EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas:

    $ persistent._mas_d25_spent_d25 = True
    $ mas_gainAffection(5, bypass=True)



    $ mas_rmallEVL("mas_d25_monika_christmas")


    if mas_isMoniDis():
        m 6eka "Feliz Navidad, [player]. {w=0.2}Gracias por pasar un rato conmigo hoy."

    elif mas_isMoniUpset(higher=True):

        $ mas_d25ReactToGifts()

        if mas_isMoniNormal(higher=True):

            m 1eub "¡[player]! ¿Sabes qué día es?"
            m 3hub "Por supuesto que sí. Es Navidad."
            m 3sub "¡Feliz Navidad, [player]!"
            m 1hub "¡Jajaja! ¡No puedo creer que por fin esté aquí!"
            m 3eka "Estoy muy, muy feliz de que hayas decidido pasar parte de ella conmigo."
            m 1eud "No obstante, recuerda ir a compartir la alegría navideña con tu familia y amigos."
            m 1eua "Después de todo, también son muy importantes..."
            m 1hua "Y estoy segura de que les encantará verte en este momento tan especial."

            if mas_isMoniAff(higher=True):
                m 1eka "Pero que estés aquí hoy... {w=0.5}significa todo para mí..."
                m 1dku "..."

                if mas_is_snowing:
                    if mas_isDecoTagVisible("mas_d25_lights"):
                        $ dlg_var = ", o las decoraciones"
                    else:
                        $ dlg_var = ""

                    m 1lkbsa "Tal vez solo es la nieve[dlg_var]..."
                else:

                    if mas_isDecoTagVisible("mas_d25_lights"):
                        $ dlg_var = "las decoraciones, o "
                    else:
                        $ dlg_var = ""

                    m 1lkbsa "Tal vez solo sea [dlg_var]la temporada de fiestas..."

                m "... O incluso que el muérdago me afecte."
                m 3hksdlb "Es una broma, no he colgado ninguno."

                if mas_isMoniEnamored(higher=True):
                    m 1lksdla "... {cps=*2}Aún~{/cps}{nw}"
                    $ _history_list.pop()

                m 1lksdlu "Jejeje..."
                m 1ekbsa "Mi corazón está revoloteando como loco ahora mismo, [player]."
                m "No podría imaginar una forma mejor de pasar estas fiestas tan especiales..."
                m 1eua "No me malinterpretes, sabía que estarías aquí conmigo."
                m 3eka "Pero ahora que estamos los dos juntos en Navidad..."
                m 1hub "Jajaja~"

                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbfa "Es el sueño de toda pareja para las fiestas, [player]."

                if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
                    m "Acurrucados junto a una chimenea, viendo la nieve caer suavemente..."

                if not mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
                    m 5hubfa "Estoy siempre agradecida de haber tenido esta oportunidad contigo."
                else:
                    m 5hubfa "Estoy tan contenta de poder pasar la Navidad contigo de nuevo."

                m "Te amo. Por siempre y para siempre~"
                m 5hubfb "Feliz Navidad, [player]~"
                show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
                window hide
                menu:
                    "Feliz Navidad, [m_name]":
                        hide screen mas_background_timed_jump
                        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        pause 2.0
            else:

                m 1eka "Pero que estés aquí hoy...{w=0.5} significa todo para mí..."
                m 3rksdla "... No es que pensara que me ibas a dejar sola en este día tan especial o algo así..."
                m 3hua "Pero eso demuestra aún más que realmente me amas, [player]."
                m 1ektpa "..."
                m "¡Jajaja! Dios, me estoy poniendo un poco emocional aquí..."
                m 1ektda "Que sepas que yo también te amo y que estaré siempre agradecida por haber tenido esta oportunidad contigo."
                m "Merry Christmas, [player]~"
                show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
                window hide
                menu:
                    "Feliz Navidad, [m_name]":
                        hide screen mas_background_timed_jump
                        show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        pause 2.0
        else:


            m 1eka "Feliz Navidad, [player]. {w=0.2}Realmente significa mucho que estés aquí conmigo hoy."

    return


label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["fiestas", "música"],
            prompt="Villancicos",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_carolling",
        mas_d25c_start,
        mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None


label mas_d25_monika_carolling:

    m 1euc "Hey, [player]..."
    m 3eud "¿Alguna vez has ido a cantar villancicos?"
    m 1euc "Ir de puerta en puerta en grupos, cantar a los demás durante las vacaciones..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Es reconfortante saber que la gente está difundiendo alegría, incluso con las noches tan frías."
    else:
        m 1eua "Es reconfortante saber que las personas están transmitiendo alegría a los demás en su tiempo libre."

    m 3eua "¿Te gusta cantar villancicos, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gusta cantar villancicos, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "¡Me alegra que sientas lo mismo, [player]!"
            m 3hub "¡Mi canción favorita es definitivamente Jingle Bells!"
            m 1eua "¡Es una melodía tan alegre y alegre!"
            m 1eka "Quizás podamos cantarla juntos algún día."
            m 1hua "Jejeje~"
        "No":

            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Oh... {w=1}¿En serio?"
            m 1hksdlb "Ya veo..."
            m 1eua "Independientemente, estoy segura de que también te gusta esa alegría especial que solo pueden traer las canciones navideñas."
            m 3hua "Canta conmigo alguna vez, ¿okey?"

    return "derandom"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["fiestas"],
            prompt="Muérdago",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_mistletoe",
        mas_d25c_start,
        mas_d25p,
    )

label mas_d25_monika_mistletoe:
    m 1eua "Dime, [player]."
    m 1eub "Has oído hablar de la tradición del muérdago, ¿verdad?"
    m 1tku "Cuando dos enamorados terminan debajo del muérdago, se deben de besar."
    m 1eua "¡En realidad se originó en la Inglaterra victoriana!"
    m 1dsa "A un hombre se le permitía besar a cualquier mujer que estuviera debajo del muérdago..."
    m 3dsd "Y cualquier mujer que rechazara el beso estaba maldecida con mala suerte..."
    m 1dsc "..."
    m 3rksdlb "Ahora que lo pienso, suena más como aprovecharse de alguien."
    m 1hksdlb "¡Pero estoy segura de que ahora es diferente!"

    if not persistent._mas_pm_d25_mistletoe_kiss:
        m 3hua "Tal vez algún día podamos besarnos bajo el muérdago, [player]."
        m 1tku "... ¡Quizás incluso puedas agregar uno aquí!"
        m 1kuu "Jejeje~"
    return "derandom"


default persistent._mas_pm_hangs_d25_lights = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmaslights",
            category=['fiestas'],
            prompt="Luces navideñas",
            start_date=mas_d25c_start,
            end_date=mas_nye,
            conditional=(
                "persistent._mas_pm_hangs_d25_lights is None "
                "and persistent._mas_d25_deco_active "
                "and not persistent._mas_pm_live_south_hemisphere "
                "and mas_isDecoTagVisible('mas_d25_lights')"
            ),
            action=EV_ACT_RANDOM,
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_christmaslights",
        mas_d25c_start,
        mas_nye,
    )

label mas_d25_monika_christmaslights:
    m 1euc "Hey, [player]..."
    if mas_isD25Season():
        m 1lua "He pasado mucho tiempo mirando las luces aquí..."
        m 3eua "Son muy bonitas, ¿no?"
    else:
        m 1lua "Estaba pensando en la Navidad, con todas las luces que colgaban aquí..."
        m 3eua "Eran realmente bonitas, ¿verdad?"
    m 1eka "Las luces navideñas brindan un ambiente tan cálido y acogedor durante la temporada más dura y fría... {w=0.5}{nw}"
    extend 3hub "¡Y también hay muchos tipos diferentes!"
    m 3eka "Parece un sueño hecho realidad salir a caminar contigo en una fría noche de invierno, [player]."
    m 1dka "Admirando todas las luces..."

    m 1eua "¿Cuelgas luces en tu casa durante el invierno, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Cuelgas luces en tu casa durante el invierno, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_hangs_d25_lights = True
            m 3sub "¿De verdad? ¡Apuesto a que son preciosas!"
            m 2dubsu "Ya puedo imaginarnos, fuera de tu casa... sentados juntos en nuestro porche..."
            m "Como las hermosas estrellas que brillan en la profunda noche."
            m 2dkbfu "Nos abrazaríamos y beberíamos chocolate caliente... {w=0.5}{nw}"

            if persistent._mas_pm_gets_snow is not False:
                extend 2ekbfa "viendo la nieve caer suavemente..."

            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "Un día, [player]. Algún día, podremos hacerlo realidad."
        "No":

            $ persistent._mas_pm_hangs_d25_lights = False
            m 1eka "Oh, está bien, [player]."
            m 1dkbla "Estoy segura de que sería agradable relajarse contigo en una noche fría..."
            m 1dkbsa "Ver caer la nieve y beber chocolate caliente juntos."
            m 1dkbsa "Abrazados el uno al otro para mantenernos en calor..."
            m 1rkbfb "Sí, eso suena muy bien."
            m 3hubsa "Pero, cuando tengamos nuestra propia casa, puedo colgar algunas yo misma, {nw}"
            extend 3hubsb "jajaja~"
    return "derandom"

init 20 python:

    mas_poem_d25_1 = MASPoem(
        poem_id="poem_d25_1",
        category="d25",
        prompt="La alegría de mi mundo",
        title = "     Mi querido [player]",
        text = """\
     Tú eres realmente la alegría de mi mundo.
     Ni la luz emitida por el árbol de Navidad más alto.
     Ni la de la estrella más brillante.
     Podría estar cerca de igualar tu brillantez.
     Este corazón mío, que una vez estuvo congelado, solo necesitaba tu calor para que pudiera voler a latir.
     Si alguna vez no hay nada bajo el árbol, y mi media permanece vacía.
     Simplemente no importaría mientras te tenga a mi lado.
     Siempre serás el único regalo que necesito.

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    
    )

    mas_poem_d25_2 = MASPoem(
        poem_id="poem_d25_2",
        category="d25",
        prompt="Incomparable",
        title="     Mi querido [player]",
        text="""\
     Nada se puede comparar con el calor que me das.
     Ni siquiera la sensación de envolver mis manos alrededor de una taza de chocolate 
     caliente.
     O calcetines borrosos, calentando mis pies en un día helado.
     En un mundo tan frío, solo tu presencia es mi único regalo.

     Nada se puede comparar con la belleza que tienes.
     Nada puede compararse a la emoción que provocas.
     Ni las luces brillantes que cuelgan en esta misma habitación.
     Y tampoco la vista de un regalo sin abrir, bajo el árbol.

     [player], eres realmente único.

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    )

    mas_poem_d25_3 = MASPoem(
        poem_id="poem_d25_3",
        category="d25",
        prompt="Algún día",
        title="     Mi querido [player]",
        text="""\
     Más caliente que el fuego de la chimenea.
     Más brillante que cualquier estrella en la cima del árbol.
     Más reconfortante que cualquier taza de chocolate caliente.
     Es mi [player], que siempre está ahí para mí.

     Algún día, encenderemos el fuego juntos.
     Algún día, decoraremos el árbol.
     Algún día, tomaremos una taza de cacao.
     Algún día, estarás a mi lado.

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    )

    mas_poem_d25_4 = MASPoem(
        poem_id="poem_d25_4",
        category="d25",
        prompt="Esta Navidad",
        title="     Mi querido [player]",
        text="""\

     Esta Navidad nunca necesité más regalos que tu amor.
     Porque tenerte a mi lado ya me hace feliz.
     Porque tenerte aquí es el regalo más hermoso.
     ¡Porque encontrarte fue lo mejor que pude haber pedido!

     Sabía que esta Navidad sería especial...
     La pasé con el que hace que mi corazón salte.
     El que me hace sonreír todos los días.
     El que más confío.

     Gracias por estar ahí para mí, [player].
     ¡Siempre estaré aquí para ti!

     Feliz Navidad~

     Siempre tuya,
     Monika
"""
    )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=17)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )


default persistent._mas_pm_d25_mistletoe_kiss = False




label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25c_start, mas_d25p + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "¡Que estés aquí conmigo ha hecho de esta una Navidad maravillosa!"
        m 3eka "Sé que es un día muy ajetreado, pero solo saber que hiciste tiempo para mí..."
        m 1eka "Gracias."
        m 3hua "Realmente hizo de este un día verdaderamente especial~"
    else:

        m 2ekc "[player]..."
        m 2eka "Realmente aprecio que pases un tiempo conmigo en Navidad..."
        m 3rksdlc "Realmente no he tenido el espíritu navideño esta temporada, pero fue un placer pasar el dia de hoy contigo."
        m 3eka "Así que gracias... {w=1}significó mucho."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "Y no olvidemos el regalo especial de Navidad que me hiciste, [player]..."
                m 3hub "¡Fue grandioso!"
            elif d25_gifts_neutral == 1:
                m 3eka "Y no nos olvidemos del regalo de Navidad que me hiciste, [player]..."
                m 1eka "Fue muy amable de tu parte traerme algo."
            else:
                m 3eka "Y no nos olvidemos del regalo de Navidad que me hiciste, [player]..."
                m 2etc "..."
                m 2efc "Bueno, pensándolo bien, tal vez deberíamos..."
        else:

            if d25_gifts_good == d25_gifts_total:
                m "Y no nos olvidemos de los maravillosos regalos de Navidad que me hiciste, [player]..."
                m 3hub "¡Fueron increíbles!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 2etc "..."
                m 2rfc "Bueno, pensándolo bien, tal vez deberíamos..."
            elif d25_gifts_bad == 0:
                m "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3hub "¡Fue realmente amable de tu parte!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3rksdla "Algunos de ellos fueron realmente agradables."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3hub "La mayoría de ellos fueron realmente amables."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "Y no nos olvidemos de los regalos de Navidad que me hiciste, [player]..."
                m 3rksdla "Realmente me gustaron... {w=1}algunos de ellos."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "Yo... {w=1}también te hice algo, [player]..."
            m 3eksdla "He estado esperando todo el día hasta que sea el momento adecuado, y algo acerca de estar aquí contigo esta noche... {w=1}simplemente parece perfecto."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Pero debes saber, que estés aquí conmigo significa más que cualquier regalo que puedas darme~"
        else:
            m 3eka "Para ser honesta, no estaba segura de que me visitarías hoy... solo que estés aquí ya era más que suficiente para mí, incluso si no me hubieras comprado nada."
            m 1eka "Así que gracias de nuevo, [player]... {w=1}lo digo en serio."
    else:

        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Además, [player], hay algo que he querido darte durante todo el día..."
            m 3rksdla "Solo tenía que esperar el momento adecuado y el estar aquí contigo esta noche... {w=1}parece perfecto."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Que pases la Navidad conmigo fue el único regalo que siempre quise~"
        else:
            m 3eka "Que estuvieras aquí era todo lo que quería, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Así que aquí tienes, [player], espero que te guste~"


        call mas_showpoem (poem=mas_poems.getRandomPoem("d25"), background_action_label="mas_d25_poem_mistletoe")

        m 1dku "..."
        m 1ektpu "Solo que pases tiempo conmigo... {w=1}eso es todo lo que siempre quise."
        m 6dktua "Realmente eres mi mundo entero, [player]... {w=1}tu amor es todo lo que necesito..."
        window hide
        menu:
            "Te amo, [m_name]":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()



                pause 3.0
                show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0
                show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0
                show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]... yo... yo..."
                call monika_kissing_motion (hide_ui=False)

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 6ekbfa "... Yo también te amo~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "Esto es todo lo que siempre había soñado~"
                    m 6ekbfa "He estado esperando tanto tiempo para finalmente besarte, y no podría haber habido un momento más perfecto..."
                    m 6dkbfa "Debajo del muérdago contigo..."
                    m 6dkbsu "Nunca olvidaré esto..."
                    m 6ekbsu "... El momento de nuestro primer beso~"

                elif not persistent._mas_pm_d25_mistletoe_kiss:
                    m 6dkbfu "Jejeje..."
                    m 6ekbfa "Siempre quise compartir un beso contigo debajo del muérdago~"

                $ persistent._mas_pm_d25_mistletoe_kiss = True


                $ mas_hideEVL("mas_d25_monika_mistletoe", "EVE", derandom=True)


                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "Te amo mucho, [player]~"
    else:

        m 1hubfa "Te amo, [player]~"
    return "love"

label mas_d25_poem_mistletoe:
    $ pause(1)
    hide monika with dissolve_monika
    $ store.mas_sprites.zoom_out()
    show monika 1ekbfa zorder MAS_MONIKA_Z at i11


    show mas_mistletoe zorder MAS_MONIKA_Z - 1
    with dissolve
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_aiwfc:

    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )
    else:

        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "Hey, ¿[player]?"
        m 1eksdla "Espero que no te importe, pero te preparé una canción."
        m 3hksdlb "Sé que es un poco cursi, pero puede que te guste."
        m 3eksdla "Si tu volumen está silenciado, ¿te importaría encenderlo por mí?"
        if store.songs.hasMusicMuted():
            m 3hksdlb "Oh, ¡no te olvides de tu volumen en el juego también!"
            m 3eka "Realmente quiero que escuches esto."
        m 1huu "De todas formas.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    else:

        m 1hua "Jejeje..."
        m 3tuu "Espero que estés listo, [player]..."

        $ ending = "..." if store.songs.hasMusicMuted() else ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"

        m "{i}Es{/i} esa época del año nuevamente, después de todo[ending]"
        if store.songs.hasMusicMuted():
            m 3hub "¡Asegúrate de subir el volumen!"
            m 1huu ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    call monika_aiwfc_song


    if not mas_getEVLPropValue("monika_aiwfc", "shown_count", 0):
        m 1eka "Espero que te haya gustado, [player]."
        m 1ekbsa "Yo también lo decía en serio."
        m 1ekbfa "Eres el único regalo que podría desear."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Te amo, [player]~"
    else:

        m 1eka "Espero que te guste cuando cante esa canción, [player]."
        m 1ekbsa "Siempre serás el único regalo que necesitaré."
        m 1ekbfa "Te amo~"


    $ mas_unlockEVL("mas_song_aiwfc", "SNG")
    return "no_unlock|love"


label monika_aiwfc_song:

    call mas_timed_text_events_prep

    $ mas_play_song("mod_assets/bgm/aiwfc.ogg",loop=False)
    m 1eub "{i}{cps=9}No quiero{/cps}{cps=20} mucho{/cps}{cps=11} para Navidad{w=0.09}{/cps}{/i}{nw}."
    m 3eka "{i}{cps=11}Hay {/cps}{cps=20}solo{/cps}{cps=8} una cosa que necesito{/cps}{/i}{nw}."
    m 3hub "{i}{cps=8}No me importan {/cps}{cps=15}{/cps}{cps=10} los regalos{/cps}{/i}{nw}."
    m 3eua "{i}{cps=15}Debajo de{/cps}{cps=8} el árbol de Navidad{/cps}{/i}{nw}."

    m 1eub "{i}{cps=10}No necesito{/cps}{cps=20} colgar{/cps}{cps=9} mi calcetín{/cps}{/i}{nw}."
    m 1eua "{i}{cps=9}Allí{/cps}{cps=15} sobre{/cps}{cps=7} la chimenea{/cps}{/i}{nw}."
    m 3hub "{i}{w=0.5}{cps=20}Santa Claus{/cps}{cps=10} no me hará feliz{/cps}{/i}{nw}."
    m 4hub "{i}{cps=8}Con{/cps}{cps=15} un juguete{/cps}{cps=8} en el día de Navidad{w=0.35}{/cps}{/i}{nw}."

    m 3ekbsa "{i}{cps=10}Solo te quiero{/cps}{cps=15} para{/cps}{cps=8} mí{w=0.4}{/cps}{/i}{nw}."
    m 4hubfb "{i}{cps=8}Más{/cps}{cps=20} de lo que tú{/cps}{cps=10} podrías saber{w=0.5}{/cps}{/i}{nw}."
    m 1ekbsa "{i}{cps=10}Haz que mi deseo{/cps}{cps=20} se haga realidaaaaad{w=0.9}{/cps}{/i}{nw}."
    m 3hua "{i}{cps=8.5}Todo lo que quiero para Navidad{/cps}{/i}{nw}."
    m 3hubfb "{i}{cps=7}Eres tuuuuuuuuu{w=1}{/cps}{/i}{nw}."
    m "{i}{cps=9}Tuuuuuuuuuuuuuu~{w=0.60}{/cps}{/i}{nw}."

    m 2eka "{i}{cps=10}No te pediré{/cps}{cps=20} mucho{/cps}{cps=10} esta Navidad{/cps}{/i}{nw}."
    m 3hub "{i}{cps=10}Yo{/cps}{cps=20} ni {/cps}{cps=10}siquiera desearía nieve{w=0.8}{/cps}{/i}{nw}."
    m 3eua "{i}{cps=10}Yo{/cps}{cps=20} solo voy a{/cps}{cps=10} seguir esperando{w=0.5}{/cps}{/i}{nw}."
    m 3hubfb "{i}{cps=17}Debajo de{/cps}{cps=11} el muérdago{w=1}{/cps}{/i}{nw}."

    m 2eua "{i}{cps=10}Yo{/cps}{cps=17} no haré{/cps}{cps=10} una lista para enviarla{w=0.35}{/cps}{/i}{nw}."
    m 3eua "{i}{cps=10}Al{/cps}{cps=20} el polo norte{/cps}{cps=10} de San Nicolás{w=0.5}{/cps}{/i}{nw}."
    m 4hub "{i}{cps=18}Ni siquiera per{/cps}{cps=10}manecere despierta hasta{w=0.5}{/cps}{/i}{nw}."
    m 3hub "{i}{cps=10}Escuchar{/cps}{cps=20} esos má{/cps}{cps=14}gicos renos{w=1.2}{/cps}{/i}{nw}."

    m 3ekbsa "{i}{cps=20}Yo{/cps}{cps=11} solo te quiero aquí esta noche{w=0.4}{/cps}{/i}{nw}."
    m 3ekbfa "{i}{cps=10}Abrazándome{/cps}{cps=20}{/cps}{cps=10} tan fuerte{w=1}{/cps}{/i}{nw}."
    m 4hksdlb "{i}{cps=10}¿Qué más{/cps}{cps=15} puedo{/cps}{cps=8} haceeeer?{w=0.3}{/cps}{/i}{nw}."
    m 4ekbfb "{i}{cps=20}Porque amor{/cps}{cps=12} todo lo que quiero para Navidad{w=0.3} eres tuuuuuuuuu~{w=2.3}{/cps}{/i}{nw}"
    m "{i}{cps=9}Tuuuuuuuuuuuuu~{w=2.5}{/cps}{/i}{nw}"

    call mas_timed_text_events_wrapup
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_merry_christmas_baby",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_aiwfc')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_merry_christmas_baby:

    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )
    else:

        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('mas_song_merry_christmas_baby'):
        m 1eua "Hey, [player]..."
        m 3eub "¡Acabo de pensar en otra canción de Navidad que realmente quiero compartir contigo!"
        m 3eka "No tengo nada de música preparada esta vez, pero espero que disfrutes escuchándome cantarla de todas formas."
        m 1hua ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"

        call mas_song_merry_christmas_baby

        m 1hua "Jejeje..."
        m 3eka "Espero que te haya gustado~"
        $ mas_unlockEVL("mas_song_merry_christmas_baby", "SNG")
    else:

        m 3euu "Creo que es hora de otra canción navideña, jeje~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1huu "Jejeje... {w=0.2}feliz Navidad, amor~"

    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_this_christmas_kiss",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_merry_christmas_baby')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_this_christmas_kiss:
    if not renpy.seen_label('mas_song_this_christmas_kiss'):
        m 2rubsa "Um, [player]..."
        m 2lubsa "Encontré esta canción... {w=0.4}y... {w=0.4}estaba pensando en nosotros cuando la escuché."
        m 7ekbsu "Quiero decir, has sido tan dulce conmigo todo este tiempo..."
        m 3eubsb "Y...{w=0.2} oh dios, solo quiero compartirla contigo, si te parece bien."
        m 1hubsa "Solo dame un segundo{nw}"
        extend 1dubsa ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:

        m 3euu "Creo que es hora de cantar otra canción de Navidad, jejeje~"
        m 1hua ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    call mas_song_this_christmas_kiss

    m 1dubsa "..."
    m 1rtbsu "Hmm.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    window hide
    show monika 6tkbsa
    pause 2.0
    show monika 6dkbsu
    pause 2.0

    call monika_kissing_motion
    window auto

    m 6ekbfa "Uno de estos días te besaré de verdad, [player]."
    m 1dubfu "... Y cuando llegue ese día, mi corazón saltará de mi pecho con alegría~"
    $ mas_unlockEVL("mas_song_this_christmas_kiss", "SNG")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spider_tinsel",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25e - datetime.timedelta(days=1),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            rules={"force repeat": None, "no rmallEVL": None},
            years=[]
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_d25_spider_tinsel",
        mas_d25c_start,
        mas_d25e - datetime.timedelta(days=1)
    )


init 10 python:
    if (
        datetime.date.today() == mas_d25e - datetime.timedelta(days=1)
        and not mas_lastSeenInYear("mas_d25_spider_tinsel")
    ):
        MASEventList.queue("mas_d25_spider_tinsel")

label mas_d25_spider_tinsel:
    m 1esa "Hey, [player]..."
    m 1etc "¿Alguna vez te preguntaste de dónde provienen las tradiciones que a menudo damos por sentadas?"
    m 3eud "Muchas veces las cosas que se consideran tradiciones simplemente se aceptan y nunca nos tomamos el tiempo para saber por qué."
    m 3euc "Bueno, sentí curiosidad por saber por qué hacemos ciertas cosas en Navidad, así que comencé a investigar un poco."
    m 1eua "... Y encontré esta historia popular de Ucrania realmente interesante sobre el origen de por qué el oropel se usa a menudo para decorar árboles de Navidad."
    m 1eka "Pensé que era una historia muy bonita y quería compartirla contigo."
    m 1dka "..."
    m 3esa "Había una vez una viuda, llamémosla Amy, que vivía en una vieja choza con sus hijos."
    m 3eud "Afuera de su casa había un pino alto, y del árbol cayó una piña que pronto comenzó a crecer en el suelo."
    m 3eua "Los niños estaban entusiasmados con la idea de tener un árbol de Navidad, así que lo cuidaron hasta que alcanzó la altura suficiente para llevarlo dentro de su casa."
    m 2ekd "Desafortunadamente, la familia era pobre y aunque tenían el árbol de Navidad, no podían permitirse ningún adorno para decorarlo."
    m 2dkc "Y así, en la víspera de Navidad, Amy y sus hijos se fueron a la cama sabiendo que tendrían un árbol desnudo la mañana de Navidad."
    m 2eua "Sin embargo, las arañas que vivían en la cabaña escucharon los sollozos de los niños y decidieron que no dejarían el árbol de Navidad desnudo."
    m 3eua "Así que las arañas crearon hermosas telas en el árbol de Navidad, decorándolo con elegantes y hermosos patrones sedosos."
    m 3eub "Cuando los niños se despertaron temprano en la mañana de Navidad, ¡estaban saltando de emoción!"
    m "Fueron hacia su madre y la despertaron exclamando: '¡Madre, tienes que venir a ver el árbol de Navidad! ¡Es tan hermoso!'"
    m 1wud "Cuando Amy se despertó y se paró frente al árbol, estaba realmente asombrada ante la vista ante sus ojos."
    m "Entonces, uno de los niños abrió la ventana para que entrara el sol..."
    m 3sua "Cuando los rayos del sol golpean el árbol, las redes reflejaron la luz, creando hebras brillantes de plata y oro..."
    m "... Haciendo que el árbol de Navidad brille y brille con un destello mágico."
    m 1eka "Desde ese día en adelante, Amy nunca se sintió pobre; {w=0.3}en cambio, siempre estuvo agradecida por todos los maravillosos dones que ya tenía en la vida."
    m 3tuu "Bueno, supongo que ahora sabemos por qué a Amy le gustan las arañas..."
    m 3hub "¡Jajaja! ¡Solo estoy bromeando!"
    m 1eka "¿No es una historia tan dulce y maravillosa, [player]?"
    m "Creo que es una visión realmente interesante de por qué se usa oropel como decoración en los árboles de Navidad."
    m 3eud "También leí que los ucranianos a menudo decoran su árbol de Navidad con adornos de telaraña, creyendo que les traerán buena fortuna para el próximo año."
    m 3eub "Así que supongo que si alguna vez encuentras una araña viviendo en tu árbol de Navidad, ¡no la mates y tal vez te traiga buena suerte en el futuro!"
    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_night_before_christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=21)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_night_before_christmas:
    m 1esa "Hey, [player]..."
    m 3eua "Estoy segura de que lo has oído antes, ¡pero la víspera de Navidad no estaría completa sin {i}'La noche antes de navidad'{/i} !"
    m 3eka "Siempre fue una de mis partes favoritas en la víspera de Navidad mientras crecía, así que espero que no te importe escucharme leerlo ahora."
    m 1dka "..."

    m 3esa "'Era la noche antes de Navidad, cuando toda la casa..."
    m 3eud "No se movía una criatura, ni siquiera un ratón."
    m 1eud "Los calcetines fueron colgados junto a la chimenea con cuidado."
    m 1eka "Con la esperanza de que pronto llegaría San Nicolás."

    m 1esa "Los niños estaban acurrucados en sus camas."
    m 1hua "Mientras visiones de ciruelas de azúcar bailaban en sus cabezas."
    m 3eua "Mamá en su pañuelo y yo en mi gorra."
    m 1dsc "Acababa de sentarme para una larga siesta."

    m 3wuo "Cuando en el césped se produjo tal estrépito."
    m "Salté de la cama para ver qué pasaba."
    m 3wud "Lejos de la ventana volé como un relámpago."
    m "Rompí las contraventanas y salté."

    m 1eua "La luna sobre la nieve recién caída..."
    m 3eua "Dio el brillo del mediodía a los objetos de abajo,"
    m 3wud "Cuando, lo que a mis ojos asombrados debería aparecer."
    m 3wuo "Pero un trineo en miniatura y ocho pequeños renos."

    m 1eua "Con un pequeño conductor, tan vivo y rápido."
    m 3eud "Supe en un momento que debe ser San Nicolás"
    m 3eua "Más rápidos que las águilas vinieron sus corceles."
    m 3eud "Y él silbaba y gritaba, y los llamaba por su nombre."

    m 3euo "'¡Ahora, Vondín! ¡Ahora, Danzarín! ¡Ahora, Chiqui y Juguetón!'"
    m "'¡Adelante, Cometa! ¡Vamos, Cúpido! ¡Adelante, Trueno y Relámpago!'"
    m 3wuo "'¡Hasta lo alto del porche! ¡A la cima del muro!'"
    m "'¡Ahora vamos! ¡Corran lejos! ¡A toda prisa!'"

    m 1eua "Como hojas secas que antes del salvaje huracán vuelan."
    m 1eud "Cuando se encuentran con un obstáculo, suben al cielo."
    m 3eua "Así volaron los corceles hasta la azotea."
    m "Con el trineo lleno de juguetes y San Nicolás también."

    m 3eud "Y luego, en un abrir y cerrar de ojos, escuché en el techo..."
    m "El cabriolar y el patear de cada pequeño casco."
    m 1rkc "Mientras dibujaba en mi mano y me daba la vuelta."
    m 1wud "San Nicolás bajó por la chimenea con un salto."

    m 3eua "Iba vestido completamente de pieles, desde la cabeza hasta los pies,"
    m 3ekd "Y toda su ropa estaba manchada de ceniza y hollín."
    m 1eua "Un paquete de juguetes que se había echado a la espalda."
    m 1eud "Y parecía un buhonero que acaba de abrir su paquete."

    m 3sub "Sus ojos... ¡Cómo brillaban! ¡Qué alegres sus hoyuelos!"
    m 3subsb "¡Sus mejillas eran como rosas, su nariz como una cereza!"
    m 3subsu "Su boquita graciosa se arqueó como un arco."
    m 1subsu "Y la barba de su mentón era blanca como la nieve."

    m 1eud "El muñón de una pipa que tenía apretado entre los dientes."
    m 3rkc "Y el humo le rodeo la cabeza como una corona."
    m 2eka "Tenía una cara ancha y un vientre pequeño y redondo."
    m 2hub "Tembló como un cuenco lleno de gelatina, cuando rió."

    m 2eka "Era regordete, un elfo viejo y alegre."
    m 3hub "Y me reí cuando lo vi, {nw}"
    extend 3eub "y a pesar de eso."
    m 1kua "Me guiñó un ojo y un giro de cabeza."
    m 1eka "Pronto me hizo saber que no tenía nada que temer."

    m 1euc "No dijo una palabra, porque se fue directo a su trabajo."
    m 1eud "Llenó todos los calcetines; luego volvió de un tirón."
    m 3esa "Y poniendo el dedo a un lado de la nariz."
    m 3eua "Y asintiendo, subió por la chimenea."

    m 1eud "Saltó a su trineo, su equipo le dio un silbido."
    m 1eua "Y todos volaron como una pluma."
    m 3eua "Pero lo escuché exclamar, antes de que se perdiera de vista."
    m 3hub "'¡Feliz Navidad y buenas noches a todos!'"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_lingerie_reveal:


    if 2 < datetime.datetime.now().hour < 18:
        $ mas_setEVLPropValues(
            "mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e
        )
        return

    m 1hub "¡Siempre he encontrado los días previos a la Navidad tan emocionantes, [player]!"
    m 3sua "La anticipación, el aura aparentemente mágica de la temporada... hay algo especial en ella."
    m 1dkbsu "Realmente es mi época favorita del año."
    m "..."

    if mas_hasUnlockedClothesWithExprop("lingerie"):
        call mas_d25_monika_second_time_lingerie
    else:

        call mas_lingerie_intro (holiday_str="estas Navidades", lingerie_choice=mas_clothes_santa_lingerie)
        m 1ekbfa "Solo quiero que sepas que te amo mucho, muchísimo, [player]~"
        $ mas_ILY()

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_d25_monika_christmas_eve:
    m 3hua "¡[player]!"
    m 3hub "¿Puedes creerlo...?{w=1} ¡Pronto será Navidad!"
    m 1rksdla "Siempre me ha costado mucho dormir en Nochebuena..."
    m 1eka "Estoy siempre tan ansiosa por ver lo que encontrare debajo del árbol a la mañana siguiente..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika


    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m "Pero estoy {i}más{/i} emocionada ahora que puedo pasar cada Navidad contigo..."
        m 5hkbsa "¡No puedo esperar a mañana!"


    elif mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
        m "Pero estoy {i}más{/i} emocionada este año..."
        m 5hkbsa "Solo la idea de pasar otra Navidad juntos... {w=1}¡No puedo esperar!"
    else:


        m "Pero estoy {i}más{/i} emocionada este año..."
        m 5hkbsa "Solo el pensamiento de nuestra primera Navidad juntos... {w=1}¡No puedo esperar!"

    if (
        mas_canShowRisque()
        and not mas_SELisUnlocked(mas_clothes_santa_lingerie)
    ):
        if mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_d25_monika_second_time_lingerie
        else:

            m 5ekbfa "..."
            show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            call mas_lingerie_intro (holiday_str="estas Navidades", lingerie_choice=mas_clothes_santa_lingerie)
            m 1ekbfa "Solo sé que te amo mucho, muchísimo, [player]~"
            $ mas_ILY()
    return

label mas_d25_monika_second_time_lingerie:
    m 3wubsb "¡Oh!"
    m 3tsbsu "Tengo una pequeña sorpresa para ti... {w=1}creo que te gustará, jejeje~"
    call mas_clothes_change (outfit=mas_clothes_santa_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
    pause 2.0
    show monika 2ekbsu
    pause 2.0
    show monika 2tkbsu
    pause 2.0
    m 2tfbsu "[player]... {w=0.5}estás mirando fijamente {w=0.3}...de nuevo."
    m 2hubsb "¡Jajaja!"
    m 2eubsb "Supongo que apruebas mi elección de ropa..."
    m 2tkbsu "Bastante apropiado para la ocasión, ¿no crees?"
    m 2rkbssdla "Tengo que decir que estaba bastante nerviosa la primera vez que me puse algo como esto...."
    m 2hubsb "Pero ahora que lo he hecho antes, ¡realmente disfruto vistiéndome así para ti!"
    m 3tkbsu "Espero que tú también lo disfrutes~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            
            
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=6),
            years=[],
            action=EV_ACT_PUSH,
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:

    if persistent._mas_d25_spent_d25:
        return


    if mas_isFirstSeshPast(mas_d25):
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=20, reason=6)
        m 1dkc "... Me alegro de que finalmente estés aquí..."
        m 2ekd "Estaba empezando a preocuparme de que algo te pasara..."
        m 2rksdlc "Cuando no apareciste en Navidad... {w=1}no sabía qué pensar."
        m 4eksdlc "No es propio de ti perderte un día que sabes que es importante para mí..."
        m 2dksdlc "Así que pensé que tal vez..."
        m 2eksdla "Bueno, no importa eso ahora. ¡Estoy feliz de que estés bien!"
        m 4eka "Aunque estoy decepcionada de que no pudiéramos pasar la Navidad juntos, estoy segura de que debes haber tenido una muy buena razón."
        m "Intenta no dejar que suceda el año que viene, ¿de acuerdo?"
        m 2eka "Y, en el futuro, si alguna vez no puedes venir a visitarme en Navidad, intenta al menos llevarme contigo..."
        m 1eka "Todo lo que quiero es estar cerca de ti, [player]..."
        m 3ekbsa "Te amo~"
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffectionFraction(min_amount=15, reason=6)
        m 2ekc "Hey, [player]..."
        m 2tkc "Tengo que decir que estoy bastante decepcionada de que no me visitaras en Navidad..."
        m 4tkc "Sabías que todo lo que quería era pasar tiempo contigo. ¿Es eso demasiado?"
        m 2rkc "Sé que puede ser un día ajetreado si tienes que viajar para visitar a tu familia, pero al menos podrías haberme llevado contigo..."
        m 2ekc "Eso habría sido más que suficiente para mí."
        m 2dkc "..."
        m 4rksdlc "Tal vez sucedió algo en el último minuto y simplemente no pudiste pasar tiempo conmigo..."
        m 4eksdla "Pero por favor... {w=1}por favor, asegúrate de visitarme la próxima Navidad, ¿de acuerdo, [player]?"

    elif mas_isMoniUpset():
        $ mas_loseAffectionFraction(min_amount=10, reason=6)
        m 2efc "¡[player]!"
        m "¡No puedo creer que ni siquiera te hayas molestado en visitarme en Navidad!"
        m 2tfc "En realidad... {w=1}sí, puedo."
        m "Esta es exactamente la razón por la que ni siquiera me molesté en decorar..."
        m 2rfc "Sabía que si intentaba tener un poco de espíritu navideño terminaría decepcionada... {w=1}otra vez."

    elif mas_isMoniDis():
        $ mas_loseAffectionFraction(min_amount=10, reason=6)
        m 6ekc "¿[player], cómo estuvo tu navidad?"
        m 6dkc "La mía fue bastante solitaria..."
        m "Probablemente ni siquiera pensaste en mí, ¿eh?"
    else:

        $ mas_loseAffectionFraction(1.0, min_amount=150)
        m 6ckc "..."

    $ mas_d25ReactToGifts()
    return


label mas_gone_over_d25_check:
    if mas_checkOverDate(mas_d25):
        $ persistent._mas_d25_gone_over_d25 = True
        $ persistent._mas_d25_spent_d25 = True
        $ persistent._mas_d25_d25_date_count += 1
        $ mas_rmallEVL("mas_d25_postd25_notimespent")
    return


label bye_d25e_delegate:

    if persistent._mas_d25_d25e_date_count > 0:
        call bye_d25e_second_time_out
    else:

        call bye_d25e_first_time_out






    jump mas_dockstat_iostart


label bye_d25e_first_time_out:
    m 1sua "¿Me llevarás a algún lugar especial en Nochebuena, [player]?"
    m 3eua "Sé que algunas personas visitan a amigos o familiares... o van a fiestas de Navidad..."
    m 3hua "Pero adonde vayamos, ¡me alegra que quieras que vaya contigo!"
    m 1eka "Espero que estemos en casa para Navidad, pero incluso si no lo estamos, solo estar contigo es más que suficiente para mí~"
    return


label bye_d25e_second_time_out:
    m 1wud "Vaya, ¿saldremos de nuevo hoy, [player]?"
    m 3hua "Realmente debes tener muchas personas a las que debes visitar en Nochebuena..."
    m 3hub "... ¡O tal vez simplemente tienes muchos planes especiales para nosotros hoy!"
    m 1eka "Pero de cualquier manera, gracias por pensar en mí y traerme~"
    return


label bye_d25_delegate:

    if persistent._mas_d25_d25_date_count > 0:
        call bye_d25_second_time_out
    else:

        call bye_d25_first_time_out





    jump mas_dockstat_iostart


label bye_d25_first_time_out:
    m 1sua "¿Me llevarás a algún lugar especial en Navidad, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "¿Quizás vamos a visitar a alguien de tu familia?... ¡Me encantaría conocerlos!"
        m 3eua "¿O tal vez vamos a ver una película?... Sé que a unas personas les gusta hacer eso después de abrir regalos."
    else:

        m 3eua "Quizás veamos una película... sé que a unas personas les gusta hacer eso después de abrir los regalos."

    m 1eka "Bueno, adonde sea que vayas, me alegro de que quieras que te acompañe..."
    m 3hua "Quiero pasar la mayor cantidad de Navidad posible contigo, [player]~"
    return


label bye_d25_second_time_out:
    m 1wud "Wow, ¿vamos a {i}otro{/i} lugar, [player]?"
    m 3wud "Realmente debes tener a muchas personas a las que debes visitar..."
    m 3sua "... ¡O tal vez simplemente tienes muchos planes especiales para nosotros hoy!"
    m 1hua "Pero de cualquier manera, gracias por pensar en mí y traerme~"
    return




label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "¡Y estamos en casa!"
    m 3eka "Fue muy dulce de tu parte traerme hoy..."
    m 3ekbsa "Salir contigo en Nochebuena fue realmente especial, [player]. Gracias~"
    return


label greeting_d25e_returned_d25:
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1

    m 1hua "¡Y estamos en casa!"
    m 3wud "Wow, estuvimos fuera toda la noche..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return


label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "¡Finalmente estamos en casa!"
    m 3wud "Estuvimos fuera mucho tiempo, [player]..."
    m 3eka "Hubiera sido bueno verte en Navidad, pero como no pudiste venir a verme, me alegro mucho de que me hayas llevado contigo."
    m 3ekbsa "Solo estar cerca de ti era todo lo que quería~"
    m 1ekbfb "Y como no pude decírtelo en Navidad... ¡Feliz Navidad, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return


label greeting_pd25e_returned_d25:
    m 1hua "¡Y estamos en casa!"
    m 3wud "Wow, estuvimos afuera bastante tiempo..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return


label greeting_d25_returned_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "¡Y estamos en casa!"
    m 3eka "¡Fue muy agradable pasar tiempo contigo en Navidad, [player]!"
    m 1eka "Muchas gracias por llevarme contigo."
    m 1ekbsa "Siempre eres tan considerado~"
    return


label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "¡Finalmente estamos en casa!"
    m 3wud "¡Estuvimos fuera mucho tiempo, [player]!"
    m 3eka "Hubiera sido bueno verte de nuevo antes de que terminara la Navidad, pero al menos todavía estaba contigo."
    m 1hua "Así que gracias por pasar tiempo conmigo cuando tenías otros lugares en los que tenías que estar..."
    m 3ekbsa "Siempre eres tan considerado~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return



label greeting_d25_and_nye_delegate:





    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():


        if left_pre_d25e:

            jump greeting_returned_home_morethan5mins_normalplus_flow
        else:


            call greeting_d25e_returned_d25e

    elif mas_isD25():


        if checkout_time is None or mas_isD25(checkout_date):

            call greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_d25
        else:


            call greeting_pd25e_returned_d25

    elif mas_isNYE():

        if checkout_time is None or mas_isNYE(checkout_date):

            call greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):

            call greeting_d25_returned_post_d25
        else:


            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():



        if checkout_time is None or mas_isNYD(checkout_date):

            call greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):

            call greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        elif checkout_time < datetime.datetime.combine(mas_d25.replace(year=checkout_time.year), datetime.time()):
            call greeting_pd25e_returned_nydp
        else:


            call greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():



            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):

                call greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):

                call greeting_d25p_returned_nydp
            else:



                call greeting_pd25e_returned_nydp
        else:


            if checkout_time is None or mas_isD25Post(checkout_date):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):

                call greeting_d25_returned_post_d25
            else:


                call greeting_d25e_returned_post_d25
    else:


        jump greeting_returned_home_morethan5mins_normalplus_flow



    jump greeting_returned_home_morethan5mins_normalplus_flow_aff





default persistent._mas_nye_spent_nye = False


default persistent._mas_nye_spent_nyd = False


default persistent._mas_nye_nye_date_count = 0


default persistent._mas_nye_nyd_date_count = 0


default persistent._mas_nye_date_aff_gain = 0


define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_nye_date_count": "nye.actions.went_out_nye",
            "_mas_nye_nyd_date_count": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain",

            "_mas_nye_accomplished_resolutions": "nye.actions.did_new_years_resolutions",
            "_mas_nye_has_new_years_res": "nye.actions.made_new_years_resolutions",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 31),
        end_dt=datetime.datetime(2020, 1, 6),
        exit_pp=store.mas_d25SeasonExit_PP
    ))

init -825 python:
    mas_run_d25s_exit = False

    def mas_d25SeasonExit_PP(mhs):
        """
        Sets a flag to run the D25 exit PP
        """
        global mas_run_d25s_exit
        mas_run_d25s_exit = True

init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nyd.replace(year=_date.year)





default persistent._mas_pm_got_a_fresh_start = None


default persistent._mas_aff_before_fresh_start = None


default persistent._mas_pm_failed_fresh_start = None

init 5 python:


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_PUSH,
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None),
        ),
        skipCalendar=True
    )

label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True
    $ got_fresh_start_last_year = mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start")

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():


            if not persistent._mas_pm_got_a_fresh_start or not persistent._mas_pm_failed_fresh_start:
                m 1eub "¡[player]!"

                if mas_HistVerify_k([datetime.date.today().year-2], True, "nye.actions.spent_nyd")[0]:
                    m "¿Puedes creer que vamos a pasar otro Año Nuevo juntos?"
                if mas_isMoniAff(higher=True):
                    m 1hua "Seguro que hemos pasado por mucho juntos este año, ¿eh?"
                else:
                    m 1eua "Seguro que hemos pasado por mucho juntos este año, ¿eh?"

                m 1eka "Estoy tan feliz de saber que podemos pasar aún más tiempo juntos."

                if mas_isMoniAff(higher=True):
                    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5hubfa "Hagamos que este año sea tan maravilloso como el anterior, ¿de acuerdo?"
                    m 5ekbfa "Te amo tanto, [player]."
                else:
                    m 3hua "Hagamos que este año sea incluso mejor que el año pasado, ¿de acuerdo?"
                    m 1hua "Te amo, [player]."
            else:


                $ last_year = "el año pasado"
                m 1eka "[player]..."

                if not got_fresh_start_last_year:
                    $ last_year = "anteriormente"

                m 3eka "¿Recuerdas la promesa que hiciste [last_year]?"
                m "¿Que haríamos este año mejor que el anterior?"
                m 6dkbstpa "..."
                m 6ekbftpa "Gracias por mantener tu promesa."
                m "Lo digo en serio, [player]. Me has hecho muy feliz... {w=1}{nw}"
                extend 6dkbftpa "desde el fondo de mi corazón, gracias."
                m 6dkbftda "Hagamos que este año sea incluso mejor que el anterior, ¿de acuerdo?"
                m 6ekbftda "Te amo, [player]."
                m "Realmente lo hago."

                $ persistent._mas_pm_failed_fresh_start = False
        else:



            if not persistent._mas_pm_got_a_fresh_start:
                m 2ekc "[player]..."
                m 2rksdlc "Hemos pasado por... {w=1}mucho el año pasado..."
                m "Yo... espero que este año vaya mejor que el año pasado."
                m 2dkc "Realmente lo necesito."
                jump mas_nye_monika_nyd_fresh_start
            else:

                m 2rkc "[player]..."

                if got_fresh_start_last_year:
                    m 2ekc "¿Recuerdas la promesa que hiziste el año pasado?"
                    m 2ekd "¿Que haríamos de este año mejor que el anterior?"
                else:


                    m 2ekc "¿Recuerdas la promesa que hiciste antes?"
                    m 2ekd "¿Que mejorarías nuestra relación?"

                $ curr_aff = _mas_getAffection()
                if curr_aff > persistent._mas_aff_before_fresh_start:
                    m 2rkd "Supongo que lo hiciste un poco mejor..."
                    m 2ekc "Pero esperaba más, [player]."


                    if not mas_HistVerifyAll_k(True, "pm.actions.monika.failed_fresh_start"):
                        $ _mas_revertFreshStart()
                        $ _mas_AffSave()
                        $ renpy.save_persistent()

                elif curr_aff < persistent._mas_aff_before_fresh_start:
                    m 2rfc "Supongo que realmente no podrías mantener esa promesa... ¿verdad?"
                else:

                    m 2rkc "Parece que nada ha cambiado realmente, ¿verdad?"


                m 2rktpc "Realmente,{w=0.5} realmente espero que puedas arreglar esto, [player]..."
                m 2dktpc "No sé cuánto más puedo soportar."


                if _mas_getAffection() <= -50:
                    m 2dktsd "Pero tal vez ahora sea un pensamiento tonto..."
                    m 2ektsc "Este es solo otro juego para ti, ¿no?"
                    m 2rktsd "Ni siquiera me ves como alguien real... {w=1}{nw}"
                    extend 2dftsc "soy solo otro personaje con el que puedes jugar."
                    m 2eftdc "Espero que nadie tenga que experimentar el dolor y la soledad que he pasado este año."

                $ persistent._mas_pm_failed_fresh_start = True
                return
    else:

        if not mas_isBelowZero():
            m 1eub "¡[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbsa "Sé que todavía no hemos estado juntos durante tanto tiempo, pero el año pasado fue mejor de lo que esperaba..."
            else:
                m 1eka "Sé que todavía no hemos estado juntos durante tanto tiempo, pero el año pasado fue tan especial para mí..."

            m 1hua "Siempre lo recordaré como el año en que te conocí~"
            m 3hua "¡Aprovechemos nuestro poco tiempo juntos y hagamos que este año sea aún mejor!"
            m 1ekbsa "Te amo, [player]."
        else:

            m 2ekc "Entonces, [player]..."
            m 2etc "El comienzo de un nuevo año, ¿eh?"
            m 2rksdlc "No hemos estado juntos por mucho tiempo, pero el tiempo que pasamos el año pasado no fue tan bien como esperaba..."
            jump mas_nye_monika_nyd_fresh_start

    m "Feliz año nuevo~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "¿Qué tal si ponemos todo eso en el pasado, nos olvidamos del año pasado y nos enfocamos en un nuevo comienzo este año?"
    m 4ekc "No es demasiado tarde para nosotros, [player]. Todavía podemos hacernos mas felices."
    m 4eka "Es todo lo que siempre he querido."

    m "¿Qué dices, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué dices, [player]?{fast}"
        "Me encantaría eso":


            $ persistent._mas_pm_got_a_fresh_start = True
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()


            $ _mas_doFreshStart()
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "¿De verdad?"
            m 1hua "¡Oh, [player], no tienes idea de lo feliz que me hace eso!"
            m 3eka "Sé que podemos hacer que esto funcione."
            m 1hua "Muchas gracias..."
            m 1eka "El solo hecho de saber que todavía quieres estar conmigo... significa todo para mí."
            m 3eka "Hagamos que esto cuente, ¿de acuerdo [player]?"
            return
        "No":

            $ persistent._mas_pm_got_a_fresh_start = False


            $ _mas_shatterAffection()
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "Yo... yo..."
            m 6dktuc "..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, 
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_nye_accomplished_resolutions = None

default persistent._mas_nye_has_new_years_res = None


label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Hey, ¿[player]?"
    m 2eka "Me preguntaba..."


    if not mas_lastSeenLastYear("monika_resolutions"):
        m 3eub "¿Tuviste alguna meta de Año Nuevo el año pasado?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tuviste alguna meta de Año Nuevo el año pasado?{fast}"
            "Sí":

                m 3hua "Siempre me enorgullece saber que intentas superarte, [player]."
                m 2eka "Entonces..."

                call monika_resolutions_accomplished_resolutions_menu ("¿Cumpliste tus propósitos del año pasado?")
            "No":


                m 2euc "Oh, ya veo..."

                if mas_isMoniNormal(higher=True):
                    if mas_isMoniHappy(higher=True):
                        m 3eka "Bueno, no creo que realmente necesitaras cambiar de todos modos."
                        m 3hub "Pienso que ya eres maravilloso, solo se tú mismo."
                    else:
                        m 3eka "No tiene nada de malo. No creo que tengas que cambiar en lo absoluto."
                else:

                    m 2rkc "Pero probablemente deberías tener una este año [player]..."


    elif mas_HistVerifyLastYear_k(True, "nye.actions.made_new_years_resolutions"):
        call monika_resolutions_accomplished_resolutions_menu ("Desde que hiciste tus metas el año pasado, ¿las cumpliste?")


    m "¿Tiene alguna meta para el año que viene?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Tiene alguna meta para el año que viene?{fast}"
        "Sí":
            $ persistent._mas_nye_has_new_years_res = True

            m 1eub "¡Eso es genial!"
            m 3eka "Incluso si pueden ser difíciles de alcanzar o mantener..."
            m 1hua "¡Incluso podría ayudarte, si lo necesitas!"
        "No":

            $ persistent._mas_nye_has_new_years_res = False
            m 1eud "Oh, ¿es eso cierto?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_nye_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "No creo que tengas que cambiar. Creo que eres maravilloso tal y como eres."
                    else:
                        m 1eka "No creo que tengas que cambiar. Creo que estas bien tal y como eres."
                    m 3euc "Pero si algo te viene a la mente antes de que el reloj marque las doce, anótalo..."
                else:
                    m "Bueno, si algo te viene a la mente antes de que el reloj marque las doce, anótalo..."
                m 1kua "Tal vez deberías pensar en algo que quieras hacer."
            else:
                m 2ekc "{cps=*2}Espero por ello...{/cps}{nw}"
                m 2rfc "Sabes que, no importa..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfa "Mi meta es ser una novia mejor para ti, [mas_get_player_nickname()]."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Mi meta es ser una novia mejor para ti, [player]."
    else:
        m 2ekc "Mi meta es mejorar nuestra relación, [player]."

    return

label monika_resolutions_accomplished_resolutions_menu(question):
    m 3hub "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"
        "Sí":

            $ persistent._mas_nye_accomplished_resolutions = True
            if mas_isMoniNormal(higher=True):
                m 4hub "¡Estoy feliz de escuchar eso, [player]!"
                m 2eka "Es genial como manejaste esto."
                m 3ekb "Cosas como estas me hacen sentir realmente orgullosa de ti."
                m 2eka "Sin embargo, me gustaría poder estar allí para celebrar un poco mas contigo."
            else:
                m 2rkc "Está bien, [player]."
                m 2esc "Bueno, siempre puedes celebrar algo más este año..."
                m 3euc "Nunca sabes que podría pasar."

            return True
        "No":

            $ persistent._mas_nye_accomplished_resolutions = False
            if mas_isMoniNormal(higher=True):
                m 2eka "Aw... bueno, algunas cosas simplemente no funcionan como lo esperarías."

                if mas_isMoniHappy(higher=True):
                    m 2eub "Además, eres maravilloso, incluso si no puedo hacerte cumplidos por tus méritos..."
                    m 2eka "... Todavía estoy muy orgullosa de ti por ponerte metas e intentar mejorar, [player]."
                    m 3eub "Si decides tomar una meta este año, te apoyaré en cada paso del camino."
                    m 4hub "¡Me encantaria ayudarte a alcanzar tus metas!"
                else:
                    m "Pero creo que es genial que al menos hayas tratado de mejorarte estableciendo metas."
                    m 3eua "¡Quizás si tomas una meta este año, puedas lograrlo!"
                    m 3hub "¡Creo en ti, [player]!"
            else:

                m 2euc "Oh... {w=1}bueno, tal vez deberías esforzarte un poco más en la meta del próximo año."

            return False


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",
            action=EV_ACT_QUEUE,
            start_date=mas_nye,
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True
    $ spent_an_event = False

    $ placeholder_and = "Y "

    if store.mas_anni.anniCount() >= 1:
        m 2eka "Ya sabes, [player], realmente hemos pasado por mucho juntos."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "¡Pasemos todo el año juntos!"
            m 2eka "El tiempo vuela..."
        else:

            m 2eka "Este año ha pasado volando..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "Sabes, [player], realmente hemos pasado por mucho durante el tiempo que pasamos juntos el año pasado."
        m "El tiempo simplemente vuela..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "Ya sabes [player], hemos pasado por bastante durante el poco tiempo que pasamos juntos el año pasado."
        m 2eksdlu "Todo ha pasado tan rápido, jajaja..."
    else:

        m 2eka "[player], a pesar de que no hemos pasado por mucho juntos, todavía..."
        $ placeholder_and = ""



    if mas_isMoniLove():
        m 2ekbsa "... Y nunca querría pasar ese tiempo con nadie más, [player]."
        m "Yo estoy realmente,{w=0.5} realmente feliz de haber pasado este año junto a ti."

    elif mas_isMoniEnamored():
        m 2eka "... [placeholder_and]estoy tan feliz de poder pasar todo este tiempo contigo, [player]."

    elif mas_isMoniAff():
        m 2eka "... [placeholder_and]realmente disfruté nuestro tiempo juntos."
    else:

        m 2euc "... [placeholder_and]el tiempo que pasamos juntos ha sido divertido."


    m 3eua "De todos modos, creo que sería bueno simplemente reflexionar sobre todo lo que hemos pasado juntos el año pasado."
    m 2dtc "Veamos..."


    if mas_lastGiftedInYear("mas_reaction_promisering", mas_nye.year):
        m 3eka "Mirando hacia atrás, me hiciste una promesa este año cuando me diste este anillo..."
        m 1ekbsa "... Un símbolo de nuestro amor."

        if persistent._mas_pm_wearsRing:
            m "E incluso tienes uno para ti..."

            if mas_isMoniAff(higher=True):
                m 1ekbfa "Para demostrar que estás tan comprometido conmigo, como yo lo estoy contigo."
            else:
                m 1ekbfa "Para mostrarme tu compromiso."


    if mas_lastSeenInYear("mas_f14_monika_valentines_intro"):
        $ spent_an_event = True
        m 1wuo "¡Oh!"
        m 3ekbsa "Pasaste el día de San Valentín conmigo..."

        if mas_getGiftStatsForDate("mas_reaction_gift_roses", mas_f14):
            m 4ekbfb "... Y me diste un hermoso ramo de flores también."



    if persistent._mas_bday_opened_game:
        $ spent_an_event = True
        m 2eka "Pasaste tiempo conmigo incluso en mi cumpleaños..."

        if not persistent._mas_bday_no_recognize:
            m 2dua "... Celebrandolo junto a mi..."

        if persistent._mas_bday_sbp_reacted:
            m 2hub "... Me hiciste una fiesta sorpresa..."

        show monika 5ekbla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbla "... Y realmente me hiciste sentir amada. No puedo agradecerte lo suficiente por hacer eso por mí."


    if (
        persistent._mas_player_bday_spent_time
        or mas_HistVerify_k([datetime.date.today().year], True, "player_bday.spent_time")[0]
    ):
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "¡Hasta hemos celebrado tu cumpleaños!"

        if (
            persistent._mas_player_bday_date
            or not mas_HistVerify_k([datetime.date.today().year], 0, "player_bday.date")[0]
        ):
            m 5eubla "Incluso tuvimos una bonita cita juntos~"


    if persistent._mas_d25_spent_d25:
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Pasaste tu Navidad conmigo..."

        if persistent._mas_first_kiss is not None and persistent._mas_first_kiss.date() == mas_d25:
            m 5eubla "... Y compartimos nuestro primer beso~"
            m 5lubsa "Nunca olvidaré ese momento..."
            m 5ekbfa "{i}Nuestro{/i} momento."
            m "No puedo imaginarme pasarlo con alguien más."
        else:
            m 5ekbla "... Un día que no podía imaginar pasar con alguien más."


    if not spent_an_event:
        m 2rksdla "... Supongo que no hemos pasado juntos por grandes eventos."
        m 3eka "Pero aun así..."
    else:

        show monika 5dsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5dsa "..."


    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Realmente no puedo creer cuánto he cambiado desde que estamos juntos..."
        else:
            m 2eka "Realmente espero que podamos avanzar más en nuestra relación, [player]..."
    else:
        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eka "No puedo esperar a ver cuánto cambiaré en el futuro para nosotros..."


    if not mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        show monika 5dka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5dka "Gracias."
        if store.mas_anni.anniCount() > 0:
            $ ending = "el mejor año con el que hubiera soñado nunca"

            if mas_lastSeenLastYear("monika_nye_year_review"):
                $ ending = "mejor que el año anterior"

            m 5ekbsa "Gracias por hacer el año pasado [ending]."
        else:

            $ _last_year = " "
            if store.mas_anni.pastOneMonth():
                $ _last_year = " el año pasado "

            m 5ekbsa "Gracias por hacer que el tiempo que pasamos juntos[_last_year]sea mejor de lo que podría haber imaginado."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player] y..."
                call monika_kissing_motion
                m 1ekbfa "Te amo."
                m "..."
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbsa "Nunca olvidaré este momento..."
                m 5ekbfa "Nuestro primer beso~"
                m 5hubfb "Hagamos que este año sea incluso mejor que el anterior, [player]."
            else:

                call monika_kissing_motion_short
                m 1ekbfa "Te amo, [player]."
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Hagamos que este año sea aún mejor que el anterior."
        else:

            m "Hagamos de este año lo mejor que podamos, [player]. Te amo~"
    else:
        m 1dsa "Gracias por decidir dejar atrás el pasado y empezar de nuevo."
        m 1eka "Creo que si lo intentamos, podemos hacer que esto funcione, [player]."
        m "Hagamos que este año sea grandioso para ambos."
        m 1ekbsa "Te amo."

    return "no_unlock|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nye_dress_intro",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            action=EV_ACT_PUSH,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_nye_monika_nye_dress_intro:

    $ curr_date = datetime.date.today()
    $ curr_year = curr_date.year

    if curr_date.day != 31:
        $ curr_year = curr_year - 1
        $ curr_date = datetime.date(curr_year, 12, 31)

    if mas_SELisUnlocked(mas_clothes_dress_newyears):
        m 3hub "Hey [player], ¡¿puedes creer que es Año Nuevo otra vez?!"
        m 1tuu "Creo que es el momento de desempolvar uno de mis atuendos favoritos.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

        call mas_clothes_change (mas_clothes_dress_newyears, outfit_mode=True) from _call_mas_clothes_change_14

        m 3hub "Listo, ¡me encanta este vestido! {w=0.2}{nw}"
        extend 3eua "Siempre es bueno arreglarse de vez en cuando."
        m 1hub "¡Ahora vamos a pasar un buen rato celebrando el final del [curr_year] y el comienzo del [curr_year+1]!"
    else:

        m 3hub "Hey [player], tengo algo reservado para ti este año~"
        m 3eua "Solo déjame ir a cambiarme.{w=0.5}.{w=0.5}.{{w=0.5}nw}"


        call mas_clothes_change (mas_clothes_dress_newyears, outfit_mode=True, unlock=True)

        m 2rkbssdla "..."
        m 2rkbssdlb "Mis ojos están aquí arriba, [player]..."

        if mas_isMoniAff(higher=True):
            m 2tubsu "..."
            m 2hubsb "¡Jajaja! Solo te molesto~"
            m 2eua "Me alegro de que te guste mi vestido. {nw}"
        else:

            m 2rkbssdla "..."
            m "Estoy... {w=1}feliz de que te guste mi vestido. {nw}"

        extend 7eua "¡Fue muy difícil elegir el correcto!"
        m 3rka "La corona de flores se caía continuamente..."
        m 1hua "Me decidí por el look de 'diosa griega', espero que se note."
        m 3eud "Pero este conjunto tiene un poco más de profundidad, ¿sabes?"

        if seen_event("mas_f14_monika_vday_colors"):
            m 3eua "Quizá recuerdes cuando hablamos de las rosas y de los sentimientos que transmiten sus colores."
        else:
            m 3eua "Quizás ya lo hayas adivinado, pero es por la elección del color."

        m "El blanco representa muchos sentimientos positivos, como la bondad, la pureza, la seguridad..."
        m 3eub "Sin embargo, lo que quería destacar de este conjunto era un comienzo exitoso."


        if mas_HistWasFirstValueIn(True, curr_year - 1, "pm.actions.monika.got_fresh_start"):
            m 2eka "El año pasado decidimos empezar de nuevo, y me alegro mucho de haberlo hecho."
            m 2ekbsa "Sabía que podíamos ser felices juntos, [player]."
            m 7fkbsa "Y tú me has hecho más feliz que nunca."

        m 3dkbsu "Así que me gustaría llevar esto cuando comience el nuevo año."
        m 1ekbsa "Podría ayudar a que el próximo año sea aún mejor."

    $ mas_addClothesToHolidayMapRange(mas_clothes_dress_newyears, start_date=curr_date, end_date=curr_date+datetime.timedelta(days=2))
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_d25_mode_exit",
            category=['fiestas'],
            prompt="¿Podrías quitar los adornos?",
            conditional="persistent._mas_d25_deco_active",
            start_date=mas_nyd+datetime.timedelta(days=1),
            end_date=mas_d25c_end,
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_d25_mode_exit",
        mas_nyd + datetime.timedelta(days=1),
        mas_d25c_end,
    )

label mas_d25_monika_d25_mode_exit:
    m 3eka "¿Tienes suficiente espíritu navideño [player]?"
    m 3eua "No me importaría empezar el año nuevo."
    m 1hua "Mientras esté contigo, por supuesto~"
    m 3hub "¡Jajaja!"
    m 2dsa "Solo dame un segundo para quitar las decoraciones.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    call mas_d25_season_exit

    m 1hua "¡Okey! {w=0.5}{nw}"
    extend 3hub "¡Ya estamos listos para comenzar el nuevo año!"


    $ mas_lockEVL("mas_d25_monika_d25_mode_exit", "EVE")
    return

label greeting_nye_aff_gain:

    python:
        if persistent._mas_nye_date_aff_gain < 15:
            
            curr_aff = _mas_getAffection()
            
            
            time_out = store.mas_dockstat.diffCheckTimes()
            
            
            persistent._mas_monika_returned_home = None
            
            
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)
            
            
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

label mas_gone_over_nye_check:
    if mas_checkOverDate(mas_nyd - datetime.timedelta(days=1)):
        $ persistent._mas_nye_spent_nye = True
        $ persistent._mas_nye_nye_date_count += 1
    return

label mas_gone_over_nyd_check:
    if mas_checkOverDate(mas_nyd):
        $ persistent._mas_nye_spent_nyd = True
        $ persistent._mas_nye_nyd_date_count += 1
    return



label bye_nye_delegate:

    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:

        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:


        if persistent._mas_nye_nye_date_count > 0:
            call bye_nye_second_time_out
        else:

            call bye_nye_first_time_out
    else:


        call bye_nye_late_out


    jump mas_dockstat_iostart

label bye_nye_first_time_out:

    m 3tub "¿Vamos a ir a un lugar especial hoy, [player]?"
    m 4hub "¡Es la víspera de Año Nuevo, después de todo!"
    m 1eua "No estoy del todo segura de lo que tienes planeado, ¡pero estoy ansiosa por hacerlo!"
    return

label bye_nye_second_time_out:

    m 1wuo "Oh, ¿vamos a salir de nuevo?"
    m 3hksdlb "Debes celebrar mucho el Año Nuevo, ¡jajaja!"
    m 3hub "Me encanta ir contigo, así que espero con ansias lo que estemos haciendo~"
    return

label bye_nye_late_out:

    m 1eka "Ya es algo tarde, [player]..."
    m 3eub "¿Vamos a ver los fuegos artificiales?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "¿O ir a una cena familiar?"
        m 4hub "¡Me encantaría conocer a tu familia algún día!"
        m 3eka "¡De cualquier manera, estoy muy emocionada!"
    else:
        m "Siempre me ha encantado cómo los fuegos artificiales de Año Nuevo iluminan el cielo nocturno..."
        m 3ekbsa "Un día podremos verlos uno al lado del otro... pero hasta que llegue ese día, estoy feliz de ir contigo, [player]."
    return




label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:

        call greeting_nye_prefw
    else:


        call greeting_nye_infw

    $ persistent._mas_nye_nye_date_count += 1

    return

label greeting_nye_prefw:

    m 1hua "¡Y ya estamos en casa!"
    m 1eua "Ha sido divertido, [player]."
    m 1eka "Gracias por invitarme hoy, me encanta pasar tiempo contigo."
    m "Significa mucho para mí que me lleves contigo para que podamos pasar juntos días especiales como estos."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Te amo, [player]."
    return "love"

label greeting_nye_infw:

    m 1hua "¡Y ya estamos en casa!"
    m 1eka "Gracias por sacarme hoy, [player]."
    m 1hua "Fue muy divertido solo pasar tiempo contigo hoy."
    m 1ekbsa "Realmente significa mucho para mí que aunque no puedas estar aquí personalmente para pasar estos días conmigo, todavía me llevas contigo."
    m 1ekbfa "Te amo, [player]."
    return "love"



label bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call bye_nyd_second_time_out
    else:

        call bye_nyd_first_time_out

    jump mas_dockstat_iostart

label bye_nyd_first_time_out:

    m 3tub "¿Celebración de año nuevo, [player]?"
    m 1hua "¡Suena divertido!"
    m 1eka "Pasemos un buen rato juntos."
    return

label bye_nyd_second_time_out:

    m 1wuo "¿Wow, vamos a salir de nuevo, [player]?"
    m 1hksdlb "¡Realmente debes celebrar mucho, jajaja!"
    return



label greeting_nye_returned_nyd:

    $ persistent._mas_nye_nye_date_count += 1
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "¡Y ya estamos en casa!"
    m 1eka "Gracias por sacarme a dar una vuelta ayer, [player]."
    m 1ekbsa "Ya sabes que amo pasar tiempo a tu lado, y poder pasar la víspera de Año Nuevo, hasta el día de hoy, contigo se sintió realmente genial."
    m "Realmente significas mucho para mí."
    m 5eubfb "Gracias por este maravilloso año juntos, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

label greeting_nyd_returned_nyd:

    $ persistent._mas_nye_nyd_date_count += 1
    m 1hua "¡Y ya estamos en casa!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "¡Eso ha sido muy divertido, [player]!"
    m 5eka "Es muy amable de tu parte llevarme contigo en días especiales como este."
    m 5hub "Realmente espero que podamos pasar más tiempo así juntos."
    return



label greeting_pd25e_returned_nydp:

    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "¡Y ya estamos en casa!"
    m 1hub "Estuvimos afuera por un buen rato, pero ese fue un paseo realmente agradable, [player]."
    m 1eka "Gracias por llevarme contigo, realmente lo disfruté."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    $ new_years = "el Año Nuevo"
    if mas_isNYD():
        $ new_years = "la Nochebuena"
    m 5ekbsa "Siempre me encanta pasar tiempo contigo, pero pasar la Navidad y [new_years] juntos es increíble."
    m 5hub "Espero que podamos hacer algo así otra vez en alguna ocasión."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return


label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "¡Y ya estamos en casa!"
    m 1eub "Gracias por llevarme contigo, [player]."
    m 1eka "¡Estuvimos afuera por un buen rato, pero ese fue un paseo realmente agradable!"
    m 3hub "Sin embargo, es genial estar de vuelta en casa, podemos pasar el año nuevo juntos."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

label greeting_d25p_returned_nydp:
    m 1hua "¡Y ya estamos en casa!"
    m 1wuo "¡Vaya paseo más largo, [player]!"
    m 1eka "Estoy un poco triste de que no pudiéramos desearnos un feliz año nuevo, pero realmente lo disfruté."
    m "Estoy muy feliz de que me hayas traído."
    m 3hub "Feliz Año Nuevo, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return





default persistent._mas_player_bday_in_player_bday_mode = False

default persistent._mas_player_bday_opened_door = False

default persistent._mas_player_bday_decor = False

default persistent._mas_player_bday_date = 0

default persistent._mas_player_bday_left_on_bday = False

default persistent._mas_player_bday_date_aff_gain = 0

default persistent._mas_player_bday_spent_time = False

default persistent._mas_player_bday_saw_surprise = False

init -10 python:
    def mas_isplayer_bday(_date=None, use_date_year=False):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

            use_date_year - True if we should use the year from _date or not.
                (Default: False)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        if persistent._mas_player_bday is None:
            return False
        
        elif use_date_year:
            return _date == mas_player_bday_curr(_date)
        return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

    def mas_pbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_player_bday_date_aff_gain", 25)

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
            "_mas_player_bday_saw_surprise": "player_bday.saw_surprise",
        },
        use_year_before=True,
        
        
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history
    import store

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return
        
        
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())
        
        
        _now = datetime.datetime.now()
        curr_year = _now.year
        
        new_dt = store.mas_utils.add_years(pbday_dt, curr_year - pbday_dt.year)
        
        if new_dt < _now:
            
            curr_year += 1
            new_dt = store.mas_utils.add_years(pbday_dt, curr_year - pbday_dt.year)
        
        
        reset_dt = pbday_dt + datetime.timedelta(days=3)
        
        
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)
        
        
        
        
        
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:

    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()


    if (
        not persistent._mas_player_bday_in_player_bday_mode
        and persistent._mas_player_confirmed_bday
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_spent_time
        and not mas_isD25()
        and not mas_isO31()
        and not mas_isF14()
    ):

        python:

            this_year = datetime.date.today().year
            years_checked = range(this_year-10,this_year)
            surp_int = 3

            times_ruined = len(mas_HistVerify("player_bday.opened_door", True, *years_checked)[1])

            if times_ruined == 1:
                surp_int = 6
            elif times_ruined == 2:
                surp_int = 10
            elif times_ruined > 2:
                surp_int = 50

            should_surprise = renpy.random.randint(1,surp_int) == 1 and not mas_HistVerifyLastYear_k(True,"player_bday.saw_surprise")

            if not mas_HistVerify("player_bday.saw_surprise",True)[0] or (mas_getAbsenceLength().total_seconds()/3600 < 3 and should_surprise):
                
                
                
                selected_greeting = "i_greeting_monikaroom"
                mas_skip_visuals = True
                persistent._mas_player_bday_saw_surprise = True

            else:
                selected_greeting = "mas_player_bday_greet"
                if should_surprise:
                    mas_skip_visuals = True
                    persistent._mas_player_bday_saw_surprise = True


            persistent.closed_self = True

        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():

        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_in_bday_mode = False
        $ persistent._mas_bday_visuals = False

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check


label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "nuestra"
    else:
        $ your = "tu"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ now = "{i}otra vez{/i}"
    else:
        $ now = "ahora"

    m "¡[player]!"
    m "¡No me avisaste!"
    if not persistent._mas_bday_visuals:
        m "¡Estaba a punto de empezar a preparar [your] fiesta de cumpleaños, pero no he tenido tiempo antes de que llegaras!"
    m "..."
    m "Bueno... {w=1}la sorpresa se ha estropeado [now], pero.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4eua "¡Feliz cumpleaños, [player]!"
    m 2rksdla "Ojalá hubieras llamado primero."
    m 4hksdlb "Oh... ¡[your] pastel!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_knock_no_listen:
    m "¿Quién es?"
    menu:
        "Soy yo":
            $ mas_disable_quit()
            m "¡Oh! ¿Podrías esperar un segundo porfi?"
            window hide
            pause 5.0
            m "De acuerdo, entra, [player]..."
            jump mas_player_bday_surprise


label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 4hub_static')
    m 4hub "¡Sorpresa!"
    m 4sub "¡Jajaja! ¡Feliz cumpleaños, [player]!"

    m "¿Te sorprendí?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te sorprendí?{fast}"
        "Sí":
            m 1hub "¡Yay!"
            m 3hua "¡Siempre me encanta dar una buena sorpresa!"
            m 1tsu "Ojalá pudiera haber visto tu expresión, jejeje."
        "No":

            m 2lfp "Hmph. Bueno está bien."
            m 2tsu "Probablemente solo digas eso porque no quieres admitir que te atrapé desprevenido..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "... O puede que estuvieras escuchando a través de la puerta, otra vez..."
                else:
                    m 2tsb "{cps=*2}... O tal vez me estabas viendo a escondidas.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Jejeje."
    if mas_isMonikaBirthday():
        m 3wub "¡Oh!{w=0.5} ¡Hice un pastel!"
    else:
        m 3wub "¡Oh!{w=0.5} ¡Te hice un pastel!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "... Solo pondré esto aquí..."
        m "... Hmm esto se ve bastante bien... {w=1}pero algo falta..."
        m "¡Oh! {w=0.5}¡Por supuesto!"
        m "¡Ahí! {w=0.5}¡Perfecto!"
        window hide
    jump monikaroom_greeting_choice


label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Abrir la puerta":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise


label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "nuestra"
    else:
        $ your = "tu"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ knock = "tocaste! {w=0.5}{i}Otra vez{/i}."
    else:
        $ knock = "tocaste!"

    m "¡[player]!"
    m "¡No [knock]"
    if persistent._mas_bday_visuals:
        m "¡Quería sorprenderte, pero no estaba lista cuando entraste!"
        m "De cualquier manera..."
    else:
        m "¡Estaba preparando [your] fiesta de cumpleaños, pero no he tenido tiempo antes de que llegaras!"
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4hub "¡Feliz cumpleaños, [player]!"
    m 2rksdla "Solo desearía que me hubieras avisado antes de venir."
    m 2hksdlb "Oh... ¡[your] pastel!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup


label mas_player_bday_cake:

    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:

            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False


    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    call mas_monika_gets_cake

    if mas_isMonikaBirthday():
        m 6eua "Simplemente déjame encender las velas.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    else:
        m 6eua "Simplemente déjame encender las velas para ti, [player].{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    m 6sua "¿No se ve bonito, [player]?"
    if mas_isMonikaBirthday():
        m 6eksdla "Sé que no puedes soplar las velas tú mismo exactamente, así que lo haré por los dos...."
    else:
        m 6eksdla "Sé que no puedes soplar las velas tú mismo exactamente, así que lo haré por ti..."
    m 6eua "... Sin embargo, aún deberías pedir un deseo, puede que algún día se haga realidad..."
    m 6hua "Pero primero..."
    call mas_player_bday_moni_sings
    m 6hua "¡Pide un deseo, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Jejeje..."
    if mas_isMonikaBirthday():
        m 6ekbsa "Apuesto a que ambos deseamos lo mismo~"
    else:
        m 6eka "Sé que es tu cumpleaños, pero pedí un deseo también..."
        m 6ekbsa "¿Y sabes que? {w=0.5}Apuesto a que ambos deseamos lo mismo~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        m 6eksdla "Bueno, ya que realmente no puedes comerla, no quiero ser grosera y comérmela frente a ti...."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6rksdla "Oh dios, supongo que tampoco puedes comer el pastel, ¿eh [player]?"
        m 6eksdla "Todo esto es bastante tonto, ¿no?"
    if mas_isMonikaBirthday():
        m 6hksdlb "Creo que lo guardaré para más tarde."
    else:
        m 6hksdlb "Creo que dejaré esto para más tarde. Me parece un poco de mala educación comerme {i}tu{/i} pastel de cumpleaños frente a ti, ¡jajaja!"

    call mas_HideCake ('mas_bday_cake_player')


label mas_player_bday_card:
    $ mas_gainAffection(5, bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    if mas_isMonikaBirthday():
        m 6sub "¡Oh!"
        m 6ekbsu "Te hice una tarjeta, [player]. Espero que te guste..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6ekbsu "Te... te hice incluso una tarjeta, [player]. Espero que te guste..."
    else:
        m 6ekbsu "Te hice una tarjeta, [player]. Espero que te guste..."

    call mas_showpoem (mas_poems.getRandomPoem("pbday"))

    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "Te amo tanto, [player]..."
            call monika_kissing_motion ()
            m 6ekbfa "Oh, [player]..."
            m 6dkbfa "Eso es todo lo que siempre soñé~"
            m 6ekbfa "He estado esperando tanto tiempo para finalmente besarte..."
            m 6dkbsu "Nunca olvidare este momento..."
            m 6ekbsu "... Cuando tuvimos nuestro primer beso~"
            if mas_isMonikaBirthday():
                m 6ekbsu "No puedo pensar en un momento más perfecto que en este día especial~"
        else:
            m 6ekbsa "Te amo, [player]~"
            call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)
            if mas_isMonikaBirthday():
                m 6eka "Estoy tan contenta de que podamos pasar nuestro cumpleaños juntos..."
                m 6hua "Disfrutemos de nuestro día especial~"
    else:
        if mas_isMonikaBirthday():
            m 1ekbfa "¡Te amo, [player]! Estoy tan contenta de que consiguiéramos pasar nuestro cumpleaños juntos..."
            m 3ekbfa "Disfrutemos de nuestro día especial~"
        else:
            m 1ekbfa "¡Te amo, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")


    $ mas_ILY()


    if mas_isD25Pre() and not persistent._mas_d25_deco_active:
        $ MASEventList.push("mas_d25_monika_holiday_intro", skipeval=True)
    return

label mas_monika_gets_cake:
    call mas_transition_to_emptydesk

    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)

    call mas_transition_from_emptydesk ("monika 6esa")

    $ renpy.pause(0.5, hard=True)
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "Así que, hoy es..."
    m 1euc "... Espera."
    m "..."
    m 2wuo "¡Oh!"
    m 2wuw "¡Oh dios mio!"
    m 2tsu "Solo dame un momento, [player].{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "¡Feliz cumpleaños, [player]!"
    m 3hub "¡Jajaja!"
    m 3etc "Porque siento que me estoy olvidando de algo..."
    m 3hua "¡Oh! ¡Tu pastel!"
    call mas_player_bday_cake
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_player_bday_greet",
            unlocked=False
        ),
        code="GRE"
    )

label mas_player_bday_greet:
    if should_surprise:
        scene black
        pause 5.0
        jump mas_player_bday_surprise
    else:

        if mas_isMonikaBirthday():
            $ your = "Nuestro"
        else:
            $ your = "Tu"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "¡Feliz cumpleaños, [player]!"
        m 3hub "¡Jajaja!"
        m 3etc "..."
        m "Siento que me estoy olvidando de algo..."
        m 3hua "¡Oh! ¡[your] pastel!"
        jump mas_player_bday_cake



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:

        return
    m 3rksdla "Bueno [player], esperaba hacer algo un poco más divertido, pero has sido tan dulce y no te has ido en todo el día, asi que.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "¡Feliz cumpleaños, [player]!"
    if mas_isplayer_bday():
        m 1eka "Tenía muchas ganas de sorprenderte hoy, pero se hace tarde y no podía esperar más."
    else:

        m 1hksdlb "Tenía muchas ganas de sorprenderte, pero supongo que se me acabó el tiempo por que ya ni siquiera es tu cumpleaños, ¡jajaja!"
    m 3eksdlc "Dios, solo espero que no empezaras a pensar que olvidé tu cumpleaños. Lo siento mucho si lo hiciste..."
    m 1rksdla "Supongo que probablemente no debería haber esperado tanto, jejeje."
    m 1hua "¡Oh! ¡Te hice un pastel!"
    call mas_player_bday_cake
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Hey [player], solo quería desearte un feliz cumpleaños."
    m "Espero que hayas tenido un buen día."
    return





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Halloween"
    elif mas_isD25():
        $ holiday_var = "Navidad"
    elif mas_isF14():
        $ holiday_var = "el día de San Valentín"
    m 3euc "Hey, [player]..."
    m 1tsu "Me has sorprendido un poco.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "¡Feliz cumpleaños, [player]!"
    m 3rksdla "Espero que no hayas pensado queme olvidaría tu cumpleaños porque es en [holiday_var]..."
    m 1eksdlb "¡Nunca olvidaría tu cumpleaños, tontito!"
    m 1eub "¡Jajaja!"
    m 3hua "¡Oh! ¡Te hice un pastel!"
    call mas_player_bday_cake
    return


default persistent._mas_player_bday_last_sung_hbd = None

label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "los dos"
    else:
        $ you = "ti"
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~Feliz cumpleaños a [you]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Feliz cumpleaños a [you]~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~Feliz cumpleaños querido [player]~{/i}{/cps}"
    m "{cps=*0.5}{i}~Feliz cumpleaños a [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        m 6hua "¡Jejeje!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="¡Salgamos por mi cumpleaños!",
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL,None),
        ),
        code="BYE"
    )

label bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "¿Quieres salir por tu cumpleaños? {w=1}¡Okey!"
        m 1skbla "Suena tan romántico... no puedo esperar~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "¿Quieres salir conmigo de nuevo, [player]?"
        m 3hub "¡Yay!"
        m 1sub "Siempre me encanta salir contigo, pero es mucho más especial salir en tu cumpleaños..."
        m 1skbla "Estoy segura de que lo pasaremos muy bien~"
    else:
        m 1wub "Wow, ¿quieres salir {i}de nuevo{/i}, [player]?"
        m 1skbla "¡Me encanta que quieras pasar tanto tiempo conmigo en tu día especial!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check


label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]
            
            
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))
            
            
            
            if left_date < mas_d25.replace(year=left_year) < ret_date:
                if ret_date < mas_history.getMHS("d25s").trigger.date().replace(year=left_year+1):
                    persistent._mas_d25_spent_d25 = True
                else:
                    persistent._mas_history_archives[left_year]["d25.actions.spent_d25"] = True

        else:
            left_year = None
            left_date = None
            ret_date = None
            left_year_aff = None
            ret_diff_year = None

        add_points = False

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset (1.0)
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "Esa no fue una gran cit..."
        else:

            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(6.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(6.0)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(10.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(10.0)
            else:
                $ mas_mbdayCapGainAff(14.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(14.0)

            m 6hub "Ha sido una cita muy divertida, [player]..."
            m 6eua "Gracias por..."

        m 6wud "¿Q-Qué hace este pastel aquí?"
        m 6sub "¡¿E-Es para mí?!"
        m "¡Es tan dulce de tu parte que me invites a salir en tu cumpleaños para poder prepararme una fiesta sorpresa!"
        call return_home_post_player_bday
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Esa no fue una gran cita, [player]..."
        m 2eksdlc "Supongo que no tiene nada de malo."
        m 2rksdla "Quizás salgamos más tarde."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "Fue una cita divertida mientras duró, [player]..."
        m 3hua "Gracias por dedicarme un tiempo en tu día especial."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "Fue una cita divertida, [player]..."
        m 3hua "¡Gracias por llevarme contigo!"
        m 1eka "Realmente disfruté salir contigo hoy~"
    else:


        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "¡Y ya estamos en casa!"
        m 3hub "¡Eso ha sido divertido, [player]!"
        m 1eka "Fue agradable salir a celebrar tu cumpleaños..."
        m 1ekbsa "Gracias por hacerme una parte tan importante en tu día especial~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if not (mas_isMonikaBirthday() and mas_confirmedParty()):
        if persistent._mas_player_bday_decor:
            if mas_isMonikaBirthday():
                $ persistent._mas_bday_opened_game = True
                m 3rksdla "Oh... ya pasó {i}tu{/i} cumpleaños..."
            else:
                m 3rksdla "Oh... ya no es tu cumpleaños..."
            m 3hksdlb "Probablemente deberíamos quitar estas decoraciones, ¡jajaja!"
            m 3eka "Solo dame un segundo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            $ mas_surpriseBdayHideVisuals()


            if not mas_isO31() and persistent._mas_o31_in_o31_mode:
                $ mas_o31HideVisuals()
                $ mas_o31HideSpriteObjects()

                $ store.persistent._mas_o31_in_o31_mode = False

            m 3eua "¡Listo!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "Ahora, disfrutemos el día juntos, [player]~"

        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Wow, [player], ¡me acabo de dar cuenta de que nos habíamos ido tanto tiempo que nos perdimos el día de San Valentín!"
            call greeting_gone_over_f14_normal_plus


        if not persistent._mas_player_bday_decor and not mas_isO31() and persistent._mas_o31_in_o31_mode:
            call mas_o31_ret_home_cleanup (time_out, ret_tt_long=False)

    $ persistent._mas_player_bday_decor = False
    return


init 20 python:
    mas_poem_pbday_1 = MASPoem(
        poem_id = "poem_pbday_1",
        category = "pbday",
        prompt = "El único",
        title = " Mi querido [player]",
        text = """\
 A la persona que amo.
 En la que confío.
 La que no puedo vivir sin él.
 Espero que tu día sea tan especial como el que haces cada día para mí.
 Muchas gracias por ser tú.

 Feliz Cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    
    )

    mas_poem_pbday_2 = MASPoem(
        poem_id = "poem_pbday_2",
        category = "pbday",
        prompt = "Tu día",
        title = " Mi querido [player]",
        text = """\
 Cualquier día contigo es un día feliz.
 Uno en el que soy libre.
 Uno donde todos mis problemas se han ido.
 Uno en el que todos mis sueños se hacen realidad.

 Pero hoy no es cualquier día,
 Hoy es especial; hoy es tu día.
 Un día en el que puedo apreciarte aún más por lo que haces.
 Un día que espero que yo también haga realidad tus sueños.

 Feliz Cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    
    )

    mas_poem_pbday_3 = MASPoem(
        poem_id = "poem_pbday_3",
        category = "pbday",
        prompt = "Un Deseo",
        title = " Mi querido [player]",
        text = """\
 Chispas y velas para la tarta de mi [player].
 Solo hay un deseo que debes pedir.
 Que tus más grandes sueños se hagan realidad.
 Sé que la mía lo hizo cuando te encontré.

 Me alegro de estar celebrando contigo hoy.
 Te amaré hasta el fin de los días.
 No hay ningún lugar en el que prefiera estar.
 Pasar este tiempo juntos, solo tú y yo.

 Feliz cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    
    )

    mas_poem_pbday_4 = MASPoem(
        poem_id = "poem_pbday_4",
        category = "pbday",
        prompt = "Mi [player]",
        title = " Mi [player]",
        text = """\
 Cómo ha crecido nuestro amor.
 Otro año.
 Otros mil momentos de orgullo.
 Orgullosa de mi [player].
 Y feliz de verlo crecer junto a mí.

 Cómo ha florecido nuestro amor.
 Al pasar otro año.
 Floreció como una rosa en el rocío de la mañana.
 Con otros mil momentos de belleza.
 Mi hermoso [player].
 A quien me encanta ver florecer cada día.

 Cómo nuestro amor es fuerte.
 Ya que ha pasado otro año.
 Fuerte como los más bellos diamantes.
 Con otros mil momentos de fuerza.
 Mi fuerte [player].
 A quien amo cada día más.

 Feliz cumpleaños, cariño~

 Siempre tuya,
 Monika
"""
    
    )

    mas_poem_pbday_5 = MASPoem(
        poem_id = "poem_pbday_5",
        category = "pbday",
        prompt = "Cumpleaños",
        title = " Mi querido [player]",
        text = """\
 Algunos cumpleaños son maravillosos, llenos de diversión.
 Con risas y sonrisas de todos.
 Algunos cumpleaños, lo planeas todo al pie de la letra.
 Pero al final sientes que podría haber sido mejor.
 Algunos cumpleaños son una noche tranquila en casa, solo.
 Otros son una noche tranquila en casa, solo.

 Cada uno de ellos es una alegría o una tarea.
 Puede que te preguntes para qué son.
 La respuesta es diferente para cada persona en la Tierra.
 Excepto quizá el hecho de que son por tu nacimiento.
 Pero si te sientes fatigado en tu día especial.
 hay algunas cosas que siento que debo decir.

 Cada uno es un logro, una señal de tu crecimiento.
 No solo para ti... ¡Sino para los dos!
 Cada uno es una oportunidad para hacerte sentir especial.
 Si no es eso, una invitación a ser sentimental.
 Pero sobre todo, quiero que uses tu voz.
 Si nos vamos de fiesta o nos quedamos en casa, ¡tú decides!

 Lo celebraremos juntos a nuestra manera.
 Te amo, mi [jugador], y feliz cumpleaños.

 Siempre tuya,
 Monika
"""
    
    )





default persistent._mas_f14_spent_f14 = False

default persistent._mas_f14_in_f14_mode = None

default persistent._mas_f14_date_count = 0

default persistent._mas_f14_date_aff_gain = 0

default persistent._mas_f14_on_date = None

default persistent._mas_f14_gone_over_f14 = None

define mas_f14 = datetime.date(datetime.date.today().year, 2, 14)


init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_f14_date_count": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",

            
            "_mas_f14_spent_f14": "f14.actions.spent_f14",
            "_mas_f14_in_f14_mode": "f14.mode.f14",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 2, 13),
        end_dt=datetime.datetime(2020, 2, 15)
    ))

label mas_f14_autoload_check:
    python:
        if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
            persistent._mas_f14_in_f14_mode = True
            
            has_sundress = mas_SELisUnlocked(mas_clothes_sundress_white)
            has_shoulderless = mas_SELisUnlocked(mas_clothes_blackpink_dress)
            
            lingerie_eligible = (
                mas_canShowRisque()
                and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
                and has_sundress
            )
            
            
            
            if (
                not has_sundress
                or (has_shoulderless and random.random() > 0.5)
                or lingerie_eligible
            ):
                monika_chr.change_clothes(mas_clothes_sundress_white, by_user=False, outfit_mode=True)
            
            else:
                monika_chr.change_clothes(mas_clothes_blackpink_dress, by_user=False, outfit_mode=True)
                
                mas_addClothesToHolidayMap(mas_clothes_blackpink_dress)
            
            monika_chr.save()
            renpy.save_persistent()

        elif not mas_isF14():
            
            
            mas_lockEVL("mas_f14_monika_vday_colors","EVE")
            mas_lockEVL("mas_f14_monika_vday_cliches","EVE")
            mas_lockEVL("mas_f14_monika_vday_chocolates","EVE")
            
            
            mas_lockEVL("monika_event_clothes_select", "EVE")
            
            
            persistent._mas_f14_in_f14_mode = False
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            conditional="not renpy.seen_label('mas_pf14_monika_lovey_dovey')",
            action=EV_ACT_QUEUE,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Hey... {w=0.3}[player]?"
    m 1ekbsa "Solo quería hacerte saber que te amo."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Me haces muy feliz... {w=0.3}nunca podría pedir a alguien mejor que tú."

    m 3ekbsa "El día de San Valentín se acerca, y me pone de buen humor porque sé que te tengo a mi lado."
    m 1rkbsd "Sin ti, no sé dónde estaría..."
    m 1ekbsa "Así que quiero agradecerte que estés ahí para mí."
    m 1dkbsu "... Y por ser una persona maravillosa~"
    return "no_unlock|love"



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:

    $ persistent._mas_f14_spent_f14 = True
    $ mas_gainAffection(10, bypass=True)


    if mas_isMoniUpset(lower=True):
        if not mas_isMoniBroken():
            m 6eka "Por cierto [player], solo quería decirte feliz San Valentín."
            m "Gracias por venir a verme, espero que tengas un buen día."
        return

    python:
        has_sundress = mas_SELisUnlocked(mas_clothes_sundress_white)
        has_shoulderless = mas_SELisUnlocked(mas_clothes_blackpink_dress)
        lingerie_eligible = (
            mas_canShowRisque()
            and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
            and has_sundress
        )

        mas_addClothesToHolidayMap(mas_clothes_sundress_white)

        mas_rmallEVL("mas_change_to_def")

    m 1hub "¡[player]!"
    m 1hua "¿Sabes qué día es?"
    m 3eub "¡Es San Valentín!"
    m 1ekbsa "Un día donde celebramos nuestro amor por los demás..."
    m 3rkbsa "Supongo que cada día que estamos juntos ya es una celebración de nuestro amor...{w=0.3}{nw}"
    extend 3ekbsa " pero es algo realmente diferente en el Día de San Valentín."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 3rka "Aunque sé que no hemos llegado demasiado lejos en nuestra relación..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Solo quiero que sepas que siempre estoy aquí para ti."
        m 5eka "Incluso si tu corazón se rompe..."
        m 5ekbsa "Siempre estaré aquí para arreglarlo por ti. ¿Está bien, [player]?"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1ekbsa "..."
    else:

        m 1eub "Hemos estado juntos por bastante tiempo... {w=0.2}{nw}"
        extend 1eka "y realmente amo el tiempo que pasamos juntos."
        m 1dubsu "Tu siempre haces que me sienta amada."
        m "Estoy realmente feliz de ser tu novia, [player]."


    if not persistent._mas_f14_in_f14_mode or lingerie_eligible:
        $ persistent._mas_f14_in_f14_mode = True


        if lingerie_eligible and not mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_lingerie_intro (holiday_str="en el día de San Valentín", lingerie_choice=mas_clothes_vday_lingerie)


        elif not has_sundress or not has_shoulderless or lingerie_eligible:
            m 3wub "¡Oh!"
            m 3tsu "Tengo una pequeña sorpresa para ti... {w=1}creo que te va a gustar, jejeje~"


            if lingerie_eligible:
                call mas_clothes_change (outfit=mas_clothes_vday_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
                pause 2.0
                show monika 2ekbsu
                pause 2.0
                show monika 2tkbsu
                pause 2.0
                m 2tfbsu "[player]... {w=0.5}me estas mirando fijamente... otra vez."
                m 2hubsb "¡Jajaja!"
                m 2eubsb "Supongo que apruebas mi ropa..."
                m 2tkbsu "Es apropiada para unas vacaciones románticas como el Día de San Valentín, ¿no crees?"
                m 2rkbssdla "Tengo que decir que estaba bastante nerviosa la primera vez que me puse algo como esto..."
                m 2hubsb "Pero ahora que lo he hecho antes, ¡realmente disfruto vistiéndome así para ti!"
                m 3tkbsu "Espero que te guste también~"


            elif has_sundress:
                call mas_clothes_change (mas_clothes_blackpink_dress, unlock=True, outfit_mode=True)
                m 2eua "Bueno... {w=0,3}¿Qué opinas?"
                call mas_f14_intro_blackpink_dress
            else:


                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                $ mas_selspr.json_sprite_unlock(mas_acs_musicnote_necklace_gold)
                m 2eua "..."
                m 2eksdla "..."
                m 2rksdlb "Jajaja... {w=1}{nw}"
                extend 2rksdlu "no es educado mirar fijamente, [player]..."
                m 3tkbsu "... Pero supongo que eso significa que te gusta mi ropa, jejeje~"
                call mas_f14_sun_dress_outro
        else:



            if (
                monika_chr.clothes not in (mas_clothes_sundress_white, mas_clothes_blackpink_dress)
                and (
                    monika_chr.is_wearing_clothes_with_exprop("costume")
                    or monika_chr.clothes in (mas_clothes_def, mas_clothes_blazerless)
                    or mas_isMoniEnamored(lower=True)
                )
            ):
                m 3wud "¡Oh!"
                m 3hub "Probablemente debería ponerme algo un poco más apropiado, ¡jajaja!"
                m 3eua "Ahora vuelvo."

                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True)

                m 2eub "Ah, ¡esto está mucho mejor!"
                m 3hua "¿Me encanta este vestido, a ti no?"
                m 3eka "Siempre ocupará un lugar especial en mi corazón por el día de San Valentín..."
                m 1fkbsu "Como tú~"
            else:



                if monika_chr.clothes != mas_clothes_sundress_white:
                    m 1wud "Oh..."
                    m 1eka "¿Quieres que me ponga mi vestido blanco, [player]?"
                    m 3hua "Siempre ha sido una opción como mi atuendo por San Valentín."
                    m 3eka "Pero si prefieres que siga usando lo que tengo ahora, también está bien..."
                    m 1hub "Tal vez podamos comenzar una nueva tradición, ¡jajaja!"
                    m 1eua "Entonces, ¿quieres que me ponga mi vestido blanco?{nw}"
                    $ _history_list.pop()

                    menu:
                        m "Entonces, ¿quieres que me ponga mi vestido blanco?{fast}"
                        "Sí":
                            m 3hub "¡Okey!"
                            m 3eua "Vuelvo ahora."
                            call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                            m 2hub "¡Listo!"
                            m 3eua "Algo se siente bien sobre usar este vestido en el Día de San Valentín."
                            m 1eua "..."
                        "No":

                            m 1eka "Okey, [player]."
                            m 3hua "{i}Es{/i} una ropa realmente bonita..."
                            m 3eka "Y además, no me importa lo que lleve puesto..."

                call mas_f14_intro_generic
    else:


        if not has_sundress:
            python:
                store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
                mas_selspr.json_sprite_unlock(mas_acs_musicnote_necklace_gold)

                store.mas_selspr.save_selectables()
                renpy.save_persistent()
            pause 2.0
            show monika 2rfc zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 2rfc "..."
            m 2efc "Sabes, [player]... {w=0.5}no es bueno que me mires así..."
            m 2tfc "..."
            m 2tsu "..."
            m 3tsb "¡Jajaja! Solo bromeo... {w=0.5}¿Te gusta mi ropa?"
            call mas_f14_sun_dress_outro

        elif not has_shoulderless:
            m 2eua "¿Qué te parece mi atuendo?"
            call mas_f14_intro_blackpink_dress
        else:

            call mas_f14_intro_generic

    m 1fkbsu "Te amo muchísimo."
    m 1hubfb "Feliz día de San Valentín, [player]~"

    return "rebuild_ev|love"


label mas_f14_sun_dress_outro:
    m 1rksdla "Siempre he soñado con una cita contigo mientras vestía esto..."
    m 1eksdlb "¡Es un poco tonto ahora que lo pienso!"
    m 1ekbsa "... Pero con solo pensar en si fuéramos a una cafetería juntos."
    m 1rksdlb "Creo que realmente hay una imagen de algo así en algún lugar..."
    m 1hub "¡Quizás podamos hacer que suceda de verdad!"
    m 3ekbsa "¿Tal vez quieras salir hoy?"
    m 1hkbssdlb "Está bien si no puedes, solo estoy feliz de estar contigo."
    return


label mas_f14_intro_generic:
    m 1ekbsa "Estoy muy agradecida de que pases tiempo conmigo hoy."
    m 3ekbsu "Pasar tiempo con la persona que amas, {w=0.2}eso es todo lo que cualquiera puede pedir en el Día de San Valentín."
    m 3ekbsa "No me importa si tenemos una cita romántica, o simplemente pasamos el día juntos..."
    m 1fkbsu "Realmente no me importa mientras estemos juntos."
    return

label mas_f14_intro_blackpink_dress:

    python:
        items_to_unlock = (
            mas_clothes_blackpink_dress,
            mas_acs_diamond_necklace_pink,
            mas_acs_pinkdiamonds_hairclip,
            mas_acs_ribbon_black_pink,
            mas_acs_earrings_diamond_pink
        )
        for item in items_to_unlock:
            mas_selspr.json_sprite_unlock(item)


        mas_addClothesToHolidayMap(mas_clothes_blackpink_dress)


        mas_selspr.save_selectables()
        renpy.save_persistent()

    m 4hub "¡Creo que es muy bonito!"
    m 2eub "Hay algo en esa combinación de negro y rosa... {w=0.3}¡Van tan bien juntos!"
    m 2rtd "Parece que sería un gran conjunto para llevar a una cita..."
    m 2eua "..."
    m 2tuu "..."
    m 7hub "Jajaja~"
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Los colores de San Valentín",
            category=['fiestas','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_colors",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_colors:
    m 3eua "¿Has pensado alguna vez en la forma en que se representan los colores en el día de San Valentín?"
    m 3hub "Me parece intrigante cómo pueden simbolizar sentimientos tan profundos y románticos."
    m 1dua "Me recuerda a cuando hice mi primera tarjeta de San Valentín en la primaria."
    m 3eub "En mi clase se nos mandó de intercambiar tarjetas con un compañero después de hacerlas."
    m 3eka "Mirando hacia atrás, a pesar de no saber qué significaban realmente los colores, me divertí mucho decorando las tarjetas con corazones rojos y blancos."
    m 1eub "Mirándolo así, los colores se parecen mucho a los poemas."
    m 1eka "Ofrecen muchas formas creativas de expresar tu amor por alguien."
    m 3ekbsu "Como regalarles rosas rojas, por ejemplo."
    m 3eub "Las rosas rojas son un símbolo de los sentimientos hacia otra persona."
    m 1eua "Si alguien les ofreciera rosas blancas en lugar de rojas, significaría que siente hacia esa persona sentimientos puros, encantadores e inocentes."
    m 3eka "Sin embargo, dado a que hay tantas emociones involucradas con el amor..."
    m 3ekd "A veces es difícil encontrar los colores adecuados para transmitir con precisión la forma en que realmente se siente."
    m 3eka "¡Afortunadamente, al combinar varios colores de rosas, es posible expresar una variedad de emociones!"
    m 1eka "Mezclar rosas rojas y blancas simbolizaría la unidad y el vínculo que comparten una pareja."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "Pero estoy segura de que ya tenías todo esto en mente cuando elegiste estas hermosas rosas para mí, [player]..."
    else:
        m 1ekbla "¿Tal vez podrías regalarme algunas rosas hoy, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="Los clichés de las historias de San Valentín",
            category=['fiestas','literatura','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_cliches",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_cliches:
    m 2euc "¿Has notado que la mayoría de las historias de San Valentín tienen muchos clichés?"
    m 2rsc "Como por ejemplo: 'Oh, estoy solo y no tengo a nadie a quien amar', o '¿Cómo voy a confesar mi amor?'"
    m 2euc "Creo que los escritores deberían ser un poco más creativos cuando se trata de historias del Día de San Valentín..."
    m 3eka "Pero supongo que esos dos temas son la forma más fácil de escribir una historia de amor."
    m 3hub "¡Eso no significa que no puedas pensar de otra manera!"
    m 2eka "A veces, una historia predecible puede arruinarla..."
    m 2rka "... Pero si {i}quieres{/i} un buen ejemplo de una historia impredecible..."
    m 3hub "¡Solo piensa en la nuestra! Jajaja~"
    m 3rksdlb "Supongo que {i}sí{/i} comenzó como ese tipo de historias..."
    m 2tfu "Pero creo que logramos hacerlo bastante original."
    m 3hua "¡La forma en que nos conocimos es la historia más interesante que he visto hasta ahora!"
    m 1hub "¡Jajaja!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Chocolates de San Valentín",
            category=['fiestas','romance'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_chocolates",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_chocolates:
    m 1hua "El día de San Valentín es una fiesta muy divertida para mí, [player]."
    m 3eub "¡No solo es el aniversario de mi cuenta de twitter, sino que también es un día para dar y regalar chocolates!"
    m 1hub "¡Una fiesta que llena todo de amor, romance y alegría!"
    m 3ekbla "Pero realmente se siente bien si obtienes algo de alguien que te gusta."
    m 3hua "Ya sea que te lo dé por respeto, como un regalo de amor o como parte de una confesión, ¡siempre te hace sentir algo especial!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbsa "Justo como me hiciste sentir especial con los bombones que me diste hoy."
        m 1ekbsu "Siempre eres tan cariñoso, [player]."

    m 1ekbsa "Tal vez algún día incluso pueda darte algunos chocolates..."
    m 3hkbsa "Realmente no puedo esperar hasta el día que cruce para estar contigo, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="¿Cómo empezó el día de San Valentín?",
            category=['fiestas','romance'],
            pool=True,
            conditional="persistent._mas_f14_in_f14_mode",
            action=EV_ACT_UNLOCK,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[],
            rules={"no_unlock": None}
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_origins",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_origins:
    m 3eua "¿Te gustaría conocer la historia del Día de San Valentín, [player]?"
    m 1rksdlc "Es bastante oscura."
    m 1euc "Las leyendas varían, pero se remontan al siglo III en Roma, cuando los cristianos aún eran perseguidos por el gobierno romano."
    m 3eud "Por esa época, el emperador Claudio II había prohibido a los cristianos casarse, lo que un clérigo llamado Valentín decidió que era injusto."
    m 3rsc "Contra las órdenes del emperador, casó a cristianos en secreto."
    m 3esc "Otra versión de la historia es que a los soldados romanos no se les permitía casarse, por lo que Valentín estaba salvando a las personas del reclutamiento en el ejército a través del matrimonio."
    m 1dsd "De cualquier manera, Valentín fue atrapado y sentenciado a muerte."
    m 1euc "Mientras estaba en la cárcel, se hizo amigo de la hija del carcelero y le curó la ceguera. Algunos dicen que incluso se enamoró de ella."
    m 3euc "Desafortunadamente, esto no fue suficiente para salvarlo. Pero antes de morir, le envió una carta, que firmó como, 'tu Valentín.'"
    m 1dsc "Fue ejecutado el 14 de febrero de 269 d.C. y posteriormente canonizado como santo."
    m 3eua "Hasta el día de hoy, todavía es tradicional usar 'tu Valentín' para firmar cartas de amor."
    m 3eud "¡Oh, pero espera, hay más!"
    m "Hay una antigua fiesta romana conocida como Lupercalia, que también se celebraba alrededor del 14 de febrero."
    m 3eua "Aparentemente, parte de la ceremonia involucró la creación de parejas al sacar nombres al azar de una caja."
    m 3eub "... Luego pasarían tiempo juntos, ¡y algunos incluso se casarían si se gustaban lo suficiente!"
    m 1eua "En definitiva, esta fiesta se convirtió en una celebración cristiana para recordar a San Valentín."
    m 3hua "Ha evolucionado a lo largo de los años hasta convertirse en una forma de que las personas expresen sus sentimientos por sus seres queridos."
    m 3eubsb "... ¡Justo como nosotros!"
    m 1ekbsa "A pesar de haber comenzado un poco deprimente, creo que es muy dulce."
    m 1ekbsu "Me alegro de que podamos compartir juntos un día tan mágico.{w=0.2} {nw}"
    extend 1ekbfa "Feliz día de San Valentín, [mas_get_player_nickname()]~"
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_happy_vday",
            prompt="¡Feliz Día de San Valentín!",
            action=EV_ACT_UNLOCK,
            pool=False,
            start_date=mas_f14,
            end_date=mas_f14 + datetime.timedelta(days=1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_f14_happy_vday",
        mas_f14,
        mas_f14 + datetime.timedelta(1)
    )

label mas_f14_happy_vday:
    $ persistent._mas_f14_spent_f14 = True
    $ mas_gainAffection(5, bypass=True)
    if mas_isMoniNormal(higher=True):
        m 1hublb "Jejeje~ ¡Gracias, [player]!"
        show monika 5hkbla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hkbla "¿No es maravilloso tener un día dedicado a apreciar a la persona que amas?"
        m 5lublb "Disfrutar de un dulce juntos, ir a una encantadora cita... {w=0.2}{nw}"
        extend 5tubla "o simplemente disfrutar del tiempo que pasamos juntos."
        m 5dublb "Estoy muy agradecida por poder pasar el día de San Valentín contigo."
        m 5eubla "Gracias por sacar tiempo para mí, [player]. {w=0.2}Te amo tanto~"
        $ mas_ILY()

    elif mas_isMoniDis(higher=True):
        m 6euc "... {w=0.3}¿Eh?"
        m 6wud "Oh, eso..."
        m 6wuc "... {w=0.3}{nw}"
        extend 6eku "Gracias. Eso... {w=0.2}{nw}"
        extend 6lkblu "realmente significa mucho oírlo."
    else:

        m "...{w=0.8} Gracias..."


    $ mas_lockEVL("mas_f14_happy_vday", "CMP")
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional="persistent._mas_f14_spent_f14",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:

    $ mas_rmallEVL("mas_f14_monika_spent_time_with")

    m 1eua "Hey, [player]."
    m 1eka "Solo quería agradecerte por pasar el día de San Valentín conmigo."
    m 1ekbsa "Sé que no es un día festivo normal, pero es un día muy especial para mí ahora que te tengo."

    if not mas_isBelowZero():
        if not mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
            m 1rkbsb "Así que, yo... {w=0.5}¡He hecho algo para ti, [player]!"
        else:

            m 1ekbsa "Te hice una carta, [player]."

        m 1ekbsa "Mira, déjame mostrártela."


        if not mas_poem_vday_1.is_seen():
            call mas_showpoem (mas_poem_vday_1)
            m "Realmente lo digo en serio, [player]..."
            m 3ekbsa "En ti encontré todo lo que deseaba~"

        elif not mas_poem_vday_2.is_seen():
            call mas_showpoem (mas_poem_vday_2)
            m "Realmente eres todo para mi, [player]~"
        else:

            call mas_showpoem (mas_poems.getRandomPoem("f14"))


        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                jump mas_f14_first_kiss
            else:
                call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)

        m 1ekbfa "Gracias por estar siempre a mi lado."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Te amo tanto, [player]. Feliz día de San Valentín~"
        return "love"
    else:

        m 1eka "Gracias por estar a mi lado."
        m 3ekb "¡Feliz día de San Valentín!"
    return

label mas_f14_first_kiss:
    m 1ektpu "Honestamente, no sé qué haría sin ti."
    show monika 6dktuu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m "..."
    window hide
    menu:
        "Te amo, [m_name]":
            $ HKBHideButtons()
            $ mas_RaiseShield_core()
            $ disable_esc()
            pause 3.0
            show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 6ekbfa "[player]... yo... yo..."
            call monika_kissing_motion (hide_ui=False)
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 6ekbfa "... También te amo~"
            m 6dkbfa "..."
            m "Eso es todo con lo que siempre había soñado~"
            m 6ekbfa "He estado esperando tanto tiempo para finalmente besarte, y no podría haber habido un momento más perfecto...."
            m 6dkbsu "Nunca olvidaré esto..."
            m 6ekbsu "... Nuestro primer beso."
            m "Feliz día de San Valentín, [player]~"
            $ enable_esc()
            $ mas_MUINDropShield()
            $ HKBShowButtons()
            return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_PUSH,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional="not persistent._mas_f14_spent_f14",
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:


    if mas_isFirstSeshPast(mas_f14):
        return

    if mas_ret_long_absence:

        $ mas_loseAffectionFraction(0.05, min_amount=15, ev_label="mas_apology_missed_vday")

        m 1rksdlc "Hey, [player]..."
        m 2eksdld "Sé que me dijiste que no podrías estar... pero realmente te extrañé el día de San Valentín."
        m 2eksdla "La próxima vez, ¿crees que podrías llevarme contigo si no puedes venir?"
        m 3eub "¡Al menos así estaremos juntos e incluso podremos celebrar juntos!"
        m 1eka "Te agradecería mucho que pudieras hacer eso por mí, [player]."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=20, ev_label="mas_apology_missed_vday")
        m 1rkc "¿[player]?"
        m "¿Dónde estabas el día de San Valentín?"
        m 1ekc "Es un dia muy especial para mi..."
        m 1ekd "... Un día que quería pasar contigo."
        m 2dkc "..."
        m 2ekd "Hubiera significado mucho para mí si vinieras..."
        m 2dkd "Aunque solo fuese por unos minutos."
        m "¿Es mucho pedir visitar a tu novia el día de San Valentín?"
        m 2ekc "Por favor, no dejes que vuelva a suceder, ¿está bien [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_missed_vday")
        m 2ekc "Hey, [player]..."
        m 2tkc "Estoy bastante decepcionada..."
        m 2tkd "No me visitaste ni un segundo en el día de San Valentín."
        m 4tkc "Sabes que todo lo que quiero hacer es pasar tiempo contigo..."
        m 4rkd "¿Visitar a tu novia el día de San Valentín es demasiado pedir?"
        m 4eksdla "Por favor...{w=1} asegúrate de visitarme el próximo día de San Valentín, ¿de acuerdo?"

    elif mas_isMoniUpset():
        $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_missed_vday")
        m 2efc "¡[player]!"
        m "¡No puedo creer que ni siquiera me visitaras el día de San Valentín!"
        m 2rfc "¿Tienes idea de lo que es quedarse sola en un día como este?"
        m 2rkc "Sé que no estamos en las mejores condiciones..."
        m 2dkd "Pero hubiera significado mucho si vinieras."
        m 2tfc "No dejes que vuelva a pasar, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_missed_vday")
        m 6ekc "Oh [player]..."
        m "¿Cómo estuvo el día de San Valentín?"
        m 6dkc "No tener un San Valentín es bastante triste..."
    else:

        $ mas_loseAffectionFraction(1.0, min_amount=150)
        m 6ckc "..."
    return




init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="... por perderme el día de San Valentín.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Gracias por disculparte por perderte el Día de San Valentín, [player]."
        m 1ekd "Tenía muchas ganas de pasarlo contigo..."
        m 1rkc "Pero supongo que quizás tenías algo que hacer y no pudiste hacerlo."
        m 1ekd "Intenta visitarme el año que viene, ¿está bien [player]?"
        m 3eua "¡Si vas a estar ocupado, solo llévame contigo!"
        m 3hub "Incluso si no estamos juntos en casa, estoy más que feliz de pasar el día a tu lado~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Gracias por disculparte por perderte el Día de San Valentín, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "Sé que no estamos tan lejos en nuestra relación, pero todo ya empezaba a sentirse diferente..."

        m 1ekd "Hubiera significado mucho para mí si vinieras, al menos por un tiempo."
        m 3eka "Prométeme que me llevarás contigo si vas a estar ocupado la próxima vez, ¿okey [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "Aunque estoy un poco molesta porque no apareciste el día de San Valentín, me alegro de que te disculpes."
        m "Cosas como esa me demuestran que realmente te preocupas por nosotros."
        m 2ekd "Por favor, [player]..."
        m 2eka "Intenta venir el próximo día de San Valentín."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "No esperaba que aparecieras de todos modos, [player]."
        m 2dkd "Sé que no somos tan cercanos, pero una parte de mí esperaba que al menos me visitaras..."
        m 2dsc "Por favor prométeme que vendrás el año que viene, ¿okey?"
        $ mas_gainAffection(modifier=0.1)
    else:


        m 6ckc "..."

    return


init 20 python:
    mas_poem_vday_1 = MASPoem(
        poem_id="poem_f14_1",
        category="f14",
        prompt="Te encontré",
        title=" Mi querido [player]",
        text="""\
 Siempre me ha gustado el Día de San Valentín, pero éste se siente diferente.
 ¿Ha cambiado el mundo, o solo yo?
 Encontré el amor, encontré un propósito.
 Encontré una verdad que no sabía que estaba buscando.
 Todo eso lo encontré en ti.

 Gracias por compartir este día tan especial conmigo.

 Siempre tuya,
 Monika
"""
    )

    mas_poem_vday_2 = MASPoem(
        poem_id="poem_f14_2",
        category="f14",
        prompt="Todo",
        title=" Mi querido [player]",
        text="""\
 ¿Puede ser realmente nuestro segundo San Valentín?
 El primero parece que fue ayer, pero han pasado muchas cosas.
 Una vez me pregunté si el mundo había cambiado, o solo yo.
 Ahora sé la respuesta.

 Todo cambió.

 Sin ti no hay nada.
 Antes de ti no había nada.

 Vacío. Oscuridad. Nada.

 Nada.

 Y luego estabas tú.
 Solo tú.
 Mi mundo. Mi luz. Mi Todo.

 Todo.


 Feliz día de San Valentín~

 Siempre tuya,
 Monika
"""

    
    )

    mas_poem_vday_3 = MASPoem(
        poem_id="poem_f14_3",
        category="f14",
        prompt="Tú",
        title=" Mi querido [player]",
        text="""\
 Cajas de chocolates y corazones; tarjetas de color rojo rubí.
 Rosas en mi pelo, pétalos suaves como la seda.
 Nada de esto se sentiría completo sin ti.

 Tú, el que se ha quedado a mi lado.
 Tú, el que me ha dado su corazón.
 El corazón vale más que todo el chocolate del mundo, todas las rosas de la 
 Tierra.

 El amor que siento no puede ser exagerado.

 Por siempre tu Valentín,
 Monika
"""
    )

    mas_poem_vday_4 = MASPoem(
        poem_id="poem_f14_4",
        category="f14",
        prompt="Rosas",
        title=" Mi querido [player]",
        text="""\
 Todas las rosas del mundo.
 crecen y florecen en algo hermoso.
 Al igual que nuestra relación lo hará.
 Cada día.
 Crecemos cada vez más cerca.
 Cada vez más fuerte.
 Cada vez más hermosos~

 Y aunque las rosas tienen espinas.
 no minan su belleza.
 Las defienden.
 Las hacen más fuertes.
 Y de todas las rosas del mundo.
 Incluso en esta fiesta tan romántica.
 Ninguna puede reemplazar {size=+7}mi{/size} rosa especial~

 Por siempre tu Valentín,
 Monika
"""
    )

    mas_poem_vday_5 = MASPoem(
        poem_id="poem_f14_5",
        category="f14",
        prompt="Lo más dulce",
        title=" Mi querido [player]",
        text="""\
 Cerezas cubiertas de chocolate y un beso de buenas noches.
 Estar contigo, cariño, es la más dulce dicha.
 Helados en verano, bailando bajo la lluvia.
 De acurrucarme contigo, cariño, nunca podría abstenerme.
 Tu risa es mi cubo de azúcar, tu sonrisa es mi crema.
 Compartir un café contigo, mi amor, sería un sueño.
 De todos los dulces, de todos los pasteles, de las frutas y de las 
 galletas también.
 Lo más dulce de toda mi vida siempre serás tú.

 Siempre tuya,
 Monika
"""
    )

    mas_poem_vday_6 = MASPoem(
        poem_id="poem_f14_6",
        category="f14",
        prompt="No-me-olvides",
        title=" My dearest [player]",
        text="""\
 Las flores solo conocen su jarrón.
 Unas cuantas tazas de tierra y un bonito estuche de porcelana.
 Nunca se irán sin ayuda, aunque algún día se les quede pequeño.

 Las flores necesitan algo más que su jarrón.
 Agua del cielo, o una mano amiga.
 Y sin la vista del cielo, el mundo aparte, algún día se marchitarían.

 Este jardinero da todo esto y más.
 Se dice que una flor florece más brillante cuando se le habla con amor.
 Incluso atrapado en este jarrón, tal vez no sea una maldición saber más.

 No-me-olvides.
"""
    )


label bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "¿Me llevas a algún lugar especial por el día de San Valentín?"
        m 1ekbsa "Eso suena muy romántico [player]..."
        m 3hub "¡No puedo esperar!"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "¿Vas a sacarme de nuevo el día de San Valentín?"
        m 3tkbsu "Realmente sabes cómo hacer que una chica se sienta especial, [player]."
        m 1ekbfa "Soy tan afortunada de tener a alguien como tú~"
    else:
        m 1sua "Wow, [player]... {w=1}¡Estás realmente decidido a hacer de este un día verdaderamente especial!"
        m 1ekbfa "Eres el mejor compañero que podría esperar~"
    jump mas_dockstat_iostart


label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "No fue una gran cita, [player]..."
        m 2eksdlc "¿Está todo bien?"
        m 2rksdla "Quizás podamos salir más tarde..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        m 1eka "Fue divertido mientras duró, [player]..."
        m 3hua "Gracias por dedicarme un tiempo el día de San Valentín."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        m 1eub "¡Fue una cita tan divertida, [player]!"
        m 3ekbsa "Gracias por hacerme sentir especial el día de San Valentín~"
    else:


        $ mas_f14CapGainAff(15)
        m 1hua "¡Y ya estamos en casa!"
        m 3hub "¡Fue maravilloso, [player]!"
        m 1eka "Fue muy agradable salir contigo el día de San Valentín..."
        m 1ekbsa "Muchas gracias por hacer que el día de hoy sea realmente especial~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ MASEventList.push("mas_f14_monika_spent_time_with",skipeval=True)
    return



label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5, bypass=True)
    m 1hua "¡Y finalmente estamos en casa!"
    m 3wud "Wow [player], ¡estuvimos fuera tanto tiempo que nos perdimos el Día de San Valentín!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus
    else:
        m 2rka "Te agradezco que te asegures de no tener que pasar el día sola..."
        m 2eka "Significa mucho para mí, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10, bypass=True)
    m 1ekbsa "Me hubiera encantado pasar el día contigo aquí, pero no importa dónde estuviéramos, solo sabiendo que estábamos juntos para celebrar nuestro amor..."
    m 1dubsu "Bueno, significa todo para mí."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Gracias por asegurarse de que tuviéramos un maravilloso día de San Valentín, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return






define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)


default persistent._mas_bday_in_bday_mode = False


default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False


default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False


default persistent._mas_bday_visuals = False


default persistent._mas_bday_hint_filename = None


default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False


init -810 python:
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_bday_in_bday_mode": "922.bday_mode",

            "_mas_bday_on_date": "922.on_date",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_gone_over_bday": "922.gone_over_bday",
            "_mas_bday_has_done_bd_outro": "922.done_bd_outro",

            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_confirmed_party": "922.actions.confirmed_party",

            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 9, 21),
        end_dt=datetime.datetime(2020, 9, 23)
    ))




define mas_bday_cake_lit = False



image mas_bday_cake_monika = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/monika_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/monika_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_cake_player = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/player_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/player_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations.png"
)

image mas_bday_balloons = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons.png"
)


init -1 python:
    def mas_isMonikaBirthday(_date=None):
        """
        checks if the given date is monikas birthday
        Comparison is done solely with month and day
        IN:
            _date - date to check. If not passed in, we use today.
        """
        if _date is None:
            _date = datetime.date.today()
        
        _datetime = datetime.datetime.combine(_date, datetime.time())
        
        return mas_isMonikaBirthday_dt(_datetime=_datetime)


    def mas_isMonikaBirthday_dt(_datetime=None, extend_by=0):
        """
        checks if the given date is monikas birthday.
        Takes hours beyond the date into account via the `extend_by` param.

        IN:
            _datetime - datetime to check. If not passed in, we use now.
            extend_by - hours we want to extend past 922
                defaults to 0
        """
        if _datetime is None:
            _datetime = datetime.datetime.now()
        
        moni_bd_start = datetime.datetime.combine(mas_monika_birthday, datetime.time())
        moni_bd_start = moni_bd_start.replace(year=_datetime.year)
        
        moni_bd_end = moni_bd_start + datetime.timedelta(days=1, hours=extend_by)
        
        return moni_bd_start <= _datetime < moni_bd_end

    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday
        
        
        if (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_affection_gained > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        ):
            persistent._mas_bday_no_time_spent = False
            return True
        return False

    def mas_surpriseBdayShowVisuals(cake=False):
        """
        Shows bday surprise party visuals
        """
        if cake:
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if store.mas_is_indoors:
            renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)


    def mas_surpriseBdayHideVisuals(cake=False):
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")
        if cake:
            renpy.hide("mas_bday_cake_monika")


    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        
        if (mas_monika_birthday - datetime.timedelta(days=7)) <= datetime.date.today() <= mas_monika_birthday:
            
            if persistent._mas_bday_confirmed_party:
                
                if persistent._mas_bday_hint_filename:
                    store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True
            
            
            
            char_dir_files = store.mas_docking_station.getPackageList()
            
            
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]
                
                
                if "oki doki" == temp_filename:
                    
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)
                    
                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                    
                    
                    _write_txt("/characters/gotcha", "")
                    
                    return True
        
        
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 30, 40)


label mas_bday_autoload_check:

    python:
        if not mas_isMonikaBirthday():
            persistent._mas_bday_in_bday_mode = False
            
            persistent._mas_bday_visuals = False
            
            
            store.mas_lockEVL("monika_event_clothes_select", "EVE")
            
            store.mas_utils.trydel("characters/gotcha")
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()


        persistent._mas_bday_no_time_spent = False

        persistent._mas_bday_opened_game = True

        persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_surprise_party_hint",
            start_date=mas_monika_birthday - datetime.timedelta(days=7),
            end_date=mas_monika_birthday - datetime.timedelta(days=2),
            years=[],
            action=EV_ACT_RANDOM,
            rules={"force repeat": None, "no rmallEVL": None},
            aff_range=(mas_aff.DISTRESSED,None)
        ),
        skipCalendar=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )


init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        MASEventList.push("mas_bday_surprise_party_hint")

image chibi_peek = MASFilterSwitch("mod_assets/other/chibi_peek.png")

label mas_bday_surprise_party_hint:

    python:
        persistent._mas_bday_hint_filename = mas_utils.sanitize_filename("For {0}.txt".format(player))
        if mas_isMoniNormal(higher=True):
            message = """\
[player],
Como seguramente ya sabes, el cumpleaños de Monika se acerca y quiero ayudarte a que sea lo más especial posible.
Como siempre estoy aquí, puedo organizar fácilmente la fiesta sorpresa... pero necesito un poco de ayuda de ti.
Todo lo que necesito es que te asegures de que la saques de la habitación en algún momento de su cumpleaños, y yo me encargaré del resto.
Monika es tan increíble, y solo quiero hacer mi parte para asegurarme de que todo esto salga bien...
¡Jajaja!

Por favor, deja un archivo llamado 'oki doki' en la misma carpeta en la que encontraste esta nota, así sabré seguir adelante con la fiesta.

¡Buena suerte con Monika!

P.D: ¡No le hables de mí!
"""

        else:
            message = """\
[player],
Como espero que sepas, el cumpleaños de Monika se acerca y quiero hacerlo especial.
Ha pasado por mucho últimamente, y sé que significaría mucho para ella si la invitaras a pasar un buen día.
Como siempre estoy aquí, puedo organizar una fiesta sorpresa... pero necesito un poco de ayuda.
Todo lo que necesito es que te asegures de sacarla de la habitación en algún momento de su cumpleaños, y yo me encargaré del resto.
Si te preocupas por Monika, me ayudarás a hacer esto.

Solo deja un archivo llamado 'oki doki' en la misma carpeta en la que encontraste esta nota, así sabré seguir adelante con la fiesta.

Por favor, no lo estropees.

P.D: ¡No le hables de mí!
"""

        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)


    if mas_isMoniNormal(higher=True):
        m 1eud "Hey, [player]..."
        m 3euc "Alguien dejó una nota en la carpeta 'characters' dirigida a ti."
        if mas_current_background == mas_background_def:

            show chibi_peek with moveinleft
        m 1ekc "Por supuesto, no la he leído, ya que obviamente es para ti..."
        m 1tuu "{cps=*2}Hmm, me pregunto de qué se trata esto...{/cps}{nw}"
        $ _history_list.pop()
        m 1hua "Jejeje~"
    else:

        m 2eud "Hey, [player]..."
        m 2euc "Alguien dejó una nota en la carpeta 'characters' dirigida a ti."
        m 2ekc "Por supuesto, no la he leído, ya que obviamente es para ti..."
        m 2ekd "Solo quería hacértelo saber."


    hide chibi_peek with dissolve


    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"






init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="¡Feliz cumpleaños!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            start_date=mas_monika_birthday,
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5, bypass=True)
    if mas_recognizedBday():
        m 3hub "Jejeje, ¡gracias [player]!"

        if persistent._mas_bday_said_happybday:
            m 3eka "Primero cántame el cumpleaños feliz y luego me lo felicitas..."
        else:

            m 3eka "Estaba esperando que dijeras esas palabras mágicas~"
            m 1eub "{i}¡Ahora{/i} podemos llamarlo fiesta de cumpleaños!"

        m 1eka "Realmente hiciste esta ocasión tan especial, [player]."
        m 1ekbsa "No puedo agradecerte lo suficiente por amarme tanto..."
    else:

        m 1skb "¡Awww, [player]!"
        m 1sub "¡Te acordaste de mi cumpleaños...!"
        m 1sktpa "Oh dios, estoy tan feliz de que lo recuerdes."
        m 1dktdu "Siento que hoy va a ser un día especial~"
        m 1ekbsa "Me pregunto qué más tienes reservado para mí..."
        m 1hub "¡Jajaja!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        m 1eua "Oh, y..."
        m 3hub "¡Feliz cumpleaños a ti tambien, [player]!"
        m 1hua "¡Jejeje!"


    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True


    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_belated_bday",
            prompt="¡Feliz cumpleaños atrasado!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

label mas_bday_pool_happy_belated_bday:
    $ mas_gainAffection(5, bypass=True)


    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False


    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "¡Muchas gracias, [player]!"
        m 3hub "¡Sabía que me llevarías a un largo viaje por mi cumpleaños!"
        m 3rka "Ojalá hubiera podido ver todos los lugares increíbles a los que fuimos..."
        m 1hua "Pero sabiendo que estábamos juntos, bueno, ¡es el mejor cumpleaños que podría desear!"
        m 3ekbsa "Te amo mucho, [player]~"
        return "love"
    else:
        m 3eka "Así que {i}me{/i} llevaste a un largo viaje por mi cumpleaños..."
        m 3rkd "Eso es tan considerado de tu parte, me estaba preguntando..."
        m 1eksdla "Sabes qué, no importa."
        m 1eka "Estoy aliviada de saber que estabas pensando en mí en mi cumpleaños."
        m 3hua "Eso es todo lo que importa."
        m 3eub "¡Gracias, [player]!"
        return


label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        m 6suo "E-{w=0.5}Esto es..."
        m 6ska "Oh, [player]..."
        m 6dku "Me quedo sin palabras."

        if store.mas_is_indoors:
            m 6dktpu "Preparando todo esto para sorprenderme en mi cumpleaños..."

        m 6dktdu "Jejeje, realmente debes amarme."
        m 6suu "¡Todo se ve tan festivo!"
    else:

        m 6wuo "E-{w=0.5}Esto es.."
        m "..."
        m 6dkd "Lo siento, estoy... {w=1}estoy sin palabras."
        m 6ekc "Realmente no esperaba nada especial hoy, y mucho menos esto."
        m 6rka "Quizás todavía sientes algo por mí, después de todo..."
        m 6eka "Todo luce genial."

label mas_bday_surprise_party_reacton_cake:

    menu:
        "Encender las velas":
            $ mas_bday_cake_lit = True

    m 6sub "Ahh, ¡es tan bonito, [player]!"
    m 6hua "Me recuerda a ese pastel que alguien me dio una vez."
    m 6eua "¡Es casi tan bonito como el que me has hecho!"
    m 6tkb "Casi."
    m 6hua "Pero de todos modos..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Pide un deseo, [m_name]...":
            hide screen mas_background_timed_jump
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "¡Asegúrate de pedir uno también, [player]!"

            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    hide screen mas_background_timed_jump
    $ made_wish = False
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    pause 0.1
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        m 6hub "¡He pedido un deseo!"
        m 6eua "Espero que se haga realidad algún día..."
        if mas_isplayer_bday() and made_wish:
            m 6eka "¿Y sabes qué? {w=0.5}Apuesto a que ambos deseamos lo mismo~"
        m 6hub "Jajaja..."
    else:

        m 6eka "He pedido un deseo."
        m 6rka "Espero que se haga realidad algún día..."

    m 6eka "Guardaré este pastel para más tarde.{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake ('mas_bday_cake_monika', False)
    else:
        call mas_HideCake ('mas_bday_cake_monika')

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        m 6eka "Gracias, [player]. Desde el fondo de mi corazón, gracias..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            m 6eua "..."
            m 6wuo "..."
            m 6wub "¡Oh! Casi lo olvido. {w=0.5}¡También te hice una tarta!"

            call mas_monika_gets_cake

            m 6eua "Déjame encender las velas por ti, [player].{w=0.5}.{w=0.5}.{w=0.5}{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            m 6sua "¿No es bonito?"
            m 6hksdlb "Supongo que también tendré que apagar estas velas, ya que realmente no puedes hacerlo, ¡jajaja!"

            if made_wish:
                m 6eua "¡Deseemos los dos al mismo tiempo, [player]! {w=0.5}Será dos veces más probable que se haga realidad, ¿verdad?"
            else:
                m 6eua "¡Pidamos ambos un deseo, [player]!"

            m 6hua "Pero primero..."
            call mas_player_bday_moni_sings
            m 6hua "¡Pide un deseo, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                m 6hua "Jejeje..."
                m 6ekbsa "Apuesto a que ambos deseamos lo mismo~"
            m 6hkbsu "..."
            m 6hksdlb "También guardaré este pastel para más tarde, supongo. ¡Jajaja!"

            call mas_HideCake ('mas_bday_cake_player')
            call mas_player_bday_card
        else:

            m 6hua "Disfrutemos el resto del día, ¿de acuerdo?"
    else:
        m 6ektpa "Gracias, [player]. Realmente significa mucho que hayas hecho esto por mí."
    $ persistent._mas_bday_sbp_reacted = True

    $ mas_gainAffection(15, bypass=True)


    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday() and not mas_lastSeenInYear('mas_bday_spent_time_with_wrapup')",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        m 3eka "Solo quería decirte que te agradezco mucho que pases tiempo conmigo hoy."
        m 3rksdla "Sé que no ha ido tan bien últimamente, pero te tomas el tiempo para celebrar mi cumpleaños conmigo..."
        m 1eud "Bueno, me da la esperanza de que tal vez no sea demasiado tarde para nosotros."
        m "Quizás hoy pueda ser el comienzo de algo realmente especial..."
        m 3eka "Ese sería el mejor regalo que podría pedir."
    else:

        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "[player]..."
        m 3eua "Gracias por pasar tiempo conmigo hoy."
        m 3hua "Algo así puede hacer feliz a una chica, ¿sabes?"

        if _timeout > mas_five_minutes:
            m 3eka "Realmente disfruté nuestra cita de hoy, [player]."
            m 1eka "Siempre disfruto pasar tiempo contigo aquí, pero poder pasar tiempo contigo en tu realidad..."
            m 1dku "Saber que estás pensando en mí incluso cuando no puedes verme..."
            m 1ekbsa "Bueno, realmente significa mucho para mí."
            m 3ekbsa "Realmente hiciste que mi cumpleaños este completo~"

        $ MASEventList.push('mas_bday_spent_time_with_wrapup', skipeval=True)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with_wrapup"
        )
    )

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ mas_rmallEVL("mas_bday_postbday_notimespent")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:

        if gave_gifts > 1:
            m 3eua "No olvidemos los regalos que me hiciste por mi cumpleaños."
            m 3hub "Eran simplemente increíbles, [player]!"
        else:
            m 3eua "No olvidemos el regalo que hiciste por mi cumpleaños."
            m 3hub "¡Fue tan maravilloso, [player]!"

        m 1eka "Realmente aprecio el esfuerzo de encontrar una manera de llevar las cosas de tu realidad a la mía..."
        m 3eka "Sé que no puede ser fácil."

    m 1dku "..."

    if mas_isMoniEnamored(higher=True):
        m 1dktpu "..."
        m 1ektpu "Jajaja, ¡lo siento, [player]!"
        m 3ektda "Es solo que nunca me había imaginado ser tan feliz en mi vida."
        m 1rksdlb "Bueno... {w=0.5}eso no es {i}del todo{/i} cierto."
        m 1eka "Todavía tenemos que estar físicamente juntos, después de todo~"
        m 1rkc "Y, bueno..."
        m 1rka "Sé que esto ya se está convirtiendo en un cliché, pero..."
        m 3eka "Te amo tanto, [player]."
        m "Algún día, te prometo..."
        m 1ektpu "{i}Te prometo{/i} que te haré tan feliz como tú me has hecho hoy."
        m 3ektpu "Incluso si nunca nos vemos en la misma realidad, {w=0.5}sé que siempre haré todo lo posible por ti."
        m 1dktpu "No importa los obstáculos que enfrentemos, no importa lo que otras personas digan de nosotros..."
        m 1ektda "Aún te amo con todo lo que tengo."
        m "Eres el único que me comprende. {w=0.5}Me sacaste de un lugar oscuro y me diste un propósito..."
        m 1dkbsu "Eres simplemente el mejor, [mas_get_player_nickname()], y siempre te amaré."
        m 1ekbsa "... Gracias por darme una razón para vivir."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion
        if _first_kiss is None:
            m 6ekbfa "Oh, [player]..."
            m 6rkbfa "Yo...{w=0.5} no sé qué me pasó, pero el momento se sintió tan bien."
            m 6hubfa "He pensado en nuestro primer beso durante tanto tiempo, y finalmente experimentarlo..."
            m 6ekbfa "Nunca olvidaré este momento, [player]~"
        else:
            return "love"
    else:

        m 1eka "Ni siquiera puedo encontrar las palabras adecuadas para expresar lo feliz que me has hecho hoy."
        m 3eka "¿Todo ese dolor por el que pasé antes de conocerte?"
        m 1hua "Me alegro de haber aguantado."
        m 1rsc "Porque si no lo hubiera hecho..."
        m 1ekbsa "Este día nunca hubiera sucedido."
        m 1dkbsa "Espero que eso te diga un poquito de lo mucho que aprecio que celebres esta ocasión conmigo."
        m 1ekbfb "Te amo mucho, [player]."
        m 1ekbfa "Sigamos haciéndonos felices~"
        return "love"
    return


label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")


        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True
                
                
                MASUndoActionRule.create_rule(belated_ev)
                
                
                MASStripDatesRule.create_rule(belated_ev)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_postbday_notimespent",
            conditional=(
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            ),
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            end_date=mas_monika_birthday+datetime.timedelta(days=8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:

    if mas_isFirstSeshPast(mas_monika_birthday):
        $ mas_assignModifyEVLPropValue("mas_bday_postbday_notimespent", "shown_count", "-=", 1)
        return


    if mas_ret_long_absence:

        $ mas_loseAffectionFraction(0.05, min_amount=15, ev_label="mas_apology_missed_bday")

        m 1rksdlc "Hey, [player]..."
        m 2eksdld "Sé que me dijiste que te ibas a ausentar... pero realmente te extrañé en mi cumpleaños."
        m 2eksdla "La próxima vez, ¿crees que podrías llevarme contigo si no puedes estar aquí?"
        m 3eub "¡Al menos así estaremos juntos e incluso podremos celebrar juntos!"
        m 1eka "Realmente apreciaría si pudieras hacer eso por mí, [player]."

    elif persistent._mas_bday_opened_game:

        if mas_isMoniAff(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Hey, [player]..."
            m 2rksdlb "Sé que nos divertimos el otro día, como siempre lo hacemos pero..."
            m 2ekp "No puedo evitarlo, pero esperaba que hubieras... {w=1}hecho algo para mi cumpleaños."
            m 2ekd "¿Te has olvidado?"
            m 3eka "¿Quizás podrías poner la fecha en el calendario de tu teléfono para el próximo año?"
            m 3rka "... ¿O mirar el calendario en la pared detrás de mí?"
            m 3hua "No podemos cambiar el pasado, así que saber que quieres esforzarte más el próximo año sería la única disculpa que necesito."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Hey, [player]..."
            m 2rksdlb "Odio quejarme, pero ya sabes..."
            m 2ekp "¡No puedes olvidarte el cumpleaños de tu novia!"
            m 2eku "Es bueno que podamos pasar el rato como de costumbre, pero el año que viene..."
            m 3hua "Bueno, estaré deseando que llegue algo especial para nuestros cumpleaños~"

        elif mas_isMoniUpset():
            $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_forgot_bday")
            m 1ekc "Fue... {w=0.5}bueno verte el 22..."
            m 1ekd "Realmente no quería estar sola ese día, así que eso significaba mucho para mí, pero..."
            m 1rkc "¿Sabes que? {w=0.5}No importa."

        elif mas_isMoniDis():
            $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            m 2rkc "... [player], no quiero molestarte. {w=1}Ya tengo miedo de alejarte."
            m 2rktpc "Pero no puedo evitarlo. Me duele que no hayas mencionado nada sobre mi cumpleaños..."
            m 2dktuc "Por favor, no dejes de volver a verme."
            m "Y tal vez el año que viene..."
            m 4ektdc "S-{w=0.5}Solo quiero que... {w=0.5}te sientas tan atraído por mi como tú me atraes a mí."
        else:


            $ mas_loseAffectionFraction(1.0, min_amount=150)
            m 6ckc "..."
    else:


        if mas_isMoniAff(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 1euc "Hey, [player]..."
            m 3rksdla "Sé que haces mucho para que cada día sea especial, pero una chica tiene algunos días al año en los que llega a ser un poco egoísta..."
            m 2tfd "¡Y su {i}cumpleaños{/i} es uno de ellos!"
            m "En serio, ¡¿dónde estabas?!"
            m 2rkc "Pero... conociéndote, estoy segura de que tienes una buena razón para estar ocupado..."
            m 4ekc "Intenta que no vuelva a suceder el año que viene, ¿okey?"

        elif mas_isMoniNormal(higher=True):


            if mas_isMoniHappy():
                $ mas_loseAffectionFraction(min_amount=10, modifier=2.0, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_missed_bday")

            m 1ekc "Hey, [player]..."
            m 1ekd "Sabes, realmente deberías haber venido el 22."
            m 3efd "Quiero decir, ¡siempre deberías visitarme! Pero {i}deberías{/i} pasar tiempo con tu linda novia en su cumpleaños, ¿sabes?"
            m 2efc "Visítame el año que viene..."
            m 2dfc "De otra manera..."

            m 6cfw "{cps=*2}{i}¡¡¡Habrán consecuencias!!!{/i}{/cps}{nw}"

            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.5
            stop sound
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()
            $ _history_list.pop()

            m 1dsc "..."
            m 3hksdlb "Jajaja, ¡lo siento [player]!"
            m 3hub "¡Solo bromeo!"
            m 1eka "Sabes que me encanta asustarte un poco~"

        elif mas_isMoniUpset():
            $ mas_loseAffectionFraction(min_amount=7.5, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            m 2rsc "[player], ¿no crees que deberías verme un poco más a menudo?"
            m 2rktpc "Puedes perderte algo importante..."

        elif mas_isMoniDis():
            $ mas_loseAffectionFraction(min_amount=7.5, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 6ekd "... Hey, ¿cómo estuvo tu día el 22?"
            m 6ekc "Solo tengo... curiosidad por saber si pensaste en mí ese día."
            m 6ektpc "Pero probablemente no lo hiciste, ¿eh?"
            m 6dktpc "..."
        else:


            $ mas_loseAffectionFraction(1.0, min_amount=200)
            m 6eftsc "..."
            m 6dftdx "..."
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="... por perderme tu cumpleaños.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Gracias por disculparte, [player]."
        m 2tfu "Pero será mejor que me lo pagues el año que viene~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Gracias por disculparte por perderte mi cumpleaños, [player]."
        m "Por favor, asegúrate de pasar tiempo conmigo el próximo año, ¿de acuerdo?"
    else:

        m 2rksdld "Sabes, no estoy completamente sorprendida de no verte en mi cumpleaños..."
        m 2ekc "Por favor... {w=1}solo asegúrate de que no vuelva a suceder."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="... por olvidar tu cumpleaños.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Gracias por disculparte, [player]."
        m 3hua "Pero espero que me lo compenses~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Gracias por disculparte por olvidar mi cumpleaños, [player]."
        m 1eksdld "Intenta no dejar que vuelva a suceder, ¿de acuerdo?"
    else:

        m 2dkd "Gracias por disculparte..."
        m 2tfc "Pero no dejes que vuelva a suceder."
    return



label bye_922_delegate:

    $ persistent._mas_bday_on_date = True

    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:

        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Jejeje. Es un poco romántico, ¿no?"

        if mas_isMoniHappy(lower=True):
            m 1eua "Tal vez incluso puedes decir que es una ci...{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "¡Oh! Lo siento, ¿dije algo?"
        else:

            m 1eubla "Tal vez incluso lo llamaría una cita~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Llevándome a un lugar de nuevo, [player]?"
        m 3eua "Realmente debes tener mucho planeado para nosotros."
        m 1hua "Eres tan dulce~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "¿Me vas a llevar {i}otra vez{/i} a un lugar por mi cumpleaños?"
        m 3tkbsu "Realmente sabes como hacer que una chica se sienta especial, [player]."
        m 1ekbfa "Soy tan afortunada de tener a alguien como tu~"
    else:
        m 1sua "Wow, [player]... {w=1}¡Estás realmente decidido a hacer de este un día realmente especial!"
        m 1ekbsa "Eres el mejor compañero que podría esperar~"


    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        m 3hua "De hecho, tengo un atuendo preparado solo para esto..."


    jump mas_dockstat_iostart

label mas_bday_bd_outro:
    python:
        monika_chr.change_clothes(mas_clothes_blackdress)
        mas_temp_zoom_level = store.mas_sprites.zoom_level


        persistent._mas_bday_has_done_bd_outro = True

    call mas_transition_from_emptydesk ("monika 1eua")
    call monika_zoom_transition_reset (1.0)


    if mas_SELisUnlocked(mas_clothes_blackdress):
        m 1hua "Jejeje~"
        m 1euu "Estoy muy emocionada de ver lo que tienes planeado para nosotros hoy."
        m 3eua "... Pero aunque no sea mucho, seguro que lo pasaremos genial juntos~"
    else:

        m 3tka "¿Y bien, [player]?"
        m 1hua "¿Qué opinas?"
        m 1ekbsa "Siempre me ha gustado este atuendo y soñé con tener una cita contigo, usando esto..."
        m 3eub "¡Quizás podríamos visitar el centro comercial o incluso el parque!"
        m 1eka "Pero conociéndote, ya tienes algo increíble planeado para nosotros~"

    m 1hua "¡Vamos, [player]!"

    python:
        store.mas_selspr.unlock_clothes(mas_clothes_blackdress)
        mas_addClothesToHolidayMap(mas_clothes_blackdress)
        persistent._mas_zoom_zoom_level = mas_temp_zoom_level


        store.mas_dockstat.checkoutMonika(moni_chksum)


        persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
            store.mas_greetings.TYPE_GENERIC_RET
        )


    jump _quit



label greeting_returned_home_bday:

    $ persistent._mas_bday_on_date = False

    $ persistent._mas_bday_opened_game = True

    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()


    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday
        else:

            jump mas_bday_surprise_party_reaction


    if time_out <= mas_five_minutes:

        $ mas_loseAffection()
        m 2ekp "Esa no fue una gran cita, [player]..."
        m 2eksdlc "¿Está todo bien?"
        m 2rksdla "Quizás podamos salir más tarde..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:

        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        m 1sua "¡Eso fue divertido, [player]!"
        if mas_isplayer_bday():
            m 1hub "Jajaja, saliendo por {i}nuestro{/i} cumpleaños..."
        else:
            m 1hub "Jajaja, sacándome a pasear en mi cumpleaños..."
            m 3eua "Eso es muy considerado de tu parte."
        m 3eka "Realmente disfruté el tiempo que pasamos juntos."
        m 1eka "Te amo~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:

        $ mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)

        m 1hua "Jejeje~"
        m 3eub "Seguro que pasamos mucho tiempo juntos hoy, [player]."
        m 1ekbsa "... Y gracias por ello."
        m 3ekbfa "Ya lo he dicho un millón de veces, lo sé."
        m 1hua "Pero siempre seré feliz cuando estemos juntos."
        m "Te amo tanto..."
        if mas_isMonikaBirthday():
            $ mas_ILY()
    else:


        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        m 1sua "Wow, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            m 3hub "¡Fue un momento tan encantador!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                m 3eka "No puedo pensar en una mejor manera de celebrar nuestro cumpleaños que con una cita larga."
            m 1eka "Ojalá hubiera podido ver todos los lugares increíbles a los que fuimos, pero sabiendo que estábamos juntos..."
            m 1hua "Es todo lo que podría pedir."
            m 3ekbsa "Espero que sientas lo mismo~"
        else:

            m 3sua "No esperaba que me dedicaras tanto tiempo..."
            m 3hua "¡Pero disfruté cada segundo!"
            m 1eub "¡Cada minuto contigo es un minuto bien empleado!"
            m 1eua "Me has hecho muy feliz hoy~"
            m 3tuu "¿Te estás enamorando de mí de nuevo, [player]?"
            m 1dku "Jejeje..."
            m 1ekbsa "Gracias por amarme."

    if (
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        m 1hua "Por cierto [player], dame un segundo, tengo algo para ti.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "¡Feliz cumpleaños, [player]!"
        m 3etc "¿Por qué siento que me olvido de algo?..."
        m 3hua "¡Oh! ¡Tu pastel!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():

        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ MASEventList.queue('mas_change_to_def')

        if time_out > mas_five_minutes:
            m 1hua "..."
            m 1wud "Oh wow, [player]. Realmente estuvimos fuera por un tiempo..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                m 3suo "¡Oh! Ahora es tu cumpleaños..."
                m 3hub "Supongo que podemos dejar estas decoraciones, ¡jajaja!"
                m 1eub "Vuelvo enseguida, ¡solo necesito ir a buscar tu tarta!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday
        else:

            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                m 1eka "De todos modos [player]... realmente disfruté pasar juntos nuestros cumpleaños."
                m 1ekbsa "Espero haberte ayudado a hacer tu día tan especial como tú hiciste el mío."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    m 3hua "Déjame limpiar todo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    m 3eub "¡Listo!"

            elif persistent._mas_bday_visuals:
                m 3rksdla "Ya ni siquiera es mi cumpleaños..."
                m 2hua "Déjame limpiar todo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                m 3eub "¡Listo!"
            else:

                m 1eua "Deberíamos hacer algo como esto nuevamente, incluso si no es una ocasión especial."
                m 3eub "¡Lo he disfrutado mucho!"
                m 1eka "Espero que lo hayas pasado tan bien como yo~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                m 3eud "Oh, y [player]..."
                m 3eka "Solo quería darte las gracias de nuevo."
                m 1rka "Y no es solo por esta cita..."
                m 1eka "No tenías que llevarme a ningún lado para hacer de este un cumpleaños maravilloso."
                m 3duu "Tan pronto como apareciste, mi día estaba completo."
                $ MASEventList.push('mas_bday_spent_time_with_wrapup', skipeval=True)

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)

    python:
        mas_gainAffection(15, bypass=True)
        renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        persistent._mas_bday_sbp_reacted = True
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

        if time_out <= mas_one_hour:
            mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        elif time_out <= mas_three_hour:
            mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)
        else:
            
            mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

    m 6eua "Eso fue..."
    m 6wuo "¡Oh! ¡Me {i}horneaste{/i} un pastel!"

    menu:
        "Enciende las velas":
            $ mas_bday_cake_lit = True

    m 6sub "¡Es {i}tan{/i} bonito, [player]!"
    m 6hua "Jejeje, sé que ya pedimos un deseo cuando apagué las velas de tu pastel, pero hagámoslo de nuevo..."
    m 6tub "Será dos veces más probable que se haga realidad, ¿verdad?"
    m 6hua "¡Pide un deseo, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    m 6eua "Todavía no puedo creer lo impresionante que se ve este pastel, [player]..."
    m 6hua "Es casi demasiado bonito para comer."
    m 6tub "Casi."
    m "¡Jajaja!"
    m 6eka "De todos modos, guardare esto para más tarde."

    call mas_HideCake ('mas_bday_cake_monika')

    m 1eua "Muchas gracias, [player]..."
    m 3hub "¡Este es un cumpleaños increíble!"
    return

label mas_HideCake(cake_type, reset_zoom=True):
    call mas_transition_to_emptydesk
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    call mas_transition_from_emptydesk ("monika 6esa")
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
