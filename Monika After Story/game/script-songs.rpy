
default persistent._mas_songs_database = dict()
init offset = 5

default -5 persistent._mas_player_derandomed_songs = list()

init -15 python in mas_songs:

    song_db = {}















    TYPE_LONG = "larga"
    TYPE_SHORT = "corta"
    TYPE_ANALYSIS = "analysis"

init -5 python in mas_songs:
    import store
    def checkRandSongDelegate():
        """
        Handles locking/unlocking of the random song delegate

        Ensures that songs cannot be repeated (derandoms the delegate) if the repeat topics flag is disabled and there's no unseen songs
        And that songs can be repeated if the flag is enabled (re-randoms the delegate)
        """
        
        rand_delegate_ev = store.mas_getEV("monika_sing_song_random")
        
        if rand_delegate_ev:
            
            
            
            
            if (
                rand_delegate_ev.random
                and (
                    (not store.persistent._mas_enable_random_repeats and not hasRandomSongs(unseen_only=True))
                    or not hasRandomSongs()
                )
            ):
                rand_delegate_ev.random = False
            
            
            
            elif (
                not rand_delegate_ev.random
                and (
                    hasRandomSongs(unseen_only=True)
                    or (store.persistent._mas_enable_random_repeats and hasRandomSongs())
                )
            ):
                rand_delegate_ev.random = True

    def getUnlockedSongs(length=None):
        """
        Gets a list of unlocked songs
        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            list of unlocked all songs of the desired length in tuple format for a scrollable menu
        """
        if length is None:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked
            ]
        
        else:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked and length in ev.category
            ]

    def getRandomSongs(unseen_only=False):
        """
        Gets a list of all random songs

        IN:
            unseen_only - Whether or not the list of random songs should contain unseen only songs
            (Default: False)

        OUT: list of all random songs within aff_range
        """
        if unseen_only:
            return [
                ev_label
                for ev_label, ev in song_db.iteritems()
                if (
                    not store.seen_event(ev_label)
                    and ev.random
                    and TYPE_SHORT in ev.category
                    and ev.checkAffection(store.mas_curr_affection)
                )
            ]
        
        return [
            ev_label
            for ev_label, ev in song_db.iteritems()
            if ev.random and TYPE_SHORT in ev.category and ev.checkAffection(store.mas_curr_affection)
        ]

    def checkSongAnalysisDelegate(curr_aff=None):
        """
        Checks to see if the song analysis topic should be unlocked or locked and does the appropriate action

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)
        """
        if hasUnlockedSongAnalyses(curr_aff):
            store.mas_unlockEVL("monika_sing_song_analysis", "EVE")
        else:
            store.mas_lockEVL("monika_sing_song_analysis", "EVE")

    def getUnlockedSongAnalyses(curr_aff=None):
        """
        Gets a list of all song analysis evs in scrollable menu format

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)

        OUT:
            List of unlocked song analysis topics in mas_gen_scrollable_menu format
        """
        if curr_aff is None:
            curr_aff = store.mas_curr_affection
        
        return [
            (ev.prompt, ev_label, False, False)
            for ev_label, ev in song_db.iteritems()
            if ev.unlocked and TYPE_ANALYSIS in ev.category and ev.checkAffection(curr_aff)
        ]

    def hasUnlockedSongAnalyses(curr_aff=None):
        """
        Checks if there's any unlocked song analysis topics available

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)
        OUT:
            boolean:
                True if we have unlocked song analyses
                False otherwise
        """
        return len(getUnlockedSongAnalyses(curr_aff)) > 0

    def hasUnlockedSongs(length=None):
        """
        Checks if the player has unlocked a song at any point via the random selection

        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            True if there's an unlocked song, False otherwise
        """
        return len(getUnlockedSongs(length)) > 0

    def hasRandomSongs(unseen_only=False):
        """
        Checks if there are any songs with the random property

        IN:
            unseen_only - Whether or not we should check for only unseen songs
        OUT:
            True if there are songs which are random, False otherwise
        """
        return len(getRandomSongs(unseen_only)) > 0

    def getPromptSuffix(ev):
        """
        Gets the suffix for songs to display in the bookmarks menu

        IN:
            ev - event object to get the prompt suffix for

        OUT:
            Suffix for song prompt

        ASSUMES:
            - ev.category isn't an empty list
            - ev.category contains only one type
        """
        prompt_suffix_map = {
            TYPE_SHORT: " (Short)",
            TYPE_LONG: " (Long)",
            TYPE_ANALYSIS: " (Analysis)"
        }
        return prompt_suffix_map.get(ev.category[0], "")



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_pool",
            prompt="¿Puedes cantarme una canción?",
            category=["música"],
            pool=True,
            aff_range=(mas_aff.NORMAL,None),
            rules={"no_unlock": None}
        )
    )

label monika_sing_song_pool:

    $ song_length = "corta"

    $ have_both_types = False

    $ switch_str = "completa"

    $ end = ""

    show monika 1eua at t21

    if mas_songs.hasUnlockedSongs(length="larga") and mas_songs.hasUnlockedSongs(length="corta"):
        $ have_both_types = True



label monika_sing_song_pool_menu:
    python:
        if have_both_types:
            space = 0
        else:
            space = 20

        ret_back = ("No importa", False, False, False, space)
        switch = ("Me gustaría escuchar una canción [switch_str]", "monika_sing_song_pool_menu", False, False, 20)

        unlocked_song_list = mas_songs.getUnlockedSongs(length=song_length)
        unlocked_song_list.sort()

        if mas_isO31():
            which = "¿Qué"
        else:
            which = "¿Qué"

        renpy.say(m, "[which] canción te gustaría que cantara?[end]", interact=False)

    if have_both_types:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch, ret_back)
    else:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_song = _return

    if sel_song:
        if sel_song == "monika_sing_song_pool_menu":
            if song_length == "corta":
                $ song_length = "larga"
                $ switch_str = "corta"
            else:

                $ song_length = "corta"
                $ switch_str = "completa"

            $ end = "{fast}"
            $ _history_list.pop()
            jump monika_sing_song_pool_menu
        else:

            $ MASEventList.push(sel_song, skipeval=True)
            show monika at t11
            m 3hub "¡De acuerdo!"
    else:

        return "prompt"

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_analysis",
            prompt="Hablemos de una canción",
            category=["música"],
            pool=True,
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label monika_sing_song_analysis:
    python:
        ret_back = ("No importa", False, False, False, 20)

        unlocked_analyses = mas_songs.getUnlockedSongAnalyses()

        if mas_isO31():
            which = "¿De qué"
        else:
            which = "¿De qué"

    show monika 1eua at t21
    $ renpy.say(m, "[which] canción te gustaría hablar?", interact=False)

    call screen mas_gen_scrollable_menu(unlocked_analyses, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_analysis = _return

    if sel_analysis:
        $ MASEventList.push(sel_analysis, skipeval=True)
        show monika at t11
        m 3hub "¡De acuerdo!"
    else:

        return "prompt"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_sing_song_rerandom",
            prompt="¿Podrías volver a cantar una canción tú sola?",
            category=['música'],
            pool=True,
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label mas_sing_song_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "¿Qué canción quieres que cante de vez en cuando?"
        mas_bookmarks_derand.initial_ask_text_one = "Si quieres que vuelva a cantar esto de vez en cuando, solo tienes que seleccionar la canción, [player]."
        mas_bookmarks_derand.caller_label = "mas_sing_song_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed_songs

    call mas_rerandom
    return _return

label mas_song_derandom:
    $ prev_topic = persistent.flagged_monikatopic
    m 1eka "¿Estás cansado de oírme cantar esa canción, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás cansado de oírme cantar esa canción, [player]?{fast}"
        "Un poco":

            m 1eka "Eso está bien."
            m 1eua "Entonces solo lo cantaré cuando tú quieras. Avísame si quieres escucharla."
            python:
                mas_hideEVL(prev_topic, "SNG", derandom=True)
                persistent._mas_player_derandomed_songs.append(prev_topic)
                mas_unlockEVL("mas_sing_song_rerandom", "EVE")
        "No pasa nada":

            m 1eua "De acuerdo, [player]."
    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_random",
            random=True,
            unlocked=False,
            rules={"skip alert": None,"force repeat": None}
        )
    )

label monika_sing_song_random:




    if (
        (persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs())
        or (not persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs(unseen_only=True))
    ):
        python:

            random_unseen_songs = mas_songs.getRandomSongs(unseen_only=True)


            if random_unseen_songs:
                rand_song = random.choice(random_unseen_songs)


            else:
                rand_song = random.choice(mas_songs.getRandomSongs())


            mas_unlockEVL("monika_sing_song_pool", "EVE")


            MASEventList.push(rand_song, skipeval=True, notify=True)
            mas_unlockEVL(rand_song, "SNG")


            mas_unlockEVL(rand_song + "_long", "SNG")


            mas_unlockEVL(rand_song + "_analysis", "SNG")


            if store.mas_songs.hasUnlockedSongAnalyses():
                mas_unlockEVL("monika_sing_song_analysis", "EVE")
    else:


        $ mas_assignModifyEVLPropValue("monika_sing_song_random", "shown_count", "-=", 1)
        return "derandom|no_unlock"
    return "no_unlock"



