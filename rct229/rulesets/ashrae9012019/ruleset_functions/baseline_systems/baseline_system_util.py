from typing import Literal


class HVAC_SYS:
    """Class holding HVAC system type value"""

    SYS_1: Literal["Sys-1"] = "Sys-1"
    SYS_1A: Literal["Sys-1a"] = "Sys-1a"
    SYS_1B: Literal["Sys-1b"] = "Sys-1b"
    SYS_1C: Literal["Sys-1c"] = "Sys-1c"
    SYS_2: Literal["Sys-2"] = "Sys-2"
    SYS_3: Literal["Sys-3"] = "Sys-3"
    SYS_3A: Literal["Sys-3a"] = "Sys-3a"
    SYS_3B: Literal["Sys-3b"] = "Sys-3b"
    SYS_3C: Literal["Sys-3c"] = "Sys-3c"
    SYS_4: Literal["Sys-4"] = "Sys-4"
    SYS_5: Literal["Sys-5"] = "Sys-5"
    SYS_5B: Literal["Sys-5b"] = "Sys-5b"
    SYS_6: Literal["Sys-6"] = "Sys-6"
    SYS_6B: Literal["Sys-6b"] = "Sys-6b"
    SYS_7: Literal["Sys-7"] = "Sys-7"
    SYS_7A: Literal["Sys-7a"] = "Sys-7a"
    SYS_7B: Literal["Sys-7b"] = "Sys-7b"
    SYS_7C: Literal["Sys-7c"] = "Sys-7c"
    SYS_8: Literal["Sys-8"] = "Sys-8"
    SYS_8A: Literal["Sys_8a"] = "Sys-8a"
    SYS_8B: Literal["Sys-8b"] = "Sys-8b"
    SYS_8C: Literal["Sys-8c"] = "Sys-8c"
    SYS_9: Literal["Sys-9"] = "Sys-9"
    SYS_9B: Literal["Sys-9b"] = "Sys-9b"
    SYS_10: Literal["Sys-10"] = "Sys-10"
    SYS_11_1: Literal["Sys-11.1"] = "Sys-11.1"
    SYS_11_1A: Literal["Sys-11.1a"] = "Sys-11.1a"
    SYS_11_1B: Literal["Sys-11.1b"] = "Sys-11.1b"
    SYS_11_1C: Literal["Sys-11.1c"] = "Sys-11.1c"
    SYS_11_2: Literal["Sys-11.2"] = "Sys-11.2"
    SYS_11_2A: Literal["Sys-11.2a"] = "Sys-11.2a"
    SYS_12: Literal["Sys-12"] = "Sys-12"
    SYS_12A: Literal["Sys-12a"] = "Sys-12a"
    SYS_12B: Literal["Sys-12b"] = "Sys-12b"
    SYS_13: Literal["Sys-13"] = "Sys-13"
    SYS_13A: Literal["Sys-13a"] = "Sys-13a"
    UNMATCHED: Literal["Not_Sys"] = "Not_Sys"


HVAC_SYSTEM_TYPE_DICTIONARY = {
    HVAC_SYS.SYS_1: [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1A, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_1C],
    HVAC_SYS.SYS_2: [HVAC_SYS.SYS_2],
    HVAC_SYS.SYS_3: [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A, HVAC_SYS.SYS_3B, HVAC_SYS.SYS_3C],
    HVAC_SYS.SYS_4: [HVAC_SYS.SYS_4],
    HVAC_SYS.SYS_5: [HVAC_SYS.SYS_5, HVAC_SYS.SYS_5B],
    HVAC_SYS.SYS_6: [HVAC_SYS.SYS_6, HVAC_SYS.SYS_6B],
    HVAC_SYS.SYS_7: [HVAC_SYS.SYS_7, HVAC_SYS.SYS_7A, HVAC_SYS.SYS_7B, HVAC_SYS.SYS_7C],
    HVAC_SYS.SYS_8: [HVAC_SYS.SYS_8, HVAC_SYS.SYS_8A, HVAC_SYS.SYS_8B, HVAC_SYS.SYS_8C],
    HVAC_SYS.SYS_9: [HVAC_SYS.SYS_9, HVAC_SYS.SYS_9B],
    HVAC_SYS.SYS_10: [HVAC_SYS.SYS_10],
    HVAC_SYS.SYS_11_1: [
        HVAC_SYS.SYS_11_1,
        HVAC_SYS.SYS_11_1A,
        HVAC_SYS.SYS_11_1B,
        HVAC_SYS.SYS_11_1C,
    ],
    HVAC_SYS.SYS_11_2: [
        HVAC_SYS.SYS_11_2,
        HVAC_SYS.SYS_11_2A,
    ],
    HVAC_SYS.SYS_12: [
        HVAC_SYS.SYS_12,
        HVAC_SYS.SYS_12A,
        HVAC_SYS.SYS_12B,
    ],
    HVAC_SYS.SYS_13: [HVAC_SYS.SYS_13, HVAC_SYS.SYS_13A],
}
