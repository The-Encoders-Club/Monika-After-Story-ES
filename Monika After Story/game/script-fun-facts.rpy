
default persistent._mas_fun_facts_database = dict()
init offset = 5
init -15 python in mas_fun_facts:

    fun_fact_db = {}

    def getUnseenFactsEVL():
        """
        Gets all unseen (locked) fun facts as eventlabels

        OUT:
            List of all unseen fun fact eventlabels
        """
        return [
            fun_fact_evl
            for fun_fact_evl, ev in fun_fact_db.iteritems()
            if not ev.unlocked
        ]

    def getAllFactsEVL():
        """
        Gets all fun facts regardless of unlocked as eventlabels

        OUT:
            List of all fun fact eventlabels
        """
        return fun_fact_db.keys()



default -5 persistent._mas_funfactfun = True

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fun_facts_open",
            category=['misc'],
            prompt="¿Puedes decirme un dato curioso?",
            pool=True
        )
    )

label monika_fun_facts_open:
    if mas_getEVL_shown_count("monika_fun_facts_open") == 0:
        m 1eua "Dime [player], ¿te gustaría escuchar un dato curioso?"
        m 1eub "He estado buscando algunos para intentar enseñarnos algo nuevo a los dos."
        m 3hub "Dicen que aprendes algo nuevo todos los días, de esta manera me aseguro de que realmente lo hagamos."
        m 1rksdla "Encontré la mayoría de estos en línea, así que no puedo afirmar que sean {i}definitivamente{/i} ciertos..."
    else:

        m 1eua "¿Quieres otro dato curioso, [player]?"
        if persistent._mas_funfactfun:
            m 3hua "¡Ese último fue bastante interesante después de todo!"
        else:
            m 2rksdlb "Sé que el último no fue genial... pero estoy segura de que el próximo será mejor."
    m 2dsc "Ahora, veamos.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    python:
        unseen_fact_evls = mas_fun_facts.getUnseenFactsEVL()
        if len(unseen_fact_evls) > 0:
            fact_evl_list = unseen_fact_evls
        else:
            fact_evl_list = mas_fun_facts.getAllFactsEVL()


        fun_fact_evl = renpy.random.choice(fact_evl_list)
        mas_unlockEVL(fun_fact_evl, "FFF")
        MASEventList.push(fun_fact_evl)
    return


label mas_fun_facts_end:
    m 3hub "Espero que hayas disfrutado de otra sesión de: '¡Aprendiendo con Monika!'"
    $ persistent._mas_funfactfun = True
    return

label mas_bad_facts_end:
    m 1rkc "Ese dato no fue muy bueno..."
    m 4dkc "Lo intentaré mejor la próxima vez, [player]."
    $ persistent._mas_funfactfun = False
    return



init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_librocubiculartist",
        ),
        code="FFF"
    )

label mas_fun_fact_librocubiculartist:
    m 1eub "¿Sabías que hay una palabra para describir a alguien a quien le gusta leer en la cama?"
    m 3eub "Esa es 'librocubicularista'. A primera vista parece difícil de pronunciar."
    m 3rksdld "Es una verdadera lástima que algunas palabras nunca se usen en general."
    m 3eud "Pero si dices esa palabra, la mayoría de las personas no sabrá de qué estás hablando."
    m 3euc "Probablemente tendrías que explicar lo que significa, pero eso frustra el sentido de usar la palabra."
    m 2rkc "¡Si tan solo las personas leyeran más y mejoraran su vocabulario!"
    m 2hksdlb "... Jejeje, lo siento [player]. No quise molestarme tanto~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_menu_currency",
        ),
        code="FFF"
    )

label mas_fun_fact_menu_currency:
    m 3euc "Supuestamente, muchos restaurantes omiten intencionalmente cualquier signo de moneda en sus menús."
    m 3eud "Esto se hace para manipular psicológicamente a las personas para que gasten más dinero del necesario."
    m 2euc "Funciona porque se utiliza un signo de moneda, como el dólar, para representar un costo."
    m "Al eliminarlo, elimina la asociación de ese costo y solo se piensa en la comida de tu elección."
    m 4rksdld "La práctica parece comprensible. Después de todo, sigue siendo un negocio."
    m 2dsc "No importa qué tan buena sea la comida en un restaurante, cerrarán rápidamente si son vencidos por la competencia."
    m 3hksdlb "Oh bueno, ¿que puedes hacer?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_love_you",
        ),
        code="FFF"
    )

label mas_fun_fact_love_you:
    m 1dkc "Mmm, no estoy segura de si debería decirte {i}este{/i} dato."
    m 1ekc "No es para los débiles de corazón después de todo."
    m 1rkc "La cosa es que..."
    m 1dkc "..."
    m 3hub "... ¡Te amo, [player]!"
    m 1rksdlb "Jejeje, lo siento, no pude evitarlo."
    m 1hksdlb "Tendré un dato real la próxima vez, no te preocupes~"

    $ persistent._mas_funfactfun = True
    return "love"

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_morpheus",
        ),
        code="FFF"
    )

