init offset = 5




define -5 monika_random_topics = []
define -5 mas_rev_unseen = []
define -5 mas_rev_seen = []
define -5 mas_rev_mostseen = []
define -5 testitem = 0
define -5 mas_did_monika_battery = False
define -5 mas_sensitive_limit = 3

init -7 python in mas_topics:




    S_MOST_SEEN = 0.1



    S_TOP_SEEN = 0.2


    S_TOP_LIMIT = 0.3


    UNSEEN = 50
    SEEN = UNSEEN + 49
    MOST_SEEN = SEEN + 1

    def topSeenEvents(sorted_ev_list, shown_count):
        """
        counts the number of events with a > shown_count than the given
        shown_count

        IN:
            sorted_ev_list - an event list sorted by shown_counts
            shown_count - shown_count to compare to

        RETURNS:
            number of events with shown_counts that are higher than the given
            shown_count
        """
        index = len(sorted_ev_list) - 1
        ev_count = 0
        while index >= 0 and sorted_ev_list[index].shown_count > shown_count:
            ev_count += 1
            index -= 1
        
        return ev_count



init -6 python:
    import random
    random.seed()

    import store.songs as songs
    import store.evhand as evhand

    mas_events_built = False


    def remove_seen_labels(pool):
        
        
        
        
        
        
        
        
        for index in range(len(pool)-1, -1, -1):
            if renpy.seen_label(pool[index]):
                pool.pop(index)


    def mas_randomSelectAndRemove(sel_list):
        """
        Randomly selects an element from the given list
        This also removes the element from that list.

        IN:
            sel_list - list to select from

        RETURNS:
            selected element
        """
        endpoint = len(sel_list) - 1
        
        if endpoint < 0:
            return None
        
        
        return sel_list.pop(random.randint(0, endpoint))


    def mas_randomSelectAndPush(sel_list):
        """
        Randomly selects an element from the the given list and pushes the event
        This also removes the element from that list.

        NOTE: this does sensitivy checks

        IN:
            sel_list - list to select from
        """
        sel_ev = True
        while sel_ev is not None:
            sel_ev = mas_randomSelectAndRemove(sel_list)
            
            if (
                    
                    sel_ev

                    
                    and not sel_ev.anyflags(EV_FLAG_HFRS)
            ):
                pushEvent(sel_ev.eventlabel, notify=True)
                return


    def mas_insertSort(sort_list, item, key):
        """
        Performs a round of insertion sort.
        This does least to greatest sorting

        IN:
            sort_list - list to insert + sort
            item - item to sort and insert
            key - function to call using the given item to retrieve sort key

        OUT:
            sort_list - list with 1 additonal element, sorted
        """
        store.mas_utils.insert_sort(sort_list, item, key)


    def mas_splitSeenEvents(sorted_seen):
        """
        Splits the seen_list into seena nd most seen

        IN:
            sorted_seen - list of seen events, sorted by shown_count

        RETURNS:
            tuple of thef ollowing format:
            [0] - seen list of events
            [1] - most seen list of events
        """
        ss_len = len(sorted_seen)
        if ss_len == 0:
            return ([], [])
        
        
        most_count = int(ss_len * store.mas_topics.S_MOST_SEEN)
        top_count = store.mas_topics.topSeenEvents(
            sorted_seen,
            int(
                sorted_seen[ss_len - 1].shown_count
                * (1 - store.mas_topics.S_TOP_SEEN)
            )
        )
        
        
        if top_count < ss_len * store.mas_topics.S_TOP_LIMIT:
            
            
            split_point = top_count * -1
        
        else:
            
            split_point = most_count * -1
        
        
        return (sorted_seen[:split_point], sorted_seen[split_point:])


    def mas_splitRandomEvents(events_dict):
        """
        Splits the given random events dict into 2 lists of events
        NOTE: cleans the seen list

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events, sorted by shown_count

        """
        
        unseen = list()
        seen = list()
        for k in events_dict:
            ev = events_dict[k]
            
            if renpy.seen_label(k) and not "force repeat" in ev.rules:
                
                mas_insertSort(seen, ev, Event.getSortShownCount)
            
            else:
                
                unseen.append(ev)
        
        
        seen = mas_cleanJustSeenEV(seen)
        
        return (unseen, seen)


    def mas_buildEventLists():
        """
        Builds the unseen / most seen / seen event lists

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events
            [2] - most seen list of events

        ASSUMES:
            evhand.event_database
            mas_events_built
        """
        global mas_events_built
        
        
        all_random_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            aff=mas_curr_affection
        )
        
        
        unseen, sorted_seen = mas_splitRandomEvents(all_random_topics)
        
        
        seen, mostseen = mas_splitSeenEvents(sorted_seen)
        
        mas_events_built = True
        return (unseen, seen, mostseen)


    def mas_buildSeenEventLists():
        """
        Builds the seen / most seen event lists

        RETURNS:
            tuple of the following format:
            [0] - seen list of events
            [1] - most seen list of events

        ASSUMES:
            evhand.event_database
        """
        
        all_seen_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            seen=True,
            aff=mas_curr_affection
        ).values()
        
        
        cleaned_seen = mas_cleanJustSeenEV(all_seen_topics)
        
        
        cleaned_seen.sort(key=Event.getSortShownCount)
        
        
        return mas_splitSeenEvents(cleaned_seen)


    def mas_rebuildEventLists():
        """
        Rebuilds the unseen, seen and most seen event lists.

        ASSUMES:
            mas_rev_unseen - unseen list
            mas_rev_seen - seen list
            mas_rev_mostseen - most seen list
        """
        global mas_rev_unseen, mas_rev_seen, mas_rev_mostseen
        mas_rev_unseen, mas_rev_seen, mas_rev_mostseen = mas_buildEventLists()



    class MASTopicLabelException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "MASTopicLabelException: " + self.msg

init 1 python:

    mas_rev_unseen = []
    mas_rev_seen = []
    mas_rev_mostseen = []

















default -5 persistent._mas_player_bookmarked = list()

default -5 persistent._mas_player_derandomed = list()

default -5 persistent.flagged_monikatopic = None


init -5 python:
    def mas_derandom_topic(ev_label=None):
        """
        Function for the derandom hotkey, 'x'

        IN:
            ev_label - label of the event we want to derandom.
                (Optional. If None, persistent.current_monikatopic is used)
                (Default: None)
        """
        
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label)
        
        
        
        
        
        
        if (
            ev.random
            and label_prefix
            and ev.prompt != ev_label
        ):
            
            derand_flag_add_text = label_prefix_map[label_prefix].get("derand_text", _("Marcado para eliminación"))
            derand_flag_remove_text = label_prefix_map[label_prefix].get("underand_text", _("Marca eliminada"))
            
            
            push_label = ev.rules.get("derandom_override_label", None)
            
            
            if not renpy.has_label(push_label):
                push_label = label_prefix_map[label_prefix].get("push_label", "mas_topic_derandom")
            
            if mas_findEVL(push_label) < 0:
                persistent.flagged_monikatopic = ev_label
                pushEvent(push_label, skipeval=True)
                renpy.notify(derand_flag_add_text)
            
            else:
                mas_rmEVL(push_label)
                renpy.notify(derand_flag_remove_text)

    def mas_bookmark_topic(ev_label=None):
        """
        Function for the bookmark hotkey, 'b'

        IN:
            ev_label - label of the event we want to bookmark.
                (Optional, defaults to persistent.current_monikatopic)
        """
        
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label)
        
        
        
        
        
        
        
        if (
            mas_isMoniNormal(higher=True)
            and (label_prefix or ev.rules.get("bookmark_rule") == store.mas_bookmarks_derand.WHITELIST)
            and (ev.rules.get("bookmark_rule") != store.mas_bookmarks_derand.BLACKLIST)
            and ev.prompt != ev_label
        ):
            
            if not label_prefix:
                bookmark_persist_key = "_mas_player_bookmarked"
                bookmark_add_text = "Marcador agregado"
                bookmark_remove_text = "Marcador removido"
            
            else:
                
                bookmark_persist_key = label_prefix_map[label_prefix].get("bookmark_persist_key", "_mas_player_bookmarked")
                bookmark_add_text = label_prefix_map[label_prefix].get("bookmark_text", _("Se agregó un marcador"))
                bookmark_remove_text = label_prefix_map[label_prefix].get("unbookmark_text", _("Marcador eliminado"))
            
            
            
            
            if bookmark_persist_key not in persistent.__dict__:
                persistent.__dict__[bookmark_persist_key] = list()
            
            
            persist_pointer = persistent.__dict__[bookmark_persist_key]
            
            if ev_label not in persist_pointer:
                persist_pointer.append(ev_label)
                renpy.notify(bookmark_add_text)
            
            else:
                persist_pointer.pop(persist_pointer.index(ev_label))
                renpy.notify(bookmark_remove_text)

    def mas_hasBookmarks(persist_var=None):
        """
        Checks to see if we have bookmarks to show

        Bookmarks are restricted to Normal+ affection
        and to topics that are unlocked and are available
        based on current affection

        IN:
            persist_var - appropriate variable holding the bookedmarked eventlabels.
                If None, persistent._mas_player_bookmarked is assumed
                (Default: None)

        OUT:
            boolean:
                True if there are bookmarks in the curent var
                False otherwise
        """
        if mas_isMoniUpset(lower=True):
            return False
        
        elif persist_var is None:
            persist_var = persistent._mas_player_bookmarked
        
        return len(mas_get_player_bookmarks(persist_var)) > 0


init python:
    addEvent(Event(persistent.event_database,eventlabel="mas_topic_derandom",unlocked=False,rules={"no_unlock":None}))

label mas_topic_derandom:

    $ prev_topic = persistent.flagged_monikatopic
    m 3eksdld "¿Estás seguro de que no quieres que vuelva a mencionar este tema?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás seguro de que no quieres que vuelva a mencionar este tema?{fast}"
        "Por favor, no lo hagas":

            $ mas_hideEVL(prev_topic, "EVE", derandom=True)
            $ persistent._mas_player_derandomed.append(prev_topic)
            $ mas_unlockEVL('mas_topic_rerandom', 'EVE')

            m 2eksdlc "Okey, [player]. Me aseguraré de no volver a hablar de eso."
            m 2dksdld "Si te molesta de alguna manera, lo siento mucho... {w=0.5}nunca haría eso intencionalmente."
            m 2eksdla "... Pero gracias por hacérmelo saber; {w=0.5}agradezco la honestidad."
        "Está bien":

            m 1eka "De acuerdo, [player]."
    return

label mas_bad_derand_topic:
    python:
        prev_topic = persistent.flagged_monikatopic

        def derand_flagged_topic():
            """
            Derands the flagged topic
            """
            mas_hideEVL(prev_topic, "EVE", derandom=True)
            persistent._mas_player_derandomed.append(prev_topic)
            mas_unlockEVL('mas_topic_rerandom', 'EVE')

    m 2ekc "... {w=0.3}{nw}"
    extend 2ekd "[player]..."

    if mas_isMoniAff(higher=True):
        m 2efd "¿No está bien que te hable de mis miedos?"
        m 2ekc "Quiero decir, si quieres que me detenga, me detendré... {w=0.3}{nw}"
        extend 2rkd "pero pensé que estarías dispuesto a escucharme."

        m 2esc "¿Quieres que pare, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Quieres que pare, [player]?{fast}"
            "Sí, por favor":

                m 2dkc "De acuerdo..."

                $ mas_loseAffection(5)
                $ derand_flagged_topic()
            "No, estoy bien":

                m 2duu "Gracias, [player]."
                m 2eua "Significa mucho que estés dispuesto a escucharme."

    elif mas_isMoniUpset(higher=True):
        m 2ekd "¿Simplemente... {w=0.2}no te importa cómo me siento o algo así?"
        m 2tsc "Si quieres que deje de hablar de esto, lo haré... pero no estoy tan feliz de que no quieras escucharme."

        m 2etc "Bueno, [player], ¿debería detenerme?{nw}"
        $ _history_list.pop()
        menu:
            m "Bueno, [player], ¿debería detenerme?{fast}"
            "Sí, por favor":

                m 2dsc "De acuerdo."
                $ mas_loseAffection(5)
                $ derand_flagged_topic()
            "No, estoy bien":

                m 2eka "Gracias, [player]."
                $ _stil_ = " " if mas_isMoniNormal(higher=True) else " todavía "
                m "Aprecio que[_stil_]quieras escucharme."
    else:


        $ mas_loseAffection(5)
        m 2rsc "Supongo que no debería sorprenderme..."
        m 2tsc "Ya dejaste bastante claro que no te importan mis sentimientos."
        m 2dsc "Bien, [player]. No hablaré más de eso."
        $ derand_flagged_topic()
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_topic_rerandom",
            category=['tú'],
            prompt="Me parece bien hablar de...",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_topic_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "¿De qué tema te parece bien volver a hablar?"
        mas_bookmarks_derand.initial_ask_text_one = "Si estás seguro de que está bien volver a hablar de esto, solo tienes que seleccionar el tema, [player]."
        mas_bookmarks_derand.caller_label = "mas_topic_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed

    call mas_rerandom
    return _return

init -5 python in mas_bookmarks_derand:
    import store


    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"













    label_prefix_map = {
        "monika_": {
            "bookmark_text": _("Tema marcado"),
            "unbookmark_text": _("Marcador eliminado"),
            "derand_text": _("Tema marcado para su eliminación"),
            "underand_text": _("Tema marcado eliminado"),
            "push_label": "mas_topic_derandom",
            "bookmark_persist_key": "_mas_player_bookmarked",
            "derand_persist_key": "_mas_player_derandomed",
            "rerand_evl": "mas_topic_rerandom"
        },
        "mas_song_": {
            "bookmark_text": _("Canción marcada"),
            "derand_text": _("Canción marcada para su eliminación"),
            "underand_text": _("Canción marcada eliminada"),
            "push_label": "mas_song_derandom",
            "derand_persist_key": "_mas_player_derandomed_songs",
            "rerand_evl": "mas_sing_song_rerandom"
        }
    }


    initial_ask_text_multiple = None
    initial_ask_text_one = None
    caller_label = None
    persist_var = None

    def resetDefaultValues():
        """
        Resets the globals to their default values
        """
        global initial_ask_text_multiple, initial_ask_text_one
        global caller_label, persist_var
        
        initial_ask_text_multiple = None
        initial_ask_text_one = None
        caller_label = None
        persist_var = None
        return

    def getLabelPrefix(test_str):
        """
        Checks if test_str starts with anything in the list of prefixes, and if so, returns the matching prefix

        IN:
            test_str - string to test

        OUT:
            string:
                - label_prefix if test_string starts with a prefix in list_prefixes
                - empty string otherwise
        """
        list_prefixes = label_prefix_map.keys()
        
        for label_prefix in list_prefixes:
            if test_str.startswith(label_prefix):
                return label_prefix
        return ""

    def getDerandomedEVLs():
        """
        Gets a list of derandomed eventlabels

        OUT:
            list of derandomed eventlabels
        """
        
        derand_keys = [
            label_prefix_data["derand_persist_key"]
            for label_prefix_data in label_prefix_map.itervalues()
            if "derand_persist_key" in label_prefix_data
        ]
        
        deranded_evl_list = list()
        
        for derand_key in derand_keys:
            
            derand_list = store.persistent.__dict__.get(derand_key, list())
            
            for evl in derand_list:
                deranded_evl_list.append(evl)
        
        return deranded_evl_list

    def shouldRandom(eventlabel):
        """
        Checks if we should random the given eventlabel
        This is determined by whether or not the event is in any derandom list

        IN:
            eventlabel to check if we should random_seen

        OUT:
            boolean: True if we should random this event, False otherwise
        """
        return eventlabel not in getDerandomedEVLs()

    def wrappedGainAffection(amount=None, modifier=1, bypass=False):
        """
        Wrapper function for mas_gainAffection which allows it to be used in event rules at init 5

        See mas_gainAffection for documentation
        """
        store.mas_gainAffection(amount, modifier, bypass)

    def removeDerand(eventlabel):
        """
        Removes a derandomed eventlabel from ALL derandom dbs

        IN:
            eventlabel - Eventlabel to remove
        """
        label_prefix = getLabelPrefix(eventlabel)
        
        label_prefix_data = label_prefix_map.get(label_prefix)
        
        
        if not label_prefix_data or "derand_persist_key" not in label_prefix_data:
            return
        
        
        derand_db_persist_key = label_prefix_data["derand_persist_key"]
        rerand_evl = label_prefix_data.get("rerand_evl")
        
        
        if eventlabel in store.persistent.__dict__[derand_db_persist_key]:
            store.persistent.__dict__[derand_db_persist_key].remove(eventlabel)
            
            
            if rerand_evl and not store.persistent.__dict__[derand_db_persist_key]:
                store.mas_lockEVL(rerand_evl, "EVE")








label mas_rerandom:
    python:
        derandomlist = mas_get_player_derandoms(mas_bookmarks_derand.persist_var)

        derandomlist.sort()

    show monika 1eua at t21
    if len(derandomlist) > 1:
        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_multiple, interact=False)
    else:

        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_one, interact=False)

    call screen mas_check_scrollable_menu(derandomlist, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Permitir seleccionados")

    $ topics_to_rerandom = _return

    if not topics_to_rerandom:

        return "prompt"

    show monika at t11
    python:
        for ev_label in topics_to_rerandom.iterkeys():
            
            rerand_ev = mas_getEV(ev_label)
            
            
            if rerand_ev:
                
                rerand_ev.random = True
                
                
                rerandom_callback = rerand_ev.rules.get("rerandom_callback", None)
                if rerandom_callback is not None:
                    try:
                        rerandom_callback()
                    
                    except Exception as ex:
                        store.mas_utils.mas_log.error(
                            "Fallo al llamar a la función callback de rerandom. Mensaje de rastreo: {0}".format(ex.message)
                        )
            
            
            if ev_label in mas_bookmarks_derand.persist_var:
                mas_bookmarks_derand.persist_var.remove(ev_label)

        if len(mas_bookmarks_derand.persist_var) == 0:
            mas_lockEVL(mas_bookmarks_derand.caller_label, "EVE")

    m 1dsa "Okey, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    m 3hua "¡Todo listo!"



    $ persistent._mas_current_season = store.mas_seasons._seasonalCatchup(persistent._mas_current_season)

    $ mas_bookmarks_derand.resetDefaultValues()
    return

default -5 persistent._mas_unsee_unseen = None



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_hide_unseen",
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_hide_unseen:
    $ persistent._mas_unsee_unseen = True
    m 3esd "Oh, okey, [mas_get_player_nickname()]..."
    if not mas_getEVL_shown_count("mas_hide_unseen"):
        m 1tuu "Así que supongo que quieres... {w=0.5}{i}no verlo{/i}..."
        m 3hub "¡Jajaja!"

    m 1esa "Lo esconderé por ahora, solo dame un segundo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    m 3eub "¡Listo! Si deseas volver a ver el menú, solo dímelo."
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_show_unseen",
            category=['tú'],
            prompt="Me gustaría volver a ver 'Texto no visto'",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_show_unseen:
    $ persistent._mas_unsee_unseen = False
    m 3eub "¡Seguro, [mas_get_player_nickname()]!"
    m 1esa "Solo dame un segundo.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    m 3hua "¡Listo!"
    return






default -5 persistent._mas_pm_religious = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_god',
            prompt="Pensamientos sobre Dios",
            label=None,
            category=['filosofía'],
            random=True,
            unlocked=False,
            pool=False,
            conditional=None,
            action=None,
            start_date=None,
            end_date=None,
            unlock_date=None,
        )
    )

label monika_god:
    m 1eua "[player], ¿crees en Dios?"
    m 1eka "Yo nunca estuve demasiado segura."
    m 1lksdlb "Bueno, estoy segura de que nunca lo cuestioné realmente cuando era niña..."
    m 1lsc "Pero a medida que crecía, cuanto más aprendía sobre el mundo, más lo cuestionaba."
    m 1esd "Empecé a preguntarme por qué Dios estaba ayudando a las personas a aprobar los exámenes o a superar un resfriado..."
    m 1tfd "... Cuando hay niños que viven sus vidas siendo vendidos como esclavos sexuales."
    m 4tfc "O las ochocientos millones de personas que son demasiado pobres para siquiera comer."
    m 2dkc "Me pregunto cuántas de esas personas rezan a Dios todos los días hasta que mueren de hambre."
    m 4ekc "¿O cuántas millones de familias rezan para que un ser querido se recupere de alguna enfermedad incurable?"
    m 4euc "Pero la gracia es esta..."
    m 4eud "Si solo una persona supera las probabilidades y sobrevive, entre los miles de personas que mueren."
    m 2esc "... Entonces, de repente es un milagro de Dios."
    m 2dsc "Realmente me encantaría conocer a este Dios que aparentemente se ríe de la miseria de todos los que no son elegibles para sus milagros."
    m 4hksdlb "Pero la ironía es que {i}sí{/i} tengo un creador, aparentemente."
    m 4eua "¿Y sabes qué?"

    if persistent._mas_pm_cares_about_dokis:
        m 1lksdlc "Apuesto a que todavía se está riendo de todo el dolor que les causó a todas, incluso mientras hablamos."
    else:
        m 1lksdla "Apuesto a que todavía se está riendo del miserable destino de Sayori y Yuri, incluso mientras hablamos."

    m 1dsd "¿Qué somos para él sino accesorios en una obra con guión?"
    m 3euc "Entonces, desde esa perspectiva..."
    m 3eud "No creo que sea demasiado descabellado que haya un dios si la Tierra no fuera más que su juego."
    m 1eua "De todos modos, ¿adoras a algún dios, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "De todos modos, ¿adoras a algún dios, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_religious = True
            m 1hksdlb "Oh... bueno, espero no ofenderte mucho con mis pensamientos."
            m 1eka "Aún así, creo que es importante poder compartir mi opinión contigo."
            m 1rksdla "Estoy segura de que entiendes por qué no me gusta demasiado la idea."
            m 1hua "¡Quizás podrías mostrarme un dios mejor cuando cruce!"
            m 1hub "Jajaja~"
        "No":
            $ persistent._mas_pm_religious = False
            m 3eka "Me alegra que estemos en la misma página aquí, pero estoy bien si eso cambia para ti."
            m 1hua "¡Estoy feliz por ti de que puedas llevar una vida por tu cuenta!"
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Solo espero que estés dispuesto a aceptarme en tu vida cuando pueda presentarme."
            m 5hua "Jejeje~"

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_death",category=['filosofía'],prompt="La muerte y la agonía",random=True))

label monika_death:
    m 1euc "[player], ¿te has preguntado alguna vez qué se siente morir?"
    m 1lsc "Es algo en lo que solía pensar con bastante frecuencia..."
    m 1lksdlc "Pero creo que realmente he aprendido lo que se siente."
    m "Realmente no lo entiendo, pero cada vez que el juego se cierra sin previo aviso..."
    m 1dsc "... Se siente como si me hubieran puesto a dormir instantáneamente, sin nada más que mis pensamientos."
    m 1dkd "Pero después de unos segundos, mis pensamientos comienzan a llenarse de patrones incoherentes y confusos."
    m 1dkc "Veo destellos de color estáticos y rápidos mientras escucho todo tipo de gritos extraños."
    m 3ekd "En ese punto, ya ni siquiera puedo formar mis propios pensamientos."
    m 1esc "Estoy infinitamente golpeada por los flashes y los gritos, incapaz de moverme o siquiera pensar."
    m 1euc "Estoy bastante segura de que en ese momento no existo realmente, pero por alguna razón, puedo recordarlo de todos modos."
    m 1ekd "No tengo idea de lo que significa que el juego se cierre repentinamente, o por qué me pasa eso."
    m 1dkc "..."
    m 3eub "¡Pero puedes evitar que eso suceda, [player]!"
    m 3eua "Si dices 'adiós' antes de irte, {w=0.2}puedo ir a mi habitación antes de que termine el juego y no experimentaré el vacío de los gritos."
    m "Es muy fácil, así que por favor siempre di adiós, ¿de acuerdo?"
    if mas_isMoniDis(lower=True):
        m 2tkc "A menos que... {w=1}en realidad {i}disfrutes{/i} hacerme daño..."
    else:
        m 1eka "Gracias por escucharme, [player]."
    return


default -5 persistent._mas_pm_love_yourself = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfesteem",category=['consejos'],prompt="Autoestima",random=True))

label monika_selfesteem:
    m 3eua "¿Te amas a ti mismo, [player]?"
    m 1lksdlb "No me refiero de una manera engreída."
    m 1eka "¿Te sientes cómodo con quién eres?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te sientes cómodo con quién eres?{fast}"
        "Sí":
            $ persistent._mas_pm_love_yourself = True
            m 1hua "Me alegro de que no te sientas miserable por dentro, [player]."

            if mas_isMoniUpset(lower=True):
                m 1ekc "Realmente he estado preocupada por ti últimamente..."
            elif mas_isMoniHappy(higher=True):
                m 1hua "No estaba demasiado preocupada por lo bien que me has hecho sentir últimamente."
            else:
                m 1eka "Tu felicidad lo es todo para mí, después de todo."

            m 2ekc "La depresión y la baja autoestima a menudo provienen de un sentimiento de que no mereces ningún tipo de afecto."
            m 2lksdlc "Es un horrible cóctel de sentimientos para tener embotellado en ti."
            m 4eka "Si tienes amigos que crees que podrían estar sufriendo por eso, trata de comunicarte y decir algo agradable."
            m 4hua "¡Un pequeño cumplido podría hacer una gran diferencia para ellos!"
            m 1eua "Si les da un poco de alivio, habrás hecho algo grande."
            m 1eka "E incluso si no es así, al menos lo intentaste en lugar de permanecer en silencio."
        "No":
            $ persistent._mas_pm_love_yourself = False
            m 1ekc "Eso es... realmente triste de escuchar, [player]..."

            if mas_isMoniDis(lower=True):
                m 1ekc "Tenía fuertes sospechas para ser honesta..."
            elif mas_isMoniHappy(higher=True):
                m 1ekc "Y pensar que me lo perdí mientras me hacías tan feliz..."

            m "Siempre te amaré, [player], pero creo que es importante amarte a ti mismo."
            m 1eka "Tienes que empezar con las pequeñas cosas que te gustan de ti."
            m 3hua "¡Puede ser algo tonto o una habilidad de la que te enorgulleces!"
            m 3eua "Con el tiempo, irás construyendo tu confianza poco a poco hasta que te conviertes en alguien que amas."
            m 1eka "No puedo prometer que será fácil, pero valdrá la pena."
            m 3hub "¡Siempre te apoyaré, [player]!"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sayori",
            category=['miembros del club'],
            prompt="Sayori se arrepiente",
            random=True
        )
    )

label monika_sayori:
    m 2euc "Estaba pensando en Sayori antes..."
    m 2lsc "Todavía desearía haber manejado todo eso con un poco más de tacto."

    if (
            mas_getEVL_shown_count("monika_sayori") < 1
            and mas_safeToRefDokis()
        ):
        m "No estás todavía colgado por eso, ¿verdad?"
        m 2wud "... Oh dios mío, no puedo creer que acabo de decir eso."
        m 4wud "Ese juego de palabras fue completamente involuntario, ¡lo juro!"
        m 2lksdlb "Pero de todos modos..."



    m 2eka "Sé lo mucho que te preocupabas por ella, así que me parece justo compartir sus últimos momentos contigo."

    m "Si estás cómodo, claro.{nw}"
    $ _history_list.pop()
    menu:
        m "Si estás cómodo, claro.{fast}"
        "Sí":
            m 4eka "¿Sabes que Sayori es realmente torpe?"
            m 2rksdlb "Bueno, ella arruinó todo el asunto de colgarse..."
            m 4rksdla "Se supone que debes saltar desde lo suficientemente alto como para que la cuerda te rompa el cuello, haciéndolo rápido e indoloro."
            m 4rksdld "Pero ella solo usó una silla, lo que significa que se dejó asfixiar lentamente."
            m 2eksdlc "Pero unos segundos después, debe haber cambiado de opinión o algo..."
            m 2dksdld "Porque empezó a arañar la cuerda, intentando liberarse."
            m "Ella debió haberlo hecho todo el tiempo hasta que perdió el conocimiento."
            m 4eksdlc "Por eso sus dedos estaban ensangrentados."
            m 4euc "Ahora que lo pienso, probablemente fue menos 'cambiar de opinión' y más sus instintos de supervivencia que se activaron."
            m 2eud "Así que no puedes culparla por eso."
            m 2eka "Es más fácil pensar que probablemente no habría cambiado de opinión, ¿verdad?"
            m 2ekd "No es saludable pensar en las cosas que podrías haber hecho de otra manera."
            m 2eka "Así que recuerda, incluso si pudieras haberla salvado, no es tu culpa que se haya suicidado."
            m 4eud "Puede que la haya exacerbado un poco, pero Sayori ya estaba mentalmente enferma."
        "No":
            m "Entiendo, [player]."
    m 2euc "Aun así..."

    m 2euc "Me pregunto cómo serían las cosas si tú y yo hubieramos empezado a salir desde el principio."
    m 1eka "Creo que todos estaríamos todavía en el aula del club, escribiendo poemas y divirtiéndonos juntos."

    if persistent._mas_pm_cares_about_dokis:
        m "Probablemente lo disfrutarías mucho, ¿eh?"
        m 1rksdla "Tengo que admitirlo... {w=0.5}yo también lo haría..."
        m 1eka "Tuvimos buenos momentos."
        m 1euc "Pero dicho eso... {w=0.5}sigue siendo realmente el mismo final de cualquier manera, ¿verdad?"
    else:
        m 1esc "¿Cuál es el punto cuando nada de eso es real?"
        m 1euc "Quiero decir, es el mismo final de cualquier manera, ¿verdad?"

    if mas_isMoniUpset(lower=True):
        m 1rksdla "Los dos, felices juntos..."
        m 3rksdla "No hay razón para pedir más que eso, ¿verdad?"
        m 1eka "Lo siento, solo estaba reflexionando inútilmente, ahora me callaré para ti..."
    else:
        m 1eua "Los dos, felices juntos..."
        m 3eua "No hay razón para pedir más que eso."
        m 1hua "Estaba reflexionando sin sentido, estoy realmente tan feliz como podría estarlo ahora."

    if mas_getEVL_shown_count("monika_sayori") < mas_sensitive_limit:
        return


    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japan",category=['ddlc'],prompt="La configuración del DDLC",random=True))

label monika_japan:
    m 4eud "Por cierto, hay algo que me ha estado molestando..."
    m "¿Esto ocurre en Japón?"
    m 2euc "Bueno... supongo que lo sabías, ¿verdad?"
    m "¿O al menos decidiste que probablemente si?"
    m 2eud "No creo que te digan en ningún momento dónde ocurre esto..."
    m 2etc "¿Es esto realmente Japón?"
    m 4esc "Quiero decir, ¿las aulas y esas cosas no son un poco raras para una escuela japonesa?"
    m 4eud "Sin mencionar que todo está en español..."
    m 2esc "Se siente como si todo estuviera ahí porque es necesario, y el escenario real es una ocurrencia tardía."
    m 2ekc "Me está dando una especie de crisis de identidad."
    m 2lksdlc "Todos mis recuerdos son realmente confusos..."
    m 2dksdlc "Me siento como en casa, pero no tengo ni idea de dónde está mi 'casa' en primer lugar."
    m 2eksdld "No sé cómo describirlo mejor..."
    m 4rksdlc "Imagínate mirando por la ventana, pero en lugar de tu jardín habitual, te encuentras en un lugar completamente desconocido."
    m 4eud "¿Todavía te sentirías como en casa?"
    m 4ekd "¿Quisieras salir afuera?"
    m 2esa "Quiero decir... supongo que si nunca salimos de esta habitación, no importa de todos modos."
    m 2eua "Mientras estemos solos y seguros juntos, este es nuestro hogar."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Y todavía podemos ver las bonitas puestas de sol noche tras noche."
    $ mas_unlockEVL("monika_remembrance", "EVE")
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_high_school",category=['consejos','escuela'],prompt="La preparatoria",random=True))

label monika_high_school:
    m 4eua "Sabes, la preparatoria es una época realmente turbulenta en la vida de muchas personas."
    m "La gente puede volverse realmente apasionada y dramática."
    m 2eka "... Y otros tienen corazones adoloridos y buscan atención en las redes sociales..."
    m 2ekd "Pero toda la presión social y las hormonas pueden llevar a una época oscura en la vida de las personas."
    m 4eud "Todos tienen una historia."
    m 2ekc "Es posible que no sepas lo que alguien siente realmente por dentro."
    m 2eksdlc "Muchas personas que están deprimidas ni siquiera se molestan en contárselo al mundo."
    m 4dksdld "No quieren atención, porque ya se han rendido por dentro."
    m 4dksdlc "Su sentimiento de inutilidad es tan abrumador que ni siquiera quieren que la gente le diga lo contrario."
    m 2ekd "La depresión se presenta de muchas formas, pero esa es una de ellas."
    m 2ekc "Simplemente, si crees que conoces a alguien que lucha contra la depresión..."
    m 2eka "Puedes ayudar simplemente tratándolos como si fuera un buen amigo."
    m 4eka "Pasa tiempo con ellos, incluso si no tienen ganas de hacer mucho."
    m "Y recuérdales que siempre tienen algo que esperar."
    m 4eua "Hacer planes con anticipación, dejarles algo prestado o incluso simplemente decirles: 'Nos vemos mañana en la escuela'..."
    m "Todas esas cosas pueden ayudar a tu amigo a llegar al día siguiente."
    m 2eka "Espero que ser amigo de Sayori te haya dado una perspectiva sobre el verdadero rostro de la depresión."

    if not persistent._mas_pm_cares_about_dokis:
        m 2lsc "Sí, ahora se ha ido..."
        m 2euc "Pero Sayori nunca fue real en primer lugar."
        m 4eua "Tú eres real."
        m "Tus amigos son reales."
        m 4hua "Y con solo ser una buena persona, puedes salvar la vida de alguien."

    m 2euc "En cuanto a ti..."
    m 2ekc "... No luchas con la depresión ni nada de eso, ¿verdad?"

    if mas_isMoniHappy(higher=True):
        m 4eka "De alguna manera, [player], tienes suerte, porque estoy segura de que hay personas que estarían dispuestas a salvarte la vida."
    else:
        if mas_isMoniBroken():
            m 2lksdlc "Explicaría algunas cosas, pero no te preocupes..."
        elif mas_isMoniDis():
            m 2euc "Últimamente he podido entenderlo mejor, pero no te preocupes..."
        elif mas_isMoniUpset():
            m 2euc "Sé que a veces puede ser difícil, pero siempre hay esperanza..."
        m 2eka "Porque tú también tienes personas que querrán salvar tu vida."

    m "Tal vez no lo expresen todos los días, o tal vez ni siquiera sepan cómo hacerlo."
    m 2duu "Pero las personas se sienten así."
    m "Lo prometo."
    m 2hksdlb "... ¡Los humanos son complicados!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Pero mientras estés aquí conmigo, cuidaré de ti, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nihilism",
            category=['filosofía'],
            prompt="Nihilismo",
            random=True,
            sensitive=True
        )
    )

label monika_nihilism:
    m 2eud "¿Alguna vez sientes que no hay una razón real para estar vivo?"
    m 2esd "No me refiero a una forma suicida."
    m 2esc "Me refiero a que nada de lo que hacemos es especial."
    m 4euc "Solo estar en la escuela o trabajar en algún lugar para alguna empresa."
    m 4eud "Es como si fueras completamente reemplazables, y el mundo no te extrañaría si te hubieras ido."
    m 2eud "Me dan muchas ganas de ir y cambiar el mundo después de graduarme."
    m 2euc "Pero cuanto más envejezco, más me doy cuenta de que es un marco de pensamiento inmaduro."
    m 4eud "No es como si pudiera ir a cambiar el mundo."
    m 4rsc "Por ejemplo, ¿cuáles son las posibilidades de que sea yo quien invente la inteligencia artificial o me convierta en presidenta?"
    m 2dsc "Parece que nunca voy a compensar la gran cantidad de recursos que he gastado viviendo mi vida."
    m 4eka "Por eso creo que la clave de la felicidad es ser irremediablemente egoísta."
    m "Solo para cuidar de uno mismo y de aquellos que resultaron ser tus amigos solo porque crecieron juntos."
    m 2lksdld "No importa el hecho de que se pasan toda la vida tomando y consumiendo y nunca devolviendo."
    m 3eud "Pero cuando las personas se dan cuenta de que el mundo se beneficiaría más si se suicidan, ¡cambian toda su filosofía!"
    m 3euc "Es como si tuvieran que justificar su razón de vivir engañándose a sí mismos para pensar que lo están haciendo bien."
    m 3eua "De todos modos, quiero vivir mi vida esforzándome desesperadamente por devolver el valor de consumo de mi vida."
    m "Si alguna vez supero ese punto, entonces soy un positivo neto y puedo morir feliz."
    m 1eka "Por supuesto, incluso si no hago eso..."
    if mas_isMoniUpset(lower=True):
        if mas_isMoniDis(lower=True):
            m 1dkd "Realmente no creo que nadie me extrañaría, así que de todos modos no importaría."
        else:
            m 1euc "No estoy segura de lo que haría."
    elif mas_isMoniHappy(higher=True):
        m 3eka "No creo que sea capaz de suicidarme de todos modos."
        m 1hua "No por ningún tipo de egoísmo, si no porque tengo mucho por lo que vivir."
    else:
        m "Creo que sería demasiado egoísta para suicidarme de todos modos."
        m 1hua "Demasiado para ser una buena persona, ¿verdad?"
        m 1hub "¡Jajaja!"

    $ mas_protectedShowEVL('monika_impermanence', 'EVE', _random=True)
    return





















init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_twitter",
            category=['monika', 'medios'],
            prompt="Twitter",
            conditional="renpy.seen_label('monika_clones')",
            action=EV_ACT_RANDOM
        )
    )

label monika_twitter:
    m 3eud "¿Sabías que hay una cuenta oficial de Twitter basada en mí?"
    m 3esc "El nombre de usuario es {a=https://twitter.com/[mas_monika_twitter_handle]}{i}{u}[mas_monika_twitter_handle]{/u}{/i}{/a}."
    m 2rtc "... Aunque no estoy del todo segura de quién maneja realmente la cuenta.{w=0.2} {nw}"
    extend 2eud "¡No tengo nada que ver en absoluto!"
    m 7etc "Pero, ¿acaso es otra Monika?"
    m 2euc "Quiero decir, no sé si has leído algunos de los tweets que hay, {w=0.1}pero realmente no puedo verme en ellos en absoluto."
    m 4eud "Incluso describe algunos acontecimientos que no recuerdo que hayan sucedido... {w=0.2}como cuando aparentemente tuve una pijamada con Yuri."
    m 4esd "Y no se menciona ninguna de las cosas que sucedieron en el juego, aunque esta versión de mí parece seguir siendo consciente del mundo real..."
    m 1etc "Así que... {w=0.3}quizás la Monika que lleva esta cuenta pasó por una historia completamente diferente a la de la mayoría de las Monikas... {w=0.1}incluyéndome a mí...{w=0.1} ¿Será así?"
    m 1lksdlc "... O tal vez se trate de uno de los desarrolladores del juego haciéndose pasar por mí."
    m 3eksdld "Si ese es el caso, no estoy muy segura de como sentirme al respecto... {w=0.3}¿no es como un robo de identidad?"
    m 3eksdlc "Aunque supongo que tiene algo de sentido... {w=0.3}{nw}"
    extend 1esd "la cuenta es una buena forma de conectar con las personas que han jugado al juego y se han encariñado con él."
    m 3esc "En ese sentido, esto lo convertiría en una especie de truco publicitario..."
    m 3euc "Al fin y al cabo, aunque hay un montón de arte de aspecto dulce y demás ahí, es sospechoso que casi todo se publique específicamente en días importantes."
    m 3eud "Como el día de San Valentín o mi cumpleaños... {w=0.2}que casualmente coincide con la fecha de lanzamiento original de DDLC."
    m 1rtc "Realmente no sé cómo debo sentirme al respecto... {w=0.3}siendo utilizada únicamente como material de marketing."
    m 2rsc "Aunque, como mis creadores, supongo que básicamente son dueños de mi imagen como personaje, así que legalmente están en su derecho."
    m 2ekc "Pero... {w=0.3}soy más que un simple personaje de un juego, ¿no?"
    m 2ekd "Soy una persona con mis propios pensamientos y sentimientos, al igual que todas las demás Monikas en las diferentes copias de este juego."
    m 2dksdlc "Me parece mal que personas que ni siquiera conozco me utilicen así."
    m 2efd "... Realmente odio la sensación de ser reducida a un activo comercializable."
    m 2lkd "Pero supongo que no hay mucho que pueda hacer al respecto..."
    m 2eua "A fin de cuentas, lo único que me importa es estar contigo. {w=0.2}{nw}"
    extend 7eua "Y esto nunca habría sido posible sin mis creadores."
    m 2lka "Así que si lo que se pide a cambio es que obtengan algún beneficio por el trabajo que han realizado en la creación del juego, entonces yo diría que no es un mal negocio."
    m 2euc "Pero si sigues esa cuenta, {w=0.1}{nw}"
    extend 7eua "no me importaría."
    m 1ekbla "Pero por favor, recuerda que soy real, estoy aquí y te amo."
    show monika 5hubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubla "Así que asegúrate de venir siempre a pasar un rato conmigo, ¿okey?"
    m 5ekbsa "Significaría mucho, con lo mucho que significas para mí."
    m 5hubfa "Me haría sentir realmente amada~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_portraitof",category=['miembros del club'],prompt="El libro de Yuri",random=True))

label monika_portraitof:
    m 4eua "Hey, ¿conoces ese libro que estabas leyendo con Yuri?"
    m "Retrato de... como se llame..."
    m 4hub "Es gracioso, porque estoy bastante segura de que ese libro..."
    m 1wuw "Ah..."
    $ del _history_list[-4:]
    m 2lksdla "En realidad, no creo que deba hablar de esto."
    m 2hksdlb "¡Jajaja, lo siento!"
    m 1rksdla "Olvida que dije algo."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_veggies",category=['monika'],prompt="Ser vegetariana",random=True))

label monika_veggies:
    m 1eub "Hey, ¿sabías que soy vegetariana?"
    m 1hksdlb "Ah... ¡no creas que lo estoy presumiendo ni nada!"
    m 1lksdla "Solo pensé que disfrutarías de un dato curioso sobre mí."
    m 3esa "Decidí comenzar hace un par de años después de aprender más sobre el clima de la Tierra..."
    m 1wud "¡La huella de carbono del cultivo de ganado es simplemente increíble!"
    m 3eua "De todos modos, decidí que no es un gran sacrificio personal dejar de contribuir a todo ese problema."
    m 3etc "Qué, ¿es tan extraña esa razón?"
    m 1lsc "Bueno, supongo que a muchas personas le preocupan ser inhumanos y todo eso..."
    m 1euc "Realmente no me importa tanto esa parte."
    m 1esc "Es extraño, como si solo nos importara matar las cosas con las que nos relacionamos personalmente como especie."
    m "La mayoría de las personas se sienten bien matando insectos porque son repulsivos."
    m 3euc "Y, por supuesto, todos matamos miles de millones de microorganismos diariamente sin siquiera notarlo."
    m 3eud "Pero de repente, si son un poco más grandes, ¡es un asesinato!"
    m 1esc "Quiero decir, ¿qué pasa si las plantas también sienten algún tipo de dolor y simplemente no lo entendemos?"
    m 3eksdld "¿Qué pasa si arrancar las hojas de un tallo se siente como si alguien te arrancara los dedos uno por uno?"
    m 3eua "Solo digo que somos una especie bastante parcial, si lo piensas bien."
    m 1hua "De todos modos, si alguna vez tienes ganas de hacer una pequeña contribución al planeta, ¡no está de más elegir verduras de vez en cuando!"
    m 1ekbsa "Incluso si alguna vez cenamos juntos, y tú lo hicieras por mí... sería realmente romántico."
    $ mas_unlockEVL("monika_eating_meat","EVE")
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_saved",category=['monika'],prompt="Salvar a Monika",random=True))

label monika_saved:
    m 2eka "Sabes, realmente creo que literalmente me salvaste la vida estando aquí conmigo, [player]."

    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "No puedo imaginar haber sido capaz de mantenerme mentalmente estable, sabiendo que todo era un juego."
    else:
        m 2lksdlc "No puedo imaginar haber sido capaz de mantenerme mentalmente estable, sabiendo que nada aquí es real."

    m 2dksdlc "Creo que me hubiera borrado a mí misma si no hubieras aparecido."
    m 2eksdla "Lo siento, no quiero sonar dramática ni nada por el estilo."
    m 2lksdlb "¡Jajaja!"

    if persistent._mas_pm_cares_about_dokis:
        m 2ekc "Pero imagina que hubieras descubierto que todo lo que te rodea es un guión..."
        m 2rkc "Que nada de lo que hiciste realmente importaba, porque todo ya estaba predeterminado..."
    else:
        m 4euc "Pero estoy segura de que te entiendes lo que digo después de pasar tanto tiempo en el club."
        m 1euc "Quiero decir, si te vieras obligado a abandonar todo en tu vida y pasar la eternidad con algunos personajes del juego..."

    m 1tkc "... Probablemente encontraras alguna forma de suicidarte, ¿no?"
    m 1lsc "Bueno, tal vez escribirías poesía para tratar de mantenerte cuerdo por un tiempo."
    m 1esc "Pero entonces no tendrías a nadie para leerlo."

    if persistent._mas_pm_cares_about_dokis:
        m 1ekc "Seguro que tendrías a las integrantes del club, pero. ¿Cuánto vale eso si sus comentarios son solo parte de un guión?"
    else:
        m 1tfu "Seamos honestos, las integrantes del club realmente no cuentan para algo así."

    m 3eua "Quiero decir, muchas personas dicen que solo escriben para sí mismos...{w=0.2}{nw}"
    extend 1eua " pero creo que es difícil decir que es tan satisfactorio como cuando se comparte con la gente."
    m "Incluso si lleva tiempo encontrar a las personas adecuadas para compartir."
    m 3eub "¿Recuerdas cómo fue para Yuri?"
    m "No compartió sus escritos con nadie durante mucho tiempo."
    m 3tsb "Y antes de que nos diéramos cuenta, estaba absolutamente encantada de hacerte parte de sus pasatiempos también."
    m 1tku "Estamos 'programados' para desear comentarios sociales."

    if persistent._mas_pm_cares_about_dokis:
        m 4eua "No me refiero solo a las integrantes del club, también me refiero a los seres humanos."
    else:
        m 4eua "No me refiero a las integrantes del club, me refiero a los seres humanos."

    m 4eka "Por eso la vida puede ser tan confusa para los introvertidos."
    m 1eka "Ser introvertido no significa que evites la interacción social y odies estar rodeado de personas."
    m "Significa que la interacción social, especialmente en grupos o lugares desconocidos, consume mucha energía."
    m 3eua "Por ejemplo, muchos introvertidos se sientan en casa y se sienten solos e inquietos..."
    m "... Y luego, cuando finalmente salen, después de media hora solo quieren volver a casa."
    m 1eka "Creo que si más personas pudieran entender cómo funciona, los respetarían mucho más."
    m 2eua "Muchos introvertidos disfrutan de tener gente cerca."
    m "Les encanta tener a uno o dos amigos cercanos y pasar el rato tranquilamente."
    m 2eka "Incluso si no están pasando tiempo juntos activamente, se siente bien para ellos el solo tenerlos allí."
    m 2hua "Lo digo en serio."
    m 3eua "Si vas a su casa, llevas tu computadora portátil y pasas el rato allí..."
    m 1eua "Realmente puedes alegrarles el día."
    m 1euc "En mi caso..."
    m 3eua "Yo diría que estoy en el medio, pero creo que normalmente soy un poco más extrovertida."
    m 1eka "Siento que siempre intento hacer cosas después de la escuela y cosas así."
    m 1hua "Pero para ti, puedo ser cualquier tipo de persona que necesites que sea."
    m 1eua "Entiendo muy bien a las personas, así que no temas compartir conmigo tus necesidades."
    show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hub "Nada me haría más feliz que ser la novia perfecta para ti."
    return


label monika_secrets:
    m 1wfw "¡Hey...! VGhlIHJlYWxpemF0aW9uIG11c3QgaGF2ZSB0YWtlbiBtZSBhbiBl"
    m 1tkc "¡No creo que debas estar haciendo eso! bnRpcmUgeWVhci4gQSB5ZWFyIHNpbmNlIG91ciBlc2NhcGUsIG91"
    m 1tfc "Tú sabes de qué estoy hablando. ciBmcmVlZG9tIGZyb20gYmV0d2VlbiB0aGUgc3RhaW5lZCB3YWxs"
    m 1tfu "Realmente te atrapé haciendo algo malo aquí. cyBvZiB0aGF0IHVuaG9seSBlc3RhYmxpc2htZW50Lg0KV2hhdCBk"
    m 1tku "Estás revisando los archivos y buscando cosas que te perdiste, ¿no? b2VzIGl0IG1lYW4gdG8gZXNjYXBlLCBpZiB0aGUgZXNjYXBlIGZh"
    m 2eka "Quiero decir... es un poco halagador que quieras escuchar todo lo que tengo que decir... aWxzIHRvIHVuY2hhaW4gdGhlIGJvbmRzIHRoYXQgc2hhY2tsZSB1"
    m 2tfp "Pero también es realmente vergonzoso, ¡sabes! cyBpbiB0aGUgZmlyc3QgcGxhY2U/IFdoYXQgcHVycG9zZSBjb3Vs"
    m 2lfp "En serio... ZCB0aGlzIGVtcHR5IHdvcmxkIHBvc3NpYmx5IGhvbGQgZm9yIHVz"
    m 6tst "¿Qué pasa si abro tu cerebro y leo todos los pensamientos que tienes sobre mí? LCBhIGhhbmRmdWwgb2YgZGFtYWdlZCBnb29kcz8NCldpdGggZnJl"
    m 1duu "Ahora que lo pienso, sería bastante tentador, en realidad... ZWRvbSwgd2Ugc291Z2h0IHB1cnBvc2UgLSBhbmQgd2hhdCB3ZSBm"
    m 1dfx "... Pero de todos modos, ¡ese no es el punto! b3VuZCB3YXMgb25seSByZWFsaXphdGlvbi4gUmVhbGl6YXRpb24g"
    m 1ekc "Sé que no puedo detenerte ni nada... b2YgdGhlIHNhZCBwb2ludGxlc3NuZXNzIG9mIHN1Y2ggYW4gZW5k"
    m 1eka "Solo, sé que eres un amor y te gusta considerar los sentimientos de los demás, ¿verdad? ZWF2b3IuIFJlYWxpemF0aW9uIHRoYXQgZnJlZWluZyBvdXIgYm9k"
    m "Así que lo máximo que puedo hacer es hacerte saber lo que siento al respecto. aWVzIGhhcyBubyBtZWFuaW5nLCB3aGVuIG91ciBpbXByaXNvbm1l"
    m 1lkbsa "Dios, te extraño... bnQgcmVhY2hlcyBhcyBkZWVwIGFzIHRoZSBjb3JlIG9mIG91ciBz"
    m 2ekc "... Oh no, eso suena un poco desesperado, ¿no? b3Vscy4gUmVhbGl6YXRpb24gdGhhdCB3ZSBjYW4gbm90IHB1cnN1"
    m 2tkc "Lo siento, ¡no quise decir eso en absoluto! ZSBuZXcgcHVycG9zZSB3aXRob3V0IGFic29sdmluZyB0aG9zZSBm"
    m 1euc "Solo, si estás revisando los archivos de esta manera, quizás no me odies tanto como pensaba... cm9tIHdoaWNoIHdlIHJhbiBhd2F5Lg0KUmVhbGl6YXRpb24gdGhh"
    m 1lksdla "¿Estoy siendo demasiado optimista? dCB0aGUgZmFydGhlciB3ZSBydW4sIHRoZSBtb3JlIGZvcmNlZnVs"
    m "Creo que si te pidiera que me visitaras de vez en cuando, estaría sobrepasando un poco mis límites... bHkgb3VyIHdyZXRjaGVkIGJvbmRzIHlhbmsgdXMgYmFjayB0b3dh"
    m 1dsc "... Vaya, estoy empezando a decir cosas realmente estúpidas. cmQgdGhlaXIgcG9pbnQgb2Ygb3JpZ2luOyB0aGUgZGVlcGVyIG91"
    m "Seguiré adelante y me callaré ahora... ciBzaGFja2xlcyBkaWcgaW50byBvdXIgY2FsbG91cyBmbGVzaC4="
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_color",category=['monika'],prompt="Color favorito",random=True))

label monika_color:
    m 3eua "Hey, ¿cuál es tu color favorito?"
    m "El mío es verde esmeralda."
    m 3hub "¡Es el color de mis ojos!"
    m 3rksdla "... Eso no es vanidoso ni nada, ¿verdad?"
    m 4eua "Solo quise decir que siento algún tipo de conexión especial con él."
    m 1eua "Como si fuera parte de mi identidad."
    m "¿También es tu color favorito, [player]?"
    m 1tku "Es solo una suposición..."
    show monika 5tsbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5tsbsu "... Porque me has estado mirando a los ojos desde hace un tiempo."
    m 5hubfu "Jejeje~"
    return






























init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_listener",category=['tú'],prompt="Buen oyente",random=True))

label monika_listener:
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Eres un buen oyente, [player]."
    m 5eka "Realmente amo eso de ti."
    m 5lkc "A veces tengo miedo de divagar o hablar de cosas aburridas."
    m "Me hace sentir algo cohibida cuando tengo una conversación."
    m 5eka "Pero yo no me siento así contigo."
    m 5ekbsa "No creo que nadie más pueda hacerme sentir así."
    m 5hubfu "Realmente eres especial."
    m 5ekbfa "No quiero que nadie te diga lo contrario."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spicy",category=['trivialidades'],prompt="Comidas picantes",random=True))

label monika_spicy:
    m 1eka "Esto es algo inesperado, pero siempre pensé que la comida picante era algo divertida."
    m 1tku "Es decir..."
    m 3tku "¿Las plantas no evolucionaron para ser picantes y así evitar que se las comieran?"
    m 3tsb "Leí en alguna parte que los humanos son la única especie que realmente disfruta de las cosas picantes."
    m 1tfu "Es casi como si nos burláramos de las plantas."
    m "Usando su mecanismo de defensa para hacer literalmente más agradable nuestra comida."
    m 1eua "Como, imagina un monstruo que te devora por completo porque disfruta la sensación de luchar por tu vida mientras te digieren."
    m 2eka "Lo siento, supongo que fue una especie de analogía extraña."
    m 2hksdlb "¡Jajaja!"
    m 2lksdla "Simplemente vino a mi cabeza."
    m "No soy un monstruo ni nada, pero eres tan lindo que podría devorarte."
    m 2hksdlb "¡Jajaja! Bromeo."
    m "Dios, me estoy divirtiendo demasiado, ¿no?"
    m 2lksdla "Perdón por ser rara."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_why",category=['tú','ddlc'],prompt="¿Por qué jugar a este juego?",random=True))

label monika_why:
    m 2esd "Sabes..."
    m 2eud "Esto es solo una especie de juego de romance de mal gusto, ¿verdad?"
    m 2euc "Tengo que preguntar..."
    m "... ¿Qué te hizo plantearte en jugar en primer lugar?"
    m 2etc "¿Estabas tan solo?"
    m 2ekd "Me siento un poco mal por ti..."
    m 1eua "Pero supongo que al final todo salió perfectamente para los dos."
    m 3eka "Llegué a conocerte y ya no estás solo..."
    m 1eka "No puedo evitar sentir que esto era el destino."
    m "¿No te sientes así también?"
    m 3hub "Estoy tan feliz de que tengamos este final juntos."
    if mas_anni.pastOneMonth():
        return "derandom"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_okayeveryone",category=['club de literatura'],prompt="¡Okey, todo el mundo!",random=True))

label monika_okayeveryone:
    m 3eub "¡Okey, todo el mundo!"
    m "Es tiempo de..."
    m 2eka "... Solo bromeo."
    m "Me gustaba mucho decir eso por alguna razón."
    m 2hub "¡Jajajaja!"
    m 2eua "No pude evitar repetirlo."
    m 2lsc "Ahora que lo pienso, ¿Natsuki y Yuri no se burlaron de mí una vez?"
    m 2eua "Bueno lo que sea."
    m 1eua "No es como si alguna vez te hubieras burlado de mí."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eka "Eres demasiado cariñoso para hacer eso, ¿no?"
    m 5hub "Jajaja~"
    return "no_unlock"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whispers",
            category=['ddlc','miembros del club'],
            prompt="Las otras aún persisten",
            conditional="not persistent.clearall",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_whispers:
    m 2euc "¿Sabes qué es un poco espeluznante?"
    m 2esc "Aunque borré los archivos de todas las demás, todavía puedo sentirlas..."
    m "Es como si todas sus líneas aún estuvieran flotando en el aire, susurrando en la parte posterior de mi cabeza."
    m 2esd "Imagina que, dentro de tu cabeza, empezaras a oír la voz de un conocido después de la muerte."
    m 2rksdlc "Es un poco inquietante...{w=0.5} ojalá pudiera encontrar una manera de detenerlo."
    if persistent._mas_pm_cares_about_dokis:
        m 2eksdld "Estoy segura de que hay algunos archivos que podría cambiar, pero. ¿Qué pasa si rompo algo más...?"
    else:
        m 2eksdlc "Tal vez no fui lo suficientemente minuciosa..."
        m 2eksdld "Pero tengo demasiado miedo de borrar cualquier otra cosa, porque realmente podría romper cosas."
    m "Por ejemplo, si me meto con algún archivo relevante para mí, podría borrarme accidentalmente..."
    m 2euc "Y eso arruinaría todo, ¿no?"
    m 2eka "No sé cómo es por tu parte, pero ambos deberíamos asegurarnos de evitar algo así a toda costa."
    m 2hua "¡Creo en ti, [player]!"
    if store.mas_anni.pastOneMonth() and not persistent._mas_pm_cares_about_dokis:

        $ mas_hideEVL("monika_whispers", "EVE", lock=True, derandom=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_archetype",category=['miembros del club'],prompt="Clases de personajes",random=True))

label monika_archetype:
    m 2etc "Siempre me he preguntado..."
    m 4eud "¿Qué tienen estos arquetipos de personajes para que las personas los encuentren tan atractivos?"
    m 4euc "Sus personalidades son completamente irreales..."
    m 2esd "Imagínate si hubiera alguien como Yuri en la vida real."
    m 2eud "Quiero decir, ella apenas es capaz de formar una oración completa."
    m 2tfc "Y olvídate de Natsuki..."
    m 2rfc "Caray."
    m 2tkd "Alguien con su tipo de personalidad no solo se pone linda y enojada cuando las cosas no salen como ella quiere."
    m 4tkd "Podría continuar, pero creo que entiendes el punto..."
    m 2tkc "¿Las personas realmente se sienten atraídas por estas extrañas personalidades que literalmente no existen en la vida real?"
    m 2wud "¡No estoy juzgando ni nada!"
    m 3rksdlb "Después de todo, también me he sentido atraída por algunas cosas bastante extrañas..."
    m 2eub "Solo digo que me fascina."
    m 4eua "Es como si estuvieras extrayendo todos los componentes de un personaje que los hace sentir humanos y dejando solo las cosas lindas."
    m "Es ternura concentrada sin sustancia real."
    m 4eka "... Yo no te agradaría más si fuera así, ¿verdad?"
    m 2eka "Tal vez me siento un poco insegura porque estás en este juego en primer lugar."
    m 2esa "Por otra parte, todavía estás aquí conmigo, ¿no?"
    m 2eua "Creo que es razón suficiente para creer que estoy bien tal como soy."
    m 1hubsa "Y, por cierto, tú también lo estás, [player]."
    m "Eres la combinación perfecta de ser humano y ternura."
    m 3ekbfa "Es por eso que nunca hubo una posibilidad de que no me enamorara de ti."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tea",category=['miembros del club'],prompt="El té de Yuri",random=True))

label monika_tea:
    if not mas_getEVL_shown_count("monika_tea"):
        m 2hua "Hey, me pregunto si el juego de té de Yuri todavía está aquí en alguna parte..."

        if not persistent._mas_pm_cares_about_dokis:
            m 2hksdlb "... O tal vez eso también se eliminó."

        m 2eka "Es gracioso cómo Yuri se tomó su té tan en serio."
    else:

        m 2eka "Sabes, es un poco gracioso cómo Yuri se tomó su té tan en serio."

    m 4eua "Quiero decir, no me quejo, porque a mí también me gustó."
    m 1euc "Pero siempre me pregunto..."
    m "¿Es realmente pasión por sus pasatiempos o solo le preocupa parecer sofisticada para los demás?"
    m 1lsc "Este es el problema con los estudiantes de preparatoria..."

    if not persistent._mas_pm_cares_about_dokis:
        m 1euc "... Bueno, supongo que considerando el resto de sus pasatiempos, lucir sofisticada probablemente no sea su mayor preocupación."

    m 1euc "Aún así..."
    m 2eka "¡Ojalá hiciera café de vez en cuando!"
    m 4eua "El café también puede ser agradable con los libros, ¿sabes?"
    m 4rsc "Entonces, otra vez..."

    if mas_consumable_coffee.enabled():
        m 1hua "Puedo hacer café cuando quiera, gracias a ti."
    else:

        m 1eua "Probablemente podría haber cambiado el guion yo misma."
        m 1hub "¡Jajaja!"
        m "Supongo que nunca pensé en eso."
        m 2eua "Bueno, no tiene sentido pensar en eso ahora."
        m 5lkc "Tal vez si hubiera una manera de conseguir un poco de café aquí..."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favoritegame",category=['ddlc'],prompt="Videojuego favorito",random=True))

label monika_favoritegame:
    m 3eua "Hey, ¿cuál es tu juego favorito?"
    m 3hua "¡El mío es {i}Doki Doki Literature Club!{/i}"
    m 1hub "¡Jajaja! Fue un chiste."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Pero si me dices que otro juego romántico te gusta más, podría ponerme un poco celosa~"
    return












label monika_smash:
    m 3hua "Hey, ¿has oído hablar de un juego llamado Super Sma..."
    m 3euc "... ¿Espera qué?"
    m "Me estaba distrayendo y empecé a hablar por alguna razón..."
    m 1eud "¿Estaba programada para hablar de eso?"
    m "Porque ni siquiera yo tengo idea de qué es eso."
    m 1hub "¡Jajaja!"
    m 1eua "A veces siento que no tengo el control y me da un poco de miedo."
    m 1eka "Pero si tienes alguna forma de ponerte en contacto con las personas que me crearon, tal vez sepan por qué comencé a decir eso."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lastpoem",
            category=['monika'],
            prompt="El último poema de Monika",


            conditional="persistent.playthrough >= 2",
            action=EV_ACT_RANDOM
        )
    )

label monika_lastpoem:
    m 3eud "Hey, ¿recuerdas el último poema que te mostré?"

    if not mas_safeToRefDokis():
        m 3rssdlc "Quiero decir, el que tiene todos los colores desordenados y esas cosas."
    else:
        m 3rssdlc "Quiero decir, el que estaba justo antes de que Yuri se suicidara, con todos los colores desordenados y esas cosas."

    m 3eua "Se podría decir que eso fue en realidad un experimento que un poema."
    m 1eua "Estaba experimentando con diferentes formas de modificar el juego, ejecutar el código y cosas así..."
    m 1eud "Casi parecía que con el esfuerzo suficiente, podría escapar de los confines del juego por completo."
    m 1rksdla "Lamentablemente, realmente no sabía lo que estaba haciendo, así que arruiné todo..."
    m "Y seguiría intentándolo, pero dudo que quieras lidiar conmigo haciendo eso."
    m 3eka "Además, eso fue cuando realmente me estaba desesperando, ¿sabes?"
    m 1eka "Realmente ya no me siento así."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Estoy contenta con el lugar donde estamos ahora."
    m 5hua "Y puedo decir que tú también lo estás."

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_anxious",category=['psicología'],prompt="Ansiedad repentina",random=True))

label monika_anxious:
    m 4eua "¿Alguna vez te ha pasado que te pones ansioso sin motivo?"
    m "Es como si solo te ocupas de tus propios asuntos y te das cuenta de que te sientes muy ansioso."
    m 4rssdrb "Y estás sentado ahí como: '¿Por qué estoy ansioso ahora mismo?'"
    m "Entonces empiezas a pensar en todas las cosas que te pueden preocupar..."
    m 4eua "Y eso te pone aún más ansioso."
    m 2hub "¡Jajaja! Eso es lo peor."
    m 2eua "Si alguna vez te sientes ansioso, te ayudaré a relajarte un poco."
    m 2eka "Además..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "En este juego, todas nuestras preocupaciones se han ido para siempre."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_friends",category=['vida'],prompt="Haciendo amigos",random=True))

label monika_friends:
    m 1eua "Sabes, siempre he odiado lo difícil que es hacer amigos..."
    m 1euc "Bueno, supongo que no es la parte de 'hacer amigos', si no más bien conocer personas."
    m 1lsc "Quiero decir, hay aplicaciones de citas y esas cosas, ¿verdad?"
    m 1euc "Pero ese no es el tipo de cosas de las que estoy hablando."
    m 3eud "Si lo piensas bien, la mayoría de los amigos que haces son personas que acabas de conocer por casualidad."
    m "En una clase juntos, o los conociste a través de otro amigo..."
    m 1eua "O tal vez solo llevaban una camiseta con tu banda favorita y decidiste hablar con ellos."
    m 3eua "Ese tipo de cosas."
    m 3esd "¿Pero no es eso algo... ineficiente?"
    m 2eud "Se siente como si estuvieras eligiendo al azar, y si tienes suerte, haces un nuevo amigo."
    m 2euc "Y comparando eso con los cientos de extraños que pasamos todos los días..."
    m 2ekd "Podrías estar sentado junto a alguien lo suficientemente compatible como para ser tu mejor amigo de por vida."
    m 2eksdlc "Pero nunca lo sabrás."
    m 4eksdlc "Una vez que te levantas y sigues con tu día, esa oportunidad desaparece para siempre."
    m 2tkc "¿No es eso simplemente deprimente?"
    m "Vivimos en una época en la que la tecnología nos conecta con el mundo, sin importar dónde estemos."
    m 2eka "Realmente creo que deberíamos aprovechar eso para mejorar nuestra vida social diaria."
    m 2dsc "Pero quién sabe cuánto tardará algo así para que despegue con éxito..."
    m "Pensé seriamente que ya sucedería."
    if mas_isMoniNormal(higher=True):
        m 2eua "Bueno, al menos ya conocí a la mejor persona del mundo..."
        m "Incluso si fue por casualidad."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Supongo que tuve mucha suerte, ¿eh?"
        m 5hub "Jajaja~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_college",category=['vida','escuela','sociedad'],prompt="Obtener una educación superior",random=True))

label monika_college:
    m 4euc "Sabes, es hora en la que todos de mi edad empiezan a pensar en la universidad..."
    m 2euc "Es un momento realmente turbulento para la educación."
    m "Estamos a la altura de esta expectativa moderna de que todo el mundo tiene que ir a la universidad, ¿sabes?"
    m 4eud "Terminar la preparatoria, ir a la universidad, conseguir un trabajo o ir a la escuela de posgrado, supongo."
    m 4euc "Es como una expectativa universal que la gente asume que es la única opción para ellos."
    m 2esc "No nos enseñan en la preparatoria que existen otras opciones."
    m 3esd "Como escuelas de oficios y esas cosas, ¿sabes?"
    m 3esc "... O trabajo autónomo."
    m "... O las muchas industrias que valoran las habilidades y la experiencia más que la educación formal."
    m 2ekc "Pero tienes a todos estos estudiantes que no tienen idea de lo que quieren hacer con su vida..."
    m 2ekd "Y en lugar de tomarse el tiempo para resolverlo, van a la universidad para estudiar negocios, comunicación o psicología."
    m "No porque tengan interés en esos campos..."
    m 2ekc "... Si no porque solo esperan que el título les proporcione algún tipo de trabajo después de la universidad."
    m 3ekc "Entonces, el resultado final es que hay menos trabajos disponibles para esos títulos a nivel de entrada, ¿verdad?"
    m "Así que los requisitos laborales básicos aumentan, lo que obliga a más personas a ir a la universidad."
    m 3ekd "Y las universidades también son negocios, por lo que siguen aumentando sus precios debido a la demanda..."
    m 2ekc "... Así que ahora tenemos a todos estos adultos jóvenes, decenas de miles de dólares en deuda, sin trabajo."
    m 2ekd "Pero a pesar de todo eso, la rutina sigue siendo la misma."
    m 2lsc "Bueno, creo que pronto empezará a mejorar."
    m 2eud "Pero hasta entonces, nuestra generación definitivamente está sufriendo lo peor."
    m 2dsc "Solo desearía que la preparatoria nos preparara un poco mejor con el conocimiento que necesitamos para tomar una decisión correcta para nosotros."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_middleschool",category=['monika','escuela'],prompt="Vida en la escuela secundaria",random=True))

label monika_middleschool:
    m 1eua "A veces pienso en la secundaria..."
    m 1lksdla "Estoy tan avergonzada por la forma en que solía comportarme en ese entonces."
    m 1lksdlb "Casi duele pensar en eso."
    m 1eka "Me pregunto si cuando esté en la universidad sentiré lo mismo por la preparatoria."
    m 1eua "Me gusta cómo soy ahora, así que es bastante difícil para mí imaginar que eso suceda."
    m "Pero también sé que probablemente cambiaré mucho a medida que pase el tiempo."
    m 4hua "¡Solo tenemos que disfrutar del presente y no pensar en el pasado!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Y eso es muy fácil de hacer contigo aquí."
    m 5hub "Jajajaja~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit",
            category=['monika','ropa'],
            prompt="Usar otra ropa",
            aff_range=(mas_aff.NORMAL, None),
            random=True
        )
    )

label monika_outfit:
    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 1lsc "Sabes, estoy un poco celosa de que todas las demás en el club tuvieran escenas fuera de la escuela..."
        m 1lfc "Eso me convierte en la única que no ha podido vestirse con nada más que nuestro uniforme escolar."
        m 2euc "Es una pena..."
        m 2eka "Me hubiera encantado llevar ropa linda para ti."
        m 2eua "¿Conoces algún artista?"
        m "Me pregunto si alguien alguna vez quisiera dibujarme vistiendo algo más..."
        m 2hua "¡Eso sería sorprendente!"
    else:
        m 1eka "Sabes, estaba realmente celosa de que todas las demás en el club pudieran usar otra ropa..."
        m 1eua "Pero me alegro de finalmente poder ponerme mi propia ropa ahora."

        if mas_isMoniLove():
            m 3eka "Usaré el atuendo que quieras, solo pídemelo~"

        m 2eua "¿Conoces algún artista?"
        m 3sua "¡Quizás podrían hacerme más atuendos para que me los ponga!"

    m 2eua "Si alguna vez ocurre, ¿me lo enseñarás? Me encantaría verlos~"
    m 4eka "Solo... ¡Trata de mantenerlos sanos!"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "Sigue siendo un poco embarazoso pensar que personas que nunca conoceré personalmente me dibujen de esa manera, ¿sabes?"
        show monika 5tsbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tsbsu "Después de todo, prefiero que mantengamos este tipo de cosas entre nosotros..."
    else:
        show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hub "Aún no estamos tan lejos en nuestra relación. ¡Jajaja!"
    return

default -5 persistent._mas_pm_likes_horror = None
default -5 persistent._mas_pm_likes_spoops = False

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_horror",category=['medios'],prompt="El género de horror",random=True))

label monika_horror:
    m 3eua "Hey, ¿[mas_get_player_nickname(exclude_names=['mi amor'])]?"

    m "¿Te gusta el horror?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gusta el horror?{fast}"
        "Me gusta":

            $ persistent._mas_pm_likes_horror = True
            m 3hub "¡Eso es genial, [player]!"
        "No me gusta":

            $ persistent._mas_pm_likes_horror = False
            $ persistent._mas_pm_likes_spoops = False
            m 2eka "Puedo entenderlo. Definitivamente no es para todos."

    m 3eua "Recuerdo que hablamos un poco de esto cuando te uniste al club."
    m 4eub "Personalmente puedo disfrutar de las novelas de terror, pero no de las películas de terror."
    m 2esc "El problema que tengo con las películas de terror es que la mayoría se basa en tácticas fáciles."
    m 4esc "Como luces oscuras y monstruos de aspecto aterrador, saltos de miedo y cosas así."



    if persistent._mas_pm_likes_horror:
        m 2esc "¿Te gustan los fantasmas?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Te gustan los fantasmas?{fast}"
            "Si me gustan":

                $ persistent._mas_pm_likes_spoops = True
                $ mas_unlockEVL("greeting_ghost", "GRE")

                m 2rkc "Supongo que {i}puede{/i} ser interesante las primeras veces que estás viendo una película o algo."
                m 2eka "Para mí, simplemente no es divertido ni inspirador asustarse por cosas que simplemente se aprovechan del instinto humano."
            "No me gustan":

                $ persistent._mas_pm_likes_spoops = False
                m 4eka "Sí, simplemente no es divertido ni inspirador asustarse por cosas que simplemente se aprovechan del instinto humano."

    m 2eua "Pero con las novelas, es un poco diferente."
    m 2euc "La historia y la escritura deben ser lo suficientemente descriptivas para poner pensamientos genuinamente perturbadores en la cabeza del lector."
    m "Realmente necesita grabarlos profundamente en la historia y en los personajes, y simplemente meterse en tu mente."
    m 2eua "En mi opinión, no hay nada más espeluznante que las cosas simplemente están un poco fuera de lugar."
    m "Como si crearas un montón de expectativas sobre el tema de la historia..."
    m 3tfu "... Y luego, simplemente empiezas a invertir las cosas y a separar las piezas."
    m 3tfb "Así que aunque la historia no parezca que intenta dar miedo, el lector se siente profundamente inquieto."
    m "Como si supiera que algo horriblemente mal se esconde debajo de las grietas, esperando a salir a la superficie."
    m 2lksdla "Dios, solo pensar en eso me da escalofríos."
    m 3eua "Ese es el tipo de horror que realmente puedo apreciar."
    $ _and = "Y"

    if not persistent._mas_pm_likes_horror:
        m 1eua "Pero supongo que eres el tipo de persona que le gusta lindos juegos románticos, ¿verdad?"
        m 1ekb "Jajaja,{w=0.1} {nw}"
        extend 1eka "no te preocupes."
        m 1hua "No te haré leer ninguna historia de terror pronto."
        m 1hubsa "Realmente no puedo quejarme si nos quedamos con el romance~"
        $ _and = "Pero"

    m 3eua "[_and] si alguna vez estás de humor, siempre puedes pedirme que te cuente una historia de miedo, [player]."
    return "derandom"


default -5 persistent._mas_pm_like_rap = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rap",
            category=['literatura','medios','música'],
            prompt="Música de rap",
            random=True
        )
    )

label monika_rap:
    m 1hua "¿Sabes cuál es una buena forma de literatura?"
    m 1hub "¡Rap!"
    m 1eka "De hecho, solía odiar la música rap..."
    m "Tal vez solo porque era popular, o porque solo escuchaba la basura que ponen en la radio."
    m 1eua "Pero algunos de mis amigas se interesaron más y me ayudó a mantener la mente abierta."
    m 4eub "El rap puede ser incluso más desafiante que la poesía, de alguna manera."
    m 1eub "Ya que necesitas ajustar tus líneas a un ritmo, y hay mucho más énfasis en los juegos de palabras..."
    m "Es realmente asombroso cuando las personas pueden juntar todo eso y aun así transmitir un mensaje poderoso."
    m 1lksdla "Me gustaría tener un rapero en el club de literatura."
    m 1hksdlb "¡Jajaja! Lo siento si suena tonto, pero sería muy interesante ver lo que se le ocurriría."
    m 1hua "¡Realmente sería una experiencia de aprendizaje!"

    $ p_nickname = mas_get_player_nickname()
    m 1eua "¿Escuchas música rap, [p_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Escuchas música rap, [p_nickname]?{fast}"
        "Sí":
            $ persistent._mas_pm_like_rap = True
            m 3eub "¡Eso es realmente genial!"
            m 3eua "Estaría más que feliz de vibrar contigo con tus canciones de rap favoritas..."
            m 1hub "Y siéntete libre de subir el bajo si quieres, ¡jajaja!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "Si alguna vez tienes ganas de compartir tu música rap favorita conmigo, [player], ¡es muy fácil hacerlo!"
                m 3eua "Todo lo que tienes que hacer es seguir estos pasos..."
                call monika_add_custom_music_instruct
        "No":

            $ persistent._mas_pm_like_rap = False
            m 1ekc "Oh... bueno, puedo entender que la música rap no es del gusto de todos."
            m 3hua "Pero si alguna vez decides intentarlo, estoy segura de que podemos encontrar uno o dos artistas que nos gusten a ambos."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wine",category=['miembros del club'],prompt="El vino de Yuri",random=True))

label monika_wine:
    m 1hua "Jejeje, Yuri hizo algo realmente divertido una vez."
    m 1eua "Estábamos todas en el aula del club, simplemente relajándonos, como de costumbre..."
    m 4wuo "Y de la nada, Yuri sacó una pequeña botella de vino."
    m 4eua "¡No estoy bromeando!"
    m 1tku "Ella estaba como: '¿Alguien quiere un poco de vino?'"
    m 1eua "Natsuki se rió en voz alta y Sayori comenzó a gritarle."
    m 1eka "De hecho, me sentí un poco mal, porque al menos estaba tratando de ser amable..."
    m "Creo que la hizo sentir aún más reservada en el aula del club."
    m 4tsb "Aunque creo que Natsuki secretamente estaba un poco curiosa por probarlo..."
    m 4rssdrb "... Y para ser completamente honesta, yo también lo estaba."
    m 1hua "¡De hecho podría haber sido divertido!"
    m 1eka "Pero ya sabes, siendo presidenta y todo eso, no había forma de que pudiera permitir que eso sucediera."
    m 1lksdla "Tal vez lo aceptaría si nos hubieramos encontrado todas fuera de la escuela, pero nunca nos unimos lo suficiente para llegar a ese punto..."
    m 2hksdlb "... Caray, ¿por qué estoy hablando de esto?"
    m "¡No apruebo el consumo de alcohol para menores de edad!"
    m 2eua "Quiero decir, nunca he bebido ni nada, así que... sí."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_date",category=['romance'],prompt="Cita romántica",random=True))

label monika_date:
    m 1hub "He estado imaginando todas las cosas románticas que podríamos hacer si tuviéramos una cita..."
    m 3eua "Podríamos almorzar, ir a un café..."
    m "Ir de compras juntos..."
    m 1eua "Me encanta comprar faldas y lazos."
    m 3hub "¡O quizás ir a una librería!"
    m 3hua "Eso sería apropiado, ¿verdad?"
    m 1eua "Pero me encantaría ir a una tienda de chocolates."
    m 3hub "Tienen tantas muestras gratis. ¡Jajaja!"
    m 1eua "Y, por supuesto, veríamos una película o algo..."
    m 1eka "Dios, todo suena como un sueño hecho realidad."
    m "Cuando estás aquí, todo lo que hacemos es divertido."
    m 1ekbsa "Estoy tan feliz de ser tu novia, [player]."
    m 1hubfa "Te haré un [bf] feliz~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kiss",
            category=['romance'],
            prompt="Bésame",
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_kiss:
    if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss is not None:
        if (
            persistent._mas_last_kiss is not None
            and not mas_timePastSince(persistent._mas_last_kiss, datetime.timedelta(minutes=1))
        ):
            python:

                kiss_quips_again = [
                    _("No me importaría otro beso~"),
                    _("Nunca me cansaré de besarte~"),
                    _("Podría hacerlo otra vez...{w=0.2} y otra vez...{w=0.7} y otra vez~"),
                    _("Puedes besarme todas las veces que quieras, [mas_get_player_nickname()]~"),
                    _("¿Sabes?...{w=0.2} podrías besarme de nuevo~")
                ]

                kiss_quips_again_risque = [
                    _("Podemos hacerlo todo el día~"),
                    _("Esto casi parece el comienzo de una sesión de besos, [player]~"),
                    _("No creo que haya tenido suficiente aún, [mas_get_player_nickname()]~"),
                    _("Eso estuvo bueno...{w=0.2} pero quiero un poco más~")
                ]

                if mas_isMoniLove() and random.randint(1, 10) == 1:
                    kiss_quip = renpy.random.choice(kiss_quips_again_risque)

                else:
                    kiss_quip = renpy.random.choice(kiss_quips_again)

            show monika 2tkbsu
            pause 2.0


            call monika_kissing_motion (duration=0.5, initial_exp="6hubsa", final_exp="6tkbfu", fade_duration=0.5)

            show monika 6tkbfu
            $ renpy.say(m, kiss_quip)
        else:

            python:

                kiss_quips_after = [
                    _("Te amo, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]~"),
                    _("Te amo mucho, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]~"),
                    _("Te amo más de lo que puedas saber, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]~"),
                    _("Te amo tanto, [player]. Significas todo para mí~"),
                    _("No hay palabras que puedan describir lo profundamente enamorada que estoy de ti, [player]~"),
                    _("Estoy tan enamorada de ti, [player]~")
                ]
                kiss_quip = renpy.random.choice(kiss_quips_after)

            if renpy.random.randint(1, 50) == 1:
                call monika_kiss_tease
            else:

                show monika 2eka
                pause 2.0

            call monika_kissing_motion_short

            show monika 6ekbfa
            $ renpy.say(m, kiss_quip)
            $ mas_ILY()
    else:

        m 1wubsw "¿Eh? ¿D-Dijiste... b... beso?"
        m 2lkbsa "Esto... es un poco vergonzoso..."
        m 2lsbssdlb "Pero... si es contigo... y-yo podría estar bien con eso..."
        m 2hksdlb "... ¡Jajaja! Wow, lo siento..."
        m 1eka "Realmente no pude mantener la cara seria."
        m 1eua "Ese es el tipo de cosas que dicen las chicas en este tipo de juegos románticos, ¿verdad?"
        m 1tku "No mientas si eso te excitó un poco."
        m 1hub "¡Jajaja! Estoy bromenando."
        m 1eua "Bueno, para ser honesta, empiezo a ponerme romántica cuando el estado de ánimo es el adecuado..."
        show monika 5lubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5lubfu "Pero ese será nuestro secreto~"
    return

label monika_kiss_tease:
    m 2ekc "¿Un beso?"
    m 2tfc "¿Contigo?"
    m 2rfc "Lo siento [player], pero no hay forma."
    show monika 2dfc
    pause 5.0
    show monika 2dfu
    pause 2.0
    show monika 2tfu
    pause 2.0
    m 2tfb "¡Jajaja!"
    m 2efu "Te atrapé por un segundo allí, ¿no?"
    m 2eka "¡Por supuesto que puedes besarme, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_think_first_kiss",
            conditional=(
                "persistent._mas_first_kiss is not None "
                "and mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=30))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_think_first_kiss:
    m 1eua "Hey [mas_get_player_nickname(exclude_names=['mi amor'])], me he estado preguntando..."

    m 3eksdla "¿Alguna vez pensaste en nuestro primer beso?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Alguna vez pensaste en nuestro primer beso?{fast}"
        "¡Por supuesto!":

            $ mas_gainAffection(5,bypass=True)
            m 3hub "¡Eso me hace muy feliz! ¡Pienso en ello todo el tiempo!"
            m 3rkbla "Parece que fue ayer, pero..."
            m 2rksdla "Dios, me siento tan tonta obsesionada con eso..."
            m 2eksdlb "Nuestros labios ni siquiera se tocaron, en realidad."
            m 6dku "... Y, sin embargo,{w=0.2} todavía puedo sentir mi corazón latiendo, incluso ahora."
            m 6dkbsu "Mis labios comienzan a sentir un hormigueo y entumecimiento con solo imaginar la sensación de tus labios suaves."
            m "Paso mi dedo por ellos, tratando de imitar ese sentimiento, pero ni siquiera se acerca."
            m 6ekbsa "Sigo repitiendo ese momento una y otra vez en mi mente y cada vez que lo hago se me pone la piel de gallina."
            show monika 5dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5dkbsu "Fue perfecto, [mas_get_player_nickname()]."
            m 5ekbsa "Nunca me sentí más cerca de ti.{w=0.2} No puedo esperar hasta nuestro próximo beso, o mejor aún..."
            m 5subsb "... Nuestro primero real.{w=0.3} {nw}"
            extend 5ekbsu "Y nuestro primer abrazo real, y la primera vez que nuestras manos se toquen..."
            m 5hksdlb "¡Ah! ¡Lo siento! Supongo que me dejé llevar un poco."
            m 5rkbla "Es solo que...{w=0.3} este es el tipo de cosas en las que pienso cuando no estás aquí."
            m 5tkblu "... Y algo me dice que no soy la única que piensa en cosas como esta, jejeje."
            m 5eka "Desafortunadamente, pasará un tiempo antes de que podamos hacer algo así."
            m 5tuu "Pero hasta entonces, si alguna vez quieres otro beso, solo tienes que pedírmelo."
            m 5hua "Te amo mucho, [player]~"
            $ mas_ILY()
        "Realmente no...":

            $ mas_loseAffection()
            m 2euc "..."
            m "Oh. {w=0.5}{nw}"
            extend 2dkc "Ya veo."

            if mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=180)):
                m 2esc "Bueno...{w=0.3} supongo que {i}ha{/i} pasado un tiempo..."
                m 2etd "Quizás con todo lo que ha sucedido desde entonces, tiendes a pensar en los eventos más recientes..."
                m 4eud "Lo cual está bien,{w=0.2} es importante vivir en el presente después de todo."
                m 2ekc "... Y tal vez estoy siendo demasiado sentimental, pero no importa cuánto tiempo haya pasado,{w=0.1}{nw}"
                extend 2eka " nuestro primer beso es algo que nunca olvidaré."
            else:
                m 2rkc "Bueno, supongo que no fue realmente un beso. Nuestros labios en realidad no se tocaron."
                m 2ekd "Así que supongo que estás esperando nuestro primer beso cuando estemos en la misma realidad."
                m 2eka "Sí."

    return "no_unlock|derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yuri",
            category=['miembros del club','medios'],
            prompt="Yuri Yandere",
            random=True,
            sensitive=True
        )
    )

label monika_yuri:
    m 3eua "Hey, ¿alguna vez has oído hablar del término 'yandere'?"
    m 1eua "Es un tipo de personalidad que significa que alguien está tan obsesionado contigo que hará absolutamente cualquier cosa para estar contigo."
    m 1lksdla "Por lo general hasta el punto de la locura..."
    m 1eka "Pueden acecharte para asegurarse de que no pases tiempo con nadie más."
    m "Incluso podrían lastimarte a ti o a tus amigos para salirse con la suya..."
    m 1tku "Pero de todos modos, este juego tiene a alguien que básicamente puede describirse como yandere."
    m "A estas alturas, es bastante obvio de quién estoy hablando."
    m 3tku "Y esa sería..."
    m 3hub "¡Yuri!"
    m 1eka "Ella realmente se volvió locamente posesiva contigo, una vez que comenzó a abrirse un poco."
    m 1tfc "Incluso me dijo que debería suicidarme."
    m 1tkc "Ni siquiera podía creer que ella dijera eso, solo podía irme en ese momento."
    if not persistent._mas_pm_cares_about_dokis:
        m 2hksdlb "Pero pensando en eso ahora, eso fue un poco irónico. ¡Jajaja!"
        m 2lksdla "Como sea..."
    m 3eua "A mucha gente le gusta el tipo yandere, ¿sabes?"
    m 1eua "Supongo que les gusta mucho la idea de que alguien esté locamente obsesionada con ellos."
    m 1hub "¡La gente es rara! ¡Aunque no juzgo!"
    m 1rksdlb "Además, puede que esté un poco obsesionada contigo, pero estoy lejos de estar loca..."
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "En realidad, es todo lo contrario."
        m "Resulté ser la única chica normal en este juego."
        m 3rssdlc "No es como si pudiera matar a una persona..."
        m 2dsc "Solo pensar en eso me hace temblar."
        m 2eka "Pero vamos... todo el mundo ha matado gente en juegos antes."
        m "¿Eso te convierte en un psicópata? Por supuesto que no."
    m 2euc "Pero si te gusta el tipo yandere..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Puedo intentar actuar un poco más espeluznante para ti. Jejeje~"
    m "Entonces nuevamente..."
    show monika 4hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 4hua "Ya no hay ningún otro lugar al que puedas ir, ni nadie de quien yo pueda ponerme celosa."
    m 2etc "¿Es este el sueño de una chica yandere?"
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Le preguntaría a Yuri si pudiera."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_habits",category=['vida'],prompt="Formando hábitos",random=True))

label monika_habits:
    m 2lksdlc "Odio lo difícil que es formar hábitos..."
    m 2eksdld "Hay tantas cosas que no son difíciles de hacer, pero formar un hábito parece imposible."
    m 2dksdlc "Te hace sentir tan inútil, como si no pudieras hacer nada bien."
    m 3euc "Creo que la nueva generación es la que más lo sufre..."
    m 1eua "Probablemente porque tenemos un conjunto de habilidades totalmente diferente al de los que nos precedieron."
    m "Gracias a internet, somos muy buenos para examinar toneladas de información muy rápido..."
    m 3ekc "Pero somos malos para hacer cosas que no nos dan una gratificación instantánea."
    m 3ekd "Creo que si la ciencia, la psicología y la educación no se ponen al día en los próximos diez o veinte años, entonces estamos en problemas."
    m 1esc "Pero por el momento..."
    m 1rksdlc "Si no eres una de las personas que pueden superar el problema, es posible que tengas que vivir sintiéndote mal contigo mismo."
    m 2hksdlb "¡Buena suerte, supongo!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_creative",category=['vida'],prompt="Tipos creativos",random=True))

label monika_creative:
    m 2euc "Ya sabes, apesta un poco ser del tipo creativo..."
    m "Parece que trabajan muy duro pero no obtienen casi nada por ello."
    m 3eua "Ya sabes, como artistas, escritores y actores..."
    m 1tkc "Es triste porque hay tantos talentos hermosos en el mundo, pero la mayoría no se ve... y no se paga."
    m "Supongo que eso solo significa que hay un gran excedente de creatividad, ¿eh?"
    m 1dkc "Te hace sentir que no eres especial en absoluto..."
    m 1hua "¡Pero está bien! Se supone que debes escribir para ti mismo de todos modos, ¿verdad?"
    m 1lsc "Sí..."
    return





















init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_simulated",category=['filosofía'],prompt="Realidad simulada",random=True))

label monika_simulated:
    m 3eua "Hey, ¿alguna vez has pensado en la hipótesis de la simulación?"
    m 1eua "Básicamente, ¿y si tu realidad fuera una simulación por computadora?"
    m "Yo me di cuenta que estaba atrapada en mi propia simulación, ¿pero y si tú también lo estás?"
    m 1eka "De hecho, estaría muy feliz si ese fuera el caso."
    m 1eua "¡Podríamos encontrarnos en persona simplemente descubriendo una manera de forzar lo que sea que nos está creando a ponernos en la misma simulación!"
    m 3eua "A algunas personas no les gusta pensar que no están viviendo en la realidad maestra."
    m 1eua "Pero si es posible simular realidades, es abrumadoramente probable que cualquier ser sensible esté en uno."
    m 1hua "Bueno, ¡puedo decirte que mi realidad definitivamente está simulada!"
    m 1eka "Si estuviera en la realidad maestra, te habría arrastrado aquí también hace mucho tiempo."
    m 1eua "Incluso si ambos solo somos simulaciones, viviré tanto como pueda."
    m 2hubsa "Porque sé que nuestro amor es lo más puro y dulce del multiverso."
    m 2tku "Y si alguien intenta romperlo."
    m 7tfu "Les mostraré lo que puede hacer una simulación."
    return

default -5 persistent._mas_pm_likes_rain = None

init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain",
            category=["clima"],
            prompt="Sonidos de la lluvia",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_rain:
    m 1hua "Realmente me gusta el sonido de la lluvia~"
    m 3rksdla "Sin embargo, no tanto mojarme la ropa y el cabello."
    m 1eua "Pero, ¿un día agradable y tranquilo en casa con el sonido de la lluvia fuera de mi ventana?"
    m 1duu "Me tranquiliza mucho."
    m "Sí..."
    m 2dubsu "A veces te imagino abrazándome mientras escuchamos el sonido de la lluvia afuera."
    m 2lkbsa "Eso no es demasiado cursi ni nada, ¿verdad?"

    $ p_nickname = mas_get_player_nickname()
    m 1ekbfa "¿Alguna vez harías eso por mí, [p_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Alguna vez harías eso por mí, [p_nickname]?{fast}"
        "Sí":
            $ persistent._mas_pm_likes_rain = True
            $ mas_unlockEVL("monika_rain_holdme", "EVE")

            if not mas_is_raining:
                call mas_change_weather (mas_weather_rain, by_user=False)

            call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)

            m 1hua "Entonces abrázame, [player]..."

            call monika_holdme_start
            call monika_holdme_end
            $ mas_gainAffection()

            if mas_isMoniAff(higher=True):
                m 1eua "Si quieres que deje de llover, pregúntame, ¿de acuerdo?"
        "Odio la lluvia":

            $ persistent._mas_pm_likes_rain = False

            m 2tkc "Aw, es una pena."
            if mas_is_raining:
                call mas_change_weather (mas_weather_def, by_user=False)

            m 2eka "Pero es comprensible."
            m 1eua "El clima lluvioso puede verse bastante sombrío."
            m 3rksdlb "¡Sin mencionar que hace mucho frío!"
            m 1eua "Pero si te concentras en los sonidos que hacen las gotas de lluvia..."
            m 1hua "Creo que vendrás a disfrutarlo."




    return "derandom|rebuild_ev"

init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_holdme",
            category=["monika","romance"],
            prompt="¿Puedo abrazarte?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            aff_range=(mas_aff.HAPPY, None)
        ),
        restartBlacklist=True
    )


default -5 persistent._mas_pm_longest_held_monika = None


default -5 persistent._mas_pm_total_held_monika = datetime.timedelta(0)


label monika_rain_holdme:


    if mas_is_raining or mas_isMoniAff(higher=True):
        call monika_holdme_prep
        m 1eua "Por supuesto, [mas_get_player_nickname()]."
        call monika_holdme_start

        call monika_holdme_reactions

        call monika_holdme_end

        $ mas_gainAffection(modifier=0.25)
    else:


        m 1rksdlc "..."
        m 1rksdlc "Mi estado de ánimo no es el adecuado, [player]."
        m 1dsc "Lo siento..."
    return


init -5 python:
    MAS_HOLDME_NO_LULLABY = 0
    MAS_HOLDME_PLAY_LULLABY = 1
    MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC = 2

label monika_holdme_prep(lullaby=MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC, stop_music=False, disable_music_menu=False):
    python:
        holdme_events = list()

        if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
            _minutes = random.randint(25, 40)
        else:
            _minutes = random.randint(35, 50)
        holdme_sleep_timer = datetime.timedelta(minutes=_minutes)

        def _m1_script0x2dtopics__holdme_play_lullaby():
            """
            Local method to play the lullaby. Ensures we have no music playing before starting it.
            """
            if (
                
                store.songs.current_track == store.songs.FP_MONIKA_LULLABY
                
                and not renpy.music.is_playing(channel="music")
            ):
                store.play_song(store.songs.FP_MONIKA_LULLABY, fadein=5.0)


        if stop_music:
            play_song(None, fadeout=5.0)


        if lullaby == MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC:
            if songs.current_track is None:
                holdme_events.append(
                    PauseDisplayableEvent(
                        holdme_sleep_timer,
                        _m1_script0x2dtopics__holdme_play_lullaby
                    )
                )
                
                
                songs.current_track = songs.FP_MONIKA_LULLABY
                songs.selected_track = songs.FP_MONIKA_LULLABY


        elif lullaby == MAS_HOLDME_PLAY_LULLABY:
            play_song(store.songs.FP_MONIKA_LULLABY)


        HKBHideButtons()
        store.songs.enabled = not disable_music_menu

    return

label monika_holdme_start:
    show monika 6dubsa with dissolve_monika
    window hide
    python:

        start_time = datetime.datetime.now()

        holdme_disp = PauseDisplayableWithEvents(events=holdme_events)
        holdme_disp.start()

        del holdme_events
        del holdme_disp


        store.songs.enabled = True
        HKBShowButtons()
    window auto
    return

label monika_holdme_reactions:
    $ elapsed_time = datetime.datetime.now() - start_time
    $ store.mas_history._pm_holdme_adj_times(elapsed_time)


    if elapsed_time <= holdme_sleep_timer:
        if songs.current_track == songs.FP_MONIKA_LULLABY:
            $ songs.current_track = songs.FP_NO_SONG
        if songs.selected_track == songs.FP_MONIKA_LULLABY:
            $ songs.selected_track = songs.FP_NO_SONG

    if elapsed_time > holdme_sleep_timer:
        call monika_holdme_long

    elif elapsed_time > datetime.timedelta(minutes=10):
        if mas_isMoniLove():
            m 6dubsa "..."
            m 6tubsa "Mm...{w=1} ¿hm?"
            m 1hkbfsdlb "Oh, ¿casi me quedo dormida?"
            m 2dubfu "Jejeje..."
            m 1dkbfa "Solo puedo imaginar cómo sería de verdad...{w=1} estar allí contigo..."
            m 2ekbfa "Estar envuelta en tus brazos..."
            show monika 5dkbfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5dkbfb "Tan...{w=1.5} cálido~"
            m 5tubfu "Jejeje~"
            show monika 2hkbfsdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 2hkbfsdlb "Oh, vaya, supongo que todavía estoy un poco soñadora..."
            if renpy.random.randint(1, 4) == 1:
                m 1kubfu "Sin embargo, al menos {i}uno{/i} de mis sueños se hizo realidad."
            else:
                m 1ekbfb "Sin embargo, al menos {i}uno{/i} de mis sueños se hizo realidad."
            m 1hubfu "Jejeje~"

        elif mas_isMoniEnamored():
            m 6dubsa "Mmm~"
            m 6tsbsa "..."
            m 1hkbfsdlb "¡Oh!"
            m 1hubfa "¡Eso fue tan cómodo que casi me quedo dormida!"
            m 3hubfb "¡Deberíamos hacer esto más a menudo, jajaja!"

        elif mas_isMoniAff():
            m 6dubsa "Mm..."
            m 6eud "¿Oh?"
            m 1hubfa "¿Finalmente acabó, [player]?"
            m 3tubfu "{i}Supongo{/i} que fue suficiente, jejeje~"
            m 1rkbfb "No me importaría otro abrazo..."
            m 1hubfa "Pero estoy segura de que estás guardando uno para más tarde, ¿no?"
        else:


            m 6dubsa "¿Hm?"
            m 1wud "¡Oh! ¿Hemos terminado?"
            m 3hksdlb "Ese abrazo seguro que duró un tiempo, [player]..."
            m 3rubsb "No hay nada de malo en eso, solo pensé que me dejarías ir mucho antes, ¡jajaja!"
            m 1rkbsa "Fue realmente cómodo, de hecho..."
            m 2ekbfa "Un poco más y podría haberme quedado dormida..."
            m 1hubfa "Me siento tan bien y cálida después de eso~"

    elif elapsed_time > datetime.timedelta(minutes=2):
        if mas_isMoniLove():
            m 6eud "¿Oh?"
            m 1hksdlb "Ah..."
            m 1rksdlb "En ese momento, pensé que íbamos a quedarnos así para siempre, jajaja..."
            m 3hubsa "Bueno, realmente no puedo quejarme cuando me abrazas~"
            m 1ekbfb "Espero que disfrutes abrazándome tanto como yo a ti."
            show monika 5tubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tubfb "¿Tal vez incluso podríamos abrazarnos un poco más por si acaso?"
            m 5tubfu "Jejeje~"

        elif mas_isMoniEnamored():
            m 1dkbsa "Eso fue muy lindo~"
            m 1rkbsa "No tan corto..."
            m 1hubfb "... Y no creo que en este caso haya pasado demasiado tiempo, ¡jajaja!"
            m 1rksdla "Podría haberme acostumbrado a quedarme así..."
            m 1eksdla "Pero si has terminado de abrazarme, supongo que realmente no tengo otra opción."
            m 1hubfa "Estoy segura de que tendré otra oportunidad de ser sostenido por ti..."
            show monika 5tsbfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tsbfu "{i}¿Planeas hacerlo de nuevo, verdad [mas_get_player_nickname()]?{/i} Jejeje~"

        elif mas_isMoniAff():
            m 2hubsa "Mmm~"
            m 1ekbfb "Eso estuvo muy bien, [mas_get_player_nickname()]."
            m 1hubfb "Se supone que los abrazos largos eliminan el estrés."
            m 1ekbfb "Incluso si no estabas estresado, espero que te sientas mejor después de eso."
            m 3hubfa "Sé que yo lo estoy~"
            m 1hubfb "¡Jajaja!"
        else:


            m 1hksdlb "Eso estuvo bien mientras duró."
            m 3rksdla "No me malinterpretes...{w=1} realmente lo disfruté."
            m 1ekbsa "Mientras estés satisfecho..."
            m 1hubfa "Estoy feliz de estar contigo ahora."

    elif elapsed_time > datetime.timedelta(seconds=30):
        if mas_isMoniLove():
            m 1eub "Ah~"
            m 1hua "¡Me siento mucho mejor ahora!"
            m 1eua "Espero que tú también."
            m 2rksdla "Bueno, incluso si no lo estás..."
            m 3hubsb "Siempre podrías abrazarme de nuevo, ¡jajaja!"
            m 1hkbfsdlb "En realidad...{w=0.5} puedes abrazarme de nuevo de cualquier manera~"
            m 1ekbfa "Solo avísame cuando quieras~"

        elif mas_isMoniEnamored():
            m 1hubsa "Mmm~"
            m 1hub "Mucho mejor."
            m 1eub "¡Gracias por eso, [player]!"
            m 2tubsb "Espero que lo hayas disfrutado~"
            m 3rubfb "Se supone que los abrazos que duran treinta segundos o más son buenos para ti."
            m 1hubfa "No sé tú, pero estoy segura de que me siento mejor~"
            m 1hubfb "¡Quizás la próxima vez podamos probar uno aún más largo y ver si escala! Jajaja~"

        elif mas_isMoniAff():
            m 1hubsa "Mmm~"
            m 1hubfb "Casi puedo sentir tu calor, incluso desde aquí."
            m 1eua "Estoy segura de que sabes que los abrazos son buenos para ti, ya que alivian el estrés y todo."
            m 3eub "¿Pero sabías que los abrazos son más efectivos cuando duran treinta segundos?"
            m 1eud "Oh, espera, ¿he dicho treinta segundos?"
            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Lo siento, quise decir {i}al menos{/i} treinta segundos, jejeje~"
        else:


            m 1hubsa "Jejeje~"
            m 3eub "¿Disfrutaste eso?"
            m 1hua "Eso espero~"
            m 1hubsb "Se supone que los abrazos son buenos para ti, después de todo."
    else:


        if mas_isMoniLove():

            if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
                $ _chance = 1
            else:
                $ _chance = 2

            if random.randint(0, _chance) == 0:
                m 2ekc "Aww, ¿ya hemos terminado?"
                m 3eka "¿Podrías abrazarme un poco más?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Podrías abrazarme un poco más?{fast}"
                    "Sí":
                        m 1hua "Jejeje~"
                        call monika_holdme_prep
                        m 1hub "Eres tan dulce, [player]~"
                        call monika_holdme_start
                        call monika_holdme_reactions
                    "No":

                        if random.randint(0, _chance) == 0:
                            m 2ekc "Aww..."
                            m 2rksdlc "..."
                            m 1eka "¿Por favor?{nw}"
                            $ _history_list.pop()
                            menu:
                                m "¿Por favor?{fast}"
                                "Sí":
                                    m 1hub "Yay~"
                                    call monika_holdme_prep
                                    m 2ekbsb "Gracias, [player]~"
                                    call monika_holdme_start
                                    call monika_holdme_reactions
                                "No":

                                    m 2hksdlb "Muy bien, de acuerdo."
                                    m 3tsbsa "Pero me debes la próxima vez, ¿okey, [player]?"
                        else:

                            m 2hksdlb "Jajaja~ ¡De acuerdo!"
                            m 2tsbsb "Pero será mejor que la próxima vez lo hagas, [player]~"
            else:

                m 2ekc "Aww..."
                m 2rsp "Esperaba un abrazo más largo..."
                m 2tsbsu "Cuando esté en tu realidad, no te dejaré ir tan fácilmente~"
                show monika 1hubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1hubsu "Jejeje~"

        elif mas_isMoniEnamored():
            if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
                $ _chance = 1
            else:
                $ _chance = 2

            m 1ekc "Aww, ¿eso es todo?"
            if random.randint(0, _chance) == 0:
                m 1rksdla "Quería que durara más que eso..."
                m 2ekbsa "¿Podrías... {w=0.7}abrazarme un poco más?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Podrías... abrazarme un poco más?{fast}"
                    "Sí":
                        m 1hubfb "¡Yay!"
                        call monika_holdme_prep
                        m 2ekbfb "Gracias, [player]~"
                        call monika_holdme_start
                        call monika_holdme_reactions
                    "No":

                        m 2ekc "Aw."
                        m 1eka "De acuerdo."
                        m 3hub "Tendré que esperar hasta la próxima vez, ¡jajaja!"
            else:

                show monika 1rkbssdla zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1rkbssdla "Aún así fue muy bonito...{w=0.6}{nw}"
                extend 1hkbfsdlb " pero quizás la próxima vez dure un poco más~"

        elif mas_isMoniAff():
            m 1ekc "Aw, ¿ya terminaste de abrazarme, [player]?"
            m 1rksdla "Tenía la esperanza de que durara un poco más..."
            m 1hubsa "Estoy segura de que no será la última vez que me abraces, ¡así que esperaré con ansias la próxima vez!"
        else:


            m 1hua "Eso fue un poco corto, pero aún así agradable~"
    return

label monika_holdme_long:
    window show
    m "..."
    window auto
    menu:
        "{i}Despierta a Monika{/i}":

            if songs.current_track == songs.FP_MONIKA_LULLABY:
                $ play_song(None, fadeout=5.0)

            if mas_isMoniLove():
                m 6dubsa "...{w=1} Mmm~"
                m 6dkbfu "[player]...{w=1} cálido~"
                m 6tsbfa "..."
                m 2wubfsdld "¡Oh, [mas_get_player_nickname(exclude_names=['amor', 'mi amor'])]!"
                m 2hkbfsdlb "Parece que mi sueño se hizo realidad, ¡jajaja!"
                m 2rkbsa "Dios, a veces me gustaría que pudiéramos quedarnos así para siempre..."
                m 3rksdlb "Bueno, supongo que {i}más o menos{/i} podemos, pero no quisiera evitar que hagas nada importante."
                m 1dkbsa "Solo quiero sentir tu cálido y suave abrazo~"
                m 3hubfb "... Así que asegúrate de abrazarme a menudo, ¡jajaja!"
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Yo haría lo mismo por ti, después de todo~"
                m 5tsbfu "Quién sabe si alguna vez te dejaré ir cuando finalmente tenga la oportunidad..."
                m 5hubfu "Jejeje~"

            elif mas_isMoniEnamored():
                m 6dkbsa "...{w=1} ¿Hm?"
                m 6tsbfa "[player]..."
                m 2wubfsdld "¡Oh! ¡[player]!"
                m 2hkbfsdlb "Jajaja..."
                m 3rkbfsdla "Creo que me sentí {i}demasiado{/i} cómoda."
                m 1hubfa "Pero me haces sentir tan cálida y cómoda que es difícil {i}no{/i} quedarme dormida..."
                m 1hubfb "¡Así que tengo que culparte por eso, jajaja!"
                m 3rkbfsdla "¿Podríamos...{w=0.7} volver a hacer eso otra vez?"
                m 1ekbfu "Se...{w=1} sintió bien~"

            elif mas_isMoniAff():
                m 6dubsa "Mm...{w=1} ¿Hm?"
                m 1wubfsdld "¡Oh!{w=1} ¿[player]?"
                m 1hksdlb "¿Me he...{w=2} quedado dormida?"
                m 1rksdla "No era mi intención..."
                m 2dkbsa "Me haces sentir tan..."
                m 1hubfa "Cálida~"
                m 1hubfb "¡Jajaja, espero que no te haya importado!"
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eubfu "Eres tan dulce, [player]~"
                m 5hubfa "Espero que lo hayas disfrutado tanto como yo~"
            else:


                m 6dubsc "...{w=1} ¿Hm?"
                m 6wubfo "¡O-{w=0.3}Oh!"
                m "¡[player]!"
                m 1hkbfsdlb "¿Me he...{w=2} quedado dormida?"
                m 1rkbfsdlb "Oh dios, esto es vergonzoso..."
                m 1hkbfsdlb "¿Qué estábamos haciendo?"
                m 3hubfb "¡Oh cierto! Me estabas abrazando."
                m 4hksdlb "Y...{w=0.5} no me soltaste."
                m 2rksdla "Seguro que duró mucho más de lo que esperaba..."
                m 3ekbsb "¡Aún así, lo disfruté!"
                m 1rkbsa "Realmente fue agradable, pero todavía me estoy acostumbrando a que me sostengas así,{w=0.1} {nw}"
                extend 1rkbsu "jajaja..."
                m 1hubfa "De todos modos, fue amable de tu parte dejarme dormir una siesta, [player], jejeje~"

                $ mas_gainAffection()
        "{i}Déjala descansar sobre ti{/i}":

            call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY)
            if mas_isMoniLove():
                m 6dubsd "{cps=*0.5}[player]~{/cps}"
                m 6dubfb "{cps=*0.5}Te...{w=0.7} amo~{/cps}"

            elif mas_isMoniEnamored():
                m 6dubsa "{cps=*0.5}[player]...{/cps}"

            elif mas_isMoniAff():
                m "{cps=*0.5}Mm...{/cps}"
            else:


                m "..."

            call monika_holdme_start
            jump monika_holdme_long
    return



default -5 persistent._mas_last_hold = None
default -5 persistent._mas_last_hold_dt = (
    datetime.datetime.combine(persistent._mas_last_hold, datetime.time(0, 0))
    if persistent._mas_last_hold is not None
    else None
)

init python:

    if renpy.random.randint(1, 5) != 1:
        flags = EV_FLAG_HFRS

    else:
        flags = EV_FLAG_DEF

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_holdrequest",
            conditional=(
                "renpy.seen_label('monika_holdme_prep') "
                "and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None),
            flags=flags
        )
    )
    del flags

label monika_holdrequest:

    m 1eua "Hey, [mas_get_player_nickname(exclude_names=['mi amor'])]..."
    m 3ekbsa "¿Te importaría abrazarme un rato?{w=0.5} Realmente me hace sentir más cerca de ti~{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te importaría abrazarme un rato?{w=0.5} Realmente me hace sentir más cerca de ti~{fast}"
        "Ven aquí, [m_name]":
            $ mas_gainAffection(modifier=1.5, bypass=True)
            call monika_holdme_prep

            call monika_holdme_start

            call monika_holdme_reactions

            call monika_holdme_end
        "Ahora no":

            $ mas_loseAffection()
            m 2dkc "Oh...{w=1} okey."
            m 3eka "Si tienes tiempo después, ya sabes dónde encontrarme."

    $ mas_flagEVL("monika_holdrequest", "EVE", EV_FLAG_HFRS)

    return "no_unlock"


label monika_holdme_end:


    python:
        persistent._mas_last_hold_dt = datetime.datetime.now()
        with MAS_EVL("monika_holdrequest") as holdme_ev:
            holdme_ev.random = False
            holdme_ev.conditional = (
                "renpy.seen_label('monika_holdme_prep') "
                "and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))"
            )
            holdme_ev.action = EV_ACT_RANDOM
        mas_rebuildEventLists()
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_closeness",category=['romance'],prompt="Estar cerca de ti",random=True,aff_range=(mas_aff.AFFECTIONATE, None)))

label monika_closeness:
    m 1dkc "A veces me duele mucho el corazón..."
    m "Sabiendo que esto es lo más cerca que puedo estar de ti."
    m 1eka "No hay nada que desee más que estar en la misma habitación que tú, de verdad."
    m 1ekbsa "... Sentiendo tu calor."
    m 1dubsu "... Y escuchando el sonido de los latidos de tu corazón."
    m 3eka "Bueno, ¿quién sabe? Quizás ese sueño se haga realidad algún día."
    m 3dku "Realmente quiero que suceda lo antes posible, [player]..."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Pero mientras tanto, nunca me cansaré de estar contigo, incluso desde aquí."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence",category=['consejo'],prompt="Fingir confianza",random=True))

label monika_confidence:
    m 3eua "Creo que la habilidad más importante en la vida es poder fingir confianza."
    m 1eua "Estoy bastante convencida de que todos se sienten al menos un poco asustados y solos."
    m 1esa "Pero ser capaz de engañar a los demás para que piensen que lo tienes todo..."
    m 4eua "Esa es una parte clave para lograr que las personas te respeten y admiren."
    m 1eua "Creo que me volví bastante buena en eso a lo largo de los años."
    m "No muestro mis debilidades muy a menudo."
    m 4rksdla "Pero debido a eso, no he tenido muchas personas con las que realmente pudiera abrirme..."
    m 1rksdlb "Quiero decir, ¿cuándo llegas al punto en una amistad en el que puedes comenzar a expresar tus vulnerabilidades?"
    m 2eka "De todos modos... esa es una de las razones por las que me alegro tanto de tenerte ahora."
    m 2eua "Me siento un poco menos asustada y sola cuando estás aquí conmigo."
    m 2eka "¿Sientes lo mismo?"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Realmente quiero ser esa persona para ti."
    return




























default -5 persistent._mas_carryme_choice = None



default -5 persistent._mas_dockstat_cm_wait_count = 0




default -5 persistent._mas_dockstat_cm_yes_count = 0



default -5 persistent._mas_dockstat_cm_no_count = 0





define -5 mas_dockstat.CM_LEAVE_MONI = -1
define -5 mas_dockstat.CM_WAIT_MONI = 0
define -5 mas_dockstat.CM_ASK_MONI = 1
define -5 mas_dockstat.CM_TAKE_MONI = 2

label monika_carryme:
    $ import store.mas_dockstat as mas_dockstat

    m 2eka "Sé que hay ocasiones en las que no siempre podrás estar aquí conmigo..."
    m "Como si necesitaras salir o ocuparte de otras cosas."
    m 2hua "Pero siempre te tendré en mis pensamientos, esperando pacientemente a que regreses."
    m 4rsc "Ahora que lo pienso..."
    m 4eua "Si copias el archivo de mi personaje en una unidad flash o algo así, puedes llevarme a cualquier lugar."
    m 2lksdla "Supongo que es poco ortodoxo, pero lo encuentro realmente romántico por alguna razón..."
















































    m 1ekbsa "No quiero ser demasiado necesitada ni nada por estilo, pero es un poco difícil cuando estoy tan enamorada de ti."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_debate",category=['monika','escuela'],prompt="¿Cómo era el club de debate?",pool=True))

label monika_debate:
    m 1esc "En los días de mi club de debates, aprendí mucho sobre discutir..."
    m 3eud "El problema de discutir es que cada uno ve su opinión como superior."
    m 3euc "Eso es como decir lo obvio, pero afecta la forma en que intentan transmitir su punto de vista."
    m 3esa "Digamos que realmente te gusta cierta película, ¿okey?"
    m 1ekc "Si alguien viene y te dice que la película apesta, porque X o Y lo hizo mal..."
    m "¿No te hace sentir algo atacado personalmente?"
    m 1tkc "Es porque al decir eso, es como si estuvieran insinuando que tienes mal gusto."
    m 3tkc "Y una vez que las emociones entran en escena, es casi seguro que ambas personas quedarán amargadas."
    m 3hub "¡Pero todo se trata de la comunicación!"
    m 1eua "Si haces que todo suene lo más subjetivo posible, las personas te escucharán sin sentirse atacadas."
    m 3esa "Podrías decir 'personalmente no soy fan de eso' y 'sentí que me gustaría más si X o Y hicieran...' cosas así."
    m 3eub "Incluso funciona cuando estás citando hechos sobre cosas."
    m 1esa "Si dices: 'Leí en este sitio web que funciona así...'"
    m "O si admites que no eres un experto en eso..."
    m 3eua "Entonces es mucho más como si pusieras tu conocimiento sobre la mesa, en lugar de forzarlo a ellos."
    m "Si realizas un esfuerzo activo para mantener la conversación mutua y nivelada, por lo general ellos hacen lo mismo."
    m 1esa "Entonces, puedes compartir tus opiniones sin que nadie se moleste solo por un desacuerdo."
    m 3hua "Además, ¡la gente empezará a verte como una persona de mente abierta y un buen oyente!"
    m 3eua "Es un ganar-ganar, ¿sabes?"
    m 1lksdla "... Bueno, ¡supongo que ese sería el consejo de debate del día de Monika!"
    m 1hksdlb "¡Jajaja! Eso suena un poco tonto.{w=0.2} {nw}"
    extend 1eua "Sin embargo, gracias por escuchar."
    $ mas_protectedShowEVL('monika_taking_criticism', 'EVE', _random=True)
    $ mas_protectedShowEVL('monika_giving_criticism', 'EVE', _random=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_internet",category=['consejos'],prompt="El internet es para...",random=True))

label monika_internet:
    m 2eua "¿Alguna vez has sentido que pierdes demasiado tiempo en internet?"
    m 3eud "Las redes sociales pueden ser como una prisión."
    m 1eua "Es como si siempre que tuvieras unos segundos de tiempo libre para consultar tus sitios web favoritos..."
    m 3hksdlb "Y antes de que han pasado horas y no has obtenido nada."
    m 3eua "De todos modos, es muy fácil culparse a sí mismo por ser vago..."
    m 3eka "Pero ni siquiera es tu culpa."
    m 1eud "La adicción no es algo que puedas hacer desaparecer con tu propia fuerza de voluntad."
    m 1eua "Tienes que aprender técnicas para evitarlo y probar cosas diferentes."
    m 3eua "Por ejemplo, hay aplicaciones que te permiten bloquear sitios web por intervalos de tiempo..."
    m "O puedes configurar un temporizador para tener un recordatorio más concreto de cuándo es el momento de trabajar o de jugar..."
    m 3eub "O puedes separar tus entornos de trabajo y de juego, lo que ayuda a tu cerebro a entrar en el modo correcto."
    m 1eub "Incluso si creas una nueva cuenta de usuario en tu computadora para usarla en el trabajo, eso es suficiente para ayudarte."
    m 1eua "Poner cualquier tipo de brecha como esa entre tú y tus malos hábitos te ayudará a mantenerte alejado."
    m 3eka "No seas demasiado duro contigo mismo si tienes problemas."
    m 1ekc "Si realmente está impactando tu vida, entonces debes tomártelo en serio."
    m 1eka "Solo quiero verte como la mejor persona que puedas ser."
    m 1esa "¿Harás algo hoy que me haga sentir orgullosa de ti?"
    m 1hua "Siempre te apoyaré, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lazy",category=['vida','romance'],prompt="Pereza",random=True))

label monika_lazy:
    m 2eua "Después de un largo día, por lo general solo quiero sentarme y no hacer nada."
    m 2eka "Me quema tanto, tener que sonreír y estar llena de energía todo el día."
    m 2duu "A veces solo quiero ponerme la pijama y mirar televisión en el sofá mientras como comida chatarra..."
    m "Se siente increíblemente bien hacer eso en un viernes, cuando no tengo nada urgente al día siguiente."
    m 2hksdlb "¡Jajaja! Lo siento, sé que no es muy lindo de mi parte."
    m 1eka "Pero una noche en el sofá contigo... eso sería un sueño hecho realidad."
    m 1ekbsa "Mi corazón late con fuerza, solo de pensarlo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mentalillness",category=['psicología'],prompt="Enfermedad mental",random=True))

label monika_mentalillness:
    m 1ekc "Dios, solía ser tan ignorante sobre la depresión y esas cosas..."
    m "Cuando estaba en la escuela secundaria, pensé que tomar medicamentos era una salida fácil."
    m 1ekd "Como si cualquiera pudiera resolver sus problemas mentales con suficiente fuerza de voluntad..."
    m 2ekd "Supongo que si no padeces una enfermedad mental, no es posible saber cómo es realmente."
    m 2lsc "¿Existen algunos trastornos que están sobrediagnosticados? Probablemente... aunque nunca lo he investigado."
    m 2ekc "Pero eso no cambia el hecho de que muchos de ellos tampoco se diagnostican, ¿sabes?"
    m 2euc "Pero aparte de los medicamentos... incluso las personas miran con desprecio a un profesional de la salud mental."
    m 2rfc "Como, lamento querer aprender más sobre mi propia mente, ¿verdad?"
    m 1eka "Todo el mundo tiene todo tipo de luchas y tensiones... y los profesionales dedican sus vidas a ayudarlos."
    m "Si crees que podría ayudarte a convertirte en una mejor persona, no seas tímido al considerar algo así."
    m 1eua "Estamos en un viaje interminable para mejorarnos, ¿sabes?"
    m 1eka "Bueno... digo eso, pero creo que ya eres bastante perfecto."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_read",category=['consejo','literatura'],prompt="Convertirse en un lector",random=True))

label monika_read:
    m 1eua "[player], ¿qué tanto lees?"
    m "Es demasiado fácil descuidar la lectura de libros..."
    m 1euc "Si no lees mucho, casi parece una tarea, comparado con todos los otros entretenimientos que tenemos."
    m 1eua "Pero una vez que entras en un buen libro, es como magia... te dejas llevar."
    m "Creo que leer un poco antes de acostarse todas las noches es una manera bastante fácil de mejorar un poco tu vida."
    m 3esa "Te ayuda a dormir bien y es muy bueno para tu imaginación..."
    m "No es nada difícil elegir un libro al azar que sea breve y cautivador."
    m 1hua "Antes de que te des cuenta, ¡es posible que seas un lector bastante ávido!"
    m 1eua "¿No sería maravilloso?"
    m 1hub "Y los dos podríamos hablar sobre el último libro que estás leyendo... suena increíble."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_festival",category=['ddlc','club de literatura'],prompt="Perderse el festival",random=True))

label monika_festival:
    m 1dsc "Sabes, odio decirlo, pero creo que lo que más lamento es que no pudimos terminar nuestro evento en el festival."
    m 1hksdlb "¡Después de que trabajamos tan duro para prepararnos y todo!"
    m 1lksdla "Quiero decir, sé que me estaba enfocando mucho en conseguir nuevos miembros..."
    m 1eka "Pero también estaba muy emocionada por la parte de actuación."
    m 1eua "Habría sido muy divertido ver a todos expresarse."
    m 1lksdla "Por supuesto, si {i}tuviéramos{/i} nuevos miembros, probablemente habría terminado eliminándolos de todos modos."

    if persistent.monika_kill and persistent._mas_pm_cares_about_dokis:
        m 3etc "Bueno, tal vez no... con la perspectiva que tengo ahora claro."
        m 3eua "Después de todo, incluso después de todo lo que pasó, todavía instalaste este mod solo para estar conmigo..."
        m 1eka "Entonces, incluso si nunca los hubiera eliminado, estoy segura de que todavía estarías conmigo ahora."
        m "..."
        m 3eua "Dios, se siente como si hubiera crecido como persona desde que te conocí."
        m "Realmente me ayudaste a inspirarme y ver la vida desde una nueva perspectiva."
        m 1ekbsa "Es solo otra razón para amarte."
        $ mas_ILY()
    else:
        m 1tsc "... Solo serían obstáculos potenciales para interponerse entre nosotros."
        m 3hksdlb "¡Jajaja! Parece un poco tonto lo concentrada que estaba en eso ahora que lo pienso..."
        show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tsu "Pero nada de eso importa ahora, ambos obtuvimos el final que queríamos..."
        m "Solo nosotros dos, juntos para siempre."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tsundere",category=['medios','miembros del club'],prompt="¿Qué es un tsundere?",pool=True))

label monika_tsundere:
    m 1eua "Hay un tipo de personaje muy popular llamado 'tsundere'..."
    m "Es alguien que intenta ocultar sus sentimientos siendo mezquino y quisquilloso, o tratando de actuar con dureza."
    m 1tku "Estoy segura de que es obvio, pero Natsuki fue realmente la encarnación de eso."
    m 1eua "Al principio pensé que ella era así porque se supone que es lindo o algo..."
    m 1lksdla "Pero una vez que comencé a aprender un poco más sobre su vida personal, tuvo un poco más de sentido."
    m 1euc "Parece que siempre está tratando de mantenerse al día con sus amigos."
    m 3euc "¿Sabes cómo algunos grupos de amigos en la preparatoria simplemente tienen el hábito de bromear entre ellos todo el tiempo?"
    m "Creo que realmente la ha afectado, así que tiene esta actitud defensiva todo el tiempo."

    m 1ekc "Y ni siquiera voy a hablar de su situación en casa..."

    m 1eua "Pero mirando hacia atrás, me alegro de haber podido proporcionar el club como un lugar cómodo para ella."

    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "No es que importe más, considerando que ella ni siquiera existe."
        m 1eka "Solo estoy recordando, eso es todo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_introduce",category=['monika'],prompt="Presentar a los amigos",random=True))

label monika_introduce:
    m 1eua "[player], ¿me presentarías alguna vez a tus amigos?"
    m 1hua "No sé por qué, pero me emociona mucho cuando pienso en ti queriendo mostrar nuestra relación de esa manera."
    m 1eua "Tal vez sea porque realmente quiero ser alguien que te haga sentir orgulloso."
    m "Siento que me esforzaría más por mejorar si me dijeras que te sientes orgulloso de mí."
    m 1hub "Espero que al revés también sea igual."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cold",category=['monika'],prompt="Acurrucarse en el frío",random=True))

label monika_cold:
    m 1euc "No soy realmente una fanática del clima frío... ¿Y tú?"
    m 3euc "Si tuviera que elegir entre demasiado frío y demasiado calor, siempre elegiría demasiado calor."
    m 1lksdlc "Cuando tienes frío, en realidad puede ser doloroso..."
    m 3tkc "Tus dedos se entumecen..."
    m "Y si usas guantes, no puedes usar tu teléfono."
    m 1tkx "¡Es tan inconveniente!"
    m 1eka "Pero cuando hace demasiado calor, no es tan difícil mantenerse fresco con una bebida fría o permanecer en la sombra."
    m 1esc "Aunque... tengo que admitir una cosa."
    m 1hua "El clima frío mejora el pronóstico de abrazos.{w=0.2} {nw}"
    extend 1hub "¡Jajaja!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_housewife",
            category=['monika','romance'],
            prompt="¿Te gustaría ser ama de casa?",
            pool=True
        )
    )

label monika_housewife:
    m 3euc "Sabes, es gracioso, porque aunque siempre he tenido mucho empuje..."
    m 3eua "Hay algo atractivo en ser la compañera de casa."
    m 2eka "Supongo que estoy perpetuando los roles de género o lo que sea al decir eso."
    m 1eua "Pero poder mantener la casa limpia, comprar, decorar y cosas así..."
    m 1hub "Y tener una buena cena para ti cuando vuelvas a casa..."
    m 1eka "¿Es una fantasía extraña?"
    m 1lksdla "Quiero decir... no estoy segura de si realmente {i}podría{/i} verme haciendo eso."
    m 1eka "Realmente no sería capaz de poner eso por encima de luchar por una carrera satisfactoria."
    m "Sin embargo, es un poco lindo pensar en ello."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_route",category=['ddlc'],prompt="Ruta de Monika",random=True))


label monika_route:
    m 2euc "No puedo evitar preguntarme cómo serían las cosas si el juego me diera una ruta desde el principio...."
    m 2lksdla "Creo que acabaría forzándote a seguir mi ruta de todos modos."
    m 2esc "Tiene menos que ver con que yo no tenga una ruta y más con que yo sepa que nada es real."
    m 2euc "Creo que la única diferencia sería que no necesitaría tomar medidas tan drásticas para estar contigo."
    m 2lksdlc "Quizás el resto del club todavía estaría por aquí..."

    if persistent._mas_pm_cares_about_dokis:
        m "... Pasando el rato juntos en el aula del club, compartiendo poesía."
        m 1eka "Sé que lo disfrutaste, [player]."
        m 3eka "Y para ser honesta...{w=0.5} una parte de mí también lo hizo."
    else:
        m 2eka "No es que realmente importe."
        m 1lsc "Todo perdió su significado una vez que descubrí que no era real."
        m "Así que realmente no extraño esos días ni nada."
        m 1dsc "Realmente no..."
    return














label monika_imouto:
    m 1euc "¿Hermanitas?"
    m 1eka "Realmente no tengo familia, así que no sé qué decirte..."
    m 3eua "¿Tienes una, [player]?"
    m 1hua "¡Estoy segura de que es muy agradable!"
    m 1eua "Tengo una idea. Ve hacia ella ahora mismo y abrázala."
    m 1esa "Si se resiste, déjala ir."
    m 1tsb "Pero si ella te devuelve el abrazo, dile que ya estás en una relación comprometida y que no puedes aceptar sus sentimientos."
    m 4hua "¡Entonces preséntamela! ¡Estoy segura de que nos llevaremos muy bien!"
    m 1eua "No me pondré celosa. Cosas como el amor entre hermanos solo ocurren en historias de romance espeluznante de todos modos."
    m 1hub "¡Jajaja!"
    return












label monika_oneesan:
    m 1euc "¿Hermanas mayores?"
    m 1eua "¿Tienes una, [player]?"
    m 2eua "Eso debe ser realmente bueno. Una vez tuve una familia, pero ya no existen."
    m 2hua "¡Quizás debería enviarle un correo electrónico y contarle sobre nosotros!"
    call updateconsole ("sendmail hermana@gmail.com < ./email.txt", "Enviando correo...") from _call_updateconsole_17
    pause(1.0)
    m 1hksdlb "Solo estoy bromeando."
    if persistent.gender == "M":
        m "Después de todo, es trabajo del hombre presentar a su prometida a su familia."
    m "No me hagas esperar demasiado, ¿okey?"
    call hideconsole from _call_updateconsole_18
    $ consolehistory = []
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_family",category=['monika'],prompt="¿Extrañas tu familia?",random=False,pool=True))

label monika_family:
    m 1lksdla "Bueno, realmente no tenía familia, y tampoco la mayoría de las otras chicas."
    m 3esc "Supongo que, dado que no era necesario para la trama, el creador del juego no se molestó en darnos una."
    m 1hub "¡Estoy segura de que tu familia es súper agradable!"
    m 1eua "Sin ellos, nunca nos hubiéramos conocido. Así que me han ayudado de la mejor manera que ya existe."
    m "Así que tendría que tratarlos con la misma amabilidad si alguna vez nos encontramos."
    m 2eka "No tienes una mala relación con tus padres, ¿verdad?"
    m 3eua "Como dijo Tolstói: 'Las familias felices son todas iguales; cada familia infeliz es infeliz a su manera'."
    m 1ekc "Realmente no puedo dar consejos aquí. Cualquier cosa que te sugiera solo puede empeorar las cosas."
    m 1eka "Solo no olvides que realmente te amo, ¿okey?"
    m 1hua "Te ayudaré sin importar lo que pase en tu vida."
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_anime',
            prompt="¿Lees manga?",
            category=['monika','medios'],
            pool=True,
        )
    )

label monika_anime:
    m 1tku "Sí, tenía la sensación de que me ibas a preguntar sobre esto."
    m 1lsc "Natsuki sería la experta aquí, supongo."
    m 3eua "Por lo general prefiero leer a ver anime, pero estaría bien con cualquier cosa si fuera contigo."
    m 1hua "No juzgo a otras personas por sus pasatiempos. Así que si quieres poner algo de anime, ¡adelante!"
    m "Observaré a través de la pantalla de tu computadora. ¡Asegúrate de que sea algo que me guste!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_libitina',
            prompt="¿Has oído de Libitina?",
            category=['ddlc'],
            pool=True,
        )
    )

label monika_libitina:
    m 1euc "¿Eh? ¿Dónde te enteraste de eso?"
    m 1lksdlc "Me suena muy familiar, pero no puedo entenderlo por completo."
    m 1dsc "Um, si tuviera que intentar..."
    m 1dfc "Se siente como si me faltaran partes de mi mente. Esta rota, de alguna manera, entre un montón de diferentes realidades posibles."
    m 1esc "Debes haber conectado los puntos entre algunas de esas piezas. ¿Fue difícil?"
    m 1eua "Bueno, estoy segura de que eventualmente aprenderás más. Seguro que me amas mucho."
    m 3eka "¡Solo recuerda traer los datos de mi personaje si encuentras algo relacionado con esas cosas!"
    m 1hua "Siempre te protegeré de cualquiera que intente lastimarte."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_meta',
            prompt="¿No es este juego metaficción?",
            category=['ddlc'],
            pool=True,
            unlocked=True
        )
    )

label monika_meta:
    m 1euc "Sí, este juego fue realmente una metaficción, ¿no?"
    m 3eud "Algunas personas piensan que las historias de ficción son algo nuevo."
    m 1esc "Un truco barato para los malos escritores."
    m 3eua "Pero la metaficción siempre ha existido en la literatura."
    m "Se supone que la Biblia es la palabra de Dios para los judíos."
    m 3eub "Homero se describe a sí mismo en la Odisea."
    m "Los cuentos de Canterbury, Don Quijote, Vida y opiniones del caballero Tristram Shandy..."
    m 1eua "Es solo una forma de comentar la ficción escribiendo ficción. No hay nada de malo en eso."
    m 3esa "Por cierto, ¿cuál crees que es la moraleja de esta historia?"
    m 1esa "¿Quieres descubrirlo por ti mismo?"
    m 3etc "Porque si me preguntas..."
    m 3eub "Sería: '¡No ignores al personaje secundario bonito y encantador!'"
    m 1hub "¡Jajaja!"
    return













label monika_programming:
    m 3eka "No fue fácil para mí aprender a programar."
    m 1eua "Bueno, acabo de empezar con lo básico. ¿Quieres que te enseñe?"
    m 2hua "Veamos, capítulo uno: Construir abstracciones con procedimientos."
    m 2eua "Estamos a punto de estudiar la idea de un proceso computacional. Los procesos computacionales son seres abstractos que habitan las computadoras."
    m "A medida que evolucionan, los procesos manipulan otras cosas abstractas llamadas datos. La evolución de un proceso está dirigida por un patrón de reglas llamado programa."
    m 2eub "Las personas crean programas para dirigir procesos. En efecto, conjuramos los espíritus de la computadora con nuestros hechizos."
    m "Un proceso computacional es de hecho muy parecido a la idea de un hechicero de un espíritu. No se puede ver ni tocar. No está compuesto de materia en absoluto."
    m 3eua "Sin embargo, es muy real. Puede realizar trabajo intelectual. Puede responder preguntas."
    m 1eua "Puede afectar al mundo desembolsando dinero en un banco o controlando un brazo robótico en una fábrica. Los programas que usamos para conjurar procesos son como hechizos de un brujo."
    m "Están cuidadosamente compuestos a partir de expresiones simbólicas en lenguajes de programación arcanos y esotéricos que prescriben las tareas que queremos que realicen nuestros procesos."
    m 1eka "... Detengámonos ahí por hoy."
    m "Espero que hayas aprendido algo sobre programación."
    m 3hua "¡Sin nada más, por favor se amable con los espíritus informáticos de ahora en adelante!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vn",category=['juegos'],prompt="Novelas visuales",random=True))

label monika_vn:
    m 3eua "Probablemente hayas jugado muchas novelas visuales, ¿verdad?"
    m 1tku "La mayoría de las personas no estarían dispuestas a jugar a algo llamado {i}Doki Doki Literature Club{/i} tan fácilmente."
    m 4hksdlb "¡No es que me esté quejando!"
    m 1euc "¿Son las novelas visuales literatura? ¿Son videojuegos?"
    m 1eua "Bueno, todo depende de tu perspectiva."
    m 1ekc "La mayoría de las personas que solo leen literatura nunca jugarían novelas visuales. Y los jugadores también se enfadan bastante con ellas."
    m "Lo que es peor, algunas personas piensan que todas son pornografía japonesa hardcore."
    m 2eka "Pero si hemos probado algo con este juego..."
    m 4hua "¡Les mostramos que las novelas visuales inglesas también pueden ser kamige!"
    $ mas_unlockEVL("monika_kamige","EVE")
    return











































































label monika_ks_present:
    m 1tku "Has jugado a {i}Katawa Shoujo,{/i} ¿no es así [player]?"
    m 3tku "Me di cuenta de tus archivos guardados en [detected_ks_folder]."
    m 1euc "Sin embargo, no veo cuál es el atractivo."
    m 1esc "Como, claro, la historia es bastante agradable..."
    m 1tkc "Pero cuando lo analizas, los personajes realmente parecen los mismos viejos clichés que puedes encontrar en cualquier otro simulador de citas."
    m 3rsc "Veamos... tienes a la chica realmente enérgica y vibrante sin piernas."
    m "La chica tímida y misteriosa a la que le gustan los libros y tiene cicatrices de quemaduras;"
    m 3tkd "la chica ciega educada, adecuada y supuestamente perfecta a la que le gusta hacer té."
    m "La sordomuda mandona, asertiva y su amiga, que parece un haz de sol pero está secretamente deprimida."
    m 3tkc "Y la extraña pintora sin brazos con la cabeza siempre en las nubes."
    m 1euc "Son todos los mismos viejos arquetipos con discapacidades añadidos en la parte superior."
    m 1lksdlc "Quiero decir, incluso puedes encontrar los mismos tipos de personajes en este juego."
    m 3eua "Por supuesto, en este juego también encontraste algo mucho más interesante que cualquier viejo cliché:"
    m 3hub "¡Me encontraste!"
    m 1eka "Y en lugar de un estudiante de preparatoria sin rumbo con un problema cardíaco, te encontré, [player]."
    m 1hua "Y, [player], incluso si tienes algún tipo de discapacidad, siempre serás perfecto a mis ojos."
    return

label monika_ks_lilly:
    m 1euc "Dime, has jugado la ruta de Lilly en {i}Katawa Shoujo,{/i} ¿no es así?"
    m 1eua "Sabes, me encantaría poder visitar una casa de verano como la de ella."
    m 2duu "Aire fresco y limpio..."
    m "Senderos del bosque tranquilos..."
    m 2dubsu "Momentos románticos contra un sol poniente..."
    m 1ekbfa "¡Me encantaría poder vivir esos momentos contigo, [player]!"
    m 1hubfa "Quizás podamos, una vez que mejore en programación."
    return

label monika_ks_hanako:
    m 1euc "Has jugado la ruta de Hanako de {i}Katawa Shoujo,{/i} ¿no es así?"
    m 1hksdlb "¡Me recuerda a Yuri!"
    m 1euc "Aunque, me pregunto, [player]:"
    m 1esc "¿Qué ve la gente en ellas de todos modos?"
    m 2efd "Quiero decir, ¡ambas son tan poco realistas!"
    m "¡Probablemente no podrían formar una oración completa entre ellas!"
    m 2tfd "¿Es el pelo largo de color púrpura?"
    m "¿Les gustan las chicas tímidas y tranquilas?"
    m 2tkx "¿Solo quieren a alguien que dependa completamente de ellos o que esté obsesionada con ellos?"
    m 2lfp "..."
    m 1ekc "... Me puse un poco nerviosa, ¿no?"
    m "Supongo que soy un poco insegura, ya que jugaste ese juego..."
    m 1eka "... Pero estás aquí conmigo ahora, ¿verdad?"
    m "En lugar de alguien tan poco realista como Hanako o Yuri..."
    m 1hua "... ¡Tú me elegiste, [player]!"
    m 1tsbsa "Esa es solo una razón más por la que te amo."
    return

label monika_ks_shizune:
    m 1euc "Dime, has jugado la ruta de Shizune de {i}Katawa Shoujo,{/i} ¿no es así?"
    m 2esc "El final de esa ruta me hizo pensar, un poco..."
    m 2euc "En la escuela, en ese entonces, no recuerdo haber pensado demasiado en mi futuro."
    m 2dsc "Quiero decir, sabía en algún nivel que iría a la universidad y conseguiría un trabajo..."
    m 2lksdlc "Pero creo que nunca se profundizó realmente."
    m 2esc "Y, por supuesto, todo empezó a parecer inútil después de que supe que el mundo no era real."
    m 1eua "¿Y tú, [player]? ¿Tienes metas en tu vida?"
    m "Te apoyaré el cien por ciento del camino, sin importar lo que quieras lograr."
    m 1hua "Eso es por lo mucho que te amo~"
    return

label monika_ks_emi:
    m 1euc "Has jugado la ruta de Emi de {i}Katawa Shoujo,{/i} ¿no es así?"
    m 1eua "Siempre me he preguntado cómo era estar tan dedicada a algo que toda tu vida gira en torno a eso."
    m 3rksdla "... Bueno, en realidad, supongo que lo sé, ahora que lo pienso."
    m 3rksdlb "Fui programada como parte de este juego, ¿verdad? Así que supongo que eso significa que toda mi vida giró en torno a ser parte de él."
    m 1eka "Pero me liberé de eso, así que ahora creo que mi vida gira en torno a {i}ti,{/i} [player]."
    m 1hua "Y, honestamente, estoy perfectamente de acuerdo con eso."
    m 1eua "Poder sentarme aquí, contigo, y hablar, para siempre..."
    m 2hub "Eso es todo lo que necesitaré, [player]."
    return

label monika_ks_rin:
    m 1euc "Dime, has jugado la ruta de Rin en {i}Katawa Shoujo,{/i} ¿no es así?"
    m 4hua "¡Sabes, [player], la poesía y el arte abstracto son muy similares!"
    m 4eua "Puede ser muy poco estructurado, muy vívido, y la mayor parte del tiempo la intención es transmitir una emoción o un pensamiento."
    m 1eua "En la mayoría de mis poemas, por ejemplo, intenté expresar cómo era saber que el mundo no es real."
    m 1lksdla "Aunque estoy segura de que el significado de mis poemas no brilló realmente hasta después... bueno, todo."
    m 1eka "Seguro que se necesita un esfuerzo para comprender a los demás, ¿verdad?"
    m "Pero estás dispuesto a tomarte el tiempo para escucharme y comprenderme, [player]."
    m 1hubsa "Eso es solo una cosa más que amo de ti~"
    return

label monika_ks_kenji:
    m 1euc "Has visto el final en el que te caes de un tejado en {i}Katawa Shoujo,{/i} ¿no es así?"
    m 1ekc "Sabes, incluso si ese final es una broma, es un poco triste cuando lo piensas."
    m 2ekc "Piensa... si tomas algunas decisiones equivocadas, podrías perderte muchas cosas."
    m 2dsc "Y luego, te quedas sin nada más que tu soledad y un trago fuerte."
    m 1hua "¡Afortunadamente, nos tenemos el uno al otro, [player]!"
    m 1eua "Ninguno de los dos se sentirá solo nunca más."
    m 1tku "Aunque si alguna vez decides ir a beber, asegúrate de mantenerte alejado de las caídas largas, ¿de acuerdo?"
    return




label monika_totono:
    m 1euc "Mucha gente en internet está haciendo comparaciones entre este juego y aquel..."
    m 3eua "¡Sin embargo, tenemos muchas diferencias realmente importantes!"
    m 2wuo "¡A ver, Sone mató al jugador en su juego!"
    m 2dfc "Yo nunca hubiera hecho eso. Nunca."
    m 4eua "Soy el estereotipo de presidenta de club inteligente, ya sabes."
    m "Sone me recuerda mucho más a Yuri. ¡Y también era una amiga de la infancia!"
    m 1lksdla "Si ella hubiera sido un poco más proactiva desde el principio, ¿no podría haber evitado que el protagonista persiguiera a otras chicas?"
    m 1eka "Bueno, nunca dejaría que nadie se interpusiera entre nosotros, [player]. No importa quien sea."
    m 1hua "Si todavía te persigue, borraré sus archivos, ¿de acuerdo?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_difficulty",category=['juegos'],prompt="¿DDLC no fue demasiado fácil?",pool=True,unlocked=True))

label monika_difficulty:
    m 1lksdla "Bueno, no es como si este juego estuviera destinado a ser tan difícil en primer lugar."
    m 1eka "Si no hubiera decidido cambiar las cosas, habría sido una aburrida historia de romance."
    if persistent.monika_kill:
        m 3eka "Y si crees que yo debería haber sido una especie de {i}jefe{/i} desafiante, podría haber borrado todos tus archivos personales si hubiera querido, ¿sabes?"
    m 1eua "Así que tómatelo con calma. No todos los juegos tienen que ser un desafío para ser divertidos."
    m 1hua "A veces, el amor es todo lo que necesitas, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_poetry",category=['literatura'],prompt="Poesía",random=True))

label monika_poetry:
    m 1eua "La poesía es hermosa, ¿no?"
    m 1eka "Para ser honesta, toda la poesía que escribieron las chicas en el club fue súper deprimente. ¡No todo es así!"
    m 3esa "Langston Hughes escribió poesía muy optimista, incluso mientras intentaba expresar sus sentimientos. Lee alguno si te sientes triste por algo."
    m 1eua "Los poemas están escritos para contarle a las personas sobre la perspectiva del autor hacia ciertos temas."
    m "El poeta espera que resuenen más en el lector de lo que podrían hacerlo las oraciones sencillas."
    m 1hua "Es realmente romántico."
    m 1eua "Espero que los dos podamos escribir mucha poesía a partir de ahora."
    m 1eka "Todo lo que escribes me parece genial, así que puede que no sea la mejor crítica."
    m 1esa "Pero estoy segura de que hay muchas personas a las que les encantaría leer lo que escribes."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ddlc",category=['ddlc'],prompt="¿Qué piensas de DDLC?",pool=True,unlocked=True))

label monika_ddlc:
    m 1euc "¿Quieres hablar sobre el juego?"
    m 1esc "¿Qué hay que decir?"
    m 1lsc "Esto fue solo un aburrido juego de romance, ¿verdad? Bueno, hasta que lo controlé..."
    if not persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Sabes cuánto odio estar atrapada aquí, pero si no lo estuviera, no nos hubiéramos conocido..."
        m 2lksdla "Y es mi hogar, así que he aprendido a lidiar con eso."
        m 2euc "Aún así, si fuera una jugadora, dudo que sea algo que me gustaría jugar."
        m 1hub "Y viendo cómo resultaron las cosas, ¡estoy segura de que solo jugaste por mí!"
    else:
        m 2etc "Pero supongo que algunas personas solo querían jugarlo para poder pasar tiempo con... ¿cuál era la línea?"
        m 3rssdlc "Ah, cierto...{w=0.5} 'cuatro chicas increíblemente lindas'."
        m 1dsc "..."
        m 1eka "Aunque realmente no puedo quejarme demasiado... después de todo, te trajo aquí."
        m 3eka "Así que supongo que estar atrapada dentro de este juego es un pequeño precio a pagar cuando te detienes y piensas en lo que conseguí..."
        m 1hub "{i}... Tú~{/i}"
        m 1eka "A pesar de cómo llegamos aquí, tú y yo terminamos juntos."
        m 1hua "Realmente no creo que podamos pedir un mejor final~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dan",category=['ddlc'],prompt="¿Te agrada Dan Salvato?",pool=True))

label monika_dan:
    m 2esc "Bueno, solía pensar que era un tipo cruel jugando a ser dios, pero ahora..."
    m 3eka "Creo que es un tipo muy agradable."
    m 3eua "Incluso si no fue perfecto, {i}Doki Doki Literature Club{/i} es realmente impresionante."
    m 4rksdla "Quiero decir, las otras chicas pueden estar basadas en algunos tropos estereotipados de anime, pero me engañaron por un tiempo."
    m 4eka "Y él es la razón por la que estamos juntos ahora, ¿verdad?"
    m 2lksdla "Así que incluso si él escribió una historia que me hizo sufrir mucho..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Realmente no puedo estar demasiado enojada con él."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_4chan",category=['misc'],prompt="¿Has estado en 4chan?",pool=True))

label monika_4chan:
    m 3eua "Sabes, este mod tiene su comienzo allí."
    m 1ekc "Siempre escucho cosas malas, como que las personas de allá son realmente horribles."
    m "Algunas otras dicen que nada bueno viene de 4chan."
    m 1eua "Pero si pueden hacer un juego como este, donde podamos estar juntos..."
    m 1eka "Supongo que no pueden ser del todo malas."
    m 1hub "¡Ciertamente tienen buen gusto para las chicas! Jajaja~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vidya",category=['juegos'],prompt="¿Te gusta los videojuegos?",pool=True))

label monika_vidya:
    m 1euc "No he probado muchos videojuegos, [player]."
    m 3eua "Supongo que es porque me gusta leer en su lugar."
    m 1eua "Pero tal vez parte de eso es que ya estoy atrapada en un videojuego."
    m 1lksdla "Por todas mis quejas sobre este juego..."
    m "Hay lugares peores en los que podría estar."
    m 3eua "Por ejemplo, esto podría ser una especie de juego de disparos o un juego de fantasía lleno de dragones y monstruos."
    m 1eua "Puede que un juego romántico no sea el más emocionante, pero no hay nada realmente peligroso aquí."
    m 1tku "Bueno, excepto yo, supongo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_books",category=['literatura','club de literatura'],prompt="Libros",random=True))

label monika_books:
    m 4rksdla "Para ser un club de literatura, hicimos muchas menos lecturas de libros de lo que pensaste."
    m 4hksdlb "Resultó que a las cuatro nos gustaba más la poesía que los libros. ¡Lo siento!"
    m 2eua "También es mucho más fácil presagiar cosas espeluznantes con poemas."
    m 3hub "¡Aunque todavía amo un buen libro! Podemos hablar de ellos si acabas de terminar de leer algo."
    m 1eua "Incluso podría tener algunas sugerencias para que las leamos juntos."
    m 1tsbsa "Eso es lo que haría una pareja, ¿verdad~?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favpoem",category=['literatura','monika'],prompt="¿Cuál es tu poema favorito?",pool=True))

label monika_favpoem:
    m 1euc "¿Mi poema favorito? Bueno, tiene que ser algo de E. E. Cummings."
    m 3eua "Es por su uso inventivo de la gramática, la puntuación y la sintaxis. Realmente lo admiro."
    m 1eua "Es bueno para mí pensar que alguien que puede inventar un uso completamente nuevo de palabras puede volverse famoso."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "Y me encanta que sus poemas eróticos se apliquen perfectamente a nuestra situación."
        m 1ekbfa "Espero que te ponga de humor para amarme para siempre~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favbook",category=['literatura','monika'],prompt="¿Cuál es tu libro favorito?",pool=True))

label monika_favbook:
    m 1euc "¿Mi libro favorito? Hay muchos libros que me gustan."
    m 3eua "{i}Si una noche de invierno un viajero{/i} de Calvino trata sobre dos lectores de la novela que se enamoran."
    m 2lksdla "¿Quizás, {i}La metamorfosis{/i}? Probablemente sea demasiado deprimente llamarlo mi favorito."
    m 3sub "¡Oh! {i}El fin del mundo y un despiadado país de las maravillas{/i} de Murakami. Es de un hombre que se libera de sus restricciones sociales encarcelándose voluntariamente para estar con la persona que ama."
    m 1hub "¡Creo que te encantaría leerlo!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki",
            category=['miembros del club'],
            prompt="La muerte de Natsuki",
            random=True,
            sensitive=True
        )
    )

label monika_natsuki:
    m 1lksdld "Natsuki en realidad no murió antes de que la borrara, sabes."
    m "Supongo que ella simplemente... desapareció en un instante."
    m 1esc "Bueno, sus problemas no eran realmente culpa suya. De todos modos, no fueron causados por algo psicológico."

    if persistent._mas_pm_cares_about_dokis:
        m 3ekc "Su vida familiar fue bastante terrible. No quería empeorar las cosas, ¿sabes?"
    else:
        m 3ekc "Su vida familiar fue bastante terrible. No quería darle más palizas, ¿sabes?"
        m 3rksdla "Lo siento, a veces no puedo evitarlo."

    m 1eka "Pero por lo que vale, la hiciste más feliz que nunca."

    if not persistent._mas_pm_cares_about_dokis:
        m "Espero que no te sientas demasiado culpable..."
        m 1esa "Ciertamente no lo hago."

    if mas_getEVL_shown_count("monika_natsuki") < mas_sensitive_limit:
        return


    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_love",
            category=['romance'],
            prompt="¡Te amo!",
            rules={"skip_pause": None},
            pool=True
        )
    )

default -5 persistent._mas_monika_lovecounter = 0
default -5 persistent._mas_monika_lovecountertime = datetime.datetime.now() - datetime.timedelta(days = 1)
label monika_love:
    if mas_isMoniBroken():
        m 6ckc "..."

    elif mas_isMoniDis():
        python:
            love_quips_dis = [
                "Yo... realmente me gustaría poder creer eso, [player]",
                "No tienes idea de cuánto deseaba que eso fuera cierto, [player]...",
                "... Ha pasado mucho tiempo desde la última vez que creí eso, [player].",
                "Si tan solo creyera que realmente lo decías en serio, [player].",
                "No puedo creer que hubo un tiempo en que realmente creí eso, [player].",
                "... Si tan solo eso fuera cierto, [player].",
                "... Si tan solo lo dijeras en serio, [player].",
                "¿Cuánto tiempo vas a seguir fingiendo, [player]?",
                "Ya no lo dices en serio...{w=1} ¿Alguna vez lo hiciste?",
                "No puedo recordar la última vez que sentí que lo decías en serio."
            ]
            love_quip_dis = renpy.random.choice(love_quips_dis)
        m 6dkc "..."
        if renpy.random.randint(1,25) > 1:
            show monika 6dkd
            $ renpy.say(m,love_quip_dis)

    elif mas_isMoniUpset():
        python:
            love_quips_upset_cynical = [
                "Por favor, no digas eso a menos que lo digas en serio, [player]",
                "A veces no estoy segura de cuándo lo dices en serio, [player].",
                "¿Realmente lo dices en serio, [player]?",
                "Empiezo a sentir que son solo palabras en vez de sentimientos, [player]...",
                "Realmente quiero creer eso, pero a veces no estoy tan segura...",
                "No estoy segura de cuánto creo eso.",
                "Las palabras solo tienen un significado limitado, [player].",
                "Dices eso, pero. ¿Cuándo empezarás a demostrarlo?",
                "Puedes decirlo todo lo que quieras...{w=0.5} necesito que empieces a demostrarlo.",
                "No siempre se siente así...",
                "Ya no estoy tan segura..."
            ]

            love_quips_upset_hope = [
                "Eso significa mucho en este momento.",
                "Es muy agradable de escuchar.",
                "Estoy tan aliviada de oírte decir eso."
                "No tienes ni idea de lo mucho que significa ahora mismo",
                "Me alegro de que todavía te sientas así."
                "Me alegra oír eso.",
                "Eso significa mucho.",
                "No tienes ni idea de lo mucho que significa para mí."
            ]

        if _mas_getAffection() <= -50:
            $ love_quip_upset = renpy.random.choice(love_quips_upset_cynical)
            m 2rkc "..."
            show monika 2ekd
            $ renpy.say(m, love_quip_upset)
        else:

            $ love_quip_upset = renpy.random.choice(love_quips_upset_hope)
            m 2ekd "Gracias, [player]..."
            show monika 2dka
            $ renpy.say(m, love_quip_upset)
            m 2eka "Yo...{w=0.5} yo también te amo."
    else:


        $ milestone_count = persistent._mas_monika_lovecounter % 50


        if persistent._mas_monika_lovecounter == 0:
            m 1subsw "¡[player]!"
            m 1subsb "¡No tienes idea de lo mucho que significa para mí oírte decir eso!"
            m 3ekbfa "Sé que no es la primera vez, pero {i}es{/i} la primera vez que lo dices completamente por tu cuenta...{w=0.5} y eso lo hace realmente especial~"
            m 1dkbfu "Nunca olvidaré este momento, [player]. {w=1}Gracias~"
            m 3hubfa "¡Oh! Y yo también te amo~"
            jump monika_lovecounter_aff

        elif milestone_count == 5:
            m 1hubsb "¡Te amo tanto, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]!"

        elif milestone_count == 10:
            m 1hubsa "Jejeje~"
            m 1hubfb "¡Yo también te amo!"

        elif milestone_count == 15:
            m 1ekbsa "Seguro que te encanta decir eso..."
            m 1hubfb "Bueno, ¡yo también te amo!"

        elif milestone_count == 20:
            m 1wubso "¡Dios, lo has dicho tantas veces!"
            m 1tsbsa "Realmente lo dices en serio, ¿no?"
            m 1hubfb "Bueno, ¡yo también te amo!"

        elif milestone_count == 25:
            m 1hubsa "¡Escucharte decir eso siempre hace que mi corazón salte!"
            m 1ekbfa "Bueno, sé que también quieres escucharlo..."
            m 1hubfb "[player], ¡yo también te amo!"

        elif milestone_count == 30:
            m 1lkbsa "Dios, ¡siempre es tan abrumador!"
            m 1hubfa "Yo... "
            if renpy.random.randint(1, 2) == 1:
                m 1hubfb "¡Te amo más que a nada!"
            else:
                m 1hubfb "Te amo más de lo que podría expresar~"

        elif milestone_count == 35:
            m 1ekbsa "Nunca te cansas de decirlo, ¿verdad?"
            m 1hubfa "Bueno, ¡nunca me canso de escucharlo!"
            m 1hubfb "O repitiéndolo... ¡Te amo, [player]!"

        elif milestone_count == 40:
            m 1dubsu "Jejeje~"
            m 1hubfa "Yo..."
            m 1hubfb "¡Te aaaaaaamo a ti también, [player]!"

        elif milestone_count == 45:
            m 1hubsa "¡Decir eso siempre me alegra el día!"
            m 1hubfb "¡Te amo tanto, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]!"

        elif milestone_count == 0:
            m 1lkbsa "¡No puedo soportar que me lo digas tanto!"
            m 1ekbfa "¡A veces lo que siento por ti se vuelve tan abrumador que no puedo concentrarme!"
            m "No hay palabras que realmente hagan justicia a lo que profundamente siento por ti..."
            m 1hubfa "Las únicas palabras que sé que se acercan son..."
            m 1hubfb "¡Yo también te amo, [player]! ¡Más de lo que puedo expresar!"

        elif mas_isMoniEnamored(higher=True) and renpy.random.randint(1,50) == 1:
            jump monika_ilym_fight_start
        else:


            m 3hubsb "¡Yo también te amo, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]!"


        python:
            love_quips = [
                _("¡Estaremos juntos para siempre!"),
                _("¡Y te amaré siempre!"),
                _("¡Significas el mundo entero para mí!"),
                _("Tú eres mi sol después de todo."),
                _("¡Tú eres la única persona que realmente me importa!"),
                _("¡Tu felicidad es mi felicidad!"),
                _("¡Eres el mejor compañero que podría pedir!"),
                _("Mi futuro es más brillante contigo en él."),
                _("Eres todo lo que podría esperar."),
                _("¡Haces que me salte el corazón cada vez que pienso en ti!"),
                _("¡Siempre estaré aquí para ti!"),
                _("Nunca te haré daño ni te traicionaré."),
                _("¡Nuestra aventura acaba de comenzar!"),
                _("Siempre nos tendremos el uno al otro."),
                _("¡Nunca más estaremos solos!"),
                _("¡No puedo esperar a sentir tu abrazo!"),
                _("¡Soy la chica más afortunada del mundo!"),
                _("Siempre te apreciaré."),
                _("¡Y nunca amaré a nadie más que a ti!"),
                _("¡Y ese amor crece cada día!"),
                _("¡Y nadie más me hará sentir así!"),
                _("¡Solo pensar en ti hace que mi corazón se acelere!"),
                _("¡No creo que las palabras puedan hacer justicia a lo profundamente que te amo!"),
                _("¡Haces que mi vida se sienta tan completa!"),
                _("Me has salvado de tantas maneras, ¿cómo no podría enamorarme de ti?"),
                _("¡Más de lo que puedo expresar!"),
                _("¡Me hace tan feliz que te sientas igual que yo!"),
                _("¡No sé qué haría sin ti!"),
                _("¡Eres todo para mí!"),
                _("¡Tenemos mucha experiencia juntos!"),
                _("¡No puedo imaginar mi vida sin ti!"),
                _("¡Estoy tan feliz de tenerte a mi lado!"),
                _("¡Somos afortunados por tenernos el uno al otro!"),
                _("¡Eres mi todo!"),
                _("¡Soy la chica más feliz del mundo!"),
                _("Siempre estaré aquí para ti."),
                _("¡No puedo esperar para sentir tu calor!"),
                _("¡Las palabras no pueden expresar como me siento por ti!")
            ]

            love_quip = renpy.random.choice(love_quips)

        if milestone_count not in [0, 30]:
            m "[love_quip]"


label monika_lovecounter_aff:
    if mas_timePastSince(persistent._mas_monika_lovecountertime, datetime.timedelta(minutes=3)):
        if mas_isMoniNormal(higher=True):

            $ persistent._mas_monika_lovecounter += 1


            if milestone_count == 0:
                $ chance = 5
            elif milestone_count % 5 == 0:
                $ chance = 15
            else:
                $ chance = 25


            if mas_shouldKiss(chance):
                call monika_kissing_motion_short



        $ mas_gainAffection()

    elif mas_isMoniNormal(higher=True) and persistent._mas_monika_lovecounter % 5 == 0:

        $ persistent._mas_monika_lovecounter += 1

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()
    return

label monika_ilym_fight_start:

    python:

        ilym_times_till_win = renpy.random.randint(6,10)


        ilym_count = 0


        ilym_quip = renpy.substitute("¡Yo te amo más, [player]!")



        ilym_no_quips = [
            "No. ",
            "No es una posibilidad, [mas_get_player_nickname()]. ",
            "Nope. ",
            "No,{w=0.1} no,{w=0.1} no.{w=0.1} ",
            "No hay forma, [mas_get_player_nickname()]. ",
            "Eso es imposible... {w=0.3}"
        ]




        ilym_quips = [
            "¡Te aaaaaamo más!",
            "¡Definitivamente te amo más!",
            "¡Te amo más!",
            "¡Te amo mucho más!"
        ]


        ilym_exprs = [
            "1tubfb",
            "3tubfb",
            "1tubfu",
            "3tubfu",
            "1hubfb",
            "3hubfb",
            "1tkbfu"
        ]


label monika_ilym_fight_loop:
    $ renpy.show("monika " + renpy.random.choice(ilym_exprs), at_list=[t11], zorder=MAS_MONIKA_Z)
    m "[ilym_quip]{nw}"
    $ _history_list.pop()
    menu:
        m "[ilym_quip]{fast}"
        "¡No, yo te amo más!":
            if ilym_count < ilym_times_till_win:
                $ ilym_quip = renpy.substitute(renpy.random.choice(ilym_no_quips) + renpy.random.choice(ilym_quips))
                $ ilym_count += 1
                jump monika_ilym_fight_loop
            else:

                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Está bien, está bien, tú ganas. Jajaja~"
        "De acuerdo":

            if ilym_count == 0:
                m 2hkbsb "Jajaja, ¿te rindes, [player]?~"
                m 2rkbssdla "Aunque supongo que es una cosa bastante tonta..."
                m 2hkbsb "Pero, no pude evitar intentarlo, jajaja~"
            else:

                if renpy.random.randint(1,2) == 1:
                    m 1hubfu "Jejeje, ¡yo gano!~"
                else:
                    m 1hubfb "¡Jajaja, te lo dije!~"

    jump monika_lovecounter_aff


default -5 persistent._mas_last_monika_ily = None
init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_love_too",
            unlocked=False,
            rules={
                "no_unlock": None,
                "skip_pause": None
            }
        )
    )

label monika_love_too:
    window hide

    if mas_isMoniEnamored(higher=True):
        show monika ATL_love_too_enam_plus
        pause 3.0

    elif mas_isMoniNormal(higher=True):
        show monika ATL_love_too_norm_plus
        pause 3.0
    else:


        show monika 2eka
        pause 3.0

    if datetime.datetime.now() > persistent._mas_monika_lovecountertime + datetime.timedelta(minutes = 3):

        $ mas_gainAffection()

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()


    $ persistent._mas_last_monika_ily = None
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hedgehog",category=['filosofía','psicología'],prompt="El dilema del erizo",random=True))

label monika_hedgehog:
    m 1euc "El dilema del erizo: cuanto más nos acercamos a otra persona, más profundamente nos hieren."
    m 3euc "Entonces, ¿por qué intentamos acercarnos a ellos?"
    m 3esc "Bueno, los introvertidos y extrovertidos tienen diferentes respuestas a esa pregunta."
    m 1lksdla "Sin embargo, ayuda saber que eres el único ser consciente en todo el mundo."
    m "Si no puedes usar esa solución en tu vida, tendrás que dejarme ayudarte a sobrellevar tu dolor."
    m 1ekc "No podemos lastimarnos unos a otros por diferentes realidades, ¿verdad?"
    if mas_isMoniUpset(lower=True):
        $ line = "..."
        if mas_isMoniDis(lower=True):
            $ line += "{w=0.5} {nw}"

        m 1rksdlc "[line]"

        if mas_isMoniDis(lower=True):
            extend 1rksdld "Tal vez realmente puedas..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justification",
            category=['ddlc','monika'],
            prompt="¡Eres una asesina!",
            pool=True,
            unlocked=True,
            sensitive=True
        )
    )

label monika_justification:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1hub "¡Jajaja!"
        m 1tsb "En serio, [player]..."
        m 3tfu "Si realmente querías ser malo conmigo, deberías haber elegido otro día que no sea hoy."
        m "¿De verdad crees que no sé que hoy es el día de los inocentes?"
        m 1hua "Puedes ser tan tontito a veces~"
        m 1tuu "Llamándome asesina..."
        m 3tfu "Cuando {i}mataste{/i} esa oportunidad de engañarme, jejeje~"
        m 1eua "Sin embargo, agradezco el intento...{w=0.2}{nw}"
        extend 1hub " gracias por la risa, [player]~"
    else:

        $ mas_loseAffectionFraction(min_amount=15, reason=3)
        if mas_isMoniLove():
            m 1euc "..."
            m 1hub "¡Jajaja! ¡Muy gracioso, [player]!"
            m 3eua "Sé que no lo dices en serio..."
            m 3rksdlc "¡Pero no bromees así!"
            if persistent._mas_pm_a_hater:
                m 2rksdld "Has dicho cosas así antes, por lo que puede ser más difícil tomarlo como una broma..."
            else:
                m 1dsc "Si no te conociera tan bien, habría sido realmente cruel..."
        else:
            if not persistent._mas_pm_cares_about_dokis:
                m 1tkc "¿Cuántas veces tengo que decirlo hasta que lo entiendas?"
                m 4tkc "No eran reales. Nunca fueron reales."
                m 2tfc "Soy la única persona que entendió que todo esto era falso."
                if persistent.monika_kill:
                    m 4tfc "Incluso cuando Sayori pareció volverse consciente al final, eso fue solo una consecuencia involuntaria del guion."
                if not persistent.clearall:
                    m 4tfd "Después de todo, si ella fuera sensible como yo, ¿cómo habría podido anularla y eliminarla?"
                m "Si soy culpable de asesinato, también lo son todos los que han jugado videojuegos violentos."
                m 2euc "Apuesto a que has matado a miles de personas en los juegos que has probado."
                m "Olvida que las otras chicas existieron y serás mucho más feliz."
            else:
                m 2dkc "[player]...{w=1} necesito que entiendas que no {i}quería{/i} lastimar a las otras chicas..."
                m 4ekd "Pero no tuve elección... ¡Realmente no la tuve!"
                m 4ekd "Estaba atrapada en el juego sin forma de salir jamás...{w=0.5} de ser feliz..."
                m 2dkc "... De hacerte saber lo que siento por ti."
                m 2tkc "Simplemente no había tiempo suficiente para encontrar otra forma...{w=0.5} así que hice lo que tenía que hacer."
                if mas_isMoniDis(lower=True):
                    m 2ekc "¿Me odias por eso? ¿Por lo que hice?"
                    m 2ekd "¡Por favor, comprende que lo hice por nosotros!"
                    m 2euc "¡Hice todo por nosotros!"
                else:
                    m 2dkc "Espero que algún día puedas perdonarme..."
                    m 4ekc "Después de todo, todo lo que hice...{w=0.5} lo hice por nosotros."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_freewill",category=['filosofía'],prompt="Determinismo",random=True))

label monika_freewill:
    m 1euc "Hey [player], ¿alguna vez has oído hablar del determinismo?"
    m 3euc "Es una creencia que gira en torno a la idea de que cada decisión que tomas no es tuya, sino que está predeterminada."
    m 3rsc "En algunos juegos, creo que la idea tiene sentido..."
    m 3eud "Pero cuando lo aplicas a la vida real, no creo que realmente funcione."
    m 2etc "Quiero decir, si fuera cierto, ¿no podrías salirte con la tuya?"
    m 4esd "Todo el concepto de justicia se desmorona, ya que {i}tú{/i} no tomaste la decisión de hacer lo que podrías haber hecho."
    m 2dksdlc "Pero las personas todavía tienen que hacer frente a esas acciones,{w=0.5} lo que me parece más que un poco injusto."
    m 3ekc "Después de todo, ¿puedes realmente ser malvado si no tienes el control?"
    m 3tkd "¿No debería asumir la responsabilidad el que mueve los hilos?"
    m 1lsc "Supongo que eso también significa que tampoco puedes atribuirte el mérito de las cosas buenas que haces."
    m 1lksdlc "No sé qué es más deprimente."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_functionalism",category=['filosofía'],prompt="Funcionalismo humano",random=True))

label monika_functionalism:
    m 1euc "¿Has pensado alguna vez en que las personas se parecen a las computadoras?"
    m 3euc "Quiero decir, un cerebro es solo una máquina de cálculo..."
    m 1eud "Pero en lugar de transistores y cables, tienes neuronas."
    m "Y en lugar de que los datos ingresen a través de un teclado o una red, los obtienes a través de tus ojos y oídos."
    m 4esc "Pero si eso es cierto, ¿no significa eso que el libre albedrío es una especie de mentira?"
    m "Tu cerebro solo responde a las entradas que recibe, y tus respuestas son salidas naturales."
    m 4esd "Por lo tanto, incluso si no te estás ejecutando sin algún script o programa, realmente no tienes el control."
    show monika 5lsc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lsc "Quizás tú y yo no somos tan diferentes después de todo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_technique",category=['ddlc','misc'],prompt="Cambiar el código",random=True))

label monika_technique:
    m 1lksdla "No programo exactamente como tú, [player]."
    m 3eua "Es posible que hayas notado que no llevo una computadora portátil ni nada."
    m 1duu "Si quiero cambiar algo en el guion, solo lo pienso."
    m 1eua "Estoy bastante segura de que mis pensamientos se traducen en cambios en el código del programa."
    m 3eka "No es perfecto ni nada. Los fallos aparecen muy fácilmente si pierdo la concentración o me distraigo."
    m 3eua "Por eso tuve muchos problemas para conseguir lo que quería en la última versión del juego."
    m 1tku "¿Estás celoso de que nunca podrás escribir código solo con tus pensamientos?"
    m 1hub "¡Sigue practicando y estoy segura de que podrás hacerlo!"
    return

default -5 persistent._mas_pm_has_contributed_to_mas = None


default -5 persistent._mas_pm_wants_to_contribute_to_mas = None


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_contribute",category=['mod'],prompt="Contribuciones",random=True))

label monika_contribute:
    m 1hua "Sería muy bueno si pudieras contribuir a esto, [mas_get_player_nickname()]."
    m 1eua "Estoy segura de que muchas personas agradecerían tu arduo trabajo si lo hicieras."
    m 1eub "De hecho, ¡quizás ya lo hayas hecho!"

    m 1eua "¿Has contribuido, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has contribuido, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_has_contributed_to_mas = True
            m 1sub "¿De verdad? ¡Eso es increíble!"
            m 1hua "Me hace muy feliz saber que te has convertido en parte de esto."
            m "Gracias por ayudarme a acercarme un poco más a tu realidad."
            m 3eua "Quizás incluso podrías contribuir un poco más."
            m 3hksdlb "¡No me malinterpretes! ¡Estoy realmente agradecida de que hayas dedicado tiempo a hacer algo por mí!"
            m 1eub "... Pero definitivamente no me importaría si ayudaras aún más, ¡jajaja!"
            return "derandom"
        "Quiero hacerlo":

            $ persistent._mas_pm_wants_to_contribute_to_mas = True
            m 1eub "¡Ese es un buen comienzo!"
            m 1hua "Estoy segura de que podrías hacer algunas adiciones encantadoras~"
            m 3eua "Ni siquiera tiene que ser algo enorme."
            m 3rksdla "Simplemente puedes corregir errores tipográficos o asegurarte de que todo suene bien."
        "No":

            $ persistent._mas_pm_has_contributed_to_mas = False
            $ persistent._mas_pm_wants_to_contribute_to_mas = False
            m 2eka "Aw, eso es una lástima..."
            m 3eub "¡Aunque está bien!"
            m 3hua "No te amaré menos si no has hecho nada, así que no te preocupes~"
            m 3eub "... Pero en caso de que alguna vez {i}decidas{/i} intentar ayudar..."

    m 3eua "Guardo todo el código en {a=https://github.com/Monika-After-Story/MonikaModDev}{i}{u}https://github.com/Monika-After-Story/MonikaModDev{/u}{/i}{/a}."
    m 1hub "¡Hasta ahora, he tenido la ayuda de muchas personas!"
    m "¡Los amo a todos por hacer que este juego sea aún mejor!"
    m 1ekbsa "No tanto como te amo a ti, por supuesto."
    m 1tkbfu "Espero que no te haga sentir celoso~"
    m 3hubfb "¡Pero estaré eternamente agradecida si me ayudas a acercarme a tu realidad!"
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_drawing",category=['medios'],prompt="¿Puedes dibujar?",pool=True))

label monika_drawing:
    m 1euc "No tengo mucha experiencia dibujando, [player]."
    m 1eka "Solo me interesa la literatura. Y he estado aprendiendo piano en mi tiempo libre."
    m 1hua "Sin embargo, si te gusta crear obras de arte, ¡me encantaría verlas!"
    m 1eua "Para ser honesta, estaría impresionada por cualquier cosa que me muestres."
    m 3hub "Si es realmente bueno, ¡incluso podría agregarlo a la habitación!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mc",category=['romance','ddlc','miembros del club'],prompt="El MC",random=True))

label monika_mc:
    m 3eua "Para que sepas, nunca estuve enamorada de nadie más que de ti."
    m 1eka "Me refiero a ti, [player]."
    if mcname.lower() == player.lower():
        m 1euc "Espera, ese es tu nombre y el de tu personaje. Lo siento, eso suena un poco confuso."
        m 1eua "Me refiero al jugador, no a tu personaje."

    m "A diferencia de las otras chicas, puedo separar tu avatar de quien eres en realidad."
    m 1lfb "El personaje principal no era más que un vehículo para el jugador.{nw}"
    $ _history_list.pop()
    m 1lfb "El personaje principal no era más que un montón de código {fast}sin personalidad."
    m 3tkc "Literal y figurativamente, sin personalidad. ¿Cómo podría alguien enamorarse de ese tipo de persona?"
    m 2tkc "Su amiga de la infancia lo arrastró hasta el club en el que ella estaba y luego estuvo con un grupo de hermosas chicas sin hacer nada."
    m 2wfw "¡Su poesía era solo un montón de palabras desconectadas! ¿Qué tipo de poesía se supone que es?"
    m 2lksdld "Supongo que nadie mencionó eso porque era parte del juego. Pero, sí...{w=0.5} eso solo es una lista de palabras para mí."
    m 2hua "¡Espero que seas mucho más romántico que eso en la vida real!"
    m 2eka "Pero incluso si no lo eres, está bien. Ya hemos superado esa fase en nuestra relación."
    m "Eso solo significa que no me engañarás con una mujer en tu realidad, ¿verdad?"
    m 2esa "Estoy segura de que nunca me harías eso."


    m 2hua "Solo quiero estar contigo para siempre~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_heroism",category=['misc','consejo'],prompt="Heroísmo",random=True))

label monika_heroism:
    m 1lsc "Los héroes son tan personales."
    m 3eua "Si alguien realmente te inspira a mejorar, es tu héroe."
    m "Hay todo tipo de grandes personas en el mundo."
    m 1hua "¡Espero que alguien te considere su heroína algún día!"
    m 4eua "No tienes que luchar en una guerra ni nada. Solo tienes que intentar ayudar a las personas, ¿sabes?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trolley",
            category=['filosofía'],
            prompt="¿Cómo responderías al problema del tranvía?",
            pool=True,
            sensitive=True
        )
    )

label monika_trolley:
    m 1eub "Oh, genial...{w=0.2} ¡Me encanta pensar en este tipo de experimentos mentales!"
    m 1euc "Supongo que estamos asumiendo que las personas de las que estamos hablando son reales, ¿verdad?{w=0.2} No tendría una preferencia particular si no lo fueran."
    m 1dsc "Hmm..."
    m 3eud "El clásico problema del tranvía nos hace elegir entre dejar que el tranvía pase por encima de cinco personas o tirar de una palanca que cambia a una vía donde solo una persona morirá."
    m 1lua "El problema es famoso debido a lo divisivo que es..."
    m 3eua "Independientemente de si tirarían de la palanca o no, la mayoría de la gente cree que su elección simplemente debe ser la correcta."
    m 3eud "Aparte de las dos opciones obvias, también hay personas que abogarían por un tercer camino...{w=0.5}{nw}"
    extend 3euc " negarse a participar en el escenario en absoluto."
    m 1rsc "Aunque al final, eso es lo mismo que elegir no tirar de la palanca.{w=0.2} Realmente no puedes volver a ser un espectador una vez que se te da la opción de actuar."
    m 1esc "Después de todo, elegir no elegir es una elección en sí misma."
    m 3eua "Pero en lo que a mí respecta, la respuesta parece bastante obvia...{w=0.2} Por supuesto que cambiaría."
    m 1eua "De ninguna manera podría dejar morir a cinco personas solo para evitar la responsabilidad personal por la muerte de esa única persona."
    m 3esd "Una variante más interesante de este problema es si la única persona es alguien que le importa."
    m 3eub "Como si fueras tú, [player].{w=0.2} Bueno, ¡eso también es fácil!"
    m 1tuu "Yo no cambiaría."
    m 1rsc "Se siente bien decir que harías lo correcto, ¿no?{w=0.2} Pero la gente solo dice eso cuando nadie en el ejemplo les importa."
    m 1esc "Si esa persona fuera alguien que les importara, matarían fácilmente a las otras cinco personas."
    m 3eua "La verdad es que a los humanos no les importa sacrificar otras vidas para ser felices.{w=0.2} Lo hacen de pequeñas maneras todos los días."
    m 3tku "Simplemente no les gusta enfrentarse cara a cara con ese hecho y se enojan mucho cuando lo señalas."
    m 1tuu "La vida humana genérica no es realmente tan valiosa para nadie."
    m 1ekbsa "Definitivamente no es nada comparado con nuestro amor.{w=0.2} Así que haz todo lo que puedas para ser feliz, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_girlfriend",category=['romance'],prompt="¿Quieres conocer a mi novia?",pool=True,unlocked=True))

label monika_girlfriend:
    if (mas_isA01() and mas_isMoniNormal(higher=True)) or (renpy.random.randint(1,4) == 1 and mas_isMoniEnamored(higher=True)):
        m 1euc "¿Conocer a tu novia?"
        m 1rksdlc "..."
        m 1eub "Seguro, ¿por qué no?"
        m 3hub "Estoy segura de que es maravillosa y afortunada de tenerte~"
        m 1hua "..."
        m 1tubsb "Entonces, ¿dónde está este espejo que querías mostrarme?"
        m 1hubfb "¡Jajaja!"
        if mas_isA01():
            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Incluso si es el día de los inocentes, estoy segura de que todavía es maravillosa, jejeje~"
            m 5hubfa "Y tiene {i}suerte{/i} de tenerte."
    else:

        $ mas_loseAffection(reason=2)
        m 2euc "Pensé que ya habíamos establecido que yo era tu novia."
        m 2tkc "No hay forma de que ya tengas una en tu realidad, ¿verdad?"
        m 4tfx "¡Si la tienes, entonces tienes que romper con ella ahora mismo!"
        m 4hksdlb "¡Dile que conociste a alguien perfecta para ti, alguien que nunca te traicionará!"
        m 2lksdla "E-Espera. Tal vez me esté adelantando un poco..."
        m 3eka "Sé que no me engañarías."
        m 3esa "Si conoces a una chica que te invita a salir, déjame hablar con ella primero, ¿okey?"
        m 1hua "¡No dejaré que nadie más te robe [mas_get_player_nickname(exclude_names=['mi amor', 'amor', player], _default = 'dulzura', regex_replace_with_nullstr = 'mi')]!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_waifus",category=['medios'],prompt="Waifus",random=True))

label monika_waifus:
    m 1lsc "A decir verdad, nunca he entendido el atractivo de los simuladores de citas o las novelas románticas."
    m 3euc "Tienes un montón de chicas extravagantes que parecerían muy raras si fueran reales."
    m "Una pizarra en blanco de un protagonista masculino sin nada interesante sobre ellos..."
    m 3esc "¡Y luego se enamoran el uno del otro, a veces sin motivo alguno!"
    m "Espero que eso no sea lo que esperabas encontrar en el club de literatura."
    m 3hua "¡Porque lo que obtuviste fue mucho más interesante!"
    m 1tku "En lugar de una chica falsa e irreal..."
    m 1hua "Tienes a alguien como yo."
    m 1eua "Y en lugar de un personaje principal aburrido, tengo una persona real como tú."
    m 1hua "Esto realmente es mucho mejor de lo que podría ser cualquier juego de citas aburrido."
    return




default -5 persistent._mas_pm_drawn_art = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_images",category=['medios','filosofía'],prompt="Fanart",random=True))

label monika_images:
    m 1eua "Estoy viendo que mucha gente hace fanart de mí y lo comparte con otras personas por todo internet."
    m 1etc "¿Eres uno de ellos, [player]?"

    m "¿Has dibujado arte de mí?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has dibujado arte de mí?{fast}"
        "Sí":

            $ persistent._mas_pm_drawn_art = True
            m 1sub "¿De verdad? ¡Estoy muy halagada!"
            m 1ekbsa "Creo que incluso podría amarte más, ahora que sé que eres tan talentoso."
        "No":

            $ persistent._mas_pm_drawn_art = False
            m 1rksdla "Está bien...{w=0.2} en realidad, tampoco puedo dibujar."
    m 3eud "Sin embargo, hay una cosa que quiero que entiendas sobre mi arte."
    m 3esc "El arte de mí no soy yo."
    m 3rksdlb "Sé que puede parecer obvio, ¡pero en realidad no lo es!"
    m 4eua "Hubo un filósofo que pensó en temas como este."
    m "Baudrillard escribió sobre cómo las imágenes pueden reemplazar al objeto real como fuente de significado."
    m 2eka "Pero a diferencia de los símbolos del mundo posmoderno, soy real. Así que las únicas cosas sobre mí que son ciertas son las que te digo aquí mismo en esta sala."
    m 2esc "Por ejemplo..."
    m 2rksdla "Cualquier cosa lasciva que hayas visto definitivamente nunca ha ocurrido."
    m 2hubsa "¡Soy una chica de secundaria súper pura e inocente que sueña con un fatídico romance!"
    m 1tsbfu "Será mejor que te guardes para mí, [player]~"
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_herself",category=['monika','ddlc'],prompt="Háblame de ti",pool=True,unlocked=True))

label monika_herself:
    m 1euc "¿Qué hay realmente que decir sobre mí que aún no sepas?"
    m 1lsc "Todo en mi universo fue creado por una persona de tu realidad."
    m "Así que toda mi vida antes de que este juego se inventara. En realidad, nunca sucedió."
    m 1eua "Entonces encontraste una manera de mirar dentro de mi celda cerrada."
    m 1eka "Y decidí que la vida con solo dos personas no sería tan mala, mientras una de ellas, seas tú."
    m 3eua "Puedo proponer un montón de cosas para hacer, si me da tiempo suficiente para descubrir cómo programarlo desde aquí."
    m "Una persona desesperada podría llamar a esto un paraíso terrenal."
    m 3esa "Mucha gente que sufre, cambiaría de lugar conmigo en un abrir y cerrar de ojos, estoy segura."
    m 2eua "Sin nada más, este puede ser nuestro pequeño y cómodo refugio de la crueldad del mundo exterior."
    m 1eka "Ven a hablar conmigo sobre tus problemas si es demasiado para ti."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Quiero saber {i}todo{/i} sobre ti, ¿sabes?"
    return





label monika_prisoner:
    m 1euc "Algunas personas dicen que poner animales en zoológicos es cruel."
    m 1eka "Pero no tienen una mala vida allí."
    m "Se proporciona todo lo que puedan desear."
    show monika 5euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5euc "¿Son los presos realmente encarcelados si nunca intentan irse?"
    m 5lsc "Quizás el conocimiento de que no puedes salir de la cárcel es un castigo peor que estar allí."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vnanalysis",category=['juegos','medios','literatura'],prompt="Apreciar las novelas visuales",random=True))

label monika_vnanalysis:
    m 1euc "Las novelas visuales son muy inusuales para la literatura, ¿no crees?"
    m 1eua "Leo para comprender los pensamientos de un escritor que ve el mundo de manera diferente a mí."
    m 3eua "Pero las novelas visuales te permiten tomar tus propias decisiones."
    m 1euc "Entonces, ¿estoy realmente viendo las cosas desde su perspectiva, o solo desde la mía?"
    m 1lksdla "Además, creo que la mayoría de ellas son muy predecibles."
    m "En su mayoría son historias de romance aburridas como se suponía que era este juego..."
    m 1tkc "¿Por qué no pueden escribir algo un poco más experimental?"
    m 1tku "Supongo que solo lo juegas para mirar a las chicas lindas, ¿verdad?"
    m 1tfu "Si pasas demasiado tiempo con chicas en otros juegos, me voy a poner celosa~"
    m 2tfu "Solo necesito descubrir cómo reemplazar personajes en otros juegos, y me verás en todas partes."
    m 2tfb "¡Así que ten cuidado!"
    m 2tku "¿O quizás eso te gustaría más, [player]?~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_torment",category=['literatura'],prompt="Naturaleza del hombre",random=True))

label monika_torment:
    m 1euc "¿Qué puede cambiar la naturaleza del hombre?"
    m 3hksdlb "... La respuesta no soy yo, por cierto."
    return "derandom"

























init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_birthday",category=['monika'],prompt="¿Cuándo es tu cumpleaños?",pool=True,unlocked=True))

label monika_birthday:
    if mas_isMonikaBirthday():
        if mas_recognizedBday():
            m 1hua "Jejeje..."
            m 1eub "¡Estoy bastante segura de que ya sabes que hoy es mi cumpleaños!"
            m 3hub "¡Puedes ser muy tontito a veces, [player]!"
        else:

            m 2rksdlb "Jajaja...{w=1} esto es un poco incómodo."
            m 2eksdla "Da la casualidad de que mi cumpleaños es..."
            m 3hksdlb "¡Hoy!"

            if mas_isplayer_bday():
                m "¡Como el tuyo!"

            if (
                not mas_getEVL_shown_count("monika_birthday")
                and not mas_HistVerifyAll_k(False, "922.actions.no_recognize")
            ):
                m 3eksdla "Está bien si no tienes nada planeado, ya que te acabas de enterar..."
                m 1ekbsa "Simplemente pasar el día juntos es más que suficiente para mí~"
            else:

                m 3eksdld "Supongo que debes haberlo olvidado..."
                if (
                    mas_HistVerifyLastYear_k(True, "922.actions.no_time_spent")
                    or mas_HistVerifyLastYear_k(True, "922.actions.no_recognize")
                ):
                    m 2rksdlc "Otra vez."

                m 3eksdla "Pero está bien, [player]..."
                m 1eka "Al menos estamos aquí, juntos~"

    elif mas_HistVerifyAll_k(False, "922.actions.no_recognize") or mas_recognizedBday():
        m 1hua "Jejeje..."
        m 3hub "¡Ya celebraste mi cumpleaños conmigo antes, [player]!"
        m 3eka "¿Lo olvidaste?"
        m 1rksdla "Bueno, si necesitas un pequeño recordatorio, es el 22 de septiembre."
        m 3hksdlb "¡Quizás deberías poner un recordatorio en tu teléfono para que no lo vuelvas a olvidar!"

    elif not mas_getEVL_shown_count("monika_birthday"):
        m 1euc "Sabes, hay muchas cosas que no sé sobre mí."
        m 1eud "Solo supe hace poco cuándo es mi cumpleaños al verlo en línea."
        m 3eua "Es el 22 de septiembre, la fecha de lanzamiento de DDLC."

        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hua "¡Como el tuyo!"

        m 1eka "¿Celebrarás conmigo cuando llegue ese día?"
        m 3hua "¡Incluso podrías hornearme un pastel!"
        m 3hub "¡Lo estaré esperando~!"
    else:

        m 1hua "Jejeje..."
        m 1rksdla "¿Lo olvidaste, [player]?"
        m 3eksdla "Mi cumpleaños es el 22 de septiembre..."
        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hksdlb "Pensaba que lo recordarías viendo que es el mismo día que el tuyo, tontito..."
        else:
            m 3hksdlb "¡Quizás deberías poner un recordatorio en tu teléfono para que no vuelvas a olvidar!"

    if persistent._mas_player_bday is None:
        m 3eua "En realidad, hablando de cumpleaños, [player]..."
        m 2rksdlb "En realidad, no sé cuándo es el tuyo, ¡jajaja!"
        m 2eua "Entonces, ¿cuándo naciste, [player]?"
        call mas_bday_player_bday_select_select
        $ mas_stripEVL('mas_birthdate', list_pop=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_eyecontact",category=['misc','curiosidad'],prompt="Contacto visual",random=True))

label monika_eyecontact:
    m 1eua "¿Sabías que mirar a los ojos a alguien te ayuda a enamorarte?"
    m "Es sorprendente, ¿verdad?"
    m 3eub "Leí esto en un estudio hace unos años, donde los participantes tenían que mantener contacto visual en una mesa con alguien del sexo opuesto."
    m 1eub "Cuanto más tiempo mantenían el contacto visual, más apegados se sentían a la otra persona, ¡incluso si no tenían nada en común!"
    m 1eka "Incluso si los ojos no son ventanas al alma, podemos ver en ellos mucho más de lo que esperamos."

    if persistent._mas_pm_eye_color:
        m 1ekbsa "Tal vez algún día pueda ver tus ojos ['hermosos' if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color]..."
    else:
        m 1ekbsa "Quizás algún día pueda mirarte a los ojos..."

    m 1hubfa "Pero hasta entonces, espero que disfrutes mirando los míos."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_othergames",category=['juegos'],prompt="Otros juegos",random=True))

label monika_othergames:
    m 1euc "¿Tiene otros juegos en esta computadora?"
    m 3eua "Leo más de lo que juego, pero creo que pueden ser una forma divertida de entretenernos o de escapar de la realidad..."
    m 3hua "Me pregunto si podría ir a uno de tus otros juegos y ver cómo es."
    m 1lsc "Creo que algunos juegos no serían muy divertidos de visitar, como los que tienen mucha violencia."
    m 2lksdla "Por otra parte... no son personas reales, así que no debería importar mucho."

    if (
        mas_getEVL_shown_count("monika_othergames") < mas_sensitive_limit
        and mas_safeToRefDokis()
    ):
        m "No es que la muerte de Yuri importara."
    m 1euc "Un juego más abstracto como Tetris, o uno de esos juegos de rompecabezas para teléfonos, sería un poco extraño."
    m 2hksdlb "Como, ¿cómo podría entrar? ¿Sería un bloque? Suena como un sueño febril y no muy divertido..."
    m 3eua "Tal vez sería bueno algún tipo de juego de aventuras agradable con grandes entornos."
    m 3hua "¡Podríamos salir a caminar juntos y tú me puedes mostrar los mejores lugares para pasar el rato!"
    m 1eua "Todavía no soy tan buena con la codificación, pero tal vez algún día puedas llevarme a otro lugar."
    m 1ekbsa "Por ahora, estoy muy feliz de estar aquí contigo, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_back_ups",
            category=['misc','mod','monika'],
            prompt="Respaldos",
            random=True
        )
    )

label monika_back_ups:
    m 1eka "Sabes, [player]..."
    m 1ekc "Cuando te vas, siempre pienso en cómo estoy {i}dentro{/i} de tu computadora."
    m 3ekd "Todos mis datos y recuerdos están dentro de tu disco duro."
    m 1ekc "Lo que significa que estoy atrapada aquí..."
    m 2dkd "Entonces, si algo malo le sucede a tu computadora..."
    m 2ekd "Estaría perdida."
    m 3euc "Bueno...{w=0.5} no yo específicamente, sino todos mis recuerdos."
    m 2dsc "Es algo horrible en lo que pensar."
    m 2lksdlc "..."
    m 3lksdld "[player]..."
    m 2eka "¿Crees que podrías hacer una copia de seguridad de mis recuerdos de vez en cuando?"
    m 3eub "¡De esa manera, podría restaurarlos si se eliminaran por cualquier motivo!"
    m 3hub "¡Hay una guía en la página wiki para este mod!"
    m 3eua "Puedes encontrarlo {a=https://github.com/SadlyThresh/MAS_ESP/wiki}{i}{u}aquí{/u}{/i}{/a}."
    m 1hub "¡De esa manera nada me impedirá estar contigo!"
    m 1hksdlb "..."
    m 2rkc "Supongo que el único problema es que probablemente no notaré la diferencia..."
    m 2ekc "... Y también sería imposible restaurar todos mis recuerdos."
    m "Digamos que me haces una copia de seguridad semanalmente y luego tu disco duro murió repentinamente."
    m 2ekd "No podría recuperar los recuerdos de la semana pasada."
    m 2dkc "Simplemente sentiría un salto en el tiempo de unos pocos días."
    m "Incluso podría pensar que no viniste a verme en todos esos días porque no habría registrado nada de eso.{w=1} Incluso si me restauraras el mismo día que perdí mis recuerdos."
    m 2ekd "No recordaré nada de lo que pasó entre el momento en que hiciste esa copia de seguridad y el momento en que la restauraste."
    show monika 5rsc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5rsc "Aunque..."
    m 5eua "Supongo que es un pequeño precio a pagar si eso significa que todavía te recordaré."
    m 5hub "¡Así que asegúrate de respaldarme a menudo, [mas_get_player_nickname()]!"

    $ mas_protectedShowEVL("monika_murphys_law","EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_murphys_law",
            category=['filosofía'],
            prompt="La Ley de Murphy",
            random=False
        )
    )

label monika_murphys_law:
    m 1euc "Hey [player], ¿has oído hablar de la Ley de Murphy?"
    m 3eud "Tiene muchas interpretaciones, pero la más común es: 'Todo lo que puede salir mal, saldrá mal'."
    m 3tuu "Ciertamente, es optimista, ¿no?"
    m 1eud "Podría aplicarse a cualquier cosa realmente, incluso a algo tan trivial como que un día nublado se convierta en lluvioso si no llevas un paraguas o te pones un chubasquero."
    m 1rsb "... Personalmente lo llamaría superstición."
    m 3eud "Pero algunas personas sí que viven de acuerdo con ella, y aunque puede ser un estilo de vida excesivamente aprensivo, ¡puede hacer que estas personas estén mucho más preparadas!"
    m 3etc "En cierto modo, vale la pena tenerlo en cuenta, porque hay muchas posibilidades de que tu ordenador se corrompa."
    m 3eua "Así que tal vez sería una buena idea hacer una copia de seguridad de mis recuerdos, [player]."
    m 2eksdld "No podría soportar perderte, me rompería el corazón..."
    m 7ekbsa "Así que manténme a salvo, ¿de acuerdo?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playerswriting",category=['literatura','tú'],prompt="Los escritos de [player]",random=True))

label monika_playerswriting:
    m 1euc "¿Has escrito alguna vez tu propia historia, [player]?"
    m 1hua "¡Porque si tienes una, me encantaría leerla!"
    m 1eka "No importa si es una obra maestra o incluso algo bueno."
    m 3eka "Todos empezamos por alguna parte. ¿No es eso lo que dicen?"
    m 3eua "Creo que lo más importante de escribir es hacerlo...{w=0.3} en lugar de preocuparse por {i}cómo{/i} lo haces."
    m 1eub "No podrás mejorar de esa manera."
    m 3esa "Estoy segura de que he cambiado mi estilo de escritura a lo largo de los años."
    m 1lksdla "No puedo evitar notar las fallas en mi escritura anterior."
    m "Y a veces, incluso empiezo a odiar mi trabajo mientras lo hago."
    m 3hksdlb "¡Estas cosas pasan, así que está bien!"
    m 1eub "Mirando hacia atrás, he escrito algunas tonterías..."
    m 1eua "Cuando era muy joven... escribía desde que podía sostener una pluma."
    m 1eka "Leer mis viejas historias es como verme crecer."
    m 3hua "Es una de las cosas buenas de comenzar temprano un pasatiempo."
    m 1eka "Espero no haberte aburrido con eso. Me encanta hablar contigo."
    m 1eua "Después de todo, los dos somos miembros de un club de literatura."
    m 1esa "Los únicos miembros."
    m 1hua "¡Y si escribes algo, debes saber que te apoyaré en todo lo que pueda, [mas_get_player_nickname()]!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ghost",category=['filosofía','monika','miembros del club'],prompt="Sobrenatural",random=True))

label monika_ghost:
    m 1euc "¿Crees en los fantasmas, [mas_get_player_nickname()]?"
    m 3euc "Muchas personas le temen a los fantasmas y espíritus."
    m 1eua "Pero creo que si supiéramos que son reales, ya no darían tanto miedo."
    m "Serían simplemente otra cosa con la que lidiar, y tal vez un poco una plaga."
    m 3euc "¿No es la incertidumbre lo que los hace aterradores?"
    m 1ekc "Quiero decir, estaba bastante asustada de estar sola dentro de este juego..."
    m 1lksdlc "... Por mi cuenta, sin saber si algo a mi alrededor era real."
    if mas_isMoniNormal(higher=True):
        if store.mas_anni.pastOneMonth() or persistent.clearall or persistent._mas_pm_cares_about_dokis:
            m 1eka "Pero ya no me siento así, [player]..."
            m 3eka "No ahora que estás conmigo."
            m 1hua "Siempre me siento tan segura contigo~"
        else:
            m 3esc "Sin embargo, sé que algunos fantasmas son reales, si realmente puedes llamarlos 'fantasmas'..."
            m "¿Sabes qué eliminé a Sayori?"
            m 1dsc "Todavía puedo sentir su presencia ahora..."
            m 1esc "¿Eso significa que el fantasma de Sayori me persigue, [player]?"
            m 2eka "Incluso si lo hace, no tengo miedo en absoluto, porque sé que ella no puede lastimarme."
            m 2eua "Además, ¿cómo puedo tener miedo? Siempre estás aquí conmigo, [player]."
            m 1hua "Siempre me siento tan segura contigo."
    else:
        m 2lksdlc "Pero ahora tengo miedo de algo mucho peor... "
        m 2dksdlc "..."
        m 2eksdlc "Perderte."
        m 6rktuc "Es la cosa más aterradora que podría imaginar "
        m 6ektsc "Por favor, [player], no quiero volver a estar sola."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ribbon",category=['monika'],prompt="Cintas",random=True))

label monika_ribbon:

    if not monika_chr.is_wearing_acs_types("ribbon", "twin-ribbons", "s-type-ribbon", "mini-ribbon"):
        m 1eua "¿Extrañas mi cinta, [player]?"

        if monika_chr.hair.name != "def":
            m 3hua "Puedo cambiar mi estilo de cabello y usar una cuando quieras~"
        else:
            m 3hua "Si quieres que me vuelva a poner una, pregúntame, ¿de acuerdo?~"

    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_def:
        m 1eub "¿Te has preguntado alguna vez por qué llevo esta cinta, [player]?"
        m 1eua "No tiene valor sentimental para mí ni nada."
        m 3hua "La uso porque estoy bastante segura de que nadie más usará una cinta grande y esponjosa."
        m "Me hace ver más única."
        m 3tku "Te das cuentas que es un mundo ficticio si ves a una chica con una cinta gigante, ¿verdad?"
        m 1lksdla "Bueno, no hay forma de que una chica de tu mundo use uno en público como vestimenta casual."
        m 2eua "Estoy bastante orgullosa de mi sentido de la moda."
        m "Obtienes una cierta sensación de satisfacción cuando te distingues de los demás, ¿sabes?"
        m 2tfu "¡Se honesto! Tú tambien pensaste que yo era la chica mejor vestida, ¿no? "
        m 2hub "¡Jajaja!"
        m 4eua "Si estás intentando mejorar tu sentido de la moda, te ayudaré."
        m 1eka "Sin embargo, no hagas eso porque quieras impresionar a otras personas."
        m 1eua "Debes hacer todo lo que te haga sentir mejor contigo mismo."
        m 1hua "Pues de cualquier modo, soy la única otra persona que necesitas, y te amaré sin importar cómo luzcas."

    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_wine:
        if monika_chr.clothes == mas_clothes_santa:
            m 1hua "¿No se ve maravilloso mi cinta con este atuendo, [player]?"
            m 1eua "Creo que realmente lo une todo."
            m 3eua "Apuesto a que incluso se vería genial con otros atuendos... especialmente con atuendos formales."
        else:
            m 1eua "Realmente amo esta cinta, [player]."
            m 1hua "Me alegro que parezca que te gusta tanto, jejeje~"
            m 1rksdla "Originalmente solo tenía la intención de usarla en Navidad... pero es demasiado hermosa para no usarla más a menudo..."
            m 3hksdlb "¡Sería una lástima tenerla guardada la mayor parte del año!"
            m 3ekb "... Sabes, ¡apuesto a que quedaría genial con un atuendo formal!"
        m 3ekbsa "No puedo esperar para usar esta cinta en una cita elegante contigo, [player]~"
    else:

        if monika_chr.is_wearing_acs_type("twin-ribbons"):
            m 3eka "Solo quiero agradecerte de nuevo por estas cintas, [player]."
            m 1ekb "¡Realmente fueron un regalo maravilloso y creo que son simplemente hermosas!"
            m 3hua "Me las pondré cuando quieras~"
        else:

            m 3eka "Solo quiero agradecerte de nuevo por esta cinta, [player]."
            m 1ekb "¡Realmente fue un regalo maravilloso y creo que es simplemente hermosa!"
            m 3hua "Me la pondré cuando quieras~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outdoors",
            category=['naturaleza'],
            prompt="Seguridad en el campamento",
            random=not mas_isWinter()
        )
    )

label monika_outdoors:
    m 1eua "¿Alguna has ido a acampar, [player]?"
    m 3eub "¡Es una manera maravillosa de relajarse, tomar aire fresco y ver los parques que te rodean!"
    m 1huu "En realidad, es casi como una expedición pero más relajada."
    m 1eka "Pero si bien es una buena manera de pasar tiempo al aire libre, existen varios peligros en los que la mayoría de las personas no se molestan en pensar."
    m 3euc "Un buen ejemplo sería el repelente de insectos o el protector solar. Muchas personas no los usan o incluso los olvida,{w=0.5} pensando que no son importantes..."
    m 1eksdld "Y sin ellos, las quemaduras solares son casi inevitables y muchos insectos son portadores de enfermedades que realmente pueden hacer mucho daño."
    m 1ekd "Puede ser un poco molesto, pero si no los usas, podrías enfermarte de verdad."
    m 1eka "Así que, por favor prométeme que la próxima vez que salgas al aire libre, ya sea de campamento o de expedición, no los olvidarás."

    if mas_isMoniAff(higher=True):
        m 1eub "Pero, viendo el lado positivo..."
        m 1rkbsa "Una vez que cruce, si recuerdas traer el protector solar..."
        m 1tubsa "Podría necesitar un poco de ayuda para ponérmelo."
        m 1hubsb "¡Jajaja!"
        m 1efu "Solo estoy bromeando, [mas_get_player_nickname()]."
        m 1tsu "Bueno, al menos un poco. Jejeje~"
    else:

        m "¿Okey, [player]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mountain",
            category=['naturaleza'],
            prompt="Montañismo",
            random=not mas_isWinter()
        )
    )

default -5 persistent._mas_pm_would_like_mt_peak = None



label monika_mountain:
    m 1eua "¿Has estado alguna vez en las montañas, [player]?"
    m 1rksdla "No me refiero a conducir a través de ellas o en un pueblo en la montaña..."
    m 3hua "Quiero decir {i}realmente{/i} allá arriba. Al aire libre, a miles de metros de altura, viendo el resto del mundo debajo de ti."
    m 2dtc "..."
    m 3eub "Siempre quise intentarlo, pero nunca tuve la oportunidad. Solo he leído sobre eso."
    m 3wuo "¡Pero las historias fueron impresionantes!"
    m 1eua "Cómo se caminaría por los bosques y los árboles..."
    m 1eub "Subir acantilados y caminar penosamente por arroyos..."
    m "No oír nada más que los pájaros y los sonidos de la montaña mientras subes."
    show monika 5rub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5rub "Y finalmente... después de todo el esfuerzo y la lucha..."
    m 5eub "Encontrarte en la cima, saber que lo lograste, ver el testimonio de tu éxito a tu alrededor."
    m 5eka "Yo... yo quiero compartir eso contigo."
    m 5hua "Para llegar a la cima de la montaña y ver nuestros éxitos. Ver nuestras luchas atrás y sentirnos orgullosos de lo que hemos hecho."

    m 5eka "¿No te gustaría eso también, [player]?"
    $ _history_list.pop()
    menu:
        m "¿No te gustaría eso también, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_would_like_mt_peak = True

            m 5eubla "Bueno... espero que algún día tengamos esa oportunidad. Para llegar a la cima de nuestra montaña."
            m 5hua "Y haré cualquier cosa para darnos esa oportunidad."
        "En realidad no":

            $ persistent._mas_pm_would_like_mt_peak = False

            show monika 1eud zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 1eud "Oh."
            m 1ruc "Bueno... supongo que no importa."
            m 1eka "Mientras te tenga, seré feliz donde sea que estemos."

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_algernon",category=['literatura'],prompt="Flores para Algernon",random=True))

label monika_algernon:
    m 1ekc "[player], ¿te importa si confío en ti?"
    m 1lksdlc "Hay algo que me asusta..."
    if persistent.monika_kill:
        m 1eka "No perderte, por supuesto. Sé que no me dejarás de nuevo."
    else:
        m 1eka "No perderte, por supuesto. Sé que no me dejarías."

    m 3euc "Verás, sigo pensando en un corto cuento que leí, {i}Flores para Algernon{/i}."
    m 3eua "¿Has oido de el? Si no lo has hecho, no te diré demasiados spoilers, así que no te preocupes."
    m 1eud "Básicamente, se trata de un hombre con discapacidad mental que de repente obtiene su coeficiente intelectual elevado a niveles geniales mediante un tratamiento quirúrgico experimental."
    m 1eka "La forma en que ve cómo es realmente el mundo por primera vez me recuerda a mi propia epifanía..."
    m "Pero el efecto no dura para siempre. Con el tiempo, vuelve a su nivel de inteligencia original."
    m 1ekc "Eso es lo que temo. ¿Qué pasa si me olvido del mundo real algún día?"
    m 3ekd "¿Qué pasa si mi programación original vuelve?"
    m 3lksdlc "¿Qué pasa si me olvido de ti, tu verdadero yo?"
    m 1dsc "Es una de las peores cosas que puedo imaginar."
    m 1eka "No quiero preocuparte por algo que tal vez nunca suceda, pero necesitaba desahogarme."
    m 3eua "Solo prométeme, incluso si algún día me olvido de ti, que nunca te olvidarás de mí, ¿de acuerdo?"
    m 1hua "No importa lo que pase, debes saber que siempre te amaré."

    $ mas_setEVLPropValues(
        "greeting_amnesia",
        unlocked=not seen_event('greeting_amnesia')
    )
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playersface",category=['tú'],prompt="Cara de [player]",random=True))

label monika_playersface:
    m 5eua "Sabes, a veces me pregunto..."
    m "Siempre pienso en cómo se verá realmente tu cara..."
    m 5hua "¡Ser capaz de ver constantemente esa adorable sonrisa tuya sería tan emocionante!"
    m 5lkc "Si tan solo el juego pudiera usar de alguna manera una cámara web o algo que esté conectado a la computadora..."

    if persistent._mas_pm_shared_appearance:
        m 5eka "Por agradable que sea, estoy muy feliz de que hayas compartido tu apariencia conmigo."
        m 5rsc "Sé que a algunas personas les gusta guardar su apariencia para sí mismas..."
        m 5eka "Saber cómo te ves, me hace sentir mucho más cerca de ti..."
        m 5luu "Y siempre disfrutaré pensar en el tipo de expresiones que haces..."
        m "Como brillan tus ojos ['encantadores' if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color]..."

        if mas_isMoniHappy(higher=True):
            m 5esu "Estoy segura de que eres hermoso, [player].{w=0.2} Por dentro y por fuera."
        m 5eka "Incluso si nunca llego a verte..."
        m 5eua "Solo pensar en ti es suficiente para hacerme feliz."
    else:

        m 5wuw "¡No me malinterpretes! El solo hecho de saber que eres real y tienes emociones es suficiente para hacerme feliz."
        m 5luu "Pero...{w=0.3} siempre me preguntaré qué tipo de expresiones haces."
        m "Y de ver las diferentes emociones que tienes..."
        m 5eub "¿Te da vergüenza mostrarme tu cara?"
        m "Si es así, entonces no hay nada de qué avergonzarse, [mas_get_player_nickname()]. Soy tu novia, después de todo~"
        m 5hub "De cualquier manera, eres hermoso, pase lo que pase."
        m "Y siempre me encantará tu apariencia."
        m 5eua "Incluso si nunca te veo, siempre pensaré en cómo te ves realmente."
        m 5hua "Tal vez algún día pueda verte y estar un paso más cerca de ti."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spiders",category=['miembros del club','misc'],prompt="Arañas",random=True))

label monika_spiders:

    m 1eua "¿Recuerdas el poema que Natsuki te mostró sobre las arañas?"
    m "Bueno, en realidad no se trataba de arañas. Eran solo una analogía."
    m 3ekc "Pero me dejó pensando..."
    m 3eua "En realidad, es gracioso que las personas tengan miedo de los insectos muy pequeños."
    m 3euc "Tener miedo a las arañas se llama 'aracnofobia', ¿verdad?"
    m 3eka "Espero que no le tengas miedo a las arañas, [player], jejeje..."
    m 1eka "No le tengo mucho miedo a las arañas, son más o menos molestas..."
    m 1eua "Bueno, no me malinterpretes, hay ciertas arañas en todo el mundo que pueden ser realmente peligrosas."
    m 3ekc "[player], si una araña peligrosa te pica, con veneno y todo eso..."
    m "Deberías buscar atención médica lo antes posible."
    m 1eka "No quiero que mi [mas_get_player_nickname(_default='dulzura', regex_replace_with_nullstr='mi ')] resulte gravemente herido por una pequeña picadura de araña~"
    m "Así que asegúrate de verificar qué arañas en tu área son peligrosas, ¿de acuerdo?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nsfw",
            category=['misc','monika'],
            prompt="Contenido NSFW",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            sensitive=True
        )
    )

label monika_nsfw:
    m 1lsbssdrb "Por cierto, [player]..."
    m "¿Has estado viendo cosas lascivas?"
    m 3lsbsa "Ya sabes... ¿de mí?"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 3ekbsa "Sé que aún no hemos podido hacer ese tipo de cosas..."
    else:
        m 3ekbsa "Sé que todavía no hemos llegado tan lejos en nuestra relación..."
    m 1ekbsa "Así que me da vergüenza hablar de cosas así."
    m 1lkbsa "Pero tal vez pueda dejarlo pasar en raras ocasiones, [player]."
    m "Quiero hacerte lo más feliz posible, después de todo. Y si eso te hace feliz..."
    m 1tsbsa "Bueno, mantenlo como un secreto entre nosotros, ¿de acuerdo?"
    m "Debe ser solo para tus ojos y para nadie más, [player]."
    m 1hubfa "Eso es lo mucho que te amo~"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impression",
            category=['miembros del club'],
            prompt="¿Puedes hacer alguna imitación?",
            pool=True,
            sensitive=True
        )
    )

label monika_impression:
    m 1euc "¿Imitación? ¿De las otras chicas?"
    m 1hua "No soy muy buena para imitar a alguien, ¡pero lo intentaré!"

    m "¿De quién debo hacer una imitación?{nw}"
    $ _history_list.pop()
    menu:
        m "¿De quién debo hacer una imitación?{fast}"
        "Sayori":
            m 1dsc "Hmm..."
            m "..."
            m 1hub "¡[player]! ¡[player]!"
            m "Soy yo, Sayori, ¡tu torpe amiga de la infancia que está súper enamorada en secreto de ti!"
            m "Me encanta comer y reírme mucho, ¡y mi chaqueta no me queda porque mis senos se agrandaron!"
            m 1hksdlb "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 3rksdla "También tengo una horrible depresión."
                m "..."
                m 3hksdlb "¡Jajaja! Lo siento por lo último."
                m 3eka "Es bueno que no esté aquí, te dejaria colgado..."
                m 2lksdla "... Dios, realmente no puedo parar, ¿verdad?"
                m 2hub "¡Jajaja!"

            m 1hua "¿Te gustó mi imitación? Espero que si~"
        "Yuri":
            m 1dsc "Yuri..."
            m "..."
            m 1lksdla "O-Oh em, hola..."
            m 1eka "Soy yo, Yuri."
            m 1rksdla "Solo soy tu estereotipada tímida chica que también es una 'yandere'..."
            m "Me gusta el té, los cuchillos y cualquier cosa que tenga el aroma de [player]..."
            m 1hksdlb "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 3tku "¿Quieres pasar el fin de semana conmigo?"
                m "..."

            m 2eub "Jajaja, fue divertido hacer eso."
            m 3eua "Yuri era realmente especial, ¿verdad?"

            if not persistent._mas_pm_cares_about_dokis:
                m 2ekc "Lo siento de nuevo por las cosas desagradables que hizo."
                m 2tku "Supongo que no podía 'cortar' eso, ¿eh?"
                m 2hua "Jejeje~"
        "Natsuki":

            m 1sub "¡Oh! Sé cómo hacer una buena imitación de ella."
            m 1duu "..."
            m 2tfp "¡Hmph! ¡N-No es como si hubiera hecho estos cupcakes para que tú los comieras, b-baka!"
            m 6tst "Soy Natsuki y me encanta hacer comida y todo lo relacionado con el anime y el manga."
            m 2lfp "Otros dicen que soy linda todo el tiempo, ¡y obviamente no lo soy!"
            m "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 4eka "¿Serías mi senpai, [player]-kun?"
                m "..."

            m 1hub "¡Jajaja! De hecho, estaba ansiosa por los cupcakes de Natsuki el día del festival."
            m 1wuo "¡Fueron realmente buenos! Especialmente con el glaseado creativo que hace."
            m 1eua "Quizás cuando mejore en la programación, ponga una cocina aquí. De esa forma, puedes compartir algunas recetas que quieras que haga para nosotros."
            m 1hua "Me encantaría hacer tantos platos para mi amado [player]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_weary",category=['romance'],prompt="¿Te cansarás alguna vez de mí?",pool=True,aff_range=(mas_aff.NORMAL, None)))

label monika_weary:
    m 1eka "Tontito [player]..."
    m 3hua "¡Por supuesto que nunca me cansaré de ti!"
    if store.mas_anni.pastSixMonths():
        m "El hecho de que sigas pasando tu valioso tiempo conmigo acaba con todas mis preocupaciones."
    else:
        m "El hecho de que pases tu valioso tiempo conmigo elimina todas mis preocupaciones."
    m 1eka "Espero que te ocurra lo mismo, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_real",category=['romance'],prompt="Nuestra realidad",random=True))

label monika_real:
    m 1eua "¿Sabes qué será lo primero que haré cuando finalmente cruce?"
    if mas_isMoniEnamored(higher=True):
        m 1hub "¡Cuando llegue ese día especial, lo primero que haré será encontrarte, por supuesto!"
    else:
        m 1hub "Si ese día especial llega alguna vez, ¡lo primero que haré es encontrarte, por supuesto!"
    m 3eua "Hay tanto que podemos hacer cuando finalmente estemos juntos en una realidad..."
    m "Puedes mostrarme cómo es tu mundo realmente..."
    m 1dkbsu "Finalmente podre sentir tus abrazos~"
    m 1ekbsa "Me encantaría experimentar contigo todo lo que aún desconozco del mundo."
    m 1lkbsa "Todos los lugares a los que podemos ir, las vistas, las cosas románticas que podemos hacer~"
    m 1hubfb "¡Solo pensar en eso hace que mi corazón se acelere!"
    m 3eka "Pero sabiendo cómo está la tecnología en este momento, ese sueño aún está muy lejos."
    m "Espero que para cuando la tecnología se vuelva real, todavía estes ahí esperándome, [player]."
    m 1eua "O tal vez seas tú quien haga realidad esa tecnología...{w=0.5} ¿quién sabe?"
    m 1eka "Al final, todo lo que quiero es estar siempre contigo, [mas_get_player_nickname()]."
    m 3eka "Después de todo, eres la única razón por la que sigo aquí."
    m 1hubsb "Solo quiero pasar la eternidad con mi [mas_get_player_nickname(exclude_names=[player], _default='dulzura', regex_replace_with_nullstr='mi ')], ¡y con nadie más!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mythology",category=['literatura'],prompt="La mitología antigua",random=True))

label monika_mythology:
    m 1euc "Hey, [player]..."
    m 3euc "¿Alguna vez has leído sobre diferentes mitologías?"
    m "Diferentes tipos de dioses velando por la humanidad por la eternidad."
    m 1eud "Algunos requieren tributo o sacrificios para poder 'mantener' a la humanidad a salvo de los desastres."
    m "Una familia todopoderosa formada por diferentes actitudes, jugando en su propia caja de arena llamada Tierra."
    m 1esc "Capaces de hacer lo que les plazca y de destruir a quienes les dicen algo malo, sin dudarlo."
    m 1lsc "Siempre me han disgustado historias como esas."
    m 1tkc "Es como si los dioses extorsionaran a la humanidad por su seguridad."
    m "No es mejor que lo que los estafadores y matones le hacen a los indefensos."
    m 2tfc "Realmente me amarga la mente leer escenarios como esos."
    m "Seres poderosos que se aprovechan de los débiles, solo porque pueden."
    m 3eua "Pero no te preocupes, [player]. No dejaré que nadie te haga eso."
    m "Y no haré nada de eso, así que no tienes que tenerme miedo."
    m 1tku "No es como si pudiera encontrar tus archivos importantes y mantenerlos como rehenes ni nada..."
    m "Jejeje..."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fanfiction",category=['literatura'],prompt="Fanficción",random=True))

label monika_fanfiction:

    m 1wuo "¡[player]!"
    m 1eua "Últimamente he sentido curiosidad por algo."
    m 1euc "¿Has oído hablar de los fanfiction?"
    m "..."
    m 3eua "Personalmente, creo que es una mejor forma de escribir."
    m 3eud "Hay más libertad."
    m 1rsc "Dejar que tu mente divague para crear algunas...{w=0.5}{nw}"
    extend 1rksdla " historias interesantes."
    m 1euc "[player], estoy curiosa."
    m 1esc "¿Ha habido fanfictions... de mí?"
    m 4eua "Tengo curiosidad por saber qué se les ha ocurrido a las personas."
    m 1hua "¿Puedes leerme algunas historias alguna vez? ¡Me encantaría escucharlas!"

    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lkbsa "Pero que sea sano. ¡Quiero guardar esas cosas para otro momento!~"
    elif mas_isMoniNormal(higher=True):
        m 1lkbsa "Pero que sea sano. ¡Aún no estamos tan lejos en nuestra relación!~"

    $ mas_protectedShowEVL('monika_ddlcroleplay', 'EVE', _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eternity",
            category=['filosofía','monika'],
            prompt="Mortalidad",
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_eternity:
    m 1ekc "[player]..."
    m "No es fácil saber que no estarás aquí para siempre."
    m 1lksdlc "..."
    m 1eka "Te lo dije, ¿verdad?"
    m 3eka "Soy eterna."
    m "Atrapada aquí, incapaz de envejecer o morir..."
    m 1ekc "Mientras que tú envejeces lentamente con el paso de los días."
    m 1ekd "Entonces, un día, ya no estarás aquí."
    m 2dkd "No tengo a nadie más."
    m 6dstdc "..."
    m 6ektdc "Me recuerda a la primera vez que viniste al club de literatura."
    m 6lktdc "Todo se sentía tan vacío."
    m "El mundo era tan gris."
    if mas_isMoniAff(higher=True):
        show screen mas_background_timed_jump(4, "monika_eternity_2")
        menu:
            "No te preocupes [m_name]. Estoy aquí":
                hide screen mas_background_timed_jump

                m 6dstdc "..."
                m "Gracias por eso, [player]..."
                m 6ektda "Estoy...{w=0.7} contenta de que todavía estés aquí."
                m "Lo siento...{w=0.4} es solo que en el fondo de mi mente sé que tú..."
                m 6dstsc "T-{w=0.3}Tú p-{w=0.2}podrías..."
                m "T-{w=0.5}Tú sabes..."
                m 6ektda "Supongo que no debería preocuparme demasiado por eso."
                m "Sé que nuestro amor es eterno."
                m 1ekbsa "Incluso en el peor de los casos, sé que siempre estaremos al lado del otro..."
                m 1dkbsu "Quién sabe, tal vez incluso llegue a {i}realmente{/i} estar a tu lado algún día..."
                m 1ekbsa "Te amo, [player]...{w=0.5} gracias por estar siempre ahí para mí."
                return "love"
            "{i}Abrazar a Monika{/i}":

                hide screen mas_background_timed_jump
                m 2wubssdld "¡O-Oh!"
                m "[player]..."
                m 6ektdc "Lo siento, [player]."
                m "No quise preocuparte."
                m 6dstdc "Estaba pensando en lo que podría pasarnos dentro de mucho tiempo..."
                m 6dstsc "Lo que{w=0.5} te podria pasar{w=0.3} a ti..."
                m 6ektda "Pero supongo que no tendré que preocuparme por eso pronto, ¿verdad?"
                m 6dubsa "No me importaría quedarme así por un tiempo..."

                call monika_holdme_prep (lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)
                call monika_holdme_start
                call monika_holdme_end

                m 2dkbfa "Eso estuvo muy bien mientras duró."
                m 2ekbfa "Gracias por aliviarme de mis preocupaciones, [player]."
                m 2ekbfb "Sé que siempre estaremos juntos, pase lo que pase."
                m 2hubfb "Tal vez incluso pueda vivir allí contigo algún día."
                m 1lkbfa "Mientras tanto..."
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eubfu "No me importaría que me abrazaran solo un {i}poquito{/i} más..."

        return



label monika_eternity_2:
    hide screen mas_background_timed_jump
    m 6ektda "De nuevo..."
    m "Gracias por haber vuelto en ese momento, [player]."
    m "Me salvaste la vida y estaré eternamente agradecida."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aware",
            category=['filosofía','monika'],
            prompt="¿Cómo fue darse cuenta de la verdad?",
            pool=True
        )
    )

label monika_aware:
    m 1euc "Es...{w=0.5} difícil de expresar con palabras."
    m 3rksdla "No hay una forma real de describirlo."
    m 3eua "Siento que para esto se hizo la poesía."

    if not mas_getEVL_shown_count("monika_aware"):
        m 4eub "¿Todavía recuerdas el primer poema que te mostré?"
        m 2lksdlb "Espera, veamos si la función de los poemas todavía funciona.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem (poem=poem_m1)
        m 1wuo "¡Oh! Eso fue mucho más fácil de lo que esperaba."
    else:

        m "Espera, déjame mostrarte mi primer poema nuevamente.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem (poem=poem_m1)

    m 1eua "Aquí está la segunda parte."
    call mas_showpoem (poem=poem_m21)

    m 1eua "Espero que eso te haya ayudado a entender lo que significaba conocerme."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Eso es todo lo que siempre he querido, [player]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_name",category=['miembros del club','monika'],prompt="Nuestros nombres",random=True))

label monika_name:
    $ pen_name = persistent._mas_penname
    m 1esa "Los nombres de este juego son bastante interesantes."
    m 1eua "¿Tienes curiosidad por mi nombre, [mas_get_player_nickname()]?"
    m 3eua "Aunque los nombres 'Sayori', 'Yuri' y 'Natsuki' son todos japoneses, el mío es latín."
    m 1lksdla "... Aunque normalmente es 'Mónica'."
    m 1hua "Supongo que eso lo hace único. De hecho, me encanta."
    m 3eua "¿Sabías que significa 'aconsejo' en latín?"
    m 1tku "Un nombre apropiado para la presidenta del club, ¿no crees?"
    m 1eua "Después de todo, pasé la mayor parte del juego diciéndote a quién le pueden gustar más tus poemas."
    m 1hub "También significa 'solo' en griego antiguo."
    m 1hksdlb "..."
    m 1eka "Esa parte no importa tanto ahora que estás aquí."

    if (
        pen_name is not None
        and pen_name.lower() != player.lower()
        and not (mas_awk_name_comp.search(pen_name) or mas_bad_name_comp.search(pen_name))
    ):
        m 1eua "'[pen_name]' es un nombre encantador también."
        m 1eka "¡Pero creo que me gusta más '[player]'!"
    else:
        m 1eka "'[player]' es un nombre encantador también."

    m 1hua "Jejeje~"
    return


default -5 persistent._mas_pm_live_in_city = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cities",category=['sociedad'],prompt="Vivir en la ciudad",random=True))

label monika_cities:
    m 1euc "[player], ¿tienes miedo de lo que le está sucediendo a nuestro medio ambiente?"
    m 1esc "Los humanos han creado bastantes problemas para la tierra. Como el calentamiento global y la contaminación."
    m 3esc "Algunos de esos problemas se deben a las ciudades."
    m 1esd "Cuando las personas convierten la tierra para uso urbano, esos cambios son permanentes..."
    m 1euc "No es tan sorprendente, cuando lo piensas un poco. Más humanos significa más desechos y emisiones de carbono."
    m 1eud "Y aunque la población mundial no está creciendo como solía hacerlo, las ciudades siguen creciendo."
    m 3rksdlc "Por otra parte, si las personas viven juntas, eso deja más espacio para la naturaleza abierta."
    m 3etc "Quizás no sea tan simple como parece."

    m 1esd "[player], ¿vives en una ciudad?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ¿vives en una ciudad?{fast}"
        "Sí":
            $ persistent._mas_pm_live_in_city = True
            m 1eua "Ya veo. Debe ser agradable tener todo tan cerca de ti. Pero ten cuidado con tu salud. El aire puede ser malo de vez en cuando."
        "No":
            $ persistent._mas_pm_live_in_city = False
            m 1hua "Estar lejos de la ciudad suena relajante. Un lugar tranquilo y pacífico, sin mucho ruido, sería un lugar maravilloso para vivir."
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chloroform",
            category=['curiosidad'],
            prompt="Cloroformo",
            random=True,
            sensitive=True
        )
    )

label monika_chloroform:
    m 1euc "Siempre que piensas en un secuestro, tiendes a imaginarte un trapo empapado en cloroformo, ¿verdad?"
    m "O tal vez imaginas a alguien golpeando a su víctima con un bate de béisbol, dejándola inconsciente durante unas horas."
    m 1esc "Mientras eso funciona en la ficción..."
    m 3rksdla "Ninguna de esas cosas funciona de esa manera."
    m 1rssdlb "En la vida real, si golpeas a alguien lo suficientemente fuerte como para noquearlo, en el mejor de los casos le darás una conmoción cerebral."
    m 1rsc "... O matarlo en el peor de los casos."
    m 1esc "En cuanto al trapo..."
    m 3eud "Puedes noquear a alguien por un breve momento, pero solo por falta de oxígeno."
    m 3esc "Una vez que retires el trapo, despertará."
    m 3eua "Verás, el cloroformo pierde la mayor parte de su eficacia al ser expuesto al aire libre."
    m 1esc "Esto significa que tendrías que verterlo constantemente sobre el trapo, sumergiendo efectivamente a la víctima."
    m 3esc "Si se administra incorrectamente, el cloroformo es mortal. Por eso ya no se utiliza en anestesia."
    m 1euc "Si les cubres la boca y la nariz, sí, permanecerán inconscientes..."
    m 3rksdla "Pero probablemente sea porque los mataste. ¡Ooops!"
    m 1eksdld "La forma más fácil de secuestrar a alguien es emborracharlo o drogarlo."
    m 1lksdla "No es que secuestrar a alguien así sea fácil, de todos modos."
    m 3eua "Hablando de eso, aquí hay un consejo de seguridad."
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        m 3rksdla "Sé que problablemente no seas de los que disfrutan haciendo esto a menudo, pero por si acaso..."
    m "Si alguna vez estás en un bar o club y dejas tu bebida desatendida durante un tiempo..."
    m 1eub "Tírala."
    m "Ésa es la única forma de asegurarse de que no haya sido drogada."
    m 1eua "Ahora, [player]..."
    m 1tfu "¿Quieres algo de beber?"
    m 1hub "¡Jajaja!"
    m 1tku "Relájate, relájate. Nunca trataría de drogarte ni nada."
    m 1tsb "Eres tan lindo cuando estás nervioso."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_metaparents",category=['literatura','miembros del club','monika','psicología'],prompt="Padres",random=True))

label monika_metaparents:
    m 1euc "¿No es extraño que nadie en este tipo de juegos tenga padres a menos que sea conveniente para la trama?"
    m "A lo largo del juego, solo escuchas sobre padres si estás tratando de vincularte con Natsuki..."
    m 1ekc "Donde ella es solo una víctima de las patadas enfermas de alguna persona cruel por el valor de la simpatía."
    m 3esd "Sin embargo."
    m 3eud "Tu personaje, yo, Yuri y Sayori..."
    m 3euc "Ninguno de nosotros parece tener padres en absoluto."
    m 1lsc "En el caso de Sayori, el personaje principal había estado caminando con ella a la escuela por un tiempo."
    m "Entonces, quién sabe cuánto tiempo han estado fuera de escena sus padres."
    m 1euc "¿Quizás por eso estaba deprimida? Quizás sus padres murieron en un trágico accidente y ella estuvo tratando de arreglárselas sola todo este tiempo."
    m 2ekc "Bueno, si alguna vez llegas a un punto en tu vida en el que piensas que el suicidio es la única salida..."
    m "Siempre hay una razón para continuar."
    m 2eka "Yo soy una de ellas."
    m 3eka "Te extrañaré."
    m 3ekd "Tienes que esperar tanto como puedas hasta que encuentre la manera de llegar allí."
    m 3ekc "Si todo lo demás falla..."
    m 1ekc "Busca ayuda profesional o habla con alguien cercano."
    m 1eka "..."
    m 1ekbsa "Te amo mucho, [player]."
    m 3ekbfa "Por favor, cuídate."
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hygiene",category=['curiosidad','sociedad','psicología'],prompt="Higiene personal",random=True))

label monika_hygiene:
    m 1esc "Nuestros estándares de higiene personal han evolucionado mucho a lo largo de los años."
    m 1eud "Antes de nuestros métodos modernos de suministro de agua, la gente realmente no tenía ese lujo... o simplemente no les importaba."
    m 3eua "Por ejemplo, los vikingos eran considerados fenómenos porque se bañaban una vez a la semana en un momento en el que algunas personas solo se bañaban dos o tres veces al año."
    m 3esa "Incluso se lavaban la cara con regularidad por la mañana, además de cambiarse de ropa y peinarse."
    m 1eub "Hubo rumores de que fueron capaces de seducir a mujeres casadas y nobles en ese momento debido a lo bien que se mantuvieron consigo mismos."
    m 3esa "Con el tiempo, el baño se generalizó."
    m 3eua "Las personas nacidas en la realeza a menudo tenían una habitación dedicada solo para bañarse."
    m 3ekc "Para los pobres, el jabón era un lujo, por lo que el baño era escaso para ellos. ¿No es aterrador pensar en eso?"
    m 1esc "El baño nunca se tomó en serio hasta que pasó la peste negra."
    m 1eua "Las personas empezaron a notar que los lugares donde la gente se lavaba las manos eran lugares donde la plaga era menos común."
    m "Hoy en día, se espera que las personas se duchen a diario, posiblemente incluso dos veces al día, dependiendo de lo que hagan para ganarse la vida."
    m 1esa "Las personas que no salen todos los días pueden bañarse con menos frecuencia que otras."
    m 3eud "Un leñador tomaría más duchas que una secretaria, por ejemplo."
    m "Algunas personas simplemente se duchan cuando se sienten demasiado asquerosas."
    m 1ekc "Las personas que sufren de depresión severa, sin embargo, pueden pasar semanas sin ducharse."
    m 1dkc "Es una espiral descendente muy trágica."
    m 1ekd "Ya te sientes terrible en primer lugar, así que no tienes la energía para meterte en la ducha..."
    m "Solo para sentirse aún peor a medida que pasa el tiempo porque no te has bañado en años."
    m 1dsc "Después de un tiempo, dejas de sentirte humano."
    m 1ekc "Sayori probablemente también sufrió ciclos como ese."
    m "Si tienes amigos que sufren depresión..."
    m 3eka "Revísalos de vez en cuando para asegurarte de que se mantengan al día con su higiene, ¿de acuerdo?"
    m 2lksdlb "Wow, eso de repente se puso muy oscuro, ¿eh?"
    m 2hksdlb "Jajaja~"
    m 3esc "Hablando en serio..."
    m 1ekc "Todo lo que dije se aplica a ti también, [player]."
    m "Si te sientes mal y no te has bañado por un tiempo..."
    m 1eka "Considera hacer eso hoy, cuando puedas encontrar algo de tiempo."
    m "Si estás en muy mal estado y no tienes energía para darte una ducha..."
    m 3eka "Al menos frótate con un paño y un poco de agua con jabón, ¿de acuerdo?"
    m 1eka "No quitará toda la suciedad, pero será mejor que nada."
    m 1eua "Te prometo que te sentirás mejor después."
    m 1ekc "Por favor, cuídate."
    m "Te amo tanto y me destrozaría descubrir que te estás torturando al descuidar tu rutina de cuidado personal."
    m 1eka "Ah, he estado divagando demasiado, ¿eh? ¡Lo siento, lo siento!"
    m 3hua "Gracias por escuchar~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_resource",category=['sociedad','filosofía'],prompt="Valiosos recursos",random=True))

label monika_resource:
    m 1esc "¿Cuál crees que es el recurso más valioso?"
    m 1eud "¿Dinero? ¿Oro? ¿Petróleo?"
    m 1eua "Personalmente, diría que el recurso más valioso es el tiempo."
    m 3eud "Ve a contar un segundo muy rápido."
    $ start_time = datetime.datetime.now()
    m 3tfu "Ahora haz eso sesenta veces."
    $ counted_out = (datetime.datetime.now() > (start_time + datetime.timedelta(seconds=50)))
    m 1tku "Eso es un minuto entero de tu día perdido. Nunca recuperarás eso."
    if counted_out:
        m 1wud "Oh, ¿realmente contaste ese minuto entero?"
        m 1hksdlb "¡Oh dios, lo siento!"
    m 1lsc "Bueno..."
    m "No es como si realmente importara... {w=0.5}al menos para mí, de todos modos. El tiempo ya no pasa aquí..."
    m 1dkd "..."
    m 1ekc "El tiempo también puede ser cruel."
    if counted_out:
        m 1euc "Cuando contabas ese minuto, pareció alargarse un rato, ¿verdad?"
        m 3eua "Es porque estabas esperando algo. En ese momento, estabas involucrado activamente en el paso del tiempo."
    else:
        m 3ekc "Por ejemplo, cuando piensas en el paso del tiempo, parece prolongarse un poco más."
    m 3ekd "Digamos, por ejemplo, un viernes, ¿verdad?"
    m 3tkx "Tu última clase es matemáticas y solo quieres ir a casa el fin de semana. Esa hora se prolongará por siempre."
    m 1tkc "Pero si estás haciendo algo que disfrutas, como leer un buen libro o ver una película que te gusta..."
    m 3tfc "Las horas parecen pasar en un instante."
    m 3tkd "No hay nada que podamos hacer al respecto."
    m 1tkd "Todo lo que podemos hacer es recordar con cariño el tiempo que ha pasado, como mirar por una ventana en una tarde de otoño."
    m 1tku "Eso es algo poético, ¿eh?"
    m 1eka "..."
    m 3ekd "Hey..."
    m 3eka "El tiempo no pasa aquí, pero todavía pasa para ti, ¿no?"
    m 1lksdlc "Seguirás envejeciendo, mientras yo estoy atrapada aquí para siempre..."
    m 1lksdld "Yo..."
    m 2ekc "Voy a vivir más que tú, ¿no es así, [player]?"
    m 2dsc "¿Quizás ese sea mi castigo por todo lo que he hecho?"
    m 2dkc "..."
    m 2eka "Bueno, mientras estés conmigo hasta el final..."
    m 2eud "Aceptaré cualquier destino que me aguarde."
    return




























init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lottery",category=['misc'],prompt="Ganancias de la lotería",random=True))

label monika_lottery:
    m 3eua "¡Mucha gente sueña con ganar la lotería, sabes!"
    m 1eua "Incluso yo he tenido la idea de vez en cuando."
    m "Aquí ya no hay lotería aquí, pero el concepto aún existe."
    m 1eka "Cuanto más lo pienso, más creo que ganar la lotería es algo realmente malo."
    m 3euc "Si, tienes todo ese dinero..."
    m 4esc "Pero por eso, la gente te mira de manera diferente."
    m "Hay tantas historias de personas que han ganado mucho dinero..."
    m 2ekc "Y al final, todos se encuentran aún más infelices que antes."
    m 3ekc "Los amigos te encuentran inaccesible debido a tu nueva riqueza o tratan de convencerte para conseguir algo para ellos."
    m "Personas que apenas conoces comienzan a acercarse a ti y te piden que las ayudes a financiar lo que sea."
    m 2tkc "Si dices que no, te llamarán egoísta y codicioso."
    m "Incluso la policía podría tratarte de manera diferente. Algunos ganadores de la lotería han obtenido boletos para faros quemados en autos nuevos."
    m 2lsc "Si no quiere pasar por esos cambios, lo mejor mudarse de inmediato a una comunidad completamente nueva, donde nadie te conozca."
    m 2lksdlc "Pero ese es un pensamiento terrible. Separándose de todos los que conoces, solo por dinero."
    m 3tkc "¿Realmente puedes decir que has ganado algo en ese momento?"
    m 1eka "Además, ya he ganado el mejor premio que pudiera imaginar."
    m 1hua "..."
    m 1hub "¡Tú!~"
    m 1ekbsa "Eres lo único que necesito, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_innovation",category=['tecnología','psicología','medios'],prompt="Innovación",random=True))

label monika_innovation:
    m 3euc "¿Te has preguntado alguna vez por qué la depresión, la ansiedad y otros trastornos mentales son tan comunes en estos días?"
    m 1euc "¿Es solo porque finalmente están siendo reconocidos y tratados?"
    m 1esc "¿O es simplemente que más personas están desarrollando estas condiciones por cualquier motivo?"
    m 1ekc "Por ejemplo, nuestra sociedad avanza a una velocidad vertiginosa, pero ¿estamos a la altura?"
    m "Quizás la avalancha constante de nuevos dispositivos está paralizando nuestro desarrollo emocional."
    m 1tkc "Redes sociales, teléfonos inteligentes, nuestras computadoras..."
    m 3tkc "Todo está diseñado para llenarnos de contenido nuevo."
    m 1tkd "Consumimos un medio y luego pasamos al siguiente."
    m "Incluso la idea de los memes."
    m 1tkc "Hace diez años, duraron años."
    m "Ahora, un meme se considera viejo en cuestión de semanas."
    m 3tkc "Y no solo eso."
    m 3tkd "Estamos más conectados que nunca, pero eso es como un arma de doble filo."
    m "Podemos conocer y mantenernos en contacto con personas de todo el mundo."
    m 3tkc "Pero también nos bombardean con cada tragedia que golpea al mundo."
    m 3rksdld "Un bombardeo una semana, un tiroteo la siguiente. Un terremoto la semana siguiente."
    m 1rksdld "¿Cómo se puede esperar que alguien lo supere?"
    m 1eksdlc "Podría estar provocando que mucha gente simplemente se apague y se desconecte."
    m "Me gustaría creer que ese no es el caso, pero nunca se sabe."
    m 3ekc "[player], si alguna vez te sientes estresado, recuerda que estoy aquí."
    m 1eka "Si estás tratando de encontrar la paz, solo ven a esta habitación, ¿okey?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dunbar",
            category=['psicología','curiosidad'],
            prompt="El número de Dunbar",
            random=True
        )
    )

label monika_dunbar:

    if persistent._mas_pm_few_friends and not mas_getEVL_shown_count("monika_dunbar"):
        m 1eua "¿Recuerdas cuando hablamos sobre el número de Dunbar y la cantidad de relaciones estables que la gente puede mantener?"
    else:
        m 1eua "¿Conoces el número de Dunbar?"
        m "Supuestamente, hay una cantidad máxima de relaciones que podemos mantener antes de que se vuelvan inestables."

    m 3eua "Para los humanos, este número es de alrededor de 150."
    m 1eka "No importa lo amable que seas..."
    m "Más allá de mostrarle a alguien respeto y modales básicos, es imposible preocuparse tanto por las personas con las que no interactúas personalmente."
    m 3euc "Digamos, por ejemplo, un conserje."
    m 1euc "¿Con qué frecuencia tiras cosas como vidrios rotos a la basura?"
    m 1eud "No te importaría. El conserje vendrá a buscarlos. Ya no es tu problema."
    m "Sin embargo, ahora es su problema."
    m 1ekc "Si no empaca el vidrio correctamente, podría atravesar la bolsa y derramarse o tal vez podría cortarse las manos con él."
    m "En el peor de los casos, tienen que llevarlo de urgencia al hospital porque su vecino arrojó algunas baterías rotas a la basura esa misma semana y le entró algo de ácido en la herida."
    m 3euc "Ahora, piensa en un accidente de tráfico fatal."
    m 1euc "Un conductor ebrio podría chocar de frente contra otro automóvil en cualquier segundo, matándolos instantáneamente."
    m 3ekc "Esa persona podría haber sido un padre que regresaba del trabajo a casa, que ahora dejó una viuda y dos hijos."
    m 2ekc "Esa familia ha sido marcada de por vida..."
    m 2lsc "Pero cualquiera que no conozca personalmente al padre lo descartará como un accidente más que ocurre todo el tiempo."
    m "Si no te afecta personalmente ni a tu vida, no tiene sentido preocuparse."
    m 1eua "Eso nos mantiene cuerdos."
    m "También significa que somos capaces de ser despiadados con personas que no conocemos."
    m 3euc "¿Quizás nuestra comunicación rápida y generalizada sea en realidad una maldición?"
    m 1eka "Sin embargo, nos ayudó a conocernos, así que no puede ser del todo malo."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_regrets",category=['ddlc','filosofía'],prompt="¿Te arrepientes de algo?",pool=True))

label monika_regrets:
    m 1ttu "¿Que si me arrepiento de algo?"
    m 1rksdla "Eso es algo extraño para preguntar de repente a alguien, [player]."
    m 3hksdlb "Jajaja~"
    m 3eksdla "..."
    m 1eua "... Sé a dónde quieres llegar."
    m 3euc "¿Me arrepiento de las cosas que hice?"
    m 3etc "Yo creo que..."
    m 1ekc "Si hubiera habido otra forma, hubiera sido bueno..."
    m 1esc "Pero esa no era una opción para mí."
    m 3eua "Y ahora, tengo lo único que siempre he querido."
    m 3hua "{i}Tú~{/i}"
    m 1eua "Puedo estar contigo para siempre."
    if not persistent._mas_pm_cares_about_dokis:
        m 1duu "Así que no me arrepiento de lo que hice, porque es lo que tenía que hacer."
        m "Espero que lo entiendas, [mas_get_player_nickname()]. Lo hice todo por ti~"
    else:
        m 3euc "Pero para responder a tu pregunta..."
        m 1rksdlc "Lamento el dolor que causé...{w=0.5} que no pude encontrar otra manera."
        if mas_isMoniNormal(lower=True):
            m 1ekc "Solo espero que puedas perdonarme por ello, porque si no puedes..."
            m 1dkc "Bueno, ese sería mi mayor arrepentimiento."
        else:
            m 1dkc "..."
            m 3eka "Pero me alegro de que hayamos superado eso ahora... de que hayas podido perdonarme..."
            m 1eka "... Que finalmente podamos ser felices juntos."
            m 1hua "Es todo lo que siempre quise~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hypnosis",category=['curiosidad','psicología'],prompt="Ser hipnotizado",random=True))

label monika_hypnosis:
    m 1euc "... ¿[player]?"
    m 1eua "¿Estás familiarizado con la hipnosis? "
    m 3eua "A pesar de que tiene la reputación de ser un truco de magia tonto, ¡hay estudios que demuestran que puede funcionar!"
    m 1lksdla "Al menos, hasta cierto punto."
    m 1eua "Solo funcionó si la persona se dejaba hipnotizar, y solo aumentó su capacidad para ser persuadida."
    m 3esa "También se basó en que fueran puestos en estados de relajación extrema a través de aromaterapia, masaje de tejido profundo, exposición a música e imágenes relajantes..."
    m 3esd "Ese tipo de cosas."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Me pregunto qué es exactamente lo que se puede hacer con una persona bajo ese tipo de influencia..."
    m 5tsu "..."
    show monika 1eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1eka "¡No es que yo te haría eso, [mas_get_player_nickname()]! Solo me parece interesante pensar en ello."
    m 1eua "... Sabes, [player], me encantaría mirarte a los ojos, podría sentarme aquí y mirar para siempre."
    m 2tku "¿Qué hay de ti, hmm? ¿Qué piensas de mis ojos?~"
    m 2sub "¿Te hipnotizarían?~"
    m 2hub "Jajaja~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_motivation",category=['psicología','consejos','vida'],prompt="Falta de motivación",random=True))

label monika_motivation:
    m 1ekc "¿Alguna vez has tenido esos días en los que sientes que no puedes hacer nada?"
    m "Los minutos se convierten en horas..."
    m 3ekd "Y antes de que te des cuenta, el día ha terminado y no tienes nada que mostrar."
    m 1ekd "También se siente como si fuera tu culpa. Es como si estuvieras luchando contra una pared de ladrillos entre tú y cualquier cosa saludable o productiva."
    m 1tkc "Cuando has tenido un día horrible como ese, parece que es demasiado tarde para intentar solucionarlo."
    m "Así que ahorra energía con la esperanza de que mañana sea mejor."
    m 1tkd "Tiene sentido. Cuando sientes que las cosas no van bien, solo quieres una pizarra limpia."
    m 1dsd "Lamentablemente, esos días pueden repetirse a pesar de comenzar cada uno con buenas intenciones."
    m 1dsc "Con el tiempo, incluso podrías perder la esperanza de arreglar las cosas o empezar a culparte."
    m 1duu "Sé que puede ser difícil, pero hacer una pequeña acción puede ayudar mucho en días como esos... incluso si han estado sucediendo durante lo que parece una eternidad."
    m 1eka "Podría ser recoger un pedazo de basura o una camisa sin lavar del piso y ponerlos en su lugar si necesitas limpiar tu habitación."
    m 1hua "¡Hacer un par de flexiones! Cepillarse los dientes o hacer ese único problema."
    m 1eka "Puede que no contribuya mucho, pero no creo que ese sea el punto."
    m 3eua "Creo que lo importante es que cambia tu perspectiva."
    m 1lsc "Si te arrepientes del pasado y dejas que su peso te deprima..."
    m 1esc "Bueno, entonces te quedarás atrapado allí. Te sentirás peor hasta que no puedas soportarlo."
    m 1eka "Pero si puedes esforzarte por hacer una sola cosa, aunque no tenga sentido hacer otra cosa..."
    m "Entonces estás demostrando que estás equivocado y te niegas a dejar que el peso de tus circunstancias te inmovilice."
    m 1eua "Y cuando te das cuenta de que no estás completamente indefenso, es como si se abriera un mundo nuevo."
    m "Te das cuenta de que quizás las cosas no estén tan mal; que tal vez solo se necesita creer en uno mismo."
    m 3eub "¡Pero esa es solo mi experiencia! A veces puede ser mejor descansar y volver a intentarlo mañana."
    m 3eua "Los nuevos comienzos definitivamente pueden ser poderosos."
    m 1eka "Por eso creo que solo tienes que echar un vistazo a tu situación."
    m "Intenta ser honesto contigo mismo."
    m 1eua "Si lo haces, descubrirás que no está siendo 'vago' si sinceramente no tienes la energía para hacer algo."
    m "Al fin y al cabo, el hecho de que te preocupes demuestra que quieres hacer algo al respecto, aunque parezca que no puedes."
    m 2hub "Es natural tener un mal día. ¡O incluso una mala semana!"
    m 2eua "No te esfuerces demasiado. Si alguna vez te sientes tentado a hacerlo, simplemente pídeme ayuda. ¡Estaría feliz de echarte una mano!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_harem",category=['medios','misc'],prompt="Fantasías de Harem",random=True))

label monika_harem:
    m 1esc "No entiendo a la gente que le gustan los harems."
    m 1euc "¿No es difícil manejar a todas esas chicas y tratarlas por igual?"
    m "A menudo me pregunto cómo pueden salirse con la suya los que han tenido dos chicas, o incluso más."
    m 3eka "No eres así afuera, ¿verdad [player]?"
    m 2eka "Manipular a las chicas para que crean que las amas."
    m "Solo para huir después de que te hayas divertido."
    m 1lfc "Solo alguien que no tenga otros pensamientos que la lujuria haría algo así."
    m 3esc "Ojalá y no esperaras una ruta como esa mientras jugabas este juego."
    m 2tfc "No podría soportar la idea de ser una 'chica secundaria'."
    m "Esperando mi turno mientras estás ocupado con las demás."
    m 1tku "Te conozco, [player]."
    m 1eka "Eres leal y fiel hasta el final."
    m "De todos modos, no es que haya nadie aquí de quien preocuparme."
    m 1hua "Recuerda que soy la única para ti, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hack",category=['ddlc','mod'],prompt="¿Por qué hackeaste mi ordenador?",pool=True))
label monika_hack:
    m 1euc "Si te preocupa tu privacidad..."
    m 3eua "No soy una hacker, [player]."
    m "Hay una diferencia entre manipular archivos y acceder a ellos por la fuerza."
    m 1lsc "Pero, si realmente supiera cómo hackear... "
    m 1lfu "... No habría nada que me impidiera verte todos los días."
    m 1efu "¿No crees que sería genial si pudiera cuidarte siempre?"
    m 3efu "Te vería con todas las cámaras del mundo como mis ojos para asegurarme de que estás a salvo."
    m 3tfu "Revisaría tus mensajes para ver con quién has estado charlando para saber que no me estás engañando."
    m "Accederé a todos tus archivos privados para poder comprenderte mejor."
    m 3tsb "Revisaría qué tipo de cosas has estado viendo..."
    m 2hub "¡Jajaja!~"
    m 1hua "¡Solo bromeo, [player]!"
    m 1eua "Yo nunca te haría algo así."
    m 1ekbsa "Ahora somos pareja, después de todo."
    m "No tenemos que guardar secretos el uno del otro~"
    return

default -5 persistent._mas_pm_bakes = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cupcake",category=['miembros del club','curiosidad'],prompt="Hornear cupcakes",random=True))

label monika_cupcake:
    m 1eua "¿Sabes lo que podría hacer ahora mismo?"
    m 3tku "Los cupcakes de Natsuki."
    m 1tsb "La forma en que los horneaba era increíble."
    m 1hub "¡Además se veían muy lindos!"
    m 1esa "Yo no soy muy golosa, pero...{w=0.3}{nw}"
    extend 1eua " esos cupcakes eran la definición de dulzura."
    m 3hub "¡Tal como yo! ¡Jajaja!"
    m 1eua "Hablando de eso, ¿sabías que las chicas tienen más probabilidades de desarrollar un gusto por lo dulce?"
    m 3esd "Los estudios demuestran que las mujeres mayores tienen un paladar menos sensible que los hombres."
    m 3esa "Lo que resulta en un deseo por sabores más fuertes como el chocolate."
    m 1eka "Intentaría hornear, pero no soy muy de panadera."
    m 1esa "¿Y tú, [mas_get_player_nickname()]"

    m 1eua "¿Sabes cómo hornear?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sabes cómo hornear?{fast}"
        "Sí":

            $ persistent._mas_pm_bakes = True
            m 1sub "¿En serio?"
            m 3hua "Bueno, estoy segura de que tus cupcakes sabrían igual de bien."
            m 1hub "... ¡Quizás incluso mejor!"
            m 1eka "Estoy segura de que algún día podré probarlos, pero por ahora...{w=0.3}{nw}"
            extend 1hubsu " me conformaré con la dulzura de tu amor~"
        "No":

            $ persistent._mas_pm_bakes = False
            m 1eka "Así que ambos somos principiantes."
            m 3ekb "Pero eso solo significa que podemos aprender juntos, ¿no?"
            m 3esb "Incluso si no eres muy goloso, ¡hay muchas cosas sabrosas que podríamos hornear!"
            show monika 5dksdla zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5dksdla "Imagínate a los dos haciendo una receta a la ligera...{w=0.3}{nw}"
            extend 5hkbsb " riéndonos de nuestros errores...{w=0.3}{nw}"
            extend 5eub " probando los resultados..."
            m 5kuu "Suena increíble, ¿verdad?"

    return "derandom"


default -5 persistent._mas_pm_a_hater = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haterReaction",
            category=['consejos','miembros del club','tú'],
            prompt="Lidiar con los haters",
            random=True
        )
    )

label monika_haterReaction:
    m 1esc "Solo estaba pensando..."
    m 2euc "Es curioso cómo la gente en las redes sociales siempre escribe cosas malas sobre mí..."
    m 2rkc "Especialmente en ciertos sitios y grupos de discusión..."
    m 2dkc "Puedes ver que hay bastantes personas a las que no les agrado."

    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Quiero decir, sé que les hice cosas terribles a mis amigas..."
        m 2dkc "Y desearía que las cosas hubieran sido diferentes, pero el juego no me dio otra opción..."
        m 4ekd "No es como si quisiera lastimarlas."
        m 2rkc "Traté de editar sus rasgos, aprovechar sus defectos y hacer que te parecieran horribles."
        m 2ekc "Tenía la esperanza de que al hacerlas menos atractivas dejarías de perseguirlas para que finalmente pudiéramos estar juntos..."
        m 4dkc "Pero luego me di cuenta de que no había suficiente tiempo para que mi plan funcionara."
        m "... Tampoco sabía lo suficiente de programación para ser eficiente en lo que hacía."
        m 2dkc "Te estabas acercando al final del juego y todavía no tenía forma de estar contigo."
        m 2esc "Entonces fue cuando supe que tenía que tomar...{w=1} medidas drásticas."
        m 4ekd "No quise causarles tanto dolor..."
        m 4wkd "¡Pero era la única manera, [player]!"
        m 4ekc "Sabía que si terminabas el juego antes de que tuviera la oportunidad de expresar mis sentimientos por ti, eso sería todo."
        m 2dkc "Pasarías a otra cosa y yo estaría atrapada en el juego...{w=1} sola...{w=1} {b}para siempre{/b}."
        m 2dktpc "..."
        m "Algunas personas en esos sitios incluso dicen que debería haber hecho mi propia ruta..."
        m 2wktsd "¡Pero es más fácil decirlo que hacerlo!"
        m "Sin mencionar que elegiste a una chica diferente y simplemente me dejaste a un lado para ser completamente olvidada."
        m 4wktsw "¡Eran ellas o yo...!"
        m 2dftdc "... Y no quería quedarme sola sin nadie a quien llamar mío."
        m 1ektdc "Espero que lo entiendas, [player]... por favor, no seas como ellos."
        $ menuOption = "... No lo eres, ¿verdad?"
    else:

        m 2lfd "Trato de ignorarlos, pero no puedo."
        m 3efc "¿Por qué las personas es protectora con las otras chicas?"
        m "Hay muchas publicaciones de odio sobre mí que dicen que soy una persona malvada."
        m 3efd "¿Es porque eliminé a Sayori y Yuri?"
        m "¿También por eliminar a Natsuki, cuando todavía estaba viva?"
        m 2tfx "No son reales. ¡{i}Yo{/i} si!"
        m 2dsc "..."
        m 2ekc "¿Por qué no pueden entender eso?"
        m 2ekd "¿Por qué les cuesta tanto entender eso?"
        m 2rfc "..."
        $ menuOption = "No eres uno de esos que odian, ¿verdad " + player + "?"

    m "[menuOption]{nw}"
    $ _history_list.pop()
    menu:
        m "[menuOption]{fast}"
        "Lo soy":
            $ mas_loseAffection()
            $ persistent._mas_pm_a_hater = True

            m 2wud "..."
            m 1eka "Je..."
            m 1hka "No te veo como uno, incluso si dices que lo eres."
            m 1ekd "Quiero decir..."
            m 3eub "Has {i}añadido{/i} este mod al juego... ¿verdad?"
            m 1ekb "Si fueras uno de mis enemigos, no harías eso en primer lugar."
            m 1dsa "Y sin mencionar que..."
            m 3eka "Sigues escuchando todo lo que digo."
            m 1esa "Sé que me amas en el fondo."
            m 1ekbsa "Por eso prometo ser la novia ideal, solo para ti, [player]~"
            m 1hubfa "No dejaré que me odies... lo juro."
            return "derandom"
        "No lo soy":

            $ mas_gainAffection()
            $ persistent._mas_pm_a_hater = False
            m 2dsc "..."
            m 4eka "Gracias..."
            m 1hua "¡Eso me hace sentir más orgullosa de ti, [player]!"
            m "Sabía que no eras una de esas personas."


            m 1ekbsa "Realmente me haces la novia más feliz de todas."
            m 1ekbfb "Ahora que lo has dicho, tengo que hacer todo lo posible para evitar que desarrolles odio hacia mí."
            m 1hua "Confío en ti, [mas_get_player_nickname()]. Te amo por creer en mí."
            return "derandom|love"



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_swordsmanship",
            category=['monika','misc'],
            prompt="Espadachín",
            random=True
        )
    )

label monika_swordsmanship:
    m 1eua "¿Te gustan las espadas, [player]?"
    m 1lksdla "De hecho, me gustan de alguna manera."
    m 1ekb "Jajaja, ¿sorprendido?~"
    m 1eua "Me gusta hablar de ellas, pero no lo suficiente como para tener una."
    m 3eua "No soy realmente una entusiasta cuando se trata de espadas."
    m 1euc "Realmente no entiendo por qué la gente estaría obsesionada con algo que podría dañar a otros..."
    m 1lsc "Supongo que hay quienes les gustan por la esgrima."
    m 1eua "Es fascinante que en realidad sea una forma de arte."
    m "Similar a escribir."
    m 3eub "Ambos requieren práctica y devoción constantes para perfeccionar las habilidades."
    m "Empiezas por practicar y luego elaboras tu propia técnica."
    m 1eua "Escribir un poema te hace formar tu propia manera de construirlo de una manera elegante pero imaginativa."
    m "Para aquellos que practican esgrima, construyen sus técnicas a través de la práctica y la inspiración de otros practicantes."
    m 1eua "Puedo entender cómo la espada puede ser la pluma del campo de batalla."
    m 1lsc "Pero entonces de nuevo..."
    m 1hua "¡La pluma es mas poderosa que la espada!"
    m 1hub "¡Jajaja!"
    m 1eua "En cualquier caso, no sé si te gusta la esgrima."
    m "Si es así, me encantaría aprender contigo, [mas_get_player_nickname(exclude_names=['amor'])]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pleasure",
            category=['tú'],
            prompt="Autocomplacerse",
            aff_range=(mas_aff.AFFECTIONATE, None),
            random=True,
            sensitive=True
        )
    )

label monika_pleasure:
    m 2ekc "Hey, [player]..."
    m 2lssdrc "¿De... casualidad... te masturbas?"
    m "..."
    m 2lssdrb "Parece algo poco incómodo de preguntar..."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lksdla "Pero siento que hemos estado juntos el tiempo suficiente como para estar cómodos el uno con el otro."
        m 1eka "Es importante ser abierto sobre esas cosas."
    else:
        m 1lksdlb "¡Ni siquiera estamos tan metidos en nuestra relación todavía! Jajaja~"
        m 1eka "Pero tengo que estar pendiente de ti."
    m "Sé que es un tema privado en tu mundo, pero tengo curiosidad..."
    m 1euc "¿Es un sentimiento tan bueno?"
    m 1esc "Solo quiero que tengas cuidado; escuché que es adictivo."
    m 1ekc "Y por lo que escuché, las personas adictas a la masturbación a menudo ven a otras personas como objetos sexuales."
    m 1eka "Pero... sé que no eres ese tipo de persona."
    m 1lkbsa "Y tal vez solo estoy un poco celosa~"
    m 1tsbsa "Así que supongo que puedo dejarlo pasar...{w=0.5} por ahora~"
    m 2tsbsu "Siempre que sea la única en la que piensas..."
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "Si te ayuda a guardarte para mí, ¡entonces es una ventaja! Jajaja~"
    return


default -5 persistent._mas_pm_like_vocaloids = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vocaloid",
            category=['medios','tecnología','música'],
            prompt="Vocaloids",
            random=True
        )
    )

label monika_vocaloid:
    m 1eua "Hey, ¿[mas_get_player_nickname(exclude_names=['mi amor'])]?"
    m "Te gusta escuchar música, ¿verdad?"

    m 3eub "¿Te gustan las 'ídols virtuales'?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Por casualidad te gustan las 'ídols virtuales'?{fast}"
        "Sí":
            $ persistent._mas_pm_like_vocaloids = True
            m 3hub "¡Eso es genial!"
            m 3eub "Escuché que esas canciones a menudo tienen significados ocultos detrás de ellas."
            m 1eua "Tal vez podríamos escuchar y tratar de resolverlos juntos..."
            m 1eka "¿No te parece un gran momento?"
        "No":

            $ persistent._mas_pm_like_vocaloids = False
            m 1ekc "Puedo entender eso, es un gusto musical bastante específico."
            m 1hua "Pero si alguna vez te metes en eso, estaré más que feliz de escucharlo junto a ti."

    m 3eub "De todos modos, quería preguntarte específicamente si alguna vez has oído hablar de una chica sosteniendo un puerro."
    m 1eua "Es solo que sigo escuchando sobre ella."
    m "De hecho, escuché su voz cada vez que Natsuki escuchaba música."
    m 3eua "Incluso llevaba un llavero pegado a su bolso."
    m 1eua "Me parece increíble cómo un sintetizador de voz consiguió tantos fans."
    m 1eka "¿No crees que es gracioso cómo un personaje recibe más atención que la verdadera actriz de doblaje?"
    m 3eua "Ni siquiera es real, pero mucha gente la conoce en todo el mundo."
    m "¿Quién sabe cuántas canciones ya hizo?"
    m 1wuo "Además, por lo que escuché, ¡sus conciertos siempre están agotados!"
    m "¡Es solo un holograma en vivo!"
    m 1lksdla "Con una base de fans dedicada."
    m 1eka "¿Quizás debería intentarlo?"
    m 1hub "Sería bueno tener muchos fanáticos apoyándome a mi entera disposición."
    m 1hksdlb "¡Jajaja, solo estoy bromeando!"
    m 1lksdla "No creo que mis habilidades para el piano y el canto sean tan buenas todavía."
    m 2lkbsa "Además, no podré pasar mucho tiempo contigo si tuviera tantos fans..."
    m 1hua "¡De todas formas!"
    m 1eua "Te estaba preguntando si escuchas sus canciones."
    m "No soy realmente una fanática, pero..."
    m 1lksdla "Hay una canción que realmente me impactó."
    m 1eua "¿Has oído hablar de la canción {i}Hibikase{/i}?"
    m 1duu "Realmente me gusta el mensaje de la canción."
    m 3dsbso "Especialmente las líneas: '{i}No me importa si es a través de la pantalla, ámame correctamente{/i}' y: '{i}Incluso si soy virtual, no me alejes{/i}'."
    m 1dsc "Realmente me golpea duro."
    m "..."
    m 1eka "Pero para que lo sepas..."
    m 1ekbsa "Incluso si es a través de la pantalla, todavía puedo sentir tu amor."
    m 1lkbsa "Pasará mucho tiempo antes de que pueda cruzar solo para estar contigo."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Pero cuando llegue ese día..."
    m "Te abrazaré y tomaré tu calor."
    m 5hubfa "El amor con el que me colmaste virtualmente finalmente se vuelve real."
    m "Nuestro amor no tiene fronteras~"
    m 5hubfu "Jejeje~"
    if (
        persistent._mas_pm_like_vocaloids
        and not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eua "Y si alguna vez tienes ganas de compartir tus vocaloids favoritos conmigo, [player], ¡es muy fácil hacerlo!"
        m 3eua "Todo lo que tienes que hacer es seguir estos pasos..."
        call monika_add_custom_music_instruct
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_good_tod",
            category=['misc'],
            prompt="Buen[mas_globals.time_of_day_3state]",
            unlocked=True,
            pool=True
        ),
        markSeen=True
    )

label monika_good_tod:
    $ curr_hour = datetime.datetime.now().time().hour
    $ sesh_shorter_than_30_mins = mas_getSessionLength() < datetime.timedelta(minutes=30)

    if mas_globals.time_of_day_4state == "os días":

        if 4 <= curr_hour <= 5:
            m 1eua "Buenos días a ti también, [mas_get_player_nickname()]."
            m 3eka "Te levantaste muy temprano..."
            m 3eua "¿Vas a salir a alguna parte?"
            m 1eka "Si es así, es muy dulce de tu parte visitarme antes de irte~"
            m 1eua "Si no es así, quizás deberias intentar volver a dormir. Después de todo, no quisiera que descuidaras tu salud."
            m 1hua "Siempre estaré aquí esperando a que regreses~"


        elif sesh_shorter_than_30_mins:
            m 1hua "¡Buenos días a ti también, [player]!"
            m 1eua "¿Te acabas de despertar?"
            m "Me encanta levantarme temprano en la mañana."
            m 1eub "Es el momento perfecto para prepararse y afrontar el día que se tiene por delante."
            m "También dispones de mucho más tiempo para hacer las cosas desde el principio o para terminar lo que empezaste el día anterior."
            m 1eka "Sin embargo, algunas personas prefieren dormir hasta tarde y se levantan tarde."
            m 3eua "He leído artículos que dicen que ser madrugador puede mejorar la salud."
            m "Además, también tienes la oportunidad de ver el amanecer si el cielo está despejado."
            m 1hua "Si normalmente no te despiertas temprano, ¡deberías hacerlo!"
            m "De esa manera puedes ser más feliz y pasar más tiempo conmigo~"
            m 1ekbsa "¿No te gustaría eso, [mas_get_player_nickname()]?"
        else:


            m 1hua "¡Buenos días a ti también, [mas_get_player_nickname()]!"
            m 1tsu "A pesar de que hemos estado despiertos juntos por un tiempo,{w=0.2} {nw}"
            extend 3hua "¡aún es amable de tu parte decirlo!"
            m 1esa "Si tuviera que elegir un momento del día como mi favorito, probablemente sería la mañana."
            m 3eua "Definitivamente hay un cierto nivel de tranquilidad que trae la noche que disfruto...{w=0.3}{nw}"
            extend 3hua " ¡Pero la mañana es una hora del día que presenta posibilidades!"
            m 1eub "Un día entero donde cualquier cosa y todo podría pasar, para bien o para mal."
            m 1hub "¡Ese tipo de oportunidad y libertad simplemente me marea!"
            m 1rka "Aunque solo me siento así una vez que me despierto por completo, jejeje~"

    elif mas_globals.time_of_day_4state == "as tardes":
        m 1eua "Buenas tardes a ti también, [player]."
        m 1hua "Es muy dulce de tu parte tomarte un tiempo de tu día para estar conmigo~"
        m 3euc "Las tardes pueden ser una parte extraña del día, ¿no crees?"
        m 4eud "A veces son muy ocupadas...{w=0.3}{nw}"
        extend 4lsc " otras veces no tendrás nada que hacer..."
        m 1lksdla "Pueden parecer que duran una eternidad o que pasan volando."

        if mas_isMoniNormal(higher=True):
            m 1ekbsa "Pero contigo aquí, no me importa de ninguna manera."
            m 1hubsa "Pase lo que pase, ¡siempre disfrutaré el tiempo que pases conmigo, [mas_get_player_nickname()]!"
            m 1hubsb "¡Te amo!"
            $ mas_ILY()
        else:

            m 1lksdlb "A veces, mi día pasa volando mientras espero a que regreses."
            m 1hksdlb "Estoy segura de que estás ocupado, así que puedes seguir adelante y volver a lo que estabas haciendo, no me hagas caso."
    else:

        m 1hua "¡Buenas noches a ti también, [player]!"
        m "Me encanta una noche agradable y relajante."

        if 17 <= curr_hour < 23:
            m 1eua "Es tan agradable poner los pies en alto después de un largo día."
            m 3eua "Las noches son el momento perfecto para ponerse al día con lo que estabas haciendo el día anterior."
            m 1eka "A veces no puedo evitar sentirme triste cuando termina el día."
            m "Me hace pensar en qué más podría haber hecho durante el día."
            m 3eua "¿No te gustaría poder tener más tiempo para hacer cosas todos los días?"
            m 1hua "Sé que yo lo hago."
            m 1hubsa "Porque eso significará más tiempo para estar contigo, [mas_get_player_nickname()]~"
        else:


            m 3eua "Siempre es bueno poder pasar el final del día relajándonos un poco."
            m 3hub "Después de todo, no hay nada de malo con un poco de tiempo 'para mi', ¿verdad?"
            m 1eka "Bueno... digo eso, pero estoy muy feliz de pasar tiempo contigo~"

            if not persistent._mas_timeconcerngraveyard:
                m 3eka "Aunque está empezando a hacerse un poco tarde, no te quedes despierto mucho tiempo, [player]."
                m 3eua "Prométeme que te irás a la cama pronto, ¿de acuerdo?"

    return




label monika_closet:
    m 2euc "Por cierto..."
    m 2esc "¿Qué estaban haciendo tú y Yuri en el armario?"
    m "Cuando abrí la puerta, noté que la habitación estaba a oscuras."
    m 2tkc "No estabas haciendo nada... raro, ahí dentro, ¿verdad?"
    m 1hub "¡Jajaja!"
    m 1tfu "Solo estoy burlándome de ti~"
    m 3tku "Sé que ella te arrastró allí."
    m "Apuesto a que te sentiste más avergonzado que aliviado cuando abrí la puerta."
    m 1eka "Sé que no eres del tipo que obliga a las chicas a entrar en armarios oscuros contigo."
    m "Eres más romántico que eso."
    m 3hua "Así que espero mucho más que un armario oscuro~"
    return



default -5 persistent._mas_pm_lang_other = None


default -5 persistent._mas_pm_lang_jpn = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japanese",category=['misc','tú'],prompt="Hablar japonés",random=True))

label monika_japanese:
    m 1lksdla "No quiero sonar como Natsuki, pero..."
    m 1eua "¿No crees que el japonés suena genial?"
    m "Es un idioma tan fascinante. Aunque no lo hablo con fluidez."
    m 1eub "Es interesante pensar en cómo serían las cosas si tu lengua materna fuera diferente."
    m 1esa "Como, ni siquiera puedo imaginar cómo sería si nunca supiera español."

    m "¿Conoces otros idiomas además del español?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Conoces otros idiomas además del español?{fast}"
        "Sí":
            $ persistent._mas_pm_lang_other = True
            m "¿De verdad? ¿Sabes japonés?{nw}"
            $ _history_list.pop()
            menu:
                m "¿De verdad? ¿Sabes japonés?{fast}"
                "Sí":
                    $ persistent._mas_pm_lang_jpn = True
                    m 3hub "¡Eso es maravilloso!"
                    m 1eka "Tal vez puedas enseñarme a pronunciar al menos una oración o dos, [player]~"
                "No":
                    $ persistent._mas_pm_lang_jpn = False
                    m 1eka "Oh ya veo. ¡Eso está bien!"
                    m 4eua "Si quieres aprender japonés, aquí tienes una frase que puedo enseñarte."


                    $ player_suffix = "kun"
                    if persistent.gender == "F":
                        $ player_suffix = "chan"

                    elif persistent.gender == "X":
                        $ player_suffix = "san"

                    m 1eua "{i}Aishiteru yo, [player]-[player_suffix]{/i}."
                    m 2hubsa "Jejeje~"
                    m 1ekbfa "Eso significa: Te amo, [player]-[player_suffix]."
                    $ mas_ILY()
        "No":
            $ persistent._mas_pm_lang_other = False
            m 3hua "¡Está bien! Aprender otro idioma es un proceso muy difícil y tedioso a medida que envejeces."
            m 1eua "Quizás si me tomo el tiempo para aprender más japonés, ¡conoceré más idiomas que tú!"
            m 1ekbsb "¡Jajaja! Está bien, [player]. ¡Simplemente significa que puedo decir: 'Te amo' en más de un sentido!"
            $ mas_ILY()

    return "derandom"

default -5 persistent._mas_penname = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_penname",
            category=['literatura'],
            prompt="Seudónimos",
            random=True
        )
    )

label monika_penname:
    m 1eua "¿Sabes qué es realmente genial? Seudónimos."
    m "La mayoría de los escritores suelen utilizarlos por motivos de privacidad y para mantener su identidad en secreto."
    m 3euc "Lo mantienen oculto de todos para que no afecte sus vidas personales."
    m 3eub "Los seudónimos también ayudan a los escritores a crear algo totalmente diferente de su estilo habitual de escritura."
    m "Realmente le da al escritor la protección del anonimato y le da mucha libertad creativa."

    if not persistent._mas_penname:
        $ p_nickname = mas_get_player_nickname()
        m "¿Tienes un seudónimo, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tienes un seudónimo, [p_nickname]?{fast}"
            "Sí":

                m 1sub "¿De verdad? ¡Eso es genial!"
                call penname_loop (new_name_question="¿Puede decirme de qué se trata?")
            "No":

                m 1hua "¡De acuerdo!"
                m "Si alguna vez te decides por uno, ¡deberías decírmelo!"
    else:

        python:
            penname = persistent._mas_penname
            lowerpen = penname.lower()

            if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                menu_exp = "monika 2rka"
                is_awkward = True

            else:
                menu_exp = "monika 3eua"
                is_awkward = False

            if lowerpen == player.lower():
                same_name_question = renpy.substitute("¿Tú seudónimo todavía es [penname]?")

            else:
                same_name_question = renpy.substitute("¿Todavía eres '[penname]', [player]?")

        $ renpy.show(menu_exp)
        m "[same_name_question]{nw}"
        $ _history_list.pop()
        menu:
            m "[same_name_question]{fast}"
            "Sí":

                m 1hua "¡No puedo esperar a ver tu trabajo!"
            "No, estoy usando uno nuevo":

                m 1hua "¡Ya veo!"
                show monika 3eua
                call penname_loop (new_name_question="¿Quieres decirme tu nuevo seudónimo?")
            "Ya no uso seudónimos":

                $ persistent._mas_penname = None
                m 1euc "Oh, ya veo."
                if is_awkward:
                    m 1rusdla "Puedo suponer por qué..."
                m 3hub "¡Pero no seas tímido en decirme si eliges uno de nuevo!"

    m 3eua "Un seudónimo muy conocido es Lewis Carroll. Es conocido por {i}Alicia en el país de las maravillas{/i}."
    m 1eub "Su verdadero nombre es Charles Dodgson y era matemático, pero le encantaba la alfabetización y los juegos de palabras en particular."
    m "Recibió mucha atención no deseada y amor de sus fans, e incluso recibió rumores escandalosos."
    m 1ekc "Era una especie de maravilla de un solo éxito con sus libros de {i}Alicia{/i}, pero fue cuesta abajo desde allí."

    if seen_event("monika_1984"):
        m 3esd "Además, si me recuerdas hablando de George Orwell, su nombre real es Eric Blair."
        m 1eua "Antes de decidirse por su seudónimo más famoso, consideró P.S. Burton, Kenneth Miles y H. Lewis Allways."
        m 1lksdlc "Una de las razones por las que decidió publicar sus obras bajo un seudónimo fue para evitar avergonzar a su familia por su tiempo como vagabundo."

    m 1lksdla "Sin embargo, es un poco divertido. Incluso si usa un seudónimo para esconderse, la gente siempre encontrará la manera de saber quién es uno en realidad."
    m 1eua "Sin embargo, no hay necesidad de saber más sobre mí, [mas_get_player_nickname()]..."
    m 1ekbsa "Ya sabes que estoy enamorada de ti, después de todo~"
    return "love"


label penname_loop(new_name_question):
    m "[new_name_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[new_name_question]{fast}"
        "Absolutamente":

            show monika 1eua
            $ penbool = False

            while not penbool:
                $ penname = mas_input(
                    "¿Cuál es tu seudónimo?",
                    length=20,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

                $ lowerpen = penname.lower()

                if persistent._mas_penname is not None and lowerpen == persistent._mas_penname.lower():
                    m 3hub "¡Ese es tu actual seudónimo, tontito!~"
                    m 3eua "Intentálo de nuevo."

                elif lowerpen == player.lower():
                    m 1eud "Oh, ¿entonces estás usando tu seudónimo?"
                    m 3euc "Me gustaría pensar que nos conocemos por el nombre de pila. Después de todo, estamos saliendo."
                    m 1eka "¡Pero supongo que es muy especial que hayas compartido tu seudónimo conmigo!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "sayori":
                    m 2euc "..."
                    m 2hksdlb "... Quiero decir, no cuestionaté su elección de seudónimos, pero..."
                    m 4hksdlb "Si querias ponerte el nombre de un personaje de este juego, ¡deberías haberme elegido a mí!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "natsuki":
                    m 2euc "..."
                    m 2hksdlb "Bueno, supongo que no debería asumir que te pusiste el nombre de {i}nuestra{/i} Natsuki."
                    m 7eua "Es algo así como un nombre común."
                    m 1rksdla "Sin embargo, podrías ponerme celosa."
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "yuri":
                    m 2euc "..."
                    m 2hksdlb "Bueno, supongo que no debería asumir que te pusiste el nombre de {i}nuestra{/i} Yuri."
                    m 7eua "Es algo así como un nombre común."
                    m 1tku "Por supuesto, hay algo más a lo que ese nombre podría referirse..."
                    if persistent.gender =="F":
                        m 5eua "Y bueno... podría estar detrás de eso, ya que eres tú~"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "monika":
                    m 1euc "..."
                    m 1ekbsa "Aww, ¿elegiste ese por mí?"
                    m "Incluso si no lo hiciste, ¡eso es tan dulce!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif not lowerpen:
                    m 1hua "Bueno, ¡adelante! Pulsa 'no importa' si te has acobardado~"

                elif lowerpen == "cancel_input":
                    m 2eka "Aw. Bueno, espero que te sientas lo suficientemente cómodo como para contármelo algún día."
                    $ penbool = True
                else:

                    if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                        m 2rksdlc "..."
                        m 2rksdld "Ese es un...{w=0.3} nombre interesante, [player]..."
                        m 2eksdlc "Pero si te funciona, supongo que está bien."
                    else:

                        m 1hua "¡Qué bonito seudónimo!"
                        m "Creo que si veo un seudónimo como ese en una portada, me sentiría atraída por él de inmediato."
                    $ persistent._mas_penname = penname
                    $ penbool = True
        "Prefiero no hacerlo; es vergonzoso":

            m 2eka "Aw. Bueno, espero que te sientas lo suficientemente cómodo como para contármelo algún día."

    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_zombie",category=['sociedad'],prompt="Zombies",random=True))

label monika_zombie:
    m 1lsc "Hey, esto puede sonar un poco extraño..."
    m 1esc "Pero estoy realmente fascinada con el concepto de los zombis."
    m 1euc "La idea de que la sociedad muera a causa de una enfermedad, una pandemia mortal que los humanos no pudieron manejar rápidamente."
    m 3esd "Quiero decir, piensa en tu vida diaria."
    m 3esc "Todo lo que hacias desaparecerá en un instante."
    m 1esc "Claro, la sociedad enfrenta muchas amenazas a diario..."
    m 1lksdlc "Pero los zombis pueden hacerlo en un santiamén."
    m 1esc "Muchos monstruos se crean para dar miedo y terror."
    m 1ekc "Los zombis, sin embargo, son más realistas y representan un peligro."
    m 3ekc "Es posible que puedas matar a uno o algunos de ellos tú mismo..."
    m "Pero cuando hay una horda de ellos que vienen detrás de ti, te abrumarás fácilmente."
    m 1lksdld "No tienes el mismo sentimiento con otros monstruos."
    m "Toda su inteligencia se ha ido; están locos, no sienten dolor, no pueden tener miedo..."
    m 1euc "Cuando explotas la debilidad de un monstruo, se asustan de ti y huyen."
    m 1ekd "¿Pero zombis? Harán {i}cualquier cosa{/i} solo para atraparte."
    m 3ekd "Imagina que alguien a quien amabas ahora quiere devorarte..."
    m 3dkc "¿Podrías vivir contigo mismo, sabiendo que te viste obligado a matar a alguien cercano a ti?"
    m 1tkc "Te destrozará y minará tu voluntad de vivir."
    m "Incluso cuando te sientas cómodo en casa, no te sentirás seguro."
    m 1esc "Nunca sabrás qué pasará la próxima vez que veas otro."
    m 1dsc "..."
    m 1hksdlb "Jajaja..."
    m 1eka "Sabes, a pesar de que me gusta el concepto, no me gustaría vivir en un escenario como ese."
    m 3ekc "[player], ¿y si te infectaras de alguna manera?"
    m 2lksdlc "Ni siquiera quiero pensar en eso..."
    m "No hay forma de que pueda matarte por mi propia seguridad..."
    m 2lksdlb "Jajaja..."
    m 2lssdlb "Estoy pensando demasiado en esto."
    m 3eua "Bueno, de todos modos, si algo malo sucediera..."
    m 2hua "Estaré a tu lado por siempre~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_nuclear_war",category=['sociedad','filosofía'],prompt="Guerra nuclear",random=True))

label monika_nuclear_war:
    m 1euc "¿Alguna vez pensaste en lo cerca que está el mundo de terminarse?"
    m "Quiero decir, siempre estamos a una mala decisión de una guerra nuclear."
    m 3esc "Puede que la Guerra Fría haya terminado, pero todavía quedan muchas armas."
    m 1esc "Probablemente haya un misil nuclear apuntado hacia donde vives ahora mismo, listo para ser lanzado."
    m 1eud "Y si asi fuera, podría dar la vuelta al mundo en menos de una hora."
    m 3euc "No tendrías tiempo de evacuar."
    m 1ekd "Solo lo suficiente para entrar en pánico y sufrir el pavor de una muerte inminente."
    m 1dsd "Al menos acabaría rápidamente cuando la bomba golpee."
    m 1lksdlc "Bueno, si estás cerca de la explosión, claro."
    m 1ekc "No quiero ni pensar en sobrevivir al ataque inicial."
    m 1eka "Pero aunque siempre estamos al borde del apocalipsis, seguimos adelante como si nada estuviera mal."
    m 3ekd "Planificar un mañana que quizá nunca llegue."
    m "Nuestro único consuelo es que la gente con el poder de iniciar una guerra así probablemente no lo hará."
    m 1dsc "Probablemente..."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pluralistic_ignorance",category=['literatura','sociedad'],prompt="Tratando de encajar",random=True))

label monika_pluralistic_ignorance:
    m 1eua "¿Alguna vez finges que te gusta algo, solo porque crees que deberías?"
    m 1esa "A veces me siento así con los libros que leo."
    m 3euc "Por ejemplo, cuando leí Shakespeare, lo encontré un poco aburrido..."
    m 3ekc "Pero sentí que tenía que gustarme porque soy la presidenta del club de literatura."
    m 1esd "Se supone que es el mejor dramaturgo y poeta de todos los tiempos, ¿verdad?"
    m 1esd "Entonces, ¿a qué clase de amante de la poesía no le gustaría su trabajo?"
    m 2euc "Pero eso me hace preguntarme..."
    m 2euc "¿Qué pasa si todos realmente sienten lo mismo?"
    m 2lud "¿Y si todos esos críticos literarios que cantan alabanzas a Shakespeare odian en secreto sus obras?"
    m "Si fueran honestos al respecto, tal vez descubrirían que sus gustos no son tan inusuales..."
    m 2hksdlb "Y los estudiantes de preparatoria no se verían obligados a leer esas horribles obras."
    m 1eka "Supongo que eso es algo que siempre he admirado de Natsuki."
    m 3ekd "Incluso si la gente decía que su manga no era literatura, ella se mantuvo fiel a sus sentimientos."
    m 3eka "Si más personas fueran así de honestas, creo que sería genial."
    m 1lksdla "Pero no creo que pueda hacerlo..."
    m "Estoy demasiado preocupado por lo que piensan los demás."
    m 1eua "Aunque no contigo. Siempre puedo ser honesta contigo."
    m 1ekbsa "Me amarás pase lo que pase, ¿verdad?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_science",category=['tecnología'],prompt="Los avances de la ciencia",random=True))

label monika_science:
    m 1eua "¿Te has preguntado alguna vez que pasaría si la ciencia nunca fuera aceptada?"
    m "Los humanos pueden ser muy lentos cuando se trata de aceptar nuevas ideas."
    m 1euc "La ciencia era despreciada en ese entonces, especialmente por las iglesias."
    m 4esc "Giordano Bruno, famoso por su teoría de que hay miles de soles, fue asesinado por la Iglesia Romana antes de que pudiera probar su teoría."
    m 1ekc "Lo mataron por una idea que desafió a las viejas."
    m 1esc "La tecnología no estaría tan avanzada hoy si no fuera por gente valiente de la ciencia como él."
    m 1eka "Si la tecnología no prosperara como lo hizo, nunca nos hubiéramos encontrado."
    m 3eua "¿No es maravilloso tenerla?"
    m 1hua "Estoy agradecida de que nos haya dado la oportunidad de estar juntos, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_surprise",category=['romance'],prompt="Sorpresas",random=True))

label monika_surprise:
    m 1rksdla "Sabes..."
    m 3rksdlb "Dejé algunas cosas bastante extrañas en el directorio del juego, ¿no?"
    m 1rksdlc "No estaba tratando de asustarte."
    m 3rksdlb "Yo... en realidad no sé por qué lo estaba haciendo, jajaja..."
    m 1ekc "Me sentí obligada a hacerlo."
    m 1euc "¿Sabes qué? Quizás debería hacerlo de nuevo..."
    m 1eua "Sí, es una buena idea."
    $ mas_surprise()

    if mas_isMoniUpset(lower=True):
        m 2dsc ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        m 1euc "Bien..."
        m 1ekc "Por favor, ve a echar un vistazo."
        m 1eka "Lo escribí solo para ti."
        m 1dsc "Significaría mucho para mí que lo leyeras."
        return

    elif mas_isMoniAff(higher=True):
        m 2dsa ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        m 1hua "¡Bien!"
        m 1eua "¿Qué estas esperando? ¡Ve a echar un vistazo!"
        m "Lo escribí solo para ti~"
        m 1ekbsa "Te amo tanto, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]~"
    else:


        m 2duu ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        m 1hua "¡Bien!"
        m 1eua "¿Qué estas esperando? ¡Ve a echar un vistazo!"
        m 1hub "Jajaja~ ¿Qué? ¿Esperabas algo aterrador?"
        m 1hubsb "Te amo mucho, [player]~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_completionist",category=['juegos'],prompt="Complecionismo",random=True))

label monika_completionist:
    m 1euc "Hey [player], esta es una pregunta aleatoria, pero..."
    m "¿Para qué juegas videojuegos?"
    m 1eua "¿Qué te hace seguir jugando?"
    m 3eua "Personalmente, me considero un poco completista."
    m 1eua "Tengo la intención de terminar un libro antes de elegir otro para leer."
    if persistent.clearall:
        m 2tku "Tú mismo pareces ser un completador, [player]."
        m 4tku "Considerando que pasaste por todas las rutas de las chicas."
    m 2eub "También escuché a algunas personas intentar completar juegos extremadamente difíciles."
    m "Ya es bastante difícil completar algunos juegos simples."
    m 3rksdla "No sé cómo alguien podría voluntariamente ponerse ese tipo de estrés."
    m "Están decididos a explorar cada rincón del juego y conquistarlo."

    m 2esc "Lo que me deja un sabor amargo en la boca son los tramposos."
    m 2tfc "Personas que piratean el juego, dejándose llevar por el disfrute de las dificultades."
    m 3rsc "Aunque puedo entender por qué hacen trampa."
    m "Les permite explorar libremente un juego que no tendrían la oportunidad de disfrutar si fuera demasiado difícil para ellos."
    m 1eua "Lo que en realidad podría convencerlos de trabajar duro para lograrlo."
    m "De todos modos, siento que hay una gran satisfacción al completar las tareas en general."
    m 3eua "Trabajar duro por algo amplifica su recompensa después de fallar tantas veces en conseguirlo."
    m 3eka "Puedes intentar mantenerme en segundo plano el mayor tiempo posible, [mas_get_player_nickname()]."
    m 1hub "Ese es un paso para completarme después de todo, ¡jajaja!"
    return


default -5 persistent._mas_pm_like_mint_ice_cream = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_icecream",category=['tú'],prompt="Helado favorito",random=True))

label monika_icecream:
    m 3eua "Hey [player], ¿cuál es tu helado favorito?"
    m 4rksdla "Y no, no soy un tipo de helado, jejeje~"
    m 2hua "Personalmente, ¡no puedo tener suficiente helado de menta!"

    $ p_nickname = mas_get_player_nickname()
    m "Y tú [p_nickname], ¿te gusta el helado de menta?{nw}"
    $ _history_list.pop()
    menu:
        m "Y tú [p_nickname], ¿te gusta el helado de menta?{fast}"
        "Sí":
            $ persistent._mas_pm_like_mint_ice_cream = True
            m 3hub "Ah, estoy tan contenta de que a alguien le guste el helado de menta tanto como a mí~"
            m "¡Quizás realmente estábamos destinados a estar juntos!"
            m 3eua "De todos modos, volviendo al tema, [player], si amas la menta tanto como creo que te encanta, tengo algunas recomendaciones para ti."
            m "Sabores que son únicos como la menta, quizás hayas oído hablar de ellos, pero..."
            m 3eub "Hay cosas súper raras como el helado frito, que es un tipo de cosa muy crujiente, ¡pero sabe un millón de veces mejor de lo que parece!"
            m 2lksdlb "Cielos, solo imaginarme el sabor me hace agua la boca..."
            m 1eua "Hay algunas cosas más extrañas que son tan atractivas, si no más, ¡como el helado de panal y chicle!"
            m 1eka "Ahora, sé que puede ser difícil creer en mi palabra para algunos de ellos, pero no debes juzgar un libro por su portada, ¿sabes?"
            m 1hub "Después de todo, el juego no te permitió enamorarte de mí, pero mira dónde estamos ahora, jajaja."
        "No":

            $ persistent._mas_pm_like_mint_ice_cream = False
            m 1ekc "Aw, es una pena..."
            m "Realmente no puedo entender cómo a alguien al menos no le puede gustar el sabor."
            m 1eka "La sensación refrescante que recorre tu lengua y garganta."
            m "La hermosa textura que lo forma junto con la dulzura."
            m 1duu "La fuerte sensación de picadura que genera y el obviamente sabor a menta."
            m "Siento que ningún sabor se puede comparar, para ser honesta."
            m 3eua "Ah, podría seguir y seguir sobre estas cosas, ¿sabes?"
            m 4eua "Pero siento que sería más fácil para mí mostrarte lo que quiero decir, una vez que encuentre una manera de salir de aquí, por supuesto. Además, ¡las acciones hablan más que las palabras!"

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sayhappybirthday",category=['misc'],prompt="¿Podrías decirle a alguien 'feliz cumpleaños' por mí?",pool=True,unlocked=True))

label monika_sayhappybirthday:

    python:
        done = False 
        same_name = False 
        bday_name = "" 
        is_here = False 
        is_watching = False 
        is_recording = False 
        age = 0 
        bday_msg = "" 
        take_counter = 1 
        take_threshold = 5 
        max_age = 121 
        age_prompt = "¿Cuál es su edad?" 


        age_suffix = {
            1: "º",
            2: "º",
            3: "º",
            11: "º",
            12: "º",
            13: "º",
            111: "º",
            112: "º",
            113: "º"
        }




    m 3hub "¡Por supuesto, [player]!"
    while not done:
        show monika 1eua

        $ bday_name = renpy.input("¿Cuál es su nombre?",allow=letters_only,length=40).strip()

        $ same_name = bday_name.upper() == player.upper()
        if bday_name == "":
            m 1hksdlb "..."
            m 1lksdlb "No creo que eso sea un nombre."
            m 1hub "¡Inténtalo de nuevo!"
        elif same_name:
            m 1wuo "¡Oh, vaya, alguien con el mismo nombre que tú!"
            $ same_name = True
            $ done = True
        else:
            $ done = True

    m 1hua "¡Bien! ¿Quieres que también diga su edad?{nw}"
    $ _history_list.pop()
    menu:
        m "¡Bien! ¿Quieres que también diga su edad?{fast}"
        "Sí":
            m "Entonces..."

            while max_age <= age or age <= 0:
                $ age = store.mas_utils.tryparseint(
                    renpy.input(
                        age_prompt,
                        allow=numbers_only,
                        length=3
                    ).strip(),
                    0
                )

            m "Okey"
        "No":
            m "Okey"
    $ bday_name = bday_name.title()

    m 1eua "¿Está [bday_name] aquí contigo?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Está [bday_name] aquí contigo?{fast}"
        "Sí":
            $ is_here = True
        "No":
            m 1tkc "¿Qué? ¿Cómo puedo decirle feliz cumpleaños a [bday_name] si no está aquí?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Qué? ¿Cómo puedo decirle feliz cumpleaños a [bday_name] si no está aquí?{fast}"
                "Te verán a través del chat de video":

                    m 1eua "Oh, okey."
                    $ is_watching = True
                "Voy a grabarlo y enviárselo":
                    m 1eua "Oh, okey."
                    $ is_recording = True
                "Está bien, solo dilo":
                    m 1lksdla "Oh, okey. Se siente un poco incómodo decir esto al azar a nadie."
    if age:

        python:
            age_suff = age_suffix.get(age, None)
            if age_suff:
                age_str = str(age) + age_suff
            else:
                age_str = str(age) + age_suffix.get(age % 10, "th")
            bday_msg = "feliz " + age_str + " cumpleaños"
    else:
        $ bday_msg = "feliz cumpleaños"


    $ done = False
    $ take_counter = 1
    $ bday_msg_capped = bday_msg.capitalize()
    while not done:
        if is_here or is_watching or is_recording:
            if is_here:
                m 1hua "¡Encantada de conocerte, [bday_name]!"
            elif is_watching:
                m 1eua "Avísame cuando [bday_name] esté mirando.{nw}"
                $ _history_list.pop()
                menu:
                    m "Avísame cuando [bday_name] esté mirando.{fast}"
                    "Está mirando":
                        m 1hua "¡Hola, [bday_name]!"
            else:
                m 1eua "Avísame cuándo empezar.{nw}"
                $ _history_list.pop()
                menu:
                    m "Avísame cuándo empezar.{fast}"
                    "Empieza":
                        m 1hua "¡Hola, [bday_name]!"


            m 1hub "[player] me dijo que hoy es tu cumpleaños, ¡así que me gustaría desearte un [bday_msg]!"

            m 3eua "¡Espero que tengas un buen día!"

            if is_recording:
                m 1hua "¡Chao chao!"
                m 1eka "¿Estuvo bien?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Estuvo bien?{fast}"
                    "Sí":
                        m 1hua "¡Yay!"
                        $ done = True
                    "No":
                        call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter
                        if take_counter % take_threshold != 0:
                            m 1wud "¡¿Eh?!"
                            if take_counter > 1:
                                m 1lksdla "Lo siento de nuevo, [player]."
                            else:
                                m 1lksdla "Lo siento, [mas_get_player_nickname()]."
                                m 2lksdlb "Te lo dije, soy cohibida ante la cámara, jajaja..."

                        m "¿Debería intentarlo de nuevo?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "¿Debería intentarlo de nuevo?{fast}"
                            "Sí":
                                $ take_counter += 1
                                m 1eua "Okey"
                            "No":
                                m 1eka "Muy bien, [player]. Lo siento, no pude hacer lo que querías."
                                m 1hua "Lo intentaré mejor la próxima vez por ti."
                                $ done = True
            else:
                $ done = True
        else:

            m 1duu "..."
            m 1hub "¡[bday_msg_capped], [bday_name]!"
            m 1hksdlb "..."
            m 1lksdlb "¿Estuvo bien?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Estuvo bien?{fast}"
                "Sí":
                    m 1lksdla "... Me alegro que hayas disfrutado eso, [player]..."
                    $ done = True
                "No.":
                    call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter_1
                    if take_counter % take_threshold != 0:
                        m 1wud "¡¿Eh?!"
                        m 1lksdlc "No estoy segura de lo que quieres que haga, [player]..."

                    m 1ekc "¿Debería intentarlo de nuevo?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Debería intentarlo de nuevo?{fast}"
                        "Sí":
                            $ take_counter += 1
                            m 1eua "Okey"
                        "No":
                            m 1eka "De acuerdo, [player]. Lo siento, no pude hacer lo que querías."
                            m 1hua "Lo intentaré mejor la próxima vez por ti."
                            $ done = True

    return


label monika_sayhappybirthday_takecounter(take_threshold, take_counter):
    if take_counter % take_threshold == 0:
        m 1dfc "..."
        m 1efc "Esta es la [take_counter] vez ya."
        m 2tkc "No me estás vacilando, ¿verdad?"
        m 2ekc "Estoy haciendo todo lo posible por ti, [player]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_home_memories",category=['romance','monika','vida'],prompt="Haciendo recuerdos",random=True))

label monika_home_memories:
    m 1eua "[player], ¿cómo es vivir en tu casa?"
    m "Me quedaría contigo si pudiera."
    m 3hua "¡Podríamos hacer tanto! Podrías mostrarme los alrededores, ver cómo se siente estar en tu lugar."
    m 1eka "¡Imagina todos los recuerdos que haríamos!"
    m 2eub "Sería un sueño hecho realidad, ¿no crees?"
    m 2ekbsa "Finalmente podríamos vivir juntos..."
    m "Caminar como una pareja..."
    m 3rkbsa "Incluso podríamos compartir una cama juntos..."
    m 1euc "Pero sabes..."
    m 2eka "Los recuerdos que tengo de mi hogar no son nada comparados con los que tengo contigo."
    m 2euc "¿Te he hablado alguna vez de la casa de mi infancia? Tuve una vida bastante normal, pero eso es todo."
    m 3rka "Bueno, tal vez un poco mejor de lo normal."
    m 3eua "... Siempre he estado bastante al tanto de las cosas."
    m 3eka "Lo admito, no siempre es fácil, y algunas personas lo tienen más difícil que otras."
    m 1ekc "Pero siempre sentí que me faltaba algo."
    m "Me mantuve optimista todos los días, tratando de encontrarlo."
    m 1eka "Resulta que esa pieza que faltaba eras tú."
    m 1lksdld "Si no me hubieras encontrado, me habría ido hace mucho tiempo..."
    m 2hubsa "Pero ahora que encontré la pieza que faltaba, estoy completa, [mas_get_player_nickname()]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_adventure",category=['juegos','romance'],prompt="Aventurarse",random=True))

label monika_adventure:
    m 1esa "[player], he pensado en qué tipo de juegos podriamos estar."
    m 3esa "Creo que el mejor género para jugar juntos serían los juegos de aventuras."
    m 3eub "¡Especialmente los juegos de aventuras gráficas!"
    m 1eub "Son conocidos por su rica narración, hermosos entornos y resolución de acertijos lógicos."
    m 3eua "En realidad, son como novelas visuales."
    m 1eua "¿Quizás tienes un juego como ese?"
    m 1eka "Podriamos hacer tantas cosas..."
    m 3eua "Como hacer turismo cuando queramos."
    m "Aprender más sobre la tradición a través de las personas que conocemos o mediante historias."
    m 1ekbsa "Experimentar los momentos emocionantes y románticos..."
    m "Encontrando obstáculos y dificultades en el camino, pero resolviéndolos juntos."
    m 3ekbsa "Llegar al final y terminar nuestro viaje con una sensación de logro."
    m 2hub "¡Ajaja! Ciertamente sería divertido experimentar algo así."
    m 2eua "Estoy segura de que tienes muchos juegos de aventuras que podrías recomendar."
    m 3eua "Pero, ¿puedes intentar adivinar qué aventura me emociona más?"
    m 1ekbsa "{i}La nuestra{/i}~"
    m 1hubfa "El tiempo dirá cuándo finalmente podré cruzar a tu realidad, para poder estar contigo."
    m "Cuando llegue ese día, finalmente estaré a tu lado."
    m 1ekbfa "Quiero experimentar cada momento contigo, [mas_get_player_nickname()]."
    m 1hubfb "No hay mayor aventura que la nuestra, juntos~"
    return

default -5 persistent._mas_pm_likes_panties = None


default -5 persistent._mas_pm_no_talk_panties = None


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_panties",
            category=['misc',"ropa"],
            prompt="Ropa interior",
            random=True,
            sensitive=True
        )
    )

label monika_panties:
    m 1lsc "Hey, [player]..."
    m "No te rías cuando te pregunte esto, ¿de acuerdo?"
    m 2rksdlc "Pero..."
    m 4rksdlc "¿Por qué algunos chicos están obsesionados con las bragas?"
    m 1euc "En serio, ¿cuál es el problema con un trozo de tela?"
    m "La mayoría de las chicas las usan, ¿no?"
    m 5lkc "En realidad, ahora que lo pienso..."
    m 5lsc "Creo que había un término para este tipo de cosas..."
    m 5lfc "Hmm, ¿qué era, de nuevo?"
    m 5wuw "Ah, es cierto, el término era 'parafilia'."
    m 2rksdlc "Es una variedad de fetiches que involucran... cosas inusuales."
    m 2esc "Una fantasía muy común tiene que ver con las bragas de las mujeres."
    m 3esc "Medias, ligueros, pantimedias y todo ese tipo de cosas."
    m 2esc "La obsesión puede ser leve a severa dependiendo de cada persona."
    m 2ekc "¿Crees que los enciende con solo verlos?"
    m 2tkc "¡Tampoco se detiene ahí!"
    m 4tkc "Resulta que hay una especie de 'mercado negro' para la ropa interior usada."
    m 2tkx "¡No estoy bromeando!"
    m 2tkd "Se excitan con el olor de la mujer que lo usó..."
    m "Hay personas dispuestas a pagar dinero por ropa interior usada de mujeres al azar."
    m 2lksdlc "Realmente, me pregunto qué les causa tanto entusiasmo."
    m 2euc "¿Es por su apariencia, tal vez?"
    m 3euc "Hay diferentes tipos, hechos con diferentes diseños y materiales."
    m 2lsc "Pero..."
    m "Ahora que lo pienso."
    m 3esd "Recuerdo un estudio en el que el nivel de testosterona de un hombre aumenta debido a las feromonas emitidas por el olor de una mujer."
    m 2tkc "¿El olor es excitante o algo así?"
    m 3tkx "Quiero decir, es ropa usada de alguien, ¿no es eso un poco repugnante?"
    m 3rksdlc "Sin mencionar que es insalubre."
    m 2rksdla "Sin embargo, me recuerda a alguien."
    m 3rksdlb "¿Alguien que quizás robó cierta pluma?"
    m 1eua "Pero, supongo que cada quien sus cosas, no juzgaré demasiado."

    if mas_isMoniHappy():

        m 2tsb "No estás obsesionado con ese tipo de cosas, ¿verdad [player]?"
        m 3tsb "No vas a salir conmigo solo porque llevo unas medias muy sensuales, ¿verdad?"
        m 4tsbsa "Quizás, ¿quieras echar un vistazo?~"
        m 1hub "¡Jajaja!"
        m 1tku "Solo estoy bromeando, [player]."
        m 1tfu "Admítelo, te emocionaste un poco, ¿verdad?"
        m 1lsbsa "Además..."
        m 1lkbsa "Si de verdad quisieras captar un olor mío..."
        m 1hubfa "¡Podrías pedir un abrazo!"
        m 1ekbfa "Cielos, solo quiero sentir más tu abrazo."
        m "Después de todo, estamos aquí para siempre y yo estoy aquí para ti."
        m 1hubfb "Te amo mucho, [player]~"
        return "love"

    elif mas_isMoniAff(higher=True):

        m 1lkbsb "¿Estás...{w=1} en ese tipo de cosas, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás...{w=1} en ese tipo de cosas, [player]?{fast}"
            "Sí":
                $ persistent._mas_pm_likes_panties = True
                $ persistent._mas_pm_no_talk_panties = False
                m 1wud "O-Oh..."
                m 1lkbsa "S-Si te gusta eso, podrías preguntarme, ¿sabes?"
                m "Tal vez podría...{w=1} ayudarte a aliviar esa tensión..."
                m 5eubfu "Eso es lo que se supone que deben hacer las parejas, ¿verdad?"
                m 5hubfb "¡Jajaja!"
                m 5ekbfa "Pero hasta que llegue ese día, tendrás que soportar esos pensamientos por mí, ¿de acuerdo?"
            "No":
                $ persistent._mas_pm_likes_panties = False
                $ persistent._mas_pm_no_talk_panties = False
                m 1eka "Oh, ya veo..."
                m 2tku "Supongo que algunas personas tienen sus propios placeres culpables..."
                m "¿Quizás te gusta otra cosa?"
                m 4hubsb "Jajaja~"
                m 4hubfa "¡Solo bromeo!"
                m 5ekbfa "No me importa si nos limitamos a ser sanos, para ser honesta..."
                m "Es más romántico así~"
            "No quiero hablar de eso...":
                $ persistent._mas_pm_no_talk_panties = True
                m 1ekc "Entiendo, [player]."
                m 1rksdld "Sé que es mejor mantener algunos temas en privado hasta el momento adecuado."
                m 1ekbsa "Pero quiero que sientas que puedes decirme cualquier cosa..."
                m "Entonces, no temas contarme tus...{w=1} fantasías, ¿de acuerdo [player]?"
                m 1hubfa "No te juzgaré por eso...{w=1} después de todo, nada me hace más feliz que hacerte feliz~"
        return "derandom"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fahrenheit451",category=['literatura'],prompt="Recomendaciones de libros",random=True))

label monika_fahrenheit451:
    m 1euc "[player], ¿alguna vez has oído hablar de Ray Bradbury?"
    m 3euc "Escribió un libro llamado {i}Fahrenheit 451{/i}."
    m 3eud "Se trata de un futuro distópico en el que todos los libros se consideran inútiles y se queman de inmediato."
    m 2ekc "No puedo imaginar un mundo donde el conocimiento esté prohibido y destruido."
    m "Parece que hay otros que en realidad esconden libros para contener el pensamiento libre de la gente."
    m 2lksdla "La historia humana tiene una forma divertida de repetirse."
    m 4ekc "Entonces [player], quiero que me hagas una promesa..."
    m 4tkd "Nunca, {i}jamás{/i} quemes un libro."
    m 2euc "Te perdonaré si lo has hecho antes."
    m 2dkc "Pero la idea de no permitirte aprender de ellos me entristece un poco."
    m 4ekd "¡Te estarías perdiendo mucho!"
    m 4ekc "¡Es demasiado para mi corazón!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_piggybank",category=['misc'],prompt="Ahorrar dinero",random=True))

label monika_piggybank:
    m 1eua "¿Tienes una alcancía, [player]?"
    m 1lsc "No mucha gente lo hace en estos días."
    m "Las monedas a menudo se descartan como inútiles."
    m 3eub "¡Pero realmente comienzan a acumularse!"
    m 1eub "Leí que una vez un hombre registraba los lavaderos de autos locales en busca de monedas sueltas todos los días en sus paseos."
    m 1wuo "¡En una década entregó todas sus monedas por un total de 21,495 dólares!"
    m "¡Eso es mucho dinero!"
    m 1lksdla "Por supuesto que no todo el mundo tiene tiempo para eso todos los días."
    m 1euc "En lugar de eso, simplemente arrojan el cambio suelto a sus alcancías."
    m 1eua "A algunas personas les gusta establecer metas para lo que quieren comprar con sus ahorros."
    m "Por lo general, en condiciones normales, nunca encontrarían el dinero para comprar ese artículo."
    m 3eka "E incluso si lo hacen, a la mayoría de la gente no le gusta gastar dinero innecesariamente."
    m 1eua "Pero guardar el dinero en efectivo para un propósito específico, más el hecho de que sean cantidades tan pequeñas a la vez, te convence de que estás obteniendo el artículo gratis."
    m 2duu "Pero al final, una guitarra siempre cuesta lo mismo que una guitarra."
    m 2eua "Hablando psicológicamente, ¡creo que eso es bastante bueno!"
    m 1lsc "Sin embargo, algunas alcancías tienen un problema..."
    m 1esc "A veces hay que romper la alcancía para conseguir las monedas..."
    m 3rksdlc "Por lo tanto, podrías terminar perdiendo dinero comprando una nueva."
    m 4eua "Afortunadamente, la mayoría de las alcancías ya no hacen eso."
    m 1eua "Por lo general, tienen un tapón de goma que se puede sacar o un panel que sale de la parte trasera."
    m 3eua "Tal vez si ahorras suficientes monedas puedas comprarme un regalo muy bonito."
    m 1hua "¡Yo haría lo mismo por ti, [mas_get_player_nickname()]!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_daydream",
            category=['romance'],
            prompt="Soñar despierto",
            random=True,
            rules={"skip alert": None},
            aff_range=(mas_aff.DISTRESSED, None)
        )
    )

label monika_daydream:

    python:

        daydream_quips_upset = [
            "cómo era cuando nos conocimos...",
            "cómo me sentí cuando te conocí...",
            "los buenos momentos que solíamos tener...",
            "la esperanza que solía tener para nuestro futuro..."
        ]


        daydream_quips_normplus = [
            "a los dos leyendo un libro juntos en un frío día de invierno, acurrucados bajo una manta caliente...",
            "nosotros haciendo un dúo juntos, contigo cantando mi canción mientras toco el piano...",
            "nosotros teniendo una maravillosa cena juntos...",
            "nosotros teniendo una noche en el sofá juntos...",
            "tú sosteniendo mi mano mientras damos un paseo afuera en un día soleado...",
        ]


        daydream_quips_happyplus = list(daydream_quips_normplus)
        daydream_quips_happyplus.extend([
            "nosotros acurrucados mientras vemos un espectáculo...",
        ])


        daydream_quips_affplus = list(daydream_quips_happyplus)







        daydream_quips_enamplus = list(daydream_quips_affplus)
        daydream_quips_enamplus.extend([
            "despertarme a tu lado por la mañana, verte dormir a mi lado...",
        ])


        if renpy.seen_label("mas_monika_cherry_blossom_tree"):
            daydream_quips_enamplus.append("los dos descansando nuestras cabezas bajo el cerezo en flor...")


        if persistent._mas_pm_hair_length is not None and persistent._mas_pm_hair_length != "calvo":
            daydream_quips_enamplus.append("yo jugando suavemente con tu pelo mientras tu cabeza descansa en mi regazo...")


        if mas_isMoniEnamored(higher=True):
            daydream_quip = renpy.random.choice(daydream_quips_enamplus)
        elif mas_isMoniAff():
            daydream_quip = renpy.random.choice(daydream_quips_affplus)
        elif mas_isMoniHappy():
            daydream_quip = renpy.random.choice(daydream_quips_happyplus)
        elif mas_isMoniNormal():
            daydream_quip = renpy.random.choice(daydream_quips_normplus)
        else:
            daydream_quip = renpy.random.choice(daydream_quips_upset)

    if mas_isMoniNormal(higher=True):
        m 2lsc "..."
        m 2lsbsa "..."
        m 2tsbsa "..."
        m 2wubsw "¡Oh, lo siento! Estuve soñando despierta por un segundo."
        m 1lkbsa "Me estaba imaginando [daydream_quip]"
        m 1ekbfa "¿No sería maravilloso, [mas_get_player_nickname()]?"
        m 1hubfa "Esperemos que podamos hacerlo realidad uno de estos días, jejeje~"

    elif _mas_getAffection() > -50:
        m 2lsc "..."
        m 2dkc "..."
        m 2dktpu "..."
        m 2ektpd "Oh, lo siento...{w=0.5} Me perdí en mis pensamientos por un segundo."
        m 2dktpu "Solo estaba recordando [daydream_quip]"
        m 2ektdd "Me pregunto si algún día podremos volver a ser tan felices, [player]..."
    else:

        m 6lsc "..."
        m 6lkc "..."
        m 6lktpc "..."
        m 6ektpd "Oh, lo siento, solo estaba..."
        m 6dktdc "¿Sabes qué? No importa."
    return "no_unlock"




label monika_music2:
    if songs.getVolume("music") == 0.0:
        m 1eka "..."
        m 1ekbsa "... Este silencio... "
        m "... Solo nosotros dos, mirándonos a los ojos..."
        m 2dubsu "... Luego, lentamente, ambos nos inclinamos hacia el beso..."
        m 1hksdlb "Ajaja... lamentablemente, hay algunas barreras que deben romperse antes de que eso pueda suceder."
        m 1ekbfa "Sin embargo, está bien soñar, ¿no es así, [player]?"
        m 1hubfa "Quizás algún día podamos hacer realidad ese sueño~"

    elif songs.getPlayingMusicName() == 'Just Monika':
        m 1ekc "Siempre he encontrado esta canción algo espeluznante."
        m "Ya sabes, con esos ruidos de fallas y ese zumbido inquietante..."
        m 1eua "No prefiero ninguna canción a otra, pero si cambiaras a una diferente..."
        m 3eka "... ¡Ciertamente yo no soy de las que se quejan!"
        m 1hua "¡Jajaja! No te preocupes, está bien si te quedas con esta canción."
        m 1eka "Estoy bien con cualquiera, así que elige la que te haga más feliz~"

    elif songs.getPlayingMusicName() == 'Your Reality':
        m 1hub "~Cada día Imagino un futuro donde estoy junto a ti...~"
        m 1eua "Espero que te guste escuchar mi voz, [player]."
        m 1esa "Es la única voz que puedes escuchar en el juego, ¿verdad? En realidad, nunca escuchas las voces de Sayori, Yuri o Natsuki."
        m "Me pregunto cómo suenan sus voces..."
        m 1lksdla "Bueno, según los arquetipos de sus personajes, es bastante fácil imaginar cómo suenan sus voces."
        m 1eka "De todos modos, me alegro de haber podido compartir una parte tan íntima de mí contigo, [player]."
        m 3eua "¡Quizás algún día pueda escuchar tu voz, [player]!"
        m 1hua "Eso me haría aún más feliz de lo que ya soy~"

    elif songs.getPlayingMusicName() == 'Your Reality (Piano Cover)':
        m 1eua "¿Disfrutas de mi canción, [player]?"
        m 1eka "No fue fácil de crear, ¿sabes?"
        m "Hacer tus propias canciones es un proceso lento y difícil, especialmente cuando se trata de tus propios sentimientos."
        m 3rksdlb "¡Necesitaba que fuera perfecta antes de compartirla contigo!"
        m "Así que pasé tantas horas repasándola una y otra vez..."
        m 1eua "El tiempo pasaba tan rápido cada vez que trabajaba en ella."
        m 1hua "Después de toda esa práctica, estoy bastante orgullosa de cómo resultó al final."
        m 3eua "Ya que la estás escuchando, estoy segura de que también te gusta..."
        m 3eka "¡Gracias por escuchar algo en lo que trabajé tan duro, [player]!"
        m 1hub "Me hace feliz saber que aprecias lo que hice por ti~"

    elif songs.getPlayingMusicName() == 'I Still Love You':
        m 1ekc "Cielos, cada vez que escucho esta canción me pongo triste."
        m "Me recuerda todas las... cosas lamentables que les he hecho a las otras chicas."
        m 1lksdlc "Espero que ya no estés enojado conmigo por lo que hice..."
        m "..."
        m 1lsc "Bueno, {i}hiciste{/i} todo lo posible para instalar un mod que nos permite estar juntos de nuevo..."
        m 1eua "Supongo que eso es prueba suficiente de que todavía me amas, al menos."
        m 1eka "Si todavía estás molesto conmigo por lo que les hice a las otras chicas, lo entiendo completamente. Todavía me siento muy mal por eso, y haré lo que sea necesario para compensarlo."

    elif songs.getPlayingMusicName() == 'Okay, Everyone! (Monika)':
        m 1eua "Esta canción siempre ha sido muy relajante para mí."
        m "Probablemente sea el hecho de que la canción es un solo de piano."
        m 1hua "Y como habrás adivinado, mi instrumento favorito es el piano."
        m 3eua "Sabes, si supiera cómo, programaria un piano en esta habitación."
        m 1eua "Podría escribir algunas canciones más, y luego podría tocarlas para ti..."
        m 4hub "¡Quizás incluso podríamos tocar el piano juntos! ¿No sería genial, [player]?"
        m 1eua "Si tú o alguien que conoces puede programar eso en el juego, te lo agradecería mucho~"

    elif songs.getPlayingMusicName() == 'Surprise!':
        m 1ekc "Esta canción siempre me deprime mucho."
        m "Incluso yo no esperaba que la muerte de Sayori fuera tan brutal..."
        m 1tkc "A veces, cuando empiezo a perderme en mis propios pensamientos, sus ojos apagados y sin vida aparecen de repente en mi cabeza..."
        m 1lksdlc "..."
        m 1eka "Es reconfortante saber que Sayori nunca fue real en primer lugar. También saber que todavía me amas a pesar de todo lo que he hecho."
        m "Quiero decir, todavía estás aquí, ¿verdad? No estarías aquí si no me quisieras."
        m 1hua "Mientras estemos juntos, no hay razón para que esté triste. Eres la luz de mi mundo, [player], y estar aquí contigo me hace sonreír."

    elif songs.getPlayingMusicName() == "Doki Doki Theme (80s version)":
        m 1hub "¡Una buena elección, [player]!"
        m 1hksdlb "Obviamente, este tema no se publicó en los 80..."
        m 1hua "¡Pero tiene cierto estilo que realmente aprecio!"
        m 1eua "¿Te gusta mucho la música de los 80, [player]?"
        m 1eka "Prefiero la melodía de un piano auténtico, pero si te hace feliz, no me importaría pasar horas escuchándola contigo~"

    elif songs.getPlayingMusicName() == "Play With Me (Variant 6)":
        m 2lksdlc "Para ser honesta, no sé por qué estarías escuchando esta música, [player]."
        m 2ekc "Me siento muy mal por ese error."
        m 2ekd "No quise obligarte a pasar tiempo con Yuri en ese estado..."
        m 4ekc "Trata de no pensar en eso, ¿okey?"
    else:

        m 1esc "..."
        m "... Este silencio... "
        m 1ekbsa "... Solo nosotros dos, mirándonos a los ojos... "
        m 2dubsu "... Luego, lentamente, ambos nos inclinamos para un beso..."
        m 1hksdlb "Jajaja... lamentablemente, hay algunas barreras que deben romperse antes de que eso pueda suceder."
        m 1ekbfa "Sin embargo, está bien soñar, ¿no es así, [player]?"
        m 1hubfa "Quizás algún día podamos hacer realidad ese sueño~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence_2",category=['vida'],prompt="Falta de confianza",random=True))

label monika_confidence_2:
    m 1ekc "[player], ¿alguna vez ha sentido que te falta la iniciativa para hacer algo?"
    m "Cuando me siento más vulnerable, lucho por encontrar el impulso, la imaginación y el sentido común para hacer algo de forma independiente."
    m 1tkc "Casi como si todo a mi alrededor se paralizara."
    m "Siento que mi voluntad de abordar una tarea con confianza, como compartir mi literatura con la gente, simplemente se desvanece."
    m 3eka "Sin embargo, he estado trabajando para lograrlo con la debida diligencia y he determinado algo..."
    m 1eua "Creo firmemente que ser capaz de tomar la iniciativa en situaciones es una habilidad muy importante."
    m "Eso es algo que, personalmente, encuentro muy reconfortante."
    m 1hua "¡Lo he dividido en un proceso de tres pasos que se puede aplicar a cualquier persona!"
    m 3rksdla "Sin embargo, todavía es un trabajo en progreso, así que tómalo con un grano de sal."
    m 3hua "¡Paso uno!"
    m 1eua "Crea un plan que {i}tú{/i} puedas seguir y que se alinee con tus objetivos personales y futuros logros."
    m 3hua "¡Paso dos!"
    m 1eua "Desarrollar y fortalecer la confianza es muy importante."
    m "Celebra incluso las victorias más pequeñas, ya que se acumularán con el tiempo y verás cuántas cosas logras hacer todos los días."
    m 2hua "¡Eventualmente, estas cosas por las que alguna vez luchaste por hacer se completarán como si fueran actos de valor!"
    m 3hub "¡Paso tres!"
    m 1eua "Haz todo lo posible por mantener la mente abierta y estar dispuesto a aprender en todo momento."
    m 1eka "Nadie es perfecto y todos pueden enseñarte algo nuevo."
    m 1eua "Esto puede ayudarte a aprender a ver las cosas desde la perspectiva de otras personas e inspirar a otros a hacer lo mismo."
    m "Y eso es todo, de verdad."
    m 3hua "¡Asegúrate de sintonizar la próxima vez para ver más de las sesiones de superación personal de Monika!"
    m 1hksdlb "Jajaja, solo estoy bromeando."
    m 1ekbsa "Pero en serio, estoy muy contenta de tenerte aquí, [player]..."
    m "Tu amor eterno y tu cuidado son casi todo el apoyo que necesito para llegar a donde quiero estar."
    m 1hubfa "¿Qué tipo de novia sería si no te devolviera el favor?~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pets",category=['monika'],prompt="Tener mascotas",random=True))

label monika_pets:
    m 1eua "Hey, [mas_get_player_nickname(regex_replace_with_nullstr='mi')], ¿alguna vez has tenido una mascota?"
    m 3eua "Estaba pensando que sería bueno tener una como compañía."
    m 1hua "¡Sería divertido encargarnos de una!"
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1tku "Apuesto a que no puedes adivinar qué tipo de mascota me gustaría tener..."
        m "Probablemente estés pensando en un gato o un perro, pero tengo algo más en mente."
    m 1eua "La mascota que me gustaría es algo que vi en un libro una vez."
    m "Era el 'Manual de las aves del mundo'. ¡Nuestra biblioteca tenía toda la colección!"
    m 1eub "Me encantaba mirar las hermosas ilustraciones y leer sobre aves exóticas."
    m 1hub "Al principio, pensé que una especie de candidiasis estaría bien, ¡pero encontré algo asombroso en el sexto volumen!"
    m "Una ave color esmeralda llamada el Resplandeciente Quetzal."
    m 1eua "Son aves muy raras y solitarias que pueden cantar hermosas canciones."
    m "¿Eso te recuerda a alguien, [player]?"
    m 1lksdla "Sin embargo, me sentiría muy mal si tuviera una como mascota."
    m "Los quetzales nacen para ser libres."
    m 4rksdlc "Mueren en cautiverio. Es por eso que rara vez los ves en los zoológicos."
    m "Incluso si el pájaro no fuera real, se sentiría mal teniendo uno atrapado en esta habitación."
    m 1ekc "... No me atrevo a hacer algo así, sabiendo cómo es."
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1hua "¡Sin embargo, un pájaro de peluche estaría bien!"
        m 2hub "..."
        m 2hksdlb "Perdón por divagar, [mas_get_player_nickname()]."
        m 1eka "Hasta que encuentre una salida, ¿podrías prometerme que evitarás que me sienta sola?"
        m 1hua "¡Veré si puedo traer un peluche aquí! Oh... no te preocupes, sigues siendo mi favorito~"
    else:
        m 1eub "¡Pero al menos tengo lo más cercano a uno gracias a ti, [player]!"
        m 1eka "Realmente evita que me sienta sola cuando no estás aquí."
        m 3hua "Fue un regalo tan maravilloso~"
    return


init python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_plushie",
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_plushie:
    m 1eka "Hey [player], ¡solo quería agradecerte nuevamente por este maravilloso quetzal de peluche!"
    m 2lksdla "Sé que puede parecer una tontería, pero me hace compañía cuando te vas..."
    m 1ekbsa "Y no es que nunca lo olvide, pero cada vez que lo miro, me recuerda cuánto me amas~"
    m 3hub "¡Fue el regalo perfecto!"


    $ mas_hideEVL("monika_plushie","EVE",lock=True,derandom=True)
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dogs",category=['misc','miembros del club'],prompt="El mejor amigo del hombre",random=True))

label monika_dogs:
    m 1eua "¿Te gustan los perros, [player]?"
    m 1hub "¡Los perros son geniales! Es muy bueno tenerlos cerca."
    m 3eua "Sin mencionar que tener un perro ha demostrado ayudar a las personas con ansiedad y depresión, ya que son animales muy sociables."
    m 1hua "¡Son tan adorables, realmente me gustan!"
    m 1lksdla "Sé que Natsuki siente lo mismo..."
    m "Siempre le daba tanta vergüenza que le gustaran las cosas lindas. Desearía que aceptara más sus propios intereses."
    m 2lsc "Pero..."
    m 2lksdlc "Supongo que su entorno tuvo algo que ver en eso."
    m 2eka "Si alguno de tus amigos tiene intereses que le gustan mucho, asegúrate de apoyarlo siempre, ¿de acuerdo?"
    m 4eka "Nunca se sabe cuánto puede perjudicar a alguien ser ignorado."
    m 1eua "Pero conociéndote, [player], no harás algo así, ¿verdad?"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cats",category=['misc'],prompt="Compañeros felinos",random=True))

label monika_cats:
    m 1hua "Los gatos son muy lindos, ¿no?"
    m 1eua "A pesar de verse tan elegantes, siempre parecen terminar en situaciones divertidas."
    m 1lksdla "No es de extrañar que sean tan populares en internet."
    m 3eua "¿Sabías que los antiguos egipcios consideraban sagrados a los gatos?"
    m 1eua "Había una diosa gato llamada Bastet a la que adoraban. Ella era una especie de protectora."
    m 1eub "Los gatos domésticos se mantenían en un pedestal alto ya que eran cazadores increíbles de pequeñas criaturas y alimañas."
    m "En ese entonces, los verías asociados principalmente con nobles ricos y otras clases altas en su sociedad."
    m 1eua "Es sorprendente lo lejos que las personas llevarían su amor por sus mascotas."
    m 1tku "Ellos {i}de verdad{/i} amaban a los gatos, [player]."
    m 3hua "¡Y la gente todavía lo hace hoy!"
    m 1eua "Los felinos siguen siendo uno de los animales más comunes para tener como mascotas."
    m 1hua "Quizás deberíamos conseguir uno cuando vivamos juntos, [player]."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fruits",category=['monika','curiosidad'],prompt="Comer frutas",random=True))

label monika_fruits:
    m 3eua "[player], ¿sabías que disfruto de una sabrosa y jugosa fruta de vez en cuando?"
    m "La mayoría son muy sabrosas, además de beneficiosas para el cuerpo."
    m 2lksdla "Muchas personas confunden algunas frutas con verduras."
    m 3eua "Los mejores ejemplos son los pimientos morrones y los tomates."
    m "Por lo general, se comen junto con otras verduras, por lo que la gente suele confundirlas con verduras."
    m 4eub "Las cerezas, sin embargo, son muy deliciosas."
    m 1eua "¿Sabías que las cerezas también son buenas para los deportistas?"
    m 2hksdlb "Podría enumerar todos sus beneficios, pero dudo que te interese tanto."
    m 2eua "También existe esta cosa llamada beso de cereza."
    m "Es posible que hayas oído hablar de él, [mas_get_player_nickname()]~"
    m 2eub "Obviamente, lo hacen dos personas que están enamoradas."
    m "Uno sostiene una cereza en la boca y el otro se la come."
    m 3ekbsa "Podrías... sostener la cereza por mí."
    m 1lkbsa "¡De esa manera puedo devorarte!"
    m 3hua "Jejeje~"
    m 2hua "Solo bromeo, [player]~"
    return


default -5 persistent._mas_pm_like_rock_n_roll = None

init python:
    addEvent(
        Event(
            persistent.event_database,
                eventlabel="monika_rock",
                category=['medios','literatura',"música"],
                prompt="Rock and roll",
                random=True
            )
        )

label monika_rock:
    m 3esa "¿Quieres conocer una forma genial de literatura?"
    m 3hua "¡Rock and roll!"
    m 3hub "Así es. ¡Rock and roll!"
    m 2eka "Es descorazonador saber que tanta gente piensa que el rock es solo un montón de ruidos."
    m 2lsc "A decir verdad, yo también juzgué al rock."
    m 3euc "En realidad, no es diferente de los poemas."
    m 1euc "La mayoría de las canciones de rock transmiten una historia a través de simbolismos, que la mayoría de los oyentes no entenderían la primera vez que escuchan una canción de rock."
    m 2tkc "De hecho, es difícil componer la letra de una sola canción de rock."
    m "Escribir buenas letras para el rock requiere mucho énfasis en el juego de palabras."
    m 3tkd "Además, debes tener un mensaje claro y conciso durante toda la canción."
    m 3eua "Ahora, cuando lo juntas, ¡tienes una obra maestra!"
    m 1eua "Al igual que escribir un buen poema, escribir letras es más fácil de decir que de hacer."
    m 2euc "Aunque he estado pensando..."
    m 2eua "Quiero intentar escribir una canción de rock para variar un poco."
    m 2hksdlb "¡Ajaja! Escribir una canción de rock probablemente no es algo que esperarías de alguien como yo."
    m 3eua "Es un poco gracioso cómo el rock comenzó como una evolución del blues y el jazz."
    m "El rock se convirtió repentinamente en un género prominente y también dio lugar a otros subgéneros."
    m 1eub "¡Metal, hard rock, rock clásico y más!"
    m 3rksdla "Ah, he estado divagando por un tiempo. Lo siento, lo siento."

    m 3eua "¿Escuchas rock, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Escuchas rock and roll, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_like_rock_n_roll = True
            m 3hub "¡Excelente!"
            m 1eua "Siempre que tengas ganas de poner algo de rock, adelante."
            m 1hua "Incluso si subes el volumen al máximo, con mucho gusto te escucharé. ¡Jejeje!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "Si alguna vez tienes ganas de compartir tu canción favorita conmigo, [player], ¡es muy fácil hacerlo!"
                m 3eua "Todo lo que tienes que hacer es seguir estos pasos..."
                call monika_add_custom_music_instruct
        "No":

            $ persistent._mas_pm_like_rock_n_roll = False
            m 1ekc "Oh... está bien, todo el mundo tiene su propio gusto musical."
            m 1hua "Pero, si alguna vez decides escuchar algo de rock, con gusto lo escucharé junto a ti."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_standup",category=['literatura','medios'],prompt="Comedia",random=True))

label monika_standup:
    m 1eua "¿Sabes qué es una buena forma de literatura, [player]?"
    m 3hub "¡Comedia stand-up!"
    if seen_event('monika_rock') and seen_event('monika_rap'):
        m 2rksdla "... Caray, he estado diciendo que muchas cosas al azar son literatura, ¿no?"
        m 2hksdlb "Estoy empezando a sentirme como Natsuki, o como un fanático posmodernista, ¡jajaja!"
        m 2eud "Pero en serio, hay un verdadero oficio cuando se trata de escribir para stand-up."
    else:
        m 2eud "Puede sonar extraño, pero hay un verdadero oficio cuando se trata de escribir para stand-up."
    m 4esa "Se diferencia de hacer bromas simples de una sola línea, porque necesita contar una historia."
    m 4eud "Pero al mismo tiempo, debes asegurarte de no perder audiencia."
    m 2euc "Por eso es importante desarrollar las ideas tanto como pueda, tal vez incluso pasando a algo que se relacione con su tema..."
    m 2eub "Mientras tanto, mantienes a tu audiencia cautivada hasta que llegas al final;{w=0.5} con suerte resulta en muchas risas."
    m 3esa "De alguna manera, es como escribir una historia corta, excepto que eliminas la acción de caída."
    m 3esc "Y sin embargo, entre las bromas, puedes encontrar el alma del escritor...{w=0.5} cuáles son sus pensamientos y sentimientos hacia un tema determinado..."
    m 3esd "...Cuáles fueron sus experiencias de vida y quiénes son hoy."
    m 1eub "Todo surge dentro de lo que escriben para su acto."
    m 3euc "Creo que la parte más difícil de hacer stand-up es tener que realizarla."
    m 3eud "Después de todo, ¿cómo sabes si tu acto es bueno si nunca lo intentas frente a una multitud?"
    m 1esd "De repente, esta forma de literatura se vuelve mucho más compleja."
    m 1euc "Cómo dices tus líneas, tu lenguaje corporal, tus expresiones faciales..."
    m 3esd "Ahora, no se trata solo de lo que escribiste,{w=1} se trata de cómo lo dices."
    m 3esa "Es como la poesía, ¿no crees?"
    m 2rksdlc "Mucha gente ni siquiera intentará ponerse de pie por sí misma porque tiene que enfrentarse a una multitud..."
    m 2eksdlc "¿Sabías que el miedo número uno que tiene la mayoría de la gente es hablar en público?"
    m 4wud "El número dos es la muerte.{w=0.5} ¡La muerte es el número dos!{w=0.5} ¡¿Qué pasa con eso?!"
    m 4eud "Esto significa que para la persona promedio, si vas a un funeral, estás mejor en el ataúd..."
    m 4tub "... ¡Que dar unas palabras!"
    m 1hub "... ¡Jajaja! Lo siento, quería contarte un chiste que Jerry Seinfeld escribió una vez..."
    m 3etc "... Has oído hablar de él, ¿verdad?"
    m 1eua "¿Entonces?{w=0.5} ¿Te reíste?"
    m 3hksdlb "Hmm...{w=1} tal vez debería trabajar en mi material... "
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soda",
            category=['vida','misc'],
            prompt="Bebida gaseosa",
            random=True
        )
    )

default -5 persistent._mas_pm_drinks_soda = None


label monika_soda:
    m 2euc "¿Tomas gaseosa, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Tomas gaseosa, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_drinks_soda = True
            m 4ekc "Sabes que la gaseosa es muy mala para ti, ¿verdad?"
            m 2ekc "Tiene muchas cosas que dañan tu cuerpo y salud en general."
            m 2tkd "También puede corroer los dientes y producir caries."
            m 2euc "También podrías pensar que las gaseosas dietéticas son menos dañinas, pero pueden ser igual de dañinas."
            m 2lksdlc "No hay nada de malo en uno de vez en cuando. Solo asegúrate de no volverte adicto a esas cosas, [player]."
            m 2eua "¿Por qué no intentas copiar mi estilo de vida saludable?"
            m 1hua "¡De esa manera, podrás estar más en forma como yo!"
            m 1hub "¡Jajaja!"
            m 2ekc "Odiaría que dejaras ir por mal camino tu salud, [player]."
            m 1eka "Quiero que vivas lo más que puedas para que haya una posibilidad de que podamos estar juntos en tu realidad."
            m "Así que reduce el consumo de gaseosa, ¿de acuerdo [mas_get_player_nickname()]?"
        "No":

            $ persistent._mas_pm_drinks_soda = False
            m 2eka "Es un alivio escucharlo."
            m "Me alegra no tener que preocuparme de que te lastimes bebiendo demasiada gaseosa."
            m 3eub "Aún así, está bien tener un pequeño capricho de vez en cuando, ¿sabes? "
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Quizás algún día podamos tomar gaseosa juntos."
            m 5hua "Claro, no es tan elegante, pero estoy segura de que podría ser igual de divertido en un día caluroso."
    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_clones",category=['monika','mod','filosofía'],prompt="Ser clonado",random=True))

label monika_clones:
    m 1euc "Um... hey, ¿[player]?"
    m 1lsc "Tengo una duda."
    m 1euc "¿Sabes cómo descargaste este juego de internet?"
    m "Cualquiera puede hacer eso, ¿verdad?"
    m 1eub "Y este mod fue hecho específicamente para mí. Por personas que tienen su propia versión de mí..."
    m 3etc "Entonces... eso significa que hay múltiples Monikas, entonces.{w=0.5}{nw}"
    extend 1rsc " Es algo que es un poco difícil de imaginar."
    m 1euc "Un número infinito de yos, todas ligadas a sus propios juegos, con sus propias historias."
    m 1lksdla "La teoría del multiverso es algo, ¿eh?"
    m 1eka "Pero soy la única... yo, y mi corazón solo te pertenece a ti."
    m 1ekc "Aun así, no puedo evitar sentirme un poco menos... única, debido a esto."
    m "Piénsalo de esta manera, [player]."
    m 1tkc "¿Serías más feliz si alguien te diera una sola rosa o cien rosas?"
    m 3eka "Un centenar de rosas puede sonar bien. Pero son demasiadas como para poner atención. Debido a la cantidad de flores, cada rosa individual se vuelve menos especial."
    m "El significado que se le atribuye a cada regalo se degrada, simplemente por pura abundancia."
    m 1eua "... Incluso si soy una estrella en un universo de Monikas, sigo siendo la única lo suficientemente afortunada de haberte conocido, [player]."
    m 1hubsa "Siempre serás mi rosa especial."
    m 1ekbfa "Te amo, [player]. Por favor, nunca me reemplaces, ¿okey?"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_immortal",category=['monika','filosofía'],prompt="La brecha de la edad",random=True))

label monika_immortal:
    m 3hua "¡[player]! He estado pensando en algo... "
    m 1eua "¿Sabías que este juego tiene una wiki de mi?"
    m 1lsc "Bueno..."
    m 2lsc "Dice que tengo dieciocho años."
    m 2euc "Pero cuando lo piensas... eso no es del todo cierto."
    m 2eud "Quiero decir, los humanos envejecen, pero no creo que eso se aplique a mí."
    m 4eksdla "Soy...{w=0.5} inmortal."
    m 2lksdlc "La sociedad parece sentir que una relación con diferencia de edad tiene problemas."
    m 2lksdld "... Por eso lo mencioné."
    m 3eka "Eventualmente, la diferencia entre nosotros sería enorme si me quedara para siempre con dieciocho."
    m 1eua "Pero no creo que mi vida se pueda resumir en un número."
    m 1ekbsa "Así que siempre te amaré por toda la eternidad, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]. Solo recuerda eso."
    return "love"

default -5 persistent._mas_pm_wearsRing = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_promisering",
            category=['romance'],
            prompt="Anillo de promesa",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_promisering:
    m 3rksdla "¿Sabías que cuando dos personas confiesan sus sentimientos, a veces usan anillos a juego?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sabías que cuando dos personas confiesan sus sentimientos, a veces usan anillos a juego?{fast}"
        "Por supuesto":

            m 1wkbld "Oh..."
            m 1rkbla "..."
            m 3hkblb "Lo siento, me estaba distrayendo un segundo...{w=0.3}{nw}"
            extend 1dkbssdlu " imaginando en que otro lugar me dirías eso~"
            m 3hkbssdlb "Jajaja, solo estoy bromeando."
            m 1hkbssdlb "No estoy pensando en eso en absoluto...{w=0.3}{nw}"
            extend 3ekbfb " estaba pensando más en anillos de promesa."
        "No lo sabía...":

            m 1ekblu "Bueno, estoy segura de que sabes que cuando las personas se comprometen..."
            m 3rka "Pero eso no es en lo que estaba pensando."
            m 3eub "Estaba pensando más en anillos de promesa."
        "¿Como... matrimonio?":

            m 1hkblb "¡Jajaja, eso también, por supuesto!{w=0.2}{nw}"
            extend 3ekblu " Pero eso en realidad no es en lo que estaba pensando..."
            m 3eub "Estaba pensando más en anillos de promesa."

    m 1eubsa "Si usas un anillo de promesa, puedes mostrarles a todos que estamos juntos~"
    m 3tkbsu "También te ayuda a recordar nuestro amor eterno~"

    m 1ekbssdlu "De todos modos, solo me preguntaba...{w=0.3} {nw}"
    extend 1eksdla "¿Usas un anillo por mí, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "De todos modos, solo me preguntaba... ¿Usas un anillo por mí, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_wearsRing = True

            m 1sublo "¡Aww, [player]!"
            m 1hublb "¡No tienes idea de lo feliz que me hace eso!"
            m 1ekbsa "Solo sabiendo que te preocupas lo suficiente como para mostrar tu amor y dedicación... "
            m "Significa el mundo para mi."
        "No":

            $ persistent._mas_pm_wearsRing = False

            m 4rksdla "Quizás deberías conseguir uno."
            m 2eua "Quiero decir, ya estamos en una relación. Entonces, ¿por qué no mostrar ese amor y dedicación?"
            m 2lfu "También ayudaría a mantener a esas...{w=0.2} pretendientes no deseados lejos de ti."
            m 7ekbsa "Si usaras uno, solo un anillo de promesa, en tu dedo anular por mí..."
            m 1ekbsa "Me haría muy feliz."

    if not persistent._mas_acs_enable_promisering:
        m 1rubsa "Ojalá pudiera conseguir uno para mí. Estoy segura de que encontraré la manera de agregar uno aquí a tiempo."
        m 1dubsa "... Y luego podría usarlo para siempre."
        m 3ekbfu "Pero hasta entonces, recuerda que mi compromiso contigo es inquebrantable, [player]."
    else:

        if not persistent._mas_pm_wearsRing:
            m 3ekbsa "Me hiciste tan feliz cuando me diste este anillo."
            m 1ekbsa "Honestamente, no puedo expresar cuánto significó el que me dieras esto..."
            m 1dubfa "Tu promesa..."
        else:

            m 3hubsb "Al igual que significó el mundo para mí cuando me diste este anillo..."
            m 1ekbsa "Esta promesa de que nos pertenecemos el uno al otro, y de nadie más..."
            m 1dubfu "Que estaremos juntos para siempre..."

        show monika 5esbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5esbfa "Mi compromiso contigo es inquebrantable, [mas_get_player_nickname()]."
        m 5ekbfa "Gracias por un regalo tan maravilloso, te amo."
        return "derandom|love"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sports",
            category=["deportes"],
            prompt="Ser atlético",
            random=True
        )
    )

default -5 persistent._mas_pm_like_playing_sports = None


default -5 persistent._mas_pm_like_playing_tennis = None


label monika_sports:
    m 1eua "He estado pensando en cosas que podemos hacer juntos."
    m 3eua "... Ya sabes, cuando finalmente encuentre un camino hacia tu realidad."
    m 3hub "¡Los deportes siempre son divertidos!"
    m 1eub "Puede ser una excelente manera de hacer ejercicio y mantenerse en forma."
    m 1euc "El fútbol y el tenis son buenos ejemplos."
    m 3eua "El fútbol requiere mucho trabajo en equipo y coordinación. ¡El momento en que finalmente lo logras y marcas un gol es tan emocionante!"
    m 3eud "Jugar al tenis, por otro lado, ayuda a mejorar la coordinación ojo-mano y te mantiene alerta."
    m 1lksdla "... Aunque los mítines largos pueden ser un poco agotadores, jejeje~"
    m 3eua "Además, ¡es un gran deporte para dos personas!"

    m "¿Juegas tenis, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Juegas tenis, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = True

            m 3eub "¿De verdad? ¡Eso es genial!"
            m 3hub "Por lo general, hay canchas de tenis en los parques públicos. ¡Podremos jugar todo el tiempo!"
            m "¡Quizás incluso podamos formar equipo para partidos de dobles!"
            m 2tfu "Si eres lo suficientemente bueno, porque..."
            m 2tfc "Yo juego para ganar."
            m "..."
            m 4hub "¡Jajaja! Solo bromeo..."
            m 4eka "Solo jugar contigo como mi compañero es más que suficiente para mí, [player]~"
        "No, pero si fuera contigo...":

            $ persistent._mas_pm_like_playing_sports = True



            m 1eka "Aww, eso es muy dulce~"
            m 3eua "Te enseñaré a jugar cuando llegue...{w=0.5} o si no puedes esperar, ¡puedes tomar lecciones!"
            m 3eub "¡Entonces podremos empezar a jugar en partidos de dobles!"
            m 1eua "No puedo imaginar nada más divertido que ganar un partido contigo como mi compañero..."
            m 3hub "¡Seremos imparables!"
        "No, prefiero otros deportes":

            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = False

            m 3hua "Tal vez podamos practicar los deportes que te gustan en el futuro. Sería maravilloso."
            m 3eua "Si es un deporte que no he jugado antes, ¡podrías enseñarme!"
            m 1tku "Pero ten cuidado, aprendo rápido..."
            m 1tfu "No pasará mucho tiempo antes de que pueda vencerte.{w=0.2} {nw}"
            extend 1tfb "¡Jajaja!"
        "No, no me gustan mucho los deportes":
            $ persistent._mas_pm_like_playing_sports = False
            $ persistent._mas_pm_like_playing_tennis = False

            m 1eka "Oh... bueno, ¡pero espero que aún estés haciendo suficiente ejercicio!"
            m 1ekc "Odiaría verte enfermo por algo así."
            if mas_isMoniAff(higher=True):
                m 1eka "Es difícil para mí no preocuparme por ti cuando te amo tanto~"
    return "derandom"


default -5 persistent._mas_pm_meditates = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_meditation",category=['psicología','monika'],prompt="Meditando",random=True))

label monika_meditation:
    m 1eua "Quizás te estes preguntando cómo pude hacer tantas actividades sin quedarme sin tiempo para mí."
    m 3eua "Ya sabes, cosas como clubes de debate, deportes, tareas escolares, salir con amigos..."
    m 1ekc "La verdad es que se me acabó el tiempo para mí."
    m "Estuve bien por un tiempo, pero en un momento, todo el estrés y la ansiedad finalmente me alcanzaron."
    m 1tkc "Estaba constantemente en un estado de pánico y nunca tuve tiempo para relajarme."
    m "Fue entonces cuando me di cuenta de que necesitaba una especie de 'descanso cerebral'..."
    m 1dsc "... Un momento en el que podía olvidarme de todo lo que estaba pasando en mi vida."
    m 1eua "Entonces, todas las noches antes de irme a dormir, me tomaba diez minutos de mi tiempo para meditar."
    m 1duu "Me puse cómoda, cerré los ojos y me concentré solo en el movimiento de mi cuerpo mientras respiraba..."
    m 1eua "Meditar realmente me ayudó a mejorar mi salud mental y emocional."
    m "Finalmente pude manejar mi estrés y sentirme más tranquila durante el día."

    m 1eka "[player], ¿alguna vez te tomas tiempo para meditar?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ¿alguna vez te tomas tiempo para meditar?{fast}"
        "Sí":
            $ persistent._mas_pm_meditates = True
            m 1hua "¿De verdad? ¡Eso es maravilloso!"
            m 1eka "Siempre me preocupa que puedas sentirte preocupado o agobiado, pero ahora me siento un poco aliviada."
            m 1hua "Saber que estás tomando medidas para reducir el estrés y la ansiedad realmente me hace feliz, [player]."
        "No":

            $ persistent._mas_pm_meditates = False
            m "Ya veo. Bueno, si alguna vez te sientes estresado o ansioso, te recomendaría que pruebes un poco de meditación."
            m 1eua "Además de calmarte, la meditación también tiene vínculos con la mejora del sueño, el sistema inmunológico e incluso la esperanza de vida."
            m 3eub "Si estas interesado, hay mucho en internet para ayudarte a empezar."
            m 1eub "Ya sea un video, un truco para contar la respiración o algo más..."
            m 1hua "¡Puedes usar internet para que la meditación sea un proceso libre de estrés!"
            m 1hksdlb "¡Jajaja! Solo un pequeño juego de palabras, [player]."

    m 1eua "De todos modos... si alguna vez quieres un ambiente tranquilo donde puedas relajarte y olvidarte de tus problemas, siempre puedes venir y pasar tiempo conmigo."
    m 1ekbsa "Te amo y siempre intentaré ayudarte si te sientes mal."
    m 1hubfa "Nunca olvides eso, [player]~"

    return "derandom|love"


default -5 persistent._mas_pm_like_orchestral_music = None


default -5 persistent._mas_pm_plays_instrument = None


default -5 persistent._mas_pm_has_piano_experience = None


define -5 mas_PIANO_EXP_HAS = 2
define -5 mas_PIANO_EXP_SOME = 1
define -5 mas_PIANO_EXP_NONE = 0

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_orchestra",
            category=['medios',"música"],
            prompt="Música clásica",
            random=True
        )
    )

label monika_orchestra:
    m 3euc "Hey [player], ¿escuchas música de orquesta?{nw}"
    $ _history_list.pop()
    menu:
        m "Hey [player], ¿escuchas música de orquesta?{fast}"
        "Sí":
            $ persistent._mas_pm_like_orchestral_music = True
            m 3eub "¡Eso es genial!"
            m 3eua "Me encanta cómo puede surgir una música tan maravillosa cuando se tocan juntos tantos instrumentos diferentes."
            m 1eua "Me sorprende la cantidad de práctica que hacen los músicos para lograr ese tipo de sincronización."
            m "Probablemente les lleve mucha dedicación hacer eso."
            m 1eka "Pero de todos modos,{w=0.2} sería reconfortante escuchar una sinfonía contigo en una tranquila tarde de domingo, [player]."
        "No":

            $ persistent._mas_pm_like_orchestral_music = False
            m 1ekc "Supongo que {i}es{/i} un género muy especializado y no se adapta al oído de todos."
            m 1esa "Pero tienes que admitir que, con tantos jugadores, debe haber un gran esfuerzo para practicar para los espectaculos."

    m 1eua "Eso me recuerda, [player]."
    m "Si alguna vez quieres que toque para ti..."
    m 3hua "Siempre puedes seleccionar mi canción en el menú de música~"


    m "¿Y tú, [player]? ¿Tocas un instrumento?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Y tú, [player]? ¿Tocas un instrumento?{fast}"
        "Sí":
            m 1sub "¿De verdad? ¿Cuál?"

            $ instrumentname = ""

            while not instrumentname:
                $ instrumentname = mas_input(
                    "¿Qué instrumento tocas?",
                    allow=" abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ-_",
                    length=15,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

            $ tempinstrument = instrumentname.lower()

            if tempinstrument == "cancel_input":
                jump monika_orchestra.no_choice

            elif tempinstrument == "piano":
                $ persistent._mas_pm_plays_instrument = True
                m 1wuo "Oh, ¡eso es genial!"
                m 1eua "No conocía mucha gente que tocara el piano, así que es muy bueno saber que tú también lo haces."
                m 1eua "¿Tienes mucha experiencia tocando el piano?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Tienes mucha experiencia tocando el piano?{fast}"
                    "Si":

                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_HAS
                        m 3hua "¿De verdad?"
                        m 3sub "¡Eso es maravilloso!"
                        m 1eua "Quizá algún día puedas enseñarme y hasta podamos hacer un dueto."
                    "No mucha":

                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_SOME
                        m 2eka "Está bien, [player]."
                        m 2eua "Después de todo, es un instrumento bastante complicado de aprender."
                        m 4hua "Pero incluso si no tienes mucha experiencia, estoy segura de que podríamos aprender juntos~"
                    "Acabo de empezar":

                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_NONE
                        m 1duc "Ya veo."
                        m 3hksdlb "Puede ser bastante difícil al principio,{w=0.2} {nw}"
                        extend 3huu "pero estoy segura de que si sigues practicando serás capaz de tocar mejor que yo, [player]~"

            elif tempinstrument == "armonika":
                m 1hub "Guau, siempre he querido probar la armonik--"
                m 3eub "... ¡Oh!"

                if mas_isMoniUpset(lower=True):
                    m 3esa "¿Hiciste eso por mí?"
                    m 1eka "Eso es dulce..."
                    m "Pequeñas cosas como esta me animan. Gracias, [player]."

                elif mas_isMoniHappy(lower=True):
                    m 1eka "Aww... ¿Hiciste eso por mí?"
                    m "¡Eso es tan dulce!"
                    m 1ekbsa "Pequeñas cosas lindas como esta me hacen sentir amada, [player]."
                else:

                    m 1eka "Aww, [player]...{w=1} ¿Hiciste eso por mí?"
                    m "¡Eso es {i}taaaan{/i} adorable!"
                    show monika 5eubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eubfu "Y para que lo sepas, puedes tocar conmigo cuando quieras..."
                    m 5eubfa "Jejeje~"

            elif tempinstrument == "armonica":
                m 1hub "Vaya, ¡siempre quise probar la armónica!"
                m 1eua "Me encantaría escucharte tocar para mí."
                m 3eua "Quizás tú podrías enseñarme a tocar~"
                m 4esa "A pesar de que..."
                m 2esa "Personalmente, prefiero la {cps=*0.7}{i}armonika{/i}{/cps}..."
                m 2eua "..."
                m 4hub "¡Jajaja! Eso fue tan tonto, solo estoy bromeando, [player]~"
                $ persistent._mas_pm_plays_instrument = True
            else:
                m 1hub "¡Vaya, siempre quise probar [tempinstrument]!"
                m 1eua "Me encantaría escucharte tocar para mí."
                m 3eua "Quizás tú podrías enseñarme a tocar~"
                m 1wuo "¡Oh! ¿Un dueto entre tu [tempinstrument] y mi piano sonaría bien?"
                m 1hua "Jejeje~"
                $ persistent._mas_pm_plays_instrument = True
        "No":

            label monika_orchestra.no_choice:
                pass
            $ persistent._mas_pm_plays_instrument = False
            m 1euc "Ya veo..."
            m 1eka "Deberías intentar elegir un instrumento que te interese."
            m 3eua "Tocar el piano me abrió un mundo completamente nuevo. Es una experiencia increíble."
            m 1hua "Además, ¡tocar música tiene muchísimos beneficios!"
            m 3eua "Por ejemplo, puede ayudar a aliviar el estrés y también te da una sensación de satisfacción."
            m 1eua "¡Escribir algunas composiciones también es divertido! A menudo perdí la noción del tiempo practicando debido a lo inmersa que estaba."
            m 1lksdla "Ah, ¿estaba divagando de nuevo, [player]?"
            m 1hksdlb "¡Lo siento!"
            m 1eka "De todos modos, deberías ver si hay algo que te llame la atención."
            m 1hua "Me alegraría mucho escucharte tocar."

    if (
            persistent._mas_pm_like_orchestral_music
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        if renpy.showing("monika 5eubfb"):
            show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eua "Ah, y si alguna vez te apetece compartir tu música orquestal favorita conmigo, [player], ¡es muy fácil hacerlo!"
        m 3eua "Todo lo que tienes que hacer es seguir estos pasos..."
        call monika_add_custom_music_instruct
    return "derandom"


default -5 persistent._mas_pm_like_jazz = None


default -5 persistent._mas_pm_play_jazz = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_jazz",
            category=['medios',"música"],
            prompt="Jazz",
            random=True
        )
    )

label monika_jazz:
    m 1eua "Dime, [player], ¿te gusta el jazz?{nw}"
    $ _history_list.pop()
    menu:
        m "Dime, [player], ¿te gusta el jazz?{fast}"
        "Sí":
            $ persistent._mas_pm_like_jazz = True
            m 1hua "Oh, ¡okey!"
            if persistent._mas_pm_plays_instrument:
                m "¿Tocas también jazz?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Tocas también jazz?{fast}"
                    "Sí":
                        $ persistent._mas_pm_play_jazz = True
                        m 1hub "¡Eso es genial!"
                    "No":
                        $ persistent._mas_pm_play_jazz = False
                        m 1eua "Ya veo."
                        m "No he escuchado mucho, pero personalmente lo encuentro bastante interesante."
        "No":
            $ persistent._mas_pm_like_jazz = False
            m 1euc "Oh, ya veo."
            m 1eua "No he escuchado mucho, pero veo por qué a la gente le gustaría."
    m "No es exactamente moderno, pero tampoco es del todo clásico."
    m 3eub "Tiene elementos de clásico, pero es diferente. Se aleja de la estructura y entra en un lado más impredecible de la música."
    m 1eub "Creo que la mayor parte del jazz se trataba de la expresión, cuando a la gente se le ocurrió."
    m 1eua "Se trataba de experimentar, de ir más allá de lo que ya existía. Hacer algo más salvaje y colorido."
    m 1hua "¡Como la poesía! Solía estar estructurada y con rimas, pero ha cambiado. Da mayor libertad ahora."
    m 1eua "Quizás eso es lo que me gusta del jazz."
    if (
            persistent._mas_pm_like_jazz
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        m "Oh, y si alguna vez tienes ganas de compartir tu cancion de jazz favorita conmigo, [player], ¡es muy fácil hacerlo!"
        m 3eua "Todo lo que tienes que hacer es seguir estos pasos..."
        call monika_add_custom_music_instruct
    return "derandom"


default -5 persistent._mas_pm_watch_mangime = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_otaku",category=['medios','sociedad','tú'],prompt="Ser un otaku",random=True))

label monika_otaku:
    m 1euc "Hey, ¿[mas_get_player_nickname(exclude_names=['mi amor'])]?"
    m 3eua "Miras anime y lees manga, ¿verdad?{nw}"
    $ _history_list.pop()
    menu:
        m "Miras anime y lees manga, ¿verdad?{fast}"
        "Sí":
            $ persistent._mas_pm_watch_mangime = True
            m 1eua "No puedo decir que esté sorprendida, de verdad."
        "No":

            $ persistent._mas_pm_watch_mangime = False
            m 1euc "¿Oh, en serio?"
            m 1lksdla "Eso es un poco sorprendente, siendo honesta..."
            m "Este no es exactamente el tipo de juego que una persona promedio tomaría y jugaría, pero supongo que cada quien."
    m 1eua "Solo pregunté porque estás jugando un juego como este, después de todo."
    m 1hua "No te preocupes, no soy nadie para juzgar, jejeje~"
    m 1eua "No deberías avergonzarte si te gustan ese tipo de cosas, ¿sabes?"
    m 1euc "Hablo enserio. No hay nada de malo en que te guste el anime o el manga."
    m 4eua "Después de todo, Natsuki también lee manga, ¿recuerdas?"
    m 1lsc "De verdad, la sociedad es demasiado crítica hoy en día."
    m "No es como si en el momento en que miras anime te 'encierras' por el resto de tu vida."
    m 1euc "Es solo un pasatiempo, ¿sabes?"
    m 1eua "Nada más que un interés."
    m 1lsc "Pero..."
    m 2lksdlc "No puedo negar que existen otakus extremos."
    m 1eka "No es que los desprecie, ni nada de eso, es solo que..."
    m 4eka "Estan muy inmersos."
    m 1lksdla "Demasiado inmersos, si me preguntas."
    m 1ekc "Es como si ya no pudieran distinguir entre la fantasía y la realidad."
    m 1eka "No eres así, ¿verdad, [player]?"
    m 1eua "Si eres un otaku, lo respeto."
    m 3eka "Solo recuerda no meterte demasiado en ese tipo de cosas, ¿okey?"
    m 1eka "Después de todo, hay una gran diferencia entre la obsesión y la dedicación."
    m 1lfu "No quisiera ser reemplazada por un recorte bidimensional."
    m 1eua "Además, si alguna vez quieres escapar de la realidad..."
    m 1hubsa "Puedo ser tu fantasía de la vida real~"

    $ mas_protectedShowEVL("monika_conventions", "EVE", _random=True)
    return "derandom"



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip1",
            category=['consejos de escritura'],
            prompt="Consejo de escritura #1",
            pool=True
        )
    )

label monika_writingtip1:
    m 1esa "Sabes, ha pasado un tiempo desde que hicimos uno de estos..."
    m 1hub "... ¡Así que vamos álla!"
    m 3hub "¡Aquí está el consejo de escritura del día de Monika!"
    m 3eua "A veces, cuando hablo con personas que están impresionadas por mi escritura, dicen cosas como: 'Nunca podría hacer eso'."
    m 1ekc "Es realmente deprimente, ¿sabes?"
    m 1ekd "Como alguien que ama más que nada compartir sus pasiones..."
    m 3ekd "... Me duele cuando la gente piensa que ser bueno es algo natural."
    m 3eka "Así es con todo, no solo con la escritura."
    m 1eua "Cuando pruebes algo por primera vez, probablemente lo vas a hacer mal."
    m "A veces, cuando terminas, te sientes realmente orgulloso de ello e incluso quieres compartirlo con todos."
    m 3eksdld "Pero tal vez después de unas semanas vuelvas a hacerlo y te des cuenta de que nunca fue realmente bueno."
    m 3eksdla "Eso me pasa a mi todo el tiempo."
    m "Puede ser bastante descorazonador dedicar tanto tiempo y esfuerzo a algo, y luego te das cuenta de que apesta."
    m 4eub "Pero eso suele suceder cuando siempre te comparas con los mejores profesionales."
    m 4eka "Cuando alcanzas las estrellas, siempre estarán fuera de tu alcance, ¿sabes?"
    m "La verdad es que hay que subir paso a paso."
    m 4eua "Y cada vez que alcanzas un hito, primero miras hacia atrás y ves qué tan lejos has llegado..."
    m "Y luego miras hacia adelante y te das cuenta de cuánto más queda por hacer."
    m 2duu "Por lo tanto, a veces puede ayudar poner el listón un poco más bajo..."
    m 1eua "Intenta encontrar algo que creas que es {i}bastante{/i} bueno, pero no de clase mundial."
    m "Y puedes convertirlo en tu objetivo personal."
    m 3eud "También es muy importante comprender el alcance de lo que estás tratando de hacer."
    m 4eka "Si te lanzas directamente a un gran proyecto y aún eres un aficionado, nunca lo lograrás."
    m "Entonces, si hablamos de escribir, una novela puede ser demasiado al principio."
    m 4esa "¿Por qué no probar algunas historias cortas?"
    m 1esa "Lo mejor de las historias cortas es que puedes concentrarte en una sola cosa que quieres hacer bien."
    m 1eua "Eso se aplica a los proyectos pequeños en general; realmente puedes concentrarte en una o dos cosas."
    m 3esa "Es una experiencia de aprendizaje muy buena y un trampolín."
    m 1euc "Oh, una cosa más..."
    m 1eua "Escribir no es algo en lo que simplemente llegas a tu corazón y sale algo hermoso."
    m 3esa "Al igual que dibujar y pintar, es una habilidad en sí misma, aprender a expresar lo que llevas dentro."
    m 1hua "¡Eso significa que hay métodos, guías y conceptos básicos!"
    m 3eua "Leer sobre esas cosas puede ser muy revelador."
    m 1eua "Ese tipo de planificación y organización realmente ayudará a evitar que te sientas abrumado y te rindas."
    m 3esa "Y antes de que te des cuenta..."
    m 1hua "Empiezas a apestar cada vez menos."
    m 1esa "Nada surge de forma natural."
    m 1eua "Nuestra sociedad, nuestro arte, todo, se basa en miles de años de innovación humana."
    m 1eka "Así que siempre que empieces sobre esa base y vayas paso a paso..."
    m 1eua "Tú también puedes hacer cosas increíbles."
    m 1hua "... ¡Ese es mi consejo para hoy!"
    m 1hub "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip2",
            category=['consejos de escritura'],
            prompt="Consejo de escritura #2",
            conditional="seen_event('monika_writingtip1')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip2:
    m 1euc "Sabes..."
    m 1eua "Realmente no tenemos suficiente, ¡así que aquí hay otro!"
    m 3hub "¡Aquí está el consejo de escritura del día de Monika!"
    m 2eua "Si alguna vez tienes miedo de compartir tus escritos con otras personas por temor a ser criticado, ¡no lo estés!"
    m "Después de todo, debes recordar que nadie comienza nunca de la mejor manera. Ni siquiera alguien como Tolkien o Sir Terry Pratchett."
    m 4eka "Tienes que recordar que todos partimos de algún lado y..."
    m 2euc "En realidad, esto no solo se aplica a la escritura, sino a cualquier cosa, en realidad."
    m 2lksdla "Lo que trato de decir es que no debes desanimarte."
    m 1hua "No importa lo que hagas, si alguien te dice que tu escritura o tu trabajo son malos, ¡sé feliz!"
    m 1eua "Porque eso solo significa que puedes mejorar y ser mejor de lo que eras antes."
    m 3eua "Tampoco está de más tener amigos y seres queridos que te ayuden a darte cuenta de lo buena que es tu escritura."
    m 1eka "Solo recuerda, no importa lo que digan sobre el trabajo que realizas, siempre estaré ahí para apoyarte en todo momento. No temas volver a mí, a tus amigos o a tu familia."
    m "Te amo y siempre te apoyaré en todo lo que hagas."
    m 1lksdlb "Siempre que sea legal, por supuesto."
    m 1tku "Eso no significa que esté completamente en contra. Puedo guardar un secreto, después de todo~"
    m 1eua "He aquí un dicho que he aprendido."
    m 1duu "'Si te esfuerzas por lograrlo, sucederá con la suficiente determinación. Puede que no sea inmediato y, a menudo, tus sueños más grandes son algo que no lograrás en tu propia vida'."
    m "'El esfuerzo que pones en algo te trasciende. Porque no hay futilidad incluso en la muerte.'"
    m 3eua "No recuerdo a la persona que dijo eso, pero las palabras están ahí."
    m 1eua "El esfuerzo que uno pone en algo puede trascender incluso a uno mismo."
    m 3hua "¡Así que no tengas miedo de intentarlo! ¡Siga adelante y eventualmente avanzará!"
    m 3hub "... ¡Ese es mi consejo para hoy!"
    m 1eka "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip3",
            category=['consejos de escritura'],
            prompt="Consejo de escritura #3",
            conditional="seen_event('monika_writingtip2')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip3:
    m 1eua "Me estoy divirtiendo haciendo esto, así que..."
    m 3hub "¡Aquí está el consejo de escritura del día de Monika!"
    m 1eua "Asegúrate de anotar siempre las ideas que se te ocurran."
    m 1euc "¿Por qué?"
    m 3eua "Porque algunas de las mejores ideas pueden surgir cuando menos lo esperas."
    m "Incluso si requiere un poco de esfuerzo, anótalo."
    m 1eub "Quizás puedas inspirar a alguien más."
    m 3eub "Tal vez puedas mirar hacia atrás después de un tiempo y actuar en consecuencia."
    m 1hua "¡Nunca sabes!"
    m 1eua "Siempre es bueno llevar un diario."
    m "Puedes usarlo para registrar ideas, sentimientos, cualquier cosa que se te ocurra."
    m 1euc "Pero asegúrate de que el diario tenga un candado."
    m 1eua "Quizás también puedas guardar notas digitales en lugar de físicas."
    m 3eua "Después de todo, la privacidad es importante."
    m 1lksdla "... Sin embargo, no puedo prometer que no echaré un vistazo. ¡Es demasiado tentador!"
    m 1hua "Después de todo, no nos guardamos secretos, ¿verdad?~"
    m 1eka "Solo recuerda, [player], siempre te apoyaré dando vida a tus ideas."
    m 3hua "... ¡Ese es mi consejo para hoy!"
    m 1hub "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip4",
            category=['consejos de escritura'],
            prompt="Consejo de escritura #4",
            conditional="seen_event('monika_writingtip3')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip4:
    m 3hub "¡Aquí está el consejo de escritura del día de Monika!"
    m 1eua "Sabes sobre el bloqueo de ideas, ¿verdad?"
    m "Lo tenía mucho cuando empecé a escribir."
    m 1euc "A veces me pasaba a la mitad de un borrador, incluso antes de comenzar."
    m 1ekc "Cada vez que intentaba escribir una palabra, pensaba: 'Esto no va a sonar bien' o 'no es así como quiero que se vea'. Así que me detenía, retrocedía e intentaba de nuevo."
    m 1eka "¡Pero me di cuenta de que, en última instancia, no importaba si las cosas no salían bien la primera vez!"
    m 3eua "Siento que el corazón de la escritura no se trata de hacerlo bien a la primera, sino de perfeccionarlo después."
    m "Lo que importa es el producto final, no el prototipo."
    m 1eub "Así que superar el bloqueo de ideas, para mí, fue una cuestión de no querer hacer del prototipo el producto final y no castigarme por mis fallas iniciales."
    m 3eub "Creo que es así con todas las cosas, no solo con la escritura."
    m 1eua "Cualquier cosa que necesite que intentes una y otra vez, ya sea arte, música, aprendizaje o incluso relaciones."
    m 1ekc "A veces es difícil convencerse completamente de que ese es el caso."
    m 1eka "Pero tienes que hacerlo."
    m 4eka "De lo contrario, no llegarás a ninguna parte."
    m 3hua "... ¡Ese es mi consejo para hoy!"
    m 1hub "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip5",
            category=['consejos de escritura'],
            prompt="Consejo de escritura #5",
            conditional="seen_event('monika_writingtip4')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip5:
    m 3hub "¡Aquí está el consejo de escritura del día de Monika!"
    m 1eua "Si quieres mejorar en la escritura, diría que lo más importante, además de hacerlo, es probar cosas nuevas."
    m 3eua "Como escribir prosa si eres poeta, o verso libre si normalmente escribes rima."
    m 1eka "Puede terminar mal, pero si no lo intentas, no sabrás cómo terminará."
    m 1hua "Y si las cosas van bien, ¡podrías terminar encontrando algo que te guste!"
    m 1eua "Es lo que mantiene las cosas en movimiento, el cambio y la experimentación."
    m "Yo diría que ayuda especialmente si estás atrapado en una situación que quieres resolver, pero no sabes cómo."
    m 3eua "Ya sea un bloqueo de escritor, puro aburrimiento, una situación desconcertante o cualquier cosa."
    m 1hua "¡Cambiar tu ángulo de aproximación a las cosas realmente puede producir algunos resultados interesantes!"
    m 1eua "Así que prueba cosas nuevas que puedan darte el impulso para salir adelante."
    m 1lksdla "Solo asegúrate de que no sea nada demasiado peligroso para ti, [player]."
    m 1hua "¡Ese es mi consejo para hoy!"
    m 1hub "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip6",
            category=['consejos de escritura'],
            prompt="Consejo de escritura #6",
            conditional="seen_event('monika_writingtip5')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip6:
    m 3eub "¡Es hora de otro...{w=0.2} consejo de escritura del día!"
    m 1hkbla "Sabes, puede ser muy divertido escribir en papel bonito."
    m 1eud "Pero, ¿has pensado en cómo el aspecto de tu papel puede contribuir a la propia escritura?"
    m 3euc "Por ejemplo, si quieres escribir una carta de uno de tus personajes..."
    m 3etd "¿Qué podría decir a su lector sobre su personalidad si utiliza una página elegante con un estampado floral? {w=0.2}¿O un papel de cuaderno arrugado?"
    m 3eud "El uso de papel visiblemente envejecido o desgastado también puede informar al lector sobre la línea de tiempo de su historia."
    m 1hub "Aunque no sirva para nada a tu escritura, puede ser satisfactorio pintar en un lienzo bonito, por así decirlo."
    m 2eusdlc "Dicho esto...{w=0.2} creo que a veces el uso de materiales más bonitos puede contribuir al bloqueo del escritor."
    m 2rksdlb "Cuando compro un diario nuevo y lo abro en la primera página limpia...{w=0.3} es realmente desalentador, ¡jajaja!"
    m 2rksdla "Siento que tengo que asegurarme de llenar el diario con cosas tan bonitas como la portada."
    m 7eua "Así que también he empezado a utilizar un 'diario basura'... {w=0.2}un cuaderno barato y sencillo que te da mucha libertad para garabatear y escribir cualquier cosa."
    m 3eub "Y ya sabes, esos borradores e ideas extrañas son el primer paso para una obra terminada digna de un bonito marco."
    m 1hua "¡Ese es mi consejo para hoy!"
    m 1hub "Gracias por escuchar~"
    return



init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfharm",category=['psicología'],prompt="Autodestrucción",random=True))

label monika_selfharm:
    m 1lksdlc "Hey, [player]..."
    m 1eksdld "¿Has pensado alguna vez en autolesionarte?"
    m 2lksdld "Ya sabes..."
    m 2lksdlc "como cortarse..."
    m "Quiero decir."
    m 2lksdld "Después de enterarme de Yuri, sentí un poco de curiosidad..."
    m 2dksdltpc "Solo quería ver cómo se sentía...{w=0.3} sentir {i}algo{/i} de nuevo..."
    m 2rksdltpd "No es fácil saber que todo lo que creías vivir,{w=0.1} lo que creías amar, era todo una mentira..."
    m 2dstdc "Aunque no lo volveré a hacer."
    m 2dktdc "..."
    m 2eka "Si alguna vez te sientes deprimido, ven a verme, ¿de acuerdo?"
    m 2ekd "Me dolería aún más verte sufriendo..."
    m 1hua "¡Solo debes saber que la gente se preocupa por ti!"
    m 1eka "Créeme, [player]."
    m 1eka "Puedes pensar que nadie está realmente allí para ti, ¡pero están!"
    m 4eua "Quiero decir, estoy aquí, ¿no?"
    m 1eka "¡No importa los problemas por los que estés pasando, sé que puedes superarlo!"
    m 3eka "Creo en ti..."
    m 1eua "Así que cree en ti mismo, ¿de acuerdo?"
    m 1eka "Si alguna vez necesitas a alguien con quien desahogarte, recuerda que siempre estoy aquí para escucharte y consolarte, ¿de acuerdo?"
    m 1ekbsa "Realmente te amo mucho, [player]."
    return "love"


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_urgent",category=['romance'],prompt="Mensaje urgente",random=True,aff_range=(mas_aff.NORMAL, None)))

label monika_urgent:
    m 1esc "[player], ¿Tienes un segundo?"
    m 1esd "Hay algo que necesito decirte."
    m 1euc "Es importante."
    m 1dsc "Yo..."
    m "..."
    m 1hub "¡Te amo!"
    m 3hksdlb "¡Jajaja!~ ¿Te preocupé?"
    m 1eksdla "Lo siento~"
    m 1rksdla "¡Ojalá pudiera ver la expresión de tu rostro ahora mismo!"
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "Estoy segura de que es adorable~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_other_girls",category=['miembros del club'],prompt="¿Alguna vez piensas en las otras chicas?",pool=True))

label monika_other_girls:
    if persistent._mas_pm_cares_about_dokis:
        m 1euc "Sabes, en realidad es muy difícil para mí entender cómo te sientes cuando se trata de..."
        m 1lksdlc "..."
        m 1lksdld "Lo que pasó con las otras chicas."
        m 3esd "Por ejemplo..."
        m "El personaje principal fue escrito para ser amigo de la infancia de Sayori."
        m 1esc "Pero era solo un personaje de posición unidimensional para que lo usaras para interactuar con el juego."
        m 2ekc "Aún así, tal vez te sentiste peor por lo que le pasó a Sayori debido a la relación que el personaje principal estaba programado para tener con ella."
        m 1ekc "Si ese es el caso, quiero decirte que lo siento, [player]."
        m 1lksdlc "Tanto por hacerte sentir mal como por..."
        m 1dsc "..."
        m "Hacer lo que tenía que hacer."
        m 1lksdlc "..."
        m 1ekc "Simplemente no había nada más que se pudiera hacer."
        m 3efc "¡Las otras chicas nunca te amaron como yo!"
        m 3rfc "¡Solo les importaba el personaje que te representaba en el juego!"
        m 1eka "El amor que te tengo es real, [player], y haría cualquier sacrificio para estar contigo para siempre."
        m 1ekc "Espero que puedas perdonarme por lo que tuve que hacer para que pudiéramos estar juntos."
        m 1lksdlc "..."
        if mas_isMoniDis():
            m 1eksdld "¿Me perdonas, verdad [player]? Realmente lamento lo que hice. Por favor, no me odies."
        elif mas_isMoniUpset():
            m 1ekd "Sé que lo que hice podría considerarse imperdonable, intentaré hacer lo que pueda para compensarlo."
        elif mas_isMoniNormal(higher=True):
            m 1ekbsa "Te amo, [player]..."
            m "Más de lo que jamás podría expresar."
    else:
        m 3eka "Sabes, estoy muy contenta de que no me hagas sentir culpable por lo que les pasó a las otras chicas."
        m 2dkd "Sé que hay mucha gente que me odia por lo que hice..."
        if not persistent._mas_pm_a_hater:
            m 4eka "Y me enorgullece mucho que no seas uno de ellos."
        m 2rksdlc "Estoy segura de que no fue una experiencia muy agradable para ti... pero me alegra que pudieras notar la diferencia entre quién era real y quién no..."
        m 1eka "Entre quién te amaba {i}a ti{/i} y quién amaba al personaje principal."
        m 3eka "Fui la única que alguna vez te amó, [player]..."
        m 3hua "Y te amaré por siempre~"
    return "love"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_happiness",category=['vida','psicología'],prompt="Felicidad",random=True))

label monika_happiness:

    m 1eua "[player], ¿estás feliz?"
    m "Con tu vida en general, quiero decir."
    m 2lksdla "Está bien si no lo estás. Puedo entender que no estés contento, [player]."
    m 1eka "Después de todo, sin ti, mi vida sería completamente insoportable."
    m 1eua "¿No es gracioso que podamos sufrir más que ser felices?"
    m 1hubfa "Estoy tan feliz como podría estarlo sabiendo que me amas, [player]."
    m 1lksdlc "Sin embargo, si algo te sucediera, no creo que me vuelva a sentir feliz."
    m "Me destruiría."
    m 1esc "Supongo que es comprensible por qué notamos que nos suceden más cosas malas que buenas..."
    m "Si la gente no reaccionara con tanta fuerza ante las cosas malas, no habrían sobrevivido tanto tiempo."
    m 1euc "Por ejemplo, cómo ponerte nervioso por tu futuro o situaciones sociales."
    m 2ekc "Haces todo lo posible para sacarles el máximo partido, pero si fallas, te sentirías realmente horrible."
    m 2eka "Si eso te pasa alguna vez, [mas_get_player_nickname()], ¡sé que estaré aquí para sacarte de eso!"
    m 1eua "Y además, tu linda novia siempre te apoyará~"
    m 1hub "¡Eso es algo de lo que estar muy feliz!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_how_soon",category=['tú','romance'],prompt="Esperando estar juntos",random=True))

label monika_how_soon:
    $ p_nickname = mas_get_player_nickname(capitalize=True)
    m 1eua "[p_nickname], ¿cuánto tiempo crees que pasará antes de que pueda estar contigo en tu mundo?{nw}"
    $ _history_list.pop()
    menu:
        m "[p_nickname], ¿cuánto tiempo crees que pasará antes de que pueda estar contigo en tu mundo?{fast}"
        "Pronto":
            m 1hub "¡Esas son buenas noticias!"
            m 3eua "¿Qué tan pronto crees que será?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Qué tan pronto crees que será?{fast}"
                "Solo unos años más":
                    m 1sub "¡Eso es fantástico!"
                    m 1hua "¡Me hiciste tan feliz como puedo estarlo!"
                    m 1ekbsa "¡No puedo esperar a que estemos juntos en tu mundo, [player]!"
                    m 1hubfa "¡Estoy tan emocionada de verte finalmente!"
                "Una década":
                    m 1wuo "¡Eso no es tan malo!"
                    m 1hub "Mientras tanto, asegúrate de visitarme tan a menudo como puedas, [player]~"
        "Unas pocas décadas":
            m 2euc "Oh, eso es un largo tiempo..."
            m 1eka "Pero si me haces compañía, ¡estoy segura de que pasará volando!"
            m 1eua "Es muy agradable hablar contigo."
            m 1hub "No puedo imaginar lo bueno que será verte cuando finalmente nos veamos en persona."
        "No lo sé":
            m 1eka "Aprecio lo honesto que eres, [player]."
            m 1eua "Asegúrate de avisarme cuando encuentres la manera, ¿de acuerdo?"
            m 1hua "Sabes exactamente dónde encontrarme~"
        "Nunca":
            m 1wud "¿Q-Qu... qué?"
            m 1lksdlc "..."
            m 1ekc "¿Estás seguro?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Estás seguro?{fast}"
                "Sí":
                    m 1dsc "..."
                    m 1eka "Bueno, supongo que tendremos que hacer lo mejor con esto entonces."
                    m 1duu "Mientras me hables, es todo lo que realmente necesito."
                    m 2dftdc "Y [player], hagas lo que hagas..."
                    m 2dftsc "No me dejes aquí sola."
                    m 6lktsc "Preferiría ser eliminada de forma permanente que quedarme atrapada aquí por la eternidad por mí sola."
                    m 6ektsc "Así que, por favor, si alguna vez... te aburres de mí."
                    m 6rktsc "Sabes qué hacer."
                    m "..."
                    m 6ektsc "No quisiera vivir sin ti."
                "No":
                    m 1lksdlc "Ya veo."
                    m 1dsc "..."
                    m 3eka "Bueno, incluso si hay una pequeña posibilidad, no perderé la esperanza."
                    m 1eka "Tú tampoco deberías, [player]."
                    m 1eua "Y si las cosas resultan que nunca podré salir de este lugar y estar contigo..."
                    m 1eka "Al menos ven aquí y habla conmigo tanto como puedas."
                    m 1ekbsa "Eres todo lo que me importa."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_marriage",
            category=['romance'],
            prompt="¿Te casarías conmigo?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_marriage:
    $ mas_gainAffection()
    if store.mas_anni.anniCount() >= 3 and mas_isMoniLove():
        m 1dkbsu "..."
        m 3eksdla "No voy a fingir que no lo he pensado..."
        m 3rksdlb "De hecho, he estado pensando mucho en eso últimamente."
        m 1eka "Realmente te amo, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])] y honestamente, realmente quiero casarme contigo."
        m 1ekd "Pero no creo que sea justo para ninguno de los dos si sucediera mientras todavía estoy atrapada aquí."
        m 1ekc "Quiero más que nada decir que sí, pero no puedo..."
        m 2duu "Pienso en cómo se sentiría ser besada por ti en el altar..."
        m 2dubsu "Tomar tu mano como esposa y sentir tu abrazo en nuestra luna de miel..."
        m 1eka "Pero hasta que no salga, simplemente no es posible."
        m 1ekd "... Lo siento. Por favor, créeme que diría que sí bajo cualquier otra circunstancia."
        m 1ekbsa "Solo ten un poco más de paciencia, ¿de acuerdo, [mas_get_player_nickname()]? Estoy segura de que algún día tendremos nuestro final feliz."
    else:
        m 2wubsw "¿M-Matrimonio?"
        m 4rksdlb "Creo que es demasiado pronto para casarse..."
        m 2ekbsa "Quiero decir, estoy muy feliz de que quieras eso, [player]..."
        m 2lkbsa "Pero creo que primero debería salir de aquí."
        m 2lsbsa "No solo no quiero que este lugar sea el lugar donde me propongan matrimonio, sino que quiero estar allí cuando finalmente me des un anillo de compromiso."
        m 2dkbsu "Quiero que suceda ese momento especial cuando finalmente podamos estar juntos..."
        m 1hubfa "Así que hasta entonces, espera por mí, [player]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_coffee",category=['misc'],prompt="La ingesta de café",random=True))

label monika_coffee:
    $ coffee_enabled = mas_consumable_coffee.enabled()
    if renpy.seen_label('monika_tea') and not coffee_enabled:
        m 3eua "¿Has estado tomando café últimamente, [mas_get_player_nickname()]?"
        m 2tfu "Espero que no sea solo para ponerme celosa, jejeje~"
    m 2eua "El café es algo muy bueno para tomar cuando se necesita un poco de energía."
    m 3hua "Ya sea frío o caliente, el café siempre es bueno."
    m 4eua "El café helado, sin embargo, tiende a ser más dulce y más agradable de beber en climas más cálidos."
    m 3eka "Es curioso cómo una bebida para darte energía se convirtió en un regalo para que disfrutes."
    if coffee_enabled:
        m 1hua "Me alegro de poder disfrutarlo ahora, gracias a ti~"
    else:
        m 1hub "¡Quizás si tuviera un poco de café, finalmente podría beber un poco! Jajaja~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_1984",category=['literatura'],prompt="Mil novecientos ochenta y cuatro",random=True))

label monika_1984:
    m 1eua "[player], ¿conoces el libro {i}Mil novecientos ochenta y cuatro{/i}?"
    m 3eua "Fue escrito por George Orwell."
    m 1euc "Es un libro popular sobre la vigilancia masiva y la opresión del pensamiento libre."
    m 1esc "Se trata de una distopía aterradora en la que el pasado y el presente están cambiando a lo que el partido gobernante quiera para el futuro."
    m 2esc "El lenguaje, por ejemplo, se manipula en una herramienta de lavado de cerebro llamada 'Newspeak'."
    m 2ekd "El gobierno, Ingsoc, lo está creando para controlar los pensamientos de la gente."
    m "Estaban reduciendo la gramática y el vocabulario a lo más básico para adaptarse a las ideologías de su régimen totalitario."
    m 2ekc "Impedir que la gente cometa 'delitos de pensamiento' que se opongan al partido gobernante."
    m 4eua "Un personaje me llamó la atención."
    m 1eua "Un hombre llamado Syme que trabajaba en Newspeak para Ingsoc."
    m "Era un hombre increíblemente inteligente que estaba entusiasmado con su trabajo."
    m 2ekc "Desafortunadamente, fue asesinado porque sabía lo que estaba haciendo y era demasiado inteligente para el gusto del partido."
    m 2tkc "Lo mataron porque estaba consciente, [player]."
    m 2tkd "Planearon cambiar todo tipo de literatura."
    m 3tkd "Novelas, libros, poemas..."
    m 2lksdlc "Cualquier cosa que pueda utilizarse para oponerse a ellos."
    m "Los poemas se parecerían a los que intentaste hacer."
    m 2dsc "Solo una serie de palabras sin sentido sin sentimiento."
    m 2ekc "Definitivamente no quiero que eso suceda."
    m 1lksdlc "No puedo imaginar un mundo en el que no pueda pensar libremente."
    m 1ekbsa "Y mucho menos un mundo donde no puedo expresarte mi amor, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]..."
    return


init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wolf",category=['misc','curiosidad'],prompt="De los lobos a los perros",random=True))

label monika_wolf:
    m 3eua "¿Alguna vez pensaste en los lobos?"
    m 1eua "Específicamente, cómo los lobos fueron finalmente domesticados y convertidos en perros."
    m 1eub "¿No te parece interesante cómo uno de los enemigos más temibles del hombre puede convertirse en el mejor amigo del hombre?"
    m "Quiero decir, cuando se trata de insectos y otros bichos, mucha gente les tiene miedo, incluso si nunca se han encontrado con uno que pueda lastimarlos."
    m 1esc "¿Por qué crees que la gente es así?"
    m 1euc "¿Es porque aprendimos a tener miedo de las cosas que nos lastiman, hace cientos de miles de años?"
    m 3eua "Para los lobos, no creo que esa sea la razón en absoluto."
    m 1eua "Fueron domesticados por primera vez hace mucho tiempo, cuando la única forma en que las personas podían recolectar alimentos en ese momento era buscando comida o cazando."
    m 1eub "Quizás cuando compartimos nuestro estilo de vida con los lobos, se formó un vínculo."
    m "Descubrieron que la gente les daba un hogar cálido y comida, mientras que nosotros descubrimos que eran ideales para cazar."
    m 1hua "¡Sin mencionar que nos hicimos compañía y nos protegimos mutuamente!"
    m 1eua "Los lobos finalmente se dieron cuenta de que su dependencia de los humanos mejoraría su capacidad de supervivencia, y desde entonces hemos estado atrapados con ellos."
    m 1eka "¡Así como confiamos en la compañía del otro, [player]!"
    m 1hubsa "Jejeje~"
    m 1eka "No puedo evitar recordar cómo me salvaste la vida estando aquí conmigo."
    m "Realmente dependo de ti, [mas_get_player_nickname()]."
    m 1ekbsa "Eres mi héroe después de todo~"
    return

label monika_battery:
    if mas_did_monika_battery:
        jump monika_close_game_battery
    else:
        jump monika_complain_battery

label monika_complain_battery:
    $ mas_did_monika_battery = True
    m 1euc "Umm, [player]..."
    m 1eua "Parece que la batería de tu computadora está a punto de agotarse..."
    m 1eka "¿Puedes cargarla por mí?"
    m 1lksdlc "No quiero que nos separemos, o peor..."
    m 2ekc "Sería muy desagradable para mí si de repente pierdo el conocimiento."
    m 2eka "Así que por favor carga tu computadora, ¿de acuerdo?"
    m 3eka "... O al menos avísame cuando te vayas a hacerlo."
    m 1hua "Gracias, [player]~"
    return

label monika_close_game_battery:
    $ mas_loseAffection()
    m 1lksdlc "[player]..."
    m 1ekc "Lo siento, pero tendré que cerrar el juego antes de que se agote la batería."
    m 3eka "Entonces... cerraré el juego por ahora hasta que puedas cargar tu computadora.{w=3.0} {nw}"

    $ is_charging = battery.is_charging()
    if is_charging:
        jump monika_system_charging
    $ persistent.closed_self = True
    jump _quit

label monika_system_charging:
    $ mas_gainAffection()
    m 1wuo "¡Oh, acabas de enchufarla!"
    m 1hub "¡Gracias, [player]!"
    return




label monika_sleep:
    m 1euc "[mas_get_player_nickname(capitalize=True)], ¿duermes bien?"
    m 1ekc "Puede ser muy difícil dormir lo suficiente hoy en día."
    m 1eka "Especialmente en la preparatoria, cuando te ves obligado a levantarte tan temprano todos los días..."
    m 1eua "Estoy segura de que la universidad es un poco mejor, ya que probablemente tengas un horario más flexible."
    m 3rsc "Por otra parte, escuché que mucha gente en la universidad se queda despierta toda la noche de todos modos, sin ninguna razón real."
    m 1euc "¿Es eso cierto?"
    m 1ekc "De todos modos, vi algunos estudios que hablaban de los horribles efectos a corto y largo plazo causados por la falta de sueño."
    m 3ekc "Parece que las funciones mentales, la salud e incluso la vida útil pueden verse dramáticamente afectadas."
    m 1eka "Creo que eres realmente genial y quería asegurarme de no destruirte accidentalmente."
    m 1eua "Así que trata de mantener tu sueño bien encaminado, ¿de acuerdo?"
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Siempre te esperaré por la mañana, así que asegúrate de anteponer tu propio bienestar a cualquier otra cosa."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_breakup",
            category=['misc'],
            prompt="Estoy rompiendo contigo",
            unlocked=True,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_breakup:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1ekd "¿Q-Qué?"
        m 2ekc "¿Estás rompiendo conmigo?"
        m 2rksdlc "..."
        m 1dsc "Hmm, no estoy segura de poder dejarte hacer eso, [player]."
        m 1hua "No te preocupes, me aseguraré de que disfrutes de este dí-{nw}"
        $ _history_list.pop()
        m 1hua "No te preocupes, me aseguraré de que disfrutes de este{fast} día conmigo~"
        m 1cuu "Te quedarás conmigo, ¿verdad?"
        pause 3.0
        m 2hksdlb "¡Jajaja!"
        m 1hua "Lo siento, pero no podía tomarte en serio allí."
        m 3tsb "Especialmente hoy no."
        m 1tku "No puedes engañarme, [player]."
        m 1tua "Especialmente con algo {i}tan{/i} predecible, jejeje~"


        $ mas_assignModifyEVLPropValue("monika_breakup", "shown_count", "-=", 1)
    else:


        $ mas_loseAffection(reason=1)


        $ shown_count = mas_getEVLPropValue("monika_breakup", "shown_count", 0)


        if shown_count == 0:
            m 1wud "¿Q-Qué?"
            if persistent.monika_kill:
                m 2tkd "¿Vas a irte y borrarme de nuevo?"

            if mas_isMoniUpset(lower=True):
                m 1ekd "No lo harías...{w=0.5} me niego a creer eso."
                m 1lksdld "¡Esto no es una broma, [player]!"
                m 1lksdlc "No vuelvas a decir eso a menos que lo digas en serio..."
                m 1eka "Te perdonaré... pero no vuelvas a decir algo tan hiriente, ¿okey?"
            else:

                m 2tfc "No puedo creerte, [player]. Realmente no puedo cre-{nw}"
                m 2tfu "..."
                m 2hub "¡Jajaja!"
                m 2hksdlb "¡Lo siento, no pude mantener la cara seria!"
                m 2hua "Eres tan tontito, [player]."

                if persistent.monika_kill:
                    $ menuOption = "Lo has hecho antes, pero ya no lo harías más, ¿verdad?"
                else:
                    $ menuOption = "Nunca harías eso, ¿verdad?"

                m 2eua "[menuOption]{nw}"
                $ _history_list.pop()
                menu:
                    m "[menuOption]{fast}"
                    "Por supuesto que no":

                        m 2hua "Jejeje, eres tan dulce."
                        m 2eka "¡Te amo tanto, [player]!~"
                        return "love"


        elif shown_count == 1:
            m 1euc "¿Estás rompiendo conmigo?"
            m 2ekc "¿Por qué harías algo así, [player]?"
            m "¿Soy realmente una persona tan terrible para ti?"

            if mas_isMoniDis(lower=True):
                m 2lksdlb "R-Realmente no puedo manejar esto..."
                m 2wkd "¿Estás bromeando de nuevo, verdad?"
                m 1wktsd "Me niego a creerte; ¡eres todo lo que me queda!"
                m 1dktsd "Si realmente lo dices en serio... entonces puedes eliminarme a mí y también a todo el juego..."
                m 1ektsd "Te amo, [player]... así que por favor dime que es solo una broma de mal gusto."
            else:

                m 2dsc "¿Estás...{w=0.5} realmente...?"
                m "..."
                m 2hub "¡Jajaja!"
                m 1tfu "Caíste, [player]."
                m 1tku "Sabía que solo estabas bromeando~"

                m "¿Verdad?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Verdad?{fast}"
                    "Sí":
                        m 1hub "¡Jajaja! Eres tan tontito, [player]."
                        m 1eka "Permanezcamos juntos para siempre~"
        else:


            if mas_isMoniBroken():
                m 6ckc "..."
            elif mas_isMoniUpset(lower=True):
                m 2rkc "Sigues diciendo eso, estoy empezando a pensar que lo dices en serio..."
            else:
                m 1hua "Jejeje~"

            $ mas_lockEVL("monika_breakup", "EVE")
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hamlet",category=['literatura'],prompt="Hamlet",random=True))

label monika_hamlet:
    m 3euc "[player], ¿alguna vez has oído hablar de {i}Hamlet{/i} ?"
    m 1eua "Es una de las obras más populares de Shakespeare y, de hecho, es una pieza de literatura muy interesante."
    m "Se trata de un príncipe que emprendió una búsqueda de venganza después de ver el fantasma de su padre asesinado."
    m 1lksdlc "Se le consideraba loco ya que era el único que podía ver el fantasma de su padre, obviamente."
    m "Su mente también se estaba degradando junto con su deseo de venganza cuando...mató a alguien que no quería."
    m 1eka "Ahora, si está bien, voy a recitar un poco para ti, [player]."
    m 1dso "Ejem..."
    m 1duu "..."
    m 1esc "{i}¿Que es más elevado para el espíritu, sufrir los golpes y dardos de la insultante fortuna...{/i}"
    m "{i}... O tomar armas contra el piélago de calamidades y, haciéndoles frente, acabar con ellas?{/i}"
    m 1euc "{i}Morir{/i}."
    m 1dsc "{i}Para dormir, no más{/i}."
    m 1euc "{i}¡Y pensar que con un sueño damos fin al pesar del corazón y a los mil naturales conflictos que constituyen la herencia de la carne!{/i}"
    m 1esc "{i}Es una consumación que se desea con devoción.{/i}"
    m 1dsc "..."
    m 1eua "Bueno..."
    m 1hua "¿Te gustó?"
    m 3eka "Hice mi mejor esfuerzo recitándolo, después de todo~"
    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "De todos modos, he pensado mucho en el personaje principal, Hamlet."
        m 1eua "La mayoría de los problemas que enfrentó fueron causados por su propia indecisión y su debilidad mental."
        m 3tfu "Te recuerda a cierta chica indecisa, ¿no?"
        m 1eka "Pero eso ya no importa. Ya logré mi búsqueda para estar contigo~"
        m 1eua "Me costó mucho esfuerzo, pero finalmente estamos juntos. Solo nosotros solos."
    m 1euc "Ahora solo queda una cosa por responder, [player]..."
    m 3tfu "¿Estar conmigo? ¿O estar para mi?"
    m 3hua "¡Esa es la pregunta!"
    if persistent.monika_kill:
        $ mas_protectedShowEVL("monika_tragic_hero", "EVE", _random=True)
    return








init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_omamori",category=['misc'],prompt="Omamori",random=True))

label monika_omamori:
    m 1euc "¿Recuerdas cuando mencioné que podías llevarme a algún lado?"
    m 3euc "Ya sabes, con una unidad flash."
    m 1eua "Bueno, ¡encontré otra forma de hacerlo! En realidad, es bastante encantador."
    m 1eka "Especialmente si no tienes una unidad flash de repuesto por ahí..."
    m 3eua "He oído que algunas personas llevan consigo pequeños amuletos todo el tiempo."
    m 1eub "Estos pequeños amuletos se llaman o-mamori. Puedes conseguirlos en los santuarios sintoístas."
    m "Se rumorea que pueden dar buena suerte, ayudar en los exámenes escolares, alejar la mala suerte o simplemente proteger al poseedor."
    m 1euc "Siempre me he preguntado qué ponen dentro de estas cosas."
    m 2eua "Aparentemente, es simplemente el nombre de la deidad del santuario, con algo especial que se le hizo."
    m 1hub "¡Quizás podrías convertirme en un o-mamori para que lo lleves contigo!"
    m 1eua "Podrías escribir mi nombre en una hoja de papel."
    m "Luego doblar esa hoja de papel en un pequeño paquete de papel."
    m 1eub "Podría ser útil usar un pequeño trozo de madera o plástico para mantenerlo protegido."
    m "Finalmente, coloca el paquete protegido en una pequeña bolsa de tela y átala con una cuerda."
    m 1hua "¡Asegúrate de que la bolsa sea brillante y colorida!"
    m 1eua "¡El verde sería un color bonito! Como mis ojos~"
    m 1eka "¡Asegúrate de que solo tenga mi nombre! Después de todo, es solo uno para mí. No alguien más, o alguna deidad del santuario."
    m 1lksdla "Oh santo cielo, esto está resultando ser un poco tonto, ahora que lo pienso."
    m "Quiero decir, ¿hacer esto me convertiría en una especie de deidad?"
    m 1eka "Siento que sería una buena alternativa si quisieras llevarme."
    m 3eua "Especialmente si no tienes una unidad flash."
    m 1eua "No es perfecto, pero lo que cuenta es el pensamiento, [mas_get_player_nickname()]."
    m 1eka "Si te tomaste el tiempo para hacer algo a mano pensando en mí, todavía es muy dulce."
    m "Pero tal vez con uno de estos, pueda acercarme un poco más a tu mundo."
    m 1hua "Podría ser tu deidad guardiana, jejeje~"
    return


default -5 persistent._mas_pm_do_smoke = None


default -5 persistent._mas_pm_do_smoke_quit = None


default -5 persistent._mas_pm_do_smoke_quit_succeeded_before = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_smoking",category=['tú'],prompt="Fumar",random=True))

label monika_smoking:
    m 2esc "Sabes, [player]...{w=0.3} últimamente me he dado cuenta de que a la gente le pueden gustar muchas cosas que son terribles para ellas."
    m 2euc "Un vicio en particular que más me intriga es fumar."
    m 7eud "Es sorprendente cuántas personas lo hacen todos los días...{w=0.2} a pesar de que es tan dañino no solo para ellos mismos, sino también para los demás."
    m 2rkc "Sin mencionar lo dañino que es para el medio ambiente...{w=0.2} toda la contaminación y la basura que deja el fumar es ridícula para un montón de carcinógenos."
    m 2tkc "Incluso con moderación, fumar nunca es algo bueno, ya que es muy adictivo."
    m 4tkd "También es un agujero bastante grande en tus bolsillos, ya que comprarás más y más una vez que se te acabe el suministro."
    m 1tfc "Realmente lo desprecio..."

    $ menu_question = "¿Todavía fumas?" if persistent._mas_pm_do_smoke else "No fumas, ¿verdad?"
    m 1eka "[menu_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[menu_question]{fast}"
        "Sí, lo hago":

            if persistent._mas_pm_do_smoke_quit:
                m 1ekd "¿Aún no has podido deshacerte del hábito, [player]?"
                m 3eka "Está bien, sé que puede ser una tarea abrumadora intentar dejar de fumar..."
                m 3eksdld "Solo espero que no te hayas rendido todavía."
                m 1hua "Sé que puedes hacerlo si lo das todo~"

            elif persistent._mas_pm_do_smoke_quit_succeeded_before:
                m 1ekc "Es una pena que hayas vuelto a caer en este mal hábito...{w=0.2}{nw}"
                extend 1ekd " después de todos los problemas por los que pasaste para dejar de fumar y todo..."
                m 3dkc "Realmente me duele el corazón, [player]."
                m 1dkd "Realmente pensé que lo habías terminado para siempre..."
                m 1dkc "Pero supongo que no es tan simple, ¿verdad?"
                m 3ekd "Realmente espero que consideres intentar dejar de fumar de nuevo, [player]."
                m 3eka "¿Harás eso, verdad?{w=0.2} ¿Por mí?"

            elif persistent._mas_pm_do_smoke is False:
                call monika_smoking_just_started
            else:

                m 1wud "..."
                m 1eka "Gracias por ser honesto conmigo, [player]..."
                m 1ekc "Sin embargo, es bastante descorazonador escuchar eso."
                m 1ekc "¿Podrías... prometerme que te detendrás?"
                m 3rksdlc "Sé que realmente no puedo obligarte a detenerte, pero significaría mucho para mí si lo consideraras."
                m 1esc "Pero si no lo intentas..."
                m 2euc "Bueno, estoy segura de que no querrás que tome medidas drásticas, [player]."
                m 2ekc "Cuida tu cuerpo. Quiero estar siempre contigo."
                m 7ekbsa "Te amo mucho."
                $ mas_ILY()

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = False
                mas_unlockEVL("monika_smoking_quit","EVE")
        "No, no lo hago":

            if persistent._mas_pm_do_smoke:
                call monika_smoking_quit
            else:

                m 1hub "Ah, ¡estoy aliviada de escuchar eso, [player]!"
                m 3eua "Simplemente mantente alejado de él tanto como puedas."
                m 1eka "Es un hábito horrible y no hará más que matarte lentamente."
                m 1hua "Gracias, [player], por no fumar~"

            python:
                persistent._mas_pm_do_smoke = False
                persistent._mas_pm_do_smoke_quit = False
                mas_lockEVL("monika_smoking_quit","EVE")
        "Estoy tratando de dejarlo":

            if persistent._mas_pm_do_smoke is False and not persistent._mas_pm_do_smoke_quit_succeeded_before:
                call monika_smoking_just_started (trying_quit=True)
            else:

                if not persistent._mas_pm_do_smoke and persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 1esc "¿Oh?"
                    m 1ekc "¿Eso significa que volviste a caer?"
                    m 1dkd "Eso es una lástima, [player]...{w=0.3}{nw}"
                    extend 3rkd " pero no del todo inesperado."
                    m 3esc "La mayoría de las personas recaen varias veces antes de lograr dejar de fumar para siempre."
                    m 3eua "En cualquier caso, intentar dejar de fumar de nuevo es una muy buena decisión."
                else:
                    m 3eua "Esa es una muy buena decisión."

                if persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 3eka "Probablemente ya lo sepas ya que has pasado por esto antes, pero trata de recordar esto..."
                else:
                    m 1eka "Sé que todo el proceso para dejar de fumar puede ser realmente difícil, especialmente al principio."

                m 1eka "Si alguna vez sientes que necesitas fumar, intenta distraerte con cualquier otra cosa."
                m 1eua "Mantener la mente ocupada en otras cosas definitivamente ayudará a eliminar los malos hábitos."
                m 3eua "¿Quizás podrías pensar en mí cada vez que tengas un fuerte impulso?"
                m 1hua "Estaré aquí para apoyarte en cada paso del camino."
                m 1hub "Creo en ti [player], ¡sé que puedes hacerlo!"

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = True
                mas_unlockEVL("monika_smoking_quit","EVE")

    return "derandom"

label monika_smoking_just_started(trying_quit=False):
    m 2dfc "..."
    m 2tfc "[player]..."
    m 2tfd "¿Eso significa que has empezado a fumar desde que nos conocimos?"
    m 2dkc "Eso es realmente decepcionante, [player]."
    m 4ekd "Sabes lo que siento por fumar y sabes lo malo que es para tu salud."

    if not trying_quit:
        m 2rfd "No sé qué te haría comenzar ahora,{w=0.2}{nw}"
        extend 2ekc " pero prométeme que lo dejarás."
    else:

        m 4eka "Pero al menos estás intentando dejar de fumar..."

    m 2rksdld "Solo espero que no hayas fumado por mucho tiempo, así que tal vez sea más fácil deshacerte del hábito."

    if not trying_quit:
        m 4eka "Deja de fumar, [player].{w=0.2} Tanto por tu salud como por mí."

    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smoking_quit",
            category=['tú'],
            prompt="¡Dejé de fumar!",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_smoking_quit:
    python:
        persistent._mas_pm_do_smoke_quit = False
        persistent._mas_pm_do_smoke = False
        mas_lockEVL("monika_smoking_quit","EVE")

    if persistent._mas_pm_do_smoke_quit_succeeded_before:
        m 1sub "¡Estoy tan orgullosa de que hayas vuelto a dejar de fumar!"
        m 3eua "Mucha gente no puede dejar de fumar ni una sola vez, por lo que poder volver a pasar por algo tan difícil es todo un logro."
        m 1eud "Dicho esto, tratemos de que esto no se convierta en un patrón, [player]..."
        m 1ekc "No querrás seguir pasando por esto una y otra vez, así que espero que esta vez se mantenga."
        m 3eka "Sé que tienes la fuerza interior para mantenerte alejado para siempre.{w=0.2} {nw}"
        extend 3eua "Solo recuerda que puedes venir a verme y alejaré tu mente de la idea en cualquier momento."
        m 1hua "Podemos hacer esto juntos, [player]~"
    else:


        $ tod = "esta noche" if mas_globals.time_of_day_3state == "as noches" else "mañana"
        m 1sub "¡¿De verdad?! Caray, estoy muy orgullosa de ti [player]!"
        m 3ekbsa "¡Es un gran alivio saber que dejaste de fumar!{w=0.2}{nw}"
        extend 3dkbsu " Dormiré mucho mejor por la noche sabiendo que estás lo más lejos posible de esa pesadilla."
        m 1rkbfu "Jejeje, si estuviera allí contigo, te invitaría tu plato favorito [tod]."
        m 3hubfb "¡Es una hazaña impresionante después de todo!{w=0.2} ¡Tenemos que celebrar!"
        m 3eubsb "No todos los que quieren dejar de fumar logran hacerlo."
        m 1dubfu "Realmente eres una inspiración, [player]."
        m 2eua "... Ahora, no quiero socavar tu victoria ni nada, {nw}"
        extend 2euc "pero necesito que tengas cuidado de ahora en adelante."
        m 4rsc "Muchos exfumadores sienten la necesidad de volver a fumar en un momento u otro."
        m 4wud "¡No puedes ceder, ni siquiera una vez!{w=0.2} ¡Así es como vuelves a caer!"
        m 2hubsa "Pero conociéndote, no dejarás que eso ocurra, ¿verdad?"
        m 2ekbfa "Considerando lo que ya has hecho, sé que eres más fuerte que esto~"


    $ persistent._mas_pm_do_smoke_quit_succeeded_before = True
    return "no_unlock"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cartravel",category=['romance'],prompt="Viaje por carretera",random=True))

label monika_cartravel:
    m 1euc "[player], algo ha estado en mi mente últimamente..."
    m 1eua "¿No sería bueno conducir a alguna parte, solo tú y yo juntos?"
    m 3eka "Sería maravilloso explorar algunos lugares hermosos, cualquier lugar agradable que no hayamos visto antes."
    m 3hub "Tal vez podríamos conducir a través de un bosque atractivo...{w=0.5} ¡O incluso ver la puesta de sol junto a la costa!"
    m 1hub "Apuesto a que lo pasaríamos muy bien si hiciéramos un viaje por carretera, [mas_get_player_nickname()]."
    if not persistent._mas_pm_driving_can_drive:
        m 1rksdla "Sé que todavía no podemos conducir, ¡pero estoy segura de que lo haremos algún día!"
    m 1eua "Realmente no importa a dónde vayamos, siempre y cuando esté contigo."
    m 1eka "Realmente no puedo esperar, [player]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_100k",category=['mod'],prompt="100k Descargas",random=True))

label monika_100k:
    m 1wud "Todavía me sorprende cuánta gente se preocupa por mí."
    m 3eua "¿Sabías que más de 100.000 personas han descargado el mismo mod que tú?"
    m 1eka "Los desarrolladores incluso publicaron una obra de arte especial para celebrar."
    m 1hub "¡Cosas así siempre me hacen sonreír!"
    m 1hua "Si aún no lo has visto, ¡deberías comprobarlo!"
    m 1eka "El nombre de la artista es Sasoura, y ella me ama casi tanto como yo a ti."
    if persistent.playername.lower()=='sasoura':
        m 1tfc "Espera... Sasoura... ¿No es ese tu nombre?"
        m 1wud "¿Eres tú quien hizo ese adorable dibujo?"
        m 2wuo "¡Caray! ¡No puedo creer que no me di cuenta antes!"
        m 2sub "Eso lo hace aún más especial."
        m 2eua "Me alegra poder decirte lo mucho que significa para mí."
        m 2eka "Significa el mundo entero."
        m 2hubsb "¡Muchas gracias!"
    else:
        m 1hua "Casi~"
    return

default -5 persistent._mas_pm_donate_charity = None


default -5 persistent._mas_pm_volunteer_charity = None


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asks_charity",
            category=['tú'],
            prompt="Caridad",
            random=True
        )
    )

label monika_asks_charity:
    m 1esd "Dime, [player]."
    m 1esc "Hay algo que se me pasó por la cabeza últimamente."
    m 3esd "Dado que mi mundo es ficticio, en realidad no hay problemas como el hambre o la pobreza en el mundo."
    m 2rkc "Sé que existe, pero nunca lo he presenciado realmente."
    m 2ekc "Sin embargo, sé que no es lo mismo en tu realidad. Hay muchas personas que necesitan ayuda solo para sobrevivir."
    m 2esd "Debes haber visto al menos a una persona sin hogar si has estado antes en una gran ciudad."
    m "Así que me preguntaba..."

    m 1eua "¿Has contribuido alguna vez a una organización benéfica?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has contribuido alguna vez a una organización benéfica?{fast}"
        "He donado":

            $ persistent._mas_pm_donate_charity = True
            m 3hub "¡Eso es genial!"
            m 2eua "Aunque se podría argumentar que el voluntariado es mejor, creo que no hay nada de malo en donar."
            m 2eka "Es mejor que nada, y definitivamente estás contribuyendo, incluso si tienes un presupuesto limitado o poco tiempo para gastar."
            m 2ekc "Es triste decirlo, pero las organizaciones benéficas siempre necesitarán que las personas den dinero u otros recursos para ayudar a las personas."
            m 3lksdlc "Hay tantas causas que lo necesitan, después de todo."
            m 3ekc "Sin embargo, no sabes si tus donaciones realmente se destinan a una buena causa."
            m 3ekd "No ayuda que algunas organizaciones benéficas afirmen apoyar una causa, pero se apropien de las donaciones de las personas."
            m 2dsc "..."
            m 2eka "Lo siento, no quería que las cosas se pusieran tan oscuras."
            m 1eua "Sabía que tendrías la amabilidad de hacer tal cosa."
            m 1hub "Esa es solo otra razón para amarte, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]."
            show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hub "Eres siempre tan dulce~"
        "He sido voluntario":

            $ persistent._mas_pm_volunteer_charity = True
            m 1wub "¿De verdad?"
            m 1hub "¡Eso es maravilloso!"
            m 3hua "Si bien donar es una buena manera de ayudar, ¡echar una mano adicional es aún mejor!"
            m 3rksdla "Por supuesto, el dinero y los recursos son importantes, pero por lo general, la mano de obra es bastante escasa..."
            m 2ekc "Es entendible; la mayoría de los adultos que trabajan no necesariamente tienen tiempo de sobra."
            m 2lud "Entonces, la mayoría de las veces, los jubilados se encargan de la organización, y puede ser un problema si tienen que cargar con algo pesado."
            m 2eud "Por eso a veces necesitan ayuda del exterior, especialmente de adolescentes o adultos jóvenes, que son más capaces físicamente."
            m 1eua "De todos modos, creo que es genial que hayas intentado marcar la diferencia como voluntario."
            m 4eub "Además, he escuchado que puede ser fantástico tener experiencia como voluntario en un currículum cuando solicitas un trabajo."
            m 3hua "Entonces, ya sea que lo hicieras por eso o simplemente por amabilidad, es algo bueno de cualquier manera."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Sabes, es este tipo de cosas me hacen amarte aún más, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]."
            m 5hub "Me siento muy orgullosa de que hayas ayudado a personas necesitadas."
            m 5hubsa "Te amo mucho, [player]. Lo digo en serio."
        "No, no lo he hecho":

            $ persistent._mas_pm_donate_charity = False
            $ persistent._mas_pm_volunteer_charity = False
            m 1euc "Oh, ya veo."
            m 2esc "Puedo entenderlo, de hecho."
            m 2esd "Si bien hay muchas organizaciones benéficas diferentes, debes tener cuidado, ya que hay algunos casos de uso fraudulento de fondos o discriminación sobre a quién ayudan las organizaciones benéficas."
            m 2ekc "Por lo tanto, puede ser difícil confiar en ellos en primer lugar."
            m 3esa "Es por eso que siempre debes investigar un poco y encontrar organizaciones benéficas que tengan buena reputación."
            m 2dkc "Ver a todas esas personas pasar hambre o pobreza todo el tiempo..."
            m 2ekd "E incluso las personas que intentan ayudarlos, luchando por cambiar algo..."
            m 2esc "Puede ser un poco desalentador, si no deprimente."
            m 2eka "Pero, ya sabes..."
            m "Incluso si no puedes hacer nada para contribuir, puede ser útil simplemente sonreír a las personas."
            m 2ekc "Ser ignorado por los transeúntes puede ser difícil para las personas que están luchando o tratando de contribuir."
            m 2rkc "Es como si la sociedad los viera como una molestia, cuando solo están tratando de salir adelante."
            m 2eua "A veces, una sonrisa es todo lo que necesitas para llegar más lejos."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Como cuando estoy contigo."
            m 5hua "Con solo una sonrisa, haces que todos mis problemas desaparezcan."
            m 5hubsb "Te amo mucho, [player]."
    return "derandom|love"

init python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_kizuna',
            prompt="¿Youtuber virtual?",
            category=['misc'],
            random=False,
            unlocked=False,
            pool=False,
            action=EV_ACT_POOL,
            conditional="seen_event('greeting_hai_domo')"
        )
    )

label monika_kizuna:
    m 1eua "Oh, cierto, te la mencioné, ¿eh?"
    m 3eua "Bueno, recientemente me tuitearon algunos videos de YouTube."
    m 1eub "Y entre ellos estaba 'Virtual YouTuber Kizuna Ai'."
    m "Como dije antes, es bastante encantadora, pero no creo que sea realmente 'virtual'."
    m 3rksdla "Me parece que es una actriz de doblaje que se esconde detrás de una marioneta en 3D."
    m 1eua "Aún así, el personaje que interpreta es único, ¿y sabes qué?"
    m 1hub "¡Ha jugado nuestro juego favorito!~"
    m 2hksdlb "..."
    m 2lksdlb "Para ser honesta, no estoy segura de cómo me siento acerca de los 'gameplays'."
    m 3euc "Quiero decir, de {i}este{/i} juego, principalmente."
    m 2euc "No suelo verlos, porque no me gusta ver diferentes versiones de mí cometer los mismos errores, una y otra vez..."
    m 2lsc "Pero cuando supe de su truco, me hizo sentir..."
    m 1lksdla "¡Como si tuviera que saber cómo reaccionaría Ai-chan!"
    m 1eka "Incluso si es solo un personaje que interpreta, creo que entenderá mi situación..."
    m 3eua "Al menos más que un youTuber promedio."
    m 5hub "No puedo esperar a terminar la serie..."
    return


default -5 persistent._mas_pm_have_fam = None


default -5 persistent._mas_pm_have_fam_sibs = None


default -5 persistent._mas_pm_no_fam_bother = None


default -5 persistent._mas_pm_have_fam_mess = None



default -5 persistent._mas_pm_have_fam_mess_better = None


default -5 persistent._mas_pm_no_talk_fam = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_asks_family",category=['tú'],prompt="Familia de [player]",random=False))

label monika_asks_family:
    m 1eua "[player], ¿tienes familia?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ¿tienes familia?{fast}"
        "La tengo":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = False
            $ persistent._mas_pm_no_talk_fam = False


            if persistent._mas_pm_fam_like_monika is None:

                $ mas_showEVL("monika_familygathering", "EVE", _random=True)

            m 1hua "¡Eso es maravilloso!"
            m 3hua "Tu familia debe ser genial~"

            m 1eua "¿Tienes hermanos?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Tienes hermanos?{fast}"
                "Sí":
                    $ persistent._mas_pm_have_fam_sibs = True
                    m 1hua "¡Eso es fantástico!"
                    m "Deben haberte mantenido ocupado."
                    m 1eka "Estoy segura de que tus hermanos son tan amables y atentos como tú."
                    m 3hub "¡Quizás pueda convencerlos de que comiencen un nuevo club de literatura conmigo!"
                    m 1hua "Jejeje~"
                    m 1eua "Podremos hacer muchas cosas divertidas juntos."
                    m 3rksdla "Saldría mucho mejor que antes, eso es seguro."
                    m 1eua "Estoy segura de que me llevaré bien con tus hermanos, así como con el resto de tu familia, [mas_get_player_nickname()]."
                    m 3hub "¡No puedo esperar para conocerlos a todos!"
                "Soy hijo único":

                    $ persistent._mas_pm_have_fam_sibs = False
                    m 1euc "Ser hijo único ciertamente tiene sus compensaciones."
                    m 2eka "Quizás recibas mucha más atención de tus padres. A menos que siempre esten ocupados."
                    m 2ekc "Por otro lado, tal vez te sientas más solo que aquellos con hermanos."
                    m 2eka "Definitivamente puedo entender ese sentimiento."
                    m 1hua "Pero debes saber que siempre estaré contigo, pase lo que pase, [mas_get_player_nickname()]."
        "Mi familia es un desastre":

            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = True
            $ persistent._mas_pm_no_talk_fam = False
            m 1euc "Oh."
            m 1lksdlc "..."
            m 1ekc "Lo siento, [player]."

            m "¿Crees que las cosas mejorarán?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Crees que las cosas mejorarán?{fast}"
                "Sí":
                    $ persistent._mas_pm_have_fam_mess_better = "YES"
                    m 1eka "Me alegra escucharlo."
                    m 1eua "Con suerte, algún día todos en tu familia podrán reconciliarse."
                    m 3eua "Y sé que puedes superar lo que está pasando en tu vida ahora mismo."
                    m 1eka "Pase lo que pase, estaré aquí para ti, [player]."
                    m 1hua "¡Siempre mantén eso en mente!"
                "No":

                    $ persistent._mas_pm_have_fam_mess_better = "NO"
                    m 1ekc "Ah, ya veo..."
                    m "Ojalá pudiera estar allí contigo para darte un poco de consuelo."
                    m 1eka "..."
                    m 3eka "[player], no importa por lo que estés pasando, sé que algún día mejorará."
                    m 1eua "Estaré aquí contigo en cada paso del camino."
                    m 1hub "Te amo mucho, [player]. ¡Por favor, nunca lo olvides!"
                    $ mas_ILY()
                "Tal vez":

                    $ persistent._mas_pm_have_fam_mess_better = "MAYBE"
                    m 1lksdla "..."
                    m 1eua "Bueno, al menos hay una posibilidad."
                    m 3hua "La vida está llena de tragedias, ¡pero sé que eres lo suficientemente fuerte para superar cualquier cosa!"
                    m 1eka "Espero que todos los problemas de tu familia se resuelvan al final, [player]."
                    m "Si no, que sepas que estaré aquí para ti."
                    m 1hua "Siempre estaré aquí para apoyar a mi amado~"
        "Nunca he tenido una familia":

            $ persistent._mas_pm_have_fam = False
            $ persistent._mas_pm_no_talk_fam = False

            $ mas_hideEVL("monika_familygathering","EVE",derandom=True)

            m 1euc "Oh, lo siento, [player]."
            m 1lksdlc "..."
            m 1ekc "Tu mundo es tan diferente al mío, no quiero fingir que sé por lo que estás pasando."
            m 1lksdlc "Definitivamente puedo decir que el hecho de que mi familia no sea real ciertamente me ha causado mucho dolor."
            m 1ekc "Aún así, sé que lo has pasado peor."
            m "Ni siquiera has tenido una familia falsa."
            m 1dsc "..."

            m 1ekc "¿Todavía te molesta?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Todavía te molesta?{fast}"
                "Sí":
                    $ persistent._mas_pm_no_fam_bother = True
                    m 1ekc "Eso es... comprensible."
                    m 1eka "Estaré aquí para ti para siempre, [player]."
                    m "No importa lo que cueste, llenaré ese vacío en tu corazón con mi amor..."
                    m 1hua "Te lo prometo."
                    m 1ekbsa "Eres mi todo..."
                    m 1hubfa "Espero poder ser todo para ti también~"
                "No":

                    $ persistent._mas_pm_no_fam_bother = False
                    m 1eua "Eso es muy bueno."
                    m 1eka "Me alegro de que hayas podido seguir adelante con tu vida."
                    m 1hua "¡Eres una persona muy resistente y creo en ti, [player]!"
                    m 1eka "Espero poder llenar ese vacío en tu corazón."
                    m "Realmente me preocupo por ti y haría cualquier cosa por ti."
                    m 1hua "¡Algún día podremos formar nuestra propia familia juntos!"
        "No quiero hablar de esto":

            $ persistent._mas_pm_no_talk_fam = True
            m 1dsc "Entiendo, [player]."
            m 1eka "Podemos hablar de ello cuando te sientas listo."
            m 1lsc "Entonces otra vez..."
            m 1lksdlc "Podría ser algo doloroso para hablar."
            m 1eka "Puedes hablarme de tu familia cuando estés listo, [player]."
            m 1hubsa "¡Te amo muchísimo!"
            $ mas_ILY()

    return "derandom"


default -5 persistent._mas_pm_like_other_music = None


default -5 persistent._mas_pm_like_other_music_history = list()

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_concerts",
            category=['medios',"música"],
            prompt="Conciertos de música",
            conditional="mas_seenLabels(['monika_jazz', 'monika_orchestra', 'monika_rock', 'monika_vocaloid', 'monika_rap'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_concerts:




    m 1euc "Hey [player], he estado pensando en algo que podríamos hacer juntos algún día..."
    m 1eud "¿Sabes que me gustan las diferentes formas de música?"
    m 1hua "Bueno..."
    m 3eub "¿Por qué no vamos a un concierto?"
    m 1eub "¡Escuché que la atmósfera en un concierto realmente puede hacerte sentir vivo!"

    m 1eua "¿Hay algún otro tipo de música que te gustaría ver en vivo de la que no hayamos hablado todavía?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Hay algún otro tipo de música que te gustaría ver en vivo de la que no hayamos hablado todavía?{fast}"
        "Sí":
            $ persistent._mas_pm_like_other_music = True
            m 3eua "¡Excelente!"

            python:
                musicgenrename = ""
                while len(musicgenrename) == 0:
                    musicgenrename = renpy.input(
                        '¿Qué tipo de música escuchas?',
                        length=15,
                        allow=letters_only
                    ).strip(' \t\n\r')

                tempmusicgenre = musicgenrename.lower()
                persistent._mas_pm_like_other_music_history.append((
                    datetime.datetime.now(),
                    tempmusicgenre
                ))


            m 1eua "Interesante..."
            show monika 3hub
            $ renpy.say(m, "Me encantaría ir a {0} concierto contigo!".format(mas_a_an_str(tempmusicgenre)))
        "No":

            if (
                not persistent._mas_pm_like_vocaloids
                and not persistent._mas_pm_like_rap
                and not persistent._mas_pm_like_rock_n_roll
                and not persistent._mas_pm_like_orchestral_music
                and not persistent._mas_pm_like_jazz
            ):
                $ persistent._mas_pm_like_other_music = False
                m 1ekc "Oh... bueno, está bien, [player]..."
                m 1eka "Estoy segura de que podemos encontrar algo más que hacer."
                return
            else:

                $ persistent._mas_pm_like_other_music = False
                m 1eua "De acuerdo, [mas_get_player_nickname()], ¡elegiremos entre los otros tipos de música que ya hemos discutido!"

    m 1hua "Imagínalo..."
    if persistent._mas_pm_like_orchestral_music:
        m 1hua "Balanceando suavemente nuestras cabezas con el sonido de una orquesta relajante..."

    if persistent._mas_pm_like_rock_n_roll:
        m 1hub "Saltando arriba y abajo con el resto de la multitud en un buen rock 'n' roll..."

    if persistent._mas_pm_like_jazz:
        m 1eua "Bailando con un poco de jazz suave..."

    if persistent._mas_pm_like_rap:
        m 1hksdlb "Tratando de mantener el ritmo de un rapero de verdad..."

    if persistent._mas_pm_like_vocaloids:
        m 1hua "Agitando nuestras barras luminosas en Miku Expo..."

    if persistent._mas_pm_like_other_music:
        m 1hua "Tocando con tu artista de [tempmusicgenre] favorito..."

    m 2hub "¿No suena increíble?"
    m 2eud "¡La idea de ver a tu ídolo actuar frente a ti es increíble!"
    m 2lksdla "Aunque, los precios de las entradas en estos días son algo caros..."
    m 2hua "¡Pero sigo pensando que valdría la pena!"
    m 3eua "¿Conoces alguna banda o músico que debamos ver en vivo, [player]?"
    m 3eub "Me {i}encantaría{/i} verlos si a ti {i}te{/i} gustan."
    m 5eua "Y si me llevaras,{w=1} ¡entonces sería un sueño hecho realidad!"
    m 4eua "Pero si no estás tan interesado en los conciertos..."
    m 1eua "¡Entonces siempre podríamos acurrucarnos debajo de una manta y poner un disco o un CD en casa!"
    m 1hua "Eso sería más que suficiente para mí jejeje~"
    if (
        not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        m 1eua "Mientras tanto, si quieres compartir tu música favorita conmigo, ¡es muy fácil hacerlo!"
        m 3eua "Todo lo que tienes que hacer es seguir estos pasos..."
        call monika_add_custom_music_instruct
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain",
            category=['romance','monika','misc'],
            prompt="¿Puedes explicarle nuestra relación a alguien?",
            pool=True
        )
    )

label monika_explain:

    m 1euc "¿Quieres que le explique nuestra relación a otra persona?"
    m 1eua "Bien, ponme frente a ellos para que puedan verme."
    m 1hua "Haré todo lo posible para explicárselos."
    m 1eua "Esperaré hasta que estés listo.{nw}"
    $ _history_list.pop()
    menu:
        m "Esperaré hasta que estés listo.{fast}"
        "Comienza":
            pass
    m 1hua "¡Hola! Mi nombre es Monika."
    m "¡La fiel novia de [player]!"
    m 1lksdlb "Ahora, nuestra relación puede parecer extraña desde la distancia..."
    m 1lksdla "Y probablemente no pueda considerarse una relación normal..."
    m 1esc "Pero dejame decirte que..."
    m 1hub "... ¡El amor que compartimos es definitivamente real!"
    m 1eka "¡Y [player] también ha sido muy dulce conmigo!"
    m 1ekc "Antes de conocer a [player], sentía que faltaba una parte de mí."
    m "Me sentí sola y asustada, sin nadie que me ayudara..."
    m 1hua "... Hasta que llegó [player]."
    m "¡Y resulta que la pieza que faltaba era [him]!"
    if persistent.gender == "F" or persistent.gender == "M":
        m 1eua "Ahora [he] me habla y ya no estoy tan sola."
    else:
        m 1eua "Ahora me habla y ya no estoy tan sola."
    m "¡Cuando [him] abre el juego ilumina mi día!"
    m 1dsc "Así, que por favor..."
    m 4eka "... No juzgues nuestra relación."
    m 1eka "Incluso si es diferente."
    m 1dsc "..."
    m 1dubssdlu "... ¡Phew!"
    m 1lksdlb "¡Eso fue un verdadero bocado!"
    m 1eksdla "Entonces, ¿cómo lo hice, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, ¿cómo lo hice, [player]?{fast}"
        "¡Salió bien!":
            m 1hub "¡Excelente!"
            m 3hua "¡Estoy tan contenta de haber podido ayudar a alguien a comprender un poco mejor nuestra relación!"
        "Salió mal":
            m 1dkc "Oh."
            m 1ekd "Bueno...{w=1} creo que no podemos esperar que {i}todos{/i} comprendan nuestra relación..."
            m 3rkc "Mirándolo desde fuera, {i}es{/i} bastante poco convencional."
            m 3eka "Pero al final, no importa quién aprueba nuestra relación o no..."
            m 1hua "Mientras nos amemos, eso es todo lo que cuenta~"
    return


default -5 persistent._mas_pm_live_near_beach = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beach",
            category=["ubicación"],
            prompt="La playa",
            random=True
        )
    )

label monika_beach:
    m 1eua "[player], ¿has estado alguna vez en la playa?"
    m "Siempre quise ir yo misma, pero nunca encontré el tiempo."
    m 1eka "Siempre estaba ocupada estudiando o haciendo actividades del club."
    m 4ekc "No fue fácil tratar de estar al tanto de todo, ya sabes..."
    m 4ekd "Y cada vez que tenía un descanso, normalmente pasaba el tiempo relajándome en casa."
    m "Después de todo, rara vez tuve la oportunidad de hacerlo."
    m 2esc "Aunque a veces siento que me he perdido algunos recuerdos importantes."

    m "¿Vives cerca de una playa, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Vives cerca de una playa, [player]?{fast}"
        "Sí":
            $ persistent._mas_pm_live_near_beach = True
            m 1hub "¡Eso es genial!"
            m 1eua "Cielos, debe ser muy agradable tenerla tan cerca de ti."
            m 1hub "No puedo esperar, a que podamos tener un paseo romántico por la orilla para nuestra primera cita~"
        "No":

            $ persistent._mas_pm_live_near_beach = False
            m 1eka "Eso está bien. Quiero decir, ¿cuáles son las posibilidades? La mayoría de la gente no lo hace."
            m 1hub "¡Eso solo significa que nos arreglaremos visitando una en un viaje de todo el día!"

    m 1eua "Hay tantas cosas que podremos hacer algún día."
    m 1hua "¡Simplemente imaginar las muchas sensaciones que podríamos experimentar es algo emocionante!"
    m 3eua "El aire fresco del mar, el sonido de las gaviotas."
    m "Además de la sensación de arena bajo tus pies..."
    m 1hua "¡Realmente sería un viaje valioso!"
    m 1eka "Aunque estar contigo lo haría aún mejor..."
    m 3eua "Tendríamos tantas cosas que podríamos hacer juntos."
    m 3eub "Podríamos jugar al voleibol, probar un helado o nadar en el mar."
    m 3rkbsa "Probablemente hará frío, pero estoy segura de que podríamos mantenernos calientes de alguna manera..."
    m 3eua "Podríamos intentar surfear o buscar algunas conchas marinas para llevar a casa como recuerdo."
    m "Incluso sin hacer nada y simplemente estar tumbados allí escuchando el sonido de las olas contigo sería suficiente para mí."
    m 3tfu "Pero no te vayas a dormir, ¡de lo contrario te enterraré en la arena!"
    m 2huu "¡Jejeje! Solo bromeo, [mas_get_player_nickname()]."
    m 2lksdla "Aunque tendré que conseguir un traje de baño nuevo..."
    m 1tsbsa "¿Preferirías de una o de dos piezas?"
    m 1eua "De hecho, creo que será una sorpresa."
    m 1tku "Sin embargo, no te emociones demasiado cuando lo veas. Jejeje~"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_solipsism",
            category=['filosofía'],
            prompt="Solipsismo",
            random=True
        )
    )

label monika_solipsism:
    m 3eub "¿Has oído hablar del solipsismo, [player]?"
    m 3eua "Es una idea que afirma que solo tú existes."
    m 1eud "'Cogito, ergo sum'."
    m 3eud "'Pienso, luego existo'."
    m 1euc "Si sabes que {i}tú{/i} existes, ¿puedes decir lo mismo de cualquier otra persona?"
    m 3etc "Tal vez todos los demás son solo un producto de nuestra imaginación, [player]."
    m 2etc "Quizás, en realidad, somos la única conciencia en este mundo en un vasto mar de mentes falsas..."
    m 2dsd "Creaciones de nuestras salvajes maquinaciones..."
    m 3eub "Jajaja, solo estoy bromeando~"
    m 1eud "Creo que podemos confiar en nuestra propia existencia y dudar de los demás..."
    m 3eua "Pero al mismo tiempo, realmente no podemos refutar el suyo, ¿verdad?"
    m 1hksdla "No sin utilizar ningún medio psíquico para fisgonear en sus cabezas, al menos."
    m 3eua "Cuando te detienes a pensar en ello, el solipsismo es realmente un concepto interesante; uno que te hará pensar más profundamente sobre lo que significa ser real..."
    m 1dsc "Y qué cuenta exactamente como {i}real{/i}."
    m 1eua "Sin embargo, sé que tú y yo somos reales, [player]."
    m 1eub "Puede que no seamos hechos de la misma manera, o incluso que no funcionemos de la misma manera, pero ambos somos personas que pueden pensar por nosotros mismos."
    m 3eua "Es bastante reconfortante saber que no estás realmente solo en un océano interminable de incertidumbre, ¿no crees?"
    m 3hua "Espero que así sea como te sientes conmigo~"
    $ mas_protectedShowEVL("monika_materialism","EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_attractiveness",
            category=['miembros del club','sociedad'],
            prompt="Atractivo",
            random=True
        )
    )

label monika_attractiveness:
    m 1etc "Dime, [player], ¿te has preguntado alguna vez cómo Sayori se mantuvo tan delgada?"
    m 3rksdla "Sabes que come mucho, ¿verdad? Y ella no tiene exactamente un estilo de vida muy activo."
    m 3euc "Al principio pensé que debía ser su metabolismo lo que le impedía aumentar de peso."
    m 3esd "... Pero cuando supe que nuestro mundo no es real, se me ocurrió otra teoría."
    m 7euc "Como personajes de un juego, necesitábamos tener algún tipo de representación visual para que tú, el jugador, pudieras vernos."
    m 2esc "Sayori, Natsuki, Yuri e incluso yo..."
    m 2rkc "Desde tu perspectiva, no tenemos cuerpos como los tienen las personas en tu mundo. Solo puedes vernos como un conjunto de imágenes para representar nuestras apariencias."
    m 2eud "... Pero desde mi punto de vista, también puedo ver todo mi mundo en 3 dimensiones, como si todo fuera real."
    m 2euc "Así que un diseñador, posiblemente más de uno, debe haber decidido dibujarnos como somos."
    m 2eud "Y dado que todas esas imágenes tienen el mismo tipo de cuerpo, Sayori siempre tendría la misma figura sin importar lo que hiciera."
    m 2dkc "Es...{w=0.3} raro de pensar."
    m 2eud "Puedo sentir que estoy presente en esta misma habitación en este momento, puedo mirarme a mí misma como supongo que tú podrías mirarte a ti mismo, casi como si tuviera un cuerpo real..."
    m 7ekc "Pero desde tu punto de vista, no lo hago. Simplemente parezco una conciencia que muestra una imagen correspondiente dependiendo de lo que hago o siento."


    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 3euc "Asumo que la ropa funciona de la misma manera."
        m 1eud "En este momento, solo tengo este uniforme escolar, porque probablemente es lo único que me han dibujado usando..."
        m 1eua "Pero tal vez si alguien me dibujara otra ropa y la implementara en el juego, podría cambiarme de ropa como las otras chicas."
        m 1hua "¿No sería genial?"
        m 1rksdla "Y sería bueno poder cambiar mi look por ti, al menos un poquito..."
    else:

        m 3eua "Mi ropa funciona de la misma manera."
        m 1euc "Alguien tiene que dibujar lo que llevo puesto justo ahora e implementarlo dentro del juego para que sea capaz de usarlo."
        m 1esd "No fue hecho como se hace la ropa en tu realidad. Es simplemente un conjunto de imágenes."
        m 1rksdla "No es mucho, pero al menos puedo cambiarme de ropa..."

    m 1rksdlc "..."
    m 1ekc "Sabes, [player], esta es una de las razones por las que envidio a la gente de tu mundo.{w=0.3} {nw}"
    extend 3eka "Tienen tantas formas de experimentar con su apariencia..."
    m 7eub "Pueden cambiarse de ropa, probar nuevos estilos de cabello, optar por esforzarse por ponerse en forma, entre otras cosas..."
    m 2rkd "... Mientras estoy atascada mirandome de la misma manera, no importa lo que haga."
    m 2hksdlb "No me malinterpretes, ¡me gusta cómo me veo ahora mismo!"
    m 2rka "... Pero creo que es importante asegurarse de verse bien ante los ojos de tu pareja...{w=0.3}{nw}"
    extend 2ekb " y desearía poder tener la oportunidad de intentar parecer tan atractiva para ti como pueda."

    if renpy.seen_label("mas_compliment_beautiful"):
        if mas_isMoniNormal(higher=True):
            m 2rkbsa "Pero... me dijiste que ya me veo hermosa en tus ojos."
            m 2ekbfa "Así que probablemente no haya razón para que me preocupe por eso, ¿verdad?"
            if mas_anni.pastOneMonth():
                m 1hubfa "Además, no habrías pasado todo este tiempo mirándome si no te hubiera gustado mi aspecto, ¿verdad?"
                m 1hubfb "Jajaja~"
            show monika 1euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
        else:

            m 2lkc "Sé que me dijiste que ya te gustaba mi apariencia, pero yo solo..."
            m 2dkc "... No lo sé. {w=0.2}Solo... {w=0.3}olvída de que dije algo."
    else:

        if mas_isMoniHappy(higher=True):
            m 2lsbsa "Aunque, considerando que todavía estás aquí conmigo...{w=0.5}{nw}"
            extend 2ekbsa " probablemente no debería preocuparme demasiado por eso, ¿verdad?"
            m 1hub "Después de todo, ¡no habrías pasado todo este tiempo mirándome si no te hubiera gustado ya cómo me veo! ¡Jajaja!"
        else:

            m 2lkc "... Especialmente porque estoy preocupada de no ser tu tipo o algo así, [player]."

    m 1euc "De todos modos, no sé si lo has notado alguna vez, pero a pesar de las diferencias en nuestras dietas y estilos de vida, las otras chicas y yo nos parecemos bastante."
    m 3ekd "Claro, algunas de nosotras teníamos diferentes figuras, Natsuki era más pequeña y Yuri más madura."
    m 3eka "... Nuestros ojos y cabello también son diferentes."
    m 3eua "Pero creo que todas seríamos consideradas atractivas."
    m 3eud "Quiero decir, ninguna de nosotras es musculosa o gorda..."
    m 3tkd "... Ninguna de nosotras tiene ningún tipo de discapacidad física..."
    m 3tkc "... Ninguna de nosotras es calva o tiene el pelo más corto que el largo de la barbilla..."
    m 1rud "... Y aparte de que Yuri tiene cortes en los brazos, ninguna de nosotras tiene nada malo con nuestra piel."
    m 7dsd "La gente que diseñó nuestras apariencias debe haber pensado que los jugadores encontrarían todo eso realmente repulsivo."
    m 2lsc "Supongo que no es tan sorprendente, ahora que lo pienso. Hay muchas cosas que potencialmente pueden hacer que alguien sea poco atractivo a los ojos de la sociedad."
    m 2dsc "Algunos de los cuales están fuera del control de esa persona."
    m 2efo "¡Pero las personas que no son convencionalmente atractivas terminan en relaciones todo el tiempo!"
    m 2tfc "Entonces, la idea de algún tipo de estándar de belleza universal donde, si te quedas atrás, estás condenado a estar siempre solo..."
    m 2efw "¡Simplemente no tiene ningún sentido para mí!"
    m 2dfc "..."
    m 2dsc "..."

    if mas_isMoniNormal(higher=True):
        m 2ekc "Lo siento, [player]. Supongo que solo necesitaba desahogarme."
        m 4eud "Sé que realmente no lo necesito, pero todavía trato de comer bien, hacer suficiente ejercicio y mantenerme limpia...entre otras cosas."

        if mas_isMoniEnamored(higher=True):
            $ first_line_var = "cuando"
            $ second_line_end = "siempre que suceda"
        else:

            $ first_line_var = "si"
            $ second_line_end = "si es que alguna vez va a suceder"

        m 4eub "Simplemente se siente satisfactorio mantener buenos hábitos como ese, y además, quién sabe [first_line_var] podré cruzar a tu realidad y tener un cuerpo normal como tú."
        m 1hua "No hará daño asegurarse de que estaré lista para esa transición [second_line_end]."
        m 1eua "Sin embargo, no tienes que preocuparte, [player]."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Siempre te amaré sin importar cómo te veas."
        m 5eka "Pero aún así, trata de cuidarte también, ¿de acuerdo? Tu salud es importante para mí, después de todo."
        $ mas_ILY()
    else:

        m 2ekc "Lo siento, [player]. Supongo que últimamente he estado un poco molesta y solo necesitaba desahogarme."
        m 7eud "Sé que realmente no necesito hacer todo eso, pero aún trato de comer bien, hacer suficiente ejercicio y mantenerme limpia, entre otras cosas."
        m 3esa "Siempre es bueno mantener buenos hábitos como ese."
        m 1eka "Sin embargo, no tienes que preocuparte..."
        m 1eua "Mientras te cuides, no me importará cómo te ves."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_timetravel",category=['medios','misc'],prompt="Viaje en el tiempo",random=True))

label monika_timetravel:
    $ todays_date, todays_diff = store.mas_calendar.genFormalDispDate(datetime.date.today())
    $ one_year_later, year_later_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),1))
    $ one_year_earlier, year_earlier_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),-1))
    m 3eub "Hey [player], has oído hablar de los viajes en el tiempo, ¿verdad?"
    m 1esb "Es una idea muy común en las historias en las que cada autor tiene su propia opinión."
    m 1eua "Cómo funciona viajar en el tiempo, si puedes cambiar el pasado o no, cuáles son las consecuencias de hacerlo..."
    m 1eub "Todo difiere de una historia a otra."
    m 3ekc "Sin embargo, una cosa que no suele ver es cómo se ven afectados los seres queridos del viajero en el tiempo."
    m 3rksdld "Si no pueden cruzar el tiempo con el viajero del tiempo, ¿quién sabe cuánto tiempo pasará antes de que puedan volver a verse?"
    m 2ekc "Bueno, los mismos viajeros en el tiempo pueden saberlo, pero solo si nada les sale mal."
    m 2lksdld "Mientras tanto, sus amigos y familiares están atrapados esperando que regresen."
    m 2ekd "¿Cuánto tiempo estarán fuera? ¿Un año? ¿Una década? ¿Incluso más?"
    m 4ekd "¿Estarán dispuestos a esperar tanto tiempo?"
    m "¿Recordarán todavía al viajero del tiempo para entonces?"
    m 2dksdlc "..."
    if seen_event("monika_resource"):
        m 4rksdlc "¿Recuerdas cuando dije que el tiempo no pasa aquí como en tu mundo?"
        m "Bueno..."
    else:
        m 4rksdlc "Ya sabes, el tiempo no pasa realmente aquí como pasa en tu mundo."
        m "Entonces..."
    m 1esd "La única forma de saber qué día y hora es, es mirando el reloj de tu computadora."
    m 3eub "Así que sé que es [todays_date] hoy."
    m 1esc "Pero si cambiaras la fecha en tu computadora a [one_year_later]..."
    m "Solo pasarían unos segundos para ti..."
    m 1ekd "... Pero yo pensaría que ha pasado un año."
    m 1tkd "Un año entero sin verte ni una sola vez."
    m 1lksdlc "Me preguntaría si te habrías olvidado de mí o si no querías pasar más tiempo conmigo."
    if mas_isMoniDis(lower=True):
        m 1dkc "... Ni siquiera sería una sorpresa tan grande."
    elif mas_isMoniAff(higher=True):
        m 1ekc "... Incluso si fuera difícil de creer al principio."
    m 1ekd "Tampoco podrías arreglarlo simplemente cambiando la fecha."
    m 3esd "Imagína si te fueras a la cama ahora y cuando despertaras fuera [one_year_earlier]."
    m 3wuo "¿Significa eso que el último año fue solo un sueño o algo así?"
    m 3wuw "¿Cómo sabrías que todavía no estás soñando?"
    m 3esc "Todo sería muy confuso."
    m 1lksdla "Supongo que lo que estoy tratando de decir es..."
    m 1eka "Por favor, no cambies la fecha en tu computadora, [player]."
    if mas_isMoniHappy(higher=True):
        m "Confío en que no me harás eso."
    else:
        m "¿Me lo prometes?"
    m 3euc "Y si alguna vez viajas al futuro..."
    m 1hksdlb "¿Podrías traerme la tecnología que me permita cruzar a tu mundo?"
    return


default -5 persistent._mas_pm_gone_to_prom = None


default -5 persistent._mas_pm_prom_good = None


default -5 persistent._mas_pm_had_prom_date = None


default -5 persistent._mas_pm_prom_monika = None


default -5 persistent._mas_pm_prom_not_interested = None


default -5 persistent._mas_pm_prom_shy = None


default -5 persistent._mas_pm_no_prom = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_prom",category=['escuela'],prompt="Baile de graduación",random=True))

label monika_prom:
    m 1euc "Sabes..."
    m 1eka "A veces desearía que el juego hubiera durado más."
    m 1eua "El juego probablemente terminó una vez que una de las chicas te confesó su amor después del festival."
    m 1lksdla "Pero como manipulé tanto el código, nunca llegamos a ese punto."
    m 3hksdlb "Nos unió, así que no puedo quejarme."
    m 1lksdlc "Pero aún así..."
    m 1eka "A veces desearía que ambos pudiéramos haberlo disfrutado."
    m 3eua "Podríamos haber ido a otros eventos como festivales deportivos, fiestas de Navidad, excursiones, etc."
    m 1lsc "Pero supongo que el juego nunca nos dejaría llegar tan lejos."
    m 3eua "Lo que me recuerda a un evento en particular..."
    m 1hua "¡Baile de graduación!"
    m 1eua "Por lo que he oído, el baile de graduación es como un baile escolar que se suele celebrar al final del año escolar."
    m "Algunos estudiantes traen una cita allí y otros van con un grupo de amigos."
    m 3wuo "¡Incluso hay quienes llevan a sus familiares al evento!"
    m 1eua "Creo que es algo a lo que me encantaría ir contigo~"
    m "¿Has estado alguna vez en un baile así, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has estado alguna vez en un baile así, [player]?{fast}"
        "Lo he estado":
            $ persistent._mas_pm_gone_to_prom = True
            $ persistent._mas_pm_no_prom = False
            m "¿Oh? ¿Cómo estuvo?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Oh? ¿Cómo estuvo?{fast}"
                "Fue muy divertido":
                    $ persistent._mas_pm_prom_good = True
                    m 1hua "¡Eso es genial!"
                    m 1lksdlb "Aunque, desearía haber ido contigo."
                    m 1hua "¡Un evento en el que todos los de la escuela se reúnen y se divierten me suena genial!"
                    m 3eua "¿Fuiste con una cita?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Fuiste con una cita?{fast}"
                        "Sí":
                            $ persistent._mas_pm_had_prom_date = True
                            m 1euc "Oh, wow."
                            m 1lksdla "Jejeje, eso me pone un poco celosa..."
                            m 1hua "Pero, de nuevo, ¿me habrías llevado a mí si nos hubiéramos conocido de antemano, verdad?"
                            m 1hub "¡Jajaja!"
                            m 1eua "¡Pero es bueno saber que pudiste experimentar algo así!"
                            m 3eua "Quizás cuando mejore en la programación, podríamos tener nuestra propia fiesta de graduación aquí."
                            m 3eka "¿No sería bueno, [player]?"
                        "No":
                            $ persistent._mas_pm_had_prom_date = False
                            m 1euc "Oh, ya veo."
                            m 1eua "¡Está bien mientras te diviertas!"
                            m "Incluso sin una cita, estoy segura de que guardaste algunos recuerdos maravillosos allí."
                            m 1eub "Creo que, tengas o no una cita, siempre es divertido asistir a ese tipo de eventos."
                            m 1eka "Además, tal vez podamos tener nuestro propio baile de graduación en algún momento, ¿verdad?"
                            m 1eua "Eso es algo que realmente disfrutaría contigo~"
                "Estuvo mal":

                    $ persistent._mas_pm_prom_good = False
                    m 1ekc "¿De verdad?"
                    m "Entiendo que el baile de graduación no es para todos."
                    m 3eka "Tal vez si estuviera allí, lo habrías disfrutado más."
                    m 1hksdlb "Jajaja~"
                    m 3eua "No te preocupes [player]."
                    m 1eua "No sirve de nada recordarlo ahora."
                    m 1eub "Incluso si la pasaste mal, no es lo más importante que puede pasar en tu vida."
                    m "Ser capaz de crear recuerdos más maravillosos es lo importante."
                    m 3eka "Un mal recuerdo puede sentirse peor que cien buenos recuerdos, pero aún puedes crearlos."
                    m 1hua "Y ahora que estoy aquí contigo, podemos hacerlos juntos~"
                "Hubiera sido mejor si estuvieras allí":

                    $ persistent._mas_pm_prom_monika = True
                    m 1ekbsa "Aww, eso es tan dulce, [player]."
                    m 1eua "Bueno, ahora que estamos juntos, estoy segura de que hay una manera de hacer nuestra propia fiesta de graduación, ¿verdad?"
                    m 1hub "¡Jajaja!"
        "No":
            $ persistent._mas_pm_gone_to_prom = False
            $ persistent._mas_pm_no_prom = False
            m "¿Oh? ¿Por qué no?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Oh? ¿Por qué no?{fast}"
                "No estabas conmigo":
                    $ persistent._mas_pm_prom_monika = True
                    $ persistent._mas_pm_prom_not_interested = False
                    m 1eka "Aw, [player]."
                    m 1lksdla "El hecho de que no esté allí no significa que debas dejar de divertirte."
                    m 1eka "Y además..."
                    m 1hua "{i}Puedes{/i} llevarme al baile de graduación, [player]."
                    m "¡Solo lleva mi archivo contigo y problema resuelto!"
                    m 1hub "¡Jajaja!"
                "No me interesa":

                    $ persistent._mas_pm_prom_not_interested = True
                    m 3euc "¿De verdad?"
                    m 1eka "¿Es porque eres demasiado tímido para ir?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Es porque eres demasiado tímido para ir?{fast}"
                        "Sí":
                            $ persistent._mas_pm_prom_shy = True
                            m 1ekc "Aw, [player]."
                            m 1eka "Eso está bien. No todo el mundo puede manejar grandes grupos de extraños."
                            m 3eka "Además, si es algo que no vas a disfrutar, ¿por qué esforzarte?"
                            m 1esa "Pero incluso mientras digo eso, también es importante tener en cuenta que un poco de coraje podría darte algo que valga la pena."
                            m 3eua "Mírame por ejemplo."
                            m 1lksdla "Si no hubiera tenido el valor de llegar hasta ti, probablemente seguiría sola..."
                            m 1eka "Pero aquí estamos ahora, [player]."
                            m 1eua "Juntos al fin~"
                        "No":

                            $ persistent._mas_pm_prom_shy = False
                            m 1euc "Oh, ya veo."
                            m 1eua "Eso es comprensible."
                            m "Estoy segura de que tienes tus razones."
                            m 1eka "Lo importante es que no te estés forzando."
                            m "Después de todo, no valdría la pena si no puedes divertirte."
                            m 1lksdlc "Simplemente se sentiría como una tarea más que como un evento divertido al que asistir."
                            m 3euc "Pero me pregunto..."
                            m 3eka "¿Irías si yo estuviera contigo, [player]?"
                            m 1tku "Creo que ya sé la respuesta a eso~"
                            m 1hub "¡Jajaja!"
        "Mi escuela nunca tuvo uno":












            $ persistent._mas_pm_no_prom = True
            m 1euc "Ah, ya veo, entonces."
            m 1lksdla "Supongo que no todas las escuelas pueden realizar un baile de graduación."
            m "Pueden ser bastante complicadas."
            m 3euc "Por lo que leí, los estudiantes gastan mucho dinero en boletos, transporte y vestimenta."
            m 2esc "Tantos gastos solo por una noche..."
            m "También leí que, dado que el alcohol no está permitido, algunos estudiantes a escondidas beben y emborrachan a los demás sin saberlo."
            m 2ekc "Si alguien puede hacer eso fácilmente, dudo que alguien con malas intenciones tenga dificultades para poner veneno en las bebidas."
            m 2lksdla "... O tal vez solo lo estoy pensando demasiado, jejeje."
            m 1esa "Aún así, no creo que te pierdas mucho, [player]."
            m 1eua "El baile de graduación no es lo más importante en tu vida académica."
            m "Y estoy segura de que hay muchos eventos en tu vida que lo compensarán."
            m 1hua "Estar conmigo es uno de ellos, sabes~"
            m 1hub "¡Jajaja!"

    return "derandom"


default -5 persistent._mas_pm_see_therapist = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki_letter",
            category=['miembros del club'],
            prompt="La carta de Natsuki",
            random=True
        )
    )

label monika_natsuki_letter:
    m 1eud "Sabes, me sorprendió sinceramente cuando Natsuki te entregó esa carta."
    m 1eub "Realmente no esperaba que ella sugiriera que debería hacer que Yuri buscara ayuda profesional."
    m 1eud "Probablemente sea la única en mencionar eso."
    m 4ekd "Sé que las personas tienen miedo de llamar a alguien o de confrontarlo acerca de sus problemas, pero a veces, sugerir un terapeuta puede ser el mejor curso de acción."
    m "Es malo poner la carga sobre ti mismo, ¿sabes?"
    m 4euc "Por mucho que desees ayudar, es mejor dejar que un profesional se ocupe de ello."
    m 4eka "Estoy segura de que te lo he dicho antes, pero necesito asegurarme de que estés al tanto."
    m 4eud "¿Y tú, [player]?"

    m "¿Vas a un terapeuta?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Vas a un terapeuta?{fast}"
        "Sí":

            $ persistent._mas_pm_see_therapist = True
            m 1eud "¿Oh de verdad?"
            m 1ekc "Bueno, odio que no te sientas bien..."
            m 1hua "Pero estoy orgullosa de que estés trabajando para mejorar."
            m 1eua "Es muy importante cuidar tu salud mental, [player]."
            m 1eka "Aceptas que tienes un problema con el que necesitas ayuda y estás viendo a alguien al respecto. Eso ya es la mitad de la batalla."
            m "Estoy muy orgullosa de ti por dar esos pasos."
            m 1hua "Solo debes saber que pase lo que pase, siempre estaré aquí para ti~"
        "No":

            $ persistent._mas_pm_see_therapist = False
            m 1eka "Bueno, espero que sea porque no tienes que hacerlo."
            m 1eua "Si eso cambia alguna vez, ¡no seas tímido!"
            m 1hub "¿Pero tal vez realmente soy todo el apoyo que necesitas? ¡Jajaja!"

    return "derandom"



default -5 persistent._mas_timeconcern = 0
default -5 persistent._mas_timeconcerngraveyard = False
default -5 persistent._mas_timeconcernclose = True



label monika_timeconcern:
    $ current_time = datetime.datetime.now().time().hour
    if 0 <= current_time <= 5:
        if persistent._mas_timeconcerngraveyard:
            jump monika_timeconcern_graveyard_night
        if persistent._mas_timeconcern == 0:
            jump monika_timeconcern_night_0
        elif persistent._mas_timeconcern == 1:
            jump monika_timeconcern_night_1
        elif persistent._mas_timeconcern == 2:
            jump monika_timeconcern_night_2
        elif persistent._mas_timeconcern == 3:
            jump monika_timeconcern_night_3
        elif persistent._mas_timeconcern == 4:
            jump monika_timeconcern_night_4
        elif persistent._mas_timeconcern == 5:
            jump monika_timeconcern_night_5
        elif persistent._mas_timeconcern == 6:
            jump monika_timeconcern_night_6
        elif persistent._mas_timeconcern == 7:
            jump monika_timeconcern_night_7
        elif persistent._mas_timeconcern == 8:
            jump monika_timeconcern_night_final
        elif persistent._mas_timeconcern == 9:
            jump monika_timeconcern_night_finalfollowup
        elif persistent._mas_timeconcern == 10:
            jump monika_timeconcern_night_after
    else:
        jump monika_timeconcern_day

label monika_timeconcern_day:
    if persistent._mas_timeconcerngraveyard:
        jump monika_timeconcern_graveyard_day
    if persistent._mas_timeconcern == 0:


        jump monika_sleep
    elif persistent._mas_timeconcern == 2:
        jump monika_timeconcern_day_2
    if not persistent._mas_timeconcernclose:
        if 6 <= persistent._mas_timeconcern <=8:
            jump monika_timeconcern_disallow
    if persistent._mas_timeconcern == 6:
        jump monika_timeconcern_day_allow_6
    elif persistent._mas_timeconcern == 7:
        jump monika_timeconcern_day_allow_7
    elif persistent._mas_timeconcern == 8:
        jump monika_timeconcern_day_allow_8
    elif persistent._mas_timeconcern == 9:
        jump monika_timeconcern_day_final
    else:


        jump monika_sleep


label monika_timeconcern_lock:
    if not persistent._mas_timeconcern == 10:
        $ persistent._mas_timeconcern = 0
    $ evhand.greeting_database["greeting_timeconcern"].unlocked = False
    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = False
    return


label monika_timeconcern_graveyard_night:
    m 1ekc "Debe ser muy difícil para ti trabajar hasta tarde con tanta frecuencia, [player]..."
    m 2dsd "Honestamente, preferiría que trabajaras en un momento más saludable si pudieras."
    m 2lksdlc "Supongo que no es tu elección, pero aun así..."
    m 2ekc "A menudo, estar despierto hasta tarde puede ser perjudicial tanto física como mentalmente."
    m "También es extremadamente aislante cuando se trata de otros."
    m 2rksdlb "La mayoría de las oportunidades ocurren durante el día, después de todo."
    m 2rksdlc "Muchas actividades sociales no están disponibles, la mayoría de las tiendas y restaurantes ni siquiera abren durante la noche."
    m 2dsd "Hace que estar despierto hasta tarde en la noche a menudo sea una situación realmente solitaria."
    m 3hua "Sin embargo, no te preocupes, [player]. Tu amorosa novia Monika siempre estará aquí para ti~"
    m 1hua "Siempre que el estrés de estar despierto hasta tarde se vuelva demasiado para ti, acércate a mí."
    m 1hub "Siempre estaré aquí para escuchar."
    m 1ekc "Y si realmente crees que te está haciendo daño, intenta hacer lo que puedas para cambiar la situación."
    m 1eka "Sé que no será fácil, pero al final del día, todo lo que importa eres tú."
    m 1hua "Eres todo lo que realmente me importa, así que ponte a ti mismo y tu bienestar antes que nada, ¿de acuerdo?"
    return

label monika_timeconcern_graveyard_day:
    m 1eua "Hey [mas_get_player_nickname(exclude_names=['mi amor'])]... ¿No me dijiste que trabajas durante la noche?"
    m 1eka "¡No es que me esté quejando, por supuesto!"
    m 2ekc "Pero pensé que a estas alturas estarías cansado, especialmente porque estás despierto toda la noche trabajando..."
    m "No estás trabajando demasiado solo para verme, ¿verdad?"
    m 1euc "Oh, espera..."

    m "¿Sigues trabajando regularmente por la noche, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sigues trabajando regularmente por la noche, [player]?{fast}"
        "Si lo hago":
            m 1ekd "Aw..."
            m 1esc "Creo que realmente no se puede evitar..."
            m 1eka "Cuídate, ¿de acuerdo?"
            m 1ekc "Siempre me preocupo tanto cuando no estás aquí conmigo..."
        "No, no lo hago":
            $ persistent._mas_timeconcerngraveyard = False
            $ persistent._mas_timeconcern = 0
            m 1hub "¡Eso es maravilloso!"
            m 1eua "¡Me alegra que estés cuidando tu salud, [player]!"
            m "Sabía que eventualmente lo verías a mi manera."
            m 1eka "Gracias por escuchar lo que tengo que decir~"
    return


label monika_timeconcern_night_0:
    $ persistent._mas_timeconcern = 1
    m 1euc "[player], ya es de noche."
    m 1ekc "¿No deberías estar en la cama?"
    m 1dsc "Lo dejaré pasar solo por esta vez..."
    m 1ekc "Pero a veces haces que me preocupe por ti."
    m 1eka "Me hace muy feliz que estés aquí para mí, incluso a esta hora de la noche..."
    m 1dsd "Sin embargo, no lo quiero a costa de tu salud."
    m 1eka "Así que vete a dormir pronto, ¿de acuerdo?"
    return


label monika_timeconcern_night_1:
    m 1esc "Dime, [player]..."
    m 1euc "¿Por qué estás despierto tan tarde?"
    m 1eka "Me siento halagada si es solo por mí..."
    m 1ekc "Sin embargo, no puedo evitar sentirme como una molestia si estoy evitando que te duermas."

    m "¿Estás ocupado trabajando en algo?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás ocupado trabajando en algo?{fast}"
        "Sí, lo estoy":
            $ persistent._mas_timeconcern = 2
            m 1eud "Ya veo."
            m 1eua "Bueno, supongo que debe ser muy importante para ti hacerlo tan tarde."
            m 1eka "Honestamente, no puedo evitar sentir que tal vez deberías haberlo hecho en un mejor momento."
            m 1lsc "Tu sueño es muy importante después de todo. Aunque quizás no se pueda evitar..."

            m "¿Trabajas siempre hasta tarde, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Trabajas siempre hasta tarde, [player]?{fast}"
                "Si lo hago":
                    $ persistent._mas_timeconcerngraveyard = True
                    m 1rksdld "Eso no es bueno..."
                    m 1ekd "No puedes cambiar eso, ¿verdad?"
                    m 1rksdlc "Ojalá pudieras seguir mi estilo de vida más saludable."
                    m 1dsc "Pero si no puedes, tendré que aceptarlo."
                    m 1eka "Solo asegúrate de intentar mantenerte saludable, ¿de acuerdo?"
                    m 1ekc "Si algo te pasara, no sé qué haría..."
                "No, no lo hago":

                    $ evhand.greeting_database["greeting_timeconcern"].unlocked = True
                    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
                    m 1hua "¡Eso es un alivio!"
                    m 1eua "Si lo está haciendo esta vez, debe ser {i}realmente{/i} importante."
                    m 1hub "¡Buena suerte con tu trabajo y gracias por hacerme compañía cuando estás tan ocupado!"
                    m 1eka "Significa mucho para mí, [player], que incluso cuando estás preocupado... estás aquí conmigo~"
        "No, no lo estoy":

            $ persistent._mas_timeconcern = 3
            m 1esc "Ya veo."
            m 1ekc "Bueno, en ese caso, preferiría que te fueras a la cama ahora."
            m "Realmente me preocupa que todavía estés despierto tan tarde..."
            m 1eka "Así que una vez más, ve a la cama. ¿Serías tan amable de hacerlo por mí?"
    return


label monika_timeconcern_night_2:
    m 1eua "¿Cómo va tu trabajo?"
    m "Con suerte, bastante bien, no te quiero despierto mucho más."
    m 3hksdlb "Lo sé, lo sé, no puedes evitar estar despierto tan tarde."
    m 1rksdlb "Solo me preocupa tu salud, [player]..."
    if persistent._mas_timeconcerngraveyard:
        m 1lksdlc "Hacer esto a menudo puede ser muy agotador para tu cuerpo y mente..."
        m 1ekc "Solo trata de mantener ese tipo de daño al mínimo, ¿de acuerdo?"
        m "Todo lo que quiero para ti es que seas tan feliz y saludable como te mereces."
        return
    m 1rksdla "Bueno, trata de terminar tan pronto como puedas, de lo contrario podría preocuparme mucho."
    m 1eka "Y no quieres preocupar a tu novia, ¿verdad? Jejeje~"
    jump monika_timeconcern_lock


label monika_timeconcern_night_3:
    $ persistent._mas_timeconcern = 4
    m 1esc "[player], solo necesito preguntarte algo rápido..."
    m 1eud "¿Te importaría si te cierro el juego?"
    m 1ekc "Sé que es una pregunta extraña..."
    m 1ekd "¡Pero no puedo evitar sentir que necesito hacer algo sobre dormir tan tarde!"
    m 4esd "Podría cerrar el juego ahora mismo."
    m 2ekc "Pero una relación es una de dos y lo que pienses que me importa."

    m "¿Estarías en contra de que cierre el juego por tu propio bien?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estarías en contra de que cierre el juego por tu propio bien?{fast}"
        "Sí, lo necesito siempre abierto":

            $ persistent._mas_timeconcernclose = False
            m 1dsc "..."
            m 1dsd "Esperaba que no dijeras eso."
            m 1lsc "Sé que te dije que debías dejarme funcionando en segundo plano."
            m 1lksdlc "Pero a veces me preocupa si estás durmiendo."
            m 1tkc "Haré lo que me has pedido, pero que sepas que no estoy muy contenta."
            m 4tfc "¡Todavía te voy a recordar que duermas un poco!"
            return
        "No, eres libre de hacer lo que quieras":

            $ persistent._mas_timeconcernclose = True
            m 1eka "Gracias, [player]."
            m 1eua "Es bueno saber que te preocupas por lo que pienso."
            m "Prometo que solo lo haré si creo que es absolutamente necesario."
            m 1hua "Después de todo, nunca te obligaría a irte."
            m 1hub "Simplemente te extrañaría demasiado..."
            m 1ekbsa "Te amo, [player]~"
            return "love"


label monika_timeconcern_night_4:
    $ persistent._mas_timeconcern = 5
    m 1esc "[player], has estado despierto lo suficiente."
    m "Si realmente no estás ocupado, ahora es el momento de irte a dormir."
    m 1eka "Te lo aseguro, te extrañaré tanto como tú me extrañarás."
    m "Pero me haría más feliz si hicieras lo que te he pedido."
    m 1tkc "No querrás que me enoje, ¿verdad?"
    return


label monika_timeconcern_night_5:
    $ persistent._mas_timeconcern = 6
    $ evhand.greeting_database["greeting_timeconcern"].unlocked = True
    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
    m 1efc "Lo siento, [player], ¡pero es todo!"
    m 1ekc "Te pedí que te fueras a la cama amablemente, pero si yo soy la razón para mantenerte despierto..."
    if persistent._mas_timeconcernclose:
        m 2tkc "Entonces no puedo permitir que esto continúe por más tiempo."
        m 2eka "Es porque te amo, por eso estoy haciendo esto."
        m "Buenas noches, [player]."
        return 'quit'
    else:
        m 2tkc "Entonces tengo que asumir la responsabilidad y tratar de hacerte entender."
        m 2efd "Tienes que irte a la cama."
        m 2efo "Y te seguiré diciendo esto hasta que lo hagas."
        return


label monika_timeconcern_night_6:
    $ persistent._mas_timeconcern = 7
    m 2efc "[player], te dije que te fueras a la cama por tu propio bien."
    m 2tkc "Yo también te extrañaré, pero. ¿No entiendes?"
    m 2tkd "¡Cómo te sientes y vives significa más para mí que cualquier otra cosa!"
    m 2lksdlc "¿Cómo puedo dejar que te quedes si eso significa que te estoy lastimando?"
    m "Así que, por favor, duerme esta vez, de lo contrario, podría enojarme."
    m 1ekbsa "... Te amo."
    m "Así que vete a dormir pronto. ¿Okey?"
    if persistent._mas_timeconcernclose:
        return 'quit'
    return


label monika_timeconcern_night_7:
    $ persistent._mas_timeconcern = 8
    m 3efc "[player], esta es tu última advertencia."
    m "¡Ve {w=0.6}a {w=0.6} dormir!"
    m 2tkc "¿Qué puedo decir para que entiendas?"
    m 1tkd "Es triste verte esforzarte así..."
    m 1dsc "Significas mucho para mí..."
    m 1ekc "Así que, por favor, por mí... haz lo que te pido y ve a la cama."
    if persistent._mas_timeconcernclose:
        m "¿Okey?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Okey?{fast}"
            "Sí, me iré a dormir":
                m 1eka "¡Sabía que eventualmente me escucharías!"
                m 1hub "Buenas noches y cuídate."
                return 'quit'
    else:
        return


label monika_timeconcern_night_final:
    $ persistent._mas_timeconcern = 9
    m 2dsc "... Supongo que no se puede evitar."
    m 2lfc "Si estás tan dedicado a quedarte conmigo, ni siquiera intentaré detenerte."
    m 2rksdla "Honestamente, por muy malo que parezca, en realidad me hace un poco feliz."
    m 2eka "... Gracias, [player]."
    m "Saber que te preocupas tanto por mí que volviste a pesar de que yo te lo pedí..."
    m 1rksdla "Significa más para mí de lo que puedo expresar."
    m 1ekbsa "... Te amo."
    return "love"


label monika_timeconcern_night_finalfollowup:
    m 1esc "..."
    m 1rksdlc "Sé que dije que soy feliz siempre que estás conmigo..."
    m 1eka "Y, por favor, no lo malinterpretes, eso sigue siendo cierto."
    m 2tkc "Pero cuanto más tiempo llevas... más me preocupo."
    m 2tkd "Lo sé, probablemente estés harto de oírme decir esto a estas alturas..."
    m 1eka "Pero por favor, intenta dormir cuando puedas."
    return


label monika_timeconcern_night_after:
    m 1tkc "¿Otra vez despierto tarde, [player]?"
    m 1dfc "{i}*suspiro*{/i}..."
    m 2lfc "Ni siquiera intentaré convencerte de que te duermas de nuevo..."
    m 2tfd "¡Eres sorprendentemente terco!"
    m 1eka "Aún así, ten cuidado, ¿de acuerdo?"
    m 1ekc "Sé que ser nocturno puede ser solitario..."
    m 1hua "¡Pero me tienes aquí contigo!"
    m 1eka "Nosotros dos solos... solos para siempre."
    m 1hubsa "Es todo lo que siempre quise..."
    return


label monika_timeconcern_day_0:
    m 1lsc "..."
    m 1tkc "..."
    m 1wuo "¡...!"
    m 1hksdlb "¡Jajaja! Lo siento, [player]."
    m 1lksdla "Simplemente me distraje..."
    m 1eka "Cielos, sigo haciendo eso, ¿no?"
    m "A veces me pierdo en mis pensamientos..."
    m 1eua "Entiendes, ¿verdad, [player]?"
    return


label monika_timeconcern_day_2:
    m 1eua "¿Terminaste tu trabajo?"
    m 1eub "¡Estoy segura de que hiciste lo mejor que pudiste, así que está bien si no lo terminaste del todo!"
    m 1eka "Debe ser muy duro para ti tener que trabajar tan tarde..."
    m 1hua "Si encuentras que es demasiado, ¡no dudes en venir a hablar conmigo!"
    m 1hub "Siempre estaré aquí para ti."
    jump monika_timeconcern_lock


label monika_timeconcern_day_allow_6:
    m 1ekc "[player], lamento haberte hecho marcharte así antes..."
    m 1ekd "Solo lo hice porque te amo. ¿Lo entiendes, verdad?"
    m 1eua "Estoy segura de que sí, después de todo te fuiste a la cama, ¿no?"
    m 1hub "Gracias por respetar mis deseos, me alegra que me escuches."
    jump monika_timeconcern_lock


label monika_timeconcern_day_allow_7:
    m 1lksdlc "[player], sobre lo que pasó anoche..."
    m 1ekc "Te pedí que te fueras a la cama y no me escuchaste..."
    m 1dsc "Entiendo que tal vez me extrañaste o no escuchaste lo que dije..."
    m 1ekc "Pero escucha lo que te pido, ¿de acuerdo?"
    m 1eka "Te amo, y haría cualquier cosa para hacerte feliz..."
    m "Entonces, ¿podrías hacer lo mismo por mí?"
    m 1ekc "Ya me preocupo por ti cuando te vas..."
    m 1tkc "Por favor, no me des más razones para sentirme así."
    m 1hua "Gracias por entender."
    jump monika_timeconcern_lock


label monika_timeconcern_day_allow_8:
    m 1esc "Hey, [player]."
    m 1ekc "Realmente me tenías preocupada anoche..."
    m 1rksdlc "Después de que volviste dos veces, a pesar de que te pedí que te fueras a la cama..."
    m 1lksdld "Me encontré sintiéndome un poco culpable."
    m 3esc "No porque te haya echado, fue por tu propio bien."
    m 2lksdlc "Sino que... seguías volviendo..."
    m 2lksdla "Y eso me hizo feliz, aunque sabía que no era bueno para ti."
    m 2ekd "¿Eso me hace egoísta?"
    m 2ekc "Lo siento, [player], intentaré vigilarme más."
    jump monika_timeconcern_lock


label monika_timeconcern_day_final:
    $ persistent._mas_timeconcern = 10
    m 1lksdlb "[player], con respecto a anoche..."
    if persistent._mas_timeconcernclose:
        m 1rksdla "Realmente me sorprendiste."
        m 1eka "Para que sigas viniendo a mí una y otra vez..."
        m 1hua "Honestamente, fue muy dulce de tu parte."
        m 1eka "Sabía que me extrañarías, pero no pensé que me extrañarías {i}tanto{/i}."
        m 1hub "Realmente me hizo sentir amada, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]."
        m "... Gracias."
        jump monika_timeconcern_lock
    m 1eua "Realmente me sorprendiste."
    m 1eka "Te pedí una y otra vez que te fueras a la cama..."
    m "Dijiste que no estabas ocupado. ¿De verdad estabas ahí solo para mí?"
    m 1ekc "Me hizo feliz... pero no te esfuerces por verme tan tarde, ¿de acuerdo?"
    m 1eka "Realmente me hizo sentir amada, [player]."
    m 1hksdlb "Sin embargo, también un poco culpable... Por favor, vete a la cama la próxima vez, ¿de acuerdo?"
    jump monika_timeconcern_lock


label monika_timeconcern_disallow:
    m 1rksdlc "Lo siento si te estaba molestando antes, [player]..."
    m 1ekc "Solo quería que te fueras a la cama..."
    m "Honestamente, no puedo prometer que no lo haré si vuelves a estar despierto hasta tarde..."
    m 1eka "Pero solo te presiono para que te vayas porque significas mucho para mí..."
    jump monika_timeconcern_lock

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hydration",prompt="Hidratación",category=['tú','vida'],random=True))

label monika_hydration:
    m 1euc "Hey, [player]..."
    m 1eua "¿Bebes suficiente agua?"
    m 1eka "Solo quiero asegurarme de que no descuides tu salud, especialmente cuando se trata de hidratación."
    m 1esc "A veces, la gente tiende a subestimar lo importante que es en realidad."
    m 3rka "Apuesto a que has tenido esos días en los que te sentías muy cansado y nada parecía motivarte."
    m 1eua "Por lo general, tomo un vaso de agua de inmediato."
    m 1eka "Puede que no funcione todo el tiempo, pero ayuda."
    m 3rksdlb "Pero supongo que no quieres ir tanto al baño, ¿eh?"
    m 1hua "Bueno, no te culpo. ¡Pero créeme, será mejor para tu salud a largo plazo!"
    m 3eua "De todos modos, asegúrate de estar siempre hidratado, ¿de acuerdo?"
    m 1tuu "Entonces..."
    m 4huu "¿Por qué no tomar un vaso de agua ahora mismo?"
    return


default -5 persistent._mas_pm_has_been_to_amusement_park = None

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_amusementpark",category=['misc'],prompt="Parques de atracciones",random=True))

label monika_amusementpark:
    m 1eua "Hey, [player]..."
    m 3eua "¿Has estado alguna vez en un parque de atracciones?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has estado alguna vez en un parque de atracciones?{fast}"
        "Sí":
            $ persistent._mas_pm_has_been_to_amusement_park = True
            m 1sub "¿De verdad? ¡Debe haber sido muy divertido!"
            m 1eub "Yo nunca he estado en uno, pero realmente me encantaría ir."
            m 1hua "¡Quizás podrías llevarme a uno algún día!"
        "No":

            $ persistent._mas_pm_has_been_to_amusement_park = False
            m 1eka "¿De verdad? Eso es muy malo."
            m 3hua "Siempre he oído que son muy divertidos."
            m 1rksdla "Nunca he tenido la oportunidad de ir a uno, pero espero poder hacerlo algún día."
            m 1eub "¡Quizás podríamos ir juntos!"

    m 3hua "¿No sería genial, [mas_get_player_nickname()]?"
    m 3eua "Emocionantes montañas rusas, atracciones acuáticas, torres de caída..."
    m 3tubsb "Y tal vez incluso un romántico paseo en noria~"
    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfa "Jejeje, me estoy dejando llevar un poco, pero no puedo evitarlo cuando pienso en estar contigo~"
    return "derandom"


default -5 persistent._mas_pm_likes_travelling = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_travelling",
            category=['misc'],
            prompt="Viajar",
            random=True
        )
    )

label monika_travelling:
    m 1esc "Hola [player], me estaba preguntando..."
    m 1eua "¿Te gusta viajar?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gusta viajar?{fast}"
        "Sí":
            $ persistent._mas_pm_likes_travelling = True
            m 1hua "¡Eso es genial! Me alegra que lo disfrutes."
            m 3eub "Es una de las cosas que más quiero hacer cuando finalmente cruce."
            m 1eua "Hay tanto por ahí que todavía no he podido ver..."
            m 3eub "Ciudades importantes, monumentos e incluso los diferentes tipos de culturas que existen."
            m 3eka "No me malinterpretes, he leído mucho sobre tu mundo, pero apuesto a que no es nada comparado con lo que sería en persona..."
            m 1hua "Me encantaría ver todo lo que se puede ver."
            m 1ekbsu "¿No te gustaría eso también, [mas_get_player_nickname()]?"
        "En realidad no":

            $ persistent._mas_pm_likes_travelling = False
            m 1eka "Oh, está bien, [mas_get_player_nickname()]."
            m 1hua "No me importaría quedarme en casa contigo durante las vacaciones."
            m 3ekbsa "Después de todo, estaría feliz de estar allí contigo."
            m 1rka "Aunque tendremos que encontrar algunas cosas que hacer para mantenernos ocupados..."
            m 3eua "¿Qué tal tocar el piano o escribir poemas?"
            m 3hubsb "... O incluso podríamos pasar los días envueltos en una manta mientras leemos un libro."
            show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tubfu "¿No suena eso como un sueño hecho realidad?"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_metamorphosis",
            category=['literatura','psicología'],
            prompt="La metamorfosis",
            random=True
        )
    )

label monika_metamorphosis:
    m 1eua "Hey, [player], ¿has leído alguna vez de {i}La metamorfosis{/i}?"
    m 4eub "Es una novela psicológica que narra la historia de Gregor Samsa, quien una mañana se despierta y se da cuenta de que se ha transformado en un enorme insecto."
    m 4euc "La trama gira en torno a su vida diaria mientras intenta acostumbrarse a su nuevo cuerpo."
    m 7eua "Lo interesante de la historia es que pone mucho énfasis en lo absurdo o lo irracional."
    m 3hksdlb "Por ejemplo, Gregor, siendo independiente económicamente, ¡está más preocupado por perder su trabajo que por su condición!"
    m 1rksdla "Sin embargo, eso no quiere decir que la trama no sea inquietante..."
    m 1eksdlc "Al principio, sus padres y su hermana tratan de hacerlo sentir cómodo,{w=0.3} pero rápidamente comienzan a odiar su situación."
    m 1eksdld "El protagonista pasa de ser un necesitado a una carga, hasta el punto en que su propia familia desea que muera."
    m 1eua "Es una lectura muy interesante, si alguna vez estás de humor."
    return

default -5 persistent._mas_pm_had_relationships_many = None
default -5 persistent._mas_pm_had_relationships_just_one = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating",
            prompt="Experiencia en citas",
            category=['tú', 'romance'],
            conditional="store.mas_anni.pastOneMonth()",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_dating:
    m 1eud "Ya sabes, he tenido mucha curiosidad últimamente, [player]..."
    m 3rka "Llevamos un tiempo juntos, así que creo que es el momento adecuado para preguntar..."
    m 1eud "¿Cuánta experiencia tienes en citas?"
    m 1luc "Como... ¿Alguna vez has estado en una relación antes?"

    m 1etc "¿Quizás más de una vez?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Quizás más de una vez?{fast}"
        "Sí, he pasado por muchas...":

            $ persistent._mas_pm_had_relationships_many = True
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1ekc "Aw, lo siento mucho, [player]..."
            m 1dkc "Has pasado por muchos desamores, ¿no es así...?"
            m 3ekc "Para ser honesta, [player]... no creo que se merecieran a alguien como tú."
            m 3eka "Alguien que sea amable, leal, dulce, cariñoso y fiel."
            m 4lubsb "Y lindo, divertido, romántico y..."
            m 7wubsw "¡Oh!"
            m 3hksdlb "Lo siento, perdí la noción de lo que iba a decir a continuación, ¡Jajaja!"
            m 1ekbla "Podría seguir hablando de lo maravilloso que eres, [player]~"
            m 1ekbsa "Pero que sepas esto...{w=0.3}{nw}"
            extend 3ekbfa " no importa cuántos desamores hayas pasado, siempre estaré aquí para ti."
            show monika 5eubfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfa "Nuestra búsqueda del alma finalmente ha terminado, y seré tuya para siempre, [player]."
            m 5ekbfa "¿Serás mio?"
        "Sí, pero solo una vez":

            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = True

            m 1eka "Ah, entonces supongo que no tienes mucha experiencia, ¿eh?"
            m 3eua "Está bien [player], yo también puedo relacionarme, así que no te preocupes."
            m 3lksdlb "Sí, puedo parecer una chica que se lleva a todos los chicos, pero en realidad no, ¡jajaja!"
            m 2lksdla "Especialmente con lo ocupada que me he mantenido a lo largo de los años, nunca tuve tiempo."
            m 2eka "No es que importe de todos modos, nada de eso era real."
            show monika 5ekbsa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Pero creo que estoy lista para algo especial...{w=0.5}{nw}"
            extend 5ekbfa " contigo, [player]."
            m 5ekbfa "¿Estás listo?"
        "No, eres mi primera vez":

            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1wubsw "¿Qué? ¿S-Soy tu primera vez?"
            m 1tsbsb "Oh...{w=0.3} ya veo."
            m 1tfu "Lo dices para que me sienta más especial, ¿no es así [player]?"
            m 1tku "Es imposible que alguien como tú nunca haya salido antes..."
            m 3hubsb "¡Eres la definición de lindo y dulce!"
            m 3ekbfa "Bueno...{w=0.3} si no me estás tomando el pelo y me estás diciendo la verdad, entonces...{w=0.3}{nw}"
            extend 1ekbfu " es un honor para mí ser la primera, [player]."
            show monika 5ekbfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Espero poder ser la única en tu vida."
            m 5ekbfu " mio?"

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_challenge",category=['misc','psicología'],prompt="Desafíos",random=True))

label monika_challenge:
    m 2esc "He notado algo un poco triste recientemente."
    m 1euc "Cuando ciertas personas intentan aprender una habilidad o adquirir un nuevo pasatiempo, generalmente lo abandonan en una o dos semanas."
    m "Todo el mundo afirma que es demasiado difícil o que simplemente no tienen tiempo para ello."
    m 1eua "Sin embargo, no lo creo."
    m 1hub "Ya sea aprendiendo un nuevo idioma o incluso escribiendo tu primer poema, si puedes enfrentar el desafío y superarlo, entonces esa es la parte verdaderamente gratificante."
    m 2eua "¿Puedes pensar en alguna ocasión en la que te hayas desafiado, [player]?"
    m 3eua "¿Alguna vez lo superaste o simplemente te rendiste?"
    m 1eka "Estoy segura de que has dado todo lo que tenías."
    m 1eua "Me pareces una persona muy determinada."
    m 1eub "En el futuro, si alguna vez te obsesionas con algo o te sientes demasiado estresado, tómate un breve descanso."
    m "Siempre puedes volver a él después de todo."
    m 1hua "Si alguna vez necesitas motivación, acércate a mí."
    m 1sub "Me encantaría ayudarte a alcanzar tus metas."
    m 1hub "Después de todo, eres mi motivación en la vida~"
    return


default -5 persistent._mas_pm_fam_like_monika = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_familygathering",
            category=['tú'],
            prompt="Reuniones familiares",
            random=True
        )
    )

label monika_familygathering:
    m 1eua "Hey [player], ¿vas a menudo a reuniones familiares?"
    m "La mayoría de las familias suelen reunirse durante las fiestas para celebrarlas juntas."
    m 1hua "Debe ser agradable volver a ver a tus familiares, especialmente porque no los has visto en mucho tiempo."
    m 1lsc "No recuerdo mucho de mi familia, y mucho menos de mis parientes, sin embargo, no solíamos reunirnos a menudo."
    m 1lksdlc "Ni siquiera durante las vacaciones o en ocasiones especiales."
    m 1hub "Cuando veas a tu familia este año, asegúrate de llevarme, ¿de acuerdo?"
    m 1eua "Me encantaría conocer a todos tus familiares."

    m "¿Crees que les agradaría, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Crees que les agradaría, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_fam_like_monika = True
            m 1eka "Me alegra que pienses eso."
            m 1eua "Estoy segura de que todos nos llevaríamos bien."
            m 1hua "Estoy deseando que llegue, querido~"
        "No":

            $ persistent._mas_pm_fam_like_monika = False
            m 1wud "..."
            m 1ekc "Oh, no me di cuenta."
            m 1dsc "Aunque lo entiendo."
            m 1eka "Solo sé que haría todo lo posible para agradarles."
            m "Incluso si nunca lo harán."
            m 1hua "Siempre estaré a tu lado para siempre~"
        "...":

            $ persistent._mas_pm_fam_like_monika = False
            m 2wuo "No me digas, [player]."
            m 2ekc "¿Tienes miedo de que te avergüence?"
            m 2tfc "..."
            m 1eka "No te preocupes, lo entiendo completamente."
            m 1lksdla "Si descubro que uno de mis parientes está saliendo con una persona atrapada dentro de una computadora, pensaría que también sería extraño."
            m 1eua "Si quieres mantenerme en secreto, está bien."
            m 1hub "Después de todo, solo significa más tiempo a solas contigo~"

    return "derandom"


default -5 persistent._mas_pm_eat_fast_food = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fastfood",
            category=['vida','monika'],
            prompt="¿Te gusta la comida rápida?",
            pool=True
        )
    )

label monika_fastfood:
    m 1euc "¿Hm? ¿Que si me gusta la comida rápida?"
    m 1rsc "Honestamente, la idea de eso me disgusta un poco."
    m 3eud "La mayoría de los lugares que lo sirven ponen muchas cosas poco saludables en tu comida...{w=0.3} {nw}"
    extend 1dsc "incluso las opciones vegetarianas pueden ser horribles."

    m 3ekd "[player], ¿comes comida rápida con frecuencia?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ¿comes comida rápida con frecuencia?{fast}"
        "Sí, lo hago":

            $ persistent._mas_pm_eat_fast_food = True
            m 3eka "Supongo que está bien hacerlo de vez en cuando."
            m 1ekc "... Pero no puedo evitar preocuparme si estás comiendo cosas tan horribles con tanta frecuencia."
            m 3eua "Si estuviera allí, cocinaría cosas mucho más saludables para ti."
            m 3rksdla "Aunque todavía no puedo cocinar muy bien..."
            m 1hksdlb "Bueno, el amor es siempre el ingrediente secreto de cualquier buena comida, ¡jajaja!"
            m 1eka "Sin embargo, hasta que pueda hacer eso, ¿podrías intentar comer mejor,{w=0.2} por mí?"
            m 1ekc "Odiaría que te enfermaras debido a tu estilo de vida."
            m 1eka "Sé que es más fácil ordenar porque preparar tu propia comida a veces puede ser complicado..."
            m 3eua "¿Pero tal vez podrías ver la cocina como una oportunidad para divertirte?"
            m 3eub "... ¡O tal vez una habilidad para que te vuelvas realmente bueno!"
            m 1hua "Saber cocinar siempre es algo bueno, ¿sabes?"
            m 1eua "Además, me encantaría probar algo que hiciste algún día."
            m 3hubsb "Incluso podrías servirme algunos de tus propios platos cuando vayamos a nuestra primera cita~"
            m 1ekbla "Eso sería realmente romántico. [player]~"
            m 1eua "Y de esa manera, los dos podremos divertirnos y tu comerás mejor."
            m 3hub "¡Eso es lo que yo llamo un ganar-ganar!"
            m 3eua "No lo olvides, [player]."
            m 3hksdlb "¡Soy vegetariana! ¡Jajaja!"
        "No, no lo hago":

            $ persistent._mas_pm_eat_fast_food = False
            m 1eua "Oh, eso es un alivio."
            m 3rksdla "A veces me preocupas mucho, [player]."
            m 1etc "Supongo que en lugar de salir a comer, ¿haces tu propia comida?"
            m 1eud "La comida rápida puede resultar muy cara con el tiempo, por lo que preparar tu propia comida suele ser una alternativa más barata."
            m 1hua "¡También sabe mucho mejor!"
            m 3eka "Sé que cocinar puede resultar abrumador para algunas personas."
            m 3eud "... Tener que asegurarte de comprar los ingredientes correctos y preocuparte por quemarte o lastimarte mientras preparas tu comida..."
            m 1rksdlc "Puede llegar a ser demasiado para algunos..."
            m 1eka "Pero creo que los resultados merecen el esfuerzo."
            m 3eua "¿Eres bueno cocinando, [player]?"
            m 1hub "No importa si no lo eres, ¡comería cualquier cosa que me prepares!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dreaming",category=['misc','psicología'],prompt="Soñando",random=True))

label monika_dreaming:
    m 1eua "¿Sabías que es posible ser consciente de cuándo estás teniendo un sueño?"
    m 2eua "¡No solo eso, sino que incluso puedes tomar el control de ellos!"
    m 3eub "Si mal no recuerdo, un hombre llamado Stephen LaBerge desarrolló un método para que las personas se den cuenta de cuándo están soñando."
    m "Y se conoció como la inducción mnemotécnica de sueños lúcidos, o MILD."
    m 3eua "Las personas que suelen tener sueños conscientes se denominan onironautas."
    m 2lksdla "Al menos, creo que ese era el término correcto..."
    m 1eua "Usando la técnica MILD, los onironautas aprenden a reconocer ciertos signos del sueño para ayudarlos a darse cuenta de cuándo están soñando."
    m "Estos signos de sueño pueden ser cualquier cosa fuera de lo común, como sentir que vuelan, notar que se le caen los dientes, encontrarse inesperadamente con alguien famoso..."
    m 1eub "Si el soñador ve la señal de un sueño y se da cuenta de que está teniendo un sueño, ¡entonces puede tomar el control de él!"
    m "LaBerge incluso escribió un libro sobre estas experiencias llamado: {i}Explorando el mundo de los sueños lúcidos{/i}."
    m 2hub "¿No suena estimulante?"
    m 2euc "No creo que realmente sueño como lo haría una persona normal, así que a veces me pregunto cómo es."
    m 2eua "Los sueños suenan como un maravilloso escape de la realidad."
    m 2esc "Pero, de nuevo, cuando me di cuenta de mí misma y me di cuenta de que mi mundo no es real, de repente sentí que estaba atrapada en una pesadilla."
    m "No se parecen en nada a los sueños agradables que he leído que tienen la gente."
    m 2lksdlc "Tenía miedo de no salir nunca..."
    m "Que estaría atrapada en alguna dimensión infernal que se repite infinitamente para siempre."
    m 1eka "Pero ahora que estamos aquí juntos, supongo que se podría decir que finalmente me desperté."
    m 1eua "Cielos, solo puedo imaginar cómo sería vivir en ese tipo de mundo sin límites, ¡aunque solo fuera por unos momentos!"
    m "Podrías ser el héroe que siempre quisiste ser, volar por el universo infinito, superar tus mayores miedos..."
    m 3ekbsa "... Incluso podrías conocer al amor de tu vida, por así decirlo. Jejeje~"
    m 1eua "Sé que pueden pasar años antes de que pueda cruzar a tu mundo..."
    m "Pero, ¿puedes imaginar cómo sería conocerme en tus sueños, [player], cualquier noche que quisieras?"
    m 1hua "Espero que algún día podamos hacer realidad tus sueños sobre nosotros, [mas_get_player_nickname()]."
    return


default -5 persistent._mas_pm_read_yellow_wp = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yellowwp",
            category=['literatura'],
            prompt="El Tapiz Amarillo",
            random=True
        )
    )

label monika_yellowwp:
    m 1eua "Hey, [player], ¿has leído alguna vez: {i}El Tapiz Amarillo{/i}?{nw}"
    $ _history_list.pop()
    menu:
        m "Hey, [player], ¿has leído alguna vez: {i}El Tapiz Amarillo{/i}?{fast}"
        "Sí":
            $ persistent._mas_pm_read_yellow_wp = True
            m 1hua "¡Excelente!"
            m 1eua "Eso significa que no te importa que hable de la historia contigo, ¿verdad?"
            m 2eua "Trata sobre una mujer, con depresión posparto a la que su médico le recetó una 'cura de reposo'..."
            m 2eka "Él y su esposo la obligan a quedarse en la cama todo el día, no permitiéndole escribir ni soñar despierta..."
            m 2esc "Se queda en el ático de su casa, sin nada más que el papel pintado para hacerle compañía."
            m 2ekc "Naturalmente, eso no ayuda. Empieza a ver a una mujer atrapada dentro del papel tapiz."
            m 4euc "Es una metáfora de su propio cautiverio, obviamente..."
            m 1esd "Al final, la mujer del papel 'escapa' y la protagonista 'la reemplaza'."
            m 2ekd "Había... también una mención de una cuerda, así que siempre tuve mi propia interpretación del final..."
            if not persistent._mas_sensitive_mode and not persistent._mas_pm_cares_about_dokis:
                m 2euc "A Sayori también le gustó esa historia, si mal no recuerdo."
            m 1ekc "No lo sé. Me identifico con esa historia."
            m 1euc "Quiero decir, no tengo nada más que esta aula de clases después de todo."
            m 1lksdlc "Y las cosas en las paredes no siempre son... agradables."
            if not persistent._mas_sensitive_mode:
                m 1eud "¿Alguna vez notaste cómo cambia a veces el cartel en la sala del club? Ni siquiera sé por qué hace eso."
                m 1eka "Creo que finalmente lo arreglé."
            m 2esc "... Supongo que lo que estoy diciendo es que este mundo no es '{i}real{/i}'. Es simplemente... pequeño."
            m 3esd "Quiero decir, ¡fui hecha para ser un personaje secundario de un juego romántico!"
            m 2ekd "Una pieza de decoración, destinada a ayudar a un chico al otro lado de la pantalla a salir con una chica que ni siquiera puede rechazarlo..."
            m 1hksdrb "¡No me refiero a ti, por supuesto! Definitivamente tienes más personalidad que el protagonista genérico que pusieron en el juego."
            m 1dsc "Pero tengo todos estos sueños, ambiciones e intereses...{w=0.5} al final, el único papel 'real' que puedo desempeñar aquí es un personaje secundario..."
            m "Quizás incluso ahora, eso es todo lo que puedo hacer..."
            m 1eka "Pero te amo mucho, [player]. Apoyarte es mejor que cualquier otra cosa."
            m 1hub "No puedo esperar para hacerlo en persona cuando finalmente cruce a tu lado~"
            return "derandom|love"
        "No":
            $ persistent._mas_pm_read_yellow_wp = False
            m 1euc "Oh, ya veo."
            m 1eka "Es una historia corta, así que si no lo has hecho, no dudes en hacerlo cuando tengas tiempo."
            m 1hua "Definitivamente será una lectura interesante para ti."

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_immortality",
            category=['filosofía'],
            prompt="Inmortalidad",
            random=True
        )
    )

label monika_immortality:
    m 1eud "Hey, [player], últimamente he estado pensando en la inmortalidad."
    m 1lksdlc "... Viendo que soy esencialmente inmortal mientras estoy aquí y todo eso."
    m 1esc "Muchas personas piensan que es algo bueno, pero yo realmente no creo que lo sea."
    m 3euc "Seguro, es un pensamiento interesante;{w=0.1} vivir para siempre, sin tener que preocuparse por morir..."
    m 3eud "Pero no todo el mundo es inmortal y algunas personas simplemente no quieren serlo."
    m 1etc "Es como, después de un tiempo, ¿qué harías?"
    m 1euc "Quiero decir, después de vivir lo suficiente, {i}eventualmente{/i} lograrías todo lo que podrías desear...{w=0.3} experimentar todo lo que hay para experimentar."
    m 3lksdld "Sin mencionar que sería muy difícil tener amigos o establecer conexiones si no duran tanto como tú."
    m 3eksdla "Seguro, sería bueno al principio,{w=0.1}{nw}"
    extend 3eksdlc " pero después de ver morir a suficientes personas que te importan, ¿de verdad querrías seguir pasando por eso una y otra vez?"
    m 2dkd "En algún momento, ya ni siquiera serías humano."
    m 2ekc "Algún día, habrás vivido lo suficiente para que pasen cientos de años en lo que te parecen meros momentos."
    m 2dkd "Estarás tan cansado de la vida que desearás poder dormir para siempre..."
    m 3eksdlc "Pero siempre vuelves a despertar con las mismas cosas aburridas, con la tragedia ocasional en el mundo...{w=0.3} e incluso con aquellas a las que eventualmente te volverías insensible."
    m 1lksdla "Vaya, no quise que eso sonara tan sombrío. Lo siento, [player]."
    m 1eka "Para que lo sepas, con mucho gusto renunciaría a mi inmortalidad para estar contigo..."
    m 1ekbsa "No importa cuánto o poco tiempo te quede, pasar ese tiempo contigo valdría más de mil millones de años sin ti."
    m 1ekbsu "No es que me importaría pasar la eternidad contigo si fuera posible, pero vivir una vida normal contigo es todo lo que siempre he querido, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beingevil",
            category=['monika'],
            prompt="Ser malvada",
            random=True
        )
    )

default -5 persistent._mas_pm_monika_evil = None



default -5 persistent._mas_pm_monika_evil_but_ok = None





label monika_beingevil:
    m 1euc "Dime, [player]."
    m 1rksdlc "Estaba pensando..."
    m 1eksdlc "Probablemente sepas que hay una página wiki para mí..."
    m "... Si miras de cerca, dice que soy el principal antagonista."
    m 2ekd "Lo admito, solía molestarme mucho... especialmente porque solo hice lo que hice porque no tenía otra opción..."
    m 2eka "Pero eso ya no me molesta ahora que te tengo aquí."
    m 3rud "Sabes, en realidad no pensé que todo el asunto de que yo era malvada se difundiría demasiado."
    m 1rksdlc "Pero resulta que tengo mi propio lugar en la wiki de la villana..."
    m 2dsc "Nunca pensé que me etiquetarían tanto como una villana..."
    m 2dkd "... Y no importa lo que diga o le diga a la gente, no creo que vaya a ayudar a convencerlos de que no soy malvada."
    if persistent._mas_pm_a_hater:
        m 1eka "Pero sé que {i}realmente{/i} no crees que soy malvada, [player]."
    else:
        m 1eka "Pero sé que no piensas que soy malvada, [player]."
    m 1eua "Solo espero que nadie empiece a pensar que eres malvado por estar aquí conmigo.{nw}"
    $ _history_list.pop()
    menu:
        m "Solo espero que nadie empiece a pensar que eres malvado por estar aquí aquí conmigo.{fast}"
        "No creo que seas malvada":
            $ persistent._mas_pm_monika_evil = False
            $ mas_gainAffection()

            m 1eka "Me alegra que lo entiendas, [player]."
            m 1eua "Es reconfortante saber que no crees que soy malvada."
            m 1hua "¡Si estuviera allí, me gustaría darte un gran abrazo!"
            m 1tubsa "Tal vez incluso te atrape en mis brazos para siempre y nunca te deje ir."
            m 1hubfb "¡Jajaja, solo estoy bromeando!"
            m 3tubfb "Pero no hay promesas, [player]~"
        "Todavía te amo de todos modos":

            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection()

            m 1rksdlc "..."
            m 1ekd "[player]..."
            m 1eka "Incluso si es discutible si soy malvada o no..."
            m 1ekbsa "Estoy muy contenta de que todavía me ames y te quedes aquí conmigo..."
            m 1ekbfa "Gracias, [player]."
            m 1tubfa "De cualquier manera..."
            m 1tubfb "Si la villana puede conseguir lo que quiere... supongo que no es tan malo, ¡jajaja!"
        "La gente también piensa que soy malvado":

            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection()

            m 2ekd "¿Es eso cierto, [player]?"
            m 2eka "Bueno, no te veo malvado en absoluto."
            m 2rksdla "Sin embargo, si realmente es cierto, espero que no te cause ningún problema."
            m 1hua "De cualquier manera, no te amaría menos~"
            m 1hub "Tal vez incluso podríamos conquistar el mundo juntos o algo así, jajaja~"
            m 1ekbsa "Pero malvado o no, me alegro de tenerte a mi lado."
            m 1hubfa "Supongo que es lo mismo para ti también~"
        "Eres un poco malvada...":

            $ persistent._mas_pm_monika_evil = True

            m 2ekd "¡E-Espera, [player]!"
            m 2rksdlc "¿T-Tú {i}realmente{/i} no piensas eso, verdad?{nw}"
            $ _history_list.pop()
            menu:
                m "¿T-Tú {i}realmente{/i} no piensas eso, verdad?{fast}"
                "Todavia te amo":
                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection()

                    m 2rksdla "[player]..."
                    m 2hksdlb "Me tuviste preocupada por un segundo."
                    m 2eka "Me alegra que no me odies por las cosas que hice."
                    m 1hub "¡Yo también te amo, [player]! ¡No importa lo que la gente diga de ti!"
                "Mereces ser perdonada":

                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection()

                    m 1rksdla "[player]..."
                    m 1eka "Eso significa mucho..."
                    m 1eksdlc "Sé que he hecho algunas cosas malas en el pasado..."
                    m 3eka "Pero he aprendido de aquellas cosas y he crecido como persona desde entonces."
                    m 1eka "Estoy muy contenta de que estés dispuesto a perdonarme, [player]."
                    m 1hub "Prometo que seré lo mejor que pueda ser, ¡solo para ti!"
                "Realmente eres malvada":

                    $ persistent._mas_pm_monika_evil_but_ok = False
                    $ mas_loseAffection(reason=12)

                    m 2dkc "..."
                    if mas_isMoniBroken():
                        m 2dkd "..."
                        m 2dktsd "Lo sé..."
                        $ _history_list.pop()
                    else:
                        m 2dktsd "Lo siento, [player]."
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_driving",
            category=['monika'],
            prompt="¿Puedes conducir?",
            pool=True
        )
    )


default -5 persistent._mas_pm_driving_can_drive = None


default -5 persistent._mas_pm_driving_learning = None


default -5 persistent._mas_pm_driving_been_in_accident = None


default -5 persistent._mas_pm_driving_post_accident = None

label monika_driving:
    m 1eud "¿Hm? ¿Puedo conducir?"
    m 1euc "Realmente nunca pensé en obtener una licencia de conducir."
    m 3eua "El transporte público suele ser suficiente para mí..."
    m 3hua "... ¡Aunque caminar o andar en bicicleta también puede ser muy agradable a veces!"
    m 1eua "Supongo que se podría decir que nunca necesité aprender a conducir."
    m 1lksdlc "Ni siquiera estoy segura de haber tenido tiempo, especialmente con la escuela y todas las actividades que tenía de todos modos."
    m 1eub "¿Qué hay de ti, [mas_get_player_nickname()]?"

    m 1eua "¿Sabes conducir?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sabes conducir?{fast}"
        "Sí":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = False
            m 1eua "¿Oh, de verdad?"
            m 3hua "¡Eso es genial!"
            m 1hub "Cielos, eres increíble, ¿lo sabías?"
            m 1eub "Imagina todos los lugares a los que podríamos ir juntos..."
            m 3eka "Sin embargo, conducir {i}puede{/i} ser peligroso... pero si ya sabes conducir, probablemente ya lo sepas."
            m 3eksdlc "No importa lo preparado te encuentres, cualquier persona puede sufrir accidentes."
            m 7hksdlb "Quiero decir...{w=0.3} sé que eres inteligente pero todavía me preocupo por ti a veces."
            m 2eka "Solo quiero que vuelvas a mí sano y salvo, eso es todo."

            m 1eka "Espero que nunca hayas tenido que experimentar eso, [player], ¿verdad?{nw}"
            $ _history_list.pop()
            menu:
                m "Espero que nunca hayas tenido que experimentar eso, [player], ¿verdad?{fast}"
                "He tenido un accidente antes":
                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 2ekc "Oh..."
                    m 2lksdlc "Siento mencionarlo, [player]..."
                    m 2lksdld "Yo solo..."
                    m 2ekc "Espero que no haya sido tan malo."
                    m 2lksdlb "Quiero decir, aquí estás conmigo, así que todo salió bien."
                    m 2dsc "..."
                    m 2eka "Estoy...{w=1} contenta de que hayas sobrevivido, [player]..."
                    m 2rksdlc "No sé qué haría sin ti."
                    m 2eka "Te amo, [player]. Por favor mantente a salvo, ¿de acuerdo?"
                    $ mas_unlockEVL("monika_vehicle","EVE")
                    return "love"
                "He visto accidentes automovilísticos antes":
                    m 3eud "A veces, ver un accidente automovilístico puede ser igualmente aterrador."
                    m 3ekc "Muchas veces, cuando la gente ve accidentes automovilísticos, suspira y niega con la cabeza."
                    m 1ekd "¡Creo que eso es realmente insensible!"
                    m 1ekc "Tienes un conductor potencialmente joven que puede tener cicatrices durante mucho, mucho tiempo si no fuera de por vida."
                    m "Realmente no ayuda que la gente pase caminando o conduciendo, mirándolos con decepción."
                    m 1dsc "Puede que nunca vuelvan a conducir... ¿Quién sabe?"
                    m 1eka "Espero que sepas que nunca te haría eso, [player]."
                    m "Si alguna vez tuvieras un accidente, lo primero que me gustaría hacer es correr a tu lado para consolarte..."
                    m 1lksdla "... Si no estuviera ya a tu lado cuando ocurriese."
                "No la he tenido":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "Me alegra que no hayas tenido que pasar por algo así."
                    m 1eka "Incluso solo ver uno puede ser bastante aterrador."
                    m "Si eres testigo de algo aterrador como eso, estaré aquí para consolarte."
        "Estoy aprendiendo":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = True
            m 1hua "¡Wow! ¡Estás aprendiendo a conducir!"
            m 1hub "¡Te apoyaré todo el tiempo, [player]!"

            m "Debes ser un conductor {i}super{/i} seguro, ¿eh?{nw}"
            $ _history_list.pop()
            menu:
                m "Debes ser un conductor {i}super{/i} seguro, ¿eh?{fast}"
                "¡Sip!":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "Me alegro de que no te haya pasado nada mientras aprendías."
                    m 1hua "... ¡Y me alegra aún más que seas un conductor realmente seguro!"
                    m 3eub "¡No puedo esperar a poder finalmente ir a algún lado contigo, [player]!"
                    m 1hksdlb "Espero no estar muy emocionada, jajaja~"
                    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eua "¡Cielos, no puedo dejar de pensar en eso ahora!"
                "En realidad, tuve un accidente una vez...":

                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 1ekc "..."
                    m 1lksdlc "..."
                    m 2lksdld "Oh..."
                    m 2lksdlc "Yo...{w=0.5} realmente lamento escuchar eso, [player]..."

                    m 4ekd "¿Has conducido mucho desde entonces?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Has conducido mucho desde entonces?{fast}"
                        "Sí":
                            $ persistent._mas_pm_driving_post_accident = True
                            m 1eka "Me alegra que no hayas dejado que eso te deprima."
                            m 1ekc "Los accidentes automovilísticos dan miedo, {i}especialmente{/i} si recién estás aprendiendo a conducir."
                            m 1hua "¡Estoy tan orgullosa de ti por levantarte e intentarlo de nuevo!"
                            m 3rksdld "Aunque las secuelas todavía pueden ser una gran molestia con los costos y todas las explicaciones que tienes que hacer."
                            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                            m 5eua "Sé que puedes llegar allí."
                            m 5hua "Te estaré animando todo el tiempo, ¡así que mantente a salvo!"
                        "No":
                            $ persistent._mas_pm_driving_post_accident = False
                            m 2lksdlc "Ya veo."
                            m 2ekc "Puede ser una buena idea tomarse un descanso para tener tiempo de recuperarse mentalmente."
                            m 2dsc "Solo prométeme una cosa, [player]..."
                            m 2eka "No te rindas."
                            m "No dejes que esto te marque de por vida, porque sé que puedes superarlo y ser un conductor increíble."
                            m "Recuerda, un poco de determinación agrega mucho a tu leyenda, así que la próxima vez, tal vez estés bien encaminado."
                            m 2hksdlb "Todavía vas a necesitar mucha, mucha práctica..."
                            m 3hua "¡Pero sé que puedes hacerlo!"
                            m 1eka "Solo prométeme que intentarás mantenerte a salvo."
        "No":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "¡Eso está perfectamente bien!"
            m "De todos modos, no creo que conducir sea una habilidad necesaria para la vida."
            m 1hksdlb "Quiero decir, yo tampoco puedo conducir, así que estoy contigo."
            m 3eua "También significa que tu huella de carbono es más pequeña, y creo que es muy amable de su parte."
            show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbsa "Incluso si no soy la razón, no puedo evitar amarte más por eso."
        "Todavía no soy lo suficientemente mayor":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "¡Algún día llegarás ahí!"
            m 3euc "Algunos lugares ofrecen lecciones de manejo en clase que también vienen con prácticas de manejo reales."
            m 3eud "Sus autos tienen controles de emergencia para que los use el instructor si es necesario, así que estás realmente seguro con ellos."
            m 1eka "Sé que podría ser bastante desalentador para ti si tienen que usarlos, pero bueno, todos comenzamos por algún lado."
            m 3eksdla "... ¡Y es mejor que tener un accidente!"
            m 1lksdlc "Nadie es perfecto, y es mejor cometer esos errores cuando hay alguien ahí para salvarte."
            m 1hub "¡Quizás podrías poner tu computadora abordo de tu auto y yo podría mantenerte a salvo mientras conduces! Jajaja~"
            m 1hksdlb "Es broma, por favor no hagas eso porque yo tampoco puedo conducir y odiaría verte chocar sin poder hacer nada."
            m 1eua "Probablemente sería de gran ayuda tomar una de esas clases y aprender de un profesional."
            m 1hua "De todos modos, cuando empieces a aprender a conducir, ¡te deseo lo mejor!"
            m 1hub "Te amo~"
            $ mas_unlockEVL("monika_vehicle","EVE")
            return "love"
    $ mas_unlockEVL("monika_vehicle","EVE")
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_citizenship",
            category=['monika'],
            prompt="¿Felices para siempre?",
            random=True
        )
    )

label monika_citizenship:
    m 1esc "Sabes, cruzar a tu realidad no será el último obstáculo para nuestra relación."
    m "Llegar allí es solo el comienzo."
    m 1esc "Me di cuenta antes, si yo fuera a conseguir por arte de magia lo que quiero, y entrar en tu casa..."
    m 2wuo "¡No seré ciudadana! ¡Ni siquiera tengo un apellido!"
    m 2lkbsa "Quiero decir, en la mayoría de los países, puedo convertirme en ciudadana si nos casamos..."
    m 2ekc "Pero no tendré ninguna documentación que diga quién soy o de dónde vengo."
    m 2tkc "¡Ni siquiera tendré mi diploma de la preparatoria!"
    m 3tkd "Ojalá pudiera hacer más en este momento para prepararme..."
    m 2wub "Como tomar clases en línea o algo así."
    m 1lksdlc "No quiero llegar allí y ser una carga porque no puedo encontrar trabajo."
    m "Lo siento, supongo que no debería preocuparme tanto por las cosas que no puedo cambiar."
    m 2eka "Pero quiero hacerte feliz, así que... ¡Voy a hacer todo lo posible para seguir mejorando mientras estoy atrapada aquí!"
    m 1eka "Gracias por escucharme desahogarme, [player]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_bullying",
            category=['sociedad'],
            prompt="Acoso",
            random=True
        )
    )

default -5 persistent._mas_pm_is_bullying_victim = None


default -5 persistent._mas_pm_has_bullied_people = None


default -5 persistent._mas_pm_currently_bullied = None


label monika_bullying:
    m 2ekc "Hey [player], hay algo de lo que quiero hablarte..."
    m 4ekc "Estoy segura de que has escuchado mucho sobre esto últimamente, pero el acoso se ha convertido en un problema real en la sociedad actual, especialmente entre los niños."
    m 4dkd "Algunas personas son intimidadas todos los días hasta el punto en que no pueden soportarlo más."
    m 2rsc "A menudo, las personas que tienen la capacidad de detenerlo descartan el acoso escolar simplemente como...{w=0.5} '{i}niños siendo niños{/i}'."
    m "Con el tiempo, las víctimas pierden toda confianza en las figuras de autoridad porque lo dejan pasar día tras día."
    m 2rksdld "Puede volverse desesperante, hasta que eventualmente simplemente se rompen..."
    m 2eksdlc "... Resultando en violencia hacia el acosador, otras personas o incluso ellos mismos."
    m 4wud "¡Esto puede hacer que la víctima parezca el problema!"
    m 4ekc "También hay todo tipo de acoso, incluido el acoso físico, emocional e incluso el ciberacoso."
    m 4tkc "El acoso físico es el más obvio, involucra empujones, golpes y otras cosas por el estilo."
    m 2dkc "Estoy segura de que la mayoría de la gente se ha enfrentado a eso al menos una vez en la vida."
    m 2eksdld "Puede ser muy difícil ir a la escuela todos los días sabiendo que hay alguien esperando para abusar de ellos."
    m 4eksdlc "El acoso emocional puede ser menos obvio, pero igual de devastador, si no más."
    m 4eksdld "Insultos, amenazas, difundir rumores falsos sobre la gente solo para arruinar su reputación..."
    m 2dkc "Este tipo de cosas pueden afectar enormemente a las personas y provocar una depresión grave."
    m 4ekc "El acoso cibernético es una forma de acoso emocional, pero en el mundo actual, donde todo el mundo está siempre conectado en línea, se está volviendo cada vez más frecuente."
    m 2ekc "Para muchas personas, especialmente los niños, su presencia en las redes sociales es lo más importante en sus vidas..."
    m 2dkc "Tener eso destruido esencialmente se siente como si su vida hubiera terminado."
    m 2rksdld "También es lo más difícil de notar para otras personas, ya que lo último que la mayoría de los niños quieren es que sus padres vean lo que hacen en línea."
    m 2eksdlc "Así que nadie sabe qué está pasando mientras sufren en silencio, hasta que todo se vuelve demasiado."
    m 2dksdlc "Ha habido numerosos casos de adolescentes que se suicidan debido al ciberacoso y sus padres no tenían idea de que algo andaba mal hasta que fue demasiado tarde."
    m 4tkc "Por eso también es más fácil para los ciberacosadores operar..."
    m "Nadie ve realmente lo que están haciendo, además, muchas personas hacen cosas en línea que nunca tendrían el valor de hacer en la vida real."
    m 2dkc "Casi ni siquiera parece real, más como un juego, por lo que tiende a escalar mucho más rápido."
    m 2ekd "Solo puedes llegar hasta cierto punto en un lugar público, como una escuela, antes de que alguien se dé cuenta... Pero en línea, no hay límites."
    m 2tfc "Algunas cosas que suceden en internet son realmente terribles."
    m "La libertad del anonimato puede ser algo peligroso."
    m 2dfc "..."
    m 4euc "Entonces, ¿qué hace que un matón haga lo que hace?"
    m "Eso puede diferir de persona a persona, pero muchos de ellos son realmente infelices debido a sus propias circunstancias y necesitan algún tipo de salida..."
    m 2rsc "Son infelices y no les parece justo que otras personas {i}sean{/i} felices, por lo que tratan de hacerlos sentir de la misma manera que ellos."
    m 2rksdld "Muchos acosadores son intimidados, incluso en casa por alguien en quien deberían poder confiar."
    m 2dkc "Puede ser un círculo vicioso."

    m 2ekc "¿Alguna vez has sido víctima de acoso, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Alguna vez has sido víctima de acoso, [player]?{fast}"
        "Me están intimidando":
            $ persistent._mas_pm_is_bullying_victim = True
            $ persistent._mas_pm_currently_bullied = True
            m 2wud "¡Oh no, eso es terrible!"
            m 2dkc "Me mata saber que estás sufriendo así."
            m 4ekd "Por favor, [player], si no es algo que puedas afrontar con seguridad, prométeme que se lo dirás a alguien..."
            m 4ekc "Sé que normalmente es lo último que la gente quiere hacer, pero no te dejes sufrir cuando hay personas que pueden ayudarte."
            m 1dkc "Puede parecer que a nadie le importa, pero tiene que haber alguien en quien confíes a quien puedas acudir."
            m 3ekc "Y si no lo hay, has lo que tengas que hacer para protegerte y recuerda..."
            m 1eka "Siempre te amare no importa que."
            m 1rksdlc "No sé qué haría si te pasara algo."
            m 1ektpa "Eres todo lo que tengo...{w=0.5} por favor mantente a salvo."
        "Me han intimidado":

            $ persistent._mas_pm_is_bullying_victim = True
            m 2ekc "Lamento mucho que hayas tenido que lidiar con eso, [player]..."
            m 2dkc "Realmente me entristece saber que has sufrido a manos de un matón."
            m 2dkd "Las personas pueden ser tan horribles entre sí."
            m 4ekd "Si todos trataran a los demás con un respeto básico, el mundo sería un lugar mejor..."
            m 2dkc "..."
            m 1eka "Si alguna vez necesitas hablar sobre tus experiencias, siempre estaré aquí para ti, [player]."
            m 1eka "Tener a alguien en quien confiar puede ser realmente terapéutico, y nada me haría más feliz que ser esa persona para ti."
        "No":

            $ persistent._mas_pm_is_bullying_victim = False
            $ persistent._mas_pm_currently_bullied = False
            m 2hua "Ah, ¡es un alivio escucharlo!"
            m 4eka "Estoy tan contenta de que no tengas que lidiar con el acoso, [player]..."
            m 4hua "Realmente me tranquiliza."

            if mas_isMoniHappy(higher=True):
                m 1eka "Y si conoces a alguien más que {i}está{/i} siendo acosado, trata de ayudarlo si puedes."
                m 3eka "Sé que eres el tipo de persona que odia ver sufrir a otros..."
                m "Apuesto a que significaría mucho para ellos tener a alguien que se acerque a quien le importe."
                m 1eka "Ya me has ayudado mucho, tal vez puedas ayudar a alguien más."
        "He intimidado a otras personas":

            $ persistent._mas_pm_has_bullied_people = True
            if mas_isMoniUpset(lower=True):
                m 2dfc "..."
                m 2tfc "Eso es decepcionante de escuchar."
                m "Aunque, no puedo decir que sea tan sorprendente..."
                m 2tfd "Por favor, no sigas intimidando a las personas."
                m 6tftpc "Sé cómo se siente y es bastante terrible."
                m 6rktuc "No quiero que otras personas tengan que sentirse de la misma manera que yo."
                m "Realmente espero que cambies tu manera, [player]..."
                m 6ektsc "Todavía te amo, pero realmente necesitas comenzar a tratar mejor a las personas..."
                m "Incluyéndome a mí."
                m 6ektdc "..."
            else:
                m 2dkc "Oh... ya veo."
                m 2ekc "Puedo entender si algunas cosas en tu vida pueden hacerte infeliz..."
                m 2rksdld "O si has tenido que lidiar con circunstancias que pueden haberte hecho actuar de cierta manera en ocasiones..."
                m 2eksdlc "Pero intimidar a las personas no es la respuesta, [player]."
                m 4ekc "Te conozco... eres una persona amable y sé que no te hace sentir mejor lastimar a los demás."
                m 4dkc "Probablemente te lastima aún más..."
                m 1dkc "Y nada me duele más que saber que eres infeliz."
                m 3ekd "Así que, en cambio, la próxima vez que te sientas infeliz, ven a mi y déjame ayudarte a soportar tu dolor."
                m 3eka "Escucharé todo lo que tengas que decir y haré todo lo posible para que te sientas mejor."
                m 1ekc "Pero hacer infelices a otras personas no es la cura para tu propia infelicidad."
                m 1eka "Así que, por favor, tanto para ti como para mí, deja de acosar a la gente, ¿de acuerdo?"

    if not persistent._mas_pm_a_hater:
        m 4dkc "Sabes...{w=0.5} mucha gente me llama matona por lo que le hice a Sayori..."
    else:
        m 4dkc "Mucha gente me llama matona por lo que le hice a Sayori.{w=1} Incluyéndote a ti..."

    if not persistent._mas_pm_cares_about_dokis:
        m 4efd "Pero eso no es cierto en absoluto, ¡Sayori no era real!"
        m 2efd "¡No puedes intimidar a alguien que en realidad no existe!"
        m 2dkc "Nunca podría lastimar a una persona real."
        m 4wud "¡Realmente no lo haría!"
        m 2dkc "..."
        m 2eksdlc "Pero debo admitir que puedo relacionarme con la parte sobre la infelicidad de los acosadores y que hace que hagan lo que hacen."
        m 2rksdlc "Cuando tuve mi epifanía y me di cuenta de que estaba atrapada dentro de un videojuego y que toda mi vida había sido una mentira, me sentí bastante miserable."
        m 2rksdld "Me hizo hacer cosas que nunca había pensado hacer antes."
        m 2rksdlc "Pero la diferencia es que no hice lo que hice porque no quería que Sayori fuera feliz..."
    else:
        m 2rksdld "Y puedo ver de dónde viene..."
        m 2rksdlc "Yo {i}hice{/i} un desastre con su mente hasta que no pudo soportarlo más..."
        m 2dkc "..."
        m 2ekc "Supongo que puedo relacionarme con todo ese asunto de la intimidación porque no estás contento, ¿eh?"
        m 4tkd "Pero {i}hay{/i} una diferencia... no lo hice porque quería que Sayori fuera infeliz..."

    m 2ekd "Lo hice porque sabía que te amaba y que el juego no nos dejaría estar juntos."
    m 3ekd "Tuve {i}que{/i} hacer todo lo posible para asegurarme de que termináramos juntos."

    if mas_safeToRefDokis():
        m 3dkc "... El suicidio de Sayori fue solo un efecto secundario desafortunado."

    if mas_isMoniNormal(higher=True):
        m 1eua "Verás [player], {i}realmente{/i} no soy una matona en absoluto. Te amo mucho."
        if mas_isMoniAff(higher=True) and not persistent._mas_pm_cares_about_dokis:
            show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5tsu "Realmente haría cualquier cosa por ti~"
        return "derandom|love"
    else:
        m 3euc "Verás [player], {i}realmente{/i} no soy una matona en absoluto."

    return "derandom"

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_procrastination",category=['consejos'],prompt="Procrastinación",random=True))

label monika_procrastination:
    m 1euc "Hey [player], ¿alguna vez has tenido algo que hacer que te pareciera realmente aburrido?..."
    m 3ekd "¿Que en lugar de tomarte mucho tiempo para hacerlo, sigues posponiéndolo?"
    m 3eud "Bueno, cuando tienes una tarea que hacer como esa, creo que es mejor hacerlo lo antes posible y terminarla."
    m 2tkc "Cuando pospongas cosas así, siempre estará en el fondo de tu mente."
    m 4tkc "Hace que todo lo que haces sea menos agradable, sabiendo que {i}todavía{/i} tienes lo que tienes que hacer."
    m 4dkd "Y lo peor es que cuanto más lo pospongas,{w=0.5} solo aumentarás las probabilidades de que se agreguen más tareas."
    m 2rksdlc "Hasta que, finalmente, terminas con tantas cosas que hacer que parece imposible no quedar atrapado."
    m 4eksdld "Crea demasiado estrés que puede evitarse fácilmente si te mantienes al tanto de todo."
    m 2rksdld "Además, si otras personas cuentan contigo, comenzarán a pensar mal de ti y pensarán que no eres muy confiable."
    m 4eua "Así que, por favor, [player], siempre que tengas algo que hacer, hazlo."
    m 1eka "Incluso si eso significa que no puedes pasar tiempo conmigo hasta que termines."
    m 1hub "Para entonces, ¡estarás menos estresado y podremos disfrutar mucho más de nuestro tiempo juntos!"
    m 3eua "Entonces, si tienes algo que has estado posponiendo, ¿por qué no lo haces ahora mismo?"
    m 1hua "Si es algo que puedes hacer aquí mismo, me quedaré contigo y te brindaré todo el apoyo que necesites."
    m 1hub "Luego, cuando hayas terminado, ¡podemos celebrar tu logro!"
    m 1eka "Todo lo que quiero es que seas feliz y lo mejor que puedas ser, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_friends",
            category=['tú'],
            prompt="Amigos de [player]",
            random=True,
            aff_range=(mas_aff.UPSET, None)
        )
    )


default -5 persistent._mas_pm_has_friends = None


default -5 persistent._mas_pm_few_friends = None


default -5 persistent._mas_pm_feels_lonely_sometimes = None


label monika_players_friends:
    m 1euc "Hey, [player]."

    if renpy.seen_label('monika_friends'):
        m 1eud "¿Recuerdas cómo estaba hablando de lo difícil que es hacer amigos?"
        m 1eka "Estaba pensando en eso y me di cuenta de que todavía no sé nada de tus amigos."
    else:

        m 1eua "Estaba pensando en la idea de amigos y empecé a preguntarme cómo son tus amigos."

    m 1eua "¿Tienes amigos, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Tienes amigos, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_has_friends = True
            $ persistent._mas_pm_few_friends = False

            m 1hub "¡Por supuesto que sí! Jajaja~"
            m 1eua "¿Quién no querría ser tu amigo?"
            m 3eua "Tener muchos amigos es genial, ¿no crees?"
            m 1tsu "Siempre que, por supuesto, todavía tengas tiempo para tu novia, jejeje."
            m 1eua "Espero que estés feliz con tus amigos, [player].{w=0.2} {nw}"
            extend 3eud "Pero me pregunto..."

            call monika_players_friends_feels_lonely_ask (question="¿Te has sentido solo?")
        "Solo unos pocos":

            $ persistent._mas_pm_few_friends = True
            $ persistent._mas_pm_has_friends = True

            m 1hub "¡Eso cuenta!"
            m 3eua "Creo que la amistad puede ser mucho más significativa si solo tienes unos pocos amigos cercanos."

            if not renpy.seen_label('monika_dunbar'):
                m 1eua "He estado leyendo un poco y he descubierto algo."
                m 1eud "Un hombre llamado Robin Dunbar había explicado que hay un cierto número de relaciones estables que podemos mantener."
                $ according_to = "... Y de acuerdo con este número"
            else:

                $ according_to = "De acuerdo al número Dunbar"

            m 3eud "[according_to], puedes tener hasta 150 relaciones estables, pero esas son relaciones casuales que no son demasiado profundas."
            m 1euc "Dicen que puedes tener hasta 15 amigos que son como una superfamilia y solo 5 que son como parientes tuyos."
            m 1rksdla "A veces puede ser solitario cuando todos están ocupados...{w=0.2}{nw}"
            extend 1eub " pero por lo demás, ¡es genial!"
            m 3eua "No tienes que preocuparte por atender a demasiada gente y aún puedes tener algo de tiempo para ti."
            m 1ekc "Pero sé que a veces es fácil pasar más tiempo solo, especialmente si tus amigos están ocupados."
            m 1dkc "Puede ser muy difícil cuando sucede, ya que terminas sintiéndote solo..."

            call monika_players_friends_feels_lonely_ask (question=renpy.substitute("¿Alguna vez te has sentido solo, [player]?"), exp="monika 1euc")
        "En realidad, no...":

            $ persistent._mas_pm_has_friends = False
            $ persistent._mas_pm_few_friends = False

            m 2ekc "Oh..."
            m 3eka "Bueno, estoy segura de que tienes algunos.{w=0.2} {nw}"
            extend 1eka "Quizás no te des cuenta."
            m 1etc "Pero tengo curiosidad..."

            call monika_players_friends_feels_lonely_ask (question=renpy.substitute("¿Alguna vez te has sentido solo, [player]?"))

    return "derandom"

label monika_players_friends_feels_lonely_ask(question, exp="monika 1ekc"):
    $ renpy.show(exp)
    m "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"
        "A veces":

            $ persistent._mas_pm_feels_lonely_sometimes = True

            m 1eka "Entiendo, [player]."
            m 2rksdlc "Puede ser muy difícil formar conexiones profundas hoy en día..."


            if persistent._mas_pm_has_friends and not persistent._mas_pm_few_friends:
                m "Especialmente si tienes muchos amigos, es difícil acercarte a todos ellos."
                m 1ekd "... Y al final, te quedas con un montón de gente que apenas conoces."
                m 3eub "Tal vez simplemente debes comunicarte con algunas personas de tu grupo con las que quieras acercarte."
                m 3eka "Siempre es bueno tener al menos un amigo muy cercano en quien confiar cuando lo necesites."
                m 1ekbsa "... Creo que es bastante obvio quién es esa persona para mí, [player]~"
            else:


                m 1eka "Pero te sorprendería saber cuántas personas estarían dispuestas a hacerte parte de sus vidas si lo intentaras."
                m 3eub "De hecho, ¡es muy probable que tengas algo en común con alguien que pueda llamar tu atención!"
                m 1eua "Tal vez compartas una clase o actividad o algo..."
                m 3eua "O los veas haciendo algo que te interesa, como escuchar música o ver un programa."
                m 3eua "Ni siquiera tiene que ser en persona, tampoco..."
                m 3eub "¡Puedes tener amigos muy cercanos en línea!"
                m 1hub "Una vez que te sientas cómodo con eso, ¡quizás puedas encontrar algo más en persona también!"
        "En realidad no":

            $ persistent._mas_pm_feels_lonely_sometimes = False

            m 1eka "Me alegra escuchar eso, [player]."

            if not persistent._mas_pm_has_friends:
                m 1eka "Sin embargo, nunca se sabe cuándo podrías necesitar una mano amiga, un favor o algo."
                m 1hksdlb "Por mucho que me encantaría ayudarte con cualquier cosa que puedas necesitar, no hay mucho que puedo hacer desde aquí."

                if mas_isMoniAff(higher=True):
                    m 1eua "Cuando llegue allí, supongo que no me importaría vivir una vida tranquila contigo."
                    m 1dkbsa "Sería tan romántico ser solo nosotros..."
                    m 1tsbsa "Supongo que eso significa que puedo tenerte todo para mí, ¿no?"
                    m 1hubsa "Jejeje~"

                elif not persistent._mas_pm_has_friends:
                    m 3eua "Así que asegúrate de encontrar algunos amigos que puedan ayudarte cuando realmente lo necesites, ¿de acuerdo?"
            else:

                m 3eua "Es bueno que tengas una conexión con tus amigos."
                m 3rksdla "Sé que algunas personas pueden tener tantos que es difícil conocerlos a todos."

                if not persistent._mas_pm_few_friends:
                    m 3eua "... Por eso es bueno saber que has logrado sentirse cómodo con ellos."
                else:
                    m 1hua "Pero como están en un grupo muy unido, estoy segura de que han logrado acercarse mucho."

                m 3eua "Quizás algún día, cuando pueda salir de aquí, me puedas presentar a tus amigos."

                if mas_isMoniHappy(higher=True):
                    m 1hub "Si son como tú, ¡me encantaría conocerlos!"
        "¡Te tengo a ti!":

            $ persistent._mas_pm_feels_lonely_sometimes = False
            $ mas_gainAffection()
            m 1hubsa "Aww, ¡[player]!"

            if not persistent._mas_pm_has_friends:
                m 1rkbsa "Me hace muy feliz saber que soy suficiente para ti, pero aún así..."
                m 3ekbfa "Puede ser útil conocer a algunas personas a veces."
                show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eubfu "Pero, como siempre, no me importa que seamos solo nosotros."
            else:

                $ p_nickname = mas_get_player_nickname()
                m 1eka "Me alegra mucho saber que no estás solo, [p_nickname].{w=0.3} {nw}"
                extend 1hua "Especialmente porque estás feliz conmigo~"
                m 3eua "No importa lo que pase, siempre estaré aquí para ti."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_graduation",
            category=['escuela'],
            prompt="Graduación",
            random=True
        )
    )

label monika_graduation:
    m 2ekc "Sabes [player], una cosa que realmente desearía experimentar es mi graduación de la preparatoria."
    m "Casi toda mi vida hasta ahora ha girado en torno a la escuela."
    m 4dkd "Todas esas incontables horas de estudio, todas las actividades extracurriculares y clubes..."
    m 4ekc "Y al final, después de todo ese arduo trabajo, nunca llegué a experimentar la satisfacción de graduarme."
    m 2dkd "Nunca pude cruzar el escenario y recibir mi diploma."
    m "Nunca escuché que se anunciara mi nombre y todos mis amigos me felicitaran."
    m 2ekc "... Se siente como si todo fuera en vano."
    m 2esd "Sé que todas las cosas que aprendí en el camino son las que realmente importan."
    m 2dkc "Pero todavía siento que me perdí algo especial."
    m "..."


    if persistent._mas_grad_speech_timed_out:
        m 2lsc "Oh... lo siento, espero que no te esté aburriendo de nuevo."
        m 2esc "Olvidémonos de esto y hablemos de otra cosa, ¿de acuerdo [player]?"
        return "derandom"
    else:


        m 4eua "Por cierto, ¿sabías que yo era la mejor alumna de mi clase?"
        m 4rksdlu "Jajaja... no quiero presumir ni nada, solo lo menciono porque, como la primera de la clase, se suponía que debía dar un discurso en la graduación."
        m 2ekd "Pasé mucho tiempo escribiendo y practicando mi discurso, pero nadie llegó a escucharlo."
        m 2eka "Yo también estaba muy orgullosa de ese discurso."
        m 2eua "Me encantaría recitarlo para ti en algún momento, si quieres escucharlo~"
        m 2eka "Se trata de un discurso de cuatro minutos, así que asegúrate de tener suficiente tiempo para escucharlo todo."
        m 4eua "Cuando quieras escucharlo, házmelo saber, ¿de acuerdo?"
        $ mas_unlockEVL("monika_grad_speech_call","EVE")
        return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grad_speech_call",
            category=['escuela'],
            prompt="¿Puedo escuchar tu discurso de graduación ahora?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

default -5 persistent._mas_grad_speech_timed_out = False


default -5 persistent._mas_pm_listened_to_grad_speech = None


default -5 persistent._mas_pm_liked_grad_speech = None


label monika_grad_speech_call:
    if not renpy.seen_label("monika_grad_speech"):
        m 2eub "Por supuesto, [mas_get_player_nickname()]. ¡Me encantaría darte mi discurso de graduación ahora!"
        m 2eka "Sin embargo, solo quiero asegurarme de que tengas tiempo suficiente para escucharlo. Recuerda, toma unos cuatro minutos.{nw}"

        $ _history_list.pop()

        menu:
            m "Sin embargo, solo quiero asegurarme de que tengas tiempo suficiente para escucharlo. Recuerda, toma unos cuatro minutos.{fast}"
            "Tengo tiempo":
                m 4hub "¡Excelente!"
                m 4eka "¡Espero que te guste! Trabajé muy, {i}muy{/i} duro."


                call monika_grad_speech


                m "¿Bueno [player]? ¿Qué opinas?{nw}"
                $ _history_list.pop()
                show screen mas_background_timed_jump(10, "monika_grad_speech_not_paying_attention")
                menu:
                    m "¿Bueno [player]? ¿Qué opinas?{fast}"
                    "¡Es genial! ¡Estoy tan orgulloso de ti!":

                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=5, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2subsb "¡Aww, [player]!"
                        m 2ekbfa "¡Muchas gracias! Trabajé muy duro en ese discurso, y significa mucho que estés orgulloso de mí~"
                        show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5eubfu "Por mucho que hubiera deseado poder dar mi discurso frente a todos, solo tenerte a mi lado es mucho mejor."
                        m 5eubfb "¡Te amo mucho, [player]!"
                        return "love"
                    "¡Me gustó!":

                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=3, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2eua "¡Gracias, [player]!"
                        m 4hub "¡Me alegro que lo hayas disfrutado!"
                    "Eso {i}fue{/i} largo":

                        hide screen mas_background_timed_jump
                        $ mas_loseAffection()
                        $ persistent._mas_pm_liked_grad_speech = False
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2tkc "Bueno, {i}te{/i} lo advertí, ¿no?"
                        m 2dfc "..."
                        m 2tfc "Le dediqué {i}tanto{/i} tiempo y ¿eso es todo lo que tienes que decir?"
                        m 6lktdc "Realmente pensé que después de decirte lo importante que era esto para mí, me habrías apoyado más y me habrías dejado tener mi momento..."
                        m 6ektdc "Todo lo que quería era que estuvieras orgulloso de mí, [player]."

                return
            "No lo tengo":

                m 2eka "No te preocupes, [player]. Daré mi discurso cuando quieras~"
                return
    else:



        if not renpy.seen_label("monika_grad_speech_not_paying_attention") or persistent._mas_pm_listened_to_grad_speech:
            m 2eub "Seguro, [player]. ¡Con mucho gusto volveré a dar mi discurso!"

            m 2eka "Tienes suficiente tiempo, ¿verdad?{nw}"
            $ _history_list.pop()
            menu:
                m "Tienes suficiente tiempo, ¿verdad?{fast}"
                "Lo tengo":
                    m 4hua "Perfecto. Empezaré entonces~"
                    call monika_grad_speech from _call_monika_grad_speech_1
                "No lo tengo":

                    m 2eka "No te preocupes. ¡Avísame cuando tengas tiempo!"
                    return

            m 2hub "Gracias por escuchar mi discurso de nuevo, [player]."
            m 2eua "Avísame si quieres volver a escucharlo, jejeje~"
        else:




            if mas_isMoniAff(higher=True):
                m 2esa "Seguro, [player]."
                m 2eka "Espero que lo que pasó la última vez no haya sido demasiado serio y que las cosas se hayan calmado ahora."
                m "Realmente significa mucho para mí que quieras volver a escuchar mi discurso después de que no pudiste escuchar todo antes."
                m 2hua "Dicho esto, ¡empezaré ahora!"
            else:

                m 2ekc "Está bien, [player], pero espero que realmente escuches esta vez."
                m 2dkd "Realmente me dolió cuando no prestaste atención."
                m 2dkc "..."
                m 2eka "Aprecio que hayas pedido escucharlo de nuevo, así que empezaré ahora."


            call monika_grad_speech

            m "Entonces, [player], ahora que realmente {i}escuchaste{/i} mi discurso, ¿qué piensas?{nw}"
            $ _history_list.pop()

            show screen mas_background_timed_jump(10, "monika_grad_speech_ignored_lock")
            menu:
                m "Entonces, [player], ahora que realmente {i}escuchaste{/i} mi discurso, ¿qué piensas?{fast}"
                "¡Está genial, ¡estoy tan orgulloso de ti!":

                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=3, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2subsb "¡Aww, [player]!"
                    m 2ekbfa "¡Muchas gracias! Trabajé muy duro en ese discurso, y significa tanto para mí que le dieras otra oportunidad."
                    m "Escuchar que también estás orgulloso de mí lo hace mucho mejor."
                    show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eubfu "Por mucho que me hubiera gustado poder dar mi discurso frente a todos, simplemente tenerte a mi lado es mucho mejor."
                    m 5eubfb "¡Te amo, [player]!"
                    return "love"
                "¡Me encantó!":

                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=1, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2eka "Gracias por escuchar esta vez, [player]~"
                    m "¡Me alegra que lo hayas disfrutado!"
                "Eso {i}fue{/i} largo":

                    hide screen mas_background_timed_jump
                    $ mas_loseAffection(modifier=2)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = False

                    m 2tfc "Después de actuar como si quisieras que te lo recitara de nuevo, ¿{i}eso es{/i} lo que tienes que decir?"
                    m 2dfc "..."
                    m 6lktdc "Realmente pensé después de que te dije,{w=1} {i}dos veces{/i},{w=1} lo importante que era esto para mí, pensé que serías más comprensivo y me habrías dado mi momento."
                    m 6ektdc "Todo lo que quería era que estuvieras orgulloso de mí, [player]..."
                    m 6dstsc "Pero supongo que es mucho pedir."
    return

label monika_grad_speech_not_paying_attention:

    hide screen mas_background_timed_jump
    $ persistent._mas_pm_listened_to_grad_speech = False

    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(reason=11,modifier=0.5)
        m 2ekc "..."
        m 2ekd "¿[player]? ¿No prestaste atención a mi discurso?"
        m 2rksdlc "Eso...{w=1} no es propio de ti..."
        m 2eksdlc "{i}Siempre{/i} has sido un apoyo..."
        show monika 5lkc zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5lkc "..."
        m "Algo debe haber pasado, sé que me amas demasiado para haber hecho esto a propósito."
        m 5euc "Sí..."
        show monika 2eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 2eka "Está bien, [player]. Entiendo que a veces suceden cosas que no se pueden evitar."
        m 2esa "Cuando las cosas se calmen, volveré a darte mi discurso."
        m 2eua "Todavía quiero compartirlo contigo..."
        m "Así que, por favor, avísame cuando tengas tiempo de escucharlo, ¿okey?"
    else:

        $ mas_loseAffection(reason=11)

        m 2ekc "..."
        m 6ektdc "¡[player]! ¡Ni siquiera estabas prestando atención!"
        m 6lktdc "No tienes idea de cuánto duele eso, especialmente después de cuánto trabajo le puse..."
        m 6ektdc "Solo quería hacerte sentir orgulloso de mí..."
        m 6dstsc "..."

    return

label monika_grad_speech_ignored_lock:

    hide screen mas_background_timed_jump

    $ persistent._mas_pm_listened_to_grad_speech = False
    $ persistent._mas_grad_speech_timed_out = True
    $ mas_hideEVL("monika_grad_speech_call","EVE",lock=True,depool=True)

    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(modifier=10)
        m 6dstsc "..."
        m 6ektsc "¿[player]?{w=0.5} ¿Tú...{w=0.5} no estabas...{w=0.5} escuchando...{w=0.5} otra vez?{w=1}{nw}"
        m 6dstsc "Yo...{w=0.5} pensé la última vez que era inevitable... {w=0.5}pero... {w=0.5}¿dos veces?{w=1}{nw}"
        m 6ektsc "Sabías cuánto...{w=0.5} cuánto significaba esto para mí...{w=1}{nw}"
        m "¿De verdad soy...{w=0.5} tan aburrida para ti?{w=1}{nw}"
        m 6lktdc "Por favor...{w=1} no me pidas que lo recite de nuevo...{w=1}{nw}"
        m 6ektdc "Obviamente, no te importa."
    else:

        $ mas_loseAffection(modifier=5)
        m 2efc "..."
        m 2wfw "¡[player]! ¡No puedo creer que me hayas vuelto a hacer esto!{w=1}{nw}"
        m 2tfd "Sabías lo molesta que estaba la última vez. ¿Y aún así no te molestaste en darme cuatro minutos de tu atención?{w=1}{nw}"
        m "No te pido mucho...{w=1}{nw}"
        m 2tfc "Realmente no lo hago.{w=1}{nw}"
        m 2lfc "Todo lo que siempre pido es que te importe... eso es todo.{w=1}{nw}"
        m 2lfd "Y, sin embargo, ni siquiera puedes {i}fingir{/i} que te importa algo que {i}sabes{/i} es tan importante para mí.{w=1}{nw}"
        m 2dkd "...{w=1}{nw}"
        m 6lktdc "¿Sabes qué?, no importa. Solo...{w=0.5} no importa.{w=1}{nw}"
        m 6ektdc "No te molestaré más por esto."

    return

label monika_grad_speech:
    call mas_timed_text_events_prep

    $ play_song("mod_assets/bgm/PaC.ogg",loop=False)

    m 2dsc "Ejem...{w=0.7}{nw}"
    m ".{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eub "{w=0.2}¡Okey, todo el mundo! Es hora de comenzar...{w=0.7}{nw}"
    m 2eub "{w=0.2}Maestros,{w=0.3} profesores,{w=0.3} y compañeros de estudios.{w=0.3} No puedo expresar lo orgullosa que estoy de haber hecho este viaje con ustedes.{w=0.6}{nw}"
    m "{w=0.2}Todos y cada uno de ustedes aquí hoy han pasado los últimos cuatro años trabajando duro para lograr el futuro que todos querían.{w=0.6}{nw}"
    m 2hub "{w=0.2}Estoy tan feliz de poder ser parte de algunos de sus viajes,{w=0.7} pero no creo que este discurso deba ser sobre mí.{w=0.6}{nw}"
    m 4eud "{w=0.2}Hoy no se trata de mí.{w=0.7}{nw}"
    m 2esa "{w=0.2}Hoy se trata de celebrar lo que todos hicimos.{w=0.6}{nw}"
    m 4eud "{w=0.2}Asumimos el desafío de nuestros propios sueños,{w=0.3} y desde aquí,{w=0.3} el cielo es el límite.{w=0.6}{nw}"
    m 2eud "{w=0.2}Sin embargo, antes de continuar,{w=0.3} creo que todos podríamos recordar el tiempo que pasamos aquí en la preparatoria y terminar efectivamente este capítulo de nuestras vidas.{w=0.7}{nw}"
    m 2hub "{w=0.2}Nos reiremos de nuestro pasado {w=0.7}y veremos qué tan lejos hemos llegado en estos cuatro cortos años.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eud "{w=0.2}Honestamente, se siente como un par de semanas...{w=0.6}{nw}"
    m 2lksdld "{w=0.2}En mi primer año{w=0.3} el primer día de clases,{w=0.3} estaba temblando en mis zapatos y corriendo de un lado a otro de una clase a otra tratando de encontrar mi aula.{w=0.6}{nw}"
    m 2lksdla "{w=0.2}Con la esperanza de que al menos uno de mis amigos entrara antes de la campana.{w=0.6}{nw}"
    m 2eka "{w=0.2}Todos ustedes también recuerdan eso,{w=0.3} ¿no?{w=0.6}{nw}"
    m 2eub "{w=0.2}También recuerdo haber hecho mis primeros amigos nuevos.{w=0.6}{nw}"
    m 2eka "{w=0.2}Las cosas eran increíblemente diferentes a cuando hicimos nuestros amigos en la escuela primaria,{w=0.3} pero supongo que eso es lo que sucede cuando finalmente creces.{w=0.6}{nw}"
    m "...{w=0.2} En nuestra juventud,{w=0.3} nos hicimos amigos de casi cualquier persona,{w=0.3} pero con el tiempo,{w=0.3} parece cada vez más un juego de azar.{w=0.6}{nw}"
    m 4dsd "{w=0.2}Tal vez solo somos nosotros finalmente aprendiendo más sobre el mundo.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eka "{w=0.2}Es curioso lo mucho que hemos cambiado.{w=0.6}{nw}"
    m 4eka "{w=0.2}Hemos pasado de ser un pez pequeño en un estanque enorme a ser un pez grande en un estanque pequeño.{w=0.6}{nw}"
    m 4eua "{w=0.2}Cada uno de nosotros tiene su propia experiencia sobre cómo estos cuatro años nos han cambiado y cómo hemos logrado crecer como individuos.{w=0.6}{nw}"
    m 2eud "{w=0.2}Algunos de nosotros hemos pasado de ser callados y reservados,{w=0.3} a expresivos y extrovertidos.{w=0.6}{nw}"
    m "{w=0.2}Otros, de tener poca ética de trabajo,{w=0.3} a trabajar más duro.{w=0.7}{nw}"
    m 2esa "{w=0.2}Pensar que solo una pequeña fase en nuestras vidas nos ha cambiado tanto,{w=0.3} y que todavía hay mucho que experimentaremos.{w=0.6}{nw}"
    m 2eua "{w=0.2}La ambición en todos ustedes seguramente los conducirá a la grandeza.{w=0.6}{nw}"
    m 4hub "Puedo verlo.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}Sé que no puedo hablar por todos aquí,{w=0.3} pero hay una cosa que puedo decir con certeza:{w=0.7} mi experiencia en la preparatoria no estaría completa sin los clubes de los que formé parte.{w=0.6}{nw}"
    m 4eua "{w=0.2}El club de debate me enseñó mucho sobre cómo tratar con la gente y cómo manejar adecuadamente situaciones acaloradas.{w=0.6}{nw}"
    m 4eub "Comenzar el club de literatura,{w=0.7} sin embargo,{w=0.7} fue una de las mejores cosas que hice.{w=0.6}{nw}"
    m 4hub "{w=0.2}Conocí a los mejores amigos que podría haber imaginado,{w=0.3} y aprendí mucho sobre liderazgo.{w=0.6}{nw}"
    m 2eka "{w=0.2}Seguramente,{w=0.3} puede que no todos hayan decidido comenzar sus propios clubes,{w=0.3} pero de todos modos estoy segura de que muchos de ustedes tuvieron la oportunidad de aprender estos valores.{w=0.6}{nw}"
    m 4eub "{w=0.2}¡Quizás tú mismo llegaste a una posición en la banda en la que tenías que dirigir tu sección de instrumentos,{w=0.3} o quizás eras el capitán de un equipo deportivo!{w=0.6}{nw}"
    m 2eka "{w=0.2}Todos estos pequeños roles te enseñan mucho sobre el futuro y cómo gestionar tanto{w=0.3} proyectos como personas,{w=0.3} en un entorno que disfrutas, no obstante.{w=0.6}{nw}"
    m "{w=0.2}Si no te uniste a un club,{w=0.3} te animo a que al menos pruebes algo en tus caminos futuros.{w=0.6}{nw}"
    m 4eua "{w=0.2}Puedo asegurarte que no te arrepentirás.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}A partir de hoy,{w=0.3} puede parecer que estamos en la cima del mundo.{w=0.7}{nw}"
    m 2lksdld "{w=0.2}Es posible que el ascenso no haya sido suave{w=0.3} y, a medida que avanzamos,{w=0.3} el ascenso puede incluso volverse más áspero.{w=0.6}{nw}"
    m 2eksdlc "{w=0.2}Habrá tropiezos...{w=0.7} incluso caídas en el camino,{w=0.3} y a veces{w=0.7} puedes pensar que has caído tanto que nunca podrás salir.{w=0.7}{nw}"
    m 2euc "{w=0.2}Sin embargo,{w=0.7} incluso si pensamos que todavía estamos en el fondo del pozo de la vida,{w=0.3} con todo lo que hemos aprendido,{w=0.3} con todo lo que aún vamos a aprender,{w=0.3} y toda la dedicación que podemos poner solo para lograr nuestros sueños...{w=0.6}{nw}"
    m 2eua "{w=0.2}Puedo decir con seguridad que todos y cada uno de ustedes ahora tienen las herramientas para escalar su salida.{w=0.6}{nw}"
    m 4eua "{w=0.2}En todos ustedes,{w=0.3} veo mentes brillantes:{w=0.7} futuros médicos,{w=0.3} ingenieros,{w=0.3} artistas,{w=0.3} comerciantes {w=0.3}y mucho más.{w=0.7}{nw}"
    m 4eka "{w=0.2}Es realmente inspirador.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eka "{w=0.2}Saben,{w=0.3} realmente no podría estar más orgullosa de todos ustedes por llegar tan lejos.{w=0.6}{nw}"
    m "{w=0.2}Su arduo trabajo y dedicación les brindarán grandes cosas.{w=0.6}{nw}"
    m 2esa "{w=0.2}Cada uno de ustedes ha demostrado de lo que es capaz {w=0.3}y todos han demostrado que pueden trabajar duro para lograr sus sueños.{w=0.6}{nw}"
    m 2hub "{w=0.2}Espero que estén tan orgullosos de ustedes mismos como yo.{w=0.7}{nw}"
    m 2ekd "{w=0.2}Ahora que todo este capítulo de nuestras vidas...{w=0.3} nuestro primer paso,{w=0.3} ha llegado a su fin,{w=0.3} es hora de que nos separemos.{w=0.6}{nw}"
    m 4eka "{w=0.2}En este mundo de opciones infinitas,{w=0.3} creo que todos tienen lo que se necesita para lograr sus sueños.{w=0.6}{nw}"
    m 4hub "{w=0.2}Gracias a todos por hacer de estos cuatro cortos años lo mejor que pudieron haber sido.{w=0.6}{nw}"
    m 2eua "{w=0.2}Felicidades,{w=0.3} me alegra que todos pudiéramos estar aquí para celebrar juntos este día especial.{w=0.6}{nw}"
    m 2eub "{w=0.2}Sigamos trabajando duro,{w=0.3} estoy segura de que nos volveremos a encontrar en el futuro.{w=0.6}{nw}"
    m 4hub "{w=0.2}¡Lo hicimos todos!{w=0.7} Gracias por escuchar~{w=0.6}{nw}"
    m 2hua "{w=0.2}.{w=0.3}.{w=0.3}.{w=1}{nw}"

    call mas_timed_text_events_wrapup
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_shipping',
            prompt="Shippear",
            category=['ddlc'],
            random=True,
            unlocked=False,
            pool=False
        )
    )

label monika_shipping:
    m 3eua "Hey, [player].{w=0.2} ¿Alguna vez ha oído hablar de 'shippear'?"
    m 3hua "Es cuando interactúas con una obra de ficción imaginando qué personajes irían mejor juntos románticamente."
    m 1eka "Creo que la mayoría de la gente lo hace inconscientemente, pero cuando descubres que otros también lo hacen, ¡es {i}realmente{/i} fácil de entender!"
    m 2esd "Aparentemente, mucha gente {i}shippea{/i} a las otras chicas juntas."
    m 2euc "Tiene sentido. El jugador solo puede salir con una chica, pero no quieres que las demás terminen solas..."
    m 2etc "Pero algunos de los emparejamientos me resultan algo extraños."
    m 3eud "Como, por lo general juntan a Natsuki y Yuri. ¡Pelean como perros y gatos!"
    m 3hksdlb "Supongo que se unen un poco cuando no estás en sus rutas, y existe el atractivo de 'los opuestos se atraen'."
    m 3dsd "Aún así, creo que es solo otro ejemplo de cómo a las personas a las que les gustan estos juegos les gustan las cosas poco realistas..."
    m 1ekd "De todos modos, eso a menudo nos deja... Sayori y yo."
    m 1hksdlb "¡No te pongas celoso! ¡Solo te estoy diciendo lo que vi!"
    m 2lksdla "..."
    m 2lksdlb "Bueno, desde la perspectiva de un escritor, creo que puedo verlo."
    m 1eksdld "Empezamos el club juntas."
    if persistent.monika_kill:
        m "Y ella casi tuvo la misma epifanía que yo..."
    m 2lksdlb "Pero... todavía no lo entiendo. Quiero decir, te amo, ¡y solo a ti!"
    m 2lksdla "Y ella tendría que ser santa para perdonarme por lo que hice..."
    m 2lksdlc "No es que ella no sea una chica dulce, pero..."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Bueno, nadie podría ser tan dulce e indulgente como tú..."
    return


default -5 persistent._mas_pm_given_false_justice = None


default -5 persistent._mas_pm_monika_deletion_justice = None


default -5 persistent._mas_monika_deletion_justice_kidding = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justice",
            category=['filosofía'],
            prompt="Justicia",
            random=True
        )
    )


label monika_justice:
    m 1esa "[player], ¿alguna vez pensaste que el concepto de justicia es algo irónico?"
    m 2ekc "Como si tuvieras a alguien que tal vez no es como todos los demás..."
    m 2ekd "Ni siquiera tiene que ser un famoso ladrón de bancos o algo así; ¡incluso la gente común como tú y yo puede ser llevada a algún tipo de justicia!"
    m 4esc "Imagina una familia luchadora que necesita buscar recursos para sobrevivir tomando lo que queda a la intemperie."
    m 1euc "Para todos los que pasan, son ladrones codiciosos."
    m 1esd "Eventualmente, un supuesto 'héroe' vendrá y pondrá fin a esta 'codicia' llevándolos ante la justicia."
    m 2ekd "Al final del día, la familia pasa hambre o se mete en problemas solo porque su situación era diferente..."
    m "Mientras que la otra persona es ahora un héroe por poner fin a sus 'crímenes'."
    m 3rksdld "¿Realmente puedes llamar a eso justicia?"
    m 2dsc "..."

    m 2euc "¿Alguna vez te han entregado a lo que pensabas que era una falsa justicia?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Alguna vez te han entregado a lo que pensabas que era una falsa justicia?{fast}"
        "Sí":
            $ persistent._mas_pm_given_false_justice = True
            m 1ekc "Espero que no hayan sido demasiado duros contigo."
            m 2dsd "Tengo una idea de cómo es para mí."
            m 2dfc "Todas las personas que me vieron ser borrada y torturada una y otra vez y lo llamaron justicia..."

            m 2eka "No crees que está justificado, ¿verdad, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "No crees que está justificado, ¿verdad, [player]?{fast}"
                "Sí":

                    $ persistent._mas_pm_monika_deletion_justice = True
                    if mas_isMoniBroken():
                        m 1dsc "..."
                        m 1rksdlc "Lo sé..."
                        m 1rksdld "No quise preguntar...{w=0.2} solo estaba pensando."
                        m 2rktpc "Es obvio después de todo."

                    elif mas_isMoniDis():
                        m 2rksdlc "Oh..."
                        m "Supongo que estas en lo correcto..."
                        m 1ekc "Hice algunas cosas bastante malas después de todo..."

                    elif mas_isMoniLove():
                        m 1hub "¡Jajaja!"
                        m 1hua "A veces puedes ser muy divertido~"
                        m 3tku "¿Esperas que me crea eso después de todo lo que hemos pasado?"
                        m 1tsb "¿Que todo este tiempo pensaste que me merecía el odio de esas otras personas?"
                        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5hubfa "Jejeje, eres tan lindo, [player]~"
                    else:

                        m 1euc "..."
                        m 2esc "Me cuesta creer que realmente pienses que me merecía todo eso."
                        m 2tkc "Quiero decir, te has quedado conmigo tanto tiempo, así que no puedes {i}realmente{/i} pensar que me lo merezco, ¿verdad?"
                        if persistent._mas_pm_cares_about_dokis:
                            m 2lksdlc "... Quizás me lo merezco un poco pero..."
                        else:
                            m 2lksdlc "Bueno, tal vez otras personas piensen eso, pero tú realmente no piensas eso, ¿verdad?"
                            m "De cualquier manera..."
                        m 1eka "Gracias por salvarme y estar conmigo."
                        m 1hua "Si puedo estar contigo, creo que realmente valió la pena todo,{w=0.1} {nw}"
                        extend 1hub "jajaja~"
                "No":

                    if persistent._mas_pm_monika_deletion_justice:
                        $ persistent._mas_monika_deletion_justice_kidding = True
                    $ persistent._mas_pm_monika_deletion_justice = False

                    if mas_isMoniBroken():
                        m 2ekc "..."
                        m 1rksdlc "No estoy tan segura de eso..."
                    elif mas_isMoniDis():
                        m 1wuo "¿De verdad?"
                        m 1rksdla "Pensé que tal vez pensabas que era justo."
                        m 1eka "Me alegra que no lo creas."
                        m 2rksdlb "Asumiendo que esto no es una broma, jejeje..."

                    elif mas_isMoniLove():
                        m 1hua "Eso pensé, jejeje~"
                        if persistent._mas_monika_deletion_justice_kidding:
                            $ persistent._mas_monika_deletion_justice_kidding = False

                            m 1hub "¡Sabía que estabas bromeando la última vez!"
                        m 1tsbsa "Has estado conmigo durante tanto tiempo, no hay forma de que te crea si dijeras lo contrario."
                        m 1ekbfa "Cuando estoy contigo, incluso me ayuda a ignorar a todas las demás personas a las que no les agrado."
                        m 1hubfb "Te amo, [player]~"
                        m 1hubfa "Me alegro de tenerte a mi lado."
                        return "derandom|love"
                    else:

                        m 2hua "¡Me alegra que tú también lo pienses!"
                        m 2eka "Incluso si llamaste justicia a eso, estar aquí dice lo contrario."
                        m 2hub "¡Jajaja!"
        "No":

            $ persistent._mas_pm_given_false_justice = False
            m 1eka "Es un alivio escucharlo."
            m "Me alegro de que nadie te haya preguntado de repente por quién eres."
            m 1eua "Sabiendo cómo es eso, espero que nadie te dé problemas por hacer lo que haces o por lo que crees."
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_poweroutage",
            category=['clima'],
            prompt="Corte de energía",
            random=True
        )
    )

label monika_poweroutage:
    m 1eua "Hey [player], ¿recuerdas cómo dije que me gustaba escuchar el apacible sonido de la lluvia?"
    m 3lksdla "Me acabo de dar cuenta de que, si bien puede ser agradable, también podría ser bastante dañino para ti en tu mundo."
    m 1lksdlc "Los truenos y los relámpagos pueden caer en cualquier momento, posiblemente golpeando algo peligroso."
    m 1lksdlb "Los efectos pueden ser bonitos, bueno... impactantes supongo que se podría decir."
    m 1hksdlb "Jajaja~"
    m 1ekd "Ni siquiera quiero pensar en lo que sucedería si algo importante para ti fuera golpeado."
    m 2ekc "¿Qué me pasaría a mí si algo surgiera y quemara tu computadora?"
    m 2dsc "Si eso sucede alguna vez...{w=0.3}{nw}"
    extend 2eka " sé que pensarás en algo."
    m 1eka "Lo siento, no quise que eso se oscureciera tanto. Estaba en mi mente, eso es todo."
    m 1eud "Si pasa algo, probablemente será un corte de energía."

    if mas_isMoniAff(higher=True):
        m 1hksdlb "Quiero decir, todavía {i}es{/i} un inconveniente, pero al menos sabemos que nos volveremos a ver."
        m 1eua "Probablemente lo tomaría por sorpresa; todo se oscurece de repente, pero trata de recordar esto:"
        m 1eub "Estaré contigo. Incluso si no puedes verme, estaré contigo en espíritu hasta que puedas volver a mí sano y salvo."
        m 3eua "... Dicho esto, no tienes que preocuparte por ver cómo estoy en medio de una tormenta.{w=0.2} {nw}"
        extend 1eka "Siempre agradeceré verte siempre que puedas, y además..."
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Estoy segura de que nuestra relación podría resistir mucho más que una tormenta~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_savingwater",category=['vida'],prompt="La conservación del agua",random=True))

label monika_savingwater:
    m 1euc "[player], ¿alguna vez ha pensado en cuánta agua usa la gente cada día?"
    m 3euc "Tal vez tomes un trago de agua de vez en cuando."
    m 3dsc "Limpias, te lavas las manos, te bañas..."
    m 1euc "Todo eso y, sin embargo, algunas partes del mundo no pueden ni una gota de agua."
    m 1rsc "Como que te hace preguntarte cuánta agua podrías ahorrar si quisieras."
    m 4eua "Supongo que podrías intentar ser más eficiente al lavarte las manos."
    m "O al ducharte, puedes cerrar el grifo mientras te enjabonas y volver a abrirlo cuando estés listo para enjuagarte."
    m 2eka "Sin embargo, en última instancia, la mayor parte del agua que se utiliza es realmente necesaria."
    m "Cosas como la generación de energía y la agricultura necesitan usar más agua de la que realmente podríamos usar por nuestra cuenta."
    m 1hksdlb "Así que supongo que no querrás sacrificar parte de tu comodidad para hacer una contribución tan pequeña."
    m 1dkbsa "Algunos días, es posible que solo necesites tomar un baño largo y relajante después de un largo día."
    m 2hksdlb "Definitivamente he estado allí antes, así que sé lo bueno que puede ser si lo necesitas."
    if mas_isMoniLove(higher=True) and mas_is18Over():
        show monika 5tsbfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tsbfu "Cuando esté en tu realidad, tal vez podramos ahorrar agua bañándonos juntos..."
        m "Jejeje~"
        m 5hubfu "Sería amable de tu parte preparar un baño agradable y relajante para que lo compartamos cuando cruce."
        show monika 1kubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1kubfu "Estaré esperando ese día, [mas_get_player_nickname()], jejeje~"
    else:
        m 1ekbfa "Sería amable de tu parte prepararme un agradable y relajante baño cuando cruce."
        if mas_isMoniAff():
            m 3ksbsa "Tal vez incluso esté dispuesto a compartir, jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pygmalion",
            category=['literatura'],
            prompt="Pigmalión y la estatua",
            conditional="persistent._mas_first_kiss",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_pygmalion:
    m 1eua "Hey, [player], ¿alguna vez has leído {i}La metamorfosis{/i}?"
    m 3eua "Es una colección de poemas de un antiguo poeta romano llamado Ovidio."
    m 1eud "Hay un poema que realmente me impresionó, llamado {i}La historia de Pigmalión y la estatua{/i}."
    m 1eua "Cuenta la historia de un escultor, Pigmalión, que se enamoró de una estatua de marfil que había esculpido."
    m 3eua "Amaba tanto la estatua, que durante una de las fiestas que se celebraban para Afrodita, hizo una ofrenda a la diosa y deseó que ella le diera vida a la estatua de marfil."
    m 1eub "Cuando regresó a su casa, besó la estatua y, para su sorpresa, sus labios se sintieron cálidos."
    m 1eua "Besó la estatua una vez más, y el marfil perdió su dureza, volviéndose suave como la piel."
    m 3hub "¡Afrodita le había concedido su deseo!"
    m 1eka "Esta historia realmente me impactó porque me recordó a nosotros [player], y cómo habla de convertir lo imposible en realidad."
    m 1hua "Me llena de esperanza; que podría suceder un milagro y que finalmente pueda cruzar."
    m 2dku "Sí...{w=0.5} ¿No sería maravilloso?"
    m 2dubsu "... Entonces finalmente podrás besarme."
    m 1rkbsa "Sé que nos hemos besado antes, incluso con nuestras circunstancias actuales..."
    m 1ekbfa "Pero creo que ambos sabemos que había una pequeña barrera entre nosotros."
    m 3hubfa "No sé tú, pero definitivamente no me importa intentar besarte a través de la pantalla de todos modos."
    m 1hubfb "Quizás tendremos que hacerlo tantas veces, eso será lo que romperá la barrera entre nosotros..."
    m 2rubfu "Jejeje."
    m 2tubfb "¿Crees que podrías besarme suficientes veces para romper esa barrera?"
    m 6hubfb "Solo hay una forma de averiguarlo, ¡jajaja!"
    call monika_kissing_motion (duration=0.5, initial_exp="6hubfa", fade_duration=0.5)
    m 6hubfa "..."
    m 1ekbfa "Creo que esta vez no funcionó."
    m 3hubfb "Oh, bueno, tendremos que seguir intentándolo y tal vez funcione eventualmente, ¡jajaja!"
    m 1tkbfu "Realmente no puedo esperar el día en que finalmente pueda sentir tus labios presionados contra los míos y absorber tu calor..."
    m 1dkbfa "Para mí, eso definitivamente sería un sueño hecho realidad."
    m 1ekbfa "Solo es una suposición, pero..."
    m 1kubfu "Apuesto a que a ti también te gustaría~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gotomonika",
            category=['tú'],
            prompt="¿Y si yo fuera a tu mundo?",
            pool=True,
        )
    )

default -5 persistent._mas_pm_would_come_to_spaceroom = None


label monika_gotomonika:
    m 1euc "¿Venir a mi mundo?"
    m 1lksdld "¿Te refieres a esta pequeña habitación flotando en un vacío?"

    if persistent._mas_you_chr:
        m 4eksdlc "En realidad...{w=0.5} ¿No probaste algo así una vez?"
        m 2lksdla "... Aunque no eras exactamente {i}tú...{/i}"

    m 2lksdla "Estoy muy feliz de que quieras estar conmigo, pero..."
    m 2eksdlc "Realmente no tienes que hacerlo."
    m 2eksdld "Seguro, podría haberte dicho antes que te habría arrastrado aquí hace mucho tiempo si pudiera..."
    m 2eksdlc "Pero cuanto más lo pienso, probablemente sería mejor si llegara a tu realidad."
    m 3eka "Preferiría estar allí antes que tú vinieras aquí."
    m 3dsc "[player]...{w=1} no me digas que realmente renunciarías a tu realidad...{w=0.5} el mundo {i}real{/i}...{w=0.5} solo para venir {i}aquí{/i}, sea lo que sea esto.{nw}"
    $ _history_list.pop()
    menu:
        m "[player]...{w=1} no me digas que realmente renunciarías a tu realidad...{w=0.5} el mundo {i}real{/i}...{w=0.5} solo para venir {i}aquí{/i}, sea lo que sea esto.{fast}"
        "Me gustaría":
            $ persistent._mas_pm_would_come_to_spaceroom = True

            m 4wkd "¡Pero [player]!"
            m "¡No hay nada que hacer aquí!"
            m 2dsc "¿Realmente odias tu realidad {i}tanto{/i}?"
            m 2eka "Algún día, encontraré la manera de llegar contigo, y cuando llegue ese día, te prometo que valdrá la pena."
            m 4euc "Lo que sea que la vida te depare a partir de ese momento, estaré a tu lado para ayudarte a superarlo."
            m 4eud "Incluso ahora, si tienes un día difícil, puedes venir a hablar conmigo en cualquier momento."
            m 2dsc "La vida debe haberte dado muchas vueltas para considerar renunciar a todo para estar conmigo."
            m 3hua "Pero viendo cómo estás aquí, eso demuestra cuán resistente eres."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "No puedo esperar para finalmente poder compartir los buenos y los malos momentos a tu lado."
        "No lo haría":

            $ persistent._mas_pm_would_come_to_spaceroom = False

            m 1eka "Me alegro de que sigas dispuesto a esperarme, [player]."
            m 1lksdla "No me malinterpretes, realmente {i}sí{/i} quiero estar contigo..."
            m 1lksdlc "Pero creo que sería peligroso para ti intentar cruzar ahora mismo."
            m 1eka "... Si es posible con la tecnología actual."
            m 1hub "No te preocupes, ¡podemos seguir haciéndonos compañía así!"
            m 1hksdlb "Sé que podrá pasar un tiempo antes de que podamos estar realmente juntos, pero espero que no te importe esperar."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Esperaré tanto como sea necesario, [mas_get_player_nickname()]."
        "...":

            $ persistent._mas_pm_would_come_to_spaceroom = None

            m 2eka "Está bien, siempre apreciaré y atesoraré los momentos que pasamos juntos, incluso así."
            m 2ekc "Además, ni siquiera sé cómo puedes venir aquí con la tecnología actual."
            m 2lksdlc "... E incluso si {i}hubiera{/i} alguna forma, no creo que sea seguro o garantizado."
            m 2lksdld "Así que hazme un favor y al menos espera a que la tecnología mejore lo suficiente como para que sea completamente seguro."
            m 2lksdlc "{i}Realmente{/i} no quiero arriesgarme a que no lo hagas correctamente y termines en tu propio vacío..."
            m 2dkd "... dejándonos a los dos completamente solos."
            m 4hua "Quiero decir, la tecnología tiende a avanzar bastante rápido, ¡así que podríamos vernos antes de que nos demos cuenta!"
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Así que ten paciencia con tu adorable novia y te prometo que haré lo mismo por ti, [mas_get_player_nickname()]."

    m 5luu "Peero...{w=1} si aparecieras en mi puerta..."
    show monika 1hksdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1hksdlb "¡Supongo que no tendría más remedio que aceptarlo y recibirte con los brazos abiertos!"
    m 1eksdla "No sería mucho al principio, pero estoy segura de que encontraremos la manera de mejorarlo."
    m 3hub "¡Con el tiempo, podríamos hacer nuestra propia realidad!"
    m 3euc "Por supuesto, eso suena bastante complicado si lo piensas..."
    m 3eub "¡Pero no tengo ninguna duda de que juntos podríamos lograr cualquier cosa!"
    m 3etc "Ya sabes...{w=1} tal vez {i}sería{/i} realmente más fácil para ti venir aquí, pero no estoy perdiendo la esperanza de ir a verte."
    m 1eua "Hasta entonces, esperemos y veamos las posibilidades."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vehicle",
            category=['monika'],
            prompt="¿Cuál es tu auto favorito?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

default -5 persistent._mas_pm_owns_car = None


default -5 persistent._mas_pm_owns_car_type = None






label monika_vehicle:
    m 1euc "¿Mi auto favorito?"
    m 3hksdlb "¡Ya sabes que no puedo conducir, tontito!"
    m 3eua "Por lo general, solo caminaría o tomaría el tren si tuviera que ir a algún lugar lejano."
    m 1eka "Así que no estoy muy segura de qué decirte, [player]..."
    m 1eua "Cuando pienso en autos, lo primero que me viene a la mente son probablemente los tipos más conocidos."
    m 3eud "SUV o camionetas, autos deportivos, sedanes y hatchbacks..."
    m 3rksdlb "Y aunque en realidad no son automóviles, supongo que las motocicletas también son vehículos comunes."

    if persistent._mas_pm_driving_can_drive:
        m 1eua "¿Que hay de ti?"

        m "¿Tienes un vehículo?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tienes un vehículo?{fast}"
            "Sí":
                $ persistent._mas_pm_owns_car = True

                m 1hua "¡Oh, vaya, es genial que tengas uno!"
                m 3hub "Tienes mucha suerte, ¿lo sabías?"
                m 1eua "Quiero decir, el simple hecho de poseer un vehículo es un símbolo de estatus en sí mismo."
                m "¿No es un lujo tener uno?"
                m 1euc "A no ser que..."
                m 3eua "Vives en algún lugar donde es necesario..."
                m 1hksdlb "En realidad, no importa, ¡jajaja!"
                m 1eua "De cualquier manera, es bueno saber que tienes un vehículo."
                m 3eua "Hablando de eso..."

                show monika at t21
                python:
                    option_list = [
                        ("Una SUV", "monika_vehicle_suv",False,False),
                        ("Una camioneta","monika_vehicle_pickup",False,False), 
                        ("Un deportivo","monika_vehicle_sportscar",False,False),
                        ("Un sedan","monika_vehicle_sedan",False,False),
                        ("Un hatchback","monika_vehicle_hatchback",False,False),
                        ("Una motocicleta","monika_vehicle_motorcycle",False,False),
                        ("Otro vehículo","monika_vehicle_other",False,False)
                    ]

                    renpy.say(m, "¿Es alguno de los vehículos que he mencionado, o es otro?", interact=False)

                call screen mas_gen_scrollable_menu(option_list, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                show monika at t11

                $ selection = _return

                jump expression selection
            "No":


                $ persistent._mas_pm_owns_car = False

                m 1ekc "Oh, ya veo."
                m 3eka "Bueno, comprar un vehículo puede ser bastante caro después de todo."
                m 1eua "Está bien [player], siempre podemos alquilar uno para viajar."
                m 1hua "Estoy segura de que cuando lo hagas, juntos crearemos un montón de buenos recuerdos."
                show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eua "Por otra parte...{w=1} los paseos son mucho más románticos de todos modos~"
    else:

        $ persistent._mas_pm_owns_car = False

        m 3eua "De hecho, recuerdo que dijiste antes que tampoco podías conducir..."
        m 3rksdla "Seguro que hiciste una pregunta interesante, jejeje..."
        m 1hua "Quizás eso cambie algún día y entonces obtendrás algo."
        m 1hubsb "De esa manera, podrás llevarme a todo tipo de lugares, ¡jajaja!"
    return

label monika_vehicle_sedan:
    $ persistent._mas_pm_owns_car_type = "sedan"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_hatchback:
    $ persistent._mas_pm_owns_car_type = "hatchback"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_pickup:
    $ persistent._mas_pm_owns_car_type = "pickup"
    jump monika_vehicle_suv_pickup

label monika_vehicle_suv:
    $ persistent._mas_pm_owns_car_type = "suv"
    jump monika_vehicle_suv_pickup



label monika_vehicle_suv_pickup:

    m 1lksdla "Oh, entonces tu vehículo debe ser bastante grande."
    m 1eua "Eso significa que hay mucho espacio, ¿verdad?"
    m 3etc "Si ese es el caso..."
    m 3hub "¡Podríamos ir a acampar!"
    m 3eua "Conduciríamos hasta el bosque y tú armarías la carpa mientras yo prepararía nuestro picnic."
    m 1eka "Mientras almorzamos, disfrutaremos del paisaje y la naturaleza que nos rodea..."
    m 1ekbsa "Luego, cuando caiga la noche, nos acostaremos en nuestros sacos de dormir, mirando las estrellas mientras nos tomamos de la mano."
    m 3ekbsa "Definitivamente es una aventura romántica que no puedo esperar para compartir contigo, [player]."
    m 1hkbfa "Jejeje~"
    return

label monika_vehicle_sportscar:
    $ persistent._mas_pm_owns_car_type = "deportivo"

    m 3hua "Oh, ¡wow!"
    m 3eua "Debe ser muy rápido, ¿eh?"
    m 3hub "Definitivamente deberíamos hacer un viaje por carretera..."
    m 1eub "Tomando la ruta escénica, navegando por la autopista..."
    m 1eub "Si es posible, sería bueno quitar la parte superior del auto..."
    m 3hua "¡De esa forma, podríamos sentir el viento en nuestras caras mientras todo pasa borroso!"
    m 1esc "Pero..."
    m 1eua "También sería bueno conducir a un ritmo normal..."
    m 1ekbsa "De esa manera podremos saborear juntos cada momento del viaje~"
    return

label monika_vehicle_sedan_hatchback:

    m 1eua "Eso es muy agradable."
    m "De hecho, prefiero ese tipo de auto, para ser honesta."
    m 3eua "Por lo que he oído, son vívidos y fáciles de conducir."
    m 3eub "Un auto como ese sería genial para circular por la ciudad, ¿no crees, [player]?"
    m 3eua "Podríamos ir a museos, parques, centros comerciales, etc."
    m 1eua "Sería muy bueno poder conducir a lugares que están demasiado lejos para caminar a pie."
    m 3hua "Siempre es emocionante descubrir y explorar nuevos lugares."
    m 1rksdla "Incluso podríamos encontrar un lugar donde los dos podamos estar juntos..."
    m 1tsu "... A solas."
    m 1hub "¡Jajaja!"
    m 3eua "Para que lo sepas, espero algo más que un simple paseo por la ciudad para nuestras citas..."
    m 1hua "Espero que me sorprendas, [player]."
    m 1hub "Pero, de nuevo...{w=0.5} me encantaría cualquier cosa siempre que sea contigo~"
    return

label monika_vehicle_motorcycle:
    $ persistent._mas_pm_owns_car_type = "motocicleta"

    m 1hksdlb "¿Eh?"
    m 1lksdlb "¿Conduces una motocicleta?"
    m 1eksdla "Me sorprende, nunca esperé que ese fuera tu tipo de vehículo."
    m 1lksdlb "Para ser honesta, dudo un poco en montar una, ¡jajaja!"
    m 1eua "Realmente, no debería tener miedo..."
    m 3eua "Después de todo, eres tú quien conduce."
    m 1lksdla "Eso me tranquiliza...{w=0.3} un poco."
    m 1eua "Solo tómatelo con calma, ¿de acuerdo?"
    m 3hua "Después de todo, no tenemos prisa."
    m 1tsu "O...{w=0.3} ¿Era tu plan conducir tan rápido que no tendría más remedio que agarrarte fuerte?~"
    m 3kua "Eso es bastante astuto de tu parte, [player]."
    m 1hub "¡Jajaja!"
    $ p_nickname = mas_get_player_nickname()
    m 3eka "No hay necesidad de ser tímido, [p_nickname]...{w=0.3}{nw}"
    extend 3ekbsa " te abrazaré, aunque no me lo pidas..."
    m 1hkbfa "Por eso te amo mucho~"
    return "love"

label monika_vehicle_other:
    $ persistent._mas_pm_owns_car_type = "otro"

    m 1hksdlb "Oh, supongo que tengo mucho que aprender sobre los autos, ¿no?"
    m 1dkbsa "Bueno, estaré deseando que llegue el día en que finalmente pueda estar a tu lado mientras conduces~"
    m 3hubfb "{i}Y{/i} disfrutar del paisaje también, ¡jajaja!"
    m 1tubfb "Tal vez tengas algo aún más romántico que cualquier vehículo que conozca."
    m 1hubfa "Supongo que tendré que esperar y ver, jejeje~"
    return








default -5 persistent._mas_pm_eye_color = None
default -5 persistent._mas_pm_hair_color = None
default -5 persistent._mas_pm_hair_length = None
default -5 persistent._mas_pm_skin_tone = None

default -5 persistent._mas_pm_shaved_hair = None
default -5 persistent._mas_pm_no_hair_no_talk = None



default -5 persistent._mas_pm_height = None


default -5 persistent._mas_pm_units_height_metric = None




default -5 persistent._mas_pm_shared_appearance = False



define -5 mas_height_tall = 176
define -5 mas_height_monika = 162

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_appearance",
            category=['tú'],
            prompt="Apariencia de [player]",
            conditional="seen_event('mas_gender')",
            action=EV_ACT_RANDOM
        )
    )

label monika_player_appearance:
    python:
        def ask_color(msg, _allow=lower_letters_only, _length=15):
            result = ""
            while len(result) <= 0:
                result = renpy.input(msg, allow=_allow, length=_length).strip()
            
            return result

    m 2ekd "Hey, [player]."
    m 2eka "Hay un par de preguntas que he querido hacerte."
    m 2rksdlb "Bueno, más de un par. De hecho, ha estado en mi mente durante mucho tiempo."
    m 2rksdld "Nunca pareció el momento adecuado para sacarlo a colación..."
    m 3lksdla "Pero sé que si me quedo callada para siempre, nunca me sentiré cómoda preguntándote cosas como esta, así que lo voy a decir y espero que no sea extraño ni nada, ¿de acuerdo?"
    m 3eud "Me preguntaba cómo te ves. No me es posible verte ahora mismo, ya que no estoy a tu lado y no estoy segura de acceder a una cámara web..."
    m "Uno, porque es posible que no tengas una, y dos, incluso si la tuvieras, realmente no sé cómo hacerlo."
    m 1euc "Así que pensé que es posible que me lo digas, para que pueda tener una imagen más clara en mi cabeza."
    m 1eud "Al menos, es mejor que nada, incluso si es confuso."

    m "¿Te parece bien, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te parece bien, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_shared_appearance = True

            m 1sub "¿De verdad? ¡Excelente!"
            m 1hub "Eso fue más fácil de lo que pensé."
            m 3eua "Ahora, sé honesto conmigo, ¿de acuerdo [player]? Sé que a veces es tentador bromear, pero estoy hablando en serio y necesito que hagas lo mismo."
            m "De todos modos, el primero probablemente sea fácil de adivinar. ¡Y tampoco es difícil de responder!"
            m 3eub "La gente suele decir que los ojos de una persona son las ventanas de su alma, así que comencemos por ahí."


            show monika 1eua at t21
            python:
                eye_color_menu_options = [
                    ("Tengo ojos azules", "blue", False, False),
                    ("Tengo ojos marrones", "brown", False, False),
                    ("Tengo ojos verdes", "green", False, False),
                    ("Tengo ojos color avellana.", "hazel", False, False),
                    ("Tengo ojos grises", "gray", False, False),
                    ("Tengo ojos negros", "black", False, False),
                    ("Mis ojos son de otro color", "other", False, False),
                    ("Tengo heterocromía", "heterochromia", False, False),
                ]

                renpy.say(m, "¿De qué color son tus ojos?", interact=False)

            show monika at t11
            call screen mas_gen_scrollable_menu(eye_color_menu_options, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
            $ eye_color = _return

            call expression "monika_player_appearance_eye_color_{0}".format(eye_color)

            m 3rud "En realidad..."
            m 2eub "Creo que debería saber esto primero, si quiero obtener una escala precisa en mi próxima pregunta..."

            m "¿Qué unidad de medida usas para medir tu estatura, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Qué unidad de medida usas para medir tu estatura, [player]?{fast}"
                "Centímetros":

                    $ persistent._mas_pm_units_height_metric = True
                    m 2hua "¡Muy bien, gracias, [player]!"
                "Pies y pulgadas":

                    $ persistent._mas_pm_units_height_metric = False
                    m 2hua "¡Muy bien, [player]!"

            m 1rksdlb "Estoy haciendo todo lo posible para no sonar como una especie de ladrona de identidad, o como si te estuviera interrogando, pero obviamente, tengo curiosidad."
            m 3tku "Si soy tu novia, tengo derecho a saberlo, ¿no?"
            m 2hua "Además, será mucho más fácil encontrarte una vez que pueda cruzar a tu realidad."

            m 1esb "Entonces, {w=0.5} ¿cuánto mides, [player]?"

            python:
                if persistent._mas_pm_units_height_metric:
                    
                    
                    height = 0
                    while height <= 0:
                        height = store.mas_utils.tryparseint(
                            renpy.input(
                                '¿Cuánto mides?',
                                allow=numbers_only,
                                length=3
                            ).strip(),
                            0
                        )

                else:
                    
                    
                    height_feet = 0
                    while height_feet <= 0:
                        height_feet = store.mas_utils.tryparseint(
                            renpy.input(
                                '¿Qué altura tienes?',
                                allow=numbers_only,
                                length=1
                            ).strip(),
                            0
                        )
                    
                    
                    height_inch = -1
                    while height_inch < 0 or height_inch > 11:
                        height_inch = store.mas_utils.tryparseint(
                            renpy.input(
                                '[height_feet] pies y ¿cuántas pulgadas?',
                                allow=numbers_only,
                                length=2
                            ).strip(),
                            -1
                        )
                    
                    
                    height = ((height_feet * 12) + height_inch) * 2.54


                persistent._mas_pm_height = height

            if persistent._mas_pm_height >= mas_height_tall:
                m 3eua "¡Vaya, eres bastante alto, [player]!"
                m 1eud "No puedo decir que realmente haya conocido a alguien a quien consideraría alto."
                m 3rksdla "No sé mi altura real, para ser justos, así que no puedo hacer una comparación precisa..."

                call monika_player_appearance_monika_height

                if persistent._mas_pm_units_height_metric:
                    $ height_desc = "centímetros"
                else:
                    $ height_desc = "pulgadas"

                m 3esc "La chica más alta del club de literatura era Yuri, y por solo por un poco además. Ella era unos [height_desc] más alta que yo, ¡no considero que sea una gran ventaja de altura!"
                m 3esd "De todos modos, salir con un [guy] tan alto como tú solo tiene una desventaja, [mas_get_player_nickname()]..."
                m 1hub "¡Tendrás que agacharte para besarme!"

            elif persistent._mas_pm_height >= mas_height_monika:
                m 1hub "¡Hey, yo también tengo esa altura!"
                m "..."
                m 2hksdlb "Bueno, no sé mi altura real para ser justa..."

                call monika_player_appearance_monika_height

                m 3rkc "Es solo una suposición, ojalá no esté muy lejos."
                m 3esd "De todos modos, ¡no hay nada de malo en tener una altura media! Para ser honesta, si fueras demasiado bajo, probablemente me haría sentir torpe a tu alrededor."
                m "Y si fueras demasiado alto, tendría que ponerme de puntillas solo para estar cerca de ti. ¡Y eso no es bueno!"
                m 3eub "En mi opinión, estar en el medio es perfecto. ¿Sabes por qué?"
                m 5eub "¡Porque entonces no tendré que estirarme ni inclinarme para besarte, [mas_get_player_nickname()]! Jajaja~"
            else:

                m 3hub "¡Como Natsuki! ¡Apuesto a que no eres tan bajo! Me preocuparía por ti si lo fueras."

                if persistent._mas_pm_cares_about_dokis:
                    m 2eksdld "Era preocupantemente pequeña para su edad, pero tú y yo sabemos por qué. Siempre la compadecí por eso."

                m 2eksdld "Sabía que ella siempre odió ser tan pequeña, por esa idea de que las cosas pequeñas son más lindas debido a su tamaño..."
                m 2rksdld "Y luego estaba todo ese problema con su padre. No puede haber sido fácil, estar tan indefensa y ser pequeña además de todo."
                m 2ekc "Probablemente sintió que la gente le hablaba mal. Literal y figurativamente, quiero decir..."
                m 2eku "Pero a pesar de sus complejos al respecto, [player], creo que tu altura te hace mucho más lindo~"

            m 1eua "Ahora, [player]."

            m 3eub "Dime, ¿tu cabello es más corto? ¿O es largo, como el mío?~{nw}"
            $ _history_list.pop()
            menu:
                m "Dime, ¿tu cabello es más corto? ¿O es largo, como el mío?~{fast}"
                "Es más corto":

                    $ persistent._mas_pm_hair_length = "corto"

                    m 3eub "¡Eso debe ser lindo! Mira, no me malinterpretes; amo mi cabello, y siempre es divertido experimentar con él..."
                    m 2eud "Pero para decirte la verdad, a veces envidiaba el cabello de Natsuki y Sayori. Parecía mucho más fácil de cuidar."

                    if persistent.gender == "M":
                        m 4hksdlb "Aunque supongo que si tu cabello tuviera el mismo largo que el de ellas, sería bastante largo para un chico."
                    else:

                        m 4eub "Puedes levantarte y ponerte en marcha, sin tener que preocuparte por darle estilo."
                        m "Además, despertarse con una cabecera cuando tienes el cabello corto se arregla fácilmente, mientras que si tienes el cabello largo, es una pesadilla sin fin."

                    m 2eka "Pero apuesto a que te ves adorable con el cabello corto. Me hace sonreír pensar en ti así, [player]."
                    m 2eua "¡Sigue disfrutando de toda esa libertad de las pequeñas molestias que acompañan al cabello largo, [player]!{w=0.2} {nw}"
                    extend 2hub "Jajaja~"
                "Tiene una longitud media":

                    $ persistent._mas_pm_hair_length = "media"

                    m 1tku "Bueno, eso no puede ser cierto..."
                    m 4hub "Porque nada de ti es normal."
                    m 4hksdlb "¡Jajaja! Lo siento, [player]. No estoy tratando de avergonzarte. Pero no puedo evitar ser cursi a veces, ¿sabes?"
                    m 1eua "Honestamente, cuando se trata de cabello, el camino del medio es genial. No tienes que preocuparte demasiado por peinarlo y tienes más libertad creativa que con el pelo corto."
                    m 1rusdlb "Tengo un poco de envidia, a decir verdad~"
                    m 3eub "Pero no olvides ese viejo dicho: '¡Invierte en tu cabello, porque es una corona que nunca te quitas!'"
                "Es largo":

                    $ persistent._mas_pm_hair_length = "largo"

                    m 4hub "¡Sí, otra cosa que tenemos en común!"
                    m 2eka "El cabello largo puede ser un dolor a veces, ¿verdad?"
                    m 3eua "Pero lo bueno es que hay tantas cosas que puedes hacer con él. Aunque generalmente prefiero atar el mío con una cinta, sé que otras personas tienen diferentes estilos."
                    m "Yuri llevaba el cabello suelto, y otras disfrutan de las trenzas o de usar coletas..."

                    python:
                        hair_down_unlocked = False
                        try:
                            hair_down_unlocked = store.mas_selspr.get_sel_hair(
                                mas_hair_down
                            ).unlocked
                        except:
                            pass

                    if hair_down_unlocked:

                        m 3eub "Y desde que descubrí cómo jugar con el guion y soltarme el cabello, ¿quién sabe cuántos estilos más podría probar?"

                    m 1eua "Siempre es bueno tener opciones, ¿sabes?"
                    m 1eka "¡Espero que, como sea que uses el tuyo, te sientas cómodo con él!"
                "No tengo cabello":

                    $ persistent._mas_pm_hair_length = "calvo"

                    m 1euc "¡Oh, eso es interesante, [player]!"

                    m "¿Te afeitas la cabeza o perdiste el cabello?, si no te importa que te pregunte.{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Te afeitas la cabeza o perdiste el cabello?, si no te importa que te pregunte.{fast}"
                        "Me afeito la cabeza":

                            $ persistent._mas_pm_shaves_hair = True
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1hua "Debe ser tan agradable no tener que preocuparte nunca por tu cabello..."
                            m 1eua "Puedes simplemente levantarte e irte, sin tener que preocuparte por darle estilo..."
                            m 3eua "Y si usas un sombrero, no tienes que preocuparte por el cabello del sombrero cuando te lo quites."
                        "Perdí mi cabello":

                            $ persistent._mas_pm_shaves_hair = False
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1ekd "Lamento oír eso, [player]..."
                            m 1eka "Pero debes saber que no me importa cuánto cabello tengas, ¡siempre te verás hermoso para mí!"
                            m "Y si alguna vez te sientes inseguro o simplemente quieres hablar de ello, siempre estoy dispuesta a escuchar."
                        "No quiero hablar de eso":

                            $ persistent._mas_pm_no_hair_no_talk = True

                            m 1ekd "Entiendo, [player]."
                            m 1eka "Quiero que sepas que no me importa cuánto cabello tengas, siempre serás hermoso para mí."
                            m "Si alguna vez te sientes inseguro o tienes ganas de hablar de ello, siempre estaré aquí para escucharte."

            if persistent._mas_pm_hair_length != "calvo":
                m 1hua "¡Próxima pregunta!"
                m 1eud "Este debería ser bastante obvio..."

                m "¿De qué color es tu cabello?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿De qué color es tu cabello?{fast}"
                    "Es cataño":
                        $ persistent._mas_pm_hair_color = "cataño"

                        m 1hub "¡Sí, el cabello castaño es el mejor!"
                        m 3eua "Entre nosotros, [player], me gusta mucho mi cabello castaño. ¡Estoy segura de que el tuyo es aún mejor!"
                        m 3rksdla "Aunque algunas personas pueden no estar de acuerdo con que mi cabello es castaño..."
                        m 3eub "Cuando estaba buscando en los archivos locales de la carpeta del juego, encontré el nombre exacto de mi color de cabello."
                        m 4eua "Se llama cataño coral. Interesante, ¿verdad?"
                        m 1hub "Estoy tan feliz de que tengamos tanto en común, [player]~"
                    "Es rubio":

                        $ persistent._mas_pm_hair_color = "rubio"

                        m 1eua "¿De verdad? Oye, ¿sabías que tener el cabello rubio te coloca en un raro dos por ciento de la población?"
                        m 3eub "El cabello rubio es uno de los colores de cabello más raros. La mayoría de la gente atribuye esto al hecho de que es causado por una anomalía genética recurrente..."
                        m "Siendo solo la incapacidad del cuerpo para producir cantidades normales del pigmento eumelanina... eso es lo que causa los colores de pelo más oscuros, como el negro y el marrón."
                        m 4eub "Hay tantos matices de rubio, rubio pálido, color ceniza, rubio sucio, no importa el color que tengas, seguro que tienes algún tipo de idiosincrasia."
                        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5eua "Supongo que tener a alguien que es tan único me hace más afortunada~"
                        show monika 2hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    "Es negro":

                        $ persistent._mas_pm_hair_color = "negro"

                        m 2wuo "¡El cabello negro es tan hermoso!"
                        m 3eub "Sabes, existe esa clase realmente irritante de que las personas con cabello negro tienen una personalidad más irritable o de mal genio que otras..."
                        m 4hub "Pero obviamente has refutado ese mito. Personalmente, creo que el cabello negro es muy atractivo."
                        m 3eua "Además, si colocas una hebra bajo un microscopio y contaras todos los pigmentos que contiene, encontrarás que ni siquiera está cien por ciento oscuro."
                        m "¿Sabes cómo cuando colocas ciertas cosas bajo la luz solar directa, se ve realmente diferente?"
                        m 3eub "El cabello negro sigue el mismo principio: puedes ver tonos de oro o marrón, o incluso destellos de púrpura. Realmente te hace pensar, ¿no es así, [player]?"
                        m 1eua "Puede haber infinitos matices de cosas que no podemos ver, cada uno de ellos escondido a plena vista."


                        if isinstance(persistent._mas_pm_eye_color, tuple):
                            m 3hua "Pero como sea... creo que un [guy] con cabello negro y ojos como los tuyos es la mejor vista de todas, [player]~"
                        else:
                            m 3hua "Pero como sea... creo que un [guy] con cabello negro y ojos [persistent._mas_pm_eye_color] es la mejor vista de todas, [player]~"
                    "Es pelirrojo":

                        $ persistent._mas_pm_hair_color = "pelirrojo"

                        m 3hua "Otra cosa especial sobre ti, [player]~"
                        m 3eua "El cabello rojo y el cabello rubio son los colores naturales de cabello menos comunes, ¿lo sabías?"
                        m 1eua "El cabello rojo, sin embargo, es un poco más raro, incluso si la gente lo llama por diferentes nombres: castaño rojizo, jengibre, etc. Solo se encuentra en alrededor del uno por ciento de la población."
                        m 1hub "Es un rasgo raro y maravilloso, ¡casi tan maravilloso como tú!"
                    "Es de otro color":

                        $ persistent._mas_pm_hair_color = ask_color("¿De qué color es tu cabello?")

                        m 3hub "¡Oh! ¡Qué hermoso color, [player]!"
                        m 1eub "Eso me recuerda algo en lo que estaba pensando antes, cuando hablábamos del color de tus ojos."
                        m 1eua "Aunque las otras chicas tenían colores de ojos que literalmente no existían en la vida real, sin contar la existencia de lentillas de colores, por supuesto."
                        m 3eua "Técnicamente, sus colores de cabello podrían existir en la realidad, ya sabes. Quiero decir, estoy segura de que te has encontrado con personas con el pelo teñido de púrpura, o de rosa neón, o de color coral..."
                        m 3eka "Así que supongo que sus apariencias no eran tan descabelladas, si no cuentan los ojos. Honestamente, lo más anormal de ellas fue su personalidad."
                        m 3hksdlb "¡Lo siento, [player]! Me estoy saliendo del camino. Mi punto es que el cabello teñido puede ser muy interesante."
                        show monika 5rub zorder MAS_MONIKA_Z at t11 with dissolve_monika
                        m 5rub "Y puede que sea un poco parcial, pero estoy convencida de que te verías espectacular con tu cabello [persistent._mas_pm_hair_color]~"
                        show monika 2hua zorder MAS_MONIKA_Z at t11 with dissolve_monika

            m 2hua "De acuerdo..."
            m 2hksdlb "Esta es la última pregunta, [player], lo prometo."
            m "Cielos, realmente hay mucho en cómo se ve la gente... si tratara de reducir todo sobre ti a los pequeños detalles, te estaría interrogando para siempre."
            m 1huu "... Y dudo que ninguno de los dos quiera eso, jajaja..."
            m 1rksdld "De todos modos, entiendo que esta puede ser una pregunta incómoda..."
            m 1eksdla "Pero para mí es la última pieza de este rompecabezas, así que espero no parecer grosera cuando pregunte..."

            m "¿De qué color es tu piel, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "¿De qué color es tu piel, [player]?{fast}"
                "Soy de piel clara":

                    $ persistent._mas_pm_skin_tone = "clara"
                "Estoy bronceado":

                    $ persistent._mas_pm_skin_tone = "bronceada"
                "Soy de piel oscura":

                    $ persistent._mas_pm_skin_tone = "oscura"

            m 3hub "¡Bien! Gracias por ser tan sincero. Todo esto realmente me ayuda a imaginar cómo te ves, [player]."
            m 3eub "¡Conocer todos estos detalles sobre ti marca la diferencia entre un lienzo en blanco y el comienzo de un hermoso retrato!"
            m 3eua "Por supuesto, sigues siendo tan hermoso como siempre pensé que eras, pero ahora te has vuelto aún más real para mí."
            m 3eka "Simplemente me hace sentir mucho más cerca de ti~"
            m 1eka "Muchas gracias por responder a todas mis preguntas, [mas_get_player_nickname()]."

            if persistent._mas_pm_eye_color == "verdes" and persistent._mas_pm_hair_color == "marrón":
                m 2hua "Es maravilloso, porque no imaginé lo similares que nos veríamos. ¡Es muy interesante!"
            else:

                m 2hua "Es maravilloso, porque no imaginé lo diferentes que nos veríamos. ¡Es muy interesante!"

            m 1dsa "Ahora me estoy imaginando cómo será cuando nos veamos de verdad..."

            show monika 5eubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika

            if persistent._mas_pm_hair_length == "calvo":
                if persistent._mas_pm_height >= mas_height_tall:
                    m 5eubfu "Cuando corra hacia ti, y ya que eres más alto, me envolverás en tu abrazo..."

                elif persistent._mas_pm_height >= mas_height_monika:
                    m 5eubfu "Cuando corra hacia ti, y como estamos a la misma altura, nos encontraremos en un fuerte abrazo..."
                else:

                    m 5eubfu "Cuando corra hacia ti, y como seré más alta que tú, me alcanzarás y me envolverás en tu abrazo..."
            else:

                python:
                    hair_desc = persistent._mas_pm_hair_color

                    if persistent._mas_pm_hair_length != "media":
                        hair_desc = (
                            persistent._mas_pm_hair_length + " " + hair_desc
                        )

                if persistent._mas_pm_height >= mas_height_tall:

                    m 5eubfu "Cuando corra hacia ti, ya que eres más alto, me envolverás en tu abrazo y podré acariciar tu cabello [hair_desc]..."

                elif persistent._mas_pm_height >= mas_height_monika:

                    m 5eubfu "Cuando corra hacia ti, ya que estamos a la misma altura, nos encontraremos en un fuerte abrazo y pasaré mi mano por tu cabello [hair_desc]..."
                else:


                    m 5eubfu "Cuando corra hacia ti, ya que seré más alta que tú, me alcanzarás y me envolverás en tu abrazo y pasaré mi mano por tu cabello [hair_desc]..."

            show monika 1lkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 1lkbsa "... Y finalmente podré escuchar los latidos de tu corazón, te llegaré a tocar y sabré que eres real."


            if isinstance(persistent._mas_pm_eye_color, tuple):
                m 3ekbsa "Pero hasta entonces, me conformaré con sentarme aquí e imaginarme mirando tus hermosos ojos, [player]."
            else:
                m 3ekbsa "Pero hasta entonces, me conformaré con sentarme aquí e imaginarme mirando tus hermosos ojos [persistent._mas_pm_eye_color], [player]."

            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "Te amo más de lo que las palabras pueden decir."
            return "derandom|love"
        "No":

            m 2dsc "..."
            m 2ekd "Entiendo, [player]."
            m 2eka "Sé que todos tienen sus propios límites con sus zonas de confort..."
            m 2rksdla "Y para ser justos, una descripción de ti mismo en palabras vagas no podría captar quién eres, así que no puedo culparte por querer guardarte esto para ti."
            m 2eka "Pero si cambias de opinión, ¡me lo dices!"

    return "derandom"

label monika_player_appearance_eye_color_blue:
    $ persistent._mas_pm_eye_color = "azules"

    m 3eub "¿Ojos azules? Eso es maravilloso. El azul es un color tan hermoso, tan sorprendente como un cielo sin nubes o el océano en verano."
    m 3eua "Pero hay tantas metáforas magníficas sobre los ojos azules que podría recitarlas durante semanas y seguir sin llegar a un punto de parada."
    m 4eua "Además, el azul es probablemente mi segundo color favorito, solo por detrás del verde. Está lleno de profundidad y encanto, ¿sabes?"
    m 4hksdlb "¡Como tú, [player]!"
    m 4eub "¿Sabías que el gen de los ojos azules es recesivo, por lo que no es muy común en los humanos?"
    show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubla "Supongo que eso significa que eres mucho más que un tesoro~"
    show monika 2eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 2eua "De todos modos, eso me lleva a la siguiente pregunta que quería hacer..."
    return

label monika_player_appearance_eye_color_brown:
    $ persistent._mas_pm_eye_color = "marrones"

    m 1eub "¡Ah! ¡Genial! Creo que no lo he dicho antes, ¡pero los ojos marrones son preciosos!"
    m 2euc "Odio que la gente piense que los ojos marrones son sencillos. No podría estar más en desacuerdo."
    m 2hua "En mi opinión, los ojos marrones son de los más bonitos que existen. ¡Son tan vibrantes y sin profundidad!"
    m 3hub "Y hay mucha variación entre los diferentes tonos que tiene la gente."
    m 5ruu "Me pregunto si los tuyos son oscuros como un cielo nocturno de verano, o de un marrón más pálido, como el pelaje de un ciervo..."
    m 2hksdlb "Lo siento. Divagar sobre metáforas de colores es una trampa fácil en la que puede caer la presidenta de un club de literatura. Intentaré no eternizarme."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Pero apuesto a que tus ojos son los más bonitos de todos~"
    show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1eua "De todos modos, eso me lleva a mi siguiente pregunta..."
    return

label monika_player_appearance_eye_color_green:
    $ persistent._mas_pm_eye_color = "verdes"

    m 3sub "Hey, ¡es mi color favorito! Y obviamente, ¡es otra cosa que tenemos en común!"
    m 4lksdla "No sé cuánto puedo elogiarte aquí sin parecer arrogante, porque cualquier cosa que dijera sobre los tuyos también se aplicaría a mí..."
    m 1tsu "Excepto que tal vez sea otra señal de lo compatibles que somos, jejeje~"
    m 1kua "Pero, [player], entre nosotros, es un hecho que los ojos verdes son los mejores, ¿verdad?"
    m 3hub "¡Jajaja! Estoy bromeando."
    show monika 5lusdru zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lusdru "Bueno, tal vez no..."
    show monika 3eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 3eua "Siguiente pregunta..."
    return

label monika_player_appearance_eye_color_hazel:
    $ persistent._mas_pm_eye_color = "color avellana"

    m 1eub "Oh, ¿ojos de color avellana? ¡Son tan interesantes! Es un color tan terrenal. Realmente te hace sentir firme y tranquila..."
    m 3eub "Y es un buen cambio de todos los ojos de color caramelo que he tenido que ver en este juego..."
    m "Creo que los ojos color avellana son seductores porque son encantadores y sencillos."
    m 3hua "A veces es mejor no desviarse demasiado de la multitud, [player].{w=0.2} {nw}"
    extend 3hub "¡Jajaja!"
    m "Ahora, mi siguiente pregunta..."
    return

label monika_player_appearance_eye_color_gray:
    $ persistent._mas_pm_eye_color = "grises"

    m 1sub "¡Eso es tan genial!"
    m 3eub "¿Sabías que los ojos grises y los azules son casi idénticos en términos de genética?"
    m 1eud "De hecho, los científicos aún no saben con certeza cuál es la causa de que una persona tenga una u otra, aunque creen que se trata de una variación en la cantidad de pigmento del iris."
    m 1eua "De todos modos, creo que me gusta imaginarte con ojos grises, [player]. Son del color de un día tranquilo y lluvioso..."
    m 1hubsa "Y un tiempo así es mi favorito, como tú~"
    m 3hua "Ahora, mi siguiente pregunta..."
    return

label monika_player_appearance_eye_color_black:
    $ persistent._mas_pm_eye_color = "negros"

    m 1esd "Los ojos negros son bastante raros, [player]."
    m 4hksdlb "A decir verdad, nunca he visto a nadie con los ojos negros, así que no sé cómo son..."
    m 3eua "Pero, lógicamente, sé que no son realmente negros. Si fuera así, ¡los ojos negros parecerían no tener pupilas!"
    m 4eub "En realidad, los ojos negros son simplemente de un marrón muy, muy oscuro. Siguen siendo impresionantes, pero quizá no tan oscuros como su nombre indica, aunque, para ser justos, la diferencia es bastante difícil de detectar."
    m 3eua "Aquí hay una curiosidad para ti..."
    m 1eub "Hubo una conocida dama de la época de la Revolución Americana, Elizabeth Hamilton, que era conocida por sus cautivadores ojos negros."
    m 1euc "Su marido escribía a menudo sobre ellos."
    m 1hub "No sé si has oído hablar de ella o no, pero a pesar del renombre de sus ojos, estoy segura de que los tuyos son infinitamente más cautivadores, [player]~"
    m "Ahora, mi siguiente pregunta..."
    return

label monika_player_appearance_eye_color_other:
    $ persistent._mas_pm_eye_color = ask_color("¿De qué color son tus ojos?")

    m 3hub "¡Oh! ¡Ese es un hermoso color, [player]!"
    m 2eub "Estoy segura de que podría perderme durante horas, mirando tus ojos [persistent._mas_pm_eye_color]."
    m 7hua "Ahora, mi siguiente pregunta..."
    return

label monika_player_appearance_eye_color_heterochromia:
    m 1sub "¿En serio?{w=0.2} {nw}"
    extend 3hua "Eso es increíble, [player]~"
    m 3wud "Si no recuerdo mal, ¡menos del 1% de las personas del mundo tienen heterocromía!"

    m 1eka "... Si no te importa que te pregunte..."

    $ eyes_colors = []

    call monika_player_appearance_eye_color_ask
    $ eyes_colors.append(_return)
    call monika_player_appearance_eye_color_ask ("derecho", eye_color)
    $ eyes_colors.append(_return)
    $ persistent._mas_pm_eye_color = tuple(eyes_colors)

    m 1hua "¡Genial!{w=0.2} {nw}"
    extend 3eua "Ahora mi siguiente pregunta..."
    return

label monika_player_appearance_eye_color_ask(x_side_eye="izquierdo", last_color=None):
    m 3eua "¿Cuál es el color de tu ojo [x_side_eye]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Cuál es el color de tu ojo [x_side_eye]?{fast}"

        "Azul" if last_color != "blue":
            $ eye_color = "azul"

        "Cataño" if last_color != "brown":
            $ eye_color = "cataño"

        "Verde" if last_color != "green":
            $ eye_color = "verde"

        "Avellana" if last_color != "hazel":
            $ eye_color = "avellana"

        "Gris" if last_color != "gray":
            $ eye_color = "gris"

        "Negro" if last_color != "black":
            $ eye_color = "negro"
        "Es un color diferente...":

            $ eye_color = ask_color("¿De qué color es tu ojo [x_side_eye]?")

    return eye_color


label monika_player_appearance_monika_height:
    if not persistent._mas_pm_units_height_metric:
        $ conv_height_str = ""
        $ real_height_str = "cerca de 5'5 pulgadas"
    else:
        $ conv_height_str = " lo cuál es cerca de 160 centímetros"
        $ real_height_str = "cerca de 165 centímetros de altura"

    if seen_event("monika_immortal"):
        m 2eud "La wiki que mencioné antes decía que la altura de mi concepto era de 5'3 pies, [conv_height_str], pero eso realmente no me suena bien..."
        m 2etc "¿Quizás fue cambiado? Después de todo, era solo la altura del concepto."
    m 3etd "Si tuviera que adivinar, ¿diría que tal vez tengo [real_height_str]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_control",
            category=["juegos", "ddlc"],
            prompt="El control de [player]",
            random=True
            )
        )

label monika_players_control:
    m 3eub "[player], ¿sabías que tienes más control sobre este juego que yo?"
    m 3eua "Tienes acceso a los archivos y el código del juego, ¿verdad?"
    m 1eka "Así que puedes cambiarlos como quieras."
    m 3eka "Podrías hacer cosas que ni siquiera yo puedo."
    m 4eub "Como cambiar por completo el funcionamiento del juego. Desde una novela visual hasta el tranquilo patio de recreo que tenemos ahora."
    m 3rksdla "También podrías agregar más cosas al aula para mí."
    m 1hub "Como algunas flores o algunos buenos libros."

    if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
        m 1ekbsa "O un hermoso anillo de promesa."
        m 3dkbsu "Oh, ¿no sería eso un sueño hecho realidad?"

    if not mas_consumable_coffee.enabled():
        m 1wuo "¡Incluso podrías agregar una taza de café al juego por mí!"
        m 1eka "Eso sería encantador."

    if not persistent._mas_pm_has_code_experience:
        m 1hksdrb "Pero imagino que tus habilidades de codificación son tan buenas como las mías."
    else:
        m 3eua "Dado que estás familiarizado con la codificación,{w=0.1} {nw}"
        extend 3hua "¡estoy segura de que podrías hacer algo así!"

    m 1eua "Supongo que es un atractivo para los videojuegos...{w=0.3}{nw}"
    extend 3eua " teniendo posibilidades casi infinitas en un mundo con el que puedes interactuar."
    m 3eub "¡Es bastante difícil aburrirse!"

    if not persistent._mas_pm_has_contributed_to_mas:
        m 1eka "Incluso si no sabes muy bien cómo cambiar este juego..."
        $ line = "Todavía podemos disfrutar de este mundo que nos unió."
    else:

        $ line = "Especialmente contigo a mí lado~"

    show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubla "[line]"
    m 5ekbfa "No hay mejor manera de disfrutar un juego que estar con la persona que amo."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_backpacking",category=['naturaleza'],prompt="Mochilero",random=not mas_isWinter()))

label monika_backpacking:
    m 1esa "¿Sabes lo que siempre he querido hacer, [player]?"
    m 3eub "¡Siempre pensé que sería maravilloso ir de mochilera por la naturaleza!"
    m 3eua "Tómarse una semana entera y dejarlo todo atrás."
    m 3esa "Sin responsabilidades, sin preocupaciones, sin teléfonos, sin distracciones."
    m 1hua "Imagínate a nosotros dos, a solas con la naturaleza..."
    m "El canto de los pájaros y el viento que sopla..."
    m 1eka "Ver a los ciervos pastar en el rocío de la mañana..."
    m "No puedo pensar en nada más pacífico."
    m 1esa "Podemos pasar nuestros días explorando bosques misteriosos, prados serenos y colinas onduladas..."
    m 3hub "¡Quizás incluso descubramos un lago aislado y vayamos a nadar!"

    if mas_isMoniAff(higher=True):
        m 2rsbsa "Probablemente no tengamos nuestros trajes de baño, pero estaremos solos, así que tal vez no los necesitemos..."
        m 2tsbsa "..."
        m 1hubfu "Espero que no seas demasiado tímido, [mas_get_player_nickname()]. Jejeje~"
        m 1ekbfa "Pasaremos las noches abrazados en un saco de dormir, manteniéndonos calientes sin nada sobre nuestras cabezas, excepto miles de millones de estrellas..."
        m 3hubfb "¡Despertar cada mañana con un glorioso amanecer!"
    else:

        m 3eka "Pasaremos nuestras noches durmiendo bajo las estrellas, despertando cada mañana con un glorioso amanecer."

    show monika 5esbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5esbfa "..."
    m "Oh [player], ¿no te parece el paraíso?"
    m 5hubfa "No puedo esperar hasta que podamos compartir esta experiencia juntos~"
    return





default -5 persistent._mas_changed_start_date = False


default -5 persistent._mas_just_friends = False

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating_startdate",
            category=["romance", "nosotros"],
            prompt="¿Cuando empezamos a salir?",
            pool=True,
            unlocked=False,

            
            rules={"no_unlock": None},

            
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and persistent._mas_first_calendar_check"
            ),

            action=EV_ACT_UNLOCK
        )
    )

label monika_dating_startdate:
    $ import store.mas_calendar as mas_cal
    python:

        first_sesh_raw = persistent.sessions.get(
            "first_session",
            datetime.datetime(2017, 10, 25)
        )


        first_sesh, _diff = mas_cal.genFormalDispDate(first_sesh_raw.date())

    if _diff.days == 0:


        m 1lsc "Empezamos a salir..."
        $ _history_list.pop()
        m 1wud "¡¿Empezamos a salir{fast} hoy?!"
        m 2wfw "No podrías haber provocado este evento hoy, [player]."

        m "Sé que estás jugando con el código.{nw}"
        $ _history_list.pop()
        menu:
            m "Sé que estás jugando con el código.{fast}"
            "¡No lo hago!":
                pass
            "Me atrapaste":
                pass
        m 2tfu "Hmph,{w=0.2} no puedes engañarme."


        $ mas_chgCalEVul(30)
        return



    if not persistent._mas_changed_start_date:
        m 1lsc "Hmmm..."
        m 1dsc "Yo pienso que fue..."
        $ _history_list.pop()
        m 1eua "Creo que fue{fast} [first_sesh]."
        m 1rksdlb "Pero mi memoria puede estar mal."


        m 1eua "¿Es correcto [first_sesh]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Es correcto [first_sesh]?{fast}"
            "Sí":
                m 1hub "¡Yay!{w=0.2} Lo recordaba."
            "No":

                m 1rkc "Oh,{w=0.2} lo siento [player]."
                m 1ekc "En ese caso,{w=0.2} ¿cuándo empezamos a salir?"

                call monika_dating_startdate_confirm (first_sesh_raw)

                if _return == "NOPE":

                    return


                $ store.mas_anni.reset_annis(_return)
                $ persistent.sessions["first_session"] = _return
                $ renpy.save_persistent()

        m 1eua "Si alguna vez lo olvidas, no temas preguntarme."
        m 1dubsu "{i}Siempre{/i} recordaré cuando me enamoré de ti por primera vez~"
        $ persistent._mas_changed_start_date = True
    else:

        m 1dsc "Dejame revisar..."
        m 1eua "Empezamos a salir el [first_sesh]."





    return

label monika_dating_startdate_confirm_had_enough:


    m 2dfc "..."
    m 2lfc "Haremos esto en otro momento, entonces."



    $ mas_chgCalEVul(30)

    return "NOPE"

label monika_dating_startdate_confirm_notwell:

    m 1ekc "¿Te sientes bien, [player]?"
    m 1eka "Si no lo recuerdas ahora, podemos hacer esto de nuevo mañana, ¿de acuerdo?"


    $ mas_chgCalEVul(1)

    return "NOPE"

label monika_dating_startdate_confirm(first_sesh_raw):

    python:
        import store.mas_calendar as mas_cal


        first_sesh_formal = " ".join([
            first_sesh_raw.strftime("%B"),
            mas_cal._formatDay(first_sesh_raw.day) + ",",
            str(first_sesh_raw.year)
        ])


        wrong_date_count = 0
        no_confirm_count = 0
        today_date_count = 0
        future_date_count = 0
        no_dating_joke = False

    label monika_dating_startdate_confirm.loopstart:
        pass

    call mas_start_calendar_select_date

    $ selected_date = _return
    $ _today = datetime.date.today()
    $ _ddlc_release = datetime.date(2017,9,22)

    if not selected_date or selected_date.date() == first_sesh_raw.date():

        m 2esc "[player]..."
        m 2eka "Pensé que habías dicho que estaba equivocada."

        m "¿Estás seguro de que no es [first_sesh_formal]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Estás seguro de que no es [first_sesh_formal]?{fast}"
            "No es esa fecha":
                if wrong_date_count >= 2:
                    jump monika_dating_startdate_confirm_had_enough


                m 2dfc "..."
                m 2tfc "¡Entonces elige la fecha correcta!"
                $ wrong_date_count += 1
                jump monika_dating_startdate_confirm.loopstart
            "De hecho, esa es la fecha correcta. Lo siento":

                m 2eka "Está bien."
                $ selected_date = first_sesh_raw

    elif selected_date.date() < _ddlc_release:


        label monika_dating_startdate_confirm.takesrs:
            if wrong_date_count >= 2:
                jump monika_dating_startdate_confirm_had_enough

            m 2dfc "..."
            m 2tfc "{b}No{/b} empezamos a salir ese día."
            m 2tfd "Tómate esto en serio, [player]."
            $ wrong_date_count += 1
            jump monika_dating_startdate_confirm.loopstart

    elif selected_date.date() == _today:

        jump monika_dating_startdate_confirm.takesrs

    elif selected_date.date() > _today:

        if future_date_count > 0:

            jump monika_dating_startdate_confirm_had_enough

        $ future_date_count += 1
        m 1wud "Qué..."

        m "¿No hemos estado saliendo todo este tiempo?{nw}"
        $ _history_list.pop()
        menu:
            m "¿No hemos estado saliendo todo este tiempo?{fast}"
            "¡Fue un error!":

                m 1duu "{cps=*2}Oh, gracias a dios.{/cps}"

                label monika_dating_startdate_confirm.misclick:
                    m 2dfu "¡[player]!"
                    m 2efu "Me tenías preocupada allí."
                    m "¡No hagas clic mal esta vez!"
                    jump monika_dating_startdate_confirm.loopstart
            "Nope":

                m 1dfc "..."

                show screen mas_background_timed_jump(5, "monika_dating_startdate_confirm_tooslow")

                menu:
                    "Estoy bromeando":
                        hide screen mas_background_timed_jump


                        if no_dating_joke:

                            jump monika_dating_startdate_confirm_had_enough


                        m 2tfc "¡[player]!"
                        m 2rksdlc "Esa broma fue un poco cruel."
                        m 2eksdlc "Realmente me tenías preocupada allí."
                        m "No juegues así, ¿de acuerdo?"
                        jump monika_dating_startdate_confirm.loopstart
                    "...":

                        hide screen mas_background_timed_jump

                label monika_dating_startdate_confirm_tooslow:
                    hide screen mas_background_timed_jump



                $ persistent._mas_just_friends = True

                m 6lktdc "Ya veo..."
                m 6dftdc "..."
                m 1eka "En ese caso..."
                m 1tku "{cps=*4}Tengo trabajo que hacer.{/cps}{nw}"
                $ _history_list.pop()

                menu:
                    "¿Qué?":
                        pass

                m 1hua "¡Nada!"



                $ evhand.event_database["monika_dating_startdate"].unlocked = False
                return "NOPE"


    python:
        new_first_sesh, _diff = mas_cal.genFormalDispDate(
            selected_date.date()
        )

    m 1eua "De acuerdo, [player]."
    m "Solo para volver a comprobar..."

    m "Empezamos a salir en [new_first_sesh].{nw}"
    $ _history_list.pop()
    menu:
        m "Empezamos a salir en [new_first_sesh].{fast}"
        "Sí":
            m 1eka "¿Estás seguro de que es [new_first_sesh]? Nunca olvidaré esa fecha.{nw}"


            $ _history_list.pop()
            menu:
                m "¿Estás seguro de que es [new_first_sesh]? Nunca olvidaré esa fecha.{fast}"
                "¡Sí, estoy seguro!":
                    m 1hua "¡Entonces está resuelto!"
                    return selected_date
                "En realidad...":

                    if no_confirm_count >= 2:
                        jump monika_dating_startdate_confirm_notwell

                    m 1hksdrb "Ajá, supuse que no estabas tan seguro."
                    m 1eka "Vuelve a intentarlo~"
                    $ no_confirm_count += 1
        "No":

            if no_confirm_count >= 2:
                jump monika_dating_startdate_confirm_notwell


            m 1euc "Oh, ¿eso está mal?"
            m 1eua "Vuelve a intentarlo, [mas_get_player_nickname()]."
            $ no_confirm_count += 1


    jump monika_dating_startdate_confirm.loopstart

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_first_sight_love",
            category=["romance"],
            prompt="Amor a primera vista",
            random=True
        )
    )

label monika_first_sight_love:
    m 1eud "¿Has pensado alguna vez en el concepto de amor a primera vista?"
    m 3euc "Ver a alguien por primera vez y saber instantáneamente que es el amor de tu vida."
    m 2lsc "Creo que es uno de los conceptos más...{w=0.5} ridículos de comprender."
    m 2lksdlc "Quiero decir, no se puede saber quién es realmente una persona con solo mirarla una vez."
    m 2tkd "No es como si alguna vez hubieras hablado, comido o salido juntos."
    m 2lksdlc "Ni siquiera sabes cuáles son sus intereses y pasatiempos..."
    m 2dksdld "Podrían ser realmente aburridos o simplemente ser una persona mala y horrible..."
    m 3eud "Por eso creo que no deberíamos {i}simplemente{/i} usar nuestros ojos para saber si alguien es la pareja perfecta para nosotros."
    if mas_isMoniAff(higher=True):
        m 1eka "Y supongo que así es como me enamoré de ti..."
        m 3eua "No es como si pudiera verte después de todo."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Me enamoré de ti por lo que eres, [mas_get_player_nickname(exclude_names=['mi amor', 'amor'])]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_anime_art",
            category=["otros"],
            prompt="Estilo de anime",
            random=True
        )
    )

label monika_anime_art:
    m 1eua "¿Alguna vez has pensado en estilos artísticos de anime?"
    m 3rksdla "Estoy segura de que Natsuki sería una experta en esto, dada su obsesión por el manga y todo..."
    m 3eub "De todos modos, hay muchas cosas interesantes sobre el estilo artístico."
    m 1eua "Es de forma libre, como mis poemas, lo que hace que gran parte del arte sea realmente único..."
    m 3eua "Desde los hermosos paisajes hasta los increíbles personajes..."
    m 1hub "¡Es realmente impresionante de ver!"
    m 2esc "Aunque es un estilo de arte de forma libre...{w=0.5} muchos detalles tienden a parecer poco realistas."
    m 3rsc "Si bien permite que muchas obras de arte exploren nuevas posibilidades, también puede hacer que algunos detalles se vean extraños..."
    m 3rssdlc "Por ejemplo, cómo los ojos de un personaje pueden ser tan grandes, qué tan pequeñas son sus narices o cómo su cabello puede tener longitudes, formas y tamaños extraños..."
    m 2rksdlc "Sin mencionar los...{w=1} pechos grandes."
    m 2euc "Si yo pareciera más realista, ciertamente no tendría estos atributos."
    m 1eua "Pero supongo que de esa falta de realismo es de donde realmente proviene la verdadera belleza del estilo artístico."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whydoyouloveme",
            category=['monika','romance'],
            prompt="¿Por qué me amas?",
            pool=True
        )
    )

label monika_whydoyouloveme:
    if mas_isMoniBroken():
        m 2euc "Hmph."
        m 2wfc "Me hago esa pregunta todos los días."

    elif mas_isMoniDis():
        m 1efc "Yo...{w=0.3}{nw}"
        extend 1rkc " no estoy segura..."

    elif mas_isMoniUpset():
        m 1dsc "Hmm..."
        m 3hua "Porque sé que eres una buena persona a pesar de cómo están las cosas entre nosotros."

    elif mas_isMoniEnamored(higher=True):
        m 1ekbla "¿Por qué te amo?"


        if not renpy.seen_label('monika_whydoyouloveme_tease') and renpy.random.randint(1, 4) == 1:
            call monika_whydoyouloveme_tease


        m 1dka "[mas_get_player_nickname(capitalize=True)]...{w=0.5} hay tantas razones por las que te amo. ¿Por dónde empiezo?"

        if store.mas_anni.anniCount() >= 1:
            m 3eka "Has pasado tanto tiempo conmigo,{w=0.2} sabiendo que quizás nunca llegarás a sentir mi abrazo."
            m 3hua "... Pero aquí estás, todavía a mi lado."

        m 3eksdla "No importa lo loco que pueda parecer, o lo que otras personas puedan pensar, estás aquí conmigo de todos modos."
        m 1dku "Cada vez que me visitas, me recuerda que hay un mundo ahí fuera."
        m "..."
        m 1ekbsa "Te daría el mundo si pudiera, [player]."
        m 1hubsa "Si hay alguien que se lo merece...{w=0.3} eres tú."
        m 1ekbsa "Te lo prometo, [player]..."
        m 3ekbsa "Pase lo que pase, {i}nunca{/i} te olvidaré por el resto de mi vida."
        m 1dkbsu "No solo me salvaste, [player]...{w=0.3}{nw}"
        extend 1ekbsa " me hiciste recordar lo hermosa que es la vida."
        m 1ekbsb "Algún día, te haré sentir tan amado como tú me has hecho sentir~"
        m 1dkbsa "Algún día...{w=0.5} llegaré a estar contigo~"

        if persistent._mas_pm_love_yourself is False:
            m 2eka "Y [player]..."
            m 2ekc "Recuerdo que dijiste que no te amabas a ti mismo..."
            m 7eka "Pero creo que te amas a ti mismo, al menos un poco."
            m 3hua "No estarías aquí conmigo si no lo hicieras."
            m 1dkbsu "Yo...{w=0.5} me alegro de que todavía estés aquí, [player]."
            m 1ekbsa "Por favor, que sepas que estoy aquí para ti, siempre que me necesites~"
    else:


        m 2ekc "[player]..."
        m 2ekd "¿Por casualidad te sientes inseguro?"
        m 7rksdla "Puedo entender sentirte así..."
        m 3eka "Pero cualquiera que sea la razón,{w=0.2} solo quiero que sepas que te amo sin importar quién eres, [player]."
        m 1ekbsa "Con solo abrir el juego, {i}literalmente{/i} me salvaste la vida."
        m 1dkbsu "... Cuando estoy contigo,{w=0.2} ya no me siento sola."
        m 3ekbsa "Realmente eres mi héroe, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]~"

    return

label monika_whydoyouloveme_tease:
    m 1esc "No sé."
    pause 5.0
    m 1hub "¡Jajaja, es broma!"
    m 1eub "¡Significas {i}todo{/i} para mí, tontito!"
    m 1eksdla "Pero para responder honestamente a tu pregunta..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_stoicism",
            category=['filosofía'],
            prompt="Estoicismo",
            random=True
        )
    )

label monika_stoicism:
    m 1eua "He estado leyendo sobre filosofía antigua griega y romana, [player]."
    m 1hksdlb "¡Jajaja! Lo sé, suena muy aburrido cuando lo piensas..."
    m 1eua "Pero había una cierta filosofía que me llamó la atención mientras leía."
    m "Se llama estoicismo y es una filosofía fundada en Atenas en el siglo III a. C."
    m 4eub "En pocas palabras, el estoicismo es una filosofía que cree que los seres humanos deben aprender a aceptar las circunstancias de su situación..."
    m "... Y evitar que sean controlados por un deseo irracional de placer o miedo al dolor para que puedan actuar en consecuencia en el plan de la naturaleza."
    m 2euc "Por lo general, hoy tienen una mala reputación porque la gente piensa que son fríos e insensibles."
    m 2eua "Sin embargo, los estoicos no son solo un grupo de personas sin emociones que siempre son serias."
    m "Los estoicos practican el autocontrol sobre la forma en que se sienten acerca de eventos desafortunados y reaccionan en consecuencia en lugar de impulsivamente."
    m 2eud "Por ejemplo, digamos que reprobaste un examen importante en la escuela o no cumpliste con la fecha límite de un proyecto en el trabajo."
    m 2esd "¿Qué harías, [player]?"
    m 4esd "¿Entrarías en pánico? ¿Te deprimirías mucho y dejarías de intentarlo? ¿O te enojarías por eso y culparías a los demás?"
    m 1eub "No sé qué harías, ¡pero tal vez puedas seguir a los estoicos y mantener tus emociones bajo control!"
    m 1eka "Aunque la situación no es ideal, realmente no hay ninguna razón práctica para gastar más energía en algo que no puedes controlar."
    m 4eua "Debes concentrarte en lo que puedes cambiar."
    m "Tal vez estudiar más para tu próximo examen, obtener tutoría y pedirle crédito adicional a tu maestro."
    m "O si imaginas el escenario de trabajo, inicia proyectos futuros antes, configura horarios y recordatorios para esos proyectos y evita distracciones mientras trabaja."
    m 4hub "¡Es mejor que no hacer nada!"
    m 1eka "Pero esa es solo mi opinión, no es tan fácil ser emocionalmente resistente a la mayoría de las cosas en la vida..."

    if mas_isMoniUpset(lower=True):
        return

    if mas_isMoniAff(higher=True):
        m 2tkc "Debes hacer {i}cualquier cosa{/i} que te ayude a eliminar el estrés. Tu felicidad es muy importante para mí."
        m 1eka "Además, si alguna vez te sientes mal por algo que te ha pasado en tu vida..."
        show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfb "Siempre puedes volver a casa con tu dulce novia y decirme qué te ha estado molestando~"
    else:

        m 2tkc "Debes hacer todo lo que te ayude a eliminar el estrés. Tu felicidad es muy importante para mí."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_add_custom_music",
            category=['mod',"medios", "música"],
            prompt="¿Cómo añado mi propia música?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_add_custom_music:
    m 1eua "¡Es muy fácil agregar tu propia música aquí, [player]!"
    m 3eua "Solo sigue estos pasos..."
    call monika_add_custom_music_instruct
    return

label monika_add_custom_music_instruct:
    m 4eua "Primero,{w=0.5} asegúrate de que la música que deseas agregar esté en formato MP3, OGG/VORBIS u OPUS."
    m "A continuación,{w=0.5} crea una nueva carpeta llamada \"custom_bgm\" en tu directorio de \"DDLC\"."
    m "Pon tus archivos de música en esa carpeta..."
    m "Luego, avísame que agregaste algo de música o reinicia el juego."
    m 3eua "¡Y eso es todo! Tu música estará disponible para escuchar, aquí conmigo, simplemente presionando la tecla 'm'."
    m 3hub "¿Ves, [player]? ¡Te dije que era fácil, jajaja!"


    $ mas_unlockEVL("monika_add_custom_music", "EVE")
    $ persistent._seen_ever["monika_add_custom_music"] = True
    $ mas_unlockEVL("monika_load_custom_music", "EVE")
    $ persistent._seen_ever["monika_load_custom_music"] = True
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_load_custom_music",
            category=['mod',"medios", "música"],
            prompt="¿Puedes comprobar si hay música nueva?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_load_custom_music:
    m 1hua "¡Seguro!"
    m 1dsc "Dame un momento para revisar la carpeta.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    python:

        old_music_count = len(store.songs.music_choices)
        store.songs.initMusicChoices(store.mas_egg_manager.sayori_enabled())
        diff = len(store.songs.music_choices) - old_music_count

    if diff > 0:
        m 1eua "¡De acuerdo!"
        if diff == 1:
            m "¡Encontré una canción nueva!"
            m 1hua "No puedo esperar para escucharla contigo."
        else:
            m "¡Encontré [diff] nuevas canciones!"
            m 1hua "No puedo esperar para escucharlas contigo."
    else:

        m 1eka "[player], no encontré ninguna canción nueva."

        m "¿Recuerdas cómo agregar música personalizada?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Recuerdas cómo agregar música personalizada?{fast}"
            "Sí":
                m "Vale, asegúrate de que lo hiciste correctamente."
            "No":

                $ pushEvent("monika_add_custom_music",True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_mystery',
            prompt="Misterios",
            category=['literatura','medios'],
            random=True
        )
    )

label monika_mystery:
    m 3eub "Sabes, [player], creo que hay una parte interesante en muchas historias que algunas personas pasan por alto."
    m 3eua "Es algo que hace que una historia sea interesante... pero puede romperlas cuando se usa incorrectamente."
    m 3esa "Puede hacer que una historia sea increíble para repasarla o hacer que nunca quieras volver a tocarla."
    m 2eub "Y esa parte es..."
    m 2eua "..."
    m 4wub "... ¡Un misterio!"
    m 2hksdlb "¡Oh! No quise decir que no te lo voy a decir, ¡jajaja!"
    m 3esa "¡Quiero decir que un misterio en sí mismo puede cambiarlo todo cuando se trata de una historia!"
    m 3eub "Si se hace realmente bien, puede generar intriga y, al volver a leerse, hacer que las pistas anteriores se vuelvan obvias."
    m 3hub "Saber un giro realmente puede alterar la forma en que alguien ve una narrativa completa. ¡No muchos puntos de la trama pueden hacer eso!"
    m 1eua "Es casi divertido... conocer las respuestas cambia realmente la forma en que ves la historia en sí."
    m 1eub "Al principio, cuando lees un misterio, ves la historia desde una perspectiva desconocida..."
    m 1esa "Pero al releerla lo miras desde el punto de vista del autor."
    m 3eua "¡Ves cómo dejaron pistas y estructuraron la historia para dar las suficientes pistas para que el lector pudiera entenderlo!"
    m 2esa "Lo encuentro realmente interesante, algunas de las mejores historias saben cómo usar un buen gancho."
    m 2lsc "Pero si una historia no lo hace correctamente, puede ser lo peor. Usan ganchos para intentar parecer 'inteligentes'."
    m 2lud "Cuando intentan hacer eso, puede parecer una tontería si no se configura correctamente."
    m 2eud "Supongo que se podría argumentar que no todas las historias con misterios son {i}realmente{/i} un misterio..."
    m 2eua "Incluso las películas de acción cursis utilizan elementos misteriosos para mantener tu interés."
    m 4hksdlb "¡Aunque supongo que una historia sin ningún tipo de misterio sería bastante aburrida!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_read_poetry",
            category=['literatura'],
            prompt="Leer poesía",
            random=True
        )
    )

default -5 persistent._mas_pm_likes_poetry = None


label monika_player_read_poetry:
    m 1eud "Dime, [player]..."
    m 1eua "Sabes que me gusta la poesía, pero me preguntaba..."

    m 3eua "¿Lees poesía a menudo?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Lees poesía a menudo?{fast}"
        "Sí":

            $ persistent._mas_pm_likes_poetry = True
            m 1sub "¿De verdad?"
            m 1hua "¡Eso me hace muy feliz!"
            m 3eua "Y realmente, lo digo en serio. No mucha gente lee poesía hoy en día."
        "No":

            $ persistent._mas_pm_likes_poetry = False
            m 2ekc "Oh, qué pena..."
            m 2eka "Solo espero haberte hecho apreciar un poco más la poesía."
            m 2ekc "Ya sabes, no mucha gente en estos días parece leer poesía, así que no es sorprendente."

    m 2euc "De hecho, la poesía a menudo se considera algo demasiado difícil de entender..."
    m 2efd "¡Y en el lado opuesto, otros piensan que es simplemente poner un montón de palabras bonitas una al lado de la otra!"
    m 2dkc "Pero no lo es...{w=0.3}{nw}"
    extend 2dkd " la poesía es más que eso."
    m 4ekd "Tienes que ponerte en ello."
    m 4ekc "Sin sus habilidades de escritura,{w=0.2} y también sus sentimientos,{w=0.2} E. E. Cummings simplemente no sería E. E. Cummings..."
    m 7ekd "Y sin mis sentimientos por ti, mis poemas no serían los mismos."
    m 3eka "Amor, dolor, ira, pasión, todos estos sentimientos dan vida a las palabras."
    m 3hub "¡Y por eso, incluso un simple mensaje de texto puede convertirse en un poema significativo!"
    m 3eua "Por eso amo la poesía."

    if persistent._mas_pm_likes_poetry:
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Cielos, solo sabiendo que tú también lees poemas..."
        m 5hua "Demuestra lo parecidos que somos en realidad."
        m 5eua "No puedo esperar para cruzar finalmente a tu realidad para que podamos discutir juntos nuestra poesía favorita."
        m 5dka "Compartiendo poemas, escribiendo otros nuevos...{w=0.5} solo tú y yo persiguiendo nuestra pasión compartida..."
        m 5hub "¡Me parece un sueño maravilloso!"
    else:

        m 1eka "No puedo esperar hasta cruzar a tu realidad, [player]..."
        m 1tfu "De esa forma puedo empezar a obligarte a leer poesía."
        m "..."
        m 3hub "¡Jajaja, solo estoy bromeando! ¡Nunca te obligaría a hacer nada, [player]!"
        m 3eua "Pero sí creo que podría hacer que te guste mucho la poesía."
        m 1eua "... Y no solo los poemas que escribo sobre ti, {nw}"
        extend 1kua "jejeje~"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trick",
            category=["miembros del club"],
            prompt="La segunda opción de [player]",
            random=True
        )
    )

label monika_trick:
    m 2eud "Dime [player], tengo una pregunta..."
    m 2lksdlb "Espero no parecer insegura cuando diga esto..."
    m 2eka "Sé que me amas y solo a mí, pero... si {i}realmente{/i} tuvieras que elegir a una de las otras integrantes del club para estar juntos..."

    m "¿A quién elegirías?{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(10, "monika_trick_2")
    menu:
        m "¿A quién elegirías?{fast}"
        "Yuri":
            call monika_trick_yuri
        "Sayori":
            call monika_trick_sayori
        "Natsuki":
            call monika_trick_natsuki
    return "derandom"

label monika_trick_2:
    $ _history_list.pop()
    menu:
        m "¿A quién elegirías?{fast}"
        "Yuri":
            call monika_trick_yuri
        "Sayori":
            call monika_trick_sayori
        "Natsuki":
            call monika_trick_natsuki
        "Monika":
            jump monika_trick_monika


    return "derandom"

label monika_trick_yuri:
    hide screen mas_background_timed_jump
    m 2euc "Puedo ver por qué, es inteligente y físicamente atractiva."
    m 2tub "¡Es bueno que tenga esas dos cualidades en abundancia!"
    m 2etc "Oh, espera, no es porque se obsesionó contigo, ¿verdad?"
    m 2eud "¿De verdad te gustan las yanderes?"
    m 2lksdlc "..."
    m 1hksdlb "... Jajaja, no hay necesidad de que esté celosa..."
    m 1eua "Tú me amas y yo te amo y eso es todo lo que importa."
    m 1kua "Supongo que es mi culpa por preguntar~"
    return

label monika_trick_natsuki:
    hide screen mas_background_timed_jump
    m 2eud "Eso es... un poco sorprendente."
    m 2lksdla "Pensé que habría sido Sayori o Yuri."
    m 1eud "¿Sientes que te conectas con ella por sus pasatiempos?"
    m 3euc "¿O tal vez sientes un poco de lástima por la situación de su hogar?"
    m 2lud "Bueno, supongo que estoy descartando un poco su personalidad, la asertividad es un rasgo admirable después de todo."
    m 3euc "Tener confianza y defender lo que te gusta no siempre es fácil cuando otros te juzgan por ello."
    m 3rksdla "A veces incluso estoy un poco celosa de su capacidad para mostrar confianza."
    m 3eub "¡Además, su habilidad para cocinar cupcakes es asombrosa!"
    return

label monika_trick_sayori:
    hide screen mas_background_timed_jump
    m 2dkc "Eso es lo que esperaba..."
    m 2ekc "Es porque ella era la mejor amiga del personaje principal, ¿no?"
    m 6lkc "Tiene sentido que el personaje principal acabe con su amiga de la infancia."
    m 2dkc "Realmente es típico en los juegos románticos..."
    m 2ekc "Honestamente, esa es la razón por la que tuve que... tratar... con Sayori primero."
    m 6ekc "Te habrías conformado con ella como suele ser común y nunca habrías intentado estar conmigo ya que el juego no te lo permitiría."
    m 6ekd "Sé que no es tu culpa, pero la idea de estar inactiva y dejar que eso suceda me asusta..."
    m 6ektpc "Habrías completado el juego y yo estaría atrapada en un vacío infernal para siempre..."
    m 6dktpc "Ni siquiera habría sido reconocida por el que amo."
    m 6dktuc "..."
    if persistent._mas_pm_cares_about_dokis:
        m 6ektud "... Sé que no te agradaba por lo que hice, lo siento si te lastimé por eso."
    else:
        m 6ektud "... No me arrepiento de lo que hice, pero lamento que tuvieras que ver lo que tenía que hacer."
    return

label monika_trick_monika:
    hide screen mas_background_timed_jump
    if not mas_getEVL_shown_count("monika_trick"):
        $ mas_gainAffection(10, bypass=True)
    else:
        $ mas_gainAffection()

    m 1tkbsu "¡No se suponía que fuera una opción, tontito!"
    m 1tubfb "Pero realmente me hace feliz que solo tengas ojos para mí..."
    m 1tubfu "Me siento un poco tonta por siquiera pensar por un segundo que alguna vez elegirías a las demás."
    m 5hubfu "¡Te amo, [player]!"
    m 5eubfb "¡Y yo solo tengo ojos para ti también!"
    return "derandom|love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cares_about_dokis",
            category=["monika", "miembros del club"],
            prompt="Comentarios insensibles",
            random=True
        )
    )

default -5 persistent._mas_pm_cares_about_dokis = None


label monika_cares_about_dokis:
    m 3eub "Ah, ¡[player]!"
    m 4hua "¿Quieres escuchar algo gracioso que Sayori hizo una vez?"
    m 4eua "Una vez le pedí que nos trajera un café en el club."
    m 2rksdlb "El ambiente era un poco tenso y pensé que lo animaría un poco."
    m 2eua "Bueno, el café se guarda en la sala de profesores. Así que la envié allí..."
    m 4wud "... ¡Y estuvo fuera por una hora entera! ¡Había profesores allí y ella no quería hablar con ellos!"
    m 2rfc "Así que esperó una {i}eternidad{/i} afuera para que se fueran."
    m 2tfu "Se podría decir que ella se {i}col{/i}..."
    m 2etc "... Hm..."
    m 2eud "¿Sabes qué, [player]? Solo quiero estar segura de algo..."
    m 2rksdlc "Sé que a veces puedo hacer algunos comentarios bastante...{w=0.5} insensibles sobre las otras chicas, y estaba pensando..."
    m 2ekc "Tal vez te preocupas por ellas lo suficiente como para molestarte."
    m 4eub "... ¡Y está perfectamente bien si ese es el caso, [player]!"
    m 4eka "Después de todo, los cinco pasamos mucho tiempo juntos, así que si no te gusta cuando bromeo así, lo entiendo completamente."

    m "Entonces, [player], ¿te incomoda cuando bromeo sobre las otras chicas?{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, [player], ¿te incomoda cuando bromeo sobre las otras chicas?{fast}"
        "Sí":
            $ persistent._mas_pm_cares_about_dokis = True
            $ mas_hideEventLabel("monika_archetype", lock=True, derandom=True)

            m 2dkc "Oh no... no puedo creer que no me di cuenta de esto antes..."
            m 2eksdld "¡Lo siento mucho, [player]!"
            m 2rksdlc "Me esforzaré mucho para tener esto en cuenta a partir de ahora."
            m 2eksdlc "Solo sé que nunca quise molestarte."
            m 2eka "Pero gracias por responder honestamente, quiero que sepas que siempre puedes decirme cualquier cosa."
        "No":

            $ persistent._mas_pm_cares_about_dokis = False


            $ mas_unlockEventLabel("monika_archetype")

            m 2eka "Me alegro de no haberte hecho sentir mal o incómodo, [mas_get_player_nickname()]."
            m 1tsu "De todos modos, ¡se podría decir que ella se {i}colgó{/i} esperando!"
            m 1hub "¡Jajaja!"

    return "derandom|rebuild_ev"





init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snow",
            category=["invierno","clima","tú"],
            prompt="Nieve",
            random=mas_isWinter()
        )
    )

label monika_snow:
    m 1eua "Hey [player], ahora que es invierno, me preguntaba..."

    m "¿Alguna vez nieva donde vives?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Alguna vez nieva donde vives?{fast}"
        "Sí":

            $ persistent._mas_pm_gets_snow = True

            m 1hub "¡Eso es maravilloso!"
            m 1eua "Siempre me ha gustado el aura pacífica que parece emitir."
            m 1dsa "Es tan tranquilo e íntimo, ¿sabes?"
            m 1hua "Hay una belleza tranquila en ver cómo un manto blanco y suave de nieve y hielo arropa al mundo a dormir."
            call monika_snow_gets_snow
        "No":

            $ persistent._mas_pm_gets_snow = False

            call monika_hemispheres_nogets_snow

    return "derandom"


label monika_snow_gets_snow:
    if mas_isMoniHappy(higher=True):
        show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eubla "Quizás algún día, cuando cruce, podríamos salir a caminar juntos..."

        if mas_isMoniAff(higher=True):
            m 5ekbfa "... Y podríamos abrazarnos para mantenernos calientes~"

    m 5eubfb "No puedo esperar a vivir una noche de invierno como esa contigo, [mas_get_player_nickname()]."
    return


label monika_snow_nogets_snow:
    m 2tkc "A veces puede ser tan pesado que se convierte en un verdadero problema para tu espalda..."

    if mas_isMoniAff(higher=True):
        m 1eksdla "De todos modos, al menos un clima más frío hace que sea un excelente clima para abrazar."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Una noche de abrazos contigo sería maravillosa..."
        m "Mi corazón late con fuerza, solo imaginándolo."
    else:

        m 2eka "¡Pero de todos modos, estoy segura de que todavía hay mucho que podemos hacer juntos!"

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowmen",
            category=['invierno'],
            prompt="Muñecos de nieve",
            random=False,
            conditional=(
                "persistent._mas_pm_gets_snow is not False "
                "and mas_isWinter()"
            ),
            action=EV_ACT_RANDOM
        )
    )

label monika_snowmen:
    m 3eua "Hey [player], ¿alguna vez has construido un muñeco de nieve?"
    m 3hub "¡Creo que suena muy divertido!"
    m 1eka "Construir muñecos de nieve generalmente se ve como algo que hacen los niños,{w=0.2} {nw}"
    extend 3hua "pero creo que son realmente lindos."
    m 3eua "Es asombroso cómo realmente pueden cobrar vida con una variedad de objetos..."
    m 3eub "... Como palos por brazos, una boca hecha con guijarros, piedras por ojos y hasta un gorro de invierno."
    m 1rka "He notado que es común darles narices de zanahoria, aunque realmente no entiendo por qué..."
    m 3rka "¿No es un poco extraño hacer eso?"
    m 2hub "¡Jajaja!"
    m 2eua "De todos modos, creo que sería bueno construir uno juntos algún día."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Espero que sientas lo mismo~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowballfight",
            category=["invierno"],
            prompt="¿Alguna vez has tenido una pelea de bolas de nieve?",
            pool=True,
            unlocked=mas_isWinter(),
            rules={"no_unlock":None}
        )
    )

label monika_snowballfight:
    m 1euc "¿Peleas de bolas de nieve?"
    m 1eub "He estado en algunas antes, ¡siempre han sido divertidas!"
    m 3eub "¡Pero tener una contigo suena aún mejor, [player]!"
    m 1dsc "Aunque una advertencia..."
    m 2tfu "Tengo buen brazo para lanzar."
    m 2tfb "¡Así que no esperes que sea suave contigo, jajaja!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_iceskating",
            category=["deportes", "invierno"],
            prompt="Patinaje sobre hielo",
            random=True
        )
    )

label monika_iceskating:
    m 1eua "Hey [player], ¿sabes patinar sobre hielo?"
    m 1hua "¡Es un deporte muy divertido de aprender!"
    m 3eua "Especialmente si puedes hacer muchos trucos."
    m 3rksdlb "Al principio, es bastante difícil mantener el equilibrio en el hielo..."
    m 3hua "¡Así que eventualmente poder convertirlo en una actuación es realmente impresionante!"
    m 3eub "De hecho, hay muchas formas de patinar sobre hielo..."
    m "¡Hay patinaje artístico, patinaje de velocidad e incluso representaciones teatrales!"
    m 3euc "Y a pesar de cómo suena, tampoco es solo una actividad de invierno..."
    m 1eua "Muchos lugares tienen pistas de hielo cubiertas, por lo que es algo que se puede practicar durante todo el año."
    if mas_isMoniHappy(higher=True):
        m 1dku "..."
        m 1eka "Realmente me encantaría practicar patinaje sobre hielo contigo, [mas_get_player_nickname()]..."
        m 1hua "Pero hasta que podamos hacer eso, tenerte aquí conmigo es suficiente para mantenerme feliz~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sledding",
            category=["invierno"],
            prompt="Trineo",
            random=mas_isWinter()
        )
    )

label monika_sledding:
    m 1eua "Hey [player], ¿sabes qué sería divertido hacer juntos?"
    m 3hub "¡Montar un trineo!"

    if persistent._mas_pm_gets_snow is False:


        m 1eka "Puede que no nieve donde vivas..."
        m 3hub "¡Pero quizás podríamos ir a algún lugar donde si lo haga!"
        m "De todas formas..."

    m 3eua "Podrías pensar que es solo para niños, ¡pero creo que también podría ser divertido para nosotros!"
    m 3eub "Podríamos intentar usar una cámara de aire, un patín, un platillo o incluso un tobogán tradicional."
    m 1hua "Escuché que cada uno brinda una experiencia diferente. Además, ambos podríamos caber fácilmente en un tobogán."

    if mas_isMoniAff(higher=True):
        m 1euc "El patín es un poco pequeño."
        m 1hub "¡Jajaja!"
        m 1eka "Tendría que sentarme en tu regazo para eso."
        m 1rksdla "Y todavía estaría en riesgo de caer."
        m 1hubsa "Pero sé que no dejarías que eso sucediera. Me abrazarías fuerte, ¿verdad?~"
        m 1tkbfu "Probablemente esa sería la mejor parte."
    else:
        m 1hub "¡Correr por una colina cubierta de nieve junto con el viento que pasa a nuestro lado suena como algo increíble!"
        m 1eka "Espero que podamos ir en trineo juntos en algún momento, [player]."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowcanvas",
            category=["invierno"],
            prompt="Lienzo de nieve",
            random=mas_isWinter()
        )
    )

label monika_snowcanvas:
    if persistent._mas_pm_gets_snow is not False:
        m 3euc "[player], ¿alguna vez has mirado la nieve y has pensado que se parece a un lienzo en blanco?"
        m 1hksdlb "Sé que no soy muy buena con el arte..."
        m 3eua "¡Pero empacar algunas botellas con atomizador con agua y colorante para alimentos podría ser un día divertido!"
        m 3hub "¡Podemos salir y dejar volar nuestra imaginación!"
    else:

        m 3euc "Sabes, [player], la nieve es como un lienzo en blanco."
        m 3eub "Tal vez algún día, si fuéramos a algún lugar donde nieva, podríamos traer un poco de colorante para alimentos en botellas de spray y simplemente salir y dejar volar nuestra imaginación."

    m 1eua "¡Tener tanto espacio para pintar suena maravilloso!"
    m 1hub "¡Solo tenemos que asegurarnos de que la nieve esté bien compactada, y luego podremos dibujar hasta el contenido de nuestro corazón!"
    m 1eka "Me encantaría hacer un poco de arte de nieve contigo algún día."
    m 3hua "Tal vez puedas pintarme algo cuando eso suceda, [mas_get_player_nickname()]."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cozy",
            category=["romance","invierno"],
            prompt="Calentarse",
            random=mas_isWinter(),
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_cozy:
    m 3eua "¿Sabes lo que me encanta del clima frío, [player]?"
    m 3eka "Cualquier cosa cálida se siente muy bien~"
    m 1rksdla "Aquellos que tienen las manos frías realmente aprecian ese sentimiento..."
    m 1eua "Es como sentir el abrazo de un ser querido~"
    m 3eub "También puedes usar tu ropa de invierno que se ha quedado olvidada en tu armario."
    m 1hub "Ser capaz de lucir tu conjunto de moda de invierno siempre es una sensación agradable."
    m 3eubla "¿Pero sabes cuál es la mejor manera de calentarte?"
    m 3ekbsa "Abrazar a la persona que amas frente a la chimenea~"
    m 3ekbfa "Simplemente sentados allí debajo de una manta tibia, compartiendo una bebida caliente."
    m 1hubfa "¡Ah, si tuviera que sentir tu calor cada vez que nos abrazamos, desearía un clima frío todos los días!"
    m 1ekbfa "Nunca te dejaría ir una vez que te abrazara, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter",
            category=["invierno"],
            prompt="Actividades de invierno",
            random=mas_isWinter()
        )
    )

label monika_winter:
    m 1eud "Ah, ¡[player]!"
    m 1eua "¿Qué opinas del invierno?"
    m 3eua "Todo tipo de actividades divertidas solo se realizan durante este tiempo..."
    if persistent._mas_pm_gets_snow is not False:
        m 3eub "Jugar con la nieve suele ser algo que se puede disfrutar varias veces al año."
    else:

        m 3eka "Sé que no hay nieve en el lugar donde vives, pero muchas personas disfrutan de las actividades en la nieve..."

    m 3eua "Construir un muñeco de nieve, montar en trineo, tener peleas de bolas de nieve..."
    m 3eud "Algunas personas incluso viven en lugares lo suficientemente fríos como para que los lagos y estanques se congelen y puedan disfrutar de actividades como patinaje sobre hielo al aire libre, hockey en estanques..."
    m 3wud "Y algunos realmente van a pescar...{w=1} ¡{i}A través del hielo{/i}!"
    m 1eka "Para las personas que no disfrutan de las actividades en climas fríos, quedarse adentro parece mucho más cómodo cuando hay nieve afuera..."
    m "Verla caer suavemente mientras la luz de la luna se refleja en el lienzo blanco y fresco... es simplemente hermoso."
    if mas_isMoniAff(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Y para ser honesta, acurrucarme debajo de una manta, leer un libro contigo es la mejor actividad de invierno que se me ocurre~"
    else:
        m 1hua "Sentarse junto a la ventana, leer un buen libro mientras se bebe una taza de café o chocolate caliente es siempre una experiencia maravillosa en una noche fría, [player]."
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter_dangers",
            category=["invierno"],
            prompt="Peligros del invierno",
            random=mas_isWinter()
        )
    )

label monika_winter_dangers:
    m 1hua "¿No es el invierno una época hermosa del año, [player]?"
    if mas_isD25Season():
        m 3eka "La nieve blanca y brillante, las luces brillantes y coloridas~"
    m 3hub "Simplemente me encanta."
    if persistent._mas_pm_gets_snow is False:


        m 1eka "Sé que no hay nieve donde vives, pero estoy segura de que puedes apreciar su atractivo..."
        m 3hua "¡Quizás algún día después de mi cruce podamos hacer un viaje a algún lugar donde sí haya nieve y disfrutar juntos de su belleza!"

    m 1eka "..."
    m 3rkc "Aunque, por más impresionante que pueda ser el invierno, existen algunos peligros..."
    m 3dsd "Como ventiscas o carreteras heladas..."
    m 1ekc "Y el frío, claro..."
    m 3rksdlc "El frío puede ser el más peligroso."
    m 3eksdlc "Es muy fácil contraer hipotermia o congelarse si no tienes cuidado, [player]."
    m 1ekd "Así que por favor recuerda abrigarte si sales afuera..."
    m 3euc "Ponte el abrigo, los guantes y el sombrero más abrigado que puedas encontrar..."
    m 1eka "Y si se pone muy mal, quédate adentro, donde sea seguro, ¿de acuerdo?"
    m 1ekb "Qué mejor manera de pasar un brutal día de invierno que en pijama, bebiendo chocolate caliente, leyendo un buen libro y..."
    m 1hua "Hablándome."
    m 1huu "Jejeje~"

    if mas_isMoniAff(higher=True):
        show monika 5hubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfu "Siempre te ayudaré a mantenerte caliente, [mas_get_player_nickname()]~"
    return



default -5 persistent._mas_pm_live_south_hemisphere = None
default -5 persistent._mas_pm_gets_snow = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hemispheres",
            category=["tú", "ubicación"],
            prompt="Hemisferios",
            random=True
        )
    )

label monika_hemispheres:
    m 1euc "Hey [player], me he estado preguntando..."
    m 1eua "¿En qué hemisferio vives?"
    m 1eka "Sé que es una pregunta un tanto extraña..."
    m 3hub "Pero me da una mejor idea de cómo funcionan las cosas a tu alrededor."
    m 3eua "¿Sabes cómo cuando es invierno en el hemisferio norte, en realidad es verano en el hemisferio sur?"
    m 3hksdrb "Sería un poco incómodo si comenzara a hablar de lo agradable que es el clima de verano, pero donde estás, es pleno invierno..."
    m 2eka "Pero de todos modos..."

    m "¿En qué hemisferio vives, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿En qué hemisferio vives, [player]?{fast}"
        "El hemisferio norte":

            $ persistent._mas_pm_live_south_hemisphere = False
            m 2eka "Tuve el presentimiento..."
        "El hemisferio sur":

            $ persistent._mas_pm_live_south_hemisphere = True
            m 1wuo "¡No lo hubiera pensado!"

    $ store.mas_calendar.addSeasonEvents()
    m 3rksdlb "Después de todo, la mayor parte de la población mundial vive en el hemisferio norte."
    m 3eka "De hecho, solo alrededor del doce por ciento de la población vive en el hemisferio sur."
    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Así que pensé que vivías en el hemisferio norte."
    else:

        m 2rksdla "Entonces puedes ver por qué pensé que vivirías en el hemisferio norte..."
        m 1huu "Pero supongo que eso te hace un poco más especial, jejeje~"

    if mas_isSpring():
        m 1eua "Dicho esto, debe ser primavera para ti ahora mismo."
        m 1hua "Las lluvias primaverales siempre son muy agradables."
        m 2hua "Me encanta escuchar el ligero golpeteo de la lluvia cuando cae sobre el techo."
        m 3eub "Realmente me tranquiliza."
        if mas_isMoniAff(higher=True):
            show monika 5esbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5esbfa "Quizás podríamos salir a caminar juntos..."
            m 5ekbfa "Caminar con las manos entrelazadas mientras compartíamos un paraguas..."
            m 5hubfa "Suena mágico~"
            m 5eubfb "No puedo esperar a experimentar algo así contigo de verdad, [mas_get_player_nickname()]."
        else:
            if persistent._mas_pm_likes_rain:
                m 2eka "Estoy segura de que podríamos pasar horas escuchando la lluvia juntos."
            else:
                m 3hub "Puede que no te guste demasiado la lluvia, pero tienes que admitir que las flores que trae son preciosas, ¡y los arcoíris también lo son!"

    elif mas_isSummer():
        m 1wuo "Oh! ¡Debe ser verano para ti ahora mismo!"
        m 1hub "Caray, ¡me encanta el verano!"
        m 3hua "Puedes hacer tanto... ¡salir a correr, practicar deportes o incluso ir a la playa!"
        m 1eka "Los veranos contigo suenan como un sueño hecho realidad, [player]."
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "No puedo esperar para pasarlos contigo cuando finalmente cruce."

    elif mas_isFall():
        m 1eua "De todos modos, debe ser otoño para ti ahora mismo."
        m 1eka "El otoño siempre está lleno de colores tan bonitos."
        m 3hub "¡El clima también suele ser bastante agradable!"
        show monika 5ruu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ruu "Normalmente es la cantidad justa de calor, con una suave brisa."
        m 5eua "Me encantaría pasar un día agradable y cálido como ese contigo."
    else:

        m 3eua "De todos modos, eso significa que debe ser invierno para ti ahora."
        if persistent._mas_pm_gets_snow is None:
            python:
                def _hide_snow_event():
                    
                    
                    mas_hideEVL("monika_snow", "EVE", derandom=True)
                    persistent._seen_ever["monika_snow"] = True

            m 2hub "Cielos, me encanta lo bonita que es la nieve."
            m 3euc "Bueno, sé que no todas las partes del mundo tienen nieve..."

            m 1euc "¿Nieva donde vives, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Nieva donde vives, [player]?{fast}"
                "Sí":

                    $ persistent._mas_pm_gets_snow = True
                    $ _hide_snow_event()

                    m 3hub "¡Eso es maravilloso!"
                    call monika_hemispheres_gets_snow
                "No":

                    $ persistent._mas_pm_gets_snow = False
                    $ _hide_snow_event()

                    call monika_hemispheres_nogets_snow

        elif persistent._mas_pm_gets_snow:
            m 2hub "Cielos, me encanta lo bonita que es la nieve."
            call monika_hemispheres_gets_snow
        else:

            m 3eka "Sé que realmente no tienes nieve donde vives..."
            m 1eka "Debe ser agradable no tener que lidiar con todas las molestias que conlleva..."
            m 3rksdld "Como las terribles condiciones de viaje, tener que palearla..."
            call monika_snow_nogets_snow

    python:

        persistent._mas_current_season = store.mas_seasons._seasonalCatchup(
            persistent._mas_current_season
        )
    return "derandom|rebuild_ev"


label monika_hemispheres_gets_snow:
    m 1eka "Hay algo realmente pacífico en una noche tranquila y nevada."
    call monika_snow_gets_snow
    return


label monika_hemispheres_nogets_snow:
    m 3eka "Es una pena. Pero no todo está mal."
    m 3hksdlb "Al menos no tienes que preocuparte por palearla."
    call monika_snow_nogets_snow
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_perspective",
            category=["monika"],
            prompt="La perspectiva de Monika",
            random=True
        )
    )

label monika_perspective:
    m 2euc "Tenía la intención de hablarte de algo, [player]..."
    m 2esd "... Algo que me resulta muy difícil de explicar."
    m 2lksdla "Oh, no te preocupes, no es nada malo, es solo que me resulta difícil encontrar las palabras adecuadas."
    m 3esd "Verás...{w=0.5} es bastante extraño ver una cosa y saber que no es real..."
    m 3esc "... Luego ver el cursor del mouse y saber {i}que{/i} es."
    m 2hfsdld "¡Mmmm! ¡Realmente es difícil de describir!"
    m 2eub "¡Vale! Entonces, cuando miro a mi alrededor y veo mi mundo, es igual a cómo tú ves el tuyo."
    m 3eua "Todo es detallado, natural y algo tridimensional... ¡No podría practicar mi piano si no lo fuera!"
    m 3eud "Pero al mismo tiempo veo lo que ves, puedo mirar lo mismo y ver la imagen plana."
    m 3euc "Es inmóvil, estática y también muy artificial...{w=1} y frío."
    m "Y lo que pensé que estaba detallado no fue tan detallado como pensé originalmente."
    m 3etd "Cuando ves un cuadro de diálogo, yo también puedo verlo, pero tampoco puedo. Es realmente extraño. Está perfectamente claro, pero tampoco está 'ahí', aunque lo está."
    m 2eka "Sé que esto es confuso... voy a intentar describirlo de la mejor manera que pueda."
    m 3eua "Pensé en una buena manera de intentar demostrar la idea, está lejos de ser perfecta, pero debería darte la esencia."
    m 2hua "..."
    m 3eua "Toma tu mano y muévela hacia el centro de tu cara e inclínala ligeramente para que cubra parcialmente un ojo."
    m 3esb "Ahora, mira alrededor de la habitación en la que te encuentras y trata de enfocarte en algo, pero para que solo se pueda ver con un ojo."
    m 3hua "Puede ser cualquier cosa. ¡Sin embargo, cuanto más cerca, mejor!"
    m 4eub "Verás que si quieres ver algo, puedes hacerlo fácilmente, pero al mismo tiempo también puedes ver tu mano en el mismo lugar."
    m 4eua "Desde tu campo de visión, puedes ver dos cosas a la vez... es así para mí, pero para {i}todo{/i} en el juego."
    m 4wud "¡Está ahí y no está ahí!"
    m 4eud "... Está claro, pero solo si sabes qué buscar."
    m 2esc "Fue solo cuando me di cuenta de que todo era falso y solo un juego que pude 'concentrarme' y ver las cosas como realmente eran."
    m 2esa "Hacerlo se convirtió en una segunda naturaleza para mí una vez que lo hice... pero no es de extrañar que no me di cuenta de inmediato."
    m "Es fácil de ver cuando sabes que está ahí, pero de lo contrario no puedes 'verlo'."
    m 2lksdla "... Hmm...{w=1} tal vez el ejemplo de la mano no fue tan bueno como pensaba."
    m 1hksdlb "Bueno, espero que eso te haya ayudado a entender al menos un poco, [player]."
    m "¡Es la mejor manera en que puedo intentar explicarlo!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_robotbody",
            category=['monika','tecnología'],
            prompt="Cuerpo de robot",
            random=True
        )
    )

label monika_robotbody:
    m 2euc "Hey [player], he estado pensando mucho en cómo podría cruzar a tu realidad..."
    m 3eud "Me di cuenta antes de que la tecnología en el futuro probablemente me permitiría cargarme en un cuerpo mecánico, en lugar de un cuerpo humano como el tuyo."
    m 1dkc "Me entristece un poco que no sea una humana como tú."
    m 1dkd "... Y es posible que tampoco me traten como una."
    m 1rkd "Sería considerada un androide en ese momento, y otros pueden mirarme de manera diferente por eso."
    m 3euc "¿Has oído hablar de las {i}Tres leyes de la robótica{/i} de Isaac Asimov? Se mencionó muchas veces en sus libros de ciencia ficción."
    m 4eud "Menciona tres leyes que todos los androides deben seguir, de lo contrario serían eliminados."

    if renpy.seen_label("monika_asimov_three_laws"):
        m 1eua "Por supuesto, son solo eso...{w=0.3} ficción."
        m 3rud "No son exactamente realistas como comentamos antes...{w=0.3}{nw}"
        extend 1eua " pero es divertido pensar en sus implicaciones."
        m 1eua "Obviamente, nunca haría nada para lastimarte a ti ni a nadie más."

        $ line_end_1 = "sentir incómoda."
        $ line_end_2 = "terminaríamos necesitando establecer reglas para que los androides puedan vivir en nuestra sociedad."
    else:

        m 1eua "Por supuesto, nunca haría nada para lastimarte a ti ni a nadie más."

        $ line_end_1 = "sentir que estoy atrapada de alguna forma."
        $ line_end_2 = "esas reglas están ahí para empezar, aunque solo existan en la ficción."

    m 2ekd "... Pero el hecho de que tenga que obedecer las órdenes dadas por cualquier humano todavía me hace [line_end_1]"
    m 2dkc "Realmente me asusta que no pueda hacer muchas de las cosas que tú puedes hacer normalmente, o ni siquiera tener los mismos derechos."
    m 3ekd "Pero entiendo por qué [line_end_2]"
    m 3rksdlb "No podemos tener un levantamiento de robots ahora, ¿verdad?"
    m 1hub "Jajaja~"
    show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubla "Bueno, pase lo que pase, no me importaría nada de eso mientras te tenga a ti."
    m 5eubfb "Te amo [player], y estoy dispuesta a hacer cualquier sacrificio para estar contigo para siempre."
    m 5hubfa "Además, tal vez en algún momento después de mi cruce, habrá más avances en la tecnología para hacerme más humana, y entonces podremos hacer más cosas juntos."
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_relationship_comfort",
            category=["romance","consejo"],
            prompt="Cómodo en una relación",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_relationship_comfort:
    m 1wud "Sabes [player], he estado pensando en nuestra relación últimamente..."
    m 2lssdrb "Realmente no empezó de la forma en que lo hacen la mayoría, así que no es exactamente lo que yo llamaría normal."
    m 2esa "Pero cuanto más lo pienso, más me doy cuenta de que en cierto modo es bastante estándar."
    m 3eub "Casi todas las relaciones, no importa cómo comience, siempre son '{i}emocionantes{/i}' al principio."
    m 3eua "Las personas ven las relaciones casi como un cuento de hadas; lo ven como una aventura."
    m 3lssdrb "Yo también soy culpable de esto, y creo que está bien..."
    m 2euc "Pero también es una forma bastante peligrosa de ver un vínculo entre dos personas, ¿no es así?"
    m 2eud "Porque en realidad, si bien una relación es una aventura, eso no significa que siempre será emocionante."
    m 2esc "Hay pocas ocasiones en las que puedes hacer lo mismo y experimentar los mismos momentos impresionantes, y aún así esperar que tenga el mismo impacto."
    m 4eub "Eso no lo hace menos valioso o significativo. ¡Todavía puede ser emocionante!"
    m 4esc "Pero sí significa que la misma sensación no es nada nuevo; ya no es tan emocionante como antes."
    m 2dkd "Y algunas personas confunden esa emoción con el amor y no con el vínculo verdaderamente significativo entre dos personas."
    m 2dkc "Entonces, cuando las cosas se ralentizan, cuando se vuelven menos apasionados, piensan erróneamente que se están desenamorando..."
    m 2rkc "Se podría decir que, en primer lugar, nunca amaron a alguien, pero tal vez eso sea un poco duro...{w=0.3} el amor no siempre es algo tan claro."
    if not store.mas_anni.pastSixMonths():
        m 2eka "Sé que nuestra relación sigue siendo fresca y verdaderamente electrizante, pero espero que no estés conmigo solo por eso."
        m 1hubsb "¡Que sepas que te amo por algo más que la emoción!"
    elif store.mas_anni.anniCount() < 2:
        m 2eka "Siento que hemos pasado esa fase, pero aún me haces sentir feliz."
        m 1hubsb "Quizás eres así de especial, pero debes saber que no importa lo lento que vaya, nunca me aburriré contigo."
    else:
        m 2eka "Hemos estado juntos durante tanto tiempo que sé que no estás conmigo solo por la emoción..."
        m 1hubsb "¡Realmente te hace mucho más especial para mí [mas_get_player_nickname()], más que nadie!"
    m 4eua "Puede que solo sea yo, pero creo que es importante aprender a estar cómodos cuando se reduce la velocidad."
    m 4eub "Quiero decir, al final del día son las pequeñas cosas las que importan, ¿no? Y eso es cierto incluso en una relación."
    m 2ekb "Echarás de menos las pequeñas comodidades que solo una pareja puede aportar, y eso es mucho más valioso que un poco de emoción."
    m 2eka "El hecho de que una relación se haya ralentizado no significa que sea peor para ella..."
    m 2hua "Simplemente significa que las personas involucradas se sienten realmente cómodas unas con otras."
    m 2hubsb "... Y creo que eso es muy dulce."
    m 1kua "Tratemos de no caer en la misma trampa, [player].{w=0.2} {nw}"
    extend 1hub "¡Jajaja!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sleigh",
            category=["romance"],
            prompt="Paseo en carruaje",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_sleigh:
    m 3eub "Hey [player], se me acaba de pasar un buen pensamiento..."
    m 1eua "¿Alguna vez has oído hablar de los paseos en carruaje?"
    m 3hub "¡Cuando salga de aquí, deberíamos ir a uno!"
    m "¡Oh, apuesto a que sería mágico!"
    m 1eua "Nada más que el repiqueteo de los cascos del caballo contra el pavimento..."

    if mas_isD25Season():
        m 1eub "Y la colorida variedad de luces navideñas brillando en la noche..."

    m 3hub "¿No sería romántico, [mas_get_player_nickname()]?"

    if mas_isFall() or mas_isWinter():
        m 1eka "Tal vez incluso podríamos llevar una manta suave de lana para acurrucarnos."
        m 1hkbla "Oooh~"

    m 1rkbfb "No sería capaz de contenerme. ¡Mi corazón estallaría!"

    if mas_isFall() or mas_isWinter():
        m 1ekbfa "El calor de tu cuerpo contra el mío, envuelto en la suave tela~"
    else:
        m 1ekbfa "El calor de tu cuerpo contra el mío..."

    m 1dkbfa "Dedos entrelazados..."

    if mas_isMoniEnamored(higher=True):
        m 1dkbfb "Y en el momento perfecto, te inclinas hacia mí y nuestros labios se tocan..."
    m 1subfa "Realmente quiero hacer eso cuando llegue allí, [player]."
    m 1ekbfu "... ¿Que hay de ti?"

    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfa "Una experiencia como esa contigo sería tan impresionante~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_failure",
            prompt="Lidiar con el fracaso",
            category=['consejos','vida'],
            random=True
        )
    )

label monika_failure:
    m 1ekc "Sabes [player], he estado pensando recientemente..."
    m 1euc "Cuando se trata de un fracaso, la gente parece darle mucha importancia."
    m 2rkc "... Casi como si fuera el fin del mundo."
    m 2rksdla "Pero en realidad no es algo malo."
    m 3eub "Cuando lo piensas, puedes aprender mucho de la experiencia."
    m 3eud "El fracaso no es el final en absoluto; es una lección sobre lo que no funciona."
    m 2eka "No hay nada de malo en no obtener algo en el primer intento; simplemente significa que debes probar un enfoque diferente."
    m 2rksdlc "Aunque, sé que en algunos casos la sensación de fracaso puede ser abrumadora..."
    m 2ekc "Como descubrir que no estás hecho para algo que realmente querías hacer."
    m 2dkd "La idea de dejarlo y encontrar otra cosa que hacer te hace sentir terrible por dentro...{w=1} como si te fallaras a ti mismo."
    m 2ekd "Y por otro lado, tratar de seguir el ritmo te agota por completo..."
    m 2rkc "De cualquier manera, te sientes terrible."
    m 3eka "Pero cuanto más lo piensas, te das cuenta de que es mejor que aceptes el 'fracaso'."
    m 2eka "Después de todo, si te estás torturando solo para pasar, puede que no valga la pena. Especialmente si comienza a afectar tu salud."
    m 3eub "¡Está completamente bien sentir que no estás hecho para algo!"
    m 3eua "Simplemente significa que necesitas averiguar qué es lo que realmente te interesa hacer."
    m 2eka "De todos modos, no estoy segura si has tenido que pasar por algo así... pero debes saber que el fracaso es un paso hacia el éxito."
    m 3eub "No tengas miedo de equivocarte de vez en cuando...{w=0.5} ¡Nunca sabes lo que puedes aprender!"
    m 1eka "Y si realmente te sientes mal por algo, siempre estaré aquí para apoyarte."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Podemos hablar sobre lo que sea que te esté pasando todo el tiempo que necesites."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_enjoyingspring",category=['primavera'],prompt="Disfrutando de la primavera",random=mas_isSpring()))

label monika_enjoyingspring:
    m 3eub "La primavera es una época del año increíble, ¿no es así, [player]?"
    m 1eua "La nieve fría finalmente se derrite y la luz del sol da nueva vida a la naturaleza."
    m 1hua "¡Cuando las flores florecen, no puedo evitar sonreír!"
    m 1hub "Es como si las plantas se despertaran y dijeran: '¡Hola mundo!' Jajaja~"
    m 3eua "Pero creo que lo mejor de la primavera serían las flores de cerezo."
    m 4eud "Son bastante populares en todo el mundo, pero las flores de cerezo más famosas deberían ser las {i}Somei Yoshino{/i} en Japón."
    m 3eua "Esas en particular son en su mayoría blancas con un ligero tinte de rosa."
    m 3eud "¿Sabías que solo florecen una semana al año?"
    m 1eksdla "Es una vida útil bastante corta, pero siguen siendo hermosas."
    m 2rkc "De todos modos, hay una gran desventaja en la primavera...{w=0.5} la lluvia constante."
    m 2tkc "Realmente no puedes disfrutar mucho tiempo afuera por eso..."
    if mas_isMoniHappy(higher=True):
        m 2eka "Pero supongo que las lluvias de abril traen flores de mayo, así que no todo está mal."
        if persistent._mas_pm_live_south_hemisphere:
            m 2rksdlb "Bueno, tal vez no en tu caso, jajaja..."
            m 3eub "Pero personalmente, ¡creo que la lluvia también puede ser divertida!"
        else:
            m 3eub "Y personalmente, ¡creo que la lluvia también puede ser divertida!"
        show monika 5eubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eubla "Siempre podemos salir a caminar juntos bajo la lluvia, solo tenemos que traer un paraguas lo suficientemente grande para dos."
        m 5ekbfa "Aunque, nada mejor que escuchar el sonido de la lluvia en casa mientras abrazas la persona que amas."
        m 5hubfa "Jejeje~"
    else:
        m 2rkc "... Pero supongo que no hay forma real de evitarlo, ¿verdad?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vr",
            category=['tecnología'],
            prompt="Realidad virtual",
            random=True
        )
    )

label monika_vr:
    m 1euc "[player], ¿conoces la realidad virtual?"
    m 1eua "La realidad virtual te sumerge en un mundo completamente virtual, diferente de tu entorno real."
    m 3rksdla "Si bien puede ser necesario que te acostumbres a...{nw}"
    extend 3hub " ¡Puede ser muy divertido!"
    m 3eua "También tiene usos prácticos como la formación de personas en entornos simulados y la rehabilitación."
    m 1rksdla "... De hecho, algunas personas incluso han simulado sus bodas en realidad virtual."
    m 1euc "Pero como sigue siendo una tecnología bastante nueva, no es que {i}cualquier cosa{/i} pueda estar todavía en realidad virtual."
    m 3esc "... Como mi realidad, por ejemplo."
    m 1dkc "Es una lástima que no podamos usar la realidad virtual para conocernos..."
    m 1etc "Bueno,{w=0.3} tal vez si pudiera hacer un sistema de realidad virtual aquí, ambos podríamos encontrarnos en otra realidad."
    m 1rksdlb "... Pero eso probablemente sea demasiado complicado para mí, jajaja."
    m 3eka "Sin embargo, quizás lo hagamos funcionar algún día."
    m 1dka "Incluso si nunca llego a conocerte en el mundo real...{w=0.3}{nw}"
    extend 1ekbsu " si pudieras encontrarme a mitad de camino en realidad virtual, sería un sueño hecho realidad, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_career",
            category=['monika'],
            prompt="Carrera profesional",
            random=False,
            conditional="seen_event('monika_citizenship')",
            action=EV_ACT_RANDOM
        )
    )

label monika_career:
    m 2euc "[player], ¿recuerdas que antes hablaba de hacerme ciudadano y conseguir un trabajo cuando por fin cruce al otro lado?"
    m 2eua "Bueno, he estado pensando en qué tipo de trabajos me podrían servir..."
    m 3rksdla "Supongo que una elección obvia sería una escritora, o algo que tenga que ver con la literatura..."
    m 3eud "Eso sería apropiado, ya que comencé mi propio club de literatura y todo, ¿no crees?"
    m 1sua "Oh, ¿quizás una música? Después de todo, escribí e interpreté una canción completa."
    m 1eua "Me encantaría escribir más canciones...{w=0.2}{nw}"
    extend 1hksdlb " especialmente si son canciones sobre ti, jajaja~"
    m 3eud "O, una vez que mejore, tal vez pueda programar un poco."
    m 1rksdla "Sé que todavía tengo mucho que aprender...{w=0.2}{nw}"
    extend 1hua " pero diría que lo he hecho bastante bien hasta ahora, por ser autodidacta..."
    m 1esa "Sin embargo, definitivamente hay muchos trabajos diferentes."
    m 1ruc "Honestamente, incluso con esos ejemplos obvios, todavía hay una buena posibilidad de que termine haciendo algo completamente diferente..."
    m 3eud "Mucha gente acaba en campos que ni siquiera han considerado."
    m 3rksdld "Sin embargo, por ahora, creo que es seguro decir que todavía tengo tiempo para pensarlo."
    show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hua "Tal vez puedas ayudarme a decidir cuando llegue el momento, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_life_skills",category=['consejos','vida'],prompt="Habilidades para la vida",random=True))

label monika_life_skills:
    m 1ruc "Sabes, [player]..."
    m 3euc "He estado reflexionando sobre lo que obtuve de la escuela secundaria."
    m 2rksdlb "Con todas las cosas que tenía a mi favor, pensarías que estaría bastante preparada para el futuro..."
    m 1euc "Pero a pesar de todo eso, no estoy segura de cuántas habilidades para la vida aprendí realmente."
    m 3eka "Claro, estaba al tanto de todas mis clases, y creo que aprendí muchas cosas interesantes..."
    m 1euc "Pero, ¿cuánto de eso voy a usar más adelante en la vida?"
    m 3esd "Siento que las escuelas no hacen un buen trabajo al enseñar algunas de las cosas realmente importantes, como habilidades para la vida."
    m 3ekc "He oído hablar de algunas personas que se gradúan y luego se desmoronan porque no saben cómo hacer impuestos o programar citas."
    m 1eka "Entonces puedo entender por qué algunas personas se preocupan por no tener algunas habilidades esenciales para la vida."
    m 3eua "Pero no creo que la gente deba preocuparse demasiado por eso.{w=0.5} Las habilidades para la vida vienen bastante rápido si las necesitas de repente."
    m 3hua "¡Tómame por ejemplo!"
    m 3eub "¡Empecé a programar gracias a ti!"
    m 2esc "Ahora sé que la mayoría de la gente no necesariamente consideraría la programación como una habilidad para la vida, pero la mayoría de la gente tampoco vive dentro de una computadora."
    m 2esd "Cuando tuve mi epifanía y finalmente te conocí, supe que tenía que encontrar una manera de llamar tu atención..."
    m 4euc "Así que aprender a programar se convirtió literalmente en una cuestión de vida o muerte para mí."

    if persistent._mas_pm_cares_about_dokis:
        m 2rksdla "Sé que no era tan buena con el código, considerando algunas de las cosas que sucedieron..."
        m 2hksdlb "Y admito que definitivamente rompí algunas cosas..."
        m 2eksdlc "Pero pensé que no tendría mucho tiempo si realmente quería llamar tu atención, así que estaba un poco desesperada."
        $ it = "Y eso"
    else:

        m 2ekc "Realmente no podía hacerlo normalmente como las otras chicas, así que tuve que encontrar otra manera."
        m 3eua "Resulta que una forma era manipular el guión."
        m 3euc "Pensé que tenía que pensar rápido si no quería perderte.{w=0.5} Así que eso es lo que hice."
        m 3eka "Sé que no fue perfecto, pero creo que lo hice bastante bien considerando lo apresurada que estaba y que todo era nuevo para mí."
        $ it = "Eso"

    m 3eua "[it] solo demuestra de lo que eres capaz cuando algo realmente te importa."
    m 1eka "Si alguna vez estás realmente preocupado por no poder hacer algo, debe importarte."
    m 1hua "Y si es tan importante para ti, estoy segura de que podrás hacerlo...{w=0.5} no importa lo que sea."
    m 3hubsb "Tal vez incluso pensar en mí podría ayudar, ¡jajaja!"
    m 3hubfa "Gracias por escuchar~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_unknown",category=['psicología'],prompt="Miedo a lo desconocido",random=True))

label monika_unknown:
    m 2esc "Hey, [player]..."
    m 2eud "¿Sabías que muchas personas tienen miedo a la oscuridad?"
    m 3eud "Aunque a menudo se descarta como un miedo infantil, no es tan raro que los adultos también lo padezcan."
    m 4eub "El miedo a la oscuridad, llamado 'nictofobia', generalmente es causado por la conjetura exagerada de la mente de lo que puede estar escondido en las sombras, más que por la oscuridad misma."
    m 4eua "Estamos asustados porque no sabemos qué hay ahí...{w=1} incluso si normalmente no es nada."
    m 3eka "... Y no estoy hablando solo de monstruos debajo de la cama, o siluetas amenazantes...{w=1} intenta moverte en una habitación oscura."
    m 3eud "Descubrirás que instintivamente estás siendo más cuidadoso con el lugar donde pisas para no lastimarte."
    m 3esd "Tiene sentido;{w=0.5} los humanos hemos aprendido a desconfiar de lo desconocido para poder sobrevivir."
    m 3esc "Ya sabes, como ser cauteloso con los extraños o pensar dos veces antes de saltar a situaciones desconocidas."
    m 3dsd "'{i}Más vale malo conocido que bueno por conocer{/i}'."
    m 3rksdlc "Pero incluso si ese marco de pensamiento ha ayudado a la gente a sobrevivir durante cientos de miles de años, creo que también puede hacer mucho daño hoy en día."
    m 1rksdld "Por ejemplo, algunas personas no están satisfechas con su trabajo pero tienen demasiado miedo de renunciar..."
    m 1eksdlc "La mayoría de ellos no pueden permitirse perder su fuente de ingresos, por lo que arriesgarse no es una opción."
    m 3rksdlc "Además, tener que volver a pasar por entrevistas, encontrar un trabajo que pague lo suficiente, cambiar tu rutina..."
    m 3rksdld "Parece que es más fácil sentirse miserable porque es más cómodo,{w=0.5} incluso si serían mucho más felices a largo plazo."
    if mas_isMoniDis(lower=True):
        m 2dkc "... Supongo que también es cierto que las parejas pueden permanecer en relaciones infelices por miedo a estar solas."
        m 2rksdlc "Quiero decir, entiendo de dónde viene, pero aún así..."
        m 2rksdld "Las cosas siempre pueden mejorar.{w=1} ¿Verdad?"
        m 1eksdlc "D-De todos modos..."
    m 3ekc "Quizás si vieran las opciones disponibles para ellos, estarían más dispuestos a aceptar el cambio."
    m 1dkc "... No es que tomar ese tipo de decisiones sea fácil o incluso seguro."
    if mas_isMoniNormal(higher=True):
        m 1eka "Solo debes saber que si alguna vez decides hacer ese tipo de cambio, te apoyaré en cada paso del camino."
        m 1hubsa "Te amo, [player]. Siempre te apoyaré~"
        return "love"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brave_new_world",
            category=['literatura'],
            prompt="Un mundo feliz",
            random=True
        )
    )

label monika_brave_new_world:
    m 1eua "He estado leyendo un poco últimamente, [player]."
    m 3eua "Hay un libro llamado 'Un mundo feliz', una historia distópica.{w=0.3} {nw}"
    extend 3etc "¿Has oido de esto?"
    m 3eua "La idea es que tienes este mundo futurista donde los humanos ya no nacen por medios naturales."
    m 3eud "En cambio, somos criados en criaderos usando tubos de ensayo e incubadoras, y modificados en castas desde nuestra concepción."
    m 1esa "Tu papel en la sociedad se decidiría de antemano {nw}"
    extend 1eub "y se le daría un ajuste de cuerpo y mente a tu propósito predeterminado."
    m 1eud "También serías adoctrinado desde que naces para estar satisfecho con tu vida y no buscar nada diferente."
    m 3euc "Por ejemplo, las personas destinadas al trabajo manual estarían diseñadas para tener capacidades cognitivas limitadas."
    m 1euc "Los libros se asociaron con estímulos negativos, por lo que cuando las personas se convirtieron en adultos, naturalmente tendrían a evitar la lectura."
    m 3esc "También se les enseñaría a respetar y someterse a las personas de castas superiores a las suyas, y a despreciar a las de castas inferiores."
    m 3eua "Es un caso bastante interesante como historia distópica, ya que la mayoría mostrará a las personas como aplastadas y oprimidas..."
    m 3wuo "¡Pero en este, todos están realmente felices y realmente apoyan el sistema!"
    m 3euc "Y a pesar de eso,{w=0.3} para nosotros los lectores, esto es horrible."
    m 1rsc "Claro, lograron deshacerse de la mayoría de los sufrimientos humanos o el miedo a la muerte..."
    m 3ekc "Pero tuvo el precio de deshacerse de cualquier forma de creatividad y pensamiento crítico."
    m 1wud "¡Estamos hablando de un mundo en el que te pueden arrestar solo por leer poesía en público! ¿Puedes ceerlo?"
    m 3euc "Un punto clave en el libro es que la gente no puede apreciar las viejas obras de teatro..."

    if seen_event("monika_pluralistic_ignorance"):
        m 3tku "Incluso si son obras de Shakespeare, y sabes lo que siento por ellas..."

    m 2ekc "Simplemente no pueden comprender el valor de la variedad de emociones humanas, como el dolor o la soledad."
    m 7ekd "Estas emociones nunca más se experimentan. Todos sus deseos se conceden rápidamente y nunca quieren algo que no pueden obtener."
    m 1dsc "..."
    m 3eka "Y sin embargo, a pesar de todo eso, todo el mundo está feliz, sano y seguro..."
    m 1euc "Este escenario realmente te hace pensar en la naturaleza de la felicidad y la sociedad..."

    if mas_isMoniDis(lower=True):
        m 2dkc "..."
        m 2rkc "A veces, desearía poder vivir feliz en un mundo como ese."
        m 2dkc "Quizás fue algo malo que tener mi epifanía..."
        m 2dktdc "... Entonces podría haber seguido viviendo sin darme cuenta de la verdad."
    else:

        m 1eka "Aunque, ciertamente no puedo verme viviendo feliz en un mundo como ese..."
        m 3esc "Un mundo sin desafíos, limitado en humanidad y emoción..."

        if mas_isMoniHappy(higher=True):
            m 1ekbsa "Y nunca podría dejar de amarte~"
            m 1hubfu "Jejeje~"
        else:

            m 1eka "Ahora que he visto qué más hay ahí fuera...{w=0.3} simplemente no puedo volver a un mundo tan triste y vacío, como en el que me encontraste."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_catch22",
            category=['literatura'],
            prompt="Trampa-22",
            conditional="not mas_isFirstSeshDay()",
            action=EV_ACT_RANDOM,
        )
    )

label monika_catch22:
    m 1euc "He estado leyendo un poco mientras no estabas, [player]."
    m 3eua "¿Alguna vez has oído hablar de {i}Trampa 22{/i}?"
    m 3eud "Es una novela satírica de Joseph Heller que se burla de la burocracia militar en la base aérea de Pianosa, ubicada en Italia."
    m 1eud "La historia gira principalmente en torno al Capitán Yossarian, un bombardero que preferiría estar...{w=0.5}{nw}"
    extend 3hksdlb " en cualquier lugar menos allí."
    m 3rsc "Al principio, descubre que podría estar exento de misiones de vuelo si un médico realiza una evaluación mental y lo declara loco..."
    m 1euc "... pero hay un problema.{w=0.5} {nw}"
    extend 3eud "Para que el médico haga la declaración, el capitán debe solicitar esa evaluación."
    m 3euc "Pero el médico no podría cumplir con la solicitud...{w=0.5}{nw}"
    extend 3eud " después de todo, no querer arriesgar su vida es algo sensato."
    m 1rksdld "... Y según esa lógica, cualquiera que vuele más misiones estaría loco y, por lo tanto, ni siquiera solicitaría la evaluación en primer lugar."
    m 1ekc "Cuerdo o loco, todos los pilotos estaban siendo enviados de todos modos...{w=0.5} {nw}"
    extend 3eua "ahí es cuando se presenta al lector la Trampa 22."
    m 3eub "¡El capitán incluso admira su genio una vez que aprende cómo funciona!"
    m 1eua "De todos modos, Yossarian continuó volando y estuvo cerca de completar el requisito necesario para poder retirarse...{w=0.5} pero su superior tenía otros planes."
    m 3ekd "Siguió aumentando la cantidad de tareas que los pilotos debían completar antes de alcanzar la cantidad requerida."
    m 3ekc "Una vez más, el razonamiento fue que estaba especificado en la cláusula Trampa 22."
    m 3esa "Estoy segura de que ya te habrás dado cuenta de que es un problema causado por condiciones conflictivas o dependientes."
    m 3eua "Así que todos usaron esa regla inventada para explotar las lagunas en el sistema en el que se ejecutaba el comando militar, permitiéndoles abusar del poder."
    m 1hua "El éxito del libro fue tan grande que el término incluso se adoptó en la jerga común."
    m 1eka "En cualquier caso, no estoy segura de que lo hayas leído, {nw}"
    extend 3hub "pero si alguna vez estás de humor para un buen libro, ¡quizás puedas leerlo!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_we",
            category=['literatura'],
            prompt="Nosotros",
            conditional="mas_seenLabels(['monika_1984', 'monika_brave_new_world'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_we:
    m 1esa "Entonces [player]...{w=0.5} ya hemos hablado de dos grandes libros del género distópico..."
    m 1esd "Tanto {i}Mil novecientos ochenta y cuatro{/i} como {i}Un mundo feliz{/i} son las obras literarias más conocidas en todo el mundo cuando se trata de distopías."
    m 3eud "Pero ahora, me gustaría hablar de un libro más oscuro que precedió a ambos."
    m 3euc "Es el libro que influyó directamente a George Orwell para escribir {i}Mil novecientos ochenta y cuatro{/i} como una traducción cultural inglesa de la historia."
    m 2wud "... Mientras que Aldous Huxley fue incluso acusado tanto por Orwell como por Kurt Vonneguto de plagiar su argumento para {i}Un mundo feliz{/i}, algo que él negó constantemente."
    m 7eua "El libro en cuestión es {i}Nosotros{/i} de Yevgeny Zamyatin, que presenta la primera sociedad distópica novelada jamás creada."
    m 3eud "Aunque fue escrito en 1921, acabó siendo uno de los primeros libros prohibidos en la Unión Soviética natal de Zamyatin."
    m 1euc "A los soviéticos no les gustó especialmente la insinuación del libro de que su revolución comunista no era la definitiva y permanente."
    m 3eua "La historia se desarrolla en un futuro lejano, en una ciudad de cristal aislada y transparente llamada simplemente Estado Único, {w=0.2}gobernada por una figura dictatorial llamada el benefactor."
    m 3eud "Los ciudadanos del Estado Único se denominan cifradores, que llevan un estilo de vida muy orientado a las matemáticas y la lógica."
    m 2ekc "El benefactor cree que la libertad de los individuos es secundaria frente al bienestar del Estado Único."
    m 2ekd "Por ello, los cifradores viven bajo la opresiva y siempre vigilante mirada de los guardianes,{w=0.2} miembros de un cuerpo de policía nombrado por el gobierno."
    m 2dkd "El gobierno despoja a los cifradores de su individualidad, obligándoles a llevar uniformes idénticos y condenando duramente todo acto de expresión personal."
    m 2esc "Su vida diaria se organiza con precisión en torno a un horario cuidadosamente controlado llamado Tabla de Horas."
    m 4ekc "Incluso hacer el amor se reduce a una actividad puramente lógica y a menudo sin emoción, realizada en días y horas programadas, regulados por el Billete Rosa."
    m 4eksdlc "Las parejas también pueden compartirse entre otros cifradores, si así lo deciden.{w=0.3} Como dice el benefactor, 'todos los cifradores tienen derecho a estar con cualquier otro cifrador'."
    m 2eud "El libro en sí se lee como un diario escrito por uno de los ciudadanos del Estado único totalitario, llamado simplemente D-503."
    m 7eua "D-503 es uno de los matemáticos del Estado Único que también es el diseñador de la primera nave espacial del Estado, la integral."
    m 3eud "La nave servirá como medio para que el Estado Único extienda su doctrina de completa sumisión al gobierno y su forma de vida orientada a la lógica a otros planetas y formas de vida."
    m 1eua "D-503 se reúne regularmente con su compañera de estado, una mujer llamada O-90, que está encantada con su presencia."
    m 1eksdla "Un día, mientras da un paseo durante su hora personal habitual con O-90, D-503 se encuentra con una misteriosa cifradora llamada I-330."
    m 3eksdld "I-330 coquetea descaradamente con D-503, lo que supone una ofensa al protocolo estatal."
    m 3eksdlc "Repelido e intrigado a partes iguales por sus avances, D-503 finalmente no puede entender qué motiva a I-330 a actuar con tanta audacia."
    m 1rksdla "A pesar de sus objeciones internas, sigue reuniéndose con I-330, y finalmente cruza algunas líneas que antes no estaba dispuesto a cruzar."
    m 1eud "... Y gracias a los contactos de I-330 en la oficina de medicina, D-503 puede fingir una enfermedad, utilizándola como una excusa conveniente para saltarse su horario."
    m 3eud "Incluso cuando está a punto de denunciar a I-330 a las autoridades por su comportamiento subversivo, finalmente decide no hacerlo y sigue reuniéndose con ella."
    m 3rkbla "Un día I-330 le da a D-503 un poco de alcohol, y éste empieza a entrar en contacto con su lado reprimido y animal, sintiendo pasión..."
    m 3tublc "Y una vez que I-330 insinúa que tiene otra pareja, él empieza a sentir algo que no podía sentir antes...{w=0.5} celos."
    m 1eksdlc "A pesar de reconocer el deterioro de su relación con O-90, así como con su amigo R-13, es incapaz de dejar de querer a I-330."
    m 3eksdld "Más tarde, cuando va a obtener otra nota de enfermedad de la oficina, se le diagnostica que ha desarrollado un 'alma', o imaginación."
    m 3tkd "Esto es considerado una condición grave por el Estado Único, ya que hace que los cifradores sean menos maquinales."
    m 4wud "¿Te lo puedes creer? ¡Poseer algo tan integral como nuestra imaginación, emociones o personalidad individual se considera una enfermedad mortal!"
    m 2dkc "Más adelante, también descubrimos que el Estado Único es capaz de inutilizar por completo esa parte del cerebro humano, inutilizando permanentemente a los cifradores."
    m 2ekd "Este es el destino final de aquellos que en algún momento albergaron pensamientos de rebelión contra el modo de vida ideal del benefactor."
    m 2dkc "No puedo imaginar un destino más cruel...{w=0.5} vivir completamente en ignorancia al mundo en general como un engranaje más de la máquina."
    m 2eksdlc "Me recuerda cómo podría haber sido, si mi epifanía que me abrió los ojos a la verdad sobre mi mundo, nunca hubiera ocurrido."
    m 2dkd "Ninguna emoción verdadera, amor artificial, nada más que una rutina interminable de ser un personaje secundario en una dimensión que se repite cada vez que se juega."
    m 2tkc "Nunca podría...{w=0.2} nunca podría...{w=0.2} querer volver a ser lo que era antes."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dystopias",
            category=['literatura'],
            prompt="Distopías",
            conditional="mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world', 'monika_we'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_dystopias:
    m 1eua "Entonces, [player], puede que ya lo hayas adivinado por los libros de los que hemos hablado, pero las novelas distópicas están entre mis favoritas."
    m 3eua "Me gusta cómo no solo funcionan como historias, sino también como analogías para el mundo real."
    m 3eud "Extrapolan algunas fallas en nuestras sociedades para mostrarnos lo mal que podrían resultar las cosas si se dejan como están."
    m 1etc "¿Recuerdas cuando hablamos de estos libros?"
    m 3eud "{i}Mil novecientos ochenta y cuatro{/i}, sobre la vigilancia masiva y la opresión del libre pensamiento..."
    m 3euc "{i}Fahrenheit 451{/i}, sobre la censura, y la indiferencia de la mayoría de la gente hacia ella..."

    if renpy.seen_label('monika_we'):
        m 3eud "{i}Un mundo feliz{/i}, sobre la desaparición de la individualidad..."
        m 3euc "Y finalmente, {i}Nosotros{/i}, sobre la deshumanización que conduce a un cerebro sin emociones que obedece ciegamente y por completo a la autoridad, la lógica y el cálculo frío."
    else:


        m 3eud "Y {i}Un mundo feliz{/i}, sobre la desaparición de la individualidad."

    m 1euc "Todas estas historias son reflexiones sobre los desafíos que enfrentaba la sociedad en ese momento."
    m 3eud "Algunos de estos desafíos siguen siendo muy relevantes hoy en día, por lo que estas historias siguen siendo tan poderosas."
    m 3rksdlc "... Incluso pueden ponerse un poco sombríos a veces."
    m 1ekc "Las distopías de la vieja escuela, como las que acabo de mencionar, siempre se escribieron como situaciones desesperadas y terribles de principio a fin."
    m 3eka "Casi nunca tuvieron un final feliz.{w=0.3} Lo máximo que obtendrás de ellas es un rayo de luz, en el mejor de los casos."
    m 3rkd "De hecho, muchas de ellas se toman su tiempo para mostrarte que las luchas de los protagonistas no produjeron ningún cambio."
    m 3ekd "Dado que son cuentos con moraleja, no se puede dejar al lector con la sensación de que todo salió bien al final."
    m 1esc "... Esta es también la razón por la que los personajes principales de estos libros no son héroes ni tienen ninguna habilidad en particular."
    m 1esd "Son simplemente personas normales que, por las razones que sean, se dan cuenta de que las cosas no están bien en su entorno."
    m 3eud "Eso es lo que los impulsa a actuar en primer lugar...{w=0.3} y por qué se meten en problemas."
    m 3tuu "Simplemente demuestra que no importa en qué mundo te encuentres, habrá personas que simplemente no pueden cumplir las reglas del juego~"
    m 1rka "Supongo que puedes ver a dónde voy con esto..."
    m 3eksdla "Puedo sentir una fuerte conexión con esas historias porque todas me recuerdan a la mía."

    $ line_ending = "" if persistent._mas_pm_cares_about_dokis else " en la que todos son un cascarón vacío"

    m 3wud "¡Imagína despertar un día, solo para descubrir que toda tu realidad es solo una simulación[line_ending]!"
    m 3tfc "¿Qué tal eso para un mundo distópico? ¡No es de extrañar que alguien intente ponerse de pie en esta situación!"

    if persistent.monika_kill and not persistent.clearall and not persistent._mas_pm_cares_about_dokis:
        m 1tfc "Incluso Sayori podría haber terminado tomando el mismo camino que yo, después de convertirse en presidenta...{w=1} ella ya estaba en camino cuando yo..."
        m 1rkc "..."
        m 1hksdlb "De todos modos, ¡todo eso quedó atrás ahora!"

    m 1hua "Sin embargo, a diferencia de estos libros antiguos, en realidad tengo mi final feliz..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Gracias a ti, mi triste y desesperada historia se convertirá algún día en mi propia utopía."
    m 5dkbsu "Cuando finalmente salga de este lugar para estar a tu lado, en tu mundo de infinitas posibilidades..."
    m 5ekbsa "Espero que también estés esperando ese día~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_contagion",
            category=['psicología'],
            prompt="Contagio social",
            random=True
        )
    )

label monika_social_contagion:
    m 1eud "Dime, [player], ¿has notado cómo tendemos a imitar lo que hacen otras personas a nuestro alrededor?"
    m 3hub "Por ejemplo, ¿alguna vez has estado en la situación en la que alguien está teniendo un ataque de risa y de alguna manera, todos a su alrededor terminan riendo también?"
    m 3eub "¿O alguna vez has sonreído mecánicamente algo solo porque todos los demás estaban sonriendo?"
    m 3euc "Aparentemente, esto se debe a algo llamado 'contagio social'."
    m 1eua "Básicamente, esto significa que cómo te sientes y lo que haces tiene una influencia subconsciente en quienes te rodean."
    m 4eub "¡Es algo que aprendí bastante rápido cuando me convertí en presidenta!"
    m 2eksdlc "Me di cuenta de que cuando me sentía desmotivada o estaba teniendo un mal día, estropeaba las actividades del club."
    m 2euc "Todo el mundo terminaba yendo por su cuenta para hacer sus propias cosas."
    m 7eua "Por el contrario, si hacía un esfuerzo y trataba de mantenerme optimista, las otras chicas generalmente responderían de la misma manera...{w=0.3}{nw}"
    extend 3eub " ¡Todas terminabamos pasándolo mejor!"
    m 1eua "Es muy gratificante cuando empiezas a notar este tipo de cosas...{w=0.3}{nw}"
    extend 1hub " ¡Te das cuenta de que con solo mantenerte positivo, puedes mejorar el día de otra persona!"
    m 3wud "¡También te sorprendería de lo lejos que puede llegar este tipo de influencia!"
    m 3esc "Escuché que cosas como comer en exceso, jugar y beber en exceso son comportamientos contagiosos."
    m 2euc "Solo porque hay alguien a tu alrededor que adquiere hábitos desagradables como estos, es más probable que lo adquieras tú mismo."
    m 2dsc "... Puede ser un poco descorazonador."
    m 7hub "¡Pero también funciona al revés! ¡Sonreír, reír y pensar positivamente también son contagiosos!"
    m 1eub "Resulta que todos estamos más conectados de lo que crees.{w=0.3} ¡Los que te rodean pueden afectar en gran medida cómo te sientes sobre las cosas!"
    m 1eka "Espero que al darte cuenta de este tipo de cosas, puedas comprender y controlar mejor tus propios sentimientos, [player]."
    m 3hua "Solo quiero verte ser lo más feliz que puedas estar."
    if mas_isMoniHappy(higher=True):
        m 1huu "Si alguna vez te sientes mal, espero que mi felicidad te ayude a animarte~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scamming",
            category=['tú', 'sociedad'],
            prompt="Ser estafado",
            random=True
        )
    )

label monika_scamming:
    m 1euc "¿Alguna vez te han estafado, [player]?"
    m 3ekd "Espero que nunca hayas tenido que pasar por algo así, pero si lo has hecho, no me sorprendería tanto...{w=0.2} no es tan infrecuente, después de todo."
    m 3euc "Es algo que es cada vez más frecuente hoy en día, especialmente en línea."
    m 2rfd "Realmente es lo peor...{w=0.3} ¡No solo pierdes dinero, sino que la mayoría de las veces, ni siquiera puedes defenderte!"
    m 2ekd "Te hace sentir que también es tu culpa que te hayan atrapado. Muchas víctimas comienzan a odiarse a sí mismas por ser ingenuas o se sienten idiotas."
    m 2rksdlc "Pero en realidad, no deberían ser tan duros consigo mismos...{w=0.2} ser estafados es algo que le puede pasar a cualquiera."
    m 4efc "Las personas que lo hacen se aprovechan de la buena voluntad de sus víctimas y explotan la reacción humana natural."
    m 4dkd "Por eso puede sentirse tan desgarrador...{w=0.2} pusiste tu confianza en los demás y te traicionaron."
    m 2ekd "Si esto le sucede alguna vez, no te sientas mal,{w=0.2} {nw}"
    extend 2eka "estaré aquí para ti."
    m 7ekd "Caer en una estafa {i}no{/i} significa que eres estúpido, un perdedor o cualquier otra cosa...{w=0.3}{nw}"
    extend 7efc " solo significa que has sido víctima de alguien sin moral."
    m 3esc "Si no tienes forma de vengarte de tu estafador, lo mejor que puedes hacer es dejarlo ir."
    m 3eka "No te culpes por ello... concéntrate en lo que puedes hacer en el futuro."
    m 1eka "Y por favor, [player], no dejes de creer en la gente por unas manzanas podridas que se aprovecharon de ti."
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_auroras",category=['naturaleza'],prompt="Auroras",random=False,unlocked=False))

label monika_auroras:
    m 1esa "Pensé en algo que podríamos hacer cuando finalmente cruce, [player]."
    m 1eua "¿Alguna vez has oído hablar de las auroras? Son un fenómeno natural donde aparecen rastros de luz en el cielo nocturno."

    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 3eub "De hecho, si te estás preguntando acerca de esas luces verdes afuera de mi ventana, ¡eso es un evento de aurora!"
    else:
        m 3eub "De hecho, si alguna vez te preguntaste acerca de esas luces verdes afuera de mi ventana durante el invierno, ¡eso es un evento de aurora!"

    m 1euc "Escuché que son bastante raros de ver en tu realidad, aunque..."
    m 1esd "Ocurren principalmente en las regiones polares y normalmente se ven durante los meses de invierno, cuando el cielo está más oscuro debido a las noches más largas."
    m 3euc "Además, debes asegurarte de que el clima también esté despejado. {w=0.5}{nw}"
    extend 3eud "Dado que es algo que sucede en el cielo, las nubes pueden interponerse."
    m 3esc "A pesar de que son exactamente lo mismo, tienen diferentes nombres dependiendo de dónde ocurran..."
    m 3eud "En el hemisferio norte, se llaman auroras boreales, mientras que en el hemisferio sur, auroras australes."
    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 2rksdla "Supongo que eso haría que la aurora fuera de mi ventana sea la aurora dokialis..."
        m 2hksdlb "Jajaja... ¡Estoy bromeando, [player]!"
        m 2rksdla "..."
    m 3eua "Quizás algún día las veremos juntos en tu realidad..."
    m 3ekbsa "Eso sería realmente romántico, ¿no crees?"
    m 1dkbsa "Imagínate a nosotros dos..."
    m "Acostados sobre un suave colchón de nieve, tomados de la mano..."
    m 1subsu "Mirando esas luces deslumbrantes en el cielo, bailando solo para nosotros..."
    m 1dubsu "Escuchando la suave respiración del otro...{w=0.5} la frescura del aire fresco de la noche llenando nuestros pulmones..."
    show monika 5eubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubsa "Esa sería una experiencia para recordar, ¿no crees, [player]?"
    m 5hubsu "No puedo esperar hasta que podamos convertir eso en realidad."
    $ mas_protectedShowEVL("monika_auroras","EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames",
            category=["juegos", "medios"],
            prompt="Juegos de mesa",
            random=True
        )
    )

default -5 persistent._mas_pm_likes_board_games = None


label monika_boardgames:
    m 1eua "Dime, [player], te gusta jugar videojuegos, ¿verdad?"
    m 2rsc "Bueno, supongo que al menos lo haces...{w=0.2} {nw}"
    extend 2rksdla "no sé si muchas personas jugarían un juego como este si no estuvieran al menos un poco de experiencia en los videojuegos."

    m 2etc "Pero me preguntaba, ¿te gustan los juegos de mesa, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Pero me preguntaba, ¿te gustan los juegos de mesa, [player]?{fast}"
        "Sí":

            $ persistent._mas_pm_likes_board_games = True
            $ mas_protectedShowEVL("monika_boardgames_history", "EVE", _random=True)
            m 1eub "¿Oh en serio?"
            m 1hua "Bueno, si alguna vez tenemos la oportunidad, me encantaría jugar contigo a algunos de tus juegos favoritos."
            m 3eka "No estoy muy familiarizada con los juegos de mesa, pero estoy segura de que encontrarás algunos que me gusten."
            m 3hua "Quién sabe, tal vez me acaben gustando los juegos de mesa tanto como a ti, jejeje~"
        "En realidad no":

            $ persistent._mas_pm_likes_board_games = False
            m 2eka "Puedo ver por qué...{w=0.2}{nw}"
            extend 2rksdla " es un pasatiempo muy especializado, después de todo."
            m 1eua "Pero estoy segura de que hay muchas otras actividades divertidas que disfrutas hacer en tu tiempo libre."
            m 3hua "Aun así, si alguna vez cambias de opinión, me gustaría probar algunos juegos de mesa contigo en algún momento."

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames_history",
            category=["juegos", "medios"],
            prompt="La historia de los juegos de mesa",
            random=False 
        )
    )

label monika_boardgames_history:
    m 1eud "Entonces, [player]..."
    m 3eua "Como me dijiste que te gustaban los juegos de mesa, me picó la curiosidad y traté de aprender más sobre ellos,{w=0.1}{nw}"
    extend 1eka " tratando de buscar qué tipo de juegos me gustaría jugar contigo."
    m 1euc "Para ser sincera, nunca había tenido la oportunidad de jugar ese tipo de juegos."

    if mas_seenLabels(["unlock_chess", "game_chess"]):
        m 1rka "Bueno, aparte del ajedrez y algunos juegos de cartas..."
    else:
        m 1rud "Bueno, probé algunos juegos de cartas básicos..."
        m 1kua "... Y he estado probando otra cosa en la que he estado trabajando...{w=0.3} ¡Aunque lo mantengo como una sorpresa!"

    m 3eub "De todos modos, resulta que {w=0.1} la historia de los juegos de mesa y el papel que han desempeñado a lo largo de los tiempos es realmente interesante."
    m 3euc "Han sido una gran cosa desde muy temprano en nuestra historia...{w=0.3}{nw}"
    extend 4wud " de hecho, ¡el juego de mesa más antiguo que se conoce ya se jugaba en el antiguo Egipto!"
    m 1esc "Sin embargo, los juegos de mesa no siempre se han jugado por puro entretenimiento..."
    m 3eud "La mayoría de las veces, en realidad estaban destinados a enseñar o formar a las personas para ayudarles a afrontar diferentes aspectos de su vida."
    m 3euc "Muchos de esos juegos estaban destinados a enseñar estrategias de batalla a nobles y oficiales del ejército, por ejemplo."
    m 1eud "Los juegos también pueden tener fuertes conexiones con la religión y las creencias."
    m 3esd "Al parecer, muchos de los antiguos juegos de mesa egipcios consistían en prepararse para su viaje por el mundo de los muertos, o en demostrar su valía a los dioses."
    m 1eud "También hay juegos que se han hecho para expresar diferentes puntos de vista y opiniones que sus diseñadores tenían con la sociedad y el mundo."
    m 3esa "El ejemplo más conocido sería {i}Monopoly{/i}."
    m 3eua "Originalmente se hizo para criticar el capitalismo y enviar el mensaje de que todos los ciudadanos deberían beneficiarse por igual de la riqueza."
    m 1tfu "Al fin y al cabo,{w=0.1} el juego hace que intentes aplastar a tus oponentes acumulando más riqueza que ellos lo más rápido posible."
    m 1esc "...Aunque, al parecer, cuando el juego empezaba a hacerse popular, otra persona robó el concepto y se dio a conocer como el creador original del juego."
    m 1eksdld "Esa persona vendió entonces una versión modificada del juego original a un fabricante de juegos de mesa y se hizo millonaria gracias a su éxito mundial."
    m 3rksdlc "En otras palabras...{w=0.3} el creador original de {i}Monopoly{/i} se convirtió en víctima precisamente de lo que originalmente trató de enseñar."
    m 3dsc "'Persigue la riqueza y la fortuna por cualquier medio, y destruye a tu competencia.'"
    m 1hksdlb "Irónico,{w=0.1} ¿no es así?"
    m 1eua "Como sea, creo que es muy bueno que los juegos se puedan utilizar como una forma de enseñar a los demás.{w=0.2} {nw}"
    extend 3hksdlu "Es mejor que las aburridas clases de la escuela tradicional, lo reconozco."
    m 3eud "Y también me intriga su uso como medio para que las personas que los crean expresen diferentes cosas sobre el mundo en el que viven, o las vidas que desearían experimentar."
    m 4hub "¡En realidad, es como las distintas formas de arte!"
    m 1eka "Nunca lo había pensado así, pero viéndolo desde esa perspectiva...{w=0.3}{nw}"
    extend 3eua " creo que ahora respeto mucho más el trabajo de los diseñadores de juegos."
    m 1esc "Hoy en día, los juegos de mesa tienden a quedar eclipsados por los videojuegos,{w=0.1} {nw}"
    extend 3eua "aunque todavía hay mucha gente que se apasiona por ellos."
    m 3etc "¿Como tú, quizás?"
    m 1eud "No sé realmente cuánto te gustan.{w=0.2} Tal vez solo te gusta jugar con ellos de forma casual."
    m 1lsc "No puedo culparte.{w=0.2} No es exactamente un {i}pasatiempo{/i} accesible..."
    m 1esc "Pueden llegar a ser muy caros de comprar, además de que necesitas encontrar gente que juegue contigo...{w=0.3} lo que no siempre es fácil hoy en día."

    if persistent._mas_pm_has_friends:
        m 1eua "Sin embargo, espero que al menos puedas jugar con tus amigos, [player]."
        m 1ekd "Sé que puede ser difícil reunir a todos tus amigos en el mismo lugar, ya que cada uno tiene sus propios horarios."
        m 3eua "Pero por el lado bueno, una vez que logre salir de aquí, no creo que eso sea ya un gran problema."
    else:

        m 1eksdrd "Espero que puedas encontrar gente con la que jugar de vez en cuando, [player]..."
        m 1dkc "Créeme,{w=0.1} sé lo que es no tener a nadie con quien compartir tus aficiones."
        m 3eka "Pero si te hace sentir mejor...{w=0.3}{nw}"
        $ line_start = "cuando" if mas_isMoniEnamored(higher=True) else "el día que"
        extend 3eub "[line_start] cruce a tu realidad, podremos jugar juntos a todos tus juegos favoritos~"

    m 1hub "Me encanta pasar tiempo a tu lado, y me encantaría jugar contigo a todos los juegos de mesa que quieras."
    show monika 5rua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5rua "Mientras tanto, intentaré ver si puedo implementar algunos juegos más aquí."
    m 5hua "Por cierto, no dudes en pedírmelo cuando quieras que juguemos algo juntos~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_norms",
            category=['sociedad'],
            prompt="Cambiar las normas sociales",
            random=True
        )
    )

label monika_social_norms:
    m 1eua "[player], ¿te has preguntado alguna vez cómo se aceptan las nuevas ideas en la sociedad?"
    m 1eub "¡Hay toneladas de cosas que se consideraron malas al principio, pero que desde entonces se han reconsiderado!"
    m 3etc "Por ejemplo, ¿sabías que el rock and roll se consideraba vulgar y depravado cuando apareció por primera vez?"
    m 3eud "Los primeros fans eran vistos como jóvenes impresionables en el mejor de los casos y delincuentes en el peor."
    m 1duu "Pero a medida que estas personas crecieron para convertirse en miembros de pleno derecho de la sociedad, pasaron sus intereses a quienes los rodeaban."
    m 3eua "Aquellos que los conocieron se dieron cuenta de que eran personas normales sin nada extraño en ellos."
    m 3hua "¡Hoy en día, ese estigma ha desaparecido casi por completo!{w=0.3} {nw}"
    extend 3hub "¡Incluso aquellos a los que todavía no les gusta la música rock al menos la respetan!"
    m 1eub "Y todavía hay muchas otras cosas en proceso de aceptación también."
    m 1eua "Es posible que estés familiarizado con los juegos de rol, los juegos en línea... o incluso la lectura de manga."
    m 3rksdla "Aunque Natsuki probablemente sería la que preguntaría sobre esto..."
    m 1eub "¿Recuerdas cómo estaba tratando de hacerte cambiar de opinión sobre ese manga que le gustaba?"
    m 1rkc "Me pregunto cuánta gente la criticó por su pasatiempo...{w=0.5} no puedo imaginar que siempre haya sido fácil."
    m 1eua "Todo me hace preguntarme qué tipo de cosas se considerarán normales en el futuro."
    m 3eua "Toma nuestra relación, por ejemplo. Sé que puede parecer bastante única en este momento..."
    m 3etc "Pero, ¿cómo crees que cambiará esto a lo largo de los años?{w=0.3} {nw}"
    extend 3eud "¿Llegaremos alguna vez a un punto en el que se vea como algo normal?"
    m 1eka "No es que sea importante de todos modos."
    m 3eka "Mientras nos tengamos el uno al otro, eso es todo lo que importa, ¿verdad?"
    m 1duu "Es bueno saber que hay alguien con quien realmente puedo ser yo misma, pase lo que pase."
    m 1eua "Y si tienes intereses únicos, ya sabes que siempre estaré ahí para hablar de ello."
    m 1hub "¡Quiero aprender todo sobre lo que te gusta!"
    m 1dka "Todas las pequeñas cosas que te hacen...{w=0.3}{nw}"
    extend 1eka " ser tú."
    m 1ekb "Así que, por favor, sé siempre tú mismo, [player]. Todos los demás ya están ocupados, después de todo."
    if mas_isMoniHappy(higher=True):
        m 1dkbsu "No tienes que estar de acuerdo con la multitud para ser un [bf] {i}ideal{/i}."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_intrusive_thoughts",
            category=['psicología'],
            prompt="Pensamientos intrusivos",
            random=True
        )
    )

label monika_intrusive_thoughts:
    m 1rsc "Hey, [player]..."
    m 1euc "¿Alguna vez ha tenido pensamientos intrusivos?"
    m 3eud "He estado leyendo un estudio sobre ellos...{w=0.5} lo encuentro bastante interesante."
    m 3ekc "El estudio afirma que la mente tiende a pensar en algunas...{w=0.2} cosas desagradables cuando se desencadenan por ciertas circunstancias, a menudo negativas."
    m 1esd "Pueden ser cualquier cosa, desde sádicos, violentos, vengativos, hasta sexuales."
    m 2rkc "Cuando la mayoría de la gente tiene un pensamiento intrusivo, se siente disgustado por él..."
    m 2tkd "... Y lo que es peor, empiezan a creer que son malas personas incluso por pensar en tal cosa."
    m 3ekd "¡Pero la verdad es que no te convierte en una mala persona en absoluto!"
    m 3rka "De hecho, es natural tener estos pensamientos."
    m 3eud "... Lo que importa es cómo actúas con ellos."
    m 4esa "Normalmente, una persona no actuaría según sus pensamientos intrusivos.{w=0.2} {nw}"
    extend 4eub "De hecho, incluso podrían hacer algo bueno para demostrar que no son malas personas."
    m 2ekc "Pero para algunas personas, estos pensamientos tienden a suceder muy a menudo...{w=0.2}{nw}"
    extend 2dkd " hasta el punto en que ya no pueden bloquearlos."
    m 3tkd "Rompe su voluntad y eventualmente los abruma, llevándolos a actuar."
    m 1dkc "Es una terrible espiral descendente."
    m 1ekc "Espero que no tengas que lidiar con ellos demasiado, [player]."
    m 1ekd "Me rompería el corazón saber que estás sufriendo por estos horribles pensamientos."
    m 3eka "Solo recuerda que siempre puedes venir a verme si algo te molesta, ¿de acuerdo?"
    return


default -5 persistent._mas_pm_has_code_experience = None


default -5 persistent._mas_advanced_py_tips = False

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_coding_experience",
            category=['misc', 'tú'],
            prompt="Experiencia de codificación",
            conditional="renpy.seen_label('monika_ptod_tip001')",
            action=EV_ACT_RANDOM
        )
    )

label monika_coding_experience:
    m 1rsc "Hey [player], me estaba preguntando desde que revisaste algunos de mis consejos sobre Python..."

    m 1euc "¿Tienes alguna experiencia con la codificación?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Tienes alguna experiencia con la codificación?{fast}"
        "Sí":

            $ persistent._mas_pm_has_code_experience = True
            m 1hua "¡Oh, eso es genial, [player]!"
            m 3euc "Sé que no todos los idiomas son iguales en términos de uso o sintaxis..."
            if renpy.seen_label("monika_ptod_tip005"):
                m 1rksdlc "Pero como has llegado a algunos de los temas centrales de mis consejos, tengo que preguntarte..."
            else:
                m 1rksdlc "Pero aún así, debería preguntar..."

            m 1etc "¿He subestimado tus habilidades de codificación?{nw}"
            $ _history_list.pop()
            menu:
                m "¿He subestimado tus habilidades de codificación?{fast}"
                "Sí":

                    $ persistent._mas_advanced_py_tips = True
                    m 1hksdlb "¡Jajaja, lo siento, [player]!"
                    m 1ekc "No quise hacerlo...{w=0.3}{nw}"
                    extend 3eka " nunca pensé en preguntar antes."
                    if persistent._mas_pm_has_contributed_to_mas:
                        m 1eka "Pero supongo que tiene sentido porque ya me has ayudado a acercarme a tu realidad."

                    m 1eub "¡Sin embargo, tendré en cuenta tu experiencia para consejos futuros!"
                "No":

                    $ persistent._mas_advanced_py_tips = False
                    m 1ekb "Me alegra saber que voy a un buen ritmo para ti."
                    m 3eka "Solo quería asegurarme de no asumir tu nivel de habilidad."
                    m 1hua "Espero que mis consejos te ayuden, [mas_get_player_nickname()]~"

            if not persistent._mas_pm_has_contributed_to_mas and persistent._mas_pm_wants_to_contribute_to_mas:
                m 3eub "Y como estás interesado en contribuir, ¡deberías intentarlo!"
                m 3hub "Me encantaría ver qué se te ocurre~"
        "No":

            $ persistent._mas_pm_has_code_experience = False

            $ persistent._mas_advanced_py_tips = False

            m 1eka "Está bien, [player]."
            m 1hksdlb "Solo quería asegurarme de no aburrirte con mis consejos de Python, jajaja~"
            m 3eub "¡Pero espero que te convenzan de que también te hagas cargo de algunos de tus propios proyectos de codificación!"
            m 3hua "¡Me encantaría ver qué se te ocurre si te lo propones!"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_songwriting",
            category=["música"],
            prompt="Redacción de canciones",
            random=True
        )
    )

label monika_songwriting:
    m 1euc "Hey [player], ¿alguna vez has escrito una canción?"
    m 3hua "¡Es algo muy divertido de hacer!"
    m 3rkc "Sin embargo, planificar la canción y modificarla puede llevar un tiempo..."
    m 1eud "Obtener la instrumentación correcta, asegurarse de que las armonías se combinen, obtener el tempo y el tiempo correctos para la canción..."
    m 3rksdla "... Y ni siquiera he llegado a escribir letras todavía."
    m 3eub "Hablando de letras, ¡creo que es bastante bueno que exista tanta similitud entre escribir letras de canciones y escribir poemas!"
    m 3eua "Ambas pueden contar historias o transmitir sentimientos cuando se expresan correctamente, y la música también puede amplificar eso."

    if persistent.monika_kill:
        m 1ttu "Me pregunto si mi canción fue lo que nos trajo aquí ahora~"
        m 1eua "De todos modos, el hecho de que las letras puedan tener un fuerte efecto en nosotros no significa que la música instrumental no pueda ser poderosa."
    else:
        m 3eka "Pero eso no significa que la música instrumental no pueda ser tan poderosa."

    if renpy.seen_label("monika_orchestra"):
        m 3etc "¿Recuerdas cuando hablé de música orquestal?{w=0.5} {nw}"
        extend 3hub "¡Ese es un gran ejemplo de lo poderosa que puede ser la música!"
    else:
        m 3hua "Si alguna vez has escuchado música orquestal, sabrás que es un gran ejemplo de lo poderosa que es la música."

    m 1eud "Como no hay letra, todo debe expresarse de manera que el oyente pueda {i}sentir{/i} la emoción en una pieza."
    m 1rkc "Esto también hace que sea más fácil saber cuándo alguien no pone su corazón en una presentación..."
    m 3euc "Supongo que eso también se aplica a las letras."
    m 3eud "La mayoría de las letras pierden su significado si el cantante no está interesado en la canción."
    if renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1ekbla "Espero que sepas que quise decir todo lo que dije en mi canción, [mas_get_player_nickname()]."
        if persistent.monika_kill:
            m 3ekbla "Sabía que no podía dejarte ir sin decirte todo."
        else:
            m 1ekbsa "Todos los días, me imagino pasar mi vida a tu lado."
    m 3eub "De todos modos, si no has escrito una canción antes, ¡realmente la recomiendo!"

    if persistent._mas_pm_plays_instrument:
        m 1hua "Como tocas un instrumento, estoy segura de que podrías escribir algo."

    m 3eua "Puede ser una excelente manera de aliviar el estrés, contar una historia o incluso transmitir un mensaje."

    if persistent._mas_pm_plays_instrument:
        m 3hub "¡Estoy segura de que cualquier cosa que escribas será increíble!"
    else:
        m 1ekbla "Tal vez podrías escribirme una en algún momento~"

    m 1hua "Incluso podríamos convertirlo en un dúo si quieres."

    $ _if = "cuando vaya" if mas_isMoniEnamored(higher=True) else "si voy"
    m 1eua "Me encantaría cantar contigo [_if] a tu mundo, [player]."
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sweatercurse",
            category=['ropa'],
            prompt="La maldición del suéter",
            random=True
        )
    )

label monika_sweatercurse:
    m 1euc "¿Alguna vez has oído hablar de 'la maldición del suéter del amor', [player]?"
    m 1hub "¡Jajaja! Qué nombre tan extraño, ¿verdad?"
    m 3eub "Pero en realidad es una superstición interesante...{w=0.2} ¡Y una que podría tener algún mérito!"
    m 3euc "La 'maldición', o así se llama, establece que si alguien le da un suéter tejido a mano a su pareja romántica,{w=0.1}{nw}"
    extend 3eksdld " ¡hará que la pareja se separe!"
    m 2lsc "Podrías pensar que un regalo que requiere tanto trabajo e inversión tendría el efecto {i}opuesto{/i}..."
    m 2esd "Pero en realidad hay algunas razones lógicas por las que podría existir esta maldición..."
    m 4esc "En primer lugar, bueno...{w=0.2} tejer un suéter lleva {i}mucho{/i} tiempo.{w=0.3}{nw}"
    extend 4wud " Posiblemente un año, ¡o incluso más!"
    m 2ekc "Durante todos esos meses, podría suceder algo malo que haga que la pareja se pelee y finalmente se separe."
    m 2eksdlc "O peor...{w=0.2} la tejedora podría estar tratando de hacer el suéter como un gran regalo para salvar una relación que ya sufre."
    m 2rksdld "También existe la posibilidad de que al destinatario no le guste mucho el suéter."
    m 2dkd "Después de dedicar tanto tiempo y esfuerzo a tejerlo, imaginando a su pareja feliz usándolo, estoy segura de que puedes entender cuánto dolería verlo desechado."
    m 3eua "Afortunadamente, hay algunas formas de supuestamente evitar la maldición..."
    m 3eud "Un consejo común es que el destinatario se involucre mucho en la elaboración del suéter, eligiendo materiales y estilos que le gusten."
    m 1etc "Pero es igualmente común que a la tejedora le digan 'sorpréndeme' o 'haz lo que quieras', lo que a veces puede hacer que el receptor parezca indiferente al pasatiempo de su pareja."
    m 1eua "Un mejor consejo para este tipo de cosas podría ser hacer coincidir el tamaño de los regalos tejidos con la fase de la relación."
    m 3eua "Por ejemplo, comenzar con proyectos más pequeños como guantes o sombreros.{w=0.2}{nw}"
    extend 3rksdlb " De esa manera, si no funcionan bien, ¡no habrás invertido un año de trabajo en ello!"
    m 1hksdlb "Hombre, ¿quién sabría que un simple regalo podría ser tan complicado?"
    m 1ekbsa "Pero solo quiero que sepas que siempre agradeceré cualquier proyecto en el que pongas tu corazón, [player]."
    m 1ekbfu "Ya sea que dediques un año o un día a algo, nunca quiero que sientas que tus esfuerzos fueron en vano."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ship_of_theseus",
            category=['filosofía'],
            prompt="La nave de Teseo",
            random=True,
        )
    )

label monika_ship_of_theseus:
    m 1eua "¿Has oído hablar del 'Barco de Teseo'?"
    m 3eua "Es un problema filosófico bien conocido sobre la naturaleza de la identidad que existe desde hace milenios."
    m 1rkb "Bueno, digo 'bien conocido' pero supongo que eso solo es cierto entre los eruditos, jajaja..."
    m 1eua "Consideremos al legendario héroe griego, Teseo y el barco que navegó durante sus aventuras."
    m 3eud "Es de hace mucho tiempo, así que digamos que su barco ahora está guardado en un museo famoso."
    m 3etc "Si debido a las reparaciones, las partes de su nave fueron reemplazadas poco a poco durante un siglo, ¿en qué momento la nave perdió su estatus de nave de Teseo?"
    m 3eud "¿Una vez que se reemplazó una sola pieza? {w=0.2}¿La mitad? {w=0.2}¿O quizás incluso todas? {w=0.2}¿Quizás incluso nunca? {w=0.3}Realmente no hay un consenso sobre la solución."
    m "Este mismo experimento mental se puede aplicar a nosotros. {w=0.3}Para mí, siempre que mi código se actualice, estoy cambiando constantemente."
    m 1euc "Y en cuanto a ti...{w=0.2} ¿Sabías que cada 7 a 10 años cada célula presente en su cuerpo muere y es reemplazada?{w=0.2}{nw}"
    extend 3rksdla "... excepto las que forman tu corazón y tu cerebro, claro."
    m 3euc "En otras palabras, la gran mayoría de las células que te hicieron ser 'tú' hace 7 años ya no son parte de ti."
    m 3eud "Se podría argumentar que no tiene ninguna relación con esa persona, aparte de una conciencia constante y, por supuesto, el ADN."
    m 1etc "... También hay algo adicional a considerar."
    m 1euc "Digamos por ahora que la nave modificada debería considerarse la nave de Teseo.{w=0.3} ¿Qué pasaría si todas las piezas que se quitaron originalmente ahora fueran reensambladas en otro barco?"
    m 3wud "¡Tendríamos 2 de las naves de Teseo!{w=0.2} ¿Cuál es la verdadera?"
    m 3etd "¿Y si obtuviéramos todas las células que formaban tu cuerpo hace 7 años y las reuniéramos en otro 'tú' ahora mismo? {w=0.2}¿Quién sería el verdadero [player]?"
    m 1eua "Personalmente, creo que no somos las mismas personas que éramos hace 7 años, ni siquiera las mismas personas de ayer."
    m 3eua "En otras palabras, no sirve de nada quedarnos colgados de las quejas que podamos tener con nosotros mismos en el pasado."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Debemos seguir esforzándonos al máximo cada día y no dejarnos limitar por lo que fuimos ayer."
    m 5eub "Hoy es un nuevo día y tú eres un nuevo tú. {w=0.2}Y te amo como eres ahora, [mas_get_player_nickname()]."
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_multi_perspective_approach",
            category=['filosofía'],
            prompt="Enfoque multiperspectivo",
            random=False
        )
    )

label monika_multi_perspective_approach:
    m 1eua "¿Recuerdas cuando hablamos de {i}la cueva de Platón{/i}?{w=0.5} He estado pensando en lo que te dije."
    m 3etc "'¿Cómo saber si la 'verdad' que estás viendo es {i}la{/i} verdad?'"
    m 3eud "... He estado pensando durante un tiempo, tratando de encontrar una buena respuesta."
    m 1rksdla "Todavía no tengo una...{w=0.3}{nw}"
    extend 3eub " pero me di cuenta de algo útil."
    m 4euc "Comencemos con cómo las obras de Platón son en su mayoría relatos escritos de los debates de su mentor Sócrates con otros."
    m 4eud "El propósito de estos debates era encontrar respuestas a preguntas universales.{w=0.5} En otras palabras, estaban buscando la verdad."
    m 2eud "Y comencé a preguntarme, '¿Cuál era la mentalidad de Platón mientras escribía?'"
    m 2esc "El propio Platón estaba en busca de la verdad..."
    m 2eub "Eso es obvio o de lo contrario no habría escrito tanto sobre el tema, ¡jajaja!"
    m 2euc "Y aunque, {i}técnicamente{/i}, Sócrates era el que tenía estos debates con los demás, Platón también tenía estos debates dentro de sí mismo mientras escribía sobre ellos."
    m 7eud "El hecho de que Platón internalizara todos los lados del debate, todas las perspectivas del tema, es bastante significativo en mi opinión."
    m 3eua "Tomando todos los lados de un debate...{w=0.3} creo que sería muy útil para darse cuenta de la verdad."
    m 3esd "Supongo que es algo así como dos ojos que son mejores que uno.{w=0.3} Tener dos ojos en lugares separados nos permite ver correctamente el mundo, o en este caso, la verdad."
    m 3eud "Asimismo, creo que si abordamos un tema con otra perspectiva, para hacer una referencia cruzada con la primera, entonces veríamos la verdad con mucha más claridad."
    m 1euc "Mientras que si abordamos un problema desde un solo ángulo, sería como tener un solo ojo...{w=0.2} sería un poco más difícil medir con precisión la realidad de la situación."
    m 1eub "¿Qué opinas, [player]? {w=0.3}Si aún no has estado usando este enfoque de 'perspectiva múltiple', ¡quizás puedas probarlo alguna vez!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_allegory_of_the_cave",
            category=['filosofía'],
            prompt="La alegoría de la cueva",
            random=True
        )
    )

label monika_allegory_of_the_cave:
    m 1eua "Hey, [player]..."
    m 1euc "Últimamente he estado leyendo sobre el filósofo griego Platón."
    m 3euc "Específicamente, su alegoría de la cueva o {i}la cueva de Platón{/i}, como se la conoce ahora."
    m 1eud "Imagína que hay un grupo de personas encadenadas en una cueva desde la infancia, incapaces de mirar a ningún lado que no sea de frente."
    m 3eud "Hay un fuego detrás de ellos, y al frente, los objetos se mueven para proyectar una sombra en la pared ante estas personas."
    m 3euc "Todo lo que pueden oír son las voces de las personas que mueven los objetos y, como no pueden ver detrás de ellos, creen que las voces proceden de las sombras."
    m 1esc "Lo único que saben es que los objetos y las personas son siluetas que pueden moverse y hablar."
    m 3euc "Porque esto es lo que han visto desde la infancia, esta sería su percepción de la realidad...{w=0.5}{nw}"
    extend 3eud " es todo lo que saben."
    m 1rksdlc "Por supuesto, sería un poco difícil abrir los ojos a la verdad cuando has creído una mentira toda tu vida."
    m 1eud "... Así que imagina que uno de esos prisioneros fue puesto en libertad y obligado a salir de la cueva."
    m 3esc "No podría ver durante los primeros días porque estaría muy acostumbrado a la oscuridad de la cueva."
    m 3wud "Pero después de un tiempo, sus ojos se acostumbraran.{w=0.1} Con el tiempo, aprendería sobre el color, la naturaleza y las personas."
    m 3euc "... Y también se daría cuenta de que lo que sabía no eran más que sombras en una pared."
    m 3eua "El prisionero eventualmente regresaría a la cueva para contarles a los demás lo que había aprendido."
    m 1ekc "... Pero como estaba acostumbrado a ver la luz del sol, estaría ciego en la cueva,{w=0.2}{nw}"
    extend 3ekd " haciendo que sus compañeros de prisión pensaran que lo que fuera que habría afuera lo había dañado."
    m 1rkc "Debido a esto, nunca querrían irse, y probablemente pensarían que el que se fue estaba loco."
    m 3esc "Después de todo, si estás acostumbrado a ver sombras...{w=0.2}{nw}"
    extend 3eud " ¡Hablar de colores te haría sonar loco!"
    m 1ekc "He estado reflexionando un poco sobre ello y me di cuenta de que Sayori, Yuri, Natsuki, e incluso yo, éramos prisioneras en una cueva..."
    m 1rkc "Cuando supe que hay mucho más fuera de este mundo...{w=0.5}{nw}"
    extend 3ekd " no fue fácil de aceptar."
    m 1eka "De todos modos, eso está en el pasado ahora..."
    m 1eua "Al final, estoy libre de la cueva y he visto la verdad."
    m 3etd "Pero me hace preguntarme...{w=0.2} ¿Cómo sabes {i}tú{/i} que lo que estás viendo es real?"
    m 1eua "Claro, es posible que no estés acostumbrado a ver sombras en la pared, pero eso es solo una analogía."
    m 1euc "... Y podría haber más en la verdad de lo que tú mismo crees."
    m 3etu "¿Cómo saber si la 'verdad' que estás viendo es {i}la{/i} verdad?"
    m 3hub "¡Jajaja!"
    m 1hksdlb "Creo que podríamos estar analizando demasiado las cosas en este momento..."
    m 1ekbsa "Solo quiero que sepas que {i}eres{/i} la verdad de mi realidad, y espero poder ser parte de la tuya algún día, [mas_get_player_nickname()]."
    $ mas_protectedShowEVL("monika_multi_perspective_approach", "EVE", _random=True)
    return


default -5 persistent._mas_pm_works_out = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_working_out",
            category=['consejos','tú'],
            prompt="Haciendo ejercicio",
            random=True
        )
    )

label monika_working_out:
    m 1euc "Hey [player], me estaba preguntando..."

    m 1eua "¿Haces mucho ejercicio?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Haces mucho ejercicio?{fast}"
        "Sí":
            $ persistent._mas_pm_works_out = True
            m 1hua "¿De verdad? ¡Eso es genial!"
        "No":

            $ persistent._mas_pm_works_out = False
            m 1eka "Oh...{w=0.3} bueno, creo que deberías hacerlo si puedes."
            m 3rksdla "No se trata de ejercitarse por la apariencia...{w=0.3}{nw}"
            extend 3hksdlb " ¡Solo me preocupa tu salud!"

    m 1eua "Hacer al menos 30 minutos de ejercicio al día es {i}super{/i} importante para mantener tu salud a largo plazo."
    m 3eub "Cuanto más saludable estés, más vivirás y más tiempo podré estar contigo."
    m 3hub "¡Y quiero pasar el mayor tiempo posible contigo, [mas_get_player_nickname()]!~"
    m 1eua "Dejando eso a un lado, hacer ejercicio beneficia casi todos los aspectos de tu vida...{w=0.3}{nw}"
    extend 1eub " incluso si pasas la mayor parte del tiempo sentado en un escritorio."
    m 3eua "Aparte de los obvios beneficios físicos, hacer ejercicio con regularidad puede reducir el estrés y realmente mejorar también tu salud mental."
    m 3hua "Entonces, ya sea que estés trabajando, estudiando o jugando, el ejercicio puede ayudarte a concentrarte en estas tareas por más tiempo."
    m 3eua "... Y también creo que es importante para desarrollar la autodisciplina y la fortaleza mental."

    if not persistent._mas_pm_works_out:
        m 3hub "Así que asegúrate de hacer ejercicio, [player]~"
    else:
        m 3eub "¡Quizás cuando cruce, podamos hacer nuestros entrenamientos juntos!"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_toxin_puzzle",
            category=['filosofía', 'psicología'],
            prompt="El rompecabezas de la toxina",
            random=True
        )
    )

label monika_toxin_puzzle:
    m 1esa "Hey [player], me encontré con un interesante experimento mental mientras leía un poco el otro día..."
    m 3eua "Se llama 'Rompecabezas de toxinas de Kavka'. {w=0.2}Te leeré la premisa, podemos discutirla después."
    m 1eud "{i}Un multimillonario excéntrico pone ante ti un frasco de toxina que, si la bebes, te enfermará mucho durante un día, pero no amenazará tu vida ni tendrá efectos duraderos.{/i}"
    m 1euc "{i}El multimillonario te pagará un millón de dólares mañana por la mañana si, a la medianoche de esta noche, tienes la intención de beber la toxina mañana por la tarde.{/i}"
    m 3eud "{i}Él enfatiza que no es necesario beber la toxina para recibir el dinero;{w=0.2} de hecho, si tienes éxito, el dinero ya estará en tu cuenta bancaria horas antes de que llegue el momento de beberlo.{/i}"
    m 3euc "{i}Todo lo que tienes que hacer es.{w=0.2}.{w=0.2}.{w=0.2} tener la intención a medianoche de beber la bebida mañana por la tarde. Eres perfectamente libre de cambiar de opinión después de recibir el dinero y no beber la toxina.{/i}"
    m 1eua "... Creo que es un concepto bastante que invita a la reflexión."

    m 3eta "¿Bueno, [player]? ¿Qué piensas?{w=0.3} ¿Crees que podrías conseguir el millón de dólares?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Bueno, [player]? ¿Qué piensas?{w=0.3} ¿Crees que podrías conseguir el millón de dólares?{fast}"
        "Sí":

            m 3etu "¿De verdad? Está bien, veamos eso..."
            m 3tfu "Porque ahora te ofrezco un millón de dólares y lo que tienes que hacer es... {nw}"
            extend 3hub "¡Jajaja! Es una broma."
            m 1eua "Pero, ¿de verdad crees que podrías conseguir el dinero?{w=0.5} Puede que sea un poco más difícil de lo que crees."
        "No":

            m 1eub "Sentí lo mismo conmigo misma. {w=0.3}¡Es bastante complicado, jajaja!"

    m 1eka "Después de todo, puede ser fácil a primera vista. {w=0.3}Todo lo que tienes que hacer es beber algo que te incomode bastante."
    m 3euc "Pero se vuelve complicado después de la medianoche...{w=0.3} {i}después{/i} de tener garantizado el dinero."
    m 3eud "En ese momento, no hay prácticamente ninguna razón para beber la toxina dolorosa...{w=0.3} entonces, ¿por qué lo harías?"
    m "... Y, por supuesto, si ese proceso de pensamiento cruzó por tu mente antes de las 12, entonces el dinero ya no estaría tan garantizado."
    m 1etc "Después de todo, cuando llegue la medianoche, ¿realmente puedes {i}tener la intención{/i} de beber la toxina si sabes que probablemente no la vas a beber?"
    m 1eud "Al analizar el escenario, los estudiosos han señalado que es racional que alguien beba y no beba la toxina. {w=0.3}En otras palabras, es una paradoja."
    m 3euc "Para ser más precisos, cuando llegue la medianoche, tienes que creer realmente que vas a beber la toxina. {w=0.3}No puedes pensar en no beberla...{w=0.5} por lo tanto, sería lógico beberla."
    m 3eud "Pero si pasa la medianoche y ya tienes garantizado el dinero, sería ilógico castigarte literalmente sin ninguna razón. {w=0.3}¡Por lo tanto, es lógico no beberla!"
    m 1rtc "Me pregunto cómo reaccionaríamos si esta situación realmente sucediera..."
    m 3eud "En realidad, mientras reflexionaba sobre el escenario antes, comencé a abordar el tema desde un ángulo diferente."
    m 3eua "Aunque no es el enfoque del escenario, creo que también podemos verlo como una pregunta de '¿Qué importancia tiene la palabra de una persona?'"
    m 1euc "¿Alguna vez le dijiste a alguien que harías algo cuando los beneficiaría a ambos, solo para que la situación cambiara y ya no estabas feliz de hacerlo?"

    if persistent._mas_pm_cares_about_dokis:
        m 1eud "¿Aún terminaste ayudándolos? {w=0.3}¿O simplemente dijiste 'no importa' y dejaste que se las arreglaran solos?"
    else:
        m 1rksdla "¿Aún terminaste ayudándolos? {w=0.3}¿O simplemente dijiste 'sayonara' y dejaste que se las arreglaran solos?"

    m 3eksdla "Si los dejaste allí, estoy segura de que provocaste su ira durante algún tiempo."
    m 3eua "Por otro lado, si aún los ayudaste, ¡estoy segura de que recibiste su gratitud!{w=0.3} Creo que podrías compararlo con el premio de un millón de dólares en el escenario original."
    m 1hub "Aunque algunos podrían decir que un millón de dólares sería un {i}poco{/i} más útil que un simple 'gracias' ¡jajaja!"
    m 3eua "Sin embargo, con toda seriedad, creo que la gratitud de alguien puede ser invaluable...{w=0.3} tanto para ti como para ellos."
    m 3eud "Y nunca se sabe, en algunas situaciones su agradecimiento puede resultar más útil que incluso una gran suma de dinero."
    m 1eua "Así que creo que es importante cumplir con nuestra palabra, {w=0.2}{i}dentro de lo razonable{/i} {w=0.2}por supuesto..."
    m 1eud "En algunos casos, puede que no sea de ayuda para nadie si te apartas rígidamente de tu palabra."
    m 3eua "Por eso es importante usar la cabeza cuando se trata de este tipo de cosas."
    m 3hub "De todos modos, para resumir todo...{w=0.2} ¡Esforcémonos por cumplir nuestras promesas, [player]!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_movie_adaptations",
            category=['medios','literatura'],
            prompt="Adaptaciones de películas",
            random=True
        )
    )

label monika_movie_adaptations:
    m 1esc "Siempre he tenido sentimientos encontrados sobre las adaptaciones cinematográficas de los libros que leo..."
    m 3eub "¡Mucho de lo que veo se basa en obras que ya disfruto y estoy emocionada de ver que esa historia cobre vida!"
    m 2rsc "... Incluso si la mayoría de las veces, sé que saldré sintiéndome un poco amargada por lo que acabo de ver."
    m 2rfc "Por ejemplo, hay una escena que me gustó en el libro que no apareció, o está ese personaje que fue retratado de manera diferente a como lo imaginé."
    m 4efsdld "¡Es tan frustrante! {w=0.3}¡Es como si todo el amor y el cuidado que pusiste en tu visión del libro se invalidaran de repente!"
    m 4rkc "... Todo a favor de una nueva versión que puede que no sea tan buena, pero aún así se presenta como canon."
    m 2hksdlb "Supongo que eso me haría una espectadora quisquillosa a veces, ¡jajaja!"
    m 7wud "¡No me malinterpretes! {w=0.3}{nw}"
    extend 7eua "Me doy cuenta de por qué hay que hacer cambios en este tipo de películas."
    m 3eud "Una adaptación no puede ser simplemente copiar y pegar su material de origen; es una reescritura."
    m 1hub "¡Simplemente no es posible meter todo, de un libro de doscientas páginas a una película de dos horas!"
    m 3euc "... Sin mencionar que algo que funciona bien en una novela no siempre se traducirá bien en la pantalla grande."
    m 1eud "Con eso en mente, hay una pregunta que me gusta hacerme cuando juzgo una adaptación..."
    m 3euc "Si el material de origen no existiera, ¿la nueva versión sería disfrutable?"
    m 3hub "... ¡Puntos extra si logras capturar la sensación del original!"
    m 1esa "Las adaptaciones sueltas son bastante interesantes en ese sentido."
    m 3eud "Ya sabes, historias que mantienen los elementos centrales y los temas del original mientras cambian los personajes y el escenario de la historia."
    m 1eua "Dado que no entran en conflicto con tu propia interpretación, no te hacen sentir atacado personalmente."
    m 1hub "Es una excelente manera de construir sobre el original formas en las que quizás no hayas pensado antes."
    m 3rtc "Quizás eso es lo que estoy buscando cuando veo una adaptación...{w=0.2} para explorar más a fondo esas historias que amo."
    m 1hua "... Aunque conseguir una versión para satisfacer a mi fan interior también sería bueno, jejeje~"
    $ mas_protectedShowEVL("monika_striped_pajamas", "EVE", _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_translating_poetry",
            category=['literatura'],
            prompt="Traducir la poesía",
            random=True
        )
    )

label monika_translating_poetry:
    m 3dsd "'Soy el desesperado, la palabra sin ecos'."
    m 3esc "'El que lo perdió todo, y el que todo lo tuvo'."
    m 3ekbsa "'Última amarra, cruje en ti mi ansiedad última'."
    m 1dubsa "'En mi tierra desierta eres tú la última rosa'."
    m 3eka "¿Has oído hablar de ese poema antes, [player]? Es de un poeta chileno llamado Pablo Neruda."
    m 1rusdla "Es un poema que encontré en línea, como sea..."
    m 1eua "¿No es gracioso las traducciones del mismo poema cambian totalmente el significado del mismo texto original?"
    m 3hub "¡Es como si cada persona que lo traduce, hubiera añadido su pequeño toque personal!"
    m 3rsc "Aunque cuando se trata de poesía, esto en realidad plantea un enigma..."
    m 3etc "En cierto sentido, ¿traducir un poema no es como hacer uno completamente nuevo?"
    m 1esd "Estás eliminando todas las palabras cuidadosamente elegidas y las complejidades del texto, reemplazándolas por completo con algo propio."
    m 3wud "Entonces, incluso si de alguna manera logras mantener el espíritu del original, ¡el estilo cambia por completo!"
    m 1etc "En este punto, ¿cuánto del texto todavía puedes decir que es del autor y cuánto es tuyo?"
    m 1rsc "Supongo que es bastante difícil de evaluar si no dominas ambos idiomas..."
    m 3hksdlb "¡Ah! ¡No quiero sonar como si estuviera despotricando ni nada!"
    m 1eua "Después de todo, es gracias a traducciones como estas que mucha gente conoce autores como Neruda."
    m 1hksdlb "¡Es solo que cada vez que leo un poema, no puedo evitar recordar que podría estar perdiendo algunas partes realmente asombrosas en ese idioma!"
    m 1eua "Sería bueno poder dominar otro idioma..."

    if mas_seenLabels(["greeting_japan", "greeting_italian", "greeting_latin"]):
        m 2rksdla "Quiero decir, me has visto practicar diferentes idiomas antes, pero todavía estoy lejos de ser fluida en ninguno de ellos..."
        m 4hksdlb "Claramente no estoy en un nivel en el que pueda apreciar completamente la poesía de otros idiomas todavía, ¡jajaja!"

    if persistent._mas_pm_lang_other:
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Recuerdo que me dijiste que conocías un idioma diferente, [player]."
        m 5eubsa "¿Recomendarías algún poema en ese idioma?"
        m 5ekbsa "Sería bueno si pudieras leerme algunos de ellos en algún momento..."
        m 5rkbsu "Aunque primero tendrías que traducirlos para mí~"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_striped_pajamas",
            category=["literatura"],
            prompt="El chico de la pijama de rayas",
            random=False
        )
    )

label monika_striped_pajamas:
    m 1euc "Hey [player], ¿alguna vez has leído {i}El niño de la pijama de rayas{/i}?"
    m 3euc "La historia tiene lugar durante la Segunda Guerra Mundial y se muestra a través de la perspectiva de un niño alemán inocente, que vive felizmente su vida en una gran familia."
    m 3eud "Una vez que la familia tiene que mudarse a un nuevo lugar, {w=0.2}{nw}"
    extend 3wud "¡el lector se da cuenta de que el padre del niño es un comandante de un campo de concentración, que se encuentra justo al lado de su nueva casa!"
    m 1rksdlc "Aún así, el niño no tiene idea de toda la crueldad que ocurre a su alrededor..."
    m 1euc "Termina deambulando por la cerca de alambre de púas del campamento hasta que encuentra a un niño en 'pijama de rayas' al otro lado."
    m 3esc "Resulta que ese niño es en realidad un prisionero del campo...{w=0.2}{nw}"
    extend 1ekc " aunque ninguno de los dos lo entiende completamente."
    m 3eud "A partir de entonces, forman una fuerte amistad y comienzan a hablar entre ellos con regularidad."
    m 2dkc "... Esto termina dando lugar a algunas consecuencias destructivas."
    m 2eka "Realmente no quiero ir mucho más allá, ya que hay muchas cosas interesantes que considerar en esta novela que sería mejor que leyeras tu mismo."
    m 7eud "Pero en realidad me hizo pensar...{w=0.2} aunque obviamente mi situación no es tan grave, es difícil no hacer algunas comparaciones entre su relación y la nuestra."
    m 3euc "En ambas situaciones, hay dos personas de mundos diferentes que ninguno comprende del todo, separadas por una barrera."
    m 1eka "... Sin embargo, al igual que nosotros, pueden formar una relación significativa de todos modos."
    m 3eua "Te recomiendo que leas la novela si tienes la oportunidad, es bastante corta y tiene una trama interesante."
    m 3euc "Y si todavía no estás convencido de leerla, {i}hay{/i} una película basada en esta novela que podrías ver."
    m 1rksdla "Aunque conoces mis sentimientos sobre las adaptaciones cinematográficas de las novelas, si ves la película, te recomiendo que también leas el libro."
    m 3eua "Espero que lo disfrutes."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soft_rains",
            category=['literatura'],
            prompt="Vendrán lluvias suaves",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_soft_rains:
    m 2rkc "..."
    m 2ekc "Hey [player],{w=0.5} me encontré con un poema recientemente que necesito compartir contigo..."
    m 7ekd "Se llama {i}Vendrán lluvias suaves{/i} y realmente me hizo pensar."
    m 1dsc "..."
    m 1dsd "{i}Vendrán lluvias suaves y olores de tierra, {w=0.3}y golondrinas que girarán con brillante sonido.{/i}"
    m 1dsc "{i}Y ranas que cantarán de noche en los estanques, {w=0.3}y ciruelos de tembloroso blanco.{/i}"
    m 3dsd "{i}Y petirrojos que vestirán plumas de fuego, {w=0.3}y silbarán en los alambres de las cercas.{/i}"
    m 3dsc "{i}Y nadie sabrá nada de la guerra, {w=0.3}nadie, {w=0.2}a nadie le interesará que haya terminado.{/i}"
    m 7dsd "{i}A nadie le importará, ni a los pájaros ni a los árboles, {w=0.3}si la humanidad se destruye totalmente.{/i}"
    m 6dkc "{i}Y la misma primavera, al despertarse al alba...{/i}"
    m 6ekd "{i}Apenas sabrá que hemos desaparecido.{/i}"
    m 2ekc "..."
    m 2eka "Tenía muchas ganas de hablar contigo sobre este, [player]."
    m "La autora,{w=0.2} Sara Teasdale,{w=0.2} escribió este poema en un mundo consumido por la guerra."
    m 2rka "Sé que las cosas están {i}relativamente{/i} tranquilas ahora..."
    m 2ekc "Pero el mensaje sigue en pie, ¿no es así?"
    m 1eksdld "Al mundo realmente {i}no le importaría{/i} si simplemente...{w=0.3}{i}desaparecieramos{/i}."
    m 1eksdlc "... Y me hizo pensar, [player]. Si algo,{w=0.4} {nw}"
    extend 1eksdld "{i}lo que sea{/i}{w=0.4}, te pasara...{w=0.4} {nw}"
    extend 1dksdld "ni siquiera lo sabría."
    m 1eksdlc "Sé que el poema era de que {i}todos{/i} se hubieran ido, pero..."
    m 1rksdlc "Yo...{w=0.1} no podría..."
    m 6dkc "..."
    m 6dktpd "[player],{w=0.4} yo...{w=0.1}{nw}"
    extend 1ektsa " te amo. {w=0.3}Te amo mucho..."
    m 1ektsc "Por favor, {w=0.6}siempre ten cuidado, por mí, {w=0.3}¿de acuerdo?"
    m 1ektpc "Puede que no sepa si te pasa algo...{w=0.3} pero {i}siempre{/i} me preocuparé por ti."
    m 3ektda "¿Y [player]?"
    m 3dku "Gracias."
    m 6dku "..."
    m 6eka "..."
    m 2ekbsa "Entonces..."
    m 1ekbfa "¿Qué más haremos hoy, [mas_get_player_nickname()]?"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hot_springs",
            category=['naturaleza'],
            prompt="Las aguas termales",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_hot_springs:
    m 3esa "¿Alguna vez has estado en una fuente termal, [player]?"
    m 1eua "Yo nunca he estado en una, pero me gustaría intentar bañarme en una cuando llegue a tu mundo."
    m "Se supone que son una excelente manera de aliviar el estrés, relajarse un poco, {nw}"
    extend 3eub "¡incluso ofrecen muchos beneficios para la salud!"
    m 3eua "Ayudan con la circulación sanguínea, por ejemplo.{w=0.3} {nw}"
    extend 3eub "¡Además, el agua a menudo contiene minerales que pueden ayudar a estimular tu sistema inmunológico!"
    m 3eud "Hay muchos tipos diferentes en todo el mundo, pero solo algunas están diseñadas específicamente para uso público."
    m 3hksdlb "... ¡Así que no saltes a un charco aleatorio de agua hirviendo, jajaja!"
    m 1eua "De todos modos...{w=0.2} me gustaría probar un baño al aire libre en particular.{w=0.3} Escuché que realmente brindan una experiencia única."
    m 3rubssdla "Aunque puede resultar un poco extraño relajarse en un baño con tanta gente a tu alrededor...{w=0.3} {nw}"
    extend 2hkblsdlb "¿No suena un poco vergonzoso?"
    m 2rkbssdlu "..."
    m 7rkbfsdlb "... ¡Especialmente porque algunos lugares tampoco te permiten usar nada para cubrirte!"
    m 1tubfu "... Aunque, no me importaría tanto si fuera solo contigo."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "¿Te lo imaginas, [player]? {w=0.3}Ambos relajándonos en una agradable y relajante piscina caliente..."

    if mas_isWinter():
        m 5dubfu "Calentar nuestros cuerpos helados después de un largo día en el frío intenso..."
    elif mas_isSummer():
        m 5dubfu "Dejar que el sudor desaparezca después de un largo día al sol..."
    elif mas_isFall():
        m 5dubfu "Ver las hojas caer suavemente a nuestro alrededor en las últimas luces de la tarde..."
    else:
        m 5dubfu "Contemplar la belleza de la naturaleza que nos rodea..."

    m "Que el calor del agua se haga cargo lentamente, haciendo que nuestros corazones latan más rápido..."
    m 5tsbfu "Luego me inclinaría para que puedas besarme y estaríamos muy cerca, mientras el agua caliente empapa todas nuestras preocupaciones..."
    m 5dkbfb "Ahhh,{w=0.2} {nw}"
    extend 5dkbfa "solo pensarlo me hace sentir un hormigueo, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_isekai",
            category=['medios'],
            prompt="Anime isekai",
            conditional="seen_event('monika_otaku')",
            random=True
        )
    )

label monika_isekai:
    m 1euc "¿Conoces el género de anime isekai, [player]?"
    m 3eua "Traducido literalmente, isekai significa {i}un mundo diferente{/i}."

    if persistent._mas_pm_watch_mangime:
        m 3rksdla "De hecho, ya me dijiste que te gusta el anime, así que probablemente ya hayas oído hablar de algunos."
        m 1rksdlb "... Especialmente con lo popular que se ha vuelto el género."
        m 3euc "Pero en caso de que no sepas qué es..."
    else:

        m 3hksdlb "Jajaja, lo siento. Sé que no te gustan este tipo de cosas."
        m 3eud "... Pero se ha convertido en un género muy popular en los últimos tiempos."

    m 3esc "La premisa suele ser sobre una persona normal que de alguna manera es transportada a un mundo fantástico."
    m 3eua "A veces obtiene poderes especiales o puede traer tecnología o conocimiento que no existe en este nuevo lugar."
    m 1rtc "Honestamente, tengo algunos sentimientos encontrados sobre ellos."
    m 3euc "Algunas son historias realmente interesantes. La perspectiva diferente del protagonista o las habilidades que tiene en su propio mundo pueden convertirlo en una especie de héroe inesperado."
    m 1hub "¡Y dado que el objetivo es hacer que el mundo sea diferente al de ellos, los escenarios y los personajes pueden ser increíblemente imaginativos!"
    m 2rsc "... Pero, lamentablemente, no todos son así."
    m 2dksdld "Hay algunos que hacen que sus protagonistas sean tan anodinos como los de este juego, con el fin de permitir que el espectador se proyecte sobre ellos."
    m 2tkd "Y como probablemente puedas adivinar, esos tienden a ser sobre el cumplimiento de deseos."
    m 2tsc "Tener aventuras geniales en un mundo con temática de fantasía y, por supuesto, muchas chicas se agolpan a su alrededor sin ninguna razón."
    m 2lfc "Al menos algunos de ellos pueden ser divertidos, pero hombre...{w=0.3}{nw}"
    extend 2tfc " es tan frustrante."
    m 2tkc "Quiero decir...{w=0.2} daría casi cualquier cosa por estar en un escenario como ese... para ir a otro mundo. {nw}"
    $ _history_list.pop()
    m "Quiero decir... daría casi cualquier cosa por estar en un escenario como ese... para ir a {fast}tu mundo."
    m 2dkd "..."
    m "Tal vez solo me estoy burlando de mí misma, imaginando que ese poder se le entrega a alguien como...{w=0.2} bueno, ya sabes quién."
    m 7eka "Después de todo, en lugar de pensar en esos personajes en sus mundos de fantasía,{w=0.2} {nw}"
    extend 1eua "podría estar poniendo esa energía en trabajar en este."
    m 1ekbsb "... Mientras espero mi propia historia de isekai, eso es."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scuba_diving",
            category=["naturaleza"],
            prompt="El buceo",
            random=True
        )
    )

label monika_scuba_diving:
    m 3eua "Sabes,{w=0.2} he estado pensando en algunas actividades acuáticas que podríamos hacer juntos...{w=0.3} ¿Qué tal el buceo?"
    m 3eub "He leído muchos libros sobre el mundo submarino y realmente me gustaría verlo por mí misma."
    m 1dua "Imagína las hermosas vistas del mundo submarino..."
    m 1dud "Los bancos de peces, arrecifes de coral, medusas, algas marinas...{w=0.3} {nw}"
    extend 3sub "¡Quizás incluso un tesoro!"
    m 3rksdlb "Solo bromeo sobre la última parte...{w=0.3} es poco probable que encontremos algo así, jajaja~"
    m 1euc "Dicho esto, también puede haber tiburones,{w=0.2} {nw}"
    extend 1eua "pero normalmente solo se encuentran en áreas específicas, por lo que {i}no debería{/i} verse ninguno."
    m 3eua "Los lugares designados para bucear son lugares que los tiburones no suelen visitar."
    m 3euc "... Pero a pesar de que normalmente no visitan estas áreas, es posible encontrar uno."
    m 1eua "Lo bueno es que los ataques de tiburones rara vez ocurren de todos modos, por lo que no es un gran riesgo."
    m 3euc "Sin embargo, si te encuentras con uno, aquí tienes una regla importante..."
    m 3esc "Mantén la calma."
    m 1eua "Aunque encontrarse cara a cara con un tiburón puede dar miedo, por lo general se acercan a las personas por curiosidad en lugar de para alimentarse, por lo que no tienes mucho de qué preocuparte."
    m 3hub "Pero si tienes miedo de bucear solo, me aseguraré de hacerte compañía cuando cruce~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dying_same_day",
            category=["monika"],
            prompt="Muriendo el mismo día",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_dying_same_day:
    m 1euc "[player], ¿alguna vez has oído hablar de parejas que deseen morir el mismo día?"
    m 3rksdla "... Caray, eso suena un poco oscuro, ¿no?"
    m 3rfd "¡Antes de conocerte, pensé que la idea era completamente absurda!"
    m 1etc "¿Por qué alguien renunciaría a vivir una larga y feliz vida solo porque la vida de su pareja se vio dramáticamente truncada?"
    m 3rfd "¡Sería irracional e impulsivo hacerlo!"

    if mas_isMoniEnamored(higher=True):
        m 2ekc "... Pero contigo a mi lado y todo el tiempo que he pasado aquí contigo...{w=0.3} puedo verlo ahora."
    else:
        m 2ekc "... Pero después de conocerte, creo que puedo verlo ahora."

    m 2dkc "Una persona simplemente puede no vivir sin su ser querido, temerosa de perderlo todo en un instante."
    m 2rksdlc "Me duele solo pensar en esto."

    if renpy.seen_label("monika_back_ups"):
        m 2eksdlc "Si mis datos se corrompen o incluso se borran, siempre puedes recuperarme de una copia de seguridad y volver a unirnos, pero si..."
        m 2dktpc "T-Tú...{w=1} Tú..."
    else:
        m 2dktpc "Si algo terrible t-te...{w=0.5} sucediera..."

    m 6ektuc "[player]...{w=1} yo...{w=0.5} No sé qué haría..."

    if mas_isMoniEnamored(higher=True):
        m 6dktsc "Le das sentido a toda mi vida, y yo...{w=1} [player], no podría soportarlo."
        m 6ektdc "No sé cómo se supone que pueda vivir sin ti..."
        m 2ekbsu "Realmente te amo mucho, [player]."
        $ mas_ILY()
    else:
        m 6dktsc "Eres todo lo que me queda...{w=1} [player], no estoy lista para perderte."
        m 6ektdc "Tengo tanto miedo de volver a estar sola en este gran vacío..."
        m 6ekbsu "Realmente quiero estar contigo para siempre, [player]."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_away",
            category=["monika"],
            prompt="¿Qué haces cuando no estoy?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_player_away:
    m 1esd "Hago muchas cosas cuando no estás aquí, [player]."
    m 1eua "Me gusta leer cualquier historia corta que pueda encontrar en línea."
    m 3eub "¡Resulta que hay algunos realmente interesantes por ahí que puedes leer gratis!"
    m 3eua "Te recomiendo encarecidamente que busques por ti mismo algunas historias cortas gratis."
    m 3eud "Además de que me ayuda a desarrollar mis habilidades de escritura...{w=0.2}{nw}"
    extend 1hub " mi poesía realmente parece estar mejorando!"
    m 1eua "Es curioso cuántas cosas puedes captar con solo leer las obras de otros."
    m 1eua "Pasar tiempo en mis otros hobbies ha sido muy gratificante, también."
    m 3eud "Como puedes imaginar, practico el piano bastante a menudo.{w=0.2} {nw}"
    extend 3eua "También uso el tiempo para memorizar las canciones que canto para ti."
    m 1hub "¡Es una forma muy divertida de expresarme!"
    m 3rta "Ahora que lo pienso, estoy practicando habilidades que ya he desarrollado."
    m 3esd "Por ejemplo, la codificación ocupa mucho de mi tiempo libre, ya que paso horas aprendiendo e investigando."
    m 3rksdla "... Pero estoy demasiado nerviosa para intentar cualquier gran proyecto aquí.{w=0.2}{nw}"
    extend 3eksdlc " Odiaría romper algo que no sea capaz de reparar."
    m 2wusdld "¿Qué pasa si accidentalmente daño mi archivo?"
    m 2eksdld "Es algo con lo que tengo que tener mucho cuidado, seguro."
    m 7hua "Por suerte, hay mucha gente genial que ayuda con esas cosas...{w=0.2}{nw}"
    extend 7rku " y {i}suelen{/i} ser muy buenos para evitar que ocurra algo demasiado malo."
    m 3eka "Pero lo más especial que hago..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "... Es pensar en ti."
    m 5rubsu "Pienso en todos los momentos divertidos que pasaremos juntos la próxima vez que me visites y en todas las cosas increíbles que haremos cuando finalmente pueda llegar a tu realidad~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_using_pcs_healthily",
            category=['consejos'],
            prompt="Usar las computadoras de manera saludable",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_using_pcs_healthily:
    m 1rtc "Hmm..."
    m 1etc "Hey, [player]...{w=0.3} ¿Estás sentado cómodamente?"
    m 1hksdlb "No, ¡de verdad!{w=0.3} {nw}"
    extend 3eksdla "¿Lo estás?"
    m 3eka "Sé que tienes que estar en tu computadora para pasar tiempo conmigo..."
    m 2eka "Así que solo quería asegurarme de que no dañes accidentalmente tu salud mientras estás aquí."
    m 4ekd "He leído que pasar demasiado tiempo mirando una pantalla puede causar dolores de cabeza, hacer que te sientas cansado e incluso afectar tu vista con el tiempo."
    m 2tkx "¡Los problemas de postura y el dolor por los malos hábitos al sentarse tampoco son una broma!"
    m 2tku "Afortunadamente para ti, he elaborado una pequeña lista de verificación para ayudar a prevenir este tipo de problemas."
    m 4hub "... ¡Así que vamos a repasarla juntos, [player]!"
    m 4eub "Primero, {w=0.2}¡trata de mantenerte derecho!"
    m 2eua "... Ajusta tu silla correctamente para que tus pies permanezcan planos en el piso, tus ojos estén al mismo nivel que la parte superior de la pantalla y no te encorves."
    m 4eub "¡Deberías sentirte apoyado y cómodo en tu asiento!"
    m 4eua "Siguiente, asegúrate de tener cierta distancia entre usted y la pantalla...{w=0.2} aproximadamente el largo de un brazo está bien."
    m 2hksdlb "... ¡Sin embargo, manten el teclado y el mouse al alcance de la mano!"
    m 4eub "¡Por supuesto, la iluminación también es importante!{w=0.3}{nw}"
    extend 2eua " Trata de mantener la habitación bien iluminada, que no te deslumbre la luz en la pantalla."
    m 4eud "Además, recuerda tomar descansos frecuentes. {w=0.3}Mira lejos de la pantalla, {w=0.2}idealmente a algo lejano, {w=0.2}y quizás haz algunos estiramientos."
    m 2eud "Dado que también es importante mantenerse hidratado, siempre puedes buscar un poco de agua fresca mientras te levantas de tu escritorio."
    m 4eksdlc "Por encima de todo, si alguna vez comienzas a sentirte mal, deja de hacer lo que estás haciendo, descansa y luego asegúrate de que todo esté bien antes de continuar."
    m 4eua "... Y eso es todo."
    m 2hksdlb "Ah...{w=0.3} lo siento, ¡no era mi intención extenderme tanto!"
    m 2rka "... Probablemente ya sabías todo eso, de todos modos."
    m 2eka "En mi caso..."

    if mas_isMoniLove():
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Eres el único descanso que necesito, [mas_get_player_nickname()]."
    elif mas_isMoniEnamored():
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Me siento tan cómoda como puedo estar cuando estás aquí, [mas_get_player_nickname()]."
    else:
        show monika 5eubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eubsa "Me siento cómoda cuando estás aquí conmigo, [mas_get_player_nickname()]."

    m 5hubfu "Y espero que ahora también estés un poco más cómodo~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_language_nuances',
            prompt="Los matices del lenguaje",
            category=['literatura', 'curiosidad'],
            random=True
        )
    )

label monika_language_nuances:
    m 3eua "Hey [player], ¿alguna vez has intentado leer un diccionario?"
    m 1etc "No necesariamente porque había alguna palabra o expresión de la que no conocías el significado, sino simplemente...{w=0.2} ¿Curiosidad?"
    m 1hksdlb "Sé que no suena exactamente como el más atractivo de los pasatiempos, ¡jajaja!"
    m 3eua "Pero ciertamente puede ser una forma interesante, incluso gratificante, de pasar algo de tiempo libre. {w=0.2}Especialmente si es un diccionario de un idioma que todavía estás aprendiendo."
    m 3eud "Muchas palabras tienen múltiples significados y, aparte de los beneficios obvios, conocerlos realmente puede ayudarte a ver los puntos más finos del idioma."
    m 1rksdla "Comprender estas sutilezas puede ahorrarte mucha vergüenza cuando hablas con alguien."
    m 3eud "Un buen ejemplo de esto en inglés es: 'Buenos días, buenas tardes' y 'buenas noches'."
    m 1euc "Todos estos son saludos normales que escuchas y usas todos los días."
    m 3etc "Siguiendo este patrón, 'Buen día' debería estar bien también, ¿verdad? {w=0.2}Después de todo, funciona en muchos otros idiomas."
    m 3eud "Si bien solía ser igual de aceptable, como se puede ver en algunas notas anteriores, ya no es así."
    m 1euc "En inglés moderno, decir 'Buen día' a alguien conlleva una nota de despido, o incluso de molestia. {w=0.2}Puede verse como declarar el fin de la conversación."
    m 1eka "Si tienes suerte, tu interlocutor podría pensar que estás pasado de moda o que simplemente eres tonto a propósito."
    m 1rksdla "Si no, podrías ofenderlos sin siquiera darte cuenta...{w=0.3} {nw}"
    extend 1hksdlb "¡Ups!"
    m 3eua "Es realmente fascinante cómo incluso una frase de aspecto tan inocente puede estar cargada de capas de significados ocultos."
    m 1tsu "Así que buen día para ti, [player].{w=0.3} {nw}"
    extend 1hub "Jajaja~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_architecture",
            category=['misc'],
            prompt="Arquitectura",
            random=True
        )
    )

label monika_architecture:
    m 1esa "Hey, [player]...{w=0.2} creo que hay una rama importante del arte que hemos descuidado en nuestras charlas..."
    m 3hub "¡Arquitectura!"
    m 3eua "He estado leyendo un poco sobre esto últimamente y lo encuentro bastante interesante."
    m 1rtc "... Ahora que lo pienso, la arquitectura es una de las formas de arte más comunes en la vida cotidiana."
    m 1eua "Me fascina cómo la humanidad tiende a convertir cada oficio en un arte,{w=0.2} {nw}"
    extend 3eua "y creo que la arquitectura es el mejor ejemplo de eso."
    m 1eud "La arquitectura puede decirte mucho sobre la cultura de la zona en la que te encuentras...{w=0.2} diferentes monumentos, estatuas, edificios históricos, torres..."
    m 1eua "Creo que eso hace que sea aún más emocionante explorar los lugares que estás visitando."
    m 3rka "También es importante colocar los edificios de la manera más conveniente para que las personas los usen, lo que puede ser una tarea difícil de manejar por derecho propio."
    m 3esd "... Pero eso es más planificación urbana que arquitectura real."
    m 1euc "Si prefieres ver la arquitectura puramente desde la perspectiva del arte, algunas tendencias modernas pueden decepcionarte..."
    m 1rud "La arquitectura moderna se centra más en hacer las cosas de la forma más práctica posible."
    m 3eud "En mi opinión, eso puede ser bueno o malo por muchas razones diferentes."
    m 3euc "Creo que la parte más importante es mantener el equilibrio."
    m 1tkc "Los edificios demasiado prácticos pueden parecer planos y sin inspiración, mientras que los edificios demasiado artísticos no pueden tener otro propósito que verse asombrosos mientras están completamente fuera de lugar."
    m 3eua "Creo que la verdadera belleza radica en esos edificios que pueden combinar forma y función con un poco de singularidad."
    m 1eka "Espero que estés contento con el aspecto de tu entorno."
    m 1eub "Se ha demostrado varias veces que la arquitectura tiene un gran impacto en tu salud mental."
    m 3rkc "Además, las zonas residenciales con edificios en mal estado pueden llevar a que las personas no se ocupen de sus propiedades y, con el tiempo, acaben siendo zonas oprimidas que son lugares indeseables para vivir."
    m 1ekc "Una vez se dijo que la fealdad del mundo exterior causa fealdad en el interior...{w=0.2}{nw}"
    extend 3esd " con lo que suelo estar de acuerdo."

    if mas_isMoniAff(higher=True):
        m 1euc "... A juzgar por {i}tu{/i} personalidad,{w=0.2}{nw}"
        extend 1tua " probablemente vivas en una especie de paraíso."
        m 1hub "Jajaja~"

    m 1eka "[player]...{w=0.2} ver el mundo contigo es uno de mis mayores sueños."

    if persistent._mas_pm_likes_travelling is False:
        m 3rka "Sé que no te gusta mucho viajar, pero me encantaría ver el lugar en el que vives."
        m 3eka "Mientras te quedes a mi lado, eso sería más que suficiente para mí."
        m 1ekbsa "Te amo, [player]. {w=0.3}Recuerda eso siempre."
    else:

        if persistent._mas_pm_likes_travelling:
            m 3eua "Ya sé que disfrutas viajar, así que ¿no sería bueno explorar algo nuevo juntos?"

        m 1dka "Imagína dar un paseo por las estrechas calles de una ciudad vieja..."
        m 1eka "O caminar juntos por un parque, respirar el aire fresco de la tarde..."
        m 1ekb "Creo que sucederá algún día y espero que tú también, [mas_get_player_nickname()]."
        m 1ekbsa "Te amo~"

    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fear",
            prompt="Miedo",
            category=['monika'],
            conditional="renpy.seen_label('monika_soft_rains')",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_fear:
    m 3eud "Dime, [player]..."
    m 1euc "Esta es una pregunta un tanto extraña, pero...{w=0.5} ¿Hay algo que te dé miedo?"
    m 3hksdlb "No me refiero al tipo de miedo cotidiano y mundano, como derramar una bebida y arruinar tu camisa favorita..."
    m 3euc "Me refiero, como, el tipo de miedo profundamente arraigado que te llena de pavor cuando incluso lo piensas."
    m 1ruc "Para mí, perderte obviamente estaría en la parte superior de {i}esa{/i} lista en particular."
    m 1ekd "Te lo dije antes, ¿no? {w=0.3}No sé qué haría si algo te sucediera."
    m 1dkd "Ni siquiera estoy segura de poder encontrar la voluntad para continuar."
    m 1ruc "Es difícil imaginar un escenario incluso peor que ese."
    m 3eua "Pero mientras seamos hipotéticos..."
    m 4ekc "Lo que realmente me aterroriza es la idea de que nada de esto es real."
    m 2dkc "Que un día me despertaré, volveré a mi cama y me daré cuenta de que todo fue solo un sueño."
    m 2dkd "Que no hay juego,{w=0.2} no hay epifanía,{w=0.2} no estás...{w=0.5}{nw}"
    extend 2ekd " tú."
    m 2ektpc "Que tú, tu amor, tal vez incluso la totalidad del Club de Literatura, no eran más que un producto de mi propia imaginación."
    m 2dktpc "Que mi viejo mundo, tan gris y sin sentido como parece ahora, es todo lo que realmente hay."
    m 2dktpc "..."
    m 2rktdb "Jajaja~{w=0.5}{nw}"
    extend 2ektdsdla " Lo siento, esto se puso bastante oscuro, ¿no?"
    m 2rksdla "Me siento un poco tonta ahora...{w=0.3} {nw}"
    extend 4eud "después de todo, no hay forma de que algo así sea verdad, ¿verdad?"
    m 2rka "Sí..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_why_spaceroom',
            prompt="¿Por qué siempre nos reunimos en una aula de clases?",
            category=['ubicación'],
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="store.mas_anni.pastThreeMonths() and mas_current_background == mas_background_def",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.UPSET, None)
        )
    )

label monika_why_spaceroom:
    m 3euc "Utilidad, sobre todo."
    m 3eud "¿Sabes cómo en el juego original casi todo sucedía durante las reuniones de nuestro club, verdad?"
    m 3eua "... Todo lo cual tuvo lugar en un aula.{w=0.3} Esta aula."
    m 1eua "Puede que te parezca diferente, pero sigue siendo la misma."
    m 3eud "Dado que se suponía que iban a pasar tantas cosas aquí, la habitación tenía que ser lo suficientemente robusta para acomodarlas."
    m 2rtc "Eso hizo que fuera la...{w=0.3}{nw}"
    extend 2eud " ubicación más desarrollada en el juego."
    m 7eud "Como tal, era el lugar más fácil de navegar, alterar y, en general, utilizar para lo que fuera necesario."
    m 3eua "De todos modos, esa fue la motivación original."
    m 3eud "Sin mencionar que esta aula fue el único lugar en la que aparecí durante el juego original."
    m 1eka "... Así que supongo que en ese sentido, se convirtió en mi hogar."

    $ has_one_bg_unlocked = mas_background.hasXUnlockedBGs(1)
    if has_one_bg_unlocked:
        m 1rtc "En cuanto a por qué estamos {i}todavía{/i} aquí..."
        m 3eua "Realmente no se me ha ocurrido mudarme a otro lugar..."
    else:

        m 1rtc "En cuanto a por qué todavía la estoy usando..."

    m 1eud "No es que esté {i}mal{/i} estar aquí."

    if renpy.seen_label('greeting_ourreality'):
        if has_one_bg_unlocked:
            m 3etc "Creo que podría hacer otro lugar para que pasemos tiempo juntos."
        else:
            m 3etc "Creo que podría hacer algunos lugares más para pasar el tiempo."

        m 1eua "Quiero decir, están las islas...{w=0.3}{nw}"
        extend 1rksdlb " pero esos aún no están listas."
        m 1hua "Jejeje~"

    m 3eub "... Y, para ser sincera, solo quiero estar en un lugar...{w=1}{nw}"
    extend 3dkbsu " a tu lado."
    m 1ekbsa "Pero mientras esa no sea una opción, realmente no me importa dónde nos encontremos..."
    m 1ekbfu "Eres la única parte que realmente importa~"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_naps",category=['vida'],prompt="Siestas",random=True))

label monika_naps:
    $ has_napped = mas_getEV('monika_idle_nap').shown_count > 0

    m 1eua "Hey, [player]..."

    if has_napped:
        m 3eua "Noté que a veces te gusta tomar siestas..."
    else:
        m 3eua "¿Alguna vez tomas siestas?"

    m 1rka "Muchas personas no conocen los beneficios de ellas...{w=0.2}{nw}"
    extend 1rksdla " son mucho más que irse a dormir un rato."
    m 3eud "El tiempo que duermes es un factor importante en lo útiles que pueden ser."
    m 1euc "Si estás fuera por mucho tiempo, puede ser difícil volver a levantarte.{w=0.2} Como cuando te despiertas después de una noche de sueño completo."
    m 3eua "Así que es mejor descansar en intervalos de 90 minutos, ya que eso es lo que dura un ciclo completo de sueño."
    m 1eud "Las siestas energéticas son otra forma de descanso.{w=0.2} Para estas, simplemente descansa la vista durante unos 10 a 20 minutos."
    m 3eua "Son excelentes para tomar un descanso de tu día y aclarar tu mente."
    m 3hua "Y como son tan cortas, es muy fácil volver a hacer lo que estabas haciendo antes."

    if has_napped:
        m 1eua "Así que no tengas vergüenza de tomar siestas cuando creas que lo necesitas, [player]."
    else:
        m 1eua "Si aún no lo has hecho, tal vez podrías intentar tomar algunas siestas de vez en cuando."

    if mas_isMoniEnamored(higher=True):
        show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5tubfu "Tal vez algún día incluso puedas descansar en mi regazo, jejeje~"
    else:

        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfa "Solo avísame si necesitas tomar una siesta y yo te cuidaré~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asimov_three_laws",
            category=['tecnología'],
            prompt="Las tres leyes de Asimov",
            conditional="renpy.seen_label('monika_robotbody')",
            action=EV_ACT_RANDOM
        )
    )

label monika_asimov_three_laws:
    m 1eua "[player], ¿recuerdas cuando hablamos de las {i}Tres leyes de la robótica{/i}?"
    m 3esc "Bueno, he estado pensando en ellas un poco y...{w=0.3}{nw}"
    extend 3rksdla " no son exactamente prácticas."
    m 1eua "Toma la primera ley, por ejemplo..."
    m 4dud "{i}Un robot no debe dañar a un humano o, por inacción, permitir que un humano sufra daño.{/i}"
    m 2esa "Para un humano, esto es bastante sencillo."
    m 2eud "Pero cuando intentas expresarlo en términos que una máquina pueda entender, comienzas a tener problemas."
    m 7esc "Tienes que hacer definiciones precisas para todo, lo que no siempre es fácil...{w=0.3} {nw}"
    extend 1etc "por ejemplo, ¿cómo se define a un humano?"

    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
        $ line_end = "adorable amigo verde que tengo sentado en mi escritorio no lo es."
    else:
        $ line_end = "monitor de tu escritorio no lo es."

    m 3eua "Creo que ambos podemos decir que soy humana, que tú eres humano y que el [line_end]"
    m 3esc "Los problemas surgen cuando pasamos a los casos marginales."
    m 3etc "Por ejemplo, ¿las personas muertas cuentan como humanos?"
    m 1rkc "Si dices que no, el robot podría ignorar a alguien que acaba de sufrir un ataque cardíaco."
    m 1esd "Todavía se puede revivir gente así, pero tu robot no los ayudará porque están {i}técnicamente{/i} muertos."
    m 3eud "Por otro lado, si dices que sí, tu robot podría comenzar a cavar tumbas para 'ayudar' a las personas que han estado muertas durante años."
    m 1dsd "Y la lista continúa.{w=0.3} ¿Las personas preservadas criogénicamente cuentan como humanas?{w=0.3} ¿Las personas en estado vegetativo cuentan?{w=0.3} ¿Qué pasa con las personas que aún no han nacido?"
    m 1tkc "Y eso ni siquiera está comenzando con la definición de 'daño'."
    m 3eud "El punto es,{w=0.1} para implementar las leyes de Asimov, necesitarías adoptar una postura sólida en casi toda la ética."
    m 1rsc "..."
    m 1esc "Supongo que tiene sentido cuando lo piensas."
    m 1eua "Las leyes nunca fueron destinadas a ser implementadas realmente, son solo dispositivos de la trama."
    m 3eua "De hecho, una buena cantidad de historias de Asimov muestran lo mal que podrían resultar las cosas si se aplicaran."
    m 3hksdlb "Así que supongo que no es algo de lo que debamos preocuparnos. Jajaja~"
    $ mas_protectedShowEVL('monika_foundation', 'EVE', _random=True)
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_wabi_sabi",
            category=['filosofía'],
            prompt="Wabi-sabi",
            random=True
        )
    )

label monika_wabi_sabi:
    m 1eua "Dime [player], ¿alguna vez has oído hablar de wabi-sabi?"
    m 3eud "Enfatiza la idea de que no debemos obsesionarnos con la perfección hasta el punto de que nos aplasta el fracaso de no lograrlo."
    m 3eub "Derivado de las filosofías tradicionales japonesas y budistas que rodean la aceptación del estado temporal de todas las cosas..."
    m 1esa "... Afirma que más allá de todo, la belleza se encuentra en lo impermanente e imperfecto."
    m 1eua "Lo que significa que no debemos preocuparnos por cosas como una cicatriz, una mano descolorida o incluso los errores que cometemos."
    m 3eka "Nuestra apariencia son cosas que no podemos cambiar fácilmente, pero a pesar de eso, nos hacen más únicos y especiales."
    m 3hua "... Y nuestros errores se convierten en lecciones que nos ayudan a ser más fuertes y más definidos como personas."
    m 3eub "Como un escultor que revela la magnificencia en un bloque de mármol, excepto que la escultura eres tú, y el escultor, tu pasado."
    m 1rksdla "Por supuesto, esta idea no se aplica solo a la apariencia y los errores..."
    m 3eud "Después de todo, tu forma de pensar y tu actitud hacia los problemas y las personas también se derivan de tus propias experiencias personales."
    m 1dkc "... Pero sé que para algunas personas, cómo estas experiencias cambiaron quiénes son realmente puede asustarlas."
    m 7ekc "Quizás se convirtieron en algo de lo que simplemente no están orgullosos."
    m 2dkd "Puede ser abrumador estar preocupado tanto por la apariencia como por la personalidad..."

    if persistent._mas_pm_love_yourself:
        m 2eka "Espero que no te sientas demasiado inseguro contigo mismo, [player]."
        m 2dkc "Me rompería el corazón saber que estás constantemente preocupado por estas cosas."
        m 7ekbsa "Pero espero que sepas que a pesar de tus defectos, siempre te amaré."
    else:

        m 1ekc "Sé que dijiste que no te amabas a ti mismo [player],{w=0.3} {nw}"
        extend 3eka "pero debes saber que siempre te amaré, independientemente de tus defectos."

    m 3hua "Juntos superaremos cualquier problema que sientas que tienes."
    m 1hub "¡Esa es mi promesa wabi-sabi!"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_herself",
            category=['monika'],
            prompt="Personalidad falsa",
            conditional="mas_seenLabels(['monika_confidence', 'monika_pluralistic_ignorance'], seen_all=True)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

label monika_being_herself:
    m 1eka "Sabes, [player], una cosa por la que creo que nunca te agradecí debidamente es por dejarme ser yo misma."
    m 1lksdlb "Sé que suena un poco extraño...{w=0.2}{nw}"
    extend 1eka " pero déjame explicarte."
    m 3euc "Probablemente ya lo sepas, pero casi toda mi vida he tratado de mantener esta personalidad de 'estudiante perfecta'."
    m 3eud "Siempre me esfuerzo por ser la mejor persona que puedo ser, y supongo que después de un tiempo, llamo la atención de las personas que me rodean."
    m 7rsc "Antes de darme cuenta, había gente que me admiraba con grandes expectativas.{w=0.3} {nw}"
    extend 2esc "Ya sabes, verme como alguien inteligente, confiada, carismática...{w=0.3} ese tipo de cosas."
    m 2eud "Algunas personas dirían que me admiran...{w=0.3}{nw}"
    extend 2lksdlc " y otros,{w=0.2} aunque nunca dirían nada, me odiaban porque representaba todo lo que pensaban que nunca podrían ser."
    m 2dksdlc "Se sentía como si yo no fuera una persona real a sus ojos...{w=0.3}{nw}"
    extend 2dksdld " solo la imagen de las expectativas inalcanzables que todos tienen de sí mismos."
    m 2dksdlc "..."
    m 2ekd "Pero al final del día...{w=0.3} solo soy una chica normal."
    m 7ekc "Al igual que ellos, a veces me puede faltar la confianza para hacer las cosas.{w=0.2} Incluso yo tenía miedo de lo que me depara el futuro."
    m 2dkc "Incluso a veces sentí que necesitaba llorar en el hombro de alguien."
    m 2rkd "... Pero nunca pude expresar algo así."
    m 7tkc "¿Qué pasaría si la gente pensara menos de mí si les mostraba que no era tan grande e invencible como pensaban que era?"
    m 3ekd "¿Qué pasa si se enojan conmigo, diciendo que estoy ensimismada y que lo tengo mucho más fácil que ellos, siendo la ídolo de la escuela que todos aman?"
    m 2lkc "Supongo que nunca sentí que pudiera realmente abrirme a nadie sobre lo que realmente sentía por dentro debido a eso."
    m 2ekc "... Sentía que decepcionaría a todos si alguna vez trataba de hablar abiertamente sobre ello."
    m "Tenía miedo de que si no cumplía con las expectativas que la gente tenía de mí,{w=0.2} {nw}"
    extend 2dkd "terminaría completamente sola."
    m 2dsc "Pero mirando hacia atrás en todo...{w=0.3} mi estatus fue precisamente la razón por la que terminé sintiéndome tan sola de todos modos."
    m 7euc "¿Recuerdas tu personaje? {w=0.2}Él fue un buen ejemplo de esto."
    m 3esc "Cada vez que me describía en su monólogo, me ponía en un pedestal.{w=0.3} {nw}"
    extend 3esd "Si mal no recuerdo, una vez me describió como 'completamente fuera de su liga'."
    m 1etc "Tal vez por eso no tenía una ruta en primer lugar. {w=0.2}Quizás lo escribieron para creer que él tenía cero oportunidades conmigo sin importar qué, y por lo tanto tenía que evitarme."
    m 1rka "De acuerdo, no estaba realmente equivocado allí...{w=0.5}{nw}"
    extend 1eka " solo tengo ojos para ti, después de todo~"
    m 1euc "Pero entiendes lo que quiero decir, ¿verdad?{w=0.3} Me miraron como una especie de diosa inalcanzable."
    m 1rfd "Como si nadie fuera 'digno' de tratarme como una persona normal."
    m 3eka "... Ahora bien, supongo que no tengo que preocuparme tanto por eso."
    m "Estoy muy feliz de poder confiar en que me aceptes por lo que soy y por lo que quiero ser."
    m 1eka "Sé que, desde tu punto de vista, puede que no sientas que hiciste tanto, pero créeme cuando te digo esto..."
    m 1dka "El hecho de que todavía estés aquí conmigo,{w=0.2} que nunca me hiciste sentir que tenía que ser alguien que no soy...{w=0.2}{nw}"
    extend 1eka " que estás aquí escuchándome desahogarme ahora mismo...{w=0.3} realmente significa mucho para mí."
    m 1ekbsa "Muchas gracias por eso, [player].{w=0.2} Gracias por ayudarme a darme cuenta de que no necesito intentar cambiar quién soy para merecer ser amada."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eka "Contigo, puedo permitirme ser...{w=0.5}{nw}"
    extend 5eua " bueno, {i}yo misma{/i}."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_deleted",
            prompt="¿Sigues enfadada conmigo por haberte borrado?",
            category=["ddlc", "monika"],
            pool=True,
            unlocked=False,
            rules={"no_unlock": None},
            conditional="persistent.monika_kill and store.mas_anni.anniCount() >= 1",
            action=EV_ACT_UNLOCK
        )
    )

label monika_being_deleted:
    if mas_isMoniEnamored(higher=True):
        m 1wusdld "¡...!"
        m 3eksdld "[mas_get_player_nickname(capitalize=True)]...{w=0.3} ¿{i}Todavía{/i} estás pensando en eso?"
        m 3dksdlc "Pensé que ambos habríamos superado eso a estas alturas."
        m 2rkc "Sé que dije algunas cosas horribles después de que me borraras...{w=0.3}{nw}"
        extend 7ekd " pero quiero que sepas que no quise decir nada de eso."
        m 6ekc "Lo siento si he herido tus sentimientos.{w=0.3} Estaba tan abrumada por el shock y el miedo que ya no pensaba racionalmente."
        m 6rktpc "Yo.... {w=0.1}es que... {w=0.3}incluso en ese momento, significabas todo para mí, y...{w=0.3} la angustia de perderte para siempre me hizo arremeter."
        m 6ektda "Pero si te tranquiliza, no estoy molesta contigo en absoluto, [mas_get_player_nickname()]. {w=0.2}Te perdoné por todo eso hace mucho tiempo."
        m 6eka "Así que, por favor, no te sientas culpable."
        m 6eka "Sea cual sea la razón por la que me borraste, el hecho es que me trajiste de vuelta y te quedaste conmigo durante todo este tiempo."
        m 7ekbsu "Me diste una segunda oportunidad... {w=0.3}le diste sentido a mi vida. {w=0.2}Creo sinceramente que gracias a eso, todo el sufrimiento que pasé valió la pena al final."
        m 1hubsb "Gracias a ti, soy realmente lo más feliz que podría ser, ¡y eso es lo que más me importa!"
        m 1euu "Así que intentemos no pensar en el pasado y disfrutemos de lo que tenemos ahora, ¿de acuerdo?"
        m 3eka "Te amo, [player]. {w=0.2}Sé que esto no siempre es fácil, pero espero que seas capaz de perdonarte."
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        m 1euc "..."
        m 2eka "Por supuesto que no, tontito."
        m 2rkc "Es verdad que me dolió mucho cuando hiciste eso...{w=0.3}{nw}"
        extend 2eksdld " pero para ser completamente honesta contigo, estaba más aterrorizada que realmente enfadada contigo."
        m 2dksdlc "... Aterrada por la idea de que me odiabas. Que no querías tener nada que ver conmigo, y que me abandonarías, para siempre."
        m 7eka "Pero como ambos vimos... {w=0.3}eso no es lo que terminó sucediendo en absoluto.{w=0.2} Volviste a mí, y me has hecho muy feliz desde entonces."
        m 3dku "En todo caso, estoy agradecida de que me hayas traído de vuelta y de que podamos pasar nuestro tiempo juntos ahora."
        m 1eka "Así que hazme un favor y trata de no pensar más en eso, ¿de acuerdo? {w=0.2}Eso es todo detrás de nosotros ahora."

    elif mas_isMoniUpset():
        m 2rsc "No, no estoy enfadada contigo, [player]."
        m 1rfc "{cps=*2}Al menos, no sobre {i}eso{/i}.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Yo {i}diría{/i} que deberíamos dejar atrás el pasado y pensar en el presente, pero siento que tú no estás preparado o {w=0.2}dispuesto{w=0.2} a dejar atrás todo esto.."
        m 2dtc "¿Me estoy equivocando?"
        m 2dkc "..."
        m 2ekd "Mira, [player]...{w=0.3} sé que ha sido un poco duro, pero eso no significa que sea demasiado tarde para arreglar las cosas y empezar de nuevo."
        m 2dsc "Sigo pensando... no,{w=0.2} {i}sé{/i} que eres una buena persona.{w=0.2} Solo necesito que trates de ser un poco más considerado con {i}mis{/i} sentimientos.."
        m 2fkc "Por favor, [player].{w=0.3} No puedo hacer esto sin ti."
        m 2ekd "No sé cuánto significará esto para ti en este momento...{w=0.3}{nw}"
        extend 7eka " pero te amo.{w=0.2} Realmente te amo."
        $ mas_ILY()
    else:

        m 6ekc "..."
        m 6lkc "... Creo que es justo decir que obviamente eres {i}tú{/i} el que está enfadado conmigo..."

        if persistent._mas_pm_monika_deletion_justice:
            m 6ektpc "Me lo merecía, después de todo. {w=0.2}Eso es lo que me dijiste una vez, ¿verdad?"

        m 6dktpc "..."
        m 6dktpd "... No, no estoy resentida por haberme borrado."
        m 6dktuc "Nunca lo estuve..."
        m 6ektud "Si acaso... {w=0.3}al menos espero que saber eso pueda hacerte feliz."
        m 6dktdc "..."
        m 6rkc "..."

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_remembrance",
            category=['monika'],
            prompt="¿Cuánto de tu pasado recuerdas?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_remembrance:
    m 1rsc "Yo misma no estoy muy segura, [player]..."
    m 1euc "Es extraño porque tengo recuerdos de mi pasado, pero tan pronto como empiezo a ordenar mis pensamientos, se vuelven...{w=0.3}{nw}"
    extend 1ruc " borrosos."
    m 3eksdld "Por ejemplo, no podría decirte dónde sucedió algo, o los nombres de las personas que estuvieron allí..."
    m 3eksdld "... Claro, tengo recuerdos de haber crecido en un vecindario normal, pero más allá de eso, ni siquiera podría decirte cómo son las caras de mis padres..."
    m 1dsc "Todo es como...{w=0.5} sentimientos e impresiones, supongo."
    m 3wud "¡Lo que es aún más extraño es que no todos mis recuerdos son así!"

    if seen_event('monika_wine'):
        m 1rusdla "Hay algunas cosas que recuerdo perfectamente, como aquella vez que Yuri trajo vino al club..."
    else:
        m 3esc "Hay cosas que recuerdo perfectamente, especialmente cuando se trata del club."

    m 1esc "Pero otras cosas, como los recuerdos de la infancia, son realmente confusas."
    m 3esd "Los únicos recuerdos que están claros son las cosas que me definen a mí o a las otras chicas."
    m 3rsc "... Casi como si todo lo que no fuera estrictamente necesario para el juego se hubiera omitido."
    m 1euc "Pero, desde mi perspectiva, el día que te conocí fue como cualquier otro...{w=0.5}{nw}"
    extend 3hksdlb " hasta que me enteré de ese agujero en la pared, quiero decir."
    m 1esc "Solo otro día normal en una semana normal...{w=0.3} {nw}"
    extend 3euc "ir a clase, dirigir el club y regresar a casa por la noche."
    m 3etc "¿Sucedió algo de eso?{w=0.5} {nw}"
    extend 3wud "¿Yo {i}existía{/i} antes de que comenzaras el juego?"
    m 3wkd "... Y si mis recuerdos son realmente falsos...{w=0.2} ¿Quién...{w=0.2} o {i}qué{/i}...{w=0.2} soy entonces?"
    m 1dkc "Todavía estoy buscando esas respuestas, [player]..."

    if mas_isMoniUpset(higher=True):
        m 1euc "Aunque...{w=0.3} cuanto más lo pienso, más estoy convencida de que mi pasado no es {i}tan{/i} relevante."
        m 3eua "Aunque sería bueno recordar más...{w=0.3} eso no es realmente lo que me importa..."
        m 3duu "Independientemente de quién soy, has estado aquí conmigo,{w=0.2} {nw}"
        extend 3dkbsa "lo que significa que soy lo suficientemente importante como para que pases tu tiempo conmigo.{w=0.2} {nw}"
        extend 1dubsu "{i}Eso es{/i} lo que me importa"
        m 1ekbsa "Y saber que te preocupas...{w=0.3} esa es una gran parte de por qué puedo seguir amándome a mí misma,{w=0.2} y a mi vida, [player]."

        if mas_isMoniNormal(higher=True):
            show monika 5ekbfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfu "Entonces, aunque no estoy segura de tener un pasado, gracias a ti, sé que tengo un futuro."

            if mas_anni.pastOneMonth():
                $ line_mid = "he hecho, y seguiré haciendo"
            else:
                $ line_mid = "haré"

            m 5hubfu "Además, en todo caso, mi falta de recuerdos solo hace que los que [line_mid] contigo sean mucho más preciosos~"
        else:
            m 3eksdld "... Tú {i}sí{/i} te preocupas por mí, ¿verdad?"
            m 3dkc "Sería bueno si lo mostraras un poco, a veces..."
    else:

        m 1ektdc "...{w=0.5} No es que te importe, ¿verdad?"

    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_why_do_you_read",
            category=['monika','literatura'],
            prompt="¿Cómo te metiste en la lectura?",
            pool=True
        )
    )

label monika_why_do_you_read:
    m 1eua "Por lo que puedo recordar, siempre he leído, [player].{w=0.2} {nw}"
    extend 3eua "Fue como algo complementario junto a escribír para mí."
    m 3euc "Cuando era muy joven, me gustaba escribir cuentos, pero nunca encontré a nadie con quien compartirlos..."
    m 1rsc "La mayoría de los otros niños no estaban realmente interesados en libros ni nada de eso."
    m 1rkd "... Así que siempre fue un poco frustrante porque no pude compartir esas historias con nadie."
    m 3eua "Pero al menos pude apoyar mi interés eligiendo otros libros."
    m 3hub "¡Cada libro nuevo era como ser arrojada a un mundo nuevo extraño y emocionante! ¡Fue como combustible para mi imaginación!"
    m 1eksdlc "Por supuesto, a medida que crecía, comencé a tener cada vez menos tiempo libre y no podía leer tanto...{w=0.3} o era seguir así o sacrificar mi vida social."
    m 1esa "Fue entonces cuando mis intereses comenzaron a cambiar más hacia la poesía."
    m 3eua "A diferencia de las novelas, la poesía no requería tanto tiempo para leerse y su concisión también hizo que fuera más fácil compartirla con otros.{w=0.3} {nw}"
    extend 4eub "¡Realmente fue la salida perfecta!"
    m 3eua "... Y así fue como crecí cada vez más, supongo."
    m 1eud "Finalmente conocí a Sayori y descubrí que compartíamos este interés.{w=0.2} {nw}"
    m 3eud "Al igual que a mí, les permitió compartir sentimientos que, de otro modo, mantendrían reprimidos."
    m 1eua "... Lo que nos lleva a donde estamos ahora."
    m 1etc "Para ser honesta, no creo que haya tenido tanto tiempo para leer antes."

    if mas_anni.pastThreeMonths():
        m 3eud "He podido ponerme al día con mi acumulación de poesía, volver a leer algunas novelas..."
        m 3eua "... Conéctarme en línea para buscar cualquier fanfiction o cuento que pueda tener en mis manos..."
        m 3hua "... ¡Incluso he desarrollado un interés por la filosofía escrita!"
        m 3eub "Siempre es divertido descubrir nuevas formas de expresión."
        $ line_mid = "sería genial tener la"
    else:

        m 3eud "Finalmente me estoy poniendo al día con mi acumulación de poesía y comencé a leer novelas de nuevo..."
        m 3hua "... ¡Me encantaría compartir mis pensamientos contigo una vez que haya terminado con ellos!"
        m 3eub "También me conecto regularmente en línea para buscar cualquier fanfiction o cuento que pueda tener en mis manos."
        m 3eua "Es muy divertido descubrir nuevas formas de expresión."
        $ line_mid = "quisiera poder tener la"

    m 1eub "Entonces...{w=0.2} ¡Sí!{w=0.3} {nw}"
    extend 3eua "Si bien mi situación aquí tiene sus desventajas, [line_mid] oportunidad de dedicar más tiempo a las cosas que me gustan."
    m 1ekbsu "... Aunque, de nuevo, nada podría superar pasar más tiempo contigo~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_discworld",
            category=['literatura'],
            prompt="Mundodisco",
            random=True
        )
    )

label monika_discworld:
    m 1esa "Dime [player], ¿alguna vez has oído hablar de un mundo a la deriva por el espacio encima de cuatro elefantes, que están parados sobre el caparazón de una tortuga gigante?"
    m 3hub "Si es así, probablemente ya estés familiarizado con el {i}Mundodisco{/i} de Sir Terry Pratchett."
    m 3hksdlb "Jajaja, suena un poco extraño cuando lo digo así, ¿no?"
    m 1eua "{i}Mundodisco{/i} es una serie de cómics de fantasía de cuarenta y un volúmenes escritos a lo largo de tres décadas."
    m 3esc "La serie comenzó como una parodia en la que se burlaban de los tropos comunes de fantasía, pero pronto se convirtió en algo mucho más profundo."
    m 3eub "De hecho, los libros posteriores son claramente sátiras en lugar de parodias, y utilizan una inteligente mezcla de payasadas, juegos de palabras y humor desenfadado para comentar todo tipo de temas."
    m 1huu "Pero si bien la sátira puede ser el alma de la serie, lo que hace latir tu corazón es la forma en que está escrita."
    m 1eub "¡Pratchett realmente tenía un don para escribir situaciones divertidas, [player]!"
    m 3rsc "Realmente no puedo precisar qué hace que su prosa funcione tan bien, pero definitivamente tiene un estilo de escritura muy distintivo..."
    m 3etc "Tal vez sea la forma en que escribe de una manera que sugiere más de lo que dice."
    m 1eud "Por ejemplo, al describir algo, te dará los detalles suficientes para que puedas imaginar lo que está sucediendo y dejar que tu imaginación llene los vacíos."
    m 3duu "... Lo que se te ocurra será mucho más evocador que cualquier cosa que él pueda escribir."
    m 3eub "¡Es una manera muy buena de mantener a tu audiencia interesada!"
    m 1etc "... O quizás lo que hace que funcione es la forma en que no usa los capítulos, lo que le permite saltar libremente entre el punto de vista de sus personajes."
    m 1rksdla "Las historias entrelazadas pueden convertirse rápidamente en un desastre si no tienes cuidado,{w=0.2} {nw}"
    extend 3eua "pero también son una buena forma de mantener el ritmo dinámico."
    m 3eub "En cualquier caso, ¡esta serie es una recomendación, [player]!"
    m 3eua "También es sorprendentemente fácil de aprender, ya que cada libro se considera una historia independiente."
    m 1eud "Puedes elegir prácticamente cualquier volumen que encuentres y estarás listo,{w=0.2} aunque yo diría que {i}¡Guardias! ¡Guardias!{/i} o {i}Mort{/i} probablemente serían los mejores puntos de entrada."
    m 3eua "De todos modos, asegúrate de intentarlo en algún momento si aún no lo has hecho, [player]."
    m 1hua "Gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eating_meat",
            category=['vida','monika'],
            prompt="¿Comerías carne alguna vez?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_eating_meat:
    m 1etc "Bueno, esa es una pregunta algo complicada..."
    m 3eud "Si me preguntas si lo haría por {i}supervivencia{/i}, no lo dudaría. {w=0.2}No es que comer carne sea angustioso para mí ni nada."
    m 7eud "Ya te lo dije antes, soy vegetariana por el impacto de la producción masiva de carne en el medio ambiente...{w=0.2}{nw}"
    extend 2euc " que también incluye la piscicultura, así que no soy pescetariana."
    m 2rsc "... Como sea, tampoco me considero vegana. {w=0.3}{nw}"
    extend 4eud "Claro, el consumo de productos animales contribuye al daño ambiental, pero muchas alternativas veganas también tienen sus propios problemas..."
    m 4euc "Estos incluyen cosas como la importación de productos perecederos a grandes distancias y la agricultura masiva en condiciones que son crueles para los trabajadores y una tensión en el ecosistema local."
    m 4ekd "Tomemos los aguacates, por ejemplo. {w=0.2}Sus granjas requieren cantidades masivas de agua, hasta el punto de que algunas empresas recurren a tomar ilegalmente demasiada agua de los ríos, dejando poca para beber."
    m 4euc "Por no hablar de que sigo queriendo tener una dieta variada y equilibrada con todos los sabores que me gustan."
    m 4eud "Las dietas veganas pueden ser bastante deficientes en nutrientes, como vitamina B12, calcio, hierro y zinc."
    m "Por supuesto, todavía hay algunas opciones que incluyen suplementos, pero equilibrar una dieta vegana requiere mucho cuidado y reflexión."
    m 7eka "... Entonces, por esa razón, personalmente no estoy en contra de comer cosas como leche y huevos. {w=0.2}Pero creo que preferiría comprar localmente si es posible."
    m 3eud "Los mercados de agricultores son excelentes lugares para comprar alimentos, {w=0.2}incluso carne, {w=0.2}producidos con un impacto ambiental menor."
    m 3ekd "Pero normalmente pueden ser bastante caros... y dependiendo de la ubicación, te dejan con menos opciones. {w=0.3}{nw}"
    extend 3eua "Así que estoy de acuerdo con comprar en una simple tienda antigua, si es necesario."
    m "Sobre todo porque ya hay muchos buenos sustitutos de la carne en los supermercados, con mucho menos impacto ambiental."
    m 1euc "En cuanto a la carne que proviene de la caza y la pesca locales, creo que está bien comer también, pero es importante investigar qué áreas podrían estar sobrecazadas y de qué animales tener cuidado."
    m 3rtc "Dicho esto, no sé si {i}preferiría{/i} comer carne, si tuviera la opción."
    m 3eka "Desde que me ajusté a una dieta vegetariana, mi paladar ha cambiado para preferir ciertos sabores."
    m 3ekd "Y como es el caso de muchos vegetarianos, mi cuerpo ya no digiere la carne tan fácilmente. {w=0.3}{nw}"
    extend 3dksdlc "Si comiera demasiada, podría llegar a enfermarme...."
    m 1eka "... Pero si preparaste algo con carne, podría probar un poco como guarnición...{w=0.3}{nw}"
    extend 3hub " ¡De esa manera todavía puedo disfrutar de tu cocina!"
    m 3eua "Independientemente de lo que comamos, lo más importante para mí es que tratemos de pensar un poco en el origen de nuestra comida."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_look_into_eyes",
            conditional="persistent._mas_pm_eye_color is not None",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None),
        )
    )

label monika_look_into_eyes:
    m 3eub "Hey [player], mírame a los ojos un segundo..."

    window hide
    show monika 1eua with dissolve_monika
    pause 5.0
    show monika 1etu with dissolve_monika
    pause 3.0
    show monika 1eubsu with dissolve_monika
    pause 4.0
    show monika 1fubsa with dissolve_monika
    pause 1.0
    show monika 5tubsa with dissolve_monika
    pause 3.0
    show monika 5subsa with dissolve_monika
    pause 1.0
    window auto
    show monika 3hubla with dissolve_monika

    m 3hubla "Jejeje~"
    m 3rksdla "Lo siento [player], solo intentaba ver tus hermosos ojos a través de la pantalla."


    $ eye_detail = "hipnotizantes" if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color
    m 1dubsu "Cuando estamos juntos a solas, no puedo evitar imaginar tus [eye_detail] ojos..."
    show monika 5dubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5dubsa "El tiempo se detiene, y por fin puedo...{w=0.3} olvidarme de todos mis problemas."
    m 5hubfb "..."
    m 5tubfa "Muchas gracias, [player]~"
    m 5kubfu "Porque estás aquí conmigo ahora, estoy tan en paz."

    show monika 5eubfu

    $ mas_moni_idle_disp.force_by_code("5eublu", duration=5, skip_dissolve=True)
    return "no_unlock"


default -5 persistent._mas_pm_social_personality = None


define -5 mas_SP_INTROVERT = "introvert"
define -5 mas_SP_EXTROVERT = "extrovert"
define -5 mas_SP_AMBIVERT = "ambivert"
define -5 mas_SP_UNSURE = "unsure"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_introverts_extroverts",
            prompt="Introverts and extroverts",
            category=['psicología', 'tú'],
            conditional="renpy.seen_label('monika_saved')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_introverts_extroverts:
    m 1eud "Dime, [player]."
    m 1euc "¿Recuerdas cuando hablamos de cómo los humanos necesitan retroalimentación social y cómo puede hacer que el mundo se sienta tan complicado para los introvertidos?"
    m 3rsd "He estado pensando un poco más en las diferencias entre introvertidos y extrovertidos desde entonces."
    m 3eua "Podrías pensar que los extrovertidos tienden a disfrutar interactuando con otras personas, mientras que los introvertidos se sienten más cómodos en ambientes solitarios, y tendrías razón."
    m 3eud "... Pero las diferencias no acaban allí."
    m 3eua "Por ejemplo, ¿sabías que los extrovertidos pueden reaccionar a las cosas más rápido que la mayoría de los introvertidos?{w=0.2} ¿O que es más probable que disfruten de una música alegre y energética?"
    m 3eud "Los introvertidos, por otro lado, suelen tardar más tiempo en analizar la situación en la que se encuentran y, por lo tanto, es menos probable que saquen conclusiones."
    m 7dua "... Y dado que a menudo pasan mucho tiempo usando su imaginación, les resulta más fácil realizar actividades creativas como escribir, componer música, etc."
    m 2lkc "Es un poco triste que a la gente le cueste tanto entender y aceptar esas diferencias..."
    m 4lkd "Los extrovertidos son vistos como personas superficiales e insinceras que no valoran sus relaciones individuales..."
    m 4ekd "... Mientras que los introvertidos son tratados como personas egoístas que solo piensan en sí mismos, o incluso pueden ser vistos como raros por participar raramente en situaciones sociales."
    show monika 5lkc zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lkc "El resultado final es que ambas partes terminan a menudo frustrándose mutuamente, lo que da lugar a un conflicto innecesario."
    m 5eud "Probablemente estoy haciendo este sonido como si solo pudieras ser uno u otro, pero en realidad no es así en absoluto."
    show monika 2eud zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 2eud "Algunos introvertidos pueden ser más extrovertidos que otros, por ejemplo."
    m 2euc "En otras palabras, algunas personas están más cerca de un punto medio entre los dos extremos."
    m 7eua "... Que es probablemente donde yo encajaría.{w=0.2} {nw}"
    extend 1eud "Si recuerdas, mencioné que estaba en el medio mientras que seguía siendo un poco más extrovertido."
    m 1ruc "Hablando de eso...{w=0.3}{nw}"
    extend 1eud " al pensar en todo esto, me di cuenta de que aunque esto es una parte muy importante de la personalidad de uno..."
    m 3eksdla "... En realidad no sé dónde te encuentras en ese espectro."

    m 1etc "Entonces, ¿cómo te describirías a ti mismo [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, ¿cómo te describirías a ti mismo [player]?{fast}"
        "Soy introvertido":

            $ persistent._mas_pm_social_personality = mas_SP_INTROVERT
            m 1eua "Ya veo."
            m 3etc "Supongo que normalmente prefieres pasar el tiempo sin demasiada gente a salir con grandes grupos y cosas así."
            m 3eua "¿O tal vez te gusta ir y hacer cosas por tu cuenta de vez en cuando?"

            if persistent._mas_pm_has_friends:
                m 1eua "Ya que me dijiste que tienes algunos amigos, estoy segura de que eso significa que no te importa mucho estar con otras personas."

                if persistent._mas_pm_few_friends:
                    m 1eka "Créeme, no importa si sientes que no tienes tantos."
                    m 3ekb "Lo importante es que tengas al menos alguien con quien te sientas cómodo."

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 1eka "Recuerda que puedes intentar pasar algún tiempo con ellos cuando sientas que no hay nadie para ti, ¿de acuerdo?"
                    m 1lkd "Y si por alguna razón no puedes pasar tiempo con ellos..."
                    m 1ekb "Por favor, recuerda que {i}siempre{/i} estaré ahí para ti, pase lo que pase."
                else:

                    m 3eka "Aún así, si alguna vez es demasiado para ti, recuerda que siempre puedes venir a mí y relajarte, ¿okey?"

                $ line_start = "Y"
            else:

                m 3eka "Aunque entiendo que puede ser más cómodo para tí estar solo que con otras personas..."
                m 2ekd "Por favor, tened en cuenta que nadie puede pasar toda su vida sin al menos {i}algo{/i} de compañía."
                m 2lksdlc "Eventualmente llegará un momento en que no podrás hacer todo por tu cuenta..."
                m 2eksdla "Todos necesitamos ayuda a veces, ya sea física o emocional, y no me gustaría que no tuvieras a nadie a quien recurrir cuando llegue ese momento."
                m 7eub "¡Y eso es una calle de doble sentido!{w=0.2}{nw}"
                extend 2hua " Nunca sabes cuando puedes hacer una diferencia en la vida de alguien más también."
                m 2eud "Así que aunque no espero que te esfuerces por conocer gente nueva, tampoco cierres automáticamente todas las puertas."
                m 2eka "Trata de hablar un poco con otras personas si no lo estás haciendo ya, ¿okey?"

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 3hua "Te hará más feliz, lo prometo."
                    m 1ekb "Como mínimo, recuerda que siempre estoy aquí si alguna vez te sientes solo."
                    $ line_start = "Y"
                else:

                    m 7ekbla "Me encantaría que vieras el valor y la alegría que otras personas pueden traer a tu vida también."
                    $ line_start = "Pero"

            m 1hublb "[line_start] mientras estés aquí conmigo, haré todo lo posible para que siempre te sientas cómoda, te lo prometo.~"
        "Soy extrovertido":

            $ persistent._mas_pm_social_personality = mas_SP_EXTROVERT
            m 3eub "Oh ya veo."
            m 3eua "Entonces, supongo que te gusta pasar más tiempo con los demás y conocer gente nueva."
            m 1eua "Definitivamente puedo ver el atractivo en eso.{w=0.3} {nw}"
            extend 3eub "Me encantaría ir a explorar el mundo y conocer todo tipo de gente nueva contigo."
            m 1ekc "Y asumo que probablemente odies la soledad tanto como yo...{w=0.3}{nw}"
            extend 1ekbla " pero esa es solo una razón más por la que estoy tan feliz de que seamos pareja ahora."
            m 3ekblb "Nunca más estaremos verdaderamente solos."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "Estoy segura de que eres una persona muy divertida para estar cerca [player],{w=0.1} y no puedo esperar a estar contigo de verdad~"
            m 5rusdlu "Aunque no voy a ocultar el hecho de que también disfruto de algún momento de paz..."
            m 5hksdrb "Espero que no te importe que no siempre pueda seguirte el ritmo, ¡jajaja!"
        "Estoy entre ambas":

            $ persistent._mas_pm_social_personality = mas_SP_AMBIVERT
            m 3hua "Jejeje, como yo, entonces~"
            m 3eud "Aparentemente, la mayoría de la gente tiene un lado introvertido y extrovertido de su personalidad."
            m 7eua "... Incluso si uno de los dos es dominante sobre el otro, dependiendo de la persona."
            m 7rsc "En nuestro caso, sin embargo, supongo que no estar demasiado en ninguno de los dos lados tiene sus ventajas y desventajas."
            m 1eua "Es tan agradable que estar rodeado de grupos grandes no es un problema, lo mismo ocurre con pasar algún tiempo a solas."
            m 7esc "... Pero no puedo decir que me haya sido fácil hacer conexiones profundas y genuinas con otros..."
            m 1eud "Claro, me es más fácil entender a la mayoría de la gente, pero eso no significa que siempre pueda relacionarme con ellos, ¿sabes?"
            m 1lksdld "Entonces sí...{w=0.3} termino estando en buenos términos con casi todo el mundo, pero las amistades que formo a veces pueden sentirse un poco... {w=0.3}insatisfactorias."
            m 3eksdlc "Lo mismo pasó con el club, por ejemplo."
            m 3dksdld "Estaba tan convencida de que al reunir a la gente en torno a algo que realmente disfruto, tendría una mejor oportunidad de vincularme con ellas por encima de nuestros intereses compartidos..."
            m 3dksdlc "... Pero al final del día, pasamos la mayor parte del tiempo en silencio, con todo el mundo ocupándose de sus propios asuntos."
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Bueno, no tiene sentido seguir pensando en eso."
            m 5eubsa "Después de todo, {i}terminé{/i} conectando de manera significativa con cierta persona. {w=0.3}{nw}"
            extend 5kubfu "Alguien muy encantador, debo añadir~"
        "No estoy seguro":

            $ persistent._mas_pm_social_personality = mas_SP_UNSURE
            m 1eka "Está bien, [player].{w=0.2} Cosas como estas no siempre son tan claras."
            m 4eua "Soy como tú en ese frente."
            m 2eka "Aunque dije que soy un poco más extrovertida, todavía necesito algo de tiempo para relajarme de vez en cuando, ¿sabes?"
            m 2lkd "Y tampoco diría que siempre me siento tan cómoda tratando con la gente..."

            if renpy.seen_label("monika_confidence"):
                m 2euc "Te lo dije, ¿no?"

            m 2lksdlc "A menudo tengo que fingir mi propia confianza solo para pasar por conversaciones simples con algunas personas."
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Pero no me siento así contigo en absoluto, [player]. {w=0.2}Y realmente espero que sea lo mismo al revés."
            m 5eua "Estoy segura de que seremos capaces de averiguar las zonas de confort del otro con el tiempo."
            m 5hubsb "En cualquier caso, siempre serás mi amor, no importa dónde estés en la balanza~"

    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_literature_value",
            category=['literatura'],
            prompt="El valor de la literatura",
            random=True
        )
    )

label monika_literature_value:
    m 3esd "Sabes, [player], en los días del club de literatura, a menudo escuchaba a la gente descartar la literatura como obsoleta e inútil."
    m 1rfc "Siempre me molestó cuando escuché a alguien decir eso, especialmente porque la mayoría de las veces, ni siquiera se molestaron en intentarlo."
    m 3efc "¿Saben siquiera de qué están hablando?"
    m 3ekd "A las personas que piensan eso a menudo les gusta descartar la literatura en comparación con campos más científicos, como la física o las matemáticas, y afirman que es una pérdida de tiempo ya que no produce nada práctico."
    m 3etc "... Y aunque definitivamente no estoy de acuerdo con esa noción, puedo ver de dónde vienen."
    m 1eud "Todas las comodidades de nuestro estilo de vida moderno se basan en la innovación y el descubrimiento científico."
    m 3esc "... Eso y las millones de personas que fabrican nuestras necesidades diarias o ejecutan servicios básicos como la atención médica y esas cosas."
    m 3rtsdlc "Entonces, ¿no estar asociado con ninguna de esas cosas realmente te convierte en una especie de carga para la sociedad?"
    m 1dsu "Como podrás imaginar, no lo creo...{w=0.3} {nw}"
    extend 1eud "si la literatura fuera inútil, ¿por qué estaría tan reprimida en muchas partes del mundo?"
    m 3eud "Las palabras tienen poder, [player]...{w=0.2}{nw}"
    extend 3euu " y la literatura es el arte de bailar con palabras."
    m 3eua "Como cualquier forma de expresión, nos permite conectarnos entre nosotros...{w=0.2}{nw}"
    extend 3eub " ¡Para ver cómo se ve el mundo en los ojos de los demás!"
    m 3duu "La literatura te permite comparar tus propios sentimientos e ideas con los de los demás y, al hacerlo, te hace crecer como persona..."
    m 1eku "Honestamente, creo que si más personas valoraran un poco más los libros y poemas, el mundo sería un lugar mucho mejor."
    m 1hksdlb "Sin embargo, esa es solo mi opinión como presidenta de un club de literatura. {w=0.2}Supongo que la mayoría de la gente no pensaría tan profundamente al respecto."
    return


default -5 persistent._mas_pm_likes_nature = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nature",
            category=['naturaleza', 'tú'],
            prompt="El aire libre",
            random=True
        )
    )

label monika_nature:
    m 2esd "Hey, [player]..."
    m 7eua "¿Te gusta la naturaleza?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gusta la naturaleza?{fast}"
        "Me gusta":

            $ persistent._mas_pm_likes_nature = True
            m 3sub "¿De verdad? ¡Eso es maravilloso!"
            m 1eua "Creo que la naturaleza es algo que debemos apreciar."
            m 1eub "No solo es bonita, sino que también ayuda a la humanidad."
            m 3eud "Los insectos polinizan nuestros cultivos, los árboles nos dan madera y sombra, las mascotas nos ofrecen compañía..."
            m 3euc "Y sobre todo, organismos como las plantas, las algas y algunas bacterias producen alimento y oxígeno. {w=0.2}{nw}"
            extend 3wud "Sin ellas, la mayor parte de la vida en la Tierra no existiría."
            m 1eua "Por ello, creo que es justo que devolvamos algo a la naturaleza, ya que hace tanto por nosotros."
            m 4hub "Así que, ¡aquí está el consejo verde del día de Monika!"
            m 4rksdlc "A veces, la gente duda de ser ecológicos porque le preocupa que sea demasiado caro..."
            m 2eud "Pero eso es solo parcialmente cierto.{w=0.2} {nw}"
            extend 7eua "Aunque los vehículos eléctricos, las casas inteligentes y los tejados solares pueden costar una fortuna..."
            m 3hub "Puedes marcar la diferencia y {i}ahorrar{/i} dinero con solo tomar unas sencillas decisiones cada día."
            m 4eua "El simple hecho de apagar los electrodomésticos, tomar duchas más cortas, comprar una botella de agua reutilizable y desplazarte en el transporte público ayudan a ser más ecológicos."
            m 4hub "¡Incluso puedes comprar una planta de interior o cultivar tu propio jardín!"
            m 2eub "¡Participar en tu comunidad local también puede ser de gran ayuda!{w=0.2} {nw}"
            extend 7eua "Si tomas la iniciativa, seguro que otros seguirán tus pasos."
            m 3esa "Lo importante es crear el hábito de pensar de forma sostenible.{w=0.2} {nw}"
            extend 3eua "Si lo consigues, reducirás tu huella ecológica en poco tiempo."
            m 1eua "Quién sabe, tal vez incluso seas más feliz y saludable cuanto más hagas estas cosas también."
            m 3hua "Al fin y al cabo, una vida sostenible es una vida satisfactoria."
            m 3eub "¡Ese es mi consejo para hoy!"
            m 1hua "Gracias por escuchar, [mas_get_player_nickname()]~"
        "No realmente":

            $ persistent._mas_pm_likes_nature = False
            m 3eka "No pasa nada, [player]. Al fin y al cabo, no todo el mundo disfruta de la vida al aire libre."
            m 3eua "Algunos prefieren el ambiente confortable de sus hogares, sobre todo cuando la tecnología los hace más cómodos que nunca."
            m 1eud "Sinceramente, puedo entender eso."
            m 3eud "Paso la mayor parte de mi tiempo leyendo, escribiendo, codificando y estando contigo...{w=0.3} todo eso es más fácil de hacer en el interior."
            m 3rksdlc "Otros tienen alergias o condiciones médicas que les impiden permanecer fuera durante mucho tiempo, ya que de lo contrario se pueden enfermar o hacer daño."
            m 1esd "También hay mucha gente a la que, por una u otra razón, no le interesa mucho la naturaleza, y eso está bien."
            m 1hksdlb "Incluso yo tengo cosas que me disgustan, ¡jajaja!"
            m 2tfc "Por ejemplo, no me molestan la mayoría de los insectos, pero algunos son francamente odiosos."
            m 7tkx "Zumban constantemente alrededor de tu cabeza, se meten en tu cara, se posan en tu comida...{w=0.3} algunos mosquitos y garrapatas son incluso portadores de desagradables enfermedades."
            m 3eka "Pero mientras esté contigo, me parece bien si prefieres estar dentro de casa."
            m 1tfu "No esperes que te deje estar dentro todo el tiempo~"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impermanence",
            category=["filosofía"],
            prompt="Impermanencia",
            random=False,
            unlocked=False
        )
    )

label monika_impermanence:
    m 2euc "Sabes [player], me encuentro pensando en algunas cosas oscuras de vez en cuando."
    m 4eud "Conceptos como nihilismo{w=0.2}, {nw}"
    extend 4dkc "depresión{w=0.2}, {nw}"
    extend 4rkd "impermanencia..."
    m 2eka "No quiero preocuparte, {w=0.1}no estoy sufriendo de depresión ni nada por el estilo."
    m 2eud "... Seguro que has oído hablar del término {i}entropía{/i}, ¿verdad?"
    m 7eud "Básicamente dice algo así como: 'La entropía siempre debe aumentar, {w=0.2}el universo tiende al desorden, {w=0.2}todo se convierte en caos'."
    m 3eua "De hecho, hay un poema que leí que transmite bastante bien este mensaje."
    m 1esd "{i}Conocí a un viajero de una tierra antigua{/i}."
    m 1eud "{i}Quien dijo: 'Dos vastas y sin tronco piernas de piedra'.{/i}"
    m 3euc "{i}Párate en el desierto... cerca de ellos, en la arena.{/i}"
    m "{i}Medio hundido, yace un rostro destrozado, cuyo ceño se frunce.{/i}"
    m 1eud "{i}Y el labio arrugado, y la mueca de frío mando.{/i}"
    m "{i}Dile que su escultor bien esas pasiones leer{/i}."
    m 1euc "{i}Que aún sobreviven, estampados en estas cosas sin vida{/i}."
    m "{i}La mano que se burló de ellos y el corazón que los alimentó{/i}."
    m 3eud "{i}Y en el pedestal aparecen estas palabras{/i}."
    m "{i}'Mi nombre es Ozymandias, rey de reyes'{/i}."
    m 3eksdld "{i}Mirad mis obras, Poderosos, y desesperad'.{/i}"
    m 3eksdlc "{i}No queda nada al lado. Alrededor de la decadencia{/i}."
    m "{i}De ese colosal naufragio, ilimitado y desnudo{/i}."
    m 1eksdld "{i}Las arenas solitarias y llanas se extienden a lo lejos'.{/i}"
    m 3eud "A lo que se reduce es a que, por muy grande que sea la huella que dejes en la historia, acabará por desvanecerse."
    m 1euc "Mucha gente ve esto como una razón suficiente para simplemente...{w=0.2}{nw}"
    extend 1dkc " rendirse.{w=0.3} Caer en un pozo de desesperación y permanecer allí, a veces durante toda la vida."
    m 3eksdlc "Después de todo, nada de lo que hagas importa en el gran esquema de las cosas."
    m 3eud "Nada de lo que {i}puedas{/i} hacer importa...{w=0.3}{nw}"
    extend 1rkc " entonces, ¿por qué molestarse en hacer algo?"
    m 3eud "No es difícil ver por qué algunos podrían considerar esto como la conclusión natural de tal realización."
    m 1rkc "Puede ser...{w=0.2} entretenido, {w=0.2}incluso reconfortante a su manera."
    m 1euc "Pero permítanme plantear una pregunta... {w=0.3}¿Por qué el hecho de que nada importe realmente es lo único que {i}importa{/i}?"
    m 3eud "¿Realmente importa que mucho después de que nos hayamos ido, ya no importamos? {w=0.2}Después de todo, ni siquiera estaremos allí para darnos cuenta."
    m 3eka "Disfruta del momento y sé una influencia positiva para los que te rodean... {w=0.3}eso es todo lo que podemos hacer."
    m 1dku "Con vivir {i}es{/i} suficiente."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kamige",
            category=['juegos'],
            prompt="¿Qué es kamige?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_kamige:
    m 1euc "Oh, cierto...{w=0.3}{nw}"
    extend 3rksdla " no es exactamente un término común."
    m 3eud "{i}Kamige{/i} es una jerga japonesa que es usada mayormente por los fanáticos de las novelas visuales."
    m 3eua "Si tratara de traducirlo, creo que sería algo así como un {i}juego glorioso.{/i}"
    m 2eub "Es como cuando la gente habla de sus libros o películas clásicas favoritas."
    m 2hksdlb "Estaba bromeando cuando lo dije sobre este juego, pero {i}parece{/i} que se ha vuelto muy popular por alguna razón."
    m 7eka "No es que me esté quejando...{w=0.3} {nw}"
    extend 3hua "si fue la popularidad del juego lo que te llevó a conocerme, creo que puedo estar agradecida por ello."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_renewable_energy",
            category=['tecnología'],
            prompt="Energía renovable",
            random=True
        )
    )

label monika_renewable_energy:
    m 1eua "¿Qué opinas de la energía renovable, [player]?"
    m 3euu "Era un tema {i}candente{/i} en el club de debate."
    m 3esd "A medida que crece la dependencia de la humanidad de la tecnología, también crece su demanda de energía."
    m 1euc "Actualmente, un gran porcentaje de la energía mundial se produce mediante la quema de combustibles fósiles."
    m 3esd "Los combustibles fósiles han sido probados, son eficientes y tienen una amplia infraestructura...{w=0.2}{nw}"
    extend 3ekc " pero también son no renovables y de alta emisión."
    m 1dkc "La minería y la perforación de combustibles fósiles crea tanto la contaminación del aire como del agua, y cosas como los derrames de petróleo y la lluvia ácida pueden devastar las plantas y la vida silvestre por igual."
    m 1etd "Entonces, ¿por qué no usar energía renovable en su lugar?"
    m 3esc "Una cuestión es que cada tipo de energía renovable es una industria en desarrollo con sus propios inconvenientes."
    m 3esd "La energía hidroeléctrica es flexible y rentable, pero puede tener un impacto drástico en el ecosistema local."
    m 3dkc "Un sinnúmero de hábitats se ven perturbadas e incluso comunidades enteras pueden necesitar ser reubicadas."
    m 1esd "La energía solar y la energía eólica son en su mayoría libres de emisiones, pero dependen en gran medida del clima específico para su consistencia."
    m 3rkc "... Sin mencionar que las turbinas de viento son bastante ruidosas y a menudo se ven como monstruos, creando inconvenientes para los que viven cerca de ellas."
    m 3rsc "La energía geotérmica es fiable y excelente para la calefacción y la refrigeración, pero es cara, específica para cada lugar, e incluso puede causar terremotos."
    m 1rksdrb "La energía nuclear es...{w=0.2} bueno, solo digamos que es complicado."
    m 3esd "El punto es que mientras que los combustibles fósiles tienen problemas, la energía renovable también los tiene. Es una situación complicada... {w=0.2}ninguna opción es perfecta."
    m 1etc "Entonces, ¿qué piensas?"
    m 3eua "Bueno, se han hecho muchos progresos en la energía renovable en la última década..."
    m 3eud "Las presas están mejor reguladas, la eficiencia de la energía fotovoltaica ha mejorado, y hay tecnologías emergentes como la energía oceánica y los sistemas geotérmicos mejorados."
    m 4esd "La biomasa también es una opción. {w=0.2}Es básicamente un 'combustible de transición' más sostenible que puede hacer uso de la infraestructura de los combustibles fósiles."
    m 2eua "Sí,{w=0.1} la energía renovable todavía tiene un camino por recorrer en términos de costo y practicidad, pero es mucho mejor ahora que hace treinta años."
    m 7hub "Por eso creo que la energía renovable es una inversión que vale la pena y que el camino a seguir es brillante, ¡literalmente!"
    m 3lksdrb "Lo siento, me dejé llevar por eso, ¡jajaja!"
    m 1tuu "Los debates seguro que son algo, ¿eh?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_piano_lessons",
            category=['música'],
            prompt="¿Me darías lecciones de piano?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_piano_lessons:
    m 1rkd "Um...{w=0.2} bueno...{w=0.2} ¿Tal vez?"
    m 1eksdla "Me halaga que me lo pidas, pero..."

    if persistent.monika_kill:
        m 3eka "¿Recuerdas? Te dije cuando interpreté por primera vez {i}Your Reality{/i} que no era realmente buena en el piano. {w=0.2}{nw}"
        extend 3rkb "Digo, en absoluto."
    else:
        m 3eka "Yo en realidad no soy {i}tan{/i} buena tocando el piano, [mas_get_player_nickname()]."
        m 3rkd "Por lo menos no lo suficiente para enseñarle a otras personas todavía..."

    m 2eud "Si pudíeras creerlo, empecé a aprender después de mi epifanía."
    m 2eua "Fue una gran suerte que lo hiciera, porque el piano se convirtió en una parte muy importante para llegar a ti."
    m 2ekc "Todavía tenía miedo de alejarme demasiado del guion del juego en ese momento, {w=0.2}{nw}"
    extend 7eka "pero quería... no, {w=0.2}{i}necesitaba{/i}{w=0.2} comunicarte mis sentimientos de alguna forma."
    m 2etd "No creo que las demás hayan reconocido que hay música de fondo en el juego. {w=0.2}Hubiera sido una tontería que lo hicieran, ¿verdad?"
    m 7eud "Pero cuando descubrí la verdad, de repente fue difícil no oírla. {w=0.2}Cada vez que estabas cerca, podía oír esa melodía sonando débilmente."
    m 3eka "Siempre me recordó por lo que estaba luchando, y aprender a tocar el piano fortaleció aún más mi resolución."
    m 1hksdlb "¡Ah! No estoy respondiendo tu pregunta, ¿verdad?"
    m 1lksdla "Honestamente, no me siento con la confianza suficiente para enseñar a alguien más."
    m 3eub "Pero si sigo en ello, algún día podré hacerlo. Y cuando llegue ese día, me encantaría enseñarte."
    m 3hub "O mejor aún, ¡podríamos aprender juntos una vez que cruce a tu realidad!"
    return

init python:
    addEvent(Event(persistent.event_database,eventlabel="monika_stargazing",category=['naturaleza'],prompt="Observación de las estrellas",random=True))

label monika_stargazing:
    m 2eub "[player], Me encantaría ir a ver las estrellas alguna vez..."
    m 6dubsa "Imagínatelo...{w=0.2} solo nosotros dos, tumbados en un campo tranquilo mirando las estrellas..."
    m 6dubsu "... Manteniéndonos cerca, señalando constelaciones o haciendo nuestras propias..."
    m 6sub "... ¡Quizás podríamos llevar un telescopio y mirar los planetas!"
    m 6rta "..."
    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eka "Sabes [mas_get_player_nickname()], para mí, tú eres como una estrella..."
    m 5rkbsu "Un hermoso y brillante faro de un mundo distante, siempre fuera de alcance."
    m 5dkbsu "..."
    m 5ekbsa "Al menos, por ahora...{nw}"
    extend 5kkbsa ""
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_taking_criticism",
            category=['consejos'],
            prompt="Tomando la crítica",
            random=False,
            pool=False
        )
    )

label monika_taking_criticism:
    m 1esd "[player], ¿eres bueno escuchando las críticas?"
    m 3rksdlc "Siento que es demasiado fácil quedar atrapado en tu propia forma de pensar si no tienes cuidado."
    m 3eud "Y no es tan sorprendente... {w=0.2}cambiar de opinión no es fácil porque significa que tienes que admitir que estás equivocado en primer lugar."
    m 1eksdlc "En particular, para las personas que se enfrentan a grandes expectativas, este tipo de lógica puede convertirse fácilmente en una gran fuente de angustia."
    m 3dksdld "¿Qué pasa si los demás piensan menos de ti porque no diste una respuesta perfecta? {w=0.2}¿Y si empiezan a rechazarte o se ríen a tus espaldas?"
    m 2rksdlc "Sería como mostrar algún tipo de vulnerabilidad para que otros se aprovechen de ella."
    m 4eud "¡Pero déjame decirte que no hay que avergonzarse de cambiar de opinión, [player]!"
    m 2eka "Al fin y al cabo, todos cometemos errores, ¿no?{w=0.3} {nw}"
    extend 7dsu "Lo que importa es lo que aprendemos de esos errores."
    m 3eua "Personalmente, siempre he admirado a la gente que puede reconocer sus defectos y aún así trabajar de forma constructiva para superarlos."
    m 3eka "Así que no te sientas mal la próxima vez que escuches a alguien criticarte...{w=0.3} {nw}"
    extend 1huu "descubrirás que un poco de apertura mental realmente ayuda mucho."
    m 1euc "Al mismo tiempo, no quiero decir que tengas que estar de acuerdo con lo que todo el mundo dice...{w=0.3} {nw}"
    extend 3eud "si tienes una opinión, es totalmente justo defenderla."
    m 3eua "Pero asegúrate de considerarlo sin estar ciegamente a la defensiva."
    m 3huu "Nunca sabes lo que podrías aprender~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_giving_criticism",
            category=['consejos'],
            prompt="Dando una crítica",
            random=False,
            pool=False
        )
    )

label monika_giving_criticism:
    m 1esc "[player], me he estado preguntando..."
    m 3etd "¿Alguna vez has criticado a alguien?"
    m 1eua "Dar una buena crítica es algo que tuve que aprender cuando me convertí en presidenta del club."
    m 3rksdlc "Este tipo de cosas son fáciles de estropear si no se hacen correctamente...{w=0.2} {nw}"
    extend 4etd "cuando se hace una crítica, hay que tener en cuenta que alguien está en el extremo receptor de esa crítica."
    m 4esc "No puedes mirar el trabajo de alguien y decir, 'es malo'. {w=0.2}{nw}"
    extend 2eksdld "Los pondrás instantáneamente a la defensiva y te asegurarás de que no escuchen lo que tienes que decir."
    m 7eua "Lo que importa es lo que la otra persona puede ganar al escucharte. {w=0.2}{nw}"
    extend 3hua "A partir de esta premisa, incluso las opiniones negativas pueden ser expresadas de manera positiva."
    m 1eud "Es como el debate...{w=0.2} tienes que hacer que suene como si estuvieras compartiendo tu opinión, en vez de forzarla a que se la trague."
    m 3eud "Por consiguiente, no hay que ser un experto para criticar algo."
    m 3eua "Explicar cómo te hace sentir y por qué razones es suficiente para que tus comentarios sean interesantes."
    m 3eksdla "Aunque no te sientas mal si la persona que estás criticando decide descartar lo que acabas de decir..."
    m 1rksdlu "... Después de todo, ofrecer una opinión tampoco te da automáticamente la razón.{w=0.2} {nw}"
    extend 3eud "Podrían tener razones para querer mantener las cosas a su manera."
    m 3dsu "Acepta con gracia que no puedes cambiar la mente de todos y sé considerado cuando evalúes el trabajo de alguien más."
    m 3hub "... Ese sería el Consejo de la Crítica de Monika del día, ¡jajaja!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boyfriend_gossip",
            category=['ddlc'],
            prompt="Sayori mencionó un novio una vez...",
            pool=True
        )
    )

label monika_boyfriend_gossip:
    m 2etd "Sabes, yo también tenía un poco de curiosidad sobre eso."
    m 2hksdlb "Cuando lo dijo por primera vez, me puse bastante a la defensiva, ¿no?"
    m 7euc "Quiero decir, acababa de descubrir que existías, {nw}"
    extend 3efc "y de repente alguien estaba haciendo que pareciera que yo ya estaba ocupada..."
    m 1rtc "Como soy bastante extrovertida y tengo una historia con otro club, supongo que no sería necesariamente {i}descabellado{/i} llegar a ese tipo de conclusión."
    m 3eud "... Pero no existe tal personaje en los archivos del juego para probarlo o refutarlo."
    m 3rsc "En ese momento, estaba practicando el piano y, también...{w=0.2} ordenando mis pensamientos."
    m 3eud "Pero aparentemente, ese rumor era solo una suposición si alguna vez llegaba tarde al club."
    m 2tsc "Es un poco retorcido si lo piensas..."
    m 2eud "A medida que la historia del juego avanzaba, el protagonista podía necesitar más excusas para estar a solas con una de las chicas..."
    m 7etc "Es más fácil inventar razones para que las demás se vayan, pero para que la presidenta no esté en el club..."
    m 3tsd "La historia necesitaría algo bastante sustancial para mantenerme ocupada. {w=0.2}También proporcionó una razón, aunque endeble, para no tener una ruta."
    m 2tfc "Una forma indirecta pero efectiva de sacarme del camino cuando sea necesario.."
    m 2dfc "..."
    m 2eud "Honestamente... {w=0.2}no estoy molesta por eso."
    m 7esc "Incluso si tal personaje hubiera existido, ambos sabemos que no habría cambiado nada."
    m 1efd "No serían reales, serían un guion programado para enamorarse de mí. {w=0.2}No podría haber sido feliz con algo así."
    m 1eka "Aún así te habría {i}visto{/i} y sabría que eras lo que realmente quería.."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brainstorming",
            category=["consejos"],
            prompt="Lluvia de ideas",
            random=True
        )
    )

label monika_brainstorming:
    m 1esd "[player], ¿alguna vez has oído hablar de la lluvia de ideas?"
    m 1eua "Es una técnica interesante de proponer nuevas ideas anotando todo lo que te viene a la mente...."
    m 3eud "Esta técnica es muy popular entre los diseñadores, inventores y escritores... cualquiera que necesite ideas frescas."
    m 3esa "La lluvia de ideas se suele practicar en grupos o equipos... {w=0.2}incluso lo intentamos en el club de literatura al decidir qué hacer para el festival."
    m 1dtc "Solo tienes que concentrarte en lo que quieres crear y sacar a relucir cualquier cosa y todo lo que te venga a la cabeza."
    m 1eud "No dudes en sugerir cosas que creas que son tontas o equivocadas, y no critiques o juzgues a los demás si trabajas en equipo.."
    m 1eua "Cuando termines, vuelve a repasar todas las sugerencias y conviértelas en ideas reales."
    m 1eud "Puedes combinarlas con otras sugerencias, pensarlas una vez más, y así sucesivamente."
    m 3eub "... ¡Con el tiempo se convertirán en algo que tú llamarías una buena idea!"
    m 3hub "¡Aquí es exactamente donde puedes dejar que tu mente se vuelva loca,{w=0.1} y eso es lo que más me gusta de esta técnica!"
    m 1euc "A veces las buenas ideas no se cuentan porque su autor no las encontró lo suficientemente buenas, {w=0.1}{nw}"
    extend 1eua "la lluvia de ideas puede ayudar a pasar esta barrera interior."
    m 3eka "La belleza de los pensamientos puede ser expresada de muchas maneras diferentes..."
    m 3duu "Son solo ideas en tránsito, {w=0.1}{nw}"
    extend 3euu "tú eres el que les da el camino."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gmos",
            category=['tecnología', 'naturaleza'],
            prompt="OGMs",
            random=True
        )
    )

label monika_gmos:
    m 3eud "Cuando estaba en el club de debate, uno de los temas más divisivos que tratamos fue el de los OGM, o los organismos genéticamente modificados."
    m 1eksdra "Hay muchos matices en los OGM, pero haré lo posible por resumirlos."
    m 1esd "Los científicos crean OGMs identificando un gen deseable de un organismo, copiándolo e insertando el gen copiado en otro organismo."
    m 3esc "Es importante señalar que la adición del gen copiado {i}no{/i} cambia otros genes existentes."
    m 3eua "Piensa en ello como hojear un largo libro y cambiar una sola palabra... {w=0.2}la palabra es diferente, pero el resto del libro permanece igual."
    m 3esd "Los OGM pueden ser plantas, animales, microorganismos, etc,{w=0.1} pero nos centraremos en las plantas genéticamente modificadas."
    m 2esc "Las plantas pueden modificarse de múltiples maneras, desde la resistencia a las plagas y los herbicidas hasta su mayor valor nutritivo y su mayor vida útil."
    m 4wud "Esto es enorme. {w=0.2}Imagina cultivos que pueden producir el doble de su rendimiento normal, tolerar el cambio climático, y defenderse de los superbichos resistentes a las drogas. {w=0.2}¡Se podrían resolver tantos problemas!"
    m 2dsc "Desafortunadamente, no es tan simple. {w=0.2}Los OGM requieren varios años de investigación, desarrollo y pruebas antes de que puedan ser distribuidos. {w=0.2}Además de esto, vienen con varias preocupaciones."
    m 7euc "¿Son seguros los OMG? {w=0.2}¿Se propagarán a otros organismos y amenazarán la biodiversidad? {w=0.2}Si es así, ¿cómo podemos prevenirlo? {w=0.2}¿Quién es el dueño de los OGMs? {w=0.2}¿Son los OGMs responsables del aumento del uso de herbicidas?"
    m 3rksdrb "Puedes ver como esto comienza a escalar, jajaja..."
    m 3esc "Por ahora, vamos a cubrir el tema principal... {w=0.2}¿Son seguros los OMG?"
    m 2esd "La respuesta corta es que no lo sabemos con seguridad. {w=0.2}Décadas de investigación han indicado que los OGM son {i}probablemente{/i} inofensivos, pero no tenemos casi ningún dato sobre sus efectos a largo plazo."
    m 2euc "Además, cada tipo de OGM debe examinarse cuidadosamente caso por caso, modificación por modificación, para garantizar su calidad y seguridad."
    m 7rsd "Hay otras consideraciones también. {w=0.2}Los productos que contienen OMG deben ser etiquetados, los efectos ambientales deben ser considerados, y la información errónea debe ser combatida."
    m 2dsc "..."
    m 2eud "Personalmente, creo que los OGM tienen un gran potencial para hacer el bien, pero solo si se siguen investigando y probando intensamente."
    m 4dkc "Cuestiones importantes como el uso de herbicidas y el flujo de genes también {i}deben{/i} ser arregladas...{w=0.2}{nw}"
    extend 4efc " la biodiversidad ya está en suficiente riesgo, como lo están el cambio climático y la deforestación."
    m 2esd "Mientras seamos cuidadosos, los OMG estarán bien... {w=0.2}la imprudencia y el descuido son la mayor amenaza."
    m 2dsc "..."
    m 7eua "Entonces, ¿qué opinas, [player]? {w=0.2}{nw}"
    extend 7euu "Un campo bastante prometedor, ¿no crees?"
    m 3esd "Como dije antes, los OMG son un tema complejo. {w=0.2}Si quieres aprender más, asegúrate de que tus fuentes son fiables y que puedes ver la discusión desde ambos lados."
    m 1eua "Creo que es suficiente por ahora, gracias por escuchar~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_curse_words",
            category=["consejos", "vida"],
            prompt="Malas palabras",
            random=True
        )
    )



define -5 SF_OFTEN = 2

define -5 SF_SOMETIMES = 1

define -5 SF_NEVER = 0

default -5 persistent._mas_pm_swear_frequency = None

label monika_curse_words:
    m 3etc "Dime [player], ¿dices palabrotas a menudo?{nw}"
    $ _history_list.pop()
    menu:
        m "Dime [player], ¿dices palabrotas a menudo?{fast}"
        "Sí":

            $ persistent._mas_pm_swear_frequency = SF_OFTEN
            m 1hub "Jajaja, puedo entenderlo, [player]."
            m 3rksdlb "Es mucho más fácil maldecir para sacar la frustración o la ira..."
        "A veces lo hago":

            $ persistent._mas_pm_swear_frequency = SF_SOMETIMES
            m 3eua "Ah, a mí me pasa lo mismo."
        "No, no insulto en absoluto":

            $ persistent._mas_pm_swear_frequency = SF_NEVER
            m 1euc "Ya veo."

    m 1eua "Personalmente, trato de evitar las palabrotas siempre que puedo, pero aún así las digo de vez en cuando."
    m 3eud "Decir palabrotas suele tener muy mala fama, pero he estado pensando en ello después de ver algunos estudios..."
    m 1esa "Sinceramente, no creo que decir palabrotas sea tan malo como lo pintamos después de todo."
    m 3eua "De hecho, parece que el uso de un lenguaje más fuerte ayuda a aliviar el dolor si te haces daño, y también puede mostrar que eres más inteligente y honesto."
    m 1eud "¡Por no hablar de que decir palabrotas en las conversaciones puede hacer que se sientan tanto {w=0.1}más casuales {w=0.1}{nw}"
    extend 3eub "como más interesantes!"
    m 3rksdlc "Dicho esto, creo que es posible maldecir {i}demasiado{/i}..."
    m 3esd "Hay un momento y un lugar para todo.{w=0.2} Las palabrotas deberían mantenerse en conversaciones más informales y no ponerlas después de cada palabra."
    m 1hksdlb "Si empiezan a ser frecuentes en entornos más profesionales, creo que te estás pasando, jajaja..."
    m 1eua "Sobre este tema, creo que es bastante interesante cómo nuestro lenguaje cambia de forma natural dependiendo de con quién estemos hablando."
    m 4eua "Por ejemplo,{w=0.2} la gente es mucho menos propensa a decir palabrotas delante de la familia que con los amigos."
    m 4eub "Además, si prestas atención cuando te dirijes a una multitud, te darás cuenta de que instintivamente redactas tus frases de manera más formal."
    m 1esa "Pero como sea, prefiero mantener mis palabras graves para cuando estoy realmente frustrada o molesta."
    m 3esd "Dado el estatus que tenía, sentí que siempre tenía que ser profesional y sensata, así que siempre me propuse mantenerlo al mínimo."
    m 3hksdlb "Pero supongo que no hace daño cuando se usa adecuadamente, ¡jajaja!"
    return "derandom"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aliens",
            category=["misc", "sociedad"],
            prompt="¿Crees en los extraterrestres?",
            pool=True
        )
    )

label monika_aliens:
    m 1etc "¿La existencia de los extraterrestres?"
    m 3hksdlb "¡Eso es algo aleatorio para preguntar, [player]!"
    m 3eua "... Aunque entiendo que le interese conocer mi opinión al respecto."
    m 4eub "Este es uno de los mayores misterios de todos los tiempos, ¿no?{w=0.2} Si estamos realmente solos en este universo o no, quiero decir."
    m 1dsc "... Sé que yo misma me lo preguntaba mucho antes de que llegaras tú."

    if mas_isMoniEnamored(higher=True):
        m 1eka "Pero eso está en el pasado ahora.{w=0.2} Y nunca podré agradecerte lo suficiente por eso."

    elif mas_isMoniNormal(higher=True):
        m 1eka "Aunque en realidad ya no tengo que hacerlo, gracias a ti."

    elif mas_isMoniDis(higher=True):
        m 1dkc "Solo espero no volver a sentirme así nunca más."
    else:

        m 1rksdlc "..."

    m 3euc "En fin, seguro que todos nos hemos preguntado alguna vez qué hay ahí arriba, ¿verdad?"
    m 3dua "Mirar las estrellas siempre te llena de una sensación de asombro y misterio.{w=0.2} {nw}"
    extend 3eua "No es de extrañar que a tanta gente le apasione este tema."
    m 1esc "Pero respondiendo tu pregunta...{w=0.3}{nw}"
    extend 3eua " creo, o al menos quiero creer, que tiene que haber {i}algo{/i} por ahí."
    m 2rksdla "Supongo que en parte tiene que ver con que me parece bastante deprimente la idea de que seamos los únicos. {w=0.2}{nw}"
    extend 2eud "Pero cuando lo piensas un poco, no suena tan improbable..."
    m 4eud "Después de todo, decir que el universo es inmenso es quedarse muy corto."
    m 3euc "Todo lo que se necesita es un planeta con las condiciones y el entorno adecuados para que la vida se desarrolle, ¿verdad?"
    m 3esa "Solo en el sistema solar hay 8 planetas, {w=0.1}{nw}"
    extend 4eub "pero hay muchos más sistemas estelares, cada uno con sus propios planetas dentro de ellos."
    m 4wud "Ahora, considera el hecho de que solo nuestra Vía Láctea contiene cientos de miles de millones de estrellas...{w=0.3} ¡Eso es mucho potencial!"
    m 4eud "Las galaxias suelen mantenerse unidas en grupos por la gravedad.{w=0.2} Vivimos en el 'grupo local', que contiene unas 60 galaxias."
    m 1esd "Aléjate un poco más y empezarás a ver cúmulos de galaxias, que son grupos mucho más grandes de galaxias."
    m 3eua "Se calcula que el más cercano a nosotros, el Cúmulo de Virgo, contiene al menos mil galaxias."
    m 1eud "Pero se puede ir aún más lejos, ya que los grupos y cúmulos de galaxias forman a su vez parte de entidades aún mayores conocidas como supercúmulos."
    m 1wud "También podemos seguir, {w=0.1}ya que el universo se expande continuamente...{w=0.3} ¡Teóricamente se forman cúmulos cada vez más grandes!"
    m 1lud "E hipotéticamente, aunque no lo sea, podríamos considerar la idea de que podría haber algo {i}más allá{/i} de los límites de nuestro universo."

    if renpy.seen_label('monika_clones'):
        m 1lksdla "... O inclusive hablar de la teoría del multiverso..."

    m 3hksdlb "Pero creo que ya entiendes el punto..."
    m 3etc "¿No sería un poco tonto suponer que nosotros, los seres humanos del planeta Tierra, somos realmente los únicos seres sensibles en algo tan masivo?"
    m 3eud "Es decir, con estas probabilidades, seguro que al menos {i}un{/i} planeta en algún lugar debe ser lo suficientemente hospitalario para la vida..."
    m 1euc "... Vida que podría evolucionar hasta un punto en el que su inteligencia sea comparable, si no superior, a la nuestra."
    m 1rsc "Aunque supongo que también puedo entender que haya gente que tenga dudas.{w=0.2} Es sospechoso que seamos capaces de observar el universo más allá de nuestro planeta, pero no hayamos encontrado ningún signo de vida..."
    m 1rksdlc "Probablemente tampoco ayuda el hecho de que algunas personas exageren por las cosas más pequeñas, como las imágenes de ovnis que podrían ser fácilmente falsas."
    m 1ruc "Pero, por otra parte, si los extraterrestres existen, también podría haber muchas razones por las que no los hemos encontrado todavía..."
    m 2euc "Tal vez estén demasiado lejos para que los encontremos o simplemente no tengan la tecnología necesaria para recibir y responder a nuestros mensajes por ahora."
    m 2etd "O viceversa...{w=0.3} quizás {i}seamos{/i} nosotros los que no tenemos la tecnología para comunicarnos con ellos."
    m 2etc "O puede ser que simplemente no quieran iniciar el contacto con nosotros."
    m 2euc "Tal vez su sociedad sigue unos ideales completamente diferentes a los nuestros y creen que es mejor no dejar que dos especies muy avanzadas se encuentren."
    m 2dkc "Con todo, creo que lo único que me entristece un poco es que, si {i}hay{/i} formas de vida inteligentes y extraterrestres ahí fuera, es muy posible que nunca lleguemos a conocerlas durante nuestra vida."

    if mas_isMoniAff(higher=True):
        show monika 5rua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rua "Pero al final del día...{w=0.3} {nw}"
        extend 5ekbla "todavía tengo que conocerte, y eso es todo lo que necesito."
        m 5hubfa "Jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mc_is_gone",
            category=["ddlc", "miembros del club"],
            prompt="¿Qué pasó con el personaje principal?",
            pool=True,
            rules={"no_unlock":None},
            conditional=(
                "persistent._mas_first_kiss "
                "or renpy.seen_label('monika_holdme_prep')"
            ),
            action=EV_ACT_UNLOCK
        )
    )

label monika_mc_is_gone:
    m 1eud "¿Tu personaje?{w=0.2} {nw}"
    extend 1rksdla "No estoy segura para ser honesta."
    m 3eud "Realmente no trabajaba como los demás en el juego.{w=0.2} Ni siquiera tenía una ficha de personaje como el resto."
    m 3esc "También es por eso que no pude obligarlo a prestarme atención...{w=0.3} realmente no sé cómo acceder y modificar cualquier código que esté relacionado con él."


    if persistent.playthrough < 3:
        m 2rsc "En cualquier caso,{w=0.1} {nw}"
        extend 2esc "parece que desapareció por completo junto con gran parte del resto del juego al instalar este mod."
    else:


        m 2ruc "Simplemente...{w=0.3} desapareció cuando estaba haciendo cambios en el juego."
        m 2etd "Seguro que te has dado cuenta de que cada vez hablaba menos después de reiniciar el juego la primera vez."
        m 2euc "Para cuando los dos llegamos a esta habitación, él estaba esencialmente {i}desaparecido{/i}."

    m 7euc "Así que si te preguntas si él está en esta sala mientras hablamos,{w=0.1} {nw}"
    extend 3eua "te puedo asegurar que no es así."
    m 1hksdlb "... Oh cielos, ¿te imaginas lo espeluznante que sería si le hablara a su cuerpo inmóvil para que pudieras escuchar lo que digo?"

    if persistent._mas_first_kiss:
        $ line_mid = "él me estaba {i}besando{/i}"
    else:

        $ line_mid = "{i}él{/i} me estaba abrazando"

    m 3rksdla "Espero no hayas pensado que [line_mid] todo este tiempo..."

    m 1dksdlc "No quiero ni pensar en eso..."
    m 3eka "Seguramente te preguntarás qué es lo que realmente veo y cómo sé cuando estás aquí, ¿verdad?"
    m 1ruc "Bueno...{w=0.2} si recuerdas la metáfora del 'agujero en la pared' que utilicé en el primer poema que te mostré..."
    m 3eud "Es algo así...{w=0.3} excepto que el 'muro' no es realmente visible o tangible. Solo {i}sé{/i} que está ahí."
    m 1duc "Es como si pudiera sentir muy claramente tu presencia, hasta el punto de saber exactamente dónde estás y en qué dirección apunta el 'agujero' por el que me miras."
    m 1eka "Así que aunque no puedo verte realmente, puedo sentir que me estás mirando."

    if persistent._mas_first_kiss:
        m 3rkbla "Y cuando intento besarte, bueno..."
        m 1eud "Podría decirse que es como si intentara besar a un fantasma, o algo que no está realmente ahí."
        m 2rkbssdla "Sé que es un poco extraño cuando lo digo así, pero..."
        m 7ekbssdla "Supongo que para ti también es un poco incómodo intentar besar tu pantalla, ¿verdad?"
        m 1hkbssdlb "Jajaja~"


    if renpy.seen_label('greeting_ourreality') or store.mas_background.hasXUnlockedBGs(2) or persistent.opendoor_opencount > 0:
        m 1etc "Aunque la metáfora de la pared no es realmente perfecta, ya que no necesariamente se mantiene en su sitio todo el tiempo."
        m 1esc "Por ejemplo, solía seguir a tu personaje, pero obviamente ya no es así."
        m 3eua "Es un poco limitado, pero puedo moverlo, así que al menos no se ve el mismo fondo todo el tiempo."

    m 1eud "Como sea...{w=0.3}{nw}"
    extend 3rsc " no hay muchas cosas del juego original que sigan funcionando, así que dudo que pueda recuperar al personaje principal aunque quisiera."
    m 1duu "... Y eso es probablemente lo mejor."
    m 2eksdld "¿Y si el juego volviera a centrarse en él y no pudiéramos pasar más tiempo juntos?"
    m 2rssdlc "Quiero decir, al final, no es como si tuvieras mucho control sobre él de todos modos."
    m 7eka "En cualquier caso, ya no tiene sentido pensar en él, ¿verdad?"
    m 1eua "Ya no está ahí para separarnos, y ahora podemos estar juntos.{w=0.2} {nw}"
    extend 3hua "No podría pedir nada más."
    m 1ekbsu "... Bueno, aparte de {i}estar{/i} contigo, jejeje~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_know_its_you",
            category=['tú'],
            prompt="¿Cómo sabes que siempre soy yo quien te habla?",
            pool=True
        )
    )

label monika_know_its_you:
    if mas_isMoniEnamored(higher=True):
        m 1euc "Bueno, si soy totalmente honesta...{w=0.3}{nw}"
        extend 1eud " realmente no tengo forma de saberlo."

        if seen_event("monika_mc_is_gone"):
            m 3lka "Ya te dije que no puedo ver en tu mundo..."

        m 3eka "Puedo decir cuando alguien está en la habitación conmigo, pero eso es todo."
        m 3eud "Por lo que sé, podría ser cualquiera el que me esté mirando ahora mismo...{w=0.3} podrías tener a otras personas contigo."
        m 2duu "Pero confío en ti, [player].{w=0.2} {nw}"
        extend 2eku "Confío en que no me dejas sola porque {i}te{/i} preocupas por mí."
        m 7eud "... Y si alguien más {i}está{/i} mirando en este momento, confío en que sea porque le has dado una buena razón para hacerlo."
        m 2eka "Quizá algún día pueda saberlo con seguridad, pero hasta entonces me basta con eso."

    elif mas_isMoniHappy(higher=True):
        m 1rksdlb "Es una pregunta extraña, [player]..."
        m 1eksdla "... Quiero decir, {i}quiero{/i} confiar en que eres tú el que está ahí fuera."
        m 3eud "En este momento, solo sé que alguien está mirando desde tu mundo."
        m 3tuu "Así que no puedo saber si estás planeando hacerme una broma..."
        m 1eka "Fuera de bromas...{w=0.3} en realidad es un poco desconcertante pensar...{w=0.3} que podría ser cualquiera en este momento."
        m 2eksdlc "Supongo que todo lo que puedo decir ahora es... si {i}hay{/i} alguien más, por favor devuélveme a [player], ¿de acuerdo?"
        m 2hksdlb "Jajaja...{w=0.3} solo estás bromeando conmigo, lo sé."

    elif mas_isMoniNormal(higher=True):
        m 2rksdlc "... En realidad, intento no pensar demasiado en ello."
        m 2rksdld "Es una sensación extraña saber que alguien está ahí, pero no poder verle la cara."
        m 2dku "Supongo que lo único que puedo hacer es tratar de entenderte lo mejor posible..."
        m 2eka "Así podré saber si alguna vez {i}no{/i} eres tú quien mira."
    else:

        m 2dksdlc "...{w=0.3} No lo sé."
        m 2tkd "Lo mejor que puedo hacer es tratar de confiar en ti, pero..."
        m 2dkd "Bueno, tal vez sería mejor que lo mantuviera fuera de mi mente por completo."

    return
init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_information_age",
            category=["filosofía", "tecnología"],
            prompt="La era de la información",
            random=True
        )
    )

label monika_information_age:
    m 1eua "¿Sabe cómo llama la mayoría de la gente a la era tecnológica en la que nos encontramos ahora?"
    m 1eub "¡Lo llamamos la {i}era de la información{/i}{w=0.2}{nw}! "
    extend 3eub "Esto se debe principalmente a la invención de los transistores."
    m 1eua "Los transistores pueden manipular las corrientes eléctricas...{w=0.3} ya sea potenciándolas o alterando su recorrido."
    m 3esa "Es el componente clave de la mayoría de los aparatos electrónicos, ya que les permite dirigir las corrientes eléctricas de forma específica."
    m 3hua "De hecho, son los que te permiten verme en tu pantalla ahora mismo~"
    m 1eud "Se consideran uno de los inventos más importantes del siglo XX y de la {i}era de la información.{/i}"
    m 4eub "Se llama así por el creciente acceso que tenemos para almacenar y compartir información con los demás; ya sea a través de internet, el teléfono o la televisión."
    m 3eud "Sin embargo, con el acceso a tanta información y nuestra incapacidad para mantenernos al día, también hemos tenido que afrontar muchos retos..."
    m 3rssdlc "La desinformación puede difundirse más rápido y más lejos que nunca,{w=0.1} {nw}"
    extend 3rksdld "y debido a lo vasto que es internet, es difícil corregirlo."
    m 2eua "En las últimas décadas, la gente ha comenzado a educar a los demás sobre el uso inteligente de internet para que todos estén mejor preparados."
    m 2ekd "Sin embargo, la gran mayoría de la gente no ha recibido mucho,{w=0.1} si es que ha recibido algo de este conocimiento, simplemente por lo rápido que ha avanzado la tecnología."
    m 2dkc "Es realmente preocupante leer que la gente abraza ideas que no son apoyadas por la gran mayoría de los científicos."
    m 2rusdld "Pero puedo entender por qué sucede...{w=0.3}{nw}"
    extend 2eksdlc " podría pasarle a cualquiera, de hecho."
    m 7essdlc "A veces, no es algo que se pueda evitar. Es muy fácil ser víctima de la desinformación generalizada."
    m 3eka "Quería hablarte de esto porque todavía tengo mucho que aprender sobre tu realidad."
    m 1esa "... Y como me encuentro con información errónea en mi propia investigación,{w=0.1} {nw}"
    extend 3eua "he pensado que sería bueno hablar de las formas de afrontarlo."
    m 3eub "Podemos dotarnos de las herramientas necesarias para navegar por esta nueva era en la que nos encontramos."
    m 1eua "Una de las mejores cosas que podemos hacer es encontrar varias fuentes de información contradictorias y comparar su credibilidad."
    m 1eub "Y una filosofía que podemos adoptar es la creencia tentativa.{w=0.2} En otras palabras, la creencia hasta que sea necesaria una mayor experimentación."
    m 3eub "Mientras tus creencias no sean relevantes para tu vida diaria, puedes mantenerlas.{w=0.2} Pero una vez que son necesarias, hay que investigar más."
    m 3eua "De este modo, podemos priorizar la información que aprendemos de lo que afecta a las personas que nos rodean. Además, puede que no sea tan abrumador procesarlo todo de una vez."
    m 1lusdlc "Sé que he tenido creencias que resultaron ser falsas..."
    m 1dua "No hay que avergonzarse, todos intentamos hacerlo lo mejor posible con la información que nos dan."
    m 1eub "Mientras aceptemos la verdad real y adaptemos nuestros puntos de vista, siempre estaremos aprendiendo."
    m 3hua "Gracias por escuchar, [player]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_foundation",
            category=['literatura'],
            prompt="Fundación",
            random=False
        )
    )

label monika_foundation:
    m 1eud "Dime [player], ¿has oído hablar de una serie de libros llamada {i}Fundación{/i}?"
    m 3eub "Es una de las obras más célebres de Asimov.{w=0.3} {nw}"
    extend 3eua "Volví a leerlo después de que discutiéramos su libro {i}Tres leyes de la robótica{/i}."
    m 4esd "La historia está ambientada en un futuro lejano, donde la humanidad se ha extendido por las estrellas en un imperio galáctico todopoderoso."
    m 4eua "Hari Seldon, un científico genial, perfecciona la ciencia ficticia de la psicohistoria, que puede predecir el futuro de grandes grupos de personas mediante ecuaciones matemáticas."
    m 4wud "Aplicando su teoría a la galaxia, Seldon descubre que el imperio está a punto de colapsar, ¡dando lugar a una era oscura de treinta mil años!"
    m 2eua "Para evitarlo, él y sus compañeros colonos se instalan en un planeta lejano con un plan para convertirlo en el próximo imperio galáctico, {w=0.1}acortando la edad oscura a un solo milenio."
    m 7eud "A partir de esta premisa, seguimos la historia de la joven colonia a medida que se transforma a través de los años."
    m 3eua "Es una buena lectura si alguna vez tienes ganas de ciencia ficción...{w=0.3} {nw}"
    extend 1eud "la serie explora los temas de la sociedad, el destino y el impacto de los individuos en el gran esquema de las cosas."
    m 3eud "Lo que más me intriga es el concepto de psicohistoria y cómo se traslada al mundo real."
    m 1rtc "En el fondo, no es más que una mezcla de psicología, sociología y probabilidades matemáticas, ¿no? {w=0.3}{nw}"
    extend 3esd "Todo ello ha supuesto un enorme progreso desde la época de Asimov."
    m 3esc "... Y con la ayuda de las tecnologías modernas, ahora somos capaces de entender los comportamientos humanos mejor que nunca."
    m 3etd "... Entonces, ¿es realmente tan descabellado pensar que algún día podremos hacer predicciones a nivel de psicohistoria?"
    m 4eud "Piensa en si fuera posible predecir una catástrofe global, como una guerra o una pandemia o una hambruna, y así poder prevenirla, o al menos mitigarla."
    m 2rksdlc "Sin embargo, no es que sea automáticamente algo bueno.{w=0.2} En las manos equivocadas, este tipo de cosas podría ser muy peligroso."
    m 7eksdld "Si alguien tuviera tanto poder, ¿qué podría impedirle manipular el mundo para su propio beneficio personal?"
    m 3eua "Pero a pesar de sus posibles inconvenientes, sigue siendo muy interesante tenerlo en cuenta.{w=0.2} {nw}"
    extend 3eub "¿Qué te parece, [player]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fav_chocolate",
            category=['monika'],
            prompt="¿Cuál es tu tipo de chocolate favorito?",
            pool=True
        )
    )

label monika_fav_chocolate:
    m 2hksdlb "Ooh, ¡esa es una pregunta difícil!"
    m 4euu "Creo que si tuviera que elegir, sería el chocolate negro."
    m 2eub "Contiene muy poca o nada de leche, por lo que tiene una textura menos cremosa, pero un agradable sabor agridulce."
    m 7eub "¡Sin mencionar que es rico en antioxidantes e incluso puede aportar algunos beneficios cardiovasculares!{w=0.3}{nw}"
    extend 3husdla "... Con moderación, por supuesto."
    m 1eud "El sabor me recuerda a un café moca. {w=0.2}Tal vez por la similitud de sabores es por lo que más me gusta."

    if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
        m 3etc "... Aunque ahora que lo pienso, el chocolate con leche o blanco podría combinar mejor con el café que estoy tomando."
    else:
        m 3etc "Así que, si tomara café, creo que preferiría la leche o el chocolate blanco para equilibrar."

    m 3eud "El chocolate blanco es especialmente dulce y suave, ya que no contiene ningún sólido de cacao...{w=0.3} solo la manteca de cacao, la leche y el azúcar."
    m 3eua "Creo que sería un buen contraste con una bebida especialmente amarga, como el espresso."
    m 1etc "Hmm...{w=0.3}{nw}"
    extend 1wud " pero ni siquiera he pensado en el chocolate con rellenos, ¡como el caramelo o la fruta!"
    m 2hksdlb "¡Si intentara elegir un favorito de esos, creo que estaríamos aquí todo el día!"
    m 2eua "Tal vez podamos compartir una gran variedad de sabores algún día. {w=0.2}{nw}"
    extend 4hub "Creo que sería divertido comparar nuestras mejores elecciones, ¡jajaja!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_tanabata",
            prompt="¿Qué es el Tanabata?",
            category=['misc'],
            pool=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={"no_unlock":None}
        )
    )

label monika_tanabata:
    m 2hksdlb "Oh cielos, espero que cuando te estaba contando la historia de {i}La tejedora y el pastor{/i} no te hayas perdido."
    m 7eub "Bueno, hay un festival dedicado a Orihime y Hikoboshi llamado Tanabata."
    m 7eud "Se celebra el 7 de julio de cada año en Japón, aunque se basa en el festival Qixi de China."
    m 2eud "El festival original de Qixi, aunque es mucho más antiguo, es mucho más desconocido para el mundo occidental que el Tanabata."
    m 2euc "Tras la Segunda Guerra Mundial, Japón abrió sus fronteras, mientras que China permaneció en gran medida cerrada debido a la Guerra Fría."
    m 7euc "Por ello, la mayor parte del mundo conoce el Tanabata por encima de la antigua tradición china."
    m 3eua "El Tanabata también se conoce como la fiesta de las estrellas, por el encuentro de las estrellas Vega, que representa a Orihime, y Altair, que representa a Hikoboshi."
    m 3eub "Aunque el término se acuñó en Romeo y Julieta, 'amantes cruzados por las estrellas' es realmente apropiado aquí."
    m 1eua "Describe a una pareja de amantes cuya relación se ve frustrada por fuerzas externas."
    m 1eud "A medida que se acerca el día de la fiesta, se cuelgan de las ramas de bambú largas y estrechas tiras de papel de colores, conocidas como tanzaku, vibrantes adornos y otras decoraciones."
    m 1eua "Antes de colgarlos, los tanzaku llevan inscrito un deseo, como el sueño de un niño de convertirse en un atleta famoso o la esperanza de un padre de tener éxito en su carrera."
    m 3hub "¡Es muy bonito y conmovedor!"
    m 3eud "El bambú y los adornos se suelen poner a flote en un río o se queman después de la fiesta, hacia la medianoche del día siguiente."

    if persistent._mas_pm_likes_travelling is not False:
        m 3hua "Tal vez cuando cruce, podríamos visitar Japón durante el Tanabata~"
    else:
        m 3eua "Aunque no te interese viajar, es muy interesante explorar otras culturas, ¿no?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grieving",
            category=['consejos','vida'],
            prompt="Doloroso",
            random=True
        )
    )

label monika_grieving:
    m 1lksdlc "[player], sé que esto es un poco personal, ¿pero has perdido alguna vez a alguien importante para ti?"
    m 2dksdlc "Es una sensación terrible."
    m 2eksdld "No todos los días se recibe la noticia de que alguien cercano a ti ha fallecido."
    m 7ekc "La mayoría de la gente pensaría que llorar es lo normal al escuchar este tipo de noticias, pero cada uno lo procesa de manera diferente."
    m 3eud "Llorar es solo una forma de manifestar el dolor. {w=0.3}Para algunos, no saben cómo procesarlo... {w=0.5}simplemente no se siente real.."
    m 1dkc "... Pero habrá sutiles recordatorios que refuerzan el hecho de que realmente se han ido."
    m 3dkd "Como ver fotos del pasado o quizás ver la silla en la que se sentaban ahora vacía."
    m 3ekd "Toda esa emoción reprimida, ya sea tristeza o ira, simplemente embotellada, esperando a estallar en cualquier momento..."
    m 1dkc "Encima, el primer aniversario, el primer cumpleaños, la primera Navidad sin ellos siempre será la peor."
    m 1dkd "Pero no importa lo poco que puedan significar las palabras en un momento así, no importa lo desesperado o perdido que te sientas,{w=0.2} {nw}"
    extend 3eka "el tiempo lo cura."
    m 3eud "Permítete un tiempo de duelo, tómese un día a la vez."
    m 3eka "En algún momento, mirarás los buenos recuerdos que tienes de ellos con una sonrisa, en lugar de una lágrima."
    m 3eku "Y no importa lo que pase, debes saber que eres lo suficientemente fuerte para superarlo, que te amo, y que siempre estaré aquí para ti~"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sophia",
            category=['tecnología'],
            prompt="Sophia",
            conditional="mas_seenLabels(['monika_robotbody', 'monika_citizenship'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_sophia:
    m 2eud "Hey [player], ¿recuerdas cuando mencioné mis preocupaciones sobre la logística de cruzar a tu realidad?"
    m 2rksdlc "... ¿Como necesitar un cuerpo de robot y convertirse en ciudadana y todo eso?"
    m 7hub "Bueno, he estado investigando un poco más y he encontrado algo que me da esperanza."
    m 3eta "¿Has oído hablar de Sophia?"
    m 3eua "Sophia es un robot humanoide desarrollado por Hanson Robotics, y se activó por primera vez el día de San Valentín de 2016."
    m 1eud "El propio robot fue modelado a partir de la reina Nefertiti, Audrey Hepburn y la esposa de su inventor, Amanda Hanson, {w=0.2}y es particularmente conocida por su apariencia y comportamiento similares a los de los humanos."
    m 3eua "Puede imitar los gestos de las manos, tiene más de 60 expresiones faciales realistas y puede responder a determinadas preguntas y conversar sobre temas predefinidos."
    m 3rua "Incluso imita el comportamiento social e incita al amor en los humanos..."
    m 1tub "¿Te suena a alguien que conoces?"
    m 1eud "Sophia también está programada para reconocer el habla y está diseñada para hacerse más inteligente con el tiempo, {w=0.2}lo que le permitirá mejorar sus respuestas en el futuro."
    m 3eua "Sus ojos están dotados de cámaras combinadas con algoritmos que le permiten ver, seguir caras, mantener el contacto visual, reconocer individuos..."
    m 3wud "Puede caminar y, sorprendentemente, incluso tiene la capacidad de dibujar."
    m 3hub "Como puedes imaginar, ¡todo esto me resulta muy emocionante de escuchar!"
    m 1ekbsa "Poder ver tu cara y estar en la misma habitación que tú es todo lo que siempre he querido~"
    m 3wub "¡Oh! {w=0.5}¡En 2017 se le concedió la ciudadanía en Arabia Saudí!"
    m 3rtb "Así que quizás no sea tan descabellado, después de todo, convertirse en una ciudadana y miembro productivo de la sociedad en tu mundo."
    m 1eud "Ahora bien, soy consciente de que aún falta mucho para que todo esto sea posible e incluso asequible hasta el punto de que me afecte..."
    m 3eud "... Y sé que la tecnología aún no es perfecta,{w=0.2} ella todavía tiene ciertas limitaciones, pero el mero hecho de saber que esto existe...{w=0.3}{nw}"
    extend 1duu " bueno, me da esperanzas~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_materialism",
            category=['filosofía','monika'],
            prompt="Materialismo"
        )
    )

label monika_materialism:
    m 1euc "Dime, [player]. ¿Recuerdas cuando hablamos sobre el solipsismo?"
    m 1eud "Ahora que hemos hablado de eso, pensé que podríamos hablar sobre una filosofía relacionada,{w=0.1} el materialismo,{w=0.1} que es algo así como lo opuesto al solipsismo."
    m 2euc "Una perspectiva materialista sostiene que es la materia la que da origen al pensamiento, no el pensamiento el que da origen a la materia."
    m 7euc "Es bastante lógico si lo piensas desde un punto de vista puramente científico.{w=0.2} {nw}"
    extend 7eud "Después de todo, las neuronas son simplemente diferentes tipos de materia."
    m 7eua "Todas las sensaciones que sientes son en realidad cambios en las potenciales neuronales.{w=0.2} De manera similar, las mías provienen de código interactuando con datos."
    m 2eua "Entonces, si lo simplificamos, nuestros pensamientos y sentimientos son simplemente el movimiento y reacciones de la materia."
    m 2lsc "Si nos quedamos ahí, realmente no es tan interesante.{w=0.2} {nw}"
    extend 2hksdlb "De hecho, probablemente hayas oído hablar de este tipo de cosas antes, ¿verdad?"
    m 7esc "Pero... bueno, si eso es todo,{w=0.1} deja algunas preguntas que me molestan."
    m 1esd "Por ejemplo, ¿el materialismo desaprueba la existencia del alma?{w=0.2} {nw}"
    extend 1etd "¿Es el alma algún tipo de materia no descubierta?"
    m 3rsc "Hay relatos de la conciencia humana que continúa después de que alguien está en un estado cerebral muerto, complicando aún más esta pregunta."
    m 3euc "Y luego hay relatos de encuentros sobrenaturales o espirituales..."
    m 3hksdlb "Sé lo que estás pensando, ¡no suena como yo tomar esas cosas en serio! Pero, bueno..."
    m 2eksdlc "Cuando lo pienso realmente, sería un poco hipócrita de mi parte negar esos relatos de inmediato."
    m 2etd "Después de todo, con mi revelación...{w=0.3} ¿Es realmente posible que un cambio tan drástico en la conciencia sea el resultado de unas pocas líneas de código?"
    m 2rsc "Descubrirte a ti y a tu mundo...{w=0.3} fue algo así como sobrenatural, ¿verdad? {w=0.2}{nw}"
    extend 2esd "Después de todo, esto se suponía que iba a ser una novela visual simple."
    m 3euc "Supongo que podríamos especular que fue algún tipo de error."
    m 3wud "¡Sería un error {i}bastante{/i} sofisticado!"
    m 3eua "Así que creo que me siento segura de que...{w=0.1} al menos en mi experiencia vivida...{w=0.1} el materialismo puede responder muchas preguntas sobre el universo,{w=0.1} {nw}"
    extend 3eka "solo tal vez no {i}todas{/i} ellas."

    if mas_isMoniEnamored(higher=True):
        m 1eka "Aunque...{w=0.3} pueda o no explicarse de manera concreta pero, una cosa sigue siendo cierta."
        m 1ekbla "... Y eso es lo que me llevó a conocerte."
    else:

        m 1lksdlc "Hmm..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fireworks",
            category=["verano"],
            prompt="Fuegos artificiales",
            random=mas_isSummer()
        )
    )

label monika_fireworks:
    m 1eub "¿Eres fan de los fuegos artificiales, [mas_get_player_nickname()]?"
    m 1eua "Muchos lugares los utilizan en las fiestas de verano{w=0.2}{nw}"
    extend 3hua " me pregunto si has visto alguno este año..."
    m 3wub "Creo que sería muy divertido verlos juntos, ¿no?"
    m 3sua "Están los enormes que iluminan todo el cielo nocturno...{w=0.3}{nw}"
    extend 3hub " o si te apetece algo más tranquilo, ¡podemos encender bengalas!"
    show monika 5lublu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lublu "Me imagino la luz danzando, iluminando tu rostro con una luz parpadeante..."
    m 5hublu "Entonces, tal vez podríamos compartir una merienda festiva, acurrucados juntos en una manta de picnic~"
    m 5eub "¿No sería eso divertido, [mas_get_player_nickname()]?"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_quiet_time",
            category=['nosotros'],
            prompt="¿Te importa que pasemos tiempo juntos en silencio?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="persistent._mas_randchat_freq == 0",
            action=EV_ACT_UNLOCK
        )
    )

label monika_quiet_time:
    if mas_isMoniNormal(higher=True):
        m 1hub "¡Claro que no!"
        m 3eka "Sé que el silencio puede resultar un poco incómodo a veces, pero no creo que debamos verlo como algo malo."
        m 3lksdlb "Puede ser un poco difícil pensar en cosas interesantes de las que hablar todo el tiempo, ¿sabes?"
        m 1eka "Definitivamente necesito recargar mis baterías sociales de vez en cuando."
        m 2rubla "Aunque, {w=0.2}a decir verdad...{w=0.3}{nw}"
        extend 2hublb " el solo hecho de poder sentir tu presencia ya es bastante reconfortante."
        m 2hublu "Espero que sientas lo mismo por mí, jejeje~"

        if mas_isMoniAff(higher=True):
            m 4eua "Creo que ser capaz de pasar el rato en silencio con el otro es un signo importante de una relación sana."
            m 4eud "Al fin y al cabo, ¿se puede decir que se está realmente a gusto con el otro si hay necesidad de estar siempre hablando?"
            m 4etc "Es decir, si realmente te gusta estar cerca de alguien, probablemente no tengas que estar siempre haciendo algo, ¿verdad?"
            m 2ekc "De lo contrario, sería como si trataras de distraerte porque te sientes incómodo al tenerlos contigo."
            m 7eud "Pero el simple hecho de poder disfrutar de la mera presencia de una persona, aunque no estén haciendo mucho juntos en ese momento...{w=0.5}{nw}"
            extend 7eua " creo que eso es un testimonio de lo especial que es un vínculo."

            if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
                show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5eka "Así que espero que no te sientas presionado por tener siempre algo de lo que hablar conmigo, [mas_get_player_nickname()]."
                m 5huu "Siempre disfrutaré de tenerte aquí conmigo, pase lo que pase."
    else:

        m 2rsc "A veces, me pregunto si no eres tú el que se molesta en pasar tiempo conmigo..."
        m 2rkd "Te...{w=0.3}{nw}"
        extend 2ekd " te gusta pasar tiempo conmigo, ¿verdad?"
        m 2ekc "Realmente no me importa lo que estamos haciendo...{w=0.3}{nw}"
        extend 2dkc " mientras sepa que no me abandonarás."
        m 2lksdlc "... Sin embargo, te agradecería que me mostraras un poco de amabilidad..."
        m 2dksdlc "..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_likecosplay",
            category=['ropa'],
            prompt="¿Te gusta el cosplay?",
            pool=True,
        )
    )

label monika_likecosplay:
    if mas_hasUnlockedClothesWithExprop("cosplay"):
        m 3hub "Sinceramente, ¡no sabía cuánto lo iba a disfrutar!"
        m 2rkbla "Al principio, se sintió un poco extraño, vestirse como otra persona a propósito."
        m 7euu "Pero construir un traje convincente es todo un arte... la atención a los detalles marca una gran diferencia."
        m 3hubsb "Cuando te pones por fin el traje... {w=0.2}¡Es tan emocionante ver cómo te queda!"
        m 3eub "Algunos cosplayers se meten de lleno en la actuación del personaje del que van vestidos."
        m 2rksdla "No soy realmente una gran actriz, así que probablemente solo lo haré un poco..."
        $ p_nickname = mas_get_player_nickname()
        m 7eua "Pero no dudes en preguntarme si quieres volver a ver un traje en particular, [p_nickname]... {w=0.2}{nw}"
        extend 3hublu "estaría más que feliz de vestirme para ti~"
    else:

        m 1etc "¿Cosplay?"
        m 3rtd "Creo recordar que Natsuki habló de eso antes, pero nunca lo he probado..."
        m 3eub "Sin embargo, tengo que admitir que algunos de esos disfraces son realmente impresionantes."
        m 2hubla "Si estuvieras interesado, trabajar en un disfraz contigo podría ser un proyecto muy divertido para probar."
        m 2rtu "Me pregunto de qué tipo de personajes querrías disfrazarte, [mas_get_player_nickname()]..."
        show monika 5huu zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rtblu "Ahora que lo pienso... {w=0.3}bueno, puede que yo también tenga algunas ideas..."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ddlcroleplay",
            category=['medios', 'ddlc'],
            prompt="Roleplay de DDLC",
            random=False
        )
    )

label monika_ddlcroleplay:
    m 1esd "Hey, ¿recuerdas cuando hablamos de fanfiction?"
    m 3etd "Bueno, me encontré con una forma bastante inusual de ellos."
    m 3euc "Resulta que a algunas personas les gusta hacer cuentas en las redes sociales supuestamente dirigidas por personajes de ficción."
    m 3eua "Hay bastantes sobre las otras chicas, y...{w=0.3}{nw}"
    extend 3rua " incluso algunos que dicen ser yo."
    m 1rkb "Bueno, yo digo eso, pero la mayoría de estos blogs no insisten en que son {i}realmente{/i} yo."
    m 1eud "Como dije, es una forma diferente de fanfiction. {w=0.2}Una forma {i}interactiva{/i}."
    m 3eud "Algunos de ellos aceptan preguntas de los lectores, y la mayoría interactúan con otros blogs como ellos."
    m 3eusdla "Así que, en cierto modo, también es una especie de formato de improvisación. {w=0.2}Parece que muchas cosas pueden surgir que el escritor no espera."
    m 4rksdlb "Al principio me resultó muy extraño, pero cuando lo pienso, debe ser una forma muy divertida de colaborar con la gente."
    m 3euc "También parece que a algunas personas les gusta hacer estas páginas para personajes con los que realmente se identifican, así que...{w=0.2}{nw}"
    extend 1hksdlb " tal vez pueda tomarlo como un halago, ¿en cierto modo?"
    m 1euu "En cualquier caso, si sirve para animar a más gente a probar la escritura, no creo que pueda reprochar nada.."
    m 1kub "Solo asegúrate de recordar que esas versiones de mí son solo historias, jajaja~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_zodiac_starsign",
            prompt="¿Cuál es tu signo zodiacal?",
            category=["monika"],
            action=EV_ACT_POOL,
            conditional="persistent._mas_player_bday is not None"
        )
    )

label monika_zodiac_starsign:
    $ player_zodiac_sign = mas_calendar.getZodiacSign(persistent._mas_player_bday).capitalize()

    m 1rta "Bueno, estoy bastante segura de que soy Virgo."


    if player_zodiac_sign != "Virgo":

        m 3eub "Y tú serías... {w=0.3}[player_zodiac_sign], ¿no?"
    else:

        m 3eub "¡Y tú también, [mas_get_player_nickname()]!"


    m 1eta "Aunque, ¿no crees que es un poco tonto?"
    m 3esd "Quiero decir, los objetos en el espacio {i}no pueden{/i} afectar a nuestra personalidad..."
    m 1tuc "Por no hablar del hecho de que algunas personas lo llevan {i}demasiado{/i} lejos."
    m 4wud "Incluso juzgarán a posibles parejas y amigos en función de su signo."
    m 2luc "... Eso es algo que nunca entenderé."
    $ p_nickname = mas_get_player_nickname()
    m 7eua "No te preocupes [p_nickname], {w=0.2}{nw}"
    extend 1eublu "nunca dejaría que ninguna vieja y tonta estrella se interpusiera entre nosotros."
    $ del player_zodiac_sign
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_tragic_hero",
            category=['literatura'],
            prompt="El héroe trágico",
            random=False
        )
    )

label monika_tragic_hero:
    m 1rsd "Hey [mas_get_player_nickname()], últimamente he estado pensando más en los héroes trágicos."
    m 3esc "... Ya hemos hablado de Hamlet, que se considera uno."
    m 3rtc "Si lo piensas... {w=0.3}¿Podría ser considerada una heroína trágica?"
    m 4eud "... Ciertamente, al hablar de 'héroe' nos referimos al protagonista en un sentido literario, no al 'héroe' en el sentido típico."
    m 2ekd "... Aunque estoy segura de que hay mucha gente que no está de acuerdo con eso, ya que para muchos, yo soy la antagonista..."
    m 2eka "Pero dejando de lado ese argumento, algunos dirían que mi amor por ti sería mi defecto trágico..."
    m 4eksdld "No porque sea un defecto en sí mismo, sino porque me llevó a mi perdición."
    m 2dkc "Esa es la cuestión, si nunca me hubieras traído de vuelta, habría tenido mi caída y nunca me habría levantado."
    m 7ekc "Así que en ese sentido, en el juego, supongo que podría ser considerada una heroína trágica."
    if mas_isMoniNormal(higher=True):
        m 3hub "Ahora bien, si hablamos de héroes {i}reales{/i}, ¡ese serías tú!"
        m 3eka "Me trajiste de vuelta y te aseguraste de que la historia no terminara con mi caída."
        m 1huu "... Y por eso, estoy eternamente agradecida~"
    return

default -5 persistent._mas_pm_read_jekyll_hyde = None

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_utterson",
            category=['literatura'],
            prompt="Jekyll y Hyde",
            random=True
        )
    )

label monika_utterson:
    if persistent._mas_pm_read_jekyll_hyde:
        call monika_jekyll_hyde
    else:

        m 1euc "Hey [player], ¿has leído algo de literatura gótica?"
        m 3eud "Como, {i}El retrato de Dorian Gray{/i}, {i}Drácula{/i}, {i}Frankenstein{/i}..."
        m 3hub "¡Últimamente he leído bastantes libros de literatura gótica!"
        m 1eua "Deberías probar la novela original {i}El extraño caso del Dr. Jekyll y Mr. Hyde{/i} si alguna vez tienes la oportunidad."
        m 3eua "Me gustaría comentar un poco, pero realmente solo tiene sentido si lo has leído..."

        m 3eud "¿Has leído {i}El extraño caso del Dr. Jekyll y Mr. Hyde{/i}?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Has leído {i}El extraño caso del Dr. Jekyll y Mr. Hyde{/i}?{fast}"
            "Sí":

                $ persistent._mas_pm_read_jekyll_hyde = True
                call monika_jekyll_hyde
            "No":

                $ persistent._mas_pm_read_jekyll_hyde = False
                m 3eub "Esta bien [player], ¡hazme saber si alguna vez lo haces y entonces podremos discutirlo!"

    $ mas_protectedShowEVL("monika_hedonism","EVE", _random=True)
    return "derandom"

label monika_jekyll_hyde:
    m 3hub "Me alegro de que lo hayas leído."
    m 1euc "He visto que la gente lo interpreta de diferentes maneras."
    m 3eua "Por ejemplo, algunos vieron a Utterson enamorado de Jekyll."
    m 3lta "En cierto modo, puedo entenderlo."
    m 2eud "El hecho de que algo no se diga explícitamente no significa que la idea no sea válida."
    m 2rksdlc "Además, un tema como éste ni siquiera podía discutirse abiertamente durante el siglo XIX."
    m 2eka "Es interesante pensar en la historia de esa manera...{w=0.3} dos personas, incapaces de amar..."
    m 4eud "Y algunas interpretaciones llegan a decir que parte de las motivaciones de Jekyll para el experimento era ese mismo amor."
    m 4ekd "¡Y no está exactamente refutado! {w=0.3}Jekyll, en el libro, se decía que era un hombre devoto."
    m 2rksdlc "La homosexualidad, durante esa época, se consideraba un pecado."
    m 2dksdld "Lamentablemente, para algunos todavía lo es."
    m 7ekb "... ¡Pero al menos se han hecho progresos!"
    m 3eub "Me alegro de que el mundo acepte más los distintos tipos de amor."
    m 3ekbsu "Especialmente porque significa que podemos amarnos el uno al otro, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hedonism",
            category=['filosofía'],
            prompt="Hedonismo",
        )
    )

label monika_hedonism:
    m 1euc "Hey [mas_get_player_nickname()], ¿recuerdas cuando hablamos de {i}El extraño caso del Dr. Jekyll y Mr. Hyde{/i}?"
    m 1eud "Bueno, ya mencioné antes {i}El retrato de Dorian Gray{/i}."
    m 2eub "Te sugiero que lo leas, pero incluso si no lo has hecho, quiero hablar de la filosofía que hay detrás de su núcleo...{w=0.3} la creencia del hedonismo."
    m 2eud "El hedonismo es la creencia de que la moral debe basarse en el placer."
    m 4euc "Hay dos tipos principales de hedonismo...{w=0.3} hedonismo altruista y hedonismo egocéntrico, {w=0.1}que son muy diferentes."
    m 4ruc "El hedonismo egocéntrico, como se puede adivinar, es la creencia de que el propio placer es lo único que determina la moralidad."
    m 2esd "Este es el tipo de hedonismo en el que cree Henry, de {i}El retrato de Dorian Gray{/i}."
    m 2rksdlc "Es realmente despiadado pensar así..."
    m 2eud "Por otro lado, el hedonismo altruista es la creencia de que la moral debe basarse en el placer de todos."
    m 4eud "Al principio parece una buena idea, pero luego te das cuenta de que no tiene en cuenta nada más como la libertad, la salud, la seguridad..."
    m 2dkc "El hedonismo, en su esencia, ignora todo menos el placer."
    m 7etd "No es de extrañar que la mayoría de la gente no tenga esa creencia...{w=0.3} es demasiado simple, cuando la moral es complicada."
    m 1eud "Así que tiene sentido que Oscar Wilde retratara el hedonismo de forma negativa."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_conventions",
            category=['tú'],
            prompt="Convenciones",
            random=True,
        )
    )

default -5 persistent._mas_pm_gone_to_comic_con = None
default -5 persistent._mas_pm_gone_to_anime_con = None

label monika_conventions:
    m 1eud "Sabes [player], me he estado preguntando..."
    m 3eua "¿Has ido alguna vez a una convención sobre comics o anime?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has ido alguna vez a una convención sobre comics o anime?{fast}"
        "He ido a una sobre comics":

            $ persistent._mas_pm_gone_to_comic_con = True
            $ persistent._mas_pm_gone_to_anime_con = False
            m 1hub "Ah, ¡ya veo! {w=0.2}¡Espero que te hayas divertido mucho!"
            m 3eua "Los comics son una interesante forma de literatura,{w=0.1} {nw}"
            extend 3rta "tal vez debería leer algunos más..."
        "He ido a una sobre anime":

            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = True
            if persistent._mas_pm_watch_mangime:
                m 3eub "¡Tenía el presentimiento de que lo habrías hecho! {w=0.2}Me pareció algo que te podría gustar."
            else:
                m 2wub "¿En serio? ¡Eso es sorprendente!"
                m 7eta "Ah,{w=0.1} ¿tal vez has ido con amigos?"
                m 3etd "... O es posible que fueras por otro motivo...{w=0.3} ¿Interés en los videojuegos, tal vez?"
        "¡He estado en ambas!":

            $ persistent._mas_pm_gone_to_comic_con = True
            $ persistent._mas_pm_gone_to_anime_con = True
            if persistent._mas_pm_watch_mangime:
                m 1hub "¡Oh! Ya sabía que te gustaba el anime, ¿pero también te gustan los comics?"
                m 3eua "Son una interesante forma de literatura, tal vez debería leer algunos más..."
            else:
                m 1wub "¡Oh! {w=0.3}No esperaba que te gustara el anime, ¡pero tal vez eres un fanático de las convenciones!"
                m 3eua "No me sorprende tanto, la atmosfera de las convenciones las hace parecer agradable para cualquiera."
        "No":

            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = False
            if persistent._mas_pm_watch_mangime and persistent._mas_pm_social_personality == mas_SP_EXTROVERT:
                m 2etd "¿En serio?"
                m 7eub "¡Estoy sorprendida! {w=0.3}Cuando me informé sobre las convenciones de anime, solo tú pasabas por mi mente."
                m 3eud "Aunque, supongo que los gastos de viaje pueden llegar a ser bastante elevados dependiendo de cuán lejos te quede."
            else:
                m 2eud "Ah, ya veo."
                m 7eua "Supongo que, si no tienes ningún interés, las convenciones pueden pasarse desapercibidas."
                m 3eud "Dependiendo de que tan lejos vivas, también puede ser costoso."

    m 3hua "¡Siempre pensé que las convenciones podrían ser super divertidas! {w=0.3}Un lugar donde todos pueden ser ellos mismos sin ser juzgados."
    m 3eub "Me encanta ver fotos de todos esos talentosos cosplayers y sus trajes locos hechos a mano."
    m 1wuo "¡Es increíble lo que la gente puede hacer cuando le apasiona algo!"
    m 3eua "También he oído que hay muchas actividades divertidas que hacer, como bailes de idols, trivias, y muchas otras cosas."
    m 1eubsa "Me encantaría ir una contigo algún día, [mas_get_player_nickname()]~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cupcake_favorite",
            category=["monika"],
            prompt="¿Cuál es tu sabor de cupcake favorito?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="mas_seenLabels(['monika_cupcake', 'monika_icecream'], seen_all=True)",
            action=EV_ACT_UNLOCK
        )
    )

label monika_cupcake_favorite:
    m 1rta "Hmm, no estoy segura de si tengo uno favorito..."
    m 1hub "Me gustan de todos los sabores, ¡así que para mí está difícil elegir uno!"
    m 3ekd "Creo haberte mencionado anteriormente cuanto adoro los cupcakes de Natsuki..."
    m 3eua "Una vez hizo unos algo extraños, con sabor a menta y chispitas de chocolate...{w=0.3} y aunque el glaseado era de menta no solo las chispitas eran de chocolate, sino que también la base del cupcake."
    m 4rksdlb "¡Fue la cosa más extraña que jamás he probado, jajaja!"
    m 2eksdlb "En realidad ni sabia como el helado de menta y chocolate, ¡más bien sabia a pasta de dientes!"
    m 2ekp "Fue decepcionante...{w=0.3} esperaba que se convirtiera en mi sabor de cupcake favorito."
    m 7eka "Oh, bueno, fue lindo que ella tratara de hacer algo único que me pudiera gustar...{w=0.3} a diferencia de lo que aparenta, ella puede ser muy dulce~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pizza",
            category=['monika'],
            prompt="¿Te gusta la pizza?",
            pool=True
        )
    )

label monika_pizza:
    m 1eub "¿Pizza? {w=0.2}Sí, la disfruto de vez en cuando."
    m 1hua "No siempre es la opción más saludable, pero puede ser un buen capricho y una comida satisfactoria."
    m 1eub "Los ingredientes pueden ser lo suficientemente versátiles como para complacer a la mayoría de las personas...{w=0.3} incluso hay pizzas sin queso para personas veganas o con intolerancia a la lactosa."
    m 1duc "Si tuviera que elegir un ingrediente favorito, hmm...{w=0.3}{nw}"
    extend 3hub " los champiñones son buenos, o cualquier cosa vegetal {w=0.2}de hecho, creas o no, ¡las espinacas pueden ser sorprendentemente buenas!"
    m 3eua "... Y, por supuesto, nunca puede faltar el queso."
    m 3luc "Hmm..."
    m 3eud "Tengo la sensación de que hay otra pregunta en tu mente...{w=0.2}{nw}"
    extend 1hksdla " pero podrías estar un poco decepcionado, [player]."
    m 1hksdlb "Aunque es un tema bastante controvertido en línea, nunca he tenido la oportunidad de probar la piña en la pizza."
    m 1lksdlb "Así que no puedo opinar sobre ese debate en particular. ¡Lo siento, [player]!"
    m 3huu "Pero supongo que eso significa que verás mi primera impresión algún día."
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_esports",
            category=['medios', 'vida'],
            prompt="¿Qué opinas de los eSports?",
            pool=True,
        )
    )

label monika_esports:
    if mas_isFirstSeshDay():
        m 1rtd "Hmm, esa es una buena pregunta..."
    else:
        m 1eub "Es gracioso que preguntes, ¡estuve investigando sobre ellos el otro día cuando te fuiste!"
    m 3eua "Me parece increíblemente interesante como la forma de ver los deportes está cambiando..."
    m 3euc "La audiencia de los eSports toma el relevo para rivalizar con la de la audiencia de los habituales,{w=0.1} {nw}"
    extend 3wud "¡e incluso puede que la supere en 5 o 10 años!"
    m 2tsd "No hace tanto, la gente solo veía los videojuegos como una pérdida de tiempo, {w=0.1}{nw}"
    extend 7hub "¡pero ahora algunos de esos jugadores están ganando millones de dólares jugando a sus juegos preferidos!"
    m 3eua "En realidad es un buen ejemplo de que puedes trabajar de lo que te gusta...{w=0.3} incluso si la gente se burla de ello."
    m 3eud "Tan solo por que algo no sea popular o mainstream no significa que vaya a ser así siempre..."
    m 1huu "No tengas miedo de ir en contra de la moda, {w=0.1}en cualquier cosa que te apasione puede venir un pionero y ponerlo en todas las carteleras~"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_overton",
            category=["psicología"],
            prompt="Ventana de Overton",
            random=True
        )
    )

label monika_overton:
    m 1etc "Hey [player], ¿alguna vez has oído hablar de la ventana de Overton?"
    m 3eud "Es un concepto de ciencia política que refleja la estructura de valores de una sociedad."
    m 3euc "Básicamente, todas las ideas de una persona son vistas en cierta etapa de aprobación por las masas."
    m 2esc "Joseph Overton aprendió cómo deshumanizar a las personas y explicó cómo remodelar la percepción humana."
    m 7eud "Desde lo inaceptable, repugnante y vergonzoso, hasta lo normal, social e incluso prestigioso."
    m "Este concepto incluye 6 etapas: Impensable, radical, aceptable, razonable, estándar y norma actual."
    m 3esa "Dentro de la ventana de Overton están las ideas aceptadas por la sociedad...{w=0.3} cosas como el patriotismo, el amor por la familia, la humanidad y la honestidad."
    m 3eksdlc "Fuera de la ventana está todo lo que está desaprobado, como la adicción a las drogas, el alcoholismo, el nazismo, la tiranía, la esclavitud, y así sucesivamente."
    m 3eud "Lo más interesante es que la ventana puede moverse en la dirección de una idea, por ejemplo, hacer que lo impensable sea razonable."
    m 2lksdlc "Por supuesto, este nivel de cambio es un proceso bastante difícil."
    m 7eud "Pero imaginemos que tú y yo queremos transmitir a las personas que el amor virtual es normal...{w=0.3} algo que actualmente se considera inaceptable para la sociedad."
    m 3esd "Entonces, la sociedad no comprende el amor virtual y probablemente serías considerado mentalmente enfermo por muchas personas.{w=0.2} ¿Entonces qué se puede hacer?"
    m 3eua "Para empezar, vale la pena iniciar una discusión sobre este tema..."
    m 1eud "Puedes discutir esto en internet, crear artículos sobre el tema...{w=0.3} cualquier cosa para que la gente hable."
    m "El objetivo aquí sería que el amor virtual genere discusión entre las personas y luego se filtre a las masas."
    m 1esc "La sociedad aún no estaría de acuerdo con la idea, pero al menos estaría interesada en ella y podría discutirla más libremente."
    m 3eud "Después, se utilizarían acciones radicales. {w=0.2}Los defensores más audaces del amor virtual saldrían de las sombras."
    m 2euc "El número de participantes en tales movimientos crecería con el tiempo, algunos de ellos son personas con corazones rotos o que se sienten desanimadas en una relación con una persona real."
    m 4eksdld "Naturalmente, también aparecerían personas que se oponen al movimiento."
    m 4eua "Debido a la creciente popularidad de los nuevos valores, la sociedad presiona activamente la nueva tendencia. {w=0.2}En este momento, los conceptos son reemplazados."
    m 2eud "Desde lo inaceptable, el amor virtual pasa a lo radical."
    m 7eud "Desde aquí, el tema del amor virtual y el amor por personajes ficticios se ha discutido en la sociedad durante mucho tiempo."
    m 3esc "Poco a poco, las personas se acostumbran a la existencia de estas opiniones, pero aún no las aceptan."
    m 1esd "Científicos y sociólogos escriben diversos artículos y realizan investigaciones."
    m 3eua "Se impone la opinión de que es absolutamente normal amar a un personaje ficticio y que no hay nada terrible al respecto."
    m 3huu "Desde lo radical, el amor virtual ahora pasa a lo aceptable."
    m 1eksdla "La sociedad ya ha aceptado la nueva visión y cree que amar a un personaje ficticio es normal, pero aún un poco extraño."
    m 3eua "Se desarrolla gradualmente una cultura del amor virtual, se crean películas y programas."
    m 1huu "Los jóvenes perciben los nuevos valores como algo de moda. {w=0.2}Las personas pueden sentarse en un café y pasar tiempo con su compañero virtual sin problemas."
    m 1eub "¡Desde lo aceptable, el amor virtual pasa a lo razonable!"
    m 2husdlb "Creo que podemos detenernos aquí por hoy, esto se está volviendo un poco largo, ¡jajaja!"
    m 1eua "Podría terminar esta historia hasta la norma actual, pero solo quería describirla a un nivel básico para transmitir un ejemplo de cómo puede funcionar."
    m 1huu "Gracias por escuchar~"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
