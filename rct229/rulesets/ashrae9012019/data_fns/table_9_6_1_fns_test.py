from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_9_6_1_fns import (
    space_type_enumeration_to_lpd_map,
    table_9_6_1_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_utils import (
    check_enumeration_to_osstd_match_field_value_map,
)
from rct229.schema.config import ureg

watts_per_ft2 = ureg("watt / foot**2")


# Testing table_9_6_1------------------------------------------
def test__table_9_6_1_guest_room():
    assert table_9_6_1_lookup("GUEST_ROOM") == {"lpd": 0.41 * watts_per_ft2}


def test__table_9_6_1_dormitory():
    assert table_9_6_1_lookup("DORMITORY_LIVING_QUARTERS") == {
        "lpd": 0.50 * watts_per_ft2
    }


# Testing building_type_enumeration_to_lpd_map ----------
def test__building_type_enumeration_to_lpd_map():
    # check_enumeration_to_osstd_match_field_value_map() will throw exception(s)
    # when a check fails
    check_enumeration_to_osstd_match_field_value_map(
        match_field_name="space_type",
        enum_type="LightingSpaceOptions2019ASHRAE901TG37",
        osstd_table=data["ashrae_90_1_table_9_6_1"],
        enumeration_to_match_field_value_map=space_type_enumeration_to_lpd_map,
        exclude_enum_names=[
            "ATRIUM_LOW_MEDIUM",
            "ATRIUM_HIGH",
            "AUDIENCE_SEATING_AREA_AUDITORIUM",
            "AUDIENCE_SEATING_AREA_CONVENTION_CENTER",
            "AUDIENCE_SEATING_AREA_EXERCISE_CENTER",
            "AUDIENCE_SEATING_AREA_GYMNASIUM",
            "AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER",
            "AUDIENCE_SEATING_AREA_PENITENTIARY",
            "AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER",
            "AUDIENCE_SEATING_AREA_RELIGIOUS_FACILITY",
            "AUDIENCE_SEATING_AREA_SPORTS_ARENA",
            "AUDIENCE_SEATING_AREA_TRANSPORTATION_FACILITY",
            "AUDIENCE_SEATING_AREA_ALL_OTHER",
            "BANKING_ACTIVITY_AREA",
            "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY",
            "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL",
            "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER",
            "CONFERENCE_MEETING_MULTIPURPOSE_ROOM",
            "CONFINEMENT_CELLS",
            "COPY_PRINT_ROOM",
            "CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED",
            "CORRIDOR_HOSPITAL",
            "CORRIDOR_MANUFACTURING_FACILITY",
            "CORRIDOR_ALL_OTHERS",
            "COURT_ROOM",
            "COMPUTER_ROOM",
            "DINING_AREA_PENITENTIARY",
            "DINING_AREA_FACILITY_FOR_THE_VISUALLY_IMPAIRED",
            "DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING",
            "DINING_AREA_CAFETERIA_OR_FAST_FOOD_DINING",
            "DINING_AREA_FAMILY_DINING",
            "DINING_AREA_ALL_OTHERS",
            "ELECTRICAL_MECHANICAL_ROOM",
            "EMERGENCY_VEHICLE_GARAGE",
            "FOOD_PREPARATION_AREA",
            "JUDGES_CHAMBERS",
            "DWELLING_UNIT",
            "LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM",
            "LAUNDRY_WASHING_AREA",
            "LOADING_DOCK_INTERIOR",
            "LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED",
            "LOBBY_ELEVATOR",
            "LOBBY_HOTEL",
            "LOBBY_MOTION_PICTURE_THEATER",
            "LOBBY_PERFORMING_ARTS_THEATER",
            "LOBBY_ALL_OTHERS",
            "LOCKER_ROOM",
            "LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY",
            "LOUNGE_BREAKROOM_ALL_OTHERS",
            "OFFICE_ENCLOSED",
            "OFFICE_OPEN_PLAN",
            "PARKING_AREA_INTERIOR",
            "PHARMACY_AREA",
            "RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED",
            "RESTROOM_ALL_OTHERS",
            "SALES_AREA",
            "SEATING_AREA_GENERAL",
            "STAIRWELL",
            "STORAGE_ROOM_HOSPITAL",
            "STORAGE_ROOM_SMALL",
            "STORAGE_ROOM_LARGE",
            "VEHICULAR_MAINTENANCE_AREA",
            "WORKSHOP",
            "ASSISTED_LIVING_FACILITY_CHAPEL",
            "ASSISTED_LIVING_FACILITY_RECREATION_ROOM_COMMON_LIVING_ROOM",
            "CONVENTION_CENTER_EXHIBIT_SPACE",
            "FIRE_STATION_SLEEPING_QUARTERS",
            "GYMNASIUM_FITNESS_CENTER_EXERCISE_AREA",
            "GYMNASIUM_FITNESS_CENTER_PLAYING_AREA",
            "HEALTHCARE_FACILITY_EMERGENCY_ROOM",
            "HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM",
            "HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM",
            "HEALTHCARE_FACILITY_NURSERY",
            "HEALTHCARE_FACILITY_NURSES_STATION",
            "HEALTHCARE_FACILITY_OPERATING_ROOM",
            "HEALTHCARE_FACILITY_PATIENT_ROOM",
            "HEALTHCARE_FACILITY_PHYSICAL_THERAPY_ROOM",
            "HEALTHCARE_FACILITY_RECOVERY_ROOM",
            "LIBRARY_READING_AREA",
            "LIBRARY_STACKS",
            "MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA",
            "MANUFACTURING_FACILITY_EQUIPMENTROOM",
            "MANUFACTURING_FACILITY_EXTRA_HIGH_BAY_AREA",
            "MANUFACTURING_FACILITY_HIGH_BAY_AREA",
            "MANUFACTURING_FACILITY_LOW_BAY_AREA",
            "MUSEUM_GENERAL_EXHIBITION_AREA",
            "MUSEUM_RESTORATION_ROOM",
            "POST_OFFICE_SORTING_AREA",
            "RELIGIOUS_FACILITY_FELLOWSHIP_HALL",
            "RELIGIOUS_FACILITY_WORSHIP_PULPIT_CHOIR_AREA",
            "RETAIL_FACILITIES_DRESSING_FITTING_ROOM",
            "RETAIL_FACILITIES_MALL_CONCOURSE",
            "SPORTS_ARENA_PLAYING_AREA_CLASS_I_FACILITY",
            "SPORTS_ARENA_PLAYING_AREA_CLASS_II_FACILITY",
            "SPORTS_ARENA_PLAYING_AREA_CLASS_III_FACILITY",
            "SPORTS_ARENA_PLAYING_AREA_CLASS_IV_FACILITY",
            "TRANSPORTATION_FACILITY_BAGGAGE_CAROUSEL_AREA",
            "TRANSPORTATION_FACILITY_AIRPORT_CONCOURSE",
            "TRANSPORTATION_FACILITY_TICKET_COUNTER",
            "WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS",
            "WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS",
        ],
    )