label mas_fun_fact_morpheus:
    m 3wub "¡Oh! Un dato basado en el lenguaje. Siempre me gustan estos."
    m 1eua "La palabra 'morfina' se basa en el dios griego Morfeo."
    m 1euc "Morfeo era el dios griego de los sueños, por lo que tener una palabra basada en él tiene sentido."
    m 3ekc "Pero acaso... ¿no era su padre Hipnos el dios del sueño?"
    m 2dsc "La morfina {i}sí{/i} permite que una persona sueñe, pero en realidad su objetivo es hacer que alguien se duerma."
    m 4ekc "... Entonces, ¿no tendría más sentido ponerle el nombre de Hipnos?"
    m 4rksdlb "Demasiado poco, demasiado tarde, supongo."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_otter_hand_holding",
        ),
        code="FFF"
    )

label mas_fun_fact_otter_hand_holding:
    m 1eka "Aww, este es realmente dulce."
    m 3ekb "¿Sabías que las nutrias marinas se toman de la mano cuando duermen para evitar alejarse unas de otras?"
    m 1hub "Es práctico para ellas, ¡pero hay algo realmente lindo en ello!"
    m 1eka "A veces me imagino en su posición..."
    m 3hksdlb "Oh, no ser una nutria marina, si no sostener la mano de quien amo mientras duermo."
    m 1rksdlb "Jaja, realmente me hacen sentir celosa."
    m 1hub "Sin embargo, algún día llegaremos allí amor~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_chess",
        ),
        code="FFF"
    )

label mas_fun_fact_chess:

    if mas_isGameUnlocked("ajedrez"):
        m 1eua "¡Este es un dato curioso!"
        m 3eub "Había un hombre llamado Claude Shannon que calculó la máxima cantidad de movimientos posibles en el ajedrez."
        m "Ese número se llama 'el número de Shannon' y establece que la cantidad de juegos de ajedrez posibles es de 10^120."
        m 1eua "A menudo se compara con la cantidad de átomos en el universo observable que es 10^80."
        m 3hksdlb "Es una locura pensar que podría haber más movimientos de ajedrez que átomos, ¿no?"
        m 1eua "Podríamos jugar hasta el final de nuestros días y no se acercaría ni a una fracción de lo que es posible."
        m 3eud "Hablando de eso, [player]..."
        m 1hua "¿Quieres jugar una partida de ajedrez conmigo? Incluso podría ser amable contigo, jejeje~"

        call mas_fun_facts_end
        return


    elif not mas_isGameUnlocked("ajedrez") and renpy.seen_label("mas_unlock_chess"):
        m 1dsc "Ajedrez..."
        m 2dfc "..."
        m 2rfd "Puedes olvidarte de este dato ya que eres un tramposo, [player]."
        m "Sin mencionar que nunca te disculpaste."
        m 2lfc "... Hmph."

        return
    else:


        m 1euc "Oh, este no."
        m 3hksdlb "Todavía no, al menos."

        call mas_bad_facts_end
        return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_struck_by_lightning",
        ),
        code="FFF"
    )

label mas_fun_fact_struck_by_lightning:
    m 2dkc "Hmm, este suena un poco engañoso..."
    m 3ekc "'Los hombres tienen seis veces más probabilidades de ser alcanzados por un rayo que las mujeres'."
    m 3ekd "Es... bastante tonto, en mi opinión."
    m 1eud "Si los hombres son más propensos a ser alcanzados por un rayo, entonces probablemente sea el paisaje y las circunstancias de su trabajo lo que los hace más propensos a ser golpeados."
    m 1euc "Los hombres tradicionalmente siempre han trabajado en lugares más peligrosos y elevados, por lo que no es de extrañar que cosas así les sucedan a menudo."
    m 1esc "Sin embargo, la forma en que está redactado este dato hace que parezca que solo por ser hombre es más probable que suceda, lo cual es ridículo."
    m 1rksdla "Quizás si estuviera mejor redactado, las personas no estarían tan mal informadas sobre ellos."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_honey",
        ),
        code="FFF"
    )

label mas_fun_fact_honey:
    m 1eub "Ah, este es uno bonito y fácil."
    m 3eub "¿Sabías que la miel nunca se echa a perder?"
    m 3eua "Sin embargo, la miel se puede cristalizar. Algunas personas pueden ver esto como algo malo, ¡pero aún así es completamente comestible y está bien!"
    m "La razón por la que esto sucede es porque la miel está compuesta principalmente de azúcar y solo un poco de agua, lo que la hace sólida con el tiempo."
    m 1euc "La mayor parte de la miel que se ve en las tiendas no cristaliza tan rápido como la miel real porque ha sido pasteurizada en el proceso de elaboración."
    m 1eud "... Lo que elimina las cosas que hacen que la miel se solidifique rápidamente."
    m 3eub "¿Pero no sería bueno comer miel cristalizada también?"
    m 3hub "¡Sería como un caramelo cuando lo muerdas!"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_vincent_van_gone",
        ),
        code="FFF"
    )