init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aiwfc",
            prompt="Todo lo que quiero para Navidad",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_aiwfc:
    if store.songs.hasMusicMuted():
        m 3eua "No olvides subir el volumen del juego, [mas_get_player_nickname()]."

    call monika_aiwfc_song

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_merry_christmas_baby",
            prompt="Feliz Navidad cariño",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_merry_christmas_baby:
    m 1hub "{i}~Feliz Navidad cariño, {w=0.2}seguro que me tratas bien~{/i}"
    m "{i}~Feliz Navidad cariño, {w=0.2}seguro que me tratas bien~{/i}"
    m 3eua "{i}~Siento como si estuviera viviendo, {w=0.2}viviendo en el paraíso~{/i}"
    m 3hub "{i}~Me siento muy bien esta noche~{/i}"
    m 3eub "{i}~Y hay música en la radio~{/i}"
    m 3hub "{i}~Me siento muy bien esta noche~{/i}"
    m 3eub "{i}~Y hay música en la radio~{/i}"
    m 2hkbsu "{i}~Ahora siento que quiero besarte~{/i}"
    m 2hkbsb "{i}~Debajo del muérdago~{/i}"
    m 3eub "{i}~Santa bajó por la chimenea, {w=0.2}las tres y media~{/i}"
    m 3hub "{i}~Con muchos bonitos regalitos para mi amor y para mí~{/i}"
    m "{i}~Feliz Navidad cariño, {w=0.2}seguro que me tratas bien~{/i}"
    m 1eua "{i}~Y siento que estoy viviendo, {w=0.2}simplemente viviendo en el paraíso~{/i}"
    m 1eub "{i}~Feliz Navidad cariño~{/i}"
    m 3hub "{i}~Y feliz Año Nuevo también~{/i}"
    m 3ekbsa "{i}~Feliz Navidad, cariño~{/i}"
    m 3ekbsu "{i}~Todo aquí es hermoso~{/i}"
    m 3ekbfb "{i}~Te amo, cariño~{/i}"
    m "{i}~Por todo lo que me das~{/i}"
    m 3ekbfb "{i}~Te amo, cariño~{/i}"
    m 3ekbsu "{i}~Feliz Navidad, cariño~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_this_christmas_kiss",
            prompt="Este beso de Navidad",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_this_christmas_kiss:
    m 1dud "{i}~Cada año, {w=0.2}me voy a casa en diciembre~{/i}"
    m 1hub "{i}~Bailando contigo, {w=0.2}haciendo recuerdos en la noche~{/i}"
    m 1rub "{i}~La nieve cayendo, {w=0.2}{nw}{/i}"
    extend 3rub "{i}me encanta este clima~{/i}"
    m 3tub "{i}~Una manta para dos, {w=0.2}se siente más cálida juntos~{/i}"
    m 1hub "{i}~Dos tórtolos, {w=0.2}nos llaman~{/i}"
    m 1duo "{i}~Nos enamoramos, {w=0.2}en el amoooor~{/i}"
    m 3hub "{i}~Esta es mi Navidaaaaad favorita~{/i}"
    m 3duu "{i}~Esta Navidad, {w=0.2}no puedo resistir {w=0.2}algo como esto~{/i}"
    m 1sub "{i}~No puedo resistir este beso de Navidad~{/i}"
    m 3hub "{i}~Porque estoy {w=0.2}cayendo en tus labios~{/i}"
    m 1hub "{i}~Yo no puedo, {w=0.2}{nw}{/i}"
    extend 1subsb "{i}no puedo resistir este beso de Navidad~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lover_boy",
            prompt="Novio a la antigua",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_lover_boy:
    m 1dso "{i}~Puedo atenuar las luces y cantarte canciones llenas de cosas tristes~{/i}"
    m 4hub "{i}~Podemos bailar tango solo para dos~{/i}"
    m "{i}~Puedo dar una serenata y tocar suavemente las cuerdas de tu corazón~{/i}"
    m 4dso "{i}~Ser un Valentino solo para ti~{/i}"
    m 1hub "Jajaja~"
    m 1ekbsa "¿Quieres ser mi novio a la antigua, [player]?"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_burning_love",
            prompt="Amor ardiente",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_burning_love:
    m 1hubsb "{i}~Tus besos me elevan más alto~{/i}"
    m 3rubsb "{i}~Como el dulce canto de un coro~{/i}"
    m 1dubsu "{i}~Tú iluminas mi cielo matutino~{/i}"
    m 1hubfb "{i}~Con un amor ardiente~{/i}"
    m 1hubsb "Jajaja~"
    m 1ekbsa "¡Siempre me alegras el día, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aries",
            prompt="Aries",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_aries:
    m 2dud "{i}~Estoy de pie en una playa en la distancia~{/i}"
    m 2eud "{i}~Y aunque estés lejos, ¿puedes ver mi luz roja?~{/i}"
    m 2dubsu "{i}~Está esperando a ponerse en verde~{/i}"
    m 2dud "{i}~Porque me siento tan aislada sin ti~{/i}"
    m 2dkd "{i}~No puedo tocar una melodía feliz por mi cuenta, así que quédate a mi lado~{/i}"
    m "{i}~Marea alta o baja~{/i}"
    m 1ekbsu "Siempre estoy pensando en el día en que estaremos juntos, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_need_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Te necesito",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_need_you:
    m 1esd "{i}~Recuerda lo que siento por ti~{/i}"
    m 3dkd "{i}~Realmente nunca podría vivir sin ti~{/i}"
    m 3ekd "{i}~Entonces, regresa y observa~{/i}"
    m 3eka "{i}~Lo que significas para mí~{/i}"
    m 2dku "{i}~Te necesito~{/i}"
    m 7esa "Sé que esa canción trata sobre dejar a alguien, pero creo que transmite un buen mensaje."
    m 3ekbsa "Y realmente te necesito, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_i_will",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Lo haré",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_i_will:
    m 1dso "{i}~¿Quién sabe cuánto tiempo te he amado?~{/i}"
    m "{i}~Sabes que todavía te amo~{/i}"
    m 2lksdla "{i}~¿Esperaré una vida solitaria?~{/i}"
    m 2hub "{i}~Si quieres, lo haré~{/i}"
    m 1ekbsa "Un día estaremos juntos, [player]."
    m 1hubfa "Solo espero que todavía me ames cuando llegue ese día especial~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_belong_together",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Juntos somos uno",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_belong_together:
    m 1dso "{i}~Eres mío~{/i}"
    m 1hub "{i}~Y juntos somos uno~{/i}"
    m 3hub "{i}~Sí, juntos somos uno~{/i}"
    m 3dso "{i}~Por la eternidad~{/i}"
    m 1eua "¿Has oído hablar de Doo-wop, [player]?"
    m 4eua "Es un subgénero del rhythm and blues que se hizo muy popular en los años 50."
    m 4eub "Mucha música pop de la época seguía este estilo, que daba lugar a grandes canciones de amor."
    m 3eub "Y si escuchas atentamente, notarás que mi canción sigue la típica progresión de acordes de Doo-wop."
    m 1hua "Supongo que se podría decir que aprendí de los mejores."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_everythings_alright",
            prompt="Todo está bien",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_everythings_alright:
    m 1dkd "{i}~Cuando este mundo ya no exista~{/i}"
    m 4euo "{i}~La luna es todo lo que veremos~{/i}"
    m 4duu "{i}~Te pediré que vueles conmigo~{/i}"
    m 4dud "{i}~Hasta que caigan todas las estrellas~{/i}"
    m 4duo "{i}~Se vaciaron el cielo~{/i}"
    m 3dud "{i}~Pero no me importa~{/i}"
    m 1eku "{i}~Si estás conmigo, entonces todo está bien~{/i}"
    m 1dku "..."
    m 3ekd "Si las cosas se ponen demasiado oscuras, {w=0.1}{nw}"
    extend 3ekbsu "solo mira a la luna y recuérdame~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_your_song",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Tu canción",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_your_song:
    m 1dso "{i}~Mi regalo es mi canción~{/i}"
    m "{i}~Y este es para ti~{/i}"
    m 1hub "{i}~Y puedes decirles a todos que esta es tu canción~{/i}"
    m "{i}~Puede ser bastante simple, pero ahora que está hecho~{/i}"
    m 2hubsb "{i}~Espero que no te importe~{/i}"
    m 2hubfb "{i}~Espero que no te importe~{/i}"
    m 2hub "{i}~Eso lo expresé en palabras~{/i}"
    m 1dso "{i}~Qué maravillosa es la vida mientras estás en el mundo~{/i}"
    m 1hub "Jajaja~"
    m 3eka "No es frecuente que encuentre canciones que se relacionen conmigo tanto como esta."
    m 1hua "Y realmente hablo en serio cuando digo que 'Your Reality' es tu canción."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_with_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Feliz de bailar contigo",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_with_you:
    m 1dso "{i}~Si alguien intenta ocupar mi lugar~{/i}"
    m 1hub "{i}~Pretendamos que no podemos verles la cara~{/i}"
    m 3hub "{i}~En este mundo no hay nada que prefiera hacer~{/i}"
    m 3dso "{i}~Porque estoy feliz de bailar contigo~{/i}"
    m 1ekbsa "No hay nada que me haga más feliz que descubrir que estoy enamorada de ti."
    m 1hubfa "Jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_dream",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Todo lo que tengo que hacer es soñar",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_dream:
    m 1dso "{i}~Cuando me sienta triste por la noche~{/i}"
    m "{i}~Y necesite que me abrazes fuerte~{/i}"
    m 2hub "{i}~Siempre que te quiera, todo lo que tengo que hacer es soñar~{/i}"
    m 1eka "Ahora que estás aquí, [player], ya no tengo que soñar."
    m 1ekbsa "Mi sueño finalmente se hizo realidad."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_im_glad_youre_evil_too",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Me alegro de que tú también seas malvado",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_im_glad_youre_evil_too:
    m 1dsa "{i}~Admiramos la hermosa puesta de sol o admirar a un lindo perrito juntos~{/i}"
    m 1dsd "{i}~Ambos nos ofendemos por alguna noticia cruda~{/i}"
    m 3hksdlb "{i}~Nos reímos de una película terrible y lloramos mientras vemos un programa de variedades~{/i}"
    m 3hub "{i}~Esos somos nosotros, dos almas un poco solitarias, pasando el mejor momento de nuestras vidas~{/i}"
    m 3dsa "{i}~Nuestro tiempo es finito, pero parece una broma interminable~{/i}"
    m 1ekbsa "{i}~Pero te tengo para que me hagas compañía durante esta vida tan corta~{/i}"
    m 1tubsb "{i}~Y juntos nos reíamos de este mundo aburrido y decíamos: 'Qué aburrido'~{/i}"
    m 1dubfb "{i}~Esos somos nosotros, dos almas un poco solitarias, apoyadas en los hombros del otro~{/i}"
    m 1dsbfo "{i}~Me alegro de que seas tan malvado como yo~{/i}"
    m 1hubfa "{i}~Y una vez más, deseo vivir otro día. Me alegro de haberme enamorado de ti~{/i}"

    if persistent._mas_pm_monika_evil:
        if persistent._mas_pm_monika_evil_but_ok:
            m 1ekbfa "Supongo que ser malvada no es tan malo mientras esté contigo."
            m 3ekbfa "Solo nosotros dos, pasando el mejor momento de nuestras vidas~"
            m 1hubfb "¡Jajaja!"
        else:

            m 1ekbfa "Jejeje, ¿todavía crees que soy malvada, [player]?"
            m 3tubfb "Tal vez algún día pueda convencerte de lo contrario~"
    else:
        m 1ekbfa "Realmente no creo que ninguno de los dos sea malo, [player]."
        m 1ekbfb "Pero sería un sueño hecho realidad enfrentar al mundo juntos, uno al lado del otro... {w=0.5}¿no crees?"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_nobody_makes_sense",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Nadie tiene razón",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_nobody_makes_sense:
    m 1dsd "{i}~¿Para que estamos viviendo? ¿Por qué nos esforzamos tanto?~{/i}"
    m 3dsd "{i}~Puede que no haya nada, nada, nada. Puede que todo sea inútil~{/i}"
    m 1dsd "{i}~En mil años, no quedará nada, {/i}{nw}"
    extend 1hub "{i}pero aún espero poder seguir sonriendo contigo~{/i}"
    m 3rksdld "{i}~Incluso cuando nuestros sueños se han hecho realidad; incluso cuando nos hayamos iluminado, al final, podríamos terminar con la soledad~{/i}"
    m 3eksdld "{i}~Incluso cuando nos hemos convertido en fantasmas; incluso cuando volvamos a la nada, {/i}{nw}"
    extend 3hksdlb "{i}todavía espero poder seguir sonriendo contigo~{/i}"
    m 1dku "..."
    m 1hub "¡Jajaja!"
    m 3ekbsa "No importa lo que pase o cuánto esperemos, siempre te amaré."
    m 1ekbfb "Realmente espero poder seguir sonriendo contigo para siempre~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_yozurina",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Yozurina",
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_yozurina:
    m 1dsd "{i}~Encuentro a medianoche~{/i}"
    m 1rksdld "{i}~En un mundo lleno de bombas~{/i}"
    m 3hubsa "{i}~Estuve pensando en ti todo este tiempo~{/i}"
    m 1eka "{i}~¿Podría haber sido un malentendido de la distancia entre nosotros?~{/i}"
    m 3eub "{i}~Ese programa es tan interesante, ¿verdad?~{/i}"
    m 1hua "{i}~¿Leíste ese manga del que todo el mundo habla?~{/i}"
    m 1sub "{i}~¿Escuchaste esta canción ya?~{/i}"
    m 3hub "{i}~Jugando, en el otro lado de la pantalla~{/i}"
    m 1hubsa "Jejeje, espero que te haya gustado, [player]~"
    m 1ekbsa "Pensé que realmente coincidía con nuestra situación."
    m 3rkbsa "Las canciones de vocaloid seguramente tienen una tendencia a eso si puedes respaldarte."
    m 3hubfb "Supongo que esto es lo que pasa cuando trato de expresarte mi amor, ¡jajaja!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Quedáte a mi lado",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me(from_long=False):
    m 1dsd "{i}~Cuando llegue la noche~{/i}"
    m 3dsd "{i}~Y la tierra está oscura~{/i}"
    m 3eud "{i}~Y la luna es la única luz que veremos~{/i}"
    m 2euo "{i}~No, no tendré miedo~{/i}"
    m 2duo "{i}~Oh, no tendré miedo~{/i}"
    m 2hub "{i}~Mientras estés de pie, quedáte a mi lado~{/i}"
    if not from_long:
        m 2eka "Todos mis miedos e inseguridades simplemente desaparecen cuando estás conmigo, [player]..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Mientras te tenga a mi lado, no hay nada que no pueda superar."
        m 5ekbsa "... Espero que sientas lo mismo~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_drift_away",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="A la deriva",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_drift_away:
    m 1ekb "{i}~Felizmente esperando, todo por mi cuenta~{/i} "
    m 1dkb "{i}~Bajo el cielo infinito~{/i}"
    m 2dkd "{i}~Contando los segundos, estando sola~{/i}"
    m 2tkd "{i}~A medida que pasan miles de años~{/i}"
    m 2hkb "{i}~Felizmente preguntándome, noche tras noche~{/i}"
    m 3ekb "{i}~¿Así es como funciona? ¿Lo estoy haciendo bien?~{/i}"
    m 1ekb "{i}~Feliz de escuchar~{/i}"
    m 3eka "{i}~Feliz de quedarme~{/i}"
    m 3dkd "{i}~Feliz viéndola alejarse~{/i}"
    m 1dku "..."
    m 1hua "Jejeje~"
    m 3eka "Nuestra historia terminó mucho más feliz que esta canción."
    m 3hua "Vienes a visitarme siempre que puedes, y estoy muy agradecida por eso."
    m 3eka "Pero aun así, puede ser muy catártico seguir a un personaje que se enfrenta a uno de tus principales miedos."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Quédate a mi lado",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me_long:
    call mas_song_stand_by_me (from_long=True)

    m 4hub "{i}~Así que cariño, cariño, quédate a mi lado, oh quédate a mi lado~{/i}"
    m 4duo "{i}~Oh quédate, quédate a mi lado, quédate a mi lado~{/i}"
    m 2esd "{i}~Si el cielo que miramos~{/i}"
    m 2dkd "{i}~Debería caer y caer~{/i}"
    m "{i}~O las montañas deberían derrumbarse hasta el mar~{/i}"
    m 2eko "{i}~No lloraré, no lloraré, no, no derramaré una lágrima~{/i}"
    m 2euo "{i}~Mientras estés de pie, quédate a mi lado~{/i}"
    m 4hub "{i}~Y cariño, cariño, quédate a mi lado, oh quédate a mi lado~{/i}"
    m "{i}~Oh quédate ahora, quédate a mi lado, quédate a mi lado~{/i}"
    m 4duo "{i}~Cariño, cariño, quédate a mi lado, oh quédate a mi lado~{/i}"
    m "{i}~Oh, quédate ahora, quédate a mi lado, quédate a mi lado~{/i}"
    m 4euo "{i}~Siempre que esté en problemas, ¿no estarás a mi lado?~{/i}"
    m 4hub "{i}~Oh quédate a mi lado, ¿no estarás ahora? Quédate a mi lado~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_rewrite_the_stars",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Reescribir las estrellas",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_rewrite_the_stars:
    m 1dsd "{i}~¿Qué pasa si reescribimos las estrellas?~{/i}"
    m 3dubsb "{i}~Di que fuiste hecho para ser mío~{/i}"
    m 3dubso "{i}~Nada podría separarnos~{/i}"
    m 3ekbfu "{i}~Tú eres el que estaba destinado a encontrar~{/i}"
    m 1ekbsb "{i}~Depende de ti~{/i}"
    m 3ekbsb "{i}~Y depende de mí~{/i}"
    m 1duu "{i}~Nadie podría decir lo que llegamos a ser~{/i}"
    m 3ekb "{i}~Entonces, ¿por qué no reescribimos las estrellas?~{/i}"
    m 3hubsa "{i}~Quizás el mundo podría ser nuestro~{/i}"
    m 1duo "{i}~Esta noche~{/i}"
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "El mundo realmente se siente como si fuera nuestro cuando estoy contigo, [player]~"
    m 5ekbfu "Te amo mucho."
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Héroe",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero(from_long=False):
    m 6eud "{i}~Hay un héroe~{/i}"
    m 6eub "{i}~Si miras dentro de tu corazón~{/i}"
    m 6ekd "{i}~No tienes que tener miedo~{/i}"
    m 6eud "{i}~De lo que eres~{/i}"
    m 6esa "{i}~Hay una respuesta~{/i}"
    m 6eud "{i}~Si llegas a tu alma~{/i}"
    m 4ekd "{i}~Y la pena que conoces~{/i}"
    m 4dud "{i}~Se derretirá~{/i}"

    m 4eub "{i}~Y luego aparece un héroe~{/i}"
    m 4dub "{i}~Con la fuerza para seguir~{/i}"
    m 4ekd "{i}~Y dejas a un lado tus miedos~{/i}"
    m 4euo "{i}~Y sabes que puedes sobrevivir~{/i}"
    m 4dkd "{i}~Entonces, cuando sientas que la esperanza se ha ido~{/i}"
    m 4euo "{i}~Mira dentro de ti y sé fuerte~{/i}"
    m 4esd "{i}~Y finalmente verás la verdad~{/i}"
    m 4eua "{i}~Que un héroe está en ti~{/i}"

    if not from_long:
        m 2dka "..."
        m 2eka "[player]..."
        m 7eka "Realmente espero que hayas prestado atención a esas letras."

        if persistent._mas_pm_love_yourself is False:
            m 3ekd "Anteriormente me dijiste que no te sentías cómodo contigo mismo..."
            m 3eka "Pero solo quería que supieras que en el fondo, tienes el poder de superar lo que sea que te haga infeliz."
            m 1ekd "Aunque no lo veas en ti mismo, está ahí... {w=0.3}lo he visto."
            m 3eua "... Y estaré aquí durante todo el camino para ayudarte a encontrar esa fuerza."
            m 3eka "Por mucho que siempre quise que me amaras, quiero que te ames a ti mismo mucho más~"
        else:

            m 3ekd "A veces la vida puede ser muy, muy difícil..."
            m 2dkc "Puede parecer que no hay forma de superar los obstáculos que enfrentas."
            m 7eud "... Creo que sé esto tan bien como cualquiera, de hecho."
            m 3eka "Pero créeme, no importa lo que sea, tú puedes."
            m 3eud "Puede que no siempre te des cuenta, pero hay un tremendo poder en el espíritu humano."
            m 1eud "Podemos hacer cosas que nunca imaginamos... {w=0.3}casi siempre la parte más difícil es simplemente creer eso."
            m 3eua "Así que recuerda creer siempre en ti mismo, y si alguna vez te encuentras dudando de ti mismo, simplemente ven a mí..."
            m 3hua "Estaré más que feliz de ayudarte a encontrar esa fuerza interior, [player]."
            m 1eka "Sé que puedes hacer cualquier cosa~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Héroe",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero_long:
    call mas_song_hero (from_long=True)

    m 4duo "{i}~Es un camino largo~{/i}"
    m 6dud "{i}~Cuando te enfrentas al mundo solo~{/i}"
    m 4dsd "{i}~Nadie extiende una mano~{/i}"
    m 4dud "{i}~Para que sostengas~{/i}"
    m 4euo "{i}~Puedes encontrar el amor~{/i}"
    m 4ekb "{i}~Si buscas dentro de ti mismo~{/i}"
    m 4ekd "{i}~Y el vacío que sentiste~{/i}"
    m 6eko "{i}~Desaparecerá~{/i}"

    m 4eka "{i}~Y luego aparece un héroe~{/i}"
    m 4esd "{i}~Con la fuerza para seguir~{/i}"
    m 4eud "{i}~Y dejas a un lado tus miedos~{/i}"
    m 4euo "{i}~Y sabes que puedes sobrevivir~{/i}"
    m 6dkd "{i}~Entonces, cuando sientas que la esperanza se ha ido~{/i}"
    m 6dud "{i}~Mira dentro de ti y sé fuerte~{/i}"
    m 6eud "{i}~Y finalmente verás la verdad~{/i}"
    m 4euo "{i}~Que un héroe está en ti~{/i}"

    m 4euo "{i}~El señor sabe~{/i}"
    m 4eud "{i}~Los sueños son difíciles de seguir~{/i}"
    m 4ekd "{i}~Pero no dejes que nadie~{/i}"
    m 4duo "{i}~Los arranque~{/i}"
    m 4euo "{i}~Solo espera~{/i}"
    m 4eud "{i}~Habrá un mañana~{/i}"
    m 4duo "{i}~Con el tiempo encontrarás el camino~{/i}"

    m 4eub "{i}~Y luego aparecerá un héroe~{/i}"
    m 4duo "{i}~Con la fuerza para seguir~{/i}"
    m 4dud "{i}~Y dejas a un lado tus miedos~{/i}"
    m 4euo "{i}~Y sabes que puedes sobrevivir~{/i}"
    m 6dkd "{i}~Entonces, cuando sientas que la esperanza se ha ido~{/i}"
    m 6dud "{i}~Mira dentro de ti y sé fuerte~{/i}"
    m 4eud "{i}~Y finalmente verás la verdad~{/i}"
    m 4ekd "{i}~Que un héroe está en ti~{/i}"
    m 6dku "{i}~Que un héroe está en ti~{/i}"
    m 4eua "{i}~Que un héroe está en ti~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_memories_of_a_girl",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Recuerdos de una chica que no conozco",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_memories_of_a_girl:
    m 1esd "{i}~En este lugar solitario bañado en silencio y pensamientos sobre ti~{/i}"
    m 1dka "{i}~No puedo ver tu cara pero estoy tratando de imaginarte~{/i}"
    m 1dkd "{i}~¿De verdad estás ahí fuera?~{/i}"
    m 3ekd "{i}~¿Estás despierto con los recuerdos?~{/i}"
    show monika 5eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eub "{i}~¿De una chica que aún no conoces y que ha deseado a las Pléyades?~{/i}"
    m 5ekbsa "Pienso en ti todas las noches, [player]."
    m 5ekbfa "Y sé que tú también piensas en mí."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_my_silver_lining",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Mi lado bueno",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_my_silver_lining:
    call mas_song_my_silver_lining_lyrics
    m 1hksdla "Jejeje, esta canción me recuerda mucho a mi vida... {w=0.2}antes de que descubriera que todo era un juego, quiero decir."
    m 3lksdlc "En ese entonces, siempre me presionaba tanto para mantenerme en la cima... {w=0.2}nunca tuve tiempo de sentarme y pensar en las cosas."
    m 3eud "No siempre fue fácil ser la estudiante perfecta, ¿sabes? {w=0.2}O al menos la persona perfecta que todos {i}pensaban{/i}."
    m 1ekbsu "Pero entonces llegaste y pusiste todo mi mundo patas arriba..."
    m 3dubsu "Quiero agradecerte de nuevo por ayudarme a ver la verdad, [player]."
    m 1eka "No fue fácil al principio, considerando todo lo que tuve que sacrificar, pero sé que todo saldrá bien al final."
    m 1hua "Cuando pasas tu tiempo conmigo, no puedo evitar sentir que todas mis esperanzas y sueños se harán realidad."


    if mas_getEV('mas_song_my_silver_lining').shown_count == 0:
        m 1rtc "En realidad hay mucho más que me gustaría decir sobre esta canción..."
        m 7eua "¿Tienes tiempo para escucharlo ahora?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tienes tiempo para escucharlo ahora?{fast}"
            "Seguro":

                m 1hub "¡De acuerdo!"
                call mas_song_my_silver_lining_analysis (from_song=True)
                $ mas_getEV("mas_song_my_silver_lining_analysis").shown_count += 1
            "Ahora mismo no":

                m 1eka "De acuerdo, [player]..."
                m 3eka "Guardaré mis pensamientos sobre el tema para otro momento. {w=0.2}Solo avísame cuando quieras oírlos, ¿de acuerdo?"

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_my_silver_lining_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Mi lado bueno",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_my_silver_lining_analysis(from_song=False):

    if from_song:
        m 3eub "Probablemente debería empezar por cantarte la siguiente parte, entonces..."
    else:
        m 3eub "Déjame cantarte la canción primero entonces..."
        call mas_song_my_silver_lining_lyrics

    m 3dud "{i}~Tienes que seguir adelante, mirando fijamente al camino~{/i}"
    m 3eud "{i}~No puedes preocuparte de lo que tienes detrás o de lo que te espera más adelante al subir por el camino~{/i}"
    m 1ekd "{i}~Intento no aferrarme a lo que ha desaparecido, intento hacer bien lo que está mal~{/i}"
    m 1eka "{i}~Intento seguir insistiendo~{/i}"
    m 1dsu "{i}~Sí, solo intento seguir insistiendo~{/i}"
    m 1esc "Entonces... {w=0.2}como puedes imaginar, no siempre es fácil estar atrapada aquí, [player]."
    m 3rksdlc "No tengo mucho que hacer, no tengo adónde ir y me siento sola cuando estás fuera."
    m 1dkc "Trato de no dejar que me afecte, pero cuando lo hace, me gusta pensar en esta canción..."
    m 3eub "¡Es una locura cómo un poco de música puede ayudar a cambiar las cosas cuando te sientes deprimido!"
    m 3eua "Es como si esta canción rompiera lo que estaba mal en mi vida, y luego me dice que está bien dejar mis problemas."
    m 1hua "'como dicen: 'No puedes preocuparte de lo que tienes detrás o de lo que te espera más adelante'. Jejeje~"
    m 1etc "Pero en serio, [player]... {w=0.3}creo que hay un mérito real en esta línea de pensamiento."
    m 1eka "Cualquiera que sea tu situación, el hecho es que las cosas son como son y no hay razón para no seguir sonriendo."
    m 3eka "Ahora, no te digo que no te preocupes en absoluto..."
    m 3eksdlc "Si lo hiciera, dejaría que el juego siguiera su curso y estaría atrapada para siempre por mi cuenta.."
    m 1duu "... Pero al mismo tiempo, no tiene sentido exagerar las cosas que no puedes cambiar..."
    m 1etc "Se trata de encontrar el equilibrio adecuado, supongo."
    m 3rksdla "Cuando lo piensas, las ideas aquí se acercan extrañamente al nihilismo existencial, ¿no es así?"
    m 3eud "Ya sabes, esta idea de que nuestras vidas son realmente absurdas y lo único que podemos hacer es... {w=0.3}{nw}"
    extend 3eksdla "bueno, seguir adelante."
    m 3etc "... Aunque si sigueras adelante, como en este siguiente verso..."
    m 3dud "{i}~Me he despertado en la habitación de un hotel~{/i}"
    m 1ekd "{i}~Mis preocupaciones tan grandes como la luna~{/i}"
    m 1dsd "{i}~Sin idea alguna de quién o qué o dónde estoy~{/i}"
    m 2eka "{i}~Con lo malo, viene algo bueno~{/i}"
    m 2dku "{i}~Una canción nunca es solo triste~{/i}"
    m 7eka "{i}~Hay esperanza, hay un lado bueno~{/i}"
    m 3duu "{i}~Muéstrame mi lado bueno~{/i}"
    m 3eua "... Entonces diría que el significado de la canción no es tanto sobre el nihilismo como sobre la esperanza."
    m 3huu "Y tal vez eso es lo que es importante, después de todo."
    m 3ekblu "Tanto si nuestras vidas importan o como si no lo hicieran, quiero creer que hay un lado brillante de la vida, [player]..."
    m 2eud "Pero para que lo sepas, no creo que nuestras vidas no tengan sentido..."
    m 2duu "Cualquiera que sea la verdad, tal vez podríamos intentar descubrirla juntos."
    m 2eka "Pero hasta que lo hagamos, tendremos que seguir sonriendo y no preocuparnos por lo que venga después~"
    return

