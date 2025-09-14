init offset = 5






init -5 python:
    def mas_setupIdleMode(brb_label=None, brb_callback_label=None):
        """
        Setups idle mode

        IN:
            brb_label - the label of this brb event, if None, use the current label
                (Default: None)
            brb_callback_label - the callback label of this brb event, if None, we build it here
                (Default: None)
        """
        
        if brb_label is None and renpy.has_label(mas_submod_utils.current_label):
            brb_label = mas_submod_utils.current_label
        
        
        mas_moni_idle_disp.add_by_tag("idle_mode_exps")
        
        
        mas_globals.in_idle_mode = True
        persistent._mas_in_idle_mode = True
        
        
        renpy.save_persistent()
        
        
        if brb_callback_label is None and brb_label is not None:
            brb_callback_label = brb_label + "_callback"
        if brb_callback_label is not None and renpy.has_label(brb_callback_label):
            mas_idle_mailbox.send_idle_cb(brb_callback_label)

    def mas_resetIdleMode(clear_idle_data=True):
        """
        Resets idle mode

        This is meant to basically clear idle mode for holidays or other
        things that hijack main flow

        IN:
            clear_idle_data - whether or not clear persistent idle data
                (Default: True)

        OUT:
            string with idle callback label
            or None if it was reset before
        """
        
        mas_moni_idle_disp.remove_by_tag("idle_mode_exps")
        
        
        mas_globals.in_idle_mode = False
        persistent._mas_in_idle_mode = False
        if clear_idle_data:
            persistent._mas_idle_data.clear()
        
        renpy.save_persistent()
        
        return mas_idle_mailbox.get_idle_cb()


init 5 python in mas_brbs:
    import random
    import store
    from store import (
        MASMoniIdleExp,
        MASMoniIdleExpGroup,
        MASMoniIdleExpRngGroup
    )

    idle_mode_exps = MASMoniIdleExpRngGroup(
        [
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("5rubla", duration=(10, 20)),
                    MASMoniIdleExp("5rublu", duration=(5, 10)),
                    MASMoniIdleExp("5rubsu", duration=(20, 30)),
                    MASMoniIdleExp("5rubla", duration=(5, 10)),
                ],
                weight=30
            ),
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("5rubla", duration=(10, 20)),
                    MASMoniIdleExp("5gsbsu", duration=(20, 30)),
                    MASMoniIdleExp("5tsbsu", duration=1),
                    MASMoniIdleExp("1hubfu", duration=(5, 10)),
                    MASMoniIdleExp("1hubsa", duration=(5, 10)),
                    MASMoniIdleExp("1hubla", duration=(5, 10))
                ],
                weight=30
            ),
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("1lublu", duration=(10, 20)),
                    MASMoniIdleExp("1msblu", duration=(5, 10)),
                    MASMoniIdleExp("1msbsu", duration=(20, 30)),
                    MASMoniIdleExp("1hubsu", duration=(5, 10)),
                    MASMoniIdleExp("1hubla", duration=(5, 10))
                ],
                weight=30
            ),
            
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExpRngGroup(
                        [
                            
                            MASMoniIdleExpGroup(
                                [
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8))
                                ]
                            ),
                            
                            MASMoniIdleExpGroup(
                                [
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1mubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gubla", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1msbsu", duration=(0.9, 1.8)),
                                    MASMoniIdleExp("1gsbsu", duration=(0.9, 1.8))
                                ]
                            )
                        ],
                        max_uses=1
                    ),
                    MASMoniIdleExp("1tsbfu", duration=1),
                    MASMoniIdleExp("1hubfu", duration=(4, 8)),
                    MASMoniIdleExp("1hubsa", duration=(4, 8)),
                    MASMoniIdleExp("1hubla", duration=(4, 8))
                ],
                weight=10
            )
        ],
        max_uses=1,
        aff_range=(store.mas_aff.AFFECTIONATE, None),
        weight=10,
        tag="idle_mode_exps"
    )

    WB_QUIPS_NORMAL = [
        _("Entonces, ¿qué más quieres hacer hoy?"),
        _("¿Qué otra cosa quieres hacer hoy?"),
        _("¿Hay algo más que quieras hacer hoy?"),
        _("¿Qué más debemos hacer hoy?"),
    ]

    def get_wb_quip():
        """
        Picks a random welcome back quip and returns it
        Should be used for normal+ quips

        OUT:
            A randomly selected quip for coming back to the spaceroom
        """
        return renpy.substitute(random.choice(WB_QUIPS_NORMAL))

    def was_idle_for_at_least(idle_time, brb_evl):
        """
        Checks if the user was idle (from the brb_evl provided) for at least idle_time

        IN:
            idle_time - Minimum amount of time the user should have been idle for in order to return True
            brb_evl - Eventlabel of the brb to use for the start time

        OUT:
            boolean:
                - True if it has been at least idle_time since seeing the brb_evl
                - False otherwise
        """
        brb_ev = store.mas_getEV(brb_evl)
        return brb_ev and brb_ev.timePassedSinceLastSeen_dt(idle_time)




