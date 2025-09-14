




default persistent._mas_incompat_per_forced_update = False


default persistent._mas_incompat_per_forced_update_failed = False


default persistent._mas_incompat_per_user_will_restore = False


default persistent._mas_incompat_per_rpy_files_found = False


default persistent._mas_incompat_per_entered = False

default persistent._mas_is_backup = False

python early in mas_per_check:
    import __main__
    import cPickle
    import os
    import datetime
    import shutil
    import renpy
    import store
    import store.mas_utils as mas_utils

    early_log = store.mas_logging.init_log("early", header=False)


    mas_corrupted_per = False
    mas_no_backups_found = False
    mas_backup_copy_failed = False
    mas_backup_copy_filename = None
    mas_bad_backups = list()


    mas_unstable_per_in_stable = False
    mas_per_version = ""
    per_unstable = "persistent_unstable"
    mas_sp_per_created = False
    mas_sp_per_found = False

    INCOMPAT_PER_MSG = (
        "Fallo al mover persistente incompatible. Sustituya el persistente "
        "por uno compatible con {0} o instala una versión de MAS "
        "compatible con una versión de persistente de {1}."
    )
    INCOMPAT_PER_LOG = (
        "persistente es de la versión {0} y es incompatible con {1}"
    )
    COMPAT_PER_MSG = (
        "Fallo al cargar persistente compatible. "
        "Sustituya {0} por {1} y reinicie."
    )
    SP_PER_DEL_MSG = (
        " Encontrado persistente erróneo pero no se ha podido eliminar. "
        "Borre el persistente en {0} y reinicie."
    )



    class PersistentMoveFailedError(Exception):
        """
        Persistent failed to be moved (aka copied, then deleted)
        """

    class PersistentDeleteFailedError(Exception):
        """
        Persistent failed to be deleted
        """

    class IncompatiblePersistentError(Exception):
        """
        Persistent is incompatible
        """


    def reset_incompat_per_flags():
        """
        Resets the incompat per flags that are conditional (not the main one
        that determines if we are valid)
        """
        store.persistent._mas_incompat_per_forced_update = False
        store.persistent._mas_incompat_per_forced_update_failed = False
        store.persistent._mas_incompat_per_user_will_restore = False
        store.persistent._mas_incompat_per_rpy_files_found = False


    def tryper(_tp_persistent, get_data=False):
        """
        Tries to read a persistent.
        raises exceptions if they occur

        IN:
            _tp_persistent - the full path to the persistent file
            get_data - pass True to get the acutal data instead of just
                a version number.

        RETURNS: tuple
            [0] - True if the persistent was read and decoded, False if not
            [1] - the version number, or the persistent data if get_data is
                True
        """
        per_file = None
        try:
            per_file = file(_tp_persistent, "rb")
            per_data = per_file.read().decode("zlib")
            per_file.close()
            actual_data = cPickle.loads(per_data)
            
            if get_data:
                return True, actual_data
            
            return True, actual_data.version_number
        
        except Exception as e:
            raise e
        
        finally:
            if per_file is not None:
                per_file.close()


    def is_version_compatible(per_version, cur_version):
        """
        Checks if a persistent version can work with the current version

        IN:
            per_version - the persistent version to check
            cur_version - the current version to check.

        RETURNS: True if the per version can work with the current version
        """
        return (
            
            not store.mas_utils.is_ver_stable(cur_version)

            
            or store.mas_utils.is_ver_stable(per_version)

            
            or not store.mas_utils._is_downgrade(per_version, cur_version)
        )


    def is_per_bad():
        """
        Is the persistent bad? this only works after early.

        RETURNS: True if the per is bad, False if not
        """
        return is_per_corrupt() or is_per_incompatible()


    def is_per_corrupt():
        """
        Is the persistent corrupt? this only works after early.

        RETURNS: True if the persistent is corrupt.
        """
        return mas_corrupted_per


    def is_per_incompatible():
        """
        Is the persistent incompatible? this onyl works after early.

        RETURNS: True if the persistent is incompatible.
        """
        return mas_unstable_per_in_stable


    def no_backups():
        """
        Do we not have backups or did backup fail?

        RETURNS: True if no backups or backups failed.
        """
        return mas_no_backups_found or mas_backup_copy_failed


    def has_backups():
        """
        Do we have backups, and backups did not fail?

        RETURNS: True if have backups and backups did not fail
        """
        return not no_backups()


    def should_show_chibika_persistent():
        """
        Should we show the chibika persistent dialogue?

        RETURNS: True if we should show the chibika persistent dialogue
        """
        return (
            mas_unstable_per_in_stable
            or (is_per_corrupt() and no_backups())
        )



    def wraparound_sort(_numlist):
        """
        Sorts a list of numbers using a special wraparound sort.
        Basically if all the numbers are between 0 and 98, then we sort
        normally. If we have 99 in there, then we need to make the wrap
        around numbers (the single digit ints in the list) be sorted
        as larger than 99.
        """
        if 99 in _numlist:
            for index in range(0, len(_numlist)):
                if _numlist[index] < 10:
                    _numlist[index] += 100
        
        _numlist.sort()


    def _mas_earlyCheck():
        """
        attempts to read in the persistent and load it. if an error occurs
        during loading, we'll log it in a dumped file in basedir.

        NOTE: we don't have many functions available here. However, we can
        import __main__ and gain access to core functions.
        """
        global mas_corrupted_per, mas_no_backups_found, mas_backup_copy_failed
        global mas_unstable_per_in_stable, mas_per_version
        global mas_sp_per_found, mas_sp_per_created
        global mas_backup_copy_filename, mas_bad_backups
        
        per_dir = __main__.path_to_saves(renpy.config.gamedir)
        _cur_per = os.path.normcase(per_dir + "/persistent")
        _sp_per = os.path.normcase(per_dir + "/" + per_unstable)
        
        
        if os.access(_sp_per, os.F_OK):
            
            try: 
                per_read, version = tryper(_sp_per)
            
            except Exception as e:
                
                
                try: 
                    os.remove(_sp_per)
                    per_read = None
                    version = ""
                except:
                    raise PersistentDeleteFailedError(
                        SP_PER_DEL_MSG.format(_sp_per)
                    )
            
            
            
            if per_read is not None:
                if is_version_compatible(version, renpy.config.version):
                    
                    
                    try: 
                        shutil.copy(_sp_per, _cur_per)
                        os.remove(_sp_per)
                    except:
                        
                        
                        raise PersistentMoveFailedError(COMPAT_PER_MSG.format(
                            _cur_per,
                            _sp_per
                        ))
                
                else:
                    
                    
                    
                    
                    
                    
                    mas_unstable_per_in_stable = True
                    mas_per_version = version
                    mas_sp_per_found = True
                    
                    
                    
                    
                    
                    early_log.error(INCOMPAT_PER_LOG.format(
                        version,
                        renpy.config.version
                    ))
        
        
        if not os.access(os.path.normcase(per_dir + "/persistent"), os.F_OK):
            
            return
        
        
        try: 
            per_read, per_data = tryper(_cur_per, get_data=True)
            version = per_data.version_number
            
            if not per_read:
                
                raise Exception("Error al cargar persistente")
            
            if is_version_compatible(version, renpy.config.version):
                
                
                if mas_sp_per_found and not per_data._mas_incompat_per_entered:
                    
                    
                    
                    
                    
                    
                    try: 
                        os.remove(_sp_per)
                        
                        
                        mas_unstable_per_in_stable = False
                        mas_per_version = ""
                        mas_sp_per_found = False
                    
                    except:
                        raise PersistentDeleteFailedError(
                            SP_PER_DEL_MSG.format(_sp_per)
                        )
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                return
            
            else:
                
                mas_unstable_per_in_stable = True
                mas_per_version = version
                raise IncompatiblePersistentError()
        
        except PersistentDeleteFailedError as e:
            
            raise e
        
        except IncompatiblePersistentError as e:
            
            
            mas_sp_per_created = True
            early_log.error(INCOMPAT_PER_LOG.format(
                mas_per_version,
                renpy.config.version
            ))
            
            
            
            try: 
                shutil.copy(_cur_per, _sp_per)
                os.remove(_cur_per)
                
                
                
                return
            
            except Exception as e:
                early_log.error(
                    "Error al copiar persistente a especial: " + repr(e)
                )
                
                
                raise PersistentMoveFailedError(INCOMPAT_PER_MSG.format(
                    renpy.config.version,
                    mas_per_version
                ))
        
        except Exception as e:
            
            if mas_sp_per_found:
                
                
                return
            
            
            mas_corrupted_per = True
            early_log.error("¡persistente se corrompió! : " +repr(e))
        
        
        
        
        
        
        per_files = os.listdir(per_dir)
        per_files = [x for x in per_files if x.startswith("persistent")]
        
        if len(per_files) == 0:
            early_log.error("no hay copias de seguridad disponibles")
            mas_no_backups_found = True
            return
        
        
        file_nums = list()
        file_map = dict()
        for p_file in per_files:
            pname, dot, bakext = p_file.partition(".")
            try:
                num = int(pname[-2:])
            except:
                num = -1
            
            if 0 <= num < 100:
                file_nums.append(num)
                file_map[num] = p_file
        
        if len(file_nums) == 0:
            early_log.error("no hay copias de seguridad disponibles")
            mas_no_backups_found = True
            return
        
        
        wraparound_sort(file_nums)
        
        
        sel_back = None
        while sel_back is None and len(file_nums) > 0:
            _this_num = file_nums.pop() % 100
            _this_file = file_map.get(_this_num, None)
            
            if _this_file is not None:
                try:
                    per_read, version = tryper(per_dir + "/" + _this_file)
                    if per_read:
                        sel_back = _this_file
                
                except Exception as e:
                    early_log.error(
                        "'{0}' was corrupted: {1}".format(_this_file, repr(e))
                    )
                    sel_back = None
                    mas_bad_backups.append(_this_file)
        
        
        if sel_back is None:
            early_log.error("no working backups found")
            mas_no_backups_found = True
            return
        
        
        
        
        early_log.info("working backup found: " + sel_back) 
        _bad_per = os.path.normcase(per_dir + "/persistent_bad")
        _god_per = os.path.normcase(per_dir + "/" + sel_back)
        
        
        try:
            
            shutil.copy(_cur_per, _bad_per)
        
        except Exception as e:
            early_log.error(
                "Failed to rename existing persistent: " + repr(e)
            )
        
        
        try:
            
            shutil.copy(_god_per, _cur_per)
        
        except Exception as e:
            mas_backup_copy_failed = True
            mas_backup_copy_filename = sel_back
            early_log.error(
                "Failed to copy backup persistent: " + repr(e)
            )