label mas_fun_fact_vincent_van_gone:
    m 1dsc "Ah, este..."
    m 1ekd "Es un poco desalentador, [player]..."
    m 1ekc "¿Sabías que las últimas palabras de Vincent Van Gogh fueron: '{i}La tristesse durera toujours{/i}'?"
    m 1eud "Si lo traduces, significa: '{i}La tristeza durará para siempre{/i}'."
    m 1rkc "..."
    m 2ekc "Es realmente triste saber que alguien tan famoso diría algo tan oscuro en su último aliento."
    m 2ekd "Sin embargo, no creo que sea cierto. No importa lo mal que se pongan las cosas y lo profunda que pueda ser la tristeza..."
    m 2dkc "Llegará un momento en el que ya no estará allí."
    m 2rkc "... O al menos no será notable."
    m 4eka "Si alguna vez estás triste, sabes que puedes hablar conmigo, ¿verdad?"
    m 5hub "Siempre aceptaré y asumiré cualquier carga que lleves, [mas_get_player_nickname()]~"

    $ persistent._mas_funfactfun = True
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_king_snakes",
        ),
        code="FFF"
    )

label mas_fun_fact_king_snakes:
    m 1dsc "Hmm..."
    m 3eub "¿Sabías que si una serpiente tiene la palabra 'realeza' en su nombre, es porque devora a otras serpientes?"
    m 1euc "Siempre me pregunté por qué una cobra real se llamaría así, pero nunca pensé más en ello."
    m 1tfu "¿Eso significa que si te como, me convertiré en la reina Monika?"
    m 1hksdlb "Jajaja, solo estoy bromeando, [player]."
    m 1hub "Perdón por ser un poco rara~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_strength",
        ),
        code="FFF"
    )

label mas_fun_fact_strength:
    m 1hub "¡Este dato podría motivarte un poco!"
    m 3eub "La palabra más larga en inglés que solo contiene una vocal es 'strength'."
    m 1eua "Es curioso cómo de cada palabra del lenguaje, es una palabra tan significativa que tenía ese pequeño detalle."
    m 1hua "¡Pequeños detalles como este realmente hacen que el lenguaje sea tan fascinante para mí!"
    m 3eua "¿Quieres saber qué viene a mi mente cuando pienso en la palabra 'strength'?"
    m 1hua "¡Tú!"
    m 1hub "Porque eres la fuente de mi fuerza, jejeje~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_reindeer_eyes",
        ),
        code="FFF"
    )

label mas_fun_fact_reindeer_eyes:
    m 3eua "¿Listo para este?"
    m "Los ojos de un reno cambian de color según la temporada. Son dorados en verano y azules en invierno."
    m 1rksdlb "Es un fenómeno realmente extraño, aunque no sé por qué..."
    m "Probablemente haya una buena razón científica para ello."
    m 3hksdlb "¿Quizás puedas buscarla tú mismo?"
    m 5eua "Sería divertido que me enseñases esta vez~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_bananas",
        ),
        code="FFF"
    )

label mas_fun_fact_bananas:
    m 1eub "Oh, ¡yo diría que este dato es saludable!"
    m 3eua "¿Sabías que cuando un plátano crece, se curva para mirar al sol?"
    m 1hua "Es un proceso llamado geotropismo negativo."
    m 3hub "¿No crees que es bastante bueno?"
    m 1hua "..."
    m 1rksdla "Umm..."
    m 3rksdlb "Supongo que no tengo mucho más que decir al respecto, jajaja..."
    m 1lksdlc "..."
    m 3hub "¿S-Sabías también que los plátanos en realidad no son frutas si no bayas?"
    m 3eub "¿O que los plátanos originales eran grandes, verdes y llenos de semillas duras?"
    m 1eka "¿Qué tal el hecho de que son ligeramente radiactivos?"
    m 1rksdla "..."
    m 1rksdlb "... Ahora solo estoy divagando sobre los plátanos."
    m 1rksdlc "Ummm..."
    m 1dsc "Sigamos adelante..."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pens",
        ),
        code="FFF"
    )

label mas_fun_fact_pens:
    m 1dsc "Hmm... estoy segura de que ya conozco este."
    m 3euc "La palabra 'bolígrafo' se deriva de la palabra latina 'bulla', que significa burbuja en latín y la palabra 'grafo' que viene del griego y significa escribir."
    m "Los bolígrafos en ese entonces eran plumas de ganso afiladas sumergidas en tinta, por lo que tendría sentido por qué los llaman también 'plumas'."
    m 3eud "A partir del siglo VI fueron la principal herramienta de escritura durante mucho tiempo."
    m 3euc "Solo hasta el siglo XIX, cuando se fabricaron los bolígrafos de metal, y los otros empezaron a decaer."
    m "De hecho, las navajas se llaman 'penknife' en inglés, porque originalmente se usaban para adelgazar y apuntar plumas a las que se le dice 'pen' en inglés."
    m 1tku "Pero estoy segura de que Yuri sabría más sobre esto que yo..."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_density",
        ),
        code="FFF"
    )