label mas_brb_back_to_idle:

    if globals().get("brb_label", -1) == -1:
        return

    python:
        mas_idle_mailbox.send_idle_cb(brb_label + "_callback")
        persistent._mas_idle_data[brb_label] = True
        mas_globals.in_idle_mode = True
        persistent._mas_in_idle_mode = True
        renpy.save_persistent()
        mas_dlgToIdleShield()

    return "idle"



label mas_brb_generic_low_aff_callback:
    if mas_isMoniDis(higher=True):
        python:
            cb_line = renpy.substitute(renpy.random.choice([
                _("Oh...{w=0.3} volviste."),
                _("Oh...{w=0.3} bienvenido de vuelta."),
                _("¿Todo listo?"),
                _("Bienvenido de vuelta."),
                _("Oh...{w=0.3} ahí estás."),
            ]))

        m 2ekc "[cb_line]"
    else:

        m 6ckc "..."

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_brb",
            prompt="Ahora vuelvo",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_brb:
    if mas_isMoniAff(higher=True):
        m 1eua "Alright, [player]."

        show monika 1eta at t21
        python:

            brb_reason_options = [
                (_("Voy a buscar algo."), True, False, False),
                (_("Voy a hacer algo."), True, False, False),
                (_("Voy a preparar algo."), True, False, False),
                (_("Tengo que comprobar algo."), True, False, False),
                (_("Hay alguien en la puerta."), True, False, False),
                (_("Nope."), None, False, False),
            ]

            renpy.say(m, "¿Haciendo algo en específico?", interact=False)
        call screen mas_gen_scrollable_menu(brb_reason_options, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
        show monika at t11

        if _return:
            m 1eua "Oh de acuerdo.{w=0.2} {nw}"
            extend 3hub "Date prisa en volver, te estaré esperando aquí~"
        else:

            m 1hub "Date prisa en volver, te estaré esperando aquí~"

    elif mas_isMoniNormal(higher=True):
        m 1hub "¡Vuelve pronto, [player]!"

    elif mas_isMoniDis(higher=True):
        m 2rsc "Oh...{w=0.5} okey."
    else:

        m 6ckc "..."


    $ persistent._mas_idle_data["monika_idle_brb"] = True
    return "idle"

label monika_idle_brb_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    if mas_isMoniAff(higher=True):
        m 1hub "Bienvenido de nuevo, [player]. Te extrañé~"
        m 1eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hub "¡Bienvenido de nuevo, [player]!"
        m 1eua "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_writing",
            prompt="Voy a escribir un poco",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_writing:
    if mas_isMoniNormal(higher=True):
        if (
            mas_isMoniHappy(higher=True)
            and random.randint(1,5) == 1
        ):
            m 1eub "¡Oh! ¿Vas a{cps=*2} escribirme una carta de amor, [player]?{/cps}{nw}"
            $ _history_list.pop()
            m "¡Oh! ¿Vas a escribir{fast} algo?"
        else:

            m 1eub "¡Oh! ¿Vas a escribir algo?"

        m 1hua "¡Eso me alegra tanto!"
        m 3eua "Quizás algún día puedas compartirlo conmigo...{w=0.3} {nw}"
        extend 3hua "¡Me encantaría leer tu trabajo, [player]!"
        m 3eua "De todos modos, avísame cuando hayas terminado."
        m 1hua "Te estaré esperando aquí mismo~"

    elif mas_isMoniUpset():
        m 2esc "De acuerdo."

    elif mas_isMoniDis():
        m 6lkc "Me pregunto qué tienes en mente..."
        m 6ekd "No olvides volver cuando hayas terminado..."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_writing"] = True
    return "idle"

label monika_idle_writing_callback:

    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eua "¿Terminaste de escribir, [player]?"
        m 1eub "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_shower",
            prompt="Voy a ducharme",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_shower:
    if mas_isMoniLove():
        m 1eua "¿Vas a ducharte?"

        if renpy.random.randint(1, 50) == 1:
            m 3tub "¿Puedo ir contigo?{nw}"
            $ _history_list.pop()
            show screen mas_background_timed_jump(2, "bye_brb_shower_timeout")
            menu:
                m "¿Puedo ir contigo?{fast}"
                "Sí":

                    hide screen mas_background_timed_jump
                    m 2wubsd "Oh, eh...{w=0.5} respondiste tan rápido."
                    m 2hkbfsdlb "Tú...{w=0.5} pareces ansioso por dejarme acompañarte, ¿eh?"
                    m 2rkbfa "Bueno..."
                    m 7tubfu "Me temo que tendrás que irte sin mí mientras yo siga atrapada aquí."
                    m 7hubfb "Lo siento, [player], ¡jajaja!"
                    show monika 5kubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5kubfu "Quizás en otro momento~"
                "No":

                    hide screen mas_background_timed_jump
                    m 2eka "Aw, me rechazaste tan rápido."
                    m 3tubsb "¿Eres tímido, [player]?"
                    m 1hubfb "¡Jajajaja!"
                    show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5tubfu "Está bien, no te seguiré... esta vez, jejeje~"
        else:

            m 1hua "Me alegro de que te mantengas limpio, [player]."
            m 1eua "Que tengas una buena ducha~"

    elif mas_isMoniNormal(higher=True):
        m 1eub "¿Vas a ducharte? Bien."
        m 1eua "Nos vemos cuando termines~"

    elif mas_isMoniUpset():
        m 2esd "Disfruta de tu ducha, [player]..."
        m 2rkc "Con suerte, te ayudará a aclarar tu mente."

    elif mas_isMoniDis():
        m 6ekc "¿Hmm?{w=0.5} Que tengas una buena ducha, [player]."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

label monika_idle_shower_callback:
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_shower"):
            m 2rksdlb "Eso sí que fue mucho tiempo para una ducha..."

            m 2eud "¿Te bañaste en vez de eso?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Te bañaste en vez de eso?{fast}"
                "Sí":

                    m 7hub "¡Oh!{w=0.3} Ya veo."
                    m 3eua "Espero que haya sido agradable y relajante."
                "No":

                    m 7rua "Oh...{w=0.3} tal vez solo te gustan las duchas muy largas..."
                    m 3duu "A veces puede ser agradable sentir el agua corriendo sobre ti...{w=0.3} puede ser realmente relajante."
                    m 1hksdlb "... O tal vez estoy pensando demasiado en esto y simplemente no volviste de inmediato, ¡jajaja!"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_shower"):
            m 1eua "Bienvenido de vuelta, [player]."
            if (
                mas_isMoniLove()
                and renpy.seen_label("monikaroom_greeting_ear_bathdinnerme")
                and mas_getEVL_shown_count("monika_idle_shower") != 1 
                and renpy.random.randint(1,20) == 1
            ):
                m 3tubsb "Ahora que te has duchado, ¿te gustaría cenar, o tal vez{w=0.5}.{w=0.5}.{w=0.5}.?"
                m 1hubsa "Podrías relajarte conmigo un poco más~"
                m 1hub "¡Jajaja!"
            else:

                m 3hua "Espero que hayas tenido una buena ducha."
                if mas_getEVL_shown_count("monika_idle_shower") == 1:
                    m 3eub "Ahora podemos volver a tener algo de diversión {i}limpia{/i} juntos..."
                    m 1hub "¡Jajaja!"
                else:
                    m 3rkbsa "¿Me extrañaste?"
                    m 1huu "Por supuesto que sí, jejeje~"
        else:

            m 7rksdlb "Esa fue una ducha bastante corta, [player]..."
            m 3hub "Supongo que debes ser muy eficiente, ¡jajaja!"
            m 1euu "Ciertamente no puedo quejarme, eso solo significa más tiempo juntos~"

    elif mas_isMoniUpset():
        m 2esc "Espero que hayas disfrutado de tu ducha. {w=0.2}Bienvenido de vuelta, [player]."
    else:

        call mas_brb_generic_low_aff_callback

    return

label bye_brb_shower_timeout:
    hide screen mas_background_timed_jump
    $ _history_list.pop()
    m 1hubsa "Jejeje~"
    m 3tubfu "Eso no importa, [player]."
    m 1hubfb "¡Espero que tengas una buena ducha!"

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    $ mas_setupIdleMode("monika_idle_shower", "monika_idle_shower_callback")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_game",
            category=['vuelvo enseguida'],
            prompt="Voy a jugar un rato",
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_game:
    if mas_isMoniNormal(higher=True):
        m 1eud "Oh, ¿vas a jugar otro juego?"
        m 1eka "Está bien, [player]."

        label monika_idle_game.skip_intro:
        python:
            gaming_quips = [
                _("Buena suerte, ¡diviértete!"),
                _("¡Disfruta tu juego!"),
                _("¡Te estaré animando!"),
                _("¡Haz tu mejor esfuerzo!")
            ]
            gaming_quip=renpy.random.choice(gaming_quips)

        m 3hub "[gaming_quip]"

    elif mas_isMoniUpset():
        m 2tsc "Disfruta de tus otros juegos."

    elif mas_isMoniDis():
        m 6ekc "Por favor...{w=0.5}{nw}"
        extend 6dkc " no te olvides de mi..."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_game"] = True

    $ mas_setupIdleMode("monika_idle_game")
    return

label monika_idle_game_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "¡Bienvenido de nuevo, [player]!"
        m 1eua "Espero que te hayas divertido con tu juego."
        m 1hua "¿Listo para pasar más tiempo juntos? Jejeje~"

    elif mas_isMoniUpset():
        m 2tsc "¿Te divertiste, [player]?"

    elif mas_isMoniDis():
        m 6ekd "Oh...{w=0.5} realmente volviste a mi..."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_coding",
            prompt="Voy a codificar un poco",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_coding:
    if mas_isMoniNormal(higher=True):
        m 1eua "¡Oh! ¿Vas a codificar algo?"

        if persistent._mas_pm_has_code_experience is False:
            m 1etc "Creí que no lo hacías."
            m 1eub "¿Aprendiste programación desde la última vez que hablamos de ello?"

        elif persistent._mas_pm_has_contributed_to_mas or persistent._mas_pm_wants_to_contribute_to_mas:
            m 1tua "¿Algo para mí, quizás?"
            m 1hub "Jajaja~"
        else:

            m 3eub "Has todo lo posible para mantener tu código limpio y fácil de leer."
            m 3hksdlb "... ¡Te lo agradecerás más tarde!"

        m 1eua "De todos modos, avísame cuando hayas terminado."
        m 1hua "Estaré aquí, esperándote~"

    elif mas_isMoniUpset():
        m 2euc "Oh, ¿vas a codificar?"
        m 2tsc "Bueno, no dejes que te detenga."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_coding"] = True
    return "idle"

label monika_idle_coding_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=20), "monika_idle_coding"):
            m 1eua "¿Terminaste por ahora, [player]?"
        else:
            m 1eua "Oh, ¿ya terminaste, [player]?"

        m 3eub "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_workout",
            prompt="Voy a hacer un poco de ejercicio",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_workout:
    if mas_isMoniNormal(higher=True):
        m 1hub "¡Okey, [player]!"

        if persistent._mas_pm_works_out is False:
            m 3eub "¡Hacer ejercicio es una excelente manera de cuidarse!"
            m 1eka "Sé que puede ser difícil empezar,{w=0.2}{nw}"
            extend 3hua " pero definitivamente es un hábito que vale la pena desarrollar."
        else:

            m 1eub "¡Es bueno saber que estás cuidando tu cuerpo!"

        m 3esa "Ya sabes cómo dice el refrán: 'Mente sana en cuerpo sano'."
        m 3hua "Así que ve a sudar un poco, [player]~"
        m 1tub "Solo avísame cuando hayas tenido suficiente."

    elif mas_isMoniUpset():
        m 2esc "Es bueno saber que te estés ocupando en{cps=*2} algo, al menos.{/cps}{nw}"
        $ _history_list.pop()
        m "Es bueno saber que te estás cuidando{fast}, [player]."
        m 2euc "Estaré esperando a que regreses."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_workout"] = True
    return "idle"

