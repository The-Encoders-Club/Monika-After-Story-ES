




init -10 python:

    def getCharacterImage(char, expression="1a"):
        
        
        
        
        
        
        
        
        
        
        
        
        return renpy.display.image.images.get((char, expression), None)


    def mas_getPropFromStyle(style_name, prop_name):
        """
        Retrieves a property from a style
        Recursively checks parent styles until the property is found.

        IN:
            style_name - name of style as string
            prop_name - property to find as string

        RETURNS: value of the propery if we can find it, None if not found
        """
        style_name = (style_name,)
        prop_not_found = True
        while prop_not_found:
            
            
            style_obj = renpy.style.styles.get(style_name, None)
            if style_obj is None:
                return None
            
            
            if len(style_obj.properties) > 0:
                
                
                if prop_name in style_obj.properties[0]:
                    return style_obj.properties[0][prop_name]
            
            
            if style_obj.parent is None:
                return None
            
            
            style_name = style_obj.parent
        
        
        return None


    def mas_prefixFrame(frm, prefix):
        """
        Generates a frame object with the given prefix substitued into the
        image. This effectively makes a copy of the given Frame object.

        NOTE: cannot use _duplicate as it does shallow copy for some reason.

        IN:
            frm - Frame object
            prefix - prefix to replace `prefix_`. "_" will be added if not
                found

        RETURNS: Frame object, or None if failed to make it
        """
        if not prefix.endswith("_"):
            prefix += "_"
        
        try:
            
            frm_borders = {
                "left": frm.left,
                "top": frm.top,
                "right": frm.right,
                "bottom": frm.bottom,
            }
            
            
            img_path = renpy.substitute(
                frm.image.name,
                scope={"prefix_": prefix}
            )
            
            
            return Frame(img_path, **frm_borders)
        except:
            return None



init -5 python:
    dissolve_monika = {"master": Dissolve(0.25, alpha=True)}
    dissolve_textbox = {"screens": Dissolve(0.2, alpha=True)}


transform leftin_slow(x=640, z=0.80, t=1.00):
    xcenter -300 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein t xcenter x



transform ls32:
    leftin_slow(x=640)


transform lps32:
    leftin_slow(x=640,t=4.00)


transform lslide(t=1.00, x=-600):
    subpixel True
    on hide:
        easeout t xcenter x


transform rs32:
    lslide()


transform rps32:
    lslide(t=4.00,x=-700)


transform mas_chdropin(x=640, y=405, travel_time=3.00):
    ypos -300 xcenter x
    easein travel_time ypos y

transform mas_chflip(dir):


    xzoom dir

transform mas_chflip_s(dir, travel_time=0.36):
    ease travel_time xzoom dir

transform mas_chhopflip(dir, ydist=-15, travel_time=0.36):


    easein_quad travel_time/2.0 yoffset ydist xzoom 0
    easeout_quad travel_time/2.0 yoffset 0 xzoom dir

transform mas_chmove(x, y, travel_time=1.0):


    ease travel_time xpos x ypos y



transform mas_chriseup(x=300, y=405, travel_time=1.00):
    ypos 800 xcenter x
    easein travel_time ypos y


transform mas_chlongjump(x, y, ymax, travel_time=1.0):
    parallel:
        linear travel_time xpos x
    parallel:
        easeout travel_time*0.6 ypos ymax
        easein travel_time*0.4 ypos y



transform blink_transform(open_eyes_img, closed_eyes_img):
    block:

        open_eyes_img
        block:
            choice:
                3
            choice:
                5
            choice:
                7
        closed_eyes_img
        choice 0.02:
            0.03
            open_eyes_img
            0.1
            closed_eyes_img
        choice 0.98:
            pass
        0.06
        repeat

transform wink_transform(wink_img, open_eyes_img):

    on default:
        wink_img
        1
        open_eyes_img
    on show:
        wink_img
        1
        open_eyes_img
    on replace:
        wink_img
        1
        open_eyes_img
transform streaming_tears_transform(open_eyes_img, closed_eyes_img):
    block:
        open_eyes_img
        block:
            choice:
                9
            choice:
                11
            choice:
                12
        closed_eyes_img
        0.15
        repeat
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
