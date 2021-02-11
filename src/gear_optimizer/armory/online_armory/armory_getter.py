import requests

from gear_optimizer.armory.online_armory import items_quantity_parser


def get_quantity_and_armory(session_identifier: str):
    with requests.Session() as session:
        session.cookies.set('__Identyfikator_sesji', session_identifier)
        main_armory_page = _get_page_content(session, 'https://i-rpg.net/guilds.php?op=viewmy&chamber=armorroom')
        quantity = items_quantity_parser.parse_armory_room_file(main_armory_page)
        armory_manager_page = _get_page_content(session,
                                                'https://i-rpg.net/guilds.php?op=viewmy&chamber=armorroom&a=manage')
        return quantity, armory_manager_page


def _get_page_content(session: requests.Session, url: str):
    response = session.get(url)
    return response.text