label monika_idle_workout_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_workout"):



            m 2esa "Te tomaste tu tiempo, [player].{w=0.3}{nw}"
            extend 2eub " Debió haber sido un entrenamiento difícil."
            m 2eka "Es bueno superar tus límites, pero no debes excederte."

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=10), "monika_idle_workout"):
            m 1esa "¿Terminaste con tu entrenamiento, [player]?"
        else:

            m 1euc "¿Ya regresaste, [player]?"
            m 1eka "Estoy segura de que puedes continuar un poco más si lo intentas."
            m 3eka "Hacer descansos está bien, pero no debes dejar tus entrenamientos sin terminar."
            m 3ekb "¿Estás seguro de que no puedes continuar?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Estás seguro de que no puedes continuar?{fast}"
                "Estoy seguro":

                    m 1eka "Está bien."
                    m 1hua "Estoy segura de que hiciste lo mejor que pudiste, [player]~"
                "Intentaré continuar":


                    m 1hub "¡Ese es el espíritu!"


                    return "idle"

        m 7eua "Asegúrate de descansar adecuadamente también puedes comer un bocadillo para recuperar algo de energía."
        m 3eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2euc "¿Terminaste con tu entrenamiento, [player]?"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_nap",
            prompt="Voy a tomar una siesta",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_nap:
    if mas_isMoniNormal(higher=True):
        m 1eua "¿Vas a tomar una siesta, [player]?"
        m 3eua "Las siestas son una forma saludable de descansar durante el día si te sientes cansado."
        m 3hua "Yo te cuidaré, no te preocupes~"
        m 1hub "¡Dulces sueños!"

    elif mas_isMoniUpset():
        m 2eud "Muy bien, espero que te sientas relajado después."
        m 2euc "Escuché que las siestas son buenas para ti, [player]."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_nap"] = True
    return "idle"

