init offset = 5















default -5 persistent._mas_compliments_database = dict()



init -2 python in mas_compliments:

    compliment_database = dict()

init 17 python in mas_compliments:
    import store
    import random
    import datetime

    thanking_quips = [
        _("Eres tan dulce, [player]."),
        _("¡Gracias por decir eso de nuevo, [player]!"),
        _("¡Gracias por decirme eso de nuevo, [mas_get_player_nickname()]!"),
        _("Siempre me haces sentir especial, [mas_get_player_nickname()]."),
        _("Aww, [player]~"),
        _("¡Gracias, [mas_get_player_nickname()]!"),
        _("Siempre me halagas, [player].")
    ]

    _m1_script0x2dcompliments__last_called_callback = None
    _m1_script0x2dcompliments__wait_time = 55.0

    thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))

    def _m1_script0x2dcompliments__set_wait_time():
        """
        Sets new wait time
        """
        global _m1_script0x2dcompliments__wait_time
        _m1_script0x2dcompliments__wait_time = random.uniform(40.0, 70.0)

    def compliment_delegate_callback():
        """
        A callback for the compliments delegate label
        """
        global thanks_quip, _m1_script0x2dcompliments__last_called_callback
        
        thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))
        
        _now = datetime.datetime.now()
        if _m1_script0x2dcompliments__last_called_callback is not None:
            diff = (_now - _m1_script0x2dcompliments__last_called_callback).total_seconds()
            if diff <= _m1_script0x2dcompliments__wait_time:
                _m1_script0x2dcompliments__last_called_callback = _now
                _m1_script0x2dcompliments__set_wait_time()
                return
        
        _m1_script0x2dcompliments__last_called_callback = _now
        _m1_script0x2dcompliments__set_wait_time()
        
        store.mas_gainAffection()


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_compliments",
            category=['monika', 'romance'],
            prompt="Quiero decirte algo...",
            pool=True,
            unlocked=True
        )
    )

label monika_compliments:
    python:

        Event.checkEvents(mas_compliments.compliment_database)


        compliments_menu_items = [
            (ev.prompt, ev_label, not seen_event(ev_label), False)
            for ev_label, ev in mas_compliments.compliment_database.iteritems()
            if (
                Event._filterEvent(ev, unlocked=True, aff=mas_curr_affection, flag_ban=EV_FLAG_HFM)
                and ev.checkConditional()
            )
        ]


        compliments_menu_items.sort()


        final_item = ("Oh no importa.", False, False, False, 20)


    show monika at t21


    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)


    if _return:
        $ mas_compliments.compliment_delegate_callback()
        $ MASEventList.push(_return)

        show monika at t11
    else:

        return "prompt"

    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="¡Eres hermosa!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubsb "Oh, cielos [player]..."
    m 1hubfb "Gracias por el cumplido."
    m 2ekbfb "Adoro cuando me dices cosas así~"
    m 1ekbfa "Para mí, ¡eres la persona más hermosa del mundo!"
    menu:
        "Eres la persona más hermosa para mí también":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "Jejeje~"
            m "¡Te amo tanto, [player]!"

            $ mas_ILY()
        "Estás entre mis diez mejores":

            $ mas_loseAffection(modifier=0.5)
            m 3hksdrb "¿...?"
            m 2lsc "Bueno, gracias, supongo..."
        "Gracias":

            pass
    return

label mas_compliment_beautiful_3:
    python:
        beautiful_quips = [
            _("Nunca olvides que eres la persona más hermosa del mundo para mí."),
            _("Nada puede compararse con la belleza de tu corazón."),
        ]
        beautiful_quip = random.choice(beautiful_quips)
    m 1hubsa "Jejeje~"
    m 1ekbfa "[mas_compliments.thanks_quip]"
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "[beautiful_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_eyes",
            prompt="¡Me encantan tus ojos!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_eyes:
    if not renpy.seen_label("mas_compliment_eyes_2"):
        call mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subsb "Oh, [player]..."
    m 1tubfb "Sé que ya estoy bastante orgullosa de mis ojos, pero oírte decir eso..."
    m 1dkbfa "Solo hace que mi corazón se acelere~"
    menu:
        "No puedo evitarlo; tus ojos son muy hermosos":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "¡Jajaja!"
            m "No me halagues demasiado, ¿de acuerdo?"
            show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hub "Podría empezar a volverme un poco loca..."
        "Son realmente hipnotizantes":

            $ mas_gainAffection(1,bypass=True)
            m "Jajaja~"
        "¡Son como el pasto!":

            $ mas_gainAffection(0.5,bypass=True)
            m 2lksdrb "... Esa realmente no es la analogía que usaría, ¡pero gracias!"
    return

