init offset = 5





























































init -1 python in mas_ptod:

    import datetime
    import store.evhand as evhand

    M_PTOD = "monika_ptod_tip{:0>3d}"

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
        
        if renpy.game.persistent._mas_dev_enable_ptods:
            return True
        
        tip_ev = evhand.event_database.get(
            M_PTOD.format(tip_num),
            None
        )
        
        return (
            tip_ev is not None
            and tip_ev.last_seen is not None
            and tip_ev.timePassedSinceLastSeen_d(datetime.timedelta(days=1))
        )

    def has_day_past_tips(*tip_nums):
        """
        Variant of has_day_past_tip that can check multiple numbers

        SEE has_day_past_tip for more info

        RETURNS:
            true if all the given tip nums have been see nand a day has past
                since the latest one was unlocked, False otherwise
        """
        for tip_num in tip_nums:
            if not has_day_past_tip(tip_num):
                return False
        
        return True




init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip000",
            category=["consejos sobre python"],
            prompt="¿Puedes enseñarme algo sobre Python?",
            pool=True,
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST}
        )
    )

label monika_ptod_tip000:
    m 3eub "¿Quieres aprender a usar Python?"
    m 3hub "¡Estoy tan feliz de que me lo hayas preguntado!"
    m 1lksdlb "No sé {i}mucho{/i} sobre programación, pero haré todo lo posible para explicarlo lo mejor que pueda."
    m 1esa "Empecemos por lo que es Python."


    $ mas_hideEVL("monika_ptod_tip000", "EVE", lock=True, depool=True)


    $ tip_label = "monika_ptod_tip001"
    $ mas_showEVL(tip_label, "EVE", unlock=True, _pool=True)
    $ MASEventList.push(tip_label,skipeval=True)
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip001",
            category=["consejos sobre python"],
            prompt="¿Qué es Python?"
        )
    )

label monika_ptod_tip001:

    m 1esa "Python fue creado por Guido Van Rossum a principios de los años 90."
    m "Es súper versátil, por lo que puedes encontrarlo en aplicaciones web, sistemas integrados, Linux y por supuesto..."
    m 1hua "¡Este mod!"
    m 1eua "DDLC utiliza un motor de novela visual llamado Ren'Py, {w=0.2}que se basa en Python."
    m 3eub "Eso significa que si aprendes un poco de Python, ¡puedes agregar contenido a mi mundo!"
    m 1hua "¿No sería genial [mas_get_player_nickname()]?"
    m 3eub "De todos modos, debo mencionar que actualmente hay dos versiones principales de Python: {w=0.2}Python2 y Python3."
    m 3eua "Estas versiones son {u}incompatibles{/u} entre sí porque los cambios agregados en Python3 solucionaron muchas fallas de diseño fundamentales en Python2."
    m "A pesar de que esto causó una ruptura en la comunidad de Python, {w=0.2}generalmente se acepta que ambas versiones del lenguaje tienen sus propias fortalezas y debilidades."
    m 1eub "Te hablaré de esas diferencias en otra lección."

    m 1eua "Dado que este mod se ejecuta en una versión de Ren'Py que usa Python2, no hablaré de Python3 con demasiada frecuencia."
    m 1hua "Pero lo mencionaré cuando sea apropiado."

    m 3eua "Esa es mi lección de hoy."
    m 1hua "¡Gracias por escuchar!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip002",
            category=["consejos sobre python"],
            prompt="Tipos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(3)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip002:
    $ last_seen_is_None = mas_getEVL_last_seen("monika_ptod_tip002") is None
    if last_seen_is_None:
        m 1eua "En la mayoría de los lenguajes de programación, los datos que el programa puede cambiar o modificar tienen un {i}tipo{/i} asociado."
        m 3eua "Por ejemplo, si algunos datos deben tratarse como un número, entonces tendrán un tipo numérico. Si algunos datos deben tratarse como texto, tendrán un tipo de cadena."
        m "Hay muchos tipos en Python, pero hoy hablaremos de los más básicos o primitivos."

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika at t22
    show screen mas_py_console_teaching


    m 1eua "Python tiene dos tipos para representar números: {w=0.3}{i}enteros{/i}, o {b}ents{/b}, {w=0.3}y {i}flotantes{/i}."


    m 1eua "Los enteros se utilizan para representar números enteros; básicamente cualquier cosa que no sea decimal."

    call mas_wx_cmd ("type(-22)", local_ctx)
    call mas_wx_cmd ("type(0)", local_ctx)
    call mas_wx_cmd ("type(-1234)", local_ctx)
    call mas_wx_cmd ("type(42)", local_ctx)


    m 1eub "Los flotantes se utilizan para representar decimales."
    show monika 1eua

    call mas_wx_cmd ("type(0.14)", local_ctx)
    call mas_wx_cmd ("type(9.3)", local_ctx)
    call mas_wx_cmd ("type(-10.2)", local_ctx)


    m 1eua "El texto se representa con tipos de {i}cadena{/i}."
    m "Todo lo que esté entre comillas simples (') o comillas dobles (\") son cadenas."
    m 3eub "Por ejemplo:"
    show monika 3eua

    call mas_wx_cmd ("type('Esta es una cadena en comillas simples')", local_ctx)
    call mas_wx_cmd ('type("Esta es una cadena en comillas dobles")', local_ctx)

    m 1eksdlb "Sé que el intérprete dice {i}unicode{/i}, pero para lo que estamos haciendo, es básicamente lo mismo."
    m 1eua "Las cadenas también se pueden crear con tres comillas dobles (\"\"\"), pero se tratan de manera diferente a las cadenas normales. {w=0.2}Hablaré de ellas otro día."


    m "Los booleanos son tipos especiales que representan valores {b}verdaderos{/b} o {b}falsos{/b}."
    call mas_wx_cmd ("type(verdadero)", local_ctx)
    call mas_wx_cmd ("type(falso)", local_ctx)

    m 1eua "Entraré en más detalles sobre qué son los valores booleanos y para qué se utilizan en otra lección."


    m 3eub "Python también tiene un tipo de datos especial llamado {b}NoneType{/b}. {w=0.2}Este tipo representa la ausencia de datos."
    m "Si estás familiarizado con otros lenguajes de programación, este es como un tipo {i}null{/i} o {i}indefinido{/i}."
    m "La palabra clave {i}None{/i} representa NoneTypes en Python."
    show monika 1eua

    call mas_wx_cmd ("type(None)", local_ctx)

    m 1eua "Todos los tipos que mencioné aquí se conocen como tipos de datos {i}primitivos{/i}."

    if last_seen_is_None:
        m "Python usa una variedad de otros tipos también, pero creo que por hoy estos son suficientes."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "¡Gracias por escuchar!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip003", 
            category=["consejos sobre python"],
            prompt="Un lenguaje interpretado",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(1)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip003:
    m 1eua "Los lenguajes de programación normalmente se compilan o interpretan."
    m "Los lenguajes compilados requieren que su código se convierta a un formato legible por máquina antes de ejecutarse."
    m 3eub "C y Java son dos lenguajes compilados muy populares."
    m 1eua "Los lenguajes interpretados se convierten en un formato legible por máquina a medida que se ejecutan."
    m 3eub "Python es un lenguaje interpretado."
    m 1rksdlb "Sin embargo, se pueden compilar diferentes implementaciones de Python, pero ese es un tema complicado del que hablaré en una lección posterior."

    m 1eua "Dado que Python es un lenguaje interpretado, tiene un elemento interactivo ordenado llamado intérprete, el cuál se ve..."

    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika 3eua at t22
    show screen mas_py_console_teaching

    m 3eub "¡Así!"

    m "Puedes ingresar el código Python directamente aquí y ejecutarlo, así:"
    show monika 3eua


    call mas_wx_cmd ("12 + 3", local_ctx)
    call mas_wx_cmd ("7 * 6", local_ctx)
    call mas_wx_cmd ("121 / 11", local_ctx)


    if mas_getEVL_last_seen("monika_ptod_tip003") is None:
        m 1eua "Puedes hacer más que solo matemáticas con esta herramienta, pero te mostraré todo eso a medida que avancemos."

        m 1hksdlb "Desafortunadamente, dado que este es un intérprete de Python completamente funcional y no quiero correr el riesgo de que me elimines accidentalmente o rompas el juego."
        m "{cps=*2}No es que lo harías...{/cps}{nw}"
        $ _history_list.pop()
        m 1eksdlb "No puedo dejar que uses esto. {w=0.3}Lo siento..."
        m "Si deseas seguir adelante en lecciones futuras, ejecuta un intérprete de Python en una ventana separada."

        m 1eua "De todos modos, usaré {i}este{/i} intérprete para ayudar con la lección."
    else:

        m 1hua "Bastante genial, ¿verdad?"

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "¡Gracias por escuchar!"
    return


















