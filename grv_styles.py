"""
GRV Text Styles Generator
Prints "GRV" in 10 different artistic styles
"""

def style_1_block():
    """Block letters style"""
    print("=== STYLE 1: BLOCK LETTERS ===")
    print("""
GGGGGG  RRRRRR   VVVVVVV
GG      RR   RR  VVVVVVV
GG      RRRRRR   VVVVVVV
GG   G  RR  RR       VV
GGGGGG  RR   RR      VV
""")

def style_2_ascii():
    """ASCII art style"""
    print("=== STYLE 2: ASCII ART ===")
    print("""
 _   _   ____   _____  
| | | | |  _ \\ | ____| 
| |_| | | |_) || |_|   
|  _  | |  _ < |  _ |  
| | | | | |_) || |___ | 
|_| |_| |____/ |_____|
""")

def style_3_3d():
    """3D effect style"""
    print("=== STYLE 3: 3D EFFECT ===")
    print("""
G   G RRRRR  V   V
G   G R   R V   V
G GG RRRRR  V   V
G  G R  R   V V V
 GG  R   R   VVV
""")

def style_4_dots():
    """Dot matrix style"""
    print("=== STYLE 4: DOT MATRIX ===")
    print("""
●●●●●  ●●●●●  ●     ●
●      ●   ●  ●     ●
●●●●●  ●●●●●  ●     ●
●      ●  ●●   ●   V 
●      ●   ●   ●●●●●
""")

def style_5_stars():
    """Star pattern style"""
    print("=== STYLE 5: STAR PATTERN ===")
    print("""
★☆★☆★  ★☆★☆★  ☆★☆
★      ★   ★  ★☆★☆
★☆☆☆★  ★☆★☆★  ☆★☆
★   ★★  ★  ★☆   ★☆
★☆☆☆★  ★   ★  ★☆★☆
""")

def style_6_wave():
    """Wave pattern style"""
    print("=== STYLE 6: WAVE PATTERN ===")
    print("""
∼∼∼∼∼∼  ∼∼∼∼∼∼  ∼∼∼∼∼
∼       ∼     ∼  ∼∼∼
∼∼∼∼∼∼  ∼∼∼∼∼∼  ∼∼∼∼∼
∼     ∼ ∼∼   ∼∼∼∼∼
∼∼∼∼∼∼  ∼     ∼∼∼∼∼
""")

def style_7_diamonds():
    """Diamond pattern style"""
    print("=== STYLE 7: DIAMOND PATTERN ===")
    print("""
◆◆◆◆◆  ◆◆◆◆◆  ◆◆◆
◆      ◆   ◆  ◆◆◆
◆◆◆◆◆  ◆◆◆◆◆  ◆◆◆
◆    ◆ ◆  ◆◆   ◆◆
◆◆◆◆◆  ◆   ◆  ◆◆◆
""")

def style_8_hearts():
    """Heart pattern style"""
    print("=== STYLE 8: HEART PATTERN ===")
    print("""
♥♥♥♥♥  ♥♥♥♥♥  ♥♥♥
♥      ♥   ♥  ♥♥♥
♥♥♥♥♥  ♥♥♥♥♥  ♥♥♥
♥  ♥♥  ♥  ♥♥   ♥♥
♥♥♥♥♥  ♥   ♥  ♥♥♥
""")

def style_9_musical():
    """Musical notes style"""
    print("=== STYLE 9: MUSICAL NOTES ===")
    print("""
♪♪♪♪♪  ♪♪♪♪♪  ♪♪♪
♪      ♪   ♪  ♪♪♪
♪♪♪♪♪  ♪♪♪♪♪  ♪♪♪
♪  ♪♪  ♪  ♪♪   ♪♪
♪♪♪♪♪  ♪   ♪  ♪♪♪
""")

def style_10_flowers():
    """Flower pattern style"""
    print("=== STYLE 10: FLOWER PATTERN ===")
    print("""
❀❀❀❀❀  ❀❀❀❀❀  ❀❀❀
❀      ❀   ❀  ❀❀❀
❀❀❀❀❀  ❀❀❀❀❀  ❀❀❀
❀    ❀ ❀  ❀❀   ❀❀
❀❀❀❀❀  ❀   ❀  ❀❀❀
""")

def display_all_styles():
    """Display all 10 styles of GRV"""
    print("🎨 GRV TEXT STYLES GENERATOR 🎨")
    print("=" * 50)
    print("Displaying 'GRV' in 10 different artistic styles:\n")
    
    styles = [
        style_1_block,
        style_2_ascii,
        style_3_3d,
        style_4_dots,
        style_5_stars,
        style_6_wave,
        style_7_diamonds,
        style_8_hearts,
        style_9_musical,
        style_10_flowers
    ]
    
    for i, style_func in enumerate(styles, 1):
        style_func()
        print()
    
    print("🎉 All 10 styles displayed! 🎉")

def main():
    """Main function"""
    display_all_styles()

if __name__ == "__main__":
    main()
