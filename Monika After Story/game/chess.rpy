
default persistent._mas_chess_stats = {
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "practice_wins": 0,
    "practice_losses": 0,
    "practice_draws": 0
}




default persistent._mas_chess_difficulty = (0, 1)


default persistent._mas_chess_quicksave = ""




default persistent._mas_chess_dlg_actions = defaultdict(int)


default persistent._mas_chess_timed_disable = None


default persistent._mas_chess_3_edit_sorry = False


default persistent._mas_chess_mangle_all = False


default persistent._mas_chess_skip_file_checks = False


init python in mas_chess:
    import os
    import chess.pgn
    import store.mas_ui as mas_ui
    import store
    import random

    CHESS_SAVE_PATH = "/chess_games/"
    CHESS_SAVE_EXT = ".pgn"
    CHESS_SAVE_NAME = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789"
    CHESS_PROMPT_FORMAT = "{0} | {1} | Turn: {2} | You: {3}"


    MODE_NORMAL = "normal_chess"
    MODE_BAD_CHESS = "badchess"
    MODE_960 = "chess960"


    REL_DIR = "chess_games/"

    CHESS_MENU_WAIT_VALUE = "MATTE"
    CHESS_MENU_WAIT_ITEM = (
        _("No puedo tomar esta decisión ahora mismo..."),
        CHESS_MENU_WAIT_VALUE,
        False,
        False,
        20
    )

    CHESS_NO_GAMES_FOUND = "NOGAMES"


    del_files = (
        "chess.rpyc",
    )


    gt_files = (
        "definitions.rpyc",
        "event-handler.rpyc",
        "script-topics.rpyc",
        "script-introduction.rpyc",
        "script-story-events.rpyc",
        "zz_pianokeys.rpyc",
        "zz_music_selector.rpyc"
    )


    IS_ONGOING = '*'


    CHESS_GAME_CONT = "USHO"



    CHESS_GAME_BACKUP = "foundyou"



    CHESS_GAME_FILE = "file"


    loaded_game_filename = None





    QS_LOST = 0




    QF_LOST_OFCN = 1




    QF_LOST_MAYBE = 2




    QF_LOST_ACDNT = 3




    QF_EDIT_YES = 4



    QF_EDIT_NO = 5


    PIECE_POOL = ('r', 'n', 'p', 'q', 'k', 'b')


    BASE_FEN = "{black_pieces_back}/{black_pieces_front}/8/8/8/8/{white_pieces_front}/{white_pieces_back} w - - 0 1"

    PIECE_POINT_MAP = {
        "1": 0,
        "p": 1,
        "n": 3,
        "b": 3,
        "r": 5,
        "q": 9
    }


    LOWEST_SIDE_WORTH = 39


    HIGHEST_SIDE_WORTH = 70

    def _checkInProgressGame(pgn_game, mth):
        """
        Checks if the given pgn game is valid and in progress.

        IN:
            pgn_game - pgn game to check
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            SEE isInProgressGame
        """
        if pgn_game is None:
            return None
        
        if pgn_game.headers["Result"] != "*":
            return None
        
        
        if pgn_game.headers["White"] == mth:
            the_player = "Negras"
        elif pgn_game.headers["Black"] == mth:
            the_player = "Blancas"
        else: 
            return None
        
        
        
        
        board = pgn_game.board()
        for move in pgn_game.main_line():
            board.push(move)
        
        return (
            CHESS_PROMPT_FORMAT.format(
                pgn_game.headers["Date"].replace(".","-"),
                pgn_game.headers["Event"],
                board.fullmove_number,
                the_player
            ),
            pgn_game
        )

    def isInProgressGame(filename, mth):
        """
        Checks if the pgn game with the given filename is valid and
        in progress.

        IN:
            filename - filename of the pgn game
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            tuple of the following format:
                [0]: Text to display on button
                [1]: chess.pgn.Game of the game
            OR NONE if this is not a valid pgn game
        """
        if filename[-4:] != CHESS_SAVE_EXT:
            return None
        
        pgn_game = None
        with open(
            os.path.normcase(CHESS_SAVE_PATH + filename),
            "r"
        ) as loaded_game:
            pgn_game = chess.pgn.read_game(loaded_game)
        
        return _checkInProgressGame(pgn_game, mth)

    def _increment_chess_difficulty():
        """
        Increments chess difficulty
        """
        level, sublevel = store.persistent._mas_chess_difficulty
        
        if sublevel == 5 and level < 9:
            level += 1
            sublevel = 1
        
        elif sublevel < 5:
            sublevel += 1
        
        else:
            return
        
        store.persistent._mas_chess_difficulty = (level, sublevel)

    def _decrement_chess_difficulty():
        """
        Decrements chess difficulty
        """
        level, sublevel = store.persistent._mas_chess_difficulty
        if sublevel == 1 and level > 0:
            level -= 1
            sublevel = 5
        
        elif sublevel > 1:
            sublevel -= 1
        
        else:
            return
        
        store.persistent._mas_chess_difficulty = (level, sublevel)

    def _get_player_color(loaded_game):
        """
        Gets player color

        IN:
            loaded_game - pgn representing the loaded game

        OUT:
            The player's color
        """
        if loaded_game.headers["White"] == store.mas_monika_twitter_handle:
            return store.chess.BLACK
        return store.chess.WHITE

    def _get_piece_chance(piece_type, selected_pieces_count_dict, available_points):
        """
        Gets the piece chance and returns the piece and weight in tuple form for a `mas_utils.weightedChoice` selection

        IN:
            piece_type - type of the piece ('b', 'r', 'n', 'q')

        OUT:
            tuple - (piece_type, weight) of the piece
        """
        prelim_value = (float(available_points) / PIECE_POINT_MAP[piece_type]) - selected_pieces_count_dict[piece_type]
        
        return (
            piece_type,
            prelim_value if prelim_value > 0 else 1
        )

    def select_piece(remaining_points, selected_pieces_count_dict):
        """
        Selects a piece according to random

        IN:
            remaining_points - amount of points left to be allocated

        OUT:
            a chess piece (str) based on available
        """
        
        piece_pool = list()
        
        if remaining_points >= 3:
            piece_pool.extend([
                _get_piece_chance('b', selected_pieces_count_dict, remaining_points),
                _get_piece_chance('n', selected_pieces_count_dict, remaining_points)
            ])
            
            if remaining_points >= 5:
                piece_pool.append(_get_piece_chance('r', selected_pieces_count_dict, remaining_points))
                
                if remaining_points >= 9:
                    piece_pool.append(_get_piece_chance('q', selected_pieces_count_dict, remaining_points))
            
            
            selected_piece = store.mas_utils.weightedChoice(piece_pool)
            selected_pieces_count_dict[selected_piece] += 1
            
            return selected_piece
        
        return 'p'

    def _gen_side(white=True, max_side_value=14):
        """
        Generates a player's side

        IN:
            white - whether or not we should generate for white
                (Default: True)
            max_side_value - The current upper limit for piece selection
                (Default: 14 -- minimum weight, most pieces are pawns)

        OUT:
            2 strings representing a random assortment of pieces (front row and back row)
        """
        king_pos = random.randint(0, 7)
        
        back_row = list()
        front_row = list()
        
        
        selected_pieces_count = {
            'q': 0,
            'r': 0,
            'n': 0,
            'b': 0
        }
        
        side_indeces = range(0, 16)
        random.shuffle(side_indeces)
        
        
        max_side_value -= 14
        
        for ind in side_indeces:
            if ind == king_pos:
                piece_to_add = 'k'
            
            else:
                piece_to_add = select_piece(max_side_value, selected_pieces_count)
                
                max_side_value -= PIECE_POINT_MAP[piece_to_add] - 1
            
            
            if white:
                piece_to_add = piece_to_add.capitalize()
            
            
            if ind < 8:
                back_row.append(piece_to_add)
            else:
                front_row.append(piece_to_add)
        
        
        random.shuffle(front_row)
        random.shuffle(back_row)
        
        
        if not white:
            back_row, front_row = front_row, back_row
        
        return "".join(front_row), "".join(back_row)

    def _validate_sides(white_front, white_back, black_front, black_back):
        """
        Validates sides for really bad chess
        so we don't end up in a check/check mate after the first turn

        IN:
            white_front - front row for white
            white_back - back row for white
            black_front - front row for black
            black_back - back row for black

        OUT:
            boolean, whether or not both sides are good to go
        """
        def validate(king_id, enemy_front):
            """
            Hardcoded validator, can't really think about anything better

            IN:
                king_id - id of the king
                enemy_front - opposide to king front row

            OUT:
                boolead, whether or not this king is safe *for now*
            """
            queen = "q"
            queen_or_bishop = ("q", "b")
            if (
                enemy_front[king_id].lower() in (queen, "r")
                or (
                    king_id > 0
                    and enemy_front[king_id - 1].lower() == queen
                )
                or (
                    king_id < 7
                    and enemy_front[king_id + 1].lower() == queen
                )
                or (
                    king_id == 0
                    and (
                        enemy_front[5].lower() in queen_or_bishop
                        or enemy_front[6].lower() in queen_or_bishop
                    )
                )
                or (
                    king_id == 1
                    and (
                        enemy_front[5].lower() in queen_or_bishop
                        or enemy_front[6].lower() in queen_or_bishop
                        or enemy_front[7].lower() in queen_or_bishop
                    )
                )
                or (
                    king_id == 3
                    and (
                        enemy_front[6].lower() in queen_or_bishop
                        or enemy_front[7].lower() in queen_or_bishop
                    )
                )
                or (
                    king_id == 5
                    and (
                        enemy_front[0].lower() in queen_or_bishop
                        or enemy_front[1].lower() in queen_or_bishop
                    )
                )
                or (
                    king_id == 6
                    and (
                        enemy_front[0].lower() in queen_or_bishop
                        or enemy_front[1].lower() in queen_or_bishop
                        or enemy_front[2].lower() in queen_or_bishop
                    )
                )
                or (
                    king_id == 7
                    and (
                        enemy_front[1].lower() in queen_or_bishop
                        or enemy_front[2].lower() in queen_or_bishop
                    )
                )
            ):
                return False
            return True
        
        white_king_id = white_back.index("K")
        white_is_good = validate(white_king_id, black_front)
        
        black_king_id = black_back.index("k")
        black_is_good = validate(black_king_id, white_front)
        
        return white_is_good and black_is_good

    def generate_random_fen(is_player_white=True):
        """
        Generates a random fen

        IN:
            is_player_white - whether or not the player is playing white this game
        """
        
        difficulty = store.persistent._mas_chess_difficulty[0] * 6 + store.persistent._mas_chess_difficulty[1]
        
        p_value_adj = int(round(-((float(difficulty) - 27)**3) / 984))
        m_value_adj = -p_value_adj
        
        delta = abs(p_value_adj)
        
        base_piece_value = random.randint(LOWEST_SIDE_WORTH, HIGHEST_SIDE_WORTH)
        
        
        max_piece_value = max(min(base_piece_value + p_value_adj, HIGHEST_SIDE_WORTH), LOWEST_SIDE_WORTH)
        
        
        
        monika_max_piece_value =  max(min(base_piece_value + m_value_adj, HIGHEST_SIDE_WORTH), LOWEST_SIDE_WORTH)
        
        good_to_go = False
        attempts = 0
        while (
            not good_to_go
            
            and attempts < 10
        ):
            attempts += 1
            player_first_row, player_second_row = _gen_side(is_player_white, max_piece_value)
            monika_first_row, monika_second_row = _gen_side(not is_player_white, monika_max_piece_value)
            
            if is_player_white:
                white_front = player_first_row
                white_back = player_second_row
                black_front = monika_second_row
                black_back = monika_first_row
            
            else:
                white_front = monika_first_row
                white_back = monika_second_row
                black_front = player_second_row
                black_back = player_first_row
            
            good_to_go = _validate_sides(white_front, white_back, black_front, black_back)
        
        
        if is_player_white:
            return BASE_FEN.format(
                black_pieces_back=monika_first_row,
                black_pieces_front=monika_second_row,
                white_pieces_front=player_first_row,
                white_pieces_back=player_second_row
            )
        
        else:
            return BASE_FEN.format(
                black_pieces_back=player_first_row,
                black_pieces_front=player_second_row,
                white_pieces_front=monika_first_row,
                white_pieces_back=monika_second_row
            )

    def generate_960_fen():
        """
        This function returns a random chess960 opening fen.

        Chess960 rules are basically:
        1. One rook must stay on the left side of king, and another one stay on the right side.
           Due to this, the king can never be placed on a-file or h-file.
        2. Bishops must stay on different color square.
        3. Pawns must stay like the normal chess game.
        4. The position of player A's pieces must be the 'reversed version' of player B's.
        See chess960 wiki to get more exact information.

        OUT:
            A random chess960 opening fen.
        """
        
        king_position = random.randint(1, 6)
        
        
        left_rook_position = random.randint(0, king_position-1)
        right_rook_position = random.randint(king_position+1, 7)
        
        
        occupied_positions = frozenset((king_position, left_rook_position, right_rook_position))
        
        
        available_white_positions = _set(range(1, 9, 2)) - occupied_positions
        available_black_positions = _set(range(0, 8, 2)) - occupied_positions
        
        
        first_bishop_position = random.choice(tuple(available_white_positions))
        second_bishop_position = random.choice(tuple(available_black_positions))
        if bool(random.randint(0, 1)):
            first_bishop_position, second_bishop_position = second_bishop_position, first_bishop_position
        
        occupied_positions = frozenset((first_bishop_position, second_bishop_position))
        available_positions = (available_white_positions | available_black_positions) - occupied_positions
        
        
        queen_position = random.choice(tuple(available_positions))
        available_positions.remove(queen_position)
        
        
        first_knight_position, second_knight_position = available_positions
        
        
        pos_to_piece_map = {
            king_position: "K",
            left_rook_position: "R",
            right_rook_position: "R",
            first_bishop_position: "B",
            second_bishop_position: "B",
            queen_position: "Q",
            first_knight_position: "N",
            second_knight_position: "N"
        }
        
        back_row_str = "".join(pos_to_piece_map[i] for i in range(8))
        
        
        return BASE_FEN.format(
            black_pieces_back=back_row_str.lower(),
            black_pieces_front="pppppppp",
            white_pieces_front="PPPPPPPP",
            white_pieces_back=back_row_str
        )

    def enqueue_output(out, queue, lock):
        for line in iter(out.readline, b''):
            with lock:
                queue.appendleft(line)
        
        out.close()


