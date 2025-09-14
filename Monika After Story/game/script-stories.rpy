init offset = 5











default -5 persistent._mas_story_database = dict()


default -5 mas_full_scares = False


default -5 persistent._mas_last_seen_new_story = {"normal": None, "aterradora": None}


define -5 mas_scary_story_setup_done = False


init -6 python in mas_stories:
    import store
    import datetime

    UNLOCK_NEW = "unlock_new"


    TYPE_NORMAL = "normal"
    TYPE_SCARY = "aterradora"


    STORY_RETURN = "No importa"
    story_database = dict()


    TIME_BETWEEN_UNLOCKS = renpy.random.randint(20, 28)






    FIRST_STORY_EVL_MAP = {
        TYPE_SCARY: "mas_scary_story_hunter",
        TYPE_NORMAL: "mas_story_tyrant"
    }


    NEW_STORY_CONDITIONAL_OVERRIDE = {
        TYPE_SCARY: (
            "mas_stories.check_can_unlock_new_story(mas_stories.TYPE_SCARY, ignore_cooldown=store.mas_isO31())"
        ),
    }

    def check_can_unlock_new_story(story_type=TYPE_NORMAL, ignore_cooldown=False):
        """
        Checks if it has been at least one day since we've seen the last story or the initial story

        IN:
            story_type - story type to check if we can unlock a new one
                (Default: TYPE_NORMAL)
            ignore_cooldown - Whether or not we ignore the cooldown or time between new stories
                (Default: False)
        """
        global TIME_BETWEEN_UNLOCKS
        
        new_story_ls = store.persistent._mas_last_seen_new_story.get(story_type, None)
        
        
        first_story = FIRST_STORY_EVL_MAP.get(story_type, None)
        
        
        if not first_story:
            return False
        
        can_show_new_story = (
            store.seen_event(first_story)
            and (
                ignore_cooldown
                or store.mas_timePastSince(new_story_ls, datetime.timedelta(hours=TIME_BETWEEN_UNLOCKS))
            )
            and len(get_new_stories_for_type(story_type)) > 0
        )
        
        
        if can_show_new_story:
            TIME_BETWEEN_UNLOCKS = renpy.random.randint(20, 28)
        
        return can_show_new_story

    def get_new_stories_for_type(story_type):
        """
        Gets all new (unseen) stories of the given ype

        IN:
            story_type - story type to get

        OUT:
            list of locked stories for the given story type
        """
        return store.Event.filterEvents(
            story_database,
            pool=False,
            aff=store.mas_curr_affection,
            unlocked=False,
            flag_ban=store.EV_FLAG_HFNAS,
            category=(True, [story_type])
        )

    def get_and_unlock_random_story(story_type=TYPE_NORMAL):
        """
        Unlocks and returns a random story of the provided type

        IN:
            story_type - Type of story to unlock.
                (Default: TYPE_NORMAL)
        """
        
        stories = get_new_stories_for_type(story_type)
        
        
        story = renpy.random.choice(stories.values())
        
        
        story.unlocked = True
        
        return story.eventlabel

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_short_stories",
            category=['literatura'],
            prompt="¿Puedes contarme una historia?",
            pool=True,
            unlocked=True
        )
    )

label monika_short_stories:
    call monika_short_stories_premenu (None)
    return _return

label monika_short_stories_premenu(story_type=None):
    python:

        if story_type is None:
            story_type = mas_stories.TYPE_NORMAL
        end = ""

label monika_short_stories_menu:

    python:

        can_unlock_story = False

        if story_type in mas_stories.NEW_STORY_CONDITIONAL_OVERRIDE:
            try:
                can_unlock_story = eval(mas_stories.NEW_STORY_CONDITIONAL_OVERRIDE[story_type])
            except Exception as ex:
                store.mas_utils.mas_log.error("No se ha podido evaluar la condición para desbloquear la nueva historia porque '{0}'".format(ex))
                
                can_unlock_story = False

        else:
            can_unlock_story = mas_stories.check_can_unlock_new_story(story_type)


        stories_menu_items = [
            (story_ev.prompt, story_evl, False, False)
            for story_evl, story_ev in mas_stories.story_database.iteritems()
            if Event._filterEvent(
                story_ev,
                pool=False,
                aff=mas_curr_affection,
                unlocked=True,
                flag_ban=EV_FLAG_HFM,
                category=(True, [story_type])
            )
        ]


        stories_menu_items.sort()


        stories_menu_items.insert(0, ("Una nueva historia", mas_stories.UNLOCK_NEW, True, False))



        if story_type == mas_stories.TYPE_SCARY:
            switch_str = "corta"
        else:
            switch_str = "aterradora"

        switch_item = ("Me gustaría escuchar una historia " + switch_str, "monika_short_stories_menu", False, False, 20)

        final_item = (mas_stories.STORY_RETURN, False, False, False, 0)


    show monika 1eua at t21

    if story_type == mas_stories.TYPE_SCARY:
        $ which = "¿Qué"
    else:
        $ which = "¿Qué"

    $ renpy.say(m, which + " historia te gustaría escuchar?" + end, interact=False)


    call screen mas_gen_scrollable_menu(stories_menu_items, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch_item, final_item)


    if _return:

        if _return == "monika_short_stories_menu":

            if story_type == mas_stories.TYPE_SCARY:
                $ story_type = mas_stories.TYPE_NORMAL
            else:
                $ story_type = mas_stories.TYPE_SCARY

            $ end = "{fast}"
            $ _history_list.pop()

            jump monika_short_stories_menu
        else:

            $ story_to_push = _return


            if story_to_push == mas_stories.UNLOCK_NEW:
                if not can_unlock_story:
                    show monika at t11
                    $ _story_type = story_type if story_type != 'normal' else 'corta'
                    m 1ekc "Lo siento [player]... no puedo pensar en una historia [_story_type] en este momento..."
                    m 1eka "Si me das un poco de tiempo puede que se me ocurra una pronto... pero mientras tanto, siempre puedo volver a contarte una vieja~"
                    show monika 1eua
                    jump monika_short_stories_menu
                else:

                    python:
                        persistent._mas_last_seen_new_story[story_type] = datetime.datetime.now()
                        story_to_push = mas_stories.get_and_unlock_random_story(story_type)


            $ MASEventList.push(story_to_push, skipeval=True)

            show monika at t11
    else:

        return "prompt"

    return


label mas_story_begin:
    python:
        story_begin_quips = [
            _("De acuerdo, comencemos la historia."),
            _("¿Listo para escuchar la historia?"),
            _("¿Listo para la hora del cuento?"),
            _("Comencemos~"),
            _("¿Estás listo?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    $ mas_gainAffection(modifier=0.2)
    m 3eua "[story_begin_quip]"
    m 1duu "Ajem."
    return


label mas_scary_story_setup:
    if mas_scary_story_setup_done:
        return

    $ mas_scary_story_setup_done = True
    show monika 1dsc
    $ mas_temp_r_flag = mas_current_weather
    $ is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_rain)
    $ are_masks_changing = mas_current_weather != mas_weather_rain
    $ mas_is_raining = True

    $ mas_play_song(None, fadeout=1.0)
    pause 1.0

    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)


    if not persistent._mas_o31_in_o31_mode:
        $ mas_changeWeather(mas_weather_rain)
        $ store.mas_globals.show_vignette = True
        call spaceroom (dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing, force_exp='monika 1dsc_static')

    play music "mod_assets/bgm/happy_story_telling.ogg" loop


    $ HKBHideButtons()
    $ mas_RaiseShield_core()

    python:
        story_begin_quips = [
            _("De acuerdo, empecemos la historia."),
            _("¿Listo para escuchar la historia?"),
            _("¿Listo para la hora del cuento?"),
            _("Comencemos."),
            _("¿Estás listo?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)

    m 3eua "[story_begin_quip]"
    m 1duu "Ajem."
    return

label mas_scary_story_cleanup:

    python:
        story_end_quips = [
            _("¿Asustado, [player]?"),
            _("¿Te asusté, [player]?"),
            _("¿Cómo estuvo?"),
            _("¿Y bien?"),
            _("Entonces... {w=0.5}¿te asusté?")
        ]
        story_end_quip=renpy.substitute(renpy.random.choice(story_end_quips))

    m 3eua "[story_end_quip]"
    show monika 1dsc
    pause 1.0


    if not persistent._mas_o31_in_o31_mode:
        $ mas_changeWeather(mas_temp_r_flag)
        $ store.mas_globals.show_vignette = False
        call spaceroom (dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing, force_exp='monika 1dsc_static')
        hide vignette

    call monika_zoom_transition (mas_temp_zoom_level, transition=1.0)

    $ mas_play_song(None, 1.0)
    m 1eua "Espero que te haya gustado, [player]~"
    $ mas_DropShield_core()
    $ HKBShowButtons()
    $ mas_scary_story_setup_done = False
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_tyrant",
            prompt="El gato y el gallo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=True
        ),
        code="STY"
    )

label mas_story_tyrant:
    call mas_story_begin
    m 1eua "Un gato atrapó a un gallo y pensó en excusas razonables para comérselo."
    m "Lo acusaba de fastidioso por cacarear de noche; no dejando dormir a los hombres."
    m 3eud "El gallo defendió su acción diciendo que esto era en beneficio de los hombres, ya que los despierta para el trabajo."
    m 1tfb "El gato respondió: 'Abundas en disculpas, pero es hora de desayunar'."
    m 1hksdrb "Y con eso, se comió al gallo."
    m 3eua "La moraleja de esta historia es que los tiranos no necesitan excusas."
    m 1hua "Espero que hayas disfrutado de esta pequeña historia, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_despise",
            prompt="El zorro",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_despise:
    call mas_story_begin
    m 1eud "Un caluroso día de verano, un zorro paseaba por un huerto hasta que llegó a un racimo de uvas que estaba madurando en una parra que había sido amasada sobre una rama alta."
    m 1tfu "'Justo lo que necesito para saciar mi sed', dijo el zorro."
    m 1eua "Retrocediendo unos pasos, corrió y saltó, y por poco no alcanzó al racimo."
    m 3eub "Dando la vuelta de nuevo con uno, {w=1.0}dos, {w=1.0}tres, {w=1.0}saltó, pero sin mayor éxito."
    m 3tkc "Una y otra vez lo intentó tras el tentador bocado, pero al final tuvo que renunciar y se alejó con la nariz en alto, diciendo: 'Estoy seguro de que están amargas'."
    m 1hksdrb "La moraleja de esta historia es que es fácil despreciar lo que no puedes conseguir."
    m 1eua "Espero que te haya gustado, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_lies",
            prompt="El pastorcito y el lobo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_lies:
    call mas_story_begin
    m 1euc "Había un pastor que cuidaba sus ovejas al pie de una montaña cerca de un bosque oscuro."
    m 1lsc "Era solitario para él, así que ideó un plan para conseguir un poco de compañía."
    m 4hfw "Corrió hacia el pueblo gritando: '¡El lobo! ¡El lobo!' y los aldeanos salían a recibirlo."
    m 1hksdrb "Esto agradó tanto al niño que pocos días después intentó el mismo truco, y nuevamente los aldeanos acudieron en su ayuda."
    m 3wud "Poco después, un lobo salió del bosque."
    m 1ekc "El niño gritó: '¡El lobo, El lobo!' aún más fuerte que antes."
    m 4efd "Pero esta vez los aldeanos, que habían sido engañados dos veces antes, pensaron que el niño estaba mintiendo de nuevo y nadie acudió en su ayuda."
    m 2dsc "Así que el lobo se hizo de una buena comida con el rebaño del niño."
    m 2esc "La moraleja de esta historia es que a los mentirosos no se les cree incluso cuando dicen la verdad."
    m 1hksdlb "No deberías preocuparte por eso, [player]..."
    m 3hua "Nunca me mentirías, ¿verdad?"
    m 1hub "Jejeje~"
    m 1eua "¡Espero que hayas disfrutado de la historia, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_grasshoper",
            category=[mas_stories.TYPE_NORMAL],
            prompt="El saltamontes",
            unlocked=False
        ),
        code="STY"
    )

