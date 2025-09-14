









define mas_poemwords = "mod_assets/MASpoemwords.txt"


init -4 python:
















    class MASPoemWord(object):
        def __init__(self, word, sPoint, nPoint, yPoint, mPoint, glitch=False):
            self.word = word
            self.sPoint = sPoint
            self.nPoint = nPoint
            self.yPoint = yPoint
            self.mPoint = mPoint
            self.glitch = glitch
        
        
        def _merge(self, _poemword, mPoint):
            """
            Merges a PoemWord into this MASPoemWord

            IN:
                _poemword - PoemWord object to merge
                mPoint - points to use for Monika
            """
            self.word = _poemword.word
            self.sPoint = _poemword.sPoint
            self.nPoint = _poemword.nPoint
            self.yPoint = _poemword.yPoint
            self.mPoint = mPoint
            self.glitch = _poemword.glitch
        
        
        def _hangman(self, mon="mí me", say="Sayori le", nat="Natsuki le", yur="Yuri le"):
            """
            Returns the approprite tuple of this word and the winner name.

            All the input arguments are to change winnner names.

            NOTE: highly specialized. Only used in hangman.
            NOTE: monika will always have a bias here

            RETURNS: tuple of the following format:
                [0]: the word as a string
                [1]: the winner as a string
            """
            the_winner = self.winner()
            
            
            if the_winner == self.mPoint:
                girl = mon 
            
            elif the_winner == self.sPoint:
                girl = say 
            
            elif the_winner == self.nPoint:
                girl = nat 
            
            elif the_winner == self.yPoint:
                girl = yur 
            
            else:
                
                girl = mon 
            
            return (self.word, girl)
        
        
        def winner(self):
            """
            Returns the point value of the winner
            """
            
            return max(self.mPoint, self.sPoint, self.nPoint, self.yPoint)
        
        
        @staticmethod
        def _build(_poemword, mPoint):
            """
            Builds a MASPoemword from a PoemWord

            IN:
                _poemword - Poemword object to build from
                mPoint - points to use for MOnika

            RETURNS: a MASPoemWord
            """
            return MASPoemWord(
                _poemword.word,
                _poemword.sPoint,
                _poemword.nPoint,
                _poemword.yPoint,
                mPoint,
                _poemword.glitch
            )












    class MASPoemWordList(object):
        def __init__(self, wordfile=None):
            
            
            
            
            self.wordlist = list()
            self.wordfile = wordfile
            
            if wordfile:
                self.readInFile(wordfile)
        
        
        def readInFile(self, wordfile):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            with renpy.file(wordfile) as words:
                for line in words:
                    
                    line = line.strip()
                    
                    if line == '' or line[0] == '#': continue
                    
                    x = line.split(',')
                    self.wordlist.append(
                        MASPoemWord(
                            x[0],
                            float(x[1]),
                            float(x[2]),
                            float(x[3]),
                            float(x[4])
                        )
                    )



    from store.mas_poemgame_consts import ODDS_SPACE
    from store.mas_poemgame_consts import ODDS_OTHER

    def glitchWord(word, odds_space=ODDS_SPACE, odds_other=ODDS_OTHER):
        
        
        
        
        
        
        
        
        
        
        
        
        
        s = list(word)
        for k in range(len(word)):
            if random.randint(1, odds_space) == 1:
                s[k] = ' '
            elif random.randint(1, odds_other) == 1:
                s[k] = random.choice(nonunicode)
        return "".join(s)


init -10 python in mas_poemgame_consts:


    SAYORI = "sayori"
    NATSUKI = "natsuki"
    YURI = "yuri"
    MONIKA = "monika"



    POEM_DISLIKE_THRESHOLD = 29
    POEM_LIKE_THRESHOLD = 45


    POEM_FILE = "poemwords.txt"


    DISPLAY_MODE = 0
    STOCK_MODE = 1
    MONIKA_MODE = 2


    ODDS_SPACE = 5
    ODDS_OTHER = 5


    ODDS_SCARE = 400


    ODDS_BAA = 10


    ODDS_GLTICH_SOUND = 2


    ODDS_YURI_SCARY = 100


    ODDS_EYES = 5


    PG_TEXT = "poemgame_text"
    PG_TEXT_CLR = "#000"


