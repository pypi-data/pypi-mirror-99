"""Genshinstats errors."""
class GenshinStatsException(Exception):
    """Base error for all Genshin Stats Errors."""
class InvalidUID(GenshinStatsException):
    """UID is not valid."""
class InvalidDS(GenshinStatsException):
    """Invalid DS token, should be renewed."""
class NotLoggedIn(GenshinStatsException):
    """Cookies have not been provided."""
class DataNotPublic(GenshinStatsException):
    """User has not allowed their data to be seen."""
class InvalidScheduleType(GenshinStatsException):
    """Invalid Spiral Abyss schedule"""
class CannotCheckIn(GenshinStatsException):
    """Could not check in."""
class InvalidItemID(GenshinStatsException):
    """Item does not exist."""


class GenshinGachaLogException(GenshinStatsException):
    """Base GenshinGachaLog Exception."""
class AuthKeyError(GenshinStatsException):
    """Authkey error."""
class AuthKeyTimeout(GenshinStatsException):
    """Authkey timeout."""
class BadGachaType(GenshinStatsException):
    """Base GenshinGachaLog Exception."""
class MissingAuthKey(GenshinStatsException):
    """No gacha authkey was provided."""

class AlreadySignedIn(GenshinStatsException):
    """Already signed in dailies"""
class FirstSignIn(GenshinStatsException):
    """First sign in must be done manually."""
class NoGameAccount(GenshinStatsException):
    """Tried to get info without an account"""