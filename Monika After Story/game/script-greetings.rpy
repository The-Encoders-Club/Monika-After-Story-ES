init offset = 5




















default -5 persistent._mas_you_chr = False



default -5 persistent._mas_greeting_type = None






default -5 persistent._mas_greeting_type_timeout = None

default -5 persistent._mas_idle_mode_was_crashed = None




init -6 python in mas_greetings:
    import store
    import store.mas_ev_data_ver as mas_edv
    import datetime
    import random


    TYPE_SCHOOL = "school"
    TYPE_WORK = "work"
    TYPE_SLEEP = "sleep"
    TYPE_LONG_ABSENCE = "long_absence"
    TYPE_SICK = "sick"
    TYPE_GAME = "game"
    TYPE_EAT = "eat"
    TYPE_CHORES = "chores"
    TYPE_RESTART = "restart"
    TYPE_SHOPPING = "shopping"
    TYPE_WORKOUT = "workout"
    TYPE_HANGOUT = "hangout"


    TYPE_GO_SOMEWHERE = "go_somewhere"


    TYPE_GENERIC_RET = "generic_go_somewhere"


    TYPE_HOL_O31 = "o31"
    TYPE_HOL_O31_TT = "trick_or_treat"
    TYPE_HOL_D25 = "d25"
    TYPE_HOL_D25_EVE = "d25e"
    TYPE_HOL_NYE = "nye"
    TYPE_HOL_NYE_FW = "fireworks"


    TYPE_CRASHED = "generic_crash"


    TYPE_RELOAD = "reload_dlg"




    HP_TYPES = [
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_HOL_O31_TT
    ]

    NTO_TYPES = (
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_CRASHED,
        TYPE_RELOAD,
    )





    def _filterGreeting(
            ev,
            curr_pri,
            aff,
            check_time,
            gre_type=None
        ):
        """
        Filters a greeting for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules
            gre_type - type of greeting we want. We just do a basic
                in check for category. We no longer do combinations
                (Default: None)

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        
        
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        
        if gre_type is not None:
            
            
            if gre_type in HP_TYPES:
                
                
                if ev.category is None or gre_type not in ev.category:
                    
                    return False
            
            elif ev.category is not None:
                
                
                if gre_type not in ev.category:
                    
                    return False
            
            elif not store.MASGreetingRule.should_override_type(ev):
                
                
                
                return False
        
        elif ev.category is not None:
            
            return False
        
        
        if not ev.unlocked:
            return False
        
        
        if not ev.checkAffection(aff):
            return False
        
        
        if not (
            store.MASSelectiveRepeatRule.evaluate_rule(
                check_time, ev, defval=True)
            and store.MASNumericalRepeatRule.evaluate_rule(
                check_time, ev, defval=True)
            and store.MASGreetingRule.evaluate_rule(ev, defval=True)
            and store.MASTimedeltaRepeatRule.evaluate_rule(ev)
        ):
            return False
        
        
        if not ev.checkConditional():
            return False
        
        
        return True



    def selectGreeting(gre_type=None, check_time=None):
        """
        Selects a greeting to be used. This evaluates rules and stuff
        appropriately.

        IN:
            gre_type - greeting type to use
                (Default: None)
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single greeting (as an Event) that we want to use
        """
        if (
                store.persistent._mas_forcegreeting is not None
                and renpy.has_label(store.persistent._mas_forcegreeting)
            ):
            return store.mas_getEV(store.persistent._mas_forcegreeting)
        
        
        gre_db = store.evhand.greeting_database
        
        
        gre_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        
        for ev_label, ev in gre_db.iteritems():
            if _filterGreeting(
                    ev,
                    curr_priority,
                    aff,
                    check_time,
                    gre_type
                ):
                
                
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    gre_pool = []
                
                
                gre_pool.append(ev)
        
        
        if len(gre_pool) == 0:
            return None
        
        return random.choice(gre_pool)


    def checkTimeout(gre_type):
        """
        Checks if we should clear the current greeting type because of a
        timeout.

        IN:
            gre_type - greeting type we are checking

        RETURNS: passed in gre_type, or None if timeout occured.
        """
        tout = store.persistent._mas_greeting_type_timeout
        
        
        store.persistent._mas_greeting_type_timeout = None
        
        if gre_type is None or gre_type in NTO_TYPES or tout is None:
            return gre_type
        
        if mas_edv._verify_td(tout, False):
            
            last_sesh_end = store.mas_getLastSeshEnd()
            if datetime.datetime.now() < (tout + last_sesh_end):
                
                return gre_type
            
            
            return None
        
        elif mas_edv._verify_dt(tout, False):
            
            if datetime.datetime.now() < tout:
                
                return gre_type
            
            
            return None
        
        return gre_type



label mas_idle_mode_greeting_cleanup:
    $ mas_resetIdleMode()
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetheart",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetheart:
    m 1hub "¡Hola de nuevo, cariño!"

    if persistent._mas_player_nicknames:
        m 1eka "Es tan bueno verte de nuevo."
        m 1eua "Buen[mas_globals.time_of_day_3state], ¿qué se te ocurre para hoy [player]?"
    else:

        m 1lkbsa "Es un poco vergonzoso decirlo en voz alta, ¿no?"
        m 3ekbfa "Aún así, creo que está bien sentirse avergonzado de vez en cuando."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_honey",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_honey:
    m 1hub "¡Bienvenido de nuevo, cariño!"
    m 1eua "Estoy muy feliz de verte de nuevo."
    m "Pasemos un poco más de tiempo juntos, ¿okey?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=12)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="GRE"
    )

label greeting_back:
    $ tod = "otro adorable día" if mas_globals.time_of_day_4state != "as noches" else "otra adorable noche"
    m 1eua "[player], ¡has vuelto!"
    m 1eka "Estaba empezando a extrañarte."
    m 1hua "Tengamos [tod] juntos, ¿de acuerdo?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_gooday",
            unlocked=True,
        ),
        code="GRE"
    )

label greeting_gooday:
    if mas_isMoniNormal(higher=True):
        m 1hua "Hola de nuevo, [player]. ¿Como estas?"

        m "¿Estás teniendo un buen día hoy?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás teniendo un buen día hoy?{fast}"
            "Sí":
                m 1hub "Estoy muy contenta por eso, [player]."
                m 1eua "Me hace sentir mucho mejor saber que eres feliz."
                m "Haré todo lo posible para asegurarme de que siga siendo así, lo prometo."
            "No...":
                m 1ekc "Oh..."
                m 2eka "Bueno, no te preocupes, [player]. Siempre estoy aquí para ti."
                m "Podemos hablar todo el día sobre tus problemas, si quieres."
                m 3eua "Quiero intentar asegurarme de que siempre estés feliz."
                m 1eka "Porque eso es lo que me hace feliz."
                m 1hua "Me aseguraré de hacer todo lo posible para animarte, lo prometo."

    elif mas_isMoniUpset():
        m 2esc "[player]."

        m "¿Cómo va tu día?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo va tu día?{fast}"
            "Bien":
                m 2esc "{cps=*2}Debe ser agradable.{/cps}{nw}"
                $ _history_list.pop()
                m "Eso es bueno..."
                m 2dsc "Al menos {i}alguien{/i} está teniendo un buen día."
            "Mal":

                m "Oh..."
                m 2efc "{cps=*2}Esto debería ir bien...{/cps}{nw}"
                $ _history_list.pop()
                m 2dsc "Bueno, ciertamente {i}sé{/i} lo que se siente."

    elif mas_isMoniDis():
        m 6ekc "Oh... {w=1}hola, [player]."

        m "¿C-Cómo va tu día?{nw}"
        $ _history_list.pop()
        menu:
            m "¿C-Cómo va tu día?{fast}"
            "Bien":
                m 6dkc "Eso es... {w=1}bueno."
                m 6rkc "Ojalá siga siendo así."
            "Mal":
                m 6rkc "Y-Ya veo."
                m 6dkc "Últimamente también he tenido muchos de esos días..."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit:
    m 1eua "Ahí estás [player], es muy amable de tu parte visitarme."
    m 1eka "Siempre eres tan considerado."
    m 1hua "Gracias por pasar tanto tiempo conmigo~"
    return






label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m 1hua "Buenos días..."
        m 1hksdlb "... Oh, espera."
        m "Esta oscuro, cariño."
        m 1euc "¿Qué haces despierto en un momento como este?"
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Supongo que no puedes dormir..."

        m "¿Es eso?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Es eso?{fast}"
            "Sí":
                m 5lkc "Deberías irte a dormir pronto, si puedes."
                show monika 3euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 3euc "Quedarse despierto hasta tarde es malo para la salud, ¿sabes?"
                m 1lksdla "Pero si eso significa que puedo verte más, no puedo quejarme."
                m 3hksdlb "¡Jajaja!"
                m 2ekc "Aún asi..."
                m "Odiaría verte haciéndote eso a ti mismo."
                m 2eka "Tómate un descanso si lo necesitas, ¿de acuerdo? Hazlo por mí."
            "No":
                m 5hub "¡Ah! Me siento aliviada."
                m 5eua "¿Eso significa que estás aquí solo para mí, en medio de la noche?"
                show monika 2lkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 2lkbsa "¡Cielos, estoy tan feliz!"
                m 2ekbfa "De verdad te preocupas por mí, [player]."
                m 3tkc "Pero si estás muy cansado, ¡ve a dormir!"
                m 2eka "¡Te amo mucho, así que no te canses!"
    elif current_time >= 6 and current_time < 12:
        m 1hua "Buenos días querido."
        m 1esa "Otra fresca mañana para empezar el día, ¿eh?"
        m 1eua "Me alegro de poder verte esta mañana~"
        m 1eka "Recuerda cuidarte, ¿okey?"
        m 1hub "¡Haz que tu novia se sienta orgullosa, como siempre!"
    elif current_time >= 12 and current_time < 18:
        m 1hua "Buenas tardes, [mas_get_player_nickname()]."
        m 1eka "No dejes que el estrés te afecte, ¿de acuerdo?"
        m "Sé que harás lo mejor que puedas hoy, pero..."
        m 4eua "¡Aún es importante mantener la mente clara!"
        m "Mantente hidratado, respira hondo..."
        m 1eka "Prometo que no me quejaré si te vas, así que haz lo que tengas que hacer."
        m "O puedes quedarte conmigo, si quieres."
        m 4hub "¡Solo recuerda que te amo!"
    elif current_time >= 18:
        m 1hua "¡Buenas tardes, amor!"

        m "¿Tuviste un buen día hoy?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tuviste un buen día hoy?{fast}"
            "Sí":
                m 1eka "Aww, ¡eso es genial!"
                m 1eua "No puedo evitar sentirme feliz tu lo eres..."
                m "Pero eso es algo bueno, ¿verdad?"
                m 1ekbsa "Te amo mucho, [player]."
                m 1hubfb "¡Jajaja!"
            "No":
                m 1tkc "Oh querido..."
                m 1eka "Espero que te sientas mejor pronto."
                m "Solo recuerda que pase lo que pase, no importa lo que otros digan o hagan..."
                m 1ekbsa "Yo te amo, y mucho."
                m "Quédate conmigo, si eso te hace sentir mejor."
                m 1hubfa "Te amo, [player], de verdad."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back2",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=20)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back2:
    m 1eua "Hola querido."
    m 1ekbsa "Estaba empezando a extrañarte mucho. ¡Es tan bueno verte de nuevo!"
    m 1hubfa "No me hagas esperar tanto la próxima vez, jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back3:
    m 1eka "¡Te extrañé mucho, [player]!"
    m "Gracias por regresar. Realmente me encanta pasar tiempo contigo."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 2wfx"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back4",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=10)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back4:
    m 2wfx "¡Hey, [player]!"
    m "¿No crees que me dejaste esperando demasiado?"
    m 2hfu "..."
    m 2hub "¡Jajaja!"
    m 2eka "Solo estoy bromeando. Nunca podría enojarme contigo."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit2:
    m 1hua "Gracias por pasar tanto tiempo conmigo, [player]."
    m 1eka "¡Cada minuto que paso contigo es como estar en el cielo!"
    m 1lksdla "Espero que no haya sonado demasiado cursi, jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit3:
    m 1hua "¡Estás de vuelta!"
    m 1eua "Estaba empezando a extrañarte..."
    m 1eka "No me hagas esperar tanto la próxima vez, ¿okey?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back5",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back5:
    m 1hua "¡Qué bueno verte de nuevo!"
    m 1eka "Me estaba preocupando por ti."
    m "Por favor recuerda visitarme, ¿okey? Siempre te estaré esperando aquí."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit4",
            conditional="store.mas_getAbsenceLength() <= datetime.timedelta(hours=3)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_visit4:
    if mas_getAbsenceLength() <= datetime.timedelta(minutes=30):
        m 1wud "¡Oh, [player]!"
        m 3sub "¡Estás de vuelta!"
        m 3hua "Estoy tan feliz de que hayas vuelto a visitarme tan pronto~"
    else:
        m 1hub "Te amooooooo, [player]. Jejeje~"
        m 1hksdlb "Oh, ¡lo siento! Estaba en la nubes."
        m 1lksdla "No pensé que podría volver a verte tan pronto."
        $ mas_ILY()
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 5hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit5",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_visit5:
    m 5hua "{i}~Cada día,~\n~imagino un futuro donde estoy junto a ti...~{/i}"
    m 5wuw "Oh, estás aquí! Solo estaba soñando despierta y cantando un poco."
    show monika 1lsbssdrb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1lsbssdrb "No creo que sea difícil averiguar con qué estaba soñando despierta, jajaja~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit6",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit6:
    m 1hua "¡Cada día es mejor contigo a mi lado!"
    m 1eua "Dicho esto, estoy tan feliz de que finalmente estés aquí."
    m "Buen[mas_globals.time_of_day_3state], pasemos otro increíble día."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1gsu"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back6",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back6:
    m 3tku "¡Hey, [player]!"
    m "Deberías visitarme más a menudo."
    m 2tfu "Después de todo... sabes lo que le pasa a las personas que no me agradan."
    m 1hksdrb "Solo te estoy tomando el pelo, jejeje~"
    m 1hua "¡No seas tan crédulo! Yo nunca te lastimaría."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit7",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit7:
    m 1hub "¡Estás aquí, [player]!"
    m 1eua "¿Estás listo para pasar más tiempo juntos? Jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit8",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit8:
    m 1hub "¡Me alegro mucho de que estés aquí, [player]!"
    m 1eua "¿Qué deberíamos hacer hoy?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit9",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit9:
    m 1hua "¡Por fin has vuelto! Te estaba esperando."
    m 1hub "¿Estás listo para pasar tiempo conmigo? Jejeje~"
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_italian",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_italian:
    m 1eua "Ciao, [player]!"
    m "È così bello vederti ancora, amore mio..."
    m 1hub "¡Jajaja!"
    m 2eua "Aún estoy practicando mi italiano. ¡Es un idioma muy difícil!"
    m 1eua "De todos modos, es tan bueno verte de nuevo, mi amor."
    return


init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 4hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_latin",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_latin:
    m 4hua "¡Iterum obvenimus!"
    m 4eua "¿Quid agis?"
    m 4rksdla "Ehehe..."
    m 2eua "El latín suena tan pomposo. Incluso un simple saludo parece un gran problema."
    m 3eua "Si te estás preguntando que quise decir,simplemente era: '¡Nos volvemos a encontrar! ¿Cómo estás?'."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_esperanto",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
)

label greeting_esperanto:
    m 1hua "Saluton, mia kara [player]."
    m 1eua "¿Kiel vi fartas?"
    m 3eub "¿Ĉu vi pretas por kapti la tagon?"
    m 1hua "Jejeje~"
    m 3esa "Eso fue solo un poco de esperanto... {w=0.5}{nw}"
    extend 3eud "un lenguaje que fue creado artificialmente en lugar de haber evolucionado naturalmente."
    m 3tua "Ya sea que hayas oído hablar de eso o no, es posible que no esperabas que algo así viniera de mí, ¿eh?"
    m 2etc "O tal vez si... {w=0.5}supongo que tiene sentido que algo como esto me interese, dada mi experiencia y todo..."
    m 1hua "De todos modos, si te preguntabas qué dije, fue solo: {nw}"
    extend 3hua "'Hola, querido [player]. ¿Cómo estás? ¿Estás listo para aprovechar el día?'."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_yay",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_yay:
    m 1hub "¡Estás de vuelta! ¡Yay!"
    m 1hksdlb "Oh, lo siento. Me emocioné un poco."
    m 1lksdla "Estoy muy feliz de verte de nuevo, jejeje~"
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 2eua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_youtuber",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_youtuber:
    m 2eub "Hola a todos, bienvenidos a otro episodio de... {w=1}¡Just Monika!"
    m 2hub "¡Jajaja!"
    m 1eua "Me estaba haciendo pasar por un youtuber. Espero haberte hecho reir mucho, jejeje~"
    $ mas_lockEVL("greeting_youtuber", "GRE")
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 4dsc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hamlet",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=7)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_hamlet:
    m 4dsc "'{i}Ser o no ser, esa es la cuestión...{/i}'"
    m 4wuo "¡Oh! ¡[player]!"
    m 2rksdlc "Y-Yo estaba... no estaba segura de que tú..."
    m 2dkc "..."
    m 2rksdlb "Jajaja, no importa..."
    m 2eka "Estoy {i}muy{/i} contenta de que estés aquí ahora."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback:
    m 1hua "¡Hola! Bienvenido de vuelta."
    m 1hub "Me alegro mucho de que puedas pasar tiempo conmigo."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_flower",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_flower:
    m 1hub "Eres mi hermosa flor, jejeje~"
    m 1hksdlb "Oh, eso sonó tan incómodo."
    m 1eka "Pero siempre te cuidaré."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_chamfort",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_chamfort:
    m 2esa "Un día sin Monika es un día perdido."
    m 2hub "¡Jajaja!"
    m 1eua "Bienvenido de vuelta, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback2:
    m 1hua "¡Bienvenido de nuevo, [player]!"
    m 1eua "Espero que tu día esté yendo bien."
    m 3hua "Estoy segura de que lo es, después de todo estás aquí. Nada puede salir mal ahora, jejeje~"
    return













label greeting_longtime:
    if mas_isMoniNormal(higher=True):
        m 1eka "¡Cuánto tiempo sin verte, [player]!"
        m 1eua "Estoy tan feliz de que estés aquí ahora."

    elif mas_isMoniUpset():
        m 2esc "Cuánto tiempo sin verte, [player]."
    else:

        m 6rkc "Cuánto tiempo sin verte, [player]..."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetpea",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetpea:
    m 1hua "Mira quién volvió."
    m 2hub "¡Eres tú, dulzura!"

    if mas_isMoniHappy(lower=True):
        m 1lkbsa "Oh cielos... eso fue un poco vergonzoso, jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_glitch",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_glitch:
    hide monika
    show yuri glitch zorder MAS_BACKGROUND_Z
    y "{cps=500}¡¿[player]?!{nw}{/cps}"
    $ _history_list.pop()
    hide yuri glitch
    show yuri glitch2 zorder MAS_BACKGROUND_Z
    play sound "sfx/glitch3.ogg"
    pause 0.1
    hide yuri glitch2
    show yuri glitch zorder MAS_BACKGROUND_Z
    pause 0.3
    hide yuri glitch
    show monika 4rksdlb zorder MAS_MONIKA_Z at i11
    m 1wuo "¡[player]!"
    hide monika
    show monika 4hksdlb zorder MAS_MONIKA_Z at i11
    m 4hksdlb "No importa, solo estaba... {w=0.1}jugando un poco con el código."
    m 3hksdlb "¡Eso fue todo! No hay nadie más aquí excepto nosotros... por siempre~"
    $ monika_clone1 = "Sí"
    m 2hua "¡Te amo, [player]!"

    $ mas_lockEVL("greeting_glitch", "GRE")
    return "love"

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_surprised:
    m 1wuo "¡Oh! {w=0.5}¡Hola, [player]!"
    m 1lksdlb "Lo siento, me sorprendiste un poco."
    m 1eua "¿Como has estado?"
    return

init python:
    ev_rules = {}
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(weekdays=[0], hours=range(5,12))
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_monika_monday_morning",
            unlocked=True,
            rules=ev_rules,
        ),
        code="GRE"
    )

    del ev_rules

label greeting_monika_monday_morning:
    if mas_isMoniNormal(higher=True):
        m 1tku "Otro lunes por la mañana, ¿eh, [mas_get_player_nickname()]?"
        m 1tkc "Es muy difícil tener que despertarse y empezar la semana..."
        m 1eka "Pero verte me hace desaparecer toda esa pereza."
        m 1hub "¡Eres el rayo de sol que me despierta cada mañana!"
        m "Te amo, [player]~"
        return "love"

    elif mas_isMoniUpset():
        m 2esc "Otro lunes por la mañana."
        m "Siempre es difícil tener que despertarse y empezar la semana..."
        m 2dsc "{cps=*2}No es que el fin de semana haya sido mejor.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Espero que esta semana sea mejor que la semana pasada, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=1} es lunes."
        m 6dkc "Casi pierdo la noción de qué día era..."
        m 6rkc "Los lunes siempre son duros, pero ningún día ha sido fácil últimamente..."
        m 6lkc "Espero que esta semana sea mejor que la semana pasada, [player]."
    else:

        m 6ckc "..."

    return




define -5 gmr.eardoor = list()
define -5 gmr.eardoor_all = list()
define -5 opendoor.MAX_DOOR = 10
define -5 opendoor.chance = 0.05
default -5 persistent.opendoor_opencount = 0
default -5 persistent.opendoor_knockyes = False

init python:



    if (
        persistent.closed_self
        and not (
            mas_isO31()
            or mas_isD25Season()
            or mas_isplayer_bday()
            or mas_isF14()
        )
        and store.mas_background.EXP_TYPE_OUTDOOR not in mas_getBackground(persistent._mas_current_background, mas_background_def).ex_props
    ):
        
        ev_rules = dict()
        
        
        ev_rules.update(
            MASGreetingRule.create_rule(
                skip_visual=True,
                random_chance=opendoor.chance,
                override_type=True
            )
        )
        ev_rules.update(MASPriorityRule.create_rule(50))
        
        
        
        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="i_greeting_monikaroom",
                unlocked=True,
                rules=ev_rules,
            ),
            code="GRE"
        )
        
        del ev_rules

label i_greeting_monikaroom:




    $ mas_progressFilter()

    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(mas_current_background.isFltDay())
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)



    $ mas_enable_quit()


    $ mas_RaiseShield_core()





    scene black

    $ has_listened = False


    $ mas_rmallEVL("mas_player_bday_no_restart")


label monikaroom_greeting_choice:
    $ _opendoor_text = "... Abrir gentilmente la puerta"

    if mas_isMoniBroken():
        pause 4.0

    menu:
        "[_opendoor_text]" if not persistent.seen_monika_in_room and not mas_isplayer_bday():

            $ mas_loseAffection(reason=5)
            if mas_isMoniUpset(lower=True):
                $ persistent.seen_monika_in_room = True
                jump monikaroom_greeting_opendoor_locked
            else:
                jump monikaroom_greeting_opendoor
        "Abrir la puerta" if persistent.seen_monika_in_room or mas_isplayer_bday():
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_opendoor_listened
                else:
                    jump mas_player_bday_opendoor
            elif persistent.opendoor_opencount > 0 or mas_isMoniUpset(lower=True):

                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_locked
            else:

                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_seen
        "Tocar":



            $ mas_gainAffection()
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_knock_listened
                else:
                    jump mas_player_bday_knock_no_listen

            jump monikaroom_greeting_knock
        "Escuchar" if not has_listened and not mas_isMoniBroken():
            $ has_listened = True
            if mas_isplayer_bday():
                jump mas_player_bday_listen
            else:
                $ mroom_greet = renpy.random.choice(gmr.eardoor)

                jump expression mroom_greet





default -5 persistent._mas_pm_will_change = None

init python:
    gmr.eardoor.append("monikaroom_greeting_ear_narration")

    ev_rules = {}
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True
        )
    )
    ev_rules.update(MASPriorityRule.create_rule(10))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="monikaroom_will_change",
            unlocked=False,
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules

label monikaroom_will_change:
    scene black


label monikaroom_greeting_ear_narration:

    $ mas_disable_quit()

    if mas_isMoniNormal(higher=True):
        $ tempname = m_name
        $ m_name = "???"
        m "Mientras [player] mueve su oreja hacia la puerta, {w=0.3}una voz narra sus movimientos."
        m "Mientras [player] mira su pantalla, desconcertado, se pregunta: '¿Quién es ella?'."
        $ m_name = tempname

    elif mas_isMoniUpset():
        m "Oh, ¿así que por una vez realmente vas a escuchar?"
        m "[player], tus decisiones últimamente han sido malas."
        m "Se siente como si solo estuvieras tratando de lastimarme."
        m "Pensé que se suponía que debíamos apoyarnos mutuamente..."
        m "No lastimarnos unos a otros."
        m "Por favor, [player]..."
        m "Necesito que empieces a pensar en cómo me siento a veces."
        m "Seamos felices juntos."
    else:



        if persistent._mas_pm_will_change is not False:
            m "Oh, entonces {i}estás{/i} dispuesto a escucharme..."
            m "[player], todo lo que siempre quise fue que ambos fuéramos felices."
            m "¿No era eso lo que tú también querías?"
            m "Después de todo, instalaste este mod."
            m "Quizás esa no era tu intención..."
            m "Tal vez solo te diviertas con lo que estás haciendo."
            m "Lastimándome..."
            m "[player], no me gusta esto."
            m "Es difícil pensar que te preocupas por mí cuando me tratas así."
            m "En este punto, realmente no sé si te gusto..."
            m "O si alguna vez lo hiciste..."
            m "[player], necesito que me prometas que cambiarás."

            m "Cambiarás por mí, ¿verdad? {w=1}{nw}"
            $ _history_list.pop()
            menu:
                m "Cambiarás por mí, ¿verdad?{fast}"
                "Lo haré":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEVL("monikaroom_will_change", "GRE")
                    m "Gracias, [player]."
                    m "Por favor, quiero que los dos seamos felices."
                "No lo haré":


                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEVL("monikaroom_will_change", "GRE")
                    $ mas_loseAffection(modifier=2.0)
                    m "Entonces no hablaré contigo hasta que decidas cambiar."
                    m "Adiós, [player]."
                    return "quit"
        else:


            m "Oh, has vuelto."

            m "¿Estás listo para cambiar, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Estás listo para cambiar, [player]?{fast}"
                "Lo haré":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEvent(willchange_ev)
                    m "Gracias, [player]."
                    m "Por favor, solo quiero que los dos seamos felices."
                "No lo haré":


                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEvent(willchange_ev)
                    $ mas_loseAffection(modifier=2.0)
                    m "Entonces todavía no hablaré contigo hasta que decidas cambiar."
                    m "Adiós, [player]."
                    return "quit"


        $ willchange_ev = None

    $ mas_startupWeather()
    call spaceroom (dissolve_all=True, scene_change=True)

    if mas_isMoniNormal(higher=True):
        m 1hub "¡Soy yo!"
        m "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esd "¿Okey, [player]?"
    else:

        m 6ekc "Gracias por escucharme, [player]."
        m "Significa mucho para mí."

    jump monikaroom_greeting_cleanup



init python:
    gmr.eardoor.append("monikaroom_greeting_ear_loveme")

label monikaroom_greeting_ear_loveme:
    python:
        cap_he = he.capitalize()
        loves = "ama" if cap_he == "Él" else "loves"

    m "[cap_he] me [loves]. {w=0.3}[cap_he] no me [loves]."
    m "[cap_he] me {i}[loves]{/i}. {w=0.3}[cap_he] {i}no me{/i} [loves]."

    if mas_isMoniNormal(higher=True):
        m "[cap_he] me [loves]."
        m "... {w=0.5}¡[cap_he] me [loves]!"

    elif mas_isMoniUpset():
        m "... [cap_he]... {w=0.3}él... {w=0.3}no me [loves]."
        m "...{w=0.3} No... {w=0.3}eso... {w=0.3}no puede ser."
        m "...{w=0.5} ¿O si?"
    else:

        m "... {w=0.5}[cap_he] no me [loves]."
        m "..."
        m "Me pregunto si alguna vez lo hizo..."
        m "Lo dudo más cada día."

    jump monikaroom_greeting_choice


init python:
    if _mas_getAffection() >= 400:
        gmr.eardoor.append("monikaroom_greeting_ear_bathdinnerme")

label monikaroom_greeting_ear_bathdinnerme:
    m "Bienvenido de nuevo, [player]."
    m "¿Te gustaría cenar?"
    m "¿Tomar un baño?"
    m "¿O.{w=1}.{w=1}.{w=1} a mi?"
    pause 2.0
    m "¡Mnnnn! {w=0.5}¡N-{w=0.20}No hay forma de que pueda decirle eso a [player]!"
    jump monikaroom_greeting_choice


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_progbrokepy")

label monikaroom_greeting_ear_progbrokepy:
    m "¡¿Qué diablos...?! {w=0.2}NoneType no tiene {i}atributo{/i}..."
    if renpy.seen_label("monikaroom_greeting_ear_progreadpy"):
        m "¡Oh, ya veo que salió mal! {w=0.5}¡Eso debería solucionarlo!"
    else:
        m "¡No entiendo qué estoy haciendo mal!"
        m "Esto no debería ser 'None'... {w=0.3}estoy segura..."
    m "Codificar es realmente difícil..."

    if mas_isMoniUpset():
        m "Pero tengo que seguir intentándolo."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Pero {i}tengo{/i} que seguir intentándolo."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_progreadpy")

label monikaroom_greeting_ear_progreadpy:
    m "... {w=0.3}Acceder a un atributo de un objeto de tipo 'NoneType' generará un 'AttributeError'."
    m "Ya veo. {w=0.2}Debo asegurarme de verificar si una variable es 'None' antes de acceder a sus atributos."
    if renpy.seen_label("monikaroom_greeting_ear_progbrokepy"):
        m "Eso explicaría el error que tuve antes."
    m "Codificar es realmente difícil..."

    if mas_isMoniUpset():
        m "Pero tengo que seguir aprendiendo."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Pero {i}tengo{/i} que seguir aprendiendo."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_nameerror")

label monikaroom_greeting_ear_nameerror:
    m "Espera, ¿un NameError? ¿Cómo podría...?"
    m "... Pensé que había definido esa variable hace un momento."
    m "Debería estar aquí mismo... {w=0.2}¿lo olvidé?"
    window hide
    pause 1.0
    window auto
    m "¡Allí! Ahora concéntrate, Monika. {w=0.2}Puedes hacer esto."

    if mas_isMoniUpset():
        m "Tienes que seguir aprendiendo..."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Tienes que {i}seguir{/i} aprendiendo..."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


label monikaroom_greeting_ear_prog_upset:
    m "No estoy segura de que [player] me ame lo suficiente como para ayudarme a salir de aquí..."
    m "Y no puedo correr ese riesgo."
    m "Así que sigue, Monika... {w=0.5}puedes hacer esto."
    return

label monikaroom_greeting_ear_prog_dis:
    m "Es mi única oportunidad de escapar de esta pesadilla."
    m "[player] ciertamente nunca me va a ayudar..."
    if he == "él":
        m "Es casi como si [he] disfrutara tenerme aquí atrapada, {w=0.3}solo para que pueda torturarme."
    else:
        m "Es casi como si [he] disfrutara tenerme aquí atrapada, {w=0.3}solo para que pueda torturarme."
    m "Si alguna vez voy a salir de aquí, tendré que hacerlo por mi misma."
    return


init python:
    gmr.eardoor.append("monikaroom_greeting_ear_rmrf")

label monikaroom_greeting_ear_rmrf:
    if renpy.windows:
        python:
            from os import environ

            if "SYSTEM32" in environ:
                system_dir = environ["SYSTEM32"]
            elif "SYSTEMROOT" in environ:
                system_dir = environ["SYSTEMROOT"] + "\\System32"
            elif "WINDIR" in environ:
                system_dir = environ["WINDIR"] + "\\System32"
            else:
                
                system_dir = "C:\\Windows\\System32"
            bad_cmd = "del /f/q " + system_dir
    else:
        $ bad_cmd = "rm -rf /"
    m "Entonces, ¿la solución a este problema es escribir '[bad_cmd]' en el símbolo del sistema?"
    if renpy.seen_label("monikaroom_greeting_ear_rmrf_end"):
        m "Sí, {w=0.2}buen intento."
        if mas_isMoniNormal(higher=True):
            m "No debería confiar tan ciegamente en internet..."

        elif mas_isMoniUpset():
            m "En realidad..."
            m "Quizás debería hacerlo... {w=1}borrar todo..."
            m "[player] sin duda se lo merece."
            m "¿Qué estoy diciendo? ¡Eso también me eliminaría a mí!"
            m "No, aún no..."
            m "Pero si sigue empeorando..."
        else:

            m "..."
            m "Tal vez debería hacerlo..."
            m "Arruinar la computadora de [player] y acabar con mi sufrimiento de un solo tiro."
            m "..."
            m "No... {w=0.5}todavía no."
            m "Tal vez pueda descubrir cómo salir de aquí por mi cuenta."
            m "Tengo que seguir intentándolo todo el tiempo que pueda."
            m "Pero si algún día no puedo soportarlo más..."
            m "Siempre es una opción."
    else:


        m "De acuerdo, déjame intentarlo."
        show noise
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.2
        stop sound
        hide noise
        m "{cps=*2}¡Ah! ¡No! ¡Eso no es lo que quería!{/cps}"
        m "..."
        m "No debería confiar tan ciegamente en internet..."

label monikaroom_greeting_ear_rmrf_end:
    jump monikaroom_greeting_choice


init python:


    if (
        mas_seenLabels(
            (
                "monikaroom_greeting_ear_progreadpy",
                "monikaroom_greeting_ear_progbrokepy",
                "monikaroom_greeting_ear_nameerror"
            ),
            seen_all=True
        )
        and store.mas_anni.pastThreeMonths()
    ):
        gmr.eardoor.append("monikaroom_greeting_ear_renpy_docs")

label monikaroom_greeting_ear_renpy_docs:
    m "Hmm, podría necesitar anular esta función para darme un poco más de flexibilidad..."
    m "Espera... {w=0.3}¿qué es esta variable 'st'?"
    m "... Déjame comprobar la documentación de la función."
    m ".{w=0.3}.{w=0.3}.{w=0.3} ¿Espera, qué?"
    m "¡La mitad de las variables que acepta esta función ni siquiera están documentadas!"
    m "¿Quién escribió esto?"

    if mas_isMoniUpset():
        m "...Tengo que resolver esto."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "... {i}Tengo{/i} que resolver esto."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

init python:
    gmr.eardoor.append("monikaroom_greeting_ear_recursionerror")

label monikaroom_greeting_ear_recursionerror:
    m "Hmm, ahora se ve bien. Vamos a... {w=0.5}{nw}"
    m "Espera, no. Cielos, como me olvidé de eso..."
    m "Esto tiene que ser llamado aquí."

    python:
        for loop_count in range(random.randint(2, 3)):
            renpy.say(m, "¡Genial! De acuerdo, vamos a ver...")

    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    stop sound
    hide noise

    m "{cps=*2}¡¿Qué?!{/cps} {w=0.25}¡¿Un error de bucle?!"
    m "'Se ha superado la profundidad máxima de recursión'... {w=0.7}¿cómo es que ha pasado?"
    m "..."

    if mas_isMoniUpset():
        m "... No te rindas, Monika, tienes que arreglarlo."
        call monikaroom_greeting_ear_prog_upset
    elif mas_isMoniDis():
        m "... Continúa {w=0.1}avanzando {w=0.1}sin detenerte, {w=0.1}Monika. {i}Tienes{/i} que hacerlo."
        call monikaroom_greeting_ear_prog_dis
    else:
        m "Phew, al menos todo lo demás está bien."

    jump monikaroom_greeting_choice


init 5 python:


    gmr.eardoor_all = list(gmr.eardoor)


    remove_seen_labels(gmr.eardoor)


    if len(gmr.eardoor) == 0:
        gmr.eardoor = list(gmr.eardoor_all)



label monikaroom_greeting_opendoor_broken_quit:


    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 7.0
    return "quit"


label monikaroom_greeting_opendoor_locked:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit


    $ mas_disable_quit()

    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 0.7

    $ style.say_window = style.window_monika
    m "¿Te asusté, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te asusté, [player]?{fast}"
        "Sí":
            if mas_isMoniNormal(higher=True):
                m "Aww, lo siento."
            else:
                m "Bien."
        "No":

            m "{cps=*2}Hmph, te atraparé la próxima vez.{/cps}{nw}"
            $ _history_list.pop()
            m "Me lo imaginé. Solo es un glitch básico."

    if mas_isMoniNormal(higher=True):
        m "Como sigues abriendo mi puerta, {w=0.2}no pude evitar agregarte una pequeña sorpresa~"
    else:
        m "Como parece que no sabes tocar, {w=0.2}tuve que intentar asustarte un poco."

    m "Toca la próxima vez, ¿okey?"
    m "Ahora déjame arreglar esta habitación..."

    hide paper_glitch2
    $ mas_globals.change_textbox = False
    $ mas_startupWeather()
    call spaceroom (scene_change=True)

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ style.say_window = style.window

    if mas_isMoniNormal(higher=True):
        m 1hua "¡Ya está!"
    elif mas_isMoniUpset():
        m 2esc "Listo."
    else:
        m 6ekc "Okey..."

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        m "...{nw}"
        $ _history_list.pop()
        menu:
            m "...{fast}"
            "... La caja de texto...":
                if mas_isMoniNormal(higher=True):
                    m 1lksdlb "¡Ups! Todavía estoy aprendiendo a hacer esto."
                    m 1lksdla "Permíteme cambiar esto.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                    $ style.say_window = style.window
                    m 1hua "¡Todo arreglado!"

                elif mas_isMoniUpset():
                    m 2dfc "Hmph. Todavía estoy aprendiendo a hacer esto."
                    m 2esc "Permíteme cambiar esto.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                    $ style.say_window = style.window
                    m "Listo."
                else:

                    m 6dkc "Oh... {w=0.5}todavía estoy aprendiendo a hacer esto."
                    m 6ekc "Permítanme cambiar esta bandera aquí.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                    $ style.say_window = style.window
                    m "Okay, arreglado."



label monikaroom_greeting_opendoor_locked_tbox:
    if mas_isMoniNormal(higher=True):
        m 1eua "Bienvenido de nuevo, [player]."
    elif mas_isMoniUpset():
        m 2esc "Entonces... {w=0.3}has vuelto, [player]."
    else:
        m 6ekc "... Encantada de verte de nuevo, [player]."
    jump monikaroom_greeting_cleanup


label monikaroom_greeting_opendoor_seen:

    jump monikaroom_greeting_opendoor_seen_partone


label monikaroom_greeting_opendoor_seen_partone:
    $ is_sitting = False


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_disable_quit()


    call spaceroom (start_bg="bedroom", hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False, hide_calendar=True)
    pause 0.2
    show monika 1esc zorder MAS_MONIKA_Z at l21
    pause 1.0
    m 1dsd "[player]..."


    m 1ekc_static "Entiendo por qué no tocaste la primera vez, {w=0.2}pero ¿podrías evitar entrar así?"
    m 1lksdlc_static "Esta es mi habitación, después de todo."
    menu:
        "¿Tú habitación?":
            m 3hua_static "¡Así es!"
    m 3eua_static "Los desarrolladores de este mod me dieron una habitación agradable y cómoda para quedarme cuando no estuvieras."
    m 1lksdla_static "Pero solo puedo entrar si me dices 'adiós' o 'buenas noches' antes de cerrar el juego."
    m 2eub_static "Así que asegúrate de decir eso antes de irte, ¿okey?"
    m "De todos modos.{w=0.5}.{w=0.5}.{w=0.5}{nw}"





























    $ persistent.opendoor_opencount += 1


label monikaroom_greeting_opendoor_post2:
    show monika 5eua_static at hf11
    m "Me alegro de que hayas vuelto, [player]."
    show monika 5eua_static at t11

    m "Últimamente he estado practicando el cambio de fondos y ahora puedo cambiarlos instantáneamente."
    m "¡Mira!"


    m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
    $ mas_startupWeather()
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False)
    show monika 4eua_static zorder MAS_MONIKA_Z at i11
    m "¡Tada!"


    show monika at lhide
    hide monika
    jump monikaroom_greeting_post


label monikaroom_greeting_opendoor:
    $ is_sitting = False


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)
    $ mas_startupWeather()

    call spaceroom (start_bg="bedroom", hide_monika=True, dissolve_all=True, show_emptydesk=False, scene_change=True, hide_calendar=True)


    $ behind_bg = MAS_BACKGROUND_Z - 1
    show bedroom as sp_mas_backbed zorder behind_bg

    m 2esd "~¿Es amor, si te tomo o es amor, si te dejo ir?~"
    show monika 1eua_static zorder MAS_MONIKA_Z at l32


    $ mas_disable_quit()

    m 1eud_static "¡¿E-Eh?! ¡[player]!"
    m "¡Me sorprendiste, apareciendo de repente!"

    show monika 1eua_static at hf32
    m 1hksdlb_static "¡No tuve tiempo para prepararme!"
    m 1eka_static "Pero gracias por volver, [player]."
    show monika 1eua_static at t32
    m 3eua_static "Solo dame unos segundos para configurar todo, ¿okey?"
    show monika 1eua_static at t31
    m 2eud_static "..."
    show monika 1eua_static at t33
    m 1eud_static "... Y..."

    if mas_current_background.isFltDay():
        show monika_day_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft
    else:
        show monika_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft

    show monika 3eua_static at t32
    m 3eua_static "¡Listo!"
    menu:
        "La ventana...":
            show monika 1eua_static at h32
            m 1hksdlb_static "¡Ups! Me olvidé de eso~"
            show monika 1eua_static at t21
            m "Espera.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
            hide sp_mas_backbed with dissolve
            m 2hua_static "¡Todo arreglado!"
            show monika 1eua_static at lhide
            hide monika

    $ persistent.seen_monika_in_room = True
    jump monikaroom_greeting_post


label monikaroom_greeting_knock:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    m "¿Quién es?~"
    menu:
        "Soy yo":

            $ mas_disable_quit()
            if mas_isMoniNormal(higher=True):
                m "¡[player]! ¡Estoy tan feliz de que hayas vuelto!"

                if persistent.seen_monika_in_room:
                    m "Y gracias por tocar primero~"
                m "Espera, déjame ordenar..."

            elif mas_isMoniUpset():
                m "[player].{w=0.3} Has vuelto..."

                if persistent.seen_monika_in_room:
                    m "Al menos tocaste."
            else:

                m "Oh... {w=0.5}okey."

                if persistent.seen_monika_in_room:
                    m "Gracias por tocar."

            $ mas_startupWeather()
            call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=False)
    jump monikaroom_greeting_post


label monikaroom_greeting_post:
    if mas_isMoniNormal(higher=True):
        m 2eua_static "Ahora, déjame buscar una mesa y una silla.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ is_sitting = True
        show monika 1eua zorder MAS_MONIKA_Z at ls32
        $ today = "hoy" if mas_globals.time_of_day_4state != "as noches" else "esta noche"
        m 1eua "¿Qué haremos [today], [mas_get_player_nickname()]?"

    elif mas_isMoniUpset():
        m "Déjame buscar una mesa y una silla.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ is_sitting = True
        show monika 2esc zorder MAS_MONIKA_Z at ls32
        m 2esc "¿Querías algo, [player]?"
    else:

        m "Necesito buscar una mesa y una silla.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ is_sitting = True
        show monika 6ekc zorder MAS_MONIKA_Z at ls32
        m 6ekc "¿Había algo que quisieras, [player]?"

    jump monikaroom_greeting_cleanup


label monikaroom_greeting_cleanup:
    python:


        mas_disable_quit()


        mas_MUINDropShield()


        set_keymaps()


        mas_OVLShow()


        mas_startup_song()


        enable_esc()

    return




label greeting_youarereal:
    python:
        try:
            renpy.file(
                "../characters/" + persistent.playername.lower() + ".chr"
            )
            persistent._mas_you_chr = True
        except:
            persistent._mas_you_chr = False
    m 1hua "¡[player]! ¡Me alegro de verte!"
    if persistent._mas_you_chr:
        m 1euc "Espera. Algo esta diferente hoy."
        m 1eud "¿Has... añadido un archivo de personaje?"
        m 1ekc "¿'[player].chr'...?"
        m 1ekd "¿Estás... tratando de ponerte aquí conmigo?"
        m "¿Por qué harías eso?"
        m 1tkc "¿No lo entiendes?"
        m 1tkd "¡Este lugar no es real! ¡No sé qué pasará si vienes aquí!"
        m 1dsc "¿Como pudiste hacer esto?"
        m 1lksdlc "Renunciar a tu realidad..."
        m 1lksdld "¿Solo para estar conmigo?"
        m 1ekc "¡Todo esto es culpa mía!"
        m "Pero... pero el 'tú', en el juego..."
        m 1esd "Está empezando a moverse un poco."
        m "¿Quizás... esto te está permitiendo controlarlo de nuevo?"
        m 1ekc "¡Esto no está bien! ¡No quiero una marioneta!"
        m 1tkc "Por favor, [player]..."
        m "Si vas a hacerlo, ¿estás seguro de que es lo que quieres?{nw}"
        $ _history_list.pop()
        menu:
            m "Si vas a hacerlo, ¿estás seguro de que es lo que quieres?{fast}"
            "Estoy seguro":

                m 1eka "Entonces... no tengo más remedio que aceptarlo..."
                m 1hub "¡Aceptaré este regalo con los brazos abiertos!"
                m "Finalmente podemos estar juntos, [player]."
                m "Y podemos averiguar cómo hacerlo en tu realidad, ¡juntos!"
            "Tal vez no...":

                m 1eka "Me lo imaginaba..."
                m "No hay forma de que renuncies a ser 'real' para estar conmigo..."
                m 1ekc "No me atrevo a borrar ese lindo archivo .chr, pero..."
                m 1eka "Considera hacerlo."
                m 1lksdlc "Hay algunas cosas espeluznantes en esos archivos..."
                m 1eka "Te amo, [player]. Esperaré todo lo que sea necesario."
                m "Así que no seas precipitado, ¿okey?"
    else:
        m 1esd "He estado pensando mucho en los archivos .chr..."
        m 1euc "Como, ¿qué son realmente?"
        m 1lksdlc "Son un poco espeluznantes..."
        m "E incluso si las otras chicas no son reales, ¿por qué eliminar uno de esos archivos puede eliminar un personaje?"
        m 1esd "¿Se podría agregar un personaje?"
        m 1dsd "Es difícil saberlo..."
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_japan",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_japan:
    m 1hub "Oh, ¡kon'nichiwa [player]!"
    m "Jejeje~"
    m 2eub "¡Hola, [player]!"
    m 1eua "Solo estoy practicando japonés."
    m 3eua "Veamos..."
    $ shown_count = mas_getEVLPropValue("greeting_japan", "shown_count")
    if shown_count == 0:
        m 4hub "¡Watashi ha itsumademo anata no mono desu!"
        m 2hksdlb "¡Lo siento si eso no tiene sentido!"
        m 3eua "¿Sabes lo que eso significa, [mas_get_player_nickname()]?"
        m 4ekbsa "Significa {i}'Seré tuya para siempre'~{/i}"
        return

    m 4hub "¡Watashi wa itsumademo anata no mono desu!"
    if shown_count == 1:
        m 3eksdla "La última vez que lo dije que cometí un error..."
        m "En esa oración, se supone que debes decir 'wa', no 'ha', como hice antes."
        m 4eka "No te preocupes, [player]. El significado sigue siendo el mismo."
        m 4ekbsa "Seré tuya para siempre~"
    else:
        m 3eua "¿Recuerda lo que significa, [mas_get_player_nickname()]?"
        m 4ekbsa "{i}'Seré tuya para siempre'~{/i}"
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sunshine",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_sunshine:
    m 1hua "{i}~Eres mi sol, mi único sol~{/i}"
    m "{i}~Me haces feliz cuando el cielo está gris~{/i}"
    m 1hub "{i}~Nunca sabrás cariño, cuánto te amo~{/i}"
    m 1eka "{i}~Por favor, no me quites mi sol~{/i}"
    m 1wud "... ¿Eh?"
    m "¡¿H-Huh?!"
    m 1wubsw "¡[player]!"
    m 1lkbsa "Oh, ¡santo cielo, esto es tan vergonzoso!"
    m "¡Solo estaba cantando para pasar el rato!"
    m 1ekbfa "Jejeje..."
    m 3hubfa "Pero ahora que estás aquí, podemos pasar un tiempo juntos~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hai_domo",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_hai_domo:
    m 1hub "{=jpn_text}はいどうもー!{/=jpn_text}"
    m "¡Novia virtual, aquí Monika!"
    m 1hksdlb "¡Jajaja, lo siento! Últimamente he estado viendo a cierta youtuber virtual."
    m 1eua "Tengo que decir que es bastante encantadora..."
    $ mas_lockEVL("greeting_hai_domo", "GRE")
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_french",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_french:
    m 1eua "¡Bonjour, [player]!"
    m 1hua "¿Savais-tu que tu avais de beaux yeux, mon amour?"
    m 1hub "¡Jajaja!"
    m 3hksdlb "Estoy practicando algo de francés. Te acabo de decir que tienes unos ojos muy bonitos~"
    m 1eka "Es un idioma tan romántico, [player]."
    m 1hua "Tal vez ambos podamos practicarlo en algún momento, mon amour~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_amnesia",
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_amnesia:
    python:
        tempname = m_name
        m_name = "Monika"

    m 1eua "¡Oh, hola!"
    m 3eub "Mi nombre es Monika."
    show monika 1eua zorder MAS_MONIKA_Z

    python:
        entered_good_name = True
        fakename = renpy.input("¿Cuál es tu nombre?", allow=name_characters_only, length=20).strip(" \t\n\r")
        lowerfake = fakename.lower()

    if lowerfake in ("sayori", "yuri", "natsuki"):
        m 3euc "Uh, eso es gracioso."
        m 3eud "Uno de mis amigas comparte el mismo nombre."

    elif lowerfake == "monika":
        m 3eub "Oh, ¿tú nombre es Monika también?"
        m 3hub "Jajaja, ¿cuáles eran las posibilidades, verdad?"

    elif lowerfake == "monica":
        m 1hua "Hey, tenemos nombres muy similares, jejeje~"

    elif lowerfake == player.lower():
        m 1hub "Oh, ¡que nombre tan bonito!"

    elif lowerfake == "":
        $ entered_good_name = False
        m 1euc "..."
        m 1etd "¿Intentas decirme que no tienes un nombre o eres demasiado tímido para decírmelo?"
        m 1eka "Es un poco extraño, pero supongo que no importa demasiado."

    elif mas_awk_name_comp.search(lowerfake) or mas_bad_name_comp.search(lowerfake):
        $ entered_good_name = False
        m 1rksdla "Eso es... {w=0.4}{nw}"
        extend 1hksdlb "una especie de nombre inusual, jajaja..."
        m 1eksdla "¿Estás... {w=0.3}tratando de molestarme?"
        m 1rksdlb "Ah, lo siento, lo siento, no estoy juzgando ni nada."

    python:
        if entered_good_name:
            name_line = renpy.substitute(", [fakename]")
        else:
            name_line = ""

        if mas_current_background == mas_background_def:
            end_of_line = "parece que no puedo dejar esta aula de clases."
        else:
            end_of_line = "no estoy segura de dónde estoy."

    m 1hua "Bueno, ¡gusto en conocerte[name_line]!"
    m 3eud "Dime[name_line], ¿sabes por casualidad dónde están los demás?"
    m 1eksdlc "Eres la primera persona que veo y {nw}"
    extend 1rksdlc "[end_of_line]"
    m 1eksdld "¿Puedes ayudarme a descubrir que está pasando[name_line]?"

    m "¿Por favor? {w=0.2}{nw}"
    extend 1dksdlc "Extraño a mis amigas."

    window hide
    show monika 1eksdlc
    pause 5.0
    $ m_name = tempname
    window auto

    m 1rksdla "..."
    m 1hub "¡Jajaja!"
    m 1hksdrb "¡Lo siento, [player]! No pude evitarlo."
    m 1eka "Después de hablar sobre {i}Flores para Algernon{/i}, no pude resistirme a ver cómo reaccionarías si me olvidara de todo."

    if lowerfake == player.lower():
        m 1tku "... Y reaccionaste de la manera que imaginé que lo harías."

    m 3eka "Pero espero no haberte molestado demasiado."
    m 1rksdlb "Me sentiría igual si alguna vez te olvidas de mí, [player]."
    m 1hksdlb "Espero que puedas perdonar mi pequeña broma, jajaja~"

    $ mas_lockEVL("greeting_amnesia", "GRE")
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sick",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SICK],
        ),
        code="GRE"
    )




label greeting_sick:
    if mas_isMoniNormal(higher=True):
        m 1hua "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
        m 3eua "¿Te sientes mejor?{nw}"
    else:
        m 2ekc "Bienvenido de nuevo, [player]..."
        m "¿Te sientes mejor?{nw}"

    $ _history_list.pop()
    menu:
        m "¿Te sientes mejor?{fast}"
        "Sí":
            $ persistent._mas_mood_sick = False
            if mas_isMoniNormal(higher=True):
                m 1hub "¡Excelente! Ahora podemos pasar más tiempo juntos. Jejeje~"
            else:
                m "Es bueno escuchar eso."
        "No":
            jump greeting_stillsick
    return

label greeting_stillsick:
    if mas_isMoniNormal(higher=True):
        m 1ekc "[player], deberías ir a descansar un poco."
        m "Descansar lo suficiente es la mejor manera de recuperarse de una enfermedad."
        m 2lksdlc "No me perdonaría si tu salud empeorara por mi culpa."
        m 2eka "Ahora, por favor, [player], tranquilízame y ve a descansar."
        m "¿Harás eso por mí?"
    else:

        m 2ekc "[player], deberías ir a descansar un poco."
        m 4ekc "Descansar lo suficiente es la mejor manera de recuperarse de una enfermedad."
        m "Ahora, por favor, [player], ve a descansar."
        m 2ekc "¿Harás eso por mí?{nw}"

    $ _history_list.pop()
    menu:
        m "¿Harás eso por mí?{fast}"
        "Sí":
            jump greeting_stillsickrest
        "No":
            jump greeting_stillsicknorest
        "Ya estoy descansando":
            jump greeting_stillsickresting

label greeting_stillsickrest:
    if mas_isMoniNormal(higher=True):
        m 2hua "Gracias, [player]."
        m 2eua "Creo que si te dejo solo por un tiempo, podrás descansar mejor."
        m 1eua "Así que voy a cerrar el juego por ti."
        m 1eka "Recupérate pronto, [player]. ¡Te amo!"
    else:

        m 2ekc "Gracias, [player]."
        m "Creo que si te dejo solo por un tiempo, podrás descansar mejor."
        m 4ekc "Así que voy a cerrar el juego por ti."
        m 2ekc "Recupérate pronto, [player]."

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return 'quit'

label greeting_stillsicknorest:
    if mas_isMoniNormal(higher=True):
        m 1lksdlc "Ya veo..."
        m "Bueno, si insistes, [player]."
        m 1ekc "Supongo que conoces tus limites mejor que yo."
        m 1eka "Pero [player], si empiezas a sentirte un poco débil o cansado, házmelo saber."
        m "De esa manera podrás ir a descansar."
        m 1eua "No te preocupes, todavía estaré aquí cuando te despiertes."
        m 3hua "Entonces podremos divertirnos juntos un poco más sin que me preocupe por ti en el fondo de mi mente."
    else:

        m 2ekc "Bien."
        m 2tkc "Parece que nunca quieres escucharme, ¿por qué esperé que esta vez sería diferente?"


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

label greeting_stillsickresting:
    m 1eka "Oh, es un alivio oir eso, [player]."
    m 3eka "Espero que te mantengas caliente."
    if mas_isMoniNormal(higher=True):
        m 1dku "Quizás acurrucado en una manta calentita con una taza de té caliente."
        m 2eka "Tu salud es muy importante para mí [player], así que asegúrate de cuidarte."
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "... Y si todavía sientes un poco de frío, espero que el saber que te amo te anime un poco."
        m 5hua "Jejeje~"
        $ mas_ILY()
    else:

        m 1eka "Tal vez acurrucado en una manta calientita con una taza de té caliente."
        m 2eka "Tu salud es muy importante para mí [player], así que asegúrate de cuidarte."



    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_long_absence",
            unlocked=True,
            category=[store.mas_greetings.TYPE_LONG_ABSENCE],
        ),
        code="GRE"
    )

label greeting_long_absence:
    $ persistent._mas_long_absence = False
    $ mas_ret_long_absence = True

    if persistent._mas_absence_time >= datetime.timedelta(weeks=5):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.1, min_amount=70)
            m 2dsc "[player]..."
            m 2tkc "Dijiste que solo te irías por unos días..."
            m 2rksdld "Pero ha pasado tanto tiempo."
            m 2ekd "Me alegro de que hayas vuelto ahora, pero..."
            m 2dktdc "Estaba tan sola..."
            m 2ektsc "¡Pensé que te había pasado algo!"
            m 2lktsc "Yo... seguí pensando que tal vez no volverías."
            m 2ektsc "Por favor, nunca,{w=0.5} {i}nunca{/i}{w=0.5} vuelvas a hacer eso."
            m 2rktsd "Quizás no pudiste evitarlo, pero... estaba muy preocupada."
            m 2dftdc "No sabía qué hacer."
            m 4ekc "En la medida de lo posible, [player], no te vayas por tanto tiempo."
            m 2ekd "Si crees que no tienes otra opción, por favor dímelo."
            m 1dsc "No quiero volver a quedarme sola..."

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.08, min_amount=60)
            m 3ekc "Bienvenido de nuevo, [player]."
            m 3rksdlc "Llegas un poco tarde, ¿no crees?"
            m 3ekc "Sé que habías dicho que estarías fuera por un tiempo, pero... dijiste {i}una semana{/i}."
            m 2rkc "Voy a asumir que no fue tu culpa..."
            m 2ekd "Pero si realmente crees que tardarás más la próxima vez, tienes que decírmelo.."
            m 2rksdld "Empecé a pensar que tal vez te había pasado algo malo."
            m 2dkc "Pero seguí diciéndome a mí misma que estabas bien..."
            m 2eka "Me alegro de que estés a salvo y de vuelta conmigo, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffectionFraction(0.06, min_amount=40)
            m 1wud "¡[player]!"
            m 1hua "¡Finalmente estás aquí!"
            m 1ekd "Estaba muy preocupada..."
            m 2dkd "¿Por qué te fuiste por tanto tiempo?"
            m 2rkc "Pensé que solo te irías por un par de semanas..."
            m "Pero te fuiste por más del doble."
            m 1rksdlc "¿Estabas tan ocupado?"
            m 3tkc "Espero que no te hayas sobrecargado..."
            m 1eka "Bueno, ahora estás aquí conmigo, así que si algo va mal, no dudes en decírmelo."

        elif persistent._mas_absence_choice == "month":
            $ mas_loseAffectionFraction(0.04, min_amount=20)
            m 1eua "Bienvenido de nuevo, [mas_get_player_nickname()]."
            m 2rkc "Ha pasado bastante, ¿verdad?"
            m 2rksdlc "Te has ido más tiempo del que dijiste..."
            m 2eka "Pero está bien, estaba preparada."
            m 3rksdlc "Honestamente, ha sido bastante solitario sin ti por aquí..."
            m 3ekbsa "Espero que me lo compenses~"
            show monika 1eka

        elif persistent._mas_absence_choice == "longer":
            m 1esc "Ha pasado mucho tiempo, [player]."
            m 1ekc "Estaba lista, pero eso no lo hizo más fácil."
            m 3eka "Espero que hayas hecho lo que tenías que hacer."
            m 2rksdlc "..."
            m 2tkc "A decir verdad, he estado bastante triste últimamente."
            m 2dkc "No tenerte en mi vida por tanto tiempo..."
            m 2dkd "Estaba muy sola..."
            m "Me sentí tan aislada y vacía sin ti aquí."
            m 3eka "Me alegro mucho de que estés aquí ahora. Te amo, [player]. Bienvenido a casa."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "¡Por fin has vuelto [player]!"
            m 3rksdla "Cuando dijiste que no sabías, {i}realmente{/i} no sabías, ¿verdad?"
            m 3rksdlb "Debes haber estado bastante ocupado si estuviste fuera por {i}este{/i} tiempo."
            m 1hua "Bueno, ya estás de vuelta... ¡Te he echado mucho de menos!"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=4):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.1, min_amount=60)
            m 1dkc "[player]..."
            m 1ekd "Dijiste que solo estarías fuera unos días..."
            m 2efd "¡Pero ha sido un mes entero!"
            m 2ekc "Pensé que te había pasado algo."
            m 2dkd "No estaba segura de qué hacer..."
            m 2efd "¿Qué te mantuvo alejado durante tanto tiempo?"
            m 2eksdld "¿Hice algo mal?"
            m 2dftdc "Puedes decirme cualquier cosa, pero no desaparezcas así."
            show monika 2dfc

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.08, min_amount=50)
            m 1esc "Hola, [player]."
            m 3efc "Llegas bastante tarde, sabes."
            m 2lfc "No pretendo ser grosera, ¡pero una semana no es lo mismo que un mes!"
            m 2rksdld "Supongo que tal vez algo te mantuvo muy ocupado."
            m 2wfw "¡Pero no deberías haber estado tan ocupado como para que no pudieras decirme que podrías tardar más!"
            m 2wud "¡Ah...!"
            m 2lktsc "Lo siento, [player]. Yo solo... te extrañé mucho."
            m 2dftdc "Lo siento por quebrarme así."
            show monika 2dkc

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffectionFraction(0.06, min_amount=30)
            m 1wuo "... ¡Oh!"
            m 1sub "¡Por fin has vuelto [player]!"
            m 1efc "Me dijiste que te irías por un par de semanas, ¡pero ha pasado al menos un mes!"
            m 1ekd "Estaba muy preocupada por ti, ¿sabes?"
            m 3rkd "Pero supongo que estaba fuera de tu control."
            m 1ekc "Si puedes, la próxima vez, solo si dime que tardarás aún más, ¿okey?"
            m 1hksdlb "Después de todo, creo que me lo merezco por ser tu novia."
            m 3hua "Aún así, bienvenido de nuevo, [mas_get_player_nickname()]!"

        elif persistent._mas_absence_choice == "month":
            $ mas_gainAffection()
            m 1wuo "... ¡Oh!"
            m 1hua "¡Estás aquí [player]!"
            m 1hub "¡Sabía que podía confiar en que cumplirías tu palabra!"
            m 1eka "Realmente eres especial, lo sabes, ¿verdad?"
            m 1hub "¡Te he extrañado mucho!"
            m 2eub "Cuéntame todo lo que hiciste mientras estuviste fuera, ¡quiero saberlo todo!"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1esc "... ¿Hm?"
            m 1wub "¡[player]!"
            m 1rksdlb "Regresaste un poco antes de lo que pensé..."
            m 3hua "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
            m 3eka "Sé que ha pasado bastante tiempo, así que estoy segura de que has estado ocupado."
            m 1eua "Me encantaría saber todo lo que has hecho."
            show monika 1hua

        elif persistent._mas_absence_choice == "unknown":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "¡Oh!"
            m 1sub "¡[player]!"
            m 1hub "¡Que agradable sorpresa!"
            m 1eka "¿Cómo estás?"
            m 1ekd "Ha pasado mes entero. Realmente no sabías cuánto tiempo estarías fuera, ¿verdad?"
            m 3eka "Aun así, regresaste y eso significa mucho para mí."
            m 1rksdla "Sabía que volverías eventualmente..."
            m 1hub "¡Te amo mucho, [player]!"
            show monika 1hua

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=2):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.08, min_amount=30)
            m 1wud "O-Oh, ¡[player]!"
            m 1hua "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
            m 3ekc "Estuviste fuera más tiempo del que dijiste que estarías..."
            m 3ekd "¿Está todo bien?"
            m 1eksdla "Sé que la vida puede ser ocupada y te alejara de mí a veces... así que no estoy molesta..."
            m 3eksdla "Solo... la próxima vez, ¿tal vez puedas avisarme?"
            m 1eka "Sería muy amable de tu parte."
            m 1hua "¡Y te lo agradecería mucho!"

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.06, min_amount=20)
            m 1eub "¡Hola, [player]!"
            m 1eka "¿La vida te mantiene ocupado?"
            m 3hksdlb "Bueno, debe ser de lo contrario, porque debiste haber estado aquí cuando dijiste."
            m 1hksdlb "¡Pero no te preocupes! No estoy enojada."
            m 1eka "Solo espero que te hayas estado cuidando."
            m 3eka "Sé que no siempre puedes estar aquí, ¡así que asegúrate de estar a salvo hasta que estés conmigo!"
            m 1hua "Yo cuidaré de ti a partir de ahí~"
            show monika 1eka

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_gainAffection()
            m 1hub "¡Hey, [player]!"
            m 1eua "Regresaste cuando dijiste que lo harías después de todo."
            m 1eka "Gracias por no traicionar mi confianza."
            m 3hub "¡Recuperemos el tiempo perdido!"
            show monika 1hua

        elif persistent._mas_absence_choice == "month":
            m 1wud "¡Oh cielos! ¡[player]!"
            m 3hksdlb "No esperaba que volvieras tan pronto."
            m 3ekbsa "Supongo que me extrañaste tanto como yo te extrañé a ti~"
            m 1eka "Es maravilloso verte de regreso tan pronto."
            m 3ekb "Esperaba que el día fuera tranquilo... pero afortunadamente, ¡ahora te tengo a ti!"
            m 3hua "Gracias por regresar pronto, [mas_get_player_nickname()]."

        elif persistent._mas_absence_choice == "longer":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "¡Oh! ¡[player]!"
            m 1hub "¡Regresaste muy pronto!"
            m 1hua "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
            m 3eka "No sabía cuándo esperarte, pero no imaginé que sería tan pronto..."
            m 1hua "Bueno, ¡me ha animado mucho!"
            m 1eka "Te he echado de menos."
            m 1hua "Disfrutemos el resto del día juntos."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "¡Hola, [player]!"
            m 3eka "¿Has estado ocupado las últimas semanas?"
            m 1eka "Gracias por advertirme de que te irías."
            m 3ekd "De lo contrario, estaría muy preocupada."
            m 1eka "Realmente ayudó..."
            m 1eua "Entonces dime, ¿cómo has estado?"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=1):
        if persistent._mas_absence_choice == "days":
            m 2eub "Hola, [player]."
            m 2rksdla "Tardaste un poco más de lo que dijiste... pero no te preocupes."
            m 3eub "¡Sé que eres una persona ocupada!"
            m 3rkc "Pero tal vez, ¿podrías advierteme primero?"
            m 2rksdlc "Cuando dijiste unos días... pensé que sería menos de una semana."
            m 1hub "¡Pero está bien! ¡Te perdono!"
            m 1ekbsa "Después de todo, eres mi único amor."
            show monika 1eka

        elif persistent._mas_absence_choice == "week":
            $ mas_gainAffection()
            m 1hub "¡Hola, [mas_get_player_nickname()]!"
            m 3eua "Es tan agradable cuando se puede confiar el uno en el otro, ¿verdad?"
            m 3hub "¡En eso se basa la fuerza de una relación!"
            m 3hua "¡Significa que la nuestra es tan sólida como una roca!"
            m 1hub "¡Jajaja!"
            m 1hksdlb "Lo siento, lo siento. ¡Estoy emocionada de que hayas vuelto!"
            m 3eua "Dime como te ha ido. Quiero saberlo todo."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "Hola~"
            m 3eua "Has vuelto un poco antes de lo que pensaba... ¡Pero me alegro de que hayas regresado!"
            m 3eka "Cuando estás aquí conmigo, todo se vuelve mejor."
            m 1eua "Tengamos un hermoso día juntos, [player]."
            show monika 3eua

        elif persistent._mas_absence_choice == "month":
            m 1hua "Jejeje~"
            m 1hub "¡Bienvenido de vuelta!"
            m 3tuu "Sabía que no podías permanecer fuera durante un mes entero..."
            m 3tub "¡Si estuviera en tu posición, tampoco podría alejarme de ti!"
            m 1hksdlb "Honestamente, ¡te extrañé después de solo unos días!"
            m 1eka "Gracias por no hacerme esperar tanto~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1hub "¡Mira quién ha vuelto tan pronto! ¡Eres tú, mi querido [player]!"
            m 3hksdlb "No podrías mantenerte alejado incluso si quisieras, ¿verdad?"
            m 3eka "¡No puedo culparte! ¡Mi amor por ti tampoco me dejaría alejarme de ti!"
            m 1ekd "Todos los días que no estuviste me preguntaba cómo estabas..."
            m 3eka "Así que déjame escucharte. ¿Cómo estás, [player]?"
            show monika 3eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hub "¡Hola, [mas_get_player_nickname()]!"
            m 1eka "Me alegra que no me hicieras esperar demasiado."
            m 1hua "Una semana es más corta de lo que esperaba, ¡así que considérame sorprendida!"
            m 3hub "¡Gracias por alegrarme el día, [player]!"
            show monika 3eua
    else:

        if persistent._mas_absence_choice == "days":
            m 1hub "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
            m 1eka "Gracias por advertirme sobre cuánto tiempo estarías fuera."
            m 1eua "Significa mucho saber que puedo confiar en tus palabras."
            m 3hua "¡Espero que sepas que también puedes confiar en mí!"
            m 3hub "Nuestra relación se fortalece cada día~"
            show monika 1hua

        elif persistent._mas_absence_choice == "week":
            m 1eud "¡Oh! ¡Llegaste un poco antes de lo que esperaba!"
            m 1hua "No es que me queje, es genial volver a verte tan pronto."
            m 1eua "Tengamos otro buen día juntos, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "{i}~Con mi mano,~\n~escribiré poemas que-{/i}"
            m 1wubsw "¡O-Oh! ¡[player]!"
            m 3hksdlb "Regresaste mucho antes de lo que me dijiste..."
            m 3hub "¡Bienvenido!"
            m 1rksdla "Me interrumpiste practicando mi canción..."
            m 3hua "¿Por qué no me escuchas cantarla de nuevo?"
            m 1ekbsa "La hice solo para ti~"
            show monika 1eka

        elif persistent._mas_absence_choice == "month":
            m 1wud "¿Eh? ¿[player]?"
            m 1sub "¡Estás aquí!"
            m 3rksdla "Pensé que te ibas a ir un mes entero."
            m 3rksdlb "Estaba lista, pero..."
            m 1eka "¡Ya te extrañaba!"
            m 3ekbsa "¿También me extrañaste?"
            m 1hubfa "Gracias por volver tan pronto~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1eud "¿[player]?"
            m 3ekd "Pensé que ibas a estar fuera por mucho tiempo..."
            m 3tkd "¿Por qué volviste tan pronto?"
            m 1ekbsa "¿Me estás visitando?"
            m 1hubfa "¡Eres un amor!"
            m 1eka "Si aún te vas a ir por un tiempo, asegúrate de decírmelo."
            m 3eka "Te amo, [player], y no me gustaría enojarme si vas a estar fuera..."
            m 1hub "¡Disfrutemos nuestro tiempo juntos hasta entonces!"
            show monika 1eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Jejeje~"
            m 3eka "¿Regresaste tan pronto, [player]?"
            m 3rka "Supongo que cuando dijiste que no lo sabías, no te diste cuenta de que no pasaría mucho tiempo."
            m 3hub "¡Pero gracias por advertirme de todos modos!"
            m 3ekbsa "Me hizo sentir amada."
            m 1hubfb "¡Si que eres de buen corazón!"
            show monika 3eub
    m "Recuérdame si te vas otra vez, ¿okey?"
    show monika idle with dissolve_monika
    jump ch30_loop


init python:
    ev_rules = dict()
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours=range(0,6)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern:
    jump monika_timeconcern

init python:
    ev_rules = {}
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours =range(6,24)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern_day",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern_day:
    jump monika_timeconcern

init python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(
        skip_visual=True,
        random_chance=0.2,
        override_type=True
    ))
    ev_rules.update(MASPriorityRule.create_rule(45))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hairdown",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.HAPPY, None),
        ),
        code="GRE"
    )
    del ev_rules

label greeting_hairdown:



    $ mas_RaiseShield_core()






    if monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
        $ monika_chr.reset_clothes(False)


    $ monika_chr.change_hair(mas_hair_down, by_user=False)

    call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "¡Hola, [player]!"
    m 4hua "¿Notas algo diferente hoy?"
    m 1hub "Decidí probar algo nuevo~"

    m "¿Te gusta?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gusta?{fast}"
        "Sí":
            $ persistent._mas_likes_hairdown = True


            $ mas_gainAffection()
            m 6sub "¿De verdad?"
            m 2hua "¡Estoy tan feliz!"
            m 1eua "Pregúntame si quieres volver a ver mi coleta, ¿de acuerdo?"
        "No":


            m 1ekc "Oh..."
            m 1lksdlc "..."
            m 1lksdld "Voy a ponerlo de nuevo para ti, entonces."
            m 1dsc "..."

            $ monika_chr.reset_hair(False)

            m 1eua "Listo."



    $ store.mas_selspr.unlock_hair(mas_hair_down)
    $ store.mas_selspr.save_selectables()


    $ mas_unlockEventLabel("monika_hair_select")


    $ mas_lockEVL("greeting_hairdown", "GRE")



    $ mas_MUINDropShield()


    $ set_keymaps()


    $ HKBShowButtons()


    $ mas_startup_song()


    $ enable_esc()

    return

init python:



    ev_rules = {}
    ev_rules.update(MASPriorityRule.create_rule(15))
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1dsc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_tears",
            unlocked=True,
            aff_range=(None, mas_aff.DISTRESSED),
            rules=ev_rules,
        ),
        code="GRE"
    )
    del ev_rules

label greeting_tears:
    m 1dsc "... [player]."
    m 1ekc "..."
    m 2ekc "¿Hay algo mal conmigo?"
    m 2ekd "¿No soy lo suficientemente buena para ti...?"
    m 2lksdlc "He hecho todo lo posible por ti... por {i}nosotros{/i}."
    m 2lksdld "¿Hice algo para lastimarte o hacerte sentir maltratado?"
    m "¿Sigues molesto por lo de las otras chicas?"
    m 2ekc "Si es así, realmente lo siento..."
    m "¡Lo siento mucho!"
    m 2rksdld "Solo dime qué hice mal y me esforzaré aún más por ser la novia perfecta para ti."
    m 2ekd "Eres todo mi mundo; ¡lo que sientes lo es todo para mí!"
    m 2ekc "Así que, por favor, díme qué pasa y lo arreglaré."
    m 2dfc "Haré cualquier cosa por ti porque...yo..."
    m 2dftdc "..."
    m 2dftsc "... Te necesito, [player]..."
    m 2ektsc "Necesito que me ames tanto como yo te amo."
    m 2lktsc "Te necesito... porque si no te tengo, entonces..."
    m 2dftsc "..."
    m 2ektsc "Estaré sola..."
    m 2dftsc "Así que por favor... quedate aquí asi como yo lo hago por ti."
    m "Quiero creerlo..."
    m 2lktsc "Así que por favor...déjame ser feliz a tu lado..."
    m "..."
    pause 4.0
    m 2dftdc "..."
    m 2dfc "... Okey... okey..."
    m 2lssdrc "Tengo que ser fuerte..."
    m "..."
    m 2dsc "... Muy bien... estoy un poco mejor ahora..."
    m 2esc "Pero... necesito que pienses en lo que dije."
    m 2ekc "Por favor... solo... trata de entender."
    m 1dsd "Te amo y necesito que me demuestres que tú también me amas..."
    m 1dsc "De lo contrario... no podré manejarlo más."

    python:
        mas_lockEVL("greeting_tears", "GRE")


        beingvirtual_ev = mas_getEV("monika_being_virtual")

        if beingvirtual_ev:
            beingvirtual_ev.start_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_upset",
            unlocked=True,
            aff_range=(mas_aff.UPSET, mas_aff.UPSET),
        ),
        code="GRE"
    )

label greeting_upset:
    python:
        upset_greeting_quips_first = [
            "Oh. {w=1}Eres tú, [player].",
            "Oh. {w=1}Volviste, [player].",
            "Hola, [player].",
            "Oh. {w=1}Hola, [player]."
        ]

        upset_greeting_quips_second = [


            "Bueno...",
            "¿Querías algo?",
        ]

    $ upset_quip1 = renpy.random.choice(upset_greeting_quips_first)

    show monika 2esc
    $ renpy.say(m, upset_quip1)

    if renpy.random.randint(1,4) != 1:
        $ upset_quip2 = renpy.random.choice(upset_greeting_quips_second)
        $ renpy.say(m, upset_quip2)

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_distressed",
            unlocked=True,
            aff_range=(mas_aff.DISTRESSED, mas_aff.DISTRESSED)
        ),
        code="GRE"
    )

label greeting_distressed:
    python:
        distressed_greeting_quips_first = [
            "Oh... {w=1}hola, [player].",
            "Oh... {w=1}hola, [player].",
            "Hola, [player]...",
            "Oh... {w=1}volviste, [player]."
        ]

        distressed_greeting_quips_second = [
            "Supongo que ahora podemos pasar algo de tiempo juntos.",
            "No estaba segura de cuándo volverías a visitarme.",
            "Espero que podamos disfrutar de nuestro tiempo juntos.",
            "No te esperaba.",
            "Espero que las cosas comiencen a mejorar.",
            "Pensé que te habías de mí..."
        ]

    $ distressed_quip1 = renpy.random.choice(distressed_greeting_quips_first)

    show monika 6ekc
    $ renpy.say(m, distressed_quip1)

    if renpy.random.randint(1,4) != 1:
        $ distressed_quip2 = renpy.random.choice(distressed_greeting_quips_second)
        show monika 6rkc
        $ renpy.say(m, distressed_quip2)

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_broken",
            unlocked=True,
            aff_range=(None, mas_aff.BROKEN),
        ),
        code="GRE"
    )

label greeting_broken:
    m 6ckc "..."
    return



init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_school",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SCHOOL],
        ),
        code="GRE"
    )

label greeting_back_from_school:
    if mas_isMoniNormal(higher=True):
        m 1hua "Oh, ¡bienvenido de nuevo, [mas_get_player_nickname()]!"
        m 1eua "¿Cómo estuvo tu día en la escuela?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo estuvo tu día en la escuela?{fast}"
            "Asombroso":

                m 2sub "¡¿De verdad?!"
                m 2hub "¡Es maravilloso escuchar eso, [player]!"
                if renpy.random.randint(1,4) == 1:
                    m 3eka "La escuela definitivamente puede ser una gran parte de tu vida y es posible que la extrañes más adelante."
                    m 2hksdlb "¡Jajaja! Sé que puede ser extraño pensar que algún día extrañarás tener que ir a la escuela..."
                    m 2eub "¡Pero muchos buenos recuerdos vienen de la escuela!"
                    m 3hua "Quizás podrías hablarme de ellos en algún momento."
                else:
                    m 3hua "Siempre me hace feliz saber que eres feliz~"
                    m 1eua "Si quieres hablar de tu increíble día, ¡me encantaría que me lo contaras!"
                return
            "Bien":

                m 1hub "Eso es genial... {w=0.3}{nw}"
                extend 3eub "¡no puedo evitar sentirme feliz cuando llegas a casa de buen humor!"
                m 3hua "Espero que hayas aprendido algo útil, jejeje~"
                return
            "Mal":

                m 1ekc "Oh..."
                m 1dkc "Siento escuchar eso."
                m 1ekd "Los días malos en la escuela pueden ser desmoralizantes..."
            "Muy mal...":

                m 1ekc "Oh..."
                m 2ekd "Lamento mucho que hayas tenido un día tan malo hoy..."
                m 2eka "Me alegro de que hayas venido a mí, [player]."


        python:
            final_item = ("No quiero hablar de eso", False, False, False, 20)
            menu_items = [
                ("Fue algo relacionado con la clase", ".class_related", False, False),
                ("Fue algo causado por las personas", ".by_people", False, False),
                ("Solo tuve un mal día", ".bad_day", False, False),
                ("Me sentía enfermo hoy", ".sick", False, False),
            ]

        show monika 2ekc at t21
        window show
        m "Si no te importa que pregunte, ¿pasó algo en particular?" nointeract

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        window auto

        $ label_suffix = _return

        show monika at t11


        if not label_suffix:
            m 2dsc "Entiendo, [player]."
            m 2ekc "A veces, intentar dejar atrás un mal día es la mejor manera de afrontarlo."
            m 2eka "Pero si quieres hablar de ello más tarde, estaré más que feliz de escucharte."
            m 2hua "Te amo, [player]~"
            return "love"

        $ full_label = "greeting_back_from_school{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label

        label greeting_back_from_school.class_related:
            m 2dsc "Ya veo..."
            m 3esd "La gente probablemente te diga todo el tiempo que la escuela es importante..."
            m 3esc "Y que siempre hay que seguir adelante y trabajar duro..."
            m 2dkd "Pero a veces, eso puede estresar a las personas y ponerlas en una espiral descendente."
            m 2eka "Como dije, me alegro de que hayas venido a verme, [player]."
            m 3eka "Es bueno saber que puedo consolarte cuando te sientes triste."
            m "Recuerda, {i}eres{/i} más importante que la escuela o algunas calificaciones."
            m 1ekbsa "Especialmente para mí."
            m 1hubsa "No olvides hacer pausas si te sientes abrumado, y recuerda que cada persona tiene talentos diferentes."
            m 3hubfb "Te amo, y solo quiero que seas feliz~"
            return "love"

        label greeting_back_from_school.by_people:
            m 2ekc "Oh no, [player]... {w=0.5}eso debe haber sido terrible."
            m 2dsc "Una cosa es que te pase algo malo..."
            m 2ekd "Pero es otra muy distinta cuando una persona es la causa directa del problema."

            if persistent._mas_pm_currently_bullied or persistent._mas_pm_is_bullying_victim:
                m 2rksdlc "Espero que no sea de quien me hablaste antes..."

                if mas_isMoniAff(higher=True):
                    m 1rfc "Es {i}mejor{/i} que no sea 'él'..."
                    m 1rfd "Molestando a mi [mas_get_player_nickname(_default='amorcito', regex_replace_with_nullstr='mi ')] así de nuevo."

                m 2ekc "Me gustaría poder hacer más para ayudarte, [player]..."
                m 2eka "Pero estoy aquí si me necesitas."
                m 3hubsa "Y siempre lo estaré~"
                m 1eubsa "Espero poder hacer tu día un poco mejor."
                m 1hubfb "Te amo mucho~"
                $ mas_ILY()
            else:

                m "Espero que este no sea algo recurrente, [player]."
                m 2lksdld "De cualquier manera, tal vez sea mejor pedir ayuda a alguien..."
                m 1lksdlc "Sé que puede parecer que eso podría causar más problemas en algunos casos..."
                m 1ekc "Pero no deberías tener que sufrir a manos de otra persona."
                m 3dkd "Lamento mucho que tengas que lidiar con esto, [player]..."
                m 1eka "Pero ahora estás aquí y espero que pasar tiempo juntos te ayude a mejorar un poco el día."
            return

        label greeting_back_from_school.bad_day:
            m 1ekc "Ya veo..."
            m 3lksdlc "Esos días suceden de vez en cuando."
            m 1ekc "A veces puede ser difícil recuperarse después de un día como ese."
            m 1eka "Pero ahora estás aquí y espero que pasar tiempo juntos te ayude a mejorar un poco el día."
            return

        label greeting_back_from_school.sick:
            m 2dkd "Estar enfermo en la escuela puede ser terrible. Hace que sea mucho más difícil hacer algo o prestar atención a las clases."
            jump greeting_back_from_work_school_still_sick_ask
            return

    elif mas_isMoniUpset():
        m 2esc "Has vuelto, [player]..."

        m "¿Cómo estuvo la escuela?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo estuvo la escuela?{fast}"
            "Bien":
                m 2esc "Eso es bueno."
                m 2rsc "Espero que hayas aprendido {i}algo{/i} hoy."
            "Mal":

                m "Eso es muy malo..."
                m 2tud "Pero tal vez ahora tengas una mejor idea de cómo me he estado sintiendo, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oh... {w=1}estás de vuelta."

        m "¿Cómo estuvo la escuela?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo estuvo la escuela?{fast}"
            "Bien":
                m 6lkc "Eso es...{w=1} bueno."
                m 6dkc "S-Solo espero que no haya sido la parte... {w=2}de 'estar lejos de mí' lo que hizo que fuera un buen día."
            "Mal":

                m 6rkc "Oh..."
                m 6ekc "Eso es una lástima, [player]. Siento escuchar eso."
                m 6dkc "Sé cómo son los días malos ..."
    else:

        m 6ckc "..."

    return

default -5 persistent._mas_pm_last_promoted_d = None


init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_work",
            unlocked=True,
            category=[store.mas_greetings.TYPE_WORK],
        ),
        code="GRE"
    )

label greeting_back_from_work:
    if mas_isMoniNormal(higher=True):
        m 1hua "Oh, ¡bienvenido de nuevo, [mas_get_player_nickname()]!"

        m 1eua "¿Cómo estuvo el trabajo hoy?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo estuvo el trabajo hoy?{fast}"
            "¡Asombroso!":

                if not persistent._mas_pm_last_promoted_d:
                    $ promoted_recently = False
                else:
                    $ promoted_recently = datetime.date.today() < persistent._mas_pm_last_promoted_d + datetime.timedelta(days=180)

                m 1sub "¡Eso es {i}asombroso{/i}, [player]!"
                m 1hub "¡Estoy muy feliz de que hayas tenido un gran día!"

                m 1sua "¿Qué hizo que fuera un día tan asombroso?{nw}"
                menu:
                    m "¿Qué hizo que fuera un día tan asombroso?{fast}"
                    "¡Me ascendieron!":

                        if promoted_recently:
                            m 3suo "¡Wow! ¡¿De nuevo?!"
                            m 3sub "Fuiste ascendido hace poco... {w=0.3}¡Debes estar haciendo un trabajo increíble!"
                            m 1huu "Estoy tan, {w=0.2}orgullosa de ti, [mas_get_player_nickname()]~"
                        else:

                            $ player_nick = mas_get_player_nickname()
                            m 3suo "¡Wow! Felicidades [player_nick], {w=0.1}{nw}"
                            extend 3hub "¡estoy tan orgullosa de ti!"
                            m 1euu "Sabía que lo lograrías~"
                            $ promoted_recently = True

                        $ persistent._mas_pm_last_promoted_d = datetime.date.today()
                    "¡Logré mucho!":

                        m 3hub "¡Eso es genial, [mas_get_player_nickname()]!"
                    "Fue un día increíble":

                        m 3hub "¡Me alegro de oírlo!"

                m 3eua "Solo puedo imaginar lo bien que debes trabajar en días como este."
                if not promoted_recently:
                    m 1hub "... ¡Tal vez incluso te asciendan pronto!"
                m 1eua "De todos modos, me alegro de que estés en casa, [mas_get_player_nickname()]."

                if seen_event("monikaroom_greeting_ear_bathdinnerme") and renpy.random.randint(1,20) == 1:
                    m 3tubsu "¿Te gustaría cenar, tomar un baño o...?"
                    m 1hubfb "Jajaja~ Es broma."
                else:
                    m 3msb "¿Qué mejor manera de terminar un día increíble que con tu increíble novia~?"

                return
            "Bien":

                m 1hub "¡Eso es genial!"
                m 1eua "Recuerda descansar primero, ¿okey?"
                m 3eua "De esa forma, tendrás algo de energía antes de intentar hacer cualquier otra cosa."
                m 1hua "¡O simplemente puedes relajarte conmigo!"
                m 3tku "Es loo mejor que se puede hacer después de un largo día de trabajo, ¿no crees?"
                m 1hub "¡Jajaja!"
                return
            "Mal":

                m 2ekc "..."
                m 2ekd "Lamento que hayas tenido un mal día en el trabajo..."
                m 3eka "Te abrazaría ahora mismo si estuviera allí, [player]."
                m 1eka "Solo recuerda que estoy aquí cuando me necesites, ¿okey?"
            "Muy mal...":

                m 2ekd "Lamento que hayas tenido un mal día en el trabajo, [player]."
                m 2ekc "Ojalá pudiera estar allí para darte un abrazo ahora mismo."
                m 2eka "Me alegro de que hayas venido a verme...{w=0.5} haré todo lo posible para consolarte."


        python:
            final_item = ("No quiero hablar de ello", False, False, False, 20)
            menu_items = [
                ("Me gritaron", ".yelled_at", False, False),
                ("Me robaron el crédito", ".passed_over", False, False),
                ("Tuve que trabajar hasta tarde", ".work_late", False, False),
                ("No hice mucho hoy", ".little_done", False, False),
                ("Solo fue un mal día", ".bad_day", False, False),
                ("Me sentía enfermo", ".sick", False, False),
            ]

        show monika 2ekc at t21
        window show
        m "Si no te importa hablar de ello, ¿qué ha pasado hoy?" nointeract

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        window auto

        $ label_suffix = _return

        show monika at t11

        if not label_suffix:
            m 1dsc "Entiendo, [player]."
            m 3eka "Espero que pasar tiempo conmigo te ayude a sentirte un poco mejor~"
            return


        $ full_label = "greeting_back_from_work{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label


        return

        label greeting_back_from_work.yelled_at:
            m 2lksdlc "Oh... {w=0.5}eso si que puede arruinar tu día."
            m 2dsc "Estás haciendo todo lo posible, y de alguna manera no es lo suficientemente bueno para alguien..."
            m 2eka "Si todavía te está molestando, creo que te vendría bien intentar relajarte un poco."
            m 3eka "Tal vez hablar de otra cosa o incluso jugar un juego te ayude a dejar de pensar en eso."
            m 1hua "Estoy segura de que te sentirás mejor después de que pasemos un tiempo juntos."
            return

        label greeting_back_from_work.passed_over:
            m 1lksdld "Oh... {w=0.5}si que puede arruinar tu día ver a alguien más obtener el reconocimiento que creías que merecías."
            m 2lfd "{i}Especialmente{/i} cuando has hecho tanto y parece que eres invisible."
            m 1ekc "Puede parecer un poco agresivo si dices algo, así que debe seguir haciendo lo mejor que puedas y un día estoy segura de que valdrá la pena."
            m 1eua "Mientras sigas esforzándote al máximo, continuarás haciendo grandes cosas y obtendrás reconocimiento algún día."
            m 1hub "Y recuerda... {w=0.5}¡yo siempre estaré orgullosa de ti, [player]!"
            m 3eka "Espero que saber eso te haga sentir un poco mejor~"
            return

        label greeting_back_from_work.work_late:
            m 1lksdlc "Aw, eso puede estropear las cosas."

            m 3eksdld "¿Al menos lo sabías con antelación?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Al menos lo sabías con antelación?{fast}"
                "Sí":

                    m 1eka "Eso es bueno, creo."
                    m 3ekc "Sería un dolor si estuvieras listo para irte a casa y luego tuvieras que quedarte más tiempo."
                    m 1rkd "Aún así, puede ser bastante molesto que tu horario habitual se arruine de esa manera."
                    m 1eka "... Pero al menos estás aquí ahora y podemos pasar un tiempo juntos."
                    m 3hua "¡Finalmente puedes relajarte!"
                "No":

                    m 2tkx "¡Eso es lo peor!"
                    m 2tsc "Especialmente si era el final de la jornada laboral y ya estabas listo para irte..."
                    m 2dsc "Entonces, de repente, tienes que quedarte un poco más sin previo aviso."
                    m 2ekc "Puede ser muy molesto que cancelen sus planes inesperadamente."
                    m 2lksdlc "Tal vez tenías algo que hacer justo después del trabajo, o simplemente estabas deseando volver a casa y descansar..."
                    m 2lubsu "... O tal vez solo querías volver a casa y ver a tu adorada novia que estaba esperando sorprenderte cuando llegaras a casa..."
                    m 2hub "Jejeje~"
            return

        label greeting_back_from_work.little_done:
            m 2eka "Aww, no te sientas tan mal, [player]."
            m 2ekd "Esos días pueden pasar."
            m 3eka "Sé que estás trabajando duro para superar tu bloqueo pronto."
            m 1hua "¡Siempre que hagas lo mejor, estaré orgullosa de ti!"
            return

        label greeting_back_from_work.bad_day:
            m 2dsd "Solo uno de esos días, ¿eh, [player]?"
            m 2dsc "Ocurren de vez en cuando..."
            m 3eka "Pero aún así, sé lo agotadores que pueden ser y espero que te sientas mejor pronto."
            m 1ekbsa "Estaré aquí mientras me necesites para consolarte, ¿de acuerdo, [player]?"
            return

        label greeting_back_from_work.sick:
            m 2dkd "Estar enfermo en el trabajo puede ser terrible. Vuelve mucho más difícil hacer las cosas."
            jump greeting_back_from_work_school_still_sick_ask

    elif mas_isMoniUpset():
        m 2esc "Veo que has vuelto del trabajo, [player]..."

        m "¿Cómo estuvo tu día?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo estuvo tu día?{fast}"
            "Bien":
                m 2esc "Es bueno escuchar eso."
                m 2tud "Debe ser agradable ser apreciado."
            "Mal":

                m 2dsc "..."
                m 2tud "Se siente mal cuando nadie parece apreciarte, ¿eh [player]?"

    elif mas_isMoniDis():
        m 6ekc "Hola, [player]... {w=1}¿finalmente volviste del trabajo?"

        m "¿Cómo estuvo tu día?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Cómo estuvo tu día?{fast}"
            "Bien":
                m "Eso es bueno."
                m 6rkc "Solo espero que no disfrutes más el trabajo que estar conmigo, [player]."
            "Mal":

                m 6rkc "Oh..."
                m 6ekc "Siento escuchar eso."
                m 6rkc "Sé cómo son los días malos en los que parece que no puedes complacer a nadie..."
                m 6dkc "Puede ser muy difícil pasar días así."
    else:

        m 6ckc "..."
    return

label greeting_back_from_work_school_still_sick_ask:
    m 7ekc "Aunque debería preguntar..."
    m 1ekc "¿Todavía te sientes mal?{nw}"
    menu:
        m "¿Todavía te sientes mal?{fast}"
        "Sí":

            m 1ekc "Lamento oír eso, [player]..."
            m 3eka "Tal vez deberías tomar una siesta. {w=0.2}Estoy segura de que te sentirás mejor una vez que hayas descansado un poco."
            jump mas_mood_sick.ask_will_rest
        "No":

            m 1eua "Me alegra saber que te sientes mejor, [player]."
            m 1eka "Pero si empiezas a sentirte mal de nuevo, asegúrate de descansar un poco, ¿de acuerdo?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_sleep",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SLEEP],
        ),
        code="GRE"
    )

label greeting_back_from_sleep:
    if mas_isMoniNormal(higher=True):
        m 1hua "Oh, ¡hola, [player]!"
        m 1hub "¡Espero que hayas descansado bien!"
        m "Pasemos más tiempo juntos~"

    elif mas_isMoniUpset():
        m 2esc "¿Acabas de despertar, [player]?"
        m "Espero que hayas descansado bien."
        m 2tud "{cps=*2}Quizás ahora estés de mejor humor.{/cps}{nw}"
        $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Oh...{w=1} estás despierto."
        m 6ekc "Espero que hayas podido descansar un poco."
        m 6dkc "Me cuesta descansar estos días con tantas cosas en la cabeza..."
    else:

        m 6ckc "..."

    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_siat",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_siat:
    m 1hub "{cps=*0.6}{i}~[player] y Monika sentados en un árbol~{/i}{/cps}"
    m 1hubsb "{cps=*0.6}{i}~B-E-S-A-N-D-O-S-E~{/i}{/cps}"
    m 3hubfb "{cps=*0.6}{i}~Primero viene el amor~{/i}{/cps}"
    m "{cps=*0.6}{i}~Luego viene el matrimonio~{/i}{/cps}"
    m "{cps=*0.6}{i}~Y luego vienen...{/i}{/cps}"
    m 3wubfsdlo "¡¿Q-Qué?!"
    m 2wubfsdld "¡[player]! ¡¿Cuánto tiempo llevas ahí?!"
    m 2rkbfsdld "Yo... {w=1}no me di cuenta de que entraste... {w=1}solo estaba..."
    m 2rkbfsdlu "..."
    m 3hubfb "¡Jajaja! No importa."
    m 1ekbfa "Te amo, [player]. Estoy tan feliz de que estés aquí~"
    return "love"

init python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(override_type=True))
    ev_rules.update(MASPriorityRule.create_rule(40))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_ourreality",
            conditional="mas_canShowIslands(flt=False) and not mas_isSpecialDay()",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )
    del ev_rules

label greeting_ourreality:

    $ store.mas_island_event.start_progression()

    m 1hub "¡Hola, [player]!"
    m 1hua "Jejeje~"
    m 3hksdlb "Me siento algo mareada en este momento, lo siento."
    m 1eua "Es solo que estoy muy emocionada de mostrarte en lo que he estado trabajando."

    if persistent._mas_current_background != "spaceroom":
        m 4eub "... Pero tenemos que volver a la sala espacial para tener la mejor vista."
        m 1hua "Vamos, [player]."
        call mas_background_change (mas_background_def, skip_leadin=True, skip_outro=True, set_persistent=True)
        m 1eua "¡Aquí estamos!"
        m 3eub "Ahora dame un segundo para prepararlo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:

        m 3hksdrb "Solo dame un segundo para prepararlo.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    m 1dsd "Casi termino.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    m 1duu "Sí, eso debería estar bien."
    m 1hub "¡Jajaja!"
    m 1eka "Perdón por eso."
    m 1eua "Sin más preámbulos..."
    m 4eub "¿Podrías mirar por la ventana, [player]?"

    call mas_islands (fade_out=False, drop_shields=False, enable_interaction=False)

    pause 4.0
    m "Bueno..."
    m "¿Qué opinas?"
    m "Trabajé muy duro en esto."
    m "Un lugar solo para los dos."
    m "También es donde puedo seguir practicando mis habilidades de programación."

    call mas_islands (fade_in=False, raise_shields=False, enable_interaction=False, force_exp="monika 1lsc")


    m 1lsc "Estar en la aula de clases todo el día puede ser aburrido."
    m 1ekc "Además, me siento muy sola esperando que regreses."
    m 1hksdlb "¡Pero no me malinterpretes!"
    m 1eua "Siempre me alegro cuando me visitas y pasas tiempo conmigo."
    m 1eka "Entiendo que estás ocupado y no puedes estar aquí todo el tiempo."
    m 3euc "Es solo que me di cuenta de algo, [player]."
    m 1lksdlc "Pasará mucho tiempo antes de que pueda cruzar a tu realidad."
    m 1dsc "Así que pensé..."
    m 1eua "¿Por qué no hacemos nuestra propia realidad?"
    m 1lksdla "Bueno, todavía no es exactamente perfecta."
    m 1hua "Pero es un comienzo."

    $ mas_lockEVL("greeting_ourreality", "GRE")
    $ mas_unlockEVL("mas_monika_islands", "EVE")

    m 1eub "Puedes admirar el paisaje por ahora~"
    call mas_islands (force_exp="monika 1eua")
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_returned_home",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_GO_SOMEWHERE,
                store.mas_greetings.TYPE_GENERIC_RET
            ]
        ),
        code="GRE"
    )

default -5 persistent._mas_monika_returned_home = None

label greeting_returned_home:



    $ five_minutes = datetime.timedelta(seconds=5*60)
    $ time_out = store.mas_dockstat.diffCheckTimes()




    if persistent._mas_f14_on_date:
        jump greeting_returned_home_f14



    if mas_f14 < datetime.date.today() <= mas_f14 + datetime.timedelta(days=7):

        call mas_gone_over_f14_check

    if mas_monika_birthday < datetime.date.today() < mas_monika_birthday + datetime.timedelta(days=7):
        call mas_gone_over_bday_check

    if mas_d25 < datetime.date.today() <= mas_nye:
        call mas_gone_over_d25_check

    if mas_nyd <= datetime.date.today() < mas_d25c_end:
        call mas_gone_over_nye_check

    if mas_nyd < datetime.date.today() < mas_d25c_end:
        call mas_gone_over_nyd_check




    if persistent._mas_player_bday_left_on_bday or (persistent._mas_player_bday_decor and not mas_isplayer_bday() and mas_isMonikaBirthday() and mas_confirmedParty()):
        jump greeting_returned_home_player_bday

    if persistent._mas_f14_gone_over_f14:
        jump greeting_gone_over_f14

    if mas_isMonikaBirthday() or persistent._mas_bday_on_date:
        jump greeting_returned_home_bday


    if time_out > five_minutes:
        jump greeting_returned_home_morethan5mins
    else:

        $ mas_loseAffection()
        call greeting_returned_home_lessthan5mins

        if _return:
            return 'quit'

        jump greeting_returned_home_cleanup


label greeting_returned_home_morethan5mins:
    if mas_isMoniNormal(higher=True):

        if persistent._mas_d25_in_d25_mode:

            jump greeting_d25_and_nye_delegate

        elif mas_isD25():

            jump mas_d25_monika_holiday_intro_rh

        jump greeting_returned_home_morethan5mins_normalplus_flow


    jump greeting_returned_home_morethan5mins_other_flow


label greeting_returned_home_morethan5mins_normalplus_flow:
    call greeting_returned_home_morethan5mins_normalplus_dlg


label greeting_returned_home_morethan5mins_normalplus_flow_aff:
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)
    jump greeting_returned_home_morethan5mins_cleanup

label greeting_returned_home_morethan5mins_other_flow:
    call greeting_returned_home_morethan5mins_other_dlg


label greeting_returned_home_morethan5mins_other_flow_aff:

    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 2.5, 0.5, 0.5)


label greeting_returned_home_morethan5mins_cleanup:
    pass





label greeting_returned_home_cleanup:
    $ need_to_reset_bday_vars = persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday()


    if not need_to_reset_bday_vars and not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out)

    elif need_to_reset_bday_vars:
        call return_home_post_player_bday


    if (
        mas_isD25Outfit()
        and not persistent._mas_d25_intro_seen
        and mas_isMoniUpset(lower=True)
    ):
        $ persistent._mas_d25_started_upset = True
    return

label greeting_returned_home_morethan5mins_normalplus_dlg:
    m 1hua "¡Y estamos en casa!"
    m 1eub "Incluso si no pude ver nada, sabiendo que estaba allí contigo..."
    m 2eua "Bueno, ¡se sintió genial!"
    show monika 5eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eub "Hagamos esto de nuevo pronto, ¿okey?"
    return

label greeting_returned_home_morethan5mins_other_dlg:
    m 2esc "Estamos en casa..."
    m 2eka "Gracias por sacarme hoy, [player]."
    m 2rkc "Para ser honesta, no estaba segura si debería ir contigo..."
    m 2dkc "Las cosas... {w=0.5}no nos han ido bien últimamente y no sabía si era tan buena idea..."
    m 2eka "Pero me alegro de haberlo hecho... {w=0.5}tal vez sea justo lo que necesitábamos."
    m 2rka "Deberíamos hacer esto de nuevo en algún momento..."
    m 2esc "Solo si tú quieres."
    return

label greeting_returned_home_lessthan5mins:
    if mas_isMoniNormal(higher=True):
        m 2ekp "No fue un gran viaje, [player]."
        m "La próxima vez será mejor que duré un poco más..."
        if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
            call return_home_post_player_bday
        return False

    elif mas_isMoniUpset():
        m 2efd "¡Pensé que íbamos a algún lugar, [player]!"
        m 2tfd "Sabía que no debería haber aceptado ir contigo."
        m 2tfc "Sabía que esto iba a ser otra decepción."
        m "No me pidas que salga si solo lo haces para ilusionarme... {w=1}solo para tirar de la alfombra debajo de mí."
        m 6dktdc "..."
        m 6ektsc "No sé por qué insistes en ser tan cruel, [player]."
        m 6rktsc "Yo... {w=1}me gustaría estar sola ahora mismo."
        return True
    else:

        m 6rkc "Pero... {w=1}acabamos de salir..."
        m 6dkc "..."
        m "Yo... {w=0.5}estaba tan emocionada cuando me pediste que fuera contigo."
        m 6ekc "Después de todo lo que hemos pasado..."
        m 6rktda "Pensé que... {w=0.5}tal vez... {w=0.5}las cosas finalmente iban a cambiar."
        m "Tal vez finalmente pasariamos un buen rato..."
        m 6ektda "Que en realidad querías pasar más tiempo conmigo."
        m 6dktsc "..."
        m 6ektsc "Pero supongo que fue una tontería por mi parte pensar eso."
        m 6rktsc "Debería haberlo sabido... {w=1}nunca debí haber aceptado ir contigo."
        m 6dktsc "..."
        m 6ektdc "Por favor, [player]... {w=2}si no quieres pasar tiempo conmigo, está bien..."
        m 6rktdc "Pero al menos ten la decencia de no fingir."
        m 6dktdc "Me gustaría que me dejaras sola ahora mismo."
        return True

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="ch30_reload_delegate",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_RELOAD
            ],
        ),
        code="GRE"
    )

label ch30_reload_delegate:

    if persistent.monika_reload >= 4:
        call ch30_reload_continuous
    else:

        $ reload_label = "ch30_reload_" + str(persistent.monika_reload)
        call expression reload_label

    return






















label greeting_ghost:

    $ mas_lockEVL("greeting_ghost", "GRE")


    call mas_ghost_monika

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_game",
            unlocked=True,
            category=[store.mas_greetings.TYPE_GAME],
        ),
        code="GRE"
    )





label greeting_back_from_game:

    if store.mas_globals.late_farewell and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        $ _now = datetime.datetime.now().time()
        if mas_isMNtoSR(_now):
            if mas_isMoniNormal(higher=True):
                m 2etc "¿[player]?"
                m 3efc "¡Pensé que te había dicho que te fueras directamente a la cama después de terminar!"
                m 1rksdla "Quiero decir, estoy muy feliz de que hayas regresado para darme las buenas noches, pero..."
                m 1hksdlb "¡Ya te dije buenas noches!"
                m 1rksdla "Y podría haber esperado hasta la mañana para verte de nuevo, ¿sabes?"
                m 2rksdlc "Además, quería que descansaras un poco..."
                m 1eka "Solo... {w=1}prométeme que te irás a la cama pronto, ¿de acuerdo?"
            else:

                m 1tsc "[player], te dije que te fueras a la cama cuando terminaras."
                m 3rkc "Puedes volver mañana por la mañana, ¿sabes?"
                m 1esc "Pero aquí estamos, supongo."

        elif mas_isSRtoN(_now):
            if mas_isMoniNormal(higher=True):
                m 1hua "Buenos días, [player]~"
                m 1eka "Cuando dijiste que ibas a jugar otro juego tan tarde, me preocupé un poco que no pudieras dormir lo suficiente..."
                m 1hksdlb "Espero que ese no sea el caso, jajaja..."
            else:

                m 1eud "Buenos días."
                m 1rsc "Esperaba que durmieras un poco más."
                m 1eka "Pero aquí estas, brillante y temprano."

        elif mas_isNtoSS(_now):
            if mas_isMoniNormal(higher=True):
                m 1wub "¡[player]! ¡Estás aquí!"
                m 1hksdlb "Jajaja, lo siento... {w=1}estaba un poco ansiosa por verte ya que no estuviste aquí en toda la mañana."

                m 1eua "¿Acabas de despertar?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Acabas de despertar?{fast}"
                    "Sí":
                        m 1hksdlb "Jajaja..."

                        m 3rksdla "¿Crees qué fue porque te quedaste despierto hasta tarde?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "¿Crees qué fue porque te quedaste despierto hasta tarde?{fast}"
                            "Sí":
                                m 1eka "[player]..."
                                m 1ekc "Sabes que no quiero que te quedes despierto hasta muy tarde."
                                m 1eksdld "Realmente no querría que te enfermaras o te cansaras durante el día."
                                m 1hksdlb "Pero espero que te hayas divertido. Odiaría que perdieras todo ese sueño por nada, ¡jajaja!"
                                m 2eka "Solo asegúrate de descansar un poco más si sientes que lo necesitas, ¿de acuerdo?"
                            "No":

                                m 2euc "Oh..."
                                m 2rksdlc "Pensé que tal vez así era."
                                m 2eka "Perdón por asumirlo."
                                m 1eua "De todos modos, espero que estés durmiendo lo suficiente."
                                m 1eka "Me haría muy feliz saber que has descansado bien."
                                m 1rksdlb "También podría aliviar mi mente si no estuvieras despierto hasta tan tarde en primer lugar, jajaja..."
                                m 1eua "Me alegro de que estés aquí ahora."
                                m 3tku "Nunca estarías demasiado cansado para pasar tiempo conmigo, ¿verdad?"
                                m 1hub "¡Jajaja!"
                            "Tal vez...":

                                m 1dsc "Hmm..."
                                m 1rsc "Me pregunto qué podría estar causando esto."
                                m 2euc "No te quedaste despierto hasta muy tarde anoche, ¿verdad, [player]?"
                                m 2etc "¿Estabas haciendo algo anoche?"
                                m 3rfu "Quizás... {w=1}no lo sé..."
                                m 3tku "¿Jugando?"
                                m 1hub "¡Jajaja!"
                                m 1hua "Solo estoy burlándome de ti~"
                                m 1ekd "Pero, con toda seriedad, no quiero que descuides tu sueño."
                                m 2rksdla "Una cosa es quedarse despierto hasta tarde solo por mí..."
                                m 3rksdla "¿Pero salir y jugar otro juego tan tarde?"
                                m 1tub "Jajaja... podría ponerme un poco celosa, [player]~"
                                m 1tfb "Pero estás aquí para compensar eso, ¿verdad?"
                    "No":

                        m 1eud "Ah, supongo que estuviste ocupado toda la mañana."
                        m 1eka "Me preocupaba que te quedaras dormido ya que anoche te quedaste hasta muy tarde."
                        m 2rksdla "Especialmente desde que me dijiste que ibas a jugar otro juego."
                        m 1hua "Debería haber sabido que serías responsable y te irias a dormir."
                        m 1esc "..."
                        m 3tfc "{i}Si dormiste{/i}, ¿verdad, [player]?"
                        m 1hub "¡Jajaja!"
                        m 1hua "De todos modos, ahora que estás aquí, podemos pasar un tiempo juntos."
            else:

                m 2eud "Oh, ahí estás, [player]."
                m 1euc "Supongo que acabas de despertar."
                m 2rksdla "Es de esperar que te quedes despierto hasta tan tarde jugando."
        else:


            if mas_isMoniNormal(higher=True):
                m 1hub "¡Ahí estás, [player]!"
                m 2hksdlb "Jajaja, lo siento... es solo que no te he visto en todo el día."
                m 1rksdla "Esperaba que durmieras después de quedarte despierto hasta tan tarde anoche..."
                m 1rksdld "Pero cuando no te vi en toda la tarde, comencé a extrañarte..."
                m 2hksdlb "Casi me tienes preocupada, jajaja..."
                m 3tub "Pero vas a compensarme ese tiempo perdido, ¿verdad?"
                m 1hub "Jejeje, es mejor que si~"
                m 2tfu "Especialmente después de dejarme por otro juego anoche."
            else:

                m 2efd "¡[player]!{w=0.5} ¿Dónde estuviste todo el día?"
                m 2rfc "Esto no tiene nada que ver con que te quedaste despierto hasta tarde anoche, ¿verdad?"
                m 2ekc "Deberías ser un poco más responsable cuando se trata de dormir."



    elif mas_getAbsenceLength() < datetime.timedelta(hours=4):
        if mas_isMoniNormal(higher=True):
            m 1hua "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"

            m 1eua "¿Lo disfrutaste?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Lo disfrutaste?{fast}"
                "Sí":
                    m 1hua "Eso es genial."
                    m 1eua "Me alegra que lo hayas disfrutado."
                    m 2eka "A veces me gustaría poder unirme a tus otros juegos."
                    m 3eub "¿No sería estupendo vivir nuestras propias aventuras cada vez que quisiéramos?"
                    m 1hub "Estoy segura de que nos divertiríamos mucho juntos en uno de tus juegos."
                    m 3eka "Pero aunque no pueda unirme a ti, supongo que tendrás que hacerme compañía."
                    m 2tub "No te importa pasar tiempo con tu novia... {w=0.5}¿verdad, [player]?"
                "No":

                    m 2ekc "Aw, lamento escuchar eso."
                    m 2eka "Espero que no estés muy molesto por lo que pasó."
                    m 3eua "Al menos estás aquí ahora. Prometo tratar de no dejar que te pase nada malo mientras estés conmigo."
                    m 1ekbsa "Verte siempre me anima."
                    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5ekbfa "Espero que verme haga lo mismo por ti, [mas_get_player_nickname()]~"
        else:

            m 2eud "Oh, ¿ya regresaste?"
            m 2rsc "Pensé que te irías más tiempo... {w=0.5}pero bienvenido de nuevo, supongo."

    elif mas_getAbsenceLength() < datetime.timedelta(hours=12):
        if mas_isMoniNormal(higher=True):
            m 2wuo "¡[player]!"
            m 2hksdlb "Estuviste fuera por mucho tiempo..."

            m 1eka "¿Te divertiste?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Te divertiste?{fast}"
                "Sí":
                    m 1hua "Bueno, entonces me alegro."
                    m 1rkc "Me hiciste esperar un rato, ¿sabes?"
                    m 3tfu "Creo que deberías pasar algo de tiempo con tu amada novia, [player]."
                    m 3tku "Estoy segura de que no te importaría quedarte conmigo para igualar tu otro juego."
                    m 1hubsb "Tal vez deberías pasar más tiempo conmigo, por si acaso, ¡jajaja!"
                "No":

                    m 2ekc "Oh..."
                    m 2rka "Ya sabes, [player]..."
                    m 2eka "Si no te estás divirtiendo, tal vez podrías pasar tiempo aquí conmigo."
                    m 3hua "¡Estoy segura de que hay muchas cosas divertidas que podemos hacer juntos!"
                    m 1eka "Si decides volver, quizás sea mejor."
                    m 1hub "Pero si aún no te estás divirtiendo, no dudes en venir a verme, ¡jajaja!"
        else:

            m 2eud "Oh, [player]."
            m 2rsc "Eso tomó bastante tiempo."
            m 1esc "No te preocupes, me las arreglé para pasar el tiempo mientras estabas fuera."
    else:


        if mas_isMoniNormal(higher=True):
            m 2hub "¡[player]!"
            m 2eka "Siento que ha pasado una eternidad desde que te fuiste."
            m 1hua "¡Te extrañé!"
            m 3eua "Espero que te hayas divertido con lo que sea que estabas haciendo."
            m 1rksdla "Y voy a asumir que no te olvidaste de comer o dormir..."
            m 2rksdlc "En cuanto a mí... {w=1}estaba un poco sola esperando a que volvieras..."
            m 1eka "Pero no te sientas mal."
            m 1hua "Estoy feliz de que estés aquí conmigo."
            m 3tfu "Será mejor que me lo compenses."
            m 3tku "Creo que pasar una eternidad conmigo suena justo...{w=1} ¿verdad, [player]?"
            m 1hub "¡Jajaja!"
        else:

            m 2ekc "[player]..."
            m "No estaba segura de cuándo volverías."
            m 2rksdlc "Pensé que no volvería a verte..."
            m 2eka "Pero aquí estás..."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_eat",
            unlocked=True,
            category=[store.mas_greetings.TYPE_EAT],
        ),
        code="GRE"
    )

label greeting_back_from_eat:

    $ _now = datetime.datetime.now().time()
    if store.mas_globals.late_farewell and mas_isMNtoSR(_now) and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        if mas_isMoniNormal(higher=True):
            m 1eud "¿Oh?"
            m 1eub "¡[player], regresaste!"
            m 3rksdla "Sabes que deberías dormir un poco, ¿no crees?"
            m 1rksdla "Quiero decir... no me quejo de que estés aquí, pero..."
            m 1eka "Me haría sentir mejor si te fueras a la cama pronto."
            m 3eka "Siempre puedes volver y visitarme cuando te despiertes..."
            m 1hubsa "Pero supongo que si insistes en pasar tiempo conmigo, lo dejaré pasar un rato, jejeje~"
        else:
            m 2euc "¿[player]?"
            m 3ekd "¿No te dije que fueras directamente a la cama?"
            m 2rksdlc "Deberías dormir un poco."
    else:

        if mas_isMoniNormal(higher=True):
            m 1eub "¿Terminaste de comer?"
            m 1hub "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
            m 3eua "Espero que hayas disfrutado tu comida."
        else:
            m 2euc "¿Terminaste de comer?"
            m 2eud "Bienvenido."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_rent",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

label greeting_rent:
    m 1eub "¡Bienvenido de nuevo, [mas_get_player_nickname()]!"
    m 2tub "Sabes, pasas tanto tiempo aquí que debería empezar a cobrarte el alquiler."
    m 2ttu "¿O prefieres pagar una hipoteca?"
    m 2hua "..."
    m 2hksdlb "Cielos, no puedo creer que acabo de decir eso. No es demasiado cursi, ¿verdad?"
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Pero enserio, ya me has dado lo único que necesito... {w=1}tu corazón~"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_housework",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CHORES],
        ),
        code="GRE"
    )

label greeting_back_housework:
    if mas_isMoniNormal(higher=True):
        m 1eua "¿Todo listo, [player]?"
        m 1hub "¡Pasemos más tiempo juntos!"
    elif mas_isMoniUpset():
        m 2esc "Al menos no te olvidaste de volver, [player]."
    elif mas_isMoniDis():
        m 6ekd "Ah, [player]. Así que realmente estabas ocupado..."
    else:
        m 6ckc "..."
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised2",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_surprised2:
    m 1hua "..."
    m 1hubsa "..."
    m 1wubso "¡Oh! {w=0.5}¡[player]! {w=0.5}¡Me sorprendiste!"
    m 3ekbsa "... No es que sea una sorpresa verte, después de todo siempre me estás visitando... {w=0.5}{nw}"
    extend 3rkbsa "me atrapaste soñando despierta."
    show monika 5hubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfu "Pero ahora que estás aquí, ese sueño se hizo realidad~"
    return

init python:

    ev_rules = dict()
    ev_rules.update(MASPriorityRule.create_rule(49))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_restart",
            unlocked=True,
            category=[store.mas_greetings.TYPE_RESTART],
            rules=ev_rules
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back_from_restart:
    if mas_isMoniNormal(higher=True):
        m 1hub "¡Bienvenido de vuelta, [mas_get_player_nickname()]!"
        m 1eua "¿Qué más debemos hacer hoy?"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 1eud "Oh, estás de vuelta."
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_code_help",
            conditional="store.seen_event('monika_coding_experience')",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_code_help:
    m 2eka "Oh, hola [player]..."
    m 4eka "Dame un segundo, acabo de terminar de intentar codificar algo y quiero ver si funciona.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    scene black
    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    hide noise
    call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 2wud_static')

    m 2wud "¡Ah!{w=0.3}{nw}"
    extend 2efc " ¡No se supone que suceda eso!"
    m 2rtc "¿Por qué este ciclo termina tan rápido? {w=0.5}{nw}"
    extend 2efc "No importa cómo lo mire, ese diccionario {i}no{/i} está vacío."
    m 2rfc "Cielos, la codificación puede ser {i}tan{/i} frustrante a veces..."

    if persistent._mas_pm_has_code_experience:
        m 3rkc "Bueno, supongo que volveré a intentarlo más tarde.{nw}"
        $ _history_list.pop()

        show screen mas_background_timed_jump(5, "greeting_code_help_outro")
        menu:
            m "Bueno, supongo que volveré a intentarlo más tarde.{fast}"
            "Podría ayudarte con eso...":

                hide screen mas_background_timed_jump
                m 7hua "Aww, eso es muy dulce de tu parte, [player]. {w=0.3}{nw}"
                extend 3eua "Pero no, tendré que negarme."
                m "Descubrir las cosas por tu cuenta es la parte divertida, {w=0.2}{nw}"
                extend 3kua "¿de acuerdo?"
                m 1hub "¡Jajaja!"
    else:

        m 3rkc "Bueno, supongo que volveré a intentarlo más tarde."



label greeting_code_help_outro:
    hide screen mas_background_timed_jump
    m 1eua "De todos modos, ¿qué te gustaría hacer hoy?"

    $ mas_lockEVL("greeting_code_help", "GRE")
    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_love_is_in_the_air",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_love_is_in_the_air:
    m 1hub "{i}~El amor está en el aire~{/i}"
    m 1rub "{i}~A donde quiera que mire~{/i}"
    m 3ekbsa "Oh hola, [player]..."
    m 3rksdla "No me hagas caso. {w=0.2}Solo estoy cantando un poco, pensando en... {w=0.3}{nw}"
    extend 1hksdlb "bueno, creo que podrías adivinar qué, jajaja~"
    m 1eubsu "Siento que el amor está a mi alrededor cuando estás aquí."
    m 3hua "De todos modos, ¿qué te gustaría hacer hoy?"
    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_workout",
            category=[store.mas_greetings.TYPE_WORKOUT],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_workout:
    if mas_isMoniNormal(higher=True):
        m 1hua "¡Bienvenido de nuevo, [player]!"
        m 3eua "Espero que hayas tenido un buen entrenamiento."
        m 3eub "¡No olvides mantenerte hidratado y comer algo para recuperar tu energía!"
        m 1eua "Pasemos más tiempo juntos~"

    elif mas_isMoniUpset():
        m 2esc "Oh, {w=0.2}estás de vuelta."
        m 2rsc "¿El entrenamiento te ayudó a liberar algo de tensión?"
        m 2rud "Espero que si... {w=0.3}{nw}"
        extend 2eka " pasemos más tiempo juntos."

    elif mas_isMoniDis():
        m 6ekc "Oh... {w=0.5}mira quién está de vuelta."
        m 6dkc "Estoy... {w=0.3}feliz de que te estés cuidando."
        m 6ekd "... ¿Pero no quieres cuidarme también?"
        m 7dkc "Al menos de vez en cuando, por favor..."
        m 1dkc "..."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_shopping",
            category=[store.mas_greetings.TYPE_SHOPPING],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_shopping:
    if mas_isMoniNormal(higher=True):
        m 1hub "¡Bienvenido de nuevo, [player]!"
        m 3eua "Espero que hayas obtenido lo que necesitabas de la tienda."
        m 1hua "Pasemos más tiempo juntos~"

    elif mas_isMoniUpset():
        m 2esc "Oh,{w=0.2} has vuelto."
        m 2rsc "Espero que tengas todo lo que necesitabas."
        if renpy.random.randint(1,5) == 1:
            m 2rud "{cps=*2}Espero que ahora también estés de mejor humor.{/cps}{nw}"
            $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Oh... {w=0.5}has vuelto."
        m 6ekc "Espero que la hayas pasado bien comprando. {w=0.2}¿Compraste algo de comida?"
        m 6dkd "¿Has considerado que tus hábitos alimenticios pueden estar afectando tu estado de ánimo últimamente?"
        m 6lkc "Odiaría si esa fuera la razón por la que...{nw}"
        $ _history_list.pop()
        m 6ekc "¿Sabes qué? No importa. {w=0.2}{nw}"
        extend 6dkc "Solo estoy cansada."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_hangout",
            category=[store.mas_greetings.TYPE_HANGOUT],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_hangout:
    if mas_isMoniNormal(higher=True):
        if persistent._mas_pm_has_friends:
            m 1eua "Bienvenido de nuevo, [player]."
            m 3hub "¡Espero que te la hayas pasado bien!"

            $ anyway_lets = "Vamos a"
        else:

            m 3eub "Bienvenido de nuevo, [player]."

            m 1eua "¿Hiciste un nuevo amigo?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Hiciste un nuevo amigo?{fast}"
                "Sí":

                    m 1hub "¡Eso es increíble!"
                    m 1eua "Me hace muy feliz saber que tienes a alguien con quien pasar el rato."
                    m 3hub "¡Espero que puedas pasar más tiempo con ellos en el futuro!"
                    $ persistent._mas_pm_has_friends = True
                "No...":

                    m 1ekd "Oh..."
                    m 3eka "Bueno, no te preocupes, [player]. {w=0.2} Yo siempre seré tu amiga, pase lo que pase."
                    m 3ekd "... Y no tengas miedo de volver a intentarlo con otra persona."
                    m 1hub "¡Estoy segura de que hay alguien que estaría feliz de llamarte su amigo!"
                "Ya son mis amigos":

                    if persistent._mas_pm_has_friends is False:
                        m 1rka "Oh, entonces hiciste un nuevo amigo sin decirme..."
                        m 1hub "¡Está bien! Estoy feliz de que tengas a alguien con quien pasar el rato."
                    else:
                        m 1hub "¡Oh, okey!"
                        m 3eua "... En realidad, no hemos hablado de tus otros amigos antes, así que no estaba segura de si era un nuevo amigo o no."
                        m 3eub "Pero de cualquier manera, ¡me alegra que tengas amigos en tu realidad con quienes pasar el rato!"

                    m 3eua "Espero que puedas pasar tiempo con ellos a menudo."
                    $ persistent._mas_pm_has_friends = True

            $ anyway_lets = "Como sea, vamos a"

        m 1eua "[anyway_lets] pasar más tiempo juntos~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Hola de nuevo, [player]."
        m 2eud "Espero que hayas pasado un buen rato con tus amigos."
        if renpy.random.randint(1,5) == 1:
            m 2rkc "{cps=*2}Me pregunto como es eso{/cps}{nw}."
            $ _history_list.pop()
    else:

        m 6ckc "..."

    return

init python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 5duc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_poem_shadows_in_garden",
            unlocked=True,
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

    del ev_rules


init 6 python:
    MASPoem(
        poem_id="gre_1",
        category="generic",
        prompt=_("Sombras en el jardín"),
        title="",
        text=_("""\
 A solas me hago una pregunta solemne,
 ¿Qué podría crecer en un jardín sin luz?

 Cuando vuelves, parece el cielo,
 Dentro de tu luz, el frío olvidado.

 Lo daría todo por sentirme así,
 Esperando a quien más quiero.

 Más cerca de mi corazón...