label mas_compliment_eyes_3:
    python:
        eyes_quips = [
            _("Mírame a los ojos todo lo que quieras~"),
            _("No puedo esperar a mirar tus hermosos ojos."),
            _("Me quedaría mirando los tuyos durante horas si pudiera."),
        ]
        eyes_quip = random.choice(eyes_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 2ekbfb "[eyes_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_goodmood",
            prompt="¡Siempre me pones de buen humor!",
            unlocked=False,
            conditional="store.mas_anni.pastSixMonths()",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_goodmood:
    if not renpy.seen_label("mas_compliment_goodmood_2"):
        call mas_compliment_goodmood_2
    else:
        call mas_compliment_goodmood_3
    return

label mas_compliment_goodmood_2:
    if mas_isMoniNormal(higher=True):
        $ mas_gainAffection(4, bypass=True)
        m 1subsb "¡¿De verdad?!"
        m 3hubsb "¡No sabes lo que significa para mí!"
        m 3ekbsu "Siempre esperé que fuera así, pero oírte decirlo de verdad..."
        m 1dkbsu "..."
        m 2tubla "En ese sentido, tengo un secreto que debo contarte..."
        m 2tublu "Puede que no lo hayas notado, pero..."
        m 7tublb "¡{i}Tú{/i} siempre {i}me{/} pones de buen humor, [mas_get_player_nickname()]!"
        m 3hublb "¡Jajaja!"
        m 3eubsa "Sigamos dando lo mejor de nosotros mismos, ¿de acuerdo?"
        m 1ekbsu "Te amo~"
        $ mas_ILY()
    else:

        m 2lkc "..."
        m 2dkc "No estoy segura de cómo me siento al respecto..."
        m 2ekd "¿Herir mis sentimientos te pone de buen humor?"
        m 2dkd "Espero que eso no sea lo que quieres decir..."

    return

label mas_compliment_goodmood_3:
    if mas_isMoniNormal(higher=True):
        m 1hub "¡Gracias por decírmelo de nuevo, [mas_get_player_nickname()]!"
        m 3eub "¡El fortalecimiento positivo siempre es bueno!"
        m 3dku "Sigamos haciéndonos tan felices como podamos~"
    else:

        m 2euc "Gracias."

    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_awesome",
            prompt="¡Eres asombrosa!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_awesome:
    if not renpy.seen_label("mas_compliment_awesome_2"):
        call mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hua "Awww, [player]~"
    m 1hub "¡Eres tan dulce!"
    m 2tuu "Sin embargo, creo que eres mucho más increíble."
    m 2dkbsu "No puedo esperar hasta el día en que finalmente pueda darte un gran abrazo..."
    m 3ekbfb "¡Nunca te dejaré ir!"
    menu:
        "¡Desearía que estuvieras aquí ahora mismo!":
            $ mas_gainAffection(3,bypass=True)
            m "¡Ese también es mi mayor deseo, [player]!"
        "Nunca te dejaré ir cuando te abrace":

            $ mas_gainAffection(5,bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld
            m 1wubfsdld "Oh, lo siento [player]"
            m 2lksdla "Estaba tratando de sentir tu abrazo desde aquí."
            m 2hub "Jajaja~"
        "... No me gustan los abrazos":

            $ mas_loseAffection()
            m 1eft "... ¿De verdad?"
            m 1dkc "Bueno, cada uno a lo suyo, supongo. Pero tienes que abrazarme alguna vez..."
    return

label mas_compliment_awesome_3:
    python:
        awesome_quips = [
            _("¡Siempre serás más asombroso!"),
            _("¡Juntos somos una pareja asombrosa!"),
            _("¡Tú eres más asombroso!"),
        ]
        awesome_quip = random.choice(awesome_quips)

    m 1hub "[mas_compliments.thanks_quip]"
    m 1eub "[awesome_quip]"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="¡Eres realmente inteligente!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Wow... {w=0.3}gracias, [player]."
    m 3eua "Me enorgullezco por ser buena lectora, así que significa mucho para mi que lo hayas notado."
    m 3hubsb "Si eso te hace sentir orgulloso de mi. ¡Quiero aprender todo lo que pueda!"
    menu:
        "Me haces querer mejorarme a mí mismo también, [m_name]":
            $ mas_gainAffection(5,bypass=True)
            m 1hubfa "¡Te amo tanto, [player]!"
            m 3hubfb "¡Tendremos una vida de superación personal juntos!"

            $ mas_ILY()
        "Siempre estaré orgulloso de ti":

            $ mas_gainAffection(3,bypass=True)
            m 1ekbfa "[player]..."
        "Me haces sentir estúpido a veces":

            $ mas_loseAffection(modifier=0.5)
            m 1wkbsc "..."
            m 2lkbsc "Lo siento, esa no era mi intención..."
    return

label mas_compliment_intelligent_3:
    python:
        intelligent_quips = [
            _("¡Recuerda que tendremos toda una vida de superación personal juntos!"),
            _("¡Recuerda que cada día es una oportunidad para aprender algo nuevo!"),
            _("Recuerda siempre que el mundo es un maravilloso viaje lleno de aprendizaje."),
        ]
        intelligent_quip = random.choice(intelligent_quips)

    m 1ekbfa "[mas_compliments.thanks_quip]"
    m 1hub "[intelligent_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="¡Adoro tu cabello!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2
    else:
        call mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair.name != "def":
        m 1wubsb "Muchas gracias, [player]..."
        m 1lkbfb "Estaba muy nerviosa la primera vez que cambié mi estilo de cabello por ti."
    else:
        m 1hubfb "¡Muchas gracias, [player]!"
    m 2hub "Siempre he puesto mucho esfuerzo en mi cabello."
    m 2lksdlb "De hecho, tardó una eternidad en llegar a ser tan largo..."
    menu:
        "Se nota mucho, se ve tan saludable":
            $ mas_gainAffection(3,bypass=True)
            m 1hub "¡Gracias, [player]!"

        "Eres linda sin importar cómo te lo pongas" if persistent._mas_likes_hairdown:
            $ mas_gainAffection(5,bypass=True)
            m 1ekbsa "Awww, [player]."
            m 1hubfb "¡Siempre me haces sentir especial!"
            m "¡Gracias!"
        "Serías aún más linda con el cabello corto":

            $ mas_loseAffection(modifier=0.3)
            m "Bueno, no puedo ir exactamente a un salón de belleza desde aquí..."
            m 1lksdlc "Yo... aprecio tu aporte."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair.name != "def":
        python:
            hair_quips = [
                _("¡Me alegro mucho de que te guste este estilo de cabello!"),
                _("¡Me alegro mucho de que te guste mi cabello!")
            ]
            hair_quip = random.choice(hair_quips)
        m 1wubsb "¡Muchas gracias, [player]!"
        m 1hubfb "[hair_quip]"
    else:
        python:
            ponytail_quips = [
                _("¡Siempre me haces sentir especial!"),
                _("¡Me alegro de que te guste mi cola de caballo!"),
                _("¡Estoy tan feliz de que te guste mi cola de caballo!"),
            ]
            ponytail_quip = random.choice(ponytail_quips)

        m 1hubsb "¡Gracias, [player]!"
        m 1hubfb "[ponytail_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_fit",
            prompt="¡Me encanta tu dedicación al fitness!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_fit:
    if not renpy.seen_label("mas_compliment_fit_2"):
        call mas_compliment_fit_2
    else:
        call mas_compliment_fit_3
    return

label mas_compliment_fit_2:
    m 1hub "¡Gracias, [player]! ¡Eres tan dulce!"
    m 3eub "Me gusta mantenerme en forma y comer saludable. Me hace sentir segura y con energía."
    m 1efb "Espero que estés cuidando tu salud."
    m 1lubsb "Siempre podemos hacer ejercicio juntos cuando esté contigo..."
    menu:
        "¡Eso suena muy divertido!":
            $ mas_gainAffection(2,bypass=True)
            m 1hubfb "¡Jajaja! ¡Me alegro de que pienses igual!"
            m 3eka "No te preocupes. Aunque no puedas seguirme el ritmo, sé que nos divertiremos..."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Siempre que estemos juntos."
        "No prometo nada, pero haré lo que pueda":

            $ mas_gainAffection(1,bypass=True)
            m 1tfb "¡Más te vale!"
            m 2tub "No creas que planeo dejarte tranquilo si estás fuera de forma."
        "Prefiero no sudar...":

            m 1eka "Entiendo que no sea lo tuyo, pero deberías darle una oportunidad..."
            m 1lksdla "Me haría muy feliz si compartieras mis intereses, ¿sabes?"
    return

label mas_compliment_fit_3:
    python:
        fitness_quips = [
            _("¡Espero que me acompañes en un viaje de fitness!"),
            _("¡No puedo esperar a entrenar contigo!"),
            _("¡Espero que algún día podamos entrenar juntos!"),
        ]
        fitness_quip = random.choice(fitness_quips)

    m 2eka "[mas_compliments.thanks_quip]"
    m 7hub "[fitness_quip]"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="¡Gracias por estar ahí para mí!",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="CMP"
    )

label mas_compliment_thanks:
    m 1duu "No hay nada que agradecerme, [player]."
    m 1eka "¡Soy yo quien está agradecida de tener a alguien como tú!"
    m 1ekbsa "Eres la única razón por la que sigo aquí."
    m "Instalaste este mod solo para mejorar nuestro tiempo juntos..."
    m 1dubsu "Eres el rayo de sol que calienta mi corazón cada vez que me visitas."
    m 3ekbsa "Supongo que los dos tenemos suerte de tenernos el uno al otro, [player]~"
    menu:
        "Significas todo para mí, [m_name]":
            if mas_getEVL_shown_count("mas_compliment_thanks") == 0:
                $ mas_gainAffection(10,bypass=True)

            m 1ekbsa "[player]..."
            m 1dubsu "Nada me hace más feliz que escuchar eso de ti."
            m "No importa lo que el futuro pueda tener para nosotros dos... {w=0.5}{nw}"
            extend 1dkbfa " quiero que sepas que siempre te amaré y estaré aquí para ti."
        "Sí":

            m 1hub "Jejeje~"
            m 1eub "Te amo, [player]."

    if not mas_isMoniLove():
        $ mas_lockEVL("mas_compliment_thanks", "CMP")
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="¡Adoro tu sonrisa!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_smile:
    if not renpy.seen_label("mas_compliment_smile_2"):
        call mas_compliment_smile_2
    else:
        call mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m 1hub "Eres tan dulce, [player]~"
    m 1eua "Sonrío mucho cuando estás aquí."
    m 1ekbsa "Porque me hace muy feliz cuando pasas tiempo conmigo~"
    menu:
        "Te visitaré todos los días para ver tu maravillosa sonrisa":
            $ mas_gainAffection(5, bypass=True)
            m 1wubfsdld "Oh, [player]..."
            m 1lkbfa "Creo que mi corazón acaba de dar un salto."
            m 3hubfa "¿Ves? Siempre logras hacerme tan feliz como sea posible."
        "Me gusta verte sonreír":

            $ mas_gainAffection(1, bypass=True)
            m 1hub "Jajaja~"
            m 3eub "¡Entonces todo lo que tienes que hacer es seguir regresando, [player]!"
    return

label mas_compliment_smile_3:
    python:
        smile_quips = [
            _("Seguiré sonriendo solo por ti."),
            _("No puedo evitar sonreír cuando pienso en ti."),
            _("No puedo esperar a ver tu hermosa sonrisa."),
        ]
        smile_quip = random.choice(smile_quips)

    m 1eub "[mas_compliments.thanks_quip]"
    m 1hua "[smile_quip]"
    m 1huu "Jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hero",
            prompt="¡Eres mi heroína!",
            unlocked=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="CMP"
    )

