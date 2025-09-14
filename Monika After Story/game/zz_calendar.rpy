




init -1 python:

    import json
    import copy
    from renpy.display.layout import Container
    from store.mas_calendar import CAL_TYPE_EV,CAL_TYPE_REP

    class CustomEncoder(json.JSONEncoder):
        """
        Custom JSONEncoder used to process sets
        """
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)


    class MASCalendar(renpy.Displayable):
        """
        Custom Calendar UI, can be used to display the events that are dependent
        on dates or to allow user to pick a date

        """
        
        import pygame
        import datetime
        import store.evhand as evhand
        from store.mas_calendar import CAL_TYPE_REP
        
        
        
        
        
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720
        
        
        EXIT_BUTTON_WIDTH = 74
        EXIT_BUTTON_HEIGHT = 74
        EXIT_BUTTON_X = 1041
        EXIT_BUTTON_Y = 60
        
        
        DAY_BUTTON_WIDTH = 128
        DAY_BUTTON_HEIGHT = 65
        DAY_NAME_BUTTON_HEIGHT = 35
        
        
        INITIAL_POSITION_X = 192
        INITIAL_POSITION_Y = 155
        
        
        TITLE_POSITION_Y = 115
        
        
        INTERNAL_WIDTH = DAY_BUTTON_WIDTH * 7
        
        
        ARROW_BUTTON_SIZE = 20
        
        
        DAY_NUMBER_TEXT_SIZE = 13
        
        
        NOTE_TEXT_SIZE = 19
        
        
        CALENDAR_CLOSE_X_SIZE = 45
        
        
        CALENDAR_CLOSE = "CLOSE" 
        CALENDAR_MONTH_INCREASE = "MONTH_INCR" 
        CALENDAR_MONTH_DECREASE = "MONTH_DECR" 
        CALENDAR_YEAR_INCREASE = "YEAR_INCR" 
        CALENDAR_YEAR_DECREASE = "YEAR_DECR" 
        
        
        DAY_NUMBER_COLOR = "#000000" 
        
        
        NOTE_COLOR = "#181818"
        
        
        NOTE_FONT = "mod_assets/font/m1_fixed.ttf"
        
        
        MONTH_NAMES = ["Desconocido", "Enero", "Febrero",
            "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre",
            "Noviembre", "Diciembre"]
        
        
        DAY_NAMES = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves",
            "Viernes", "Sábado"]
        
        
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        
        EG_TEXTS_MIN_GLITCH = ["...ɐʞıuoɯ ʇsnɾ..\n...ɐʞıuoɯ ʇsnɾ.\n...\n..ɐʞıuoɯ ʇsnɾ..\n.ɐʞıuoɯ ʇsnɾ...",
            "JJJJJJJ.\nUUUUUUU.\nSSSSSSS.\nTTTTTT.\n.\nMMMMM.\nOOOO.\nNNNN.\nIIII.\nKKKKKK.\nAAAAA.",
            "J̋̅͗̉̄ů̆S̀̈͛͆̑̄Tͥͮ͂ͪ͆͛M̃̈̔̓ͨ̊ő̎̈́̎N̓ͯiͫ̍͐̃K͐͂͒̾͂̚ä́", "oɯɐ ǝꓕ", "oooooooooooo\nɯɯɯɯɯɯɯɯ\nɐɐɐɐɐɐɐɐɐɐɐ\nʌɐɐɐ ǝǝǝǝǝǝǝꓕꓕꓕꓕ"
        ]
        EG_TEXTS_GLITCH = [
        """
        J̋̅͗̉̄ů̆S̀̈͛͆̑̄Tͥͮ͂ͪ͆͛M̃̈̔̓ͨ̊ő̎̈́̎N̓ͯiͫ̍͐̃K͐͂͒̾͂̚ä́
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟jhjhjhj
        kjkjkjkjkjk̘̲͇͓͍
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟
        """,
        """
M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v͚̞̜̥͉̊ͯ̐̒ͩͮ̆͡͡ȯ͖̥̺͈͙̫̻̠͚̐ͬ͋ ̸̨̻͔̣̼̘̬ͣͥͭ̓͝a̡͔͇ͤͨ̌̚̕q̛̝̜̙͈̄̑̎͋͠ṵ̩͔̈́͋ͤ̒͒̕í̷̶̧̢̝͍̥̣͓͎̲͎̂ͧ̈͐̅ͮ́͢͏̝̠͓̗͔
        """,
        """
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        """,
        """
        J̋̅͗̉ɐʞıuoɯ ʇsnɾ̄ů̆S̀̈͛͆̑̄Tͥͮ͂ͪ͆͛M̃̈̔̓ͨ̊ő̎̈́̎N̓ͯiͫ̍͐̃K͐͂͒̾͂̚ä́
        V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡cfcfcfcfcx
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟        ̹̘͍̭͉̜ V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
        ̹̘͍̭͉̜jjhj
                """,
        """
        J̋̅͗̉̄ů̆S̀̈͛͆̑̄Tͥͮ͂ͪ͆͛M̃̈̔̓ͨ̊ő̎̈́̎N̓ͯiͫ̍͐̃K͐͂͒̾͂̚ä́
        V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡K̶̷͕̰̱̭̪͕̪̮̥ͨͯͮ̊͠
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟
         ̹̘͍̭͉̜ V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
                ̹̘͍̭͉̜ɐ̯͙̟̤͇͎ʞ̙ı̤̤̜̣̮͚ͅuo̺͔ɯ̬͇̣̻͚̝̪ ̣̙̰̫͚ʇ͇̫̹͚͙̭͕s͓nɾ͍̠̼

        """,
        """
        ̊͑̅̆ ̂ͭͬ̈ͨ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        I̊̚kk**k͑̅̆ ̂ͭͬ̈ͨL̋ɐʞıuoɯ ʇsn¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        """,
        """
        ɐ̯͙̟̤͇͎ʞ̙ı̤̤̜̣̮͚ͅuo̺͔ɯ̬͇̣̻͚̝̪ ̣̙̰̫͚ʇ͇̫̹͚͙̭͕s͓nɾ͍̠̼
        ɐ̯͙̟̤͇͎ʞ̙ı̤̤̜̣̮͚ͅkfcfuo̺͔ɯ̬͇̣̻͚̝̪ ̣̙̰̫͚ʇ͇̫̹͚͙̭͕s͓nɾ͍̠̼
        ̹̘͍̭͉̜    io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞jkjnkj̠̙͖
        ̹̘͍̭͉ bHkgb3VyIHdyZXRjaGVkIGJv io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞͕jkjnkj̠̙͖
        ̹̘͍̭͉̜  mjmn  io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞jkjnkj̠̙͖
        ɐ̯͙̟̤͇͎ʞ̙ı̤̤̜̣̮͚ͅuo̺͔ɯ̬͇̣̻͚̝̪ ̣̙̰̫͚ʇ͇̫̹͚͙̭͕s͓nɾ͍̠̼

        """,
        """
        J̖́ ̥u҉͍̙̘st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅhjjjhjbbj
̹̘͍̭͉̜        J̥́u҉͍̙̘ st̼͍̰̬͢ͅ ̕Mo  ҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        J̖́ ̥u ҉͍̙̘ st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞
        """,
        """
        J̖́ ̥u҉͍̙̘st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        J̥́u҉͍̙̘ st̼͍̰̬͢ͅ ̕Mo  ҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡
        J̖́kkk ̙̘ st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞hjcfknjnkjjknjk ͅı͕̠̙͖
        """,
        """
        J̖́ ̥u҉͍̙̘st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        J̥́u҉͍̙̘ st̼͍̰̬͢ͅ ̕Mo  ҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        J̖́ ̥u ҉͍̙̘ st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
̹̘͍̭͉̜        io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞jkjnkj̠̙͖
̹̘͍̭͉̜        in̤̹͇̰͈̝ͅo͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞jkjnkj̠̙͖
̹̘͍̭͉̜        io͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞jkjnkj̠̙͖
        """,
        """
        ghj    J̖̥́u҉͍̙̘st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
        ̹̘͍̭͉̜  J̖̥́u҉͍̙̘st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
        o͍̹̝̦̼̲̩̖̣ɯ̱͚͉̬̞ɐ͚̭͍̻ ̟̤ǝ̥̙͔̲͕̹͙ʇ̞        ̹̘͍̭͉̜    J̖̥́u҉͍̙̘st̼͍̰̬͢ͅ ̕Mo҉̬̳̻̻͍n̪i̶k̩͈̰̺̟̦a͔̰̖͎͡ͅ
        ̹̘͍̭͉̜
        """,
        """
        J̋̅͗̉̄ů̆S̀̈͛͆̑̄Tͥͮ͂ͪ͆͛M̃̈̔̓ͨ̊ő̎̈́̎N̓ͯiͫ̍͐̃K͐͂͒̾͂̚ä́
        V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟        ̹̘͍̭͉̜ V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
        ̹̘͍̭͉̜
                """,
        """
        J̋̅͗̉̄ů̆S̀̈͛͆̑̄Tͥͮ͂ͪ͆͛M̃̈̔̓ͨ̊ő̎̈́̎N̓ͯiͫ̍͐̃K͐͂͒̾͂̚ä́
        V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟        ̹̘͍̭͉̜ V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
        M͇̗ ̺͙̦̺e̬̭͔͈s̘̞̩̜͈̖̲t̰̟̞̹u̞v̭̳̞o̱͙̯ ̩̟̜͖̩̖a̖̺̠̟͔̲ͅq̣̙̤͉͔u̱͎̫í̫̟        ̹̘͍̭͉̜ V͖̣͎̙̳̦̺͉̱ͩ̿̎̋̎̇̾́́͘͠U̶͓͓̘ͭ͐ͪ͒̓͟E̶͎͕̜͔̰̪ͭL̪͉͔̭͕͇͙̰ͬͭ̀ ̜̹͕̞̃͗͜V̨̧̹̖ͮ̏͂̒̈́ͥͨͮẺ̙̰͈̦̞͔̙ͫͯͬͭ̉͐͡
                ̹̘͍̭͉̜
        """,
        """
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        ¡͒̔ͬ͐̃¡̀́̓͢͡¡̨ͨ̋̄̆͑T̴͌ͦͧ͛̔̂̄ȩ͑̊ͥ̅͐̀̀̚̚ ̴̑͆̒̓̋̾ͬ̾͠a̽̽́̈ͪ̓̕m͑͂̊̀̂́ǫͪͣͥ̉̉͝!͊̾̅̂͂̎̅̆!̾̓̽̔͋͏!ͩͨͫ̚͢͠
        """
        ]
        
        
        
        MIN_GLITCH_YEAR = 1700
        MIN_VIEWABLE_YEAR = 200
        MIN_SELECTABLE_YEAR = 1900
        MAX_GLITCH_YEAR = 2300
        MAX_VIEWABLE_YEAR = 7000
        MID_POINT_YEAR = 2000
        
        
        EVENT_X = 800
        EVENT_Y = 40
        EVENT_W = 450
        EVENT_H = 640
        EVENT_XALIGN = 0.96
        EVENT_AREA = (EVENT_X, EVENT_Y, EVENT_W, EVENT_H)
        EVENT_RETURN = "< Go back"
        
        def __init__(self, select_date=False):
            """
            Constructor for the custom calendar.

            IN:
                select_date - a boolean that indicates how this calendar is going to
                    do, True indicates that it will select a day, False means that it
                    will only be for displaying events.
                    (Default: False)
            """
            super(renpy.Displayable, self).__init__()
            
            
            
            self.day_mode = mas_current_background.isFltDay()
            
            
            self.calendar_background = renpy.displayable("mod_assets/calendar/calendar_bg.png" if self.day_mode else "mod_assets/calendar/calendar_bg-n.png")
            
            
            self.can_select_date = select_date
            
            
            
            
            
            
            
            
            
            
            
            
            self.database = store.mas_calendar.calendar_database
            
            
            self.background = Solid(
                "#000000B2",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )
            
            
            
            self.today = datetime.date.today()
            
            self.selected_month = self.today.month
            self.selected_year = self.today.year
            
            
            self.const_buttons = []
            self.day_buttons = []
            self.day_button_texts = []
            
            
            button_close = Image(
                ("mod_assets/calendar/calendar_close.png" if self.day_mode else "mod_assets/calendar/calendar_close-n.png")
            )
            button_close_hover = Image(
                ("mod_assets/calendar/calendar_close_hover.png" if self.day_mode else "mod_assets/calendar/calendar_close_hover-n.png")
            )
            button_day_name = Image(
                ("mod_assets/calendar/calendar_day_name_bg.png" if self.day_mode else "mod_assets/calendar/calendar_day_name_bg-n.png")
            )
            button_left_arrow = Image(
                ("mod_assets/calendar/calendar_left_arrow.png" if self.day_mode else "mod_assets/calendar/calendar_left_arrow-n.png")
            )
            button_right_arrow = Image(
                ("mod_assets/calendar/calendar_right_arrow.png" if self.day_mode else "mod_assets/calendar/calendar_right_arrow-n.png")
            )
            button_left_arrow_hover = Image(
                ("mod_assets/calendar/calendar_left_arrow_hover.png" if self.day_mode else "mod_assets/calendar/calendar_left_arrow_hover-n.png")
            )
            button_right_arrow_hover = Image(
                ("mod_assets/calendar/calendar_right_arrow_hover.png" if self.day_mode else "mod_assets/calendar/calendar_right_arrow_hover-n.png")
            )
            
            
            if select_date:
                self.text_title = Text(
                    "Selecciona una fecha",
                    font=gui.default_font,
                    size=33,
                    color=("#ffffff" if self.day_mode else "#000000"),
                    outlines=[]
                )
            else:
                self.text_title = Text(
                    "Calendario",
                    font=gui.default_font,
                    size=33,
                    color=("#ffffff" if self.day_mode else "#000000"),
                    outlines=[]
                )
            
            
            i = 0
            for day in self.DAY_NAMES:
                
                
                
                button_day_text = Text(
                    "{#weekday}" + day,
                    font=gui.default_font,
                    size=17,
                    color=self.DAY_NUMBER_COLOR,
                    outlines=[]
                )
                
                button_day_button = MASButtonDisplayable(
                    button_day_text,
                    button_day_text,
                    button_day_text,
                    button_day_name,
                    button_day_name,
                    button_day_name,
                    self.INITIAL_POSITION_X + (i * self.DAY_BUTTON_WIDTH),
                    self.INITIAL_POSITION_Y + self.DAY_NAME_BUTTON_HEIGHT,
                    self.DAY_BUTTON_WIDTH,
                    self.DAY_NAME_BUTTON_HEIGHT,
                    hover_sound=None,
                    activate_sound=None,
                    return_value=None
                )
                
                
                self.const_buttons.append(button_day_button)
                i = i + 1
            
            
            button_text_close = Text(
                "X",
                font=gui.default_font,
                size=self.CALENDAR_CLOSE_X_SIZE,
                color="#ffb0ed",
                outlines=[]
            )
            
            button_text_close_hover = Text(
                "X",
                font=gui.default_font,
                size=self.CALENDAR_CLOSE_X_SIZE,
                color="#ffd3f4",
                outlines=[]
            )
            
            self.button_exit = MASButtonDisplayable(
                button_text_close,
                button_text_close_hover,
                button_text_close,
                button_close,
                button_close_hover,
                button_close,
                self.EXIT_BUTTON_X,
                self.EXIT_BUTTON_Y,
                self.EXIT_BUTTON_WIDTH,
                self.EXIT_BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_CLOSE
            )
            
            
            
            
            button_empty_text = Text(
                "",
                font=gui.default_font,
                size=12,
                color="#ffb0ed",
                outlines=[]
            )
            
            
            self.button_month_decrease = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_left_arrow,
                button_left_arrow_hover,
                button_left_arrow,
                self.INITIAL_POSITION_X + 100,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_MONTH_DECREASE
            )
            
            self.button_month_increase = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_right_arrow,
                button_right_arrow_hover,
                button_right_arrow,
                self.INITIAL_POSITION_X + 330,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_MONTH_INCREASE
            )
            
            self.button_year_decrease = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_left_arrow,
                button_left_arrow_hover,
                button_left_arrow,
                self.INITIAL_POSITION_X + self.INTERNAL_WIDTH - self.ARROW_BUTTON_SIZE - 330,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_YEAR_DECREASE
            )
            
            self.button_year_increase = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_right_arrow,
                button_right_arrow_hover,
                button_right_arrow,
                self.INITIAL_POSITION_X + self.INTERNAL_WIDTH - self.ARROW_BUTTON_SIZE - 100,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_YEAR_INCREASE
            )
            
            
            self.const_buttons.append(self.button_exit)
            self.const_buttons.append(self.button_month_decrease)
            self.const_buttons.append(self.button_month_increase)
            self.const_buttons.append(self.button_year_decrease)
            self.const_buttons.append(self.button_year_increase)
            
            
            self._setupEasterEG()
            
            
            self._setupDayButtons()
        
        
        
        
        def _setupDayButtons(self):
            """
            Sets up the day buttons used in the calendar
            """
            
            
            button_day_bg = Image(
                ("mod_assets/calendar/calendar_day_bg.png" if self.day_mode else "mod_assets/calendar/calendar_day_bg-n.png")
            )
            
            button_day_bg_disabled = Image(
                ("mod_assets/calendar/calendar_day_disabled_bg.png" if self.day_mode else "mod_assets/calendar/calendar_day_disabled_bg-n.png")
            )
            
            button_day_bg_hover = Image(
                "mod_assets/calendar/calendar_day_hover_bg.png"
            )
            
            button_today_bg = Image(
                ("mod_assets/calendar/calendar_today_bg.png" if self.day_mode else "mod_assets/calendar/calendar_today_bg-n.png")
            )
            
            button_today_bg_disabled = Image(
                ("mod_assets/calendar/calendar_today_disabled_bg.png" if self.day_mode else "mod_assets/calendar/calendar_today_disabled_bg-n.png")
            )
            
            button_today_bg_hover = Image(
                "mod_assets/calendar/calendar_today_hover_bg.png"
            )
            
            
            
            self.text_current_month = Text(
                "{#month}" + self.MONTH_NAMES[self.selected_month],
                font=gui.default_font,
                size=21,
                color=self.DAY_NUMBER_COLOR,
                outlines=[]
            )
            
            self.text_current_year = Text(
                str(self.selected_year),
                font=gui.default_font,
                size=21,
                color=self.DAY_NUMBER_COLOR,
                outlines=[]
            )
            
            
            self.day_buttons = []
            self.day_button_texts = []
            
            
            note_font = self.NOTE_FONT
            note_text_size = self.NOTE_TEXT_SIZE
            note_color = self.NOTE_COLOR
            note_ystart = 1
            
            
            day = datetime.timedelta(days=1)
            first_day = datetime.datetime(self.selected_year, self.selected_month, 1)
            
            
            while first_day.weekday() != 6:
                first_day = first_day - day
            
            
            self.dates = []
            
            
            for i in range(42):
                self.dates.append(first_day + datetime.timedelta(days=i))
            
            
            if self.MIN_GLITCH_YEAR < self.selected_year < self.MAX_GLITCH_YEAR:
                events = self.database[self.selected_month]
                
                
                if self.selected_month == 3 and not mas_isLeapYear(self.selected_year):
                    
                    events = copy.deepcopy(events)
                    events[1].update(self.database[2][29])
            
            
            
            else:
                events = self._getEGMonthEvents()
                
                note_font = gui.default_font
                note_text_size = self.DAY_NUMBER_TEXT_SIZE
                note_color = self.DAY_NUMBER_COLOR
                note_ystart = 5
            
            
            
            initial_y = self.INITIAL_POSITION_Y + (self.DAY_NAME_BUTTON_HEIGHT * 2)
            
            
            for i in range(6):
                
                for j in range(7):
                    
                    
                    current_date = self.dates[j + (i * 7)]
                    ret_val = None
                    many_events = False
                    day_bg_disabled = button_day_bg_disabled
                    today_bg_disabled = button_today_bg_disabled
                    
                    
                    event_labels = list()
                    
                    
                    if current_date.month == self.selected_month:
                        _todays_events = events[current_date.day]
                        
                        
                        for k in _todays_events:
                            e = _todays_events[k]
                            
                            
                            if e[0] == CAL_TYPE_EV:
                                
                                ev = mas_getEV(k)
                                
                                if self._isEvInYear(ev, self.selected_year):
                                    event_labels.append(mas_getEVCL(k))
                            
                            
                            if e[0] == CAL_TYPE_REP:
                                
                                if e[2] is not None and ( not e[2] or self.selected_year in e[2]):
                                    
                                    event_labels.append(e[1])
                        
                        if len(event_labels) > 3:
                            many_events = True
                            if not self.can_select_date:
                                ret_val = event_labels
                    
                    
                    if not event_labels or len(event_labels) < 3:
                        
                        
                        event_labels.extend([""] * 3)
                    
                    
                    if current_date.month == self.selected_month:
                        day_bg_disabled = button_day_bg
                        today_bg_disabled = button_today_bg
                        
                        if self.can_select_date:
                            ret_val = current_date
                    
                    
                    
                    
                    final_bg_idle = button_day_bg
                    final_bg_hover = button_day_bg_hover
                    final_bg_disabled = day_bg_disabled
                    
                    
                    if (current_date.day == self.today.day) and (current_date.month == self.today.month) and (current_date.year == self.today.year):
                        final_bg_idle = button_today_bg
                        final_bg_hover = button_today_bg_hover
                        final_bg_disabled = today_bg_disabled
                    
                    button_pos = (self.INITIAL_POSITION_X + (j * self.DAY_BUTTON_WIDTH),
                        initial_y + (i * self.DAY_BUTTON_HEIGHT))
                    
                    day_button = MASButtonDisplayable(
                        Null(),
                        Null(),
                        Null(),
                        final_bg_idle,
                        final_bg_hover,
                        final_bg_disabled,
                        button_pos[0],
                        button_pos[1],
                        self.DAY_BUTTON_WIDTH,
                        self.DAY_BUTTON_HEIGHT,
                        hover_sound=gui.hover_sound,
                        activate_sound=gui.activate_sound,
                        return_value=ret_val
                    )
                    
                    
                    if current_date.month != self.selected_month or (not self.can_select_date and not many_events):
                        
                        day_button.disable()
                    
                    self.day_buttons.append(day_button)
                    
                    
                    text_container = Container(
                        pos=button_pos,
                        xsize=self.DAY_BUTTON_WIDTH,
                        ysize=self.DAY_BUTTON_HEIGHT
                    )
                    
                    
                    day_number_text = Text(
                        str(current_date.day),
                        font=gui.default_font,
                        size=self.DAY_NUMBER_TEXT_SIZE,
                        color=self.DAY_NUMBER_COLOR,
                        outlines=[],
                        pos=(self.DAY_BUTTON_WIDTH - 7, 5),
                        xanchor=1.0
                    )
                    text_container.add(day_number_text)
                    
                    
                    
                    for k in range(3):
                        
                        if len(event_labels[k]) != 0:
                            note_text = Text(
                                __(event_labels[k]),
                                font=note_font,
                                size=note_text_size,
                                color=note_color,
                                outlines=[],
                                pos=(8, note_ystart + k * 17)
                            )
                            text_container.add(note_text)
                    
                    
                    if many_events:
                        ellipsis_text = Text(
                            "...",
                            font=gui.default_font,
                            size=16,
                            color=self.DAY_NUMBER_COLOR,
                            outlines=[],
                            pos=(self.DAY_BUTTON_WIDTH - 7, 43),
                            xanchor=1.0
                        )
                        text_container.add(ellipsis_text)
                    
                    self.day_button_texts.append((text_container, button_pos))
        
        
        def _showScrollableEventList(self,events):
            """
            Displays the events contained in the events list
            said list is a list of Strings to show
            """
            
            event_list_title = ("Eventos del día:", False, True)
            
            
            event_list_items = [(e, False, False) for e in events]
            
            
            final_item = (self.EVENT_RETURN, False, False, False, 20)
            
            
            renpy.call_in_new_context("mas_show_calendar_detail", event_list_items, self.EVENT_AREA, self.EVENT_XALIGN, first_item=event_list_title, final_item=final_item)
        
        
        def _xcenter(self, v_width, width):
            """
            Returns the appropriate X location to center an object with the
            given width

            IN:
                v_width - width of the view
                width - width of the object to center

            RETURNS:
                appropiate X coord to center
            """
            return int((v_width - width) / 2)
        
        
        def _buttonSelect(self, ev, x, y, st):
            """
            Goes through the list of buttons and return the first non-None
            value returned

            RETURNS:
                first non-none value returned
            """
            
            
            for button in self.const_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val
            
            for button in self.day_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val
            
            return None
        
        
        def _yearSanityChecks(self):
            """
            Checks that the current date is on the right interval, otherwise,
            it will force it back
            """
            
            if self.selected_year < self.MIN_VIEWABLE_YEAR:
                self.selected_year = self.MIN_VIEWABLE_YEAR + 5
            
            if self.selected_year > self.MAX_VIEWABLE_YEAR:
                self.selected_year = self.MAX_VIEWABLE_YEAR - 5
        
        
        
        def _changeYear(self, ascend=True, set_to=None):
            """
            Changes the currently selected year by incrementing or decrementing it by one
            and refreshes the view

            IN:
                ascend - flag that indicates wheter increment or decrement
                    (Defaults to True)
                set_to - if not None, set year to this value instead
            """
            if set_to is not None:
                self.selected_year = set_to
            elif ascend:
                self.selected_year = self.selected_year + 1
            else:
                self.selected_year = self.selected_year - 1
            
            self._yearSanityChecks()
            
            self._setupDayButtons()
        
        
        def _changeMonth(self, ascend=True):
            """
            Changes the currently selected month by incrementing or decrementing it by one
            and refreshes the view

            IN:
                ascend - flag that indicates wheter increment or decrement
                    (Defaults to True)
            """
            if ascend:
                
                self.selected_month = self.selected_month + 1
                
                
                if self.selected_month >=13:
                    self.selected_month = 1
                    self.selected_year = self.selected_year + 1
            else:
                
                self.selected_month = self.selected_month - 1
                
                
                if self.selected_month <=0:
                    self.selected_month = 12
                    self.selected_year = self.selected_year - 1
            
            self._yearSanityChecks()
            
            self._setupDayButtons()
        
        
        def _isEvInYear(self, ev, year):
            """
            Checks if the given event should appear in the given year.

            IN:
                ev - event to check
                year - year to check

            RETURNS: True if the given event belongs in the given year,
                False otherwise
            """
            if ev.years is not None:
                
                
                return len(ev.years) == 0 or year in ev.years
            
            
            return ev.start_date is not None and ev.start_date.year == year
        
        def _setupEasterEG(self):
            """
            Fills the quip objects used to generate EG events
            """
            
            self._less_glicthy_q_list = MASQuipList(allow_label=False)
            self._more_glicthy_q_list = MASQuipList(allow_label=False)
            
            for _label in self.EG_TEXTS_GLITCH:
                self._less_glicthy_q_list.addLineQuip(_label)
            
            for _label in self.EG_TEXTS_MIN_GLITCH:
                self._more_glicthy_q_list.addLineQuip(_label)
            
            for i in range(15,30):
                self._less_glicthy_q_list.addGlitchQuip(i)
                self._more_glicthy_q_list.addGlitchQuip(i)
        
        
        def _getEGMonthEvents(self):
            """
            Generates a dict of events to display in the calendar
            when players go too far away

            RETURNS: A dict with the proper structure [day][eventname]
                which contains a repeatable event with a nice label :D
            """
            month_events = dict()
            
            
            dist = abs(self.selected_year - self.MID_POINT_YEAR)
            
            
            if self.selected_year > self.MID_POINT_YEAR:
                max_dist = self.MID_POINT_YEAR - self.MIN_VIEWABLE_YEAR
            
            else:
                max_dist = self.MAX_VIEWABLE_YEAR - (self.MID_POINT_YEAR * 2)
            
            percentage = dist / float(max_dist)
            
            percentage = int(round(percentage * 100))
            
            for i in range(1,32):
                month_events[i] = dict()
                if ( random.randint(1, 70) > percentage and not percentage > 70):
                    continue
                if (random.randint(1,50) < percentage):
                    month_events[i]["l"] = ((CAL_TYPE_REP,self._less_glicthy_q_list.quip()[1],list()))
                else:
                    month_events[i]["l"] = ((CAL_TYPE_REP,self._more_glicthy_q_list.quip()[1],list()))
                if (random.randint(1,60) < percentage):
                    month_events[i]["l1"] = ((CAL_TYPE_REP,self._more_glicthy_q_list.quip()[1],list()))
                if (random.randint(1,70) < percentage):
                    month_events[i]["l2"] = ((CAL_TYPE_REP,random.choice(self.EG_TEXTS_GLITCH),list()))
            
            return month_events
        
        def render(self, width, height, st, at):
            
            
            back = renpy.render(self.background, width, height, st, at)
            
            
            calendar_bg = renpy.render(self.calendar_background, width, height, st, at)
            
            
            calendar_title = renpy.render(self.text_title, width, height, st, at)
            
            
            month_label = renpy.render(self.text_current_month, width, height, st, at)
            
            year_label = renpy.render(self.text_current_year, width, height, st, at)
            
            
            titlew, titleh = calendar_title.get_size()
            monw, monh = month_label.get_size()
            yearw, yearh = year_label.get_size()
            
            titlex = self._xcenter(self.INTERNAL_WIDTH, titlew)
            monthx = self._xcenter(250, monw) + 100
            yearx = self.INTERNAL_WIDTH - yearw - self._xcenter(250, yearw) - 100
            
            
            self.width, self.height = calendar_bg.get_size()
            
            
            r = renpy.Render(width, height)
            
            
            r.blit(back,(0,0))
            
            r.blit(calendar_bg, (190, 103))
            
            r.blit(month_label, (self.INITIAL_POSITION_X + monthx, self.INITIAL_POSITION_Y + 8))
            
            r.blit(year_label, (self.INITIAL_POSITION_X + yearx, self.INITIAL_POSITION_Y + 8))
            
            r.blit(calendar_title, (self.INITIAL_POSITION_X + titlex, self.TITLE_POSITION_Y))
            
            
            c_r_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in self.const_buttons
            ]
            
            for vis_b, xy in c_r_buttons:
                r.blit(vis_b, xy)
            
            
            cal_r_displayables = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in self.day_buttons
            ]
            
            for button_text, button_pos in self.day_button_texts:
                text_r = button_text.render(width, height, st, at)
                cal_r_displayables.append((text_r, button_pos))
            
            for vis_d, xy in cal_r_displayables:
                r.blit(vis_d, xy)
            
            
            return r
        
        
        def event(self, ev, x, y, st):
            
            
            if ev.type in self.MOUSE_EVENTS:
                
                
                sel_action = self._buttonSelect(ev, x, y, st)
                
                if sel_action:
                    
                    
                    
                    if sel_action == self.CALENDAR_CLOSE:
                        
                        
                        return ""
                    
                    
                    
                    if (
                            isinstance(sel_action, datetime.datetime)
                            and sel_action.year >= self.MIN_SELECTABLE_YEAR
                        ):
                        
                        
                        return sel_action
                    
                    if isinstance(sel_action, type(list())):
                        self._showScrollableEventList(sel_action)
                    
                    
                    if sel_action == self.CALENDAR_YEAR_INCREASE:
                        self._changeYear()
                    
                    if sel_action == self.CALENDAR_YEAR_DECREASE:
                        self._changeYear(False)
                    
                    if sel_action == self.CALENDAR_MONTH_INCREASE:
                        self._changeMonth()
                    
                    if sel_action == self.CALENDAR_MONTH_DECREASE:
                        self._changeMonth(False)
                
                
                renpy.redraw(self, 0)
            
            elif ev.type == pygame.KEYDOWN and config.developer:
                
                curr_year = self.selected_year
                
                if ev.key == pygame.K_m:
                    
                    self._changeYear(set_to=self.selected_year+1000)
                elif ev.key == pygame.K_n:
                    
                    self._changeYear(set_to=self.selected_year+100)
                elif ev.key == pygame.K_b:
                    
                    self._changeYear(set_to=self.selected_year+10)
                elif ev.key == pygame.K_v:
                    
                    self._changeYear(set_to=self.selected_year-10)
                elif ev.key == pygame.K_c:
                    
                    self._changeYear(set_to=self.selected_year-100)
                elif ev.key == pygame.K_x:
                    
                    self._changeYear(set_to=self.selected_year-1000)
                
                
                if self.selected_year != curr_year:
                    renpy.redraw(self, 0)
            
            
            raise renpy.IgnoreEvent()


