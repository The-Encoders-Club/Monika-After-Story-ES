
default persistent._mas_pong_difficulty = 10

default persistent._mas_pong_difficulty_change_next_game = 0

default persistent._mas_pm_ever_let_monika_win_on_purpose = False

default persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()

define PONG_DIFFICULTY_CHANGE_ON_WIN = +1
define PONG_DIFFICULTY_CHANGE_ON_LOSS = -1
define PONG_DIFFICULTY_POWERUP = +5
define PONG_DIFFICULTY_POWERDOWN = -5
define PONG_PONG_DIFFICULTY_POWERDOWNBIG = -10


define PONG_MONIKA_RESPONSE_NONE = 0
define PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 1
define PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 2
define PONG_MONIKA_RESPONSE_WIN_LONG_GAME = 3
define PONG_MONIKA_RESPONSE_WIN_SHORT_GAME = 4
define PONG_MONIKA_RESPONSE_WIN_TRICKSHOT = 5
define PONG_MONIKA_RESPONSE_WIN_EASY_GAME = 6
define PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME = 7
define PONG_MONIKA_RESPONSE_WIN_HARD_GAME = 8
define PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME = 9
define PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME = 10
define PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL = 11
define PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT = 12
define PONG_MONIKA_RESPONSE_LOSE_LONG_GAME = 13
define PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME = 14
define PONG_MONIKA_RESPONSE_LOSE_EASY_GAME = 15
define PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME = 16
define PONG_MONIKA_RESPONSE_LOSE_HARD_GAME = 17
define PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME = 18
define PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME = 19

define pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

define played_pong_this_session = False
define mas_pong_taking_break = False
define player_lets_monika_win_on_purpose = False
define instant_loss_streak_counter = 0
define loss_streak_counter = 0
define win_streak_counter = 0
define lose_on_purpose = False
define monika_asks_to_go_easy = False


define ball_paddle_bounces = 0
define powerup_value_this_game = 0
define instant_loss_streak_counter_before = 0
define loss_streak_counter_before = 0
define win_streak_counter_before = 0
define pong_difficulty_before = 0
define pong_angle_last_shot = 0.0