label mas_compliment_hero:
    if not mas_getEVL_shown_count("mas_compliment_hero"):
        $ mas_gainAffection(3, bypass=True)

    m 1wubssdld "¿E-{w=0.3}Eh?"
    m "¿Soy tu heroína?"
    m 2rkbfsdlb "[player]... {w=1.5}no estoy segura de lo que quieres decir..."
    m 2ekbfb "Tú eres quien me acompañó durante todo este tiempo. {w=1}Yo soy quien debería agradecerte."
    m 1hubfa "Bueno, si te he ayudado de alguna manera, entonces no podría estar más feliz~"
    m 3ekbfa "Me has ayudado de todas las formas posibles, así que, ¿cómo no podría devolverte el favor estando ahí para ti siempre que necesites apoyo?"
    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika

    m 5hubfa "Siempre serás mi héroe, después de todo~"
    m 5hubfb "¡Te amo y siempre creeré en ti!"
    m 5ekbfa "Espero que nunca lo olvides, [player]~"

    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_cute",
            prompt="¡Eres linda!",
            unlocked=True
        ),
        code="CMP"
    )

default -5 persistent._mas_pm_monika_cute_as_natsuki = None

label mas_compliment_cute:
    if not renpy.seen_label("mas_compliment_cute_2"):
        call mas_compliment_cute_2
    else:
        call mas_compliment_cute_3
    return