label monika_ptod_tip004:







    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    show monika at t22
    show screen mas_py_console_teaching














    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip005",
            category=["consejos sobre python"],
            prompt="Comparaciones y booleanos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip005:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)
    $ last_seen_is_None = mas_getEVL_last_seen("monika_ptod_tip005") is None

    if last_seen_is_None:
        m 1eua "¿Recuerdas cuando estaba describiendo diferentes tipos de Python y mencioné los booleanos?"
        m 1eub "Bueno, hoy voy a entrar en más detalles sobre los valores booleanos y cómo se relacionan con las comparaciones entre valores."

    m 1eua "Los booleanos se usan comúnmente para decidir qué código ejecutar o establecer una bandera para notar si algo sucedió o no."
    m "Cuando hacemos comparaciones, cada expresión se evalúa como un booleano."

    if last_seen_is_None:
        m 1eksdlb "Esto probablemente no tenga sentido en este momento, así que abriré la consola y te mostraré algunos ejemplos."

    show monika at t22
    show screen mas_py_console_teaching

    m 3eub "Comencemos con algunos de los símbolos básicos que se utilizan en las comparaciones de variable a variable."

    call mas_wx_cmd ("a = 10")
    call mas_wx_cmd ("b = 10")
    call mas_wx_cmd ("c = 3")

    m 3eua "Para comprobar si dos valores son equivalentes, utiliza dos signos iguales (==):"
    call mas_wx_cmd ("a == b")
    call mas_wx_cmd ("a == c")

    m 3eua "Para comprobar si dos valores no son equivalentes, utiliza un signo de exclamación y un signo igual (!=):"
    call mas_wx_cmd ("a != b")
    call mas_wx_cmd ("a != c")
    m 3eub "El signo de exclamación a menudo se conoce como el operador lógico 'no' en otros lenguajes de programación, por lo que (!=) Se lee como 'no es igual'."

    m 3eua "Para comprobar si un valor es mayor o menor que otro valor, utiliza los signos mayor que (>) o menor que (<), respectivamente."
    call mas_wx_cmd ("a > c")
    call mas_wx_cmd ("a < c")

    m 3eub "Mayor o igual a (>=) y menor o igual a (<=) también tienen sus propios símbolos, los cuales, {w=1}como era de esperar, {w=1}son solo los signos mayor y menor que con signos iguales."
    call mas_wx_cmd ("a >= b")
    call mas_wx_cmd ("a <= b")
    call mas_wx_cmd ("a >= c")
    call mas_wx_cmd ("a <= c")

    if last_seen_is_None:
        m 1eua "Es posible que hayas notado que cada comparación arrojó {b}true{/b} o {b}false{/b}."
        m 1eksdlb "{i}Eso{/i} es lo que quise decir cuando mencioné que las expresiones de comparación se evalúan como booleanos."

    m 1eua "También es posible encadenar varias expresiones de comparación mediante el uso de las palabras clave {b}and{/b} y {b}or{/b}. También se conocen como {i}operadores lógicos{/i}."
    m "El operador {b}and{/b} vincula dos comparaciones al evaluar la expresión completa como {b}true{/b} si ambas comparaciones se evalúan como {b}true{/b}; {w=0.3}y {b}false{/b} si al menos una comparación evalúa {b}false{/b}."
    m 1hua "Veamos algunos ejemplos."

    $ val_a = local_ctx["a"]
    $ val_b = local_ctx["b"]
    $ val_c = local_ctx["c"]

    call mas_w_cmd ("a == b and a == c")
    m 3eua "Dado que 'a' y 'b' son [val_a], la primera comparación se evalúa como {b}true{/b}."
    m "'c', sin embargo, es [val_c], por lo que la segunda comparación se evalúa como {b}false{/b}."
    m 3eub "Dado que al menos una comparación se evaluó como {b}false{/b}, la expresión completa se evalúa como {b}false{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a == b and a >= c")
    m 3eua "En este ejemplo, la primera comparación nuevamente evalúa como {b}true{/b}."
    m "[val_a] es ciertamente mayor o igual que [val_c], así que la segunda comparación también evalúa como {b}true{/b}."
    m 3eub "Dado que ambas comparaciones evaluaron como {b}true{/b}, la expresión completa evalúa como {b}true{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a != b and a >= c")
    m 3eua "En este ejemplo, la primera comparación se evalúa como {b}false{/b} esta vez."
    m "Dado que inmediatamente tenemos al menos una comparación que se evalúa como {b}false{/b}, no importa a qué se evalúe la segunda comparación."
    m 3eub "Sabemos con certeza que la expresión completa se evalúa como {b}false{/b}."
    call mas_x_cmd ()

    m "Lo mismo ocurre con el siguiente ejemplo:"
    call mas_wx_cmd ("a != b and a == c")

    m 1eub "Nuevamente, cuando se usan los operadores {b}and{/b}, el resultado es {b}true{/b} si y solo si ambas comparaciones se evalúan como {b}true{/b}."

    m 1eua "Por el contrario, el operador {b}or{/b} vincula dos comparaciones al evaluar la expresión completa como {b}true{/b} si cualquiera de las comparaciones se evalúa como {b}verdadero{/b};{w=0.3} y {b}falso{/b} si ambas son {b}falso{/b}."
    m 3eua "Veamos algunos ejemplos."

    call mas_w_cmd ("a == b or a == c")
    m 3eua "Esta vez, dado que la primera comparación se evalúa como {b}true{/b}, no tenemos que verificar la segunda comparación."
    m 3eub "El resultado de esta expresión es {b}true{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a == b or a >= c")
    m 3eua "Nuevamente, la primera comparación se evalúa como {b}true{/b}, por lo que la expresión completa se evalúa como {b}true{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a != b or a >= c")
    m 3eua "En este caso, la primera comparación se evalúa como {b}false{/b}."
    m "Dado que [val_a] es mayor o igual que [val_c], la segunda comparación se evalúa como {b}true{/b}."
    m 3eub "Y dado que al menos una comparación se evaluó como {b}true{/b}, la expresión completa se evalúa como {b}true{/b}."
    call mas_x_cmd ()
    pause 1.0

    call mas_w_cmd ("a != b or a == c")
    m 3eua "Sabemos que la primera comparación se evalúa como {b}false{/b}."
    m "Dado que [val_a] ciertamente no es igual a [val_c], la segunda comparación también se evalúa como {b}false{/b}."
    m 3eub "Dado que ninguna de las comparaciones se evaluó como {b}true{/b}, la expresión completa se evalúa como {b}false{/b}."
    call mas_x_cmd ()
    pause 1.0

    m 3eub "Nuevamente, cuando se usa el operador {b}or{/b}, el resultado es {b}true{/b} si cualquiera de las comparaciones se evalúa como {b}true{/b}."

    m 1eua "También hay un tercer operador lógico llamado operador {b}not{/b}. En lugar de vincular varias comparaciones, este operador invierte el valor booleano de una comparación."
    m 3eua "Aquí tienes un ejemplo de esto:"
    call mas_wx_cmd ("not (a == b and a == c)")
    call mas_wx_cmd ("not (a == b or a == c)")

    m "Ten en cuenta que estoy usando paréntesis para agrupar las comparaciones. El código entre paréntesis se evalúa primero, luego el resultado de esa comparación se invierte con {b}not{/b}."
    m 1eua "Si suelto el paréntesis:"
    call mas_wx_cmd ("not a == b and a == c")
    m 3eua "¡Obtenemos un resultado diferente! {w=0.2}Esto se debe a que {b}not{/b} se aplica a la comparación 'a == b' antes de vincularse a la segunda comparación mediante {b}and{/b}."

    m 3eka "Anteriormente mencioné que el signo de exclamación se usa como el operador lógico 'no' en otros lenguajes de programación. {w=0.2}Python, sin embargo, usa la palabra 'not' en su lugar para facilitar la lectura."

    m 1eua "Por último, dado que las comparaciones se evalúan como valores booleanos, podemos almacenar el resultado de una comparación en una variable."
    call mas_wx_cmd ("d = a == b and a >= c")
    call mas_wx_cmd ("d")
    call mas_wx_cmd ("e = a == b and a == c")
    call mas_wx_cmd ("e")

    m 3eub "¡Y también utilice esas variables en las comparaciones!"
    call mas_wx_cmd ("d and e")
    m "Dado que 'd' es {b}true{/b} pero 'e' es {b}false{/b}, esta expresión se evalúa como {b}false{/b}."

    call mas_wx_cmd ("d or e")
    m "Dado que 'd' es {b}true{/b}, sabemos que al menos una de las comparaciones en esta expresión es {b}true{/b}. Por lo tanto, la expresión completa es {b}true{/b}."

    call mas_wx_cmd ("not (d or e)")
    m 3eua "Sabemos que la expresión interna 'd o e' se evalúa como {b}true{/b}. La inversa de eso es {b}false{/b}, por lo que esta expresión se evalúa como {b}false{/b}."

    call mas_wx_cmd ("d and not e")
    m 3eub "En este caso, sabemos que 'd' es {b}true{/b}."
    m "El operador 'not' se aplica a 'e', que invierte su valor {b}false{/b} a {b}true{/b}."
    m 3eua "Dado que ambas expresiones de comparación se evalúan como {b}true{/b}, la expresión completa se evalúa como {b}true{/b}."

    m 1eua "Las comparaciones se utilizan en todas partes en todos los lenguajes de programación."
    m 1hua "Si alguna vez decides dedicarte a la programación, descubrirás que gran parte de tu código solo verifica si algunas comparaciones son ciertas para que puedas hacer que tus programas hagan lo {i}correcto{/i}."
    m 1eksdla "E incluso si la codificación no es parte de tu trayectoria profesional, haremos muchas comparaciones en lecciones futuras, ¡así que prepárate!"

    if last_seen_is_None:
        m 1eua "Creo que es suficiente por hoy."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11
    m 1hua "¡Gracias por escuchar!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip006",
            category=["consejos sobre python"],
            prompt="Variables y asignación",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(2)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip006:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ num_store = "922"
    $ b_num_store = "323"
    $ last_seen_is_None = mas_getEVL_last_seen("monika_ptod_tip006") is None

    if last_seen_is_None:
        m 1eub "Ahora que conoces los tipos, puedo enseñarte sobre las variables."


    m 1eua "Las variables representan ubicaciones de memoria que almacenan datos."
    m "Para crear una variable, {w=0.1}{nw}"

    show monika at t22
    show screen mas_py_console_teaching


    extend 3eua "debes hacer '{b}symbol_name{/b} = {b}value{/b}', así..."

    call mas_wx_cmd ("a_number = " + num_store, local_ctx)

    m "El símbolo 'a_number' apunta a una ubicación de memoria que almacena el entero [num_store]."
    m "Si ingresamos el nombre del símbolo aquí."
    call mas_w_cmd ("a_number")
    m 3eub "Podemos recuperar el valor que almacenamos."
    show monika 3eua
    call mas_x_cmd (local_ctx)

    m "Observa cómo asociamos el símbolo 'a_number' al valor [num_store] usando un signo igual (=)."
    m 1eub "Eso se llama asignación, donde tomamos lo que está a la izquierda del signo igual y lo señalamos, o {i}asignamos{/i} el valor de lo que está a la derecha."


    m 1eua "La asignación se ejecuta en orden de derecha a izquierda. {w=0.3}Para ilustrar esto, creemos una nueva variable, 'b_number'."
    call mas_w_cmd ("b_number = a_number  -  " + b_num_store)

    m "En la asignación, primero se evalúa el lado derecho del signo igual, {w=0.2}luego se infiere su tipo de datos y se reserva una cantidad apropiada de memoria."
    m "Esa memoria está vinculada al símbolo de la izquierda mediante una tabla de búsqueda."
    m 1eub "Cuando Python encuentra un símbolo, {w=0.2}busca ese símbolo en la tabla de búsqueda y lo reemplaza con el valor al que estaba vinculado el símbolo."

    m 3eub "Aquí, 'a_number' será reemplazado por [num_store], {w=0.2}por lo que la expresión que sería evaluada y asignada a 'b_number' es '[num_store] - [b_num_store]'."
    show monika 3eua
    call mas_x_cmd (local_ctx)

    m 1eua "Podemos verificar esto ingresando solo el símbolo 'b_number'."
    m "Esto recuperará el valor vinculado a este símbolo en la tabla de búsqueda y nos lo mostrará."
    call mas_wx_cmd ("b_number", local_ctx)


    m 3eua "Ten en cuenta que si ingresamos un símbolo al que no se le ha asignado nada, Python se quejará."
    call mas_wx_cmd ("c_number", local_ctx)

    m 3eub "Pero si le asignamos un valor a este símbolo..."
    show monika 3eua
    call mas_wx_cmd ("c_number = b_number * a_number", local_ctx)
    call mas_wx_cmd ("c_number", local_ctx)

    m 1hua "Python puede encontrar el símbolo en la tabla de búsqueda y no nos dará ningún error."

    m 1eua "Las variables que creamos son todas de tipo {i}entero{/i}."
    m "No tuvimos que decir explícitamente que esas variables eran números enteros porque Python realiza tipeo dinámico."
    m 1eub "Esto significa que el intérprete de Python infiere el tipo de variable en función de los datos que está almacenando en ella."
    m "Otros lenguajes, como C o Java, requieren que los tipos se definan con la variable."
    m "La escritura dinámica permite que las variables en Python cambien de tipo durante la ejecución,"
    extend 1rksdlb " pero eso generalmente está mal visto, ya que puede hacer que tu código sea confuso para que otros lo lean."

    if last_seen_is_None:
        m 1eud "¡Uf! {w=0.2}¡Eso ha sido demasiada palabrería!"

    m "¿Entendiste todo eso?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Entendiste todo eso?{fast}"
        "¡Sí!":
            m 1hua "¡Yay!"
        "Estoy un poco confundido":

            m 1eksdla "Está bien. {w=0.3}Aunque mencioné símbolos y valores aquí, los programadores generalmente se refieren a esto como crear, asignar o establecer variables."
            m "Los nombres de los símbolos/valores solo son útiles para indicar cómo funcionan las variables, así que no te sientas mal si no lo has entendido todo."
            m 1eua "Saber cómo trabajar con variables es suficiente para lecciones futuras."
            m "De todas formas..."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    if last_seen_is_None:
        m 1eua "Creo que es suficiente Python por hoy."

    m 1hua "¡Gracias por escuchar!"
    return




















