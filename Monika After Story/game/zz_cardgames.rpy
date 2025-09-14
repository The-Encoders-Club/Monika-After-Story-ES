



default persistent._mas_game_nou_points = {"Monika": 0, "Player": 0}
default persistent._mas_game_nou_wins = {"Monika": 0, "Player": 0}
default persistent._mas_game_nou_abandoned = 0

default 10 persistent._mas_game_nou_house_rules = store.mas_nou.get_default_house_rules()


init 500 python in mas_nou:

    NOU._load_sfx()

    update_house_rules()



init 5 python in mas_nou:
    import random
    import os

    from store import (
        m,
        persistent,
        config,
        Solid,
        Null
    )
    from store.mas_cardgames import *


    ASSETS = "mod_assets/games/nou/"

    DEF_RULES_VALUES = {
        "points_to_win": 200,
        "starting_cards": 7,
        "stackable_d2": False,
        "unrestricted_wd4": False,
        "reflect_chaos": False
    }



    player_wins_this_sesh = 0
    monika_wins_this_sesh = 0

    player_win_streak = 0
    monika_win_streak = 0


    in_progress = False



    winner = None


    game = None



    disable_remind_button = False
    disable_yell_button = False


    disable_sfx = False


    class NOU(object):
        """
        A class to represent a shedding card game - NOU
        Total cards in the deck: 108
        The one who first gets rid of cards wins the round
        The one who first reaches the points cap (default 200) wins the game
        One game takes about 5-10 minutes, you keep your points through sessions
            so you can start the game in one sesh and finish it later if you wish
        """
        
        TYPES = ("number", "action", "wild")
        NUMBER_LABELS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        ACTION_LABELS = ("Skip", "Draw Two", "Reverse")
        WILD_LABELS = ("Wild", "Wild Draw Four")
        COLORS = ("rojo", "celeste", "verde", "amarillo")
        
        
        DRAWPILE_X = 445
        DRAWPILE_Y = 352
        DISCARDPILE_X = 850
        DISCARDPILE_Y = 352
        PLAYERHAND_X = 640
        PLAYERHAND_Y = 595
        MONIKAHAND_X = PLAYERHAND_X
        MONIKAHAND_Y = 110
        PLAYER_CARDS_OFFSET = 0
        MONIKA_CARDS_OFFSET = -6
        
        
        HAND_CARDS_LIMIT = 30
        
        
        SFX_EXT = ".mp3"
        
        SFX_SHUFFLE = []
        SFX_MOVE = []
        SFX_DRAW = []
        SFX_PLAY = []
        
        
        
        
        
        
        QUIPS_MONIKA_RESHUFFLE_DECK = (
            _("Oh, déjame barajar de nuevo.{w=1.5}{nw}"),
            _("Oops, vamos a intentarlo de nuevo.{w=1.5}{nw}"),
            _("Dudo que queramos un más cuatro como primera carta, jajaja~{w=1.5}{nw}"),
            _("No, no, no... vamos a barajar de nuevo...{w=1.5}{nw}")
        )
        
        
        QUIPS_MONIKA_PLAYS_TURN = (
            _("Oh, es mi turno."),
            _("Mi turno~"),
            _("Voy a tirar primero~")
        )
        QUIPS_MONIKA_SKIPS_TURN = (
            _("Oh, tengo que saltarme mi turno."),
            _("Qué suerte tienes, tendré que saltarme este turno."),
            _("Aww, tendré que saltarme mi turno.")
        )
        QUIPS_MONIKA_DRAWS_CARDS = (
            _("Oh, debo de tomar unas pocas mas."),
            _("Qué mala suerte suerte, voy a darte mucha ventaja con estas cartas."),
            _("Dios, aún más cartas para mí..."),
            _("Oh, supongo que tendré que sacar más cartas.")
        )
        QUIPS_MONIKA_WILL_REFLECT = (
            _("¡Estoy preparada! Jejeje~"),
            _("No, no, no~ ¡No voy a saltarme este turno!"),
            _("¡Nop! Esta vez te saltarás un turno~"),
            _("¡Suerte que tengo buenas cartas! Jeje~"),
            _("Estaba lista~")
        )
        
        QUIPS_PLAYER_PLAYS_TURN = (
            _("Es tu turno, cariño~"),
            _("Tu vas primero."),
            _("Tu turno, [player].")
        )
        QUIPS_PLAYER_SKIPS_TURN = (
            _("¡Ups! Tienes que saltarte tu turno."),
            _("¡Qué mala suerte!")
        )
        QUIPS_PLAYER_DRAWS_CARDS = (
            _("Adelante, saca tus cartas, jejeje~"),
            _("Uy, parece que tienes que tomar más cartas.")
        )
        
        
        
        if not persistent._mas_chess_skip_file_checks:
            QUIPS_PLAYER_CLICKS_MONIKA_CARDS = [
                _("¡[player], estas son mis cartas!"),
                _("Veo lo que estás haciendo, [player]~"),
                _("Esto es un poco embarazoso~"),
                _("¿Ah?{w=0.2} ¿Qué estás tratando de hacer?")
            ]
            if store._mas_getAffection() >= 400:
                QUIPS_PLAYER_CLICKS_MONIKA_CARDS.append(
                    _("Si es contigo, no me importaría hacer eso, [player]~")
                )
            
            else:
                QUIPS_PLAYER_CLICKS_MONIKA_CARDS.append(
                    _("No creo que estemos {i}tan{/i} lejos en nuestra relación.")
                )
        
        else:
            QUIPS_PLAYER_CLICKS_MONIKA_CARDS = (_("¿Estás tratando de hacer trampa otra vez?"),)
        
        
        QUIPS_MONIKA_CARDS_LIMIT = (
            _("[player]...{w=0.2} ¡Mira, apenas puedo sostener todas mis cartas!{w=0.5} No hay manera de que pueda tomar más, jeje~"),
        )
        QUIPS_PLAYER_CARDS_LIMIT = (
            _("No hay manera de que puedas tener más cartas, ¡jajaja!{w=0.5} No tienes que tomar todas, [player]."),
        )
        
        
        
        QUIPS_MONIKA_ANNOUNCE_COLOR_FIRST_TURN = (
            _("Creo que me iré al.{w=0.2}.{w=0.2}.{w=0.2}[store.mas_nou.game.monika.chosen_color]!"),
            _("Quiero [store.mas_nou.game.monika.chosen_color]."),
            _("Voy a escoger [store.mas_nou.game.monika.chosen_color]."),
            _("Hmm.{w=0.2}.{w=0.2}.{w=0.2} ¡Voy a escoger [store.mas_nou.game.monika.chosen_color]!")
        )
        
        QUIPS_MONIKA_ANNOUNCE_COLOR_AFTER_REFLECT = (
            _("Yo preferiría [store.mas_nou.game.monika.chosen_color]~"),
            _("Yo quiero [store.mas_nou.game.monika.chosen_color]~"),
            _("Eligo... ¡[store.mas_nou.game.monika.chosen_color]!"),
            _("Será... ¡[store.mas_nou.game.monika.chosen_color]!")
        )
        
        
        
        QUIPS_MONIKA_YELLS_NOU = (
            _("¡NOU, [player]!"),
            _("¡Solo me queda una carta, [player]! ¡NOU!"),
            _("¡NOU! ¡Sigues tú, [player]!~"),
            _("NOU [player], jejeje~"),
            _("NOU, [player]~"),
            _("NOU~"),
            _("¡Solo me queda una carta! NOU, [player]~"),
            _("Jejeje~ ¡N.{w=0.2}O.{w=0.2}U{w=0.2}!"),
            _("¡NOU [player] esta vez no ganaras!")
        )
        
        QUIPS_MONIKA_ALREADY_YELLED_NOU = (
            _("Pero [player], ¡ya dije 'NOU'!"),
            _("¡Ya he dicho 'NOU' [player]!"),
            _("Tontito, ¡ya lo hice!~"),
            _("[player]... ¿Cómo se te pasó eso? ¡Ya he dicho 'NOU'!"),
            _("Uh, [player]...{w=0.3} ¡Ya he dicho 'NOU'!")
        )
        
        QUIPS_MONIKA_DONT_NEED_YELL_NOU = (
            _("[player], ¡pero aún tienes más de una carta en tus manos!"),
            _("Tontito, gritas 'NOU' cuando solo te queda una carta."),
            _("Jajaja~ Aún es demasiado pronto, ¡[player]!"),
            _("¡Todavía no es el momento, [player]!"),
            _("[player], ¡Aún tienes [len(store.mas_nou.game.monika.hand)] cartas mas para jugar!")
        )
        
        QUIPS_MONIKA_TIMEDOUT_NOU = (
            _("¡Jejeje, demasiado tarde, [player]!"),
            _("¡Llegas demasiado tarde, [player]!"),
            _("¡Deberías haberlo hecho antes de jugar tu turno!~"),
            _("¡Es demasiado tarde ahora que has empezado tu turno!~"),
            _("¡Demasiado tarde, [player]! Esta vez puedo tirar gratis~")
        )
        
        QUIPS_MONIKA_FORGOT_YELL_NOU = (
            _("Oh... ¡Tienes razón!"),
            _("¡Uy, me has atrapado!"),
            _("Cielos, cómo se me olvidó..."),
            _("Jejeje, completamente involuntario~"),
            _("Jejeje, ¡me atrapaste!"),
            _("¡Qué tonta soy! ¡Jajaja!")
        )
        
        
        QUIPS_MONIKA_FALSE_NOU = (
            _("Esto es vergonzoso...{w=0.5} debería haber jugado una carta, pero lo olvidé...{w=0.5} lo siento, [player]."),
        )
        
        
        QUIPS_PLAYER_YELLS_NOU = (
            _("¡Te tengo!"),
            _("¡De acuerdo!"),
            _("Ya veo, ya veo..."),
            _("Okey, [player]...")
        )
        
        QUIPS_PLAYER_ALREADY_YELLED_NOU = (
            _("¡Jajaja, te tengo, [player]!"),
            _("Ya lo has dicho, tontito~"),
            _("¡Ya te escuché, [player]!"),
            _("No es necesario repetirlo otra vez, tontito~")
        )
        
        QUIPS_PLAYER_DONT_NEED_YELL_NOU = (
            _("Tontito, ¡todavía tienes muchas cartas que jugar!"),
            _("Tontito, ¡solo puedes gritar 'NOU' cuando solo te quede una carta!"),
            _("Creo que todavía tienes más de una carta, [player]."),
            _("Tienes demasiadas cartas para decir 'NOU' ahora."),
            _("¡Es un muy pronto para gritar 'NOU'. [player]!"),
            _("Debes decir 'NOU' antes de jugar tu penúltima carta, [player]."),
            _("[player], a veces puedes ser tan tontito~")
        )
        
        QUIPS_PLAYER_FORGOT_YELL_NOU = (
            _("¡Ajá!{w=0.3} ¡No has dicho NOU, [player]!"),
            _("¡Te olvidaste de decir 'NOU', [player]!"),
            _("¿Pensaste que no me daría cuenta? ¡Debiste haber dicho 'NOU'!"),
            _("Parece que alguien se olvidó de gritar 'NOU'~"),
            _("Parece que te llevarás 2 cartas por no decir 'NOU'~"),
            _("¡Te atrapé! ¡No has dicho 'NOU'!"),
            _("¡No has dicho 'NOU'! ¡Agarra dos cartas!")
        )
        
        QUIPS_PLAYER_FALSE_NOU = (
            _("Debes decir 'NOU' solo si vas a jugar una carta, [player]."),
            _("¿Por qué no has jugado una carta?"),
            _("¿Eh, [player]? ¡Debes jugar una carta después de decir 'NOU'!"),
            _("No digas 'NOU' si no vas a jugar una carta."),
            _("[player], no grites 'NOU' sin razón..."),
            _("[player], a veces puedes ser tan tontito~")
        )
        
        
        
        
        NO_REACTION = 0
        MONIKA_REFLECTED_ACT = 1
        PLAYER_REFLECTED_ACT = 2
        MONIKA_REFLECTED_WDF = 3
        PLAYER_REFLECTED_WDF = 4
        MONIKA_REFLECTED_WCC = 5
        PLAYER_REFLECTED_WCC = 6
        MONIKA_PLAYED_WILD = 7
        
        
        
        
        
        
        
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_CARD = {
            0: [
                (_("¡Nope!"),),
                (_("No lo creo, [player]~"),),
                (_("Pero, ¿estabas preparado para esto?"),)
            ],
            1: [
                (_("¡Aún no!"),),
                (_("Jejeje~ ¡Estaba lista!"),),
                (_("¡No esta vez, [player]!"),),
                (_("¡La paz nunca fue una opción!"),)
            ],
            2: [
                (_("Te leo como a un libro abierto."), _("Jajaja~")),
                (_("No me rendiré tan fácilmente~"),)
            ]
        }
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_ACT = {
            0: [
                (_("¿Pensaste que podrías atraparme desprevenida?"), _("¡Lo vi venir a kilometros de distancia! Jejeje~")),
                (_("No tan rápido, [player]~"),)
            ],
            1: [
                (_("Jejeje~ De ninguna manera, [player]~"),),
                (_("¿De {i}verdad{/i} quieres que me lleve esto, eh?~"),),
                (_("Un segundo.{w=0.2}.{w=0.2}.{w=0.2} tengo más para ti."),),
                (_("¿Qué hay de esto?~"),)
            ],
            2: [
                (_("¿Me seguirás amando{w=0.2} después de esto?"), _("Jajaja~")),
                (_("Aun tengo mas cosas para ti~"),)
            ]
        }
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_WCC = {
            0: [
                (_("Hmm...{w=0.5} no me gusta este color~"),),
                (_("Lo siento, [player] pero..."), _("este no es el color que quiero ahora~")),
                (_("[store.mas_nou.game.discardpile[-1].color.capitalize()] no es lo que quiero ahora~"),)
            ],
            1: [
                (_("¡No-no-no!"),),
                (_("Déjame...{w=0.3} elegir el color correcto~"),)
            ],
            2: [
                (_("Jejeje~"), _("¡Aún tengo mas de reserva!~"))
            ]
        }
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_WD4 = {
            0: list(REACTIONS_MAP_MONIKA_REFLECTED_ACT[0]) + [
                (_("¡No-no-no!"),),
            ],
            1: list(REACTIONS_MAP_MONIKA_REFLECTED_ACT[1]) + [
                (_("¡No puedes reflejar esto!"),),
                (_("¡No hay manera de que puedas reflejar esto!"),)
            ],
            2: list(REACTIONS_MAP_MONIKA_REFLECTED_ACT[2])
        }
        
        
        for i in range(3):
            REACTIONS_MAP_MONIKA_REFLECTED_ACT[i] += list(REACTIONS_MAP_MONIKA_REFLECTED_CARD[i])
            REACTIONS_MAP_MONIKA_REFLECTED_WCC[i] += list(REACTIONS_MAP_MONIKA_REFLECTED_CARD[i])
            REACTIONS_MAP_MONIKA_REFLECTED_WD4[i] += list(REACTIONS_MAP_MONIKA_REFLECTED_CARD[i])
        
        
        
        REACTIONS_MAP_MONIKA_PLAYED_WILD = {
            0: [
                (_("Creo que.{w=0.2}.{w=0.2}.{w=0.2} ¡Voy a elegir [store.mas_nou.game.monika.chosen_color]!"),),
                (_("Quiero [store.mas_nou.game.monika.chosen_color]."),),
                (_("Yo elijo [store.mas_nou.game.monika.chosen_color]."),),
                (_("Hmm.{w=0.1}.{w=0.1}.{w=0.1} ¡Yo elijo [store.mas_nou.game.monika.chosen_color]!"),)
            ]
        }
        
        
        
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_1 = [
            (_("Son muchas cartas para ti, jejeje~"),)
        ]
        
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_2 = [
            (_("Jejeje~ ¡Menos mal que no voy a sacar todas esas cartas!"),),
            (_("Una baraja así de grande se te da bien~"),)
        ]
        
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_3 = [
            (_("No,{w=0.1} {i}tú{/i} te saltarás este turno."),),
            (_("Jajaja~"), _("¡Nope, [player]!")),
            (_("No, creo que tú también te vas a saltar este turno~"),)
        ]
        
        
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_WD4_MODIFIER_1 = list(REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_1)
        
        
        REACTIONS_MAP_MONIKA_REFLECTED_WCC_MODIFIER_1 = [
            (_("Déjame elegir el mejor color~"),)
        ]
        
        
        
        
        REACTIONS_MAP_PLAYER_REFLECTED_CARD = {
            0: [
                (_("¡Aw, no me lo esperaba!"),),
                (_("Solo esta vez, [player]... ¡Una vez!~"),)
            ],
            1: [
                (_("De acuerdo,{w=0.1} de acuerdo...{w=0.3} tú ganas esta vez."),),
                (_("Yo.{w=0.1}.{w=0.1}.{w=0.1} lo dejaré pasar...{w=0.3} ¡Pero solo esta vez!"),),
                (_("¡Tienes mucha suerte!"),),
                (_("¡No puede ser!"),)
            ],
            2: [
                (_("Tú...{w=0.3} {i}podrías{/i} ser un poco más suave con tu novia, sabes~"), _("Jajaja~")),
                (_("¡[player]!"),),
                (_("¡Haces trampa!"),)
            ]
        }
        
        
        REACTIONS_MAP_PLAYER_REFLECTED_ACT = {
            0: [
                (_("¡Aw, qué pena!"),),
                (_("Eso es lamentable..."),)
            ],
            1: [
                (_("¡Cielos, no puedo creer que tengas otra carta!"),),
                (_("¡Cielos, realmente estás tratando de ganar!"),),
                (_("No puedes dejarlo ir, ¿eh?"),)
            ],
            2: [
                (_("¡Oh, dios mío!{w=0.2} ¡¿Cuántos de esos tienes?!"),),
                (_("Jejeje~ Pensé que esto era un simple juego entre novios, no una competencia..."), _("supongo que estaba equivocada~")),
                (_("{color=#d31f1f}{font=gui/font/VerilySerifMono.otf}Monika recordará esto.{/font}{/color}"),)
            ]
        }
        
        REACTIONS_MAP_PLAYER_REFLECTED_WCC = {
            0: [
                (_("¡Mmmm!"),),
                (_("Bueno{w=0.2}... que así sea, ¡[player]!"),)
            ],
            1: [
                (_("¡Muy bien, muy bien!~"), _("Esta vez ganas tú~")),
                (_("Bien...{w=0.2} esta vez {i}tú{/i} eliges el color~"),)
            ],
            2: [
                (_("¡Oh, dios!"),)
            ]
        }
        
        REACTIONS_MAP_PLAYER_REFLECTED_WD4 = {
            0: list(REACTIONS_MAP_PLAYER_REFLECTED_ACT[0]) + list(REACTIONS_MAP_PLAYER_REFLECTED_WCC[0]) + [
                (_("Hmm, ¡no estaba preparada para eso!"),)
            ],
            1: list(REACTIONS_MAP_PLAYER_REFLECTED_ACT[1]) + list(REACTIONS_MAP_PLAYER_REFLECTED_WCC[1]) + [
                (_("Recordaré esto~"), _("¡Cuidado, [player]!~")),
                (_("¡Vaya, tienes un montón de roba 2!"),),
                (_("¡Cielos!{w=0.2} ¡¿Cuántos de estos tienes?!"),)
            ],
            2: list(REACTIONS_MAP_PLAYER_REFLECTED_ACT[2]) + list(REACTIONS_MAP_PLAYER_REFLECTED_WCC[2]) + [
                (_("...{w=0.3} ¿Cómo lo has hecho?"), _("¡Si sigues jugando así, no tendré ninguna oportunidad!"))
            ]
        }
        
        
        for i in range(3):
            REACTIONS_MAP_PLAYER_REFLECTED_ACT[i] += list(REACTIONS_MAP_PLAYER_REFLECTED_CARD[i])
            REACTIONS_MAP_PLAYER_REFLECTED_WCC[i] += list(REACTIONS_MAP_PLAYER_REFLECTED_CARD[i])
            REACTIONS_MAP_PLAYER_REFLECTED_WD4[i] += list(REACTIONS_MAP_PLAYER_REFLECTED_CARD[i])
        
        
        
        
        
        
        REACTIONS_MAP_PLAYER_REFLECTED_ACT_MODIFIER_1 = [
            (_("Oh bien, ahora tengo toda la baraja en mis manos."), _("¡Gracias amor!"))
        ]
        
        
        REACTIONS_MAP_PLAYER_REFLECTED_WD4_MODIFIER_1 = list(REACTIONS_MAP_PLAYER_REFLECTED_ACT_MODIFIER_1)
        
        
        REACTIONS_MAP = {
            NO_REACTION: None,
            MONIKA_REFLECTED_ACT: REACTIONS_MAP_MONIKA_REFLECTED_ACT,
            PLAYER_REFLECTED_ACT: REACTIONS_MAP_PLAYER_REFLECTED_ACT,
            MONIKA_REFLECTED_WDF: REACTIONS_MAP_MONIKA_REFLECTED_WD4,
            PLAYER_REFLECTED_WDF: REACTIONS_MAP_PLAYER_REFLECTED_WD4,
            MONIKA_REFLECTED_WCC: REACTIONS_MAP_MONIKA_REFLECTED_WCC,
            PLAYER_REFLECTED_WCC: REACTIONS_MAP_PLAYER_REFLECTED_WCC,
            MONIKA_PLAYED_WILD: REACTIONS_MAP_MONIKA_PLAYED_WILD
        }
        
        
        
        TIER_REACTION_CHANCE_MAP = {
            0: 0.33,
            1: 0.66,
            2: 0.9
        }
        
        def __init__(self):
            """
            Constructor
            """
            
            self.table = Table(
                back=ASSETS + "cards/back.png",
                
                
                
                
                
                base=Null(),
                springback=0.3,
                rotate=0.15,
                can_drag=self._m1_zz_cardgames__can_drag
            )
            
            self.drawpile = self.table.stack(
                self.DRAWPILE_X,
                self.DRAWPILE_Y,
                xoff=-0.03,
                yoff=-0.08,
                click=True,
                drag=DRAG_TOP
            )
            
            self.discardpile = self.table.stack(
                self.DISCARDPILE_X,
                self.DISCARDPILE_Y,
                xoff=0.03,
                yoff=-0.08,
                drag=DRAG_TOP,
                drop=True
            )
            
            
            self.player = _NOUPlayer(leftie=persistent._mas_pm_is_righty is False)
            self.monika = _NOUPlayerAI(self, leftie=True)
            
            
            self.player.hand = self.table.stack(
                self.PLAYERHAND_X,
                self.PLAYERHAND_Y,
                xoff=self._m1_zz_cardgames__calculate_xoffset(self.player),
                yoff=0,
                click=True,
                drag=DRAG_CARD,
                drop=True,
                hover=True
            )
            self.monika.hand = self.table.stack(
                self.MONIKAHAND_X,
                self.MONIKAHAND_Y,
                xoff=self._m1_zz_cardgames__calculate_xoffset(self.monika, self.MONIKA_CARDS_OFFSET),
                yoff=0,
                click=True
            )
            
            
            self.set_sensitive(False)
            
            self.game_log = []
            
            self.current_turn = 1
            
            self._m1_zz_cardgames__fill_deck()
        
        def _m1_zz_cardgames__can_drag(self, table, stack, card):
            """
            Checks if you can drag card from stack

            OUT:
                True if you can, False otherwise
            """
            
            return not (stack is self.discardpile and len(self.discardpile) < 2)
        
        def _m1_zz_cardgames__springback_cards(self, hand):
            """
            Makes all cards in the given hand to spring back

            IN:
                hand - hand to spring back cards in
            """
            for card in hand:
                self.table.get_card(card).springback()
        
        def _m1_zz_cardgames__say_quip(self, what, interact=True, new_context=False):
            """
            Wrapper around renpy.say

            IN:
                what - a list/tuple of quips or a single quip to say
            """
            if isinstance(what, (list, tuple)):
                quip = renpy.random.choice(what)
            
            else:
                quip = what
            
            if new_context:
                renpy.invoke_in_new_context(renpy.say, m, quip, interact=interact)
            
            else:
                renpy.say(m, quip, interact=interact)
        
        @classmethod
        def _reset_sfx(cls):
            """
            Resets sfx data
            """
            cls.SFX_SHUFFLE = []
            cls.SFX_MOVE = []
            cls.SFX_DRAW = []
            cls.SFX_PLAY = []
        
        @classmethod
        def _load_sfx(cls):
            """
            'Loads' sound assets from the disk
            This should be called on init, but after class creation
            """
            nou_ma_dir = os.path.join(ASSETS, "sfx")
            nou_sfx = os.listdir(os.path.join(config.gamedir, nou_ma_dir))
            
            cls._reset_sfx()
            
            name_to_sfx_list_map = {
                "shuffle": cls.SFX_SHUFFLE,
                "move": cls.SFX_MOVE,
                "slide": cls.SFX_DRAW,
                "place": cls.SFX_PLAY,
                "shove": cls.SFX_PLAY
            }
            
            for f in nou_sfx:
                if not f.endswith(cls.SFX_EXT):
                    continue
                
                name, undscr, rest = f.partition("_")
                sfx_list = name_to_sfx_list_map.get(name, None)
                if sfx_list is None:
                    continue
                
                f = os.path.join(nou_ma_dir, f).replace("\\", "/")
                sfx_list.append(f)
        
        @staticmethod
        def _play_sfx(sfx_files, channel="sound"):
            """
            Plays a random sound from the given list

            IN:
                sfx_files - the list with the filepaths to the sounds
            """
            global disable_sfx
            
            if not sfx_files or disable_sfx:
                return
            
            sfx_file = random.choice(sfx_files)
            renpy.play(sfx_file, channel=channel)
        
        @classmethod
        def _play_shuffle_sfx(cls):
            """
            Plays an sfx for shuffling
            """
            cls._play_sfx(cls.SFX_SHUFFLE)
        
        @classmethod
        def _play_move_sfx(cls):
            """
            Plays an sfx for moving the deck
            """
            cls._play_sfx(cls.SFX_MOVE)
        
        @classmethod
        def _play_draw_sfx(cls):
            """
            Plays an sfx for drawing a card
            """
            cls._play_sfx(cls.SFX_DRAW)
        
        @classmethod
        def _play_play_sfx(cls):
            """
            Plays an sfx for playing a card
            """
            cls._play_sfx(cls.SFX_PLAY)
        
        def _m1_zz_cardgames__calculate_xoffset(self, player, shift=0):
            """
            Determines the x offset depending on quantity of cards in player's hand

            IN:
                player - the player in whose hand we change the offset
                shift - extra offset
                    (Default: 0)

            OUT:
                integer as the offset

            ASSUMES:
                Monika is a leftie
            """
            
            offset = 32
            
            if player.hand is not None:
                amount = len(player.hand)
                
                if amount > 10:
                    offset = 28
                
                elif amount > 7:
                    offset = 30
            
            if player.isAI:
                if player.leftie:
                    xoffset = offset + shift
                else:
                    xoffset = -(offset + shift)
            
            else:
                if player.leftie:
                    xoffset = -(offset + shift)
                else:
                    xoffset = offset + shift
            
            return xoffset
        
        def _m1_zz_cardgames__set_xoffset(self, player, shift=0):
            """
            Changes cards offset depending on quantity of cards in hand

            IN:
                player - the player in whose hand we change the offset
                shift - extra offset
                    (Default: 0)
            """
            player.hand.xoff = self._m1_zz_cardgames__calculate_xoffset(player, shift)
            self._m1_zz_cardgames__springback_cards(player.hand)
        
        def _m1_zz_cardgames__calculate_xpos(self, player):
            """
            Determines position of the first card
            depending on quantity of cards in player's hand

            IN:
                player - the player in whose hand we change
                    the x attribute of the card

            OUT:
                integer as the x coordinate for the hand

            ASSUMES:
                we updated (if needed) the x offset for the hand before calling this
            """
            if player.isAI:
                xpos = self.MONIKAHAND_X
            
            else:
                xpos = self.PLAYERHAND_X
            
            if player.hand is not None:
                amount = len(player.hand) - 1
                offset = player.hand.xoff
            
            else:
                amount = 6
                offset = 32
            
            xpos -= (amount * offset / 2)
            
            return xpos
        
        def _m1_zz_cardgames__set_xpos(self, player):
            """
            Changes the placement of the first card
            depending on quantity of cards in player's hand

            IN:
                player - the player in whose hand we set
                    the x attribute of the card

            ASSUMES:
                we updated (if needed) the x offset for the hand before calling this
            """
            
            player.hand.x = self._m1_zz_cardgames__calculate_xpos(player)
            self._m1_zz_cardgames__springback_cards(player.hand)
        
        def _m1_zz_cardgames__update_cards_positions(self, player, shift=0):
            """
            Updates cards positions in player's hand

            IN:
                player - the player for whose hand we update cards positions
                shift - extra offset (see __calculate_xoffset)
                    (Default: 0)
            """
            self._m1_zz_cardgames__set_xoffset(player, shift)
            self._m1_zz_cardgames__set_xpos(player)
        
        def _m1_zz_cardgames__get_card_filename(self, card):
            """
            Generates filename for a card based on its color and type

            IN:
                card - card object

            OUT:
                string with filename w/o extension
            """
            
            if card.color:
                part1 = card.color[0]
                
                if card.type == "number":
                    part2 = card.label
                else:
                    if card.label == "Skip":
                        part2 = "s"
                    elif card.label == "Draw Two":
                        part2 = "d2"
                    
                    else:
                        part2 = "r"
            
            
            else:
                part1 = ""
                
                if card.label == "Wild":
                    part2 = "wcc"
                
                else:
                    part2 = "wd4"
            
            return part1 + part2
        
        def _m1_zz_cardgames__load_card_asset(self, card):
            """
            Associates a card object with its asset, adds it to the deck and sets it face down
            # NOTE: Thanks to Velius aka big pout booplicate for these cool cards

            IN:
                card - card object
            """
            card_png = self._m1_zz_cardgames__get_card_filename(card)
            self.table.card(card, "{0}cards/{1}.png".format(ASSETS, card_png))
            self.table.set_faceup(card, False)
        
        def _m1_zz_cardgames__fill_deck(self):
            """
            Fills the deck with cards and adds them to the drawpile

            NOTE: does not shuffles the drawpile
            """
            for type in self.TYPES:
                if type != "wild":
                    for color in self.COLORS:
                        
                        if type == "number":
                            for dupe in range(2):
                                for label in self.NUMBER_LABELS:
                                    
                                    if dupe == 1 and label == "0":
                                        continue
                                    else:
                                        card = _NOUCard(type, label, color)
                                        self._m1_zz_cardgames__load_card_asset(card)
                                        self.drawpile.append(card)
                        
                        else:
                            for dupe in range(2):
                                for label in self.ACTION_LABELS:
                                    card = _NOUCard(type, label, color)
                                    self._m1_zz_cardgames__load_card_asset(card)
                                    self.drawpile.append(card)
                
                else:
                    for dupe in range(4):
                        for label in self.WILD_LABELS:
                            card = _NOUCard(type, label)
                            self._m1_zz_cardgames__load_card_asset(card)
                            self.drawpile.append(card)
        
        def _update_drawpile(self, smooth=True, sound=None):
            """
            Moves all - except the top one - cards from the discardpile
            onto the drawpile, then shuffles drawpile

            IN:
                smooth - bool, if True we use pause
                sound - bool, if True we play sfx, if None, defaults to smooth
                    (Default: None)
            """
            if sound is None:
                sound = smooth
            
            if smooth:
                renpy.pause(0.5, hard=True)
            if sound:
                self._play_move_sfx()
            
            while len(self.discardpile) > 1:
                card = self.discardpile[0]
                
                
                if card.type == "wild":
                    card.color = None
                
                self.table.set_faceup(card, False)
                self.table.set_rotate(card, 0)
                self.table.get_card(card).set_offset(0, 0)
                
                self.drawpile.append(card)
            
            if smooth:
                renpy.pause(0.2, hard=True)
            
            
            last_card = self.table.get_card(self.discardpile[0])
            self.table.set_rotate(last_card.value, 90)
            last_card.set_offset(0, 0)
            
            self.shuffle_drawpile(smooth=smooth, sound=sound)
        
        def _update_game_log(self, current_player, next_player):
            """
            Updates the log with the actions/attributes of the current and next players
            We can back in to any turn and check what happened there

            NOTE: have to do fill the log in 2 steps:
                1. write first bits when the previous player ends their turn
                2. add more data after the current player ends their turn
                and so on

            NOTE: for the reason above we update the log in prepare_game()
                for the 1st time

            IN:
                current_player - the player who ends their turn
                next_player - next played
            """
            next_player_data = {
                "turn": self.current_turn + 1,
                "player": next_player,
                "had_skip_turn": next_player.should_skip_turn,
                "had_draw_cards": next_player.should_draw_cards,
                "drew_card": None,
                "played_card": None
            }
            
            current_player_data = {
                "drew_card": current_player.drew_card,
                "played_card": self.discardpile[-1] if current_player.played_card else None
            }
            
            self.game_log[-1].update(current_player_data)
            self.game_log.append(next_player_data)
        
        def end_turn(self, current_player, next_player):
            """
            Updates players' attributes at the end of turn
            Also switches sensitivity and makes sure that the drawpile has cards

            IN:
                current_player - the player who ends their turn
                next_player - next player

            ASSUMES:
                mas_nou.disable_remind_button
                mas_nou.disable_yell_button
            """
            global disable_remind_button
            global disable_yell_button
            
            
            disable_remind_button = False
            disable_yell_button = False
            
            if not self.drawpile:
                
                
                renpy.invoke_in_new_context(self._update_drawpile)
            
            self._update_game_log(current_player, next_player)
            
            
            
            
            
            if current_player.yelled_nou:
                
                if len(current_player.hand) > 1:
                    current_player.yelled_nou = False
                    current_player.nou_reminder_timeout = 0
                
                
                if current_player.should_play_card:
                    
                    
                    if current_player.isAI:
                        quips = self.QUIPS_MONIKA_FALSE_NOU
                    
                    else:
                        quips = self.QUIPS_PLAYER_FALSE_NOU
                    
                    self.set_sensitive(False)
                    self._m1_zz_cardgames__say_quip(quips, new_context=True)
                    
                    current_player.should_play_card = False
            
            current_player.should_skip_turn = False
            current_player.plays_turn = False
            
            
            if (
                next_player.should_draw_cards
                and len(next_player.hand) + next_player.should_draw_cards > self.HAND_CARDS_LIMIT
            ):
                if next_player.isAI:
                    quips = self.QUIPS_MONIKA_CARDS_LIMIT
                
                else:
                    quips = self.QUIPS_PLAYER_CARDS_LIMIT
                
                self.set_sensitive(False)
                self._m1_zz_cardgames__say_quip(quips, new_context=True)
                
                
                
                next_player.should_draw_cards = max(self.HAND_CARDS_LIMIT - len(next_player.hand), 0)
            
            next_player.drew_card = False
            next_player.played_card = False
            next_player.plays_turn = True
            
            self.current_turn += 1
            
            self.set_sensitive(not next_player.isAI)
        
        def _win_check(self, player):
            """
            Checks if player can win the game (has no cards left)
            If we have a winner, we update wins and jump to the end game label
            The rest will be handled in the label

            IN:
                player - the player we check
            """
            global winner
            if player.hand:
                return
            
            self.set_sensitive(False)
            
            if player.isAI:
                winner = "Monika"
            
            else:
                winner = "Player"
            
            persistent._mas_game_nou_wins[winner] += 1
            
            renpy.pause(2, hard=True)
            renpy.jump("mas_nou_game_end")
        
        def _is_matching_card(self, player, card):
            """
            Checks if the given card matches the top card in the discardpile

            IN:
                player - the player who tries to play the card
                card - the card the player wants to play

            OUT:
                True if the player can play the card, False otherwise

            ASSUMES:
                len(discardpile) > 0
            """
            
            if card not in player.hand:
                return False
            
            def has_color(hand, color):
                """
                Checks if there's a card with the given color in the given hand
                NOTE: to avoid unwanted incidents, we don't check cards w/o color

                IN:
                    hand - the hand we check
                    color - the color we're looking for

                OUT:
                    True if there is a card with that color, False otherwise
                """
                return color in {card.color for card in hand if card.color is not None}
            
            
            if not player.should_skip_turn:
                return (
                    card.label == "Wild"
                    or (
                        card.label == "Wild Draw Four"
                        and (
                                get_house_rule("unrestricted_wd4")
                                or not has_color(player.hand, self.discardpile[-1].color)
                        )
                    )
                    or card.color == self.discardpile[-1].color
                    or card.label == self.discardpile[-1].label
                )
            
            
            else:
                return (
                    (
                        self.discardpile[-1].label == "Wild Draw Four"
                        and (
                            (
                                card.label == "Draw Two"
                                and self.discardpile[-1].color == card.color
                            )
                            or (
                                get_house_rule("reflect_chaos")
                                and card.label == "Wild Draw Four"
                            )
                        )
                    )
                    or (
                        self.discardpile[-1].label == "Draw Two"
                        and (
                            card.label == "Draw Two"
                            or (
                                get_house_rule("reflect_chaos")
                                and card.label == "Wild Draw Four"
                            )
                        )
                    )
                    or (
                        self.discardpile[-1].label == "Skip"
                        and card.label == "Skip"
                        and (
                            self.discardpile[-1].color == card.color
                            or get_house_rule("reflect_chaos")
                        )
                    )
                    or (
                        self.discardpile[-1].label == "Reverse"
                        and card.label == "Reverse"
                    )
                )
        
        def play_card(self, current_player, next_player, card):
            """
            A method to play cards and change players' attributes
            NOTE: this doesn't check if the card matches

            IN:
                current_player - the player who plays card
                next_player - the player who will be affected by card if any
                card - card to play
            """
            
            if current_player.isAI:
                cards_offset = self.MONIKA_CARDS_OFFSET
                card_rotation = renpy.random.randint(-193, -167)
            
            else:
                cards_offset = self.PLAYER_CARDS_OFFSET
                card_rotation = renpy.random.randint(-13, 13)
            
            card_position = (renpy.random.randint(-14, 14), renpy.random.randint(-10, 10))
            
            
            self._play_play_sfx()
            self.discardpile.append(card)
            self.table.set_rotate(self.discardpile[-1], card_rotation)
            self.table.get_card(self.discardpile[-1]).set_offset(*card_position)
            self.table.set_faceup(self.discardpile[-1], True)
            
            self._m1_zz_cardgames__update_cards_positions(current_player, cards_offset)
            
            
            current_player.played_card = True
            current_player.should_play_card = False
            
            if self.discardpile[-1].type == "action" or self.discardpile[-1].label == "Wild Draw Four":
                next_player.should_skip_turn = True
                current_player.should_skip_turn = False
                
                if self.discardpile[-1].label == "Draw Two":
                    next_player.should_draw_cards = 2
                    
                    if get_house_rule("stackable_d2"):
                        next_player.should_draw_cards += current_player.should_draw_cards
                    
                    current_player.should_draw_cards = 0
                
                elif self.discardpile[-1].label == "Wild Draw Four":
                    next_player.should_draw_cards = 4
                    
                    if get_house_rule("reflect_chaos") and get_house_rule("stackable_d2"):
                        next_player.should_draw_cards += current_player.should_draw_cards
                    
                    current_player.should_draw_cards = 0
            
            
            
            if len(current_player.hand) == 1:
                current_player.nou_reminder_timeout = self.current_turn + 2
        
        def _actually_deal_cards(self, player, amount, smooth, sound):
            """
            Moves cards from the drawpile into player's hand,
            updates offsets, rotation and sets cards faceup if needed

            NOTE: Unsafe to use this directly, we use deal_cards

            IN:
                player - the player who will get the cards
                amount - amount of cards to deal
                smooth - whether or not we use a little pause between dealing cards
                sound - whether or not we play sfx
            """
            player_cards = len(player.hand)
            if player_cards + amount > self.HAND_CARDS_LIMIT:
                amount = self.HAND_CARDS_LIMIT - player_cards
            
            for i in range(amount):
                if sound:
                    self._play_draw_sfx()
                card = self.drawpile[-1]
                player.hand.append(card)
                
                if player.isAI:
                    self.table.set_rotate(card, -180)
                    faceup = False
                    offset = self.MONIKA_CARDS_OFFSET
                
                else:
                    faceup = True
                    offset = self.PLAYER_CARDS_OFFSET
                
                self.table.set_faceup(card, faceup)
                self._m1_zz_cardgames__update_cards_positions(player, offset)
                
                if smooth:
                    renpy.pause(0.3, hard=True)
        
        def deal_cards(self, player, amount=1, smooth=True, sound=None, mark_as_drew_card=True, reset_nou_var=True):
            """
            Deals cards to players
            Also refreshing the drawpile if there're not enough cards

            IN:
                player - the player whose hand we deal cards in
                amount - amount of cards to deal
                    (Default: 1)
                smooth - whether or not we use a little pause between dealing cards
                    (Default: True)
                sound - whether or not we play sfx, if None defaults to smooth
                    (Default: None)
                mark_as_drew_card - whether or not we set the var for the player
                    (Default: True)
                reset_nou_var - whether or not we reset the nou var for the player who draws cards
                    (Default: True)
            """
            if sound is None:
                sound = smooth
            
            drawpile_cards = len(self.drawpile)
            
            if mark_as_drew_card:
                player.drew_card = True
            if reset_nou_var:
                player.yelled_nou = False
                player.nou_reminder_timeout = 0
            
            
            if drawpile_cards >= amount:
                self._actually_deal_cards(player, amount, smooth, sound=sound)
                
                if player.should_draw_cards:
                    player.should_draw_cards -= amount
                
                if drawpile_cards == amount:
                    
                    self._update_drawpile(smooth=smooth, sound=sound)
            
            
            else:
                
                cards_to_deal = amount - drawpile_cards
                self._actually_deal_cards(player, drawpile_cards, smooth, sound=sound)
                
                if player.should_draw_cards:
                    player.should_draw_cards -= drawpile_cards
                
                self._update_drawpile(smooth=smooth, sound=sound)
                drawpile_cards = len(self.drawpile)
                
                
                if drawpile_cards < cards_to_deal:
                    self._actually_deal_cards(player, drawpile_cards, smooth, sound=sound)
                    player.should_draw_cards = 0
                
                
                else:
                    self._actually_deal_cards(player, cards_to_deal, smooth, sound=sound)
                    player.should_draw_cards = 0
        
        def _get_current_next_players(self):
            """
            Returns current and next player for the first turn

            OUT:
                tuple of 2 items
            """
            global player_win_streak
            global monika_win_streak
            
            if player_win_streak:
                current_player = self.player
                next_player = self.monika
            
            elif monika_win_streak:
                current_player = self.monika
                next_player = self.player
            
            else:
                if random.random() < 0.5:
                    current_player = self.player
                    next_player = self.monika
                
                else:
                    current_player = self.monika
                    next_player = self.player
            
            return (current_player, next_player)
        
        def _deal_initial_cards(self, current_player, next_player):
            starting_cards = get_house_rule("starting_cards")
            
            if starting_cards < 12:
                for i in range(0, starting_cards*2):
                    if i % 2:
                        temp_player = next_player
                    else:
                        temp_player = current_player
                    
                    self.deal_cards(temp_player, mark_as_drew_card=False, reset_nou_var=False)
            
            
            else:
                extra_step = 1 if starting_cards % 2 else 0
                for i in range(0, starting_cards + extra_step):
                    if i % 2:
                        temp_player = next_player
                    else:
                        temp_player = current_player
                    
                    if len(temp_player.hand) + 2 <= starting_cards:
                        
                        self.deal_cards(temp_player, smooth=False, mark_as_drew_card=False, reset_nou_var=False)
                    
                    self.deal_cards(temp_player, mark_as_drew_card=False, reset_nou_var=False)
        
        def prepare_game(self):
            """
            This method sets up everything we need to start a game of NOU:
                1. Chooses who plays first
                2. Shuffles the deck
                3. Deals cards
                4. Places first card onto the discardpile
                    and handles if it's an action/wild card
                5. Fills first bits in the log
                6. Makes our table sensetive to the user's imput
                    if needed
            """
            
            current_player, next_player = self._get_current_next_players()
            
            self.shuffle_drawpile()
            
            
            self._deal_initial_cards(current_player, next_player)
            
            
            ready = False
            pulled_wdf = False
            
            while not ready:
                card = self.drawpile[-1]
                
                self._play_draw_sfx()
                
                self.discardpile.append(card)
                self.table.set_rotate(card, 90)
                self.table.set_faceup(card, True)
                
                if card.label == "Wild Draw Four":
                    if not pulled_wdf:
                        pulled_wdf = True
                        self._m1_zz_cardgames__say_quip(
                            self.QUIPS_MONIKA_RESHUFFLE_DECK
                        )
                        renpy.pause(0.5, hard=True)
                    
                    else:
                        renpy.pause(1, hard=True)
                    
                    
                    new_id = len(self.drawpile) / 2 + renpy.random.randint(-10, 10)
                    
                    self._play_draw_sfx()
                    
                    self.drawpile.insert(new_id, card)
                    self.table.set_rotate(card, 0)
                    self.table.set_faceup(card, False)
                    
                    renpy.pause(0.1, hard=True)
                    self.shuffle_drawpile()
                
                else:
                    ready = True
            
            
            if self.discardpile[-1].label == "Wild":
                
                if current_player.isAI:
                    self.monika.chosen_color = self.monika.choose_color()
                    self.discardpile[-1].color = self.monika.chosen_color
            
            
            elif self.discardpile[-1].type == "action":
                current_player.should_skip_turn = True
                
                
                if self.discardpile[-1].label == "Draw Two":
                    current_player.should_draw_cards = 2
            
            
            current_player_data = {
                "turn": self.current_turn,
                "player": current_player,
                "had_skip_turn": current_player.should_skip_turn,
                "had_draw_cards": current_player.should_draw_cards,
                "drew_card": None,
                "played_card": None
            }
            self.game_log.append(current_player_data)
            
            if current_player.isAI:
                if current_player.should_skip_turn:
                    can_reflect = current_player.choose_card(should_draw=False)
                    
                    if can_reflect:
                        quips = self.QUIPS_MONIKA_WILL_REFLECT
                    
                    elif current_player.should_draw_cards:
                        quips = self.QUIPS_MONIKA_DRAWS_CARDS
                    
                    else:
                        quips = self.QUIPS_MONIKA_SKIPS_TURN
                
                else:
                    quips = self.QUIPS_MONIKA_PLAYS_TURN
            
            else:
                if current_player.should_skip_turn:
                    if current_player.should_draw_cards:
                        quips = self.QUIPS_PLAYER_DRAWS_CARDS
                    
                    else:
                        quips = self.QUIPS_PLAYER_SKIPS_TURN
                
                else:
                    quips = self.QUIPS_PLAYER_PLAYS_TURN
            
            renpy.pause(0.5, hard=True)
            
            
            self._m1_zz_cardgames__say_quip(
                quips
            )
            
            if current_player.isAI and self.discardpile[-1].label == "Wild":
                self._m1_zz_cardgames__say_quip(
                    self.QUIPS_MONIKA_ANNOUNCE_COLOR_FIRST_TURN
                )
                
                self.monika.chosen_color = None
            
            
            current_player.plays_turn = True
            self.set_sensitive(not current_player.isAI)
        
        def reset_game(self):
            """
            Reinitialize the game so you can start another round
            """
            del self.monika, self.player, self.drawpile, self.discardpile, self.table
            self.__init__()
        
        def player_turn_loop(self):
            """
            Tracks the player's actions and responds to their interactions
            """
            def is_player_allowed_draw_card():
                """
                Unified check whether the player can draw a card

                OUT:
                    bool
                """
                return (
                    
                    self.discardpile[-1].color is not None
                    
                    and not (
                        
                        
                        (
                            self.player.drew_card
                            or self.player.should_skip_turn
                        )
                        
                        and not self.player.should_draw_cards
                    )
                    
                    and len(self.player.hand) < self.HAND_CARDS_LIMIT
                )
            
            def is_player_allowed_play_card():
                """
                Unified check whether the player can play a card

                OUT:
                    bool
                """
                return (
                    
                    self.discardpile[-1].color is not None
                    
                    and not self.player.played_card
                    
                    and not (self.player.should_skip_turn and self.player.drew_card)
                )
            
            def player_play_card(card_to_play):
                """
                Unified method to play a card
                DOES NOT CHECK WHETHER OR NOT THE PLAYER IS ALLOWED TO PLAY

                IN:
                    card_to_play - the card to play
                """
                if not self._is_matching_card(self.player, card_to_play):
                    return
                
                self.set_sensitive(False)
                self.play_card(self.player, self.monika, card_to_play)
                self.set_sensitive(True)
                
                self._win_check(self.player)
                
                
                if self.discardpile[-1].color is not None:
                    self.end_turn(self.player, self.monika)
            
            while self.player.plays_turn:
                events = ui.interact(type="minigame")
                
                for event in events:
                    if event.type == "hover":
                        if event.card in self.player.hand:
                            
                            card = self.table.get_card(event.card)
                            
                            card.set_offset(0, -35)
                            card.springback()
                            
                            stack = card.stack
                            self.table.stacks.remove(stack)
                            self.table.stacks.append(stack)
                    
                    elif event.type == "unhover":
                        if event.card in self.player.hand:
                            card = self.table.get_card(event.card)
                            
                            card.set_offset(0, 0)
                            card.springback()
                    
                    elif event.type == "doubleclick":
                        
                        if (
                            event.stack is self.drawpile
                            and is_player_allowed_draw_card()
                        ):
                            self.set_sensitive(False)
                            
                            if self.player.should_draw_cards:
                                self.deal_cards(self.player, self.player.should_draw_cards)
                            else:
                                self.deal_cards(self.player)
                            
                            self.set_sensitive(True)
                        
                        
                        elif (
                            event.stack is self.player.hand
                            and event.card is not None
                            and is_player_allowed_play_card()
                        ):
                            player_play_card(event.card)
                    
                    elif event.type == "drag":
                        
                        
                        
                        
                        
                        
                        if (
                            event.stack is self.drawpile
                            and event.drop_stack is self.player.hand
                            and is_player_allowed_draw_card()
                        ):
                            self.set_sensitive(False)
                            self.deal_cards(self.player)
                            self.set_sensitive(True)
                        
                        
                        elif (
                            event.stack is self.player.hand
                            and event.drop_stack is self.discardpile
                            and is_player_allowed_play_card()
                        ):
                            player_play_card(event.card)
                    
                    elif event.type == "click":
                        if (
                            event.stack is self.monika.hand
                            and random.random() < 0.2
                        ):
                            self._m1_zz_cardgames__say_quip(
                                self.QUIPS_PLAYER_CLICKS_MONIKA_CARDS
                            )
        
        def monika_turn_loop(self):
            """
            Monika's actions during her turn
            Yes, I know that this isn't a loop
            """
            if not self.monika.plays_turn:
                return
            
            self.monika.thonk_pause()
            self.monika.shuffle_hand()
            self.monika.thonk_pause()
            
            self.monika.guess_player_cards()
            next_card_to_play = self.monika.choose_card()
            reaction = self.monika.choose_reaction(next_card_to_play)
            self.monika.announce_reaction(reaction)
            self.monika.play_card(next_card_to_play)
            
            self.end_turn(self.monika, self.player)
        
        def game_loop(self):
            """
            This wrapper is supposed to be called in the main while loop
            """
            self.monika_turn_loop()
            self.player_turn_loop()
        
        def set_visible(self, value):
            """
            Shows/Hides cards on the table

            IN:
                value - True/False
            """
            if value:
                self.table.show()
            else:
                self.table.hide()
        
        def set_sensitive(self, value):
            """
            Make cards (in-)sensitive to the player's input

            IN:
                value - True/False
            """
            self.table.set_sensitive(value)
        
        def is_sensitive(self):
            """
            Checks if the table is sensitive to the input

            OUT:
                True if sensitive, False otherwise
            """
            return self.table.sensitive
        
        def shuffle_drawpile(self, smooth=True, sound=None):
            """
            Shuffles the drawpile and animates cards shuffling

            IN:
                smooth - bool, if True we use pause for animation
                    (Default: True)
                sound - bool, if True, we play sfx, if None, defaults to smooth
                    (Default: None)

            ASSUMES:
                len(drawpile) > 15
            """
            if sound is None:
                sound = smooth
            
            total_cards = len(self.drawpile)
            
            
            if total_cards > 15:
                if sound:
                    self._play_shuffle_sfx()
                
                k = renpy.random.randint(0, 9)
                
                self.table.springback = 0.2
                if smooth:
                    renpy.pause(0.2, hard=True)
                
                for i in range(7):
                    card_id = renpy.random.randint(0, total_cards - 2)
                    if k == i:
                        insert_id = total_cards - 1
                    else:
                        insert_id = renpy.random.randint(0, total_cards - 2)
                    
                    card = self.table.get_card(self.drawpile[card_id])
                    
                    x_offset = renpy.random.randint(160, 190)
                    y_offset = renpy.random.randint(-15, 15)
                    
                    card.set_offset(x_offset, y_offset)
                    card.springback()
                    if smooth:
                        renpy.pause(0.15, hard=True)
                    
                    self.drawpile.insert(insert_id, card.value)
                    
                    card.set_offset(0, 0)
                    card.springback()
                    if smooth:
                        renpy.pause(0.15, hard=True)
                
                
                self.table.springback = 0.3
            
            self.drawpile.shuffle()
            if smooth:
                renpy.pause(0.2, hard=True)
        
        def handle_nou_logic(self, player):
            """
            A method that handles "yelling system" from the player side
            NOTE: Everything here must be called in a new context
                since we 100% will have an active interaction when we get here.
                We also toggle the sensitivity so you don't skip the dlg

            IN:
                player - 'name' of the player we will check for nou
                    (either 'monika' or 'player')

            ASSUMES:
                the player didn't start to play their turn
            """
            self.set_sensitive(False)
            
            if player == "monika":
                if self.monika.yelled_nou:
                    self._m1_zz_cardgames__say_quip(self.QUIPS_MONIKA_ALREADY_YELLED_NOU, new_context=True)
                
                elif len(self.monika.hand) > 1:
                    self._m1_zz_cardgames__say_quip(self.QUIPS_MONIKA_DONT_NEED_YELL_NOU, new_context=True)
                
                elif self.monika.nou_reminder_timeout <= self.current_turn:
                    self._m1_zz_cardgames__say_quip(self.QUIPS_MONIKA_TIMEDOUT_NOU, new_context=True)
                
                else:
                    self._m1_zz_cardgames__say_quip(self.QUIPS_MONIKA_FORGOT_YELL_NOU, new_context=True)
                    
                    self.deal_cards(self.monika, amount=2, smooth=False, sound=True, mark_as_drew_card=False)
                    renpy.invoke_in_new_context(renpy.pause, 0.5, hard=True)
            
            elif player == "player":
                if self.player.yelled_nou:
                    self._m1_zz_cardgames__say_quip(self.QUIPS_PLAYER_ALREADY_YELLED_NOU, new_context=True)
                
                
                elif len(self.player.hand) > 2:
                    self._m1_zz_cardgames__say_quip(self.QUIPS_PLAYER_DONT_NEED_YELL_NOU, new_context=True)
                
                else:
                    
                    if random.random() < 0.25:
                        self._m1_zz_cardgames__say_quip(self.QUIPS_PLAYER_YELLS_NOU, new_context=True)
                    
                    self.player.yelled_nou = True
                    self.player.should_play_card = True
                    self.player.nou_reminder_timeout = 0
            
            self.set_sensitive(True)
        
        def _select_help(self):
            """
            Method to help the player if they are "stuck"

            OUT:
                string
            """
            global monika_win_streak, player_win_streak
            
            player = self.player
            monika = self.monika
            discardpile = self.discardpile
            
            
            if (
                not discardpile
                or not player.plays_turn
                or player.played_card
            ):
                return "Lo siento, no estoy segura [player]..."
            
            card = discardpile[-1]
            
            if get_total_games() > 15 and random.random() < 0.2:
                if player.should_skip_turn:
                    return "El botón para rendirse está justo debajo~"
                
                elif (
                    
                    sum(
                        log_data["had_draw_cards"]
                        for log_data in self.game_log[-2:-21:-2]
                        if log_data["drew_card"]
                    ) > 10
                ):
                    return "Encuentra una baraja mejor, esta está amañada..."
                
                elif (
                    (player.hand and len(monika.hand)/len(player.hand) < 0.7)
                    or monika_win_streak > 2
                ):
                    return "¡Solo no seas noob, [player]! Jajaja~"
                
                elif (
                    (monika.hand and len(player.hand)/len(monika.hand) < 0.7)
                    or player_win_streak > 2
                ):
                    return "Juega a cualquier cosa menos {i}Roba Dos{/i} y {i}Roba Cuatro{/i}, querido. No tengo nada para contrarrestar esos~"
                
                else:
                    return "Simplemente roba más cartas, siempre funciona~"
            
            
            dlg_line_list = []
            
            if card.type == "number":
                dlg_line_list.append(
                    "Tienes que jugar un{} '{}' o cualquier {} carta.".format(
                        "n" if card.label == "8" else "",
                        card.label,
                        card.color
                    )
                )
                
                if player.drew_card:
                    dlg_line_list.append(
                        " Como has robado una carta, puedes intentar jugarla o saltarte el turno."
                    )
                
                elif len(player.hand) >= self.HAND_CARDS_LIMIT:
                    dlg_line_list.append(
                        " Si no tienes una carta apropiada, entonces tendrás que saltarte este turno."
                    )
                
                else:
                    dlg_line_list.append(
                        " Si no tienes una carta apropiada, debes robar una carta y luego jugarla o saltarte el turno."
                    )
            
            else:
                if player.should_skip_turn:
                    dlg_line_list.append("Tienes que saltarte este turno.")
                    
                    insert_line = (
                        len(self.game_log) > 2
                        and self.game_log[-3]["had_skip_turn"]
                        and random.random() < 0.33
                    )
                    
                    if insert_line:
                        dlg_line_list.append("--Tal como el anterior--")
                    
                    if player.should_draw_cards and len(player.hand) < self.HAND_CARDS_LIMIT:
                        dlg_line_list.append(
                            "{}y robo {}".format(
                                "" if insert_line else " ",
                                player.should_draw_cards
                            )
                        )
                        if player.drew_card:
                            dlg_line_list.append(" more")
                        
                        dlg_line_list.append(
                            " carta{}".format(
                                "s" if player.should_draw_cards != 1 else ""
                            )
                        )
                    
                    dlg_line_list.append(".")
                    
                    if not player.drew_card:
                        if not get_house_rule("reflect_chaos"):
                            if card.type == "action":
                                card_for_reflect = card.label
                                if card.label == "Skip":
                                    color_for_reflect = card.color
                                else:
                                    color_for_reflect = ""
                            
                            else:
                                card_for_reflect = "Draw Two"
                                color_for_reflect = card.color
                        
                        else:
                            if card.type == "action":
                                if card.label == "Draw Two":
                                    card_for_reflect = "Draw Two{/i} or {i}Draw Four"
                                
                                else:
                                    card_for_reflect = card.label
                                
                                color_for_reflect = ""
                            
                            else:
                                card_for_reflect = "Draw Two{/i} or {i}Draw Four"
                                color_for_reflect = card.color
                        
                        dlg_line_list.append(
                            " Si tienes una {}{}{{i}}{}{{/i}}, podrías {{i}}intentar{{/i}} reflejar la carta{}.".format(
                                color_for_reflect,
                                "" if not color_for_reflect else " ",
                                card_for_reflect,
                                "my" if self.monika.played_card else "the top"
                            )
                        )
                        if random.random() < 0.33:
                            if random.random() < 0.5:
                                dlg_line_list.append(
                                    " No puedo prometerte que no te lo reflejaré.~"
                                )
                            else:
                                dlg_line_list.append("... Si eres lo suficientemente valiente~")
                
                else:
                    if card.type == "action":
                        dlg_line_list.append(
                            "Es necesario jugar una {{i}}{}{{/i}} o cualquier {} carta.".format(
                                card.label,
                                card.color
                            )
                        )
                    
                    else:
                        if card.color is None:
                            dlg_line_list.append(
                                "Debes elegir un color antes de continuar."
                            )
                        
                        else:
                            dlg_line_list.append(
                                "Tienes que jugar cualquier {} carta.".format(card.color)
                            )
                            
                            if player.drew_card or len(player.hand) >= self.HAND_CARDS_LIMIT:
                                dlg_line_list.append(
                                    " De lo contrario tendrás que saltarte tu turno~"
                                )
                            
                            else:
                                dlg_line_list.append(
                                    " Si no, roba una carta e intenta jugarla."
                                )
            
            if dlg_line_list:
                return "".join(dlg_line_list)
            
            return "Lo siento, no estoy segura, [player]..."
        
        def say_help(self):
            """
            Method to say the selected advice
            """
            advice = self._select_help()
            self.set_sensitive(False)
            renpy.invoke_in_new_context(renpy.say, m, advice, interact=True)
            self.set_sensitive(True)


    class _NOUCard(object):
        """
        A class to represent a card

        PROPERTIES:
            type - (str) number, action or wild
            label - (str) number/action on card '0'-'9', "Draw Two", etc
            color - (str/None) red, blue, green, yellow or None
                (Default: None (colorless))
            value - (int) how much points the card gives
        """
        def __init__(self, t, l, c=None):
            """
            Constructor

            IN:
                t - type of the card
                l - the card's label
                c - the card's color
                    (Default: None)
            """
            self.type = t
            self.label = l
            self.color = c
        
        @property
        def value(self):
            """
            Cards values can be dynamically calculated
            """
            if self.type == "number":
                v = int(self.label)
            
            elif self.type == "action":
                v = 20
            
            else:
                v = 50
            
            return v
        
        def __repr__(self):
            if self.color is not None:
                card_info = "'{} {}'".format(self.color.capitalize(), self.label)
            
            else:
                card_info = "'{}'".format(self.label)
            
            return "<_NOUCard {}>".format(card_info)


    class _NOUPlayer(object):
        """
        A class to represent players

        PROPERTIES:
            leftie - (bool) is player leftie or rightie
            isAI - (bool) is it the Player or Monika
            hand - (stack) represents player's hand (a Stack object)
            drew_card - (bool) has player drew a card in this turn
            plays_turn - (bool) is it player's turn
            should_draw_cards - (int) should player draw cards and how much
            played_card - (bool) has player played a card in this turn
            should_skip_turn - (bool) should player skip their turn
            yelled_nou - (bool) has player yelled "NOU" before playing their last card
            should_play_card - (bool) do we expect this player to play a card (after saying 'NOU')
            nou_reminder_timeout - (int) the turn when this player cannot be caught for not saying 'NOU' any longer
        """
        def __init__(self, leftie=False):
            """
            Constructor

            IN:
                leftie - is player leftie or rightie
            """
            self.leftie = leftie
            self.isAI = False
            self.hand = None
            self.drew_card = False
            self.should_draw_cards = 0
            self.played_card = False
            self.plays_turn = False
            self.should_skip_turn = False
            self.yelled_nou = False
            self.should_play_card = False
            self.nou_reminder_timeout = 0
        
        def __repr__(self):
            return "<_NOUPlayer '{0}'>".format(persistent.playername)


    class _NOUReaction(object):
        def __init__(
            self,
            type_=NOU.NO_REACTION,
            turn=-1,
            monika_card=None,
            player_card=None,
            tier=0,
            shown=False
        ):
            self.type = type_
            self.turn = turn
            self.monika_card = monika_card
            self.player_card = player_card
            self.tier = tier
            self.shown = shown
        
        @property
        def tier(self):
            return self._tier
        
        @tier.setter
        def tier(self, value):
            if not 0 <= value < 3:
                value = max(min(value, 2), 0)
            self._tier = value
        
        
        def __getitem__(self, key):
            return getattr(self, key)
        
        def __setitem__(self, key, value):
            setattr(self, key, value)
        
        def __repr__(self):
            return "<_NOUReaction (type_={}, turn={}, monika_card={}, player_card={}, tier={}, shown={})>".format(
                self.type,
                self.turn,
                self.monika_card,
                self.player_card,
                self.tier,
                self.shown
            )


    class _NOUPlayerAI(_NOUPlayer):
        """
        AI variation of player

        PROPERTIES:
            everything from _NOUPlayer
            game - (NOU) pointer for internal use
            cards_data - (dict) data about our cards (amount, values, ids)
            queued_card - (_NOUCard) the card Monika wants to play on the next turn
            player_cards_data - (dict) potentially the most common color (or None)
                and most rare colors (or an empty list) in the Player's hand
                'reset_in' shows how much turns left until we reset 'has_color'
            reactions - (list) all reactions that monika had during this game
                (even if they didn't trigger)
        """
        MIN_THONK_TIME = 0.2
        MAX_THONK_TIME = 0.8
        SHUFFLING_CHANCE = 0.15
        LOW_MISSING_NOU_CHANCE = 0.1
        HIGH_MISSING_NOU_CHANCE = 0.25
        
        def __init__(self, game, leftie=False):
            """
            Constructor

            IN:
                leftie - is this player leftie or rightie
                game - pointer to our NOU object
            """
            super(_NOUPlayerAI, self).__init__(leftie)
            
            self.isAI = True
            self.game = game
            self.queued_card = None
            self.chosen_color = None
            self.player_cards_data = {
                "reset_in": 0,
                "has_color": None,
                "lacks_colors": []
            }
            
            
            self.reactions = []
        
        def __repr__(self):
            return "<_NOUPlayerAI 'Monika'>"
        
        def thonk_pause(self):
            """
            Pauses the game giving some time to Monika to thonk out her next turn
            """
            if len(self.hand) == 1:
                thonk_time = self.MIN_THONK_TIME
            
            else:
                thonk_time = renpy.random.uniform(self.MIN_THONK_TIME, self.MAX_THONK_TIME)
            
            renpy.pause(thonk_time, hard=True)
        
        def _randomise_color(self):
            """
            Chooses one of the colors at random
            Excludes the potential color that the player may have
            If we know what the colors the player doesn't have,
            we will return one of them at random

            OUT:
                string with one of 4 colors
            """
            if self.player_cards_data["lacks_colors"]:
                return renpy.random.choice(self.player_cards_data["lacks_colors"])
            
            colors = list(self.game.COLORS)
            
            if self.player_cards_data["has_color"] is not None:
                colors.remove(self.player_cards_data["has_color"])
            
            return renpy.random.choice(colors)
        
        def guess_player_cards(self):
            """
            Guesses cards' colors in the player's hand
            NOTE: must run this before anything else
            NOTE: this method is quite a mess
            """
            
            if len(self.game.game_log) < 2:
                return
            
            
            if (
                self.player_cards_data["reset_in"] > 0
                and self.game.game_log[-2]["played_card"] is not None
            ):
                self.player_cards_data["reset_in"] -= 1
            
            
            
            if (
                (
                    self.game.game_log[-2]["played_card"] is not None
                    and self.game.game_log[-2]["played_card"].type == "wild"
                )
                or (
                    self.game.current_turn == 2
                    and len(self.game.discardpile) > 1
                    and self.game.discardpile[-2].type == "wild"
                )
            ):
                color = self.game.game_log[-2]["played_card"].color
                
                self.player_cards_data["has_color"] = color
                self.player_cards_data["reset_in"] = 3
                
                
                if color in self.player_cards_data["lacks_colors"]:
                    self.player_cards_data["lacks_colors"].remove(color)
            
            
            
            if (
                
                
                self.game.game_log[-2]["played_card"] is not None
                and self.game.game_log[-2]["played_card"].type == "wild"
                and (
                    not get_house_rule("unrestricted_wd4")
                    or random.random() < 0.25
                )
                and len(self.game.discardpile) > 1
            ):
                if self.game.discardpile[-2].color not in self.player_cards_data["lacks_colors"]:
                    self.player_cards_data["lacks_colors"].append(self.game.discardpile[-2].color)
                
                if self.player_cards_data["has_color"] in self.player_cards_data["lacks_colors"]:
                    self.player_cards_data["has_color"] = None
            
            
            
            elif (
                self.game.game_log[-2]["drew_card"]
                and not self.game.game_log[-2]["had_skip_turn"]
            ):
                
                
                if not self.game.game_log[-2]["played_card"]:
                    
                    
                    self.player_cards_data["lacks_colors"] = [self.game.discardpile[-1].color]
                
                elif self.game.discardpile[-2].color not in self.player_cards_data["lacks_colors"]:
                    
                    self.player_cards_data["lacks_colors"].append(self.game.discardpile[-2].color)
                
                if self.player_cards_data["has_color"] in self.player_cards_data["lacks_colors"]:
                    self.player_cards_data["has_color"] = None
            
            
            if len(self.player_cards_data["lacks_colors"]) == 3:
                missing_colors = self.player_cards_data["lacks_colors"]
                
                all_colors = frozenset(self.game.COLORS)
                
                
                self.player_cards_data["has_color"] = next(iter(all_colors.difference(missing_colors)))
                self.player_cards_data["reset_in"] = 3
            
            
            
            if (
                self.game.game_log[-2]["drew_card"]
                and self.game.game_log[-2]["had_draw_cards"]
            ):
                self.player_cards_data["lacks_colors"] = []
            
            
            if self.player_cards_data["reset_in"] == 0:
                self.player_cards_data["has_color"] = None
        
        def _sort_cards_data(self, cards_data, keys_sort_order=["num", "act"], values_sort_order=["value", "amount"], consider_player_cards_data=True):
            """
            Sorts (by keys and then values) the cards data dict
            and returns it as a list of tuples

            Example:
                [
                    ('num_red', {'amount': 5, 'ids': [6, 1, 3, 12], 'value': 26}),
                    ('num_yellow', {'amount': 4, 'ids': [5, 10, 8, 11], 'value': 9}),
                    ...
                    ('act_yellow', {'amount': 2, 'ids': [2, 9], 'value': -1}),
                    ('wcc', {'amount': 0, 'ids': [], 'value': -1}),
                    ('wd4', {'amount': 1, 'ids': [4], 'value': -1})
                ]

            IN:
                cards_data - dict with info about Monika's cards
                NOTE: check sortKey for these
                keys_sort_order - the dict's keys we're sorting by
                values_sort_order - the dict's values (inner dict's keys) we're sorting by
                consider_player_cards_data - whether or not we consider player's cards in sorting

            OUT:
                sorted list of tuples
            """
            def sortKey(item, keys_sort_order=["num", "act"], values_sort_order=["value", "amount"], consider_player_cards_data=True):
                """
                Function which we use as a sort key for cards data
                NOTE: keys have priority over values

                IN:
                    item - tuple from the list from the cards data dict
                    keys_sort_order - list of strings to sort the list by the dict's keys
                        (Default: ['num', 'act'])
                        For example: ['num'] will put the number cards first
                        or ['red', 'act'] will put the red colored cards first, then action ones, and then the rest
                    values_sort_order - list of strings to sort the list by the dict's values
                        (Default: ['value', 'amount'])
                        For exaple: the default list will sort by cards values first,
                        and then by their amount
                    consider_player_cards_data - whether or not we consider player's cards in sorting

                OUT:
                    list which we'll use in sorting
                """
                
                rv = list()
                
                for _key in keys_sort_order:
                    rv.append(_key in item[0])
                
                for _value in values_sort_order:
                    rv.append(item[1][_value])
                
                if consider_player_cards_data:
                    
                    if self.player_cards_data["has_color"] is not None:
                        rv.append(self.player_cards_data["has_color"] not in item[0])
                    
                    
                    for color in self.player_cards_data["lacks_colors"]:
                        rv.append(color in item[0])
                
                return rv
            
            sorted_list = sorted(
                cards_data.iteritems(),
                key=lambda item: sortKey(
                    item,
                    keys_sort_order=keys_sort_order,
                    values_sort_order=values_sort_order,
                    consider_player_cards_data=consider_player_cards_data
                ),
                reverse=True
            )
            
            return sorted_list
        
        def _get_cards_data(self, cards=None):
            """
            A method that builds a dict that represents cards in a Monika-friendly way (c)
                NOTE: ids of number and action cards are sorted by cards values
                NOTE: This should be called after any change in Monika's hand,
                    and before she'll do anything with cards so Monika has an actual info about her cards

            IN:
                cards - cards whose data we will return, if None, uses the current Monika's cards
                    (Default: None)

            OUT:
                dict with various data about Monika's cards
            """
            if cards is None:
                cards = [card for card in self.hand]
            
            new_cards_data = {
                "num_rojo": {
                    "amount": 0,
                    "value": 0,
                    "ids": []
                },
                "num_celeste": {
                    "amount": 0,
                    "value": 0,
                    "ids": []
                },
                "num_verde": {
                    "amount": 0,
                    "value": 0,
                    "ids": []
                },
                "num_amarillo": {
                    "amount": 0,
                    "value": 0,
                    "ids": []
                },
                "act_rojo": {
                    "amount": 0,
                    "value": -1,
                    "ids": []
                },
                "act_celeste": {
                    "amount": 0,
                    "value": -1,
                    "ids": []
                },
                "act_verde": {
                    "amount": 0,
                    "value": -1,
                    "ids": []
                },
                "act_amarillo": {
                    "amount": 0,
                    "value": -1,
                    "ids": []
                },
                "wd4": {
                    "amount": 0,
                    "value": -1,
                    "ids": []
                },
                "wcc": {
                    "amount": 0,
                    "value": -1,
                    "ids": []
                }
            }
            
            
            
            
            should_reverse = bool(get_house_rule("points_to_win"))
            
            sorted_cards = sorted(
                cards,
                key=lambda card_obj: card_obj.value,
                reverse=should_reverse
            )
            
            
            for card in sorted_cards:
                if card.type == "number":
                    new_cards_data["num_" + card.color]["amount"] += 1
                    new_cards_data["num_" + card.color]["value"] += card.value
                    
                    new_cards_data["num_" + card.color]["ids"].append(cards.index(card))
                
                elif card.type == "action":
                    new_cards_data["act_" + card.color]["amount"] += 1
                    
                    
                    new_cards_data["act_" + card.color]["ids"].append(cards.index(card))
                
                elif card.label == "Wild Draw Four":
                    new_cards_data["wd4"]["amount"] += 1
                    
                    new_cards_data["wd4"]["ids"].append(cards.index(card))
                
                
                else:
                    new_cards_data["wcc"]["amount"] += 1
                    
                    new_cards_data["wcc"]["ids"].append(cards.index(card))
            
            
            return new_cards_data
        
        def shuffle_hand(self):
            """
            Sorts some cards in Monika's hand
            This is just for visuals
            NOTE: Since this changes cards' ids,
                either do this at the start of the turn (optimal),
                or update cards data again after shuffling.
            """
            if self.game.current_turn < 4:
                
                return
            
            total_cards = len(self.hand)
            if total_cards < 4:
                
                return
            
            if random.random() > self.SHUFFLING_CHANCE:
                
                return
            
            
            shuffle_type = renpy.random.randint(1, 3)
            
            
            if shuffle_type == 1:
                
                card_id = renpy.random.randint(0, total_cards - 1)
                
                free_ids = [id for id in range(total_cards) if id != card_id]
                
                insert_id = renpy.random.choice(free_ids)
                
                card = self.hand[card_id]
                self.hand.insert(insert_id, card)
            
            
            elif shuffle_type == 2:
                all_ids = [id for id in range(total_cards)]
                ids_to_shuffle = []
                free_ids = list(all_ids)
                
                
                if total_cards > 12:
                    total_to_shuffle = 7
                else:
                    total_to_shuffle = total_cards / 2
                
                
                for i in range(total_to_shuffle):
                    id = renpy.random.choice(all_ids)
                    
                    all_ids.remove(id)
                    ids_to_shuffle.append(id)
                
                
                for card_id in ids_to_shuffle:
                    insert_id = renpy.random.choice(free_ids)
                    card = self.hand[card_id]
                    self.hand.insert(insert_id, card)
            
            
            else:
                self.hand.cards.sort(key=lambda card: card.value.value, reverse=True)
            
            renpy.pause(0.5, hard=True)
        
        def choose_color(self, ignored_card=None):
            """
            Monika chooses color to set for Wild cards

            ignored_card - card that will be ignored in calculation of the color
                (Default: None)

            OUT:
                string with color
            """
            def sortKey(id):
                """
                For action cards
                Sorts by both cards colors and labels

                ASSUMES:
                    cards
                    sorted_cards_data
                """
                labels = (
                    "Skip",
                    "Draw Two",
                    "Reverse"
                )
                colors = [sorted_cards_data[i][0].replace("num_", "") for i in range(4)]
                
                return [cards[id].label == label for label in labels] + [cards[id].color == color for color in colors]
            
            cards = [card for card in self.hand]
            
            if (
                ignored_card is not None
                and ignored_card in cards
            ):
                cards.remove(ignored_card)
            
            cards_data = self._get_cards_data(cards)
            
            
            if len(cards) == 1:
                if cards[0].type == "wild":
                    color = self._randomise_color()
                
                else:
                    color = cards[0].color
                
                return color
            
            else:
                if get_house_rule("points_to_win"):
                    sorted_cards_data = self._sort_cards_data(cards_data)
                
                else:
                    
                    sorted_cards_data = self._sort_cards_data(cards_data, values_sort_order=["amount"])
                
                
                if len(self.game.player.hand) < 3:
                    action_ids = []
                    
                    for color in self.game.COLORS:
                        action_ids += cards_data["act_" + color]["ids"]
                    
                    if action_ids:
                        action_ids.sort(
                            key=sortKey,
                            reverse=True
                        )
                        
                        self.queued_card = cards[action_ids[0]]
                        
                        color = self.queued_card.color
                        return color
                
                
                else:
                    
                    sortByLabel = lambda card: (
                        card.label == "Skip",
                        card.label == "Draw Two",
                        card.label == "Reverse"
                    )
                    
                    
                    if get_house_rule("points_to_win"):
                        srt_data_key = "value"
                    
                    else:
                        srt_data_key = "amount"
                    
                    highest_value = float(sorted_cards_data[0][1][srt_data_key])
                    
                    
                    if highest_value:
                        for j in range(4):
                            
                            
                            
                            if float(highest_value - sorted_cards_data[j][1][srt_data_key]) / highest_value >= 0.6:
                                break
                            
                            
                            if sorted_cards_data[j][1]["amount"]:
                                
                                data_key = sorted_cards_data[j][0].replace("num_", "act_")
                                
                                if cards_data[data_key]["amount"]:
                                    
                                    self.queued_card = sorted(
                                        [cards[id] for id in cards_data[data_key]["ids"]],
                                        key=sortByLabel,
                                        reverse=True
                                    )[0]
                                    
                                    color = self.queued_card.color
                                    return color
                
                
                if sorted_cards_data[0][1]["amount"]:
                    color = sorted_cards_data[0][0].replace("num_", "")
                
                elif sorted_cards_data[4][1]["amount"]:
                    color = sorted_cards_data[4][0].replace("act_", "")
                
                else:
                    color = self._randomise_color()
                
                return color
        
        def choose_card(self, should_draw=True, should_choose_color=True):
            """
            Monika chooses a card to play

            IN:
                should_draw - should Monika draw a card
                    if she's not found one to play?
                    (Default: True)
                should_choose_color - should Monika choose a color
                    if the chosen card is a wild card?
                    (Default: True)

            OUT:
                card if we found or drew one
                or None if we don't want to (or can't) play a card this turn
            """
            
            def analyse_numbers():
                """
                Goes through the cards data in the order we sorted it
                and tries to find a number card that we can play

                OUT:
                    card object if found a card, None otherwise

                ASSUMES:
                    total_player_cards
                    sorted_cards_data
                    player_cards_data
                """
                MAX_ID = 4
                
                if get_house_rule("points_to_win"):
                    data_key = "value"
                
                else:
                    data_key = "amount"
                
                highest_value = float(sorted_cards_data[0][1][data_key])
                reserved_card = None
                
                for color_id in range(MAX_ID):
                    
                    if sorted_cards_data[color_id][1]["amount"] > 2:
                        
                        last_card = self.hand[sorted_cards_data[color_id][1]["ids"][-1]]
                        
                        if (
                            last_card.label == "0"
                            and (
                                last_card.color in self.player_cards_data["lacks_colors"]
                                or (
                                    total_player_cards > 2
                                    and (
                                        (
                                            self.player_cards_data["has_color"] is not None
                                            and last_card.color != self.player_cards_data["has_color"]
                                        )
                                        or (
                                            self.player_cards_data["has_color"] is None
                                            and random.random() < 0.3
                                        )
                                    )
                                )
                            )
                        ):
                            
                            if self.game._is_matching_card(self, last_card):
                                return last_card
                    
                    
                    
                    this_color = sorted_cards_data[color_id][0].replace("num_", "")
                    
                    
                    
                    next_color_id = color_id + 1
                    
                    
                    if next_color_id < MAX_ID:
                        
                        next_color_value = float(sorted_cards_data[next_color_id][1][data_key])
                    
                    else:
                        
                        next_color_value = None
                    
                    
                    want_try_another_color = (
                        this_color == self.player_cards_data["has_color"]
                        and next_color_value is not None
                        and (
                            highest_value == 0
                            or (highest_value - next_color_value) / highest_value < 0.5
                            or total_player_cards < 4
                        )
                        and (
                            this_color != self.game.discardpile[-1].color
                            or random.random() < 0.2
                        )
                    )
                    
                    
                    for id in sorted_cards_data[color_id][1]["ids"]:
                        card = self.hand[id]
                        
                        if self.game._is_matching_card(self, card):
                            if (
                                want_try_another_color
                                and reserved_card is None
                            ):
                                
                                reserved_card = card
                                
                                break
                            
                            else:
                                return card
                
                
                if (
                    reserved_card is not None
                    and (
                        total_cards < 4
                        or random.random() < 0.25
                    )
                ):
                    return reserved_card
                
                return None
            
            def analyse_actions():
                """
                Goes through all action cards we have and tries to find
                one that we can play this turn

                OUT:
                    card object if we found one, None otherwise

                ASSUMES:
                    sorted_cards_data
                    cards_data
                """
                def sortKey(id):
                    """
                    This is a sort key, it sorts

                    IN:
                        id - card id

                    OUT:
                        key to sort by
                    """
                    
                    label_order = (
                        "Skip",
                        "Draw Two",
                        "Reverse"
                    )
                    sorted_colors = [sorted_cards_data[i][0].replace("num_", "") for i in range(4)]
                    
                    return [self.hand[id].label == label for label in label_order] + [self.hand[id].color == color for color in sorted_colors]
                
                action_cards_ids = []
                
                for color in self.game.COLORS:
                    action_cards_ids += cards_data["act_" + color]["ids"]
                
                action_cards_ids.sort(key=sortKey, reverse=True)
                
                for id in action_cards_ids:
                    card = self.hand[id]
                    
                    if self.game._is_matching_card(self, card):
                        return card
                
                return None
            
            def analyse_wilds(label=None):
                """
                Return one of wilds we have

                IN:
                    label - card label either 'wd4' or 'wcc'
                        (Default: None - any of wild cards)

                OUT:
                    card object if we found one, None otherwise

                ASSUMES:
                    cards_data
                """
                if not label:
                    wild_cards_ids = cards_data["wd4"]["ids"] + cards_data["wcc"]["ids"]
                
                else:
                    wild_cards_ids = cards_data[label]["ids"]
                
                
                if not wild_cards_ids:
                    return None
                
                card = self.hand[renpy.random.choice(wild_cards_ids)]
                
                if self.game._is_matching_card(self, card):
                    return card
                
                
                return None
            
            def analyse_cards(func_list):
                """
                Analyses all cards we have using funcs in func_list and returns first
                appropriate card we want and can play in this turn

                IN:
                    func_list - a list/tuple of tuples with func, args and kwargs,
                        we call those to find the card

                OUT:
                    card if we found one,
                    or None if no card was found
                """
                for func, args, kwargs in func_list:
                    card = func(*args, **kwargs)
                    
                    if card is not None:
                        return card
                
                return None
            
            cards_data = self._get_cards_data()
            
            total_cards = len(self.hand)
            total_player_cards = len(self.game.player.hand)
            
            
            if self.should_skip_turn:
                
                if get_house_rule("points_to_win"):
                    sorted_cards_data = self._sort_cards_data(cards_data)
                
                else:
                    sorted_cards_data = self._sort_cards_data(cards_data, values_sort_order=["amount"])
                
                action_cards_ids = []
                
                
                for i in reversed(range(4)):
                    
                    
                    color = sorted_cards_data[i][0].replace("num_", "")
                    action_cards_ids += cards_data["act_" + color]["ids"]
                
                
                if get_house_rule("reflect_chaos"):
                    action_cards_ids += cards_data["wd4"]["ids"]
                
                
                for id in action_cards_ids:
                    card = self.hand[id]
                    
                    if self.game._is_matching_card(self, card):
                        
                        
                        
                        if (
                            should_choose_color
                            and card.type == "wild"
                        ):
                            self.chosen_color = self.choose_color(ignored_card=card)
                        
                        return card
                
                
                if (
                    self.should_draw_cards
                    and should_draw
                ):
                    self.game.deal_cards(self, self.should_draw_cards)
            
            
            
            else:
                
                if (
                    self.queued_card is not None
                    and self.game._is_matching_card(self, self.queued_card)
                ):
                    
                    if (
                        should_choose_color
                        and self.queued_card.type == "wild"
                    ):
                        self.chosen_color = self.choose_color(ignored_card=self.queued_card)
                    
                    return self.queued_card
                
                
                else:
                    
                    if total_cards == 1:
                        card = self.hand[0]
                        
                        if self.game._is_matching_card(self, card):
                            
                            if (
                                should_choose_color
                                and card.type == "wild"
                            ):
                                self.chosen_color = self.choose_color(ignored_card=card)
                            
                            return card
                    
                    else:
                        if get_house_rule("points_to_win"):
                            sorted_cards_data = self._sort_cards_data(cards_data)
                        
                        else:
                            sorted_cards_data = self._sort_cards_data(cards_data, values_sort_order=["amount"])
                        
                        
                        
                        if (
                            total_player_cards < 4
                            or total_cards/total_player_cards > 1.05
                            or random.random() < 0.2
                        ):
                            analysis = (
                                (
                                    analyse_wilds,
                                    (),
                                    {"label": "wd4"}
                                ),
                                (
                                    analyse_actions,
                                    (),
                                    {}
                                ),
                                (
                                    analyse_numbers,
                                    (),
                                    {}
                                ),
                                (
                                    analyse_wilds,
                                    (),
                                    {"label": "wcc"}
                                )
                            )
                        
                        
                        else:
                            analysis = (
                                (
                                    analyse_numbers,
                                    (),
                                    {}
                                ),
                                (
                                    analyse_actions,
                                    (),
                                    {}
                                ),
                                (
                                    analyse_wilds,
                                    (),
                                    {}
                                )
                            )
                        
                        card = analyse_cards(analysis)
                        
                        if card is not None:
                            
                            if (
                                should_choose_color
                                and card.type == "wild"
                            ):
                                self.chosen_color = self.choose_color(ignored_card=card)
                            
                            return card
                    
                    
                    if should_draw:
                        self.game.deal_cards(self)
                        card = self.hand[-1]
                        
                        if (
                            self.game._is_matching_card(self, card)
                            
                            and (
                                
                                len(self.hand) < 3
                                
                                or self.game.discardpile[-1].color not in self.player_cards_data["lacks_colors"]
                                
                                or random.random() < 0.2
                            )
                        ):
                            
                            if (
                                should_choose_color
                                and card.type == "wild"
                            ):
                                self.chosen_color = self.choose_color(ignored_card=card)
                            
                            return card
            
            
            return None
        
        def play_card(self, card):
            """
            Inner wrapper around play_card
            NOTE: we do only certain checks here

            IN:
                card - card to play
            """
            if not card:
                return
            
            if card is self.queued_card:
                self.queued_card = None
            
            self.game.play_card(self, self.game.player, card)
            
            self.game._win_check(self)
            
            if (
                self.game.discardpile[-1].type == "wild"
            ):
                self.game.discardpile[-1].color = self.chosen_color
                self.chosen_color = None
        
        def choose_reaction(self, next_card_to_play):
            """
            Helps Monika choose a dialogue based on the state of the game
            NOTE: 'NOU' is handled differently, right in announce_reaction(), w/o corresponding reactions from here

            TODO: reaction when you both are drawing cards
                because no one has a card with the current color
            TODO: reactions when Monika reflected a card on her 1st turn
                (the player had (had not) to skip their turn)
            TODO: reactions when the player reflected a card on their 1st turn

            IN:
                next_card_to_play - the next card Monika's going to play
                    (we base reaction on it)
            """
            
            if (
                next_card_to_play is not None
                and self.should_skip_turn
                and len(self.game.game_log) > 1
                and self.game.game_log[-2]["played_card"] is not None
                and next_card_to_play.label == self.game.game_log[-2]["played_card"].label
            ):
                
                
                if (
                    len(self.game.game_log) > 2
                    and self.game.game_log[-3]["played_card"] is not None
                    and self.game.game_log[-3]["played_card"].label == "Wild Draw Four"
                ):
                    reaction = _NOUReaction(
                        type_=self.game.MONIKA_REFLECTED_WDF,
                        tier=0
                    )
                
                
                elif (
                    self.reactions
                    and self.reactions[-1].type == self.game.MONIKA_REFLECTED_WDF
                    and len(self.game.game_log) > 1
                    and self.game.game_log[-2]["played_card"] is not None
                ):
                    reaction = _NOUReaction(
                        type_=self.game.MONIKA_REFLECTED_WDF,
                        tier=self.reactions[-1].tier + 1
                    )
                
                
                
                else:
                    reaction = _NOUReaction(type_=self.game.MONIKA_REFLECTED_ACT)
                    
                    
                    if (
                        self.reactions
                        and self.reactions[-1].type == self.game.MONIKA_REFLECTED_ACT
                    ):
                        if (
                            len(self.reactions) > 1
                            and self.reactions[-2].type == self.game.MONIKA_REFLECTED_ACT
                        ):
                            reaction.tier = 2
                        
                        else:
                            reaction.tier = 1
                    
                    else:
                        reaction.tier = 0
                
                reaction.turn = self.game.current_turn
                reaction.monika_card = next_card_to_play
                reaction.player_card = self.game.game_log[-2]["played_card"]
                reaction.shown = False
                
                self.reactions.append(reaction)
                
                return reaction
            
            
            if (
                next_card_to_play is None
                and self.should_skip_turn
                and len(self.game.game_log) > 1
                and self.game.game_log[-2]["played_card"] is not None
                and self.game.game_log[-2]["played_card"].type == "action"
            ):
                
                
                if (
                    self.reactions
                    and self.reactions[-1].type == self.game.MONIKA_REFLECTED_WDF
                ):
                    reaction = _NOUReaction(
                        type_=self.game.PLAYER_REFLECTED_WDF,
                        turn=self.game.current_turn,
                        monika_card=None,
                        player_card=self.game.game_log[-2]["played_card"],
                        tier=self.reactions[-1].tier + 1,
                        shown=False
                    )
                    
                    self.reactions.append(reaction)
                    
                    return reaction
                
                
                
                elif (
                    self.reactions
                    and self.reactions[-1].type == self.game.MONIKA_REFLECTED_ACT
                ):
                    reaction = _NOUReaction(
                        type_=self.game.PLAYER_REFLECTED_ACT,
                        turn=self.game.current_turn,
                        monika_card=None,
                        player_card=self.game.game_log[-2]["played_card"],
                        tier=self.reactions[-1].tier + 1,
                        shown=False
                    )
                    
                    self.reactions.append(reaction)
                    
                    return reaction
                
                
                elif (
                    len(self.game.game_log) > 2
                    and self.game.game_log[-3]["played_card"] is not None
                    and self.game.game_log[-3]["played_card"].label == self.game.game_log[-2]["played_card"].label
                ):
                    reaction = _NOUReaction(
                        type_=self.game.PLAYER_REFLECTED_ACT,
                        turn=self.game.current_turn,
                        monika_card=None,
                        player_card=self.game.game_log[-2]["played_card"],
                        tier=0,
                        shown=False
                    )
                    
                    self.reactions.append(reaction)
                    
                    return reaction
            
            
            
            
            
            if (
                next_card_to_play is not None
                and next_card_to_play.label == "Draw Two"
                and self.should_skip_turn
                and len(self.game.game_log) > 1
                and self.game.game_log[-2]["played_card"] is not None
                and self.game.game_log[-2]["played_card"].label == "Wild Draw Four"
            ):
                reaction = _NOUReaction(
                    type_=self.game.MONIKA_REFLECTED_WDF,
                    turn=self.game.current_turn,
                    monika_card=next_card_to_play,
                    player_card=self.game.game_log[-2]["played_card"],
                    tier=0,
                    shown=False
                )
                
                
                
                
                
                
                
                
                self.reactions.append(reaction)
                
                return reaction
            
            
            if (
                next_card_to_play is None
                and self.should_skip_turn
                and len(self.game.game_log) > 2
                and self.game.game_log[-3]["played_card"] is not None
                and self.game.game_log[-3]["played_card"].label == "Wild Draw Four"
                and self.game.game_log[-2]["played_card"] is not None
                and self.game.game_log[-2]["played_card"].label == "Draw Two"
            ):
                reaction = _NOUReaction(
                    type_=self.game.PLAYER_REFLECTED_WDF,
                    turn=self.game.current_turn,
                    monika_card=None,
                    player_card=self.game.game_log[-2]["played_card"],
                    tier=0,
                    shown=False
                )
                
                self.reactions.append(reaction)
                
                return reaction
            
            
            if (
                next_card_to_play is not None
                and next_card_to_play.type == "wild"
                and len(self.game.game_log) > 1
                and self.game.game_log[-2]["played_card"] is not None
                and self.game.game_log[-2]["played_card"].label == "Wild"
            ):
                reaction = _NOUReaction(
                    type_=self.game.MONIKA_REFLECTED_WCC,
                    turn=self.game.current_turn,
                    monika_card=next_card_to_play,
                    player_card=self.game.game_log[-2]["played_card"],
                    shown=False
                )
                
                if (
                    self.reactions
                    and self.reactions[-1].type == self.game.MONIKA_REFLECTED_WCC
                ):
                    if (
                        len(self.reactions) > 1
                        and self.reactions[-2].type == self.game.MONIKA_REFLECTED_WCC
                    ):
                        reaction.tier = 2
                    
                    else:
                        reaction.tier = 1
                
                else:
                    reaction.tier = 0
                
                self.reactions.append(reaction)
                
                return reaction
            
            
            if (
                (
                    next_card_to_play is None
                    or next_card_to_play.type != "wild"
                )
                and len(self.game.game_log) > 2
                and self.game.game_log[-3]["played_card"] is not None
                and self.game.game_log[-3]["played_card"].label == "Wild"
                and self.game.game_log[-2]["played_card"] is not None
                and self.game.game_log[-2]["played_card"].label == "Wild"
            ):
                reaction = _NOUReaction(
                    type_=self.game.PLAYER_REFLECTED_WCC,
                    turn=self.game.current_turn,
                    monika_card=next_card_to_play,
                    player_card=self.game.game_log[-2]["played_card"],
                    shown=False
                )
                
                if (
                    self.reactions
                    and self.reactions[-1].type == self.game.MONIKA_REFLECTED_WCC
                ):
                    
                    reaction.tier = self.reactions[-1].tier + 1
                
                else:
                    reaction.tier = 0
                
                self.reactions.append(reaction)
                
                return reaction
            
            
            if (
                next_card_to_play is not None
                and next_card_to_play.type == "wild"
                and len(self.hand) > 1
            ):
                reaction = _NOUReaction(
                    type_=self.game.MONIKA_PLAYED_WILD,
                    turn=self.game.current_turn,
                    monika_card=next_card_to_play,
                    player_card=self.game.game_log[-2]["played_card"] if len(self.game.game_log) > 1 else None,
                    tier=0,
                    shown=False
                )
                
                self.reactions.append(reaction)
                
                return reaction
            
            
            reaction = _NOUReaction(
                type_=self.game.NO_REACTION,
                turn=self.game.current_turn,
                monika_card=next_card_to_play,
                player_card=self.game.game_log[-2]["played_card"] if len(self.game.game_log) > 1 else None,
                tier=0,
                shown=False
            )
            
            self.reactions.append(reaction)
            
            return reaction
        
        def _handle_nou_logic(self, current_reaction):
            """
            Handles nou logic for Monika

            IN:
                current_reaction - current Monika's reaction

            OUT:
                tuple of 2 booleans:
                    has_yelled_nou - whether or not Monika yelled 'NOU' this turn
                    has_reminded_yell_nou - whether or not Monika reminded the player to yell 'NOU' this turn
            """
            def should_miss_this_nou():
                """
                An inner method to check if Monika misses/wants to let slide this nou check

                OUT:
                    boolean - True/False

                ASSUMES:
                    mas_nou.monika_win_streak
                    persistent._mas_game_nou_abandoned
                    persistent._mas_game_nou_house_rules
                    persistent._mas_game_nou_points['Player']
                """
                if (
                    persistent._mas_game_nou_abandoned > 1
                    or (
                        get_house_rule("points_to_win") > 0
                        and get_player_points_percentage("Player") <= 0.2
                        and get_player_points_percentage("Monika") >= 0.8
                    )
                    or (
                        get_house_rule("points_to_win") == 0
                        and (
                            monika_win_streak > 2
                            or monika_wins_this_sesh - player_wins_this_sesh > 4
                        )
                    )
                ):
                    chance = self.HIGH_MISSING_NOU_CHANCE
                
                else:
                    chance = self.LOW_MISSING_NOU_CHANCE
                
                return random.random() < chance
            
            
            has_yelled_nou = False
            has_reminded_yell_nou = False
            
            
            if (
                current_reaction.monika_card is not None
                and not self.yelled_nou
                and len(self.hand) == 2
                and not should_miss_this_nou()
            ):
                has_yelled_nou = True
                
                self.yelled_nou = True
                self.should_play_card = True
                self.nou_reminder_timeout = 0
                nou_quip = renpy.random.choice(self.game.QUIPS_MONIKA_YELLS_NOU)
                renpy.say(m, nou_quip, interact=True)
            
            
            if (
                not self.game.player.yelled_nou
                and self.game.player.nou_reminder_timeout > self.game.current_turn
                and len(self.game.player.hand) == 1
                and not should_miss_this_nou()
            ):
                has_reminded_yell_nou = True
                
                remind_quip = renpy.random.choice(self.game.QUIPS_PLAYER_FORGOT_YELL_NOU)
                
                if has_yelled_nou:
                    remind_quip = "... Y hablando de NOU...{w=0.5}" + remind_quip
                
                renpy.say(m, remind_quip, interact=True)
                
                self.game.deal_cards(self.game.player, amount=2, smooth=False, sound=True, mark_as_drew_card=False)
                renpy.pause(0.5, hard=True)
            
            return has_yelled_nou, has_reminded_yell_nou
        
        def announce_reaction(self, reaction):
            """
            A wrapper around renpy.say for Monika's reactions

            Here we check if the reaction passes rng check, add modifiers to it,
                and handle 'NOU' quips

            IN:
                reaction - reaction to announce
            """
            
            
            
            monika_yelled_nou, monika_reminded_yell_nou = self._handle_nou_logic(reaction)
            
            reaction_map = self.game.REACTIONS_MAP.get(reaction.type, None)
            
            if (
                reaction.type != self.game.NO_REACTION
                and (
                    
                    not monika_yelled_nou
                    and not monika_reminded_yell_nou
                )
                and reaction_map
            ):
                max_tier = len(reaction_map) - 1
                
                tier = min(reaction.tier, max_tier)
                
                
                chance_to_trigger = self.game.TIER_REACTION_CHANCE_MAP.get(tier, 0.33)
                if (
                    reaction.type == self.game.MONIKA_PLAYED_WILD
                    or random.random() < chance_to_trigger
                ):
                    
                    reaction.shown = True
                    
                    
                    reaction_quips = list(reaction_map[tier])
                    
                    
                    additional_quips = None
                    
                    if reaction.type == self.game.MONIKA_REFLECTED_ACT:
                        if (
                            tier == 2
                            and reaction.monika_card is not None
                            and reaction.monika_card.label == "Draw Two"
                            and get_house_rule("stackable_d2")
                        ):
                            additional_quips = self.game.REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_1
                        
                        elif (
                            tier == 0
                            and reaction.monika_card is not None
                        ):
                            if reaction.monika_card.label == "Draw Two":
                                additional_quips = self.game.REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_2
                            
                            
                            else:
                                additional_quips = self.game.REACTIONS_MAP_MONIKA_REFLECTED_ACT_MODIFIER_3
                    
                    elif (
                        reaction.type == self.game.MONIKA_REFLECTED_WDF
                        and tier == 2
                        and get_house_rule("stackable_d2")
                    ):
                        additional_quips = self.game.REACTIONS_MAP_MONIKA_REFLECTED_WD4_MODIFIER_1
                    
                    elif (
                        reaction.type == self.game.MONIKA_REFLECTED_WCC
                        and tier == 2
                        and self.chosen_color == "green"
                    ):
                        additional_quips = self.game.REACTIONS_MAP_MONIKA_REFLECTED_WCC_MODIFIER_1
                    
                    elif (
                        (
                            (
                                reaction.type == self.game.PLAYER_REFLECTED_ACT
                                and reaction.monika_card is not None
                                and reaction.monika_card.label == "Draw Two"
                            )
                            or reaction.type == self.game.PLAYER_REFLECTED_WDF
                        )
                        and tier == 2
                        and len(self.hand) > 4
                        and get_house_rule("stackable_d2")
                    ):
                        if reaction.type == self.game.PLAYER_REFLECTED_ACT:
                            additional_quips = self.game.REACTIONS_MAP_PLAYER_REFLECTED_ACT_MODIFIER_1
                        
                        else:
                            additional_quips = self.game.REACTIONS_MAP_PLAYER_REFLECTED_WD4_MODIFIER_1
                    
                    
                    if additional_quips is not None:
                        reaction_quips += additional_quips
                    
                    
                    
                    
                    quip = renpy.random.choice(
                        reaction_quips
                    )
                    
                    
                    for line in quip:
                        renpy.say(m, line, interact=True)
            
            
            if (
                (
                    reaction.type == self.game.MONIKA_REFLECTED_WCC
                    or (
                        reaction.type == self.game.MONIKA_PLAYED_WILD
                        and (
                            monika_yelled_nou
                            or monika_reminded_yell_nou
                        )
                    )
                    or (
                        reaction.type in (self.game.MONIKA_REFLECTED_WDF, self.game.MONIKA_REFLECTED_ACT)
                        and get_house_rule("reflect_chaos")
                        and reaction.monika_card
                        and reaction.monika_card.type == "wild"
                    )
                )
                and len(self.hand) > 1
            ):
                color_quip = renpy.random.choice(self.game.QUIPS_MONIKA_ANNOUNCE_COLOR_AFTER_REFLECT)
                renpy.say(m, color_quip, interact=True)