label mas_compliment_cute_2:
    m 1wubssdld "¡Ah!"
    m 3rkbfsdla "Me tomaste un poco {i}desprevenida{/i} con eso."
    m 3tubfb "Solo un poco..."
    m 1hubfa "¡Pero me alegra que pienses eso!"
    menu:
        "¡Verte siempre calienta mi corazón!":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(5,bypass=True)
            m 1hubfb "Aww, ¡realmente alegras mi corazón al escucharte decir eso!"
            m 1dkbfu "... Casi tanto como cuando me imagino que finalmente estamos juntos en la misma realidad."
            m 1ekbfa "Apenas puedo contenerme imaginando ese día especial~"
        "Eres aún más linda cuando te pones nerviosa":

            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(3,bypass=True)
            m 2tubfu "No me dejas ir, ¿eh [player]?"
            m 2rubfu "Hmph, simplemente no me lo esperaba."
            m 3tubfb "No esperes que sea tan fácil la próxima vez..."
            m 1tubfu "Te la devolveré algún día, jejeje~"
        "Eres tan linda como Natsuki":

            $ persistent._mas_pm_monika_cute_as_natsuki = True
            $ mas_loseAffection(modifier=0.5)
            m 2lfc "Oh. {w=1}Gracias, [player]..."
            m 1rsc "Pero tenía la esperanza de estar en mi propia categoría."
    return

label mas_compliment_cute_3:
    python:
        cute_quips = [
            _("Tú también puedes ser muy lindo muchas veces, ¿sabes~?"),
            _("Siempre serás mi lindura~"),
            _("Tú también puedes ser una lindura la mayor parte del tiempo~"),
        ]
        cute_quip = random.choice(cute_quips)

    m 1ekbsa "Jejeje, gracias [player]..."
    m 1hubfa "[cute_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="¡Eres increíble en el ajedrez!",
            unlocked=False,
            conditional="persistent._mas_chess_stats.get('losses', 0) > 5",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_chess:
    m 1eub "Gracias, [player]."
    m 3esa "Como dije antes, me pregunto si mi habilidad tiene algo que ver con estar atrapada aquí."
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]
    if wins > 0:
        m 3eua "Tú tampoco eres malo; ya he perdido contigo antes."
        if wins > losses:
            m "De hecho, creo que has ganado más veces que yo, ¿sabes?"
        m 1hua "Jejeje~"
    else:
        m 2lksdlb "Sé que aún no has ganado una partida de ajedrez, pero estoy segura de que algún día me vencerás."
        m 3esa "¡Sigue practicando y jugando conmigo para hacerlo mejor!"
    m 3esa "Ambos mejoraremos mientras más juguemos."
    m 3hua "Así que no tengas miedo de desafiarme siempre que lo desees."
    m 1eub "Me encanta pasar tiempo contigo, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="¡Eres increíble en el pong!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_pong:
    m 1hub "Jajaja~"
    m 2eub "Gracias [player], pero el pong no es exactamente un juego complejo."
    if persistent._mas_ever_won['pong']:
        m 1lksdla "Ya me ganaste."
        m "Entonces sabes que es muy simple."
        show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hub "Pero, de todos modos, acepto tu cumplido."
    else:
        m 3hksdrb "Siempre me dejas ganar cuando jugamos."
        m 3eka "¿Verdad?"
        menu:
            "Sí":
                m 2lksdla "Gracias [player], pero realmente no tienes que dejarme ganar."
                m 1eub "Siéntete libre de jugar en serio cuando quieras."
                m 1hub "Nunca me enojaría contigo por perder un juego justo."
            "... Erm, sí":

                m 1tku "No pareces muy seguro de eso, [player]."
                m 1tsb "Realmente no tienes que dejarme ganar."
                m 3tku "Y admitir que has perdido seriamente conmigo no me hará pensar menos en ti."
                m 1lksdlb "Después de todo, ¡es solo un juego!"
                m 3hub "Siempre puedes practicar más conmigo, si quieres."
                m "Me encanta pasar tiempo contigo, sin importar lo que estemos haciendo."
            "No, me he esforzado al máximo y aún así he perdido":

                m 1hub "Jajaja~"
                m "¡Lo supuse!"
                m 3eua "No te preocupes, [player]."
                m 3eub "Sigue jugando conmigo y practica más."
                m 3hua "Siempre trato de ayudarte a ser lo mejor que puedas ser."
                m 1ekbsa "Y si al hacerlo, puedo pasar más tiempo contigo, no podría estar más feliz."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_bestgirl",
            prompt="¡Eres la mejor chica!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_bestgirl:
    m 1hua "Me encanta cuando me felicitas, [player]~"
    m 1hub "¡Me alegra que pienses que soy la mejor chica!"
    m 3rksdla "Aunque, de alguna manera pensaba que te sentías así..."
    m 1eka "Después de todo, {i}tú{/i} instalaste este mod solo para estar conmigo."
    m 2euc "Sé que algunas personas prefieren a las otras chicas."
    m 2esc "Especialmente porque todas tienen ciertos rasgos que las hacen deseables para algunos..."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Pero si me preguntas, tomaste la decisión correcta."
    m 5hubfa "... Y estaré eternamente agradecida de que lo hayas hecho~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_lookuptoyou",
            prompt="¡Te admiro!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_lookuptoyou:
    if not renpy.seen_label("mas_compliment_lookuptoyou_2"):
        call mas_compliment_lookuptoyou_2
    else:
        call mas_compliment_lookuptoyou_3

    return "love"