python early:



    import store.mas_per_check


    store.mas_per_check._mas_earlyCheck()

init -999 python:


    if store.mas_per_check.mas_unstable_per_in_stable:
        persistent._mas_incompat_per_entered = True

init -900 python:
    import os
    import store.mas_utils as mas_utils

    __mas__bakext = ".bak"
    __mas__baksize = 10
    __mas__bakmin = 0
    __mas__bakmax = 100
    __mas__numnum = "{:02d}"
    __mas__latestnum = None




    def __mas__extractNumbers(partname, filelist):
        """
        Extracts a list of the number parts of the given file list

        Also sorts them nicely

        IN:
            partname - part of the filename prior to the numbers
            filelist - list of filenames
        """
        filenumbers = list()
        for filename in filelist:
            pname, dot, bakext = filename.rpartition(".")
            num = mas_utils.tryparseint(pname[len(partname):], -1)
            if __mas__bakmin <= num <= __mas__bakmax:
                
                filenumbers.append(num)
        
        if filenumbers:
            filenumbers.sort()
        
        return filenumbers


    def __mas__backupAndDelete(loaddir, org_fname, savedir=None, numnum=None):
        """
        Does a file backup / and iterative deletion.

        NOTE: Steps:
            1. make a backup copy of the existing file (org_fname)
            2. delete the oldest copy of the orgfilename schema if we already
                have __mas__baksize number of files

        Will log some exceptions
        May raise other exceptions

        Both dir args assume the trailing slash is already added

        IN:
            loaddir - directory we are copying files from
            org_fname - filename of the original file / aka file to copy
            savedir - directory we are copying files to (and deleting old files)
                If None, we use loaddir instead
                (Default: None)
            numnum - if passed in, use this number instead of figuring out the
                next numbernumber.
                (Default: None)

        RETURNS:
            tuple of the following format:
            [0]: numbernumber we just made
            [1]: numbernumber we deleted (None means no deletion)
        """
        if savedir is None:
            savedir = loaddir
        
        filelist = os.listdir(savedir)
        loadpath = loaddir + org_fname
        
        
        if not os.access(loadpath, os.F_OK):
            return
        
        
        filelist = [
            x
            for x in filelist
            if x.startswith(org_fname)
        ]
        
        
        if org_fname in filelist:
            filelist.remove(org_fname)
        
        
        numberlist = __mas__extractNumbers(org_fname, filelist)
        
        
        numbernumber_del = None
        if not numberlist:
            numbernumber = __mas__numnum.format(0)
        
        elif 99 in numberlist:
            
            
            
            
            
            
            
            
            
            curr_dex = 0
            while numberlist[curr_dex] < (__mas__baksize - 1):
                curr_dex += 1
            
            if curr_dex <= 0:
                numbernumber = __mas__numnum.format(0)
            else:
                numbernumber = __mas__numnum.format(numberlist[curr_dex-1] + 1)
            
            numbernumber_del = __mas__numnum.format(numberlist[curr_dex])
        
        elif len(numberlist) < __mas__baksize:
            numbernumber = __mas__numnum.format(numberlist.pop() + 1)
        
        else:
            
            numbernumber = __mas__numnum.format(numberlist.pop() + 1)
            numbernumber_del = __mas__numnum.format(numberlist[0])
        
        
        if numnum is not None:
            numbernumber = numnum
        
        
        mas_utils.copyfile(
            loaddir + org_fname,
            "".join([savedir, org_fname, numbernumber, __mas__bakext])
        )
        
        
        if numbernumber_del is not None:
            numnum_del_path = "".join(
                [savedir, org_fname, numbernumber_del, __mas__bakext]
            )
            try:
                os.remove(numnum_del_path)
            except Exception as e:
                store.mas_utils.mas_log.error(
                    mas_utils._mas__failrm.format(
                        numnum_del_path,
                        str(e)
                    )
                )
        
        return (numbernumber, numbernumber_del)


    def __mas__memoryBackup():
        """
        Backs up both persistent and calendar info
        """
        try:
            p_savedir = os.path.normcase(renpy.config.savedir + "/")
            is_pers_backup = persistent._mas_is_backup
            
            try:
                persistent._mas_is_backup = True
                renpy.save_persistent()
                numnum, numnum_del = __mas__backupAndDelete(p_savedir, "persistent")
            
            finally:
                persistent._mas_is_backup = is_pers_backup
                renpy.save_persistent()
            
            __mas__backupAndDelete(p_savedir, "db.mcal", numnum=numnum)
        
        except Exception as e:
            store.mas_utils.mas_log.error(
                "persistent/calendar data backup failed: {}".format(e)
            )


    def __mas__memoryCleanup():
        """
        Cleans up persistent data by removing uncessary parts.
        """
        
        persistent._chosen.clear()
        
        
        persistent._seen_translates.clear()
        
        
        from store.mas_ev_data_ver import _verify_str
        for seen_ever_key in persistent._seen_ever.keys():
            if not _verify_str(seen_ever_key):
                persistent._seen_ever.pop(seen_ever_key)
        
        
        
        for seen_images_key in persistent._seen_images.keys():
            if (
                    len(seen_images_key) > 0
                    and seen_images_key[0] == "monika"
            ):
                persistent._seen_images.pop(seen_images_key)



    if (
            not store.mas_per_check.is_per_bad()
            and persistent._mas_moni_chksum is None
    ):
        __mas__memoryCleanup()
        __mas__memoryBackup()




