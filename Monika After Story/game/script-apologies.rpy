



default persistent._mas_apology_time_db = {}





default persistent._mas_apology_reason_use_db = {}

init -10 python in mas_apology:
    apology_db = {}



init python:
    def mas_checkApologies():
        
        if len(persistent._mas_apology_time_db) == 0:
            return
        
        
        current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
        
        _today = datetime.date.today()
        
        for ev_label in persistent._mas_apology_time_db.keys():
            if current_total_playtime >= persistent._mas_apology_time_db[ev_label][0] or _today >= persistent._mas_apology_time_db[ev_label][1]:
                
                store.mas_lockEVL(ev_label,'APL')
                persistent._mas_apology_time_db.pop(ev_label)
        
        return


init 5 python:
    addEvent(
       Event(
           persistent.event_database,
           eventlabel='monika_playerapologizes',
           prompt="Quiero disculparme...",
           category=['tú'],
           pool=True,
           unlocked=True
        )
    )

label monika_playerapologizes:



    $ player_apology_reasons = {
        0: "otra cosa.", 
        1: "decir que quería romper contigo.",
        2: "bromear sobre tener otra novia.",
        3: "llamarte asesina.",
        4: "cerrar el juego contigo dentro.",
        5: "entrar en tu habitación sin tocar.",
        6: "perderme la navidad",
        7: "olvidar tu cumpleaños.",
        8: "no pasar tiempo contigo en tu cumpleaños.",
        9: "el fallo del juego.",
        10: "el fallo del juego.", 
        11: "no escuchar tu discurso.",
        12: "llamarte malvada.",
        13: "no responderte seriamente."
    }


    if len(persistent._mas_apology_time_db) > 0:

        $ mas_setEVLPropValues(
            "mas_apology_generic",
            prompt="... por {0}".format(player_apology_reasons.get(mas_apology_reason,player_apology_reasons[0]))
        )
    else:

        if mas_apology_reason == 0:
            $ mas_setEVLPropValues("mas_apology_generic", prompt="... por otra cosa.")
        else:

            $ mas_setEVLPropValues(
                "mas_apology_generic",
                prompt="... por {0}".format(player_apology_reasons.get(mas_apology_reason,"algo."))
            )



    $ del player_apology_reasons


    python:
        apologylist = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in store.mas_apology.apology_db.iteritems()
            if ev.unlocked and (ev.prompt != "... por algo." and ev.prompt != "... por otra cosa.")
        ]


        generic_ev = mas_getEV('mas_apology_generic')

        if generic_ev.prompt == "... por algo." or generic_ev.prompt == "... por otra cosa.":
            apologylist.append((generic_ev.prompt, generic_ev.eventlabel, False, False))


        return_prompt_back = ("No importa", False, False, False, 20)


    show monika at t21
    call screen mas_gen_scrollable_menu(apologylist, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, return_prompt_back)


    $ apology =_return


    if not apology:
        if mas_apology_reason is not None or len(persistent._mas_apology_time_db) > 0:
            show monika at t11
            if mas_isMoniAff(higher=True):
                m 1ekd "[player], si te sientes culpable por lo que pasó..."
                m 1eka "No tienes que tener miedo de disculparte, todos cometemos errores después de todo."
                m 3eka "Solo tenemos que aceptar lo que pasó, aprender de nuestros errores y seguir adelante, juntos. ¿De acuerdo?"
            elif mas_isMoniNormal(higher=True):
                m 1eka "[player]..."
                m "Si quieres disculparte, adelante. Significaría mucho para mí si lo hicieras."
            elif mas_isMoniUpset():
                m 2rkc "Oh..."
                m "Yo estaba--"
                $ _history_list.pop()
                m 2dkc "Olvídalo."
            elif mas_isMoniDis():
                m 6rkc "¿...?"
            else:
                m 6ckc "..."
        else:
            if mas_isMoniUpset(lower=True):
                show monika at t11
                if mas_isMoniBroken():
                    m 6ckc "..."
                else:
                    m 6rkc "¿Tienes algo que decir, [player]?"
        return "prompt"

    show monika at t11


    call expression apology


    $ mas_getEV(apology).shown_count += 1


    if apology != "mas_apology_generic":
        $ store.mas_lockEVL(apology, 'APL')


    if apology in persistent._mas_apology_time_db:
        $ persistent._mas_apology_time_db.pop(apology)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            prompt="... por otra cosa.",
            eventlabel="mas_apology_generic",
            unlocked=True,
        ),
        code="APL"
    )