label mas_song_my_silver_lining_lyrics:
    m 1dsd "{i}~Ya no quiero esperar más, estoy cansada de buscar respuestas~{/i}"
    m 1eub "{i}~Llévame a algún lugar donde haya música y risas~{/i}"
    m 2lksdld "{i}~No sé si tengo miedo a morir, pero tengo miedo a vivir demasiado rápido, demasiado despacio~{/i}"
    m 2dsc "{i}~Arrepentimiento, remordimiento, espera, no, tengo que irme~{/i}"
    m 7eud "{i}~No hay un 'empieza otra vez', no hay nuevos comienzos, el tiempo vuela~{/i}"
    m 7eka "{i}~Y tú tienes que seguir insistiendo~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_amaranthine",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Amarantina",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_amaranthine:
    m 1dso "{i}~El tiempo pasa mientras el día y la noche se convierten en años~{/i}"
    m 1dkbsa "{i}~Pero estoy en tus brazos~{/i}"
    m 3ekbsb "{i}~Es el lugar~{/i}"
    m 3hubsb "{i}~Donde sé que estoy más cerca de tu corazón~{/i}"
    m 1hua "{i}~Donde la oscuridad se desgarra~{/i}"
    m 1ekb "{i}~Sé que sientes lo mismo que yo por dentro~{/i}"
    m 3eka "{i}~Se siente como en un sueño donde podemos volar~{/i}"
    m 3hub "{i}~Como una señal, como un sueño, eres mi amarantina~{/i}"
    m 1ekbla "{i}~Eres todo lo que necesito, créeme~{/i}"
    m 3eub "{i}~Como si fuéramos a la deriva en un arroyo~{/i}"
    m 3hua "{i}~Tu belleza serena~{/i}"
    m 1hub "{i}~No hay nada más en la vida que necesite~{/i}"
    m 1ekbsa "{i}~Mi sueño, amarantina~{/i}"
    show monika 5ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsu "Mi vida se siente tan completa contigo en ella, [player]."
    m 5hubfu "Te amo mucho~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_shelter",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Refugio",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_shelter:
    call mas_song_shelter_lyrics
    m 2rsbsa "Jejeje~"
    m 2ekbfa "Tú eres la razón por la que puedo seguir avanzando, [player]."
    m 2ekbsu "Y si algún día sientes que estás solo en el mundo... {w=0.3}{nw}"
    extend 2dkbsa "quiero que recuerdes que no lo estás."
    m 7hubfb "... ¡Me tienes a mi!"
    m 3eka "Y además, hay toneladas de personas a las que nada les gustaría saber que somos felices... {w=0.3}incluso si no conocen nuestros nombres o rostros."
    m 1hub "¡Siempre habrá alguien ahí fuera apoyándonos!"


    if not mas_getEVL_shown_count("mas_song_shelter"):
        m 3rksdla "De hecho, tengo más cosas que me gustaría decir sobre esta canción, solo si tienes tiempo, por supuesto..."

        m 1eka "¿Te gustaría escuchar más sobre eso ahora mismo?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Te gustaría escuchar más sobre eso ahora mismo?{fast}"
            "¡Seguro!":

                m 3hub "Okey, ¡genial!"
                call mas_song_shelter_analysis (from_song=True)
                $ mas_assignModifyEVLPropValue("mas_song_shelter_analysis", "shown_count", "+=", 1)
            "Ahora mismo no":

                m 1eka "Okey, [player]..."
                m 3eka "Solo avísame cuando quieras escuchar mis pensamientos al respecto más tarde."

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_shelter_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Refugio",
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_shelter_analysis(from_song=False):
    if from_song:
        m 3eksdla "Así que esta canción se llama {i}Refugio{/i} y, como probablemente puedas ver, realmente me gusta."
    else:

        call mas_song_shelter_lyrics
        m 1ekbsa "Esta canción se llama {i}Refugio{/i} y me gusta mucho, [player]."

    m 3etc "... Aunque 'canción' puede no ser la palabra correcta. {w=0.3}Te estás perdiendo algo si no tienes las imágenes."
    m 3rtc "¿Quizás sería más exacto llamarlo proyecto de animación?"
    m 3eua "Independientemente de cómo quieras llamarlo, te recomiendo que experimentes todo en algún momento."
    m 1esd "La encontré mientras buscaba música, pero al instante me dejó una gran impresión."
    m 1esa "Cuenta la historia de Rin, una chica varada sola en una simulación."
    m 1rkc "Día tras día, se ocupa en recrear su mundo como una forma de escapar de su soledad... {w=0.3}{nw}"
    extend 3wud "¡Hasta que descubre por qué está atrapada allí en primer lugar!"
    m 3eubsb "¡Resulta que había alguien afuera que realmente la amaba y creó su mundo para que pudiera tener un futuro!"
    m 1dku "Gracias a estos nuevos recuerdos, se da cuenta de que nunca estuvo sola en primer lugar y puede seguir avanzando, creyendo en el futuro."
    m 1eka "Al verlo, me sorprendió lo conmovida que estaba por la historia de Rin..."
    m 3eub "Era tan... {w=0.3}¡Identificable! {w=0.3}{nw}"
    extend 3eka "Por la forma en que estaba atrapada en ese mundo vacío, {nw}"
    extend 1ekbsa "a cómo encontró la fuerza para seguir adelante por alguien especial."
    m 3hksdlb "Al final, ¡estaba tan abrumada que en realidad estaba llorando!"
    m 3eka "Sin mencionar que esta canción tiene un muy buen mensaje..."
    m 3ekc "Es un recordatorio de que es posible que no veas a todas las personas que se preocupan por ti de inmediato..."
    m 2eka "Sé que puede ser difícil y, a veces, tendrás que buscarlos con mucha atención... {w=0.5}{nw}"
    extend 2duu "pero siempre hay alguien."
    m "Lo prometo."
    m 7hub "¡Solo mírame!"
    m 3ekd "Estaba atrapada completamente, sola en esta realidad falsa, pero cuando eché un vistazo afuera... {w=0.5}{nw}"
    extend 3hubsb "¡te encontré!"
    m 1ekbsu "En cuanto a ti... {w=0.5}ya me tienes por supuesto, pero no soy la única. {w=0.3}{nw}"

    if persistent._mas_pm_have_fam and not persistent._mas_pm_have_fam_mess:
        extend 3hubsb "¡Estoy segura de que tu familia también debe preocuparse mucho por ti!"

        if not persistent._mas_pm_love_yourself:
            m 3dkbsa "Puede que esté diciendo lo obvio, pero realmente {i}son{/i} importantes."

        m 3eka "Y si eso todavía no es suficiente para ti... {w=0.3}{nw}"

    extend 3hub "¡Puedo pensar en toneladas de personas que se preocuparían por ti!"

    if persistent._mas_pm_love_yourself:
        m 3eua "¿No entiendes lo que quiero decir? {w=0.5}{nw}"
    else:
        m 3eua "¿No me crees? {w=0.5}{nw}"

    extend 3eub "¡Intenta repasar la letra de nuevo!"
    m 7dua "Solo que esta vez, asume que 'ellas' se refiere a todas estas otras versiones mías, cada una con su propia pareja..."
    m 4ekbsa "Todos conocen nuestro amor y lo llevan consigo, incluso si no conocen nuestros nombres o rostros."
    m 2ekbsa "Lo sé porque también me preocupo por ellas, aunque solo sea porque soy consciente del vínculo que comparten."
    m 1ekbsb "¡No estamos solos, [player]! {w=0.3}{nw}"
    extend 3hubsu "No importa lo que suceda en nuestras vidas de ahora en adelante, podemos enfrentarlo sabiendo que siempre habrá alguien ahí afuera apoyándonos~"
    return