label mas_story_grasshoper:
    call mas_story_begin
    m 1eua "Un día de verano, un saltamontes estaba saltando, gorjeando y cantando a todo pulmón."
    m "Pasó una hormiga que llevaba una mazorca de maíz que llevaba al nido."
    m 3eud "'¿Por qué no vienes a charlar conmigo, en lugar de trabajar de esa manera?', dijo el saltamontes."
    m 1efc "'Estoy ayudando a guardar comida para el invierno y te recomiendo que hagas lo mismo', dijo la hormiga."
    m 1hfb "'¿Por qué preocuparse por el invierno? ¡Ahora tenemos mucha comida!', dijo el saltamontes."
    m 3eua "La hormiga siguió su camino."
    m 1dsc "Cuando llegó el invierno, el saltamontes no tenía comida y se encontró muriendo de hambre, mientras veía a las hormigas distribuir maíz y granos de las tiendas que habían recolectado durante el verano."
    m 3hua "La moraleja de esta historia es que hay un momento para trabajar y un momento para jugar."
    m 1dubsu "Pero siempre hay tiempo para pasar con tu linda novia~"
    m 1hub "Jejeje, ¡te amo mucho, [player]!"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_wind_sun",
            prompt="El viento y el sol",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_wind_sun:
    call mas_story_begin
    m 1dsc "El viento y el sol se disputaban cuál era el más fuerte."
    m 1euc "De repente vieron a un viajero que venía por la carretera y el sol dijo: 'Veo una manera de decidir nuestra disputa'."
    m 3efd "'Cualquiera de nosotros que pueda hacer que ese viajero se quite la capa será considerado el más fuerte, tú empiezas'."
    m 3euc "Así que el sol se retiró detrás de una nube, y el viento comenzó a soplar tan fuerte como pudo sobre el viajero."
    m 1ekc "Pero cuanto más sopló, más de cerca se envolvió el viajero con su capa, hasta que por fin el viento tuvo que rendirse desesperado."
    m 1euc "Entonces salió el sol y brilló con todo su esplendor sobre el viajero, que pronto encontró demasiado calor para caminar con su capa."
    m 3hua "La moraleja de esta historia es que la gentileza y la persuasión bondadosa ganan donde la fuerza y la fanfarronería fallan."
    m 1hub "Espero que te hayas divertido, [player]."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_seeds",
            prompt="Las semillas",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_seeds:
    call mas_story_begin
    m 1euc "Sucedió que un campesino estaba sembrando algunas semillas de cáñamo en un campo donde una golondrina y algunos otros pájaros saltaban para recoger su comida."
    m 1tfd "'Cuidado con ese hombre', dijo la golondrina."
    m 3eud "'¿Por qué, qué está haciendo?', preguntaron las demás."
    m 1tkd "'Esa es la semilla de cáñamo que está sembrando; tengan cuidado de recoger cada una de las semillas, o de lo contrario se arrepentirán'. Respondió la golondrina."
    m 3rksdld "Los pájaros no prestaron atención a las palabras de la golondrina, y poco a poco el cáñamo creció y se convirtió en cuerda, y de las cuerdas se hicieron redes."
    m 1euc "Muchas aves que habían despreciado el consejo de la golondrina fueron atrapadas en redes hechas con ese mismo cáñamo."
    m 3hfu "'¿Qué les dije?', citó la golondrina."
    m 3hua "La moraleja de esta historia es, destruye las semillas del mal antes de que crezcan y sean tu ruina."
    m 1lksdlc "..."
    m 2dsc "Ojalá pudiera haber seguido esa moraleja..."
    m 2lksdlc "No habrías tenido que pasar por lo que viste."
    m 4hksdlb "De todos modos, ¡espero que te haya gustado la historia, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_gray_hair",
            prompt="El cabello gris",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_gray_hair:
    call mas_story_begin
    m 1eua "En los viejos tiempos, un hombre de mediana edad tenía una esposa que era vieja y otra que era joven; cada una lo amaba y no deseaba nada más que ganarse su afecto."
    m 1euc "El cabello del hombre se estaba volviendo gris, lo que a la joven esposa no le gustó, ya que lo hacía parecer demasiado mayor."
    m 3rksdla "Así que, cada noche ella tomaba los cabellos blancos."
    m 3euc "Pero a la esposa mayor no le gustaba que la confundieran con su madre."
    m 1eud "Por lo tanto, todas las mañanas tomaba tantos pelos negros como podía."
    m 3hksdlb "El hombre pronto se encontró completamente calvo."
    m 1hua "La moraleja de esta historia es, cede a todos y pronto no tendrás nada que ceder."
    m 1hub "Así que antes de darlo todo, ¡asegúrate de tener algo para ti!"
    m 1lksdla "... No es que ser calvo sea malo, [player]."
    m 1hksdlb "Jejeje, ¡te amo!~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_fisherman",
            prompt="El Pescador",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_fisherman:
    call mas_story_begin
    m 1euc "Un pescador pobre, que vivía de los peces que pescaba, tuvo mala suerte un día y no pescó más que un alevín muy pequeño."
    m 1eud "El pescador estaba a punto de ponerlo en su canasta cuando el pececito habló."
    m 3ekd "'¡Por favor tenga piedad, señor pescador! Soy tan pequeño que no vale la pena llevarme a casa. ¡Cuando sea más grande, seré una comida mucho mejor!'"
    m 1eud "Pero el pescador rápidamente puso el pescado en su canasta."
    m 3tfu "'Qué tonto tendría que ser para devolverte. Por pequeño que seas, eres mejor que nada', dijo el pescador."
    m 3esa "La moraleja de esta historia es que una pequeña ganancia vale más que una gran promesa."
    m 1hub "Espero que hayas disfrutado de esta pequeña historia, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_ravel",
            prompt="Los tres deseos del viejo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_ravel:
    call mas_story_begin
    m 3euc "Una vez, un anciano estaba sentado solo en un camino oscuro."
    m 1euc "Había olvidado tanto a dónde viajaba como quién era."
    m "De repente, miró hacia arriba y vio a una anciana frente a él."
    m 1tfu "Ella sonrió sin dientes y con una carcajada, dijo: 'Ahora tu {i}tercer{/i} deseo. ¿Cuál será?'."
    m 3eud "'¿Tercer deseo?' El hombre estaba desconcertado. '¿Cómo puedo tener un tercer deseo si no he tenido un primer y segundo deseo?'."
    m 1tfd "'Ya tenías dos deseos, pero tu segundo deseo era que yo lo devolviera todo a la forma en que estaba antes de que hicieras tu primer deseo', dijo la bruja."
    m 3tku "'Por eso no recuerdas nada, porque todo está como estaba antes de pedir cualquier deseo'."
    m 1dsd "'Está bien, no creo en esto, pero no hay nada de malo en desear. Deseo saber quién soy', dijo el hombre."
    m 1tfb "Mientras le concedía su deseo y desaparecía para siempre, la anciana le dijo: 'Es curioso, ese fue tu primer deseo'."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_simple",
            prompt="El genio simple",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_simple:
    call mas_story_begin
    m 1eua "Una vez hubo un genio que viajó a través de diferentes mundos para escapar del caos propio."
    m 3euc "Durante sus viajes, conoció a una mujer que desafió su forma de ver el mundo."
    m 3eua "Era inteligente y talentosa, pero la frenaban las dificultades que enfrentaba y lo poco que tenía."
    m 3eub "El genio vio esto y se sintió generoso, ofreciendo herramientas para acelerar su trabajo y hacerle la vida más fácil."
    m 1euc "Pero ella simplemente rechazó su oferta."
    m 1eud "Nadie había rechazado un deseo del genio antes, {w=0.1}{nw}"
    extend 1etc "lo que lo dejó confundido en cuanto a por qué."
    m 1esa "La mujer simplemente le preguntó si él era feliz... {w=0.5}{nw}"
    extend 1rsc "no sabía cómo responder."
    m 3eud "La mujer dijo que podía decir que él nunca había experimentado la felicidad y que, a pesar de todas sus dificultades, ella podía disfrutar de la vida."
    m 1euc "El genio no podía entender por qué alguien querría trabajar tan duro por algo tan pequeño."
    m 3euc "Él mejoró sus ofertas con riquezas y otras cosas por el estilo, pero aún así, ella se negó."
    m 1eua "Finalmente, la mujer le pidió al genio que se uniera a su forma de vida."
    m "Y así, imitó las cosas que ella hizo, sin usar ningún poder."
    m 1hua "El genio comenzó a sentir una pequeña sensación de logro, creando algo por primera vez sin querer que existiera."
    m 3eub "Vio cómo cosas simples como el arte y la escritura inspiraban a la mujer y realmente la hacían brillar."
    m 1eua "Intrigado, quería pasar mucho más tiempo con esta mujer y aprender de ella."
    m 1euc "Finalmente, un día la mujer se enfermó."
    m 1eud "Ella le hizo prometer al genio que no usaría sus poderes para curarla."
    m 3eud "Fue en este momento que el genio supo que quería vivir como un humano sin volver a usar sus poderes."
    m 1dsc "Pensó en todos los deseos pasados que concedió a los demás, en todas las riquezas que generó..."
    m "Todos sus compañeros genios concediendo deseos, sin saber ni preocuparse por las consecuencias..."
    m 1dsd "Nunca ser capaz de saber lo que es dejarlo todo solo para estar con alguien a quien amas."
    m 1esd "Todo lo que podía hacer era vivir con lo que ahora había encontrado en la vida."
    m 1dsc "..."
    m 1eua "Espero que te haya gustado esa historia, [player]."
    m 3eua "Hay algunas cosas que podemos sacar de ella..."
    m 3eka "Si ya lo tienes todo, realmente no vale la pena tener nada."
    m 1hua "... Excepto tal vez tú, por supuesto."
    m 3eub "La lucha es lo que hace que todo valga la pena."
    m 1eua "Otra moraleja podría ser que, a veces, la felicidad radica en las cosas más simples que podrías haber tenido todo el tiempo."

    if mas_isMoniNormal(higher=True):
        m 1eka "Quiero decir, estamos sentados aquí juntos disfrutando de la compañía del otro después de todo."
        m 1hubsb "Cuando estás aquí, realmente siento que lo tengo todo~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_regret",
            prompt="El arrepentimiento del genio",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_regret:
    call mas_story_begin
    m 1eua "Había una vez un genio que era inmortal..."
    m "A lo largo de los años, había visto cómo el mundo cambiaba con el tiempo y otorgaba deseos a cualquiera que cruzara su camino."
    m 1esc "Con el tiempo que había vivido, había visto muchas cosas, {w=0.2}{nw}"
    extend 1rsc "algunas de ellas desagradables."
    m 1ekd "Guerras, desastres naturales, la muerte de todos los amigos que hizo..."
    m 1rkc "Algunas de las cuales, sabía que fueron causadas por deseos que había concedido."
    m 1ekc "Al principio, no estaba demasiado preocupado por las consecuencias... pero después de un tiempo, eso comenzó a preocuparle cada vez más."
    m 1ekd "Había llegado a un mundo simple, hermoso y puro, y causó un daño inmenso en él."
    m 1lksdlc "Desbalance y celos se propagaron a medida que concedía más deseos, sembrando la venganza y la avaricia."
    m 2dkd "Esto era algo con lo que tendría que vivir el resto de su vida."
    m 2ekc "Quería que las cosas volvieran a ser como antes, pero sus ruegos siempre caían en oídos sordos."
    m 2eka "A medida que pasaba el tiempo, sin embargo, conoció a algunas personas y hizo amigos que le enseñaron cómo seguir adelante a pesar de todos sus actos."
    m "Si bien era cierto que él era quien otorgaba los deseos que iniciaban el caos... {w=0.5}{nw}"
    extend 2ekd "algunos de ellos habrían sucedido incluso sin su intervención."
    m 3ekd "Siempre habría celos e injusticias entre las personas... {w=0.3}{nw}"
    extend 3eka "pero aun así, el mundo seguía adelante."
    m 3eua "Iba a vivir con las cosas que había hecho, pero la pregunta seguía siendo qué planeaba hacer al respecto."
    m 1hua "Fue gracias a todo lo que había pasado que pudo aprender y seguir adelante, {w=0.3}mejor que antes."
    m 1eua "Espero que te haya gustado la historia, [player]."
    m 1eka "La moraleja de la historia es que, incluso si has hecho cosas de las que te arrepientes, no deberías dejar que eso te derribe."
    m 3ekd "Cometeremos errores, la gente se lastimará. {w=0.5}Nada cambiará eso."
    m 3eka "De hecho, a menudo nos culpamos a nosotros mismos por cosas que probablemente habrían sucedido con o sin nuestra participación."
    m 3eub "De hecho, es a través del arrepentimiento que aprendemos compasión, empatía y el perdón."
    m 3eua "No puedes cambiar el pasado, pero tienes que perdonarte algún día para vivir una vida sin remordimientos."
    m 1eka "En cuanto a mí..."
    m 1rksdlc "Quién sabe qué habría pasado en mi mundo si no hubiera hecho nada..."

    $ placeholder = " al menos"
    if persistent.clearall:
        $ placeholder = ""
        m 1eua "Has llegado a conocer a todos y cada uno de los miembros del club, así que supongo que no te arrepientes de haberte perdido nada."
        m 1hub "Jajaja~"

    m 1eua "Pero[placeholder] ahora estás aquí conmigo."
    m 3eua "Desde que estamos juntos, puedo decir que he crecido y he aprendido de mis errores."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_end",
            prompt="El fin del genio",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_end:
    call mas_story_begin
    m 1eua "Había una vez un genio inmortal que había vivido una larga vida."
    m 1euc "Había visto todo lo que había que ver... {w=0.3}vivió libremente y aprendió el cumplimiento de trabajar hacia una meta."
    m 3euc "Esencialmente, renunció a todo menos a su inmortalidad para poder vivir como un humano."
    m 1ekc "Es cierto que había vivido una vida agradable y se había rodeado de familiares y amigos cariñosos..."
    m 1ekd "Pero se fue enfriando con el paso de los años y vio morir a cada uno de sus seres queridos."
    m 1rksdlc "Todavía había unas pocas personas seleccionadas a quienes apreciaba, a pesar de saber que también tendría que verlos morir."
    m 3rksdld "Nunca les dijo a sus amigos que no era humano, ya que todavía quería que lo trataran como tal."
    m 1euc "Un día, mientras viajaba con uno de sus amigos, se encontraron con un genio que les concedería un deseo a cada uno."
    m 1dsc "Esto le hizo pensar en todo lo que había pasado; {w=0.5}desde que concedió sus deseos hasta que lo dejó por una vida sencilla."
    m 1dsd "... Todo lo que lo había llevado a este momento, donde podía pedir su propio deseo por primera vez en mucho tiempo."
    m 1dsc "..."
    m 2eud "Deseó morir."
    m 2ekc "Confundido, su amigo preguntó por qué y de dónde venía eso de repente."
    m 2dsc "Fue allí que luego le explicó todo a su amigo."
    m 3euc "Que había sido un genio, hace muchos años..."
    m 3eud "... Cómo se encontró con alguien que le hizo renunciar a todo solo para estar con alguien a quien amaba."
    m 3ekd "... Y cómo se había ido enfermando y cansándose lentamente de lo que le quedaba de vida."
    m 1esc "A decir verdad, no estaba cansado de vivir... {w=0.5}{nw}"
    extend 1ekd "estaba cansado de ver morir a sus seres queridos una y otra vez."
    m 1dsd "Su última petición a su amigo fue que volviera con sus otros amigos y atara los cabos sueltos por él."
    m 1dsc "..."
    m 1eka "Espero que hayas disfrutado de esa pequeña historia, [player]."
    m 3eka "Supongo que se podría decir que la moraleja es que todo el mundo necesita un cierre."
    m 1eka "Aunque, es posible que te preguntes qué deseó su amigo en ese escenario."
    m 1eua "Deseó que su amigo tuviera el descanso pacífico que se merecía."
    m 1lksdla "Si bien es cierto que su amigo genio podría no haber sido alguien particularmente especial..."
    m 3eua "Definitivamente era alguien que merecía respeto, {w=0.2}{nw}"
    extend 3eub "especialmente después de vivir una vida tan larga."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_immortal_love",
            prompt="El amor nunca termina",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_immortal_love:
    call mas_story_begin
    m 3eua "Había una pareja casada que vivió felices juntos durante muchos años."
    m "Cada día de San Valentín, el esposo le enviaba un hermoso ramo de flores a su esposa."
    m 1eka "Cada uno de estos ramos vino con una nota con unas pocas palabras escritas."
    m 3dsc "{i}Mi amor por ti solo crece.{/i}"
    m 1eud "Después de algún tiempo, el esposo falleció."
    m 1eka "La esposa, entristecida por su pérdida, creía que pasaría su próximo San Valentín sola y de luto."
    m 1dsc "..."
    m 2euc "Sin embargo, {w=0.3}en su primer día de San Valentín sin su esposo, ella todavía recibió un ramo de él."
    m 2efd "Con el corazón roto y enojado, se quejó a la floristería de que había un error."
    m 2euc "El florista explicó que no había ningún error."
    m 3eua "El esposo había pedido muchos ramos de flores con anticipación para asegurarse de que su amada esposa continuaría recibiendo flores mucho después de su muerte."
    m 3eka "Sin palabras y atónita, la esposa leyó la nota adjunta al ramo."
    m 1ekbsa "{i}Mi amor por ti es eterno.{/i}"
    m 1dubsu "Ahh..."
    m 1eua "¿No fue una historia conmovedora, [player]?"
    m 1hua "Pensé que era realmente romántica."
    m 1lksdlb "Pero no quiero pensar en ninguno de los dos muriendo."
    m 1eua "Al menos el final fue muy reconfortante."
    m 1hua "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_mother_and_trees",
            prompt="Una madre y sus árboles",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_mother_and_trees:
    call mas_story_begin
    m 1eua "Había una vez un niño que vivía con su madre."
    m 3eud "Ella le dio todo el cariño que una madre podría darle... {w=0.2}{nw}"
    extend 3rksdla "pero él siempre pensó que ella podía ser un poco rara."
    m 3eub "En sus cumpleaños, ella {i}siempre{/i} horneaba galletas para él y todos sus compañeros de clase para agradecerles por ser sus amigos."
    m 1eua "Ella también guardaba y exhibía cada pequeño dibujo que él hacía en la escuela de arte, por lo que sus paredes estaban cubiertas con arte de los últimos años."
    m 2rksdlc "A veces, incluso se deshacía de sus dibujos porque no quería que ella los pusiera junto al resto."
    m 2euc "Sin embargo, lo que más se destacó de ella... {w=0.3}{nw}"
    extend 2eud "era que hablaba a menudo con sus árboles."
    m 1eua "Había tres árboles en su patio trasero con los que ella hablaba todos los días."
    m 3rksdlb "¡Incluso tenía nombres para cada uno de ellos!"
    m 3hksdlb "A veces, incluso le pedía que se vistiera y posara junto a los árboles para poder tomarles fotos juntos."
    m 1eka "Un día, cuando la vio hablando con los árboles, le preguntó por qué siempre les hablaba tanto."
    m 3hub "Su madre respondió: 'Bueno, ¡porque necesitan sentirse amados!'"
    m 1eka "Pero él todavía no la entendía... {w=0.2}{nw}"
    extend 1eua "y tan pronto como se fue, ella continuó justo donde lo había dejado en su conversación."
    m 2ekc "Con el paso del tiempo, el niño finalmente tuvo que mudarse y comenzar su propia vida."
    m 2eka "Su madre le dijo que no se preocupara por dejarla porque tenía sus árboles para hacerle siempre compañía."
    m 2eua "Mientras estaba ocupado con su vida, todavía tenía tiempo para mantenerse en contacto con ella."
    m 2ekc "Hasta que un día... {w=0.5}{nw}"
    extend 2dkd "recibió la llamada."
    m 2rksdlc "Su madre había muerto y fue encontrada tirada junto a uno de los árboles."
    m 2ekd "En su testamento, solo tenía una petición para él... {w=0.3}y era que siguiera cuidando los árboles, hablando con ellos todos los días."
    m 1eka "Por supuesto, cuidó bien de los árboles, pero nunca pudo animarse a hablar con ellos."
    m 3euc "Algún tiempo después, mientras revisaba y limpiaba las pertenencias antiguas de su madre, encontró un sobre."
    m 1eud "En el interior, se sorprendió por lo que encontró."
    m 2wud "Había tres certificados de defunción de mortinatos para sus posibles hermanos."
    m 2dsc "Cada uno de ellos tenía un nombre idéntico a uno de los árboles que había estado en el patio trasero toda su vida."
    m 2dsd "Nunca había sabido que tenía hermanos, pero finalmente entendió por qué su madre hablaba con los árboles..."
    m 2eka "Siempre quiso tomarse muy en serio el deseo de su madre, y fue entonces cuando empezó a hablar con los árboles todos los días, tal como deseaba su madre."
    m 2duu "... E incluso siguió adelante y plantó un árbol más."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_self_hate",
            prompt="Auto-odio",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_self_hate:
    call mas_story_begin
    m 1eua "Una vez, había dos personas que habían estado viviendo juntas durante mucho tiempo."
    m 1hua "La vida era simple y ambos se amaban. Las cosas iban bien."
    m 3euc "Entonces, un día, el hombre mató repentinamente a su amante sin ninguna razón aparente."
    m 3eud "Él {i}sí{/i} la amaba, ¡y de una manera saludable también!"
    m 2ekc "Tampoco hubo nunca peleas ni discusiones."
    m "No había nada que ganar con asesinarla."
    m 4ekd "Sin satisfacción, nada fuera de lo común en su testamento..."
    m 1dkc "De hecho, el hombre quedó emocionalmente marcado por haber perdido al amor de su vida."
    m "..."
    m 1ekd "¿Entonces por qué?"
    m 1rksdlc "¿Cómo pudo pasar esto de repente?"
    m 1eksdlc "No es que no la amase."
    m 3eksdla "Fue porque la amaba muchísimo."
    m "Él no la odiaba..."
    m 2eksdld "Simplemente se odiaba a sí mismo tanto como para negar su propia felicidad."
    m 2dkc "..."
    if persistent._mas_pm_love_yourself is False:
        m 3ekc "Hey [player], ¿recuerdas cuando te pregunté si te amabas a ti mismo?"
        m 1rksdld "Por lo que recuerdo, me dijiste que no..."
        m 1rksdla "Lo siento, no pretendo ponerte en aprietos ni nada..."
        m 3eka "Solo quiero asegurarme de que recuerdes que te amo."
        m 3ekd "Más importante aún, quiero asegurarme de que sepas cómo amarte a ti mismo."
        m 1ekbsa "Sé que vale la pena amarte y haría cualquier cosa para mostrarte por qué."
        m 1ekbfa "Espero que nunca lo olvides~"
    else:
        m 1rksdlb "Perdón por contar una historia tan oscura, [player]..."
        m 3eksdla "Pero tiene un mensaje importante..."
        m 3eud "Y ese es, que necesitas encontrar una manera de amarte a ti mismo o podrías hacer algo de lo que te arrepientas más adelante."
        m 1ekc "Por mucho que lo intentes, intentar vivir tu vida únicamente para otra persona nunca funcionará."
        m 1eka "Tienes que amarte a ti mismo para poder permitirte amar de verdad a otra persona."
        m 3ekbsa "Solo recuerda que siempre te amaré, [player]."
        m 3ekbfa "Si alguna vez empiezas a dudar de amarte a ti mismo, ven a mí y estaré más que feliz de recordarte todas tus maravillosas cualidades~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_o_tei",
            prompt="La historia de O-Tei",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_o_tei:
    call mas_story_begin
    m 1eua "Hace mucho tiempo, vivía un hombre llamado Kenji, que estaba estudiando para ser médico."
    m 3eub "Estaba comprometido con una joven llamada Tomoe y se casarían después de que él terminara sus estudios."
    m 1esc "Desafortunadamente, Tomoe contrajo una enfermedad grave antes de que eso sucediera."
    m 2dsd "No pasó mucho tiempo hasta que estuvo postrada en cama, acercándose al final de su vida."
    m 2esd "Kenji se arrodilló junto a su cama y ella le dijo: 'Nos hemos prometido el uno al otro desde la infancia...'"
    m 3ekc "'Desafortunadamente con este frágil cuerpo mío, ha llegado mi momento y voy a morir antes de poder convertirme en tu esposa'."
    m "'Por favor, no te aflijas cuando me vaya. Creo que nos volveremos a encontrar'."
    m 3eud "Él preguntó: '¿Cómo sabré de tu regreso?'."
    m 2dsc "Desafortunadamente, ella había sucumbido antes de poder darle una respuesta."
    m "Kenji lamentó profundamente la pérdida de su amor, arrebatado demasiado pronto."
    m 2esc "Nunca se olvidó de Tomoe a medida que pasaba el tiempo, pero se le pidió que se casara con otra persona y conservara el apellido."
    m "Pronto se casó con otra chica, pero su corazón se quedó en otro lugar."
    m 2esd "Y como ocurre con todo en la vida, su familia también había sido arrebatada por el tiempo y él se quedó solo de nuevo."
    m 4eud "Fue entonces cuando decidió abandonar su hogar y emprender un largo viaje para olvidar sus problemas."
    m 1esc "Viajó por todo el país en busca de una cura para su malestar."
    m 1euc "Y luego, una noche, se encontró con una posada y se detuvo allí para descansar."
    m "Mientras se acomodaba en su habitación, una nakai abrió la puerta para recibirlo."
    m 3euc "Su corazón dio un vuelco..."
    m 3wud "La chica que lo recibió se parecía exactamente a Tomoe."
    m "Todo lo que vio en ella le recordó perfectamente a su amor pasado."
    m 1esc "Kenji entonces recordó las últimas palabras que intercambiaron antes de su partida."
    m 1esc "Hizo señas a la chica y le dijo: 'Lamento ser una molestia, pero me recuerdas tanto a alguien que conocí hace mucho tiempo que me sorprendió al principio'."
    m 3euc "'Si no le importa que le pregunte, ¿cuál es su nombre?'."
    m 3wud "Inmediatamente, con la voz inolvidable de su amada fallecida, la chica respondió: 'Mi nombre es Tomoe y tú eres Kenji, mi esposo prometido'."
    m 1wud "'Morí trágicamente antes de que pudiéramos completar nuestro matrimonio...'"
    m "'Y ahora he vuelto, Kenji, mi futuro esposo'."
    m 1dsc "La chica luego se derrumbó al suelo, inconsciente."
    m 1esa "Kenji la sostuvo en sus brazos, las lágrimas fluían de su rostro."
    m 1dsa "'... Bienvenida de nuevo, Tomoe...'"
    m 3esa "Cuando volvió en sí, no recordaba lo que sucedió en la posada."
    m 1hua "No mucho después, Kenji se casó con ella tan pronto como pudo, y vivieron felices por el resto de sus vidas."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_crow_and_pitcher",
            prompt="El cuervo y la jarra",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_crow_and_pitcher:
    call mas_story_begin
    m 2ekd "Hubo una vez una sequía tan severa que ni siquiera los pájaros podían encontrar mucho para beber."
    m 7eub "Mientras buscaba desde arriba, un cuervo sediento encontró una jarra y se sintió aliviado al descubrir que todavía había algo de agua dentro."
    m 3eksdlc "Sin embargo, el jarrón era alto con un cuello estrecho. No importaba cómo lo intentara, no podía alcanzar el agua con su pico."
    m 1dksdlc "Para el pobre cuervo, toda esperanza parecía perdida. Seguramente moriría de sed."
    m 3wud "... Entonces él tuvo una idea."
    m 3esc "Comenzó a buscar pequeñas piedras en el suelo y las dejó caer en la jarra, una por una."
    m 2efsdlc "Pasaron las horas. Fue un trabajo lento y agotador, reunir más y más."
    m 2esa "Pero con cada pequeño guijarro, el agua subía más y más, hasta que finalmente..."
    m 4hub "¡Pudo tomar un trago largo y refrescante!"
    m 2dka "..."
    m 2eka "Sabes, esta historia me recuerda nuestra situación, [player]."
    m 7ekc "En este momento, nuestro objetivo parece muy lejano. Nos estamos esforzando tanto como podemos, pero la brecha entre nosotros es enorme."
    m 3dkc "A veces se siente como si fuera imposible superarlo. Si tratáramos de cruzarlo de un salto, seríamos como el cuervo que alcanza con solo su pico."
    m 1tkd "... Créeme, lo intenté."
    m 3ekb "Pero cuando lo piensas, estamos agregando guijarros a nuestra jarra. ¡Y no somos solo tú y yo!"
    m 3eua "Los avances tanto en la tecnología de realidad virtual como de inteligencia artificial están avanzando gradualmente..."
    m 3hua "Y más específicamente a nuestra situación, muchas personas están trabajando juntas para ayudarme a acercarme a tu realidad."
    m 1eka "Cuando lo pienso de esa manera, el nivel del agua en esa jarra sube lentamente, hace que sea mucho más fácil seguir adelante todos los días."
    m 1hua "Espero que también lo haga para ti, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_friend",
            prompt="Tener un mejor amigo",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_friend:
    call mas_story_begin
    m 3eua "Una vez, dos amigos caminaban por el desierto..."
    m 1eua "Durante algún momento de su viaje, tuvieron una discusión. {nw}"
    extend 1wud "¡Y uno de los amigos abofeteó al otro en la cara!"
    m 1eud "El que recibió la bofetada resultó herido, pero sin decir nada escribió en la arena: {w=0.1}'Hoy mi mejor amigo me abofeteó'."
    m 1eua "Siguieron caminando hasta que encontraron un oasis, donde decidieron bañarse."
    m 1ekc "El que había sido abofeteado se quedó atrapado en el fango y comenzó a ahogarse, {w=0.1}{nw}"
    extend 3wuo "¡pero el otro lo salvó!"
    m 3eua "Después de recuperarse de casi ahogarse, escribió en una piedra: {w=0.1}'Hoy mi mejor amigo me salvó la vida'."
    m 3eud "El amigo que había abofeteado y salvado a su mejor amigo le preguntó: {w=0.1}'Después de que te lastimé, escribiste en la arena y ahora, escribes en una piedra, ¿por qué?'."
    m 3eua "El otro amigo respondió: 'Cuando alguien nos lastima, debemos escribirlo en la arena donde los vientos del perdón puedan borrarlo...'"
    m 3eub "'¡Pero!'"
    m 3eua "'Cuando alguien hace algo bueno por nosotros, debemos grabarlo en la piedra donde ningún viento pueda borrarlo'."
    m 1hua "La moraleja de la historia es que no dejes que las sombras de tu pasado oscurezcan el umbral de tu futuro. {w=0.2}{nw}"
    extend 3hua "Perdona y olvida."
    m 1hua "¡Espero que lo hayas disfrutado, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_tanabata",
            prompt="La tejedora y el pastor",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="STY"
    )

