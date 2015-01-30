# colors
BLACK = (   0,   0,   0)
GREEN = (   0, 200,   0)
WHITE = ( 255, 255, 255)

FIELDS_X = 11
FIELDS_Y = 11
FIELD_SIZE_WIDTH = 64
FIELD_SIZE_HEIGHT = 64

size = (FIELDS_X*FIELD_SIZE_WIDTH, FIELDS_Y*FIELD_SIZE_HEIGHT)

BOMB_TIMER = 90
EXPLOSION_EXPAND = 8
EXP_DURATION = 15

EXP_INITIAL = "type_i"
# EXP_CENTER = "type_c"
EXP_CENTER_X = "type_c_x"
EXP_CENTER_T = "type_c_t"
EXP_CENTER_U = "type_c_u"
EXP_CENTER_L = "type_c_l"
EXP_CENTER_B = "type_c_b"
EXP_BRIDGE = "type_b"
EXP_END = "type_e"
EXP_UP = "type_u"
EXP_RIGHT = "type_r"
EXP_DOWN = "type_d"
EXP_LEFT = "type_l"

CENTER_DICTIONARY = {'1000': (EXP_CENTER_U, EXP_UP), '0100': (EXP_CENTER_U, EXP_RIGHT), '0010': (EXP_CENTER_U, EXP_DOWN), '0001': (EXP_CENTER_U, EXP_LEFT),
                     '1100': (EXP_CENTER_L, EXP_UP), '0110': (EXP_CENTER_L, EXP_RIGHT), '0011': (EXP_CENTER_L, EXP_DOWN), '1001': (EXP_CENTER_L, EXP_LEFT),
                     '1010': (EXP_CENTER_B, EXP_UP), '0101': (EXP_CENTER_B, EXP_RIGHT),
                     '1110': (EXP_CENTER_T, EXP_UP), '0111': (EXP_CENTER_T, EXP_RIGHT), '1011': (EXP_CENTER_T, EXP_DOWN), '1101': (EXP_CENTER_T, EXP_LEFT),
                     '1111': (EXP_CENTER_X, EXP_UP)}