label monika_ptod_tip007:



    m 1eua "En C y muchos otros lenguajes, los números enteros generalmente se almacenan en 4 bytes."
    m "Python, sin embargo, reserva una cantidad diferente de memoria dependiendo del tamaño del entero que se almacena."
    m 3eua "Podemos comprobar cuánta memoria almacena una variable 'a_number' tomando prestada una función de la libreria {i}sys{/i}."

    call mas_wx_cmd ("import sys", local_ctx)
    call mas_wx_cmd ("sys.getsizeof(a_number)", local_ctx)
    $ int_size = store.mas_ptod.get_last_line()

    m 1eksdla "Hablaré de las bibliotecas y su importación más tarde."
    m 1eua "Por ahora, observa el número devuelto por la función {i}getsizeof{/i}."
    m "Para almacenar el número [num_store], Python usa [int_size] bytes."

    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip008",
            category=["consejos sobre python"],
            prompt="Literales",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip008:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)
    $ last_seen_is_None = mas_getEVL_last_seen("monika_ptod_tip008") is None

    m 1eua "¿Recuerdas cuando te mostré cómo crear variables y asignarles valores?"
    m 1dsa "Imagínate si abandonáramos la noción de variables y nos enfocamos en usar los valores directamente en el código."
    m 1hua "Ahí es donde entran los literales. Te mostraré lo que quiero decir con esto con la siguiente demostración."

    show monika at t22
    show screen mas_py_console_teaching

    call mas_wx_cmd ("a = 10")
    m 3eua "Hice una variable llamada 'a' y le asigné un valor entero de 10."
    m "Cuando escribo 'a' en el intérprete..."

    call mas_wx_cmd ("a")
    m 3eub "Python busca el símbolo 'a' y encuentra que está asociado con el valor 10, por lo que se nos muestra 10."
    m "Sin embargo, si escribo solo '10'..."

    call mas_wx_cmd ("10")
    m 3hua "¡Python todavía nos muestra un 10!"
    m 3eua "Esto sucede porque Python interpreta el '10' como un valor entero de inmediato, sin tener que buscar un símbolo y recuperar su valor."
    m "El código que Python puede interpretar en valores directamente se llama {i}literales{/i}."
    m 3eub "Todos los tipos de datos que mencioné en la lección 'tipos' se pueden escribir como literales."

    call mas_wx_cmd ("23")
    call mas_wx_cmd ("21.05")
    m 3eua "Estos son literales {b}enteros{/b} y {b}flotantes{/b}."

    call mas_wx_cmd ('"Esta es una cadena"')
    call mas_wx_cmd ("'Esta es otra cadena'")
    m "Estos son literales de {b}cadena{/b}."

    call mas_wx_cmd ("true")
    call mas_wx_cmd ("false")
    m "Estos son literales {b}booleanos{/b}."

    call mas_wx_cmd ("None")
    m "La palabra clave {i}None{/i} es en sí misma un literal."



    if last_seen_is_None:
        m 1eua "Hay más literales para otros tipos, pero los mencionaré cuando hable de esos tipos."

    m 1eua "Se pueden utilizar literales en lugar de variables al escribir código. Por ejemplo:"

    call mas_wx_cmd ("10 + 21")
    call mas_wx_cmd ("10 * 5")
    m "Podemos hacer matemáticas con literales en lugar de variables."

    call mas_wx_cmd ("a + 21")
    call mas_wx_cmd ("a * 5")
    m "También podemos usar literales junto con variables."
    m 1eub "Además, los literales son excelentes para crear y usar datos sobre la marcha sin la sobrecarga de crear variables innecesarias."

    if last_seen_is_None:
        m 1kua "Muy bien, eso es todo lo que {i}literalmente{/i} puedo decirte sobre los literales."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11

    m 1hua "¡Gracias por escuchar!"
    return