label mas_story_tanabata:
    call mas_story_begin
    m 1eub "Orihime, la hija del Emperador de Jade, gobernante del cielo, tejía hermosas ropas en la orilla del Amanogawa."
    m 3eua "A su padre le encantaba la tela que ella tejía y por eso trabajaba muy duro cada día para tejerla."
    m 2ekd "Sin embargo, Orihime estaba triste porque a causa de su duro trabajo, nunca pudo conocer ni enamorarse de nadie."
    m 2eksdla "Preocupado por su hija, su padre la hizo conocer al pastor de vacas Hikoboshi, que vivía y trabajaba al otro lado del Amanogawa."
    m 7hub "Cuando se conocieron, ¡se enamoraron al instante y se casaron poco después!"
    m 2eksdld "Sin embargo, una vez casada, Orihime dejó de tejer y Hikoboshi dejó que sus vacas se perdieran por todo el cielo."
    m 4wud "Enfadado, el emperador separó a los dos esposos y les prohibió reunirse."
    m 2dkc "Orihime se abatió ante la pérdida de su esposo y pidió a su padre que les permitiera volver a reunirse."
    m 2eksdla "Conmovido por las lágrimas de su hija, permitió que ambos se reunieran el séptimo día del séptimo mes si ella se esforzaba y terminaba su tejido."
    m 2wud "Sin embargo, la primera vez que intentaron reunirse, se encontraron con que no podían cruzar el río porque no había puente."
    m 2dkc "Orihime lloró tanto que una bandada de urracas vino y prometió hacer un puente con sus alas para que ella pudiera cruzar el río."
    m 7ekd "Se dice que si llueve en Tanabata, las urracas no pueden venir y los enamorados deben esperar hasta otro año para encontrarse."
    m 3eud "La lluvia que cae en Tanabata se llama apropiadamente: {i}Las lágrimas de Orihime y Hikoboshi.{/i}"
    m 1dksdlc "No puedo imaginar lo que debe ser poder reunirse con tu ser querido solo una vez al año."
    m 3eua "Pero ya sabes lo que dicen, [player]... {w=0.3}el amor puede mover montañas."
    m 3hubsu "... Y mi amor por ti es tan fuerte que ni el mismo cielo podría separarnos."
    $ mas_unlockEVL("monika_tanabata", "EVE")
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_mindthegap",
            prompt="Cuidado con la brecha",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_mindthegap:
    call mas_story_begin
    m 3eud "En realidad se trata de una historia real que ocurrió en Londres, Inglaterra, en 2013."
    m 2dkd "Comienza con una mujer llamada Margaret McCollum llorando en medio de la estación de tren de Embankment."
    m 2ekd "Cuando se le acercó para preguntarle por su gran angustia, preguntó al personal dónde había ido 'la voz'."
    m 7ekd "Aclaró que se refería al anuncio que sonaba a la llegada de cada tren, en el que se advertía a los pasajeros de que tuvieran cuidado con 'la brecha'."
    m 1eka "El personal le aseguró que el anuncio no había desaparecido, solo se había actualizado a una nueva grabación cuando las emisoras se habían actualizado a un nuevo sistema digital."
    m 1tkc "Sin embargo, esta explicación no pareció calmarla. {w=0.3}'Esa voz', explicó, era mi esposo."
    m 1eud "Su esposo, Oswald Laurence, un actor que nunca llegó a ser famoso, había grabado todos los anuncios de la línea norte."
    m 2dkc "Oswald había muerto hace cinco años."
    m 2ekc "Se habían amado mucho, y su muerte la había dejado sumida en un terrible dolor."
    m 2euc "Pero una cosa, {w=0.2}durante esos cinco años, {w=0.2}la había ayudado a seguir adelante."
    m 7eka "Todos los días, cuando se dirigía al trabajo, escuchaba su voz en la estación.{w=0.3} A veces se quedaba sentada, solo para oírle decir esas breves palabras."
    m 2dkc "Pero ahora..."
    m 2dkd "El personal se disculpó, pero no sabía si tenía acceso al antiguo expediente. {w=0.3}Le dijeron que si lo encontraban, se pondrían en contacto con ella."
    m 7eud "Resultó que muchas personas que trabajaban en la estación sentían empatía y querían que Margaret pudiera disfrutar de ese precioso recuerdo un tiempo más."
    m 7ekb "Así que, aunque les costó un trabajo extra actualizar la antigua grabación de los archivos para que funcionara con el sistema actual, pero al final lo consiguieron."
    m 3eua "Un día, cuando Margaret estaba haciendo su viaje diario, una voz familiar sonó en el andén."
    m 1fkb "'Cuidado con la brecha', dijo Oswald."
    m 1dku "..."
    m 3eka "Dije que era una historia real, y resulta que todavía se puede escuchar esa vieja grabación concretamente en la estación de Embankment."
    m 3ekb "Es un ejemplo realmente hermoso de bondad humana. {w=0.3}Los trabajadores no ganaban mucho restaurando una grabación mucho más corta y de menor calidad."
    m 1fka "Pero sabían lo que era perder a alguien, y lo precioso que resulta cada foto, cada recuerdo."
    m 1dku "Esto demuestra que las personas pueden hacer cosas increíbles simplemente por compasión y amor."
    m 1ekbla "Esta historia me recuerda que debo atesorar cada momento, y no dar por sentado ningún trozo de nuestro tiempo juntos."
    m 1dkblu "Siempre te atesoraré, [player]."
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_knock",
            prompt="Knock",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_knock:
    call mas_story_begin
    m 1euc "El último hombre en la Tierra estaba solo en una habitación."
    m 3rud "... Hubo un golpe en la puerta."
    m 3duc "Algunos podrían decir que aquí termina la historia. {w=0.2}{nw}"
    extend 1dud "Pero eso no es realmente cierto."
    m 3etc "¿Quién golpeó la puerta? {w=0.2}{nw}"
    extend 3esa "La respuesta no fue tan horrible, realmente."
    m 3eua "El último hombre en la Tierra era Walter Phelan. {w=0.2}Su única compañía era una especie llamada los Zan."
    m 3eud "La raza humana había sido destruida por ellos, excepto por él y, en algún lugar... {w=0.3}{nw}"
    extend 3wud "una mujer... {w=0.1}una mujer."
    m 3euc "Tanto Walter como esta mujer fueron elegidos como especímenes para el zoológico organizado por los Zan."
    m 2esc "Había dos de cada especie, al igual que en el Arca de Noé."
    m 2euc "De todos modos, cuando abrió la puerta, Walter no se sorprendió al ver a uno de los Zan."
    m 2etd "El extraño alienígena, después de saludar al humano de la mejor manera que un alienígena podía hacerlo, le pidió ayuda a Walter."
    m 2euc "El alienígena dijo: 'Algo que no entendemos ocurrió, {w=0.1}{nw}"
    extend 2ekd "dos de los otros animales duermen y no despiertan. Están fríos'."
    m 7euc "Era obvio para Walter que los dos animales, una serpiente y un pato, habían muerto."
    m 3esc "Sin embargo, los Zan no lo sabían."
    m 1dsc "El humano rápidamente ideó una estrategia en su mente.{w=0.2} Le dijo a los Zan que los animales nunca despertarían. {w=0.2}Que la vieja parca estaba suelta, matando a todos a la vista."
    m 1euc "... Pero él podría ayudar. {w=0.2}Con una condición:{w=0.2} La última mujer en la Tierra también debía ayudar."
    m 1eua "Los Zan le permitieron ir a ver a los animales y se organizó una reunión."
    m 1dsc "Walter pensó que nunca vería a la última mujer en la Tierra... {w=0.3}{nw}"
    extend 1wub "pero... ¡encontrarse con ella fue un giro asombroso de los acontecimientos!"
    m 1esa "Grace Evans, la última mujer en la Tierra, se sorprendió al saber lo que Walter había descubierto: {w=0.2}los Zan no podían morir por causas naturales."
    m 3ttu "... Pero tal vez podrían ser asesinados."
    m 1eud "El hombre tenía todas las piezas para probar esa teoría y, después de despedirse de Grace, puso su plan en acción."
    m 3esc "Le pidió a los Zan que vieran al último pato, ya que el otro había muerto, y le dijo al alienígena lo que debía hacer."
    m 4eud "'Dale afecto acariciándolo, o de lo contrario, también morirá... {w=0.2}de soledad'."
    m 3rsc "Ahora, los alienígenas no tenían conocimiento de cómo funcionaba el afecto, así que simplemente observaron mientras Walter acariciaba al pato con amor."
    m 1esc "'Debes hacer lo mismo con la serpiente restante', dijo."
    m 1euc "... Y así lo hizo el Zan."
    m 3wud "Pero ten en cuenta, [player], que no era una serpiente común... {w=0.3}{nw}"
    extend 3tfu "sino una venenosa."
    m 1euc "Entonces, el Zan asignado para acariciar la serpiente restante fue afectado por su veneno mortal."
    m 1wud "Al día siguiente, otro Zan entró en la habitación de Walter desesperado. {w=0.2}{nw}"
    extend 4wko "Él gritó: '¡Uno de nosotros murió!'."
    m 2dud "'Bueno, no hay nada que hacer entonces. {w=0.2}{nw}"
    extend 2esc "La maldición se ha propagado y debes huir', declaró el hombre."
    m 7euc "Los Zan tuvieron una reunión del consejo y les informaron a los dos humanos que se ellos se iban del planeta."
    m 1ekd "El riesgo era demasiado alto, no podían perder más de su propia raza."
    m 3eud "Dejaron a todos los animales 'malditos', incluidos Walter y Grace, y despegaron en su nave."
    m 1dua "El último hombre y la última mujer en la Tierra estaban juntos al fin. {w=0.2}{nw}"
    extend 1rkbla "Ahora, ¿qué harían con su eternidad?"
    m 3gsbsu "Eso queda para que lo imaginemos..."
    m 1hubsa "Espero que te haya gustado esta historia, [player]."
    return