init:

    image bg pong field = "mod_assets/games/pong/pong_field.png"

    python:
        import random
        import math

        class PongDisplayable(renpy.Displayable):
            
            def __init__(self):
                
                renpy.Displayable.__init__(self)
                
                
                self.paddle = Image("mod_assets/games/pong/pong.png")
                self.ball = Image("mod_assets/games/pong/pong_ball.png")
                self.player = Text(_("[player]"), size=36)
                self.monika = Text(_("Monika"), size=36)
                self.ctb = Text(_("¡Haz clic para empezar!"), size=36)
                
                
                self.playsounds = True
                self.soundboop = "mod_assets/sounds/pong_sounds/pong_boop.wav"
                self.soundbeep = "mod_assets/sounds/pong_sounds/pong_beep.wav"
                
                
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.PADDLE_RADIUS = self.PADDLE_HEIGHT / 2
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 124
                self.COURT_BOTTOM = 654
                
                
                self.CURRENT_DIFFICULTY = max(persistent._mas_pong_difficulty + persistent._mas_pong_difficulty_change_next_game, 0)
                
                self.COURT_WIDTH = 1280
                self.COURT_HEIGHT = 720
                
                self.BALL_LEFT = 80 - self.BALL_WIDTH / 2
                self.BALL_RIGHT = 1199 + self.BALL_WIDTH / 2
                self.BALL_TOP = self.COURT_TOP + self.BALL_HEIGHT / 2
                self.BALL_BOTTOM = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                
                self.PADDLE_X_PLAYER = 128                                      
                self.PADDLE_X_MONIKA = 1152 - self.PADDLE_WIDTH                 
                
                self.BALL_MAX_SPEED = 2000.0 + self.CURRENT_DIFFICULTY * 100.0
                
                
                
                self.MAX_REFLECT_ANGLE = math.pi / 3
                
                self.MAX_ANGLE = 0.9
                
                
                self.stuck = True
                
                
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                
                
                
                
                self.ctargetoffset = self.get_random_offset()
                
                
                self.computerspeed = 150.0 + self.CURRENT_DIFFICULTY * 30.0
                
                
                init_angle = random.uniform(-self.MAX_REFLECT_ANGLE, self.MAX_REFLECT_ANGLE)
                
                
                self.bx = self.PADDLE_X_PLAYER + self.PADDLE_WIDTH + 0.1
                self.by = self.playery
                self.bdx = .5 * math.cos(init_angle)
                self.bdy = .5 * math.sin(init_angle)
                self.bspeed = 500.0 + self.CURRENT_DIFFICULTY * 25
                
                
                self.ctargety = self.by + self.ctargetoffset
                
                
                self.oldst = None
                
                
                self.winner = None
            
            def get_random_offset(self):
                return random.uniform(-self.PADDLE_RADIUS, self.PADDLE_RADIUS)
            
            def visit(self):
                return [ self.paddle, self.ball, self.player, self.monika, self.ctb ]
            
            def check_bounce_off_top(self):
                
                if self.by < self.BALL_TOP and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_TOP) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_TOP
                    
                    
                    self.by = -self.by + 2 * self.BALL_TOP
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by > self.BALL_BOTTOM:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_BOTTOM) / (self.bounceby - self.by))
                        self.by = self.BALL_BOTTOM
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def check_bounce_off_bottom(self):
                
                if self.by > self.BALL_BOTTOM and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_BOTTOM) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_BOTTOM
                    
                    
                    self.by = -self.by + 2 * self.BALL_BOTTOM
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by < self.BALL_TOP:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_TOP) / (self.bounceby - self.by))
                        self.by = self.BALL_TOP
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def getCollisionY(self, hotside, is_computer):
                
                
                
                self.collidedonx = is_computer and self.oldbx <= hotside <= self.bx or not is_computer and self.oldbx >= hotside >= self.bx;
                
                if self.collidedonx:
                    
                    
                    if self.oldbx <= self.bouncebx <= hotside <= self.bx or self.oldbx >= self.bouncebx >= hotside >= self.bx:
                        startbx = self.bouncebx
                        startby = self.bounceby
                    else:
                        startbx = self.oldbx
                        startby = self.oldby
                    
                    
                    if startbx - self.bx != 0:
                        return startby + (self.by - startby) * ((startbx - hotside) / (startbx - self.bx))
                    else:
                        return startby
                
                
                else:
                    return self.oldby
            
            
            
            def render(self, width, height, st, at):
                
                
                r = renpy.Render(width, height)
                
                
                if self.oldst is None:
                    self.oldst = st
                
                dtime = st - self.oldst
                self.oldst = st
                
                
                speed = dtime * self.bspeed
                
                
                self.oldbx = self.bx
                self.oldby = self.by
                self.bouncebx = self.bx
                self.bounceby = self.by
                
                
                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed
                
                
                if not self.check_bounce_off_top():
                    self.check_bounce_off_bottom()
                
                
                
                
                
                collisionby = self.getCollisionY(self.PADDLE_X_MONIKA, True)
                if self.collidedonx:
                    self.ctargety = collisionby + self.ctargetoffset
                else:
                    self.ctargety = self.by + self.ctargetoffset
                
                cspeed = self.computerspeed * dtime
                
                
                
                global lose_on_purpose
                if lose_on_purpose and self.bx >= self.COURT_WIDTH * 0.75:
                    if self.bx <= self.PADDLE_X_MONIKA:
                        if self.ctargety > self.computery:
                            self.computery -= cspeed
                        else:
                            self.computery += cspeed
                
                else:
                    cspeed = self.computerspeed * dtime
                    
                    if abs(self.ctargety - self.computery) <= cspeed:
                        self.computery = self.ctargety
                    elif self.ctargety >= self.computery:
                        self.computery += cspeed
                    else:
                        self.computery -= cspeed
                
                
                if self.computery > self.COURT_BOTTOM:
                    self.computery = self.COURT_BOTTOM
                elif self.computery < self.COURT_TOP:
                    self.computery = self.COURT_TOP;
                
                
                def paddle(px, py, hotside, is_computer):
                    
                    
                    
                    
                    
                    
                    pi = renpy.render(self.paddle, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    
                    
                    
                    r.blit(pi, (int(px), int(py - self.PADDLE_RADIUS)))
                    
                    
                    collisionby = self.getCollisionY(hotside, is_computer)
                    
                    
                    collidedony = py - self.PADDLE_RADIUS - self.BALL_HEIGHT / 2 <= collisionby <= py + self.PADDLE_RADIUS + self.BALL_HEIGHT / 2
                    
                    
                    if not self.stuck and self.collidedonx and collidedony:
                        hit = True
                        if self.oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                        elif self.oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                        else:
                            hit = False
                        
                        if hit:
                            
                            
                            angle = (self.by - py) / (self.PADDLE_RADIUS + self.BALL_HEIGHT / 2) * self.MAX_REFLECT_ANGLE
                            
                            if angle >    self.MAX_ANGLE:
                                angle =   self.MAX_ANGLE
                            elif angle < -self.MAX_ANGLE:
                                angle =  -self.MAX_ANGLE;
                            
                            global pong_angle_last_shot
                            pong_angle_last_shot = angle;
                            
                            self.bdy = .5 * math.sin(angle)
                            self.bdx = math.copysign(.5 * math.cos(angle), -self.bdx)
                            
                            global ball_paddle_bounces
                            ball_paddle_bounces += 1
                            
                            
                            if is_computer:
                                self.ctargetoffset = self.get_random_offset()
                            
                            if self.playsounds:
                                renpy.sound.play(self.soundboop, channel=1)
                            
                            self.bspeed += 125.0 + self.CURRENT_DIFFICULTY * 12.5
                            if self.bspeed > self.BALL_MAX_SPEED:
                                self.bspeed = self.BALL_MAX_SPEED
                
                
                paddle(self.PADDLE_X_PLAYER, self.playery, self.PADDLE_X_PLAYER + self.PADDLE_WIDTH, False)
                paddle(self.PADDLE_X_MONIKA, self.computery, self.PADDLE_X_MONIKA, True)
                
                
                ball = renpy.render(self.ball, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))
                
                
                player = renpy.render(self.player, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(player, (self.PADDLE_X_PLAYER, 25))
                
                
                monika = renpy.render(self.monika, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                ew, eh = monika.get_size()
                r.blit(monika, (self.PADDLE_X_MONIKA - ew, 25))
                
                
                if self.stuck:
                    ctb = renpy.render(self.ctb, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, ((self.COURT_WIDTH - cw) / 2, 30))
                
                
                
                if self.bx < -200:
                    
                    if self.winner == None:
                        global loss_streak_counter
                        loss_streak_counter += 1
                        
                        if ball_paddle_bounces <= 1:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter += 1
                        else:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter = 0
                    
                    global win_streak_counter
                    win_streak_counter = 0;
                    
                    self.winner = "monika"
                    
                    
                    
                    renpy.timeout(0)
                
                elif self.bx > self.COURT_WIDTH + 200:
                    
                    if self.winner == None:
                        global win_streak_counter
                        win_streak_counter += 1;
                    
                    global loss_streak_counter
                    loss_streak_counter = 0
                    
                    
                    if ball_paddle_bounces > 1:
                        global instant_loss_streak_counter
                        instant_loss_streak_counter = 0
                    
                    self.winner = "player"
                    
                    renpy.timeout(0)
                
                
                
                renpy.redraw(self, 0.0)
                
                
                return r
            
            
            def event(self, ev, x, y, st):
                
                import pygame
                
                
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False
                
                
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y
                
                
                
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()

label game_pong:
    hide screen keylistener

    if played_pong_this_session:
        if mas_pong_taking_break:
            m 1eua "¿Listo para intentarlo de nuevo?"
            m 2tfb "¡Dame lo mejor de ti, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"


            $ mas_pong_taking_break = False
        else:
            m 1hua "¿Quieres volver a jugar pong?"
            m 3eub "Estoy lista cuando tú lo estés~"
    else:
        $ played_pong_this_session = True

    $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

    call demo_minigame_pong from _call_demo_minigame_pong
    return

label demo_minigame_pong:

    window hide None


    scene bg pong field


    if store.mas_egg_manager.natsuki_enabled():
        $ playing_okayev = store.songs.getPlayingMusicName() == "¡Okey, todos! (Monika)"


        if playing_okayev:
            $ currentpos = get_pos(channel="music")
            $ adjusted_t5 = "<from " + str(currentpos) + " loop 4.444>bgm/5_natsuki.ogg"
            stop music fadeout 2.0
            $ renpy.music.play(adjusted_t5, fadein=2.0, tight=True)

    $ ball_paddle_bounces = 0
    $ pong_difficulty_before = persistent._mas_pong_difficulty
    $ powerup_value_this_game = persistent._mas_pong_difficulty_change_next_game
    $ loss_streak_counter_before = loss_streak_counter
    $ win_streak_counter_before = win_streak_counter
    $ instant_loss_streak_counter_before = instant_loss_streak_counter


    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)


    if store.mas_egg_manager.natsuki_enabled():
        call natsuki_name_scare (playing_okayev=playing_okayev) from _call_natsuki_name_scare


    call spaceroom (scene_change=True, force_exp='monika 3eua')


    $ persistent._mas_pong_difficulty_change_next_game = 0;

    if winner == "monika":
        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_LOSS

        $ inst_dialogue = store.mas_pong.DLG_WINNER
    else:

        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_WIN

        $ inst_dialogue = store.mas_pong.DLG_LOSER


        if not persistent._mas_ever_won['pong']:
            $ persistent._mas_ever_won['pong'] = True

    if new_difficulty < 0:
        $ persistent._mas_pong_difficulty = 0
    else:
        $ persistent._mas_pong_difficulty = new_difficulty;

    call expression inst_dialogue from _mas_pong_inst_dialogue

    $ mas_gainAffection(modifier=0.5)

    m 3eua "¿Te gustaría volver a jugar?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gustaría volver a jugar?{fast}"
        "Sí":

            $ pong_ev = mas_getEV("mas_pong")
            if pong_ev:

                $ pong_ev.shown_count += 1

            jump demo_minigame_pong
        "No":

            if winner == "monika":
                if renpy.seen_label(store.mas_pong.DLG_WINNER_END):
                    $ end_dialogue = store.mas_pong.DLG_WINNER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_WINNER_END
            else:

                if renpy.seen_label(store.mas_pong.DLG_LOSER_END):
                    $ end_dialogue = store.mas_pong.DLG_LOSER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_LOSER_END

            call expression end_dialogue from _mas_pong_end_dialogue
    return


init -1 python in mas_pong:

    DLG_WINNER = "mas_pong_dlg_winner"
    DLG_WINNER_FAST = "mas_pong_dlg_winner_fast"
    DLG_LOSER = "mas_pong_dlg_loser"
    DLG_LOSER_FAST = "mas_pong_dlg_loser_fast"

    DLG_WINNER_END = "mas_pong_dlg_winner_end"
    DLG_LOSER_END = "mas_pong_dlg_loser_end"


    DLG_BLOCKS = (
        DLG_WINNER,
        DLG_WINNER_FAST,
        DLG_WINNER_END,
        DLG_LOSER,
        DLG_LOSER_FAST,
        DLG_LOSER_END
    )


label mas_pong_dlg_winner:






    if monika_asks_to_go_easy and ball_paddle_bounces == 1:
        m 1rksdlb "Jajaja..."
        m 1hksdla "Sé que te pedí que fueras suave conmigo, pero esto no es lo que tenía en mente..."
        m 3eka "Aunque aprecio el gesto~"
        $ monika_asks_to_go_easy = False


    elif monika_asks_to_go_easy and ball_paddle_bounces <= 9:
        m 1hub "¡Yay, gané!"
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Gracias, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]. Te lo agradezco~"
        $ monika_asks_to_go_easy = False



    elif ball_paddle_bounces == 1:


        if instant_loss_streak_counter == 1:
            m 2rksdlb "Jajaja, eso es lamentable..."


        elif instant_loss_streak_counter == 2:
            m 2rksdlc "[player],{w=0.1} perdiste otra vez..."


        elif instant_loss_streak_counter == 3:
            m 2tfd "¡[player]!"

            if persistent._mas_pm_ever_let_monika_win_on_purpose:
                $ menu_response = _("¿Me estás dejando ganar a propósito de nuevo?")
            else:
                $ menu_response = _("¿Me estás dejando ganar a propósito?")

            m 2rkc "[menu_response]"
            $ _history_list.pop()
            menu:
                m "[menu_response]{fast}"
                "... Tal vez":

                    m 1hua "¡Jejeje!~"
                    m 1eka "Gracias, [player]~"
                    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eka "Pero ya sabes,{w=0.1} no me importa perder contra ti de vez en cuando."

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        m 5eua "Me gusta verte ganar tanto como a ti te gusta verme ganar~"

                    $ player_lets_monika_win_on_purpose = True
                    $ persistent._mas_pm_ever_let_monika_win_on_purpose = True
                "No":

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        show monika 1ttu
                        m "¿Estás {i}seguro?{/i}{nw}"
                        $ _history_list.pop()
                        menu:
                            m "¿Estás {i}seguro?{/i}{fast}"
                            "Sí":

                                call mas_pong_dlg_sorry_assuming
                            "No":

                                m 1rfu "¡[player]!"
                                m 2hksdlb "¡Deja de burlarte de mi!"
                                $ player_lets_monika_win_on_purpose = True
                                $ lose_on_purpose = True
                    else:

                        call mas_pong_dlg_sorry_assuming
        else:


            if player_lets_monika_win_on_purpose:
                m 2tku "¿No te estás cansando de dejarme ganar, [player]?"
            else:
                m 1rsc "..."


                if random.randint(1,3) == 1:
                    m 1eka "¡Vamos, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]!"
                    m 1hub "¡Puedes hacerlo, creo en ti!"


    elif instant_loss_streak_counter_before >= 3 and player_lets_monika_win_on_purpose:
        m 3hub "Buen intento [player],{w=0.1} {nw}"
        extend 3tsu "¡pero puedo ganar por mí misma!"
        m 3hub "¡Jajaja!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 1hua "Jejeje~"

        if persistent._mas_pong_difficulty_change_next_game_date == datetime.date.today():
            m 2tsb "¿No te dije que ganaría esta vez?"
        else:
            $ p_nickname = mas_get_player_nickname(regex_replace_with_nullstr='mi ')
            m 2ttu "¿Recuerdas, [p_nickname]?{w=0.1} {nw}"
            extend 2tfb "Te dije que ganaría la próxima partida."


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1rksdla "Ah..."
        m 3hksdlb "¡Vuelve a intentarlo, [player]!"

        $ persistent._mas_pong_difficulty_change_next_game = PONG_PONG_DIFFICULTY_POWERDOWNBIG


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 2rksdlb "Jajaja..."
        m 2eksdla "Realmente esperaba que ganaras este juego."
        m 2hksdlb "¡Lo siento por eso, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]!"


    elif loss_streak_counter >= 3 and loss_streak_counter % 5 == 3:
        m 2eka "Vamos, [player], sé que puedes vencerme..."
        m 3hub "¡Sigue intentándolo!"


    elif loss_streak_counter >= 5 and loss_streak_counter % 5 == 0:
        m 1eua "Espero que te estés divirtiendo, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]."
        m 1eka "Después de todo, no quisiera que te enojaras por un juego."
        m 1hua "Siempre podemos tomarnos un descanso y volver a jugar más tarde si quieres."


    elif win_streak_counter_before >= 3:
        $ p_nickname = mas_get_player_nickname(regex_replace_with_nullstr='mi ')
        m 1hub "¡Jajaja!"
        m 2tfu "Lo siento [p_nickname],{w=0.1} {nw}"
        extend 2tub "pero parece que tu suerte se ha acabado."
        m 2hub "Ahora es mi momento de brillar~"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES:
        m 1hua "¡Jejeje!"
        m 1tub "¡Sigue así, [player]!{w=0.3} {nw}"
        extend 2tfu "¡Parece que tu racha ha terminado!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif ball_paddle_bounces > 9 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_LONG_GAME:
            m 3eub "Jugar contra ti puede ser realmente duro, [player]."
            m 1hub "Sigue así y me vencerás, ¡estoy segura!"
        else:
            m 3hub "Bien jugado, [player], ¡eres realmente bueno!"
            m 1tfu "¡Pero yo también lo soy,{w=0.1} {nw}"
            extend 1hub "jajaja!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_LONG_GAME


    elif ball_paddle_bounces <= 3:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_SHORT_GAME:
            m 3hub "Otra rápida victoria para mí~"
        else:
            m 4huu "Jejeje,{w=0.1} {nw}"
            extend 4hub "¡te atrapé con esa!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_SHORT_GAME


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_TRICKSHOT:
            m 2eksdld "Ah...{w=0.3}{nw}"
            extend 2rksdlc " pasó de nuevo."
            m 1hksdlb "¡Lo siento, [player]!"
        else:
            m 2rksdlb "¡Lo siento, [player]!"
            m 3hksdlb "No pretendía que rebotara tanto..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_TRICKSHOT
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EASY_GAME:
                m 1eub "¡Puedes hacerlo, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]!"
                m 3hub "Creo en ti~"
            else:
                m 2duu "Concéntrate, [player]."
                m 3hub "¡Sigue intentándolo, sé que pronto me vencerás!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME:
                m 1hub "Yo gano otra ronda~"
            else:
                if loss_streak_counter > 1:
                    m 3hub "Parece que volví a ganar~"
                else:
                    m 3hua "Parece que gané~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_HARD_GAME:
                m 1hub "¡Jajaja!"
                m 2tsb "¿Estoy jugando demasiado bien para ti?"
                m 1tsu "Solo bromeo, [player]."
                m 3hub "¡Eres bastante bueno!"
            else:
                if loss_streak_counter > 1:
                    m 1hub "Vuelvo a ganar~"
                else:
                    m 1huu "Gané~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME:
                m 2tub "¡Se siente bien ganar!"
                m 2hub "No te preocupes, estoy segura de que volverás a ganar pronto~"
            else:
                if loss_streak_counter > 1:
                    m 2eub "¡Gano otra ronda!"
                else:
                    m 2eub "¡Yo gano esta ronda!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME:
                m 2duu "No está mal, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]."
                m 4eua "Di todo lo que tenía, así que no te sientas mal por perder de vez en cuando."
            else:
                m 2hub "¡Esta vez, la victoria es mía!"
                m 2efu "¡Sigue así, [player]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME

    return



