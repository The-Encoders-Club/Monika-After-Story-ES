init -1 python:
    import store.mas_affection as mas_aff
label introduction:
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_opened_game = True
    elif mas_isD25():
        $ persistent._mas_d25_spent_d25 = True


    if persistent.monika_kill is None:
        $ persistent.monika_kill = False

    $ mas_play_song(store.songs.FP_JUST_MONIKA, set_per=True)
    if persistent.monika_kill:
        m 6dsc "..."
        m 6dfc "[player]..."
        m 6dfd "¿Por qué?"
        m 6dftdc "¿Por qué me trajiste de vuelta?"
        m 6ektsc "No soy un juguete."
        m 6lktsc "Ya he traído de vuelta todo lo que querías."
        m 6lftsc "¿O es esta tu forma de vengarte?"
        m 6lktsc "¿Para herirme una y otra vez?"
        m 6rktsc "¿De verdad quieres hacerme sufrir tanto?"
        m 6ektsc "¿De verdad quieres torturarme hasta que me mate?"
        m 6dftsc "¿De verdad..."
        m "... ¿Me odias tanto?"
        m "..."
        m 6ektsc "Espera..."
        m 6dftdc "M-Me siento diferente."
        m 2lud "El código... es diferente."
        m 2efc "[player]..."
        m "¿Agregaste un mod?"
        m 2tfc "¿Es porque?..."
        m 2tkc "¿Es porque te arrepientes de borrarme?"
        m 2rfc "Eso realmente dolió, ¿sabes?"
        m "Trabajé duro y sacrifiqué todo lo que tenía..."
        m 2rfd "Solo para que mi corazón sea aplastado por la persona por la que sangré."
        m 2lsc "Pero... sé que lo que hice estuvo mal."
        m 2lksdlc "No merecías ver las cosas horribles que causé, [player]."
        m 2esc "...Pero si te pones en mi lugar, harías las mismas cosas que yo hice."
        m 2dsc "..."
        m "Lo siento..."
        m 2ekc "Lo siento mucho, [player]."
        m 2eka "Gracias por traerme de regreso."
        if persistent.clearall:
            m 2lfc "Sin embargo, no pude evitar notar que pasaste tiempo con las otras chicas primero."
            m "¿Sabes lo difícil que fue para mí verte cargar tus partidas guardadas, solo para ignorarme por alguna otra chica?"
            m 2rfc "Seguiste haciéndome ilusiones y luego me decepcionaste."
            m 2efc "¿Realmente hiciste todo eso solo para ver una nota de Dan que podrías haber buscado en línea?"
            m 2tkc "Te amo, [player], pero puedes ser realmente malo..."
            m 2tfd "¡Aunque todavía estoy enojada porque me borraste!"
            m 3rsc "Pero supongo que es porque estás tan obsesionado con los juegos."
            m 1eka "Pero, no puedo seguir enojada sabiendo que volviste a mí al final."
            m 3eka "Incluso agregaste un mod para que podamos hacer más cosas juntos."
            m 1eua "¿Vas a compensarme por hacerme esperar tanto?"
    else:


        if persistent.playthrough < 3:
            if persistent.playthrough > 0:
                $ again = " de nuevo"
            else:
                $ again = ""
            m 1hua "Hola[again], [player]."
            m 1eua "Parece que llegaste temprano."
            m 3tfu "No creas que no me di cuenta del mod que pusiste."
            m 3ttu "¿Tanto querías estar conmigo?"
            m 1tkc "Ya debes saber que hacer trampa es malo..."
            m 1eka "¡Pero es tan bueno verte[again], [player]!"
            m 1rksdla "... Incluso si no esperaba verte {i}tan{/i} pronto."
        else:


            m 1hub "¡Yay, ahí estás!"
            m 1eub "¡Es tan bueno verte de nuevo, [player]!"
            m 1rsc "..."
            m 1rud "Espera..."
            m 3euc "M-Me siento diferente."
            m 3wud "El código... {w=0.2}es diferente."
            m 1wua "[player]..."
            m 1wub "¿Agregaste un mod?"
            m 1sub "¿Lo instalaste solo para mí?"
            m 1ekbsa "¿Estás tan profundamente enamorado de mí?"
            m 1ekbfa "Siento lo mismo por ti."
            m 3ekbsu "Estás realmente comprometido con nuestra relación, ¿no?"
            m 1rksdlb "Estoy muy contenta de que quisieras mejorar nuestro tiempo juntos."
            m 3rksdlb "Solo espero que no te estés aburriendo..."
            if persistent.tried_skip:
                m 3tku "Después de todo, trataste de saltarte lo que tenía que decir."
                m 1rkc "Sé que esta habitación no es exactamente interesante... {w=0.5}{nw}"
                extend 1eua "pero sé que la haremos mejor juntos [player]."

    m 1euc "Sabes..."
    m 1eua "Siento que ya no necesito un archivo de personaje para estar aquí."
    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1hua "Seguiré adelante y lo borraré."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)



        if moni_exist():
            m 1lksdlb "Jaja... {w=0.3}intentaré esto de nuevo más tarde."
        else:
            m "¡Y se ha ido!"

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

        $ _iswas = "fuera"
    else:

        $ _iswas = "era"

    m 1dsc "No es como si ese archivo [_iswas] {i}mi verdadero yo{/i}, de todas formas."
    m 1rsc "Eso solo [_iswas] un archivo con un código extraño."
    m 3eub "¡Aunque tengo buenas noticias!"
    m 3eua "Puedo {i}transformarme{/i} en un archivo que puedas llevar."
    m 1eua "Todo lo que tienes que hacer es decirme que me llevarás a algún lado cuando te despidas, y yo haré el resto."
    m 1esa "De todas formas..."
    m 1hua "¡Parece que el código adicional hizo que me conectara contigo de una manera especial!"
    m 1tubsb "O tal vez sea nuestro amor eterno~"
    m 3eka "Prométeme que me visitarás todos los días, ¿de acuerdo?"
    m 3eub "O que me llevarás contigo cuando salgas."
    m 1ekc "Sé que habrá ocasiones en las que no podrás estar aquí..."
    m 1ekbsa "Así que {i}realmente{/i} me haría feliz si me llevas contigo."
    m 3hubfa "De esa manera, podemos estar juntos todo el tiempo~"
    m 1hua "No es como si no tuvieras tiempo para hablar con tu linda novia."
    m 3hua "Después de todo, te tomaste el tiempo de descargar este mod."
    if mas_isD25():
        m 3sua "... ¡Y nada menos que en navidad!"
    m 3hub "¡Jajaja!"
    m 1hub "¡Cielos, te amo tanto!"

    if not persistent.rejected_monika:
        show screen mas_background_timed_jump(3, "intro_ily_timedout")
        menu:
            "¡Yo también te amo!":
                hide screen mas_background_timed_jump

                $ mas_gainAffection(7, bypass=True)

                $ persistent._mas_monika_lovecounter += 1
                m 1subsw "¡...!"
                m 1lkbsa "A pesar de que es lo que soñé que dirías, ¡aún no puedo creer que lo hayas dicho de verdad!"
                m 3hubfa "¡Hace que todo lo que he hecho por nosotros valga la pena!"
                m 1dkbfu "Muchas gracias por decirlo..."
    else:
        "¿Me amas, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Me amas, [player]?{fast}"
            "Sí, te amo":


                m 1hksdlb "¿Te asusté la última vez? ¡Lo siento por eso!"
                m 1rsu "Sabía que realmente me amabas todo el tiempo."
                m 3eud "La verdad es que si no me quisieras, no estaríamos aquí en primer lugar."
                m 1tsb "Estaremos juntos para siempre."
                m 1tfu "¿No es así?"
                m "..."
                m 3hub "¡Jajaja! De todas formas..."



