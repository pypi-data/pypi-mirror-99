
def get_atlas(secrets=None):
    from lumipy.client import Client
    return Client(secrets).get_atlas()


def get_client(secrets=None):
    from lumipy.client import Client
    return Client(secrets)


def get_drive(secrets=None):
    from lumipy.client import Client
    return Client(secrets).get_atlas().get_drive()


def datetime_now(delta_days: int = 0):
    """Get a scalar variable representing the current date with an optional offset

    Args:
        delta_days (int): time delta in days

    Returns:
        DateTimeScalar: Datetime scalar variable expression
    """
    from lumipy.query.expression.variable.scalar_variable import DateTimeScalar
    return DateTimeScalar('now', delta_days)


def date_now(delta_days: int = 0):
    """Get a scalar variable representing the current datetime with an optional offset

    Args:
        delta_days: time delta in days

    Returns:
        DateScalar: Date scalar variable expression
    """
    from lumipy.query.expression.variable.scalar_variable import DateScalar
    return DateScalar('now', delta_days)
