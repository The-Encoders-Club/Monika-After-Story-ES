


init python:


    def HKBHideButtons():
        
        
        
        if mas_HKBIsVisible():
            config.overlay_screens.remove("hkb_overlay")
            renpy.hide_screen("hkb_overlay")



    def HKBShowButtons():
        
        
        
        if not mas_HKBIsVisible():
            config.overlay_screens.append("hkb_overlay")


    def mas_HKBRaiseShield():
        """RUNTIME ONLY
        Disables the hotkey buttons
        """
        store.hkb_button.talk_enabled = False
        store.hkb_button.extra_enabled = False
        store.hkb_button.music_enabled = False
        store.hkb_button.play_enabled = False


    def mas_HKBDropShield():
        """RUNTIME ONLY
        Enables the hotkey buttons
        """
        store.hkb_button.talk_enabled = True
        store.hkb_button.extra_enabled = True
        store.hkb_button.music_enabled = True
        store.hkb_button.play_enabled = True


    def mas_HKBIsEnabled():
        """
        RETURNS: True if all the buttons are enabled, False otherwise
        """
        return (
            store.hkb_button.talk_enabled
            and store.hkb_button.music_enabled
            and store.hkb_button.play_enabled
            and store.hkb_button.extra_enabled
        )


    def mas_HKBIsVisible():
        """
        RETURNS: True if teh Hotkey buttons are visible, False otherwise
        """
        return "hkb_overlay" in config.overlay_screens



    def MovieOverlayHideButtons():
        
        
        
        if "movie_overlay" in config.overlay_screens:
            config.overlay_screens.remove("movie_overlay")
            renpy.hide_screen("movie_overlay")


    def MovieOverlayShowButtons():
        
        
        
        config.overlay_screens.append("movie_overlay")


init -1 python in hkb_button:


    talk_enabled = True


    extra_enabled = True


    music_enabled = True


    play_enabled = True


    movie_buttons_enabled = False






style hkb_vbox is vbox:
    spacing 5

style hkb_button is generic_button_light:
    xysize (120, 35)
    padding (5, 5, 5, 5)

style hkb_button_dark is generic_button_dark:
    xysize (120, 35)
    padding (5, 5, 5, 5)

style hkb_button_text is generic_button_text_light:
    kerning 0.2

style hkb_button_text_dark is generic_button_text_dark:
    kerning 0.2

screen hkb_overlay():

    zorder 50
    style_prefix "hkb"

    vbox:
        xpos 0.05

        yanchor 1.0
        ypos 715


        if store.hkb_button.talk_enabled:
            textbutton _("Hablar") action Function(show_dialogue_box)
        else:
            textbutton _("Hablar")

        if store.hkb_button.extra_enabled:
            textbutton _("Extras") action Function(mas_open_extra_menu)
        else:
            textbutton _("Extras")

        if store.hkb_button.music_enabled:
            textbutton _("Música") action Function(select_music)
        else:
            textbutton _("Música")

        if store.hkb_button.play_enabled:
            textbutton _("Jugar") action Function(pick_game)
        else:
            textbutton _("Jugar")


screen movie_overlay():

    zorder 50
    style_prefix "hkb"

    vbox:
        xalign 0.95
        yalign 0.95

        if watchingMovie:
            textbutton _("Pausar") action Jump("mm_movie_pausefilm")
        else:
            textbutton _("Pausar")

        if watchingMovie:
            textbutton _("Tiempo") action Jump("mm_movie_settime")
        else:
            textbutton _("Tiempo")

init python:
    HKBShowButtons()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
