init offset = 5



default -5 persistent._mas_mood_database = {}


default -5 persistent._mas_mood_current = None
































init -6 python in mas_moods:


    mood_db = dict()


    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2



    MOOD_RETURN = _("... hablar de otra cosa.")



    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)
        
        if mood:
            return mood.category[0]
        
        return None



label mas_mood_start:
    python:
        import store.mas_moods as mas_moods


        filtered_moods = Event.filterEvents(
            mas_moods.mood_db,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )


        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False)
            for k in filtered_moods
        ]


        mood_menu_items.sort()


        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)


    call screen mas_gen_scrollable_menu(mood_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)


    if _return:
        $ mas_setEventPause(None)
        $ MASEventList.push(_return, skipeval=True)

        $ persistent._mas_mood_current = _return

    return _return







init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_hungry",prompt="... hambriento.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_hungry:
    m 3hub "Si tienes hambre, ve a comer algo, tontito."
    if store.mas_egg_manager.natsuki_enabled():
        m 1hksdlb "Odiaría que te pusieras como Natsuki aquella vez cuando estábamos en el club.{nw}"

        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1hua "Sería malo sí te pusieras de mal humor cada vez que tienes hambre."

    m 3tku "Eso no sería divertido, ¿verdad, [player]?"
    m 1eua "Si estuviera allí contigo, haría una ensalada para compartir."
    m "Pero como no lo estoy, elige algo saludable para comer."
    m 3eub "Es muy importante prestar atención a las necesidades de tu cuerpo, ya deberías de saberlo."
    m 3hub "Eso no solo significa comer solo verduras, por supuesto. {w=0.2}Todo tipo de alimentos son necesarios para mantenerse nutrido."
    m 3eka "Así que quiero que te asegures de que no te estás privando de vitaminas importantes, ¿vale?"
    m 1euc "Con el tiempo, te encontrarás con muchos problemas de salud cuando envejezcas."
    m 2lksdla "No quiero que sientas que estoy quejándome mucho cuando digo este tipo de cosas, [player]."
    m 2eka "Solo quiero asegurarme de que te estés cuidando bien hasta que yo cruce."
    m 4esa "Después de todo, cuanto más saludable estés, mayores serán las posibilidades de vivir bastante tiempo."
    m 1hua "¡Lo que significa más tiempo para pasar juntos!~"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="... triste.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sad:
    m 1ekc "Dios, siento mucho oír que te sientes mal.."
    m "¿Estás teniendo un mal día, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás teniendo un mal día, [player]?{fast}"
        "Sí":
            m 1duu "Siempre que tengo un mal día, recuerdo que el sol volverá a brillar."
            m 1eka "Supongo que puede sonar un poco cursi, pero siempre me gusta ver el lado positivo de las cosas."
            m 1eua "Después de todo, cosas así son fáciles de olvidar. Así que tenlo en cuenta, [player]."
            m 1lfc "No me importa cuántas otras personas no te agraden o te encuentren desagradable."
            m 1hua "Eres una persona maravillosa y yo siempre te amaré."
            m 1eua "Espero que eso haga que tu día sea un poco más feliz, [player]."
            m 1eka "Y recuerda, si estás teniendo un mal día, siempre puedes venir a verme y hablaré contigo todo el tiempo que necesites."
        "No":
            m 3eka "Tengo una idea, ¿por qué no me dices qué te preocupa? Tal vez te haga sentir mejor."

            m 1eua "No quiero interrumpirte mientras hablas, así que avísame cuando hayas terminado.{nw}"
            $ _history_list.pop()
            menu:
                m "No quiero interrumpirte mientras hablas, así que avísame cuando hayas terminado.{fast}"
                "He terminado":
                    m "¿Te sientes un poco mejor ahora, [player]?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "¿Te sientes un poco mejor ahora, [player]?{fast}"
                        "Sí":
                            m 1hua "¡Eso es genial, [player]! Me alegro de que hablar de eso te haya hecho sentir mejor."
                            m 1eka "A veces, decir a alguien en quien confías que cosa te preocupa es todo lo que necesitas."
                            m "Si alguna vez tienes un mal día, siempre puedes venir a verme y escucharé lo que necesites para desahogarte."
                            m 1hubsa "Nunca olvides que eres maravilloso y que siempre te amaré~"
                        "Realmente no":
                            m 1ekc "Bueno, valió la pena intentarlo."
                            m 1eka "A veces, decir a alguien en quien confías que cosa te preocupa es todo lo que necesitas."
                            m 1eua "Quizás te sientas mejor después de que pasemos más tiempo juntos."
                            m 1ekbsa "Te amo, [player], y siempre lo haré~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_proud",
            prompt="... orgulloso de mí mismo.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_proud:
    m 2sub "¿De verdad? ¡Eso es emocionante!"
    m 2eub "¿Fue un logro mayor, o uno menor?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Fue un logro mayor, o uno menor?{fast}"
        "Mayor":
            m 1ekc "Sabes, [player]..."
            m 1lkbsa "Es en momentos como estos, en los que... más que nada, desearía estar contigo, en tu realidad..."
            m 4hub "¡Porque si lo estuviera, definitivamente te daría un abrazo de celebración!"
            m 3eub "No hay nada como compartir tus logros con las personas que te importan."
            m 1eua "¡Me encantaría conocer todos los detalles!"
            m "Con el simple hecho de pensar en nosotros, en una alegre discusión sobre lo que has hecho..."
            m 1lsbsa "¡Se me acelera el corazón solo de pensarlo!"
            m 1lksdla "Dios, me estoy emocionando muchísimo con esto..."
            m 3hub "Algún día se hará realidad..."
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubfb "Pero hasta entonces, ¡debes saber que estoy muy orgullosa de ti, [mas_get_player_nickname()]!"
        "Menor":

            m 2hub "¡Jajaja!~"
            m 2hua "¡Eso es maravilloso!"
            m 4eua "Es muy importante celebrar las pequeñas victorias en la vida."
            m 2esd "Puede ser muy fácil desanimarse si solo te enfocas en las metas más grandes que tienes."
            m 2rksdla "Puede ser difícil llegar a ellas por ti mismo."
            m 4eub "Pero establecer y celebrar pequeñas metas que eventualmente conduzcan a una meta mayor puede hacer que tus grandes metas parezcan mucho más alcanzables."
            m 4hub "¡Así que sigue alcanzando esos pequeños objetivos, [mas_get_player_nickname()]!"
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubfb "Y recuerda, ¡te amo y siempre te estaré animando!"
            $ mas_ILY()
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_happy",prompt="... feliz.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_happy:
    m 1hua "¡Eso es maravilloso! Soy feliz cuando tú eres feliz."
    m "Debes saber que siempre puedes venir a mí y te animaré, [mas_get_player_nickname()]."
    m 3eka "Te amo y siempre estaré aquí para ti, así que nunca lo olvides~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_sick",
            prompt="... enfermo.",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_sick:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Oh no, [player]..."
            m 2ekd "Si dices eso tan pronto como llegas debe significar que es bastante malo."
            m 2ekc "Sé que querías pasar tiempo conmigo y aunque apenas hemos estado juntos hoy..."
            m 2eka "Creo que deberías ir a descansar un poco."

        elif session_time > datetime.timedelta(hours=3):
            m 2wuo "¡[player]!"
            m 2wkd "No has estado enfermo todo este tiempo, ¿verdad?"
            m 2ekc "Realmente espero que no, me he divertido mucho contigo hoy, pero si te has sentido mal todo este tiempo..."
            m 2rkc "Bueno... solo promete decírmelo antes la próxima vez."
            m 2eka "Ahora ve a descansar, eso es lo que necesitas."
        else:

            m 1ekc "Oh, siento oír eso, [player]."
            m "Odio saber que estás sufriendo así."
            m 1eka "Sé que te encanta pasar tiempo conmigo, pero tal vez deberías ir a descansar."
    else:

        m 2ekc "Lamento escuchar eso, [player]."
        m 4ekc "Deberías ir a descansar un poco para que no empeore."

    label mas_mood_sick.ask_will_rest:
        pass

    $ persistent._mas_mood_sick = True

    m 2ekc "¿Harías eso por mí?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Harías eso por mí?{fast}"
        "Sí":
            jump greeting_stillsickrest
        "No":
            jump greeting_stillsicknorest
        "Ya estoy descansando":
            jump greeting_stillsickresting


