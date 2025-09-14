








init 501 python:


    def mas_OVLDropShield():
        """RUNTIME ONLY
        Enables all overlay screens. This is like "dropping a shield" because
        it allows user interactions with the overlays.
        """
        
        mas_HKBDropShield()
        mas_calDropOverlayShield()


    def mas_OVLHide():
        """RUNTIME ONLY
        Hides all overlay screens.
        """
        
        HKBHideButtons()
        mas_calHideOverlay()


    def mas_OVLRaiseShield():
        """RUNTIME ONLY
        Disables all overlay screens. This is like "raising a shield" because
        it prevents user interactions with the overlays.
        """
        
        mas_HKBRaiseShield()
        mas_calRaiseOverlayShield()


    def mas_OVLShow():
        """RUNTIME ONLY
        Shows all overlay screens.
        """
        
        HKBShowButtons()
        mas_calShowOverlay()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
