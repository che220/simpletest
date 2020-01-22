from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

now = QDate.currentDate()

print(now.toString(Qt.ISODate))
print(now.toString(Qt.DefaultLocaleLongDate))

datetime = QDateTime.currentDateTime()

print(datetime.toString())

time = QTime.currentTime()

print(time.toString(Qt.DefaultLocaleLongDate))

# UTC time
now = QDateTime.currentDateTime()

print("Local datetime: ", now.toString(Qt.ISODate))
print("Universal datetime: ", now.toUTC().toString(Qt.ISODate))

print("The offset from UTC is: {0} seconds".format(now.offsetFromUtc()))

# Number of days
now = QDate.currentDate()

d = QDate(1945, 5, 7)

print("Days in month: {0}".format(d.daysInMonth()))
print("Days in year: {0}".format(d.daysInYear()))

# diff in days
xmas1 = QDate(2016, 12, 24)
xmas2 = QDate(2017, 12, 24)

now = QDate.currentDate()

dayspassed = xmas1.daysTo(now)
print("{0} days have passed since last XMas".format(dayspassed))

nofdays = now.daysTo(xmas2)
print("There are {0} days until next XMas".format(nofdays))

# arithmetic
now = QDateTime.currentDateTime()

print("Today:", now.toString(Qt.ISODate))
print("Adding 12 days: {0}".format(now.addDays(12).toString(Qt.ISODate)))
print("Subtracting 22 days: {0}".format(now.addDays(-22).toString(Qt.ISODate)))

print("Adding 50 seconds: {0}".format(now.addSecs(50).toString(Qt.ISODate)))
print("Adding 3 months: {0}".format(now.addMonths(3).toString(Qt.ISODate)))
print("Adding 12 years: {0}".format(now.addYears(12).toString(Qt.ISODate)))

# daylight savings
now = QDateTime.currentDateTime()

print("Time zone: {0}".format(now.timeZoneAbbreviation()))

if now.isDaylightTime():
    print("The current date falls into DST time")
else:
    print("The current date does not fall into DST time")

# epoch
now = QDateTime.currentDateTime()

unix_time = now.toSecsSinceEpoch()
print(unix_time)

d = QDateTime.fromSecsSinceEpoch(unix_time)
print(d.toString(Qt.ISODate))

# julian days
now = QDate.currentDate()

print("Gregorian date for today: ", now.toString(Qt.ISODate))
print("Julian day for today: ", now.toJulianDay())

borodino_battle = QDate(1812, 9, 7)
slavkov_battle = QDate(1805, 12, 2)

now = QDate.currentDate()

j_today = now.toJulianDay()
j_borodino = borodino_battle.toJulianDay()
j_slavkov = slavkov_battle.toJulianDay()

d1 = j_today - j_slavkov
d2 = j_today - j_borodino

print("Days since Slavkov battle: {0}".format(d1))
print("Days since Borodino battle: {0}".format(d2))