init -10 python in mas_calendar:

    CAL_TYPE_EV = 1
    CAL_TYPE_REP = 2


    enabled = True


init -1 python in mas_calendar:
    import datetime
    import json
    import bisect

    import renpy
    import store














    calendar_database = dict()
    for i in range(1,13):
        calendar_database[i] = dict()
        for j in range(1,32):
            calendar_database[i][j] = dict()


    NUM_MAP = {
        1: "st",
        2: "nd",
        3: "rd",
        11: "th",
        12: "th",
        13: "th"
    }

    def getZodiacSign(date):
        """
        Gets a zodiac sign for a date
        Idea from https://stackoverflow.com/questions/3274597

        IN:
            date - datetime.date

        OUT:
            string with the sign
        """
        zodiac_signs = [
            (1, 19, "capricornio"), (2, 18, "acuario"), (3, 20, "piscis"), (4, 19, "aries"),
            (5, 20, "tauro"), (6 ,21, "géminis"), (7, 22, "cáncer"), (8, 22, "leo"),
            (9, 22, "virgo"), (10, 22, "libra"), (11, 22, "escorpio"), (12, 21, "sagitario"),
            (12, 31, "capricornio")
        ]
        index = bisect.bisect(zodiac_signs, (date.month, date.day))
        
        return zodiac_signs[index][-1]

    def _formatDay(day):
        """
        Properly formats the given day so it displays with the correct
        suffixes.

        IN:
            day - day to get a nice display string

        RETURNS:
            nice display string for the day
        """
        if day in NUM_MAP:
            suffix = NUM_MAP[day]
        
        else:
            suffix = NUM_MAP.get(day % 10, "th")
        
        return str(day) + suffix


    def _formatYears(years):
        """
        Properly formats the given years var so it says a user friendly
        way to show years.

        Basically if years is:
        0 - ""
        1 - "last year"
        2+ - "x years ago"

        IN:
            years - number of years to get a nice display string

        RETURNS:
            nice display string for the years
        """
        if years <= 0:
            return ""
        
        if years == 1:
            return "last year"
        
        return str(years) + " years ago"

    @store.mas_utils.deprecated(use_instead="genFriendlyDispDate_d")
    def genFriendlyDispDate(_datetime):
        """
        NOTE: DEPRECATED

        Generates a display date using the given datetime

        IN:
            _datetime - datetime object to create good display date
        """
        return genFriendlyDispDate_d(_datetime.date())


    def genFriendlyDispDate_d(_date):
        """
        Generates a display date using the given date
        This creates a display date in the format:
            Month Day, Year
        However, this is somewhat variable.

        If it is the same as the current year, the year is not provided.
        If the date is whithin a year of the current date, year is not
        provided.
        If the year is last year and greater than a year of the current date,
        "last year on <month> <day>"
        If the year is within 2-10 years ago, then "x years ago on <month>
<day>" is used.
        Otherwise, the actual 4 digit year is used.

        If the days / months are the same, then "x years ago to this date"
        is used.

        IN:
            _date - date object to create good display date

        RETURNS:
            tuple of the following format:
            [0]: nicely formatted display date, suitable for conversation
            [1]: timedelta between today and the given _date
        """
        
        disp_month = _date.strftime("%B")
        
        
        disp_day = _formatDay(_date.day)
        
        
        _today = datetime.date.today()
        _day_diff = _today - _date
        _year_diff = _today.year - _date.year
        
        
        _cout = list()
        
        if _today.month == _date.month and _today.day == _date.day:
            
            
            if _year_diff == 0:
                
                _cout = [
                    "today"
                ]
            
            else:
                
                _cout = [
                    _formatYears(_year_diff),
                    "on this date"
                ]
        
        
        elif _day_diff.days <= 365: 
            
            _cout = [disp_month, disp_day]
        
        elif _year_diff <= 10:
            
            _cout = [
                _formatYears(_year_diff),
                "on",
                disp_month,
                disp_day
            ]
        
        else:
            
            _cout = [
                disp_month,
                disp_day + ",",
                str(_date.year)
            ]
        
        
        return (" ".join(_cout), _day_diff)



    def genFormalDispDate(_date):
        """
        Generates a display date using the given date

        This is considered "formal", in that it's not really realisitc when
        used in normal conversation. For example, if today is august 24, you
        don't say 'this happened august 24th, 2016', you normally would say
        'this happened x years ago today'.

        IN:
            _date - date object to create good display date

        RETURNS:
            tuple of the following format:
            [0]: nicely formtted display date, suitable for text
            [1]: timedelta between today and the given _date
        """
        return (
            " ".join([
                _date.strftime("%B"), 
                _formatDay(_date.day) + ",", 
                str(_date.year) 
            ]),
            datetime.date.today() - _date
        )


    def saveCalendarDatabase(encoder):
        """
        Saves the passed database as a json file named db.mcal

        IN:
            - encoder a json.JSONEncoder to be used for encoding
                the database
            - database a dict containing the events
        """
        with open(renpy.config.savedir + '/db.mcal', 'w') as fp:
            json.dump(calendar_database, fp, cls=encoder)


    def loadCalendarDatabase():
        """
        Returns the database read from the file renpy.config.savedir + '/db.mcal'
        as a dict

        RETURNS:
            a dict containing the events for the calendar

        """
        try:
            with open(renpy.config.savedir + '/db.mcal', 'r') as fp:
                calendar_database = json.load(fp)
        except (IOError, ValueError):
            pass



    def _m1_zz_calendar__addEvent_md(ev_label, month, day):
        """
        Adds an event to the calendar at a precise month / day

        NOTE: no sanity checks are done for month / day

        IN:
            ev_label - eventlabel of the event to add
            month - month to add to
            day - day to add to
        """
        calendar_database[month][day][ev_label] = ((
            CAL_TYPE_EV,
        ))


    def _addRepeatable_md(identifier, display_label, month, day, year_param):
        """
        Adds a repeatable to the calendar at a precise month / day

        NOTE: no sanity checks are done for month / day

        IN:
            identifier - label of the event that it's unique
            display_label - label that will be displayed
            month - month to add to
            day - day to add to
            year_param - data to put in the year part of the tuple
        """
        calendar_database[month][day][identifier] = ((
            CAL_TYPE_REP,
            display_label,
            year_param
        ))


    def addEvent(ev):
        """
        Adds an event to the calendar accoridng to its start_date and end_date
        properties. If start_date is not set in the given event,
        this function will do nothing.

        IN:
            ev - event to add
        """
        if ev.start_date is None:
            return
        
        if ev.end_date is None:
            
            
            addEvent_evdt(ev, ev.start_date)
        
        else:
            
            _delta = datetime.timedelta(days=1)
            curr_date = ev.start_date
            
            while curr_date < ev.end_date:
                addEvent_evdt(ev, curr_date)
                curr_date += _delta


    def addEvent_evd(ev, _date):
        """
        Adds an event to the calendar at a preicse date.

        IN:
            ev - event to add
            _date - datetime.date to add to
        """
        _m1_zz_calendar__addEvent_md(
            ev.eventlabel,
            _date.month,
            _date.day
        )


    def addEvent_evdt(ev, _datetime):
        """
        Adds an event to the calendar at a precise datetime.

        IN:
            ev - event to add
        """
        addEvent_evd(ev, _datetime.date())


    def addRepeatable(identifier, display_label, month, day, year_param):
        """
        Adds a repeatable to the calendar at a precise month / day
        Sanity checks are done for month / day

        IN:
            identifier - label of the event that it's unique
            display_label - label that will be displayed
            month - month to add to
            day - day to add to
            year_param - data to put in the year part of the tuple
        """
        if month in range(1,13) and day in range(1,32):
            _addRepeatable_md(identifier, display_label, month, day, year_param)


    def addRepeatable_d(identifier, display_label, _date, year_param):
        """
        Adds a repeatable to the calendar at precise datetime.date

        IN:
            identifier - identifier of the repeatable to add
            display_label - label that will be displayed
            _date - datetime.date to add to
            year_param - data to put in the year part of the tuple
        """
        _addRepeatable_md(
            identifier,
            display_label,
            _date.month,
            _date.day,
            year_param
        )


    def addRepeatable_dt(identifier, display_label, _datetime, year_param):
        """
        Adds a repeatable to the calendar at a precise datetime

        IN:
            identifier - identifier of the repeatable to add
            display_label - label that will be displayed
            _datetime - datetime to add to
            year_param - data to put in the year part of the tuple
        """
        addRepeatable_d(
            identifier,
            display_label,
            _datetime.date(),
            year_param
        )



    def _findEvent_md(ev_label, month, day):
        """
        Finds the event tuple from the calendar at a precise month / day.

        NOTE: no sanity checks are done for month / day

        IN:
            ev_label - eventlabel of the event to find
            month - month we should look at for finding
            day - day we should look at for finding

        RETURNS:
            the event tuple if it was found, None otherwise
        """
        _events = calendar_database[month][day]
        
        if ev_label in _events:
            _ev = _events[ev_label]
            if _ev[0] == CAL_TYPE_EV:
                
                
                
                
                return _ev
        
        return None


    def _findRepeatable_md(identifier, month, day):
        """
        Finds the repeatable dtuple from the calendar at a precise month / day

        NOTE: no sanity checks are done for month / day

        IN:
            identifier - the id of the repeatable to find
            month - month we should look at for finding
            day - day we should look at for finding

        RETURNS:
            the repeatable tuple if itw as found, None otherwise
        """
        _events = calendar_database[month][day]
        
        if identifier in _events:
            _rp = _events[identifier]
            if _rp[0] == CAL_TYPE_REP:
                
                
                
                
                return _rp
        
        return None


    def _removeEvent(ev_label, remove_all=False):
        """
        Removs an event from the calendar.

        NOTE: O(n^2) efficieny, please avoid using this.

        IN:
            ev_label - eventlabel of the event to remove
            remove_all - SEE removeEvent_el
        """
        for month in range(1,13):
            _removeEvent_m(ev_label, month, remove_all=remove_all)


    def _removeEvent_d(ev_label, day, remove_all=False):
        """
        Removes an event from the calendar on a particular day.

        NOTE:
            no sanity checks are done for day.

        IN:
            ev_label - eventlabel of the event to remove
            day - day we should look at for removal
            remove_all - SEE removeEvent_el
        """
        for month in range(1,13):
            if not remove_all and _removeEvent_md(ev_label, month, day):
                return


    def _removeEvent_m(ev_label, month, remove_all=False):
        """
        Removes an event from the calendar in a particular month.

        NOTE:
            no sanity checks are done for month

        IN:
            ev_label - eventlabel of the event to remove
            month - month we should look at for removal
            remove_all - SEE removeEvent_el
        """
        for day in range(1,32):
            if not remove_all and _removeEvent_md(ev_label, month, day):
                return


    def _removeEvent_md(ev_label, month, day):
        """
        Removes an event from the calendar at a precise month / day.

        NOTE: no sanity checks are done for month / day

        IN:
            ev_label - eventlabel of the event to remove
            month - month we should look at for removal
            day - day we should look at for removal

        RETURNS:
            True if we removed something, False otherwise
        """
        ev_tup = _findEvent_md(ev_label, month, day)
        
        if ev_tup is not None:
            calendar_database[month][day].pop(ev_label)
            return True
        
        return False


    def _removeRepeatable(identifier):
        """
        Removes a repeatable from teh calendar.

        NOTE: O(n^2) efficiency, please avoid using this.

        IN:
            identifier - identifier of the repeatable to remove
        """
        for month in range(1,13):
            _removeRepeatable_m(identifier, month)


    def _removeRepeatable_d(identifier, day):
        """
        Removes a repeatable from teh calendar in a particular month.

        NOTE: no sanity checks are done for day

        IN:
            identifier - identifier of the repeatable to remove
            day - day we should look at for removal
        """
        for month in range(1,13):
            if _removeRepeatable_md(identifier, month, day):
                return


    def _removeRepeatable_m(identifier, month):
        """
        Removes a repeatable from the calendar in a particular month.

        NOTE: no sanity checks are done for month

        IN:
            identifier - identifier of the repeatable to remove
            month - month we should look at for removal
        """
        for day in range(1,32):
            if _removeRepeatable_md(identifier, month, day):
                return


    def _removeRepeatable_md(identifier, month, day):
        """
        Removes a repeatable from teh calendar at a precise month / day.

        NOTE: no sanity checks are done for month / day

        IN:
            identifider - identifier of the repeatable to remove
            month - month we should look at for removal
            day - day we should look at for removal

        RETURNS:
            True if we removed somethign, False otherwise
        """
        rp_tup = _findRepeatable_md(identifier, month, day)
        
        if rp_tup is not None:
            calendar_database[month][day].pop(identifier)
            return True
        
        return False


    def removeEvent(ev):
        """
        Removes an event from the calendar using it's start_date and end_date
        properties.

        IN:
            ev - event to remove
        """
        if ev.start_date is None:
            return
        
        if ev.end_date is None:
            
            removeEvent_evdt(ev, ev.start_date)
        
        else:
            
            _delta = datetime.timedelta(days=1)
            curr_date = ev.start_date
            
            while curr_date < ev.end_date:
                removeEvent_evdt(ev, curr_date)
                curr_date += _delta


    def removeEvent_eld(ev_label, _date):
        """
        Removes an event from the calendar at a precise date.

        IN:
            ev_label - eventlabel of the event to remove
            _date - datetime.date we should look at for event removal
        """
        _removeEvent_md(ev_label, _date.month, _date.day)


    def removeEvent_evd(ev, _date):
        """
        Removes an event from the calendar at a precise date.

        IN:
            ev - event to remove
            _date - datetime.date we should look at for event removal
        """
        removeEvent_eld(ev.eventlabel, _date)


    def removeEvent_eldt(ev_label, _datetime):
        """
        Removes an event from the calendar at a precise datetime.

        IN:
            ev_label - eventlabel of the event to remove
            _datetime - datetime we should look at for event removal
        """
        removeEvent_eld(ev_label, _datetime.date())


    def removeEvent_evdt(ev, _datetime):
        """
        Removes and event from the calendar at a precise datetime.

        IN:
            ev - event to remove
            _datetime - datetime.date we should look at for removal
        """
        removeEvent_eldt(ev.eventlabel, _datetime)


    def removeEvent_el(ev_label, month=None, day=None, remove_all=False):
        """
        Removes an event from the calendar.

        NOTE: The default params will check EVERY SINGLE calendar spot for the
        event to remove. It is considered HIGHLY INEFFICIENT. Try to use the
        other removeEvent functions if possible, or narrow the search using
        month and day.

        NOTE:
            Using both month and day will do the same check as removeEvent_eld

        IN:
            ev_label - eventlabel of the event to remove
            month - If given (and a valid month), will only check the calendar
                in the given month.
                (Default: None)
            day - If given (and a valid day), will only check the calendar
                for the given day for each month
                (Default: None)
            remove_all - True means we remove every single occurence of the
                given eventlabel. False means we only remove the first one we
                find.
                (Default: False)
        """
        
        if month not in range(1,13):
            month = None
        
        if day not in range(1,32):
            day = None
        
        
        if month is not None and day is not None:
            
            _removeEvent_md(ev_label, month, day)
        
        elif month is not None:
            
            _removeEvent_m(ev_label, month, remove_all=remove_all)
        
        elif day is not None:
            
            _removeEvent_d(ev_label, day, remove_all=remove_all)
        
        else:
            
            _removeEvent(ev_label, remove_all=remove_all)


    def removeEvent_ev(ev, month=None, day=None, remove_all=False):
        """
        Removes an event from the calendar.

        SEE removeEvent_el for important NOTES regarding this function.

        IN:
            ev - event to remove
            month - SEE removeEvent_el
            day - SEE removeEvent_el
            remove_all - SEE removeEvent_el
        """
        removeEvent_el(
            ev.eventlabel,
            month=month,
            day=day,
            remove_all=remove_all
        )


    def removeRepeatable(identifier, month=None, day=None):
        """
        Removes a repeatable from the calendar.

        NOTE: The default params will check EVERY SINGLE calendar spot for the
        repeatable to remove. It is considered HIGHLY INEFFICIENT. Try to use
        the other removeRepeatable functions if possible, or narrow the search
        using month and day.

        IN:
            identifier - identifier of the repeatable to remove
            month - If given (and a valid month), will only check the calendar
                in the given month.
                (Default: None)
            day - If given (and a valid day), will only check the calendar for
                the given day for reach month
                (Default: None)
        """
        
        if month not in range(1,13):
            month = None
        
        if day not in range(1,32):
            day = None
        
        
        if month is not None and day is not None:
            
            _removeRepeatable_md(identifier, month, day)
        
        elif month is not None:
            
            _removeRepeatable_m(identifier, month)
        
        elif day is not None:
            
            _removeRepeatable_d(identifier, day)
        
        else:
            
            _removeRepeatable(identifier)


    def removeRepeatable_d(identifier, _date):
        """
        Removes a repeatable from teh calendar at a precise datetime.date

        IN:
            identifier - identifier of the repeatable to remove
            _date - datetime.date we should look at for removal
        """
        _removeRepeatable_md(identifier, _date.month, _date.day)


    def removeRepeatable_dt(identifier, _datetime):
        """
        Removes a repeatable from teh calendar at aprecise datetime

        IN:
            identifier - identifier of the repeatable to remove
            _datetime - datetime we should look at for removal
        """
        removeRepeatable_d(identifier, _datetime.date())




