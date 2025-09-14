init -999:
    default persistent._mas_submod_version_data = dict()

init 10 python:

    store.mas_submod_utils.Submod._checkUpdates()

init -989 python:

    if store.mas_submod_utils.submod_map:
        mas_submod_utils.submod_log.info(
            "\nSUBMODS INSTALADOS:\n{0}".format(
                ",\n".join(
                    ["    '{0}' v{1}".format(submod.name, submod.version) for submod in store.mas_submod_utils.submod_map.itervalues()]
                )
            )
        )


    store.mas_submod_utils.Submod._checkDependencies()

init -991 python in mas_submod_utils:
    import re
    import store



    persistent = store.persistent

    submod_log = store.mas_logging.init_log("submod_log")

    @store.mas_utils.deprecated(use_instead="submod_log.debug, submod_log.info, submod_log.warning, submod_log.error, submod_log.exception")
    def writeLog(msg):
        """
        Writes to the submod log if it is open

        IN:
            msg - message to write to log
        """
        submod_log.info(msg)

    submod_map = dict()

    class SubmodError(Exception):
        def __init__(self, _msg):
            self.msg = _msg
        def __str__(self):
            return self.msg

    class Submod(object):
        """
        Submod class

        PROPERTIES:
            author - submod author
            name - submod name
            version - version of the submod installed
            description - submod description
            dependencies - dependencies required for the submod
            settings_pane - string referring to the screen used for the submod's settings
            version_updates - update labels
        """
        
        FB_VERS_STR = "0.0.0"
        
        
        AN_REGEXP = re.compile(ur'^[ a-zA-Z_\u00a0-\ufffd][ 0-9a-zA-Z_\u00a0-\ufffd]*$')
        
        def __init__(
            self,
            author,
            name,
            version,
            description=None,
            dependencies={},
            settings_pane=None,
            version_updates={},
            coauthors=[]
        ):
            """
            Submod object constructor

            IN:
                author - string, author name.

                name - submod name

                version - version number in format SPECIFICALLY like so: `1.2.3`
                    (You can add more or less as need be, but splits MUST be made using periods)

                description - a short description for the submod
                    (Default: None)

                dependencies - dictionary in the following structure: {"name": ("minimum_version", "maximum_version")}
                corresponding to the needed submod name and version required
                NOTE: versions must be passed in the same way as the version property is done
                    (Default: empty dict)

                settings_pane - a string representing the screen for this submod's settings

                version_updates - dict of the format {"old_version_update_label_name": "new_version_update_label_name"}
                    NOTE: submods MUST use the format <author>_<name>_v<version> for update labels relating to their submods
                    NOTE: capital letters will be forced to lower and spaces will be replaced with underscores
                    NOTE: Update labels MUST accept a version parameter, defaulted to the version of the label
                    For example:
                        author name: MonikaAfterStory,
                        submod name: Example Submod
                        submod vers: 1.2.3

                    becomes:
                        label monikaafterstory_example_submod_v1_2_3(version="v1_2_3")

                coauthors - list/tuple of co-authors of this submod
                    (Default: empty list)
            """
            
            if name in submod_map:
                raise SubmodError("Se ha instalado dos veces un submod con el nombre '{0}'. Por favor, desinstale el duplicado.".format(name))
            
            
            try:
                map(int, version.split('.'))
            except:
                raise SubmodError("El número de versión '{0}' no es válido.".format(version))
            
            
            if not Submod.AN_REGEXP.match(author):
                raise SubmodError("Author '{0}' es inválido.".format(author))
            if not Submod.AN_REGEXP.match(name):
                raise SubmodError("Name '{0}' es inválido.".format(name))
            
            
            self.author = author
            self.name = name
            self.description = description if description is not None else ""
            self.version = version
            self.dependencies = dependencies
            self.settings_pane = settings_pane
            self.version_updates = version_updates
            self.coauthors = tuple(coauthors)
            
            
            submod_map[name] = self
            
            
            if name not in persistent._mas_submod_version_data:
                persistent._mas_submod_version_data[name] = version
        
        def __repr__(self):
            """
            Representation of this object
            """
            return "<Submod: ({0} v{1} by {2})>".format(self.name, self.version, self.author)
        
        def getVersionNumberList(self):
            """
            Gets the version number as a list of integers

            OUT:
                List of integers representing the version number
            """
            return map(int, self.version.split('.'))
        
        def hasUpdated(self):
            """
            Checks if this submod instance was updated (version number has incremented)

            OUT:
                boolean:
                    - True if the version number has incremented from the persistent one
                    - False otherwise
            """
            old_vers = persistent._mas_submod_version_data.get(self.name)
            
            
            if not old_vers:
                return False
            
            try:
                old_vers = map(int, old_vers.split('.'))
            
            
            except:
                persistent._mas_submod_version_data[self.name] = Submod.FB_VERS_STR
                return False
            
            return self.checkVersions(old_vers) > 0
        
        def updateFrom(self, version):
            """
            Updates the submod, starting at the given start version

            IN:
                version - the version number in the parsed format ('author_name_v#_#_#')
            """
            while version in self.version_updates:
                updateTo = self.version_updates[version]
                
                
                if renpy.has_label(updateTo) and not renpy.seen_label(updateTo):
                    renpy.call_in_new_context(updateTo, updateTo)
                version = self.version_updates[version]
        
        def checkVersions(self, comparative_vers):
            """
            Generic version checker for submods

            IN:
                curr_vers - current installed version of the submod as a list
                comparative_vers - the version we're comparing to (or need the current version to be at or greater than) as a list

            OUT:
                integer:
                    - (-1) if the current version number is less than the comparitive version
                    - 0 if the current version is the same as the comparitive version
                    - 1 if the current version is greater than the comparitive version
            """
            return store.mas_utils.compareVersionLists(
                self.getVersionNumberList(),
                comparative_vers
            )
        
        @staticmethod
        def _checkUpdates():
            """
            Checks if submods have updated and sets the appropriate update scripts for them to run
            """
            
            for submod in submod_map.itervalues():
                
                if submod.hasUpdated():
                    submod.updateFrom(
                        "{0}_{1}_v{2}".format(
                            submod.author,
                            submod.name,
                            persistent._mas_submod_version_data.get(submod.name, Submod.FB_VERS_STR).replace('.', '_')
                        ).lower().replace(' ', '_')
                    )
                
                
                persistent._mas_submod_version_data[submod.name] = submod.version
        
        @staticmethod
        def _checkDependencies():
            """
            Checks to see if the dependencies for this submod are met
            """
            def parseVersions(version):
                """
                Parses a string version number to list format.

                IN:
                    version - version string to parse

                OUT:
                    list() - representing the parsed version number

                NOTE: Does not handle errors as to get here, formats must be correct regardless
                """
                return map(int, version.split('.'))
            
            for submod in submod_map.itervalues():
                for dependency, minmax_version_tuple in submod.dependencies.iteritems():
                    dependency_submod = Submod._getSubmod(dependency)
                    
                    if dependency_submod is not None:
                        
                        minimum_version, maximum_version = minmax_version_tuple
                        
                        
                        if (
                            minimum_version
                            and dependency_submod.checkVersions(parseVersions(minimum_version)) < 0
                        ):
                            raise SubmodError(
                                "Submod '{0}' no está actualizado. Versión {1} necesaria para {2}. La versión instalada es {3}".format(
                                    dependency_submod.name, minimum_version, submod.name, dependency_submod.version
                                )
                            )
                        
                        
                        
                        elif (
                            maximum_version
                            and dependency_submod.checkVersions(parseVersions(maximum_version)) > 0
                        ):
                            raise SubmodError(
                                "La versión '{0}' de '{1}' está instalada y es incompatible con {2}.\nLa versión {3} es compatible.".format(
                                    dependency_submod.version, dependency_submod.name, submod.name, maximum_version
                                )
                            )
                    
                    
                    else:
                        raise SubmodError(
                            "Submod '{0}' no está instalado y es necesario para {1}.".format(
                                dependency, submod.name
                            )
                        )
        
        @staticmethod
        def _getSubmod(name):
            """
            Gets the submod with the name provided

            IN:
                name - name of the submod to get

            OUT:
                Submod object representing the submod by name if installed and registered
                None if not found
            """
            return submod_map.get(name)


    def isSubmodInstalled(name, version=None):
        """
        Checks if a submod with `name` is installed

        IN:
            name - name of the submod to check for
            version - if a specific version (or greater) is installed
            (NOTE: if None, this is ignored. Default: None)

        OUT:
            boolean:
                - True if submod with name is installed
                - False otherwise
        """
        submod = Submod._getSubmod(name)
        
        if submod and version:
            return submod.checkVersions(version) >= 0
        return bool(submod)


