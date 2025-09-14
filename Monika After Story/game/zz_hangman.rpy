





default persistent._mas_hangman_playername = False
define hm_ltrs_only = "abcdefghijklmnñopqrstuvwxyz?!- "



image hm_6 = "mod_assets/games/hangman/hm_6.png"
image hm_5 = "mod_assets/games/hangman/hm_5.png"
image hm_4 = "mod_assets/games/hangman/hm_4.png"
image hm_3 = "mod_assets/games/hangman/hm_3.png"
image hm_2 = "mod_assets/games/hangman/hm_2.png"
image hm_1 = "mod_assets/games/hangman/hm_1.png"
image hm_0 = "mod_assets/games/hangman/hm_0.png"


image hm_s:
    block:


        block:
            choice:
                "mod_assets/games/hangman/hm_s1.png"
            choice:
                "mod_assets/games/hangman/hm_s2.png"
        block:



            choice:
                0.075
            choice:
                0.09
            choice:
                0.05
        repeat



define hm.SAYORI_SCALE = 0.25
image hm_s_win_6 = im.FactorScale(im.Flip(getCharacterImage("sayori", "4r"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_5 = im.FactorScale(im.Flip(getCharacterImage("sayori", "2a"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_4 = im.FactorScale(im.Flip(getCharacterImage("sayori", "2i"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_3 = im.FactorScale(im.Flip(getCharacterImage("sayori", "1f"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_2 = im.FactorScale(im.Flip(getCharacterImage("sayori", "4u"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_1 = im.FactorScale(im.Flip(getCharacterImage("sayori", "4w"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_0 = im.FactorScale(im.Flip("images/sayori/end-glitch1.png", horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_fail = im.FactorScale(im.Flip("images/sayori/3c.png", horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_leave = im.FactorScale(getCharacterImage("sayori", "1a"), hm.SAYORI_SCALE)





image hm_frame = "mod_assets/games/hangman/hm_frame.png"
image hm_frame_dark = "mod_assets/games/hangman/hm_frame_d.png"


transform hangman_board:
    xanchor 0 yanchor 0 xpos 675 ypos 100 alpha 1.0

transform hangman_missed_label:
    xanchor 0 yanchor 0 xpos 680 ypos 105

transform hangman_missed_chars:
    xanchor 0 yanchor 0 xpos 780 ypos 105

transform hangman_display_word:
    xcenter 975 yanchor 0 ypos 475

transform hangman_hangman:
    xanchor 0 yanchor 0 xpos 880 ypos 125



transform hangman_sayori(z=1.0):
    xcenter -300 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True
    easein 0.25 xcenter 90


transform hangman_sayori_i(z=1.0):
    xcenter 90 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True


transform hangman_sayori_i3(z=1.0):
    xcenter 82 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True


transform hangman_sayori_h(z=1.0):
    xcenter 90 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True
    easein 0.1 yoffset -20
    easeout 0.1 yoffset 0


transform hangman_sayori_lh(z=1.0):
    subpixel True
    on hide:
        easeout 0.5 xcenter -300


transform hangman_monika(z=0.80):
    tcommon(330,z=z)

transform hangman_monika_i(z=0.80):
    tinstant(330,z=z)


style hangman_text:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    kerning 10.0



















init -1 python in mas_hangman:
    import store
    import copy
    import random



    EASY_MODE = 0
    NORM_MODE = 1
    HARD_MODE = 2

    hm_words = {
        EASY_MODE: list(), 
        NORM_MODE: list(), 
        HARD_MODE: list() 
    }

    all_hm_words = {
        EASY_MODE: list(),
        NORM_MODE: list(),
        HARD_MODE: list()
    }



    LETTER_SPACE = 10.0


    WORD_FONT = "mod_assets/font/m1_fixed.ttf"
    WORD_SIZE = 36
    WORD_OUTLINE = []
    WORD_COLOR = "#202020"
    WORD_COLOR_GET = "#CC6699"
    WORD_COLOR_MISS = "#000"


    HM_IMG_NAME = "hm_"


    MONI_WORDS = ["esmeralda","borrar","libertad","piano","música","realidad","lluvia","envidia",
        "cafe","cinta","consejo","cruce","pluma","resumen","corrupcion",
        "calamar","presidenta","pasion","vegetales","soledad","simbolo",
        "verde","poema","ruta","literatura","epifania","desesperacion","miserable","orilla",
        "olas","playa","natacion","debate","liderazgo","festival","confianza",
        "creatividad","extrovertida","desilusionado","artificial","python","renpy","programacion",
        "letargo"
    ]


    HM_HINT = "A {0} gustaría esa palabra."

    def _add_monika_words(wordlist):
        for word in MONI_WORDS:
            wordlist.append(renpy.store.PoemWord(glitch=False,sPoint=0,yPoint=0,nPoint=0,word=word))



    NORMAL_LIST = "mod_assets/games/hangman/MASpoemwords.txt"
    HARD_LIST = "mod_assets/games/hangman/1000poemwords.txt"


    game_name = "Ahorcado"


    def copyWordsList(_mode):
        """
        Does a deepcopy of the words for the given mode.

        Sets the hm_words dict for that mode

        NOTE: does a list clear, so old references will still work

        RETURNS: the copied list of words. This is the same reference as
            hm_words's list. (empty list if mode is invalid)
        """
        if _mode not in all_hm_words:
            return list()
        
        
        hm_words[_mode][:] = copy.deepcopy(all_hm_words[_mode])
        return hm_words[_mode]


    def _buildWordList(filepath, _mode):
        """
        Builds a list of words given the filepath and mode

        IN:
            filepath - filepath of words to load in
            _mode - mode to build word list for
        """
        all_hm_words[_mode][:] = [
            word._hangman()
            for word in store.MASPoemWordList(filepath).wordlist
        ]
        copyWordsList(_mode)


    def buildEasyList():
        """
        Builds the easy word list

        Sets hm_words and all_hm_words appropritaley

        NOTE: clears the list (noticable in all references)
        """
        easy_list = all_hm_words[EASY_MODE]
        
        
        easy_list[:] = [
            store.MASPoemWord._build(word, 0)._hangman()
            for word in store.full_wordlist
        ]
        
        
        moni_list = list()
        _add_monika_words(moni_list)
        for m_word in moni_list:
            easy_list.append(store.MASPoemWord._build(m_word, 4)._hangman())
        
        copyWordsList(EASY_MODE)


    def buildNormalList():
        """
        Builds the normal word list

        Sets hm_words and all_hm_words appropraitely

        NOTE: clears the list (noticable in all references)
        """
        _buildWordList(NORMAL_LIST, NORM_MODE)


    def buildHardList():
        """
        Builds the hard word list

        Sets hm_words and all_hm_words appropraitely

        NOTE: cleras the list (noticable in all references)
        """
        _buildWordList(HARD_LIST, HARD_MODE)


    def addPlayername(_mode):
        """
        Adds playername to the given mode if appropriate

        IN:
            _mode - mode to add playername to
        """
        if (
                not store.persistent._mas_hangman_playername
                and store.persistent.playername.lower() != "sayori"
                and store.persistent.playername.lower() != "yuri"
                and store.persistent.playername.lower() != "natsuki"
                and store.persistent.playername.lower() != "monika"
            ):
            hm_words[_mode].append(-1)


    def removePlayername(_mode):
        """
        Removes the playername from the given mode if found

        IN:
            _mode - mode to remove in
        """
        wordlist = hm_words.get(_mode, None)
        if wordlist is not None and -1 in wordlist:
            wordlist.remove(-1)


    def randomSelect(_mode):
        """
        Randomly selects and pulls a word from the hm_words, given the mode

        Will refill the words list if it is empty

        IN:
            _mode - mode to pull word from

        RETURNS: tuple of the following format:
            [0]: word
            [1]: winner (for hint)
        """
        words = hm_words.get(_mode, hm_words[EASY_MODE])
        
        
        if len(words) <= 0:
            copyWordsList(_mode)
        
        
        return words.pop(random.randint(0, len(words)-1))


    def wordToDisplay(word):
        """
        Formats a word so it can be displayed in hangman

        IN:
            word - word to format (string)

        RETURNS: display word
        """
        return ["_" if c != "-" else "-" for c in word]



init 10 python:


    import store.mas_hangman as mas_hmg

    mas_hmg.buildEasyList()
    mas_hmg.buildNormalList()
    mas_hmg.buildHardList()



label game_hangman:

    $ disable_esc()

    python:
        import store.mas_hangman as mas_hmg
        is_sayori = store.mas_egg_manager.sayori_enabled()
        is_window_sayori_visible = False


        instruct_txt = (
            "Adivina una letra, escribe {0}'!' para rendirte."
        )

        instruct_txt = instruct_txt.format("'?' para repetir la pista, ")
        store.mas_hangman.game_name = "Ahorcado"

label mas_hangman_game_select_diff:
    m "Elige una dificultad.{nw}"
    $ _history_list.pop()
    menu:
        m "Elige una dificultad.{fast}"
        "Fácil":
            $ hangman_mode = mas_hmg.EASY_MODE
        "Normal":
            $ hangman_mode = mas_hmg.NORM_MODE
        "Difícil":
            $ hangman_mode = mas_hmg.HARD_MODE

label mas_hangman_game_preloop:


    show monika at t21
    if store.mas_globals.dark_mode:
        show hm_frame_dark zorder 13 at hangman_board
    else:
        show hm_frame zorder 13 at hangman_board

    python:

        missed_label = Text(
            "Fallos:",
            font=mas_hmg.WORD_FONT,
            color=mas_hmg.WORD_COLOR,
            size=mas_hmg.WORD_SIZE,
            outlines=mas_hmg.WORD_OUTLINE
        )


    show text missed_label as hmg_mis_label zorder 18 at hangman_missed_label


    if hangman_mode not in mas_hmg.hm_words:
        $ hangman_mode = mas_hmg.EASY_MODE


    $ mas_hmg.addPlayername(hangman_mode)
    $ hm_words = mas_hmg.hm_words[hangman_mode]




label mas_hangman_game_loop:
    m 1eua "Pensaré en una palabra.{w=0.5}.{w=0.5}.{w=0.5}{nw}"

    python:
        player_word = False


        if len(hm_words) == 0:
            mas_hmg.copyWordsList(hangman_mode)


        word = mas_hmg.randomSelect(hangman_mode)


        if (
                word == -1
                and persistent.playername.isalpha()
                and len(persistent.playername) <= 15
            ):
            display_word = mas_hmg.wordToDisplay(persistent.playername.lower())
            hm_hint = mas_hmg.HM_HINT.format("I")
            word = persistent.playername.lower()
            player_word = True
            persistent._mas_hangman_playername = True

        else:
            if word == -1:
                word = mas_hmg.randomSelect(hangman_mode)
            
            display_word = mas_hmg.wordToDisplay(word[0])
            hm_hint = mas_hmg.HM_HINT.format(word[1])
            
            word = word[0]












    if is_sayori:
        if is_window_sayori_visible:
            show hm_s_win_6 as window_sayori at hangman_sayori_i
        else:
            show hm_s_win_6 as window_sayori at hangman_sayori
        $ is_window_sayori_visible = True

    m "Muy bien, tengo una."
    m "[hm_hint]"


    $ done = False
    $ win = False
    $ chances = 6
    $ guesses = 0
    $ missed = ""
    $ avail_letters = list(hm_ltrs_only)
    $ give_up = False

    $ dt_color = mas_hmg.WORD_COLOR
    while not done:

        python:
            if chances == 0:
                dt_color = mas_hmg.WORD_COLOR_MISS
            elif "_" not in display_word:
                dt_color = mas_hmg.WORD_COLOR_GET

            display_text = Text(
                "".join(display_word),
                font=mas_hmg.WORD_FONT,
                color=dt_color,
                size=mas_hmg.WORD_SIZE,
                outlines=mas_hmg.WORD_OUTLINE,
                kerning=mas_hmg.LETTER_SPACE
            )

            missed_text = Text(
                missed,
                font=mas_hmg.WORD_FONT,
                color=mas_hmg.WORD_COLOR,
                size=mas_hmg.WORD_SIZE,
                outlines=mas_hmg.WORD_OUTLINE,
                kerning=mas_hmg.LETTER_SPACE
            )


        show text display_text as hmg_dis_text zorder 18 at hangman_display_word
        show text missed_text as hmg_mis_text zorder 18 at hangman_missed_chars


        if is_sayori:


            if chances == 0:


                $ mas_RaiseShield_core()


                $ hm_glitch_word = glitchtext(40) + "?"
                $ style.say_dialogue = style.edited


                show hm_s zorder 18 at hangman_hangman


                hide monika
                show monika_body_glitch1 as mbg zorder MAS_MONIKA_Z at i21


                show hm_s_win_0 as window_sayori


                show screen tear(20, 0.1, 0.1, 0, 40)
                play sound "sfx/s_kill_glitch1.ogg"
                pause 0.2
                stop sound
                hide screen tear


                m "{cps=*2}[hm_glitch_word]{/cps}{w=0.2}{nw}"
                $ _history_list.pop()


                show screen tear(20, 0.1, 0.1, 0, 40)
                play sound "sfx/s_kill_glitch1.ogg"
                pause 0.2
                stop sound
                hide screen tear


                hide mbg
                hide window_sayori
                hide hm_s
                show monika 1esa zorder MAS_MONIKA_Z at i21
                $ mas_resetTextSpeed()
                $ is_window_sayori_visible = False


                $ mas_MUINDropShield()
                $ enable_esc()
            else:


                $ next_window_sayori = "hm_s_win_" + str(chances)
                show expression next_window_sayori as window_sayori

        $ hm_display = mas_hmg.HM_IMG_NAME + str(chances)

        show expression hm_display as hmg_hanging_man zorder 18 at hangman_hangman


        if chances == 0:
            $ done = True
            if player_word:
                m 1eka "[player]..."
                m "¿No pudiste adivinar tu propio nombre?"
            m 1hua "Mejor suerte la próxima vez~"
        elif "_" not in display_word:
            $ done = True
            $ win = True
        else:
            python:


                bad_input = True
                while bad_input:
                    guess = renpy.input(
                        instruct_txt,
                        allow="".join(avail_letters),
                        length=1
                    )
                    
                    if len(guess) != 0:
                        bad_input = False


            if guess == "?":
                m "[hm_hint]"
            elif guess == "!":
                if is_window_sayori_visible:
                    show hm_s_win_fail as window_sayori at hangman_sayori_i3

                $ give_up = True
                $ done = True



                m 1lksdlb "[player]..."
                if guesses == 0:
                    m "Pensé que dijiste que querías jugar al [store.mas_hangman.game_name]."
                    m 1lksdlc "Ni siquiera adivinaste una sola letra."
                    m "..."
                    m 1ekc "Realmente disfruto jugar contigo, ¿sabes?"

                elif chances == 5:
                    m 1ekc "No te rindas tan fácilmente."
                    m 3eka "¡Esa fue solo tu primera letra incorrecta!"
                    if chances > 1:
                        m 1eka "Aún te quedan [chances] vidas más."
                    else:
                        m 1eka "Aún te queda [chances] vida más."

                    m 1hua "¡Sé que puedes hacerlo!"
                    m 1eka "Realmente significaría mucho para mí si lo intentaras un poco más."
                else:

                    m "Deberías jugar al menos hasta el final..."
                    m 1ekc "Rendirse tan fácilmente es señal de falta de determinación."
                    if chances > 1:
                        m "Quiero decir, tendrías que fallar [chances] letras más para perder."
                    else:
                        m "Quiero decir, tendrías que fallar [chances] letra más para perder."

                m 1eka "¿Puedes jugar hasta el final la próxima vez, [player]? ¿Por mi?"
            else:

                $ guesses += 1
                python:
                    if guess in word:
                        for index in range(0,len(word)):
                            if guess == word[index]:
                                display_word[index] = guess
                    else:
                        chances -= 1
                        missed += guess
                        if chances == 0:
                            
                            display_word = word


                    avail_letters.remove(guess)


                hide text hmg_dis_text
                hide text hmg_mis_text
                hide hmg_hanging_man


    if win:
        if is_window_sayori_visible:
            show hm_s_win_6 as window_sayori at hangman_sayori_h

        if player_word:
            $ the_word = "tu nombre"
        else:
            $ the_word = "la palabra"

        m 1hua "¡Vaya, has adivinado [the_word] correctamente!"
        m "¡Buen trabajo, [player]!"

        if not persistent._mas_ever_won['hangman']:
            $ persistent._mas_ever_won['hangman']=True



    if give_up:
        jump mas_hangman_game_end


    m "¿Te gustaría volver a jugar?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gustaría volver a jugar?{fast}"
        "Sí":
            $ hang_ev = mas_getEV("mas_hangman")
            if hang_ev:

                $ hang_ev.shown_count += 1

            show monika at t21
            jump mas_hangman_game_loop
        "No":

            pass






label mas_hangman_game_end:

    hide hmg_hanging_man
    hide hmg_mis_label
    hide hmg_dis_text
    hide hmg_mis_text
    hide hm_frame
    hide hm_frame_dark
    show monika at t32
    if is_window_sayori_visible:
        show hm_s_win_leave as window_sayori at hangman_sayori_lh
        pause 0.1
        hide window_sayori

    $ mas_hmg.removePlayername(hangman_mode)

    if renpy.seen_label("mas_hangman_dlg_game_end_long"):
        call mas_hangman_dlg_game_end_short from _mas_hangman_dges
    else:
        call mas_hangman_dlg_game_end_long from _mas_hangman_dgel

    $ enable_esc()

    return



label mas_hangman_dlg_game_end_long:
    m 1euc "El [store.mas_hangman.game_name] es en realidad un juego bastante difícil."
    m "Necesitas tener un buen vocabulario para poder adivinar diferentes palabras."
    m 1hua "¡La mejor manera de mejorar eso es leer más libros!"
    m 1eua "Sería muy feliz si hicieras eso por mí, [player]."
    return


label mas_hangman_dlg_game_end_short:
    if give_up:
        $ dlg_line = "Juguemos de nuevo pronto, ¿okey?"
    else:
        $ dlg_line = "Okey. ¡Juguemos de nuevo pronto!"

    m 1eua "[dlg_line]"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