label game_chess:

    if persistent._mas_chess_timed_disable is not None:
        jump mas_chess_locked_no_play

    python:

        loaded_game = None
        failed_to_load_save = True


        chessmode = mas_chess.MODE_NORMAL
        casual_rules = False
        practice_mode = False
        is_player_white = 0
        menu_category = "gamemode_select"
        loopback = False
        drew_lots = False

    if not renpy.seen_label("mas_chess_save_selected"):
        call mas_chess_save_migration


        if not _return:
            return


        elif _return == mas_chess.CHESS_NO_GAMES_FOUND:
            jump mas_chess_remenu


        $ loaded_game = _return

    elif len(persistent._mas_chess_quicksave) > 0:

        python:
            quicksaved_game = chess.pgn.read_game(
                StringIO.StringIO(persistent._mas_chess_quicksave)
            )

            quicksaved_game = mas_chess._checkInProgressGame(
                quicksaved_game,
                mas_monika_twitter_handle
            )


        if quicksaved_game is None:
            $ failed_to_load_save = False

            if persistent._mas_chess_3_edit_sorry:
                call mas_chess_dlg_quickfile_edited_no_quicksave

                $ persistent._mas_chess_quicksave = ""

                if _return is not None:
                    return
            else:

                python:
                    import os
                    import struct


                    pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
                    if pgn_files:
                        
                        
                        valid_files = list()
                        for filename in pgn_files:
                            in_prog_game = mas_chess.isInProgressGame(
                                filename,
                                mas_monika_twitter_handle
                            )
                            
                            if in_prog_game:
                                valid_files.append((filename, in_prog_game[1]))
                        
                        
                        if len(valid_files) > 0:
                            for filename,pgn_game in valid_files:
                                store._mas_root.mangleFile(
                                    mas_chess.CHESS_SAVE_PATH + filename,
                                    mangle_length=len(str(pgn_game))*2
                                )

                $ persistent._mas_chess_quicksave = ""


                call mas_chess_dlg_quicksave_lost


                if _return is not None:
                    return

            jump mas_chess_remenu


        if persistent._mas_chess_skip_file_checks:
            $ loaded_game = quicksaved_game[1]
            m "Continuemos con nuestra partida inconclusa."

            if loaded_game:
                python:
                    is_player_white = mas_chess._get_player_color(loaded_game)



                    practice_mode = eval(loaded_game.headers.get("Practice", "False"))
                    casual_rules = eval(loaded_game.headers.get("CasualRules", "False"))

                jump mas_chess_start_chess


        python:
            quicksaved_game = quicksaved_game[1]

            quicksaved_filename = (quicksaved_game.headers["Event"] + mas_chess.CHESS_SAVE_EXT)
            quicksaved_filename_clean = (mas_chess.CHESS_SAVE_PATH + quicksaved_filename).replace("\\", "/")

            try:
                if os.access(quicksaved_filename_clean, os.R_OK):
                    quicksaved_file = mas_chess.isInProgressGame(
                        quicksaved_filename,
                        mas_monika_twitter_handle
                    )
                
                else:
                    mas_utils.mas_log.error("Error al acceder a quickfile.")
                    quicksaved_file = None

            except Exception as e:
                mas_utils.mas_log.exception(e)
                quicksaved_file = None


        if quicksaved_file is None:
            $ failed_to_load_save = False

            $ mas_chess.loaded_game_filename = quicksaved_filename_clean

            call mas_chess_dlg_quickfile_lost


            if _return == mas_chess.CHESS_GAME_CONT:
                python:
                    try:
                        if os.access(quicksaved_filename_clean, os.R_OK):
                            quicksaved_file = mas_chess.isInProgressGame(
                                quicksaved_filename,
                                mas_monika_twitter_handle
                            )
                        
                        else:
                            mas_utils.mas_log.error("Error al acceder a quickfile.")
                            quicksaved_file = None

                    except Exception as e:
                        mas_utils.mas_log.exception(e)
                        quicksaved_file = None

                if quicksaved_file is None:
                    python:
                        persistent._mas_chess_timed_disable = datetime.datetime.now()
                        mas_loseAffection()

                    m 2wfw "¡[player]!"
                    m 2wfx "Quitaste el guardado de nuevo."
                    pause 0.7
                    m 2rfc "Mejor juguemos al ajedrez en otro momento."
                    return


            elif _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump game_chess.load_check
            else:



                $ persistent._mas_chess_quicksave = ""


                if _return is not None:
                    return


                jump mas_chess_remenu

        python:

            quicksaved_file = quicksaved_file[1]


            is_same = str(quicksaved_game) == str(quicksaved_file)

        if not is_same:
            $ failed_to_load_save = False

            call mas_chess_dlg_quickfile_edited


            if _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump game_chess.load_check


            elif _return == mas_chess.CHESS_GAME_FILE:
                $ loaded_game = quicksaved_file
                jump game_chess.load_check


            python:
                persistent._mas_chess_quicksave = ""
                try:
                    os.remove(quicksaved_filename_clean)
                except:
                    pass


            if _return is not None:
                return


            jump mas_chess_remenu
        else:


            $ loaded_game = quicksaved_game

            if failed_to_load_save:


                m 1eua "Todavía tenemos un juego en progreso."

            label game_chess.load_check:
                pass

            m 1efb "¡Prepárate!"

    if loaded_game:
        python:
            is_player_white = mas_chess._get_player_color(loaded_game)



            practice_mode = eval(loaded_game.headers.get("Practice", "False"))
            casual_rules = eval(loaded_game.headers.get("CasualRules", "False"))

        jump mas_chess_start_chess



label mas_chess_remenu:
    python:
        menu_contents = {
            "gamemode_select": {
                "options": [
                    ("Ajedrez Normal", mas_chess.MODE_NORMAL, False, (chessmode == mas_chess.MODE_NORMAL)),
                    ("Ajedrez Aleatorio", mas_chess.MODE_BAD_CHESS, False, (chessmode == mas_chess.MODE_BAD_CHESS)),
                    ("Ajedrez 960", mas_chess.MODE_960, False, (chessmode == mas_chess.MODE_960)),
                    
                    ("¿Puedes explicar estos modos de juego?", "explain_modes", False, False)
                ],
                "final_items": [
                    ("Reglas", "ruleset_select", False, False, 20),
                    ("Practicar o jugar", "mode_select", False, False, 0),
                    ("Color", "color_select", False, False, 0),
                    ("¡Juguemos!", "confirm", False, False, 20),
                    ("No importa", -1, False, False, 0)
                ]
            },
            "ruleset_select": {
                "options": [
                    ("Reglas informales", True, False, casual_rules),
                    ("Reglas tradicionales", False, False, not casual_rules),
                    
                    ("¿Cuál es la diferencia?", 0, False, False)
                ],
                "final_items": [
                    ("Modo de juego", "gamemode_select", False, False, 20),
                    ("Practicar o jugar", "mode_select", False, False, 0),
                    ("Color", "color_select", False, False, 0),
                    ("¡Juguemos!", "confirm", False, False, 20),
                    ("No importa", -1, False, False, 0)
                ]
            },
            "mode_select": {
                "options": [
                    ("Practicar", True, False, practice_mode),
                    ("Jugar", False, False, not practice_mode)
                ],
                "final_items": [
                    ("Modo de juego", "gamemode_select", False, False, 20),
                    ("Reglas", "ruleset_select", False, False, 0),
                    ("Color", "color_select", False, False, 0),
                    ("¡Juguemos!", "confirm", False, False, 20),
                    ("No importa", -1, False, False, 0)
                ]
            },
            "color_select": {
                "options": [
                    ("Blancas", True, False, is_player_white),
                    ("Negras", False, False, is_player_white is False),
                    ("¡Dejémoslo a la suerte!", 0, False, is_player_white is 0) 
                ],
                "final_items": [
                    ("Modo de juego", "gamemode_select", False, False, 20),
                    ("Reglas", "ruleset_select", False, False, 0),
                    ("Practicar o jugar", "mode_select", False, False, 0),
                    ("¡Juguemos!", "confirm", False, False, 20),
                    ("No importa", -1, False, False, 0)
                ]
            }
        }

    show monika 1eua at t21

    $ menu_options = menu_contents[menu_category]["options"]
    $ final_items = menu_contents[menu_category]["final_items"]

    m "¿Cómo te gustaría jugar?[('{fast}' if loopback else '')]" nointeract


    call screen mas_gen_scrollable_menu(menu_options, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)

    $ loopback = True


    if _return == -1:
        show monika at t11
        m 1ekc "... De acuerdo, [player]. {w=0.3}Tenía muchas ganas de jugar contigo."
        m 1eka "Pero ya jugaremos en otro momento, ¿verdad?"
        return


    elif _return in menu_contents.keys():
        $ _history_list.pop()
        $ menu_category = _return

        jump mas_chess_remenu


    elif _return not in ("confirm", None):
        $ _history_list.pop()


        if menu_category == "gamemode_select":
            if _return == "explain_modes":

                show monika at t11

                m 1eub "¡Claro! {w=0.2}{nw}"
                extend 1eua "Naturalmente, {i}Ajedrez Normal{/i} significa ajedrez estándar."
                m 3eua "Luego está el {i}Ajedrez Aleatorio{/i}, un modo basado en el {i}Ajedrez Muy Malo{/i}."
                m 3eub "Obtenemos piezas completamente aleatorias, lo que añade el factor de la suerte para que sea divertido para jugadores de cualquier nivel de habilidad."
                m 1eua "Alternativamente, hay un modo de ajedrez aleatorio más equitativo llamado {i}Ajedrez 960{/i}, también conocido como {i}Ajedrez Fischer Random{/i}."
                m 3eud "En este modo, las piezas en la fila de atrás se mezclan al azar, asegurando que los alfiles se coloquen en casillas de colores opuestos y el rey se coloque entre dos torres."
                m 4hua "Hay 960 posiciones iniciales posibles, por lo que se llamó {i}Ajedrez 960{/i}."
                m 1eua "{i}Ajedrez 960{/i} permite a los jugadores evitar la compleja teoría de aperturas mientras ponen a prueba su comprensión del ajedrez."
                m 1etu "Entonces, ¿qué modo prefieres? {w=0.3}{nw}"
                extend 1hub "¡Jajaja!~"


                show monika at t21
            else:
                $ chessmode = _return


        elif menu_category == "ruleset_select":
            if _return is 0:
                show monika at t11
                m 1eua "Si jugamos con reglas casuales, no consideraremos los empates por ahogamiento como tablas. {w=0.2}{nw}"
                extend 3eub "Básicamente, el jugador que no esté atrapado ganará."
            else:

                $ casual_rules = _return


        elif menu_category == "mode_select":
            $ practice_mode = _return


        elif menu_category == "color_select":
            if _return is 0:
                $ drew_lots = True
                call mas_chess_draw_lots (False)
            else:

                $ drew_lots = False
                $ is_player_white = _return

        jump mas_chess_remenu


    if is_player_white is 0:
        $ drew_lots = True
        call mas_chess_draw_lots