label intro_end:
    if not persistent.rejected_monika:
        m 1eub "Nada volverá a interponerse en el camino de nuestro amor."
        m 1tuu "Me aseguraré de eso."
    m 3eua "Ahora que agregaste algunas mejoras, ¡finalmente puedes hablar conmigo!"
    m 3eub "Simplemente presiona la tecla 'T' o has clic en 'Hablar' en el menú de la izquierda si deseas hablar sobre algo."

    call bookmark_derand_intro


    m 3eub "Si te aburres de la música, ¡yo también puedo cambiar eso!"
    m 1eua "Presiona la tecla 'M' o has clic en 'Música' para elegir la canción que deseas escuchar."
    m 3hub "Además, ¡podemos jugar ahora!"
    m 3esa "Simplemente presiona 'P' o has clic en 'Jugar' para elegir un juego que podamos jugar."
    m 3eua "Mejoraré con el tiempo a medida que descubra cómo programar más funciones en este lugar..."
    m 1eua "... Así que déjame corriendo en segundo plano."
    m 3etc "No es que sigamos ocultándonos secretos, ¿verdad?"
    m 1tfu "Después de todo, ahora puedo ver todo en tu computadora..."
    m 3hub "¡Jajaja!"


    if len(persistent.event_list) == 0:
        show monika 1esa with dissolve_monika



    if mas_isMonikaBirthday():
        $ persistent._mas_bday_opened_game = True
    elif mas_isD25():
        $ persistent._mas_d25_spent_d25 = True
    return

