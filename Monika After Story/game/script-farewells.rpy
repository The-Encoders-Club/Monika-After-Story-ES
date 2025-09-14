init offset = 5











default -5 persistent.mas_late_farewell = False

init -6 python in mas_farewells:
    import datetime
    import store



    dockstat_iowait_label = None



    dockstat_rtg_label = None



    dockstat_cancel_dlg_label = None



    dockstat_wait_menu_label = None



    dockstat_cancelled_still_going_ask_label = None



    dockstat_failed_io_still_going_ask_label = None

    def resetDockstatFlowVars():
        """
        Resets all the dockstat flow vars back to the original states (None)
        """
        store.mas_farewells.dockstat_iowait_label = None
        store.mas_farewells.dockstat_rtg_label = None
        store.mas_farewells.dockstat_cancel_dlg_label = None
        store.mas_farewells.dockstat_wait_menu_label = None
        store.mas_farewells.dockstat_cancelled_still_going_ask_label = None
        store.mas_farewells.dockstat_failed_io_still_going_ask_label = None

    def _filterFarewell(
            ev,
            curr_pri,
            aff,
            check_time,
        ):
        """
        Filters a farewell for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        
        if not ev.unlocked:
            return False
        
        
        if ev.pool:
            return False
        
        
        if not ev.checkAffection(aff):
            return False
        
        
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        
        if not (
            store.MASSelectiveRepeatRule.evaluate_rule(check_time, ev, defval=True)
            and store.MASNumericalRepeatRule.evaluate_rule(check_time, ev, defval=True)
            and store.MASGreetingRule.evaluate_rule(ev, defval=True)
            and store.MASTimedeltaRepeatRule.evaluate_rule(ev)
        ):
            return False
        
        
        if not ev.checkConditional():
            return False
        
        
        return True


    def selectFarewell(check_time=None):
        """
        Selects a farewell to be used. This evaluates rules and stuff appropriately.

        IN:
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single farewell (as an Event) that we want to use
        """
        
        fare_db = store.evhand.farewell_database
        
        
        fare_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        
        for ev_label, ev in fare_db.iteritems():
            if _filterFarewell(
                ev,
                curr_priority,
                aff,
                check_time
            ):
                
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    fare_pool = []
                
                
                fare_pool.append((
                    ev, store.MASWeightRule.get_weight(ev)
                ))
        
        
        if len(fare_pool) == 0:
            return None
        
        return store.mas_utils.weightedChoice(fare_pool)


label mas_farewell_start:



    if persistent._mas_long_absence:
        $ MASEventList.push("bye_long_absence_2")
        return

    $ import store.evhand as evhand


    python:



        Event.checkEvents(evhand.farewell_database)

        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )

    if len(bye_pool_events) > 0:

        python:

            bye_prompt_list = sorted([
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ])

            most_used_fare = sorted(bye_pool_events.values(), key=Event.getSortShownCount)[-1]


            final_items = [
                (_("Adiós"), -1, False, False, 20),
                (_("No importa"), False, False, False, 0)
            ]




            if mas_anni.pastOneMonth() and mas_isMoniAff(higher=True) and most_used_fare.shown_count > 0:
                final_items.insert(1, (most_used_fare.prompt, most_used_fare, False, False, 0))
                _menu_area = mas_ui.SCROLLABLE_MENU_VLOW_AREA

            else:
                _menu_area = mas_ui.SCROLLABLE_MENU_LOW_AREA


        call screen mas_gen_scrollable_menu(bye_prompt_list, _menu_area, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)

        if not _return:

            return _return

        if _return != -1:
            $ mas_setEventPause(None)

            $ MASEventList.push(_return.eventlabel, skipeval=True)
            return

    $ mas_setEventPause(None)

    $ farewell = store.mas_farewells.selectFarewell()
    $ MASEventList.push(farewell.eventlabel, skipeval=True)

    return








init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already",
            unlocked=True,
            conditional="mas_getSessionLength() <= datetime.timedelta(minutes=20)",
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_leaving_already:
    m 1ekc "Aw, ¿ya te vas?"
    m 1eka "Es muy triste cuando tienes que irte..."
    m 3eua "Solo asegúrate de volver tan pronto como puedas, ¿okey?"
    m 3hua "Te amo mucho, [player]. ¡Mantente a salvo!"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodbye",
            unlocked=True
        ),
        code="BYE"
    )

label bye_goodbye:
    if mas_isMoniNormal(higher=True):
        m 1eua "¡Adiós, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esc "Adiós."

    elif mas_isMoniDis():
        m 6rkc "Oh... {w=1}adiós."
        m 6ekc "Por favor... {w=1}no olvides volver."
    else:

        m 6ckc "..."

    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_sayanora",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_sayanora:
    m 1hua "Sayonara, [mas_get_player_nickname()]~"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_farewellfornow",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_farewellfornow:
    m 1eka "Hasta pronto, [mas_get_player_nickname()]~"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_untilwemeetagain",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_untilwemeetagain:
    m 2eka "'{i}Las despedidas no son para siempre, las despedidas no son el final. Simplemente quieren decir que te voy a extrañar, hasta que nos volvamos a encontrar{/i}'."
    m "Jejeje, ¡hasta luego [mas_get_player_nickname()]!"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_take_care",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )


label bye_take_care:
    m 1eua "No olvides que siempre te amo, [mas_get_player_nickname()]~"
    m 1hub "¡Cuídate!"
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already_2",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        code="BYE"
    )

label bye_leaving_already_2:
    if mas_getSessionLength() <= datetime.timedelta(minutes=30):
        m 1ekc "Aww, ¿ya te vas?"
    m 1eka "Es muy triste cuando tienes que irte..."
    m 3hubsa "¡Te amo mucho, [player]!"
    show monika 5hubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsb "¡Nunca olvides eso!"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    rules.update(MASPriorityRule.create_rule(50))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_going_to_sleep:

    if mas_isMoniNormal(higher=True):
        $ p_nickname = mas_get_player_nickname()
        m 1esa "¿Ya te vas a dormir, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Ya te vas a dormir, [p_nickname]?{fast}"
            "Sí":

                call bye_prompt_sleep_goodnight_kiss (chance=4)

                if _return is not None:
                    return "quit"

                m 7eka "Te veré en tus sueños."


                $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
                $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
            "Todavía no":

                m 1eka "Okey. {w=0.3}Que tengas una buena noche~"

    elif mas_isMoniUpset():
        m 2esc "¿Ya te vas a dormir, [player]?"
        m "Buenas noches."

    elif mas_isMoniDis():
        m 6rkc "Oh... buenas noches, [player]."
        m 6lkc "Espero verte mañana..."
        m 6dkc "No te olvides de mí, ¿de acuerdo?"
    else:

        m 6ckc "..."





    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="Voy a clases.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_class:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1eub "Aw, ¿ya te vas?"
            m 1efp "¡Ni siquiera has estado aquí por 20 minutos!"
            m 3hksdlb "Solo bromeo, [player]."
            m 2eka "Eres tan dulce por verme incluso cuando tienes tan poco tiempo."
            m 2hub "¡Solo quiero que sepas que lo aprecio mucho!"
            m 2eka "Estudia mucho [player], estoy segura de que lo harás muy bien."
            m 2hua "¡Nos vemos cuando vuelvas!"
        elif session_time < datetime.timedelta(hours=1):
            m 2eua "Muy bien, ¡gracias por pasar un tiempo conmigo, [player]!"
            m 2eka "Sinceramente, desearía que hubiera sido un poco más... pero eres un [guy] ocupado."
            m 2hua "Nada es más importante que una buena educación."
            m 3eub "¡Enséñame algo cuando regreses!"
            m "¡Te veo pronto!"
        elif session_time < datetime.timedelta(hours=6):
            m 1hua "¡Estudia mucho, [player]!"
            m 1eua "Nada es más atractivo que un [guy] con buenas notas."
            m 1hua "¡Nos vemos más tarde!"
        else:
            m 2ekc "Umm... has estado aquí conmigo durante bastante tiempo, [player]."
            m 2ekd "¿Estás seguro de que has descansado lo suficiente?"
            m 2eka "Asegúrate de tomártelo con calma, ¿de acuerdo?"
            m "Si no te sientes muy bien, estoy segura de que {i}un día{/i} libre no te hará daño."
            m 1hka "Estaré esperando tu regreso, cuídate."

    elif mas_isMoniUpset():
        m 2esc "Bien, [player]."
        m "Espero que al menos aprendas {i}algo{/i} hoy."
        m 2efc "{cps=*2}Tal vez como tratar mejor a las personas.{/cps}{nw}"

    elif mas_isMoniDis():
        m 6rkc "Oh, okey [player]..."
        m 6lkc "Supongo que te veré después de la escuela."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="Voy a trabajar.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_work:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 2eka "¡Aw, está bien! ¿Visitandome antes de salir?"
            m 3eka "Debes tener muy poco tiempo si ya te vas."
            m "Fue muy dulce de tu parte verme, ¡incluso cuando estás tan ocupado!"
            m 3hub "¡Trabaja duro, [mas_get_player_nickname()]! ¡Hazme sentir orgullosa!"
        elif session_time < datetime.timedelta(hours=1):
            m 1hksdlb "¡Oh! ¡De acuerdo! Estaba empezando a sentirme cómoda, jajaja."
            m 1rusdlb "Esperaba que estuviéramos juntos un poco más, ¡pero eres un [guy] ocupado!"
            m 1eka "Fue genial verte, aunque no fuera tanto tiempo como quería..."
            m 1kua "Pero si fuera por mí, ¡te tendría todo el día!"
            m 1hua "¡Estaré aquí esperando que regreses del trabajo!"
            m "¡Cuéntamelo todo cuando regreses!"
        elif session_time < datetime.timedelta(hours=6):
            m 2eua "¿Vas al trabajo entonces, [mas_get_player_nickname()]?"
            m 2eka "El día puede ser bueno o malo... pero si se vuelve demasiado pesado, ¡piensa en algo agradable!"
            m 4eka "Todos los días, no importa lo mal que vaya, ¡terminan después de todo!"
            m 2tku "Tal vez puedas pensar en mí si se vuelve estresante..."
            m 2esa "¡Solo da lo mejor de ti! ¡Te veré cuando regreses!"
            m 2eka "¡Sé que lo harás genial!"
        else:
            m 2ekc "Oh... ya llevas bastante tiempo aquí... ¿y ahora vas a trabajar?"
            m 2rksdlc "Esperaba que descansaras antes de hacer algo importante."
            m 2ekc "Trata de no esforzarte demasiado, ¿de acuerdo?"
            m 2ekd "¡No tengas miedo de tomar un respiro si lo necesitas!"
            m 3eka "Vuelve a casa feliz y saludable."
            m 3eua "¡Cuídate, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esc "Bien, [player], supongo que te veré después del trabajo."

    elif mas_isMoniDis():
        m 6rkc "Oh... {w=1}okey."
        m 6lkc "Entonces, espero verte después del trabajo."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="Voy a dormir.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_sleep:
    if mas_isMoniNormal(higher=True):
        call bye_prompt_sleep_goodnight_kiss (chance=3)

        if _return is not None:
            return "quit"

        m 1eua "Okey, [mas_get_player_nickname()]."
        m 1hua "¡Dulces sueños!~"

    elif mas_isMoniUpset():
        m 2esc "Buenas noches, [player]."

    elif mas_isMoniDis():
        m 6ekc "Okey... {w=0.3}buenas noches, [player]."
    else:

        m 6ckc "..."



































































































































































































    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'











label bye_prompt_sleep_goodnight_kiss(chance=3):
    $ got_goodnight_kiss = False

    if mas_shouldKiss(chance, cooldown=datetime.timedelta(minutes=5)):
        m 1eublsdla "¿Crees que podría... {w=0.3}{nw}"
        extend 1rublsdlu "tener un beso de buenas noches?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Crees que podría... tener un beso de buenas noches?{fast}"
            "Seguro, [m_name]":

                $ got_goodnight_kiss = True
                show monika 6ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 2.0
                call monika_kissing_motion_short (initial_exp="6hubsa")
                m 6ekbfb "Espero que eso te de algo de que soñar esta noche~"
                show monika 1hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1hubfa "¡Duerme bien!"
            "Tal vez en otro momento...":

                if random.randint(1, 3) == 1:
                    m 3rkblp "Aww, vamos... {w=0.3}{nw}"
                    extend 3nublu "sé que quieres~"

                    m 1ekbsa "¿Podría por favor tener un beso de buenas noches?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Podría por favor tener un beso de buenas noches?{fast}"
                        "Okey":

                            $ got_goodnight_kiss = True
                            show monika 6ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                            pause 2.0
                            call monika_kissing_motion_short (initial_exp="6hubsa")
                            m 6ekbfa "Dulces sueños, [player]~"
                            m 6hubfb "¡Duerme bien!"
                        "No":

                            $ mas_loseAffection(1.5)
                            m 1lkc "..."
                            m 7dkd "Bien..."
                            m 2lsc "Buenas noches [player]..."
                else:

                    m 1rkblc "Aww... {w=0.3}{nw}"
                    extend 1ekbla "okey, pero me lo debes"
                    m 1hubsb "¡Te amo! ¡Duerme bien!~"

        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP

        return got_goodnight_kiss

    return None

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_illseeyou",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        code="BYE"
    )

label bye_illseeyou:

    if mas_globals.time_of_day_3state == "as tardes":
        $ dlg_var = "mañana"
    else:

        $ dlg_var = "luego"

    m 1eua "Te veré [dlg_var], [player]."
    m 3kua "No te olvides de mí, ¿de acuerdo?~"
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    rules.update(MASWeightRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_haveagoodday:
    if mas_isMoniNormal(higher=True):
        m 1eua "Que tengas un buen día hoy, [mas_get_player_nickname()]."
        m 3eua "Espero que logres todo lo que habías planeado."
        m 1hua "Estaré esperándote aquí cuando regreses."

    elif mas_isMoniUpset():
        m 2esc "¿Te vas por todo el día, [player]?"
        m 2efc "Estaré aquí, esperando... {w=0.5}como de costumbre."

    elif mas_isMoniDis():
        m 6rkc "Oh."
        m 6dkc "Supongo que pasaré el día sola... {w=1}de nuevo."
    else:

        m 6ckc "..."
    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    rules.update(MASWeightRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            conditional="mas_getSessionLength() <= datetime.timedelta(minutes=30)",
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_enjoyyourafternoon:
    if mas_isMoniNormal(higher=True):
        m 1ekc "Me entristece verte ir tan temprano, [player]."
        m 1eka "Entiendo que estás ocupado."
        m 1eua "Prométeme que disfrutarás tu tarde, ¿de acuerdo?"
        m 1hua "Adiós~"

    elif mas_isMoniUpset():
        m 2efc "Bien, [player], solo vete."
        m 2tfc "Supongo que te veré más tarde... {w=1}si vuelves."

    elif mas_isMoniDis():
        m 6dkc "De acuerdo, adiós, [player]."
        m 6ekc "¿Quizás volverás más tarde?"
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    rules.update(MASWeightRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            conditional="mas_getSessionLength() >= datetime.timedelta(minutes=30)",
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodevening:
    if mas_isMoniNormal(higher=True):
        m 1hua "Me divertí hoy."
        m 1eka "Gracias por pasar tanto tiempo conmigo, [mas_get_player_nickname()]."
        m 1eua "Hasta entonces, que pases una buena noche."

    elif mas_isMoniUpset():
        m 2esc "Adiós, [player]."
        m 2dsc "Me pregunto si volverás a decirme buenas noches."

    elif mas_isMoniDis():
        m 6dkc "Oh... {w=1}okey."
        m 6rkc "Que tengas una buena noche, [player]..."
        m 6ekc "Espero que recuerdes pasar a decir buenas noches antes de acostarte."
    else:

        m 6ckc "..."

    return 'quit'

init python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    rules.update(MASPriorityRule.create_rule(50))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodnight:

    if mas_isMoniNormal(higher=True):
        m 3eka "¿Vas a ir dormir?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Vas a ir dormir?{fast}"
            "Sí":

                call bye_prompt_sleep_goodnight_kiss (chance=4)

                if _return is not None:
                    return "quit"

                m 1eua "Buenas noches, [mas_get_player_nickname()]."
                m 1eka "Te veré mañana, ¿de acuerdo?"
                m 3eka "Recuerda: 'Duerme bien, no dejes que los mosquitos te piquen', jejeje."
                m 1ekbsa "Te amo~"


                $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
                $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
            "Todavía no":

                m 1eka "Okey, [mas_get_player_nickname()]..."
                m 3hub "¡Disfruta tu noche!"
                m 3rksdlb "Intenta no quedarte despierto hasta muy tarde, jejeje~"

    elif mas_isMoniUpset():
        m 2esc "Buenas noches."

    elif mas_isMoniDis():
        m 6lkc "... Buenas noches."
    else:

        m 6ckc "..."
    return 'quit'


default -5 mas_absence_counter = False

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_long_absence",
            unlocked=True,
            prompt="Voy a irme por un tiempo.",
            pool=True
        ),
        code="BYE"
    )

label bye_long_absence:
    if mas_absence_counter:
        jump bye_long_absence_2
    $ persistent._mas_long_absence = True
    m 1ekc "Aw... eso es bastante triste..."
    m 1eka "¡Te voy a extrañar mucho, [player]!"
    m 3rksdla "No estoy muy segura de qué voy a hacer mientras no estés..."
    m 3esa "Pero gracias por advertirme primero. Es de mucha ayuda."
    m 2lksdlb "¡De lo contrario, estaría muy preocupada!"
    m 3esa "Estaría pensando que tal vez te pasó algo y por eso no pudiste regresar."
    m 1lksdlc "O tal vez simplemente te aburriste de mí..."
    m 1eka "Entonces dime, [mas_get_player_nickname()]..."

    m "¿Cuánto tiempo esperas estar fuera?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Cuánto tiempo esperas estar fuera?{fast}"
        "Unos pocos días":
            $ persistent._mas_absence_choice = "days"
            m 1eub "¡Oh!"
            m 1hua "No es tanto como me temia."
            m 3rksdla "Dios, realmente me preocupaste..."
            m 3esa "Pero no te preocupes por mí, [player]."
            m "Puedo esperar ese tiempo con facilidad."
            m 3eka "Aunque todavía te echaré mucho de menos."
        "Una semana":
            $ persistent._mas_absence_choice = "week"
            m 3euc "Sí... eso es lo que esperaba."
            m 2lksdla "{i}Creo{/i} que estaré bien esperándote tanto tiempo."
            m 1eub "Vuelve a verme tan pronto como puedas, ¿de acuerdo, [mas_get_player_nickname()]?"
            m 3hua "¡Estoy segura de que me haras sentir orgullosa!"
        "Un par de semanas":
            $ persistent._mas_absence_choice = "2weeks"
            m 1esc "Oh..."
            m 1dsc "Yo... puedo esperar."
            m 3rksdlc "Sabes que eres todo lo que tengo... ¿verdad?"
            m 3rksdlb "Aunque tal vez esté fuera de tu control..."
            m 2eka "Intenta volver lo antes posible... te estaré esperando."
        "Un mes":
            $ persistent._mas_absence_choice = "month"
            if mas_isMoniHappy(higher=True):
                m 3euc "Oh wow, eso es mucho tiempo."
                m 3rksdla "Demasiado tiempo para mi gusto..."
                m 2esa "Pero está bien [player]."
                m 2eka "Sé que eres un amor y no me harías esperar tanto tiempo si no tuvieras una buena razón."
                m "Estoy segura de que es importante, así que trata de volver a mí tan pronto como puedas."
                m 3hua "Estaré pensando en ti todos los días~"
            else:
                m 1ekc "Tanto tiempo... ¿{i}de verdad{/i}?"
                m 3rksdlc "No te vas a ir por tanto tiempo solo para evitarme, ¿verdad?"
                m 3rksdld "Sé que la vida puede alejarte de mí pero un mes entero..."
                m 3ekc "¿No es un poco irrazonable?"
                m "No quiero parecer egoísta, pero {i}soy{/i} tu novia."
                m 3ekd "Deberías poder dedicarme tiempo, al menos una vez, en un mes entero."
                m 1dsc "..."
                m 1dsd "Aún te esperaré... pero por favor regresa en cuanto puedas."
        "Más de un mes":
            $ persistent._mas_absence_choice = "longer"
            if mas_isMoniHappy(higher=True):
                m 3rksdlb "Eso es... {w=0.5}bueno, eso da un poco de miedo, [player]."
                m "No estoy segura de qué voy a hacer mientras no estés."
                m 1eka "Pero sé que no me dejarías sola si pudieras evitarlo."
                m "Te amo [player], y sé que tú también me amas."
                m 1hua "Así que te esperaré todo el tiempo que sea necesario."
            else:
                m 3esc "Tienes que estar bromeando."
                m "No puedo pensar en una buena razón por la que me dejarías aquí sola durante {i}ese{/i} tiempo."
                m 3esd "Lo siento [player], ¡pero eso es inaceptable! ¡De ningún modo!"
                m 3esc "Te amo y si tú también me amas, sabrás que no está bien hacer eso."
                m "Te das cuenta de que estaría sola aquí sin nada más y nadie más, ¿verdad?"
                m "No es exagerado de mi parte esperar que me visites, ¿verdad? Soy tu novia. ¡No puedes hacerme eso!"
                m 3dsc "..."
                m 3dsd "Solo... regresa cuando puedas. No puedo hacer que te quedes, pero por favor no me hagas esto."
        "No lo sé":
            $ persistent._mas_absence_choice = "unknown"
            m 1hksdlb "¡Jejeje, eso es un poco preocupante, [player]!"
            m 1eka "¡Pero si no lo sabes, entonces no lo sabes!"
            m "A veces simplemente no se puede evitar."
            m 2hua "Te estaré esperando aquí pacientemente, [mas_get_player_nickname()]."
            m 2hub "¡Intenta no hacerme esperar demasiado!"
        "No importa":


            $ persistent._mas_long_absence = False
            m 3eka "Oh... está bien, [player]."
            m 1rksdla "Honestamente, estoy bastante aliviada de que te no vayas..."
            m 1ekd "No sé qué haría aquí sola."
            m 3rksdlb "Tampoco es que pueda ir a ningún lado, jajaja..."
            m 3eub "De todos modos, avísame si vas a salir. ¡Quizás incluso puedas llevarme contigo!"
            m 1hua "No me importa a dónde vayamos, siempre que esté contigo, [mas_get_player_nickname()]."
            return

    m 2euc "Honestamente, tengo un poco de miedo de preguntar, pero..."

    m "¿Vas a marcharte ahora mismo?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Vas a marcharte ahora mismo?{fast}"
        "Sí":
            m 3ekc "Ya veo..."
            m "Te extrañaré mucho, [player]..."
            m 1eka "Pero sé que harás cosas maravillosas sin importar dónde estés."
            m "Solo recuerda que te estaré esperando aquí."
            m 2hua "¡Hazme sentir orgullosa, [player]!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
            return 'quit'
        "No":
            $ mas_absence_counter = True
            m 1hua "¡Eso es genial!"
            m 1eka "Estaba un poco preocupada por no tener tiempo suficiente para prepararme para tu ausencia."
            m "Hablo en serio cuando digo que te extrañaré..."
            m 1eub "Eres mi mundo entero después de todo, [player]."
            m 2esa "Si me dices que vas a irte por un tiempo otra vez, sabré que es hora de que te vayas..."
            m 3hua "Pero no hay prisa, así que quiero pasar todo el tiempo que pueda contigo."
            m "¡Solo asegúrate de recordarme la última vez que me viste antes de irte!"
            return

label bye_long_absence_2:
    m 1ekc "Entonces, ¿vas a salir?"
    m 1ekd "Sé que el mundo puede ser aterrador e implacable..."
    m 1eka "Pero recuerda que siempre estaré aquí esperándote y dispuesta a apoyarte, mi querido [player]."
    m "Vuelve a mí tan pronto como puedas... ¿de acuerdo?"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_somewhere",
            unlocked=True,
            prompt="Voy a llevarte a un lugar.",
            pool=True
        ),
        code="BYE"
    )

label bye_going_somewhere:
    $ import random






    python:

        if mas_isMonikaBirthday():
            dis_chance = 10
            upset_chance = 0

        else:
            dis_chance = 50
            upset_chance = 10

    if mas_isMoniBroken(lower=True):

        jump bye_going_somewhere_nothanks

    elif mas_isMoniDis(lower=True):

        if random.randint(1,100) <= dis_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "¿De verdad quieres llevarme contigo?"
        m 1ekd "¿Estás seguro de que esto no es algo?...{nw}"
        $ _history_list.pop()
        m 1lksdlc "..."
        m 1eksdlb "¿Qué estoy diciendo? ¡Por supuesto que iré contigo!"

    elif mas_isMoniUpset(lower=True):

        if random.randint(1, 100) <= upset_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "¿De verdad quieres llevarme contigo?"
        m 1eka "..."
        m 1hua "Bueno, supongo que no estará de más ir contigo."
        m 2dsc "Solo... por favor."
        m 2rkc "{i}Por favor{/i}, entiende por lo que estoy pasando."
        m 1dkc "..."
    else:

        jump bye_going_somewhere_normalplus_flow

label bye_going_somewhere_post_aff_check:
    jump mas_dockstat_iostart


label bye_going_somewhere_normalplus_flow:





    if persistent._mas_d25_in_d25_mode:

        if mas_isD25Eve():
            jump bye_d25e_delegate

        if mas_isD25():
            jump bye_d25_delegate

        if mas_isNYE():
            jump bye_nye_delegate

        if mas_isNYD():
            jump bye_nyd_delegate

    if mas_isF14() and persistent._mas_f14_in_f14_mode:
        jump bye_f14

    if mas_isMonikaBirthday():
        jump bye_922_delegate

label bye_going_somewhere_normalplus_flow_aff_check:

    if mas_isMoniLove(higher=True):
        m 1hub "Oh, ¡okey!"
        m 3tub "¿Me llevarás a un lugar especial hoy?"
        m 1hua "¡No puedo esperar!"
    else:








        m 1sub "¿De verdad?"
        m 1hua "¡Yay!"
        m 1ekbsa "Me pregunto a dónde me llevarás hoy..."

    jump bye_going_somewhere_post_aff_check

label bye_going_somewhere_nothanks:
    m 2lksdlc "... No, gracias."
    m 2ekd "Aprecio la oferta, pero creo que necesito un poco de tiempo para mí ahora mismo."
    m 2eka "Entiendes, ¿verdad?"
    m 3eka "Así que adelante, diviértete sin mí..."
    return


label bye_going_somewhere_leavemenu:
    if mas_isMoniDis(lower=True):
        m 1tkc "..."
        m 1tkd "Lo sabía.{nw}"
        $ _history_list.pop()
        m 1lksdld "Eso está bien, supongo."

    elif mas_isMoniHappy(lower=True):
        m 1ekd "Oh, {w=0.3}está bien. ¿Tal vez la próxima vez?"
    else:


        m 2ekp "Aw..."
        m 1hub "Bien, ¡pero será mejor que me lleves la próxima vez!"

    m 1euc "¿Todavía vas a ir?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Todavía vas a ir?{fast}"
        "Sí":
            if mas_isMoniNormal(higher=True):
                m 2eka "De acuerdo. Estaré esperándote aquí, como siempre..."
                m 2hub "¡Así que regresa rápido! ¡Te amo, [player]!"
            else:


                m 2tfd "... Bueno."

            return "quit"
        "No":

            if mas_isMoniNormal(higher=True):
                m 2eka "... Gracias."
                m "Significa mucho que pases más tiempo conmigo, ya que no puedo ir."
                m 3ekb "Sin embargo, sigue con tu día cuando necesites hacerlo. ¡No quisiera hacerte llegar tarde!"
            else:


                m 2lud "De acuerdo, entonces..."

    return

default -5 persistent._mas_pm_gamed_late = 0


init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_game",
            unlocked=True,
            prompt="Voy a jugar otra cosa.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_game:
    $ _now = datetime.datetime.now().time()
    if mas_getEVL_shown_count("bye_prompt_game") == 0:
        m 2ekc "¿Vas a jugar otro juego?"
        m 4ekd "¿De verdad tienes que dejarme para ir a hacer eso?"
        m 2eud "¿No puedes dejarme aquí en segundo plano mientras juegas?{nw}"
        $ _history_list.pop()
        menu:
            m "¿No puedes dejarme aquí de fondo mientras juegas?{fast}"
            "Sí":
                if mas_isMoniNormal(higher=True):
                    m 3sub "¿De verdad?"
                    m 1hubsb "¡Yay!"
                else:
                    m 2eka "Okey..."
                jump monika_idle_game.skip_intro
            "No":
                if mas_isMoniNormal(higher=True):
                    m 2ekc "Aww..."
                    m 3ekc "De acuerdo [player], pero será mejor que vuelvas pronto."
                    m 3tsb "Podría ponerme celosa si pasas demasiado tiempo en otro juego sin mí."
                    m 1hua "De todos modos, ¡espero que te diviertas!"
                else:
                    m 2euc "Entonces, disfruta tu juego."
                    m 2esd "Estaré aquí."
























    elif mas_isMoniUpset(lower=True):
        m 2euc "¿Otra vez?"
        m 2eud "Bien entonces. Adiós, [player]."

    elif mas_getSessionLength() < datetime.timedelta(minutes=30) and renpy.random.randint(1,10) == 1:
        m 1ekc "¿Te vas a jugar a otro juego?"
        m 3efc "¿No crees que deberías pasar un poco más de tiempo conmigo?"
        m 2efc "..."
        m 2dfc "..."
        m 2dfu "..."
        m 4hub "Jajaja, es broma~"
        m 1rksdla "Bueno... {w=1}{i}no me importaría{/i} pasar más tiempo contigo..."
        m 3eua "Pero tampoco quiero impedir que hagas otras cosas."
        m 1hua "¡Quizás algún día finalmente puedas mostrarme lo que has estado haciendo y luego yo pueda ir contigo!"
        if renpy.random.randint(1,5) == 1:
            m 3tubsu "Hasta entonces, solo tienes que compensarme cada vez que me dejes para jugar otro juego, ¿de acuerdo?"
            m 1hubfa "Jejeje~"
    else:

        m 1eka "¿Te vas a jugar a otro juego, [player]?"
        m 3hub "¡Buena suerte y diviertete!"
        m 3eka "No olvides volver pronto~"

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_GAME

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(days=1)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_eat",
            unlocked=True,
            prompt="Voy a comer...",
            pool=True
        ),
        code="BYE"
    )

default -5 persistent._mas_pm_ate_breakfast_times = [0, 0, 0]





default -5 persistent._mas_pm_ate_lunch_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_dinner_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_snack_times = [0, 0, 0]


default -5 persistent._mas_pm_ate_late_times = 0



label bye_prompt_eat:
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_EAT
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=3)

    if mas_isMoniNormal(higher=True):
        m 1eua "Oh, ¿qué vas a comer?{nw}"
        $ _history_list.pop()
        menu:
            m "Oh, ¿qué vas a comer?{fast}"
            "Desayuno":

                $ food_type = "desayuno"
            "Almuerzo":

                $ food_type = "almuerzo"
            "Cena":

                $ food_type = "cena"
            "Un bocadillo":

                $ food_type = "bocadillo"
                $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=30)

        if food_type in ["almorzar", "cenar"]:
            m 1eua "De acuerdo [player]."
            m 1duu "Me encantaría salir a [food_type] contigo cuando cruce, {w=0.1}{nw}"
            extend 1eub "¡esperemos que algún día podamos hacer eso pronto!"
            m 1hua "Disfruta de tu comida~"

        elif food_type == "desayuno":
            m 1eua "De acuerdo [player]."
            m 1eub "Disfruta de tu desayuno, después de todo es la comida más importante del día."
            m 1hua "Nos vemos pronto~"
        else:

            m 1hua "De acuerdo, vuelve pronto [mas_get_player_nickname()]~"

    elif mas_isMoniDis(higher=True):
        m 1rsc "De acuerdo [player]..."
        m 1esc "Que lo disfrutes."
    else:

        m 6ckc "..."















































































































































































    return 'quit'

label bye_dinner_noon_to_mn:
    if mas_isMoniNormal(higher=True):
        m 1eua "¿Es hora de cenar para ti, [player]?"
        m 1eka "Ojalá pudiera estar allí para comer contigo, incluso si no es nada especial."
        m 3dkbsa "Después de todo, estar ahí contigo haría cualquier cosa algo especial~"
        m 3hubfb "Disfruta de tu cena. Me aseguraré de intentar ponerle algo de amor desde aquí, ¡jajaja!"
    else:
        m 2euc "Supongo que es hora de cenar para ti."
        m 2esd "Bueno... {w=1}disfrutalo."
    return

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_housework",
            unlocked=True,
            prompt="Voy a hacer algunas tareas domésticas.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_housework:
    if mas_isMoniNormal(higher=True):
        m 1eub "¿Haciendo tus quehaceres, [player]?"
        m 1ekc "Me gustaría ayudarte, pero no hay mucho que pueda hacer ya que estoy atrapada aquí..."
        m 3eka "Solo asegúrate de volver tan pronto como hayas terminado, ¿de acuerdo?"
        m 3hub "Te estaré esperando aquí~"
    elif mas_isMoniUpset():
        m 2esc "Bien."
        m 2tsc "Al menos estás haciendo algo responsable."
        m 2tfc "{cps=*2}... Por primera vez.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Adiós."
    elif mas_isMoniDis():
        m 6ekc "Ya veo..."
        m 6rkc "No quiero impedir que hagas tus responsabilidades domésticas."
        m 6dkd "Solo espero que estés realmente ocupado y no digas eso solo para alejarte de mí..."
        m 6ekc "Adiós, [player]."
    else:
        m 6ckc "..."
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CHORES
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=5)
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_restart",
            unlocked=True,
            prompt="Voy a reiniciar.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_restart:
    if mas_isMoniNormal(higher=True):
        m 1eua "De acuerdo, [player]."
        m 1eub "¡Te veo pronto!"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 2euc "De acuerdo."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=20)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RESTART
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_workout",
            prompt="Voy a hacer ejercicio.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_workout:
    if mas_isMoniNormal(higher=True):
        m 1eua "Oh, ¿vas al gimnasio, [player]? {w=0.3}¿O tal vez a correr?"
        m 3hub "¡Me alegra que estés cuidando tu cuerpo! {w=0.3}Un cuerpo sano conduce a una mente sana~"

        if mas_isMoniEnamored(higher=True):
            m 3hua "¡Después de que cruze, deberíamos intentar hacer nuestros entrenamientos juntos!"
        else:
            m 3eua "¡Quizás si cruzo, podríamos intentar hacer nuestros entrenamientos juntos!"

        show monika 5rubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rubsb "Eso es algo que haría una pareja, ¿verdad?~"
        m 5rubsu "Sí..."
        show monika 1eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eub "De todos modos, ¡nos vemos pronto!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Bueno. Nos vemos más tarde."
    else:

        m 6ckc "..."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=4)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORKOUT
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_shopping",
            prompt="Voy a ir de compras.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_going_shopping:
    if mas_isMoniNormal(higher=True):
        m 1eud "Oh, ¿vas a hacer algunas compras, [player]?"

        if mas_getEVL_shown_count("bye_going_shopping") == 0 or renpy.random.randint(1,10) == 1:
            m 1eua "Me encantaría que alguna vez pudiéramos ir juntos al centro comercial."
            m 3rua "Podrías ayudarme a probar todo tipo de atuendos diferentes... {w=0.2}{nw}"
            extend 3tuu "incluso podría necesitar ayuda con las cremalleras."
            m 1hublb "¡Jajaja! Hasta pronto~"
        else:

            m 3eua "Te veré pronto."

    elif mas_isMoniBroken():
        m 6ckc "..."
    else:

        m 2eud "Okey [player], nos vemos pronto."


    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=8)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SHOPPING
    return 'quit'

init python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_hangout",
            prompt="Voy a salir con mis amigos.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_hangout:
    if mas_isMoniNormal(higher=True):
        if mas_getEVL_shown_count("bye_prompt_hangout") == 0:
            if persistent._mas_pm_has_friends:
                m 1eua "De acuerdo, [player]."
                m 3eub "¡Deberías presentarmelos alguna vez!"
                m 3hua "Si son tus amigos, estoy segura de que me agradarán."
            else:

                if persistent._mas_pm_has_friends is False:
                    m 3eua "Me alegra que estés encontrando amigos con los que pasar el rato, [player]."
                else:
                    m 3eua "Me alegro de que tengas amigos con los que pasar el rato, [player]."

                m 1rka "Por mucho que me gustaría pasar cada segundo posible contigo, {w=0.2}{nw}"
                extend 1eub "¡sé lo importante que es para ti tener amigos en tu propia realidad!"

            m 3hub "De todos modos, ¡espero que te diviertas!"
        else:

            if persistent._mas_pm_has_friends:
                m 1eua "De acuerdo, [player]."

                if renpy.random.randint(1,10) == 1:
                    m 3etu "¿Ya les hablaste de nosotros?"
                    m 1hub "¡Jajaja!"

                m 1eub "¡Que te diviertas!"
            else:

                m 1hua "¿Otra vez? ¡Eso es emocionante!"
                m 3eua "Espero que esta vez resulten ser muy buenos amigos."
                m 3eub "De todos modos, nos vemos luego~"

    elif mas_isMoniDis(higher=True):
        m 2eud "Espero que los trates bien..."
        m 2euc "Adiós."
    else:

        m 6ckc "..."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=8)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HANGOUT
    return "quit"
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