init 5 python in mas_nou:
    import datetime

    _m1_zz_cardgames__SENTRY = object()

    def get_default_house_rules():
        """
        Returns default house rules

        OUT:
            dict
        """
        return dict(DEF_RULES_VALUES)

    def update_house_rules(force=False):
        """
        Adds keys from the def values dict to the persistent dict
        Useful after updates

        IN:
            force - bool, do we want to rewrite existing keys?
        """
        if persistent._mas_game_nou_house_rules is None:
            persistent._mas_game_nou_house_rules = get_default_house_rules()
            return
        
        for k, v in DEF_RULES_VALUES.items():
            if k not in persistent._mas_game_nou_house_rules or force:
                persistent._mas_game_nou_house_rules[k] = v

    def are_default_house_rules():
        """
        Checks if the current settings are default

        OUT:
            bool
        """
        if persistent._mas_game_nou_house_rules is None:
            return False
        
        for k, def_v in DEF_RULES_VALUES.items():
            if def_v != persistent._mas_game_nou_house_rules.get(k, _m1_zz_cardgames__SENTRY):
                return False
        
        return True

    def get_house_rule(name):
        """
        Returns a house rule for the given name

        This WILL raise KeyError if you enter invalid name

        But this WILL try to fall back to a sane value if the key isn't
        in the persistent for some reason

        IN:
            name - the string with the rule key

        OUT:
            rule value
            or None in the worst case
        """
        data = persistent._mas_game_nou_house_rules
        if data is None:
            return None
        
        if name in data:
            return data[name]
        
        if name in DEF_RULES_VALUES:
            return DEF_RULES_VALUES[name]
        
        raise KeyError("Unknown name for a house rule: {}".format(name))

    def set_house_rule(name, value):
        """
        Sets a new value for a house rule

        This WILL raise KeyError if you enter invalid name

        IN:
            name - the string with the rule key
            value - the new value for the rule
        """
        data = persistent._mas_game_nou_house_rules
        if data is None:
            return
        
        if name not in DEF_RULES_VALUES:
            raise KeyError("Unknown name for a house rule: {}".format(name))
        
        data[name] = value

    def reverse_house_rule(name):
        """
        Reversed a value of a house rule
        Only useful for bools
        """
        old_value = get_house_rule(name)
        if not isinstance(old_value, bool):
            raise TypeError("reverse_house_rule can only be used for boolean rules")
        
        set_house_rule(name, not old_value)

    def visit_game_ev():
        """
        Updates game ev props like if it was seen by the player now
        Increments show count
        Sets last seen
        """
        with store.MAS_EVL("mas_nou") as game_ev:
            
            if game_ev.unlocked:
                game_ev.shown_count += 1
                game_ev.last_seen = datetime.datetime.now()

    def does_want_suggest_play():
        """
        A func to check if Monika wants to suggest play nou
        Yes if:
            NEVER played nou before
            played in the last 15 mins
            NOT played in the past 3 days
            otherwise 30% to say yes

        OUT:
            bool
        """
        last_played = store.mas_getEVL_last_seen("mas_nou")
        if last_played is None:
            return True
        
        now_dt = datetime.datetime.now()
        delta_t = now_dt - last_played
        return (
            delta_t < datetime.timedelta(minutes=15)
            or delta_t > datetime.timedelta(days=3)
            or random.random() < 0.3
        )

    def give_points():
        """
        Gives points to the winner

        ASSUMES:
            mas_nou.game
            mas_nou.winner
        """
        if winner in ("Monika", "Surrendered"):
            persist_key = "Monika"
            loser = game.player
        
        elif winner == "Player":
            persist_key = "Player"
            loser = game.monika
        
        
        else:
            return
        
        
        if loser.should_draw_cards:
            game.deal_cards(
                player=loser,
                amount=loser.should_draw_cards,
                smooth=False,
                sound=False,
                mark_as_drew_card=False,
                reset_nou_var=False
            )
        
        for card in loser.hand:
            persistent._mas_game_nou_points[persist_key] += card.value

    def reset_points():
        """
        Resets the persistent var to 0 for both Monika and the player
        """
        persistent._mas_game_nou_points["Monika"] = 0
        persistent._mas_game_nou_points["Player"] = 0

    def get_player_points_percentage(player_persist_key):
        """
        Returns proportion of the corrent points of a player to the maximum possible score

        IN:
            player_persist_key - persistent key for the player
                ('Monika' or 'Player')

        OUT:
            float as proportion (0.0 - 1.0)

        ASSUMES:
            persistent._mas_game_nou_house_rules['points_to_win'] > 0
        """
        p2w = get_house_rule("points_to_win")
        if p2w == 0:
            return 1.0
        return float(persistent._mas_game_nou_points[player_persist_key]) / float(p2w)

    def get_wins_for(player):
        """
        Returns wins in nou

        IN:
            player - the player key to return the stats for

        OUT:
            int
        """
        if not persistent._mas_game_nou_wins:
            return 0
        
        return persistent._mas_game_nou_wins.get(player, 0)

    def get_total_games():
        """
        Returns total nou games

        OUT:
            int
        """
        if not persistent._mas_game_nou_wins:
            return 0
        
        return persistent._mas_game_nou_wins.get("Monika", 0) + persistent._mas_game_nou_wins.get("Player", 0)



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_introduce_nou_house_rules"
        )
    )