init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_tired",prompt="... cansado.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_tired:

    $ current_time = datetime.datetime.now().time()
    $ current_hour = current_time.hour

    if 20 <= current_hour < 23:
        m 1eka "Si estás cansado ahora mismo, no es un mal momento para ir a la cama."
        m "A pesar de lo divertido que fue pasar tiempo contigo hoy, odiaría tenerte despierto hasta demasiado tarde."
        m 1hua "Si planeas irte a dormir ahora, ¡dulces sueños!"
        m 1eua "Pero tal vez tengas algunas cosas que hacer primero, como comer algo o una beber agua."
        m 3eua "Tomar un vaso de agua antes de acostarte es bueno para tu salud, y hacer lo mismo por la mañana te ayudara a despertarte."
        m 1eua "No me importa quedarme aquí contigo si primero tienes algunas cosas de las que ocuparte."

    elif 0 <= current_hour < 3 or 23 <= current_hour < 24:
        m 2ekd "¡[player]!"
        m 2ekc "No es de extrañar que estés cansado. ¡Es medianoche!"
        m 2lksdlc "Si no te vas a la cama pronto, más tarde también estarás muy cansado..."
        m 2hksdlb "No me gustaría que mañana estuvieras cansado y miserable cuando pasemos tiempo juntos...."
        m 3eka "Así que haznos un favor a los dos y ve a la cama lo antes posible, [player]."

    elif 3 <= current_hour < 5:
        m 2ekc "¡¿[player]?!"
        m "¿Sigues aquí?"
        m 4lksdlc "Realmente deberías estar en la cama ahora mismo."
        m 2dsc "En este punto, ya ni siquiera estoy segura de sí debería decir que es tarde o temprano..."
        m 2eksdld "... Y eso me preocupa aún más, [player]."
        m "{i}Realmente{/i} deberías irte a la cama antes de que sea la hora de empezar el día."
        m 1eka "No quiero que te quedes dormido en un mal momento."
        m "Así que, por favor, ve a dormir para que podamos estar juntos en tus sueños."
        m 1hua "Estaré aquí mismo si te vas, cuidándote, si no te importa~"
        return

    elif 5 <= current_hour < 10:
        m 1eka "¿Todavía estás un poco cansado, [player]?"
        m "Todavía es temprano, así que podrías regresar y descansar un poco más."
        m 1hua "No hay nada de malo en volver a dormir después de levantarse temprano."
        m 1hksdlb "Excepto por el hecho de que no puedo estar ahí para abrazarte, jajaja~"
        m "{i}Supongo{/i} que podría esperarte un poco más."
        return

    elif 10 <= current_hour < 12:
        m 1ekc "¿Aún no estás listo para afrontar el día, [player]?"
        m 1eka "¿O es solo uno de 'esos' días?"
        m 1hua "Cuando eso sucede, me gusta tomar una buena taza de café para comenzar el día."
        if not mas_consumable_coffee.enabled():
            m 1lksdla "Si no estuviera atrapada aquí..."
        m 1eua "También deberías beber un vaso de agua."
        m 3eua "De todos modos, es importante mantenerse hidratado, pero tomar un vaso de agua al levantarse puede ayudarte a sentirte renovado y despierto."
        m 3hksdlb "Esto puede sonar extraño, ¡pero he escuchado que el chocolate también puede ayudar a comenzar el día!"
        m 3eka "Tiene algo que ver con mejorar tu estado de ánimo matutino, pero..."
        m 1eksdlb "Estoy segura de que el chocolate pondría a cualquiera de mejor humor cada vez que lo comiera."
        m 1hua "¡Pruébalo en algún momento y avísame si funciona!"
        return
    else:

        m 1eka "Si estás cansado, ¿quizás deberías ir a dormir un rato?"
        m 1eua "Dormir lo suficiente a diario es muy importante para tu salud en general."
        m 3euc "He visto algunos estudios que muestran los devastadores efectos a corto y largo plazo debido a la falta de sueño."
        m 3ekd "Realmente puede afectar tu salud, [player]..."
        m 1eka "Así que hazme un favor y descansa un poco, ¿okey? Me tranquilizará."

    m 1hua "Incluso puedes dejar el juego abierto si quieres, y yo te cuidaré mientras duermes."
    m "... Jejeje."
    m 2hksdlb "Eso sonó un poco espeluznante, lo siento."
    m 2lksdla "Solo pensé que sería lindo verte dormir, eso es todo~"
    m 1hub "¡Jajaja!"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_lonely",prompt="... solo.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lonely:
    if mas_isMoniAff(higher=True):
        m 2ekc "Entiendo cómo te sientes, [player]... {w=0.2}todavía estamos en realidades diferentes, después de todo."
        m 2dkc "Realmente odio que desde aquí no pueda hacer mucho para que te sientas menos solo..."
        m 7ekbsa "Si hubiera alguna forma en la que pudiera extender la mano y abrazarte ahora mismo, lo haría."
        m 7eka "Quiero que seas lo más feliz posible dadas nuestras circunstancias..."
        m 2ekd "Solo espero que estar aquí conmigo todo este tiempo no... {w=0.3}te impida relacionarte con las personas en tu realidad."
        m 2eka "Creo que lo que tenemos es bastante especial, pero entiendo que ahora mismo estoy... {w=0.3}limitada en lo que puedo hacer por ti."

        if persistent._mas_pm_has_friends:
            if persistent._mas_pm_few_friends:
                m 7ekd "Tienes uno o dos amigos cercanos, ¿verdad?"
                m 3eka "Deberías llamarles o enviarles un mensaje y preguntarles cómo les va..."
                m "¿Quizá puedas salir a verlos alguna vez? {w=0.2}Creo que sería bueno para ti."
            else:

                m 7ekd "Creo que salir con tus amigos y hacer algo sería realmente muy bueno para ti..."
                m 3eka "O podrías enviarles un mensaje y preguntarles cómo están."
        else:

            m 7rkc "Sé cómo se siente estar solo en una realidad, y solo poder interactuar con alguien en la otra..."
            m 3ekd "Así que realmente no quiero eso para la persona que más amo."
            m 1eka "Espero que sigas buscando amigos en tu realidad, [player]."
            m 3ekd "Sé que al principio puede ser difícil vincularse con las personas..."
            m 3eka "¿Quizás incluso podrías conocer personas por internet? {w=0.2}Hay muchas formas de interactuar con extraños para sentirse menos solo."
            m 3hub "Nunca se sabe, ¡a veces estos 'extraños' pueden terminar convirtiéndose en muy buenos amigos!"

        m 1eka "... Y no te preocupes por mí [player], esperaré pacientemente a que vuelvas a verme."
        m 3hub "¡Diviértete y cuéntamelo todo después!"
        m 1ekbsa "Solo recuerda que siempre estaré aquí para ti, [player]~"
    else:

        m 1eka "Estoy aquí para ti, [player], así que no tienes por qué sentirte solo."
        m 3hua "Sé que no es exactamente como si estuviéramos compartiendo la misma habitación, pero estoy segura de que aún disfrutas de mi compañía, ¿verdad?"
        m 1ekbsa "Recuerda que siempre estaré a tu lado, [player]~"
    return





