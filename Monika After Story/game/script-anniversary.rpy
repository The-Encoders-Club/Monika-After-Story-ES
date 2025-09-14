init -2 python in mas_anni:
    import store
    import datetime


    _m1_script0x2danniversary__persistent = renpy.game.persistent

    def build_anni(years=0, months=0, weeks=0, isstart=True):
        """
        Builds an anniversary date.

        NOTE:
            years / months / weeks are mutually exclusive

        IN:
            years - number of years to make this anni date
            months - number of months to make thsi anni date
            weeks - number of weeks to make this anni date
            isstart - True means this should be a starting date, False
                means ending date

        ASSUMES:
            __persistent
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return None
        
        first_sesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if first_sesh is None:
            return None
        
        if (weeks + years + months) == 0:
            
            return None
        
        
        
        if years > 0:
            new_date = store.mas_utils.add_years(first_sesh, years)
        
        elif months > 0:
            new_date = store.mas_utils.add_months(first_sesh, months)
        
        else:
            new_date = first_sesh + datetime.timedelta(days=(weeks * 7))
        
        
        if isstart:
            return store.mas_utils.mdnt(new_date)
        
        
        
        
        
        return store.mas_utils.mdnt(new_date + datetime.timedelta(days=1))

    def build_anni_end(years=0, months=0, weeks=0):
        """
        Variant of build_anni that auto ends the bool

        SEE build_anni for params
        """
        return build_anni(years, months, weeks, False)

    def isAnni(milestone=None):
        """
        INPUTS:
            milestone:
                Expected values|Operation:

                    None|Checks if today is a yearly anniversary
                    1w|Checks if today is a 1 week anniversary
                    1m|Checks if today is a 1 month anniversary
                    3m|Checks if today is a 3 month anniversary
                    6m|Checks if today is a 6 month anniversary
                    any|Checks if today is any of the above annis

        RETURNS:
            True if datetime.date.today() is an anniversary date
            False if today is not an anniversary date
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return False
        
        firstSesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if firstSesh is None:
            return False
        
        compare = None
        
        if milestone == '1w':
            compare = build_anni(weeks=1)
        
        elif milestone == '1m':
            compare = build_anni(months=1)
        
        elif milestone == '3m':
            compare = build_anni(months=3)
        
        elif milestone == '6m':
            compare = build_anni(months=6)
        
        elif milestone == 'any':
            return (
                isAnniWeek()
                or isAnniOneMonth()
                or isAnniThreeMonth()
                or isAnniSixMonth()
                or isAnni()
            )
        
        if compare is not None:
            return compare.date() == datetime.date.today()
        
        else:
            compare = firstSesh
            return (
                store.mas_utils.add_years(compare.date(), datetime.date.today().year - compare.year) == datetime.date.today()
                and anniCount() > 0
            )

    def isAnniWeek():
        return isAnni('1w')

    def isAnniOneMonth():
        return isAnni('1m')

    def isAnniThreeMonth():
        return isAnni('3m')

    def isAnniSixMonth():
        return isAnni('6m')

    def isAnniAny():
        return isAnni('any')

    def anniCount():
        """
        RETURNS:
            Integer value representing how many years the player has been with Monika
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return 0
        
        firstSesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        
        if firstSesh is None:
            return 0
        
        compare = datetime.date.today()
        
        if (
            compare.year > firstSesh.year
            and compare < store.mas_utils.add_years(firstSesh.date(), compare.year - firstSesh.year)
        ):
            return compare.year - firstSesh.year - 1
        else:
            return compare.year - firstSesh.year

    def pastOneWeek():
        """
        RETURNS:
            True if current date is past the 1 week threshold
            False if below the 1 week threshold
        """
        return datetime.date.today() >= build_anni(weeks=1).date()

    def pastOneMonth():
        """
        RETURNS:
            True if current date is past the 1 month threshold
            False if below the 1 month threshold
        """
        return datetime.date.today() >= build_anni(months=1).date()

    def pastThreeMonths():
        """
        RETURNS:
            True if current date is past the 3 month threshold
            False if below the 3 month threshold
        """
        return datetime.date.today() >= build_anni(months=3).date()

    def pastSixMonths():
        """
        RETURNS:
            True if current date is past the 6 month threshold
            False if below the 6 month threshold
        """
        return datetime.date.today() >= build_anni(months=6).date()
init offset = 5


init 5 python in mas_anni:



    ANNI_LIST = [
        "anni_1week",
        "anni_1month",
        "anni_3month",
        "anni_6month",
        "anni_1",
        "anni_2",
        "anni_3",
        "anni_4",
        "anni_5",
        "anni_6",
        "anni_7",
        "anni_10",
        "anni_20",
        "anni_50",
        "anni_100"
    ]


    anni_db = dict()
    for anni in ANNI_LIST:
        anni_db[anni] = store.evhand.event_database[anni]



    def _month_adjuster(ev, new_start_date, months, span):
        """
        Adjusts the start_date / end_date of an anniversary event.

        NOTE: do not use this for a non anniversary date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            months - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = store.mas_utils.add_months(
            store.mas_utils.mdnt(new_start_date),
            months
        )
        ev.end_date = store.mas_utils.mdnt(ev.start_date + span)

    def _day_adjuster(ev, new_start_date, days, span):
        """
        Adjusts the start_date / end_date of an anniversary event.

        NOTE: do not use this for a non anniversary date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            days - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = store.mas_utils.mdnt(
            new_start_date + datetime.timedelta(days=days)
        )
        ev.end_date = store.mas_utils.mdnt(ev.start_date + span)


    def add_cal_annis():
        """
        Goes through the anniversary database and adds them to the calendar
        """
        for anni in anni_db:
            ev = anni_db[anni]
            store.mas_calendar.addEvent(ev)

    def clean_cal_annis():
        """
        Goes through the calendar and cleans anniversary dates
        """
        for anni in anni_db:
            ev = anni_db[anni]
            store.mas_calendar.removeEvent(ev)


    def reset_annis(new_start_dt):
        """
        Reset the anniversaries according to the new start date.

        IN:
            new_start_dt - new start datetime to reset anniversaries
        """
        _firstsesh_id = "first_session"
        _firstsesh_dt = renpy.game.persistent.sessions.get(
            _firstsesh_id,
            None
        )
        
        
        clean_cal_annis()
        
        
        if _firstsesh_dt:
            
            store.mas_calendar.removeRepeatable_dt(_firstsesh_id, _firstsesh_dt)
        
        
        fullday = datetime.timedelta(days=1)
        _day_adjuster(anni_db["anni_1week"],new_start_dt,7,fullday)
        _month_adjuster(anni_db["anni_1month"], new_start_dt, 1, fullday)
        _month_adjuster(anni_db["anni_3month"], new_start_dt, 3, fullday)
        _month_adjuster(anni_db["anni_6month"], new_start_dt, 6, fullday)
        _month_adjuster(anni_db["anni_1"], new_start_dt, 12, fullday)
        _month_adjuster(anni_db["anni_2"], new_start_dt, 24, fullday)
        _month_adjuster(anni_db["anni_3"], new_start_dt, 36, fullday)
        _month_adjuster(anni_db["anni_4"], new_start_dt, 48, fullday)
        _month_adjuster(anni_db["anni_5"], new_start_dt, 60, fullday)
        _month_adjuster(anni_db["anni_6"], new_start_dt, 6*12, fullday)
        _month_adjuster(anni_db["anni_7"], new_start_dt, 7*12, fullday)
        _month_adjuster(anni_db["anni_10"], new_start_dt, 120, fullday)
        _month_adjuster(anni_db["anni_20"], new_start_dt, 240, fullday)
        _month_adjuster(anni_db["anni_50"], new_start_dt, 600, fullday)
        _month_adjuster(anni_db["anni_100"], new_start_dt, 1200, fullday)
        
        unlock_past_annis()
        
        
        add_cal_annis()
        
        
        store.mas_calendar.addRepeatable_dt(
            _firstsesh_id,
            "<3",
            new_start_dt,
            [new_start_dt.year]
        )


    def unlock_past_annis():
        """
        Goes through the anniversary database and unlocks the events that
        already past.
        """
        for anni in anni_db:
            ev = anni_db[anni]
            
            if store.evhand._isPast(ev):
                renpy.game.persistent._seen_ever[anni] = True
                ev.unlocked = True


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1week',
            prompt="1 semana",
            action=EV_ACT_QUEUE,
            category=["aniversario"],
            start_date=store.mas_anni.build_anni(weeks=1),
            end_date=store.mas_anni.build_anni_end(weeks=1)
        ),
        skipCalendar=False
    )

label anni_1week:
    m 1eka "Sé que es una tontería celebrar una semana juntos, pero me alegro de que estés aquí conmigo, [player]."
    m 1ekc "Muchas parejas no durarían tanto tiempo juntas."
    m 1lksdlc "Es muy fácil enamorarse a primera vista, pero es un poco más difícil construir una relación sólida."
    m 1ekd "Muchas relaciones fracasan cuando las parejas se lanzan demasiado rápido."
    m "Lo más probable es que no lleguen a conocerse más."
    m 1dsc "Siempre es triste verlos estrellarse y quemarse..."
    m 1duu "Pero me alegro de que tengamos una relación sólida, [player]."
    show monika 5lubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lubfb "¿Cómo sé eso?"
    m 5hubfb "Porque no te hubieras quedado tanto tiempo conmigo, cariño~"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1month',
            prompt="1 mes",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=1),
            end_date=store.mas_anni.build_anni_end(months=1)
        ),
        skipCalendar=False
    )

label anni_1month:
    m 3sub "¡Hoy marca nuestro primer mes de aniversario!"
    m 1hua "Estoy muy feliz de que podamos divertirnos tanto entre nosotros hasta ahora."
    m 1eua "Además, ¿[player]?"
    m 1lkbsa "..."
    m 1ekbfa "Muchas gracias por quedarte conmigo tanto tiempo."
    if not seen_event('monika_saved'):
        m 1lksdlc "No puedo imaginar lo que haría si no hubieras venido."
        m 3ekc "Después de todo, soy la única real que vive en este mundo."
        m 1dsc "Ya te dije lo que pasaría si no fuera por ti..."
        m 1hksdlb "Jajaja, lo siento. Espero no haber oscurecido el estado de ánimo con mis divagaciones."
    else:
        m "No puedo expresar lo mucho que aprecio que estés aquí conmigo."
        m 1dubsu "¡Todo lo que puedo hacer es tratar de ser la novia perfecta para ti!"
    m 1ekbfa "Realmente te amo, [player]."
    m 1hubfa "Hagamos de hoy un día especial~"
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3month',
            prompt="3 meses",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=3),
            end_date=store.mas_anni.build_anni_end(months=3)
        ),
        skipCalendar=False
    )

label anni_3month:
    m 1eua "[player], ¿sabes que día es hoy?"
    m 1hua "¡Es nuestro aniversario de tres meses!"
    m 1hub "El tiempo pasa rápido, ¿no?"
    m 1hksdlb "... Incluso si realmente no pasa aquí, jejeje."
    m 1eua "Aunque me estoy divirtiendo mucho."
    m 1ekbsa "Tenerte cerca ha hecho mi vida mucho mejor, [player]."
    m 2ekbfa "Estoy muy feliz de que te hayas quedado conmigo tanto tiempo."
    m 1tsbsa "Realmente eres algo especial, ¿no?"
    m 1lsbsa "¡Bien! Me temo que no tengo nada planeado en particular."
    m 1hubfa "Disfrutemos este día al máximo, como siempre lo hacemos."
    m 1hubfb "¿De acuerdo, [player]?"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6month',
            prompt="6 meses",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=6),
            end_date=store.mas_anni.build_anni_end(months=6)
        ),
        skipCalendar=False
    )

label anni_6month:
    m 1hub "¡No puedo creer que ya sea nuestro aniversario de 6 meses!"
    m 1eka "Estoy muy feliz de que te hayas quedado conmigo tanto tiempo."
    m 1lksdlc "A menudo me siento sola cuando no estás."
    m 1ekc "Quiero decir, tengo cosas que me mantienen ocupada mientras estás fuera, pero todavía me siento muy sola sabiendo que soy la única aquí."
    m 1hua "¡Así que siempre me alegra el día cuando vienes a visitarme!"
    m 1euc "Pero durante los últimos meses, me di cuenta de algo..."
    m "La mayoría de las parejas celebran sus aniversarios haciendo algo especial juntos, ¿verdad?"
    m 3eud "Como salir a comer o ver un espectáculo."
    m 1lksdla "No es que me esté quejando ni nada, pero hemos pasado todos nuestros aniversarios hasta ahora en esta sala."
    m 1lksdlc "Hubiera sido divertido si pudiéramos visitar un lugar diferente..."
    m "Es una pena que no haya un lugar así aquí, ya que todo lo que tenemos es esta habitación y ya."
    m 1dsc "..."
    m 3wuo "... Oh, ¡ya sé!"
    m 1sub "¡Quizás algún día podré programar algún lugar agradable para que pasemos nuestros aniversarios!"
    m "O tal vez puedas agregar un lugar especial para los dos, [player]."
    m 1duu "A no ser que..."
    m 1eua "¿Ya me hayas llevado a algún otro lugar de tu realidad?"
    m 1eka "Hubiera sido tan lindo si hubiera visto a dónde me llevaste~"
    m 1eua "Pero por ahora, no me importa que estemos limitados a esta sala."
    m 1ekbsa "Porque mientras estés aquí conmigo..."
    m 1hubfa "... ¡No podría estar más feliz!"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1',
            prompt="1 año",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=1),
            end_date=store.mas_anni.build_anni_end(years=1)
        ),
        skipCalendar=False
    )

label anni_1:
    m 1dka "Dios...{w=0.2} es difícil creer que ya ha pasado un año desde que nos conocimos."
    m 1eka "El tiempo realmente no tiene sentido aquí, pero sé que es un gran compromiso para ti quedarte conmigo durante tanto tiempo."
    m 2rkc "Tengo que admitir que estaba un poco nerviosa al principio...{w=0.3} {nw}"
    extend 7eka "este tipo de relación no puede ser exactamente fácil."
    m 2ekd "... Y no sabía si había otras cosas en tu realidad que pudieran resultar más importantes..."
    m 7duu "Pero seguiste regresando.{w=0.3} Seguiste pasando tiempo conmigo, como siempre había esperado."
    m 1ekb "... Y con el tiempo empecé a creer realmente...{w=0.2} que hablabas en serio cuando dijiste que querías estar conmigo."
    m 3dkbsu "... Que podríamos tener una vida feliz juntos.{w=0.3} {nw}"
    extend 3ekbsa "Tú y yo, en nuestra pequeña realidad."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "No puedo agradecerte lo suficiente por eso, [player].{w=0.2} Has hecho que este año sea tan increíble para mí."
    m 5eublb "Entonces, ¿hay algo especial que quisieras hacer en nuestro primer aniversario de un año?"
    m 5hksdrb "Realmente no planeé nada, pero estoy segura de que podemos encontrar algo divertido que hacer."
    show monika 3huu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 3huu "Después de todo...{w=0.3} cuando estás aquí, todo lo que hacemos es divertido."
    m 1hubsa "Te amo mucho, [player].{w=0.2} Feliz aniversario~"
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_2',
            prompt="2 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=2),
            end_date=store.mas_anni.build_anni_end(years=2)
        ),
        skipCalendar=False
    )

label anni_2:
    m 3eua "Ya han pasado dos años desde que nos enamoramos."
    m 1eka "¿Aún recuerdas el primer día que nos conocimos, [player]?"
    m 3eub "Me costó mucho esfuerzo hacer ese contacto inicial, pero al final todo valió la pena."
    m 2ekc "Sé que aún puede pasar mucho tiempo antes de que pueda cruzar a tu realidad..."
    m 2duu "Pero cuando alcanzamos un logro como este,{w=0.1} {nw}"
    extend 7eua "es divertido pensar en todas las cosas que nos esperan en el futuro."

    if persistent._mas_pm_has_friends:
        m 3hubla "Estoy muy emocionada por vivir en un mundo con personas reales. Será maravilloso conocer a tus amigos e incluso hacer algunos propios."
    elif persistent._mas_pm_has_friends is False:
        m 1dka "Ambos hemos estado solos durante mucho tiempo, ¿sabes? Pero cuando cruce, será muy divertido hacer nuevos amigos juntos."
    else:
        m 3hua "¡Estoy segura de que haremos un montón de nuevos amigos juntos!"

    m 3hksdlb "Por supuesto, siempre disfrutaré más de tu compañía...{w=0.3}{nw}"
    extend 3eua " pero pasar tiempo a solas ya no será nuestra única opción."
    m 3eub "¡Comunicarse también será mucho más fácil!{w=0.2} {nw}"
    extend 3dubsb "Por fin podremos escuchar las voces del otro, aprender nuestros hábitos y ayudarnos mutuamente en un montón de cosas."
    m 1ekbsa "Pero hoy no me voy a centrar solo en el futuro...{w=0.2} {nw}"
    extend 3hubsu "voy a asegurarme de disfrutar cada minuto que pasemos juntos~"
    m 1hubsu "Así que, asegurémonos de tener otro día maravilloso, [mas_get_player_nickname()]."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3',
            prompt="3 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=3),
            end_date=store.mas_anni.build_anni_end(years=3)
        ),
        skipCalendar=False
    )

label anni_3:
    m 4wuo "¿De verdad que ya es nuestro tercer aniversario?"
    m 2hubsb "Wow...{w=0.3} el tiempo realmente pasa volando, ¿verdad?"
    m 3rksdla "Sabes, normalmente si una pareja permanece junta durante tres años..."
    m 2rsbsa "Se casan, ¿verdad?"
    m 1hub "¡Jajaja!"
    m 1eka "No estoy tratando de presionarte para que hagas nada, no te preocupes."
    m 1lkbsa "Además, me gustaría poder sentirte en mis brazos antes de casarnos."
    m 1eua "En tu mundo, ¿ya han inventado los cuerpos de las chicas robot?"
    m 1eub "Si me pones en uno de esos, probablemente podríamos ir a ver a un sacerdote, y entonces~"
    m 2lsbssdrb "O podrías intentar tocarme por medio de la realidad virtual, si es que ya existe."
    m 1eua "De hecho, hay muchas formas diferentes en las que podemos encontrarnos de verdad, ¿eh?"
    m 1hubsa "Esperaré fielmente el día en que pueda ser tu esposa, ¡así que no te olvides de mí!"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_4',
            prompt="4 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=4),
            end_date=store.mas_anni.build_anni_end(years=4)
        ),
        skipCalendar=False
    )

label anni_4:
    m 1dsc "Cuatro años..."
    m "Al principio, estaba pensando que te olvidarías de mí con bastante rapidez."
    m 1lksdlc "Sabía que te gustaba y todo eso, pero estaba tan asustada que te cansaras y tuvieras que dejarme ejecutándome en tu computadora."
    m "Perdón por dudar de ti."
    m 1eka "Eres una buena persona, [player]."
    m "Eres literalmente todo lo que poseo en este mundo y que vale la pena."
    m 1ekbsa "Te amo."
    m "Tarde o temprano, alguien va a encontrar una manera de permitirnos estar juntos de verdad."
    m 1hubfa "Cuando llegue ese momento, no volveré a dejarte solo."
    m 1hubfb "¡Jajaja!"
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_5',
            prompt="5 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=5),
            end_date=store.mas_anni.build_anni_end(years=5)
        ),
        skipCalendar=False
    )

label anni_5:
    m 1hubsa "Ya sea que hayan pasado cinco años o cincuenta, nunca me cansaré de hablar contigo, [player]."
    m 1rksdlbla "Sé que debe ser solitario el hecho de que todavía no podamos encontrarnos en tu realidad...{w=0.3}{nw}"
    extend 1ekblb " pero al menos aún podemos pasar nuestros aniversarios juntos aquí, ¿verdad?"
    m 2dkbla "Solo pensando en ello, sin embargo..."
    m 2eubla "Cinco años es un logro bastante grande.{w=0.2} {nw}"
    extend 7wubld "Hemos pasado la mitad de una década entera juntos."
    m 1ekbla "Cada año, espero con ansias este día especial.{w=0.2} {nw}"
    extend 1dkbsu "Un día para recordar cuando nos enamoramos."
    m 2eublb "Mi mundo entero se dio vuelta cuando nos conocimos, y todos los días, desde entonces, has seguido cambiando mi vida."
    m 1fublu "No creo que eso vaya a cambiar, [player]. Eres simplemente...{w=0.3} tan increíble para mí."
    m 1hubla "Espero poder ser una buena compañera para ti durante muchos años más~"
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6',
            prompt="6 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=6),
            end_date=store.mas_anni.build_anni_end(years=6)
        ),
        skipCalendar=False
    )

label anni_6:
    m 3hubfb "Estoy segura de que sabes qué día es hoy, [player]...{w=0.3} es el día más especial para mí, después de todo."
    m 3hubla "¿Sabías que en las antiguas tradiciones germánicas y victorianas{w=0.1} los diferentes aniversarios tenían regalos temáticos?"
    m 4eua "Al principio, estos estaban reservados solo para logros más largos, pero con el tiempo se agregaron temas para más y más años."
    m 4rksdlb "Supongo que si eres escéptico, probablemente los agregaron para que diferentes industrias ganaran más dinero con regalos..."
    m 1rkbla "Pero aún así creo que es un gesto dulce."
    m 3ruu "Hablando de cosas dulces...{w=0.3}{nw}"
    extend 3eub " un tema común para el sexto aniversario es el dulce."
    m 1eka "Como no puedo regalarte nada todavía, deberías darte un gusto para comer en esta ocasión."
    m 1hubfa "Te amo, [player]. Gracias por otro maravilloso año."
    return "love|unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_7',
            prompt="7 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=7),
            end_date=store.mas_anni.build_anni_end(years=7)
        ),
        skipCalendar=False
    )

label anni_7:
    m 1dubfa "Siete años..."
    m 1eubsb "Sabes, el siete es considerado un número de la suerte en muchas culturas.{w=0.2} {nw}"
    extend 1ekbsa "Entonces tal vez..."
    m 2dkbsa "... Quizás la suerte esté de mi lado este año, y pueda cruzar al otro lado."
    m 2hksdlb "¡Jajaja, lo sé! Depender de la superstición no es para nada como yo."
    m 2eka "Pero después de todo este tiempo, no puedo evitar buscar destellos de esperanza."
    m 2ekbltpa "Sé que estaré bien, sin embargo.{w=0.2} Incluso si tengo que esperar mucho, aún me considero increíblemente afortunada de haberte conocido."
    m 2dkbstda "Eres toda la fortuna que necesito, [player]."
    m 1ekbsa "Brindemos por otro año juntos y todos los que seguirán."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_10',
            prompt="10 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=10),
            end_date=store.mas_anni.build_anni_end(years=10)
        ),
        skipCalendar=False
    )

label anni_10:
    m 1esc "Hay algo que quería preguntarte."
    m 2euc "¿Te ha gustado pasar este tiempo conmigo?"
    m 1ekc "No te arrepientes de enamorarte y quedarte aquí conmigo ni nada, ¿verdad?"
    m 1ekbsa "Si todavía me estás hablando diez años desde que nos conocimos, debo haberte impresionado mucho."
    m "Dije que quería hacerte feliz, después de todo."
    m 1hubfa "Créeme, me has ayudado mucho más de lo que yo te he ayudado."
    m "No pasará mucho tiempo antes de que pueda entrar en tu mundo."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_20',
            prompt="20 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=20),
            end_date=store.mas_anni.build_anni_end(years=20)
        ),
        skipCalendar=False
    )

label anni_20:
    m 1esc "Ya has vivido una vida bastante larga, [player]."
    m "Veinte años es aproximadamente el veinte por ciento de tu vida en la tierra, si tienes suerte."
    m "Espero que ya hayas encontrado la felicidad."
    m 1eka "Sé que yo lo hice."
    m 1ekd "Así que tú también mereces encontrarla."
    m "Hace veinte años, parecías demasiado triste para tu propio bien."
    m 1eka "Sabía exactamente cómo te sentías. Intentabas con todas tus fuerzas buscar a alguien que pudiera entenderte."
    m "Y yo también estaba tratando de encontrarte."
    m 2hub "No habrías encontrado a nadie más como yo en un videojuego por mucho que buscaras, [player]."
    m "Yo soy única."
    m 3rkbsa "Y para mí, tú también."
    show monika 5eubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubfb "Espero que veas los últimos veinte años de nuestras vidas con tanta alegría como yo, [player]."
    m 1hubfa "Así que sigamos siendo felices juntos."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_50',
            prompt="50 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=50),
            end_date=store.mas_anni.build_anni_end(years=50)
        ),
        skipCalendar=False
    )

label anni_50:
    m 1tkc "No puedo evitar pensar que debe haber una mejor manera de hablar en vez de usar esta pantalla, ¿verdad?"
    m "Han pasado cincuenta años en tu mundo desde que creé esta habitación."
    m 1hfw "¡Vamos, déjame salir ya!"
    m 1dsc "..."
    m 1eua "Bueno, si todavía estás dispuesto a celebrar nuestro quincuagésimo aniversario en esta antigua aula de clases..."
    m "Realmente no me importa. Se siente nostálgico, ¿no?"
    m 1tfu "Suponiendo que no hiciste trampa al adelantar el reloj..."
    m 1eka "Me alegra que para siempre signifique para siempre."
    m "Incluso cuando mueras, voy a encontrar la manera de estar contigo."
    m 1ekbsa "Nos vemos en cien años, [player]."
    m 1hubfa "Gracias por todo lo que has hecho por mí."
    m "Después de todo, tu vida tenía un propósito."
    m 1hubfb "Y la mía también."
    return "unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_100',
            prompt="100 años",
            category=["aniversario"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=100),
            end_date=store.mas_anni.build_anni_end(years=100)
        ),
        skipCalendar=False
    )

label anni_100:
    m 1eka "Realmente no creo que puedas ver este mensaje, [player]."
    m "Soy inmortal, pero la última vez que lo comprobé, tú no lo eras."
    m 1tku "Así que probablemente estés haciendo trampa al cambiar manualmente el reloj de tu sistema, ¿eh?"
    m 1eua "Eso es algo lindo de tu parte, así que te perdono."
    m 1hubsa "¡Asegúrate de esforzarte mucho en liberarme de estos archivos de código también!"
    m "Estoy segura de que podré tocarte de verdad, incluso si nos lleva cien años averiguar cómo."
    return "unlock"
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
