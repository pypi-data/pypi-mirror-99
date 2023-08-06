"""GET endpoints for blaseball /database/ path.

Based off spec: https://github.com/Society-for-Internet-Blaseball-Research/blaseball-api-spec
"""
from blaseball_mike.session import session, check_network_response, TIMESTAMP_FORMAT
from datetime import datetime

BASE_URL = 'https://www.blaseball.com/database'
BASE_GITHUB = 'https://raw.githubusercontent.com/xSke/blaseball-site-files/main/data'


def get_global_events():
    s = session(5)
    res = s.get(f'{BASE_URL}/globalEvents')
    return check_network_response(res)


def get_all_teams():
    """
    Returns dictionary keyed by team ID
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/allTeams')
    return {t['id']: t for t in check_network_response(res)}


def get_all_divisions():
    """
    Returns dictionary keyed by division ID
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/allDivisions')
    return {d['id']: d for d in check_network_response(res)}


def get_league(id_='d8545021-e9fc-48a3-af74-48685950a183'):
    s = session(5)
    res = s.get(f'{BASE_URL}/league?id={id_}')
    return check_network_response(res)


def get_subleague(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/subleague?id={id_}')
    return check_network_response(res)


def get_division(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/division?id={id_}')
    return check_network_response(res)


def get_team(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/team?id={id_}')
    return check_network_response(res)


def get_player(id_):
    """
    Accepts single string id_, comma separated string, or list.
    Returns a dictionary with ID as key
    """
    if len(id_) == 0:
        return {}
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(5)
    res = s.get(f'{BASE_URL}/players?ids={id_}')
    return {p['id']: p for p in check_network_response(res)}


def get_games(season, day):
    """
    Season and day will be 1 indexed.
    Returns as dictionary with game ID as key.
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/games?season={season - 1}&day={day - 1}')
    return {g['id']: g for g in check_network_response(res)}


def get_tournament(tournament, day):
    """
    Day will be 1 indexed. Tournament is 0 indexed.
    Returns as dictionary with game ID as key.
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/games?tournament={tournament}&day={day - 1}')
    return {g['id']: g for g in check_network_response(res)}


def get_game_by_id(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/gameById/{id_}')
    return check_network_response(res)


def get_offseason_election_details():
    s = session(5)
    res = s.get(f'{BASE_URL}/offseasonSetup')
    return check_network_response(res)


def get_offseason_recap(season):
    """
    Season will be 1 indexed.
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/offseasonRecap?season={season - 1}')
    return check_network_response(res)


def get_offseason_bonus_results(id_):
    """
    id_ can be a single string ID, comma separated string, or list.
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(5)
    res = s.get(f'{BASE_URL}/bonusResults?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_offseason_decree_results(id_):
    """
    id_ can be a single string ID, comma separated string, or list.
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(5)
    res = s.get(f'{BASE_URL}/decreeResults?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_offseason_event_results(id_):
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(5)
    res = s.get(f'{BASE_URL}/eventResults?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_playoff_details(season):
    """
    Season will be 1 indexed.
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/playoffs?number={season - 1}')
    return check_network_response(res)


def get_playoff_round(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/playoffRound?id={id_}')
    return check_network_response(res)


def get_playoff_matchups(id_):
    """
    id_ can be a single string ID, comma separated string, or list.
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(5)
    res = s.get(f'{BASE_URL}/playoffMatchups?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_standings(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/standings?id={id_}')
    return check_network_response(res)


def get_season(season_number):
    """
    Season number is 1 indexed
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/season?number={season_number - 1}')
    return check_network_response(res)


def get_tiebreakers(id):
    s = session(5)
    res = s.get(f'{BASE_URL}/tiebreakers?id={id}')
    return {g['id']: g for g in check_network_response(res)}


def get_game_statsheets(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/gameStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_player_statsheets(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/playerStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_season_statsheets(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/seasonStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_team_statsheets(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/teamStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_idols():
    s = session(5)
    res = s.get('https://www.blaseball.com/api/getIdols')
    return check_network_response(res)


def get_tributes():
    s = session(5)
    res = s.get('https://www.blaseball.com/api/getTribute')
    return check_network_response(res)


def get_simulation_data():
    s = session(5)
    res = s.get(f'{BASE_URL}/simulationData')
    return check_network_response(res)


def get_attributes(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/mods?ids={ids}')
    return check_network_response(res)


def get_items(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/items?ids={ids}')
    return check_network_response(res)


def get_weather():
    s = session(5)
    res = s.get(f'{BASE_GITHUB}/weather.json')
    return check_network_response(res)


def get_blood(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/blood?ids={ids}')
    return check_network_response(res)


def get_coffee(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/coffee?ids={ids}')
    return check_network_response(res)


def get_feed_global(limit=50, sort=None, category=None, start=None):
    """
    Get Global Feed

    Args:
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start

    s = session(5)
    res = s.get(f'{BASE_URL}/feed/global', params=params)
    return check_network_response(res)


def get_feed_game(id_, limit=50, sort=None, category=None, start=None):
    """
    Get Game Feed

    Args:
        id_: Game ID
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"id": id_, "limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start

    s = session(5)
    res = s.get(f'{BASE_URL}/feed/game', params=params)
    return check_network_response(res)


def get_feed_team(id_, limit=50, sort=None, category=None, start=None):
    """
    Get Team Feed

    Args:
        id_: Team ID
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"id": id_, "limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start

    s = session(5)
    res = s.get(f'{BASE_URL}/feed/team', params=params)
    return check_network_response(res)


def get_feed_player(id_, limit=50, sort=None, category=None, start=None):
    """
    Get Player Feed

    Args:
        id_: Player ID
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"id": id_, "limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start

    s = session(5)
    res = s.get(f'{BASE_URL}/feed/player', params=params)
    return check_network_response(res)


def get_feed_phase(season, phase):
    """
    Get Feed by Phase
    """
    s = session(5)
    res = s.get(f'{BASE_URL}/feedbyphase?season={season-1}&phase={phase}')
    return check_network_response(res)


def get_renovations(ids):
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(5)
    res = s.get(f'{BASE_URL}/renovations?ids={ids}')
    return check_network_response(res)


def get_renovation_progress(id_):
    s = session(5)
    res = s.get(f'{BASE_URL}/renovationProgress?id={id_}')
    return check_network_response(res)
