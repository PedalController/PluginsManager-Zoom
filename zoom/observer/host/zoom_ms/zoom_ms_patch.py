from decoder.lib.decoder_util import decode_message
from zoom.database import ZoomMSSeries
from zoom.model.zoom.zoom_effect import ZoomEffect


class ZoomMSPatch:
    """
    Based on: https://github.com/g200kg/zoom-ms-utility/blob/master/midimessage.md#patch-data-format
    """
    effects_status_bits = [
        [(5, 1, 0)],
        [(25, 1, 0)],
        [(46, 1, 0)],
        [(66, 1, 0)],
        [(87, 1, 0)],
        [(107, 1, 0)]
    ]

    effects_bits = [
        [(4, 64, 24), (5, 126, 16), (6, 7, 8), (8, 31, 0)],
        [(20, 4, 28), (25, 126, 16), (26, 7, 8), (29, 31, 0)],
        [(44, 32, 25), (46, 126, 16), (47, 7, 8), (49, 31, 0)],
        [(60, 2, 29), (66, 126, 16), (67, 7, 8), (70, 31, 0)],
        [(84, 16, 26), (87, 126, 16), (88, 7, 8), (90, 31, 0)],
        [(100, 1, 30), (107, 126, 16), (109, 7, 8), (111, 31, 0)],
    ]

    params_bits = [
        [[(8, 96, -5), (4, 8, -1), (9, 127, 3), (4, 4, 8), (10, 1, 11)],
          [(10, 124, -2), (4, 2, 4), (11, 31, 6)],
          [(4, 1, 0), (13, 127, 1), (12, 64, 2), (14, 3, 9)],
          [(14, 112, -4), (12, 32, -2), (15, 15, 4)],
          [(15, 112, -4), (12, 16, -1), (16, 15, 4)],
          [(16, 112, -4), (12, 8, 0), (17, 15, 4)],
          [(17, 112, -4), (12, 4, 1), (18, 15, 4)],
          [(18, 112, -4), (12, 2, 2), (19, 31, 4), (22, 64, 'NZ')],
          [(23, 127, 0), (20, 16, 3)]],
        [[(29, 96, -5), (28, 64, -4), (30, 127, 3), (28, 32, 5), (31, 1, 11)],
          [(31, 124, -2), (28, 16, 1), (32, 31, 6)],
          [(28, 8, -3), (33, 127, 1), (28, 4, 6), (34, 3, 9)],
          [(34, 112, -4), (28, 2, 2), (35, 15, 4)],
          [(35, 112, -4), (28, 1, 3), (37, 15, 4)],
          [(37, 112, -4), (36, 64, -3), (38, 15, 4)],
          [(38, 112, -4), (36, 32, -2), (39, 15, 4)],
          [(39, 112, -4), (36, 16, -1), (40, 31, 4), (42, 64, 'NZ')],
          [(43, 127, 0), (36, 1, 7)]],
        [[(49, 96, -5), (44, 4, 0), (50, 127, 3), (44, 2, 9), (51, 1, 11)],
          [(51, 124, -2), (44, 1, 5), (53, 31, 6)],
          [(52, 64, -6), (54, 127, 1), (52, 32, 3), (55, 3, 9)],
          [(55, 112, -4), (52, 16, -1), (56, 15, 4)],
          [(56, 112, -4), (52, 8, 0), (57, 15, 4)],
          [(57, 112, -4), (52, 4, 1), (58, 15, 4)],
          [(58, 112, -4), (52, 2, 2), (59, 15, 4)],
          [(59, 112, -4), (52, 1, 3), (61, 31, 4), (63, 64, 'NZ')],
          [(64, 127, 0), (60, 8, 4)]],
        [[(70, 96, -5), (68, 32, -3), (71, 127, 3), (68, 16, 6), (72, 1, 11)],
          [(72, 124, -2), (68, 8, 2), (73, 31, 6)],
          [(68, 4, -2), (74, 127, 1), (68, 2, 7), (75, 3, 9)],
          [(75, 112, -4), (68, 1, 3), (77, 15, 4)],
          [(77, 112, -4), (76, 64, -3), (78, 15, 4)],
          [(78, 112, -4), (76, 32, -2), (79, 15, 4)],
          [(79, 112, -4), (76, 16, -1), (80, 15, 4)],
          [(80, 112, -4), (76, 8, 0), (81, 31, 4), (83, 64, 'NZ')],
          [(85, 127, 0), (84, 64, 1)]],
        [[(90, 96, -5), (84, 2, 1), (91, 127, 3), (84, 1, 10), (93, 1, 11)],
          [(93, 124, -2), (92, 64, -1), (94, 31, 6)],
          [(92, 32, -5), (95, 127, 1), (92, 16, 4), (96, 3, 9)],
          [(96, 112, -4), (92, 8, 0), (97, 15, 4)],
          [(97, 112, -4), (92, 4, 1), (98, 15, 4)],
          [(98, 112, -4), (92, 2, 2), (99, 15, 4)],
          [(99, 112, -4), (92, 1, 3), (101, 15, 4)],
          [(101, 112, -4), (100, 64, -3), (102, 31, 4), (104, 64, 'NZ')],
          [(105, 127, 0), (105, 4, 5)]],
        [[(111, 96, -5), (108, 16, -2), (112, 127, 3), (108, 8, 7), (113, 1, 11)],
          [(113, 124, -2), (108, 4, 3), (114, 31, 6)],
          [(108, 2, -1), (115, 127, 1), (108, 1, 8), (117, 3, 9)],
          [(117, 112, -4), (116, 64, -3), (118, 15, 4)],
          [(118, 112, -4), (116, 32, -2), (119, 15, 4)],
          [(119, 112, -4), (116, 16, -1), (120, 15, 4)],
          [(120, 112, -4), (116, 8, 0), (121, 15, 4)],
          [(121, 112, -4), (116, 4, 1), (122, 31, 4), (125, 64, 'NZ')],
          [(126, 127, 0), (124, 32, 2)]]]

    @staticmethod
    def get_effect_status(data, effect: int) -> bool:
        status_data = ZoomMSPatch.effects_status_bits[effect]
        return decode_message(data, status_data)

    @staticmethod
    def get_effect(data, id_effect: int) -> ZoomEffect:
        effect_data = ZoomMSPatch.effects_bits[id_effect]

        id = decode_message(data, effect_data)

        plugin = ZoomMSSeries.effectlist[id]
        return ZoomEffect(plugin)

    @staticmethod
    def get_param(data, id_effect: int, id_param: int):
        param_data = ZoomMSPatch.params_bits[id_effect][id_param]

        return decode_message(data, param_data)