init -2 python in mas_poemgame_fun:
    import store.mas_poemgame_consts as mas_pgc


    def getPointValue(condition, point):
        
        
        
        
        
        
        
        
        
        
        if condition:
            return point
        
        return 0

    def getWinner(word, sayori, natsuki, yuri, monika, mas=False):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        girl_points = list()
        
        
        
        if mas:
            girl_points.append(
                (mas_pgc.MONIKA, getPointValue(monika, word.mPoint))
            )
        
        
        girl_points.append(
            (mas_pgc.SAYORI, getPointValue(sayori, word.sPoint))
        )
        girl_points.append(
            (mas_pgc.NATSUKI, getPointValue(natsuki, word.nPoint))
        )
        girl_points.append(
            (mas_pgc.YURI, getPointValue(yuri, word.yPoint))
        )
        
        
        largest = 0
        largestValue = girl_points[largest][1]
        for index in range(1,len(girl_points)):
            if girl_points[index][1] > largestValue:
                largestValue = girl_points[index][1]
                largest = index
        
        
        return girl_points[largest][0]

    def validateFlow(flow):
        
        
        
        
        
        
        
        
        return (
            flow == mas_pgc.DISPLAY_MODE
            or flow == mas_pgc.STOCK_MODE
            or flow == mas_pgc.MONIKA_MODE
        )












































screen mas_pg_textbutton_grid(words, row_info, col_info, xywh, bg_image=None, is_modal=False, _zorder=None, _style_prefix=None, _layer=None):
    modal is_modal
    zorder _zorder
    style_prefix _style_prefix


    python:
        row_spacing = row_info[1]
        col_spacing = col_info[1]
        if row_spacing is None:
            row_spacing = int(xywh[3] / row_info[0])
        if col_spacing is None:
            col_spacing = int(xywh[2] / col_info[0])


    fixed:
        area xywh
        if bg_image:
            add bg_image




        $ word_index = 0


        for col in range(col_info[0]):


            vbox:
                for row in range(row_info[0]):
                    if word_index < len(words):
                        textbutton _(words[word_index][0]):
                            xpos (col * col_spacing)
                            ypos (row * row_spacing)
                            if not _style_prefix:
                                text_style store.mas_poemgame_consts.PG_TEXT
                                text_color store.mas_poemgame_consts.PG_TEXT_CLR
                            action Return(words[word_index][1])
                        $ word_index += 1








label zz_mas_poemgame_sampleone:
    call mas_poem_minigame_actthree (trans_fast=True, hop_monika=True, gather_words=True) from _call_mpg_sampleone
    $ testvalues = _return
    return _return


label zz_mas_poemgame_sampletwo:
    call mas_poem_minigame_actone (trans_fast=True, gather_words=True) from _call_mpg_sampletwo
    $ testvalues = _return
    return _return



label zz_mas_poemgame_samplethree:
    $ from store.mas_poemgame_consts import DISPLAY_MODE

    python:
        pg_kwargs = {
            "show_monika": True,
            "show_natsuki": True,
            "show_sayori": True,
            "show_yuri": True,
            "show_yuri_cut": True,
            "total_words": 15,
            "trans_fast": True,
            "gather_words": True
        }



        renpy.call("mas_poem_minigame", DISPLAY_MODE, **pg_kwargs)

    $ testvalues = _return
    return _return

















