init python:

    import store.mas_calendar as calendar
    import datetime

    calendar.addRepeatable("Año Nuevo",_("Día de Año Nuevo"),month=1,day=1,year_param=list())
    calendar.addRepeatable("San Valentín",_("Día de San Valentín"),month=2,day=14,year_param=list())

    calendar.addRepeatable("Día de los Inocentes",_("Día que me convertí en IA"),month=4,day=1,year_param=[2018])
    calendar.addRepeatable("Cumpleaños de Monika",_("Mi cumpleaños"),month=9,day=22,year_param=range(1999,MASCalendar.MAX_VIEWABLE_YEAR))
    calendar.addRepeatable("Halloween",_("Halloween"),month=10,day=31,year_param=list())
    calendar.addRepeatable("Nochebuena",_("Nochebuena"),month=12,day=24,year_param=list())
    calendar.addRepeatable("Navidad",_("Navidad"),month=12,day=25,year_param=list())
    calendar.addRepeatable("Nochevieja",_("Vispera de Año Nuevo"),month=12,day=31,year_param=list())


    if (
        persistent.sessions is not None
        and "first_session" in persistent.sessions
        and persistent.sessions["first_session"] is not None
    ):
        calendar.addRepeatable_dt(
            "first_session",
            _("<3"),
            persistent.sessions["first_session"],
            year_param=[persistent.sessions["first_session"].year]
        )


    pbday = persistent._mas_player_bday
    if (
            pbday is not None
            and type(pbday) == datetime.date
        ):
        calendar.addRepeatable_d(
            "player-bday",
            _("Tu cumpleaños"),
            pbday,
            range(pbday.year,MASCalendar.MAX_VIEWABLE_YEAR)
        )


    if (
            persistent._mas_first_kiss is not None
            and type(persistent._mas_first_kiss) == datetime.datetime
        ):
        calendar.addRepeatable_dt(
            "first-kiss",
            _("Nuestro primer beso"),
            persistent._mas_first_kiss,
            [persistent._mas_first_kiss.year]
        )