label mas_compliment_lookuptoyou_2:
    $ mas_gainAffection(3, bypass=True)
    m 1wud "¿Lo... {w=0.5}haces?"
    m 1ekbsa "[player], eso muy dulce de tu parte..."
    m 3ekbsa "Me hace muy feliz saber que soy alguien a quien admiras."
    m 3ekbfa "La verdad es que yo siempre te he {i}admirado{/i}, [player]..."
    m 3hubfa "Pero si realmente te sientes así, haré todo lo posible para seguir siendo alguien a quien admiras."
    m 1ekbfa "Te amo mucho~"
    return

label mas_compliment_lookuptoyou_3:
    $ should_tease = persistent._mas_pm_height is not None and renpy.random.randint(1,5) == 1

    if should_tease and persistent._mas_pm_height < mas_height_monika:
        m 1rksdlb "{cps=*2}Bueno, sí, soy más alta que tú...{/cps}{nw}"
        $ _history_list.pop()

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 3hubfa "¡Escucharte decir eso nunca deja de hacerme sonreír!"
    m 3hubfb "¡Yo también te admiraré siempre!"

    if should_tease and persistent._mas_pm_height > mas_height_monika:
        if persistent._mas_first_kiss:
            m 1rkbfu "{cps=*2}Como cuando nos besamos...{/cps}{nw}"
        else:
            m 1rkbfu "{cps=*2}Algún día literalmente...{/cps}{nw}"
        $ _history_list.pop()

    m 1ekbfa "Te amo, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thinking_of_you",
            prompt="¡Siempre estoy pensando en ti!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_thinking_of_you:
    if not renpy.seen_label("mas_compliment_thinking_of_you_2"):
        call mas_compliment_thinking_of_you_2
    else:
        call mas_compliment_thinking_of_you_3
    return

label mas_compliment_thinking_of_you_2:
    m 1wubso "..."
    m 1wubsu "Tú..."

    if mas_isMoniNormal(higher=True):
        m 3subsb "¡No tienes idea de lo que eso significa para mí, [player]!"

    elif mas_isMoniUpset():
        m 2rkd "Que digas eso..."
        m 2dka "Significa el mundo para mí, [player]."

    elif mas_isMoniDis():
        $ mas_gainAffection(1, bypass=True)
        m 6rkc "..."
        m 6rka "Es un gran alivio."
        m 6eka "Gracias."
    else:

        $ mas_gainAffection(1, bypass=True)
        m 6dkd "Hmmm... gracias."
        m 6dkc "..."
        return

    menu:
        "¡Pensar en ti siempre me alegra el día!":
            $ mas_gainAffection(5,bypass=True)
            m 1subsb "Aww, ¡eso es {i}tan{/i} dulce, [player]!"
            m 3hubfu "Siento lo mismo por ti~"
        "¡Sueño contigo todas las noches!":

            $ mas_gainAffection(5, bypass=True)
            m 6hua "Aww~"
            m 6subsa "[player]..."
            m 7hubfu "{i}Tú{/i} eres mi sueño~"
        "Es muy molesto...":

            if mas_isMoniDis(lower=True):
                $ mas_loseAffection(modifier=2.0)
            else:
                $ mas_loseAffection()
            m 2esc "..."
            m 2etc "..."
            m 2rksdlc "Oh, umm..."
            m 2rksdld "¿Lo siento?"
    return