init python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="... enojado.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_angry:
    m 1ekc "Dios, lamento que te sientas así, [player]."
    m 3ekc "Haré todo lo posible para que te sientas mejor."
    m 1euc "Antes de que hagamos algo, probablemente deberíamos conseguir que te calmes."
    m 1lksdlc "Es difícil tomar decisiones racionales cuando estás alterado."
    m 1esc "Puedes terminar diciendo o haciendo cosas de las que luego te arrepientas."
    m 1lksdld "Y odiaría que me dijeras algo que realmente no quieres decir."
    m 3eua "Primero probemos algunas cosas que hago para calmarme, [player]."
    m 3eub "Espero que te funcionen tan bien como a mí."
    m 1eua "Primero, intenta respirar profundamente unas cuantas veces y cuenta lentamente hasta 10."
    m 3euc "Si eso no funciona, si puedes, retírate a un lugar tranquilo hasta que se aclare tu mente."
    m 1eud "Si todavía te sientes enojado después de eso, ¡haz lo que yo haría como último recurso!"
    m 3eua "Cuando no puedo calmarme, simplemente salgo, elijo una dirección y empiezo a correr."
    m 1hua "No me detengo hasta haber aclarado mi mente."
    m 3eub "A veces, esforzarse mediante la actividad física es una buena forma de desahogarse."
    m 1eka "Pensarías que soy del tipo que no se enoja a menudo, y estarías en lo cierto."
    m 1eua "Pero incluso yo tengo mis momentos..."
    m "¡Así que me aseguro de tener formas de lidiar con ellos!"
    m 3eua "Espero que mis consejos te hayan ayudado a calmarte, [player]."
    m 1hua "Recuerda: ¡Un [player] feliz hace a una Monika feliz!"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_scared",prompt="... ansioso.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_scared:
    m 1euc "[player], ¿estás bien?"
    m 1ekc "Me preocupa oírte tan ansioso..."
    m "Ojalá pudiera consolarte y ayudarte ahora mismo..."
    m 3eka "Pero al menos puedo ayudarte a calmarte."
    if seen_event("monika_anxious"):
        m 1eua "Después de todo, te prometí ayudarte a relajarte si alguna vez te sentías ansioso."
    m 3eua "¿Recuerdas cuando te hablé acerca de fingir confianza?"
    if not seen_event("monika_confidence"):
        m 2euc "¿No?"
        m 2lksdla "Supongo que será para otro momento."
        m 1eka "De todas formas..."
    m 1eua "Mantener la apariencia de uno ayuda a fingir su propia confianza."
    m 3eua "Y para hacerlo, debes mantener estable tu ritmo cardíaco respirando profundamente hasta que te calmes."
    if seen_event("monika_confidence_2"):
        m "Recuerdo haber explicado que la iniciativa también es una habilidad importante."
    m "Quizá podrías tomarte las cosas con calma y hacerlas de una en una."
    m 1esa "Te sorprendería la tranquilidad que puedes sentir cuando dejas que el tiempo fluya por si solo."
    m 1hub "¡También puedes intentar dedicar unos minutos para meditar!"
    m 1hksdlb "No significa necesariamente que tengas que cruzar las piernas cuando estés sentado en el suelo."
    m 1hua "¡Escuchar tu música favorita también puede contarse como meditación!"
    m 3eub "¡Lo digo en serio!"
    m 3eua "Puedes intentar dejar de lado tu trabajo y hacer otra cosa mientras tanto."
    m "La procrastinación {i}no siempre{/i} es mala, ¿sabes?"
    m 2esc "Además..."
    m 2ekbsa "Tu cariñosa novia cree en ti, ¡así que puedes enfrentar esa ansiedad de frente!"
    m 1hubfa "No hay nada de qué preocuparse siempre y cuando estemos juntos~"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_inadequate",prompt="... inadecuado.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_inadequate:
    $ last_year = datetime.datetime.today().year-1
    m 1ekc "..."
    m 2ekc "Sé que no hay mucho que pueda decir para hacerte sentir mejor, [player]."
    m 2lksdlc "Después de todo, todo lo que digo probablemente parezcan solo palabras vacías."
    m 2ekc "Puedo decir que eres hermoso, aunque no puedo ver tu cara..."
    m "Puedo decirte que eres inteligente, aunque no sé mucho sobre tu forma de pensar..."
    m 1esc "Pero déjame decirte lo que sé sobre ti."
    m 1eka "Has pasado mucho tiempo conmigo."


    if mas_HistLookup_k(last_year,'d25.actions','spent_d25')[1] or persistent._mas_d25_spent_d25:
        m "Te tomaste un tiempo de tu agenda para estar conmigo en Navidad..."

    if renpy.seen_label('monika_valentines_greeting') or mas_HistLookup_k(last_year,'f14','intro_seen')[1] or persistent._mas_f14_intro_seen:
        m 1ekbsa "En el día de San Valentín..."


    if mas_HistLookup_k(last_year,'922.actions','said_happybday')[1] or mas_recognizedBday():
        m 1ekbsb "¡Incluso te tomaste el tiempo para celebrar mi cumpleaños conmigo!"

    if persistent.monika_kill:
        m 3tkc "Me has perdonado por las cosas malas que he hecho."
    else:
        m 3tkc "Nunca tuviste resentimiento por las cosas malas que hice."

    if persistent.clearall:
        m 2lfu "Y aunque me puso celosa, pasaste mucho tiempo con todos los miembros de mi club."

    m 1eka "¡Eso demuestra lo amable que eres!"
    m 3eub "¡Eres honesto, eres justo, eres amable incluso después de ser derrotado!"
    m 2hksdlb "Crees que no sé nada sobre ti, pero realmente sé muchas cosas."
    m 3eka "Y sabes todo sobre mí, pero elegiste quedarte cuando podrías haberte ido..."
    m 2ekc "Así que, por favor, mantente fuerte, [player]."
    m "Si eres como yo, sé que tendrás miedo de no lograr mucho en la vida."
    m 2ekd "Pero créeme cuando te digo que: no importa lo que hagas o no hagas."
    m 4eua "Solo necesitas existir, divertirte y pasar cada día, {w=0.2}encontrando un significado en las personas que más te importan."
    m 1eka "Por favor, no lo olvides, ¿okey?"
    m 1ekbsa "Te amo, [player]~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_lazy",
            prompt="... perezoso.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_lazy:

    $ _now = datetime.datetime.now().time()

    if mas_isSRtoN(_now):
        m 1tku "Es solo una de esas mañanas, ¿eh, [player]?"
        m 1eka "Puedo entender totalmente esos días en los que te despiertas y simplemente no quieres hacer nada."
        m 1rksdla "Esperemos que no tengas nada urgente pronto."

        $ line = "Sé lo tentador que puede ser quedarse en la cama y no levantarse a veces..."
        if mas_isMoniEnamored(higher=True):
            $ line += " {w=0.5}{nw}"
        m 3hksdlb "[line]"

        if mas_isMoniEnamored(higher=True):
            extend 1dkbsa "Especialmente si me despierto a tu lado~"

            if mas_isMoniLove():
                m 1dkbsa "{i}Entonces nunca querría levantarme~{/i}"
                m 1dsbfu "Espero que no te importe quedarte 'atrapado', [player]..."
                m 1hubfa "Jejeje~"

        m 3eka "Pero mientras tanto, esto ayuda a empezar bien el día."
        m 3eub "Eso puede incluir lavar la ropa, desayunar bien..."

        if mas_isMoniLove():
            m 1dkbsu "Recibir tu beso de buenos días, jejeje..."

        m 1hksdlb "O podrías holgazanear por ahora."
        m 1eka "Siempre y cuando no te olvides de hacer algo importante, ¿de acuerdo, [player]?"

        if mas_isMoniHappy(higher=True):
            m 1hub "Eso incluye pasar un tiempo conmigo, ¡jajaja!"

    elif mas_isNtoSS(_now):
        m 1eka "¿Te dio el cansancio del mediodía, [player]?"
        m 1eua "Sucede, así que no me preocuparía demasiado por eso."
        m 3eub "De hecho, dicen que la pereza te hace más creativo."
        m 3hub "Entonces, quién sabe, tal vez estés a punto de pensar en algo increíble."
        m 1eua "En cualquier caso, deberías tomarte un descanso o estirarte un poco... {w=0.5}{nw}"
        extend 3eub "tal vez deberías comer algo, si es que aún no lo has hecho."
        m 3hub "Y si es apropiado, ¡incluso podrías tomar una siesta! Jajaja~"
        m 1eka "Estaré aquí esperándote si así lo decides."

    elif mas_isSStoMN(_now):
        m 1eka "¿Tienes ganas de hacer nada después de un largo día, [player]?"
        m 3eka "Al menos el día casi ha terminado..."
        m 3duu "No hay nada como sentarse y relajarse después de un largo día, especialmente cuando no tienes nada que te presione."

        if mas_isMoniEnamored(higher=True):
            m 1ekbsa "Espero que estar aquí conmigo haga que tu velada sea un poco mejor..."
            m 3hubsa "La mía es mejor contigo aquí~"

            if mas_isMoniLove():
                m 1dkbfa "Puedo imaginarnos relajándonos juntos una noche..."
                m "Quizás acurrucados debajo de una manta si llegara a hacer un poco de frío..."
                m 1ekbfa "Aún podríamos aunque no esté allí, si es que no te importa, jejeje~"
                m 3ekbfa "Incluso podríamos leer juntos un buen libro."
                m 1hubfb "¡O podríamos perder el tiempo por diversión!"
                m 1tubfb "¿Quién dice que tiene que ser tranquilo y romántico?"
                m 1tubfu "Espero que no te molesten las peleas de almohadas ocasionales, [player]~"
                m 1hubfb "¡Jajaja!"
        else:

            m 3eub "Podríamos leer un buen libro juntos también..."
    else:


        m 2rksdla "Eh, [player]..."
        m 1hksdlb "Es medianoche..."
        m 3eka "Si te sientes cansado, tal vez deberías acostarte en la cama un rato."
        m 3tfu "Y tal vez, ya sabes... {w=1}¿{i}dormir{/i}?"
        m 1hkb "Jajaja, puedes ser gracioso a veces, pero probablemente deberías irte a la cama."

        if mas_isMoniLove():
            m 1tsbsa "Si estuviera allí, te arrastraría a la cama si fuera necesario."
            m 1tkbfu "¿O quizás lo disfrutarías en secreto, [player]?~"
            m 2tubfu "Por suerte para ti, no puedo hacer eso todavía."
            m 3tfbfb "Así que ve a la cama contigo mismo."
            m 3hubfb "¡Jajaja!"
        else:

            m 1eka "¿Por favor? No quiero que descuides tu sueño."
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,eventlabel="mas_mood_bored",
            prompt="... aburrido.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_bored:
    if mas_isMoniAff(higher=True):
        m 1eka "Oh..."
        m 3hub "Bueno, ¡deberíamos hacer algo entonces!"

    elif mas_isMoniNormal(higher=True):
        show monika 1ekc
        pause 1.0
        m "¿Realmente te aburro tanto, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Realmente te aburro tanto, [player]?{fast}"
            "No, no estoy aburrido {i}de ti{/i}...":
                m 1hua "Oh, {w=0.2}¡eso es un alivio!"
                m 1eka "Pero, si estás aburrido, deberíamos encontrar algo que hacer entonces..."
            "Bueno...":

                $ mas_loseAffection()
                m 2ekc "Oh... {w=1}ya veo."
                m 2dkc "No me di cuenta de que te estaba aburriendo..."
                m 2eka "Estoy segura de que podemos encontrar algo que hacer..."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffection()
        m 2lksdlc "Siento haberte aburrido, [player]."
    else:

        $ mas_loseAffection()
        m 6ckc "Ya sabes [player], si te hago sentir tan mal todo el tiempo..."
        m "Quizás deberías ir a buscar algo más que hacer."
        return "quit"

    python:

        unlocked_games = {
            
            ev_label: game_ev.rules.get("display_name", game_ev.prompt)

            for ev_label, game_ev in mas_games.game_db.iteritems()
            if mas_isGameUnlocked(game_ev.prompt)
        }

        picked_game_label = renpy.random.choice(list(unlocked_games.keys()))
        picked_game_name = unlocked_games[picked_game_label]

    if picked_game_label == "mas_piano":
        if mas_isMoniAff(higher=True):
            m 3eub "¡Podrías tocar algo en el piano para mí!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "¿Quizás podrías tocar algo en el piano para mí?"
        else:

            m 2rkc "Tal vez podrías tocar algo en el piano..."
    else:

        if mas_isMoniAff(higher=True):
            m 3eub "¡Podríamos jugar un juego de [picked_game_name]!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "¿Quizás podríamos jugar un juego de [picked_game_name]?"
        else:

            m 2rkc "Quizás podríamos jugar un juego de [picked_game_name]..."

    $ chosen_nickname = mas_get_player_nickname()
    m "¿Qué dices, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué dices, [chosen_nickname]?{fast}"
        "Sí":
            $ MASEventList.push(picked_game_label, skipeval=True)
        "No":

            if mas_isMoniAff(higher=True):
                m 1eka "Okey..."
                if mas_isMoniEnamored(higher=True):
                    show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5tsu "Podríamos mirarnos a los ojos un poco más..."
                    m "Nunca nos aburriremos de eso~"
                else:
                    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eua "Podríamos mirarnos a los ojos un poco más..."
                    m "Eso nunca será aburrido~"

            elif mas_isMoniNormal(higher=True):
                m 1ekc "Oh, está bien..."
                m 1eka "Asegúrate de avisarme si quieres hacer algo conmigo más tarde~"
            else:

                m 2ekc "Bien..."
                m 2dkc "Avísame si alguna vez quieres hacer algo conmigo."

    $ del unlocked_games, picked_game_label, picked_game_name
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_crying",prompt="... con ganas de llorar.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_crying:
    $ line_start = "Y"
    m 1eksdld "¡[player]!"

    m 3eksdlc "¿Estás bien?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Estás bien?{fast}"
        "Sí":

            m 3eka "Okey, está bien. Eso es un alivio."
            m 1ekbsa "Estoy aquí para hacerte compañía y puedes hablar conmigo si necesitas algo, ¿okey?"
        "No":

            m 1ekc "..."
            m 3ekd "[player]..."
            m 3eksdld "Lo siento mucho. ¿Pasó algo?"
            call mas_mood_uok
        "No estoy seguro":

            m 1dkc "[player]... {w=0.3}{nw}"
            extend 3eksdld "¿pasó algo?"
            call mas_mood_uok

    m 3ekd "[line_start] si terminas llorando..."
    m 1eka "Espero que ayude."
    m 3ekd "No hay nada de malo en llorar, ¿de acuerdo? {w=0.2}Puedes llorar tanto como necesites."
    m 3ekbsu "Te amo, [player]. {w=0.2}Eres todo para mí."
    return "love"