init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_hunter",
    category=[store.mas_stories.TYPE_SCARY], prompt="El cazador",unlocked=True),
    code="STY")

label mas_scary_story_hunter:
    call mas_scary_story_setup
    m 3esa "Un día, un cazador salió al bosque."
    m 3esc "El bosque era denso y oscuro a su alrededor, por lo que luchó por dar en el blanco."
    m 1esd "Pronto se le acercó un vendedor, que mantuvo su rostro cubierto."
    m 3esd "El vendedor ofreció siete balas mágicas que alcanzarían cualquier objetivo que el propietario quisiera sin falta."
    m "Él le daría al cazador estas balas con una condición."
    m 1euc "El cazador podría usar las primeras seis balas como quisiera, pero el vendedor elegiría la marca de la última bala."
    m "El cazador estuvo de acuerdo y rápidamente se hizo famoso en su ciudad por traer a casa muerte tras muerte."
    m 3eud "No pasó mucho tiempo antes de que el cazador agotara las seis balas."
    m 1esc "En su siguiente cacería, el cazador vio un jabalí, el más grande que jamás había visto. Era una presa demasiado grande para dejarla pasar."
    m 1euc "Cargó la última bala con la esperanza de acabar con la bestia..."
    m 1dsc "Pero cuando disparó, la bala alcanzó a su amada prometida en el pecho, matándola."
    m 3esc "El vendedor se pareció ante cazador mientras lamentaba su trágica pérdida, y le reveló que en realidad era el diablo."
    m 1esd "'Te daré la oportunidad de redimirte, cazador'. Dijo el vendedor."
    m 4esb "'Permanece siempre fiel a tu amada asesinada por el resto de tu vida, y te reunirás con ella después de la muerte'."
    m 1eud "El cazador juró permanecer fiel a ella mientras viviera..."
    m 1dsd "... {w=1}O así lo quiso hacer."
    m 1dsc "Mucho después de su muerte, se enamoró de otra mujer y pronto se casó con ella, olvidando su amor pasado."
    m 1esc "Fue hasta que un año después del fatal incidente, mientras el cazador cabalgaba por el bosque persiguiendo alguna presa, se encontró con el lugar donde mató a su amada..."
    m 3wud "No podía creer lo que veía; {w=1}su cadáver, que estaba enterrado en otro lugar, estaba parado en el mismo lugar donde la mataron."
    m "Ella se acercó al cazador, despreciándolo por su infidelidad y prometiendo venganza por haberla asesinado."
    m "El cazador se alejó preso del pánico."
    m 1euc "Al cabo de un rato, miró detrás de él para ver si le seguía..."
    m 1wkd "... Y para su horror, {w=1}vio que se le había adelantado significativamente."
    m 3wkd "En su estado de miedo, no pudo evitar la rama que estaba delante de él, y rápidamente se desmontó de su corcel y cayó al frío suelo."
    m 4dsc "Sin embargo, la atención de ella no estaba en su caballo, ya que la criatura se alejó sin él."
    $ store.mas_sprites.show_empty_desk()
    m 1esc "... En cambio, fue en la figura con la que prometió estar eternamente en la otra vida."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        hide monika
        play sound "sfx/giggle.ogg"
        show yuri dragon2 zorder 72 at malpha
        $ style.say_dialogue = style.edited
        y "{cps=*2}Yo también te atraparé.{/cps}{nw}"
        hide yuri
        $ mas_resetTextSpeed()
        show monika 1eua zorder MAS_MONIKA_Z at i11
    hide emptydesk
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_kuchisake_onna",
    category=[store.mas_stories.TYPE_SCARY], prompt="Kuchisake-Onna",unlocked=False),
    code="STY")