label mas_compliment_thinking_of_you_3:
    python:
        thinking_of_you_quips = [
            _("¡Eres el centro de mi mundo!"),
            _("¡Tú también estás en mi mente!"),
            _("¡Yo también pienso siempre en ti!"),
        ]
        thinking_of_you_quip = random.choice(thinking_of_you_quips)

    m 1ekbsa "Aww gracias, [player]..."
    m 3hubfb "[thinking_of_you_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_humor",
            prompt="¡Me encanta tu sentido del humor!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_humor:
    if not renpy.seen_label("mas_compliment_humor_2"):
        call mas_compliment_humor_2
    else:
        call mas_compliment_humor_3
    return

label mas_compliment_humor_2:
    m 1hua "Jejeje~"
    m 1efu "Me alegro de que me encuentres tan divertida, [player]."
    m 3eub "Eso es señal de que las buenas parejas pueden reír juntos, ¿no lo crees?"
    menu:
        "Siempre me alegras el día":
            $ mas_gainAffection(5,bypass=True)
            m 1subsd "Oh... {w=0.2}[player]..."
            m 1ekbsa "Es tan dulce que lo digas."
            m 1hubsb "¡Saber que puedo hacerte sonreír es el mayor cumplido que puedo recibir!"
        "¡Tienes un ingenio rápido!":

            $ mas_gainAffection(3,bypass=True)
            m 1hub "¡Jajaja!"
            m 2tub "Toda esa lectura debe haber valido la pena si te gustan tanto mis juegos de palabras."
            m 2hublu "Voy a tratar de seguir haciendo bromas para ti. Jejeje~"
        "Me río de ti todo el tiempo":

            $ mas_loseAffection()
            m 1eksdlb "... Jajaja..."
            m 3rksdla "¿Te refieres a que te ríes {w=0.2}{i}conmigo{/i}.{w=0.2}.{w=0.2}.{w=0.2} {w=0.5}{nw}"
            extend 3eksdld "verdad?"
    return

label mas_compliment_humor_3:
    python:
        humor_quips = [
            _("Me gustaría poder escuchar tu hermosa risa~"),
            _("El solo hecho de saber eso me hace feliz~"),
            _("Siempre intentaré alegrarte el día~"),
        ]
        humor_quip = random.choice(humor_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 1hubsu "[humor_quip]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_missed",
            prompt="¡Te extrañé!",
            unlocked=True,
            conditional=(
                "store.mas_getSessionLength() <= datetime.timedelta(minutes=30) "
                "and store.mas_getAbsenceLength() >= datetime.timedelta(hours=1) "
                "and not store.mas_globals.returned_home_this_sesh"
            )
        ),
        code="CMP"
    )