label monika_introduce_nou_house_rules:
    m 3eud "Oh [player], ¡casi lo olvido!"
    m 3eua "Si alguna vez sientes que esas reglas oficiales no son lo suficientemente divertidas...{w=0.5}{nw}"
    extend 1kua " solo házmelo saber y jugaremos con las reglas de nuestra casa."
    $ mas_unlockEVL("monika_change_nou_house_rules", "EVE")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_nou_house_rules",
            prompt="Cambiemos las reglas de la casa para NOU",
            category=["juegos"],
            pool=True,
            unlocked=False,
            
            conditional="store.mas_nou.get_total_games() > 0",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_change_nou_house_rules:
    if (
        mas_nou.get_house_rule("points_to_win")
        and (
            persistent._mas_game_nou_points["Monika"]
            or persistent._mas_game_nou_points["Player"]
        )
    ):
        m 3eud "[player], todavía no hemos terminado nuestro juego."
        m 1euc "Si quieres jugar con nuevas reglas, entonces tendremos que empezar un nuevo juego la próxima vez."
    else:

        m 1eub "Por supuesto."



    label monika_change_nou_house_rules.pre_menu(has_changed_rules=False, from_game=False):
        pass

    label monika_change_nou_house_rules.menu_loop:
        python:
            menu_items = [
                (
                    _("Me gustaría cambiar el número de puntos necesarios para ganar."),
                    "points_to_win",
                    False,
                    False
                ),
                (
                    _("Me gustaría cambiar el número de cartas con las que empezamos cada ronda."),
                    "starting_cards",
                    False,
                    False
                ),
                (
                    _("Me gustaría jugar con los roba 2 apilables.") if not mas_nou.get_house_rule("stackable_d2") else _("Me gustaría jugar con los Roba 2 no apilables."),
                    "stackable_d2",
                    False,
                    False
                ),
                (
                    _("Me gustaría jugar con el Comodín Roba 4 sin restricciones.") if not mas_nou.get_house_rule("unrestricted_wd4") else _("Me gustaría jugar con los Comodin Roba 4 restringidos."),
                    "unrestricted_wd4",
                    False,
                    False
                ),
                (
                    _("Me gustaría jugar a reflejos caóticos.") if not mas_nou.get_house_rule("reflect_chaos") else _("Me gustaría jugar con los reflejos clásicos."),
                    "reflect_chaos",
                    False,
                    False
                )
            ]

            if not mas_nou.are_default_house_rules():
                menu_items.append((_("Me gustaría volver a las reglas clásicas."), "restore", False, False))

            final_items = (
                (_("¿Puedes explicar estas reglas de la casa?"), "explain", False, False, 20),
                (_("Hecho" if has_changed_rules else "No importa"), False, False, False, 0)
            )

        show monika 1eua zorder MAS_MONIKA_Z at t21

        if has_changed_rules:
            m "¿Te gustaría cambiar algo más?" nointeract
        else:

            m "¿Qué tipo de regla te gustaría cambiar?" nointeract

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)

        show monika 1eua zorder MAS_MONIKA_Z at t11

        if not _return:

            call monika_change_nou_house_rules.no_change
            $ del menu_items, final_items

            if _return:
                jump mas_nou_game_define

            return

        elif _return == "points_to_win":
            m 1eub "¡De acuerdo!"
            call monika_change_nou_house_rules.change_points_to_win_loop

        elif _return == "starting_cards":
            m 1eub "¡De acuerdo!"
            call monika_change_nou_house_rules.change_starting_cards_loop

        elif _return == "stackable_d2":
            if not mas_nou.get_house_rule("stackable_d2"):
                m 1tub "Okey, pero debo advertirte que eso podría ir en tu contra~"
            else:

                m 1ttu "¿Tienes miedo de que te haga sacar todas las cartas?~"
                m 1hub "Jajaja~ ¡Estoy bromeando!"

            $ mas_nou.reverse_house_rule("stackable_d2")

        elif _return == "unrestricted_wd4":
            if not mas_nou.get_house_rule("unrestricted_wd4"):
                m 1eua "Eso suena divertido."
            else:

                m 1eua "De vuelta a lo clásico, ya veo."

            $ mas_nou.reverse_house_rule("unrestricted_wd4")

        elif _return == "reflect_chaos":
            if not mas_nou.get_house_rule("reflect_chaos"):
                m 1kuu "Oh, será mejor que estés preparado para esto, [player]~"
            else:

                m 1ttu "¿Fue demasiado caótico?~"

            $ mas_nou.reverse_house_rule("reflect_chaos")

        elif _return == "restore":
            m 3eub "¡Okey! ¡Entonces acomódate!"

            python:
                mas_nou.update_house_rules(force=True)
                store.mas_nou.reset_points()
                del menu_items, final_items

            return
        else:

            m 1eub "¡Seguro!"
            m 1eua "Puntos de victoria es el número de puntos que necesitas alcanzar para ganar la partida."
            m 3eud "Si quieres jugar sin puntos, solo tienes que elegir '0'."
            m 1eua "También podemos empezar cada ronda con un número diferente de cartas en nuestras manos."
            m 3esa "Por ejemplo, si quieres partidas más largas, podemos empezar con 10 cartas."
            m 1eua "{i}Roba 2 apilable{/i} significa que cada vez que alguien refleja un 'roba 2', las cartas se {i}agrupan{/i}...{w=0.3}{nw}"
            extend 4tsb " y la última persona desafortunada tendrá que sacar todas esas cartas."
            m 1eua "Esto también se aplica a los comodines roba 4, ya que utilizas los comodines roba 2 para reflejarlos."
            m 1ttu "Suena divertido, heh~"
            m 3eud "También hay una regla en el set oficial que te permite jugar un roba 4 solo si no tienes cartas del color actual."
            m 1rtu "Eso...{w=0.3} suena un poco aburrido, {w=0.2}{nw}"
            extend 3eua "así que podemos ignorar esa regla si quieres."
            m 1eud "La regla reflejo caótico hace que el juego sea más {w=0.2}{nw}"
            extend 1tsu "{i}caótico{/i}...{w=0.3}{nw}"
            extend 1hub " como podrías suponer, ¡jajaja!~"
            m 3eub "Permite reflejar {i}comodines roba 4{/i} y {i}roba 2{/i} usando {i}comodines roba 4{/i}."
            m 3eua "Así como reflejar {i}saltar{/i}s con cualquier otro {i}Skip{/i}."
            m 1eua "¡Y eso es todo!"

            jump monika_change_nou_house_rules.menu_loop

    $ store.mas_nou.reset_points()
    $ has_changed_rules = True
    jump monika_change_nou_house_rules.menu_loop