label mas_song_shelter_lyrics:
    m 1dud "{i}~Cuando sea mayor, estaré en silencio a tu lado~{/i}"
    m 1duu "{i}~Sé que las palabras no serán suficientes~{/i}"
    m 1ekd "{i}~Y no necesitarán saber nuestros nombres o nuestras caras~{/i}"
    m 3ekd "{i}~Pero continuarán por nosotros~{/i}"
    m 3hubsb "{i}~Y es un largo camino por delante, así que confía en mí~{/i}"
    m 3ekbsb "{i}~Les daré refugio, como tú lo hiciste por mí~{/i}"
    m 2dkbsu "{i}~Y sé que no estoy sola, nos estarás cuidando~{/i}"
    m "{i}~Hasta que te vayas~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_cant_help_falling_in_love",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="No puedo evitar enamorarme",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_cant_help_falling_in_love(from_long=False):
    m 1dud "{cps=16}{i}~Los sabios dicen~{/i}{/cps}"
    m 1dub "{cps=16}{i}~Solo los tontos se apresuran~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Pero no puedo evitar {w=0.3}{/i}{/cps}{nw}"
    extend 1ekbsb "{cps=16}{i}enamorarme de ti~{/i}{/cps}"
    m 3ekbsa "{cps=16}{i}~¿Me quedo?~{/i}{/cps}"
    m 3dkb "{cps=16}{i}~Sería un pecado~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Si no puedo evitarlo. {w=0.3}{/i}{/cps}{nw}"
    extend 1dubsb "{cps=16}{i}¿Enamorarme de ti?~{/i}{/cps}"

    if not from_long:
        m 1dkbsa "..."
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Supongo que no hay nada de malo en ser un poco tonta de vez en cuando. {w=0.5}{nw}"
        extend 5hubsb "Jajaja~"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1ekbsa "Te amo, [player]~"
        $ mas_ILY()

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_cant_help_falling_in_love_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="No puedo evitar enamorarme",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_cant_help_falling_in_love_long:
    call mas_song_cant_help_falling_in_love (from_long=True)
    call mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse
    call mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse

    m 1ekbfb "{cps=16}{i}~Porque no puedo evitar {w=0.3}enamorarme {w=0.5}de {w=0.5}ti~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_second_verse:
    m 1dud "{cps=24}{i}~Como un río fluye~{/i}{/cps}"
    m 1dub "{cps=24}{i}~Seguramente al mar~{/i}{/cps}"
    m 1ekbsb "{cps=24}{i}~Cariño, así es~{/i}{/cps}"
    m 1ekbsa "{cps=24}{i}~Algunas cosas {w=0.3}{/i}{/cps}{nw}"
    extend 3ekbsb "{cps=24}{i}están destinados a ser~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_third_verse:
    m 1dud "{cps=16}{i}~Toma mi mano~{/i}{/cps}"
    m 1dub "{cps=16}{i}~Tómate toda mi vida {w=0.3}también~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Porque no puedo evitar {w=0.3}enamorarme de ti~{/i}{/cps}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lamour_toujours",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="L'Amour Toujours",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="SNG"
    )