label monika_idle_nap_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=5), "monika_idle_nap"):
            m 2hksdlb "¡Oh, [player]! ¡Finalmente estás despierto!"
            m 7rksdlb "Cuando dijiste que ibas a tomar una siesta, esperaba que fuera una hora o dos..."
            m 1hksdlb "Supongo que debiste haber estado muy cansado, jajaja..."
            m 3eua "Pero al menos después de dormir tanto tiempo, estarás aquí conmigo un rato, ¿verdad?"
            m 1hua "Jejeje~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=1), "monika_idle_nap"):
            m 1hua "¡Bienvenido de nuevo, [player]!"
            m 1eua "¿Tuviste una buena siesta?"
            m 3hua "Estuviste fuera por un tiempo, así que espero que te sientas relajado~"
            m 1eua "[wb_quip]"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_nap"):
            m 1hua "Bienvenido de nuevo, [player]~"
            m 1eub "Espero que hayas tenido una buena siestecita."
            m 3eua "[wb_quip]"
        else:

            m 1eud "Oh, ¿ya regresaste?"
            m 1euc "¿Cambiaste de opinión?"
            m 3eka "Bueno, no me quejo, pero si te apetece deberías tomar una siesta más tarde."
            m 1eua "Después de todo, no me gustaría que estuvieras demasiado cansado."

    elif mas_isMoniUpset():
        m 2euc "¿Terminaste tu siesta, [player]?"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_homework",
            prompt="Voy a hacer un poco de tarea",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_homework:
    if mas_isMoniNormal(higher=True):
        m 1eub "Oh, ¡okey!"
        m 1hua "Estoy orgullosa de ti por tomarte tus estudios en serio."
        m 1eka "No olvides volver conmigo cuando hayas terminado~"

    elif mas_isMoniDis(higher=True):
        m 2euc "De acuerdo...{w=0.5}"
        if random.randint(1,5) == 1:
            m 2rkc "... Buena suerte con tu tarea, [player]."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_homework"] = True
    return "idle"