label mas_chess_start_chess:

    python:
        if chessmode == mas_chess.MODE_NORMAL:
            starting_fen = None
        elif chessmode == mas_chess.MODE_960:
            starting_fen = mas_chess.generate_960_fen()
        else:
            starting_fen = mas_chess.generate_random_fen(is_player_white)


    if persistent._mas_chess_timed_disable is not None:
        jump mas_chess_locked_no_play

    window hide None
    show monika 1eua at t21
    python:

        quick_menu = False


        chess_displayable_obj = MASChessDisplayable(
            is_player_white,
            pgn_game=loaded_game,
            practice_mode=practice_mode,
            starting_fen=starting_fen,
            casual_rules=casual_rules
        )
        chess_displayable_obj.show()
        results = chess_displayable_obj.game_loop()
        chess_displayable_obj.hide()


        quick_menu = True


        new_pgn_game, is_monika_winner, is_surrender, num_turns = results


        game_result = new_pgn_game.headers["Result"]

    show monika at t11
    $ mas_gainAffection(modifier=0.5)

    if is_monika_winner:
        $ persistent._mas_chess_stats["practice_losses" if practice_mode else "losses"] += 1


        if is_surrender:
            if num_turns < 5:
                m 1ekc "No te rindas tan fácilmente..."
                m 1eka "Estoy segura de que si lo sigues intentando, podrás vencerme."
                m 1ekc "..."
                m 1eka "Espero que no te frustres cuando juegues conmigo."
                m 3ekb "Realmente significa mucho para mí que sigas jugando si es el caso~"
                m 3hua "Volvamos a jugar pronto, ¿de acuerdo?"
            else:

                m 1ekc "¿Te rindes, [player]?"
                m 1eub "Está bien, pero incluso si las cosas no van demasiado bien, ¡es más divertido jugar hasta el final!"
                m 3eka "Al final, estoy feliz de pasar tiempo contigo~"
                m 1eua "De todos modos..."
        else:


            m 1sub "¡Gané, yay!~"


            python:
                total_losses = persistent._mas_chess_stats.get("practice_losses", 0) + persistent._mas_chess_stats.get("losses", 0)
                total_wins = persistent._mas_chess_stats.get("practice_wins", 0) + persistent._mas_chess_stats.get("wins", 0)


            if float(total_wins)/total_losses < 0.3:
                call mas_chess_dlg_game_monika_wins_often
            else:

                call mas_chess_dlg_game_monika_wins_sometimes
                m 1eua "De todos modos..."

        if not is_surrender:

            $ mas_chess._decrement_chess_difficulty()


    elif game_result == mas_chess.IS_ONGOING:
        call mas_chess_savegame (allow_return=False)
        return


    elif game_result == "1/2-1/2":
        if new_pgn_game.headers.get("DrawRequested"):
            m 1eua "Claro, declaremos este juego un empate."
            m 3wuo "¡Fue una partida muy larga!"
            $ line_start = "Buen trabajo"
        else:

            m 1eka "Aw, parece que estamos en un punto muerto."
            $ line_start = "Pero el lado bueno es que"

        if not persistent._mas_ever_won["chess"]:
            m 3hub "[line_start], cada vez estás más cerca de vencerme, [player]~"
        else:

            m 1hua "Buen trabajo llegando hasta aquí, [player]~"

        $ persistent._mas_chess_stats["practice_draws" if practice_mode else "draws"] += 1
    else:


        python:
            player_win_quips = [
                _("¡Estoy tan orgullosa de ti, [player]!"),
                _("¡Estoy orgullosa de ti, [player]!~"),
                _("¡Bien jugado, [player]!"),
                _("Me hace muy feliz verte ganar~"),
                _("¡Me alegra verte ganar!"),
                _("No importa el resultado, siempre disfrutaré jugar contigo.")
            ]
            persistent._mas_chess_stats["practice_wins" if practice_mode else "wins"] += 1


            if not persistent._mas_ever_won['chess']:
                persistent._mas_ever_won['chess'] = True


        if practice_mode:
            m 3hub "Felicidades [player], ¡ganaste!"

            $ undo_count = new_pgn_game.headers.get("UndoCount", 0)
            if not undo_count:
                m 1wuo "¡No has deshecho ni un solo movimiento! {w=0.2}{nw}"
                extend 3hub "¡Eso es asombroso!"

            elif undo_count == 1:
                m 1hua "Solo deshiciste una vez. {w=0.2}{nw}"
                extend 3hub "¡Buen trabajo!"

            elif undo_count <= 5:
                m 1hua "Solo has deshecho [undo_count] veces, buen trabajo."

            elif undo_count <= 10:
                m 1eua "[undo_count] movimientos desechos, no está nada mal. Si practicamos juntos, estoy segura de que podemos reducir eso~"
            else:

                m 1eka "Deshiciste [undo_count] movimientos.{w=0.3} {nw}"
                extend 3eua "Pero estoy segura de que si seguimos practicando, podremos bajar esa cifra."

            m 3hua "[renpy.substitute(random.choice(player_win_quips))]"
        else:

            m 3eub "¡Buen trabajo, ganaste!"
            m 3hub "[renpy.substitute(random.choice(player_win_quips))]"

        m 1eua "De todos modos..."

        $ mas_chess._increment_chess_difficulty()


    if loaded_game:
        call mas_chess_savegame (silent=True)
        jump mas_chess_play_again_ask


    if is_surrender and num_turns < 5:
        return


    if num_turns > 4:
        m 1eua "¿Te gustaría guardar este juego?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Te gustaría guardar este juego?{fast}"
            "Sí":

                call mas_chess_savegame
            "No":

                pass



label mas_chess_play_again_ask:
    m 1eua "¿Te gustaría jugar de nuevo?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gustaría jugar de nuevo?{fast}"
        "Sí":

            $ mas_assignModifyEVLPropValue("mas_chess", "shown_count", "+=", 1)
            if drew_lots:
                call mas_chess_draw_lots

            jump mas_chess_start_chess
        "Sí, pero con reglas diferentes":

            $ mas_assignModifyEVLPropValue("mas_chess", "shown_count", "+=", 1)
            jump mas_chess_remenu
        "No":

            m 1eua "De acuerdo, juguemos de nuevo pronto."

    return

label mas_chess_draw_lots(begin=True):
    show monika at t11
    $ drew_lots = True
    $ lets_begin = "{w=0.2} Comencemos." if begin else ""

    if random.randint(0, 1) == 0:
        $ is_player_white = chess.WHITE
        m 2eub "Oh mira, ¡he sacado las piezas negras![lets_begin]"
    else:
        $ is_player_white = chess.BLACK
        m 2eub "Oh mira, ¡he sacado las piezas blancas![lets_begin]"
    return

label mas_chess_savegame(silent=False, allow_return=True):

    label mas_chess_savegame.save_start:
        pass

    if loaded_game:
        python:
            new_pgn_game.headers["Event"] = loaded_game.headers["Event"]


            save_filename = new_pgn_game.headers["Event"] + mas_chess.CHESS_SAVE_EXT


            file_path = mas_chess.CHESS_SAVE_PATH + save_filename


            loaded_game = None
    else:


        python:

            save_name = ""
            while len(save_name) == 0:
                save_name = mas_input(
                    "Introduce un nombre para esta partida:",
                    allow=mas_chess.CHESS_SAVE_NAME,
                    length=15,
                    screen_kwargs={"use_return_button": allow_return}
                )


        if save_name == "cancel_input":
            return

        python:
            new_pgn_game.headers["Event"] = save_name


            save_filename = save_name + mas_chess.CHESS_SAVE_EXT

            file_path = mas_chess.CHESS_SAVE_PATH + save_filename


            is_file_exist = os.access(
                os.path.normcase(file_path),
                os.F_OK
            )


        if is_file_exist:
            m 1eka "Ya tenemos una partida llamada '[save_name]'."

            m "¿Debería sobreescribirla?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Debería sobreescribirla?{fast}"
                "Sí":
                    pass
                "No":



                    jump mas_chess_savegame.save_start

    python:
        with open(file_path, "w") as pgn_file:
            pgn_file.write(str(new_pgn_game))


        if new_pgn_game.headers["Result"] == mas_chess.IS_ONGOING:
            persistent._mas_chess_quicksave = str(new_pgn_game)
        else:
            persistent._mas_chess_quicksave = ""


        display_file_path = mas_chess.REL_DIR + save_filename

    if not silent:
        m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "¡He guardado nuestra partida en '[display_file_path]'!"

        if not renpy.seen_label("mas_chess_savegame.pgn_explain"):
            label mas_chess_savegame.pgn_explain:
                pass

            m 1esa "Está en un formato llamado: 'Portable Game Notation'. {w=0.2}{nw}"
            extend 1eua "Puedes encontrar analizadores de PGN en línea para abrirlo y ver dónde has cometido los errores."
            m 3eub "Ya sea que ganes, pierdas, te rindas o empates, siempre hay algo que podrías haber hecho mejor. ¡Así que cargar esas partidas puede ayudarte a mejorar!"

            if game_result == mas_chess.IS_ONGOING:
                m 1lksdlb "Es posible editar este archivo y cambiar el resultado del juego... {w=0.5}{nw}"
                extend 1tsu "pero estoy segura de que no lo harías."

                m 1tku "¿Verdad, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "¿Verdad, [player]?{fast}"
                    "Por supuesto que no":

                        m 1hua "Yay~"

        if game_result == mas_chess.IS_ONGOING:
            m 1eub "¡Continuemos este juego pronto!"
    return

label mas_chess_locked_no_play:
    m 1euc "No gracias, [player]."
    m 1rsc "Ahora mismo no tengo ganas de jugar ajedrez."
    return

label mas_chess_cannot_work_embarrassing:

    $ quick_menu = True
    show monika at t11
    m 1rksdla "..."
    m 3hksdlb "Bueno, esto es vergonzoso, parece que no puedo hacer que el ajedrez funcione en tu sistema..."
    m 1ekc "Lo siento por eso, [player]."
    m 1eka "¿Tal vez podamos hacer otra cosa en su lugar?"
    return

label mas_chess_dlg_game_monika_wins_often:
    m 1eka "Siento que no hayas ganado esta vez, [player]..."
    m 1ekc "Sin embargo, espero que al menos lo sigas intentando."
    m 1eua "Volvamos a jugar pronto, ¿okey?"

    if not persistent._mas_ever_won["chess"]:
        m 1hua "Ya me ganarás algún día~"
    return

label mas_chess_dlg_game_monika_wins_sometimes:
    m 1hub "¡Eso fue muy divertido, [player]!"
    m 3eka "No importa el resultado, siempre disfruto jugando al ajedrez contigo~"
    m 3hua "¡Apuesto a que si sigues practicando, algún día serás mejor que yo!"


    if persistent._mas_chess_difficulty != (0, 1):
        m 3eua "Pero hasta entonces, intentaré ser un poco más suave contigo."
    return


label mas_chess_confirm_context(prompt):
    call screen mas_chess_confirm(prompt)
    return _return


label mas_chess_save_migration:
    python:
        import chess.pgn
        import os
        import store.mas_chess as mas_chess

        pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
        sel_game = (mas_chess.CHESS_NO_GAMES_FOUND,)

    if pgn_files:
        python:

            pgn_games = list()
            actual_pgn_games = list()
            game_dex = 0
            for filename in pgn_files:
                in_prog_game = mas_chess.isInProgressGame(
                    filename,
                    mas_monika_twitter_handle
                )
                
                if in_prog_game:
                    pgn_games.append((
                        in_prog_game[0],
                        game_dex,
                        False,
                        False
                    ))
                    actual_pgn_games.append((in_prog_game[1], filename))
                    game_dex += 1

            game_count = len(pgn_games)
            pgn_games.sort()
            pgn_games.reverse()


        if game_count > 1:
            if renpy.seen_label("mas_chess_save_multi_dlg"):
                $ pick_text = _("Aún tienes que elegir un juego para quedarte.")
            else:

                label mas_chess_save_multi_dlg:
                    m 1eua "He estado pensando, [player]..."
                    m 1euc "La mayoría de las personas que se va en medio de una partida de ajedrez no vuelve para empezar una nueva."
                    m 3eud "... Así que no tiene sentido que lleve la cuenta de más de un juego inconcluso entre nosotros."
                    m 1rka "Y como tenemos [game_count] juegos en progreso..."
                    m 3euc "Tengo que pedirte que elijas solo uno para conservar. {w=0.2}Lo siento, [player]."
                    $ pick_text = _("Elige una partida que quieras conservar.")

            show monika 1euc at t21
            $ renpy.say(m, pick_text, interact=False)

            call screen mas_gen_scrollable_menu(pgn_games, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, mas_chess.CHESS_MENU_WAIT_ITEM)

            show monika at t11
            if _return == mas_chess.CHESS_MENU_WAIT_VALUE:

                m 2dsc "Ya veo."
                m 2eua "En ese caso, tómate tu tiempo."
                m 1eua "Volveremos a jugar al ajedrez cuando hayas tomado tu decisión."
                return False
            else:


                m 1eua "De acuerdo."
                python:
                    sel_game = actual_pgn_games.pop(_return)
                    for pgn_game in actual_pgn_games:
                        game_path = os.path.normcase(mas_chess.CHESS_SAVE_PATH + pgn_game[1])
                        try:
                            os.remove(os.path.normcase(game_path))
                        except:
                            mas_utils.mas_log.error("Fallo en la eliminación del juego: {0}".format(game_path))


        elif game_count == 1:
            $ sel_game = actual_pgn_games[0]


