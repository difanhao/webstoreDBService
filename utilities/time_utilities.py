import time

# 根据时间单位转换间隔值为秒
time_multipliers = {
    "seconds": 1,
    "minutes": 60,
    "hours": 3600,
    "days": 86400
}

def is_within_timestamp_interval(timestamp, interval_value, unit="seconds"):
    """
    检查时间戳与当前时间的间隔是否在指定的时间单位内。
    :param timestamp: float，时间戳
    :param interval_value: int，允许的时间间隔
    :param unit:  str，时间单位，可以是 "seconds", "minutes", "hours", 或 "days"。默认为 "seconds"。
    :return: bool
    """

    if unit not in time_multipliers:
        raise ("无效的unit. 请用 'seconds', 'minutes', 'hours', or 'days'.")

    interval_in_seconds = interval_value * time_multipliers[unit]

    current_timestamp = time.time()
    difference = current_timestamp - timestamp

    return difference <= interval_in_seconds


def set_timestamp(timestamp, interval_value, unit="seconds", direction="forward"):
    """
    设置给定时间戳
    :param timestamp: float，时间戳
    :param interval_value: int，允许的时间间隔
    :param unit:  str，时间单位，可以是 "seconds", "minutes", "hours", 或 "days"。默认为 "seconds"。
    :param direction: str, 时间方向，可以是 "forward"向后 或 "backward"向前. 默认为 "forward".
    :return: bool
    """
    if unit not in time_multipliers:
        raise ValueError("无效的unit. 请用 'seconds', 'minutes', 'hours', or 'days'.")

    interval_in_seconds = interval_value * time_multipliers[unit]

    if direction == "forward":
        return timestamp + interval_in_seconds
    elif direction == "backward":
        return timestamp - interval_in_seconds
    else:
        raise ValueError("无效的direction. 请用 'forward' 或 'backward'.")
