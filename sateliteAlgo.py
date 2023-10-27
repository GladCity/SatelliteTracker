import math
from datetime import datetime, date, timedelta
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from pyorbital.orbital import Orbital

earthWeight = 5.97 * 10 ** 24
graviConst = 6.67 * 10 ** -11
earthRadius = 6.378 * 10 ** 6


def calcSateliteSpeed(sateliteHeight):
    return (graviConst * earthWeight / (earthRadius + sateliteHeight))


def calcSatelitePeriod(sateliteHeight):
    return (2 * math.pi * (earthRadius + sateliteHeight) / calcSateliteSpeed(sateliteHeight))


def fromGeodetToGeocent(LBHlist):
    x = (earthRadius + LBHlist[2]) * math.cos(LBHlist[1]) * math.cos(LBHlist[0])
    y = (earthRadius + LBHlist[2]) * math.cos(LBHlist[1]) * math.sin(LBHlist[0])
    z = (earthRadius + LBHlist[2]) * math.sin(LBHlist[1])
    return [x, y, z]


def fromGeocentToGeodet(XYZlist):
    x = XYZlist[0]
    y = XYZlist[1]
    z = XYZlist[2]
    rd = earthRadius
    r = (x ** 2 + y ** 2) ** 0.5
    e2 = math.e ** 2
    et2 = 1 / rd ** 2
    F = 54 * rd ** 2 * z ** 2
    G = r ** 2 + (1 - e2) * z ** 2
    c = e2 ** 2 * F * r ** 2 / G ** 3
    s = (1 + c + (c ** 2 + 2 * c) ** 0.5) ** (1 / 3)
    P = F / (3 * (s + 1 / s + 1) ** 2 * G ** 2)
    Q = (1 + 2 * e2 ** 2 * P) ** 0.5
    r0 = -(P * e2 * r) / (1 - Q) + (1 / 2 * rd ** 2 * (1 + 1 / Q)
                                    - P(1 - e2) * z ** 2 / (Q * (1 + Q))
                                    - 1 / 2 * P + r ** 2) ** 0.5
    U = ((r - e2 * r0) ** 2 + z ** 2) ** 0.5
    V = ((r - e2 * r0) ** 2 + (1 - e2) * z ** 2) ** 0.5
    z0 = rd * z / V
    H = U * (1 - rd / V)
    B = math.atan((z + et2 * z0) / r)
    L = math.atan2(y, x)
    return [L, B, H]


def get_spacetrack_tle(sat_id, start_date, end_date, username, password, latest=False):
    st = SpaceTrackClient(identity=username, password=password)
    if not latest:
        daterange = op.inclusive_range(start_date, end_date)
        data = st.tle(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle', epoch=daterange)
    else:
        data = st.tle_latest(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle')

    if not data:
        return 0, 0
    tle_1 = data[0:69]
    tle_2 = data[70:139]
    return tle_1, tle_2


USERNAME = "vladimirga1511@gmail.com"
PASSWORD = "4456Vektor654456"


def calcGeodeticDist(p1, p2):
    fm = (p1[0] + p2[0]) / 2 * math.pi / 180
    k1 = 111.13209 - 0.56605 * math.cos(2 * fm) + 0.0012 * math.cos(4 * fm)
    k2 = 111.41513 * math.cos(fm) - 0.09455 * math.cos(3 * fm) + 0.00012 * math.cos(5 * fm)
    return ((k1 * (p1[0] - p2[0])) ** 2 + (k2 * (p1[1] - p2[1])) ** 2) ** 0.5


def checkCover(location, satPos, mainStripWidth):
    d1 = calcGeodeticDist(location[0], satPos)
    d2 = calcGeodeticDist(location[1], satPos)
    if d1 < mainStripWidth:
        return d2 - mainStripWidth
    elif d2 < mainStripWidth:
        return d1 - mainStripWidth
    else:
        return None


def calcRequiredTimeAndSatTrack(sat_id, cameraViewStrip, location):
    result = [0, 0]
    satTrack = [[], []]
    tle_1, tle_2 = get_spacetrack_tle(sat_id, date.today() - timedelta(days=1), date.today(), USERNAME, PASSWORD, False)
    if not tle_1 or not tle_2:
        print
        'Impossible to retrieve TLE'
        return

    midLon = (location[0][0] + location[1][0]) / 2
    halfLocationWidth = calcGeodeticDist([midLon, location[0][1]], [location[0][0], location[0][1]])
    mainStripWidth = cameraViewStrip / 2 + halfLocationWidth
    orb = Orbital("N", line1=tle_1, line2=tle_2)
    curPeriod = 24 * 60 / float(tle_2[52:63])
    i = 0
    minutes = datetime.now().time().hour * 60 + datetime.now().time().minute
    timeStep = 5
    requiredTime = 0
    coveredFlag = False
    while minutes < requiredTime or not coveredFlag:
        utc_hour = int(minutes // 60 % 24)
        utc_minutes = int((minutes - (utc_hour * 60)) // 1) % 60
        utc_seconds = int(round((minutes - (utc_hour * 60) - utc_minutes) * 60)) % 60
        utc_time = datetime(date.today().year, date.today().month, date.today().day, utc_hour, utc_minutes, utc_seconds)
        lon, lat, alt = orb.get_lonlatalt(utc_time)
        if not coveredFlag:
            uncovered = checkCover(location, [lon, lat], mainStripWidth)
            coveredFlag = True
            if uncovered != None:
                if uncovered < 0:
                    requiredTime = minutes
                elif uncovered > 0:
                    utc_hour1 = int(minutes // 60 % 24)
                    utc_minutes1 = int((minutes - (utc_hour1 * 60) + curPeriod) // 1) % 60
                    utc_seconds1 = int(round((minutes - (utc_hour1 * 60) - utc_minutes1) * 60)) % 60
                    utc_time1 = datetime(date.today().year, date.today().month, date.today().day, utc_hour1,
                                         utc_minutes1,
                                         utc_seconds1)
                    lon1, lat1, alt1 = orb.get_lonlatalt(utc_time1)
                    satPeriodicalOffset = calcGeodeticDist([lon1, lat], [lon, lat])
                    requoredAmountOfRoundate = uncovered // satPeriodicalOffset + 1
                    requiredTime += requoredAmountOfRoundate * curPeriod
                    requiredTime += minutes
            else:
                coveredFlag = False
        satTrack[0].append(lon)
        satTrack[1].append(lat)
        minutes += timeStep
        if minutes > 80 * curPeriod:
            result[0] = None
            result[1] = None
            return result
    result[0] = satTrack
    result[1] = requiredTime
    return result