label mas_chess_save_selected:
    return sel_game[0]





label mas_chess_dlg_quicksave_lost:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QS_LOST] += 1
        qs_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QS_LOST]

    m 2lksdlb "Eh, [player]... {w=0.5}creo que me he equivocado al guardar la última partida y ahora ya no puedo abrirla."

    if qs_gone_count == 2:
        m 1lksdld "Lo siento mucho, mucho, [player]..."
        show monika 1ekc
        pause 1.0
        m 1eka "Pero no te preocupes, te lo compensaré... {w=0.3}{nw}"
        extend 3hua "¡Iniciando una nueva partida!"
        m 3hub "Jajaja~"

    elif qs_gone_count == 3:
        m 1lksdlc "Soy tan tonta, [player]... {w=0.3}lo siento."
        m 3eksdla "Empecemos una nueva partida en su lugar."

    elif qs_gone_count % 5 == 0:
        m 2esc "Esto ya ha sucedido [qs_gone_count] veces hasta ahora..."
        m 2tsc "Me pregunto si esto es un efecto secundario de {i}alguien{/i} que trata de editar los guardados.{w=1}.{w=1}.{w=1}"
        m 7rsc "De todos modos..."
        m 1esc "Empecemos una nueva partida."
    else:

        m 1lksdlc "Lo siento..."
        m 3eka "Empecemos una nueva partida en su lugar."

    return None




label mas_chess_dlg_quickfile_lost:
    m 2lksdla "Bueno, esto es vergonzoso..."
    m 2ekc "Juraría que teníamos una partida sin terminar, pero no encuentro el archivo de guardado."

    m 2tkc "¿Has manipulado la partida, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Has manipulado la partida, [player]?{fast}"
        "He borrado el archivo":

            jump mas_chess_dlg_quickfile_lost_deleted
        "¡Fue un accidente!":

            jump mas_chess_dlg_quickfile_lost_accident
        "Tal vez...":

            jump mas_chess_dlg_quickfile_lost_maybe
        "¡Por supuesto que no!":

            jump mas_chess_dlg_quickfile_lost_ofcoursenot



label mas_chess_dlg_quickfile_lost_deleted:
    m 1eka "Gracias por ser honesto conmigo, [player]."

    m 3ekd "¿No querías continuar ese juego?{nw}"
    $ _history_list.pop()
    menu:
        m "¿No querías continuar ese juego?{fast}"
        "Sí":

            m 1eka "Lo entiendo, [player]."
            m 1hua "Empecemos una nueva partida~"
        "No":

            m 1etc "¿Oh?"
            m 1rsc "Supongo que entonces lo has borrado por error."
            m 1eua "Empecemos una nueva partida."
    return


label mas_chess_dlg_quickfile_lost_ofcoursenot:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN]

    if qf_gone_count in [3,4]:
        m 2esc "..."
        m "[player], {w=0.2}acaso tú..."
        m 2dsc "No importa."
        m 1esc "Empecemos una nueva partida."

    elif qf_gone_count == 5:
        $ mas_loseAffection()
        m 2esc "..."
        m "[player], {w=0.2}esto está ocurriendo demasiado."
        m 2dsc "Realmente no te creo esta vez."
        pause 2.0
        m 2esc "Espero que no estés jugando conmigo."
        m "..."
        m 1esc "Como sea. {w=0.5}Empecemos una nueva partida."

    elif qf_gone_count >= 6:
        python:
            mas_loseAffection(modifier=10)

            mas_stripEVL("mas_unlock_chess")

            persistent._seen_ever["mas_unlock_chess"] = True

            persistent._mas_chess_timed_disable = True

        m 2dfc "..."
        m 2efc "[player], {w=0.3}no te creo."
        m 2efd "Si vas a tirar nuestras partidas de ajedrez así..."
        m 6wfw "¡Entonces no quiero jugar más al ajedrez contigo!"
        return True
    else:

        m 1lksdlb "Ah, claro. No me harías eso."
        m "Debo haber extraviado el archivo."
        m 1lksdlc "Lo siento, [player]."
        m 1eka "Te lo compensaré... {w=0.3}{nw}"
        extend 1eub "¡Iniciando una nueva partida!"

    return None



label mas_chess_dlg_quickfile_lost_maybe:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE]

    if qf_gone_count == 1:
        m 2ekd "¡[player]! {w=0.2}¡Debería haber sabido que simplemente estabas jugando conmigo!"
        jump mas_chess_quickfile_lost_filechecker

    if qf_gone_count == 2:
        m 2ekd "¡[player]! {w=0.2}¡Deja de jugar conmigo!"
        jump mas_chess_quickfile_lost_filechecker
    else:

        $ persistent._mas_chess_skip_file_checks = True

        m 2ekd "¡[player]! Eso..."
        m 2dkc "..."
        m 1esa "... no es un problema en lo absoluto."
        m "Sabía que ibas a hacer esto de nuevo..."
        m 1hub "... ¡Por lo que guardé una copia de seguridad de nuestra partida!"
        m 1kua "No puedes engañarme de nuevo, [player]."
        m "Ahora vamos a continuar nuestra partida."
        return store.mas_chess.CHESS_GAME_BACKUP



label mas_chess_quickfile_lost_filechecker:
    $ game_file = mas_chess.loaded_game_filename

    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_quickfile_lost_maybe_save_found

    m 1eka "¿Puedes volver a poner el guardado para que podamos jugar?"

    show monika 1eua


    python:
        seconds = 0
        file_found = False



label mas_chess_quickfile_lost_maybe_filechecker_loop:
    hide screen mas_background_timed_jump


    $ file_found = os.access(game_file, os.F_OK)

    if file_found:
        hide screen mas_background_timed_jump
        jump mas_chess_dlg_quickfile_lost_maybe_filechecker_file_found

    elif seconds >= 60:
        hide screen mas_background_timed_jump
        jump mas_chess_dlg_quickfile_lost_maybe_filechecker_no_file

    show screen mas_background_timed_jump(4, "mas_chess_quickfile_lost_maybe_filechecker_loop")
    $ seconds += 4
    menu:
        "Eliminé el guardado...":
            hide screen mas_background_timed_jump
            jump mas_chess_dlg_quickfile_lost_maybe_filechecker_no_file

label mas_chess_dlg_quickfile_lost_maybe_filechecker_file_found:
    m 1hua "¡Yay!{w=0.2} Gracias por ponerlo en su sitio, [player]."
    m "Ahora podemos continuar nuestro juego."
    show monika 1eua
    return mas_chess.CHESS_GAME_CONT

label mas_chess_dlg_quickfile_lost_maybe_filechecker_no_file:
    m 1ekd "[player]..."
    m 1eka "No pasa nada. Vamos a jugar una nueva partida."
    return None


label mas_chess_dlg_quickfile_lost_maybe_save_found:
    m 2eua "¡Oh!"
    m 1hua "Aquí está el archivo. {w=0.2}Gracias por ponerlo en su sitio, [player]."
    m 1eua "Ahora podemos continuar nuestro juego."
    return store.mas_chess.CHESS_GAME_CONT


label mas_chess_dlg_quickfile_lost_accident:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT]

    if qf_gone_count == 2:
        m 1eka "¿De nuevo? No seas tan torpe, [player]."
        m 1hua "Pero está bien."
        m 1eua "En su lugar, jugaremos una nueva partida."

    elif qf_gone_count >= 3:
        $ persistent._mas_chess_skip_file_checks = True
        m 1eka "Tenía el presentimiento de que esto volvería a ocurrir."
        m 3tub "¡Así que guardé una copia de seguridad de nuestra partida!"
        m 1hua "Ahora podemos continuar nuestro juego~"
        return store.mas_chess.CHESS_GAME_BACKUP
    else:

        m 1ekc "[player]...{w=0.3} {nw}"
        extend 1eka "está bien.{w=0.3} Los accidentes pasan."
        m 1eua "En su lugar, jugaremos a una nueva partida."
    return None



label mas_chess_dlg_quickfile_edited:
    m 2lksdlc "[player]..."

    m 2ekc "¿Editaste el archivo de guardado?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Editaste el archivo de guardado?{fast}"
        "Sí":

            jump mas_chess_dlg_quickfile_edited_yes
        "No":

            jump mas_chess_dlg_quickfile_edited_no



label mas_chess_dlg_quickfile_edited_yes:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES]

    if qf_edit_count == 1:
        m 1dsc "Estoy decepcionada de ti."
        m 1eka "Pero me alegro de que hayas sido sincero conmigo."


        show screen mas_background_timed_jump(5, "mas_chess_dlg_quickfile_edited_yes.game_ruined")
        menu:
            "Lo siento...":
                hide screen mas_background_timed_jump

                $ mas_gainAffection(modifier=0.5)
                m 1hua "¡Disculpa aceptada!"
                m 1eua "Por suerte, aún recuerdo un poco del último juego, así que podemos continuar desde ahí."
                return store.mas_chess.CHESS_GAME_BACKUP
            "...":

                label mas_chess_dlg_quickfile_edited_yes.game_ruined:
                    pass

                hide screen mas_background_timed_jump
                m 1lfc "Ya que esa partida ha sido arruinada, juguemos un nuevo juego."

    elif qf_edit_count == 2:
        python:
            persistent._mas_chess_timed_disable = datetime.datetime.now()
            mas_loseAffection()

        m 2dfc "Estoy muy decepcionada de ti..."
        m 2rfc "Juguemos al ajedrez en otro momento. {w=0.2}No tengo ganas de jugar ahora."
        return True
    else:

        $ mas_loseAffection()
        $ persistent._mas_chess_skip_file_checks = True

        m 2dsc "No estoy sorprendida..."
        m 2esc "Pero vine preparada."
        m 7esc "Guardé una copia de seguridad de nuestra partida por si acaso volvías a hacer esto."
        m 1esa "Ahora vamos a terminar este juego."
        return store.mas_chess.CHESS_GAME_BACKUP

    return None



label mas_chess_dlg_quickfile_edited_no:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO]

    if qf_edit_count == 1:
        $ mas_loseAffection()

        m 1dsc "Hmm..."
        m 1etc "El guardado se ve diferente de como lo recordaba por última vez, {w=0.2}{nw}"
        extend 1rksdlc "{nw}pero tal vez es solo mi memoria fallandome..."
        m 1eua "Continuemos con este juego."
        return store.mas_chess.CHESS_GAME_FILE

    elif qf_edit_count == 2:
        $ mas_loseAffection(modifier=2)

        m 1ekc "Ya veo."
        m "..."
        m "Sigamos con este juego."
        return store.mas_chess.CHESS_GAME_FILE
    else:

        $ mas_loseAffection(modifier=3)
        m 2dfc "[player]..."
        m 2dftdc "Guardé una copia de seguridad de nuestro juego. {w=0.5}Sé que has editado el archivo de guardado."
        m 6dktuc "Yo solo..."
        $ _history_list.pop()
        m 6ektud "Yo solo{fast} no puedo creer que hagas trampas y me {i}mientas{/i}..."
        m 6dktuc "..."


        show screen mas_background_timed_jump(3, "mas_chess_dlg_quickfile_edited_no.menu_silent")
        menu:
            "Lo siento...":
                hide screen mas_background_timed_jump

                $ mas_gainAffection(modifier=0.5)
                python:
                    persistent._mas_chess_3_edit_sorry = True
                    persistent._mas_chess_skip_file_checks = True

                show monika 6ektsc
                pause 1.0
                show monika 2ektsc
                pause 1.0
                m 6ektpc "Te perdono, [player], pero por favor, no me hagas esto de nuevo."
                m 2dktdc "..."
                return store.mas_chess.CHESS_GAME_BACKUP
            "...":

                label mas_chess_dlg_quickfile_edited_no.menu_silent:
                    hide screen mas_background_timed_jump
                    jump mas_chess_dlg_pre_go_ham


