import asyncio
import datetime

from dateutil.relativedelta import relativedelta


class Plural:
    def __init__(self, value):
        self.value = value

    def __format__(self, format_spec):
        singular, _, plural = format_spec.partition("|")

        if not plural:
            plural = f"{singular}s"

        if abs(self.value) != 1:
            return f"{self.value} {plural}"
        else:
            return f"{self.value} {singular}"


def human_join(seq, *, delimiter=", ", final="and"):
    if not seq:
        return ""

    if len(seq) == 1:
        return str(seq[0])

    return f"{delimiter.join(map(str, seq[:-1]))} {final} {seq[-1]}"


def human_time(end, *, source=None, accuracy=2, brief=False, suffix=True):
    now = source or datetime.datetime.now(datetime.timezone.utc)

    if isinstance(end, datetime.timedelta):
        end = now + end

    now = now.replace(tzinfo=now.tzinfo or datetime.timezone.utc, microsecond=0)
    end = end.replace(tzinfo=end.tzinfo or datetime.timezone.utc, microsecond=0)

    if end > now:
        delta = relativedelta(end, now)
        affix = ""
    else:
        delta = relativedelta(now, end)
        affix = " ago" if suffix else ""

    units = [
        ("year", "y"),
        ("month", "M"),
        ("day", "d"),
        ("hour", "h"),
        ("minute", "m"),
        ("second", "s"),
    ]

    result = []
    for unit, brief_unit in units:
        value = getattr(delta, unit + "s")

        if not value:
            continue

        if brief:
            result.append(f"{value}{brief_unit}")
        else:
            result.append(format(Plural(value), unit))

    if accuracy:
        result = result[:accuracy]

    if not result:
        return "now"

    return " ".join(result) + affix if brief else human_join(result) + affix


async def fetch_recent_audit_log_entry(guild, *, target=None, action=None, retry=0):
    while retry >= 0:
        async for entry in guild.audit_logs(limit=1, action=action):
            delta = datetime.datetime.now(datetime.timezone.utc) - entry.created_at
            if delta < datetime.timedelta(seconds=10):
                if target is None or entry.target == target:
                    return entry

        await asyncio.sleep(2.5)
        retry -= 1

    return None