label monika_change_nou_house_rules.no_change:

    if from_game:
        return False

    if not has_changed_rules:
        m 1eua "Oh, de acuerdo."
        return False

    if not mas_nou.does_want_suggest_play():
        m 2eub "Juguemos juntos pronto~"
        return False

    m "¿Podríamos jugar ahora?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Podríamos jugar ahora?{fast}"
        "Seguro":

            show monika 1hua zorder MAS_MONIKA_Z
            $ mas_nou.visit_game_ev()
            return True
        "Quizás más tarde":

            m 2eub "De acuerdo, juguemos juntos pronto~"

    return False


label monika_change_nou_house_rules.change_points_to_win_loop:
    $ ready = False
    while not ready:
        show monika 1eua zorder MAS_MONIKA_Z at t11

        $ points_cap = store.mas_utils.tryparseint(
            renpy.input(
                "¿Cuántos puntos quieres que tenga?",
                allow=numbers_only,
                length=4
            ).strip("\t\n\r"),
            200
        )

        if points_cap < 0:
            m 2rksdla "[player], el juego nunca terminará si el resultado es negativo."
            m 7ekb "¡Intenta de nuevo, tontito!"

        elif points_cap == 0:
            m 3eua "Oh, ¿solo quieres jugar partidas rápidas?"
            m 2tuu "¡Entendido! Pero no esperes que sea fácil para ti~"
            $ mas_nou.set_house_rule("points_to_win", points_cap)
            $ ready = True

        elif points_cap < 50:
            m 3rksdlb "Hmm, no tiene sentido jugar con un total de puntos {i}tan{/i} pequeño."
            m 1eka "Podemos jugar sin puntos si lo deseas.{nw}"
            $ _history_list.pop()
            menu:
                m "Podemos jugar sin puntos si lo deseas.{fast}"
                "Me gustaría eso":

                    m 1eub "Oh, ¡de acuerdo!"
                    $ mas_nou.set_house_rule("points_to_win", 0)
                    $ ready = True
                "Nah.":

                    m 3eua "Entonces elige de nuevo."

        elif points_cap > 3000:
            m 2eka "Oh, es demasiado, creo..."
            m 7eka "¿Lo dejamos en 3000?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Lo dejamos en 3000?{fast}"
                "De acuerdo":

                    m 1eua "Establecido."
                    $ mas_nou.set_house_rule("points_to_win", 3000)
                    $ ready = True
                "Nah":

                    m 3eua "Entonces elige de nuevo."
        else:

            m 3eub "Bien, a partir de ahora, ¡quien llegue a [points_cap] puntos, gana!"
            $ mas_nou.set_house_rule("points_to_win", points_cap)
            $ ready = True

    $ del ready, points_cap

    return