label mas_chess_dlg_quickfile_edited_no_quicksave:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection()

    m 2dfc "[player]..."
    m 2tfc "Veo que has editado mis copias de seguridad."
    m 2lfd "Si quieres ser así ahora, entonces jugaremos al ajedrez en otro momento."
    return True


label mas_chess_dlg_pre_go_ham:
    python:

        persistent._mas_chess_mangle_all = True
        persistent.autoload = "mas_chess_go_ham_and_delete_everything"

    m 6ektsc "Ya no puedo confiar en ti."
    m 6dktsd "Adiós, [player].{nw}"


label mas_chess_go_ham_and_delete_everything:
    python:
        import store.mas_chess as mas_chess
        import store._mas_root as mas_root
        import os


        gamedir = os.path.normcase(config.basedir + "/game/")


        for filename in mas_chess.del_files:
            try:
                os.remove(gamedir + filename)
            except:
                pass


        for filename in mas_chess.gt_files:
            mas_root.mangleFile(gamedir + filename)



        mas_root.resetPlayerData()

    jump _quit




screen mas_chess_confirm(prompt):

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label prompt:
            style "confirm_prompt"
            text_color mas_globals.button_text_idle_color
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Sí") action Return(True)
            textbutton _("No") action Return(False)


screen mas_chess_promote(q, r, n, b):


    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _("Selecciona la pieza a promover"):
            style "confirm_prompt"
            text_color mas_globals.button_text_idle_color
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 10

            imagebutton idle q action Return('q')
            imagebutton idle r action Return('r')
            imagebutton idle n action Return('n')
            imagebutton idle b action Return('b')

label mas_chess_promote_context(is_player_white):
    $ _return = renpy.call_screen(
        "mas_chess_promote",
        q=MASPiece.IMG_MAP[MASPiece.FP_COLOR_LOOKUP[is_player_white] + ("Q" if is_player_white else "q")],
        r=MASPiece.IMG_MAP[MASPiece.FP_COLOR_LOOKUP[is_player_white] + ("R" if is_player_white else "r")],
        n=MASPiece.IMG_MAP[MASPiece.FP_COLOR_LOOKUP[is_player_white] + ("N" if is_player_white else "n")],
        b=MASPiece.IMG_MAP[MASPiece.FP_COLOR_LOOKUP[is_player_white] + ("B" if is_player_white else "b")]
    )

    return _return