label mas_scary_story_kuchisake_onna:
    call mas_scary_story_setup
    m 3eud "Había una vez una mujer hermosa, que era la esposa de un samurái."
    m 3eub "Ella era tan increíblemente hermosa como vanidosa, acogiendo la atención de cualquier hombre dispuesto a ofrecérsela."
    m 1tsu "Y a menudo les pedía a los hombres que evaluaran su apariencia."
    m 1euc "La mujer era propensa a engañar a su marido varias veces y pronto se enteró de sus aventuras."
    m 1esc "Cuando se enfrentó a ella, estaba más que enfurecido porque ella estaba dañando su condición de nobles, humillándolo."
    m 2dsc "Luego la castigó brutalmente cortándole la boca de oreja a oreja, desfigurando su delicada belleza."
    m 4efd "'¿Quién te considerará hermosa ahora?' fue su sal para su horrible herida."
    m 2dsd "Poco después, la mujer murió."
    m "No podía seguir viviendo después de que todos los que la rodeaban la trataran como un monstruo."
    m 1esc "Su marido, denunciado por su crueldad, cometió seppuku poco después."
    m 3eud "La mujer, muriendo por tal destino, se convirtió en un espíritu vengativo y malicioso."
    m "Dicen que ahora deambula sin rumbo fijo por la noche, con la cara cubierta con una máscara y un arma blanca en las manos."
    m 1dsd "Cualquiera que tenga la mala suerte de encontrarse con ella oirá su escalofriante pregunta..."
    m 1cua "{b}{i}¿Soy b o n i t a?{/i}{/b}"

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,15) == 1) or mas_full_scares:
        hide monika
        show screen tear(20, 0.1, 0.1, 0, 40)
        play sound "sfx/s_kill_glitch1.ogg"
        show natsuki ghost2 zorder 73 at i11
        show k_rects_eyes1 zorder 74
        show k_rects_eyes2 zorder 74
        $ pause(0.25)

        stop sound
        hide screen tear
        $ style.say_dialogue = style.edited
        show screen mas_background_timed_jump(5, "mas_scary_story_kuchisake_onna.no")
        menu:
            "¿Soy bonita?"
            "Sí":
                hide screen mas_background_timed_jump
                jump mas_scary_story_kuchisake_onna.clean
            "No":
                jump mas_scary_story_kuchisake_onna.no
    else:
        jump mas_scary_story_kuchisake_onna.end

label mas_scary_story_kuchisake_onna.no:
    hide screen mas_background_timed_jump
    "{b}{i}¿Es eso, así?{w=1.0}{nw}{/i}{/b}"
    $ _history_list.pop()
    $ _history_list.pop()
    $ pause(1.0)
    hide natsuki
    play sound "sfx/run.ogg"
    show natsuki mas_ghost onlayer front at i11
    $ pause(0.25)
    hide natsuki mas_ghost onlayer front

label mas_scary_story_kuchisake_onna.clean:
    show black zorder 100
    hide k_rects_eyes1
    hide k_rects_eyes2
    hide natsuki
    $ pause(1.5)
    hide black
    $ mas_resetTextSpeed()
    show monika 1eua zorder MAS_MONIKA_Z at i11

label mas_scary_story_kuchisake_onna.end:
    m 3eud "El destino que ella te da depende de tu respuesta, en realidad."
    m "Encontrarse con ella no siempre sellará tu perdición."
    m 3esc "Sin embargo..."
    m "Si no eres inteligente con tu respuesta..."
    m 3tku "Podrías acabar como ella."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_mujina",
    category=[store.mas_stories.TYPE_SCARY], prompt="Mujina",unlocked=False),
    code="STY")

label mas_scary_story_mujina:
    call mas_scary_story_setup
    m 1esc "Una noche, a última hora, un viejo comerciante caminaba por un camino rumbo a casa después de un largo día vendiendo sus mercancías."
    m 3esc "El camino por el que viajaba conducía a una gran colina que estaba muy oscura y aislada por la noche, por lo que muchos viajeros tendían a evitar la zona."
    m "Sin embargo, el hombre estaba cansado y decidió tomar la carretera de todos modos, ya que lo llevaría a casa más rápido."
    m "A un lado de la colina había un viejo foso que era bastante profundo."
    m 3eud "Mientras avanzaba, vio a una mujer agachada junto al foso, sola y llorando amargamente."
    m "Aunque el hombre estaba exhausto, temía que la mujer tuviera la intención de tirarse al agua, por lo que se detuvo."
    m 3euc "Era pequeña y bien vestida, cubriéndose la cara con una de las mangas de su kimono mirando hacia otro lado."
    m 3eud "El hombre le dijo: 'Señorita, por favor no llore. ¿Cuál es el problema? Si hay algo que pueda hacer para ayudarla, estaría encantado de hacerlo'."
    m "La mujer siguió llorando, ignorándolo."
    m 3ekd "'Señorita, escúcheme. Este no es lugar para una dama de noche. Por favor, déjame ayudarte'."
    m 1euc "Lentamente, la mujer se levantó, todavía sollozando."
    m 1dsc "El hombre puso su mano suavemente sobre su hombro..."
    m 4wud "Cuando ella giró bruscamente la cabeza hacia él, mostrando un rostro en blanco, desprovisto de todos los rasgos humanos."
    m 4wuw "Sin ojos, boca o nariz. ¡Solo un rostro vacío que le devolvió la mirada!"
    m "El comerciante se escapó tan rápido como pudo, preso del pánico por la figura inquietante."
    m 1efc "Continuó corriendo hasta que vio la luz de una linterna y corrió hacia ella."
    m 3euc "La linterna pertenecía a un viajante de comercio que caminaba."
    m 1esc "El anciano se detuvo frente a él, se dobló para recuperar el aliento."
    m 3esc "El vendedor preguntó por qué el hombre corría."
    m 4ekd "'¡Un m-monstruo! ¡Había una chica sin rostro junto al foso! gritó el comerciante."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        $ style.say_dialogue = style.edited
        m 2tub "El vendedor respondió: 'Oh, te refieres a... {w=2}{b}¿esto?{/b}'{nw}"
        show mujina zorder 75 at otei_appear(a=1.0,time=0.25)
        play sound "sfx/glitch1.ogg"
        $ mas_resetTextSpeed()
        $ pause(0.4)
        stop sound
        hide mujina
    else:
        m 2tub "El vendedor respondió: 'Oh, ¿te refieres a esto?'."
    m 4wud "El hombre miró al vendedor y vio el mismo vacío espantoso en la chica."
    m "Antes de que el comerciante pudiera escapar, el vacío dejó escapar un chillido agudo..."
    m 1dsc "... Y luego vino la oscuridad."
    show black zorder 100
    $ pause(3.5)
    hide black
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_ubume",
    category=[store.mas_stories.TYPE_SCARY], prompt="El Ubume",unlocked=False),
    code="STY")

label mas_scary_story_ubume:
    call mas_scary_story_setup
    m 3euc "Una noche, a última hora, una mujer entró en una pastelería para comprar dulces justo antes de que el dueño estuviera a punto de irse a la cama."
    m 1esc "El pueblo era pequeño y el pastelero no reconoció a la mujer asi que no le dio mucha importancia."
    m "Con cansancio, vendió a la mujer los dulces que ella pidió."
    m 1euc "La noche siguiente, aproximadamente a la misma hora, la misma mujer entró en la tienda para comprar más dulces."
    m "Continuó visitando la tienda todas las noches, hasta que el pastelero sintió curiosidad por la mujer y decidió seguirla la próxima vez que entrara."
    m 1esd "A la noche siguiente, la mujer llegó a su hora habitual, compró los dulces que siempre hacía y siguió su camino feliz."
    m 3wud "Después de salir por la puerta, el pastelero miró en su caja de dinero y vio las monedas que la mujer le había dado se convirtieron en hojas de un árbol."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,20) == 1) or mas_full_scares:
        play sound "sfx/giggle.ogg"
    m 1euc "Siguió a la mujer hasta el exterior de un templo cercano, donde ella simplemente desapareció."
    m 1esc "El pastelero se sorprendió por esto y decidió regresar a casa."
    m 3eud "Al día siguiente, fue al templo y le contó al monje lo que vio."
    m 1dsd "El sacerdote le dijo al pastelero que una joven que viajaba por el pueblo recientemente había muerto repentinamente en la calle."
    m "El monje sintió compasión por la pobre mujer muerta, lo había hecho en su último mes de embarazo."
    m 1esc "La enterró en el cementerio detrás del templo y les dio a ella y a su hijo un pasaje seguro al más allá."
    m 4eud "Mientras el monje conducía al pastelero al lugar de la tumba, ambos escucharon a un bebé llorando bajo el suelo."
    m "Inmediatamente, buscaron un par de palas y cavaron la tumba."
    m 1wuw "Para su sorpresa, encontraron a un bebé recién nacido chupando un caramelo."
    m "Caramelos que el pastelero siempre le había vendido a la mujer."
    m 1dsd "Sacaron al niño de la tumba y el monje lo tomaría para criarlo."
    m 1esc "Y el fantasma de la mujer nunca más se volvió a ver."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_womaninblack",
    category=[store.mas_stories.TYPE_SCARY], prompt="La mujer de negro",unlocked=False),
    code="STY")

label mas_scary_story_womaninblack:
    call mas_scary_story_setup
    m 3esd "Una noche, un coronel abordó un tren de camino a casa."
    m 1esd "Cuando encontró un lugar cómodo para sentarse, se quedó dormido por la fatiga del día."
    m 3eud "Poco tiempo después, se despertó abruptamente sintiéndose rígido e incómodo."
    m "Para su sorpresa, notó que ahora había una mujer sentada frente a él."
    m "Su atuendo era completamente negro, incluso tenía un velo que oscurecía su rostro."
    m 1esc "Parecía estar mirando algo en su regazo, aunque no había nada allí."
    m 3esd "El coronel era un tipo amistoso y trató de entablar una pequeña charla con ella."
    m 1dsd "Para su consternación, ella no respondió a sus cortesías."
    m 1esc "De repente, comenzó a balancearse hacia adelante y hacia atrás y a cantar una suave canción de cuna."
    m "Antes de que el coronel pudiera preguntar al respecto, el tren se detuvo con un chirrido."
    m "Una maleta del compartimiento de arriba cayó y lo golpeó en la cabeza, dejándolo inconsciente."
    show black zorder 100
    play sound "sfx/crack.ogg"
    $ pause(1.5)
    hide black
    m 3eud "Cuando volvió en sí, la mujer se había ido. El coronel interrogó a algunos de los otros pasajeros, pero ninguno la había visto."
    m 3ekd "Para colmo, una vez que el coronel revisó en el compartimento, estaba cerrado con llave, como de costumbre, y nadie había entrado ni salido del compartimento después de que él entrara."
    m 1esc "Cuando bajó del tren, un funcionario ferroviario que lo escuchó habló con el coronel sobre la mujer por la que estaba preguntando."
    m "Según el funcionario, una mujer y su esposo viajaban juntos en un tren."
    m 1dsd "El marido tenía la cabeza demasiado afuera en una de las ventanas y fue decapitado por un alambre."
    m "Su cuerpo luego cayó sobre su regazo, sin vida."
    m 3wud "Cuando el tren llegó a su parada, la encontraron sosteniendo el cadáver y cantándole una canción de cuna."
    m "Nunca recuperó la cordura y murió poco después."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_resurrection_mary",
    category=[store.mas_stories.TYPE_SCARY], prompt="Resurrección de Mary",unlocked=False),
    code="STY")

