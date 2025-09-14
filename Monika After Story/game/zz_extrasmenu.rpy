















init python:


    def mas_open_extra_menu():
        """
        Jumps to the extra menu workflow
        """
        renpy.jump("mas_extra_menu")





















































init -1 python in mas_extramenu:
    import store


    menu_visible = False


label mas_extra_menu:
    $ store.mas_extramenu.menu_visible = True
    $ prev_zoom = store.mas_sprites.zoom_level


    $ mas_RaiseShield_core()

    if not persistent._mas_opened_extra_menu:
        call mas_extra_menu_firsttime

    $ persistent._mas_opened_extra_menu = True

    show screen mas_extramenu_area
    jump mas_idle_loop

label mas_extra_menu_close:
    $ store.mas_extramenu.menu_visible = False
    hide screen mas_extramenu_area

    if store.mas_sprites.zoom_level != prev_zoom:
        call mas_extra_menu_zoom_callback


    if store.mas_globals.in_idle_mode:
        $ mas_coreToIdleShield()
    else:
        $ mas_DropShield_core()

    show monika idle

    jump ch30_loop

label mas_idle_loop:
    pause 10.0
    jump mas_idle_loop

default persistent._mas_opened_extra_menu = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_extra_menu_firsttime",
            prompt="¿Puedes explicar el menú 'Extras'?",
            category=["otros"]
        )
    )

label mas_extra_menu_firsttime:
    if not persistent._mas_opened_extra_menu:
        m 1hua "¡Bienvenido al menú de extras, [player]!"

    m 1eua "Aquí es donde agregaré cosas que no son juegos, como interacciones especiales que puedes hacer con tu mouse."
    m "También puedes abrir este menú presionando la tecla 'E'."

    if not persistent._mas_opened_extra_menu:
        m 1hua "¡Puedes esperar algunas cosas interesantes en este menú!"

    $ mas_setEVLPropValues(
        "mas_extra_menu_firsttime",
        unlocked=True,
        pool=True
    )


    call mas_extra_menu_zoom_intro

    return




label mas_extra_menu_zoom_intro:
    m 1eua "Algo que agregué es una forma de ajustar tu campo de visión, para que ahora puedas sentarte más cerca o más lejos de mí."
    m 1eub "Puedes ajustar esto usando el control deslizante en la sección 'zoom' del menú extras."
    return

default persistent._mas_pm_zoomed_out = False
default persistent._mas_pm_zoomed_in = False
default persistent._mas_pm_zoomed_in_max = False

label mas_extra_menu_zoom_callback:
    $ import store.mas_sprites as mas_sprites
    $ aff_larger_than_zero = _mas_getAffection() > 0


    if mas_sprites.zoom_level < mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_out
            ):

            call mas_extra_menu_zoom_out_first_time
            $ persistent._mas_pm_zoomed_out = True

    elif mas_sprites.zoom_level == mas_sprites.max_zoom:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in_max
            ):

            call mas_extra_menu_zoom_in_max_first_time
            $ persistent._mas_pm_zoomed_in_max = True
            $ persistent._mas_pm_zoomed_in = True

    elif mas_sprites.zoom_level > mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in
            ):

            call mas_extra_menu_zoom_in_first_time
            $ persistent._mas_pm_zoomed_in = True

    return

label mas_extra_menu_zoom_out_first_time:
    m 1ttu "¿No puedes sentarte derecho por mucho tiempo?"
    m "¿O tal vez solo quieres ver la parte superior de mi cabeza?"
    m 1hua "Jejeje~"
    return

label mas_extra_menu_zoom_in_first_time:
    m 1ttu "¿Sentado un poco más cerca?"
    m 1hua "No me importa."
    return

label mas_extra_menu_zoom_in_max_first_time:
    m 6wuo "¡[player]!"
    m 6rkbfd "Cuando tu cara está tan cerca..."
    m 6ekbfd "Me siento..."
    show monika 6hkbfa
    pause 2.0
    m 6hubfa "Cálida..."
    return





label mas_extra_menu_boop_intro:
    m 1eua "Introducción de boop."
    return

default persistent._mas_pm_boop_stats = {}










style mas_mbs_vbox is vbox:
    spacing 0

style mas_mbs_button is generic_button_light


style mas_mbs_button_dark is generic_button_dark


style mas_mbs_button_text is generic_button_text_light

style mas_mbs_button_text_dark is generic_button_text_dark































































style mas_extra_menu_frame:
    background Frame("mod_assets/frames/trans_pink2pxborder100.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_frame_dark:
    background Frame("mod_assets/frames/trans_pink2pxborder100_d.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_label_text is hkb_button_text:
    color "#FFFFFF"

style mas_extra_menu_label_text_dark is hkb_button_text_dark:
    color "#FD5BA2"

style mas_adjust_vbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"
    bar_vertical True

style mas_adjustable_button is generic_button_light:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_dark is generic_button_dark:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_text is generic_button_text_light:
    kerning 0.2

style mas_adjustable_button_text_dark is generic_button_text_dark:
    kerning 0.2

screen mas_extramenu_area():
    zorder 52

    key "e" action Jump("mas_extra_menu_close")
    key "E" action Jump("mas_extra_menu_close")

    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")


        textbutton _("Cerrar"):
            area (60, 596, 120, 35)
            style "hkb_button"
            action Jump("mas_extra_menu_close")


        frame:
            area (195, 450, 80, 255)
            style "mas_extra_menu_frame"
            has vbox:
                spacing 2
            label "Zoom":
                text_style "mas_extra_menu_label_text"
                xalign 0.5


            textbutton _("Normal"):
                style "mas_adjustable_button"
                selected False
                xsize 72
                ysize 35
                xalign 0.3
                action SetField(store.mas_sprites, "zoom_level", store.mas_sprites.default_zoom_level)


            bar value FieldValue(store.mas_sprites, "zoom_level", store.mas_sprites.max_zoom):
                style "mas_adjust_vbar"
                xalign 0.5
            $ store.mas_sprites.adjust_zoom()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