label monika_change_nou_house_rules.change_starting_cards_loop:
    $ ready = False
    while not ready:
        show monika 1eua zorder MAS_MONIKA_Z at t11

        $ starting_cards = store.mas_utils.tryparseint(
            renpy.input(
                "¿Con cuántas cartas te gustaría empezar el juego?",
                allow=numbers_only,
                length=2
            ).strip("\t\n\r"),
            7
        )

        if starting_cards < 1:
            m 2rksdlb "¡No podemos jugar a las cartas sin cartas, [player]!"
            m 7ekb "Inténtalo de nuevo, tontito~"

        elif starting_cards < 4:
            m 2eka "[starting_cards] cartas no es suficiente para disfrutar del juego, [player]..."
            m 7eka "¿Qué tal si empezamos con al menos 4 cartas?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Qué tal si empezamos con al menos 4 cartas?{fast}"
                "De acuerdo":

                    $ mas_nou.set_house_rule("starting_cards", 4)
                    $ ready = True
                "Nah":

                    m 3eua "Entonces inténtalo de nuevo."

        elif starting_cards > 20:
            m 2hub "Jajaja, ¡[player]! ¿Esperas que sostenga [starting_cards] cartas?"
            m 7eua "Si quieres, ¿podemos dejarlo en 20 cartas?{nw}"
            $ _history_list.pop()
            menu:
                m "Si quieres, ¿podemos dejarlo en 20 cartas?{fast}"
                "De acuerdo":

                    $ mas_nou.set_house_rule("starting_cards", 20)
                    $ ready = True
                "Nah":

                    m 3eua "PEntonces inténtalo de nuevo."
        else:

            $ _round = _("round") if mas_nou.get_house_rule("points_to_win") else _("game")
            m 3eub "Okey, a partir de ahora, ¡empezaremos cada [_round!t] con [starting_cards] cartas!"
            $ mas_nou.set_house_rule("starting_cards", starting_cards)
            $ ready = True

    $ del ready, starting_cards

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain_nou_rules",
            prompt="¿Puede explicarme las reglas del NOU?",
            category=["juegos"],
            pool=True,
            unlocked=False,
            conditional="renpy.seen_label('mas_reaction_gift_noudeck')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_explain_nou_rules:
    m 1hua "Por supuesto, [player]."
    m 3eub "Al principio, el juego parece complicado, {w=0.1}{nw}"
    extend 4eub "pero en realidad es muy sencillo."
    m 4eua "Seguro que si jugamos unas cuantas partidas más, le cogerás el truco."

    if mas_nou.get_house_rule("starting_cards") == 7:
        m 7esa "Entonces, empezamos el juego con 7 cartas."
    else:

        m 7esa "Así que, como estamos jugando con las reglas de la casa, empezamos el juego con [mas_nou.get_house_rule('starting_cards')] cartas."

    m 1esa "Tu objetivo es jugar todas tus cartas antes de que yo juegue todas las mías."
    m 3eub "Para jugar una carta tienes que hacerla coincidir por el color o el texto con la carta superior de la pila de descartes."
    m 3eua "Si no puedes jugar una carta en tu turno, debes robar una de la pila de robo."
    m 1esa "Sin embargo, no es {i}necesario{/i} que lo juegues."

    if mas_nou.get_house_rule("points_to_win"):
        m 3eub "Después de que hayas jugado una carta o hayas saltado tu turno, comienza mi turno. Y así sucesivamente hasta que alguien gane la ronda."
        m 1eua "El ganador recibe los puntos iguales a las cartas restantes en la mano del oponente."
        m "Entonces jugamos más rondas hasta que uno de nosotros llega a la meta de [mas_nou.get_house_rule('points_to_win')] puntos."
        m 1esa "Esta puntuación hace que el juego sea más competitivo y estratégico."
    else:

        m 3eub "Después de que juegues una carta o saltes tu turno, comienza mi turno y así hasta que alguien gane la partida."
        m 1esa "Este tipo de puntuación hace que el juego sea más rápido y casual."

    m 3eub "Una regla importante es que {i}antes{/i} de jugar tu penúltima carta, {w=0.2}{nw}"
    extend 7eub "debes gritar 'NOU'. ¡Para que sepa que estás cerca de la victoria!"
    m 2rksdla "Bueno, supongo que gritar no funcionará en nuestro caso..."
    m 7hub "Pero puedes pulsar un botón para hacérmelo saber."
    m 1eua "Si uno de nosotros se olvida de decir 'NOU', el otro puede {i}recordárselo{/i}. Eso hará que la persona desafortunada robe 2 cartas más."
    m 3eub "Además de las cartas con {i}números{/i}, también hay cartas especiales conocidas como cartas de {i}acción{/i} y {i}comodines{/i}."
    m 3eua "Puedes distinguir una carta de {i}acción{/i} por su símbolo, y una carta {i}comodín{/i} por su color negro."
    m 1eua "Estas cartas pueden hacer que tu oponente se salte su turno o incluso robar más cartas."
    m 1tsu "Y por más, me refiero a 12 cartas seguidas."
    m 1eua "Los {i}comodines{/i} no tienen un color, lo que significa que pueden colocarse en cualquier carta."

    if not mas_nou.get_house_rule("unrestricted_wd4"):
        m 3eua "Si no tienes otras cartas con el color de la pila de descarte, claro."
    else:

        m 3eua "Usualmente, solo puedes jugarlas si no tienes otras cartas del mismo color en la pila de descartes, pero estamos jugando con nuestras propias reglas."

    m 1eua "Cuando juegas cualquier {i}comodín{/i}, debes elegir qué color quieres poner para él."
    m "Por muy poderosos que parezcan puedes salvarte de los {i}comodines {/i} y las cartas de {i}acción{/i}."
    m 1eub "Por ejemplo, puedes reflejar un {i}comodin roba 4{/i} jugando un {i}roba 2{/i} con el nuevo color."
    m 3eua "... O puedes jugar cualquier roba 2 para reflejar otro roba 2 a tu oponente. El color no importa en ese caso."
    m 1ekb "Espero que todo eso te sirva para entender mejor el juego."
    m 1eku "Pero de todos modos no creo que se trate realmente de ganar."
    show monika 5hubla zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubla "Jejeje~"
    return