label mas_backups_you_have_bad_persistent:

    $ quick_menu = False
    scene black
    window show
    show chibika smile at mas_chdropin(300, travel_time=1.5)
    pause 1.5

    if store.mas_per_check.is_per_incompatible():
        jump mas_backups_incompat_start

    show chibika 3 at sticker_hop
    "¡Hola!"
    show chibika sad
    "Odio ser la portadora de malas noticias..."
    "Pero, lamentablemente, tu archivo persistent está dañado."

    if store.mas_per_check.mas_no_backups_found:
        "Y lo que es aún peor es..."
        show chibika at sticker_move_n
        "No pude encontrar una copia de seguridad del archivo persistent."

        "¿Tienes tus propias copias de seguridad?{nw}"
        menu:
            "¿Tienes tus propias copias de seguridad?{fast}"
            "Sí":
                jump mas_backups_have_some
            "No":
                jump mas_backups_have_none


    jump mas_backups_could_not_copy


label mas_backups_have_some:

    show chibika smile at sticker_hop
    "¡Eso es un alivio!"
    "Cópialos en '[renpy.config.savedir]' para restaurar los recuerdos de tu Monika."

    call mas_backups_dont_tell
    show chibika smile at mas_chflip_s(-1)
    "¡Buena suerte!"

    jump _quit