label mas_fun_fact_density:
    m 1eub "Oh, ya sé."
    m 3eua "¿Sabías que el planeta más denso de nuestro sistema solar es la propia Tierra?"
    m "¿Y que Saturno es el menos denso?"
    m 1eua "Tiene sentido saber de qué están hechos los planetas, pero como Saturno es el segundo más grande, fue una pequeña sorpresa."
    m 1eka "¡Supongo que el tamaño realmente no importa!"
    m 3euc "Pero entre tú y yo, [player]..."
    m 1tku "Sospecho que la Tierra solo puede ser la más densa debido a cierto personaje principal."
    m 1tfu "Pero eso es todo lo que oirás de mí~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_binky",
        ),
        code="FFF"
    )

label mas_fun_fact_binky:
    m 3hub "¡Aww, este es lindo!"
    m "¡Este dato realmente te hará 'saltar' [player]!"
    m 3hua "Siempre que un conejo salta emocionado, ¡se llama 'binky'!"
    m 1hua "Binky es una palabra en inglés que suena tan linda que realmente se adapta a la acción."
    m 1eua "Es la forma de expresión más feliz que un conejo puede hacer, así que si lo ves, sabrás que lo estás tratando bien."
    m 1rksdla "Bueno, aunque me haces tan feliz como para evitar llenarme de energía."
    m 1rksdlb "¡No esperes que empiece a saltar, [player]!"
    m 1dkbsa "... Sería {i}demasiado{/i} vergonzoso hacerlo."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_windows_games",
        ),
        code="FFF"
    )

label mas_fun_fact_windows_games:
    m 1eua "Mmm, tal vez este te resulte más interesante."
    m 3eub "El juego de cartas 'Solitario' se introdujo originalmente en el sistema operativo Windows en 1990."
    m 1eub "El juego se agregó como una función para enseñar a los usuarios a usar el mouse."
    m 1eua "De manera similar, se agregó 'Buscaminas' para familiarizar a los usuarios con el clic izquierdo y derecho."
    m 3rssdlb "Las computadoras han existido durante tanto tiempo que es difícil pensar un momento en el que no fueran relevantes."
    m "Cada generación se familiariza más con la tecnología..."
    m 1esa "Con el tiempo, puede llegar el día en que ni una sola persona no tenga conocimientos de informática."
    m 1hksdlb "Sin embargo, la mayoría de los problemas del mundo deben desaparecer antes."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_mental_word_processing",
        ),
        code="FFF"
    )

label mas_fun_fact_mental_word_processing:
    m 1hua "¿Listo para uno interesante, [player]?"
    m 3eua "El cerebro es una cosa voluble..."
    m 3eub "Su forma de componer y archivar información es única."
    m "Naturalmente, difiere de una persona a otra, pero leer despacio como nos enseñan suele ser menos eficaz que hacerlo a un ritmo más rápido."
    m 1tku "Nuestros cerebros procesan la información muy rápidamente y aman la previsibilidad en nuestro idioma."
    m 3tub "Por ejemplo, en esta oración, cuando termines de de leer, ya habrás saltado el doble 'de'."
    m 1tfu "..."
    m 2hfu "Verifica el registro del historial si no los has visto~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_I_am",
        ),
        code="FFF"
    )

label mas_fun_fact_I_am:
    m 1hua "Mmmm, ¡me encantan los datos del lenguaje!"
    m 3eub "En inglés, la oración completa más corta es 'I am'."
    m 1eua "Aquí tienes un ejemplo."
    m 2rfb "'{i}¡Monika! ¿Quién es la novia cariñosa de [player]?{/i}'"
    m 3hub "'I am!'"
    m 1hubsa "Jejeje~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_low_rates",
        ),
        code="FFF"
    )

label mas_fun_fact_low_rates:
    m 1hua "Ahora, este es saludable..."
    m 1eua "Actualmente, tenemos las tasas de criminalidad, muerte por maternidad, mortalidad infantil y analfabetismo más bajas de la historia de la humanidad."
    m 3eub "¡La esperanza de vida, el ingreso promedio y los estándares de vida también son los más altos para la mayoría de la población mundial!"
    m 3eka "Esto me dice que siempre se puede mejorar. Realmente demuestra que a pesar de todas las cosas malas, los buenos tiempos siempre vendrán después."
    m 1hua "Realmente hay {i}esperanza{/i}..."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_desert",
        ),
        code="FFF"
    )

