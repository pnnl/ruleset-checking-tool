from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums

# This dictionary maps the LightingSpaceOptions2019ASHRAE901TG37 enumerations to
# the corresponding lpd_space_type values in the OSSTD file
# ashrae_90_1_prm_2019.prm_interior_lighting.json
lighting_space_enumeration_to_lpd_space_type_map = {
    "ATRIUM_LOW_MEDIUM": "atrium <= 40 ft height",
    "ATRIUM_HIGH": "atrium > 40 ft height",
    "AUDIENCE_SEATING_AREA_AUDITORIUM": "audience seating - auditorium",
    "AUDIENCE_SEATING_AREA_CONVENTION_CENTER": "audience seating - convention center",
    "AUDIENCE_SEATING_AREA_EXERCISE_CENTER": "audience seating - exercise center",
    "AUDIENCE_SEATING_AREA_GYMNASIUM": "audience seating - gymnasium",
    "AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER": "audience seating - motion picture theater",
    "AUDIENCE_SEATING_AREA_PENITENTIARY": "audience seating - penitentiary",
    "AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER": "audience seating - performing arts theater",
    "AUDIENCE_SEATING_AREA_RELIGIOUS_FACILITY": "audience seating - religious facility",
    "AUDIENCE_SEATING_AREA_SPORTS_ARENA": "audience seating - sports arena",
    "AUDIENCE_SEATING_AREA_TRANSPORTATION_FACILITY": "audience seating - transportation facility",
    "AUDIENCE_SEATING_AREA_ALL_OTHER": "audience seating - all other",
    "BANKING_ACTIVITY_AREA": "banking activity",
    "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY": "classroom/lecture/training - penitentiary",
    "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL": "classroom/lecture/training - preschool to 12th",
    "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER": "classroom/lecture/training - all other",
    "CONFERENCE_MEETING_MULTIPURPOSE_ROOM": "conference/meeting/multipurpose",
    "CONFINEMENT_CELLS": "confinement cells",
    "COPY_PRINT_ROOM": "copy/print",
    "CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED": "corridor for visually impaired",
    "CORRIDOR_HOSPITAL": "corridor - hospital",
    "CORRIDOR_MANUFACTURING_FACILITY": "corridor - manufacturing facility",
    "CORRIDOR_ALL_OTHERS": "corridor - all other",
    "COURT_ROOM": "courtroom",
    "COMPUTER_ROOM": "computer room",
    "DINING_AREA_PENITENTIARY": "dining - penitentiary",
    "DINING_AREA_FACILITY_FOR_THE_VISUALLY_IMPAIRED": "dining for visually impaired",
    "DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING": "dining - bar/lounge/leisure",
    "DINING_AREA_CAFETERIA_OR_FAST_FOOD_DINING": "dining - cafeteria/fast food",
    "DINING_AREA_FAMILY_DINING": "dining - family",
    "DINING_AREA_ALL_OTHERS": "dining - all other",
    "ELECTRICAL_MECHANICAL_ROOM": "electrical/mechanical",
    "EMERGENCY_VEHICLE_GARAGE": "emergency vehicle garage",
    "FOOD_PREPARATION_AREA": "kitchen",
    "GUEST_ROOM": "guest room",
    "JUDGES_CHAMBERS": "judges chambers",
    "DWELLING_UNIT": "apartment - hardwired",
    "LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM": "laboratory",
    "LAUNDRY_WASHING_AREA": "laundry/washing",
    # FIXME: The w/ft^2 value should be 0.59 but is set to 0.6 in the OSSTD
    "LOADING_DOCK_INTERIOR": "loading dock",
    "LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED": "lobby for visually impared",
    "LOBBY_ELEVATOR": "lobby - elevator",
    "LOBBY_HOTEL": "lobby - hotel",
    "LOBBY_MOTION_PICTURE_THEATER": "lobby - motion picture theater",
    "LOBBY_PERFORMING_ARTS_THEATER": "lobby - performing arts theater",
    "LOBBY_ALL_OTHERS": "lobby - all other",
    "LOCKER_ROOM": "locker room",
    "LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY": "lounge/breakroom - healthcare facility",
    "LOUNGE_BREAKROOM_ALL_OTHERS": "lounge/breakroom - all other",
    "OFFICE_ENCLOSED": "office - enclosed <= 250 sf",
    "OFFICE_OPEN_PLAN": "office - open",
    "PARKING_AREA_INTERIOR": "parking area, interior",
    "PHARMACY_AREA": "pharmacy",
    "RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED": "restroom - visually impaired",
    "RESTROOM_ALL_OTHERS": "restroom - all other",
    "SALES_AREA": "sales",
    "SEATING_AREA_GENERAL": "seating area, general",
    "STAIRWELL": "stairwell",
    "STORAGE_ROOM_HOSPITAL": "storage 50 to 1000 sf - hospital",
    "STORAGE_ROOM_SMALL": "storage < 50 sf",
    "STORAGE_ROOM_LARGE": "storage 50 to 1000 sf - all other",
    "VEHICULAR_MAINTENANCE_AREA": "vehicular maintenance",
    "WORKSHOP": "workshop",
    "ASSISTED_LIVING_FACILITY_CHAPEL": "chapel - visually impaired",
    "ASSISTED_LIVING_FACILITY_RECREATION_ROOM_COMMON_LIVING_ROOM": "recreation/common living - visually impaired",
    "CONVENTION_CENTER_EXHIBIT_SPACE": "exhibit - convention center",
    "DORMITORY_LIVING_QUARTERS": "dormitory - living quarters",
    "FIRE_STATION_SLEEPING_QUARTERS": "firestation - sleeping quarters",
    "GYMNASIUM_FITNESS_CENTER_EXERCISE_AREA": "gymnsasium exercise area",
    "GYMNASIUM_FITNESS_CENTER_PLAYING_AREA": "gymnasium playing area",
    "HEALTHCARE_FACILITY_EMERGENCY_ROOM": "emergency room",
    "HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM": "exam/treatment",
    "HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM": "medical supply",
    "HEALTHCARE_FACILITY_NURSERY": "nursery",
    "HEALTHCARE_FACILITY_NURSES_STATION": "nurses station",
    "HEALTHCARE_FACILITY_OPERATING_ROOM": "operating room",
    "HEALTHCARE_FACILITY_PATIENT_ROOM": "patient room",
    "HEALTHCARE_FACILITY_PHYSICAL_THERAPY_ROOM": "physical therapy",
    "HEALTHCARE_FACILITY_RECOVERY_ROOM": "recovery",
    "LIBRARY_READING_AREA": "library - reading",
    "LIBRARY_STACKS": "library - stacks",
    # NOTE: The typo "manufacuring" below matches the OSSTD file
    "MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA": "detailed manufacuring",
    "MANUFACTURING_FACILITY_EQUIPMENTROOM": "manufacturing equipment room",
    "MANUFACTURING_FACILITY_EXTRA_HIGH_BAY_AREA": "manufacturing extra high bay",
    "MANUFACTURING_FACILITY_HIGH_BAY_AREA": "manufacturing high bay",
    "MANUFACTURING_FACILITY_LOW_BAY_AREA": "manufacturing low bay",
    "MUSEUM_GENERAL_EXHIBITION_AREA": "museum exhibit area",
    "MUSEUM_RESTORATION_ROOM": "museum restoration",
    "POST_OFFICE_SORTING_AREA": "post office - sorting area",
    "RELIGIOUS_FACILITY_FELLOWSHIP_HALL": "fellowship hall - religious facility",
    "RELIGIOUS_FACILITY_WORSHIP_PULPIT_CHOIR_AREA": "worship/pulpit/choir area",
    "RETAIL_FACILITIES_DRESSING_FITTING_ROOM": "retail dressing room",
    "RETAIL_FACILITIES_MALL_CONCOURSE": "retail mall concourse",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_I_FACILITY": "sports arena playing area, class I",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_II_FACILITY": "sports arena playing area, class II",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_III_FACILITY": "sports arena playing area, class III",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_IV_FACILITY": "sports arena playing area, class IV",
    "TRANSPORTATION_FACILITY_BAGGAGE_CAROUSEL_AREA": "baggage/carousel",
    "TRANSPORTATION_FACILITY_AIRPORT_CONCOURSE": "airport concourse",
    "TRANSPORTATION_FACILITY_TICKET_COUNTER": "transportation ticket counter",
    "WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS": "warehouse - bulk storage",
    "WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS": "warehouse - fine storage",
}