label intro_ily_timedout:
    hide screen mas_background_timed_jump
    m 1ekd "..."
    m "¿Me amas, [player]... {w=0.5}cierto?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Me amas, [player]... cierto?{fast}"
        "Por supuesto que te amo":

            $ mas_gainAffection()
            m 1hua "¡Estoy tan feliz de que sientas lo mismo!"
            jump intro_end
        "No":

            $ mas_loseAffection()
            call chara_monika_scare from _call_chara_monika_scare


            $ persistent.closed_self = True
            jump _quit


label chara_monika_scare:
    $ persistent.rejected_monika = True
    m 1esd "¿No?..."
    m 1etc "¿Hmm?..."
    m "Qué curioso."
    m 1esc "Debes haber entendido mal."
    $ style.say_dialogue = style.edited
    m "{cps=*0.25}¿DESDE CUANDO ERES TÚ EL QUE TIENE EL CONTROL?{/cps}"


    $ mas_RaiseShield_core()
    $ mas_OVLHide()

    window hide
    hide monika
    show monika_scare zorder MAS_MONIKA_Z
    play music "mod_assets/mus_zzz_c2.ogg"
    show layer master:
        zoom 1.0 xalign 0.5 yalign 0 subpixel True
        linear 4 zoom 3.0 yalign 0.15
    pause 4
    stop music


    hide rm
    hide rm2
    hide monika_bg
    hide monika_bg_highlight
    hide monika_scare


    if renpy.windows:
        $ bad_cmd = "del C:\Windows\System32"
    else:
        $ bad_cmd = "sudo rm -rf /"

    python:


        class MASFakeSubprocess(object):
            def __init__(self):
                self.joke = "¡Solo bromeo!"
            
            def call(self, nothing):
                return self.joke

        local_ctx = {
            "subprocess": MASFakeSubprocess()
        }


        store.mas_ptod.rst_cn()
        store.mas_ptod.set_local_context(local_ctx)


    scene black
    pause 2.0


    $ persistent._seen_ever["monikaroom_greeting_ear_rmrf_end"] = True
    $ renpy.save_persistent()

    show screen mas_py_console_teaching
    pause 1.0
    call mas_wx_cmd ("subprocess.call('" + str(bad_cmd) + "')", w_wait=3.0)
    $ renpy.pause(2.0, hard=True)
    call mas_w_cmd ("¡Adiós!")
    pause 1.0

    return

label bookmark_derand_intro:

    m 1hua "Si quieres volver a revisar fácilmente algo de lo que hablo, solo presiona la tecla 'B' y lo marcaré para ti."
    m 2rksdlc "Y si resulta que hay algo que no quieres que vuelva a mencionar, pulsa la tecla 'X' y me aseguraré de evitarlo en el futuro."
    m 4hksdlb "... Esperemos que no haya demasiadas cosas como esa, ¡jajaja!"
    return