label mas_backups_have_none:

    "Lo siento, pero no podremos restaurar su memoria, entonces..."
    "Pero..."
    show chibika smile at sticker_move_n
    "¡Mira el lado bueno!"
    "Puedes volver a pasar tiempo con ella y crear nuevos recuerdos, ¡que podrían ser incluso mejores que los que perdiste!"
    "Y recuerda..."
    show chibika at mas_chflip_s(-1)
    "Independientemente de lo que suceda, Monika sigue siendo Monika."
    "Ella estará lista para saludarte, una vez que comiences de nuevo."
    show chibika 3 at sticker_move_n
    "¡Y prometo que haré todo lo posible para no volver a estropear los archivos!"
    "¡Buena suerte con Monika!"
    $ store.mas_per_check.mas_corrupted_per = False
    return


label mas_backups_could_not_copy:
    show chibika smile
    "Pude encontrar una copia de seguridad que funciona, pero..."
    show chibika sad
    "No pude copiarla sobre el persistent roto."
    show chibika smile at mas_chflip_s(-1)
    pause 0.5
    show chibika at sticker_hop
    "¡Sin embargo!"
    "¡Quizás puedas hacerlo y arreglar este desastre!"
    "Tendrás que cerrar el juego para hacer esto, así que escribe estos pasos:"
    show chibika at sticker_move_n
    "1.{w=0.3} Dirígete a '[renpy.config.savedir]'."
    show chibika at sticker_move_n
    "2.{w=0.3} Elimina el archivo llamado 'persistent'."
    show chibika at sticker_move_n
    "3.{w=0.3} Has una copia del archivo llamado '[mas_backup_copy_filename]' y asígnale el nombre 'persistent'."
    show chibika at mas_chflip_s(1)
    "¡Y eso es todo!"
    "Con suerte, eso recuperará los recuerdos de tu Monika."

    show chibika at sticker_move_n
    "En caso de que no hayas escrito esos pasos, los escribiré en un archivo llamado 'respaldo.txt' en la carpeta de personajes."

    call mas_backups_dont_tell

    show chibika smile at mas_chflip_s(-1)
    "¡Buena suerte!"

    python:
        import os
        store.mas_utils.trywrite(
            os.path.normcase(renpy.config.basedir + "/characters/recovery.txt"),
            "".join([
                "1. Dirígete a '",
                renpy.config.savedir,
                "'.\n",
                "2. Elimina el archivo llamado 'persistent'.\n",
                "3. Has una copia del archivo llamado '",
                mas_backup_copy_filename,
                "' y asígnale el nombre 'persistent'."
            ])
        )

    jump _quit