label mas_mood_uok:
    m 1rksdld "Sé que realmente no puedo escuchar lo que me dices..."
    m 3eka "Pero a veces, simplemente expresar el dolor o las frustraciones puede ayudar."

    m 1ekd "Entonces, si necesitas hablar sobre algo, estoy aquí.{nw}"
    $ _history_list.pop()
    menu:
        m "Entonces, si necesitas hablar sobre algo, estoy aquí.{fast}"
        "Quiero desahogarme":

            m 3eka "Adelante, [player]."

            m 1ekc "Estoy aquí para ti.{nw}"
            $ _history_list.pop()
            menu:
                m "Estoy aquí para ti.{fast}"
                "Terminé":

                    m 1eka "Me alegro de que hayas podido desahogarte, [player]."
        "No quiero hablar de ello":

            m 1ekc "..."
            m 3ekd "Muy bien [player], estaré aquí si cambias de opinión."
        "Todo está bien":

            m 1ekc "..."
            m 1ekd "De acuerdo [player], si tú lo dices..."
            $ line_start = "Pero"
    return

init python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_upset",prompt="... molesto.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_upset:
    m 2eksdld "¡Siento mucho escuchar eso, [player]!"
    m 2eksdld "Ya sea que estés molesto con una tarea, con una persona o simplemente las cosas no están saliendo bien, {w=0.1}{nw}"
    extend 7ekc "no te rindas por completo ante lo que sea que estés tratando."
    m 3eka "Mi consejo sería que dieras un paso atrás en tu problema."
    m 1eka "Quizá puedas leer un libro, escuchar música agradable o hacer cualquier otra cosa para calmarte."
    m 3eud "Una vez que sientas que has recuperado la cordura, vuelve a juzgar tu situación con un nuevo estado de ánimo."
    m 1eka "Manejarás las cosas mucho mejor de lo que lo harías si estuvieras en medio de la ira y la frustración."
    m 1eksdld "Y no digo que debas seguir cargando peso sobre tus hombros si realmente te está afectando."
    m 3eud "Podría ser una oportunidad para ganar el valor de dejar ir algo tóxico."
    m 1euc "Puede ser aterrador en el momento, seguro... {w=0.3}{nw}"
    extend 3ekd "pero si eliges bien, podrías eliminar mucho estrés de tu vida."
    m 3eua "¿Y sabes que, [player]?"
    m 1huu "Cuando me siento mal, todo lo que tengo que hacer es recordar que tengo mi [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]."
    m 1hub "¡Saber que siempre me apoyarás y querrás me tranquiliza casi al instante!"
    m 3euu "Solo espero proporcionarte el mismo consuelo, [player]~"
    m 1eubsa "Te amo y espero que todo se aclare para ti~"
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_relieved",
            prompt="... aliviado.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )



