from datetime import datetime
import argparse
def main():
    current = datetime.now()
    zone = current.astimezone()
    offset = int(zone.utcoffset().total_seconds() / 60)
    if offset >= 0:
        sign = "+"
    else:
        sign = "-"
    h = abs(offset) // 60
    m = abs(offset) % 60
    local_utc = f"UTC{sign}{h:02d}:{m:02d}"
    local_date = f"{current.year:04d}-{current.month:02d}-{current.day:02d}"

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", default = local_utc, help="sets source time zone in UTC±XX:XX format, defaults to current time zone. use value current and destination value utc to see your local timezone in utc.")
    parser.add_argument("destination", help="sets destination timezone in UTC±XX:XX format")
    parser.add_argument("--source_time", "-st", help = "set source time in XX:XX format, defaults to local time") 
    parser.add_argument("--date", "-d", default = local_date, help = "set source date, YYYY-MM-DD format, defaults to local date")
    args = parser.parse_args()

    
    if args.destination.lower() == "current":
        offset2 = offset
    else:
        offset2 = offsety(args.destination) #minute offset
    if args.source.lower() == "current" and args.destination == "utc": 
        print(local_utc)
    else:
        if args.source_time == None:
            hour = current.hour
            minute = current.minute
            offset1 = offset
        else:
            if args.source.lower() == "current":
                offset1 = offset
            else:
                offset1 = offsety(args.source) #minute offset
            hour, minute = timey(args.source_time) #parses time into hour and minute
        ct = convert_time(hour, minute, offset1, offset2) #gives day offset, new hour and new minute
        d = args.date
        y, m, dy = datey(d)
        ft = convert(m, y, ct[0], ct[1], ct[2], dy) #gives day, month, year time
        fm = monthination(ft[1])
        print(f"{ft[3]} {fm} {ft[0]}, {ft[2]}")

def monthination(month_number):
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return month[month_number - 1]

#takes in a utc string and converts it to otc offset in minutes, used for convert time
def offsety(utc): 
    # format is like UTC+01:23
    if utc.lower() == "utc":
        return 0
    if len(utc)!= 9 or utc[0:3].lower() != "utc" or utc[3] not in "+-" or utc[6] != ":" or not utc[4:6].isdigit() or not utc[7:9].isdigit() or int(utc[7:9]) >= 60:
        raise ValueError
   
    water = int(utc[4:6])
    o2m = int(utc[7:9])
    if utc[3] == "+":
        offset2 = water * 60 + o2m
    else: 
        offset2 = -water * 60 - o2m
    return offset2

#parses time string into hour and minute
def timey(time):
    if len(time) not in (4, 5) or time.count(":") != 1:
        raise ValueError
    hour, minute = time.split(":")
    if len(hour) not in (1, 2) or len(minute) != 2 or not hour.isdigit() or not minute.isdigit() or not 0 <= int(hour) <= 23 or not 0 <= int(minute) <= 59:
        raise ValueError
    hour = int(hour)
    minute = int(minute)
    return hour, minute

# takes hour, minute, current utc in mins, destinaton utc in mins, give back the day offset, new hour, and new minuted
def convert_time(hour, minute, offset, offset2): #hour and minute of current place, offset 1 is current timezone's deivation form utc, same with offsert 2
    total_minutes = hour * 60 + minute # total mins is the time in minutes. militaryx2? seal team 6 time?
    new_time = total_minutes - offset + offset2
    day = new_time // 1440 #calcs day offset
    new_h = new_time % 1440 // 60 #if day, bye bye. finds hours by dividing to min->hours, then floor cuz decimal is minutes and i no want
    new_m = new_time % 1440 % 60 # bye bye day! ignores hrs by like basically ignoring them kindas [yk what mod does bro] keeps remainer, which is mins
    return day, new_h, new_m #gives back tuple of values

#takes in year and month, returns the days in a the specified month
def day_month_calc(year, month):
    days_in = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0: 
        days_in[1] = 29
    return days_in[month-1]

#takes in month, year, day offset, hour, minute and day; converts time to a tuple containing day number, month number, year number, and time in XX:XX XM format
def convert(month, year, day_off, hour, minute, day):
    monthy = month
    yeary = year
    flow = day + day_off #short for over and underflow!!!!
    fday = flow #format day [w crative?]

    if month == 1 and flow <= 0:
        monthy = 12
        yeary-=1
        fday = flow + day_month_calc(year, 12)

    elif month == 12 and flow > day_month_calc(year, month):
        monthy = 1
        yeary+=1
        fday = flow - day_month_calc(year, month)

    elif flow <= 0:
        monthy-=1
        fday = flow + day_month_calc(year, month-1)

    elif flow > day_month_calc(year, month):
        monthy+=1
        fday = flow - day_month_calc(year, month)

    #uses milatry (absollute) hours
    #we want like 8:45 pm and stiff
    badabumbabum = "AM"
    houry = hour % 12
    if houry == 0:
        houry = 12  
    if hour // 12 == 1:
        badabumbabum = "PM"
    ftime = f"{houry}:{minute:02d} {badabumbabum}"
    return fday, monthy, yeary, ftime

#takes in string date YYYY-MM-DD
def datey(date):
    things = date.split("-")
    if len(things) != 3 or len(things[0]) != 4 or not things[0].isdigit() or not len(things[1]) == 2 or not things[1].isdigit() or not len(things[2]) == 2 or not things[2].isdigit():
        raise ValueError
    year, month, day = map(int, things)
    if not 1 <= year <= 9999 or not 1 <= month <= 12 or not 1 <= day <= day_month_calc(year, month):
        raise ValueError
    return year, month, day

if __name__ == "__main__":
    main()