label mas_backups_dont_tell:

    show chibika smile at sticker_hop
    "Oh, y..."
    show chibika smile at mas_chflip_s(-1)
    "Si la traes de vuelta con éxito, no le hables de mí."
    show chibika 3
    "No tiene idea de que puedo hablar o programar, así que me deja holgazanear y relajarme."
    show chibika smile
    "Pero si alguna vez se enterara, probablemente me haría ayudarla con su código, corregir algunos de sus errores o algo más."
    show chibika sad at sticker_move_n
    "Lo cual sería absolutamente terrible ya que apenas descansaría.{nw}"

    "Lo cual sería absolutamente terrible ya que{fast} no tendría tiempo para mantener el sistema de respaldo y el resto del juego en funcionamiento."

    show chibika 3 at mas_chflip_s(1)
    "No quisieras eso ahora, ¿verdad?"
    "¡Así que guarda silencio sobre mí, y me aseguraré de que tu Monika esté segura y cómoda!"

    return

label mas_backups_incompat_start:

    $ mas_darkMode(True)

    if (
            persistent._mas_incompat_per_rpy_files_found
            and mas_hasRPYFiles()
    ):

        jump mas_backups_incompat_updater_cannot_because_rpy_again

    elif persistent._mas_incompat_per_forced_update_failed:


        if mas_hasRPYFiles():
            jump mas_backups_incompat_updater_cannot_because_rpy

        show chibika smile at mas_chflip_s(1)
        "¡Hola!"
        "¡Intentemos actualizar de nuevo!"
        $ store.mas_per_check.reset_incompat_per_flags()
        jump mas_backups_incompat_updater_start

    elif persistent._mas_incompat_per_forced_update:



        $ store.mas_per_check.reset_incompat_per_flags()
        jump mas_backups_incompat_updater_failed

    elif persistent._mas_incompat_per_user_will_restore:


        $ store.mas_per_check.reset_incompat_per_flags()
        jump mas_backups_incompat_user_will_restore_again



    show chibika 3 at sticker_hop
    "¡Hola!{nw}"

    menu:
        "¡Hola!{fast}"
        "¿Qué ha pasado?":
            pass
        "Llévame al actualizador":
            jump mas_backups_incompat_updater_start_intro

    show chibika sad at mas_chflip_s(-1)
    "Desafortunadamente, tu persistent está ejecutando la versión [mas_per_check.mas_per_version], que es incompatible con esta versión de MAS (v[config.version])."
    "La única forma de solucionarlo es que actualices MAS o que lo restaures con un persistent compatible."