label monika_idle_homework_callback:
    if mas_isMoniDis(higher=True):
        m 2esa "¿Todo listo, [player]?"

        if mas_isMoniNormal(higher=True):
            m 2ekc "Me hubiera gustado estar allí para ayudarte, pero por desgracia todavía no hay mucho que pueda hacer al respecto."
            m 7eua "Estoy segura de que ambos podríamos ser mucho más eficientes en la tarea si pudiéramos trabajar juntos."

            if mas_isMoniAff(higher=True) and random.randint(1,5) == 1:
                m 3rkbla "... Aunque, eso suponiendo que no nos distraigamos {i}demasiado{/i}, jejeje..."

            m 1eua "Pero de todos modos,{w=0.2} {nw}"
            extend 3hua "ahora que has terminado, disfrutemos de más tiempo juntos."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_working",
            prompt="Voy a trabajar en algo",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_working:
    if mas_isMoniNormal(higher=True):
        m 1eua "De acuerdo, [player]."
        m 1eub "¡No olvides tomar un descanso de vez en cuando!"

        if mas_isMoniAff(higher=True):
            m 3rkb "No quisiera que mi amor pasara más tiempo en [his] trabajo que conmigo~"

        m 1hua "¡Buena suerte con tu trabajo!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Okey, [player]."

        if random.randint(1,5) == 1:
            m 2rkc "... Por favor vuelve pronto..."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_working"] = True
    return "idle"