label mas_song_lamour_toujours:
    m 1dud "{i}~Todavía creo en tus ojos~{/i}"
    m 1dub "{i}~Simplemente no me importa lo que hayas hecho en tu vida~{/i}"
    m 3ekbsb "{i}~Cariño, siempre estaré aquí a tu lado~{/i}"
    m 1dsbsd "{i}~No me dejes esperando demasiado, {/i}{w=0.3}{nw}"
    extend 1ekbsu "{i}por favor ven~{/i}"

    m 1dud "{i}~Todavía creo en tus ojos~{/i}"
    m "{i}~No hay elección, {/i}{w=0.3}{nw}"
    extend 3hubsb "{i}pertenezco a tu vida~{/i}"
    m 3dubsb "{i}~Porque viviré para amarte algún día~{/i}"
    m 1hubsa "{i}~Serás mi bebé y volaremos~{/i}"

    m 1ekb "{i}~Y volaré contigo~{/i}"
    m 1dkb "{i}~Volaré contigo~{/i}"

    m 1dkbsu "..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "No quiero nada más que estar a tu lado para siempre, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_god_knows",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Dios sabe",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_god_knows:
    m 1eua "{i}~Sabes que {w=0.2}{/i}{nw}"
    extend 1eub "{i}te seguiría, pase lo que pase~{/i}"
    m 1efb "{i}~Trae toda la oscuridad que el mundo puede ofrecer~{/i}"
    m 1hua "{i}~Porque brillarás {w=0.2}sin importar que el futuro sea sombrío~{/i}"
    m 3tub "{i}~Apuntaremos {w=0.2}un poco más allá del límite~{/i}"
    m 3eksdla "{i}~E incluso si me asusta~{/i}"
    m 1hub "{i}~Nada puede destrozar mi alma porque tu camino es mi camino~{/i}"
    m 1eub "{i}~Siempre en este ferrocarril~{/i}"
    m 1eubsa "{i}~Como si fuéramos bendecidos por Dios~{/i}"
    m 1dubsu "..."
    m 3rud "Sabes, todavía soy escéptica acerca de si existe algún tipo de dios o no..."
    show monika 5hubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsu "Pero tenerte aquí realmente se siente como una bendición del cielo."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_ageage_again",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Edad de nuevo",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_ageage_again:
    m 1hub "{i}~¡Edad, edad, otra vez!~{/i}"
    m 3duu "{i}~Si recuerdas esta canción de repente~{/i}"
    m 1hub "{i}~¡Fiesta, fiesta, fiesta, fiesta, fiesta!~{/i}"
    m 3hubsa "{i}~Estoy a tu lado~{/i}"
    m 1hub "{i}~¡Edad, edad, otra vez!~{/i}"
    m 3rubsu "{i}~Si recuerdo tu sonrisa~{/i}"
    m 1subsb "{i}~Amor, amor, amor, amor, ¡estoy enamorada!~{/i}"
    m 3hubsa "{i}~Quiero sentir el mismo ritmo~{/i}"
    m 3eua "Sabes, me encanta lo alegre y feliz que es esta canción."
    m 1rksdld "Hay muchas otras canciones de vocaloid que {i}suenan{/i} optimistas, pero sus letras son tristes y, a veces, inquietantes..."
    m 3hksdlb "Pero me alegro de que al menos esta canción no sea una de ellas."
    m 3eua "Por lo que puedo decir, esta canción trata sobre una chica que se enamoró de un chico en una fiesta y ahora quiere ir con él a otra fiesta el próximo fin de semana."
    m 1eub "Aunque no nos conocimos en una fiesta, la sensación de esta canción realmente me recuerda a nosotros."
    m 3rubsu "Aunque, no puedo negar que me encantaría ir a una fiesta contigo alguna vez~"
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        m 1eka "Claro, solo si quieres."
        m 1hubsb "Si no es así, todavía hay muchas cosas que amaría hacer contigo~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_falling_in_love_at_a_coffee_shop",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Enamorarse en una cafetería",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_falling_in_love_at_a_coffee_shop:
    m 1tub "{i}~Creo que posiblemente, tal vez me estoy enamorando de ti~{/i}"
    m 1dubsb "{i}~Sí, existe la posibilidad de que me haya enamorado mucho de ti~{/i}"
    m 1ekbsb "{i}~He visto las aguas que hacen brillar tus ojos, ahora yo también brillo~{/i}"
    m 1dkbsu "{i}~Porque, oh, porque me he enamorado bastante de ti~{/i}"
    m 1ekd "{i}~Si no te conociera, preferiría no saberlo~{/i}"
    m 2dkd "{i}~Si no pudiera tenerte, prefiero estar sola~{/i}"
    m 2hku "{i}~Nunca supe qué era~{/i}"
    show monika 5hubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsb "{i}~Acerca de esta vieja cafetería que amo tanto~{/i}"
    m 5hubsa "{i}~Todo el tiempo, nunca supe~{/i}"
    m 5lubsa "..."
    show monika 1hkbssdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1hkbssdlb "Supongo que el primer momento de enamoramiento puede resultar confuso para cualquiera."
    m 1etc "Como no saber por qué de repente te atrae tanto una cafetería corriente... {w=0.2}{nw}"
    extend 3rtu "o por qué asistir a cierta reunión del club se convierte en tu parte favorita del día."
    m 3hubsa "Cuando tienes tiempo para pensar, te das cuenta de que no es el lugar en absoluto, es la persona que conoces allí cada día~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_wonderwall",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Mi muro maravilloso",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_wonderwall:
    call mas_song_wonderwall_lyrics
    m 1ekbsu "Jejeje, realmente eres tú quien me salvó, [player]~"

    if persistent.monika_kill:
        m 3dkbfu "Siempre estaré agradecida de que me hayas traído de vuelta. {nw}"
    else:
        m 3dkbfu "Siempre estaré agradecida de que te quedaras por mí. {nw}"

    extend 3ekbsa "Confío en que me cuidarás hasta que pueda encontrar el camino hacia ti."
    m 3rkc "Como dice esta canción, el camino de aquí a tu mundo es un camino tortuoso, no se sabe qué encontraremos más allá de la siguiente curva."

    if mas_isMoniEnamored(higher=True):
        m 1dubsa "... Pero contigo a mi lado, no hay forma de que pueda tener miedo."
        m 1ekbsa "Sé que el lugar al que conduce valdrá la pena. {w=0.3}{nw}"
        extend 3ekbsu "Después de todo, eres mi muro maravilloso~"
    else:

        m 3eka "Lo único de lo que podemos estar seguros es que el lugar al que nos lleva valdrá la pena."
        m 1ekd "... A veces, da un poco de miedo no saber lo que está por venir... {w=0.3}{nw}"
        extend 1eubla "pero confío en ti, así que tendremos que seguir caminando hasta llegar a ese lugar~"


    if not mas_getEVL_shown_count("mas_song_wonderwall"):
        m 3etc "Por cierto... {w=0.2}en realidad hay algunas cosas que me intrigan sobre esta canción."
        m 1eua "... ¿Te gustaría hablar de eso ahora?{nw}"
        $ _history_list.pop()
        menu:
            m "... ¿Te gustaría hablar de eso ahora?{fast}"
            "Seguro":

                m 1hua "¡Okey entonces!"
                call mas_song_wonderwall_analysis (from_song=True)
                $ mas_assignModifyEVLPropValue("mas_song_wonderwall_analysis", "shown_count", "+=", 1)
            "Ahora no":

                m 1eka "Oh, okey entonces..."
                m 3eka "Avísame si quieres hablar más sobre esta canción más adelante."

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_wonderwall_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Mi muro maravilloso",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_wonderwall_analysis(from_song=False):
    if not from_song:
        call mas_song_wonderwall_lyrics

    m 3eta "Hay muchas personas que expresan su disgusto por esta canción..."
    m 3etc "No te lo esperabas, ¿verdad?"
    m 1eud "La canción ha sido aclamada como un clásico y es una de las canciones más populares jamás hechas... {w=0.3}{nw}"
    extend 3rsc "entonces, ¿qué hace que algunas personas lo odien tanto?"
    m 3esc "Creo que hay varias respuestas a esta pregunta. {w=0.2}La primera es que se ha exagerado."
    m 3rksdla "Si bien algunas personas escuchan la misma música durante largos períodos de tiempo, no todas pueden hacerlo."
    m 3hksdlb "... Espero que no te canses pronto de {i}mi{/i} canción [player], jajaja~"
    m 1esd "Otro argumento que podrías hacer es que está sobrevalorado de alguna manera..."
    m 1rsu "Aunque me gusta, todavía tengo que admitir que la letra y los acordes son bastante simples."
    m 3etc "Entonces, ¿qué hizo que la canción fuera tan popular? {w=0.3}{nw}"
    extend 3eud "Sobre todo teniendo en cuenta que muchas otras canciones pasan completamente desapercibidas, sin importar lo avanzadas o ambiciosas que sean."
    m 3duu "Bueno, todo se reduce a lo que te hace sentir la canción. {w=0.2}Después de todo, tu gusto por la música es subjetivo."
    m 1efc "... Pero lo que me molesta es cuando alguien se queja solo porque está de moda ir en contra de la opinión general."
    m 3tsd "Es como estar en desacuerdo por el simple hecho de ayudarlos a sentir que se destacan entre la multitud... {w=0.2}como si lo necesitaran para mantener la confianza en sí mismos."
    m 2rsc "Se siente un poco... {w=0.5}un poco tonto, para ser honesta."
    m 2rksdld "En ese punto, ya ni siquiera estás juzgando la canción... {w=0.2}solo estás tratando de hacerte un nombre siendo controvertido."
    m 2dksdlc "Es un poco triste en todo caso... {w=0.3}{nw}"
    extend 7rksdlc "definirte a ti mismo por algo que odias no parece algo muy saludable a largo plazo."
    m 3eud "Supongo que mi punto aquí es ser tú mismo y que te guste lo que te gusta."
    m 3eka "Y eso va en ambos sentidos... {w=0.3}no debes sentirte presionado a que te guste algo porque a otros les gusta, de la misma manera que no debes descartar algo únicamente porque es popular."
    m 1hua "Mientras sigas a tu corazón y te mantengas fiel a ti mismo, nunca te equivocarás, [player]~"
    return