init python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ptod_tip009",
            category=["consejos sobre python"],
            prompt="Valores verdaderos",
            pool=True,
            conditional="store.mas_ptod.has_day_past_tip(5)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )



label monika_ptod_tip009:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()
    $ store.mas_ptod.set_local_context(local_ctx)

    if mas_getEVL_last_seen("monika_ptod_tip009") is None:
        m 1eua "Cuando hablamos de comparaciones y valores booleanos, usamos números enteros como base para nuestras comparaciones."
        m 1dsa "Pero..."
        m 3eua "¿Sabías que cada tipo tiene su propio valor de verdad asociado?"

    m 1eua "Todos los tipos tienen un 'valor de verdad' que puede cambiar según el valor del tipo."



    m "Podemos verificar el valor de verdad de un tipo usando la palabra clave {b}bool{/b}."

    show monika at t22
    show screen mas_py_console_teaching

    m 3eua "Empecemos por echar un vistazo a los valores de verdad de los números enteros."
    call mas_wx_cmd ("bool(10)")
    call mas_wx_cmd ("bool(-1)")
    m 3eua "Todos los enteros distintos de cero tienen un valor de verdad de {b}true{/b}."
    call mas_wx_cmd ("bool(0)")
    m 3eub "Cero, por otro lado, tiene un valor de verdad de {b}false{/b}."

    m 1eua "Los flotantes siguen las mismas reglas que los números enteros:"
    call mas_wx_cmd ("bool(10.02)")
    call mas_wx_cmd ("bool(0.14)")
    call mas_wx_cmd ("bool(0.0)")

    m 1eua "Ahora veamos las cadenas."
    call mas_wx_cmd ('bool("cadena con texto")')
    call mas_wx_cmd ('bool("  ")')
    m 3eub "Una cadena con texto, incluso si el texto es solo caracteres de espacio en blanco, tiene un valor de verdad de {b}true{/b}."
    call mas_wx_cmd ('bool("")')
    m "Una cadena vacía, o una cadena con longitud 0, tiene un valor de verdad de {b}false{/b}."

    m 1eua "Ahora veamos {b}None{/b}."
    call mas_wx_cmd ("bool(None)")
    m 1eub "{b}None{/b} siempre tiene un valor de verdad de {b}false{/b}."



    m 1eua "Si hacemos comparaciones con estos valores, los valores se evalúan a sus valores de verdad antes de aplicarse en las comparaciones."
    m 1hua "Permíteme mostrar algunos ejemplos."
    m 3eua "Primero, configuraré algunas variables:"
    call mas_wx_cmd ("num10 = 10")
    call mas_wx_cmd ("num0 = 0")
    call mas_wx_cmd ('text = "text"')
    call mas_wx_cmd ('empty_text = ""')
    call mas_wx_cmd ("None_var = None")

    m 3eub "Y luego haré varias comparaciones."
    call mas_wx_cmd ("bool(num10 and num0)")
    call mas_wx_cmd ("bool(num10 and text)")
    call mas_wx_cmd ("bool(empty_text or num0)")
    call mas_wx_cmd ("bool(None_var and text)")
    call mas_wx_cmd ("bool(empty_text or None_var)")

    m 1eua "Conocer los valores de verdad de diferentes tipos puede ser útil para realizar ciertas comparaciones de manera más eficiente."
    m 1hua "Mencionaré cuándo es posible hacerlo cuando nos encontremos con esas situaciones en lecciones futuras."

    $ store.mas_ptod.ex_cn()
    hide screen mas_py_console_teaching
    show monika at t11
    m 1hua "¡Gracias por escuchar!"
    return
















