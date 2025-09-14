


init python:
    def dumpPersistentToFile(dumped_persistent,dumppath):
        """
        Prints a file containing each dictionary element of a persistent variable

        IN:
            dumped_persistent - a renpy persistent variable
            dumppath - a file path to the text file to be created. Must be a valid write location
        """
        dumped_persistent = vars(dumped_persistent)
        
        fo = open(dumppath, "w")
        
        for key in sorted(dumped_persistent.iterkeys()):
            fo.write(str(key) + ' - ' + str(type(dumped_persistent[key])) + ' >>> '+ str(dumped_persistent[key]) + '\n\n')
        
        fo.close()

label import_ddlc_persistent_in_settings:
    $ mas_RaiseShield_core()

    call import_ddlc_persistent

    if store.mas_globals.dlg_workflow:


        $ enable_esc()
        $ mas_MUINDropShield()
    else:


        $ mas_DropShield_core()
    return

label import_ddlc_persistent:
    $ quick_menu = False
    scene black
    with Dissolve(1.0)

    if persistent._mas_imported_saves:
        menu:
            "Los datos guardados de Doki Doki Literature Club ya han sido fusionados. Abortando."
            "Okey":

                pass

        pause 0.3
        return

    python:

        from glob import glob


        if renpy.macintosh:
            rv = "~/Library/RenPy/"
            check_path = os.path.expanduser(rv)

        elif renpy.windows:
            if 'APPDATA' in os.environ:
                check_path =  os.environ['APPDATA'] + "/RenPy/"
            else:
                rv = "~/RenPy/"
                check_path = os.path.expanduser(rv)

        else:
            rv = "~/.renpy/"
            check_path = os.path.expanduser(rv)

        ddlc_save_path = glob(check_path + 'DDLC/persistent')
        if not ddlc_save_path:
            ddlc_save_path = glob(check_path + 'DDLC-*/persistent')


    if ddlc_save_path:
        $ ddlc_save_path = ddlc_save_path[0]
        "Se encontraron datos guardados de Doki Doki Literature Club en [ddlc_save_path]."
        menu:
            "¿Te gustaría importar los datos de Doki Doki Literature Club en [config.name]?\n(DDLC no se verá afectado)"
            "Sí, importar datos de DDLC":

                pause 0.3
            "No, no importar":

                pause 0.3
                return
    else:


        "No se pudieron encontrar datos de Doki Doki Literature Club."
        menu:
            "Ningún dato será importado en este momento"
            "Okey":

                pause 0.3
                return


    python:

        ddlc_persistent = None
        try:
            with open(ddlc_save_path, "rb") as ddlc_pfile:
                ddlc_persistent = mas_dockstat.cPickle.loads(ddlc_pfile.read().decode("zlib"))

        except Exception as e:
            store.mas_utils.mas_log.error("Fallo en la lectura/decodificación del persistent: {0}".format(e))

        else:
            
            store.mas_versions.init()
            ddlc_persistent = updateTopicIDs("v030", ddlc_persistent)
            ddlc_persistent = updateTopicIDs("v031", ddlc_persistent)
            ddlc_persistent = updateTopicIDs("v032", ddlc_persistent)
            ddlc_persistent = updateTopicIDs("v033", ddlc_persistent)
            mas_versions.clear()

    if ddlc_persistent is None:
        menu:
            "No se han podido leer/decodificar los datos de Doki Doki Literature Club. Abortando."
            "Okey":

                pass

        pause 0.3
        return


    if not persistent.first_run:
        label import_ddlc_persistent.save_merge_or_replace:
        menu:
            "También se han encontrado datos de Monika After Story.\n¿Te gustaría fusionarlos con los datos de DDLC?"
            "Fusionar datos":

                pass
            "Cancelar":

                "Los datos de DDLC se pueden importar más tarde en el menú de ajustes"
                return


    python:
















































        def _updatePersistentDict(key, old_persistent, new_persistent):
            """
            Merges the old persistent dict at the key provided into the new persistent

            IN:
                key - key to update
                old_persistent - persistent to copy data from
                new_persistent - persistent to copy data to

            NOTE: Should only be used to update dicts
            """
            if key not in old_persistent.__dict__:
                return
            
            if old_persistent.__dict__[key] is not None:
                if (
                    key in new_persistent.__dict__
                    and new_persistent.__dict__[key] is not None
                ):
                    new_persistent.__dict__[key].update(old_persistent.__dict__[key])
                
                else:
                    new_persistent.__dict__[key] = old_persistent.__dict__[key]

        def _updatePersistentBool(key, old_persistent, new_persistent):
            """
            Merges bools from the old persistent at the key provided into the new persistent

            IN:
                key - key to update
                old_persistent - persistent to copy data from
                new_persistent - persistent to copy data to

            NOTE: Should only be used to update bools
            """
            if key not in old_persistent.__dict__:
                return
            
            if old_persistent.__dict__[key] is not None:
                new_persistent.__dict__[key] = old_persistent.__dict__[key]



        _updatePersistentDict("_seen_ever", ddlc_persistent, persistent)


        _updatePersistentDict("_seen_audio", ddlc_persistent, persistent)


        _updatePersistentDict("_seen_images", ddlc_persistent, persistent)


        _updatePersistentBool("clearall", ddlc_persistent, persistent)


        _updatePersistentBool("monika_kill", ddlc_persistent, persistent)


        _updatePersistentBool("tried_skip", ddlc_persistent, persistent)


        if ddlc_persistent.monika_reload is not None:
            if persistent.monika_reload is not None:
                persistent._mas_ddlc_reload_count = persistent.monika_reload + ddlc_persistent.monika_reload
            
            else:
                persistent._mas_ddlc_reload_count = ddlc_persistent.monika_reload


        if ddlc_persistent.clear is not None:
            if persistent.clear is not None:
                for index in range(len(persistent.clear)-1):
                    persistent.clear[index] = persistent.clear[index] or ddlc_persistent.clear[index]
            
            else:
                persistent.clear = ddlc_persistent.clear


        if ddlc_persistent.playername:
            if persistent.playername and persistent.playername != ddlc_persistent.playername:
                renpy.call_in_new_context("merge_unmatched_names")
            
            else:
                persistent.playername = ddlc_persistent.playername

        player = persistent.playername



        if ddlc_persistent.playthrough is not None:
            if (
                persistent.playthrough is None
                or persistent.playthrough < ddlc_persistent.playthrough
            ):
                persistent.playthrough = ddlc_persistent.playthrough


        __mas__memoryCleanup()


        persistent._mas_imported_saves = True
    return

label merge_unmatched_names:
    menu:
        "Los nombres de los jugadores no coinciden. ¿Cuál te gustaría conservar?"
        "[ddlc_persistent.playername]":
            $ persistent.playername = ddlc_persistent.playername
        "[persistent.playername]":
            $ persistent.playername
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