init -980 python in mas_submod_utils:
    import inspect
    import store
    from store import mas_utils


    current_label = None

    last_label = None


    function_plugins = dict()


    DEF_PRIORITY = 0


    JUMP_CALL_PRIORITY = 999

    PRIORITY_SORT_KEY = lambda x: x[1][2]


    def functionplugin(_label, _args=None, auto_error_handling=True, priority=0):
        """
        Decorator function to register a plugin

        The same as registerFunction. See its doc for parameter details
        """
        
        def wrap(_function):
            registerFunction(
                _label,
                _function,
                _args,
                auto_error_handling,
                priority
            )
            return _function
        return wrap


    def getAndRunFunctions(key=None):
        """
        Gets and runs functions within the key provided

        IN:
            key - Key to retrieve and run functions from
        """
        global function_plugins
        
        
        if not key:
            key = inspect.stack()[1][3]
        
        func_dict = function_plugins.get(key)
        
        if not func_dict:
            return
        
        
        
        sorted_plugins = _m1_zz_submods__prioritySort(key)
        for _action, data_tuple in sorted_plugins:
            if data_tuple[1]:
                try:
                    store._m1_zz_submods__run(_action, _m1_zz_submods__getArgs(key, _action))
                except Exception as ex:
                    store.mas_utils.mas_log.error("function {0} failed because {1}".format(_action.__name__, ex))
            
            else:
                store._m1_zz_submods__run(_action, _m1_zz_submods__getArgs(key, _action))

    def registerFunction(key, _function, args=None, auto_error_handling=True, priority=DEF_PRIORITY):
        """
        Registers a function to the function_plugins dict

        NOTE: Does NOT allow overwriting of existing functions in the dict
        NOTE: Function must be callable
        NOTE: Functions run when a label matching the key for the function is:
            called, jumped, or fallen through to.
            Or if plugged into a function, when a function by the name of the key calls getAndRunFunctions
        NOTE: If you need to provide args/kwargs to the function,
            wrap it into functools.partial

        IN:
            key - key to add the function to.
                NOTE: The key is either a label, or a function name
                NOTE: Function names only work if the function contains a getAndRunFunctions call.
                    Without it, it does nothing.
            _function - function to register
            auto_error_handling - whether or function plugins should ignore errors in functions
                (Set this to False for functions which call or jump)
            priority - Order priority to run functions
                (Like init levels, the lower the number, the earlier it runs)

        OUT:
            boolean:
                - True if the function was registered successfully
                - False otherwise
        """
        global function_plugins
        
        
        if not callable(_function):
            store.mas_utils.mas_log.error("{0} is not callable".format(_function.__name__))
            return False
        
        
        if args is None:
            args = ()
        
        else:
            mas_utils.report_deprecation(
                "parameter 'args' in 'registerFunction'",
                use_instead="functools.partial",
                use_instead_msg_fmt="Wrap your callable in '{use_instead}' to provide it args/kwargs."
            )
            
            if len(args) > len(inspect.getargspec(_function).args):
                store.mas_utils.mas_log.error("Demasiados argumentos proporcionados para la función {0}".format(_function.__name__))
                return False
        
        
        key = _m1_zz_submods__getOverrideLabel(key)
        
        
        if key not in function_plugins:
            function_plugins[key] = dict()
        
        
        elif _function in function_plugins[key]:
            return False
        
        function_plugins[key][_function] = (args, auto_error_handling, priority)
        return True

    def _m1_zz_submods__getArgs(key, _function):
        """
        TODO: remove this with r8
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        global function_plugins
        
        try:
            return function_plugins[key][_function][0]
        
        except KeyError:
            
            
            
            return None

    @mas_utils.deprecated(
        use_instead="functools.partial",
        use_instead_msg_fmt="Wrap your callable in '{use_instead}' to provide it args/kwargs."
    )
    def getArgs(key, _function):
        """
        Gets args for the given function at the given key

        IN:
            key - key to retrieve the function from
            _function - function to retrieve args from

        OUT:
            list of args if the function is present
            If function is not present, None is returned
        """
        return _m1_zz_submods__getArgs(key, _function)

    @mas_utils.deprecated(
        use_instead="functools.partial",
        use_instead_msg_fmt="Wrap your callable in '{use_instead}' to provide it args/kwargs."
    )
    def setArgs(key, _function, args=None):
        """
        Sets args for the given function at the key

        IN:
            key - key that the function's function dict is stored in
            _function - function to set the args

        OUT:
            boolean:
                - True if args were set successfully
                - False if not
        """
        global function_plugins
        
        func_dict = function_plugins.get(key)
        
        
        if not func_dict:
            return False
        
        
        if _function not in func_dict:
            return False
        
        if args is None:
            args = ()
        
        
        elif len(args) > len(inspect.getargspec(_function).args):
            store.mas_utils.mas_log.error("Demasiados argumentos proporcionados para la función {0}".format(_function.__name__))
            return False
        
        
        old_values = func_dict[_function]
        func_dict[_function] = (args, old_values[1], old_values[2])
        return True

    def unregisterFunction(key, _function):
        """
        Unregisters a function from the function_plugins dict

        IN:
            key - key the function we want to unregister is in
            _function - function we want to unregister

        OUT:
            boolean:
                - True if function was unregistered successfully
                - False otherwise
        """
        global function_plugins
        
        func_dict = function_plugins.get(key)
        
        
        if not func_dict:
            return False
        
        
        elif _function not in func_dict:
            return False
        
        
        function_plugins[key].pop(_function)
        return True

    def _m1_zz_submods__prioritySort(_label):
        """
        Sorts function plugins based on the priority order system

        IN:
            _label - label to sort functions by priority for

        OUT:
            sorted list of (_function, data_tuple) tuples

        NOTE: This assumes that the label exists in the function_plugins dict
        """
        global function_plugins
        
        
        func_list = [
            (_function, data_tuple)
            for _function, data_tuple in function_plugins[_label].iteritems()
        ]
        
        return sorted(func_list, key=PRIORITY_SORT_KEY)

    def _m1_zz_submods__getOverrideLabel(_label):
        """
        Gets the override label for the given label (will follow the chain if overrides are overridden)

        IN:
            _label - label to get the override label for

        OUT:
            string representing the last label in the override chain or _label if there are no overrides
        """
        while renpy.config.label_overrides.get(_label) is not None:
            _label = renpy.config.label_overrides[_label]
        return _label


init -990 python:
    def _m1_zz_submods__run(_function, args):
        """
        Private function to run a function in the global store
        """
        return _function(*args)


init 999 python:
    def label_callback(name, abnormal):
        """
        Function to run plugin functions and store the last label
        """
        
        store.mas_submod_utils.last_label = store.mas_submod_utils.current_label
        
        store.mas_submod_utils.current_label = name
        
        store.mas_submod_utils.getAndRunFunctions(name)
        
        
        base_label = _OVERRIDE_LABEL_TO_BASE_LABEL_MAP.get(name)
        if base_label is not None:
            persistent._seen_ever[base_label] = True

    config.label_callback = label_callback

    @store.mas_submod_utils.functionplugin("ch30_reset", priority=-999)
    def _m1_zz_submods__build_override_label_to_base_label_map():
        """
        Populates a lookup dict for all label overrides which are in effect
        """
        
        for overridden_label, label_override in config.label_overrides.iteritems():
            _OVERRIDE_LABEL_TO_BASE_LABEL_MAP[label_override] = overridden_label
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