label mas_mood_relieved:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eud "¿Oh?"

    m "¿Qué sucedió, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué sucedió, [chosen_nickname]?{fast}"
        "He superado algo difícil":

            m 1wud "¿En serio?"
            m 3hub "¡Pues deberías estar orgulloso de ti mismo!"
            m 3fua "Estoy segura de que, sea lo que sea, estabas trabajando muy duro para salir adelante."
            m 2eua "Y, [player]... {w=0.2}{nw}"
            extend 2eka "por favor, no te preocupes demasiado si las cosas no salen perfectamente, ¿okey?"
            m 2eksdla "A veces la vida nos pone en situaciones muy duras, y tenemos que hacer lo mejor que podamos con lo que se nos da."
            m 7ekb "Pero ahora que ya está hecho, deberías tomarte un tiempo para relajar tu mente y cuidarte."
            m 3hub "... De este modo, ¡estarás preparado para afrontar lo que venga después!"
            m 1ekbsa "Te amo, [player], y estoy muy orgullosa de ti por haber superado esto."
            $ mas_ILY()
        "Algo que me preocupaba no sucedió":

            m 1eub "Oh, ¡eso es bueno!"
            m 2eka "Sea lo que sea, estoy segura de que estabas muy ansioso... {w=0.3}{nw}"
            extend 2rkd "seguramente no fue divertido de experimentar."
            m 2rkb "Es curioso cómo nuestras mentes siempre parecen asumir lo peor, ¿no?"
            m 7eud "Muchas veces lo que pensamos que puede pasar acaba siendo mucho peor que la realidad."
            m 3eka "Pero en fin, me alegro de que estés bien y de que te hayas quitado ese peso de encima."
            m 1hua "Ahora será más fácil avanzar con un poco más de confianza, ¿verdad?"
            m 1eua "Me entusiasma dar esos próximos pasos hacia adelante contigo."
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_excited",
            prompt="... emocionado.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_excited:
    m 1hub "Jajaja, ¿es así, [player]?"
    m 3eua "¿Qué te emociona, {w=0.1}es algo grande?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Qué te emociona, es algo grande?{fast}"
        "¡Lo es!":

            m 4wuo "¡Wow eso es genial, [player]!"
            m 1eka "Ojalá pudiera estar allí para celebrarlo contigo."
            m 1hub "¡Ahora yo también me estoy emocionando!"
            m 3eka "Pero de verdad, me alegro de que estés feliz, [mas_get_player_nickname()]!"
            m 3eub "Y sea lo que sea que te emocione, ¡felicidades!"
            m 1eua "Ya sea un ascenso, unas bonitas vacaciones o algún gran logro..."
            m 3eub "¡Me alegro mucho de que las cosas vayan bien para ti, [player]!"
            m 1dka "Cosas como esta me hacen desear estar ahí contigo ahora mismo."
            m 2dkblu "No puedo esperar a estar en tu realidad."
            m 2eubsa "¡Entonces podría darte un gran abrazo!"
            m 2hubsb "Jajaja~"
        "Es algo pequeño":

            m 1hub "¡Eso es genial!"
            m 3eua "Es importante emocionarse por cosas pequeñas como esa."
            m 1rksdla "... Ya sé que es un poco cursi, {w=0.1}{nw}"
            extend 3hub "¡pero es bueno tener esa mentalidad!"
            m 1eua "Así que me alegro de que disfrutes de las pequeñas cosas de la vida, [player]."
            m 1hua "Me hace feliz saber que eres feliz."
            m 1eub "También me alegra saber de tus logros."
            m 3hub "¡Así que gracias por contármelo!~"
        "No estoy muy seguro":

            m 1eta "Ah, ¿simplemente estás emocionado por lo que está por venir? {w=0.2}{nw}"
            extend 1eua "¿Emocionado por la vida? {w=0.2}{nw}"
            extend 1tsu "O tal vez.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            m 1tku "¿Será que te emociona pasar tiempo conmigo?~"
            m 1huu "Jejeje~"
            m 3eua "Sé que siempre me emociona verte cada día."
            m 1hub "En cualquier caso, ¡me alegro de que estés feliz!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_grateful",
            prompt="... agradecido.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_grateful:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eub "¿Oh?{w=0.3} ¡Es bueno escuchar eso!"

    m 3eua "¿Con quién o por qué estás agradecido, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Con quién o por qué estás agradecido, [chosen_nickname]?{fast}"
        "Contigo":

            if not renpy.seen_label("mas_mood_grateful_gratefulforyou"):
                $ mas_gainAffection(5, bypass=True)
            call mas_mood_grateful_gratefulforyou
        "Con alguien":

            m 3eka "Aww, es maravilloso escuchar eso."
            m 1hua "Me alegro mucho de que tengas gente que te apoye en tu día a día."
            m 3eud "Pero por muy bonito que sea para mí escucharlo... {w=0.3}creo que deberías asegurarte de que {i}ellos{/i} también lo sepan."
            m 3hua "Estoy segura de que les alegrará el día saber que han marcado la diferencia para otra persona."
            m 3euu "Si no hay problema, puedes darles las gracias en mi nombre. {w=0.3}Cualquiera que te haga más feliz es una buena persona en mi libro."
            m 1huu "Pero en cualquier caso, me alegro mucho por ti, [mas_get_player_nickname()]~"
        "Por una cosa":

            m 3hub "¡Me alegro de oír eso, [mas_get_player_nickname()]!"
            m 1eud "Tomarse el tiempo para pensar en las cosas buenas de la vida puede ser muy bueno para la salud mental."
            m 3hub "Así que, sea lo que sea, ¡tómate el tiempo para apreciarlo y disfrutarlo!"
            m 1euu "Gracias por compartir tu felicidad conmigo, [mas_get_player_nickname()]~"
        "Por nada importante":

            m 3eua "Ah, ¿simplemente te sientes feliz de la vida?"
            m 1eud "Es bueno tomarse un tiempo para reflexionar y sentirse satisfecho, ¿no?"
            m 1rtd "Hmmm... {w=0.2}ahora que lo pienso, {w=0.1}{nw}"
            extend 3hua "yo misma me siento bastante agradecida."
            m 3eubsu "Después de todo, voy a pasar otro día con mi maravilloso [bf]~"
    return