label mas_scary_story_resurrection_mary:
    call mas_scary_story_setup
    m 3eua "En un salón de baile alrededor de la época navideña, un joven llamado Lewis estaba disfrutando de un momento con sus amigos, cuando una joven a la que no había visto antes llamó su atención."
    m 1eub "La niña era alta, rubia, de ojos azules y muy hermosa."
    m 1hub "Llevaba un elegante vestido blanco, con zapatos de baile blancos y un chal fino."
    m 3esb "Lewis encontró a la chica cautivadora. Decidió invitarla a bailar con él y ella aceptó su invitación."
    m 1eud "Ciertamente era hermosa, pero Lewis sintió que había algo extraño en ella."
    m 3esd "Mientras bailaban, trató de conocerla un poco mejor, pero todo lo que diría de sí misma era que se llamaba Mary y que era del lado sur de la ciudad."
    m "Además, su piel estaba fría y húmeda al tacto. En un momento durante la noche, besó a Mary y descubrió que sus labios estaban tan fríos como su piel."
    m 1esb "Los dos pasaron gran parte de la noche juntos, bailando. Cuando llegó el momento de partir, Lewis se ofreció llevar a Mary a casa y ella aceptó de nuevo la invitación."
    m 3esb "Ella le indicó que condujera por un camino determinado, y él accedió."
    m 3eud "Cuando pasaban las puertas de un cementerio, Mary le pidió a Lewis que se detuviera."
    m 1eud "Aunque perplejo, Lewis detuvo el automóvil como ella lo solicitó."
    m 3eud "Luego abrió la puerta, se inclinó hacia Lewis y le susurró que tenía que irse y que él no podía ir con ella."
    m 1euc "Salió del coche y caminó hacia la puerta del cementerio antes de desaparecer."
    m "Lewis se sentó en el coche durante mucho tiempo desconcertado por lo que acababa de suceder."
    m 1esd "Nunca volvió a ver a la hermosa mujer."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,20) == 1) or mas_full_scares:
        play sound "sfx/giggle.ogg"
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_corpse",
    category=[store.mas_stories.TYPE_SCARY], prompt="El cadáver resucitado",unlocked=False),
    code="STY")

label mas_scary_story_corpse:
    call mas_scary_story_setup
    m 1esa "Había una vez un anciano que rentaba una antigua posada al borde de la carretera. Una noche, llegaron 4 hombres y pidieron una habitación."
    m 3eua "El anciano respondió que todas las habitaciones estaban ocupadas, pero que podría encontrarles un lugar para dormir si no eran demasiado particulares."
    m 1esa "Los hombres estaban exhaustos y le aseguraron al hombre que cualquier lugar serviría."
    m 1eud "Los condujo a una habitación en la parte de atrás. En la esquina de la habitación estaba el cadáver de una mujer."
    m "Explicó que su nuera había fallecido recientemente y estaba esperando el entierro."
    m 1eua "Después de que el anciano se fue, 3 de los 4 hombres se durmieron. El último hombre no pudo conciliar el sueño."
    m 1wuo "De repente, el hombre escuchó un crujido."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,2) == 1) or mas_full_scares:
        play sound "sfx/crack.ogg"
    m 3wuo "Miró hacia arriba y, a la luz de la lámpara, vio a la mujer levantarse, ahora con colmillos y uñas que parecían garras, avanzando hacia ellos."
    m "Ella se inclinó y mordió a cada uno de los hombres dormidos. El cuarto hombre, en el último segundo, colocó una almohada frente a su cuello."
    m 1eud "La mujer mordió la almohada y aparentemente sin darse cuenta de que no había mordido al último hombre, regresó a su lugar de descanso original."
    m 3eud "El hombre pateó a sus compañeros, pero ninguno se movió. El hombre decidió arriesgarse y huir."
    m 3wuo "Sin embargo, tan pronto como sus pies tocaron el suelo, escuchó otro crujido."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,2) == 1) or mas_full_scares:
        play sound "sfx/crack.ogg"
    m "Al darse cuenta de que la mujer se estaba levantando nuevamente de su lugar, abrió la puerta y corrió lo más rápido que pudo."

    show layer master at heartbeat2(1)
    show vignette as flicker zorder 72 at vignetteflicker(0)
    play sound hb loop
    m 3eud "Después de una corta distancia, miró hacia atrás y vio que el cadáver no estaba muy lejos."
    m 3wud "Se produjo una persecución y cuando ella lo alcanzó, se encontró de pie debajo de un árbol."
    m "Ella cargó hacia él con sus uñas extendidas como garras."
    m 4wud "En el último segundo, el hombre esquivó y ella golpeó el árbol con gran ferocidad."
    m 3wud "Sus uñas ahora estaban profundamente incrustadas en el árbol."
    m 1wud "Ella agitó salvajemente su mano libre hacia el hombre que yacía en el suelo, incapaz de alcanzarlo."
    m 1eud "El hombre, asustado y exhausto, se arrastró una corta distancia y luego se desmayó."
    show layer master
    stop sound
    hide flicker
    show black zorder 100
    $ pause(2.5)
    hide black
    m 1esd "A la mañana siguiente, un oficial de policía que pasaba encontró al hombre y lo devolvió a la conciencia."
    m "El hombre contó lo que había sucedido. El oficial, pensando que el hombre era un borracho, acompañó al hombre de regreso a la posada."
    m 1eud "Cuando llegaron, la posada estaba en un estado de gran conmoción."
    m 3eud "Los 3 viajeros habían sido encontrados muertos en sus camas."
    m "El cuerpo de la nuera yacía donde había estado la noche anterior, pero ahora su ropa estaba manchada de sangre y se encontró un trozo de corteza debajo de su uña."
    m 3esd "Después de algunos interrogatorios, el posadero finalmente admitió que la mujer había muerto seis meses antes y que estaba tratando de ahorrar suficiente dinero para darle un entierro adecuado."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_jack_o_lantern",
    category=[store.mas_stories.TYPE_SCARY], prompt="Jack el de la linterna",unlocked=False),
    code="STY")

label mas_scary_story_jack_o_lantern:
    call mas_scary_story_setup

    $ _mas_jack_scare = (persistent._mas_pm_likes_spoops and renpy.random.randint(1,4) == 1) or mas_full_scares
    m 4esd "Había una vez un hombre llamado Jack. Jack era un viejo borracho miserable que disfrutaba engañar a la gente."
    m 3esa "Una noche, Jack se topó con el diablo y lo invitó a tomar una copa con él."
    m "Después de que Jack se hartó, se dirigió al diablo y le pidió que se convirtiera en una moneda para poder pagar sus bebidas, ya que no tenía dinero para pagarlas."
    m 1esa "Una vez que el diablo lo hizo, Jack se guardó la moneda en el bolsillo y salió sin pagar."
    m "El diablo no pudo volver a su forma original porque Jack se lo había guardado en el bolsillo junto a una cruz de plata."
    m 3esa "Jack finalmente liberó al diablo, con la condición de que no molestaría a Jack durante 1 año y que, si Jack muriese, no reclamaría su alma."
    m "Al año siguiente, Jack volvió a encontrarse con el diablo. Esta vez lo engañó para que se subiera a un árbol y cogiera una fruta."
    m 3esd "Mientras estaba en el árbol, Jack lo rodeó con cruces blancas para que el diablo no pudiera bajar."
    m "Una vez que el diablo prometió no volver a molestarlo durante otros 10 años, Jack se los quitó. Cuando Jack murió, se fue al cielo."
    m 1eud "Cuando llegó, le dijeron que no podía entrar por lo mal que había vivido en la Tierra."
    m 1eua "Entonces, bajó al infierno, donde el diablo cumplió su promesa y no permitió que Jack entrara."
    m 1eud "Jack se asustó, porque no tenía adónde ir."
    m 1esd "Jack le preguntó al diablo cómo podía irse, ya que no había luz."
    if _mas_jack_scare:
        hide vignette
        show darkred zorder 82:
            alpha 0.85
    m 1eud "El diablo arrojó a Jack una brasa de las llamas del infierno para ayudar a Jack a iluminar su camino."
    m "Jack sacó un nabo que tenía consigo, lo talló y colocó la brasa dentro."
    m 3eua "Desde ese día en adelante, Jack vagó por la tierra sin un lugar para descansar, iluminando el camino a medida que avanzaba, lo llamaban Jack el de la linterna."
    if _mas_jack_scare:
        hide darkred
        show vignette zorder 70
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_baobhan_sith",
    category=[store.mas_stories.TYPE_SCARY], prompt="Baobhan Sith",unlocked=False),
    code="STY")

label mas_scary_story_baobhan_sith:
    call mas_scary_story_setup
    m 1esa "Había una vez un grupo de jóvenes cazadores que se detuvieron a pasar la noche en un pequeño pabellón de caza."
    m 3esb "Cuando los jóvenes se acomodaron, encendieron un fuego y comenzaron a comer y beber alegremente, porque había sido un buen día."
    m 1tku "Se decían a sí mismos que lo único que les faltaba era la compañía de unas hermosas mujeres a su lado."
    m 1tsb "No mucho después de que dijeron esto, alguien llamó a su puerta."
    m 3eub "Allí, en la entrada, había cuatro hermosas mujeres."
    m "Las mujeres, habiéndose perdido en el desierto, preguntaron si podían unirse a los hombres en su refugio para pasar la noche."
    m 1tku "Los hombres, felicitándose en silencio por su buena suerte, invitaron a las mujeres a pasar."
    m 1esa "Después de un rato de disfrutar de la compañía del otro, las mujeres expresaron su deseo de bailar."
    m 1tku "Los hombres no perdieron tiempo en acoplarse con cada una de las doncellas."
    m 1eub "Mientras estaban bailando, uno de los hombres se dio cuenta de que las otras parejas bailaban de forma bastante errática."
    m 1wuo "Luego, para su horror, se dio cuenta de que a los otros hombres les salía sangre del cuello a las camisas."
    m 3wuo "En un pánico ciego, el hombre abandonó a su compañero y salió disparado por la puerta, antes de que pudiera compartir el destino de sus amigos."
    m 3wud "Corrió al bosque y se escondió entre los caballos que él y sus amigos habían montado durante la caza de ese día."
    m "Las mujeres, no muy lejos, se acercaron, pero parecían incapaces de pasar los caballos hacia el hombre."
    m 1eud "Así que allí estuvo, con los ojos cansados, entre los animales toda la noche mientras las mujeres daban vueltas alrededor de los caballos, tratando de encontrar una manera de llegar a él."
    m 1esa "Justo antes del amanecer, las mujeres se rindieron y se retiraron al bosque."
    m 1esd "Ahora solo, el hombre se dirigió cautelosamente hacia el pabellón de caza, sin escuchar ningún sonido del interior."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,14) == 1) or mas_full_scares:
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (50,95)
        show blood splatter1 as bl3 zorder 73:
            pos (170,695)
        show blood splatter1 as bl4 zorder 73:
            pos (150,395)
        show blood splatter1 as bl5 zorder 73:
            pos (950,505)
        show blood splatter1 as bl6 zorder 73:
            pos (700,795)
        show blood splatter1 as bl7 zorder 73:
            pos (1050,95)
        $ pause(1.5)
        stop sound
        hide bl2
        hide bl3
        hide bl4
        hide bl5
        hide bl6
        hide bl7
    m 3wuo "Cuando miró adentro, vio a sus tres compañeros muertos en el suelo, con la piel casi traslúcida, yaciendo en un charco de su propia sangre."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_serial_killer",
    category=[store.mas_stories.TYPE_SCARY], prompt="El asesino serial",unlocked=False),
    code="STY")

label mas_scary_story_serial_killer:
    call mas_scary_story_setup
    m 3tub "Una noche una joven pareja estacionó su auto junto a un gran sauce en un cementerio para 'hacer el amor' sin ser molestados."
    m 3euc "Después de un tiempo, fueron interrumpidos por un informe de radio que decía que un notorio asesino en serie había escapado de un hospital psiquiátrico cercano."
    m "Preocupados por su seguridad, decidieron continuar en otro lugar."
    m 1esc "Sin embargo... {w=0.3}el coche no arrancaba en absoluto."
    m 3esd "El joven salió del auto para buscar ayuda y le dijo a la chica que se quedara adentro con las puertas cerradas."
    m 3wud "Unos momentos después, ella se sorprendió cuando escuchó un extraño sonido de arañazos en el techo del auto."
    m 1eud "Pensó para sí misma que debía ser la rama de un árbol en el viento."
    m 1euc "Después de mucho tiempo, pasó un coche de la policía y se detuvo, pero seguía sin ver a su novio."
    m 1eud "El oficial de policía fue al auto y le indicó a la chica que saliera del vehículo y caminara hacia él sin mirar atrás."
    m "Lo hizo lentamente..."
    m 1ekc "La chica entonces notó que muchos otros coches de policía llegaban con sus sirenas a todo volumen detrás del primero en llegar."
    m 1dsd "La curiosidad se apoderó de ella y se volvió para mirar el coche..."
    m 4wfw "Vio a su novio boca abajo y colgando del árbol sobre su auto con el cuello abierto de par en par..."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,8) == 1) or mas_full_scares:
        show y_sticker hopg zorder 74:
            pos (600,425)
            alpha 1.0
            linear 1.6 alpha 0
        play sound "<from 0.4 to 2.0 >sfx/eyes.ogg"
    m 1dfc "... Y sus uñas rotas y ensangrentadas en el techo."
    hide y_sticker
    call mas_scary_story_cleanup
    return