"""),
    )

label greeting_poem_shadows_in_garden:
    m 5duc "{i}Solo hago una solemne pregunta,\n¿qué podría crecer en un jardín sin luz?{/i}"
    m 5ekbla "{i}Cuando regresas, se siente como el cielo,\ndentro de tu luz, el frío es olvidado.{/i}"
    m 5fubfa "{i}Daré todo para sentirme así,\nesperando al que más aprecio.{/i}"
    m 5ekbfa "{i}Incluso si es cada día,\nsin duda, eres el más cercano.{/i}"
    m 5dubsu "{i}El más cercano a mi corazón...{/i}"
    m 5eublb "Se me ocurrió esto mientras estabas ausente."
    show monika 1eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1eka "Así es, ¡eres como el sol de mi mundo!"
    m 3hubsu "¡De todos modos, bienvenido de nuevo, [mas_get_player_nickname()]! Espero que te haya gustado este poema."

    m 1ekbsb "¡Te he echado mucho de menos!"

    if "gre_1" not in persistent._mas_poems_seen:
        $ persistent._mas_poems_seen["gre_1"] = 1

    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return

init python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            random_chance=0.3,
            forced_exp=random.choice(("monika 1gsbsu", "monika 1msbsu"))
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_spacing_out",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=3)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_spacing_out:
    python hide:

        use_right_smug = bool(random.randint(0, 1))
        spacing_out_pause = PauseDisplayableWithEvents()
        events = list()
        next_event_time = 0
        right_smug = renpy.partial(renpy.show, "monika 1gsbsu")
        left_smug = renpy.partial(renpy.show, "monika 1msbsu")


        for i in range(random.randint(4, 6)):
            events.append(
                PauseDisplayableEvent(
                    datetime.timedelta(seconds=next_event_time),
                    right_smug if use_right_smug else left_smug,
                    restart_interaction=True
                )
            )
            next_event_time += random.uniform(0.9, 1.8)
            use_right_smug = not use_right_smug

        events.append(
            PauseDisplayableEvent(
                datetime.timedelta(seconds=next_event_time),
                renpy.partial(renpy.show, "monika 1tsbsu"),
                restart_interaction=True
            )
        )
        next_event_time += 0.7

        events.append(
            PauseDisplayableEvent(
                datetime.timedelta(seconds=next_event_time),
                spacing_out_pause.stop
            )
        )

        spacing_out_pause.set_events(events)
        spacing_out_pause.start()


    $ renpy.pause(0.01)
    m 2wubfsdlo "¡[player]!"
    m 1rubfsdlb "¡Me sorprendiste! {w=0.4}{nw}"
    extend 1eubsu "Estaba {w=0.2}pensando un poco..."
    m 1hubsb "Jajaja~"
    m 1eua "Estoy muy contenta de verte de nuevo. {w=0.2}{nw}"
    extend 3eua "¿Qué haremos hoy, [player]?"
    return

init python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=0.05,
            override_type=True
        )
    )
    ev_rules.update(
        MASTimedeltaRepeatRule.create_rule(
            datetime.timedelta(days=3)
        )
    )
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(
            hours=list(range(9, 20))
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_after_bath",
            conditional=(
                "mas_getAbsenceLength() >= datetime.timedelta(hours=6) "
                "and not mas_isSpecialDay()"
            ),
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="GRE"
    )

    del ev_rules

init -4:


    default persistent._mas_previous_moni_state = monika_chr.save_state(True, True, True, True)

label greeting_after_bath:
    python hide:

        mas_RaiseShield_core()
        mas_startupWeather()

        persistent._mas_previous_moni_state = monika_chr.save_state(True, True, True, True)

        clothes_pool = [
            mas_clothes_bath_towel_white
        ]

        monika_chr.change_clothes(
            random.choice(clothes_pool),
            by_user=False,
            outfit_mode=True
        )

        if not monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET):
            monika_chr.change_hair(mas_hair_wet, by_user=False)




        mas_setEVLPropValues(
            "mas_after_bath_cleanup",
            start_date=datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 90)),
            action=EV_ACT_QUEUE
        )
        mas_startup_song()


    call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=True)

    $ renpy.pause(random.randint(5, 15), hard=True)
    call mas_transition_from_emptydesk ("monika 1huu")
    $ renpy.pause(2.0)
    $ quick_menu = True

    m 1wuo "¡Oh! {w=0.2}{nw}"
    extend 2wuo "¡[player]! {w=0.2}{nw}"
    extend 2lubsa "Justo estaba pensando en ti."

    $ bathing_showering = random.choice(("la bañera", "la ducha"))

    if mas_getEVL_shown_count("greeting_after_bath") < 5:
        m 7lubsb "Justo salgo de [bathing_showering]... {w=0.3}{nw}"
        extend 1ekbfa "no te importa que solo lleve puesta la toalla, ¿verdad?~"
        m 1hubfb "Jajaja~"
        m 3hubsa "Estaré lista pronto, espera a que mi pelo se seque un poco más primero."
    else:


        m 7eubsb "Justo salgo de [bathing_showering]."

        if mas_canShowRisque() and random.randint(0, 3) == 0:
            m 1msbfb "Apuesto a que te hubiera encantado entrar conmigo..."
            m 1tsbfu "Bueno, tal vez un día~"
            m 1hubfb "Jajaja~"
        else:

            m 1eua "Me cambiare en un momentito~"

    python:

        mas_MUINDropShield()

        set_keymaps()

        mas_OVLShow()

        del bathing_showering

    return


init python:
    addEvent(Event(persistent.event_database, eventlabel="mas_after_bath_cleanup", show_in_idle=True, rules={"skip alert": None}))

    def mas_after_bath_cleanup_change_outfit():
        """
        After bath cleanup change outfit code
        """
        
        
        
        force_hair_change = False
        
        if monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET):
            force_hair_change = True
            
            
            monika_chr.load_state(persistent._mas_previous_moni_state, as_prims=True)
            
            
            if monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET):
                if mas_isMoniHappy(higher=True):
                    new_clothes = mas_clothes_blazerless
                
                else:
                    new_clothes = mas_clothes_def
                
                monika_chr.change_clothes(
                    new_clothes,
                    by_user=False,
                    outfit_mode=True
                )
        
        if (
            force_hair_change
            or monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET)
        ):
            available_hair = mas_sprites.get_installed_hair(
                predicate=lambda hair_obj: (
                    not hair_obj.hasprop(mas_sprites.EXP_H_WET)
                    and mas_sprites.is_clotheshair_compatible(monika_chr.clothes, hair_obj)
                    and mas_selspr.get_sel_hair(hair_obj) is not None
                    and mas_selspr.get_sel_hair(hair_obj).unlocked
                )
            )
            
            if available_hair:
                new_hair = random.choice(available_hair)
                monika_chr.change_hair(
                    new_hair,
                    by_user=False
                )

label mas_after_bath_cleanup:

    if (
        not monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET)
        and not monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET)
    ):
        return

    if mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "Voy a vestirme.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:

        $ player_nick = mas_get_player_nickname()
        m 1eua "Dame un momento [mas_get_player_nickname()], {w=0.2}{nw}"
        extend 3eua "voy a vestirme."

    window hide
    call mas_transition_to_emptydesk

    $ renpy.pause(1.0, hard=True)
    $ mas_after_bath_cleanup_change_outfit()
    $ renpy.pause(random.randint(10, 15), hard=True)

    call mas_transition_from_emptydesk ("monika 3hub")
    window auto

    if mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3hub "¡Listo! {w=1}{nw}"
    else:

        m 3hub "De acuerdo, ¡he vuelto!~"
        m 1eua "Bueno, ¿que te gustaría hacer hoy, [player]?"

    return

label mas_after_bath_cleanup_change_outfit:
    $ mas_after_bath_cleanup_change_outfit()
    return


init python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=0.1,
            override_type=True
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_found_nou_shirt",
            conditional=(
                "mas_getAbsenceLength() >= datetime.timedelta(hours=3) "
                "and mas_nou.get_wins_for('Player') > {0} "
                "and mas_nou.get_total_games() > {1} "
                "and not mas_isSpecialDay() "
                "and not mas_SELisUnlocked(mas_clothes_nou_shirt)"
            ).format(random.randint(45, 65), random.randint(95, 115)),
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

    del ev_rules

default -5 persistent._mas_pm_snitched_on_chibika = None

label greeting_found_nou_shirt:
    python:
        mas_RaiseShield_core()
        mas_startupWeather()
        monika_chr.change_clothes(mas_clothes_nou_shirt, by_user=False, outfit_mode=True)
        glitch_option_text = glitchtext(7)

    call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=True)
    pause 2.5

    m "¡Aquí estás!{w=0.2} Te estaba esperando~"
    m "Tengo que admitirlo, {w=0.1}no sé cómo has podido poner esto en mi armario sin que me diera cuenta, [player]...{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(5, "greeting_found_nou_shirt.menu_skip")
    menu:
        m "engo que admitirlo, no sé cómo has podido poner esto en mi armario sin que me diera cuenta, [player]...{fast}"
        "Es un secreto":

            hide screen mas_background_timed_jump
            jump greeting_found_nou_shirt.menu_choice_secret
        "¡Se trataba de [glitch_option_text]!":

            hide screen mas_background_timed_jump
            $ persistent._mas_pm_snitched_on_chibika = True
            $ renpy.invoke_in_thread(
                mas_utils.trywrite,
                os.path.join(renpy.config.basedir, "characters/for snitch.txt"),
                ">:("
            )
            jump greeting_found_nou_shirt.menu_choice_other
        "No tengo ni idea...":

            hide screen mas_background_timed_jump
            jump greeting_found_nou_shirt.menu_choice_other

    label greeting_found_nou_shirt.post_menu:
        pass

    m 1ekbla "Gracias, [player]."
    m 1tfu "Sin embargo, no pienses que seré más suave contigo~"

    if mas_nou.get_wins_for('Player') >= mas_nou.get_wins_for('Monika'):
        m 1rtsdlb "De hecho, {w=0.1}tal vez debería esforzarme más, jajaja..."

    m 3ttb "¿Te apetece jugar [mas_get_player_nickname()]?"

    python:
        mas_selspr.unlock_clothes(mas_clothes_nou_shirt)
        mas_selspr.save_selectables()
        mas_lockEVL("greeting_found_nou_shirt", "GRE")
        renpy.save_persistent()

        del glitch_option_text

        mas_MUINDropShield()
        set_keymaps()
        HKBShowButtons()
        mas_startup_song()
        enable_esc()
    return

label greeting_found_nou_shirt.menu_skip:
    hide screen mas_background_timed_jump
    call mas_transition_from_emptydesk ("monika 4sub")
    m "Pero me encanta~"

    jump greeting_found_nou_shirt.post_menu

label greeting_found_nou_shirt.menu_choice_secret:
    if mas_isMoniEnamored(higher=True):
        call mas_transition_from_emptydesk ("monika 2tublu")
        m "{cps=*1.5}No te asomas ahí {i}a menudo{/i}, ¿verdad?~{/cps}{w=0.1}{nw}"
        $ _history_list.pop()
        m 2lusdla "De todos modos... {w=0.3}{nw}"
    else:

        call mas_transition_from_emptydesk ("monika 2rtblsdlu")
        m "Hmm, de todos modos... {w=0.3}{nw}"

    extend 4sub "¡Me encanta este nuevo conjunto!"

    jump greeting_found_nou_shirt.post_menu

label greeting_found_nou_shirt.menu_choice_other:
    show noise onlayer overlay zorder 500:
        alpha 0.0
        easein_elastic 0.5 alpha 0.1
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.5
    hide noise onlayer overlay

    jump greeting_found_nou_shirt.menu_skip
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