label mas_nou_game_start:
    if (
        (
            persistent._mas_game_nou_abandoned > 1
            or store.mas_nou.monika_win_streak > 2
        )
        and random.random() < 0.5
    ):
        m 1kua "¡Estoy segura de que ganarás esta vez!"

    elif (
        store.mas_nou.player_win_streak > 2
        and random.random() < 0.5
    ):
        m 1tuu "Será mejor que estés preparado, esta vez no te lo voy a poner fácil~"

    elif (
        mas_nou.get_house_rule("points_to_win")
        and (
            persistent._mas_game_nou_points["Monika"] > 0
            or persistent._mas_game_nou_points["Player"] > 0
        )
    ):
        if store.mas_nou.winner is not None:
            m 1hua "Continuemos~"
        else:

            m 1hua "¿Quieres terminar nuestro juego?"
            m 3eua "Déjame tomar nota de nuestra puntuación.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    else:

        m 1eub "Déjame repartir nuestras cartas~"



label mas_nou_game_define:
    $ store.mas_nou.game = store.mas_nou.NOU()


label mas_nou_game_loop:

    window hide
    $ HKBHideButtons()
    $ disable_esc()

    scene bg cardgames desk onlayer master zorder 0

    $ store.mas_nou.game.set_visible(True)

    show screen nou_gui
    show screen nou_stats
    with Fade(0.2, 0, 0.2)
    $ renpy.pause(0.2, hard=True)

    $ store.mas_nou.game.prepare_game()
    $ store.mas_nou.in_progress = True


    while store.mas_nou.in_progress:
        $ store.mas_nou.game.game_loop()



label mas_nou_game_end:

    $ store.mas_nou.in_progress = False

    $ store.mas_nou.game.set_visible(False)

    hide screen nou_stats
    hide screen nou_gui

    call spaceroom (scene_change=True, force_exp="monika 1eua")

    $ enable_esc()
    $ HKBShowButtons()
    window auto

    python:
        if mas_nou.get_house_rule("points_to_win"):
            _round = _("ronda")

        else:
            _round = _("partida")

        dlg_choice = None

        if (
            store.mas_nou.winner != "Surrendered"
            and not seen_event("monika_introduce_nou_house_rules")
        ):
            MASEventList.push("monika_introduce_nou_house_rules")

    if store.mas_nou.winner == "Player":
        call mas_nou_reaction_player_wins_round

        python:
            store.mas_nou.give_points()
            persistent._mas_game_nou_abandoned = 0
            store.mas_nou.player_wins_this_sesh += 1
            store.mas_nou.player_win_streak += 1
            store.mas_nou.monika_win_streak = 0
            persistent._mas_ever_won["nou"] = True

        if (
            mas_nou.get_house_rule("points_to_win")
            and persistent._mas_game_nou_points["Player"] >= mas_nou.get_house_rule("points_to_win")
        ):
            call mas_nou_reaction_player_wins_game

            $ store.mas_nou.reset_points()

            m 3eua "¿Te gustaría jugar un poco más?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Te gustaría jugar un poco más?{fast}"
                "Seguro":

                    m 1hub "¡Yay!"
                    show monika 1hua zorder MAS_MONIKA_Z
                    python:
                        store.mas_nou.game.reset_game()
                        mas_nou.visit_game_ev()

                    jump mas_nou_game_loop
                "Me gustaría cambiar algunas reglas de la casa":

                    jump mas_nou_game_end_change_rules_and_continue
                "Ahora no":

                    m 1hua "Okey, avísame cuando quieras volver a jugar~"

            jump mas_nou_game_end_end

    elif store.mas_nou.winner == "Monika":
        call mas_nou_reaction_monika_wins_round

        python:
            store.mas_nou.give_points()
            persistent._mas_game_nou_abandoned = 0
            store.mas_nou.monika_wins_this_sesh += 1
            store.mas_nou.monika_win_streak += 1
            store.mas_nou.player_win_streak = 0

        if (
            mas_nou.get_house_rule("points_to_win")
            and persistent._mas_game_nou_points["Monika"] >= mas_nou.get_house_rule("points_to_win")
        ):
            call mas_nou_reaction_monika_wins_game

            $ store.mas_nou.reset_points()

            m 3eua "¿Quieres jugar un poco más?{nw}"
            $ _history_list.pop()
            menu:
                m "¿Quieres jugar un poco más?{fast}"
                "Seguro":

                    m 1hub "¡Yay!"
                    show monika 1hua zorder MAS_MONIKA_Z
                    python:
                        store.mas_nou.game.reset_game()
                        mas_nou.visit_game_ev()

                    jump mas_nou_game_loop
                "Me gustaría cambiar algunas reglas de la casa":

                    jump mas_nou_game_end_change_rules_and_continue
                "Ahora no":

                    m 1hua "Okey, avísame cuando quieras volver a jugar~"

            jump mas_nou_game_end_end
    else:


        python:
            persistent._mas_game_nou_abandoned += 1
            store.mas_nou.player_win_streak = 0

            mas_nou.give_points()
            if persistent._mas_game_nou_points["Monika"] >= mas_nou.get_house_rule("points_to_win"):
                store.mas_nou.reset_points()

        call mas_nou_reaction_player_surrenders


        jump mas_nou_game_end_end

    m 3eua "¿Te gustaría jugar otra [_round!t]?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Te gustaría jugar otra [_round!t]?{fast}"
        "Seguro":

            show monika 1hua zorder MAS_MONIKA_Z
            python:
                store.mas_nou.game.reset_game()
                mas_nou.visit_game_ev()

            jump mas_nou_game_loop

        "Me gustaría cambiar algunas reglas de la casa" if not mas_nou.get_house_rule("points_to_win"):
            jump mas_nou_game_end_change_rules_and_continue
        "Ahora no":

            m 1hua "De acuerdo, juguemos de nuevo pronto~"


label mas_nou_game_end_end:

    $ del dlg_choice, _round, store.mas_nou.game

    return


label mas_nou_game_end_change_rules_and_continue:
    call monika_change_nou_house_rules.pre_menu (from_game=True)

    m 3hub "¿Listo para continuar?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Listo para continuar?{fast}"
        "Sip":

            show monika 1hua zorder MAS_MONIKA_Z
            python:
                store.mas_nou.game.reset_game()
                mas_nou.visit_game_ev()

            jump mas_nou_game_loop
        "Juguemos más tarde":

            if (mas_nou.player_wins_this_sesh + mas_nou.monika_wins_this_sesh) < 4:
                m 1ekc "Aww, de acuerdo."
            else:

                m 1eka "Oh, de acuerdo."

    jump mas_nou_game_end_end



label mas_nou_reaction_player_wins_round:
    if persistent._mas_game_nou_abandoned > 2:
        m 1hua "Me alegro de que hayas ganado esta vez..."
        m 3eub "¡Buen trabajo, [player]!"

    elif store.mas_nou.player_win_streak > 3:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 1wud "[player]...{w=0.5} sigues ganando..."

            if len(store.mas_nou.game.monika.hand) > 2:
                m 1hksdlb "¡No tengo ninguna oportunidad contra ti!"
            else:

                m 1hksdlb "Al menos dame una oportunidad~"

        elif dlg_choice == 2:
            m 1eub "¡Y otra [_round!t] más!"
            m 3hub "¡Increíble, [player]!"
        else:

            m 1wud "¡Vaya! ¡Has vuelto a ganar!"
            m 3esa "¿Me vas a contar tu secreto,[player]?"
            m 1hua "Yo también quiero ganar~"

    elif store.mas_nou.player_win_streak > 2:
        $ dlg_choice = renpy.random.randint(1, 4)

        if dlg_choice == 1:
            m 1hub "¡Y ganaste otra [_round!t]!"
            m 3eub "¡Eres realmente bueno!"

        elif dlg_choice == 2:
            m 4eub "Increíble, ¡volviste a ganar!"
            m 1tsu "Pero estoy segura de que ganaré la próxima [_round!t]."

        elif dlg_choice == 3:
            m 1hub "¡Increíble! ¡Otra victoria para ti!"
            m 1eub "Pero no te relajes. {w=0.5}{nw}"
            extend 1kua "¡Estoy segura de que ganaré la próxima vez!"
        else:

            m 1tuu "Hoy estás de suerte."
            m 1hub "Jajaja~ ¡Buen trabajo, [player]!"

    elif store.mas_nou.monika_win_streak > 3:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 3eua "Me alegra mucho que hayas ganado esta vez~"

        elif dlg_choice == 2:
            m 1hua "Tenía la sensación de que ganarías~"
            m 3hub "Jejeje~ ¡Buen trabajo!"
        else:

            if len(store.mas_nou.game.monika.hand) > 2:
                m 1tuu "Tu suerte debe estar de vuelta~"
                m 1hua "¡Bien jugado! Jejeje~"
            else:

                m 1hub "¡Yay, has ganado!~"

    elif store.mas_nou.monika_win_streak > 2:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 1tsa "Oh, ¿empezaste a jugar en serio?"
            m 1hub "Jajaja~"

        elif dlg_choice == 2:
            if len(store.mas_nou.game.monika.hand) < 3:
                m 1ruu "Ah... ¡Yo también estuve a punto de ganar!"
                m 3hua "Bien jugado, [player]."
            else:

                m 1hub "Ganaste, [player]!"
                if len(store.mas_nou.game.monika.hand) > 3:
                    m 3hub "¡Eso fue increíble!"
        else:

            if store.mas_nou.game.current_turn > 40:
                m 2tub "¡Esta vez sí que te has esforzado!"
                m 1hub "¡Buen trabajo, [player]!"
            else:

                m 1hua "¡Y ganaste! Que bien~"

    elif store.mas_nou.game.current_turn < 25:
        if store.mas_nou.player_win_streak > 0:
            $ dlg_choice = renpy.random.randint(1, 3)

            if dlg_choice == 1:
                m 1hub "¡Otra victoria rápida para tí!"

                if random.random() < 0.25:
                    m 1kuu "Pero será mejor que no te relajes, [player]~"

            elif dlg_choice == 2:
                m 1wuo "¡Wow, [player]!"
                m 1hksdlb "¡No puedo seguirte el ritmo!"
            else:

                if len(store.mas_nou.game.monika.hand) > 3:
                    m 1rka "¿Quizás debería esforzarme un poco más?~"
                    m 1hksdla "Jejeje, sigues terminando cada [_round!t] antes de que pueda hacer algo."
                else:

                    m 1hfb "Ah...{w=0.2} ¡Estuve tan cerca!"
                    m 3efb "¡Buen trabajo, [player]!"

        elif (
            mas_nou.get_house_rule("starting_cards") > 12
            and (
                len(store.mas_nou.game.monika.hand) > 4
                or (
                    not store.mas_nou.game.player.yelled_nou
                    and random.random() < 0.5
                )
            )
        ):
            m 4wuo "¡Wow!{w=0.2} ¿Ya has jugado todas tus cartas?"
            m 7husdlb "¡Eso fue rápido!"
        else:

            $ dlg_choice = renpy.random.randint(1, 3)

            if dlg_choice == 1:
                m 3hub "¡Bien jugado!"

            elif dlg_choice == 2:
                m 3hub "¡Impresionante, [player]!"
            else:

                m 3hub "¡Eso ha sido una [_round!t] rápida para ti!"

    elif store.mas_nou.game.current_turn > 55:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            if mas_nou.get_house_rule("starting_cards") < 12:
                m 1esa "Ha sido una [_round!t] bastante larga, [player]."

                if len(store.mas_nou.game.monika.hand) < 4:
                    if store.mas_nou.player_win_streak > 0:
                        m 1hua "¡Y casi gano esta vez!"
                    else:

                        m 1hua "¡Y casi gano!"

                    m 1hub "Jajaja~ ¡Bien jugado!"
                else:

                    m 1hub "¡Bien jugado!"
            else:

                m 1hub "¡Bien jugado!"

        elif dlg_choice == 2:
            m 1kuu "¡Eso fue intenso!"
        else:

            m 1hua "Jejeje~ {w=0.3}{nw}"
            extend 1eub "¡Eres realmente bueno!"
    else:

        $ dlg_choice = renpy.random.randint(1, 4)

        if dlg_choice == 1:
            if store.mas_nou.player_win_streak > 0:
                m 1eub "¡Ganaste de nuevo!"
            else:

                m 1eub "¡Ganaste!~"

        elif dlg_choice == 2:
            m 1hub "¡Esta [_round!t] es tuya!"

        elif dlg_choice == 3:
            m 2eub "¡Y has ganado! ¡Buen trabajo!"
            if random.random() < 0.2:
                m 2kuu "Pero no esperes ganar siempre~"
        else:

            if store.mas_nou.monika_win_streak > 1:
                m 2eua "Me alegro de que hayas ganado esta vez~"

            m 3hub "¡Buen trabajo, [player]!"
    return