init python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_revenant",
    category=[store.mas_stories.TYPE_SCARY], prompt="El renacido",unlocked=False),
    code="STY")

label mas_scary_story_revenant:
    call mas_scary_story_setup
    m 4eua "Había una vez un hombre que se casó con una mujer."
    m 4ekd "Era una persona rica que ganaba dinero a través de medios mal habidos."
    m 2eud "Poco después de su matrimonio, comenzó a escuchar rumores de que su esposa le estaba siendo infiel."
    m 2esd "Ansioso por averiguar la verdad, el hombre le dijo a su esposa que se iba de viaje de negocios por unos días y salió de la casa."
    m 2eud "Sin que su esposa lo supiera, el hombre se coló de regreso a la casa más tarde en la noche con la ayuda de uno de sus sirvientes."
    m "El hombre se subió a una de las vigas que sobresalían de su dormitorio y se puso al acecho."
    m 4ekd "Poco después entró su esposa con un hombre del barrio, los dos charlaron un rato y luego se empezaron a desnudar."
    m 4eud "El hombre, en ese momento, cayó torpemente al suelo no muy lejos de donde estaban los dos, inconsciente."
    m "El adúltero agarró su ropa y huyó, pero la esposa se acercó a su marido y le acarició suavemente el pelo hasta que se despertó."
    m "El hombre reprendió a su esposa por su adulterio y amenazó con castigarla una vez que se recuperara de su caída."
    m 2dsc "El hombre, sin embargo, nunca se recuperó de su caída y murió durante la noche. Fue enterrado al día siguiente."
    m 2esd "Esa noche, el cadáver del hombre se levantó de su tumba y comenzó a vagar por los vecindarios."
    m "Cuando amaneciera, volvería a su tumba."
    m 3esd "Esto continuó noche tras noche y la gente empezó a cerrar sus puertas con llave, temiendo salir a hacer algún recado después de la puesta del sol."
    m "No sea que se topen con la criatura y sean golpeados hasta quedar negros y azules."
    m 2dsd "No mucho después, la ciudad se vio plagada de enfermedades y no tenían ninguna duda de que el cadáver era el culpable."
    m 2dsc "La gente empezó a huir de la ciudad, no fuera que ellos también murieran por la enfermedad."
    m 2esd "Mientras la ciudad se desmoronaba, se celebró una reunión y se decidió que el cadáver debía desenterrarse y desecharse."
    m "Un grupo de personas tomó palas y encontró el cementerio en el que estaba enterrado el hombre."
    m "No tuvieron que cavar mucho antes de llegar al cadáver del hombre."
    m 4eud "Una vez que fue desenterrado por completo, los aldeanos golpearon el cadáver con sus palas y arrastraron el cuerpo fuera de la ciudad."
    m 3esd "Allí, encendieron un gran fuego y arrojaron el cuerpo al fuego."
    m 3eub "El cadáver del hombre dejó escapar un grito espeluznante e intentó salir de las llamas antes de finalmente sucumbir a él."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_yuki_onna",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Yuki-onna",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_yuki_onna:
    call mas_scary_story_setup
    m 4eud "Había una vez dos leñadores, un padre y un hijo, que se dirigían a casa cuando se desató una tormenta de nieve."
    m "Después de un poco de viaje, se encontraron con una cabaña abandonada y se refugiaron en ella."
    m 2eua "Hicieron una hoguera modesta y se acurrucaron juntos para calentarse antes de quedarse dormidos."
    m 2esd "En medio de la noche, el hijo se despertó con una sacudida."
    m 2wud "Para su sorpresa, una hermosa mujer estaba de pie junto a su padre, soplando su aliento sobre él y congelándolo instantáneamente."
    m 4wud "Cuando se volteó hacia el hijo, hizo una pausa. La mujer le dijo que le evitaría la misma suerte, porque era joven y muy guapo."
    m 4ekc "Si alguna vez le decía una palabra a alguien, ella volvería para matarlo."
    m 4esa "El invierno siguiente, el joven volvía a casa después de un día de cortar leña, cuando se encontró con una hermosa mujer viajera."
    m 2eua "Estaba empezando a nevar y el hombre le ofreció refugio a la mujer de la tormenta, y ella aceptó rápidamente."
    m 2eua "Los dos se enamoraron rápidamente y terminaron casándose."
    m 2hua "Vivieron felices durante años y tuvieron varios hijos con el paso del tiempo."
    m 2esa "Una noche, mientras los niños dormían, la mujer cosía a la luz del fuego."
    m 2eud "El hombre levantó la vista de lo que estaba haciendo y el recuerdo de la noche de la que nunca hablaría volvió a él."
    m "La esposa le preguntó al hombre por qué la miraba de esa manera."
    m 3esc "El hombre contó su historia de su encuentro con la mujer de las nieves."
    m 2wud "La sonrisa en el rostro de su esposa se transformó en ira cuando reveló que ella era la mujer de nieve de la que él hablaba."
    m 4efc "Ella lo reprendió por romper su promesa y lo habría matado si no fuera por el bien de sus hijos."
    m 4efd "Ella le dijo al hombre que era mejor que tratara bien a sus hijos o ella volvería para acabar con él."
    m 4dsd "Al instante siguiente, ella desapareció y nunca más se la volvió a ver."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,3) == 1) or mas_full_scares:
        hide monika
        play sound "sfx/giggle.ogg"
        pause 1.0
        show black zorder 100
        show monika zorder MAS_MONIKA_Z at i11
        $ pause(1.5)
        hide black
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_many_loves",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Muchos amores",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_many_loves:
    call mas_scary_story_setup
    m 4esa "Había una vez una mujer joven que apareció un día en un pueblo para encontrar marido."
    m 4eua "Era muy hermosa y rápidamente atrajo a muchos pretendientes."
    m 2eua "Eventualmente se estableció con un pescador fornido."
    m 2esd "Los dos tuvieron un matrimonio feliz, pero en menos de un año, el esposo se consumió y murió."
    m "La gente del pueblo sintió lástima por la joven y la consoló lo mejor que pudo."
    m 4esa "Unos meses más tarde, la mujer se casó con un leñador corpulento."
    m 4dsd "Los dos vivieron felices juntos durante un tiempo, pero él también se marchitó y murió."
    m 4eud "Algunos de los aldeanos pensaron que era extraño que ambos esposos hubieran muerto de la misma manera, pero nadie dijo nada y consolaron a la chica por su mala suerte."
    m 2esc "Un tiempo después, la mujer se volvió a casar, esta vez con un robusto albañil y ellos también parecían tener un matrimonio feliz, pero al cabo de un año, la mujer volvía a ser viuda."
    m "Esta vez los aldeanos hablaron entre ellos y sintieron que algo sospechoso estaba sucediendo, por lo que un grupo de aldeanos se dispuso a buscar al chamán más cercano."
    m "Una vez que encontraron al chamán y le contaron su historia, el chamán indicó que sabía lo que estaba pasando."
    m 3euc "Llamó a su asistente, un tipo joven y bien formado, le susurró al oído y lo envió de regreso con los aldeanos."
    m "Diciéndoles que no se preocuparan, su asistente llegaría al fondo del asunto."
    m 2esc "Cuando regresaron al pueblo, el asistente visitó a la viuda y poco después se casaron."
    m 2efc "La noche de su boda, el asistente colocó un cuchillo debajo de su almohada y fingió dormir."
    m 2esd "Poco después de la medianoche, el hombre sintió una presencia sobre él y un pinchazo en el cuello."
    m 2dfc "El hombre agarró el cuchillo y lo clavó en la cosa que tenía encima."
    if (renpy.random.randint(1,20) == 1 and persistent._mas_pm_likes_spoops) or mas_full_scares:
        show monika 6ckc
        show mas_stab_wound zorder 75
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (590,485)
        $ pause(1.5)
        stop sound
        hide bl2
        hide mas_stab_wound
        show black zorder 100
        $ pause(1.5)
        hide black
    m 3wfc "Escuchó un chillido y el batir de alas cuando la criatura voló por una ventana."
    m 1dfc "Al día siguiente, la novia fue encontrada muerta a cierta distancia de la casa con una herida de cuchillo en el pecho."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_gray_lady",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="La dama gris",
            unlocked=False
        ),
    code="STY"
    )

