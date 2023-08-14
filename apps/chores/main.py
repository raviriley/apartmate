from __future__ import print_function

from chores.utils import contacts, get_current_week_chores, gmail_send_message

def main() -> None:
    """Every week, a new chore should be assigned to each person."""
    current_week_chores = get_current_week_chores()
    assert len(current_week_chores) == len(
        contacts
    ), "Chores and contacts lists must be the same length (assuming 1 chore per person)"
    for i in range(len(contacts)):
        contact = list(contacts.keys())[i]  # get ith contact
        subject = current_week_chores[i]["subject"]
        instructions = current_week_chores[i]["instructions"]
        task = instructions.split("\n")[1]
        print(f"{contact}: {subject} {task}")
        gmail_send_message(contacts[contact], subject, instructions)


def demo() -> None:
    """Demo sending a chore to a single contact + me."""
    demo_contact = "2135053061@tmomail.net"  # Terry
    demo_chores = get_current_week_chores()[1:3]
    for chore in demo_chores:
        gmail_send_message(demo_contact, chore["subject"], chore["instructions"])
        gmail_send_message(contacts["Ravi"], chore["subject"], chore["instructions"])


if __name__ == "__main__":
    # main()
    demo()
