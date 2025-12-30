from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums

# This dictionary maps the LightingSpaceOptions2022ASHRAE901TG37 enumerations to
# the corresponding lpd_space_type values in the OSSTD file
# ashrae_90_1_prm_2022.prm_interior_lighting.json
lighting_space_enumeration_to_prm_lpd_map = {
    # ATRIUM
    "ATRIUM_LOW": "atrium < 20 ft height",
    "ATRIUM_MEDIUM": "atrium >= 20 ft and <= 40 ft height",
    "ATRIUM_HIGH": "atrium > 40 ft height",
    # AUDIENCE SEATING AREA
    "AUDIENCE_SEATING_AREA_AUDITORIUM": "audience seating - auditorium",
    "AUDIENCE_SEATING_AREA_CONVENTION_CENTER": "audience seating - convention center",
    "AUDIENCE_SEATING_AREA_GYMNASIUM": "audience seating - gymnasium",
    "AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER": "audience seating - motion picture theater",
    "AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER": "audience seating - performing arts theater",
    "AUDIENCE_SEATING_AREA_SPORTS_ARENA": "audience seating - sports arena",
    "AUDIENCE_SEATING_AREA_ALL_OTHER": "audience seating - all other",
    # BANK
    "BANKING_ACTIVITY_AREA": "banking activity",
    # CLASSROOM/LECTURE HALL/TRAINING ROOM
    "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL": "classroom/lecture/training - preschool to 12th",
    "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER": "classroom/lecture/training - all other",
    # COMPUTER ROOM
    "COMPUTER_ROOM": "computer room",
    # CONFERENCE
    "CONFERENCE_MEETING_MULTIPURPOSE_ROOM": "conference/meeting/multipurpose",
    # COPY / PRINT
    "COPY_PRINT_ROOM": "copy/print",
    # CORRIDOR
    "CORRIDOR_ALL_OTHERS": "corridor - all other",
    # COURTROOM
    "COURT_ROOM": "courtroom",
    # DINING (normal)
    "DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING": "dining - bar/lounge/leisure",
    "DINING_AREA_CAFETERIA_OR_FAST_FOOD_DINING": "dining - cafeteria/fast food",
    "DINING_AREA_FAMILY_DINING": "dining - family",
    "DINING_AREA_ALL_OTHERS": "dining - all other",
    # ELECTRICAL
    "ELECTRICAL_MECHANICAL_ROOM": "electrical/mechanical",
    # EMERGENCY VEHICLE GARAGE
    "EMERGENCY_VEHICLE_GARAGE": "emergency vehicle garage",
    # EQUIPMENT ROOM
    "EQUIPMENT_ROOM": "manufacturing equipment room",
    # FOOD PREP
    "FOOD_PREPARATION_AREA": "kitchen",
    # GUEST / DWELLING
    "GUEST_ROOM": "guest room",
    "DWELLING_UNIT": "apartment - hardwired",
    # LABORATORY
    "LABORATORY_SCHOOL": "classroom - laboratory or shop",
    "LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM": "laboratory",
    # LAUNDRY
    "LAUNDRY_WASHING_AREA": "laundry/washing",
    # LOADING DOCK
    "LOADING_DOCK_INTERIOR": "loading dock",
    # LOBBY
    "LOBBY_ELEVATOR": "lobby - elevator",
    "LOBBY_HOTEL": "lobby - hotel",
    "LOBBY_MOTION_PICTURE_THEATER": "lobby - motion picture theater",
    "LOBBY_PERFORMING_ARTS_THEATER": "lobby - performing arts theater",
    "LOBBY_ALL_OTHERS": "lobby - all other",
    # LOCKER
    "LOCKER_ROOM": "locker room",
    # LOUNGE
    "LOUNGE_BREAKROOM_MOTHERS_WELLNESS": "mother's/wellness room",
    "LOUNGE_BREAKROOM_ALL_OTHERS": "lounge/breakroom - all other",
    # OFFICE
    "OFFICE_ENCLOSED_SMALL": "office - enclosed <= 250 sf",
    "OFFICE_ENCLOSED_LARGE": "office - enclosed > 250 sf",
    "OFFICE_OPEN_PLAN": "office - open",
    # PARKING
    "PARKING_AREA_INTERIOR_DAYLIGHT_TRANSITION": "parking area, interior - daylight transition zone",
    "PARKING_AREA_INTERIOR_ALL_OTHERS": "parking area, interior - all other",
    # PHARMACY
    "PHARMACY_AREA": "pharmacy",
    # RESTROOMS
    "RESTROOM_ALL_OTHERS": "restroom - all other",
    # SALES
    "SALES_AREA": "sales",
    # SEATING
    "SEATING_AREA_GENERAL": "seating area, general",
    # SECURITY SCREENING
    "SECURITY_SCREENING_TRANSPORTATION_SCREENING": "security screening - airport/bus/ship/train/transportation screening",
    "SECURITY_SCREENING_TRANSPORTATION_QUEUE": "security screening - airport/bus/ship/train/transportation screening queue",
    "SECURITY_SCREENING_GENERAL": "security screening - general",
    # STAIRWELL
    "STAIRWELL": "stairwell",
    # STORAGE
    "STORAGE_ROOM_LARGE": "storage 50 to 1000 sf - all other",
    "STORAGE_ROOM_SMALL": "storage < 50 sf",
    # VEHICULAR
    "VEHICULAR_MAINTENANCE_AREA": "vehicular maintenance",
    # WORKSHOP
    "WORKSHOP_SCHOOL": "workshop - preschool to 12th, laboratory, and shop classrooms",
    "WORKSHOP_ALL_OTHERS": "workshop - all other",
    # CASINO AREAS
    "CASINO_BETTING_AREA": "casino - betting/sportsbook/keno/bingo",
    "CASINO_HIGH_LIMIT_AREA": "casino - high-limit game area",
    "CASINO_SLOT_MACHINE_AREA": "casino - slot machine/digital gaming area",
    "CASINO_TABLE_GAMES_AREA": "casino - table games area",
    # CONVENTION CENTER
    "CONVENTION_CENTER_EXHIBIT_SPACE": "exhibit - convention center",
    # CORRECTIONAL
    "CORRECTIONAL_FACILITY_AUDIENCE_SEATING_AREA": "correctional facilities - audience seating",
    "CORRECTIONAL_FACILITY_CLASSROOM": "correctional facilities - classroom",
    "CORRECTIONAL_FACILITY_CONFINEMENT_CELLS": "correctional facilities - confinement cells",
    "CORRECTIONAL_FACILITY_DINING_AREA": "correctional facilities - dining",
    # DORM
    "DORMITORY_LIVING_QUARTERS": "dormitory - living quarters",
    # VISUALLY IMPAIRED
    "FACILITY_FOR_VISUALLY_IMPAIRED_CHAPEL": "visually impaired - chapel",
    "FACILITY_FOR_VISUALLY_IMPAIRED_CORRIDOR": "visually impaired - corridor",
    "FACILITY_FOR_VISUALLY_IMPAIRED_DINING": "visually impaired - dining",
    "FACILITY_FOR_VISUALLY_IMPAIRED_LOBBY": "lobby for visually impared",
    "FACILITY_FOR_VISUALLY_IMPAIRED_RECREATION_ROOM": "visually impaired - recreation room",
    "FACILITY_FOR_VISUALLY_IMPAIRED_RESTROOM": "restroom - visually impaired",
    # FIRE STATION
    "FIRE_STATION_SLEEPING_QUARTERS": "firestation - sleeping quarters",
    # GYM
    "GYMNASIUM_FITNESS_CENTER_EXERCISE_AREA": "gymnsasium exercise area",
    "GYMNASIUM_FITNESS_CENTER_PLAYING_AREA": "gymnasium playing area",
    # HEALTHCARE
    "HEALTHCARE_FACILITY_CONTROL_ROOM": "health care - control room",
    "HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM": "health care - exam/treatment",
    "HEALTHCARE_FACILITY_HOSPITAL_CORRIDOR": "health care - corridor",
    "HEALTHCARE_FACILITY_LOUNGE": "health care - lounge",
    "HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM": "health care - medical supply",
    "HEALTHCARE_FACILITY_NURSERY": "health care - nursery",
    "HEALTHCARE_FACILITY_NURSES_STATION": "health care - nurses station",
    "HEALTHCARE_FACILITY_OPERATING_ROOM": "health care - operating room",
    "HEALTHCARE_FACILITY_PATIENT_ROOM": "health care - patient room",
    "HEALTHCARE_FACILITY_PHYSICAL_THERAPY_ROOM": "health care - physical therapy",
    "HEALTHCARE_FACILITY_RECOVERY_ROOM": "health care - recovery",
    "HEALTHCARE_FACILITY_TELEMEDICINE": "health care - telemedicine",
    # LIBRARY
    "LIBRARY_READING_AREA": "library - reading",
    "LIBRARY_STACKS": "library - stacks",
    # MANUFACTURING
    "MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA": "detailed manufacuring",
    "MANUFACTURING_FACILITY_LOW_BAY_AREA": "manufacturing low bay",
    "MANUFACTURING_FACILITY_HIGH_BAY_AREA": "manufacturing high bay",
    "MANUFACTURING_FACILITY_EXTRA_HIGH_BAY_AREA": "manufacturing extra high bay",
    # MUSEUM
    "MUSEUM_GENERAL_EXHIBITION_AREA": "museum exhibit area",
    "MUSEUM_RESTORATION_ROOM": "museum restoration",
    # PERFORMING ARTS
    "PERFORMING_ARTS_THEATER_DRESSING_ROOM": "performing arts theater - dressing room",
    # POST OFFICE
    "POST_OFFICE_SORTING_AREA": "post office - sorting area",
    # RELIGIOUS
    "RELIGIOUS_FACILITY_AUDIENCE_SEATING_AREA": "religious facility - audience seating",
    "RELIGIOUS_FACILITY_FELLOWSHIP_HALL": "religious facility - fellowship hall",
    "RELIGIOUS_FACILITY_WORSHIP_PULPIT_CHOIR_AREA": "religious facility - worship/pulpit/choir area",
    # RETAIL
    "RETAIL_FACILITIES_DRESSING_FITTING_ROOM": "retail - dressing room",
    "RETAIL_FACILITIES_HAIR_CARE": "retail - hair care",
    "RETAIL_FACILITIES_MANICURE_PEDICURE": "retail - manicure/pedicure",
    "RETAIL_FACILITIES_MALL_CONCOURSE": "retail - mall concourse",
    "RETAIL_FACILITIES_MASSAGE": "retail - massage",
    # SPORTS ARENA
    "SPORTS_ARENA_PLAYING_AREA_CLASS_I_FACILITY": "sports arena playing area, class I",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_II_FACILITY": "sports arena playing area, class II",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_III_FACILITY": "sports arena playing area, class III",
    "SPORTS_ARENA_PLAYING_AREA_CLASS_IV_FACILITY": "sports arena playing area, class IV",
    # NATATORIUM
    "NATATORIUM_CLASS_I_FACILITY": "natatorium, class I",
    "NATATORIUM_CLASS_II_FACILITY": "natatorium, class II",
    "NATATORIUM_CLASS_III_FACILITY": "natatorium, class III",
    "NATATORIUM_CLASS_IV_FACILITY": "natatorium, class IV",
    # TRANSPORTATION
    "TRANSPORTATION_FACILITY_AIRPORT_HANGER": "airport hanger",
    "TRANSPORTATION_FACILITY_BAGGAGE_CAROUSEL_AREA": "baggage/carousel",
    "TRANSPORTATION_FACILITY_AIRPORT_CONCOURSE": "airport concourse",
    "TRANSPORTATION_FACILITY_PASSENGER_LOADING_AREA": "passenger loading",
    "TRANSPORTATION_FACILITY_TICKET_COUNTER": "ticket counter",
    # WAREHOUSE
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
    lpd_space_type = lighting_space_enumeration_to_prm_lpd_map[lighting_space_type]

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