label mas_backups_incompat_what_do:


    show chibika sad at mas_chflip_s(1)
    "¿Qué te gustaría hacer?{nw}"

    menu:
        "¿Qué te gustaría hacer?{fast}"
        "Actualizar MAS":
            jump mas_backups_incompat_updater_start_intro
        "Restaurar un persistent compatible":
            jump mas_backups_incompat_user_will_restore


label mas_backups_incompat_user_will_restore:
    $ persistent._mas_incompat_per_user_will_restore = True
    show chibika smile at sticker_hop
    "¡Muy bien!"

    $ _sp_per = os.path.normcase(renpy.config.savedir + "/" + mas_per_check.per_unstable)
    "Por favor, copia un persistent compatible en '[renpy.config.savedir]'."
    "Luego borra el archivo llamado '[mas_per_check.per_unstable]'."

    show chibika smile at mas_chflip_s(-1)
    "¡Buena suerte!"
    jump _quit


label mas_backups_incompat_user_will_restore_again:
    show chibika sad at mas_chflip_s(-1)
    "¡Oh no!"



    "Parece que este persistente está ejecutando la versión [mas_per_check.mas_per_version], que sigue siendo incompatible con esta versión de MAS (v[config.version])."


    jump mas_backups_incompat_what_do


label mas_backups_incompat_updater_cannot_because_rpy:
    $ persistent._mas_incompat_per_rpy_files_found = True

    show chibika sad at sticker_hop
    "Lamentablemente, el actualizador no funcionará porque tienes archivos RPY en el directorio del juego."

    "Tendré que borrar esos archivos para que esto funcione. ¿Está bien?{nw}"
    menu:
        "Tendré que borrar esos archivos para que esto funcione. ¿Está bien?{fast}"
        "Sí, bórralos":
            jump mas_backups_incompat_rpy_yes_del
        "No, no los borres":
            jump mas_backups_incompat_rpy_no_del