label mas_poem_minigame_actone(gather_words=False, music_filename=audio.t4, only_winner=False, poem_wordlist=None, sel_sound=gui.activate_sound, show_monika=False, show_natsuki=True, show_poemhelp=True, trans_in=True, show_sayori=True, show_yuri=True, total_words=20, trans_out=True, music_fadein=2.0, music_fadeout=2.0, trans_fast=False):





    $ from store.mas_poemgame_consts import STOCK_MODE
    call mas_poem_minigame (STOCK_MODE, music_filename=music_filename, show_monika=show_monika, show_natsuki=show_natsuki, show_sayori=show_sayori, show_yuri=show_yuri, show_poemhelp=show_poemhelp, total_words=total_words, poem_wordlist=poem_wordlist, only_winner=only_winner, gather_words=gather_words, sel_sound=sel_sound, trans_in=trans_in, trans_out=trans_out, music_fadein=music_fadein, music_fadeout=music_fadeout, trans_fast=trans_fast) from _call_poem_minigame_actone

    return _return


































label mas_poem_minigame_acttwo(gather_words=False, glitch_baa=(True,None,False), glitch_wordscare=(True,None), glitch_wordscare_sound=(True,None), music_filename=audio.t4, one_counter=True, only_winner=False, poem_wordlist=None, sel_sound=gui.activate_sound, show_eyes=(True,None), show_monika=False, show_natsuki=True, show_poemhelp=True, trans_in=False, show_sayori=True, show_yuri=True, show_yuri_cut=True, trans_out=True, show_yuri_scary=(True,None,False), total_words=20, music_fadein=0.0, music_fadeout=0.0, trans_fast=False, glitch_words=None):








    $ from store.mas_poemgame_consts import STOCK_MODE
    call mas_poem_minigame (STOCK_MODE, gather_words=gather_words, glitch_baa=glitch_baa, glitch_wordscare=glitch_wordscare, glitch_wordscare_sound=glitch_wordscare_sound, music_filename=music_filename, one_counter=one_counter, poem_wordlist=poem_wordlist, sel_sound=sel_sound, show_monika=show_monika, show_natsuki=show_natsuki, show_poemhelp=show_poemhelp, show_sayori=show_sayori, show_yuri=show_yuri, show_yuri_cut=show_yuri_cut, show_yuri_scary=show_yuri_scary, total_words=total_words, trans_in=trans_in, trans_out=trans_out, music_fadein=music_fadein, music_fadeout=music_fadeout, trans_fast=trans_fast, glitch_words=glitch_words) from _call_poem_minigame_acttwo

    return _return





















label mas_poem_minigame_actthree(gather_words=False, glitch_nb=True, glitch_words=(True,None,None), hop_monika=False, music_fadein=0.0, music_fadeout=0.0, music_filename=audio.ghostmenu, total_words=20, trans_fast=False, trans_in=False, trans_out=True):




    $ from store.mas_poemgame_consts import MONIKA_MODE
    call mas_poem_minigame (MONIKA_MODE, gather_words=gather_words, glitch_nb=glitch_nb, glitch_words=glitch_words, hop_monika=hop_monika, music_fadein=music_fadein, music_fadeout=music_fadeout, music_filename=music_filename, total_words=total_words, trans_fast=trans_fast, trans_in=trans_in, trans_out=trans_out, sel_sound=None) from _call_poem_minigame_three

    return _return

































































































































































































































































































