label monika_ptod_tip010:

    return











init 495 image cn_frame = "mod_assets/console/cn_frame.png"
define -5 mas_ptod.font = mas_ui.MONO_FONT







init -5 style mas_py_console_text is console_text:
    font mas_ptod.font
init -5 style mas_py_console_text_cn is console_text_console:
    font mas_ptod.font






init -6 python in mas_ptod:
    import store.mas_utils as mas_utils


    SYM = ">>> "
    M_SYM = "... "


    cn_history = list()


    H_SIZE = 20


    cn_line = ""


    cn_cmd = ""


    blk_cmd = list()




    stack_level = 0




    indent_stack = list()


    VER_TEXT_1 = "Python {0}"
    VER_TEXT_2 = "{0} en MAS"


    LINE_MAX = 66



    STATE_SINGLE = 0


    STATE_MULTI = 1


    STATE_BLOCK = 2


    STATE_BLOCK_MULTI = 3


    STATE_OFF = 4


    state = STATE_SINGLE


    local_ctx = dict()


    def clr_cn():
        """
        SEE clear_console
        """
        clear_console()


    def ex_cn():
        """
        SEE exit_console
        """
        exit_console()


    def rst_cn():
        """
        SEE restart_console
        """
        restart_console()


    def w_cmd(cmd):
        """
        SEE write_command
        """
        write_command(cmd)


    def x_cmd(context):
        """
        SEE exec_command
        """
        exec_command(context)


    def wx_cmd(cmd, context):
        """
        Does both write_command and exec_command
        """
        w_cmd(cmd)
        x_cmd(context)


    def write_command(cmd):
        """
        Writes a command to the console

        NOTE: Does not EXECUTE
        NOTE: remove previous command
        NOTE: does NOT append to previously written command (unless that cmd
            is in a block and was executed)

        IN:
            cmd - the command to write to the console
        """
        if state == STATE_OFF:
            return
        
        global cn_line, cn_cmd, state, stack_level
        
        if state == STATE_MULTI:
            
            
            
            cn_cmd = ""
            cn_line = ""
            state = STATE_SINGLE
        
        elif state == STATE_BLOCK_MULTI:
            
            
            cn_cmd = ""
            cn_line = ""
            state = STATE_BLOCK
        
        
        
        cn_cmd = str(cmd)
        
        
        if state == STATE_SINGLE:
            
            sym = SYM
        
        else:
            
            sym = M_SYM
        
        
        prefixed_cmd = sym + cn_cmd
        
        
        cn_lines = _line_break(prefixed_cmd)
        
        if len(cn_lines) == 1:
            
            cn_line = cn_cmd
        
        else:
            
            
            
            _update_console_history_list(cn_lines[:-1])
            
            
            cn_line = cn_lines[len(cn_lines)-1]
            
            if state == STATE_SINGLE:
                
                state = STATE_MULTI
            
            else:
                
                state = STATE_BLOCK_MULTI


    def clear_console():
        """
        Cleares console hisotry and current line

        Also resets state to Single
        """
        global cn_history, cn_line, cn_history, state, local_ctx
        cn_line = ""
        cn_cmd = ""
        cn_history = []
        state = STATE_SINGLE
        local_ctx = {}


    def restart_console():
        """
        Cleares console history and current line, also sets up version text
        """
        global state
        import sys
        version = sys.version
        
        
        split_dex = version.find(")")
        start_lines = [


            VER_TEXT_1.format(version[:split_dex+1]),
            VER_TEXT_2.format(version[split_dex+2:])
        ]
        
        
        clear_console()
        _update_console_history_list(start_lines)
        
        
        state = STATE_SINGLE


    def exit_console():
        """
        Disables the console
        """
        global state
        state = STATE_OFF


    def _m1_script0x2dpython__exec_cmd(line, context, block=False):
        """
        Tries to eval the line first, then executes.
        Returns the result of the command

        IN:
            line - line to eval / exec
            context - dict that represnts the current context. should be locals
            block - True means we are executing a block command and should
                skip eval

        RETURNS:
            the result of the command, as a string
        """
        if block:
            return _m1_script0x2dpython__exec_exec(line, context)
        
        
        return _m1_script0x2dpython__exec_evalexec(line, context)


    def _m1_script0x2dpython__exec_exec(line, context):
        """
        Runs exec on the given line
        Returns an empty string or a string with an error if it occured.

        IN:
            line - line to exec
            context - dict that represents the current context

        RETURNS:
            empty string or string with error message
        """
        try:
            exec(line, context)
            return ""
        
        except Exception as e:
            return _exp_toString(e)


    def _m1_script0x2dpython__exec_evalexec(line, context):
        """
        Tries to eval the line first, then executes.
        Returns the result of the command

        IN:
            line - line to eval / exec
            context - dict that represents the current context.

        RETURNS:
            the result of the command as a string
        """
        try:
            return str(eval(line, context))
        
        except:
            
            return _m1_script0x2dpython__exec_exec(line, context)


    def exec_command(context):
        """
        Executes the command that is currently in the console.
        This is basically pressing Enter

        IN:
            context - dict that represnts the current context. You should pass
                locals here.
                If None, then we use the local_ctx.
        """
        if state == STATE_OFF:
            return
        
        if context is None:
            context = local_ctx
        
        global cn_cmd, cn_line, state, stack_level, blk_cmd
        
        
        
        
        block_mode = state == STATE_BLOCK or state == STATE_BLOCK_MULTI
        
        
        empty_line = len(cn_cmd.strip()) == 0
        
        
        time_to_block = cn_cmd.endswith(":")
        
        
        bad_block = time_to_block and len(cn_cmd.strip()) == 1
        
        
        full_cmd = None
        
        
        
        if empty_line:
            
            
            if block_mode:
                
                _m1_script0x2dpython__popi()
            
            else:
                
                
                _update_console_history(SYM)
                cn_line = ""
                cn_cmd = ""
                return
        
        if bad_block:
            
            
            full_cmd = cn_cmd
            stack_level = 0
            blk_cmd = list()
        
        elif time_to_block:
            
            blk_cmd.append(cn_cmd)
            
            if not block_mode:
                
                _m1_script0x2dpython__pushi(0)
            
            else:
                
                pre_spaces = _count_sp(cn_cmd)
                
                if _m1_script0x2dpython__peeki() != pre_spaces:
                    
                    
                    _m1_script0x2dpython__pushi(pre_spaces)
        
        elif block_mode:
            
            blk_cmd.append(cn_cmd)
            
            if stack_level == 0:
                
                full_cmd = "\n".join(blk_cmd)
                blk_cmd = list()
        
        else:
            
            
            
            full_cmd = cn_cmd
        
        
        
        
        if full_cmd is not None:
            result = _m1_script0x2dpython__exec_cmd(full_cmd, context, block_mode)
        
        else:
            result = ""
        
        
        
        if block_mode and empty_line:
            
            output = [M_SYM]
        
        else:
            
            if state == STATE_SINGLE:
                sym = SYM
            
            elif state == STATE_BLOCK:
                sym = M_SYM
            
            else:
                
                sym = ""
            
            output = [sym + cn_line]
        
        
        if len(result) > 0:
            output.append(result)
        
        
        cn_line = ""
        cn_cmd = ""
        _update_console_history_list(output)
        
        
        
        if bad_block:
            
            state = STATE_SINGLE
            block_mode = False
        
        elif time_to_block:
            
            state = STATE_BLOCK
            block_mode = True
        
        
        
        if (state == STATE_MULTI) or (block_mode and stack_level == 0):
            
            state = STATE_SINGLE
        
        elif state == STATE_BLOCK_MULTI:
            
            state = STATE_BLOCK


    def get_last_line():
        """
        Retrieves the last line from the console history

        RETURNS:
            last line from console history as a string
        """
        if len(cn_history) > 0:
            return cn_history[len(cn_history)-1]
        
        return ""


    def set_local_context(context):
        """
        Sets the local context to the given context.

        Stuff in the old context are forgotten.
        """
        global local_ctx
        local_ctx = context


    def _m1_script0x2dpython__pushi(indent_level):
        """
        Pushes a indent level into the stack

        IN:
            indent_level - indent to push into stack
        """
        global stack_level
        stack_level += 1
        indent_stack.append(indent_level)


    def _m1_script0x2dpython__popi():
        """
        Pops indent level from stack

        REUTRNS:
            popped indent level
        """
        global stack_level
        stack_level -= 1
        
        if stack_level < 0:
            stack_level = 0
        
        if len(indent_stack) > 0:
            indent_stack.pop()


    def _m1_script0x2dpython__peeki():
        """
        Returns value that would be popped from stack

        RETURNS:
            indent level that would be popped
        """
        return indent_stack[len(indent_stack)-1]


    def _exp_toString(exp):
        """
        Converts the given exception into a string that looks like
        how python interpreter prints out exceptions
        """
        err = repr(exp)
        err_split = err.partition("(")
        return err_split[0] + ": " + str(exp)


    def _indent_line(line):
        """
        Prepends the given line with an appropraite number of spaces, depending
        on the current stack level

        IN:
            line - line to prepend

        RETURNS:
            line prepended with spaces
        """
        return (" " * (stack_level * 4)) + line


    def _count_sp(line):
        """
        Counts number of spaces that prefix this line

        IN:
            line - line to cound spaces

        RETURNS:
            number of spaces at start of line
        """
        return len(line) - len(line.lstrip(" "))


    def _update_console_history(*new_items):
        """
        Updates the console history with the list of new lines to add

        IN:
            new_items - the items to add to the console history
        """
        _update_console_history_list(new_items)


    def _update_console_history_list(new_items):
        """
        Updates console history with list of new lines to add

        IN:
            new_items - list of new itme sto add to console history
        """
        global cn_history
        
        
        for line in new_items:
            broken_lines = _line_break(line)
            
            
            for b_line in broken_lines:
                
                cn_history.append(b_line)
        
        if len(cn_history) > H_SIZE:
            cn_history = cn_history[-H_SIZE:]


    def _line_break(line):
        """
        Lines cant be too large. This will line break entries.

        IN:
            line - the line to break

        RETURNS:
            list of strings, each item is a line.
        """
        if len(line) <= LINE_MAX:
            return [line]
        
        
        broken_lines = list()
        while len(line) > LINE_MAX:
            broken_lines.append(line[:LINE_MAX])
            line = line[LINE_MAX:]
        
        
        broken_lines.append(line)
        return broken_lines