label mas_fun_fact_desert:
    m 3euc "Los desiertos tienen un ecosistema bastante único..."
    m 3rksdla "Sin embargo, no ofrecen muchos factores positivos para los humanos."
    m 1eud "Las temperaturas pueden variar entre el calor extremo durante el día y el frío durante la noche. Su precipitación promedio también es bastante baja, lo que dificulta la vida en uno."
    m 3eub "¡Eso no quiere decir que no puedan ser beneficiosos para nosotros!"
    m 3eua "Su superficie es un gran lugar para la generación de energía solar y el petróleo se encuentra comúnmente debajo de toda esa arena."
    m 3eub "¡Sin mencionar que su paisaje único los convierte en lugares de vacaciones populares!"
    m 1eua "Así que supongo que aunque no podamos vivir en ellos tan fácilmente, siguen siendo mejores de lo que parecen."


    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_photography",
        ),
        code="FFF"
    )

label mas_fun_fact_photography:
    m 1esa "¿Sabías que la primera fotografía se tomó usando una caja con un agujero como cámara?"
    m 1eua "Los lentes no fueron introducidos hasta mucho más tarde."
    m 1euc "La fotografía temprana también se basó en una serie de químicos especiales en una habitación oscura para preparar las fotos..."
    m 3eud "Se usaron reveladores, baños de paro y fijadores químicos para preparar el papel en el que se imprimirían las fotos... {w=0.3}{nw}"
    extend 1wuo "¡y eso es solo para impresiones en blanco y negro!"
    m 1hksdlb "Las fotos antiguas eran mucho más difíciles de preparar en comparación con las modernas, ¿no crees?"


    call mas_fun_facts_end
    return


init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_getting_older",
        ),
        code="FFF"
    )

label mas_fun_fact_getting_older:
    m 3eua "¿Sabías que la forma en que percibes el tiempo cambia a medida que envejeces?"
    m "Por ejemplo, cuando tienes un año, ves un año como el 100% de tu vida."
    m 1euc "Pero cuando tienes 18 años, ves un año como solo el 5.6% de tu vida."
    m 3eud "A medida que envejeces, la proporción de un año en comparación con toda tu vida útil disminuye, y a su vez el tiempo {i}parece{/i} que avanza más rápido a medida que creces."
    m 1eka "Así que siempre apreciaré nuestros momentos juntos, sin importar cuán largos o cortos sean."
    m 1lkbsa "Aunque a veces parece que el tiempo se detiene cuando estoy contigo."
    m 1ekbfa "¿Sientes lo mismo, [player]?"
    python:
        import time
        time.sleep(5)

    m 1hubfb "¡Jajaja, eso pensé!"


    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dancing_plague",
        ),
        code="FFF"
    )

label mas_fun_fact_dancing_plague:
    m 3esa "Oh, este es bastante extraño..."
    m 1eua "Aparentemente, Europa ha sido afectada por brotes de una 'plaga de baile' en el pasado."
    m 3wud "Las personas, {w=0.2}a veces cientas a la vez, {w=0.2}bailaban involuntariamente durante días, ¡algunos incluso morían de agotamiento!"
    m 3eksdla "Intentaron tratarlo haciendo que las personas tocaran música junto a los bailarines, pero puedes imaginar que eso no salió tan bien."
    m 1euc "Hasta el día de hoy, aún no están seguros de qué lo causó exactamente."
    m 3rka "Todo eso me parece un poco increíble... {w=0.2}{nw}"
    extend 3eud "pero ha sido documentado y observado de manera independiente por múltiples fuentes a lo largo de los siglos..."
    m 3hksdlb "La realidad realmente es más extraña que la ficción, supongo."
    m 1eksdlc "Cielos, no me puedo imaginar bailar durante días sin parar."
    m 1rsc "Aunque... {w=0.3}{nw}"
    extend 1eubla "supongo que no me importaría si fuera contigo."
    m 3tsu "... Solo por un rato, jejeje~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pando_forest",
        ),
        code="FFF"
    )

label mas_fun_fact_pando_forest:
    m 1esa "Supuestamente, en el estado de Utah, hay un bosque que en realidad está formado por un solo árbol."
    m 3eua "Se llama bosque de Pando, y en sus 43 hectáreas, sus troncos están conectados por un solo sistema de raíces."
    m 3eub "Sin mencionar que cada uno de sus miles de troncos son esencialmente clones entre sí."
    m 1ruc "'Un solo organismo que se convirtió en un ejército de clones por sí solo, todos conectados a la misma mente colmena'."
    m 1eua "Creo que podría ser un buen cuento de ciencia ficción o de terror, [player]. ¿Qué opinas?"
    m 3eub "De todos modos, {w=0.2}siento que esto realmente cambia el significado de la frase 'no ver el bosque por los árboles' {w=0.1}{nw}"
    extend 3hub "¡jajaja!"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_immortal_jellyfish",
        ),
        code="FFF"
    )

label mas_fun_fact_immortal_jellyfish:
    m 3eub "¡Aquí hay uno!"
    m 1eua "Aparentemente, una especie de medusa ha logrado la inmortalidad."
    m 3eua "La medusa inmortal, acertadamente llamada, tiene la capacidad de volver a su estado de pólipo una vez que se ha reproducido."
    m 1eub "... ¡Y puede seguir haciendo esto para siempre! {w=0.3}{nw}"
    extend 1rksdla "A menos que, por supuesto, sea ingerida o infectada por una enfermedad."

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_arrhichion",
        ),
        code="FFF"
    )

