import itertools
from datetime import date, datetime
from typing import List, Optional, TypedDict

START_DATE = date(2023, 6, 1)
START_DATE_WEEK_NUM = int(START_DATE.strftime("%V"))


class Chore(TypedDict):  # TODO: use namedtuple instead?
    """Chore data structure"""

    subject: str
    instructions: str


bathroom_chores = [
    (
        "Sink & Mirror",
        "\n1. Wipe down the counters with paper towels\n"
        "\n2. Scrub the sink and faucets with Clorox wipes\n"
        "(Ensure you pick things up so that no surface is left uncleaned)\n"
        "\n3. Wipe down the mirror with Windex and paper towels",
    ),
    (
        "Toilet",
        "\n1. Apply toilet bowl cleaner to the underside of the bowl's rim\n"
        "\n2. Wipe down the flush handle and the entire outside of the toilet with Clorox wipes\n"
        "\n3. Scrub the bowl clean with the toilet brush. Flush\n"
        "\n4. Wipe down the top and bottom of the toilet seat and lid with a fresh Clorox wipe",
    ),
    (
        "Shower & Floor",
        "\n1. Wipe down the top of the tub with paper towels if wet\n"
        "\n2. Scrub the tub top surface with Clorox wipes, removing any visible mold/mildew\n"
        "\n3. Swiffer or vacuum the floor",
    ),
]

bathroom: List[Chore] = [
    {
        "subject": f"Floor {i} Bathroom",
        "instructions": f"\n{chore[0]}\n{chore[1]}",
    }
    for i, chore in itertools.product(range(1, 4), bathroom_chores)
]

common_areas: List[Chore] = [
    {
        "subject": "Kitchen",
        "instructions": "\nTake out the trash"
        "\n1. Empty all the trash and recycling into the bins outside\n"
        "\n2. Take the bins to the curb\n"
        "\n3. Replace the trash bags\n"
        "\nNOTE: Unlike the flexibilty of the other chores, this one must be done Sunday night. "
        "The bins are collected Monday morning.",
    },
    {
        "subject": "Downstairs",
        "instructions": "\nFloors"
        "\n1. Swiffer/vacuum the living room and kitchen floors"
        "\n2. Empty the vacuum into the trash",
    },
]


weekly_chores: List[Chore] = bathroom + common_areas

# floor  1 2 3:
#        -----
# sink   0 3 6
# toilet 1 4 7
# shower 2 5 8
#        -----
# trash  9
# floors 10
optimal_bathroom_order = [0, 5, 7, 9, 3, 1, 8, 10, 4, 6, 2]
# current order:
# floor 1 sink, floor 2 shower, floor 3 toilet, take out trash,
# floor 2 sink, floor 1 toilet, # floor 3 shower, vacuum the floors,
# floor 2 toilet, floor 3 sink, floor 1 shower (repeat)

weekly_chores = [weekly_chores[i] for i in optimal_bathroom_order]  # chores in optimal order


def rotate_list(lst: list, n: int = 1) -> list:
    """Rotate a list by n positions, so that the nth item is now the first item"""
    n %= len(lst)
    return lst[-n:] + lst[:-n]


def get_current_week_chores(week_num: Optional[int] = None) -> list:
    """Get the list of chores for the current week"""
    current_week_num = int(datetime.now().strftime("%V")) - START_DATE_WEEK_NUM
    if week_num is not None:
        current_week_num = week_num
    return rotate_list(weekly_chores, current_week_num)