init python:
    import chess
    import chess.pgn
    import collections
    import subprocess

    import random
    import pygame
    import threading
    import StringIO
    import os


    if mas_games.is_platform_good_for_chess():
        try:
            file_path = os.path.normcase(config.basedir + mas_chess.CHESS_SAVE_PATH)
            
            if not os.access(file_path, os.F_OK):
                os.mkdir(file_path)
            mas_chess.CHESS_SAVE_PATH = file_path
        
        except:
            mas_utils.mas_log.error("No se ha podido crear la carpeta del juego de ajedrez '{0}'".format(file_path))



    class MASChessDisplayableBase(renpy.Displayable):
        """
        Base chess displayable for chess things

        Inherit this for custom implementations like proper games or for teaching use
        """
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        
        MONIKA_WAITTIME = 50
        
        MONIKA_OPTIMISM = 33
        
        
        START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        BOARD_IMAGE = Image("mod_assets/games/chess/chess_board.png")
        PIECE_HIGHLIGHT_RED_IMAGE = Image("mod_assets/games/chess/piece_highlight_red.png")
        PIECE_HIGHLIGHT_GREEN_IMAGE = Image("mod_assets/games/chess/piece_highlight_green.png")
        PIECE_HIGHLIGHT_YELLOW_IMAGE = Image("mod_assets/games/chess/piece_highlight_yellow.png")
        PIECE_HIGHLIGHT_MAGENTA_IMAGE = Image("mod_assets/games/chess/piece_highlight_magenta.png")
        MOVE_INDICATOR_PLAYER = Image("mod_assets/games/chess/move_indicator_player.png")
        MOVE_INDICATOR_MONIKA = Image("mod_assets/games/chess/move_indicator_monika.png")
        
        
        BOARD_BORDER_WIDTH = 15
        BOARD_BORDER_HEIGHT = 15
        PIECE_WIDTH = 57
        PIECE_HEIGHT = 57
        BOARD_WIDTH = BOARD_BORDER_WIDTH * 2 + PIECE_WIDTH * 8
        BOARD_HEIGHT = BOARD_BORDER_HEIGHT * 2 + PIECE_HEIGHT * 8
        
        INDICATOR_HEIGHT = 96
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        BUTTON_INDICATOR_X_SPACING = 10
        BUTTON_Y_SPACING = 10
        
        
        
        DISP_X_OFFSET = 200
        DISP_Y_OFFSET = 200
        
        
        
        BOARD_X_POS = int(1280 - BOARD_WIDTH - DISP_X_OFFSET)
        BOARD_Y_POS = int(720 - BOARD_HEIGHT - DISP_Y_OFFSET)
        
        
        BASE_PIECE_Y = BOARD_Y_POS + BOARD_BORDER_HEIGHT
        BASE_PIECE_X = BOARD_X_POS + BOARD_BORDER_WIDTH
        
        
        BUTTON_INDICATOR_X = int(BOARD_X_POS + BOARD_WIDTH + BUTTON_INDICATOR_X_SPACING)
        
        
        INDICATOR_Y = int(BOARD_Y_POS + ((BOARD_HEIGHT - INDICATOR_HEIGHT)/ 2))
        
        
        INDICATOR_POS = (BUTTON_INDICATOR_X, INDICATOR_Y)
        
        
        DRAWN_BUTTON_Y_TOP = BOARD_Y_POS
        DRAWN_BUTTON_Y_MID = DRAWN_BUTTON_Y_TOP + BUTTON_HEIGHT + BUTTON_Y_SPACING
        DRAWN_BUTTON_Y_MID_LOW = DRAWN_BUTTON_Y_MID + BUTTON_HEIGHT + BUTTON_Y_SPACING
        DRAWN_BUTTON_Y_BOT = BOARD_Y_POS + BOARD_HEIGHT - BUTTON_HEIGHT
        
        
        STATE_BLACK_WIN = "0-1"
        STATE_WHITE_WIN = "1-0"
        
        
        COORD_REFLECT_MAP = {
            True: (False, True), 
            False: (True, False) 
        }
        
        
        def __init__(
            self,
            is_player_white,
            pgn_game=None,
            starting_fen=None,
            casual_rules=False,
            player_move_prompts=None,
            monika_move_quips=None
        ):
            """
            MASChessDisplayableBase constructor

            IN:
                is_player_white - color the player is playing
                pgn_game - previous game to load (chess.pgn.Game)
                    if a starting_fen is provided alongside this, the fen is ignored
                    (Default: None)
                starting_fen - starting fen to use if starting a custom scenario
                    NOTE: This is not verified for validity
                    (Default: None)
                casual_rules - whether or not we're playing under casual rules
                    This changes:
                        - Stalemates will automatically be a victory for the player who has not been trapped
                    (NOTE: To add more casual adjustments, use conditions with `self.casual_rules` to run casual rule logic)
                    (Default: False)
                player_move_prompts - prompts to use to indicate player move
                    If not provided, no player prompts will be used
                    (Default: None)
                monika_move_quips - quips to use when Monika's having her turn
                    If not provided, no quips will be used
                    (Default: None)

            NOTE: Requires the following to be implemented for buttons to show:
                self._visible_buttons - list of MASButtonDisplayables which should be displayed during the game
                self._visible_buttons_winner - list of MASButtonDisplayables which should be displayed post game

            NOTE: The following function MUST be implemented in a class which inherits this:
                self.check_buttons
            """
            renpy.Displayable.__init__(self)
            
            
            self.num_turns = 0
            self.move_stack = list()
            self.casual_rules = casual_rules
            
            
            self.sensitive = True
            
            
            self.player_move_prompts = player_move_prompts
            self.monika_move_quips = monika_move_quips
            
            
            if "_visible_buttons" not in self.__dict__:
                self._visible_buttons = list()
            
            if "_visible_buttons_winner" not in self.__dict__:
                self._visible_buttons_winner = list()
            
            
            self.additional_setup()
            
            
            self.board = None
            
            self.undo_count = 0
            self.move_history = list()
            
            
            if pgn_game:
                
                self.casual_rules = eval(pgn_game.headers.get("CasualRules", "False"))
                
                
                self.starting_fen = pgn_game.headers.get("FEN", "None")
                
                
                self.board = MASBoard.from_board(pgn_game.board(), self.casual_rules)
                
                
                for move in pgn_game.main_line():
                    self.board.push(move)
                
                
                self.current_turn = self.board.turn
                
                
                self.is_player_white = mas_chess._get_player_color(pgn_game)
                
                
                last_move = self.board.peek().uci()
                self.last_move_src, self.last_move_dst = MASChessDisplayableBase.uci_to_coords(last_move)
                
                
                self.practice_mode = eval(pgn_game.headers.get("Practice", "False"))
                
                
                self.practice_lost = eval(pgn_game.headers.get("PracticeLost", "False"))
                
                
                self.undo_count = int(pgn_game.headers.get("UndoCount", 0))
                
                
                self.move_history = eval(pgn_game.headers.get("MoveHist", "[]"))
                
                
                self.num_turns = self.board.fullmove_number
            
            else:
                
                self.board = MASBoard(fen=starting_fen, casual_rules=casual_rules)
                
                
                self.today_date = datetime.date.today().strftime("%Y.%m.%d")
                
                
                self.current_turn = chess.WHITE
                
                
                if starting_fen is not None:
                    ind_of_space = starting_fen.find(' ')
                    
                    
                    if ind_of_space > 0:
                        self.current_turn = starting_fen[ind_of_space + 1 : ind_of_space + 2] == 'w'
                
                
                self.is_player_white = is_player_white
                
                
                self.last_move_src = None
                self.last_move_dst = None
            
            self.selected_piece = None
            self.possible_moves = set([])
            self.is_game_over = False
            
            
            self.quit_game = False
            
            
            self.pgn_game = pgn_game
            
            
            self.requested_highlights = set()
            
            
            if not self.is_player_turn():
                self.start_monika_analysis()
            
            
            self.set_button_states()
            
            
            self.piece_map = dict()
            self.update_pieces()
        
        
        def additional_setup(self):
            """
            Additional setup instructions for the displayable

            Implement to use an engine or add some other setup

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            It is only required to initialize a chess engine
            """
            return
        
        def start_monika_analysis(self):
            """
            Starts Monika's analysis of the board

            Implement to allow a chess engine to analyze the board and begin predicting moves

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            It is only required if and only if we want Monika to play using an engine rather than manually queued moves
            """
            return NotImplemented
        
        def poll_monika_move(self):
            """
            Polls for a Monika move

            Implement to automate Monika's moves (use for an engine)

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            It is only required if and only if we want Monika to play using an engine rather than manually queued moves
            """
            return NotImplemented
        
        def set_button_states(self):
            """
            Sets button states

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            If is only required for chess displayables which would need to manage any buttons for states
            """
            return NotImplemented
        
        def check_buttons(self, ev, x, y, st):
            """
            Runs button checks/functions if pressed

            Should be implemnted as necessary for provided buttons

            NOTE: REQUIRED for displayables with buttons added, otherwise their actions will never execute

            THROWS:
                NotImplementedError - Provided the displayable has buttons and is run
            """
            raise NotImplementedError("Function 'check_buttons' was not implemented.")
        
        def handle_monika_move(self):
            """
            Handles Monika's move

            Re-implement to allow Monika's moves to be handled by an engine
            """
            if not self.move_stack:
                return
            
            move_str = self.move_stack.pop(0)
            
            self._m1_chess__push_move(move_str)
        
        def handle_player_move(self, *args):
            """
            Handles the player's move

            Re-implement to allow the player to move pieces
            """
            if self.is_game_over:
                return
            
            if not self.move_stack:
                return
            
            move_str = self.move_stack.pop(0)
            
            self._m1_chess__push_move(move_str)
        
        
        def toggle_sensitivity(self):
            """
            Toggles sensitivity of this displayable

            OUT:
                new sensitivity as a boolean
            """
            self.sensitive = not self.sensitive
            return self.sensitive
        
        def queue_move(self, move_str):
            """
            Queues a move to the player move stack

            IN:
                move_str - uci move string
            """
            self.move_stack.append(move_str)
        
        def is_player_turn(self):
            """
            Checks if it's currently the player's turn
            """
            return self.is_player_white == self.current_turn
        
        def check_redraw(self):
            """
            Checks if we need to redraw the MASPieces on the board and redraws if necessary
            """
            if self.board.request_redraw:
                self.update_pieces()
            
            self.board.request_redraw = False
        
        def update_pieces(self):
            """
            Updates the position of all MASPieces
            """
            
            self.piece_map = dict()
            
            
            for position, Piece in self.board.piece_map().iteritems():
                MASPiece.fromPiece(
                    Piece,
                    MASChessDisplayableBase.square_to_board_coords(position),
                    self.piece_map
                )
        
        def get_piece_at(self, px, py):
            """
            Gets the piece at the given coordinates

            OUT:
                chess.Piece if exists at that location
                None otherwise
            """
            return self.piece_map.get((px, py), None)
        
        def request_highlight(self, board_pos):
            """
            Requests the renderer to draw a highlight on the square at the specified square

            IN:
                board_pos - position string representing the board square to highlight (example a2)
            """
            x = MASChessDisplayableBase.uci_alpha_to_x_coord(board_pos[0])
            y = int(board_pos[1]) - 1
            
            self.requested_highlights.add((x, y))
        
        def remove_highlight(self, board_pos):
            """
            Removes a requested highlight from the board-coordinates provided

            IN:
                board_pos - position string representing the board square to remove the highlight
            """
            x = MASChessDisplayableBase.uci_alpha_to_x_coord(board_pos[0])
            y = int(board_pos[1]) - 1
            
            self.requested_highlights.discard((x, y))
        
        def _m1_chess__push_move(self, move_str):
            """
            Internal function which pushes a uci move to the board and all MASPieces, handling promotions as necessary

            IN:
                move_str - uci string representing the move to push

            NOTE: This does NOT verify validity
            """
            
            (x1, y1), (x2, y2) = MASChessDisplayableBase.uci_to_coords(move_str)
            
            
            piece = self.get_piece_at(x1, y1)
            
            
            piece.move(x2, y2)
            
            
            if len(move_str) > 4:
                piece.promote_to(move_str[4])
            
            
            if self.is_player_turn():
                self.move_history.append(self.board.fen())
            
            self.last_move_src = (x1, y1)
            self.last_move_dst = (x2, y2)
            
            
            self.board.push_uci(move_str)
            
            
            self.check_redraw()
            
            
            if not self.current_turn:
                self.num_turns += 1
            
            
            self.current_turn = not self.current_turn
            self.is_game_over = self.board.is_game_over()
        
        def game_loop(self):
            """
            Runs the game loop
            """
            while not self.quit_game:
                
                if not self.is_player_turn() and not self.is_game_over:
                    renpy.show("monika 1dsc")
                    renpy.say(
                        m,
                        renpy.random.choice(
                            self.monika_move_quips["check"] if self.board.is_check() else self.monika_move_quips["generic"]
                        ),
                        False
                    )
                    store._history_list.pop()
                    self.handle_monika_move()
                
                
                should_update_quip = False
                quip = renpy.random.choice(
                    self.player_move_prompts["check"] if self.board.is_check() else self.player_move_prompts["generic"]
                )
                
                
                
                while self.is_player_turn() or self.is_game_over:
                    
                    renpy.show("monika 1eua")
                    if not self.is_game_over:
                        if (
                            should_update_quip
                            and "{fast}" not in quip
                        ):
                            quip = quip + "{fast}"
                        
                        should_update_quip = True
                        renpy.say(m, quip, False)
                        store._history_list.pop()
                    
                    
                    interaction = ui.interact(type="minigame")
                    
                    if self.quit_game:
                        return interaction
            return None
        
        def show(self):
            """
            Shows this displayable
            """
            ui.layer("minigames")
            ui.implicit_add(self)
            ui.close()
        
        def hide(self):
            """
            Hides this displayable
            """
            ui.layer("minigames")
            ui.remove(self)
            ui.close()
        
        def is_player_winner(self):
            """
            Checks if Monika has won the game

            OUT:
                boolean:
                    - True if Monika has won the game
                    - False if not, or the game is still in progress
            """
            result = self.board.result()
            
            return(
                (result == MASChessDisplayableBase.STATE_WHITE_WIN and self.is_player_white) 
                or (result == MASChessDisplayableBase.STATE_BLACK_WIN and not self.is_player_white) 
            )
        
        
        def render(self, width, height, st, at):
            
            
            renderer = renpy.Render(width, height)
            
            
            board = renpy.render(MASChessDisplayableBase.BOARD_IMAGE, 1280, 720, st, at)
            
            
            highlight_red = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_RED_IMAGE, 1280, 720, st, at)
            highlight_green = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_GREEN_IMAGE, 1280, 720, st, at)
            highlight_yellow = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_YELLOW_IMAGE, 1280, 720, st, at)
            highlight_magenta = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_MAGENTA_IMAGE, 1280, 720, st, at)
            
            
            mx, my = mas_getMousePos()
            
            
            visible_buttons = list()
            if self.is_game_over:
                
                visible_buttons = [
                    (b.render(width, height, st, at), b.xpos, b.ypos)
                    for b in self._visible_buttons_winner
                ]
            
            else:
                
                visible_buttons = [
                    (b.render(width, height, st, at), b.xpos, b.ypos)
                    for b in self._visible_buttons
                ]
            
            
            renderer.blit(board, (MASChessDisplayableBase.BOARD_X_POS, MASChessDisplayableBase.BOARD_Y_POS))
            
            
            renderer.blit(
                renpy.render((
                        MASChessDisplayableBase.MOVE_INDICATOR_PLAYER
                        if self.is_player_turn() else
                        MASChessDisplayableBase.MOVE_INDICATOR_MONIKA
                    ),
                    1280, 720, st, at),
                MASChessDisplayableBase.INDICATOR_POS
            )
            
            
            for b in visible_buttons:
                renderer.blit(b[0], (b[1], b[2]))
            
            
            if self.last_move_src and self.last_move_dst:
                
                highlight = highlight_magenta if self.is_player_turn() else highlight_green
                
                
                renderer.blit(
                    highlight,
                    MASChessDisplayableBase.board_coords_to_screen_coords(
                        self.last_move_src,
                        MASChessDisplayableBase.COORD_REFLECT_MAP[self.is_player_white]
                    )
                )
                
                renderer.blit(
                    highlight,
                    MASChessDisplayableBase.board_coords_to_screen_coords(
                        self.last_move_dst,
                        MASChessDisplayableBase.COORD_REFLECT_MAP[self.is_player_white]
                    )
                )
            
            
            if self.selected_piece and self.possible_moves:
                
                possible_moves_to_draw = filter(
                    lambda x: MASChessDisplayableBase.square_to_board_coords(x.from_square) == (self.selected_piece[0], self.selected_piece[1]),
                    self.possible_moves
                )
                
                for move in possible_moves_to_draw:
                    renderer.blit(
                        highlight_green,
                        MASChessDisplayableBase.board_coords_to_screen_coords(
                            MASChessDisplayableBase.square_to_board_coords(move.to_square),
                            MASChessDisplayableBase.COORD_REFLECT_MAP[self.is_player_white]
                        )
                    )
            
            
            for hl in self.requested_highlights:
                renderer.blit(highlight_yellow, MASChessDisplayableBase.board_coords_to_screen_coords(hl))
            
            
            for piece_location, Piece in self.piece_map.iteritems():
                
                ix, iy = piece_location
                
                
                iy_orig = iy
                ix_orig = ix
                
                
                if self.is_player_white:
                    iy = 7 - iy
                
                
                else:
                    
                    ix = 7 - ix
                
                x, y = MASChessDisplayableBase.board_coords_to_screen_coords((ix, iy))
                
                
                if (
                    self.selected_piece is not None
                    and ix_orig == self.selected_piece[0]
                    and iy_orig == self.selected_piece[1]
                ):
                    renderer.blit(highlight_yellow, (x, y))
                    continue
                
                piece = self.get_piece_at(ix_orig, iy_orig)
                
                possible_move_str = None
                blit_rendered = False
                
                if piece is None:
                    continue
                
                if (
                    self.selected_piece is None
                    and not self.is_game_over
                    and self.is_player_turn()
                    and mx >= x and mx < x + MASChessDisplayableBase.PIECE_WIDTH
                    and my >= y and my < y + MASChessDisplayableBase.PIECE_HEIGHT
                    and (
                        (piece.is_white and self.is_player_white)
                        or (not piece.is_white and not self.is_player_white)
                    )
                ):
                    renderer.blit(highlight_green, (x, y))
                
                
                if self.is_game_over:
                    result = self.board.result()
                    
                    
                    if piece.symbol == "K" and result == MASChessDisplayableBase.STATE_BLACK_WIN:
                        renderer.blit(highlight_red, (x, y))
                    
                    
                    elif piece.symbol == "k" and result == MASChessDisplayableBase.STATE_WHITE_WIN:
                        renderer.blit(highlight_red, (x, y))
                
                
                piece.render(width, height, st, at, x, y, renderer)
            
            if self.selected_piece is not None:
                
                piece = self.get_piece_at(self.selected_piece[0], self.selected_piece[1])
                
                px, py = mas_getMousePos()
                px -= MASChessDisplayableBase.PIECE_WIDTH / 2
                py -= MASChessDisplayableBase.PIECE_HEIGHT / 2
                piece.render(width, height, st, at, px, py, renderer)
            
            
            renpy.redraw(self, 0)
            
            
            return renderer
        
        
        def event(self, ev, x, y, st):
            
            
            if ev.type in self.MOUSE_EVENTS:
                ret_value = None
                
                if self._visible_buttons or self._visible_buttons_winner:
                    ret_value = self.check_buttons(ev, x, y, st)
                
                if ret_value is not None:
                    return ret_value
            
            elif config.developer and ev.type == pygame.KEYDOWN:
                
                if ev.key == pygame.K_d:
                    
                    if self._button_draw.disabled:
                        self._button_draw.enable()
                    else:
                        self._button_draw.disable()
            
            
            if self.sensitive:
                
                if (
                    ev.type == pygame.MOUSEBUTTONDOWN
                    and ev.button == 1
                    and not self.is_game_over
                ):
                    
                    px, py = self.get_piece_pos()
                    test_piece = self.get_piece_at(px, py)
                    if (
                        self.is_player_turn()
                        and test_piece is not None
                        and (
                            (test_piece.is_white and self.is_player_white)
                            or (not test_piece.is_white and not self.is_player_white)
                        )
                    ):
                        piece = test_piece
                        
                        self.possible_moves = self.board.legal_moves
                        self.selected_piece = (px, py)
                        return "mouse_button_down"
                
                
                if (
                    ev.type == pygame.MOUSEBUTTONUP
                    and ev.button == 1
                ):
                    self.handle_player_move()
                    
                    self.selected_piece = None
                    self.possible_moves = set([])
                    return "mouse_button_up"
            
            return None
        
        def get_piece_pos(self):
            """
            Gets the piece position of the current piece held by the mouse

            OUT:
                Tuple of coordinates (x, y) marking where the piece is
            """
            mx, my = mas_getMousePos()
            mx -= MASChessDisplayableBase.BASE_PIECE_X
            my -= MASChessDisplayableBase.BASE_PIECE_Y
            px = mx / MASChessDisplayableBase.PIECE_WIDTH
            py = my / MASChessDisplayableBase.PIECE_HEIGHT
            
            
            if self.is_player_white:
                py = 7 - py
            
            
            else:
                
                px = 7 - px
            
            if py >= 0 and py < 8 and px >= 0 and px < 8:
                return (px, py)
            
            return (None, None)
        
        @staticmethod
        def coords_to_uci(x, y):
            """
            Converts board coordinates to a uci move

            IN:
                x - x co-ord of the piece
                y - y co-ord of the piece

            OUT:
                the move represented in the uci form
            """
            x = chr(x + ord('a'))
            y += 1
            return "{0}{1}".format(x, y)
        
        @staticmethod
        def uci_to_coords(uci):
            """
            Converts uci to board-coordinates

            IN:
                uci - uci move to convert to coords

            OUT:
                list of tuples, [(x1, y1), (x2, y2)] representing from coords -> to coords
            """
            x1 = MASChessDisplayableBase.uci_alpha_to_x_coord(uci[0])
            x2 = MASChessDisplayableBase.uci_alpha_to_x_coord(uci[2])
            y1 = int(uci[1]) - 1
            y2 = int(uci[3]) - 1
            
            return [(x1, y1), (x2, y2)]
        
        @staticmethod
        def uci_alpha_to_x_coord(alpha):
            """
            Converts a uci alphabet (a-h) to an x-coord for the board

            IN:
                alpha - alphabet to convert to a board x-coord
            """
            return ord(alpha) - 97
        
        @staticmethod
        def square_to_board_coords(sq_num):
            """
            Converts from square number to board coords

            IN:
                sq_num - square number to convert

            OUT:
                tuple - (x, y) coords representing board coordinates for the square provided
            """
            return (sq_num % 8, sq_num / 8)
        
        @staticmethod
        def board_coords_to_screen_coords(pos_tuple, inversion_tuple=(False,False)):
            """
            Converts board coordinates to (x, y) coordinates to use to position things on screen

            IN:
                pos_tuple - (x, y) tuple representing coordinates which need to be converted
                inversion_tuple - (x_invert, y_invert) tuple representing direction to invert piece coords

            OUT:
                Tuple - (x, y) coordinates for the screen to use
            """
            x = pos_tuple[0]
            y = pos_tuple[1]
            
            if inversion_tuple[0]:
                x = MASChessDisplayableBase.invert_coord(x)
            if inversion_tuple[1]:
                y = MASChessDisplayableBase.invert_coord(y)
            
            return (
                int(MASChessDisplayableBase.BASE_PIECE_X + (x * MASChessDisplayableBase.PIECE_WIDTH)),
                int(MASChessDisplayableBase.BASE_PIECE_Y + (y * MASChessDisplayableBase.PIECE_HEIGHT))
            )
        
        @staticmethod
        def invert_coord(value):
            """
            Inverts a board coordinate

            IN:
                value - coordinate part (x or y) to invert
            """
            return 7 - value


    class MASPiece(object):
        """
        MASChessPiece

        A better implementation of chess.Piece which also manages piece location in addition to color and symbol

        PROPERTIES:
            color - Color of the piece:
                True - white
                False - black
            symbol - letter symbol representing the piece. If capital, the piece is white
            piece_map - the map containing all the pieces (the MASPiece object will be stored in it)
            x_pos - x coordinate of this piece on the board
            y_pos - y coordinate of this piece on the board
        """
        
        
        DEF_PIECE_FP_BASE = "mod_assets/games/chess/pieces/{0}{1}.png"
        
        
        FP_COLOR_LOOKUP = {
            True: "w",
            False: "b"
        }
        
        IMG_MAP = {
            color + (symbol.upper() if color == "w" else symbol): Image("mod_assets/games/chess/pieces/{0}{1}.png".format(color, (symbol.upper() if color == "w" else symbol)))
            for color in FP_COLOR_LOOKUP.itervalues()
            for symbol in mas_chess.PIECE_POOL
        }
        
        def __init__(
            self,
            is_white,
            symbol,
            posX,
            posY,
            piece_map
        ):
            """
            MASPiece constructor

            IN:
                is_white - Whether or not the piece is white
                symbol - letter symbol representing the piece. If capital, the piece is white
                posX - x position of the piece
                posY - y position of the piece
                piece_map - Map to store this piece in
            """
            self.is_white = is_white
            self.symbol = symbol
            
            
            self.piece_map = piece_map
            
            
            self._m1_chess__piece_image = MASPiece.IMG_MAP[MASPiece.FP_COLOR_LOOKUP[is_white] + symbol]
            
            
            self.x_pos = posX
            self.y_pos = posY
            
            
            piece_map[(posX, posY)] = self
        
        def __eq__(self, other):
            """
            Checks if this piece is the same as another piece
            """
            if not isinstance(other, MASPiece):
                return False
            return self.symbol == other.symbol
        
        def __repr__(self):
            """
            Handles a representation of this piece
            """
            return "MASPiece which: {0} and symbol: {1}".format("is white" if self.is_white else "is black", self.symbol)
        
        @staticmethod
        def fromPiece(piece, pos_tuple, piece_map):
            """
            Initializes a MASPiece from a chess.Piece object

            IN:
                piece - piece to base the MASPiece off of
                pos_tuple - (x, y) tuple representing the piece's board coords

                SEE: __init__ for the rest of the parameters

            OUT:
                MASPiece
            """
            return MASPiece(
                piece.color,
                piece.symbol(),
                pos_tuple[0],
                pos_tuple[1],
                piece_map
            )
        
        def get_type(self):
            """
            Gets the type of piece as the lowercase letter that is its symbol

            OUT:
                The lower only symbol, representing the type of piece this is
            """
            return self.symbol.lower()
        
        def get_location(self):
            """
            Gets the location of this piece

            OUT:
                Tuple, (x, y) coords representing the location of the piece on the board
            """
            return (self.x_pos, self.y_pos)
        
        def promote_to(self, promoted_piece_symbol):
            """
            Promotes this piece and builds a new render for it

            IN:
                promoted_piece_symbol - Symbol representing the piece we're promoting to
            """
            self.symbol = promoted_piece_symbol.upper() if self.is_white else promoted_piece_symbol
            
            self._m1_chess__piece_image = MASPiece.IMG_MAP[MASPiece.FP_COLOR_LOOKUP[self.is_white] + self.symbol]
        
        def move(self, new_x, new_y):
            """
            Moves the piece from the given position, to the given position
            """
            self.piece_map.pop((self.x_pos, self.y_pos))
            
            
            self.x_pos = new_x
            self.y_pos = new_y
            
            
            self.piece_map[(new_x, new_y)] = self
        
        def render(self, width, height, st, at, x, y, renderer):
            """
            Internal render call to render the pieces. To be called by the board

            IN:
                width - screen width
                height - screen height
                st - start time
                at - animation time
                x - x position on the board to render the piece
                y - y position on the board to render the piece
                renderer to draw this piece on
            """
            renderer.blit(
                renpy.render(self._m1_chess__piece_image, width, height, st, at),
                (x, y)
            )

    class MASBoard(chess.Board):
        """
        Extension class for the chess.Board class
        """
        def __init__(self, fen=None, chess960=False, casual_rules=False):
            """
            MASBoard constructor

            IN (New property):
                casual_rules:
                    - Whether or not we'll be using casual rules
                    (Default: False)

            Same as chess.Board constructor, adds two properties
            """
            if fen is None:
                fen = chess.STARTING_FEN
            
            super(MASBoard, self).__init__(fen, chess960)
            
            
            self.request_redraw = False
            self.casual_rules = casual_rules
        
        @staticmethod
        def from_board(Board, casual_rules=False):
            """
            Initializes a MASBoard from a chess.Board

            IN:
                Board - chess.Board to convert
                casual_rules - Whether or not we're using casual rules

            OUT:
                MASBoard object representing the given Board.
            """
            return MASBoard(Board.fen(), Board.chess960, casual_rules)
        
        def push(self, move):
            """
            push override

            Updates the position with the given move and puts it onto the
            move stack

            Also sets a flag which the MASChessDisplayableBase can use to manage redrawing MASPieces

            IN:
                chess.Move to push
            """
            
            self.stack.append(chess._BoardState(self))
            self.move_stack.append(move)
            
            move = self._to_chess960(move)
            
            
            ep_square = self.ep_square
            self.ep_square = None
            
            
            self.halfmove_clock += 1
            if not self.turn:
                self.fullmove_number += 1
            
            
            if not move:
                self.turn = not self.turn
                return
            
            
            if move.drop:
                self._set_piece_at(move.to_square, move.drop, self.turn)
                self.turn = not self.turn
                return
            
            
            if self.is_zeroing(move):
                self.halfmove_clock = 0
            
            from_bb = chess.BB_SQUARES[move.from_square]
            to_bb = chess.BB_SQUARES[move.to_square]
            
            promoted = self.promoted & from_bb
            piece_type = self._remove_piece_at(move.from_square)
            capture_square = move.to_square
            captured_piece_type = self.piece_type_at(capture_square)
            
            
            self.castling_rights = self.clean_castling_rights() & ~to_bb & ~from_bb
            
            if piece_type == chess.KING and not promoted:
                if self.turn:
                    self.castling_rights &= ~chess.BB_RANK_1
                else:
                    self.castling_rights &= ~chess.BB_RANK_8
            
            elif captured_piece_type == chess.KING and not self.promoted & to_bb:
                if self.turn and chess.square_rank(move.to_square) == 7:
                    self.castling_rights &= ~chess.BB_RANK_8
                
                elif not self.turn and chess.square_rank(move.to_square) == 0:
                    self.castling_rights &= ~chess.BB_RANK_1
            
            
            if piece_type == chess.PAWN:
                diff = move.to_square - move.from_square
                
                if diff == 16 and chess.square_rank(move.from_square) == 1:
                    self.ep_square = move.from_square + 8
                
                elif diff == -16 and chess.square_rank(move.from_square) == 6:
                    self.ep_square = move.from_square - 8
                
                elif move.to_square == ep_square and abs(diff) in [7, 9] and not captured_piece_type:
                    
                    down = -8 if self.turn == chess.WHITE else 8
                    capture_square = ep_square + down
                    captured_piece_type = self._remove_piece_at(capture_square)
                    
                    
                    self.request_redraw = True
            
            
            if move.promotion:
                promoted = True
                piece_type = move.promotion
            
            
            castling = piece_type == chess.KING and self.occupied_co[self.turn] & to_bb
            
            if castling:
                a_side = chess.square_file(move.to_square) < chess.square_file(move.from_square)
                
                self._remove_piece_at(move.from_square)
                self._remove_piece_at(move.to_square)
                
                if a_side:
                    self._set_piece_at(chess.C1 if self.turn == chess.WHITE else chess.C8, chess.KING, self.turn)
                    self._set_piece_at(chess.D1 if self.turn == chess.WHITE else chess.D8, chess.ROOK, self.turn)
                
                else:
                    self._set_piece_at(chess.G1 if self.turn == chess.WHITE else chess.G8, chess.KING, self.turn)
                    self._set_piece_at(chess.F1 if self.turn == chess.WHITE else chess.F8, chess.ROOK, self.turn)
                
                
                self.request_redraw = True
            
            
            if not castling and piece_type:
                was_promoted = self.promoted & to_bb
                self._set_piece_at(move.to_square, piece_type, self.turn, promoted)
                
                if captured_piece_type:
                    self._push_capture(move, capture_square, captured_piece_type, was_promoted)
            
            
            self.turn = not self.turn
        
        def result(self, claim_draw=False):
            """
            Gets the game result.

            ``1-0``, ``0-1`` or ``1/2-1/2`` if the
            :func:`game is over <chess.Board.is_game_over()>`. Otherwise, the
            result is undetermined: ``*``.
            """
            
            if self.is_variant_loss():
                return "0-1" if self.turn == chess.WHITE else "1-0"
            elif self.is_variant_win():
                return "1-0" if self.turn == chess.WHITE else "0-1"
            elif self.is_variant_draw():
                return "1/2-1/2"
            
            
            if self.is_checkmate():
                
                return "0-1" if self.turn else "1-0"
            
            
            if claim_draw and self.can_claim_draw():
                return "1/2-1/2"
            
            
            if self.is_seventyfive_moves() or self.is_fivefold_repetition():
                return "1/2-1/2"
            
            
            if self.is_insufficient_material():
                return "1/2-1/2"
            
            
            if not any(self.generate_legal_moves()):
                if self.casual_rules:
                    return "0-1" if self.turn else "1-0"
                return "1/2-1/2"
            
            
            return "*"

    class MASChessDisplayable(MASChessDisplayableBase):
        def __init__(
            self,
            is_player_white,
            pgn_game=None,
            starting_fen=None,
            practice_mode=False,
            casual_rules=False
        ):
            
            self.practice_mode = practice_mode
            self.starting_fen = starting_fen
            self.casual_rules = casual_rules
            
            self.surrendered = False
            self.practice_lost = False
            
            
            self._button_save = MASButtonDisplayable.create_stb(
                _("Guardar"),
                True,
                MASChessDisplayableBase.BUTTON_INDICATOR_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_TOP,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._button_giveup = MASButtonDisplayable.create_stb(
                _("Rendirse"),
                True,
                MASChessDisplayableBase.BUTTON_INDICATOR_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_MID,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._button_draw = MASButtonDisplayable.create_stb(
                _("Empatar"),
                True,
                MASChessDisplayableBase.BUTTON_INDICATOR_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_MID_LOW,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            
            
            self._button_draw.disable()
            
            self._button_done = MASButtonDisplayable.create_stb(
                _("Hecho"),
                False,
                MASChessDisplayableBase.BUTTON_INDICATOR_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_TOP,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._button_undo = MASButtonDisplayable.create_stb(
                _("Deshacer"),
                True,
                MASChessDisplayableBase.BUTTON_INDICATOR_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_BOT,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            
            super(MASChessDisplayable, self).__init__(
                is_player_white,
                pgn_game,
                starting_fen,
                casual_rules,
                player_move_prompts={
                    "generic": [
                        "Es tu turno, [player].",
                        "Te toca, [player]~",
                        "Me pregunto que harás...",
                        "De acuerdo, es tu turno [player]~",
                        "¡Tú puedes, [player]!"
                    ],
                    "check": [
                        "[mas_quipExp('3tfb')]¡Jaque!",
                        "[mas_quipExp('3huu')]¡Te tengo ahora, [player]!",
                        "[mas_quipExp('3hub')]¡Parece que estás en jaque!"
                    ]
                },
                monika_move_quips={
                    "generic": [
                        "De acuerdo, veamos...",
                        "Okey, mi turno...",
                        "Veamos qué puedo hacer.",
                        "Creo que intentaré esto...",
                        "Ok, entonces moveré esto aquí."
                    ],
                    "check": [
                        "[mas_quipExp('1eusdlc')]Oh...",
                        "[mas_quipExp('1rksdlc')]Hmm... {w=0.2}necesito salir de esto...",
                        "[mas_quipExp('1etc')]¿Cuál sería la mejor jugada?..."
                    ]
                }
            )
            
            if self.practice_mode:
                
                self._visible_buttons = [
                    self._button_save,
                    self._button_undo,
                    self._button_giveup,
                    self._button_draw
                ]
                
                self._visible_buttons_winner = [
                    self._button_done,
                    self._button_undo
                ]
            
            else:
                self._visible_buttons = [
                    self._button_save,
                    self._button_giveup,
                    self._button_draw
                ]
                
                self._visible_buttons_winner = [
                    self._button_done
                ]
        
        def __del__(self):
            self.stockfish.stdin.close()
            self.stockfish.wait()
        
        def poll_monika_move(self):
            """
            Polls stockfish for a move for Monika to make

            OUT:
                move - representing the best move stockfish found
            """
            with self.lock:
                res = None
                while self.queue:
                    line = self.queue.pop()
                    match = re.match(r"^bestmove (\w+)", line)
                    if match:
                        res = match.group(1)
            
            return res
        
        def start_monika_analysis(self):
            """
            Starts Monika's analysis of the board
            """
            self.stockfish.stdin.write("position fen {0}\n".format(self.board.fen()))
            self.stockfish.stdin.write("go depth {0}\n".format(persistent._mas_chess_difficulty[1]))
            self.stockfish.stdin.write("go movetime {0}\n".format(self.MONIKA_WAITTIME))
        
        def additional_setup(self):
            """
            Additional stockfish setup to get the game going using it as Monika's engine
            """
            
            def open_stockfish(path, startupinfo=None):
                """
                Runs stockfish

                IN:
                    path - filepath to the stockfish application
                    startupinfo - startup flags
                """
                try:
                    return subprocess.Popen(
                        os.path.join(renpy.config.gamedir, path).replace('\\', '/'),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        startupinfo=startupinfo
                    )
                
                
                except OSError as os_err:
                    if not renpy.windows:
                        renpy.show("monika 1etsdlc", at_list=[t11])
                        renpy.say(m, "Hmm, es extraño. Parece que algunos permisos fueron cambiados y no puedo hacer funcionar el ajedrez en tu sistema.")
                        renpy.show("monika 3eua")
                        renpy.say(m, "Dame un segundo, [player]. Voy a intentar algo rápidamente.{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                        
                        store.mas_ptod.rst_cn()
                        local_ctx = {
                            "basedir": renpy.config.basedir
                        }
                        renpy.show("monika", at_list=[t22])
                        renpy.show_screen("mas_py_console_teaching")
                        renpy.pause(1.0)
                        store.mas_ptod.wx_cmd("import subprocess", local_ctx)
                        renpy.pause(1.0)
                        store.mas_ptod.wx_cmd("import os", local_ctx)
                        renpy.pause(1.0)
                        store.mas_ptod.wx_cmd(
                            "subprocess.call(['chmod','+x', os.path.normcase(basedir + '/game/mod_assets/games/chess/stockfish_8_{0}_x64')])".format(
                                "linux" if renpy.linux else "macosx"
                            ),
                            local_ctx
                        )
                        renpy.pause(2.0)
                        
                        renpy.hide_screen("mas_py_console_teaching")
                        
                        try:
                            stockfish_proc = subprocess.Popen(
                                os.path.join(renpy.config.gamedir, path).replace('\\', '/'),
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                startupinfo=startupinfo
                            )
                            
                            renpy.show("monika 3hua", at_list=[t11])
                            renpy.say(m, "¡Yay! Deberíamos poder jugar ahora~")
                            renpy.show("monika", at_list=[t21])
                            return stockfish_proc
                        
                        
                        except Exception as ex:
                            os_err = ex
                    
                    mas_utils.mas_log.exception(os_err)
                    renpy.jump("mas_chess_cannot_work_embarrassing")
                
                
                except Exception as ex:
                    mas_utils.mas_log.exception(ex)
                    renpy.jump("mas_chess_cannot_work_embarrassing")
            
            
            if not mas_games.is_platform_good_for_chess():
                
                renpy.jump("mas_chess_cannot_work_embarrassing")
            
            is_64_bit = sys.maxsize > 2**32
            
            if renpy.windows:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                self.stockfish = open_stockfish(
                    'mod_assets/games/chess/stockfish_8_windows_x{0}.exe'.format("64" if is_64_bit else "32"),
                    startupinfo
                )
            
            elif is_64_bit:
                fp = "mod_assets/games/chess/stockfish_8_{0}_x64".format("linux" if renpy.linux else "macosx")
                
                os.chmod(config.basedir + "/game/".format(fp), 0755)
                self.stockfish = open_stockfish(fp)
            
            
            self.stockfish.stdin.write("setoption name Skill Level value {0}\n".format(persistent._mas_chess_difficulty[0]))
            self.stockfish.stdin.write("setoption name Contempt value {0}\n".format(self.MONIKA_OPTIMISM))
            self.stockfish.stdin.write("setoption name Ponder value False\n")
            
            
            self.queue = collections.deque()
            self.lock = threading.Lock()
            thrd = threading.Thread(target=store.mas_chess.enqueue_output, args=(self.stockfish.stdout, self.queue, self.lock))
            thrd.daemon = True
            thrd.start()
        
        def check_buttons(self, ev, x, y, st):
            """
            Runs button checks/functions if pressed
            """
            
            if self.is_game_over:
                if self._button_done.event(ev, x, y, st):
                    
                    self.quit_game = True
                    return self._quitPGN()
                
                elif self._button_undo.event(ev, x, y, st):
                    return self.undo_move()
            
            
            elif self.is_player_turn():
                if self._button_save.event(ev, x, y, st):
                    wants_save = renpy.call_in_new_context("mas_chess_confirm_context", prompt=_("¿Te gustaría continuar más tarde?"))
                    if wants_save:
                        
                        self.quit_game = True
                        return self._quitPGN()
                
                elif self._button_draw.event(ev, x, y, st):
                    
                    self.quit_game = True
                    return self._quitPGN(2)
                
                elif self._button_undo.event(ev, x, y, st):
                    return self.undo_move()
                
                elif self._button_giveup.event(ev, x, y, st):
                    wants_quit = renpy.call_in_new_context("mas_chess_confirm_context", prompt=_("¿Estás seguro de que quieres rendirte?"))
                    if wants_quit:
                        
                        self.quit_game = True
                        return self._quitPGN(1)
        
        def undo_move(self):
            """
            Undoes the last move

            OUT:
                None
            """
            
            
            
            last_move_fen = self.move_history.pop(-1)
            
            
            old_board = self.board
            old_board.move_stack = old_board.move_stack[:len(old_board.move_stack)-2]
            old_board.stack = old_board.stack[:len(old_board.stack)-2]
            
            
            self.board = MASBoard(fen=last_move_fen)
            
            
            self.board.move_stack = old_board.move_stack
            self.board.stack = old_board.stack
            self.board.fullmove_number = old_board.fullmove_number - 1
            
            if self.board.move_stack:
                last_move_uci = self.board.move_stack[-1].uci()
                self.last_move_src, self.last_move_dst = MASChessDisplayableBase.uci_to_coords(last_move_uci)
            
            else:
                self.last_move_src = None
                self.last_move_dst = None
            
            
            self.update_pieces()
            
            
            self.undo_count += 1
            
            
            if self.is_game_over:
                self.practice_lost = True
                self.is_game_over = False
            
            self.set_button_states()
            return None
        
        def handle_player_move(self):
            """
            Manages player move
            """
            
            if self.is_game_over:
                self.set_button_states()
                return
            
            px, py = self.get_piece_pos()
            
            move_str = None
            
            if px is not None and py is not None and self.selected_piece is not None:
                move_str = self.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) + self.coords_to_uci(px, py)
                
                
                if (
                    chess.Move.from_uci(move_str + 'q') in self.possible_moves
                    and self.get_piece_at(self.selected_piece[0], self.selected_piece[1]).get_type() == 'p'
                    and (py == 0 or py == 7)
                ):
                    
                    self.selected_piece = None
                    
                    
                    promote = renpy.call_in_new_context("mas_chess_promote_context", self.is_player_white)
                    move_str += promote
            
            if move_str is None:
                return
            
            if chess.Move.from_uci(move_str) in self.possible_moves:
                self._m1_chess__push_move(move_str)
                self.set_button_states()
                
                
                if not self.is_game_over:
                    self.start_monika_analysis()
        
        def handle_monika_move(self):
            """
            Manages Monika's move
            """
            
            if not self.is_game_over:
                
                monika_move = self.poll_monika_move()
                
                if monika_move is not None:
                    
                    monika_move_check = chess.Move.from_uci(monika_move)
                    
                    if self.board.is_legal(monika_move_check):
                        
                        renpy.pause(1.5)
                        
                        
                        self._m1_chess__push_move(monika_move)
                        
                        
                        self.set_button_states()
        
        def set_button_states(self):
            """
            Manages button states
            """
            if not self.is_game_over and self.is_player_turn():
                
                if self.board.halfmove_clock >= 40:
                    self._button_draw.enable()
                else:
                    self._button_draw.disable()
                
                
                if self.board.fullmove_number > 0:
                    self._button_giveup.enable()
                
                else:
                    self._button_giveup.disable()
                
                
                if self.board.fullmove_number > 1:
                    self._button_save.enable()
                
                else:
                    self._button_save.disable()
                
                
                self._button_done.disable()
            
            else:
                self._button_giveup.disable()
                self._button_save.disable()
                
                
                if self.is_game_over:
                    self._button_done.enable()
            
            
            if (
                self.practice_mode
                and self.move_history
                and self.is_player_turn()
                and not self.is_player_winner()
            ):
                self._button_undo.enable()
            
            else:
                self._button_undo.disable()
        
        def _quitPGN(self, quit_reason=0):
            """
            Generates a pgn of the board, and depending on if we are
            doing previous game or not, does appropriate header
            setting

            IN:
                quit_reason - reason the game was quit
                    0 - Normal savegame/victor found
                    1 - Player surrendered
                    2 - Player requested draw
                    (Default: 0)

                giveup - True if the player surrendered, False otherwise
                requested_draw - whether or not the player requested a draw

            RETURNS: tuple of the following format:
                [0]: chess.pgn.Game object of this game
                [1]: True if monika won, False if not
                [2]: True if player gaveup, False otherwise
                [3]: number of turns of this game
            """
            new_pgn = chess.pgn.Game.from_board(self.board)
            
            if quit_reason == 1:
                
                if self.is_player_white:
                    new_pgn.headers["Result"] = MASChessDisplayableBase.STATE_BLACK_WIN
                
                else:
                    new_pgn.headers["Result"] = MASChessDisplayableBase.STATE_WHITE_WIN
            
            elif quit_reason == 2:
                new_pgn.headers["Result"] = "1/2-1/2"
                
                new_pgn.headers["DrawRequested"] = True
            
            
            
            if self.is_player_white:
                new_pgn.headers["White"] = persistent.playername
                new_pgn.headers["Black"] = mas_monika_twitter_handle
            
            
            else:
                new_pgn.headers["White"] = mas_monika_twitter_handle
                new_pgn.headers["Black"] = persistent.playername
            
            
            new_pgn.headers["Site"] = "MAS"
            new_pgn.headers["Date"] = datetime.date.today().strftime("%Y.%m.%d")
            new_pgn.headers["FEN"] = self.starting_fen if self.starting_fen is not None else MASChessDisplayableBase.START_FEN
            new_pgn.headers["SetUp"] = "1"
            
            
            new_pgn.headers["Practice"] = self.practice_mode
            new_pgn.headers["CasualRules"] = self.casual_rules
            new_pgn.headers["MoveHist"] = self.move_history
            new_pgn.headers["UndoCount"] = self.undo_count
            
            
            new_pgn.headers["PracticeLost"] = self.practice_lost
            
            return (
                new_pgn,
                (
                    (
                        new_pgn.headers["Result"] == MASChessDisplayableBase.STATE_WHITE_WIN
                        and not self.is_player_white 
                    )
                    or (
                        new_pgn.headers["Result"] == MASChessDisplayableBase.STATE_BLACK_WIN
                        and self.is_player_white 
                    )
                ),
                quit_reason == 1, 
                self.board.fullmove_number
            )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