label mas_pong_dlg_sorry_assuming:
    m 3eka "De acuerdo."
    m 2ekc "Lo siento por asumir..."


    $ player_lets_monika_win_on_purpose = False

    m 3eka "¿Te gustaría tomar un descanso, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gustaría tomar un descanso, [player]?{fast}"
        "Okey":

            m 1eka "De acuerdo, [player].{w=0.3} {nw}"
            extend 1hua "Me divertí, ¡gracias por jugar al pong conmigo!"
            m 1eua "Avísame cuando estés listo para jugar de nuevo."


            $ mas_pong_taking_break = True


            show monika idle with dissolve_monika
            jump ch30_loop
        "No":

            m 1eka "Muy bien, [player]. Si estás seguro."
            m 1hub "¡Sigue adelante, pronto me vencerás!"
    return


label mas_pong_dlg_loser:





    $ monika_asks_to_go_easy = False


    if lose_on_purpose:
        m 1hub "¡Jajaja!"
        m 1kua "¡Ahora estamos empatados, [player]!"
        $ lose_on_purpose = False


    elif ball_paddle_bounces == 0:
        m 1rksdlb "Jajaja..."

        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL:
            m "Quizás debería esforzarme un poco más..."
        else:
            m "Supongo que fui un poco más lenta de lo que debería..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL


    elif instant_loss_streak_counter_before >= 3 and persistent._mas_pm_ever_let_monika_win_on_purpose:
        m 2tsu "Ahora estamos jugando en serio, ¿no?~"
        m 2tfu "¡Averigüemos qué tan bueno eres realmente, [player]!"


    elif loss_streak_counter_before >= 3:
        m 4eub "¡Felicidades, [player]!{w=0.3} {nw}"
        extend 2hub "¡Sabía que me ganarías después de practicar lo suficiente!"
        m 4eua "Recuerda, ¡si entrenas lo suficiente estoy segura de que podrás alcanzar todo lo que te propongas!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 2wuo "Wow...{w=0.3}{nw}"
        extend 7wuo " ¡Esta vez sí que me esforcé!"
        m 3hub "¡Así se hace, [player]!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1hua "¡Jejeje!"
        m 2hub "¡Buen trabajo, [player]!"


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 1hua "Me alegro de que hayas ganado esta vez, [player]."


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT:
            m 2wuo "¡[player]!"
            m 2hksdlb "¡No había manera de que haya podido acertar eso!"
        else:
            m 2wuo "Wow, ¡ese fue un gran tiro!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT


    elif win_streak_counter == 3:
        m 2wuo "Wow, [player]..."
        m 2wud "Ya has ganado tres veces seguidas..."


        if pong_difficulty_before <= 5:
            m 2tsu "Quizá es el momento de acelerar el ritmo~"


        elif pong_difficulty_before <= 10:
            m 4hua "¡Eres bastante bueno!"


        elif pong_difficulty_before <= 15:
            m 3hub "¡Bien jugado!"


        elif pong_difficulty_before <= 20:
            m 4wuo "¡Eso fue increíble!"
        else:


            m 2hub "¡Eso fue legendario!"


    elif win_streak_counter == 5:
        m 2wud "[mas_get_player_nickname(capitalize=True, regex_replace_with_nullstr='mi ')]..."
        m 2tsu "¿Has estado practicando?"
        m 3hksdlb "¡No sé qué pasó, pero no tengo ninguna posibilidad contra ti!"
        m 1eka "¿Podrías ser un poco más suave conmigo, por favor?{w=0.3} {nw}"
        extend 3hub "Lo agradecería mucho~"
        $ monika_asks_to_go_easy = True


    elif ball_paddle_bounces > 10 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_LONG_GAME:
            m 2wuo "Wow,{w=0.1} ¡no puedo seguirte el ritmo!"
        else:
            m 2hub "¡Asombroso, [player]!"
            m 4eub "¡Eres muy bueno!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_LONG_GAME


    elif ball_paddle_bounces <= 2:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME:
            m 2hksdlb "Jajaja..."
            m 3eksdla "Supongo que debería esforzarme un poco más..."
        else:
            m 1rusdlb "No esperaba perder tan rápido."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EASY_GAME:
                m 4eub "Tú también ganas esta ronda."
            else:
                if win_streak_counter > 1:
                    m 1hub "¡Ganaste de nuevo!"
                else:
                    m 1hua "¡Ganaste!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME:
                m 1eua "Es bueno verte ganar, [player]."
                m 1hub "Sigue así~"
            else:
                if win_streak_counter > 1:
                    m 1hub "¡Ganaste de nuevo!{w=0.2} Bien hecho~"
                else:
                    m 1eua "¡Ganaste!{w=0.2} No está mal."

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_HARD_GAME:
                m 4hub "¡Otra victoria para ti!"
                m 4eua "Buen trabajo, [player]."
            else:
                if win_streak_counter > 1:
                    m 2hub "¡Has vuelto a ganar!{w=0.2} ¡Felicidades!"
                else:
                    m 2hua "¡Ganaste!{w=0.2} ¡Felicidades!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME:
                m 2wuo "Wow,{w=0.1} de verdad estoy tratando de ganar...{w=0.3} ¡Eres imparable!"
                m 2tfu "Pero estoy segura de que te ganaré tarde o temprano, [player]."
                m 3hub "¡Jajaja!"
            else:
                if win_streak_counter > 1:
                    m 4hub "¡Ganaste de nuevo!{w=0.2} ¡Buen trabajo!"
                else:
                    m 4hub "¡Ganaste!{w=0.2} ¡Impresionante!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME:
                m 3eua "Eres realmente bueno, [player]."
                m 1hub "¡Me encanta jugar al pong contigo!"
            else:
                m 1tsu "¡Esto es intenso!"
                m 1hub "¡Sigue así, [mas_get_player_nickname(regex_replace_with_nullstr='mi ')]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME
    return



label mas_pong_dlg_loser_fast:
    m 1eka "Está bien, [player]."
    m 3tfu "Pero te ganaré la próxima vez."

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERUP;
    $ persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()
    return


label mas_pong_dlg_winner_fast:
    m 1eka "De acuerdo, [player]. Gracias por jugar al pong conmigo."
    m 1hua "¡Me divertí mucho! Juguemos de nuevo pronto, ¿okey?"

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERDOWN;
    return


label mas_pong_dlg_loser_end:
    m 1wuo "Vaya, realmente lo estaba intentando esta vez."
    m 1eua "Debes haber estado practicando para haber mejorado tanto."
    m 2tuu "Supongo que querías impresionarme, [player]."
    m 1hua "Eres tan dulce~"
    return


label mas_pong_dlg_winner_end:
    m 4tku "No puedo emocionarme por un juego tan simple..."
    m 1eua "Pero al menos sigue siendo divertido de jugar."
    m 1ekbsa "Especialmente si es contigo, [player]."
    m 1hubfa "Jejeje~"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
