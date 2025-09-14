python early in mas_statements:
    from collections import namedtuple

    _m1_0statements__JumpWithArgsParseData = namedtuple("__JumpWithArgsParseData", ("label", "is_expression", "arg_info"))


    def _m1_0statements__jump_with_args(label, args, kwargs):
        """
        Jumps to the given label and passes the provided args and kwargs
        You're probably looking for mas_jump_with_args which
            utilises Python's * and ** starred syntax

        IN:
            label - the label to jump to
            args - the positional arguments for the label
            kwargs - the named arguments forthe label
        """
        renpy.store._args = args
        renpy.store._kwargs = kwargs
        renpy.jump(label)

    def mas_jump_with_args(label, *args, **kwargs):
        """
        Jumps to the given label and passes the provided args and kwargs

        IN:
            label - the label to jump to
            *args - the positional arguments for the label
            **kwargs - the named arguments forthe label
        """
        _m1_0statements__jump_with_args(label, args, kwargs)


    def _m1_0statements__get_label(parsed_data):
        """
        Returns label from the parsed data
        NOTE: may raise exceptions

        IN:
            parsed_data - __JumpWithArgsParseData for this statement

        OUT:
            str
        """
        label_ = parsed_data.label
        if parsed_data.is_expression:
            label_ = eval(label_)
        return label_

    def _m1_0statements__parse_jump_with_args(lex):
        """
        Parses the jump_with_args statement

        IN:
            lex - the Lexer object

        OUT:
            __JumpWithArgsParseData
        """
        lex.expect_noblock("jarg")
        
        if lex.keyword("expression"):
            is_expression = True
            label_ = lex.require(lex.simple_expression)
            lex.keyword("pass")
        
        else:
            is_expression = False
            label_ = lex.require(lex.label_name)
        
        arg_info = renpy.parser.parse_arguments(lex)
        
        lex.expect_eol()
        lex.advance()
        
        return _m1_0statements__JumpWithArgsParseData(label_, is_expression, arg_info)

    def _m1_0statements__execute_jump_with_args(parsed_data):
        """
        Executes the jump_with_args statement

        IN:
            parsed_data - __JumpWithArgsParseData for this statement
        """
        label_ = _m1_0statements__get_label(parsed_data)
        
        arg_info = parsed_data.arg_info
        if arg_info:
            args, kwargs = arg_info.evaluate()
            _m1_0statements__jump_with_args(label_, args, kwargs)
        
        else:
            _m1_0statements__jump_with_args(label_, None, None)

    def _m1_0statements__predict_jump_with_args(parsed_data):
        """
        Predicts the jump_with_args statement

        IN:
            parsed_data - __JumpWithArgsParseData for this statement
        """
        try:
            label_ = _m1_0statements__get_label(parsed_data)
        except Exception:
            return
        
        if not renpy.has_label(label_):
            return
        
        return [renpy.game.script.lookup(label)]

    def _m1_0statements__lint_jump_with_args(parsed_data):
        """
        A lint function for the jump_with_args statement

        IN:
            parsed_data - __JumpWithArgsParseData for this statement
        """
        try:
            label_ = _m1_0statements__get_label(parsed_data)
        except Exception:
            return
        
        if not renpy.has_label(label_):
            raise Exception("jarg is being used with unknown label: '{}'", label_)



    renpy.register_statement(
        "jarg", 
        parse=_m1_0statements__parse_jump_with_args,
        execute=_m1_0statements__execute_jump_with_args,
        predict=_m1_0statements__predict_jump_with_args,
        lint=_m1_0statements__lint_jump_with_args
    )


    renpy.store.mas_jump_with_args = mas_jump_with_args
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