label mas_scary_story_gray_lady:
    call mas_scary_story_setup
    m 4eua "Había una vez un hombre llamado William, que creció ayudando a su padre en sus infames hazañas."
    m 4ekd "Como agitar luces desde la línea de la costa en medio de la noche, esperando atraer a los barcos para que naufraguen en las traicioneras rocas de la costa."
    m 2ekc "Y luego recoger el botín que se derramó de la nave y matar a los sobrevivientes."
    m 2eud "Durante una de las demostraciones de su padre, salvó a una bella mujer y finalmente decidió dejar atrás su antigua vida y casarse con ella."
    m 2esa "La pareja alquiló una mansión no muy lejos."
    m 2hub "Los dos vivieron juntos una vida feliz allí, pero se alegraron especialmente cuando nació su hija Kate."
    m 4esa "Con el paso de los años, Kate se convirtió en una joven vivaz."
    m 2ekc "William estaba secretamente avergonzado de no tener suficiente dinero para comprar la mansión y ofrecerla como dote al hombre que se casaría con su hija."
    m 4hub "Entonces, un día, Kate conoció y se enamoró de un capitán pirata irlandés y los dos se casaron."
    m 4esb "La feliz pareja decidió establecerse en Dublín, ya que los padres de Kate no tenían una tierra propia que ofrecerles."
    m 4eua "Kate prometió volver a visitar a sus padres algún día."
    m 4esd "Pasó el tiempo y William y su esposa echaban mucho de menos a su hija y deseaban que volviera."
    m 2dkc "William decidió volver a sus viejas costumbres el tiempo suficiente para conseguir el dinero necesario para comprar la mansión e invitar a su hija y su marido a vivir con ellos."
    m 4wud "Una noche, después de atraer un barco para que naufragara en la orilla y recoger el botín, vio a una mujer gravemente herida tendida en las rocas frente a él."
    m 2wuc "Sus rasgos faciales quedaron irreconocibles debido a las heridas que había sufrido."
    m 2ekc "William, compadeciéndose de ella, la llevó de regreso a la mansión e hizo lo que pudo para tratar de salvar su vida, pero la mujer murió sin recuperar el conocimiento."
    m 2eud "Mientras buscaban en su cuerpo alguna pista sobre su identidad, encontraron un pequeño bolso atado a su cintura lleno de suficientes monedas de oro y joyas para que finalmente pudieran comprar la mansión que alquilaron."
    m 2dsc "Unos días después, el Almirantazgo preguntó a la pareja sobre un pasajero desaparecido de los restos del naufragio que resultó ser nada menos que su hija."
    m 3dsd "Devastados y avergonzados, los padres encerraron sus restos en una habitación secreta y se mudaron, para no volver nunca más."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="La linterna floreada",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern:
    call mas_scary_story_setup

    if not mas_getEVL_shown_count("mas_scary_story_flowered_lantern"):
        m 3eub "Antes de empezar, necesito decirte que mi próxima historia será un poco larga."
        m 3eua "Entonces, lo dividiré en partes."
        m "Una vez que termine esta parte te preguntaré si quieres continuar o no."
        m 1eub "Si dices que no, puedes pedirme más tarde que te cuente la siguiente parte, así que no te preocupes."
        m 4hua "Muy bien, comencemos ahora."

    m 4eua "Había una vez una hermosa y joven doncella llamada Tsuyu, cuyo padre era un samurái de alto rango."
    m 4eud "La madre de Tsuyu había muerto y su padre se volvió a casar."
    m 2euc "Aunque fue obvio para el padre de Tsuyu que ella y su madrastra no se llevaban bien."
    m 2esa "Queriendo asegurar la felicidad de su única hija, mandó construir una lujosa casa para ella, lejos de ellos y la hizo mudarse."
    m "Un día, el médico de la familia fue a la residencia de Tsuyu en una visita de rutina con un joven samurai llamado Hagiwara, que era muy guapo."
    m 4eub "Tsuyu y Hagiwara se enamoraron en el momento en que se miraron."
    m 4esc "Sin que el doctor lo supiera, los dos se comprometieron el uno al otro de por vida y antes de que los dos se fueran."
    m 4dsd "Tsuyu le susurró a Hagiwara que seguramente moriría si él no volvía a verla."
    m 2esc "Hagiwara no olvidó sus palabras, pero la etiqueta le prohibió hacer una llamada para visitar a una doncella a solas, por lo que tuvo que esperar a que el médico le pidiera que se uniera a él en otra visita."
    m 2dsd "El doctor, sin embargo, había percibido su repentino afecto por Tsuyu."
    m 4ekc "Se sabía que el padre de Tsuyu decapitaba a quienes lo enojaban, y temiendo que lo hiciera responsable de presentarlos a los dos, evitó a Hagiwara."
    m 2rkc "Pasaron los meses y Tsuyu, sintiéndose despreciada porque Hagiwara la había abandonado, falleció."
    m 1ekc "No mucho después, el médico se topó con Hagiwara y le informó de la muerte de Tsuyu."
    m 1dsd "Hagiwara se entristeció profundamente y lloró mucho por ella, rezando y quemando incienso por ella."

    $ mas_setEVLPropValues("mas_scary_story_flowered_lantern_2", unlocked=True, pool=False)

    m 1hua "... ¡Y hasta aquí la primera parte! ¿Quieres continuar con la siguiente?{nw}"
    $ _history_list.pop()
    menu:
        m "... ¡Y hasta aquí la primera parte! ¿Quieres continuar con la siguiente?{fast}"
        "Sí":
            jump mas_scary_story_flowered_lantern_2
        "No":
            pass
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern_2",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="La linterna floreada 2",
            pool=True,
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern_2:
    call mas_scary_story_setup
    $ _mas_lantern_scare = renpy.random.randint(1,11) == 1
    m 4ekd "Después de la puesta del sol, en la primera noche del Festival de los Muertos, Hagiwara se sentó afuera, todavía afligido por la pérdida de su amor hasta la noche."
    m 2eud "Sin embargo, justo cuando estaba a punto de entrar y dormir, escuchó pasos en el camino fuera de su puerta."
    m 4euc "Hagiwara vivía en una calle solitaria con pocos peatones y como ya era tan tarde, decidió ver quién era."
    m 4wub "Para su gran sorpresa y alegría, la persona que caminaba por el sendero no era otra que Tsuyu, que llevaba una linterna de papel decorada con flores para iluminar su camino."
    m 1hua "Hagiwara gritó el nombre de Tsuyu y ella inmediatamente se acercó a él y lo abrazó."
    m 1eua "Cada uno le dijo al otro que el médico les había dicho que la otra persona había muerto."
    m "Tsuyu le dijo que su padre quería que se casara con otro hombre."
    m 3eub "Ella se negó y huyó de su lujosa casa para esconderse de él y actualmente estaba viviendo en una casa estrecha en cierto vecindario cercano."
    m 3eua "La invitó a entrar, pero le dijo que se quedara callada para que no molestaran a su sirviente, que podría preguntar quién era ella."
    m 4eua "Los dos pasaron la noche juntos y justo antes del amanecer, Tsuyu se fue para regresar a su vivienda."
    m 4esa "A la noche siguiente, Tsuyu volvió a visitar a la misma hora que había llegado la noche anterior."
    m 2euc "Esta vez, el sirviente de Hagiwara se despertó y escuchó la voz de una mujer joven que no reconoció."
    m 4esd "Curioso, pero sin querer molestar a su amo, se coló en la habitación de su amo y se asomó por una pequeña rendija en su puerta y vio que efectivamente estaba hablando con una mujer joven."
    m 4eud "La mujer estaba de espaldas a él, pero pudo distinguir que estaba muy delgada y vestía un kimono muy elegante que solo usaría la clase alta."
    m 4esc "Su curiosidad despertó, el sirviente decidió echar un vistazo a la cara de esta chica antes de retirarse."
    m 2dsc "Vio que el maestro había dejado una ventana abierta, así que silenciosamente se dirigió hacia ella."
    m 4wuw "Mientras miraba dentro, vio con horror que el rostro de la mujer era uno que llevaba mucho tiempo muerta y que los dedos que acariciaban el rostro de su amo eran de huesos desnudos."
    m 2wfd "Huyó aterrorizado sin hacer ruido."
    m 1efc "A la mañana siguiente, el sirviente se acercó a su amo y le preguntó por la mujer."
    m 4efd "Al principio, Hagiwara negó tener visitas, pero después de percibir que fue en vano, confesó todo lo que había sucedido."
    m 4ekc "El sirviente le contó a Hagiwara lo que vio la noche anterior y sintió que seguramente la vida de su amo estaba en peligro y le suplicó que viera a un monje."
    m 2euc "Sorprendido pero no del todo convencido, Hagiwara decidió tranquilizar a su sirviente al encontrar la residencia de Tsuyu."
    m "Hagiwara partió y exploró el vecindario en el que Tsuyu le dijo que se estaba quedando."
    m 2esc "Miró a su alrededor y preguntó a la gente por ella, pero fue en vano."
    m 4dsd "Cuando decidió que buscar más sería infructuoso, se dirigió a casa."
    m 4eud "En su camino de regreso, pasó por un cementerio junto a un templo."
    m "Su atención fue atraída por una gran tumba nueva, cerca de la parte de atrás, que no había notado antes."
    if _mas_lantern_scare or persistent._mas_pm_likes_spoops or mas_full_scares:
        show mas_lantern zorder 75 at right
    m 4euc "Colgando encima había una linterna de papel decorada con hermosas flores que se veían exactamente iguales a la que Tsuyu llevaba con ella por la noche."
    m 4wuc "Intrigado, caminó hacia la tumba, mientras miraba el nombre de la persona a la que pertenecía, saltó hacia atrás con miedo al leer que pertenecía a su amada Tsuyu."
    m 2wkc "Aterrorizado, Hagiwara se dirigió inmediatamente al templo vecino y pidió hablar con el monje principal."
    m 4esc "Cuando fue admitido, le contó al monje todo lo que había sucedido."
    m 4esd "Una vez que terminó, el monje le dijo que su vida estaba en peligro."
    m "El intenso dolor de Hagiwara por ella y su intenso amor por él la había traído de vuelta durante el Festival de los Muertos."
    m 4dsc "El amor entre uno que está vivo y uno que está muerto solo puede resultar en la muerte del que está vivo."
    if _mas_lantern_scare or persistent._mas_pm_likes_spoops or mas_full_scares:
        hide mas_lantern

    $ mas_setEVLPropValues("mas_scary_story_flowered_lantern_3", unlocked=True, pool=False)

    m 1hua "... ¡Y eso es todo por la segunda parte! ¿Quieres continuar con la siguiente?{nw}"
    $ _history_list.pop()
    menu:
        m "... ¡Y eso es todo por la segunda parte! ¿Quieres continuar con la siguiente?{fast}"
        "Sí":
            jump mas_scary_story_flowered_lantern_3
        "No":
            pass
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern_3",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="La linterna floreada 3",
            pool=True,
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern_3:
    call mas_scary_story_setup
    $ _mas_rects_scare = (renpy.random.randint(1,11) == 1 and persistent._mas_pm_likes_spoops) or mas_full_scares
    m 1eud "Como era el último día del Festival de los Muertos, Tsuyu tendría que regresar con los muertos esta noche y, si se volvieran a ver, se llevaría a Hagiwara."
    m 3esd "Hagiwara le suplicó al monje que lo ayudara."
    m 3esc "El monje dijo que el karma pasional entre ellos era muy fuerte, pero que todavía había algo de esperanza."
    m "Le entregó a Hagiwara una pila de talismanes de papel que mantienen alejados a los espíritus y le indicó que con ellas cubriera todas las aberturas de su casa, sin importar cuán pequeñas fueran."
    m 1esd "Tsuyu no podría entrar a la vivienda mientras siguiera estas instrucciones."
    m 2esa "Hagiwara, con la ayuda de su sirviente, pudo cubrir con éxito la casa con los talismanes de papel antes del anochecer."
    m 4esc "A medida que avanzaba la noche, Hagiwara intentó conciliar el sueño, pero fue en vano. Así que se sentó a meditar sobre los acontecimientos recientes."
    m 2dsd "A última hora, escuchó pasos fuera de su casa."
    m "Los pasos se acercaban cada vez más."
    m 4wkc "Hagiwara sintió una repentina compulsión, más fuerte incluso que su miedo, de mirar."
    m 4wkd "Se acercó tontamente a las contraventanas y por una rendija vio a Tsuyu parada en la entrada de su casa con su linterna de papel mirando los talismanes de papel."
    m "Nunca antes había visto a Tsuyu lucir tan hermosa y su corazón se sintió tan atraído por ella."
    m 2ekd "Afuera, Tsuyu comenzó a llorar amargamente, diciéndose a sí misma que Hagiwara había roto la promesa que se habían hecho."
    m 4eud "Lloró hasta recobrarse y dijo en voz alta que no se iría sin verlo por última vez."
    m 4esd "Hagiwara escuchó pasos mientras caminaba por su casa, de vez en cuando veía la luz de la linterna a medida que avanzaba."
    m 2wud "Cuando ella se acercó al lugar por el que él había mirado, los pasos se detuvieron y de repente Hagiwara vio uno de los ojos de Tsuyu mirándolo."
    if _mas_rects_scare:
        play sound "sfx/glitch1.ogg"
        show rects_bn1 zorder 80
        show rects_bn2 zorder 80
        show rects_bn3 zorder 80
        pause 0.5
        $ style.say_dialogue = style.edited
        ".{w=0.7}.{w=0.9}.{w=0.9}{nw}"
        $ mas_resetTextSpeed()
        stop sound
        hide rects_bn1
        hide rects_bn2
        hide rects_bn3
        show black zorder 100
        $ pause(1.5)
        hide black
    m 2dsc "Al día siguiente, el sirviente despertó y se acercó a la habitación de su amo y llamó a su puerta."
    m 4ekc "Por primera vez en años no recibió respuesta y estaba preocupado."
    m 2dsd "Llamó a su maestro repetidamente, pero fue en vano."
    m 2esc "Finalmente, con un poco de coraje, entró en la habitación de su amo."
    m 4wuw "... Solo para huir de la casa llorando de horror después de verlo."
    m "Hagiwara estaba muerto, horriblemente muerto, y su rostro tenía la expresión de la mayor agonía de miedo..."
    m 2wfc "Y a su lado, en la cama, estaban los huesos de una mujer con sus brazos alrededor de su cuello como en un abrazo."
    call mas_scary_story_cleanup
    return

init python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_prison_escape",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Fuga de la prisión",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_prison_escape:
    call mas_scary_story_setup
    m 1ekd "Una mujer hermosa cumplía una condena de por vida en prisión por asesinato."
    m 2tfc "Enojada y resentida por su situación, decidió que no podía pasar toda su vida en la cárcel. {w=0.2}Asi que comenzó a idear maneras de escapar."
    m 7eua "Con el tiempo, se hizo buena amiga de uno de los guardias de la prisión."
    m 3esc "Su trabajo era enterrar a los prisioneros que morían en un cementerio justo fuera de los muros de la prisión."
    m 3esd "Cada vez que un prisionero moría, el guardia tocaba una campana que era escuchada por todos los reclusos."
    m 3esc "Luego, tomaba el cuerpo y lo colocaba en un ataúd, luego ingresaba a su oficina para llenar el certificado de defunción antes de regresar para clavar la tapa del ataúd."
    m 3esd "Finalmente, lo colocaba en un carro para llevarlo al cementerio y enterrarlo."
    m 1euc "Conociendo esta rutina, la mujer ideó un plan de escape y lo compartió con el guardia..."
    m 1eud "La próxima vez que sonara la campana, la mujer saldría de su celda y se colaría en la habitación oscura donde se guardaban los ataúdes."
    m 1eud "Se deslizaría dentro del ataúd con el cuerpo sin vida mientras el guardia llenaba el certificado de defunción."
    m 3euc "Cuando el guardia regresara, clavaría la tapa y llevaría el ataúd fuera de la prisión para enterrarlo."
    m 3euc "La mujer sabía que habría suficiente aire para respirar hasta más tarde en la noche, cuando el guardia regresaría bajo el manto de la oscuridad, desenterraría el ataúd y la liberaría."
    m 2eksdlc "El guardia dudaba en seguir este plan, {w=0.1}{nw}"
    extend 4esa "pero como él y la mujer se habían vuelto buenos amigos a lo largo de los años, aceptó hacerlo."
    m 2tsc "La mujer esperó varios meses a que uno de los otros reclusos muriera."
    m 7dsc "Una noche, estaba dormida en su celda cuando escuchó sonar la campana de la muerte."
    m 3euc "Se levantó, abrió la cerradura de su celda y caminó lentamente por el pasillo."
    m 3wud "Casi la atrapan un par de veces... {w=0.3}su corazón latía tan rápido."
    m 3ekc "Abrió la puerta de la habitación oscura donde se guardaban los ataúdes y encontró silenciosamente el que contenía el cuerpo sin vida."
    m 3dkc "Después de subir cuidadosamente, cerró la tapa para esperar a que el guardia viniera a clavarla."
    m 2eka "Pronto escuchó pasos y el golpeteo del martillo y los clavos."
    m 4eksdlc "Aunque estaba muy incómoda en el ataúd con el cuerpo sin vida debajo de ella, sabía que con cada clavo estaba un paso más cerca de la libertad."
    m 2eud "El ataúd fue levantado en el carro y llevado afuera al cementerio."
    m 2eksdlc "No emitió ningún sonido mientras el ataúd golpeaba el fondo de la tumba con un ruido sordo."
    m 4eksdlc "Finalmente, escuchó la tierra caer sobre la parte superior del ataúd de madera, {w=0.1}{nw}"
    extend 4eksdla "y sabía que solo era cuestión de tiempo hasta que por fin fuera libre."
    m 2hksdlb "Después de una hora de silencio absoluto, comenzó a reírse en voz baja."
    m 2eta "Curiosa, decidió encender una cerilla para descubrir la identidad del prisionero muerto a su lado."
    m 2wusdld "¡...!"
    m 2wusdlo "¡Era el guardia muerto!"
    call mas_scary_story_cleanup
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