init -505 screen mas_py_console_teaching():

    frame:
        xanchor 0
        yanchor 0
        xpos 5
        ypos 5
        background "mod_assets/console/cn_frame.png"

        has fixed
        python:
            starting_index = len(store.mas_ptod.cn_history) - 1
            cn_h_y = 413
            cn_l_x = 41


        for index in range(starting_index, -1, -1):
            $ cn_line = store.mas_ptod.cn_history[index]
            text "[cn_line]":
                style "mas_py_console_text"
                anchor (0, 1.0)
                xpos 5
                ypos cn_h_y
            $ cn_h_y -= 20


        if store.mas_ptod.state == store.mas_ptod.STATE_SINGLE:
            text ">>> ":
                style "mas_py_console_text"
                anchor (0, 1.0)
                xpos 5
                ypos 433

        elif store.mas_ptod.state == store.mas_ptod.STATE_BLOCK:
            text "... ":
                style "mas_py_console_text"
                anchor (0, 1.0)
                xpos 5
                ypos 433

        else:

            $ cn_l_x = 5


        if len(store.mas_ptod.cn_line) > 0:
            text "[store.mas_ptod.cn_line]":
                style "mas_py_console_text_cn"
                anchor (0, 1.0)
                xpos cn_l_x
                ypos 433


label mas_w_cmd(cmd, wait=0.7):
    $ store.mas_ptod.w_cmd(cmd)
    $ renpy.pause(wait, hard=True)
    return


label mas_x_cmd(ctx=None, wait=0.7):
    $ store.mas_ptod.x_cmd(ctx)
    $ renpy.pause(wait, hard=True)
    return


label mas_wx_cmd(cmd, ctx=None, w_wait=0.7, x_wait=0.7):
    $ store.mas_ptod.w_cmd(cmd)
    $ renpy.pause(w_wait, hard=True)
    $ store.mas_ptod.x_cmd(ctx)
    $ renpy.pause(x_wait, hard=True)
    return


label mas_wx_cmd_noxwait(cmd, ctx=None):
    call mas_wx_cmd (cmd, ctx, x_wait=0.0)
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