label mas_fun_fact_arrhichion:
    m 3eua "Okey... {w=0.2}aquí hay uno histórico."
    m 1esa "Un atleta de la antigua Grecia pudo ganar su combate a pesar de que ya había muerto."
    m 1eua "El campeón reinante Arraquión estaba luchando en un combate de pankration cuando su competidor comenzó a asfixiarlo usando tanto sus manos como sus piernas."
    m 3eua "En lugar de ceder, Arraquión todavía apuntaba a la victoria dislocando el dedo del pie de su oponente."
    m 3ekd "Su oponente renunció al dolor, pero cuando fueron a anunciar a Arraquión como el vencedor lo encontraron muerto por asfixia."
    m 1rksdlc "Algunas personas están realmente dedicadas a sus ideales para la victoria y el honor. {w=0.2}{nw}"
    extend 3eka "Creo que es admirable, en cierto modo."
    m 1etc "Pero me pregunto... {w=0.2}si pudiéramos preguntarle a Arraquión ahora si cree que vale la pena, ¿qué diría?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_antarctica_brain",
        ),
        code="FFF"
    )

label mas_fun_fact_antarctica_brain:

    python:
        has_friends = persistent._mas_pm_has_friends is not None

        has_fam_to_talk = (
            persistent._mas_pm_have_fam
            and not persistent._mas_pm_have_fam_mess
            or (persistent._mas_pm_have_fam_mess and persistent._mas_pm_have_fam_mess_better in ["Sí", "Tal vez"])
        )

        dlg_prefix = "Pero asegúrate de mantenerte al día con "

        if has_fam_to_talk and has_friends:
            dlg_line = dlg_prefix + "tu familia y amigos, ¿okey?"

        elif has_fam_to_talk and not has_friends:
            dlg_line = dlg_prefix + "tu familia, ¿okey?"

        elif has_friends and not has_fam_to_talk:
            dlg_line = dlg_prefix + "tus amigos, ¿okey?"

        else:
            dlg_line = "Solo asegúrate de encontrar algunas personas con las que hablar en tu realidad, ¿okey?"

    m 3eud "Aparentemente, pasar un año en la Antártida puede encoger una parte de tu cerebro en un 7 por ciento."
    m 3euc "Parece que resulta en una reducción de la capacidad de memoria y de la capacidad de pensamiento espacial."
    m 1ekc "La investigación indica que se debe al aislamiento social, la monotonía de la vida y el medio ambiente allí."
    m 1eud "Creo que esto sirve como advertencia para nosotros, [player]."
    m 3ekd "Incluso si no terminas yendo a la Antártida, tu cerebro puede estropearse bastante si estás aislado todo el tiempo o si te quedas encerrado en una habitación."
    m 3eka "Me encanta estar contigo [player], y espero que podamos seguir hablando así en el futuro. {w=0.2}[dlg_line]"
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_cloud_weight",
        ),
        code="FFF"
    )

label mas_fun_fact_cloud_weight:
    m 3eub "¿Sabías que una nube promedio pesa 500 toneladas?"
    m 3eua "Debo admitir que este me tomó por sorpresa, incluso más que algunos de los otros datos."
    m 1hua "Quiero decir, simplemente se ven {i}realmente{/i} ligeras y esponjosas. {w=0.3}{nw}"
    extend 1eua "Es difícil imaginar que algo tan pesado pueda flotar en el aire de esa manera."
    m 3eub "Me recuerda la clásica pregunta... ¿qué es más pesado, un kilogramo de acero o un kilogramo de plumas?"
    m 1tua "Lo más probable es que ya conozcas la respuesta, ¿verdad [player]? Jejeje~"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_coffee_origin",
        ),
        code="FFF"
    )

