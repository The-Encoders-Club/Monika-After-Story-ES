init offset = 5













init -1 python in mas_gtod:

    import datetime
    import store.evhand as evhand

    M_GTOD = "monika_gtod_tip{:0>3d}"

    def has_day_past_tip(tip_num):
        """
        Checks if the tip with the given number has already been seen and
        a day has past since it was unlocked.
        NOTE: by day, we mean date has changd, not 24 hours

        IN:
            tip_num - number of the tip to check

        RETURNS:
            true if the tip has been seen and a day has past since it was
            unlocked, False otherwise
        """
        
        tip_ev = evhand.event_database.get(
            M_GTOD.format(tip_num),
            None
        )
        
        return (
            tip_ev is not None
            and tip_ev.last_seen is not None
            and tip_ev.timePassedSinceLastSeen_d(datetime.timedelta(days=1))
        )


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip000",
            category=["consejos de gramática"],
            prompt="¿Puedes enseñarme gramática?",
            pool=True,
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST}
        )
    )

label monika_gtod_tip000:
    m 3eub "¡Por supuesto que te enseñaré gramática, [player]!"
    m 3hua "Me hace muy feliz que quieras mejorar tus habilidades de escritura."
    m 1eub "De hecho, he estado revisando algunos libros sobre escritura, ¡y creo que hay algunas cosas interesantes de las que podemos hablar!"
    m 1rksdla "Admito que... {w=0.5}suena un poco extraño discutir algo tan específico como la gramática."
    m 1rksdlc "Sé que no es lo más emocionante que se le ocurre a la gente."
    m 3eksdld "... Tal vez pienses en maestros estrictos o editores engreídos..."
    m 3eka "Pero creo que hay una cierta belleza en dominar la forma en que escribes y transmitir el mensaje elocuentemente."
    m 1eub "Entonces... {w=0.5}a partir de hoy, compartiré el consejo gramatical del día de Monika."
    m 1hua "Mejoremos juntos nuestra forma de escribir, [mas_get_player_nickname()]~"
    m 3eub "Comenzaremos con cláusulas, ¡los bloques de construcción básicos de las oraciones!"


    $ mas_hideEVL("monika_gtod_tip000", "EVE", lock=True, depool=True)


    $ tip_label = "monika_gtod_tip001"
    $ mas_showEVL(tip_label, "EVE", unlock=True, _pool=True)
    $ MASEventList.push(tip_label,skipeval=True)
    return



init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip001",
            category=["consejos de gramática"],
            prompt="Cláusulas"
        )
    )