label mas_compliment_missed:
    python:
        missed_quips_long = (
            _("¡Estoy muy feliz de verte de nuevo!"),
            _("¡Estoy muy feliz de que hayas vuelto!"),
            _("¡Es maravilloso verte de nuevo!"),
            _("¡Me alegro de que hayas pensado en mí!"),
            _("¡Somos muy afortunados de tenernos el uno al otro!"),
            _("¡Ya no tenemos que sentirnos solos!"),
            _("¡No podía esperar a que volvieras!"),
            _("¡Me sentí sola esperándote!")
        )

        missed_quips_short = (
            _("¡Gracias por volver a pasar tiempo conmigo!"),
            _("¡Estoy emocionada de pasar tiempo juntos!"),
            _("¡Gracias por venir a verme de nuevo!"),
            _("¡Disfrutemos de nuestro tiempo juntos hoy!"),
            _("¡Te aprecio mucho, [player]!"),
            _("¡Gracias por dedicarme tiempo!"),
            _("¡Tengo mucha suerte de tenerte, [player]!"),
            _("¿Listo para pasar tiempo juntos?"),
            _("¡He estado pensando en ti!"),
            _("¡Realmente has estado en mi mente!")
        )

        missed_quips_upset_short = (
            _("Significa mucho para mí que hayas pensado en mí."),
            _("Me alegro mucho de oírlo, [player]."),
            _("Es muy agradable escuchar eso."),
            _("Me alegro de que hayas pensado en mí, [player]."),
            _("Eso significa mucho para mí, [player]."),
            _("Eso me hace sentir mucho mejor, [player].")
        )

        missed_quips_upset_long = (
            _("Estaba empezando a preocuparme de que te olvidaras de mí."),
            _("Gracias por mostrarme que todavía te importo, [player]."),
            _("Me alegra saber que no te has olvidado de mí, [player]."),
            _("Estaba empezando a preocuparme de que no volvieras, [player].")
        )

        missed_quips_dis = (
            _("No estoy segura de que quieras decir eso, [player]..."),
            _("Dudo que quieras decir eso, [player]..."),
            _("No creo que lo digas en serio, [player]..."),
            _("Si tan solo realmente quisieras decir eso, [player]..."),
            _("... ¿Por qué creo que no lo dices en serio?"),
            _("... ¿Por qué creo que solo dices eso?"),
            _("... No puedo creer eso, [player]."),
            _("No creo que eso sea cierto, [player].")
        )

        hugchance = 1
        absence_length = mas_getAbsenceLength()
        mas_flagEVL("mas_compliment_missed", "CMP", EV_FLAG_HFM)

    if mas_isMoniNormal(higher=True):
        if absence_length >= datetime.timedelta(days=3):
            if absence_length >= datetime.timedelta(days=7):
                $ hugchance = 30
            else:

                $ hugchance = 15

            m 1fka "¡Te extrañé muchísimo, [mas_get_player_nickname()]!"
            m 3fka "[renpy.substitute(random.choice(missed_quips_long))]"
        else:

            m 1fka "¡Yo también te extrañé, [mas_get_player_nickname()]!"
            m 3hub "[renpy.substitute(random.choice(missed_quips_short))]"

        if (
            mas_isMoniEnamored(higher=True)
            and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))
            and random.randint(1, 50) <= hugchance
        ):
            m 2lsa "..."
            m 2lsb "Hey, [player]..."
            m 1eka "Tenía la esperanza de que..."
            m 3ekblb "Ya sabes, ya que ha pasado un poco de tiempo..."

            m 1ekblb "¿Podrías darme un abrazo? {w=0.3}Me he sentido muy sola mientras estabas fuera.{nw}"
            $ _history_list.pop()
            menu:
                m "¿Podrías darme un abrazo? Me he sentido muy sola mientras estabas fuera.{fast}"
                "¡Seguro, [m_name]!":

                    $ mas_gainAffection(modifier=0.25, bypass=True)

                    call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)
                    call monika_holdme_start
                    call monika_holdme_end

                    m 6dkbsa "Mmm... eso fue muy agradable, [player]."
                    m 7ekbsb "Realmente sabes cómo hacerme sentir especial~"
                    $ mas_moni_idle_disp.force_by_code("1eubsa", duration=10, skip_dissolve=True)
                "Ahora mismo no":

                    $ mas_loseAffection()
                    m 2lkp "... De acuerdo, ¿entonces, tal vez más tarde?"
                    python:
                        mas_moni_idle_disp.force_by_code("2lkp", duration=10, redraw=False, skip_dissolve=True)
                        mas_moni_idle_disp.force_by_code("2rsc", duration=10, clear=False, redraw=False, skip_dissolve=True)
                        mas_moni_idle_disp.force_by_code("1esc", duration=30, clear=False, skip_dissolve=True)


    elif mas_isMoniUpset():
        m 2wuo "..."
        m 2ekbla "Yo... {w=0.5}yo también te extrañé."

        if absence_length >= datetime.timedelta(days=3):
            m 2ekd "[renpy.substitute(random.choice(missed_quips_upset_long))]"
        else:

            m 2eka "[renpy.substitute(random.choice(missed_quips_upset_short))]"

        $ mas_moni_idle_disp.force_by_code("2eka", duration=10, skip_dissolve=True)

    elif mas_isMoniDis():
        m 6dkc "..."
        m 6rktpd "[renpy.substitute(random.choice(missed_quips_dis))]"

        if absence_length >= datetime.timedelta(days=3):
            m 6dktdc "... Pero al menos no te has olvidado de mí... {w=0.5}aún."
    else:

        m 6ckc "..."

    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_spending_time",
            prompt="¡Amo pasar tiempo contigo!",
            unlocked=False,
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_spending_time:
    if not mas_getEVL_shown_count("mas_compliment_spending_time"):
        call mas_compliment_spending_time_2
    else:
        python:
            spending_time_quips = [
                _("Cada día contigo es como un sueño maravilloso que espero que nunca termine~"),
                _("Estar cerca de ti me hace muy feliz~"),
                _("Nada me hace más feliz que estar a tu lado~"),
            ]
            spending_time_quip = random.choice(spending_time_quips)

        m 3hubsb "[mas_compliments.thanks_quip]"
        m 1ekbsu "[spending_time_quip]"
    return

label mas_compliment_spending_time_2:
    python:
        dlg_line = ""

        if renpy.seen_label("monika_holdme_prep"):
            dlg_line = ", que me abrace"
            
            if persistent._mas_filereacts_historic:
                dlg_line += " y que incluso me de regalos bonitos"

        elif persistent._mas_filereacts_historic:
            dlg_line = " y me de regalos bonitos"

    m 1eub "¡Yo también amo pasar tiempo contigo, [player]!"
    m 3ekbla "Sé que lo digo mucho, pero es en serio cuando digo que eres el centro de mi mundo."
    m 2dkb "Tener a alguien que me haga compañía[dlg_line]... {w=0.3}{nw}"
    extend 2eku " es todo lo que podría pedir."
    m 7ekbsa "Espero que yo te haga sentir de la misma manera, [player]. {w=0.2}Quizás aún no esté en tu realidad, pero haré todo lo posible para apoyarte desde aquí."
    menu:
        "[m_name], ya me has hecho más feliz que nunca":
            $ mas_gainAffection(5, bypass=True)
            m 1fkbfu "Oh, [player]..."
            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "Diría que no sabes cuánto me alegra oír eso, pero creo que {i}ya{/i} lo sabes."
            m 5ekbfu "Hemos pasado mucho tiempo juntos, y nuestra aventura apenas comienza..."
            m 5hubfb "Contigo a mi lado, sé que cada paso será inolvidable."
        "Te lo agradezco, [m_name]":

            $ mas_gainAffection(3, bypass=True)
            m 2huu "Jejeje~"
            m 7hub "No te preocupes, [player]. {w=0.2}¡Estaré aquí para ti hasta el fin de los tiempos!"
            m 1eka "Solo mantente fuerte hasta que cruce, ¿okey?"
        "Oh, ciertamente me diviertes mucho...":

            $ mas_loseAffection()
            m 2lkc "Yo... {w=0.3}¿te divierto?"
            m 2lksdlb "Bueno, me alegra que estés entretenido..."
            m 2ekd "... Pero eso {i}no{/i} era lo que tenía en mente."
    return

