ZERO_WIDTH = '\u200b'


class ListMarker:
    hand = '☛'
    star = '⋆'
    circle_star = '⍟'
    circle_small = '∘'
    square_black = '∎'
    triangle = '⊳'
    triangle_black = '▶'
    hexagon = '⎔'
    hexagon_double = '⏣'
    logic = '⊸'
    arrow = '→'
    arrow_down = '↳'
    arrow_up = '↱'
    arrow_big = '⇒'
    arrow_curved = '↪'
    arrow_two = '⇉'
    arrow_three = '⇶'
    bullet = '•'


class Seperators:
    basic = '-'
    thick = '█'
    double = '═'
    line = '─'

    @classmethod
    def make_line(cls, character_name: str, amount: int = 15):
        character = getattr(cls, character_name)
        return character * amount