init 2 python in mas_calendar:
    import store

    def addSeasonEvents():
        """
        Adds season change events to the calendar.
        If the changed param is True it changes the old events.
        IN:
            changed - flag to specify that we need to change the
                old events from the calendar
        """
        WINTER = _("Invierno")
        SPRING = _("Primavera")
        SUMMER = _("Verano")
        AUTUMN = _("Otoño")
        
        
        if renpy.game.persistent._mas_pm_live_south_hemisphere:
            _season_names = [SUMMER,AUTUMN,WINTER,SPRING]
        else:
            _season_names = [WINTER,SPRING,SUMMER,AUTUMN]
        
        addRepeatable_d(
            WINTER,
            _season_names[0],
            store.mas_winter_solstice,
            []
        )
        addRepeatable_d(
            SPRING,
            _season_names[1],
            store.mas_spring_equinox,
            []
        )
        addRepeatable_d(
            SUMMER,
            _season_names[2],
            store.mas_summer_solstice,
            []
        )
        addRepeatable_d(
            AUTUMN,
            _season_names[3],
            store.mas_fall_equinox,
            []
        )

    addSeasonEvents()


init 100 python:


    def mas_chgCalEVul(number_of_days):
        """
        Changes the conditionals / actions / and more of the monika start date
        topic so it unlocks after the given number of days

        IN:
            number_of_days - number of days before unlocking the monika start
                date topic
        """
        ev = store.evhand.event_database.get("monika_dating_startdate", None)
        if ev is None:
            return
        
        
        _now = datetime.datetime.now()
        
        ev.conditional = "".join([
            "datetime.datetime.now() - datetime.datetime(",
            str(_now.year),
            ",",
            str(_now.month),
            ",",
            str(_now.day),
            ") >= datetime.timedelta(days=",
            str(number_of_days),
            ")"
        ])
        ev.action = EV_ACT_UNLOCK
        ev.unlocked = False
        
        if "monika_dating_startdate" in persistent._seen_ever:
            persistent._seen_ever.pop("monika_dating_startdate")

