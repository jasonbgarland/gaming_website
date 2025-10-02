"""
IGDB API enumeration constants.

This module contains ID mappings for various IGDB entities to make
filtering more readable and maintainable.

Data fetched from IGDB API endpoints on 2025-10-01.
"""


# Platform IDs
# pylint: disable=too-few-public-methods
class Platform:
    """IGDB Platform IDs"""

    # Popular modern platforms
    PC = 6
    PLAYSTATION_4 = 48
    PLAYSTATION_5 = 167
    XBOX_ONE = 49
    XBOX_SERIES_X = 169
    NINTENDO_SWITCH = 130

    # Legacy platforms
    LINUX = 3
    PLAYSTATION_2 = 8
    PLAYSTATION_3 = 9
    XBOX = 11
    XBOX_360 = 12

    # Mobile platforms
    IOS = 39
    ANDROID = 34

    # Handheld platforms
    NINTENDO_DS = 20
    PLAYSTATION_VITA = 46
    GAME_BOY_ADVANCE = 24

    # VR platforms
    OCULUS_VR = 162
    STEAMVR = 163
    PLAYSTATION_VR = 165
    PLAYSTATION_VR2 = 390


# Genre IDs
# pylint: disable=too-few-public-methods
class Genre:
    """IGDB Genre IDs"""

    # Action genres
    FIGHTING = 4
    SHOOTER = 5
    HACK_AND_SLASH = 25

    # RPG genres
    RPG = 12
    ADVENTURE = 31
    VISUAL_NOVEL = 34

    # Strategy genres
    STRATEGY = 15
    REAL_TIME_STRATEGY = 11  # RTS
    TURN_BASED_STRATEGY = 16  # TBS
    TACTICAL = 24
    MOBA = 36

    # Other popular genres
    PLATFORM = 8
    PUZZLE = 9
    RACING = 10
    SIMULATOR = 13
    SPORT = 14
    MUSIC = 7
    ARCADE = 33
    INDIE = 32
    PINBALL = 30
    CARD_AND_BOARD_GAME = 35
    QUIZ_TRIVIA = 26
    POINT_AND_CLICK = 2


# Theme IDs
# pylint: disable=too-few-public-methods
class Theme:
    """IGDB Theme IDs"""

    HORROR = 19
    FANTASY = 17
    SCIENCE_FICTION = 18

    # Other popular themes
    ACTION = 1
    THRILLER = 20
    SURVIVAL = 21
    HISTORICAL = 22
    STEALTH = 23
    COMEDY = 27
    BUSINESS = 28
    DRAMA = 31
    NON_FICTION = 32
    SANDBOX = 33
    EDUCATIONAL = 34
    KIDS = 35
    OPEN_WORLD = 38
    WARFARE = 39
    PARTY = 40
    FOUR_X = 41  # 4X (explore, expand, exploit, and exterminate)
    EROTIC = 42
    MYSTERY = 43
    ROMANCE = 44


# Player Perspective IDs
# pylint: disable=too-few-public-methods
class PlayerPerspective:
    """IGDB Player Perspective IDs"""

    FIRST_PERSON = 1
    THIRD_PERSON = 2
    BIRD_VIEW = 3
    SIDE_VIEW = 4
    TEXT = 5
    AUDITORY = 6
    VIRTUAL_REALITY = 7


# Game Mode IDs
# pylint: disable=too-few-public-methods
class GameMode:
    """IGDB Game Mode IDs"""

    SINGLE_PLAYER = 1
    MULTIPLAYER = 2
    CO_OPERATIVE = 3
    SPLIT_SCREEN = 4
    MMO = 5
    BATTLE_ROYALE = 6


# Age Rating Category IDs (for age_ratings endpoint)
# pylint: disable=too-few-public-methods
class AgeRatingCategory:
    """IGDB Age Rating Category IDs (ESRB, PEGI, etc.)"""

    ESRB = 1
    PEGI = 2
    CERO = 3
    USK = 4
    GRAC = 5
    CLASS_IND = 6
    ACB = 7


# Release Status IDs
# pylint: disable=too-few-public-methods
class ReleaseStatus:
    """IGDB Release Status IDs"""

    RELEASED = 0
    ALPHA = 2
    BETA = 3
    EARLY_ACCESS = 4
    OFFLINE = 5
    CANCELLED = 6
    RUMORED = 7
    DELISTED = 8


# Common Keywords (only most useful ones due to large number)
# pylint: disable=too-few-public-methods
class Keyword:
    """Common IGDB Keyword IDs"""

    OPEN_WORLD = 270

    # Note: IGDB has thousands of keywords. For less common keywords,
    # use the IGDB API search functionality rather than hardcoding here.
    # Common ones can be added as we validate them through testing.


# Convenience collections for filtering
# pylint: disable=too-few-public-methods
class PopularPlatforms:
    """Popular platform collections for easy filtering"""

    CURRENT_GEN = [
        Platform.PC,
        Platform.PLAYSTATION_5,
        Platform.XBOX_SERIES_X,
        Platform.NINTENDO_SWITCH,
    ]
    LAST_GEN = [Platform.PLAYSTATION_4, Platform.XBOX_ONE]
    PC_FAMILY = [Platform.PC, Platform.LINUX]
    PLAYSTATION_FAMILY = [
        Platform.PLAYSTATION_2,
        Platform.PLAYSTATION_3,
        Platform.PLAYSTATION_4,
        Platform.PLAYSTATION_5,
    ]
    XBOX_FAMILY = [
        Platform.XBOX,
        Platform.XBOX_360,
        Platform.XBOX_ONE,
        Platform.XBOX_SERIES_X,
    ]
    MOBILE = [Platform.IOS, Platform.ANDROID]
    VR = [
        Platform.OCULUS_VR,
        Platform.STEAMVR,
        Platform.PLAYSTATION_VR,
        Platform.PLAYSTATION_VR2,
    ]


# pylint: disable=too-few-public-methods
class PopularGenres:
    """Popular genre collections for easy filtering"""

    ACTION_GAMES = [Genre.FIGHTING, Genre.SHOOTER, Genre.HACK_AND_SLASH]
    RPG_GAMES = [Genre.RPG, Genre.ADVENTURE, Genre.VISUAL_NOVEL]
    STRATEGY_GAMES = [
        Genre.STRATEGY,
        Genre.REAL_TIME_STRATEGY,
        Genre.TURN_BASED_STRATEGY,
        Genre.TACTICAL,
    ]
    CASUAL_GAMES = [Genre.PUZZLE, Genre.PLATFORM, Genre.ARCADE, Genre.MUSIC]
