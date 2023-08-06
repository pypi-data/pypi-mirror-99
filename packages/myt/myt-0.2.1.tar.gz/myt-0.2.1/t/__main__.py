import sys
import os
import logging
import datetime
import json
import click
import pytz
import dateparser
import t

W = "\033[0m"  # white (normal)
R = "\033[31m"  # red
G = "\033[32m"  # green
O = "\033[33m"  # orange
B = "\033[34m"  # blue
P = "\033[35m"  # purple

DEFAULT_ZONES = [
    "Europe/Copenhagen",
    "UTC",
    "US/Eastern",
    "US/Central",
    "US/Mountain",
    "America/Phoenix",
    "US/Pacific",
    "US/Alaska",
    "Pacific/Tahiti",
    "Pacific/Auckland",
    "Australia/Sydney",
]

def _dtDeltaHours(td):
    return td.seconds/3600.0 + td.days*24.0

def _hrsToHHMM(hrs):
    hh = int(hrs)
    mm = int(60*abs(hrs-hh))
    return hh,mm

def _printRow(row, t_format):
    tz = row[0]
    line = f"{tz:17}"
    for v in row[1:]:
        if v.hour < 6 or v.hour > 18:
            sv = f" {B}{v.strftime(t_format)}{W}"
        else:
            sv = f" {O}{v.strftime(t_format)}{W}"
        line = line + sv
    line += W
    return line


@click.group()
@click.option(
    "-F",
    "--outformat",
    "out_format",
    type=click.Choice(["text", "json"],case_sensitive=False),
    default="text",
    help="Output format (text | json)",
)
@click.pass_context
def main(ctx, out_format):
    ctx.ensure_object(dict)
    ctx.obj["format"] = out_format
    return 0


@main.command("zones", help="List common time zones and UTC offset (on date)")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.pass_context
def listTimeZones(ctx, date_str):
    if date_str is None:
        for_date = datetime.datetime.now()
    else:
        for_date = dateparser.parse(
            date_str
        )
    res = []
    for tz in pytz.common_timezones:
        z = pytz.timezone(tz)
        ofs = z.utcoffset(for_date)
        res.append((_dtDeltaHours(ofs), z.zone))
    res.sort()
    if ctx.obj['format'] == 'json':
        print(json.dumps(res))
        return 0
    for row in res:
        hh,mm = _hrsToHHMM(row[0])
        print(f"{hh:+03d}:{mm:02} {row[1]}")
    return 0


@main.command("z", help="24hrs in time zones (on date)")
@click.option("-f", "--format", "t_format", default="%H", help="Output time format")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.option(
    "-z",
    "--zones",
    "zone_list",
    default=",".join(DEFAULT_ZONES),
    help="Comma separated list of timezones",
)
@click.pass_context
def showZones(ctx, t_format, date_str, zone_list):
    if date_str is None:
        for_date = datetime.datetime.now().astimezone()
    else:
        for_date = dateparser.parse(
            date_str, settings={"RETURN_AS_TIMEZONE_AWARE": True}
        )
    zone_list = zone_list.split(",")
    t_zones = []
    for tz in zone_list:
        t_zones.append(pytz.timezone(tz.strip()))
    res = t.generateDayMatrix(t_zones, for_date)
    if ctx.obj["format"] == "json":
        print(json.dumps(res, default=t._jsonConverter))
        return 0
    print(_printRow(res[0], t_format))
    for row in res[1:]:
        print(_printRow(row, t_format))
    return 0

@main.command("t", help="Time in different zones")
@click.option("-t", "--date", "date_str", default=None, help="Date for calculation")
@click.option(
    "-z",
    "--zones",
    "zone_list",
    default=",".join(DEFAULT_ZONES),
    help="Comma separated list of timezones",
)
@click.pass_context
def showTimes(ctx, date_str, zone_list):
    if date_str is None:
        for_date = datetime.datetime.now().astimezone()
    else:
        for_date = dateparser.parse(
            date_str, settings={"RETURN_AS_TIMEZONE_AWARE": True}
        )
    zone_list = zone_list.split(",")
    res = [
        ('Local', for_date.astimezone()),
    ]
    for tzstr in zone_list:
        tz = pytz.timezone(tzstr.strip())
        dt = for_date.astimezone(tz)
        res.append((tz.zone, dt))
    if ctx.obj["format"] == "json":
        print(json.dumps(res, default=t._jsonConverter))
        return 0
    for row in res:
        print(f"{row[0]:17} {t.datetimeToJsonStr(row[1])}")

if __name__ == "__main__":
    sys.exit(main(auto_envvar_prefix="T"))