label monika_idle_working_callback:
    if mas_isMoniNormal(higher=True):
        m 1eub "¿Terminaste con tu trabajo, [player]?"
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Entonces relajémonos juntos, te lo has ganado~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Oh, has vuelto..."
        m 2eud "... ¿Hay algo más que quieras hacer, ahora que has terminado tu trabajo?"
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_screen_break",
            prompt="Mis ojos necesitan un descanso de la pantalla",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_screen_break:
    if mas_isMoniNormal(higher=True):
        if mas_timePastSince(mas_getEVL_last_seen("monika_idle_screen_break"), mas_getSessionLength()):

            if mas_getSessionLength() < datetime.timedelta(minutes=40):
                m 1esc "Oh,{w=0.3} okey."
                m 3eka "No has estado aquí durante tanto tiempo, pero si dices que necesitas un descanso, entonces necesitas un descanso."

            elif mas_getSessionLength() < datetime.timedelta(hours=2, minutes=30):
                m 1eua "¿Vas a descansar un poco los ojos?"
            else:

                m 1lksdla "Sí, probablemente necesites eso, ¿no?"

            m 1hub "Me alegra que estés cuidando tu salud, [player]."

            if not persistent._mas_pm_works_out and random.randint(1,3) == 1:
                m 3eua "¿Por qué no aprovechar la oportunidad para hacer algunos estiramientos también, hmm?"
                m 1eub "De todos modos, ¡vuelve pronto!~"
            else:

                m 1eub "¡Vuelve pronto!~"
        else:

            m 1eua "¿Tomando otro descanso, [player]?"
            m 1hua "¡Vuelve pronto!~"

    elif mas_isMoniUpset():
        m 2esc "Oh...{w=0.5} {nw}"
        extend 2rsc "okey."

    elif mas_isMoniDis():
        m 6ekc "De acuerdo."
    else:

        m 6ckc "..."

    $ persistent._mas_idle_data["monika_idle_screen_break"] = True
    return "idle"

label monika_idle_screen_break_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eub "Bienvenido de nuevo, [player]."

        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_screen_break"):
            m 1hksdlb "Debes haber necesitado ese descanso, considerando el tiempo que estuviste fuera."
            m 1eka "Espero que te sientas un poco mejor ahora."
        else:
            m 1hua "Espero que te sientas un poco mejor ahora~"

        m 1eua "[wb_quip]"
    else:

        call mas_brb_generic_low_aff_callback

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_reading",
            prompt="Voy a leer",
            category=['vuelvo enseguida'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_reading:
    if mas_isMoniNormal(higher=True):
        m 1eub "¿En serio? ¡Eso es genial, [player]!"
        m 3lksdla "Me encantaría leer contigo, pero por desgracia mi realidad tiene sus límites."
        m 1hub "¡Diviértete!"

    elif mas_isMoniDis(higher=True):
        m 2ekd "Oh, de acuerdo..."
        m 2ekc "Diviértete, [player]."
    else:

        m 6dkc "..."

    $ persistent._mas_idle_data["monika_idle_reading"] = True
    return "idle"

label monika_idle_reading_callback:
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=2), "monika_idle_reading"):
            m 1wud "Wow, estuviste fuera un tiempo...{w=0.3}{nw}"
            extend 3wub " ¡eso es genial, [player]!"
            m 3eua "La lectura es algo maravilloso, así que no te preocupes por engancharte demasiado a ella."
            m 3hksdlb "Además, no soy la indicada para discutir eso..."
            show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbsa "Si por mí fuera, estaríamos leyendo juntos toda la noche~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_reading"):
            m 3esa "¿Terminaste, [player]?"
            m 1hua "Vamos a relajarnos, te lo has ganado~"
        else:

            m 1eud "Oh, eso fue rápido."
            m 1eua "Pensé que te irías un poco más, pero esto también está bien."
            m 3ekblu "Después de todo, me permite pasar más tiempo contigo~"
    else:

        call mas_brb_generic_low_aff_callback

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