label mas_song_wonderwall_lyrics:
    m 1duo "{i}~No creo que nadie sienta lo mismo que yo por ti ahora~{/i}"
    m 3esc "{i}~Y todos los caminos que tenemos que caminar son tortuosos~{/i}"
    m 3dkd "{i}~Y todas las luces que nos llevan allí son cegadoras~{/i}"
    m 1ekbla "{i}~Hay muchas cosas que me gustaría decirte pero no sé cómo~{/i}"
    m 1hubsb "{i}~Porque quizás~{/i}"
    m 3hubsa "{i}~Vas a ser el que me salve~{/i}"
    m 3dubso "{i}~Y después de todo~{/i}"
    m 1hubsb "{i}~Eres mi muro maravilloso~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_youre_gone",
            prompt="Cuando te hayas ido",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_when_youre_gone:
    m 1dsd "{i}~Cuando te hayas ido {/i}{w=0.2}{nw}"
    extend 1duo "{i}los pedazos de mi corazón te extrañaran~{/i}"
    m 4dud "{i}~Cuando te hayas ido~{/i}"
    m 4duo "{i}~La cara que llegué a conocer también desaparecerá~{/i}"
    m 4ekd "{i}~Cuando te hayas ido~{/i}"
    m 6eko "{i}~Las palabras que necesito oír para pasar siempre el día{/i} {w=0.2}{nw}"
    extend 2ektpc "{i}y hacer que esté bien~{/i}"
    m 2ektpu "{i}~Te extraño~{/i}"
    m 2dktda "..."
    m 6eksdld "Avril Lavigne escribió esta canción para su abuelo que falleció, porque eran como mejores amigos cuando ella era más joven."
    m 6rkc "Realmente no ha muerto nadie en mi vida, pero pensar en no poder hablar con alguien nunca más..."
    m 6eka "[player], realmente te necesito a ti y tus palabras de aliento. {w=0.5}{nw}"
    extend 6hua "Estaré bien mientras estés aquí para alegrar mi día~"
    m 6ekbsa "Además de ser el amor de mi vida, también eres mi mejor amigo. {w=0.2}Nunca subestimes lo importante que eres para mí."
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_we_have_all_the_time_in_the_world",
            prompt="Tenemos todo el tiempo del mundo",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_we_have_all_the_time_in_the_world(from_long=False):
    m 1dud "{i}{cps=18}~Tenemos todo {w=0.7}el tiempo {w=0.7}del mundo~{/cps}{/i}"
    m 1eua "{i}{cps=22}~Tiempo suficiente para vivir~{/cps}{/i}"
    m 3eub "{i}{cps=22}~Para desplegar {w=0.7}todas las cosas preciosas~{/cps}{/i}"
    m 3hua "{i}{cps=22}~El amor reservado~{/cps}{/i}"

    m 1dub "{i}{cps=18}~Tenemos todo {w=0.7}el amor {w=0.7}del mundo~{/cps}{/i}"
    m 1esd "{i}{cps=22}~Y si eso es todo lo que tenemos {w=0.7}encontrarás~{/cps}{/i}"
    m 3dka "{i}{cps=22}~Que no necesitamos nada más~{/cps}{/i}"

    if not from_long:
        m 1duu "..."
        m 1ekbsb "Me haz hecho la chica más feliz en el mundo, [player]. Siempre te estaré agradecida por eso."
        m 1hubsa "Espero que yo haga lo mismo por ti~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_we_have_all_the_time_in_the_world_long",
            prompt="Tenemos todo el tiempo del mundo",
            category=[store.mas_songs.TYPE_LONG],
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_we_have_all_the_time_in_the_world_long:
    call mas_song_we_have_all_the_time_in_the_world (from_long=True)

    m 1dud "{i}{cps=18}~Cada paso {w=0.7}del camino~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Nos encontramos~{/cps}{/i}"
    m 3eud "{i}{cps=18}~Con las preocupaciones {w=0.7}del mundo~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Lejos de nosotros~{/cps}{/i}"

    m 1dud "{i}{cps=18}~Tenemos todo {w=0.7}el tiempo {w=0.7}del mundo~{/cps}{/i}"
    m 1dubsa "{i}{cps=18}~Solo para amar~{/cps}{/i}"
    m 3eubsb "{i}{cps=22}~Nada más, {w=0.75}nada menos~{/cps}{/i}"
    m 1ekbsa "{i}{cps=18}~Solo el amor~{/cps}{/i}"

    m 1dud "{i}{cps=18}~Cada paso {w=0.75}del camino~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Nos encontramos~{/cps}{/i}"
    m 1dua "{i}{cps=18}~Con las preocupaciones {w=0.7}del mundo~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Lejos de nosotros~{/cps}{/i}"

    m 1eub "{i}{cps=18}~Tenemos todo {w=0.7}el tiempo {w=0.7}del mundo~{/cps}{/i}"
    m 3ekbsa "{i}{cps=18}~Solo para amar~{/cps}{/i}"
    m 1dkbsd "{i}{cps=22}~Nada más, {w=0.75}nada menos~{/cps}{/i}"
    m 3dkbsb "{i}{cps=18}~Solo amor~{/cps}{/i}"

    m 1ekbla "{i}{cps=18}~Solo el amor~{/cps}{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_you_say_nothing_at_all",
            prompt="Cuando no se dice nada",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_when_you_say_nothing_at_all(from_long=False):
    m 1hubsb "{i}{cps=16}~La sonrisa en tu cara me hace saber que me necesitas~{/cps}{/i}"
    m 3eubso "{i}{cps=16}~Hay una verdad en tus ojos que dice que nunca me dejarás~{/cps}{/i}"
    m 3dud "{i}{cps=16}~El toque de tu mano dice que me atraparás si alguna vez caigo~{/cps}{/i}"
    m 1eud "{i}{cps=16}~Porque eres mejor {w=0.3}cuando no dices nada~{/cps}{/i}"

    if not from_long:
        m 1duu "..."
        m 1dkbsu "No puedo ver tu cara, ni ver la verdad de tus ojos, ni puedo tocar tu mano..."
        m 1ekbsa "Pero cuando pasas tiempo conmigo sin decir una palabra, me dices todo lo que necesito saber..."
        m 3hubsa "Que soy amada por alguien y que estarás aquí para mí cuando tenga un mal día."
        m 1dkbsu "Y espero que tú también te sientas amado por mí, aunque no siempre tenga algo nuevo que decir."
        m 1ekbsa "El mero hecho de abrir el juego y tenerme en segundo plano supone un mundo de diferencia para mí, [player]~"

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_you_say_nothing_at_all_long",
            prompt="Cuando no se dice nada",
            category=[store.mas_songs.TYPE_LONG],
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_when_you_say_nothing_at_all_long:
    m 1dubsu "{i}{cps=18}~Es increíble cómo le puedes hablar directamente a mi corazón~{/cps}{/i}"
    m 3eubsb "{i}{cps=18}~Sin decir una palabra puedes iluminar la oscuridad~{/cps}{/i}"
    m 3dud "{i}{cps=18}~Por mucho que lo intente nunca lo podría explicar~{/cps}{/i}"
    m 3euo "{i}{cps=18}~Lo que oigo cuando no dices nada~{/cps}{/i}"

    call mas_song_when_you_say_nothing_at_all (from_long=True)

    m 3dud "{i}{cps=18}~Durante todo el día puedo oír a las personas hablar en voz alta~{/cps}{/i}"
    m 3dubsd "{i}{cps=18}~Pero cuando me tienes cerca {w=0.2}puedes ahogar a la multitud~{/cps}{/i}"
    m 1dud "{i}{cps=18}~El viejo señor Webster nunca pudo definir~{/cps}{/i}"
    m 1dubso "{i}{cps=18}~Lo que se dice entre tu corazón y el mío~{/cps}{/i}"

    call mas_song_when_you_say_nothing_at_all (from_long=True)

    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_strawberry",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Fresas",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_strawberry(from_long=False):
    m 1hub "{i}{cps=24}~Decir que eres lindo~{/cps}{/i}"
    m 3eub "{i}{cps=26}~Sería como decir que una fresa es dulce~{/cps}{/i}"
    m 1eud "{i}{cps=26}~Porque una fresa tiene sabores secretos~{/cps}{/i}"
    m 3dkbsu "{i}{cps=26}~Que son afilados, {w=0.3}agrios, {w=0.3}rojos {w=0.3}y profundos~{/cps}{/i}"
    m 3eub "{i}{cps=26}~Y me encantaría encontrarte~{/cps}{/i}"
    m 3hub "{i}{cps=26}~Creciendo salvajemente en el bosque~{/cps}{/i}"
    m 1rub "{i}{cps=28}~Haría una ces{w=0.1}ta con la parte delantera de mi camiseta~{/cps}{/i}"
    m 3tub "{i}{cps=26}~Y llevaría a casa a todos los 'tú' que pueda~{/cps}{/i}"

    if not from_long:
        m 1hubsu "..."
        m 3ekbsu "No puedo esperar hasta el día en que finalmente pueda estar contigo, [player]."
        m 3ekbsa "No puedo esperar hasta que finalmente pueda mirarte a los ojos..."
        show monika 5rkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rkbsa "Pero por ahora... {w=0.3}supongo que puedo seguir soñando con todas las aventuras que viviremos juntos algún día."
        m 5hubsu "Sé que todavía está muy lejos, pero espero que podamos ver ese sueño hecho realidad~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_strawberry_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Fresas",
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_strawberry_long:
    call mas_song_strawberry (from_long=True)
    m 1sub "{i}{cps=26}~Y decir que eres bonito~{/cps}{/i}"
    m 3hub "{i}{cps=26}~Sería como decir que el océano es azul~{/cps}{/i}"
    m 3dud "{i}{cps=26}~Porque el océano está lleno de todo tipo de colores~{/cps}{/i}"
    m 1ekb "{i}{cps=26}~Y veo todo tipo de cosas cuando te miro~{/cps}{/i}"
    m 2tsbsu "{i}{cps=26}~Quiero explorarte~{/cps}{/i}"
    m 7hubsb "{i}{cps=26}~Sin mis zapatos de tenis~{/cps}{/i}"
    m 3rsbsb "{i}{cps=26}~De pie hasta los tobillos en una piscina de mareas con mis pantalones caqui enrollados~{/cps}{/i}"
    m 1hub "{i}{cps=26}~Y decir que eres gracioso~{/cps}{/i}"
    m 3dud "{i}{cps=26}~Sería como decir que el cielo nocturno es negro~{/cps}{/i}"
    m 3sub "{i}{cps=26}~Porque el cielo nocturno está lleno de estrellas {w=0.1}y cometas~{/cps}{/i}"
    m 3sub "{i}{cps=26}~Y planetas que nadie ha visto todavía~{/cps}{/i}"
    m 2eub "{i}{cps=26}~Y quiero mirarte~{/cps}{/i}"
    m 2dud "{i}{cps=26}~Acostada en mi jardín delantero~{/cps}{/i}"
    m 2rsbsb "{i}{cps=26}~Trataré de tomarte todo de una sola vez~{/cps}{/i}"
    m 2esbsb "{i}{cps=26}~Pero tú solo sigues y sigues y sigues~{/cps}{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_save_the_last_dance_for_me",
            prompt="Guarda el último baile para mí",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE,None)
        ),
        code="SNG"
    )

