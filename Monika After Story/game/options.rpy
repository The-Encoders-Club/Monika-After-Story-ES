









define gui.show_name = False




define gui.about = _("")






define build.name = "Monika_After_Story"






default preferences.text_cps = 50





default preferences.afm_time = 15

default preferences.music_volume = 0.75
default preferences.sfx_volume = 0.75



init 50 python:

    from __future__ import print_function

    config.lint_hooks = [
        lambda: print(),
        lambda: print("#"*5, "START MAS LINT HOOKS", "#"*5),
        
        lambda: print(
            "Known uses of deprecated functions/classes in initialisation:",
            (
                "\n".join([msg.rjust(len(msg) + 4) for msg in store.mas_utils._deprecation_warnings])
                if store.mas_utils._deprecation_warnings
                else "    None"
            ),
            "",
            sep="\n"
        ),
        lambda: print("#"*5, "END MAS LINT HOOKS", "#"*5)
    ]

init python:

    mas_override_label("_choose_renderer", "mas_choose_renderer_override")



    renpy.game.preferences.pad_enabled = False
    def replace_text(s):
        s = s.replace('--', u'\u2014') 
        s = s.replace(' - ', u'\u2014') 
        return s
    config.replace_text = replace_text

    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

    def force_integer_multiplier(width, height):
        if float(width) / float(height) < float(config.screen_width) / float(config.screen_height):
            return (width, float(width) / (float(config.screen_width) / float(config.screen_height)))
        else:
            return (float(height) * (float(config.screen_width) / float(config.screen_height)), height)







init python:



























    build.include_update = True





    build.classify("game/gui/**",build.name)


    build.classify("game/mod_assets/**",build.name)

    build.classify("game/*.rpyc",build.name) 
    build.classify("game/dev/*.*",None) 
    build.classify("README.html",build.name) 
    build.classify("game/python-packages/**",build.name)
    build.classify("CustomIcon**.**",build.name)


    build.package(build.directory_name + "Mod",'zip',build.name,description='DDLC Compatible Mod')

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.rpy', None)
    build.classify('**.psd', None)
    build.classify('**.sublime-project', None)
    build.classify('**.sublime-workspace', None)
    build.classify('/music/*.*', None)
    build.classify('script-regex.txt', None)
    build.classify('/game/10', None)
    build.classify('/game/cache/*.*', None)
    build.classify('**.rpa',None)
    build.classify("game/mod_assets/api_keys.json", None)
    build.classify("**.pem", None)




    build.documentation('*.html')
    build.documentation('*.txt')
    build.documentation('*.md')

    build.include_old_themes = False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