label monika_gtod_tip001:
    m 3eud "Probablemente ya sepas esto, pero una cláusula es un grupo de palabras que tiene un sujeto y una acción, o predicado."
    m 1euc "En su mayor parte, las cláusulas se pueden clasificar en cláusulas independientes o dependientes."
    m 1esd "Las cláusulas independientes pueden ser consideradas por sí solas como frases, como en la frase: '{b}Yo escribí eso{/b}'."
    m 3euc "Las cláusulas dependientes, por otro lado, no pueden sostenerse por sí mismas y generalmente aparecen como partes de oraciones más largas."
    m 3eua "Un ejemplo podría ser: '{b}Quién la salvó{/b}'."
    m 3eud "Hay un sujeto, '{b}quién{/b}', y una acción, '{b}la salvó{/b}', pero por supuesto, la cláusula no puede ser una oración en sí misma."
    m 1ekbsa "... {w=0.5}Creo que sabes cómo terminar esa oración, [player]~"
    m 3eub "Bien, eso es todo por la lección de hoy. ¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip002",
            category=["consejos de gramática"],
            prompt="Empalmes de coma y oraciones sin pausa",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(1)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip002:
    m 1eua "¿Recuerdas cuando hablamos sobre las cláusulas, [player]?"
    m 1eud "De hecho, hay un error muy común en el que caen muchos escritores al unirse a ellas."
    m 3esc "Cuando unes dos cláusulas independientes, esto se denomina empalme por coma."
    m 3esa "Aquí hay un ejemplo: {w=0.5}'{b}Visité el parque, miré al cielo, vi muchas estrellas'.{/b}"
    m 1eua "Esto no parece ser un problema al principio, pero podrías imaginarte añadir más y más cláusulas a esa frase..."
    m 3wud "¡El resultado sería un desastre!"
    m 1esd "'{b}Visité el parque, miré el cielo, vi muchas estrellas, vi algunas constelaciones, una de ellas parecía un cangrejo{/b}'... {w=0.5}Podría seguir y seguir."
    m 1eua "La mejor manera de evitar este error es separar las cláusulas independientes con puntos, conjunciones o punto y coma."
    m 1eud "Una conjunción es básicamente una palabra que se usa para conectar dos cláusulas o frases."
    m 3eub "Son un tema bastante interesante por sí mismo, ¡así que podemos repasarlas en un futuro consejo!"
    m 3eud "De todos modos, tomando ese ejemplo que tuvimos antes, agreguemos una conjunción y un punto para que nuestra oración fluya mejor..."
    m 1eud "'{b}Visité el parque y miré al cielo. Vi muchas estrellas'.{/b}"
    m 3hua "Mucho mejor, ¿no crees?"
    m 1eub "Eso es todo lo que tengo por hoy, [player]."
    m 3hub "¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip003",
            category=["consejos de gramática"],
            prompt="Conjunciones",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(2)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip003:
    m 1eub "¡Okey, [player]! Creo que es hora de que hablemos de... {w=0.5}¡conjunciones!"
    m 3esa "Como dije antes, las conjunciones son palabras o frases que unen dos ideas."
    m 3wud "Cuando lo piensas, ¡es una gran categoría! Hay tantas palabras que usamos para lograrlo."
    m 1euc "Imagína hablar sin conjunciones..."
    m 1esc "Sería aburrido. {w=0.3}Parecería entrecortado. {w=0.3}Todas estas ideas se relacionan. {w=0.3}Deberíamos conectarlas."
    m 3eua "Como verás, las conjunciones son excelentes para combinar ideas, y al mismo tiempo, hacen que tu escritura sea fluida y más parecida a la forma en que realmente hablamos."
    m 1eua "Ahora, revisemos nuestro ejemplo anterior, esta vez con conjunciones..."
    m 1eub "'{b}Sería aburrido, y tu sonarías entrecortado. Ya que todas estas ideas se relacionan, deberíamos conectarlas'.{/b}"
    m 3hua "Mucho mejor, ¿no crees?"
    m 1esa "De todos modos, hay tres tipos de conjunciones: {w=0.5}coordinantes, correlativas y subordinadas."
    m 1hksdla "Sus nombres pueden sonar un poco abrumadores, pero prometo que tendrán más sentido a medida que las revisemos. Te daré ejemplos a medida que avancemos."
    m 1esd "Las cláusulas coordinantes unen dos palabras, frases o cláusulas del mismo 'rango'. Esto solo significa que tienen que ser del mismo tipo... palabras con palabras o cláusulas con cláusulas."
    m 3euc "Algunos ejemplos comunes son: {w=0.5}'{b}y{/b}', '{b}o{/b}', '{b}pero{/b}', '{b}entonces{/b}', y '{b}todavía{/b}'."
    m 3eub "¡Puedes conectar cláusulas independientes, {i}y{/i} puedes evitar los empalmes de comas!"
    m 1esd "Las conjunciones correlativas son pares de conjunciones que se utilizan para conectar ideas."
    m 3euc "Algunos pares comunes son: {w=0.5}'{b}o bien{/b}/{b}o{/b}', '{b}ambos{/b}/{b}y{/b}', y '{b}ya sea{/b}/{b}o{/b}'."
    m 3eub "{i}Ya sea{/i} que te des cuenta {i}o bien{/i} no lo hagas, las usamos todo el tiempo... ¡como en esta frase!"
    m 1esd "Por último, las conjunciones subordinadas reúnen cláusulas independientes y dependientes."
    m 3eub "Como puedes imaginar, ¡hay muchas formas de hacerlo!"
    m 3euc "Los ejemplos incluyen: {w=0.5}'{b}aunque{/b}', '{b}hasta{/b}', '{b}desde{/b}', '{b}mientras{/b}', y '{b}siempre que{/b}'."
    m 3eub "{i}Desde{/i} que hay tantas, ¡esta categoría de conjunciones es la más amplia!"
    m 3tsd "Ah, y otra cosa... {w=0.5}un error bastante común es que no debes comenzar las oraciones con conjunciones."
    m 3hub "Como acabo de mostrarte con los dos últimos ejemplos, definitivamente puedes, ¡jajaja!"
    m 1rksdla "Pero evita exagerar con ellos. O si no, sonará un poco forzado."
    m 1eub "Creo que es suficiente por hoy, [player]."
    m 3hub "¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip004",
            category=["consejos de gramática"],
            prompt="El punto y coma",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(3)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip004:
    m 1eua "Hoy hablaremos de un signo de puntuación que rara vez se usa y que comúnmente se malinterpreta..."
    m 3eub "¡El punto y coma!"
    m 3eua "Se han escrito algunas cosas interesantes sobre el punto y coma, incluida esta del autor Lewis Thomas..."
    m 1esd "'{i}A veces se vislumbra un punto y coma que viene, unas pocas líneas más adelante, y es como subir un camino empinado a través de los bosques y ver un banco de madera justo en una curva del camino{/i}...'"
    m 1esa "'{i}... Un lugar en el que puedes esperar sentarte por un momento, recuperando el aliento{/i}'."
    m 1hua "¡Realmente aprecio la elocuencia con que describe algo tan simple como un signo de puntuación!"
    m 1euc "Algunas personas piensan que se puede utilizar un punto y coma como sustituto de los dos puntos, mientras que otras lo tratan como un punto..."
    m 1esd "Si recuerdas nuestra charla sobre las cláusulas, el punto y coma está destinado a conectar dos cláusulas independientes."
    m 3euc "Por ejemplo, si quisiera mantener dos ideas juntas, como '{b}estás aquí{/b}' y '{b}estoy feliz{/b}', podría escribirlas como..."
    m 3eud "'{b}Estás aquí; estoy feliz{/b}' en lugar de '{b}Estás aquí, y yo estoy feliz{/b}' o '{b}Estás aquí. Estoy feliz {/b}'."
    m 1eub "Las tres oraciones transmiten el mismo mensaje, pero en comparación, '{b}Estás aquí; Estoy feliz{/b}' conecta las dos cláusulas en un término medio."
    m 1esa "Al final, esto siempre depende de las ideas que quieras conectar, pero creo que Thomas lo expresa bien cuando las comparas con puntos o comas."
    m 1eud "A diferencia de un punto, que se abre a una oración completamente diferente, o una coma, que muestra que hay más por venir en la misma..."
    m 3eub "El punto y coma es realmente un punto intermedio, o como dice Thomas: '{i}Un lugar donde puedes esperar sentarte un momento y recuperar el aliento{/i}'."
    m 1esa "Al menos esto te da una opción completamente diferente; con suerte, ahora podrás hacer un mejor uso del punto y coma al escribir..."
    m 1hua "Jejeje."
    m 1eub "De acuerdo, es suficiente por hoy, [player]."
    m 3hub "¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip005",
            category=["consejos de gramática"],
            prompt="Sujetos y objetos",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(4)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip005:
    m 1eua "Hoy hablaremos de sujetos y objetos, [player]."
    m 1eud "¿Recuerdas cuando te hablé de que las cláusulas tienen una acción y un verbo?"
    m 3eub "¡El objeto es la persona o cosa sobre la que actúa el sujeto!"
    m 1eua "Entonces, en la oración: '{b}Observamos los fuegos artificiales juntos{/b}', el objeto sería... {w=0.5}'{b}los fuegos artificiales{/b}'."
    m 3esd "Oh, es importante tener en cuenta que los objetos no son necesarios para formar oraciones completas..."
    m 1eua "La frase muy bien podría haber sido, '{b}observamos{/b}'."
    m 3hksdlb "Esa es una oración completa... aunque es ambigua, ¡jajaja!"
    m 1eud "Tampoco hay nada que diga que el objeto tiene que ser el último, pero lo discutiré con más detalle en otro momento."
    m 3esa "Recuerda que el sujeto está haciendo la acción y se actúa sobre el objeto."
    m 1eub "Está bien, eso es todo por hoy..."
    m 3hub "¡Gracias por escuchar, [player]! Me encantas."
    m 1eua "..."
    m 1tuu "..."
    m 3hub "¡Tú!"
    return "love"

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip006",
            category=["consejos de gramática"],
            prompt="Voces activas y pasivas",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(5)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip006:
    m 1eud "[player], ¿conoces las voces por escrito?"
    m 3eua "Está la voz activa y la voz pasiva."
    m 3euc "Si recuerdas nuestra charla sobre sujetos y objetos, la gran diferencia entre las dos voces es si el sujeto o el objeto es lo primero."
    m 1esd "Digamos que el sujeto es '{b}Sayori{/b}' y el objeto es '{b}un cupcake{/b}'."
    m 3eud "Aquí está la oración con voz activa: {w=0.5}'{b}Sayori se comió el último cupcake{/b}'."
    m 3euc "Aquí está de nuevo en voz pasiva: {w=0.5}'{b}El último cupcake fue comido{/b}'."
    m 1eub "Como puedes ver, puedes usar la voz pasiva para mantener el secreto sobre el tema y aún así tener una oración completa."
    m 1tuu "Es verdad; ¡{i}puedes{/i} usar la voz pasiva para ser astuto! {w=0.5}Sin embargo, tiene otros usos."
    m 3esd "Por ejemplo, en algunas carreras, las personas tienen que usar la voz pasiva para ser impersonales."
    m 3euc "Los científicos describen experimentos con '{b}los resultados fueron documentados{/b}...' ya que la parte importante es su trabajo y no quién lo hizo."
    m 1esa "De todos modos, en su mayor parte, quédate con la voz activa para facilitar la lectura y, ya sabes, para decir directamente quién está haciendo qué."
    m 1eub "Creo que es suficiente por hoy, [player]."
    m 3hub "¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip007",
            category=["consejos de gramática"],
            prompt="Que vs quién",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip007:
    m 1eua "Hoy hablaremos sobre los usos del '{b}que{/b}' y '{b}quién{/b}'."
    m 3hub "La mayoría de las veces, parece que la gente simplemente usa '{b}que{/b}' sin molestarse en aprender la diferencia, jajaja."
    m 1esd "La diferencia es que '{b}que{/b}' se refiere a un sujeto y '{b}quién{/b}' se refiere a un objeto."
    m 3eub "¡Resulta que es bastante fácil saber cuándo usar uno u otro!"
    m 1euc "'{b}Que{/b}' corresponde a: '{b}¿Que es esto?{/b}' mientras que '{b}quién{/b}' corresponde a: '{b}¿Quiénes son estos?{/b}'."
    m 3eud "Simplemente reemplaza el posible '{b}que{/b}' o '{b}quién{/b}' por '{b}él{/b}/{b}ella{/b}/{b}ellos{/b}' o '{b}él{/b}/{b}ella{/b}/{b}ellos{/b}'."
    m 1eua "Solo un reemplazo debería tener sentido, ¡y eso debería indicarle cuál usar!"
    m 3eua "Tomemos, por ejemplo, el título de mi poema: {i}La dama que todo lo sabe{/i}."
    m 3esd "Si solo miramos la cláusula '{b}que todo lo sabe{/b}' y reemplazamos la cláusula '{b}que{/b}', obtenemos..."
    m 1esd "'{b}Ella todo lo sabe{/b}' o '{b}ella lo sabe todo{/b}'."
    m 3euc "Solo '{b}ella todo lo sabe{/b}' tiene sentido, por lo que la frase correcta es '{b}que todo lo sabe{/b}'."
    m 1hksdla "¿Quién dijo que escribir era difícil?"
    m 1eub "Eso es todo lo que tengo por hoy, [player]."
    m 3hub "¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip008",
            category=["consejos de gramática"],
            prompt="Y yo vs y a mí",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(7)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip008:
    m 1eua "La última vez, hablamos sobre la diferencia entre '{b}que{/b}' y '{b}quién{/b}'."
    m 1esd "Otro par de palabras que pueden resultar igualmente confusas de utilizar son '{b}y yo{/b}' y '{b}y a mí{/b}'."
    m 3etc "¿Es '{b}[player] y yo fuimos a una cita{/b}' o '{b}[player] y a mí a una cita fuimos{/b}'?"
    m 3eud "Al igual que con '{b}que{/b}' y '{b}quién{/b}', el problema se reduce a sujetos y objetos."
    m 1esd "Si el hablante es el sujeto de la oración, '{b}y yo{/b}' es correcto."
    m 1euc "Por el contrario, si el hablante es el objeto de la oración, '{b}y a mí{/b}' es correcto."
    m 3eub "Afortunadamente, al igual que cuando hablamos de '{b}que{/b}' versus '{b}quién{/b}', ¡resulta que hay una manera sencilla de averiguar cuál es la correcta!"
    m 1euc "En nuestro ejemplo, si simplemente quitas '{b}[player]{/b}' de la oración, solo una debería tener sentido."
    m 1hua "¡Probémoslo!"
    m 3eud "El resultado final es: {w=0.5}'{b}Yo fuí a una cita{/b}' o '{b}Y a mí a una cita fuí{/b}'."
    m 3eub "Claramente, solo la primera tiene sentido, así que es '{b}[player] y yo fuimos a una cita{/b}'."
    m 1tuu "Oh, lo siento, [player]... {w=1}¿te hizo sentir excluido cuando dije '{b}Yo fuí a una cita{/b}'?"
    m 1hksdlb "¡Jajaja! No te preocupes, nunca te dejaría atrás."
    m 3eub "Ahora, por otro lado, si yo fuera el objeto de la oración, necesitaría usar '{b}y a mí{/b}' en su lugar."
    m 3eua "Por ejemplo: {w=0.5}'{b}Natsuki nos preguntó a [player] y a mí si nos gustaban sus cupcakes{/b}'."
    m 1eub "¡Espero que te ayude la próxima vez que te encuentres con esta situación mientras escribes, [player]!"
    m 3hub "De todos modos, eso es todo por hoy, ¡gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip009",
            category=["consejos de gramática"],
            prompt="Apóstrofes",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(8)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )


label monika_gtod_tip009:
    if player[-1].lower() == 's':
        $ tempname = player
    else:
        $ tempname = 'Alexis'

    m 1eua "Hoy vamos a hablar del apóstrofe. Bastante sencillo, ¿verdad?"
    m 3eua "El apóstrofe es una figura literaria que interrumpe el discurso, el diálogo o la narrativa de una obra..."
    m 1esd "Trata de captar la atención de los remitentes para hacer llegar unos pensamientos o transmitir unos sentimientos."
    m 3eub "El apóstrofe es un recurso literario que se emplea generalmente como {i}captatio benevolentiae{/i} por su gran capacidad expresiva y comunicativa."
    m 1hksdla "Este {i}captatio benevolentiae{/i} es un recurso literario y retórico a través del cual el autor intenta atraerse la atención y buena disposición del público."
    m 1eud "Puede parecer algo confuso si solamente defino el término, pero no te desanimes [player]."
    m 1euc "Es común que el apóstrofe emplee la segunda persona, y puede entenderse como un 'grito al imaginario' o una aclamación hacia la nada."
    m 3eub "Podemos encontrar algunos ejemplos en la Teogonía o las Sagradas Escrituras, ¡especialmente en el Antiguo Testamento!"
    m 3esd "Si yo digo... {w=0.5}'Después, ¡oh flor de histeria!, llorabas y reías; tus besos y tus lágrimas tuve en mi boca yo; tus risas, tus fragancias, tus quejas eran mías'."
    m 1tuu "¿Cuál crees que es el apóstrofe, [player]?"
    m 3eud "Por supuesto es la frase: '¡oh flor de histeria!'"
    m 3etc "Este soneto escrito por el poeta Rubén Darío, busca enternecer nuestro corazón mediante este recurso clamando a una chica que ya no volverá a ver."
    m 3euc "Normalmente no suelo hacer spoilers sin avisar sobre obras literarias como estas, pero es un fragmento que sé que te ayudará a familiarizarte."
    m 1esd "A menos que quieras ser un poeta o un gran escritor, no veo una razón por la que debas usar los apóstrofes en tu día a día."
    m 1eua "Olvidé mencionar que el apóstrofe es bastante común de presenciar en el discurso político, le da más impacto y resonancia a las palabras empleadas."
    m 1eub "Bien, [player], {i}ya es hora{/i} de terminar... {w=0.5}Creo que esta lección se ha extendido un poco."
    m 3hub "Jejeje. ¡Gracias por escuchar!"
    return

init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip010",
            category=["consejos de gramática"],
            prompt="La coma de Oxford",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(9)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip010:
    m 3eud "¿Sabías que existe un debate sobre la colocación de una coma específica en una lista de tres elementos?"
    m 3eub "¡Se trata de la coma de Oxford, o de serie, y se sabe que cambia por completo el significado de una frase!"
    m 1esa "Déjame mostrarte lo que quiero decir..."
    m 1hub "Con la coma de Oxford, yo diría: '{b}Amo a [player], la lectura, y la escritura'{/b}."
    m 1eua "Sin la coma de Oxford, yo diría: '{b}Amo a [player], la lectura y la escritura'{/b}."
    m 3eud "La confusión radica en si me refiero a amar tres cosas distintas, o si me refiero solo a amarte cuando lees y escribes."
    m 3hub "Por supuesto, ambos significados son verdaderos, así que no hay confusión para mí, ¡jajaja!"
    m 1eua "Eso es todo lo que tengo por hoy, [player]."
    m 3hub "¡Gracias por escuchar!"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