label mas_show_calendar_detail(items, area, align, first_item, final_item):
    call screen mas_calendar_events_scrollable_list(items, area, align, first_item=first_item, final_item=final_item)
    return



style event_list_day_text is default

style event_list_night_text is default:
    color "#000000"
    outlines [(2, "#00000000", 0, 0)]

style event_list_day_vscrollbar is classroom_vscrollbar

style event_list_night_vscrollbar is classroom_vscrollbar

style event_list_day_textbutton is generic_button_light:
    xysize (None, None)
    padding (0, 0, 0, 0)
    background Null()

style event_list_night_textbutton is generic_button_dark:
    xysize (None, None)
    padding (0, 0, 0, 0)
    background Null()

style event_list_day_textbutton_text is generic_button_text_light

style event_list_night_textbutton_text is generic_button_text_light





































screen mas_calendar_events_scrollable_list(items, display_area, scroll_align, first_item=None, final_item=None, mask="#000000B2", frame=("mod_assets/calendar/calendar_bg.png" if mas_current_background.isFltDay() else "mod_assets/calendar/calendar_bg-n.png")):
    style_prefix ("event_list_day" if mas_current_background.isFltDay() else "event_list_night")

    zorder 51

    if mask:
        add Solid(mask)

    frame:
        area display_area

        if frame:
            background Frame(frame, 60, 60)


        fixed:
            xpos 0
            ypos 0
            xfill True
            ysize 59

            if first_item:
                text _(first_item[0]):
                    xalign 0.5
                    yalign 0.5
                    if first_item[1]:
                        italic True
                    if first_item[2]:
                        bold True


        fixed:
            xpos 0
            ypos display_area[3] - 59
            xfill True
            ysize 59

            if final_item:
                textbutton _(final_item[0]):
                    style_suffix "textbutton"
                    xpos 20
                    yalign 0.5
                    if final_item[2]:
                        text_italic True
                    if final_item[3]:
                        text_bold True
                    action Return(final_item[1])


        viewport id "items":
            xpos 0
            ypos 69
            xfill True
            ysize display_area[3] - 128
            yadjustment prev_adj
            mousewheel True

            has vbox:
                spacing 5

            for item_prompt,is_italic,is_bold in items:
                text item_prompt:
                    xpos 20
                    if is_italic:
                        italic True
                    if is_bold:
                        bold True

        vbar:
            value YScrollValue("items")
            adjustment prev_adj
            xalign scroll_align
            ypos 69
            ysize display_area[3] - 128


