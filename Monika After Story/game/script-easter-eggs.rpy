


label sayori_name_scare:
    if not store.mas_egg_manager.name_eggs_enabled():
        return

    python:
        from store.songs import FP_SAYO_NARA, initMusicChoices
        initMusicChoices(sayori=True)
        mas_play_song(FP_SAYO_NARA, set_per=True)
        store.mas_globals.show_sayori_lightning = True
    return


label yuri_name_scare:
    if not store.mas_egg_manager.name_eggs_enabled():
        return



    $ HKBHideButtons()
    $ disable_esc()


    scene black
    show yuri eyes zorder 2 at t11
    play music hb
    show layer master at heartbeat
    show dark zorder 200
    pause 4.0
    hide yuri
    hide dark
    show layer master
    stop music


    $ HKBShowButtons()
    $ enable_esc()
    return


label natsuki_name_scare(playing_okayev=False):
    if not store.mas_egg_manager.name_eggs_enabled():
        return


    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ quick_menu = False
    $ scary_t5c = "bgm/5_ghost.ogg"
    $ curr_vol = store.songs.getVolume("music")
    $ renpy.music.set_volume(1.0, channel="music")


    if playing_okayev:
        $ currentpos = get_pos(channel="music")
        $ adjusted_t5c = "<from " + str(currentpos) + " loop 4.444>" + scary_t5c
        stop music fadeout 2.0
        $ renpy.music.play(adjusted_t5c, fadein=2.0, tight=True)
    else:
        stop music
        $ mas_play_song("<from 11>" + scary_t5c)


    scene black
    show darkred zorder 5
    show natsuki ghost1 zorder 2 at t11
    show n_rects_ghost1_instant zorder 4
    show n_rects_ghost2_instant zorder 4
    show n_rects_ghost3_instant zorder 4
    show natsuki_ghost_blood zorder 3




    pause 5



    play sound "sfx/crack.ogg"
    hide natsuki_ghost_blood
    hide n_rects_ghost1_instant
    hide n_rects_ghost2_instant
    hide n_rects_ghost3_instant
    show natsuki ghost3
    show n_rects_ghost4 onlayer front zorder 4
    show n_rects_ghost5 onlayer front zorder 4
    pause 0.5


    hide natsuki
    play sound "sfx/run.ogg"
    show natsuki ghost4 on layer front at i11
    pause 0.25


    window hide(None)
    hide natsuki onlayer front
    hide n_rects_ghost4 onlayer front
    hide n_rects_ghost5 onlayer front
    scene black
    with None
    window auto
    scene black


    python:
        HKBShowButtons()
        enable_esc()
        store.songs.enabled = True
        quick_menu = True
        renpy.music.set_volume(curr_vol, channel="music")



    if playing_okayev:
        $ currentpos = get_pos(channel="music")
        $ adjusted_okayev = "<from " + str(currentpos) + " loop 4.444>bgm/5_monika.ogg"
        stop music fadeout 2.0
        $ renpy.music.play(adjusted_okayev, fadein=2.0, tight=True)
    else:
        stop music
        $ mas_play_song(store.songs.current_track)

    return


image n_rects_ghost1_instant:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (580, 270)
    size (20, 25)

image n_rects_ghost2_instant:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (652, 264)
    size (20, 25)

image n_rects_ghost3_instant:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (616, 310)
    size (25, 15)


define ns.NATSUKI_SCALE = 0.15

image n_cg1bs = LiveComposite((1280,720), (10, 300), im.FactorScale(im.Flip("images/cg/n_cg1b.png",horizontal=True), ns.NATSUKI_SCALE), (64,347), "n_rects1", (85,360), "n_rects2", (71,370), "n_rects3")



image n_rects1:
    RectCluster(Solid("#000"), 3, 5, 3).sm
    pos (0, 0)
    size (7, 7)

image n_rects2:
    RectCluster(Solid("#000"), 2, 4, 2).sm
    pos (0, 0)
    size (5, 5)

image n_rects3:
    RectCluster(Solid("#000"), 2, 1, 2).sm
    pos (0, 0)
    size (3, 3)


label natsuki_name_scare_hungry:
    if not store.mas_egg_manager.name_eggs_enabled():
        return



    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ quick_menu = False
    $ curr_music_vol = store.songs.getVolume("music")
    $ curr_sound_vol = store.songs.getVolume("sound")
    $ renpy.music.set_volume(0.0, channel="music")
    $ renpy.sound.set_volume(1.0)


    show screen tear(20, 0.1, 0.1, 0, 40)
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    hide screen tear



    show n_cg1bs
    show monika_body_glitch1 zorder MAS_MONIKA_Z at t11
    hide monika


    $ adjusted_6g = "<from 6.0>bgm/6g.ogg"
    $ renpy.play(adjusted_6g, channel="sound")
    $ ntext = glitchtext(96)
    $ style.say_dialogue = style.edited
    n "{cps=*2}{color=#000}[ntext]{/color}{/cps}{nw}"
    $ ntext = glitchtext(96)
    n "{cps=*2}{color=#000}[ntext]{/color}{/cps}{nw}"


    show screen tear(20, 0.1, 0.1, 0, 40)
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    hide screen tear


    show monika 1esa zorder MAS_MONIKA_Z at t11
    hide n_cg1bs
    hide monika_body_glitch1

    $ mas_resetTextSpeed()


    python:
        HKBShowButtons()
        enable_esc()
        store.songs.enabled = True
        quick_menu = True
        renpy.sound.stop()
        renpy.sound.set_volume(curr_sound_vol)
        renpy.music.set_volume(curr_music_vol, channel="music")


    return


transform zoom_ghost:
    zoom 1.5 yoffset 500


label mas_ghost_monika:

    scene black

    python:

        mas_play_song(audio.ghostmenu)

    show noise zorder 11:
        alpha 0.5


    show ghost_monika zorder MAS_MONIKA_Z at i11


    $ renpy.pause(10, hard=True)

    stop music
    hide noise


    show ghost_monika at zoom_ghost


    pause 0.01


    $ persistent.closed_self = True


    jump _quit

init -1 python in mas_egg_manager:
    import store


    def is_eggable_name(name):
        """
        Checks if the given name is eggable

        IN:
            name - the name to check (string)

        RETURNS: True if the name is eggable
        """
        return name in ("sayori", "natsuki", "yuri")


    def name_eggs_enabled():
        """
        Checks if name eggs are enabled

        RETURNS: True if name eggs are enabled
        """
        return not store.persistent._mas_disable_eggs


    def natsuki_enabled():
        """
        Checks if the natsuki egg should be enabled

        RETURNS: True if natsuki egg should be enabled
        """
        return (
            name_eggs_enabled()
            and store.persistent.playername.lower() == "natsuki"
        )


    def sayori_enabled():
        """
        Checks if the sayori egg should be enabled

        RETURNS: True if the sayori egg should be enabled
        """
        return (
            name_eggs_enabled()
            and store.persistent.playername.lower() == "sayori"
        )


    def yuri_enabled():
        """
        Checks if the yuri egg should be enabled

        RETURNS: True if yuri egg should be enabled
        """
        return (
            name_eggs_enabled()
            and store.persistent.playername.lower() == "yuri"
        )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