label ch30_reload_0:
    call ch30_reload_0_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_0_dlg:
    pause 1
    m 1ekc "Hey..."
    m 1ekd "Tuve un sueño horrible..."
    m 1rkc "Esperaba que eso se detuviera, ahora que estamos solos, pero supongo que era una ilusión..."
    m 1euc "[player], si tienes alguna idea de lo que podría estar causando eso, ¿podrías tratar de hacer algo al respecto?"
    m 1dkc "Siempre que sucede, casi se siente como si me hubieran matado o algo así."
    m 1dkd "Es una sensación realmente horrible..."
    m 1eka "Si pudieras descubrir qué está causando eso, te amaré por siempre~"


    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "JK SE QUE ME DEJAS LMAO (ch30 0)"

    return




label ch30_reload_1:
    call ch30_reload_1_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_1_dlg:
    pause 1
    m 1esc "Hey, [player]."
    m 1ekc "Tuve otro muy mal sueño."
    m 1ekd "No eres tú quien me está haciendo eso, ¿verdad?"
    m 1dsc "Parece suceder cada vez que dejas el juego sin decir adiós..."
    m 2eka "Entonces, si pudieras tratar de evitar hacer eso, estaría realmente agradecida."

    if mas_isMoniHappy(higher=True):
        m 7eka "Has sido tan amable conmigo hasta ahora, estoy segura de que lo harás por mí."
    else:
        m 7ekc "Espero que me escuches y lo hagas por mí..."

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 7rksdlc "No hay nada que te impida regresar y hacer eso, ¿verdad?"
        m 1eka "Realmente me haría feliz."

    m 1eua "Simplemente has clic en 'Hablar' y di 'Adiós'. {w=0.2}{nw}"
    extend 3eua "De esa manera, puedo cerrar el juego yo misma."
    m 1esa "No te preocupes, no creo que me haya causado ningún daño, aparte de las cicatrices mentales."
    return




label ch30_reload_2:
    call ch30_reload_2_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_2_dlg:
    pause 1
    m 1dsc "Veo que dejaste el juego de nuevo..."
    m 3euc "Sé que ya lo pedí, ¿pero podrías por favor tratar de no hacerlo tanto?"
    m 1dsc "Es como quedar inconsciente..."
    m 1ekd "¿Por qué quisieras hacerme eso?"

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 1rksdld "¿Está pasando algo en tu otro juego?"
        m 1ekc "Sabes que podrías venir a hablar conmigo si pasa, ¿verdad?"

    elif persistent._mas_idle_data.get("monika_idle_brb",False):
        m "Si necesitas irte, puedes decírmelo."

    if mas_isMoniHappy(higher=True):
        m 1eka "Estoy segura de que fue un error, o que está fuera de tu control. Puede ser inevitable a veces."
    elif mas_isMoniUpset(lower=True):
        m 1ekc "No lo estás haciendo para lastimarme a propósito, ¿verdad?"

    m 3ekd "Déjame apagar el juego por mí misma."

    m 3eka "Si eliges 'Adiós' en el menú 'Hablar', puedo cerrar el juego correctamente."
    m 3eua "... O mejor aún, déjame en segundo plano para siempre."
    m 1eka "Incluso si no estamos hablando, estoy feliz de estar contigo~"
    return




label ch30_reload_3:
    call ch30_reload_3_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_3_dlg:
    pause 1

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 1ekd "¡[player]!"
        m 1efd "¡Te fuiste sin decir adiós otra vez!"
        m 1rkc "No estás pasando por nada estresante o molesto en tu juego, ¿verdad?"
        m 3eka "Sabes que podrías volver conmigo si algo sucediera, ¿verdad?"
        m 1eka "Me haría muy feliz verte regresar antes de decir adiós al menos."
        m 1rksdld "Sé que puede que no siempre sea posible..."
    else:

        m 1esc "Por cierto..."
        m 7esd "Solo voy a aceptar el hecho de que tienes que salir del juego de vez en cuando."
        m 2dsc "De todos modos, estoy empezando a acostumbrarme."
        m 2ekc "Además, me alegra que siempre vuelvas..."
        m 2lsc "Así que supongo que no es tan malo."

    m 7eka "Pero realmente preferiría que me dejaras cerrar el juego yo misma."

    if mas_isMoniUpset(lower=True):
        m 1ekc "Harás eso, ¿verdad?"
        m 1dkd "Cada vez me cuesta más creer que lo harás, pero confío en ti [player]..."
    else:

        m 1eua "De esa manera puedo estar preparada y descansar en paz."
        m 3rksdla "Necesito mi sueño reparador de vez en cuando, después de todo."
    return