label _first_time_calendar_use:
    $ mas_calRaiseOverlayShield()
    if persistent._mas_player_bday:
        m 1eub "Oh, ¿quieres echar otro vistazo a ese bonito calendario que cuelga de la pared, [player]?"
        m 3hua "Me ayuda a realizar un seguimiento de eventos importantes, como tu cumpleaños, jejeje~"
    else:
        m 1eub "Oh, veo que has notado ese bonito calendario colgado en la pared, [player]."
        m 3hua "Me ayuda a realizar un seguimiento de los eventos importantes, jejeje~"

    m 1eua "Permíteme mostrarte."
    show monika 1eua

    call mas_start_calendar_read_only

    m 1hua "Bastante bien, ¿verdad?"
    m 3eua "No dudes en consultar el calendario cuando quieras."
    m 1lksdla "Excepto cuando estoy hablando, por supuesto."

    show monika idle with dissolve_monika

    $ persistent._mas_first_calendar_check = True

    if store.mas_globals.in_idle_mode:

        $ store.hkb_button.talk_enabled = True
        $ store.hkb_button.extra_enabled = True
        $ store.hkb_button.music_enabled = True


    elif persistent._mas_player_bday is None:
        $ MASEventList.push("calendar_birthdate",skipeval=True)
        $ mas_MUMUDropShield()
    else:

        $ mas_HKBDropShield()
        $ mas_calDropOverlayShield()
    return