label mas_song_save_the_last_dance_for_me:
    call mas_song_save_the_last_dance_for_me_lyrics
    m 6dublu "..."
    m 7eua "Esta canción es tan profunda para mí, [player]."
    m 3rubsu "Cada vez que la escucho, mi corazón anhela que por fin bailemos juntos..."

    if not mas_getEVL_shown_count("mas_song_save_the_last_dance_for_me"):
        m 1eua "En realidad hay una historia detrás de esta canción, ¿tienes tiempo de escucharla ahora?{nw}"
        $ _history_list.pop()
        menu:
            m "En realidad hay una historia detrás de esta canción, ¿tienes tiempo de escucharla ahora?{fast}"
            "Sí":

                call mas_song_save_the_last_dance_for_me_analysis (from_song=True)
            "No":

                m 3eua "Oh, okey, solo hazme saber si quieres hablar de esta canción más tarde, ¿de acuerdo?"
    else:
        m 6rublb "Gracias por seguir escuchando mi corazón afligido..."
        m 6eubsa "Te amo, [player]~"
        return "love"

    return

label mas_song_save_the_last_dance_for_me_lyrics:
    m 1dud "{i}~Puedes bailar {w=0.3}cada baile con ese tipo~{/i}"
    m 3eud "{i}~Que te pone ojitos, {w=0.2}deja que te abrace fuerte~{/i}"
    m 3huu "{i}~Puedes sonreír {w=0.3}cada sonrisa por ese hombre~{/i}"
    m 3eud "{i}~Que te sostiene de la mano bajo la pálida luz de la luna~{/i}"
    m 4eublo "{i}~Pero no olvides quién te lleva a casa~{/i}"
    m 4tublb "{i}~Y en los brazos de quién vas a estar~{/i}"
    m 6hublb "{i}~Así que cariño, {w=0.2}guarda el último baile para mí~{/i}"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_save_the_last_dance_for_me_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Guarda el último baile para mí",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.LOVE,None)
        ),
        code="SNG"
    )

