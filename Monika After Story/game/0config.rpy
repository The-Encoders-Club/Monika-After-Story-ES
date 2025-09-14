







python early:




    renpy.config.name = "Monika After Story"


    renpy.config.version = "0.12.17"


    config.window_title = "Monika After Story   "















    renpy.config.save_directory = "Monika After Story"

init -1200 python:





    renpy.config.has_sound = True
    renpy.config.has_music = True
    renpy.config.has_voice = False

















    renpy.config.enter_transition = Dissolve(.2)
    renpy.config.exit_transition = Dissolve(.2)




    renpy.config.after_load_transition = None




    renpy.config.end_game_transition = Dissolve(.5)
















    renpy.config.window = "auto"







    renpy.config.window_icon = "gui/window_icon.png"



    renpy.config.allow_skipping = True
    renpy.config.has_autosave = False
    renpy.config.autosave_on_quit = False
    renpy.config.autosave_slots = 0
    renpy.config.layers = ["master", "transient", "minigames", "screens", "overlay", "front"]
    renpy.config.image_cache_size = 64
    renpy.config.debug_image_cache = config.developer
    renpy.config.predict_statements = 5
    renpy.config.rollback_enabled = config.developer
    renpy.config.menu_clear_layers = ["front"]
    renpy.config.gl_test_image = "white"




    if len(renpy.loadsave.location.locations) > 1:
        renpy.loadsave.location.locations.pop()







define config.main_menu_music = audio.t1


define config.window_show_transition = dissolve_textbox
define config.window_hide_transition = dissolve_textbox
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
