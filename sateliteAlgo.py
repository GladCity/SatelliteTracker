import math

earthWeight = 5.97 * 10 ** 24
graviConst = 6.67 * 10 ** -11
earthRadius = 6,378 * 10 ** 6

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
    e2 = 1 / rd ** 2
    F = 54 * rd ** 2 * z ** 2
    G = r ** 2 + (1 - e2) * z ** 2
    c = e2 ** 2 * F * r ** 2 / G ** 3
    s = (1 + c + (c ** 2 + 2 * c) ** 0.5) ** (1 / 3)
    P = F / (3 * (s + 1 / s + 1) ** 2 * G ** 2)
    Q = (1 + 2 * e2 ** 2 * P) ** 0.5
    r0 = -(P * e2 * r) / (1 - Q) + (1 / 2 * rd ** 2 * (1 + 1 / Q) - P(1 - e2) * z ** 2 / (Q * (1 + Q)) - 1 / 2 * P + r ** 2) ** 0.5