FULL_AUTO_ON = SchemaEnums.schema_enums["LightingOccupancyControlOptions"].FULL_AUTO_ON
PARTIAL_AUTO_ON = SchemaEnums.schema_enums[
    "LightingOccupancyControlOptions"
].PARTIAL_AUTO_ON
MANUAL_ON = SchemaEnums.schema_enums["LightingOccupancyControlOptions"].MANUAL_ON
OTHER = SchemaEnums.schema_enums["LightingOccupancyControlOptions"].OTHER
NONE = SchemaEnums.schema_enums["LightingOccupancyControlOptions"].NONE


# ATRIUM_LOW_MEDIUM
def table_G3_7_lookup(lighting_space_type, space_height, space_area):
    """Returns the lighting power density for a space as
    required by ASHRAE 90.1 Table G3.7

    Parameters
    ----------
    lighting_space_type : str
        One of the LightingSpaceOptions2019ASHRAE901TG37 enumeration values
    space_height : Quantity
        The height of the space
    space_area: Quantity
        The area of the space

    Returns
    -------
    dict
        { lpd: Quantity - The lighting power density given by Table G3.7 }

    """
    lpd_space_type = lighting_space_enumeration_to_lpd_space_type_map[
        lighting_space_type
    ]

    osstd_entry = find_osstd_table_entry(
        [("lpd_space_type", lpd_space_type)],
        osstd_table=data["ashrae_90_1_prm_2019.prm_interior_lighting"],
    )
    watts_per_ft2 = osstd_entry["w/ft^2"] * ureg("watt / foot**2")
    # Note: the units for the w/ft fields should actually be W/ft^3
    # This might be None, so make the Quantity below instead
    watts_per_ft = osstd_entry["w/ft"]

    if watts_per_ft is None:
        lpd = watts_per_ft2
    else:
        lpd = (
            watts_per_ft2
            + watts_per_ft * ureg("watt / foot") * space_height / space_area
        )

    control_credit = osstd_entry["occup_sensor_auto_on_svgs"]

    return {"lpd": lpd, "control_credit": control_credit}