label mas_nou_reaction_player_wins_game:
    $ dlg_choice = renpy.random.randint(1, 4)

    if dlg_choice == 1:
        m 1eud "¡Oh! {w=0.2}{nw}"
        extend 3eub "En realidad, ¡ganaste esta ronda!"

        m 1ruu "No me di cuenta de que estabas tan cerca de la victoria."
        m 3hua "Buen trabajo, jejeje~"

    elif dlg_choice == 2:
        m 3eub "¡Oh, y también ganaste esta ronda!"
        m 1hua "¡Felicidades! Jejeje~"

    elif dlg_choice == 3:
        m 1rsc "Veamos.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
        m 4eub "¡Oh, [player]! ¡Has ganado esta ronda!"

        if mas_isMoniEnamored(higher=True) and random.random() < 0.5:
            m 1hub "Te daría un gran abrazo si estuviera cerca de ti~"
            m 1hua "Jejeje~"
        else:
            m 1hua "¡Eso fue divertido!"
    else:

        m 4eub "... ¡Y eres el primero en alcanzar [mas_nou.get_house_rule('points_to_win')] puntos!"
        m 1hua "Felicidades, [player]~"
    return

label mas_nou_reaction_monika_wins_round:
    if persistent._mas_game_nou_abandoned > 2:
        m 2wub "¡He ganado!~"
        m 7eka "Gracias por terminar esta ronda, [player]. {w=0.3}{nw}"
        extend 1hub "¡Estoy segura de que ganarás la próxima vez!"

    elif store.mas_nou.player_win_streak > 3:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            if len(store.mas_nou.game.player.hand) > 4:
                m 1hub "¡He ganado!"
                m 1hksdla "..."
                m 1eka "No sin tu ayuda, supongo. Jejeje~"
            else:

                m 3tsb "¡Te dije que ganaría!"
                m 1tfu "Ahora te toca sacar cartas."

        elif dlg_choice == 2:
            m 4sub "¡Jajaja! Mi suerte ha vuelto~"
        else:

            m 4sub "¡Ahí está!"
            m 7hub "Finalmente gané~"

    elif store.mas_nou.player_win_streak > 2:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 2tub "No te relajes, [player]~"

        elif dlg_choice == 2:
            m 1hua "¡Gané!"
        else:

            m 1hub "¡Yay, gané esta vez!"

    elif store.mas_nou.monika_win_streak > 3:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 1hub "¡Y otra victoria para mí!~"

        elif dlg_choice == 2:
            if len(store.mas_nou.game.player.hand) < 3:
                m 1eub "¡Eso fue duro, [player]! {w=0.5}{nw}"
                extend 3eua "Casi ganas esta vez."
            else:

                m 1kua "Tengo el presentimiento de que ganarás la próxima [_round!t]~"
        else:

            if len(store.mas_nou.game.player.hand) < 3:
                m 1huu "Bien jugado, [player]. Pero la victoria es mía de nuevo~"
            else:

                m 3eub "¡Eso fue divertido!"
                m 1eka "Espero que disfrutes jugando conmigo, [player]~"
                m 1kua "Tal vez la próxima vez ganes."

    elif store.mas_nou.monika_win_streak > 2:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 1hua "Jejeje~ Otra victoria para mí~"

        elif dlg_choice == 2:
            if len(store.mas_nou.game.player.hand) < 3:
                m 3eub "Esta vez estuviste muy cerca, [player]."
            else:

                m 2tuu "¿Debería ser más suave contigo?"
                m 7hub "Jajaja, es una broma, [player]~"
        else:

            m 4hub "¡Gané de nuevo!"

    elif store.mas_nou.game.current_turn < 25:
        if store.mas_nou.monika_win_streak > 0:
            $ dlg_choice = renpy.random.randint(1, 3)

            if dlg_choice == 1:
                m 4hub "¡Otra victoria rápida para mí!"

            elif dlg_choice == 2:
                m 1tub "No puedes seguirme el ritmo, ¿eh?~"
            else:

                m 1eub "¡Yay, he vuelto a ganar!"
        else:

            $ dlg_choice = renpy.random.randint(1, 2)

            if dlg_choice == 1:
                m 1wub "Yay, gané~"
            else:

                m 3eub "¡Eso fue rápido!"

    elif store.mas_nou.game.current_turn > 55:
        $ dlg_choice = renpy.random.randint(1, 3)

        if dlg_choice == 1:
            m 1eub "¡Esa fue una [_round!t] larga!"

            if len(store.mas_nou.game.player.hand) < 4:
                if store.mas_nou.monika_win_streak > 0:
                    m 3eua "Casi ganas esta vez."
                else:

                    m 3eua "Casi ganas."

                m 3hub "Jejeje~ ¡Bien jugado!"
            else:

                m 3hub "¡Bien jugado!"

        elif dlg_choice == 2:
            m 1hub "¡Eso fue intenso!"
        else:

            if len(store.mas_nou.game.player.hand) > 4:
                m 1tsb "Nada mal, [player]."
                m 3tub "Creo que incluso podrías haber ganado esta vez, {w=0.5}{nw}"
                extend 1tuu "si no fuera por todas esas cartas que tomaste."
                m 1hub "Jajaja~"
            else:

                m 1wub "Oh, ¡gané!"
    else:

        if store.mas_nou.monika_win_streak > 0:
            m 1hua "Gané de nuevo~"

        elif store.mas_nou.player_win_streak > 1:
            m 1sub "Finalmente, gané~"
        else:

            m 1hua "Gané~"
    return

label mas_nou_reaction_monika_wins_game:
    $ dlg_choice = renpy.random.randint(1, 4)

    if dlg_choice == 1:
        m 1eub "¡Y esta vez gané la partida!"
        if store.mas_nou.get_player_points_percentage("Player") < 0.3:
            m 4eub "Sin embargo, ¡estuviste bastante cerca!"
            if random.random() < 0.7:
                m 4hua "Estoy segura de que ganarás la próxima vez."
            else:

                m 7ttu "¿Me dejaste ganar a propósito?"
                m 1huu "Jejeje~"
        else:


            m 1hub "¡Me divertí mucho!"
            m 3eua "Estoy segura de que ganarás la próxima vez."

    elif dlg_choice == 2:
        m 1wub "¡Oh!{w=0.1} ¡Gané esta ronda!"
        m 3hub "¡Eso fue muy divertido!"
        if store.mas_nou.get_player_points_percentage("Player") < 0.3:
            m 1eka "Espero que también te hayas divertido."

            if (
                mas_nou.get_total_games() < 40
                and mas_nou.get_wins_for("Monika") > mas_nou.get_wins_for("Player")
            ):
                m 3hua "Estoy segura de que si jugamos más partidas tú también ganarás."
            else:

                m 3hua "Tal vez la próxima vez ganes~"

    elif dlg_choice == 3:
        m 2wub "¡También gané esta ronda!"
        m 2hua "Jejeje~"
        m 1hub "Gracias por jugar conmigo, [player]~"
    else:

        m 3eub "¡Y soy la primera que alcanzó [mas_nou.get_house_rule('points_to_win')] puntos!"
        m 1hua "Esta vez gané~"
    return

label mas_nou_reaction_player_surrenders:
    if persistent._mas_game_nou_abandoned > 4:
        m 1ekc "Está bien, [player]..."
        m 1eka "¿Pero prometes que terminarás el juego la próxima vez?{w=0.4} ¿Por mí?~"

    elif persistent._mas_game_nou_abandoned > 2:
        m 1ekc "[player]...{w=0.3}{nw}"
        extend 1eksdld " sigues renunciando a nuestras partidas..."
        m 1rksdlc "Espero que disfrutes jugando conmigo."
        m 1eka "Yo disfruto cada momento que estoy contigo~"

    elif store.mas_nou.game.current_turn == 1:
        m 1etd "Pero acabamos de empezar..."
        m 1ekc "Avísame cuando tengas tiempo para jugar, ¿de acuerdo?"

    elif store.mas_nou.game.current_turn < 6:
        m 1ekc "¿Ya te has rendido, [player]?"
        if (
            len(store.mas_nou.game.monika.hand) < 5
            and len(store.mas_nou.game.player.hand) > 8
        ):
            m 3ekb "¡Me encanta jugar contigo sin importar el resultado!"
            m 1eka "Espero que sientas lo mismo~"
        else:

            m 1rud "Al menos podrías intentar..."
            m 1eka "Significaría mucho para mí."
    else:


        if len(store.mas_nou.game.monika.hand) >= len(store.mas_nou.game.player.hand):
            m 3ekb "¡Estoy segura de que podrías ganar esta [_round!t], [player]!"
        else:

            if len(store.mas_nou.game.monika.hand) > 1:
                m 2esa "En realidad, tenía cartas bastante malas, [player]."
            else:
                m 2esa "En realidad, tuve una última carta bastante mala, [player]."

            m 7eka "Creo que podrías ganar esta [_round!t]."

        m 3ekb "No te rindas tan fácilmente la próxima vez."
    return





screen nou_stats():

    layer "master"
    zorder 5

    style_prefix "nou"

    add MASFilterSwitch(
        "mod_assets/games/nou/note.png"
    ) pos (5, 120) anchor (0, 0) at nou_note_rotate_left


    add MASFilterSwitch(
        "mod_assets/games/nou/pen.png"
    ) pos (210, 370) anchor (0.5, 0.5) at nou_pen_rotate_right

    text _("Nuestro puntaje:") pos (87, 110) anchor (0, 0.5) at nou_note_rotate_left


    if mas_nou.get_house_rule("points_to_win") == 0:
        $ monika_score = store.mas_nou.monika_wins_this_sesh
        $ player_score = store.mas_nou.player_wins_this_sesh

    else:
        $ monika_score = store.persistent._mas_game_nou_points["Monika"]
        $ player_score = store.persistent._mas_game_nou_points["Player"]

    text _("Monika: [monika_score]") pos (60, 204) anchor (0, 0.5) at nou_note_rotate_left
    text _("[player]: [player_score]") pos (96, 298) anchor (0, 0.5) at nou_note_rotate_left


screen nou_gui():

    zorder 50

    style_prefix "nou"

    default fn_end_turn = store.mas_nou.game.end_turn
    default fn_handle_nou_logic = store.mas_nou.game.handle_nou_logic
    default game = store.mas_nou.game
    default player = store.mas_nou.game.player
    default monika = store.mas_nou.game.monika
    default discardpile = store.mas_nou.game.discardpile


    vbox:
        xalign 0.975
        yalign 0.5

        textbutton _("Me salto este turno"):
            sensitive (
                
                player.plays_turn
                and (
                    
                    (player.drew_card or len(player.hand) >= game.HAND_CARDS_LIMIT)
                    
                    or player.should_skip_turn
                )
                and (
                    
                    not player.should_draw_cards
                    
                    or len(player.hand) >= game.HAND_CARDS_LIMIT
                )
                and (
                    
                    discardpile
                    and discardpile[-1].color is not None
                )
            )
            action [
                Function(fn_end_turn, player, monika),
                Return([])
            ]

        null height 15

        if (
            player.plays_turn
            and not player.played_card
        ):
            textbutton _("¡NOU!"):
                sensitive not store.mas_nou.disable_yell_button
                action [
                    SetField(mas_nou, "disable_yell_button", True),
                    Function(fn_handle_nou_logic, "player")
                ]

            textbutton _("¡Te olvidaste de decir 'NOU'!"):
                sensitive (
                    not store.mas_nou.disable_remind_button
                    and not player.drew_card
                )
                action [
                    SetField(mas_nou, "disable_remind_button", True),
                    Function(fn_handle_nou_logic, "monika")
                ]

        else:
            textbutton _("¡NOU!")
            textbutton _("¡Te olvidaste de decir 'NOU'!")

        null height 15

        textbutton _("¿Puedes ay{}darme?".format("a" if mas_isA01() or mas_isO31() else "u")):
            sensitive player.plays_turn and not player.played_card
            action Function(game.say_help)



        textbutton _("Me rindo..."):
            selected False
            sensitive player.hand and monika.hand
            action [
                SetField(mas_nou, "winner", "Surrendered"),
                SetField(mas_nou, "in_progress", False),
                Jump("mas_nou_game_end")
            ]


    vbox:
        align (0.5, 0.5)

        if (
            player.plays_turn
            
            and (
                discardpile
                and discardpile[-1].color is None
            )
            and player.hand
        ):
            $ top_card = game.discardpile[-1]

            textbutton _("Rojo"):
                xminimum 230
                action If(
                    player.played_card,
                    true = [
                        SetField(top_card, "color", "rojo"),
                        Function(fn_end_turn, player, monika),
                        Return([])
                    ],
                    false = [
                        SetField(top_card, "color", "rojo"),
                        Return([])
                    ]
                )
            textbutton _("Celeste"):
                xminimum 230
                action If(
                    player.played_card,
                    true = [
                        SetField(top_card, "color", "celeste"),
                        Function(fn_end_turn, player, monika),
                        Return([])
                    ],
                    false = [
                        SetField(top_card, "color", "celeste"),
                        Return([])
                    ]
                )
            textbutton _("Verde"):
                xminimum 230
                action If(
                    player.played_card,
                    true = [
                        SetField(top_card, "color", "verde"),
                        Function(fn_end_turn, player, monika),
                        Return([])
                    ],
                    false = [
                        SetField(top_card, "color", "verde"),
                        Return([])
                    ]
                )
            textbutton _("Amarillo"):
                xminimum 230
                action If(
                    player.played_card,
                    true = [
                        SetField(top_card, "color", "amarillo"),
                        Function(fn_end_turn, player, monika),
                        Return([])
                    ],
                    false = [
                        SetField(top_card, "color", "amarillo"),
                        Return([])
                    ]
                )


style nou_vbox is vbox:
    spacing 5

style nou_vbox_dark is vbox:
    spacing 5

style nou_button is generic_button_light:
    xsize 200
    ysize None
    ypadding 5

style nou_button_dark is generic_button_dark:
    xsize 200
    ysize None
    ypadding 5

style nou_button_text is generic_button_text_light:
    kerning 0.2
    layout "subtitle"
    text_align 0.5

style nou_button_text_dark is generic_button_text_dark:
    kerning 0.2
    layout "subtitle"
    text_align 0.5

style nou_text:
    size 30
    color "#000"
    outlines []
    font "gui/font/m1.ttf"

style nou_text_dark:
    size 30
    color "#000"
    outlines []
    font "gui/font/m1.ttf"

transform nou_note_rotate_left:
    rotate -23
    rotate_pad True
    transform_anchor True

transform nou_pen_rotate_right:
    rotate 40
    rotate_pad True
    transform_anchor True




















image bg cardgames desk = mas_cardgames.DeskSpriteSwitch()

init 500 python in mas_cardgames:


    _m1_zz_cardgames__scanDeskSprites()