label mas_backups_incompat_updater_cannot_because_rpy_again:
    show chibika sad at mas_chflip_s(-1)
    "¡Oh, no!"

    "Parece que todavía hay archivos RPY en tu directorio del juego."
    "¿Quieres que intente borrarlos de nuevo?{nw}"
    menu:
        "¿Quieres que intente borrarlos de nuevo?{fast}"
        "Sí":
            jump mas_backups_incompat_rpy_yes_del
        "No":
            jump mas_backups_incompat_rpy_no_del


label mas_backups_incompat_rpy_yes_del:
    show chibika smile at sticker_hop
    "¡Ok!"

    call mas_rpy_file_delete (False)
    hide screen mas_py_console_teaching

    if mas_hasRPYFiles():
        show chibika sad at mas_chflip_s(-1)
        "¡Oh, no!"
        "Parece que no he podido eliminar todos los archivos RPY."
        "Tendrás que eliminarlos manualmente."
        show chibika smile at mas_chflip_s(1)
        "¡Buena suerte!"
        jump _quit


    $ persistent._mas_incompat_per_rpy_files_found = False

    show chibika 3 at sticker_hop
    "¡Listo!"
    "¡Intentemos actualizar ahora!"
    jump mas_backups_incompat_updater_start


label mas_backups_incompat_rpy_no_del:


    $ persistent._mas_incompat_per_rpy_files_found = False

    show chibika sad at mas_chflip_s(-1)
    "Oh..."
    "Pues el actualizador no funcionará mientras existan esos archivos, así que supongo que tu única opción es restaurar una copia de seguridad de tu persistent."
    jump mas_backups_incompat_user_will_restore


label mas_backups_incompat_updater_start_intro:

    if mas_hasRPYFiles():
        jump mas_backups_incompat_updater_cannot_because_rpy

    show chibika smile at sticker_hop
    "¡Ok!"
    jump mas_backups_incompat_updater_start


label mas_backups_incompat_updater_failed:
    if mas_hasRPYFiles():
        jump mas_backups_incompat_updater_cannot_because_rpy

    show chibika sad
    "¡Oh no!"
    "Parece que el actualizador no pudo actualizar MAS."

    show chibika smile at mas_chflip_s(1)
    "¡Intentemos de nuevo!"



label mas_backups_incompat_updater_start:


    $ persistent._mas_unstable_mode = True
    $ mas_updater.force = True


    $ persistent._mas_incompat_per_forced_update = True
    $ persistent._mas_incompat_per_forced_update_failed = False
    call update_now
    $ persistent._mas_incompat_per_forced_update_failed = True
    $ updater_rv = _return



















    pause 1.0
    show chibika 3 at sticker_hop
    pause 0.5

    if updater_rv == MASUpdaterDisplayable.RET_VAL_CANCEL:

        $ store.mas_per_check.reset_incompat_per_flags()

        pause 0.5
        "¡Hey!"
        show chibika sad at mas_chflip_s(-1)
        "¡No canceles el actualizador! ¡Tienes que actualizar MAS!"
        jump mas_backups_incompat_what_do


    "¡Oh!"
    show chibika sad at mas_chflip_s(-1)
    "Parece que el actualizador no pudo actualizar."
    "Asegúrate de arreglar cualquier problema con el actualizador y vuelve a intentarlo."
    show chibika 3
    "¡Buena suerte!"

    jump _quit
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