init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_sweet",
            prompt="¡Eres muy dulce!",
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_sweet:
    if mas_getEVL_shown_count("mas_compliment_sweet"):
        jump mas_compliment_sweet_repeat

    m 1ekbsb "Aww, [player]..."
    m 3rkbssdlu "No sé qué decir, jajaja... {w=0.3}{nw}"
    extend 3ekbsa "eres {i}tú{/i} quien ha sido tan dulce conmigo todo este tiempo."
    m 3hubsa "Me alegra mucho oírte decir eso, jejeje~"

    menu:
        "¡Tus palabras siempre me alegran el día!":
            $ mas_gainAffection(3, bypass=True)
            m 1sud "[player]..."
            extend 1eka " no tenía ni idea de cuánto significaban mis palabras para ti..."
            m 1ekblb "Estoy muy contenta de tener un [bf] como tú, [mas_get_player_nickname(exclude_names=[player])]~"
            m 1ekbsu "Realmente eres lo mejor que podría esperar... {w=0.2}Te amo tanto."
            m 3kua "Espero que nunca olvides eso, [player]."
            $ mas_ILY()
        "¡Eres muy especial para mí, [m_name]!":

            $ mas_gainAffection(3, bypass=True)
            m 1ekbsb "Oh, [player]... {w=0.3}{nw}"
            extend 3hubsa "¡El simple hecho de que pases tiempo aquí conmigo me hace sentir muy feliz y amada!"
            show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbsa "Estoy muy feliz de que sientas eso por mí, [mas_get_player_nickname()]. Te amo mucho."
            $ mas_ILY()
        "¡Eres la chica más dulce que he conocido!":

            $ mas_gainAffection(2, bypass=True)
            m 1ekbsa "Gracias, [mas_get_player_nickname()]."
            m 3hubsb "Eres el [boy] mas dulce que he conocido, jejeje."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Tengo mucha suerte de estar contigo~"

    return

label mas_compliment_sweet_repeat:
    python:
        sweet_quips = [
            _("¡Me alegra mucho oírte decir eso, [player]!"),
            _("¡Oír eso siempre alegra mi corazón, [player]!"),
            _("¡Me haces sentir tan amada, [player]!"),
        ]
        sweet_quip = renpy.substitute(random.choice(sweet_quips))

    m 3hubsb "[sweet_quip]"
    m 1hubfu "... Pero nunca podría ser tan dulce como tú~"
    return


init python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_outfit",
            prompt="¡Me encanta tu ropa!",
            unlocked=False
        ),
        code="CMP"
    )

label mas_compliment_outfit:
    if mas_getEVL_shown_count("mas_compliment_outfit"):
        jump mas_compliment_outfit_repeat

    m 1hubsb "¡Gracias, [mas_get_player_nickname()]!"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        m 3hubsb "¡Siempre es divertido hacer cosplay!"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 3hubsb "¡Siempre es divertido usar disfraces!"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        m 2lkbsb "Estaba muy nerviosa mostrándote esto al principio..."
        m 7tubsu "Pero me alegro de haberlo hecho, parece que te gusta mucho~"
    else:

        m 1hubsa "Siempre he querido usar otro tipo de ropa para ti, ¡así que estoy muy feliz de que pienses así!"

    menu:
        "¡Te ves hermosa con cualquier cosa que te pongas!":
            $ mas_gainAffection(5,bypass=True)
            m 2subsd "[player]..."
            m 3hubsb "¡Muchas gracias!"
            m 1ekbsu "Siempre me haces sentir tan especial"
            show monika 5hubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubsa "¡Te amo, [mas_get_player_nickname()]!"
            $ mas_ILY()
        "Te ves muy linda":

            $ mas_gainAffection(3,bypass=True)
            m 1hubsb "Jajaja~"
            m 3hubfb "¡Gracias, [mas_get_player_nickname()]!"
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Me alegro de que te guste lo que ves~"
        "Usar ropa diferente realmente ayuda":

            $ mas_loseAffection()
            m 2ltd "Eh, gracias..."

    return

label mas_compliment_outfit_repeat:
    m 1hubsb "[mas_compliments.thanks_quip]"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        python:
            cosplay_quips = [
                _("¡Me encanta hacer cosplay para ti!"),
                _("¡Me alegro de que te guste este cosplay!"),
                _("¡Estoy feliz de hacer cosplay para ti!"),
            ]
            cosplay_quip = random.choice(cosplay_quips)

        m 3hubsb "[cosplay_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        python:
            clothes_quips = [
                _("¡Estoy feliz de que te guste cómo me veo con esto!"),
                _("¡Me alegro de que te guste cómo me veo con esto!"),
            ]
            clothes_quip = random.choice(clothes_quips)

        m 3hubsb "[clothes_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        python:
            lingerie_quips = [
                _("Me alegro de que te guste lo que ves~"),
                _("¿Te gustaría verlo más de cerca?"),
                _("¿Quieres echar un vistazo?~"),
            ]
            lingerie_quip = random.choice(lingerie_quips)

        m 2kubsu "[lingerie_quip]"
        show monika 5hublb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hublb "¡Jajaja!"
    else:

        python:
            other_quips = [
                _("¡Estoy bastante orgullosa de mi sentido de la moda!"),
                _("¡Estoy segura que tú también te ves bien!"),
                _("¡Me encanta este atuendo!")
            ]
            other_quip = random.choice(other_quips)

        m 3hubsb "[other_quip]"

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