init -10 python in mas_cardgames:
    import pygame
    import store
    from store import RotoZoom, ConditionSwitch, MASFilterSwitch



    GAME_DIR_PATH = renpy.config.gamedir.replace("\\", "/") + "/"

    DESK_SPRITES_PATH = "mod_assets/games/nou/desks/"





    DESK_SPRITES_MAP = dict()

    def _m1_zz_cardgames__scanDeskSprites():
        """
        Scans the folder with the desk sprites and fills the desk sprites map
        """
        sprites_map = dict()
        
        for file in store.MASDockingStation(GAME_DIR_PATH + DESK_SPRITES_PATH).getPackageList():
            
            key = file.rpartition(".")[0]
            if key:
                sprites_map[key] = file
        
        
        fb = sprites_map.get(store.mas_background.MBG_DEF)
        for bg_id in store.mas_background.BACKGROUND_MAP.iterkeys():
            if bg_id not in DESK_SPRITES_MAP:
                filename = sprites_map.get(bg_id, fb)
                DESK_SPRITES_MAP[bg_id] = MASFilterSwitch(DESK_SPRITES_PATH + filename)

    class DeskSpriteSwitch(renpy.display.core.Displayable):
        """
        This displayable represents a desk for card games;
        It takes care of different backgrounds, too, using the map for desk sprites.
        """
        BLIT_COORDS = (0, 0)
        
        def __init__(self, **props):
            """
            Constructor

            IN:
                **props - general props for renpy displayable
            """
            super(DeskSpriteSwitch, self).__init__(**props)
            
            
            self._last_bg = store.mas_current_background
        
        def render(self, width, height, st, at):
            """
            Render of this disp

            ASSUMES:
                store.mas_current_background
            """
            try:
                sprite = DESK_SPRITES_MAP[store.mas_current_background.background_id]
            except KeyError:
                
                
                sprite = DESK_SPRITES_MAP[store.mas_background.MBG_DEF]
            
            desk_render = renpy.render(sprite, width, height, st, at)
            main_render = renpy.Render(desk_render.width, desk_render.height)
            main_render.blit(desk_render, DeskSpriteSwitch.BLIT_COORDS)
            
            return main_render
        
        def per_interact(self):
            """
            Interact callback
            While technically I doubt the background can be changed while the game is on
            and the disp seems to update when switching the bg
            (probably because of a different filter)
            I think it's more safe to just redraw after every interaction
            """
            bg = store.mas_current_background
            if self._last_bg != bg:
                self._last_bg = bg
                renpy.redraw(self, 0.0)
        
        def visit(self):
            """
            Returns imgs for prediction

            OUT:
                list of displayables

            ASSUMES:
                store.mas_current_background
            """
            return [DESK_SPRITES_MAP[store.mas_current_background.background_id]]


    DRAG_NONE = 0
    DRAG_CARD = 1
    DRAG_ABOVE = 2
    DRAG_STACK = 3
    DRAG_TOP = 4

    def _m1_zz_cardgames__rect_overlap_area(r1, r2):
        """
        Checks if 2 given rectangles overlap

        IN:
            r1, r2 - tuples of the following format: (x, y, w, h)

        OUT:
            overlap between the 2 rectangles (False if they don't overlap)
        """
        if r1 is None or r2 is None:
            return 0
        
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        
        maxleft = max(x1, x2)
        minright = min(x1 + w1, x2 + w2)
        maxtop = max(y1, y2)
        minbottom = min(y1 + h1, y2 + h2)
        
        if minright < maxleft:
            return 0
        
        if minbottom < maxtop:
            return 0
        
        return (minright - maxleft) * (minbottom - maxtop)

    def _m1_zz_cardgames__default_can_drag(table, stack, card):
        """
        Function to check if the player can drag card
        NOTE: You can use yours in the constructor,
            but it must always take 3 arguments
            and return True or False

        IN:
            table - the table the card belongs to
            stack - the stack the card belongs to
            card - the card the player tries to drag

        OUT:
            True if the card is set faceup, False otherwise
        """
        return table.get_faceup(card)

    class Table(renpy.display.core.Displayable):
        """
        Table class to represent a "table" for card games

        PROPERTIES:
            back - the back of cards that don't have a more specific back defined
            base - the base of stacks that don't have a more specific base defined
            springback - the amount of time it takes for cards to springback into their rightful place
            rotate - the amount of time it takes for cards to rotate into their proper orientation
            can_drag - a function that is called to tell if we can drag a particular card
            doubleclick - the time between clicks for the click to be considered a double-click
            cards - a map from card value to the card object corresponding to that value
            stacks - a list of the stacks that have been defined
            sensitive - weather or not we're sensetive to the user's input
            last_event - last click event (CardEvent() obj)
            click_card - the card that has been clicked
            click_stack - the stack that has been clicked
            drag_cards - the list of cards that are being dragged
            dragging - weather or not we're dragging some cards
            click_x - the x position where we clicked
            click_y - the y position where we clicked
            st - the amount of time we've been shown for
        """
        
        def __init__(
            self,
            back=None,
            base=None,
            springback=0.1,
            rotate=0.1,
            can_drag=_m1_zz_cardgames__default_can_drag,
            doubleclick=0.33,
            **kwargs
        ):
            """
            Constructor for Table objects

            IN:
                back - the back of cards that don't have a more specific back defined
                    (Default: None)
                base - the base of stacks that don't have a more specific base defined
                    (Default: None)
                springback - the amount of time it takes for cards to springback into their rightful place
                    (Default: 0.1)
                rotate - the amount of time it takes for cards to rotate into their proper orientation
                    (Default: 0.1)
                can_drag - a function that is called to tell if we can drag a particular card
                    (Default: __default_can_drag)
                doubleclick - the time between clicks for the click to be considered a double-click
                    (Default: 0.33)
            """
            super(Table, self).__init__(**kwargs)
            
            
            if isinstance(back, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.back = MASFilterSwitch(back)
            
            
            elif isinstance(back, renpy.display.core.Displayable):
                self.back = back
            
            
            else:
                self.back = None
            
            if isinstance(base, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.base = MASFilterSwitch(base)
            
            elif isinstance(base, renpy.display.core.Displayable):
                self.base = base
            
            else:
                self.base = None
            
            self.springback = springback
            
            self.rotate = rotate
            
            self.can_drag = can_drag
            
            self.doubleclick = doubleclick
            
            
            self.cards = {}
            
            
            self.stacks = []
            
            self.sensitive = True
            
            self.last_event = CardEvent()
            
            self.click_card = None
            
            self.click_stack = None
            
            self.drag_cards = []
            
            self.dragging = False
            
            self.click_x = 0
            self.click_y = 0
            
            self.st = 0
        
        def show(self, layer="minigames"):
            """
            Shows the table on the given layer

            IN:
                layer - the layer we'll render our table on
                    (Default: "minigames")
            """
            for v in self.cards.itervalues():
                v._offset = _m1_zz_cardgames__Fixed(0, 0)
            
            ui.layer(layer)
            ui.implicit_add(self)
            ui.close()
        
        def hide(self, layer="minigames"):
            """
            Hides the table on the given layer

            IN:
                layer - the layer we rendered our table on
                    (Default: "minigames")
            """
            ui.layer(layer)
            ui.remove(self)
            ui.close()
        
        def set_sensitive(self, value):
            """
            Changes the table's sensetivity

            IN:
                value - True if we set to sensetive, False otherwise
            """
            self.sensitive = value
        
        def get_card(self, value):
            """
            Gets the table's card object corresponding to the given value

            IN:
                value - your custom card object

            OUT:
                table's card object
            """
            if value not in self.cards:
                
                
                raise Exception("No card has the value {0!r}.".format(value))
            
            return self.cards[value]
        
        def set_faceup(self, card, faceup=True):
            """
            Sets the given card faceup/down and makes renpy redraw the table

            in:
                card - card
                faceup - True if we set it faceup, False otherwise
                    (Default: True)
            """
            self.get_card(card).faceup = faceup
            renpy.redraw(self, 0)
        
        def get_faceup(self, card):
            """
            Checks if the given card is faceup

            IN:
                card - card

            OUT:
                True if the card is set faceup, False otherwise
            """
            return self.get_card(card).faceup
        
        def set_rotate(self, card, rotation):
            """
            Sets the rotation of the given card and makes renpy redraw the table

            IN:
                card - card
                rotation - rotation for the card
            """
            _m1_zz_cardgames__Rotate(self.get_card(card), rotation)
            renpy.redraw(self, 0)
        
        def get_rotate(self, card):
            """
            Returns card rotation

            IN:
                card - card

            OUT:
                card's rotation
            """
            return self.get_card(card).rotate.rotate_limit()
        
        def add_marker(self, card, marker):
            """
            Adds marker on card and redraws the table

            IN:
                card - card
                marker - marker
            """
            self.get_card(card).markers.append(marker)
            renpy.redraw(self, 0)
        
        def remove_marker(self, card, marker):
            """
            Removes marker from card and redraws the table

            IN:
                card - card
                marker - marker
            """
            table_card = self.get_card(card)
            if marker in table_card.markers:
                table_card.markers.remove(marker)
                renpy.redraw(self, 0)
        
        def card(self, value, face, back=None):
            """
            Creates a card and adds it to the table's cards map

            IN:
                value - your custom card object
                face - is the card face up or face down
                back - the card's back
                    (Default: None)
            """
            self.cards[value] = _m1_zz_cardgames__Card(self, value, face, back)
        
        def stack(
            self,
            x,
            y,
            xoff=0,
            yoff=0,
            show=1024,
            base=None,
            click=False,
            drag=DRAG_NONE,
            drop=False,
            hover=False,
            hidden=False
        ):
            """
            Creates a stack and adds it to the table's stacks list

            IN:
                x - the x position for the stack
                y - the y position for the stack
                xoff - the offset x for the stack
                    (Default: 0)
                yoff - the offset y for the stack
                    (Default: 0)
                show - maximum cards to render
                    (Default: 1024)
                base - img for the stack's base
                    (Default: None)
                click - whether or not the user can click on the stack
                    (Default: False)
                drag - the drag mode for the stack
                    (Default: DRAG_NONE)
                drop - whether or not the user can drop cards on the stack
                    (Default: False)
                hover - whether or not we respond to user hovering mouse over the stack
                    (Default: False)
                hidden - whether or not we hide the stack
                    (Default: False)

            OUT:
                new stack object
            """
            rv = _m1_zz_cardgames__Stack(self, x, y, xoff, yoff, show, base, click, drag, drop, hover, hidden)
            
            self.stacks.append(rv)
            return rv
        
        def per_interact(self):
            """
            Forces redraw on each interaction
            """
            renpy.redraw(self, 0)
        
        def render(self, width, height, st, at):
            """
            Renders the table's stacks and cards that should be rendered
            """
            self.st = st
            
            rv = renpy.Render(width, height)
            
            for s in self.stacks:
                
                if s.hidden:
                    s.rect = None
                    for c in s.cards:
                        c.rect = None
                    continue
                
                s.render_to(rv, width, height, st, at)
                
                for c in s.cards:
                    c.render_to(rv, width, height, st, at)
            
            return rv
        
        def visit(self):
            """
            Returns a list of all displayable objects we use
            """
            stacks_bases = [stack.base for stack in self.stacks]
            cards_faces = [card.face for card in self.cards.itervalues()]
            cards_backs = [card.back for card in self.cards.itervalues()]
            
            return stacks_bases + cards_faces + cards_backs
        
        def event(self, ev, x, y, st):
            """
            Event handler
            This framework allows you to work with 5 event types
                each event has its own attributes (they share some of them):
                    'drag' - the user dragged 1 or more cards:
                        table
                        stack
                        card
                        drag_cards
                        drop_stack (can be None)
                        drop_card (can be None)
                        time
                    'click' and 'doubleclick' - the user
                        clicked somewhere:
                        table
                        stack
                        card (can be None)
                        time
                    'hover' and 'unhover' - the user started/ended
                        hovering mouse over card:
                        table
                        stack
                        card
                        time
                if the event doesn't have an attribute, it means the attribute is None

            OUT:
                list of events happened during this interaction
            """
            self.st = st
            
            if not self.sensitive:
                return
            
            
            evt_list = list()
            grabbed = renpy.display.focus.get_grab()
            
            if (grabbed is not None) and (grabbed is not self):
                return
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.click_stack:
                    return
                
                stack = None
                card = None
                
                for s in self.stacks:
                    
                    sx, sy, sw, sh = s.rect
                    if sx <= x and sy <= y and sx + sw > x and sy + sh > y:
                        stack = s
                    
                    
                    for c in s.cards[-s.show:]:
                        if c.rect is None:
                            continue
                        
                        cx, cy, cw, ch = c.rect
                        if cx <= x and cy <= y and cx + cw > x and cy + ch > y:
                            card = c
                            stack = c.stack
                
                if stack is None:
                    return
                
                
                renpy.display.focus.set_grab(self)
                
                
                if card is not None:
                    xoffset, yoffset = card._offset.offset()
                    if (xoffset or yoffset) and not card.hovered:
                        raise renpy.IgnoreEvent()
                
                
                self.stacks.remove(stack)
                self.stacks.append(stack)
                
                if stack.click or stack.drag:
                    self.click_card = card
                    self.click_stack = stack
                
                if (
                    card is None
                    or not self.can_drag(self, card.stack, card.value)
                ):
                    self.drag_cards = []
                
                elif card.stack.drag == DRAG_CARD:
                    self.drag_cards = [card]
                
                elif card.stack.drag == DRAG_ABOVE:
                    self.drag_cards = []
                    for c in card.stack.cards:
                        if c is card or self.drag_cards:
                            self.drag_cards.append(c)
                
                elif card.stack.drag == DRAG_STACK:
                    self.drag_cards = list(card.stack.cards)
                
                elif card.stack.drag == DRAG_TOP:
                    if card.stack.cards[-1] is card:
                        self.drag_cards = [card]
                    else:
                        self.drag_cards = []
                
                for c in self.drag_cards:
                    c._offset = _m1_zz_cardgames__Fixed(0, 0)
                
                self.click_x = x
                self.click_y = y
                self.dragging = False
                
                renpy.redraw(self, 0)
            
            
            
            if ev.type == pygame.MOUSEMOTION or (ev.type == pygame.MOUSEBUTTONUP and ev.button == 1):
                if abs(x - self.click_x) > 7 or abs(y - self.click_y) > 7:
                    self.dragging = True
                
                dx = x - self.click_x
                dy = y - self.click_y
                
                for c in self.drag_cards:
                    xoffset, yoffset = c._offset.offset()
                    
                    cdx = dx - xoffset
                    cdy = dy - yoffset
                    
                    c._offset = _m1_zz_cardgames__Fixed(dx, dy)
                    
                    if c.rect:
                        cx, cy, cw, ch = c.rect
                        cx += cdx
                        cy += cdy
                        c.rect = (cx, cy, cw, ch)
                
                
                dststack = None
                dstcard = None
                
                for s in self.stacks:
                    if not s.drop:
                        continue
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    if s.rect is not None:
                        sx, sy, sw, sh = s.rect
                        if sx <= x and sy <= y and sx + sw > x and sy + sh > y:
                            dststack = s
                    
                    for c in s.cards:
                        if c.rect is not None:
                            cx, cy, cw, ch = c.rect
                            if cx <= x and cy <= y and cx + cw > x and cy + ch > y:
                                dststack = s
                                dstcard = c
                                break
                    
                    if dststack is not None:
                        break
            
            
            
            
            
            
            
            
            
            
            if (
                ev.type == pygame.MOUSEMOTION
                or (
                    ev.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
                    and ev.button == 1
                )
            ):
                if not self.drag_cards:
                    for s in self.stacks:
                        if not s.hover:
                            continue
                        
                        for i, c in enumerate(s.cards):
                            if not c.rect:
                                continue
                            
                            c_x_min, c_y_min, c_w, c_h = c.rect
                            c_x_max = 0
                            c_y_max = 0
                            
                            if i == len(s.cards) - 1:
                                c_x_max = c_x_min + c_w
                                c_y_max = c_y_min + c_h
                            
                            
                            elif not s.xoff == 0 or not s.yoff == 0:
                                if abs(s.xoff) >= c_w:
                                    c_x_max = c_x_min + c_w
                                
                                else:
                                    if s.xoff > 0:
                                        c_x_max = c_x_min + s.xoff
                                    
                                    elif s.xoff < 0:
                                        c_x_max = c_x_min + c_w
                                        c_x_min = c_x_min + c_w + s.xoff
                                    
                                    else:
                                        c_x_max = c_x_min + c_w
                                
                                if abs(s.yoff) >= c_h:
                                    c_y_max = c_y_min + c_h
                                
                                else:
                                    if s.yoff > 0:
                                        c_y_max = c_y_min + s.yoff
                                    
                                    elif s.yoff < 0:
                                        c_y_max = c_y_min + c_h + s.yoff
                                        c_y_min = c_y_min + s.yoff
                                    
                                    else:
                                        c_y_max = c_y_min + c_h
                            
                            
                            if not c.hovered and c_x_min <= x < c_x_max and c_y_min <= y < c_y_max:
                                evt = CardEvent()
                                evt.type = "hover"
                                evt.table = self
                                evt.stack = s
                                evt.card = c.value
                                evt.time = st
                                c.hovered = True
                                evt_list.insert(0, evt)
                            
                            
                            elif c.hovered and (not c_x_min <= x < c_x_max or not c_y_min <= y < c_y_max):
                                evt = CardEvent()
                                evt.type = "unhover"
                                evt.table = self
                                evt.stack = s
                                evt.card = c.value
                                evt.time = st
                                c.hovered = False
                                evt_list.insert(0, evt)
            
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                
                renpy.display.focus.set_grab(None)
                
                evt = None
                
                if self.dragging:
                    if self.drag_cards:
                        for c in self.drag_cards:
                            if c.hovered:
                                evt = CardEvent()
                                evt.type = "unhover"
                                evt.table = self
                                evt.stack = self.click_stack
                                evt.card = c.value
                                evt.time = st
                                c.hovered = False
                                evt_list.append(evt)
                        
                        if evt is not None:
                            self.last_event = evt
                            evt = None
                        
                        if dststack is not None:
                            evt = CardEvent()
                            evt.type = "drag"
                            evt.table = self
                            evt.stack = self.click_stack
                            evt.card = self.click_card.value
                            evt.drag_cards = [c.value for c in self.drag_cards]
                            evt.drop_stack = dststack
                            if dstcard:
                                evt.drop_card = dstcard.value
                            evt.time = st
                
                else:
                    if self.click_stack is not None:
                        if self.click_stack.click:
                            evt = CardEvent()
                            evt.table = self
                            evt.stack = self.click_stack
                            if self.click_card:
                                evt.card = self.click_card.value
                            else:
                                evt.card = None
                            evt.time = st
                            
                            if (
                                self.last_event.type == "click"
                                and self.last_event.stack == evt.stack
                                and self.last_event.card == evt.card
                                and self.last_event.time + self.doubleclick > evt.time
                            ):
                                evt.type = "doubleclick"
                            else:
                                evt.type = "click"
                
                if evt is not None:
                    self.last_event = evt
                    evt_list.append(evt)
                
                for c in self.drag_cards:
                    c.springback()
                
                self.click_card = None
                self.click_stack = None
                self.drag_cards = []
            
            if evt_list:
                return evt_list
            
            else:
                return None


    class CardEvent(object):
        """
        Represents cards events
        PROPERTIES:
            type - the type of the event
            stack - the stack where the event started
            card - the card that triggered the event
            drag_cards - the cards we're dragging
            drop_stack - the stack we're dropping our cards on
            drop_card - the bottom card we're dropping
            time - the event time
        """
        
        def __init__(self):
            self.type = None
            self.stack = None
            self.card = None
            self.drag_cards = None
            self.drop_stack = None
            self.drop_card = None
            self.time = 0

    class _m1_zz_cardgames__Stack(object):
        """
        Represents a stack of one or more cards, which can be placed on the table.

        PROPERTIES:
            table - the table the stack belongs to
            x/y - coordinates of the center of the top card of the stack
            xoff/yoff - the offset in the x and y directions of each successive card
            show - the number of cards to render
            base - the image that is shown behind the stack
            click - whether or not we report click events on the stack
            drag - the drag mode for the stack
            drop - whether or not the user can drop cards on the stack
            hover - whether or not we report hover/unhover events for the stack
            hidden - whether or not we render the stack
            cards - the list of cards in the stack
            rect - the rectangle for the background
        """
        def __init__(
            self,
            table,
            x,
            y,
            xoff,
            yoff,
            show,
            base,
            click,
            drag,
            drop,
            hover,
            hidden
        ):
            """
            Constructor for a stack
            NOTE: since we define stacks via the table method,
                they don't have default parameters in the init method

            IN:
                table - the table of this stack
                x - x of the center of the top card
                y - y of the center of the top card
                xoff - x offset of each successive card
                yoff - y offset of each successive card
                show - maximum cards to render
                base - the image for the base of this stack
                click - whether or not we report the user's clicks
                drag - the drag mode for this stack
                drop - whether or not the user's can drop cards on this stack
                hover -  whether or not we report hover events for the stack
                hidden - whether or not we render the stack
            """
            self.table = table
            
            self.x = x
            self.y = y
            
            self.xoff = xoff
            self.yoff = yoff
            
            self.show = show
            
            
            if isinstance(base, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.base = MASFilterSwitch(base)
            
            elif isinstance(base, renpy.display.core.Displayable):
                self.base = base
            
            
            elif self.table.base is not None:
                self.base = self.table.base
            
            else:
                raise Exception(
                    "Ni la Pila {0} ni la Tabla {1} tienen imagen definida para la base de la pila.".format(self, self.table)
                )
            
            self.click = click
            self.drag = drag
            self.drop = drop
            self.hover = hover
            
            self.hidden = hidden
            
            self.cards = []
            
            self.rect = None
        
        def insert(self, index, card):
            """
            Inserts card in the stack at index

            IN:
                index - the index to insert the card at
                card - card to move
            """
            card = self.table.get_card(card)
            
            if card.stack:
                card.stack.cards.remove(card)
            
            card.stack = self
            self.cards.insert(index, card)
            
            self.table.stacks.remove(self)
            self.table.stacks.append(self)
            
            card.springback()
        
        def append(self, card):
            """
            Places card on the top of the stack

            IN:
                card - card to move
            """
            if card in self.cards:
                self.insert(len(self.cards) - 1, card)
            
            else:
                self.insert(len(self.cards), card)
        
        def remove(self, card):
            """
            Removes card from the stack
            NOTE: cards that don't have a stack won't be rendered!

            IN:
                card - card to remove
            """
            card = self.table.get_card(card)
            
            self.cards.remove(card)
            
            card.stack = None
            card.rect = None
        
        def index(self, card):
            """
            Returns card index in the stack

            IN:
                card - the card which index we're trying to find

            OUT:
                int as card index
                or None if no such card in the stack
            """
            card = self.table.get_card(card)
            
            try:
                id = self.cards.index(card)
            
            except ValueError:
                id = None
            
            return id
        
        def deal(self):
            """
            Removes the card at the top of the stack from the stack

            OUT:
                the card that was removed
                or None if the stack si empty
            """
            if not self.cards:
                return None
            
            card = self.cards[-1]
            self.remove(card.value)
            return card.value
        
        def shuffle(self):
            """
            Shuffles the cards in the stack
            """
            renpy.random.shuffle(self.cards)
            renpy.redraw(self.table, 0)
        
        def __repr__(self):
            return "<__Stack " + "{0!r}".format(self.cards).strip("[]") + ">"
        
        def __len__(self):
            return len(self.cards)
        
        def __getitem__(self, idx):
            if isinstance(idx, slice):
                return [card.value for card in self.cards[idx]]
            
            else:
                return self.cards[idx].value
        
        def __iter__(self):
            for i in self.cards:
                yield i.value
        
        def __contains__(self, card):
            return self.table.get_card(card) in self.cards
        
        def render_to(self, rv, width, height, st, at):
            """
            Blits the stack to the table's render
            """
            render = renpy.render(self.base, width, height, st, at)
            cw, ch = render.get_size()
            
            cx = self.x - cw / 2
            cy = self.y - ch / 2
            
            self.rect = (cx, cy, cw, ch)
            rv.blit(render, (cx, cy))

    class _m1_zz_cardgames__Card(object):
        """
        Represent a card for our table
        NOTE: THIS IS NOT THE CLASS FOR YOUR CARDS
        This is only for internal use only

        PROPERTIES:
            table - the table the card belongs to
            value - value of the card (your card object)
            face - the face for the card
            back - the back for the card
            faceup - whether or not this card is set face up
            rotate - an object for cards rotation
            markers - a list of marker that will be rendered over the card
            stack - the stack the card belongs to
            _offset - an object that gives the offset of this card relative to
                where it would normally be placed. THIS IS THE PRIVATE VARIANT FOR INTERNAL USE
            rect - the rectangle where this card was last drawn to the screen at
            hovered - whether or not the user hovered over this card
            positional_offset - the offsets which you can use to change the card positions (PUBLIC)
        """
        def __init__(self, table, value, face, back):
            """
            The constructor for a card
            NOTE: no default values since we use the table method for defining cards

            table - the table of this card
            value - your card object corresponding to this card
            face - the face of this card
            back - the back of this card
            """
            self.table = table
            
            self.value = value
            
            self.face = MASFilterSwitch(face)
            
            if isinstance(back, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.back = MASFilterSwitch(back)
            
            elif isinstance(back, renpy.display.core.Displayable):
                self.back = back
            
            elif self.table.back is not None:
                self.back = self.table.back
            
            else:
                raise Exception(
                    "Ni la Tarjeta {0} ni la Tabla {1} tienen imagen definida para el reverso de la tarjeta.".format(self, self.table)
                )
            
            self.faceup = True
            
            self.rotate = None
            
            self.markers = []
            
            self.stack = None
            
            self._offset = _m1_zz_cardgames__Fixed(0, 0)
            
            self.rect = None
            
            self.hovered = False
            
            self.positional_offset = (0, 0)
            
            _m1_zz_cardgames__Rotate(self, 0)
        
        def set_offset(self, x=0, y=0):
            """
            Sets ofsets for this card to x and y

            IN:
                x - x offset
                    (Default: 0)
                y - y offset
                    (Default: 0)
            """
            self.positional_offset = (x, y)
        
        def place(self):
            """
            Returns the base x and y placement of this card

            OUT:
                tuple with x and y coordinates of this card
            """
            s = self.stack
            offset = max(len(s.cards) - s.show, 0)
            index = max(s.cards.index(self) - offset, 0)
            
            x_pos_off, y_pos_off = self.positional_offset
            
            return (x_pos_off + s.x + s.xoff * index, y_pos_off + s.y + s.yoff * index)
        
        def springback(self):
            """
            Makes this card to springback
            """
            if self.rect is None:
                self._offset = _m1_zz_cardgames__Fixed(0, 0)
            else:
                self._offset = _m1_zz_cardgames__Springback(self)
        
        def render_to(self, rv, width, height, st, at):
            """
            Blits the card to the table's render
            """
            
            x, y = self.place()
            xoffset, yoffset = self._offset.offset()
            x += xoffset
            y += yoffset
            
            if self.faceup:
                d = self.face
            else:
                d = self.back
            
            
            
            if self.markers:
                d = Fixed(* ([d] + [renpy.easy.displayable(i) for i in self.markers]))
            
            r = self.rotate.rotate()
            if r:
                d = RotoZoom(r, r, 0, 1, 1, 0)(d)
            
            render = renpy.render(d, width, height, st, at)
            w, h = render.get_size()
            
            x -= w / 2
            y -= h / 2
            
            self.rect = (x, y, w, h)
            
            rv.blit(render, (x, y))
        
        def __repr__(self):
            return "<__Card {0!r}>".format(self.value)

    class _m1_zz_cardgames__Springback(object):
        
        def __init__(self, card):
            self.card = card
            self.table = table = card.table
            
            self.start = table.st
            
            cx, cy, cw, ch = self.card.rect
            x = cx + cw / 2
            y = cy + ch / 2
            
            self.startx = x
            self.starty = y
        
        def offset(self):
            
            t = (self.table.st - self.start) / self.table.springback
            t = min(t, 1.0)
            
            if t < 1.0:
                renpy.redraw(self.table, 0)
            
            px, py = self.card.place()
            
            return int((self.startx - px) * (1.0 - t)), int((self.starty - py) * (1.0 - t))

    class _m1_zz_cardgames__Fixed(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def offset(self):
            return self.x, self.y

    class _m1_zz_cardgames__Rotate(object):
        def __init__(self, card, amount):
            
            self.table = table = card.table
            self.start = table.st
            
            if card.rotate is None:
                self.start_rotate = amount
            else:
                self.start_rotate = card.rotate.rotate()
            
            self.end_rotate = amount
            
            card.rotate = self
        
        def rotate(self):
            
            if self.start_rotate == self.end_rotate:
                return self.start_rotate
            
            t = (self.table.st - self.start) / self.table.springback
            t = min(t, 1.0)
            
            if t < 1.0:
                renpy.redraw(self.table, 0)
            
            return self.start_rotate + (self.end_rotate - self.start_rotate) * t
        
        def rotate_limit(self):
            return self.end_rotate
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