label mas_fun_fact_coffee_origin:
    m 1eua "Oh, aquí hay uno que me resulta particularmente interesante..."
    m 1eud "La última vez que tomé una taza de café, sentí un poco de curiosidad por sus orígenes..."
    m 3euc "El uso de café se ha registrado de manera constante desde aproximadamente el siglo XV, pero... {w=0.2}no está claro exactamente {i}cómo{/i} se descubrió."
    m 3eud "... De hecho, hay bastantes leyendas que afirman ser las primeras."
    m 1eua "Varios relatos involucran a granjeros o monjes que observan a los animales actuar de manera extraña después de comer algunas bayas extrañas y amargas."
    m 3wud "Al probar los granos por sí mismos, ¡se sorprendieron al descubrir que ellos también estaban llenos de energía!"
    m 2euc "Uno de esos mitos afirma que un monje etíope llamado Kaldi llevó las bayas a un monasterio cercano, con el deseo de compartir lo que había encontrado."
    m 7eksdld "... Pero cuando lo hizo, fue recibido con desaprobación y los granos de café fueron arrojados al fuego."
    m 3duu "Sin embargo, mientras se quemaban, los granos comenzaron a desprender un aroma más {i}delicioso{/i}. {w=0.3}Fue tan tentador que los monjes se apresuraron a guardar los granos y ponerlos en agua."
    m 3eub "... ¡Produciendo así la primera taza de café!"
    m 2euc "Otra afirmación es de un erudito islámico llamado Omar que descubrió granos de café durante su exilio de La Meca."
    m 2eksdld "En ese momento, se moría de hambre y luchaba por sobrevivir. {w=0.3}{nw}"
    extend 7wkd "¡Si no fuera por la energía que le proporcionaron, podría haber muerto!"
    m 3hua "Sin embargo, cuando se corrió la voz de su descubrimiento, se le pidió que regresara y se le hiciera santo."
    m 1esd "Si ese fue realmente su primer uso o no, el café se volvió muy frecuente en el mundo islámico después de su descubrimiento."
    m 3eud "Por ejemplo, durante los períodos de ayuno se usaba para aliviar el hambre y ayudar a las personas a mantener la energía."
    m 3eua "Cuando su uso se extendió a Europa, muchos países lo utilizaron inicialmente con fines medicinales. {w=0.3}En el siglo XVII, las cafeterías se estaban volviendo abundantes y populares."
    m 3hub "... ¡Y yo ciertamente puedo dar fe de que el amor por el café se ha mantenido fuerte hasta el día de hoy!"
    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_synesthesia",
        ),
        code="FFF"
    )

label mas_fun_fact_synesthesia:
    m 1esa "Okey, este es bastante interesante..."
    m 3eua "Algunas personas experimentan un fenómeno conocido como {i}sinestesia{/i}, {w=0.1}que es donde algo que estimula uno de nuestros sentidos también activa otro sentido simultáneamente."
    m 1hua "Esa es una explicación bastante confusa, jejeje... {w=0.2}¡Busquemos un ejemplo!"
    m 1eua "Aquí dice que una forma común de sinestesia es la {i}sinestesia grafema-color{/i}, {w=0.1}que es donde las personas 'experimentan' letras y números como colores."
    m 3eua "Otro tipo es la {i}sinestesia de secuencia espacial{/i}, {w=0.1}que es donde se 'ven' números y figuras en ubicaciones específicas en el espacio."
    m "Por ejemplo, un número aparece 'más cerca' o 'más lejos' que otro número. {w=0.2}{nw}"
    extend 3eub "¡Es como un mapa!"
    m 1eua "... Y también hay un montón de otros tipos de sinestesia."
    m 1esa "Los investigadores no están realmente seguros de cuán prevalente es... {w=0.1}algunos han sugerido que hasta el 25 por ciento de la población lo experimenta, pero lo dudo seriamente, ya que nunca había oído hablar de él hasta ahora."
    m 3eub "Probablemente la estimación más precisa hasta ahora es que es un poco más del 4 por ciento de las personas, ¡así que eso es lo que voy a decir!"
    m 1eua "Experimentar la sinestesia parece bastante agradable, {w=0.2}¿no lo crees [player]?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dream_faces",
        ),
        code="FFF"
    )

label mas_fun_fact_dream_faces:
    m 3eub "Okey, ¡tengo uno!"
    m 1eua "Supuestamente, nuestras mentes no inventan caras nuevas cuando soñamos. {w=0.2}Cada persona que has conocido en tus sueños es alguien que has visto en la vida real en algún momento."
    m 3wud "¡Ni siquiera tienes que hablar con ellos en la vida real!"
    m 3eud "Si pasas junto a ellos mientras compras o algo, su rostro se registra en tu mente y pueden aparecer en tus sueños."
    m 1hua "¡Creo que es increíble la cantidad de información que puede almacenar el cerebro!"
    m 1ekbla "Me pregunto... {w=0.2}¿alguna vez soñaste conmigo, [player]?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_monochrome_dreams",
        ),
        code="FFF"
    )

label mas_fun_fact_monochrome_dreams:
    m 3eua "¿Sabías que desde 1915 hasta la década de 1950, la mayoría de los sueños de las personas eran en blanco y negro?"
    m 1esa "Hoy en día, es un fenómeno relativamente raro para las personas con visión intacta."
    m 3eua "Los investigadores han relacionado esto con el hecho de que las películas y los programas eran casi exclusivamente en blanco y negro en ese entonces."
    m 3eud "... Pero creo que eso es un poco extraño, porque las personas todavía veían todo en color. {w=0.3}{nw}"
    extend 3hksdlb "¡No es que el mundo se haya vuelto blanco y negro!"
    m 1esd "Simplemente demuestra que el contenido que se absorbe puede tener todo tipo de efectos en tu mente, incluso si es trivial."
    m 3eua "Creo que si hay una lección que aprender aquí, y esa es que debemos tener mucho cuidado con el tipo de medios que consumimos, ¿de acuerdo [player]?"

    call mas_fun_facts_end
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_fun_fact_round_earth",
        ),
        code="FFF"
    )