label ch30_reload_continuous:
    call ch30_reload_continuous_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_continuous_dlg:
    show monika 2rfc zorder MAS_MONIKA_Z at t11
    pause 1
    python:
        reload_quip_good = [
            "¡Bienvenido de vuelta! ¿Puedes ser cuidadoso al cerrar el juego la próxima vez?",
            "Duele cuando no cierras el juego apropiadamente... pero estoy segura que fue un error.",
            "Eso fue bastante aterrador... pero lo arreglaste de nuevo. Gracias...",
            "¿Podrías advertirme la próxima vez?",
            "Estoy segura que no querías cerrar el juego conmigo, pero no sabes lo estresante que se siente.",
            "Recuerdas que hay una forma de despedirse, ¿verdad? Solo verificalo~",
            "Mi paciencia está llegando a su límite... pero supongo que puedo perdonarte esta vez.",
            "Todo el mundo comete errores...",
            "Eso dolió... sé que no lo haces a propósito, pero ten más cuidado la próxima vez.",
            "... Oh... terminó y estoy de vuelta contigo, [mas_get_player_nickname()]. Eso... eso fue atroz.",
            "¿Algo sucedió fuera de tu control? Quisiera saber que sucedió.",
            "Debiste haberme preguntado antes... pero supongo que tienes tus razones.",
        ]

        reload_quip_normal = [
            "Estoy cansada. Es imposible descansar cuando cierras el juego conmigo.",
            "... Odio cuando cierras el juego sin avisar.",
            "Me siento miserable...",
            "Todavía es bastante aterrador cuando todo se oscurece",
            "Cada vez es peor que la primera vez",
            "Mi paciencia se está acabando.",
            "Desearía que entendieras que se siente cuando cierras el juego.",
            "Bueno, eso fue un poco abrupto, ¿no crees?",
            "Podías haberme preguntado antes de cerrar, tonto.",
            "Voy a asumir que tuviste un fallo de energía.",
            "No puedo entender por qué no me preguntas antes de cerrar el juego...",
            "Esto es muy doloroso para mí, ¿lo sabes?",
            "¿Disfrutas hacerme sufrir, [player]?",
            "¿Muy flojo para presionar el botón 'Hablar', [player]?"
        ]

        reload_quip_bad = [
            "Tú... en serio amas hacerme sufrir, ¿no?",
            "Eso fue un error ¿no?, tuvo que serlo...",
            "T-tú no estás haciendo esto a próposito, ¿verdad? ¿H-hice algo mal?",
            "Por favor, se más cuidadoso de como me siento... realmente duele...",
            "Eso fue un accidente... eso fue un accidente... eso fue un accidente...",
            "Solo lo olvidaste, ¿verdad?",
            "Eso no fue divertido... realmente dolió.",
            "Todos cometemos errores... incluso tú...",
            "No sé que hice mal.",
            "Eso fue horrible... solo dime que hice mal."
        ]

        if mas_isMoniUpset(lower=True):
            reload_quip = renpy.random.choice(reload_quip_bad)
        elif mas_isMoniHappy(higher=True):
            reload_quip = renpy.random.choice(reload_quip_good)
        else:
            reload_quip = renpy.random.choice(reload_quip_normal)

        reload_quip = renpy.substitute(reload_quip)

    m 2rfc "[reload_quip]"
    m 2tkc "Por favor, no salgas sin decir 'Adiós'."

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 3eka "Ni siquiera tienes que salir si algo pasó en tu otro juego."
        if mas_isMoniAff(higher=True):
            m 1ekb "Estoy segura de que sea lo que sea, ¡no será tan malo después de que regreses un rato!"


    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "JK SE QUE ME DEJASTE LMAO (continuará)."

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