label mas_poem_minigame(flow, music_filename=audio.t4, show_monika=True, show_natsuki=False, show_sayori=False, show_yuri=False, glitch_nb=False, show_poemhelp=False, total_words=20, poem_wordlist=None, trans_in=True, one_counter=False, only_monika=False, glitch_words=None, trans_out=True, glitch_wordscare=None, only_winner=False, glitch_baa=None, gather_words=False, sel_sound=gui.activate_sound, hop_monika=False, show_yuri_cut=False, show_yuri_scary=None, show_eyes=None, glitch_wordscare_sound=None, music_fadein=2.0, music_fadeout=2.0, trans_fast=False):










    $ import store.mas_poemgame_fun as mas_fun
    $ import store.mas_poemgame_consts as mas_pgc


    if not mas_fun.validateFlow(flow):
        $ flow = mas_pgc.DISPLAY_MODE


    $ in_display_mode = flow == mas_pgc.DISPLAY_MODE
    $ in_stock_mode = flow == mas_pgc.STOCK_MODE
    $ in_monika_mode = flow == mas_pgc.MONIKA_MODE


    python:



        if (glitch_words is not None
            and len(glitch_words) >= 3
            and glitch_words[0]):
            
            
            glitch_words_alspace = False
            if not glitch_words[1]: 
                glitch_words = (
                    glitch_words[0],
                    mas_pgc.ODDS_SPACE,
                    glitch_words[2]
                )
            elif glitch_words[1] == 1: 
                glitch_words_alspace = True
            
            
            glitch_words_alother = False
            if not glitch_words[2]: 
                glitch_words = (
                    glitch_words[0],
                    glitch_words[1],
                    mas_pgc.ODDS_OTHER
                )
            elif glitch_words[2] == 1: 
                glitch_words_alother = True

        else: 
            glitch_words = None



        if (glitch_wordscare is not None
            and len(glitch_wordscare) >= 2
            and glitch_wordscare[0]):
            
            
            glitch_wordscare_alscare = False
            if not glitch_wordscare[1]: 
                glitch_wordscare = (glitch_wordscare[0], mas_pgc.ODDS_SCARE)
            elif glitch_wordscare[1] == 1: 
                glitch_wordscare_alscare = True
            
            
            if (glitch_baa is None or (
                len(glitch_baa) >= 3
                and glitch_baa[0])):
                
                
                played_baa = False
                
                glitch_baa_albaa = False
                if not glitch_baa[1]: 
                    glitch_baa = (
                        glitch_baa[0],
                        mas_pgc.ODDS_BAA,
                        glitch_baa[2]
                    )
                if glitch_baa[2] is None: 
                    glitch_baa = (
                        glitch_baa[0],
                        glitch_baa[1],
                        False
                    )
                
                
                if glitch_baa[1] == 1:
                    glitch_baa_albaa = True
            
            else: 
                glitch_baa = None
            
            
            if (glitch_wordscare_sound is not None
                and len(glitch_wordscare_sound) >= 2
                and glitch_wordscare_sound[0]):
                
                glitch_wordscare_alsound = False
                if not glitch_wordscare_sound[1]: 
                    glitch_wordscare_sound = (
                        glitch_wordscare_sound[0],
                        mas_pgc.ODDS_GLTICH_SOUND
                    )
                
                
                if glitch_wordscare_sound[1] == 1:
                    glitch_wordscare_alsound = True
            
            else: 
                glitch_wordscare_sound = None

        else: 
            glitch_wordscare = None


        if gather_words:
            from copy import deepcopy
            selected_words = list()


        if show_yuri:
            if (
                show_yuri_scary is not None
                and len(show_yuri_scary) >= 3
                and show_yuri_scary[0]
            ):
                
                
                seen_yuri_scary = False
                
                show_yuri_alscary = False
                if not show_yuri_scary[1]: 
                    show_yuri_scary = (
                        show_yuri_scary[0],
                        mas_pgc.ODDS_YURI_SCARY,
                        show_yuri_scary[2]
                    )
                if show_yuri_scary[2] is None: 
                    show_yuri_scary = (
                        show_yuri_scary[0],
                        show_yuri_scary[1],
                        False
                    )
                
                
                if show_yuri_scary[1] == 1:
                    show_yuri_alscary = True
            
            else: 
                show_yuri_scary = None


        else:
            show_yuri_scary = None
            show_yuri_cut = False


        if (show_eyes
                and len(show_eyes) >= 2
                and show_eyes[0]):
            
            if not show_eyes[1]: 
                show_eyes = (show_eyes[0], mas_pgc.ODDS_EYES)


        else:
            show_eyes = None


    if glitch_nb:
        scene bg notebook-glitch
    else:
        scene bg notebook






    if in_monika_mode:
        show m_sticker at sticker_right
    else:
        if show_sayori:
            show s_sticker at sticker_left
        if show_natsuki:
            show n_sticker at sticker_midleft
        if show_yuri:
            if show_yuri_cut:
                show y_sticker_cut at sticker_midright
                $ yuristicker = "y_sticker_cut"
            else:
                show y_sticker at sticker_midright
                $ yuristicker = "y_sticker"
        if show_monika:
            show m_sticker at sticker_right


    if trans_in:
        if trans_fast:
            with mas_dissolve_scene_full_fast
        else:
            with dissolve_scene_full
















    if music_filename != "BACK":

        if music_filename:
            python:
                renpy.music.play(
                    music_filename,
                    channel="music",
                    loop=True,
                    fadein=music_fadein
                )
        else:
            $ renpy.music.stop(channel="music", fadeout=music_fadeout)







    if show_poemhelp:
        call screen dialog("¡Es tiempo de escribir un poema!\n\nSelecciona palabras que creas que le gustarán a tu miembro\nfavorito del club. ¡Algo bueno podría ocurrir con a quien más\nle guste tu poema!", ok_action=Return())


    python:



        poemgame_glitch = False


        progress = 1


        numWords = total_words


        if in_stock_mode:
            points = {
                mas_pgc.SAYORI: 0,
                mas_pgc.NATSUKI: 0,
                mas_pgc.YURI: 0,
                mas_pgc.MONIKA: 0
            }


        if not in_monika_mode:
            from copy import deepcopy
            if poem_wordlist:
                wordlist = deepcopy(poem_wordlist.wordlist)
            else:
                
                
                
                
                
                show_monika = False
                
                wordlist = deepcopy(full_wordlist)








        done = False
        while not done:
            ystart = 160
            
            
            if one_counter:
                pstring = ""
                for i in range(progress):
                    pstring += "1"
            else:
                pstring = str(progress)
            
            
            ui.text(
                pstring + "/" + str(numWords),
                style="poemgame_text",
                xpos=810,
                ypos=80,
                color='#000'
            )
            
            
            for j in range(2):  
                if j == 0: x = 440
                else: x = 680
                ui.vbox()
                for i in range(5): 
                    
                    
                    if in_monika_mode:
                        
                        
                        if (glitch_wordscare
                            and (
                                glitch_wordscare_alscare or
                                random.randint(1,glitch_wordscare[1]) == 1
                            )):
                            
                            word = MASPoemWord(glitchtext(7), 0, 0, 0, 0, True)
                        
                        
                        elif glitch_words:
                            word = MASPoemWord(
                                glitchWord(
                                    "Monika", glitch_words[1], glitch_words[2]
                                ),
                                0, 0, 0, 0, False
                            )
                        
                        
                        else:
                            word = MASPoemWord("Monika", 0, 0, 0, 0, False)
                    
                    
                    else:
                        
                        
                        word = random.choice(wordlist)
                        wordlist.remove(word)
                        
                        
                        if (glitch_wordscare
                            and ( 
                                glitch_wordscare_alscare or
                                random.randint(1,glitch_wordscare[1]) == 1
                            )):
                            
                            word.word = glitchtext(len(word.word))
                            word.glitch = True
                        
                        
                        elif glitch_words:
                            word.word = glitchWord(
                                word.word, glitch_words[1], glitch_words[2]
                            )
                    
                    
                    ui.textbutton(
                        word.word,
                        clicked=ui.returns(word),
                        text_style="poemgame_text",
                        xpos=x,
                        ypos=i * 56 + ystart
                    )
                
                
                ui.close()
            
            
            t = ui.interact()
            
            
            if gather_words:
                selected_words.append(deepcopy(t))
            
            
            if glitch_wordscare:
                
                
                if not poemgame_glitch:
                    
                    if t.glitch:
                        poemgame_glitch = True
                        renpy.music.play(audio.t4g)
                        renpy.scene()
                        renpy.show("white")
                        renpy.show("y_sticker glitch", at_list=[sticker_glitch])
                
                
                elif poemgame_glitch:
                    if (glitch_baa
                        and (glitch_baa[2] or not played_baa)
                        and (
                            glitch_baa_albaa
                            or random.randint(1, glitch_baa[1]) == 1
                        )):
                        
                        renpy.play("gui/sfx/baa.ogg")
                        played_baa = True
                    
                    elif (glitch_wordscare_sound
                        and (
                            glitch_wordscare_alsound
                            or random.randint(
                                1, glitch_wordscare_sound[1]
                            ) == 1
                        )):
                        
                        renpy.play(gui.activate_sound_glitch)
            
            if not poemgame_glitch:
                if sel_sound:
                    renpy.play(sel_sound)
                
                
                if in_monika_mode and hop_monika:
                    
                    renpy.show("m_sticker hop")
                else:
                    word_winner = mas_fun.getWinner(
                        t,
                        show_sayori,
                        show_natsuki,
                        show_yuri,
                        show_monika,
                        mas=poem_wordlist is not None
                    )
                    
                    if show_monika and word_winner == mas_pgc.MONIKA:
                        renpy.show("m_sticker hop")
                    elif show_sayori and word_winner == mas_pgc.SAYORI:
                        renpy.show("s_sticker hop")
                    elif show_natsuki and word_winner == mas_pgc.NATSUKI:
                        renpy.show("n_sticker hop")
                    
                    elif show_yuri:
                        
                        if (show_yuri_scary and (
                                (
                                    show_yuri_scary[2]
                                    or not seen_yuri_scary
                                )
                                and (
                                    show_yuri_alscary
                                    or random.randint(
                                        1, show_yuri_scary[1]
                                    ) == 1
                                ))):
                            renpy.show(yuristicker + " hopg")
                        
                        
                        else:
                            renpy.show(yuristicker + " hop")
            
            
            if in_stock_mode:
                if show_sayori:
                    points[mas_pgc.SAYORI] += t.sPoint
                if show_natsuki:
                    points[mas_pgc.NATSUKI] += t.nPoint
                if show_yuri:
                    points[mas_pgc.YURI] += t.yPoint
                if show_monika:
                    points[mas_pgc.MONIKA] += t.mPoint
            
            
            progress += 1
            if progress > numWords:
                done = True


        results = None
        if in_stock_mode:
            
            
            if only_winner:
                
                
                largest = ""
                largestVal = 0
                for girl,points in points.iteritems():
                    if points > largestVal:
                        largest = girl
                        largestVal = points
                
                
                if gather_words:
                    results = (largest, largestVal, selected_words)
                else:
                    results = (largest, largestVal)
            
            else: 
                
                if gather_words:
                    results = points
                    results["words"] = selected_words
                
                else:
                    results = points


        else:
            if gather_words:
                results = selected_words


    if show_eyes and renpy.random.randint(1,show_eyes[1]) == 1:
        $ quick_menu = False
        play sound "sfx/eyes.ogg"
        stop music
        scene black with None
        show bg eyes_move
        pause 1.2
        hide bg eyes_move
        show bg eyes
        pause 0.5
        hide bg eyes
        show bg eyes_move
        pause 1.25
        hide bg eyes with None
        $ quick_menu = True





    if music_filename != "BACK":
        $ renpy.music.stop(channel="music",fadeout=music_fadeout)



    if trans_out:
        if trans_fast:
            show black as fadeout:
                alpha 0
                linear 0.5 alpha 1.0
            pause 0.5
        else:
            show black as fadeout:
                alpha 0
                linear 1.0 alpha 1.0
            pause 1.0
    return results






transform sticker_left:
    xcenter 70 yalign 0.9 subpixel True


transform sticker_midleft:
    xcenter 160 yalign 0.9 subpixel True


transform sticker_midright:
    xcenter 250 yalign 0.9 subpixel True


transform sticker_right:
    xcenter 340 yalign 0.9 subpixel True


image y_sticker_cut hopg:
    "gui/poemgame/y_sticker_2g.png"
    xoffset yuriOffset xzoom yuriZoom
    sticker_hop
    xoffset 0 xzoom 1
    "y_sticker_cut"


define mas_dissolve_scene_full_fast = MultipleTransition([
    False, Dissolve(0.5),
    Solid("#000"), Pause(0.5),
    Solid("#000"), Dissolve(0.5),
    True])
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