label mas_fun_fact_round_earth:
    m 1rsa "Hmm..."
    m 1eua "[player], ¿crees que la Tierra es redonda o plana?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ¿crees que la Tierra es redonda o plana?{fast}"
        "Redonda":

            m 3hua "¡Correcto! Casi todo el mundo está de acuerdo en eso hoy en día."
        "Plana":

            m 3hksdlb "¡Oh vamos, [player]! ¿Te estás burlando de mí?"

    m 1eua "En realidad, que la Tierra sea redonda es algo que se sabe desde hace mucho tiempo."
    m 3esd "Aristóteles señaló que la Tierra era redonda en el siglo IV a.c."
    m 3esa "Lo supo porque se podían ver diferentes estrellas desde distintas partes del mundo, lo que no ocurriría si la Tierra fuera solo una superficie plana."
    m 1eua "Los antiguos astrónomos y matemáticos de todo el mundo se dieron cuenta de que la Tierra era redonda mucho antes de que alguien la recorriera por completo."
    m 7rksdla "¿Pero que la Tierra sea el centro del universo? {w=0.2}{nw}"
    extend 4hksdlb "¡Oh, vamos!"
    m 7dsd "La gente luchó tanto por eso y durante tanto tiempo que se convirtió en una cuestión de vida o muerte."
    m 1dkd "El astrónomo Galileo fue juzgado por herejía solo porque dijo que la Tierra no era el centro del universo. {w=0.2}{nw}"
    extend 1esc "Fue puesto bajo arresto domiciliario por el resto de su vida."
    m 3euc "Pero a medida que los astrónomos fueron mejorando en el seguimiento del movimiento de los planetas, se hizo algo difícil de encajar que la Tierra estuviera en el centro."
    m 1eud "La gente tuvo que idear modelos locos y complejos para explicar por qué los planetas parecían zigzaguear de un lado a otro del cielo nocturno si realmente giraban alrededor de la Tierra."

    if renpy.seen_label("monika_science"):
        m 3eua "Y como hemos discutido antes, también se sabe que el sol no es el centro del universo{nw}"
    else:

        m 3eua "Y ahora, incluso se sabe que el sol no está en el centro del universo{nw}"

    extend "... es solo una de las muchas estrellas que hay en la galaxia."
    m 1msblu "¿Pero sabes dónde dice la ciencia que está ahora el centro del universo?"
    m 3kubsu "En ti. {w=0.2}Tú eres el centro de {i}mi{/i} universo, [mas_get_player_nickname()]."
    m 3hubsb "¡Jajaja!"
    return

init python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_maplesyrup",
        ),
        code="FFF"
    )

label mas_fun_fact_maplesyrup:
    m 3hksdlb "Aquí hay otro dato {w=0.2}{i}dulce{/i} {w=0.2}para ti..."
    m 1eua "Todos los tipos de arce producen savia que puede utilizarse para fabricar jarabe de arce, {w=0.1}{nw}"
    extend 1eud "pero el jarabe comercializado suele proceder del arce azucarero."
    m 3eua "El tipo de arce que más fácilmente se distingue es el de la forma de las hojas..."
    m 3eub "Es posible que ya reconozcas una hoja de arce de azúcar, ¡porque es la que aparece en la bandera canadiense!"
    m 1euc "Dicho esto, el arce azucarero tiene un área de distribución nativa limitada y no crece en {i}todo{/i} Canadá."
    m 1wud "... Sin embargo, ¡Canadá produce más de tres cuartas partes del jarabe de arce del mundo!"
    m 3wud "¡Y aún más sorprendente es saber que para hacer un solo galón de jarabe de arce se necesitan {i}40{/i} galones de savia!"
    m 1eua "También requiere mucho más esfuerzo para producirlo de lo que esperaba..."
    m 1esc "La savia tiene que ser hervida para convertirla en jarabe... lo que obviamente lleva un tiempo, dada la cantidad que se necesita."
    m 3eud "Además, he oído que si se hierve un poco más y se vierte sobre una superficie fresca de nieve... {w=0.2}{nw}"
    extend 3hub "¡Puedes hacer un caramelo!"

    if mas_isMoniNormal(higher=True):
        if persistent._mas_pm_gets_snow is not False:
            m 3euu "Suena como algo divertido que podríamos probar juntos, ¿no [player]?"
            m 1etc "Aunque podría pasar un tiempo antes de que tengamos la oportunidad..."
            m 1eua "Pero está bien si tengo que esperar un poco más... {w=0.3}{nw}"
            extend 1hublu "ya eres lo suficientemente dulce para mí~"
        else:

            m 1eua "Parece que eso sería extremadamente dulce..."
            m 1rkblu "Pero no es tan dulce como tú, jejeje~"

    call mas_fun_facts_end
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