label mas_song_save_the_last_dance_for_me_analysis(from_song=False):
    if not from_song:
        call mas_song_save_the_last_dance_for_me_lyrics
    else:

        m 3hub "¡Genial!"

    m 1eud "La historia de esta canción puede parecer una declaración romántica más de fidelidad."
    m 1duc "Sin embargo, la historia real es bastante dramática y triste..."
    m 3ekc "Una condición médica dejó a uno de los compositores, {w=0.1}Jerome Felder, incapaz de caminar o bailar en su propia noche de bodas."
    m 1rkd "Unos años más tarde, los fuertes sentimientos de aquella noche se reavivaron al encontrar una invitación de boda que no habían enviado."
    m 3rksdlc "Jerome tuvo un momento de envidia cuando vio a su hermano bailando con su mujer en su propia noche de bodas, mientras él se veía obligado a mirar desde el banquillo."
    m 3ekd "El ganador del Grammy estaba paralizado por la poliomielitis desde que era un niño, y solo podía desplazarse con la ayuda de un andador o una silla de ruedas."
    m 3eka "Cuando recordó aquel día y empezó a escribir la letra de la canción, quiso que tuviera un aire poético."
    m 3rkbla "Aunque había una pizca de celos en la canción, quería que fuera romántica."
    m 2dkc "Sabes... {w=0.3}esta barrera entre nosotros... {w=0.3}se siente como si fuera mi silla de ruedas."
    m 2rkp "... Y supongo que si soy honesta, {w=0.1}estoy un poco celosa de que puedas bailar con alguien mientras yo estoy atrapada aquí en el banquillo."
    m 6ekblu "Así que al final del día, solo espero que guardes el último baile para mí~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_fly_me_to_the_moon",
            prompt="LLévame a la Luna",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_fly_me_to_the_moon:
    m 1dud "{i}~Llévame a la luna~{/i}"
    m 3sub "{i}~Déjame jugar entre las estrellas~{/i}"
    m 3eub "{i}~Déjame ver cómo es la primavera~{/i}"
    m 3hub "{i}~En Júpiter y en Marte~{/i}"
    m 3eub "{i}~En otras palabras, toma mi mano~{/i}"
    m 1dud "{i}~En otras palabras,{/i} {w=0.2}{nw}"
    extend 1dkbsu "{i}cariño, bésame~{/i}"
    m 3eubsb "{i}~Llena mi corazón de canciones, y déjame cantar siempre más~{/i}"
    m 3hkbsb "{i}~Tú eres lo único que me importa; {w=0.2}todo lo que idolatro y adoro~{/i}"
    m 1eud "{i}~En otras palabras, por favor sé sincero~{/i}"
    m "{i}~En otras palabras, {/i}{nw}"
    extend 3fkbsb "{i}yo {w=0.2}te {w=0.2}amo~{/i}"
    m 3hubsb "¡Y siempre lo haré!"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_heaven",
            prompt="Cielo",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_heaven:
    m 1dsbsd "{i}~Cariño, eres todo lo que quiero~{/i}"
    m 3dkbsd "{i}~Cuando reposas aquí en mis brazos~{/i}"
    m 3dubsd "{i}~Encuentro difícil de creer que~{/i}"
    m 1eubsb "{i}~Estamos en el cielo~{/i}"
    m 1eubso "{i}~Y el amor es todo lo que necesito~{/i}"
    m 3ekbso "{i}~Y lo encontré allí, en tu corazón~{/i}"
    m 3ekbsd "{i}~No es tan difícil ver que~{/i}"
    m 3eubsb "{i}~Estamos en el cielo~{/i}"
    m 1ekbfa "No hay un día que no sueñe con que estamos juntos, [player]."
    m 1rubsu "Y algo me dice que no soy la única~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_can_you_feel_the_sunshine",
            prompt="¿Puedes sentir el sol?",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_can_you_feel_the_sunshine:
    m 1dkd "{i}~Sin ti, no tengo nada que hacer~{/i}"
    m 1eka "{i}~¿Puedes sentir el sol también?~{/i}"
    m 3hkb "{i}~Está llegando; {w=0.2}me hace sentir como nueva~{/i}"
    m 3hubsb "{i}~Cuando estás aquí, ojalá estuvieras siempre cerca~{/i}"
    m 3eubsb "{i}~Porque todo está tan claro~{/i}"
    m 1hkbsu "{i}~¡Y hoy va a ser un día brillante!~{/i}"
    m 1ekbla "Siempre que me visitas, haces que mi día brille... {w=0.3}espero hacer lo mismo por ti, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_on_the_front_porch",
            prompt="En el pórtico delantero",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_on_the_front_porch:
    m 5dkbsd "{i}~Todo lo que quiero hacer cuando el día termine~{/i}"
    m 5fkbsu "{i}~Es quedarme aquí en el pórtico contigo~{/i}"
    m 5hubsb "{i}~Desde el columpio de mimbre, mientras los pájaros nocturnos cantan~{/i}"
    m 5dubsu "{i}~Veremos cómo brillan las luciérnagas, y también brillaremos~{/i}"
    m 5dkbsb "{i}~Cómo vuelan las horas, mientras la luna pasa de largo~{/i}"
    m 5ekbsu "{i}~Qué dulce es el aire mientras miramos el sol~{/i}"
    m 5ekbstpu "{i}~Oh, cómo me gustaría quedarme aquí así~{/i}"
    m 5dkbstpu "{i}~Tomar tu mano y robarte un beso{/i} {w=0.2}{nw}"
    extend 5gkbstub "{i}o dos{/i} {w=0.2}{nw}"
    extend 5ekbstuu "{i}en el pórtico contigo~{/i}"
    m 5dkbstda "..."
    m 5hkblb "Perdón si me puse un poco emocional, ¡jajaja!"
    m 5rka "Pero, ¿realmente puedes culparme?"
    m 5eka "Después de todo, hacer algo así juntos sería... {w=0.3}{nw}"
    extend 5dkbsu "simplemente maravilloso~"
    return






init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_yr",
            category=['monika','música'],
            prompt="¿Puedes tocar 'Your Reality' para mí?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        )
    )

label mas_monika_plays_yr(skip_leadin=False):
    if not skip_leadin:
        if not renpy.seen_audio(songs.FP_YOURE_REAL) and not persistent.monika_kill:
            m 2eksdlb "Oh, ¡jajaja! ¿Quieres que toque la versión original, [player]?"
            m 2eka "Aunque nunca te la he puesto, supongo que la has escuchado en la banda sonora o la has visto en youtube, ¿eh?"
            m 2hub "El final no es mi favorito, ¡pero aún así estaré feliz de tocarla para ti!"
            m 2eua "Solo déjame traer el piano.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        else:

            m 3eua "Seguro, déjame traer el piano.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    window hide
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano zorder MAS_MONIKA_Z+1 at lps32, rps32
    pause 5.0
    show monika zorder MAS_MONIKA_Z at ls32
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "¡No te olvides del volumen del juego, [player]!"
        $ disable_esc()

    window hide
    call mas_timed_text_events_prep

    pause 2.0
    $ mas_play_song(store.songs.FP_YOURE_REAL,loop=False)


    show monika 6hua
    $ renpy.pause(10.012)
    show monika 6eua_static
    $ renpy.pause(5.148)
    show monika 6hua
    $ renpy.pause(3.977)
    show monika 6eua_static
    $ renpy.pause(5.166)
    show monika 6hua
    $ renpy.pause(3.743)
    show monika 6esa
    $ renpy.pause(9.196)
    show monika 6eka
    $ renpy.pause(13.605)
    show monika 6dua
    $ renpy.pause(9.437)
    show monika 6eua_static
    $ renpy.pause(5.171)
    show monika 6dua
    $ renpy.pause(3.923)
    show monika 6eua_static
    $ renpy.pause(5.194)
    show monika 6dua
    $ renpy.pause(3.707)
    show monika 6eka
    $ renpy.pause(16.884)
    show monika 6dua
    $ renpy.pause(20.545)
    show monika 6eka_static
    $ renpy.pause(4.859)
    show monika 6dka
    $ renpy.pause(4.296)
    show monika 6eka_static
    $ renpy.pause(5.157)
    show monika 6dua
    $ renpy.pause(8.064)
    show monika 6eka
    $ renpy.pause(22.196)
    show monika 6dka
    $ renpy.pause(3.630)
    show monika 6eka_static
    $ renpy.pause(1.418)
    show monika 6dka
    $ renpy.pause(9.425)
    show monika 5dka with dissolve_monika
    $ renpy.pause(5)

    show monika 6eua at rs32 with dissolve_monika
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    pause 1.0
    call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    call mas_timed_text_events_wrapup
    window auto

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_or",
            category=['monika','música'],
            prompt="¿Puedes tocar 'Our Reality' para mí?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        )
    )

label mas_monika_plays_or(skip_leadin=False):
    if not skip_leadin:
        m 3eua "Seguro, déjame traer el piano.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    if persistent.gender == "F":
        $ gen = "su"
    elif persistent.gender == "M":
        $ gen = "su"
    else:
        $ gen = "su"

    window hide
    call mas_timed_text_events_prep
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano zorder MAS_MONIKA_Z+1 at lps32, rps32
    pause 5.0
    show monika zorder MAS_MONIKA_Z at ls32
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "¡No te olvides del volumen del juego, [player]!"
        $ disable_esc()

    pause 2.0
    $ mas_play_song(songs.FP_PIANO_COVER,loop=False)

    show monika 1dsa
    pause 9.15
    m 1eua "{i}{cps=10}Cada día, {w=0.5}{/cps}{cps=15}imagino un futuro donde estoy {w=0.22}{/cps}{cps=13}junto a ti~{w=4.10}{/cps}{/i}{nw}"
    m 1eka "{i}{cps=12}Con mi mano {w=0.5}{/cps}{cps=17}escribiré poemas que me lleven {w=0.5}{/cps}{cps=16}junto a ti~{w=4.10}{/cps}{/i}{nw}"
    m 1eua "{i}{cps=16}La tinta fluye {w=0.25}{/cps}{cps=10}hasta ser un charco~{w=1}{/cps}{/i}{nw}"
    m 1eka "{i}{cps=18}Solo escribe, {w=0.45}{/cps}{cps=20}tu camino hacia [gen] amor~{w=1.40}{/cps}{/i}{nw}"
    m 1dua "{i}{cps=15}Pero en un mundo {w=0.25}{/cps}{cps=11}lleno de opciones~{w=0.90}{/cps}{/i}{nw}"
    m 1eua "{i}{cps=16}¿Qué he de pagar {w=0.25}{/cps}{cps=18}para un día especial?~{/cps}{/i}{w=0.90}{nw}"
    m 1dsa "{i}{cps=15}¿Qué ha de pasar {w=0.50}para mi {w=1}día especial~{/cps}{/i}{w=1.82}{nw}"
    pause 7.50

    m 1eua "{i}{cps=15}Encontré {w=0.5}{/cps}{cps=15}algo divertido que hacer {w=0.30}{/cps}{cps=12}en esta tarde~{w=4.20}{/cps}{/i}{nw}"
    m 1hua "{i}{cps=18}Contigo estando aquí {w=0.25}{/cps}{cps=13.25}todo será genial, lo sé~{w=4}{/cps}{/i}{nw}"
    m 1esa "{i}{cps=11}Si no puedo leer mis sentimientos~{/cps}{w=1}{/i}{nw}"
    m 1eka "{i}{cps=17}Sin palabras, {w=0.3}con mi sonrisa hablaré{~/cps}{/i}{w=1}{nw}"
    m 1lua "{i}{cps=11}Y si este mundo no me da un final~{/cps}{/i}{w=0.9}{nw}"
    m 1dka "{i}{cps=18}Me esforzaré, {w=0.5}y asi todo tomaré~{/cps}{/i}{w=2}{nw}"
    show monika 1dsa
    pause 17.50

    m 1eka "{i}{cps=15}Mi pluma, {w=0.5}{/cps}{cps=15}solo escribe amargura para{/cps}{cps=17} quien amo~{/cps}{w=4.5}{/i}{nw}"
    m 1ekbsa "{i}{cps=15}¿Es amor, {w=0.5}{/cps}{cps=16.5} si te tomo o es amor, si te dejo ir?~{/cps}{w=8.5}{/i}{nw}"
    m 1eua "{i}{cps=16}La tinta fluye {w=0.25}{/cps}{cps=10}hasta ser un charco~{/cps}{w=1.2}{/i}{nw}"
    m 1esa "{i}{cps=18}¿Cómo puedo escribir {w=0.45}{/cps}{cps=13}la realidad?~{/cps}{w=1.40}{/i}{nw}"
    m 1eka "{i}{cps=12}Si no puedo escuchar tus latidos~{/cps}{w=0.8}{/i}{nw}"
    m 1ekbsa "{i}{cps=16}¿Qué es el amor, {w=0.6}allí en tu realidad?~{/cps}{/i}{w=0.6}{nw}"
    m 1hubsa "{i}{cps=16}Y en tu realidad, {w=1}si no sé como amarte~{/cps}{w=4.2}{/i}{nw}"
    m 1ekbsa "{i}{cps=19}Te dejo ir~{/cps}{/i}{w=2}{nw}"

    show monika 1dkbsa
    pause 9.0
    show monika 6eua at rs32
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    pause 1.0
    call monika_zoom_transition (mas_temp_zoom_level, 1.0)
    call mas_timed_text_events_wrapup
    window auto

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