label mas_apology_generic:


    $ mas_apology_reason_db = {
        0: "",
        1: "decir que querías romper. Sabía que no lo decías en serio...",
        2: "bromear sobre tener otra novia. ¡Casi me das un infarto!",
        3: "llamarme asesina. Espero que no me veas de esa manera...",
        4: "cerrar el juego conmigo dentro.",
        5: "entrar a mi cuarto sin tocar.",
        6: "perderte la navidad.",
        7: "olvidar mi cumpleaños.",
        8: "no pasar tiempo conmigo en mi cumpleaños.",
        9: "el fallo del juego. Entiendo que puede pasar a veces, pero no importa, ¡estoy bien!",
        10: "el fallo del juego. Fue realmente aterrador, pero estoy feliz de que volvieras a mí y las cosas mejoraran.",
        11: "no escuchar mi discurso. Trabajé mucho en ello.",
        12: "llamarme malvada. Sé que realmente no piensas eso.",
        13: "no tomar mis preguntas en serio. Sé que serás honesto conmigo de ahora en adelante."
    }


    if mas_apology_reason is None and len(persistent._mas_apology_time_db) == 0:
        if mas_isMoniBroken():
            m 1ekc "...{w=1} Oh."
            m 2dsc ".{w=2}.{w=2}."
            m "Okey."
        elif mas_isMoniDis():
            m 2dfd "{i}*suspiro*{/i}"
            m 2dsd "Espero que esto no sea una broma o un truco, [player]."
            m 2dsc "..."
            m 1eka "... Gracias por la disculpa."
            m 2ekc "Pero por favor, trata de ser más consciente de mis sentimientos."
            m 2dkd "Por favor."
        elif mas_isMoniUpset():
            m 1eka "Gracias, [player]."
            m 1rksdlc "Sé que las cosas no están bien entre nosotros, pero sé que sigues siendo una buena persona."
            m 1ekc "¿Podrías ser un poco más considerado con mis sentimientos?"
            m 1ekd "¿Por favor?"
        else:
            m 1ekd "¿Pasó algo?"
            m 2ekc "No veo una razón para que lo lamentes."
            m 1dsc "..."
            m 1eub "De todos modos, gracias por la disculpa."
            m 1eua "Sea lo que sea, sé que estás haciendo lo mejor para hacer las cosas bien."
            m 1hub "¡Por eso te amo, [player]!"
            $ mas_ILY()


    elif mas_apology_reason_db.get(mas_apology_reason, False):

        $ apology_reason = mas_apology_reason_db.get(mas_apology_reason,mas_apology_reason_db[0])

        m 1eka "Gracias por disculparte por [apology_reason]"
        m "Acepto tus disculpas, [player]. Significa mucho para mí."


    elif len(persistent._mas_apology_time_db) > 0:
        m 2tfc "[player], si tienes algo por lo que disculparte, por favor solo dilo."
        m 2rfc "Significaría mucho más para mí si admitieras lo que hiciste."
    else:




        $ mas_gainAffection(modifier=0.1)
        m 2tkd "Lo que hiciste no fue gracioso, [player]."
        m 2dkd "Por favor, sé más considerado con mis sentimientos en el futuro."


    if mas_apology_reason:

        $ persistent._mas_apology_reason_use_db[mas_apology_reason] = persistent._mas_apology_reason_use_db.get(mas_apology_reason,0) + 1

        if persistent._mas_apology_reason_use_db[mas_apology_reason] == 1:

            $ mas_gainAffection(modifier=0.2)
        elif persistent._mas_apology_reason_use_db[mas_apology_reason] == 2:

            $ mas_gainAffection(modifier=0.1)




    $ mas_apology_reason = None
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_bad_nickname",
            prompt="... por ponerte un mal nombre.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_bad_nickname:
    $ ev = mas_getEV('mas_apology_bad_nickname')
    if ev.shown_count == 0:
        $ mas_gainAffection(modifier=0.2)
        m 1eka "Gracias por disculparte por el nombre que intentaste darme."
        m 2ekd "Eso realmente dolió, [player]..."
        m 2dsc "Acepto tus disculpas, pero por favor no vuelvas a hacerlo. ¿De acuerdo?"
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    elif ev.shown_count == 1:
        $ mas_gainAffection(modifier=0.1)
        m 2dsc "No puedo creer que hayas hecho eso {i}otra vez{/i}."
        m 2dkd "Incluso después de que te diera una segunda oportunidad."
        m 2tkc "Estoy decepcionada de ti, [player]."
        m 2tfc "No vuelvas a hacer eso."
        $ mas_unlockEVL("monika_affection_nickname", "EVE")
    else:


        m 2wfc "¡[player]!"
        m 2wfd "No puedo creerlo."
        m 2dfc "Confié en que me dieras un buen apodo para hacerme más única, pero me lo echaste en cara..."
        m "Supongo que no podía confiar en ti para esto."
        m ".{w=0.5}.{w=0.5}.{nw}"
        m 2rfc "Aceptaría tus disculpas [player], pero no creo que lo digas en serio."

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