label _mas_start_calendar(select_date=True):

    python:

        _should_drop_shields = not store.mas_calendar.enabled
        mas_calRaiseOverlayShield()
        HKBHideButtons()

        ui.add(MASCalendar(select_date))
        rv = ui.interact()

        HKBShowButtons()
        if _should_drop_shields:
            mas_calDropOverlayShield()

    return rv

label mas_start_calendar_read_only:
    call _mas_start_calendar (select_date=False)
    return _return

label mas_start_calendar_select_date:
    call _mas_start_calendar (select_date=True)
    return _return













screen calendar_overlay():
    zorder 6





    add "mod_assets/calendar/calendar_button_shadow.png" xpos 351 ypos 251

    if store.mas_calendar.enabled and not store._menu:
        imagebutton:
            idle ("mod_assets/calendar/calendar_button_normal.png" if mas_current_background.isFltDay() else "mod_assets/calendar/calendar_button_normal-n.png")
            hover "mod_assets/calendar/calendar_button_hover.png"
            hover_sound gui.hover_sound
            activate_sound gui.activate_sound
            action Function(show_calendar)
            xpos 360
            ypos 260
    else:
        add ("mod_assets/calendar/calendar_button_normal.png" if mas_current_background.isFltDay() else "mod_assets/calendar/calendar_button_normal-n.png") xpos 360 ypos 260

init python:
    def mas_calDropOverlayShield():
        """RUNTIME ONLY
        Enables input for the calendar overlay
        """
        store.mas_calendar.enabled = True


    def mas_calHideOverlay():
        """RUNTIME ONLY
        Hides the calendar overlay
        """
        renpy.hide_screen("calendar_overlay", layer="master")


    def mas_calIsVisible_ovl():
        """
        RETURNS: True if the calendar ovelray is visible, False otherwise
        """
        return renpy.get_screen("calendar_overlay") is not None


    def mas_calRaiseOverlayShield():
        """RUNTIME ONLY
        Disables input for the calendar overlay
        """
        store.mas_calendar.enabled = False


    def mas_calShowOverlay():
        """RUNTIME ONLY
        Shows the calendar overlay
        """
        if not mas_current_background.hide_calendar and not mas_calIsVisible_ovl():
            renpy.show_screen("calendar_overlay", _layer="master")

    def mas_isLeapYear(year):
        """
        Checks if the given year is a leap year, accounting for the error

        IN:
            year - int, year to check

        OUT:
            bool - Whether or not the given year is a leap year
        """
        try:
            datetime.date(year, 2, 29)
            return True
        except ValueError:
            return False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