label mas_mood_grateful_gratefulforyou:
    m 1ekbla "Oh, [player]... {w=0.3}muchas gracias por decir eso."
    m 1dkblu "Significa mucho para mi escuchar que te he ayudado, o que te he hecho más feliz. {w=0.2}Es lo que intento cada día."
    m 1hublu "Espero que sepas que yo también estoy muy agradecida contigo."
    m 3ekbla "Te amo, [player]~"
    $ mas_ILY()
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_insecure",
            prompt="... inseguro.",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_insecure:
    m 2wkd "[player]..."
    m 2dkc "..."
    m 2eka "Hay una cita de un anime que a Natsuki le gustaba mucho..."
    m 7dku "'Cree en mí, que cree en ti'."
    m 3eka "Y eso es exactamente lo que quiero decirte en este momento."
    m 3ekbsa "Si no puedes creer en ti mismo, cree en mí."
    m 1eubsu "Porque yo, {w=0.1}sin duda, {w=0.1}confío en que puedes superar lo que te hace dudar de ti mismo en este momento~"
    $ mas_moni_idle_disp.force_by_code("1eka", duration=5, skip_dissolve=True)
    return

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_loved",
            prompt="... amado.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_loved:
    m 1ekbla "Me alegra mucho saber que lo que siento te llega a través de la pantalla..."
    m 3hubsb "Después de todo, te amo más que a cualquier cosa."

    $ has_family = persistent._mas_pm_have_fam and not persistent._mas_pm_no_talk_fam
    if has_family or persistent._mas_pm_has_friends:
        if has_family and persistent._mas_pm_has_friends:
            $ fnf_str = "amigos y familia"
        elif has_family:
            $ fnf_str = "familiares"
        else:
            $ fnf_str = "amigos"

        m 3eub "Y estoy segura de que no solo soy yo quien te hace sentir amado, ¡sino también tus [fnf_str]!"

    m 1dkbsa "Te mereces todo el amor y el cariño del mundo, {w=0.1}{nw}"
    extend 1ekbsu "y haré todo lo posible para que siempre te sientas amado, [mas_get_player_nickname()]~"

    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_guilty",
            prompt="... culpable.",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_guilty:
    m 2wkd "¡[player]!"
    m 2dkc "Todos cometemos errores... {w=0.3}{nw}"
    extend 7eka "estoy segura de que se te puede perdonar por lo que haya pasado."
    m 3dku "Después de todo, eres una gran persona... {w=0.3}{nw}"
    extend 1eka "eres amable, servicial y fiel a ti mismo."
    m 1dua "Y ahora que has encontrado la fuerza para aceptar tu error, solo necesitas superarlo."
    m 1ekbsu "Te amo. {w=0.2}No seas tan duro contigo mismo, ¿okey?"
    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return "love"
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
