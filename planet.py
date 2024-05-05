'''
******************************************************
Star chart program by Python（Archaeoastronomy version）
2019.08.18 Ver1.0 Archaeoastronomy version1.2
2023.01.06 Ver3.0 repair for varue Cent and date
Ver3.0.1 small size
******************************************************
'''
# 2019.08.18 trial manufacture version is finished and upgrade 8/28 Ver.1.0
# 8/30 Archaeoastronomy version def insert def Batch() 8/31
# 9/11 add the calculation of the eclipse of the moon
# 2020.2 add GUIclass　and change it without using it to calculate with numpy-modure
# 2020/03/27　version 2.4  display the photograph of the month age
# 08/11 version 2.5 display size-down to 1000*750
# 12/04 version 2.6 repair def(defining fuction) "saisa-hosei"
# 12/05 virsion 2.7 display nomalization(large) , repair def timeforward ~ dateback
# 2022/10/20 version 2.8 repair for day-forward/back about varue"Cent"
import os
import tkinter as tk
import csv
import math

# Calculation to cure Julius day in the Gregorian calendar
def JDT(jd):
    Z = int(jd + 0.5)
    if Z >= 2299161:
        a = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + a - int(a / 4)
    else:
        A = Z
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    K = int(365.25 * C)
    E = int((B - K)/30.6001)
    D = B - K - int(30.6001 * E) + (jd + 0.5) - int(jd + 0.5)
    if E < 13.5:
        M = E -1
    else:
        M = E -13
    if M > 2.5:
        Y = C - 4716
    else:
        Y = C - 4715
    if M >= 13:
        Y = Y + 1
        M = M -12
    if Y <= 0:
        Y = Y -1

    h = D - int(D)
    D = int(D)
    h = h*24
    lh = round(long/15)
    h = h +lh
    if h >= 24.0:
        h = h - 24
        D = D + 1
    if D >= 32:
        D = D - 31
        M = M + 1
    if M >= 13:
        Y = Y + 1
        M = M - 12
    h = round(h,1)
    return [Y,M,D,h]

def koseji(jd,long):    # Calculate sidereal time
    B = jd - 2415020.0
    R = 366.2422/365.2422
    ST = 18.6461 + 24*B*R + 3.24e-14*B*B + long/15
    ST = 24*(ST/24-int(ST/24))
    if ST < 0:
        ST = ST + 24
    return ST

def yogen_AD(arfa,drta):  # Calculation of the direction cosine
    a = math.radians(arfa)
    d = math.radians(drta)
    L = math.cos(a) * math.cos(d)
    M = math.cos(d) * math.sin(a)
    N = math.sin(d)
    return [L,M,N]

def horizon(ad):   # to horizontal coordinate（ST;sideral time LAT;latitude　ad; direction cosine)
    sT = math.sin(math.radians(ST))
    cT = math.cos(math.radians(ST))
    sL = math.sin(math.radians(LAT))
    cL = math.cos(math.radians(LAT))
    L = sL*cT*ad[0] + sL*sT*ad[1] - cL*ad[2]
    M = -sT*ad[0] + cT*ad[1]
    N = cL*cT*ad[0] + cL*sT*ad[1] + sL*ad[2]
    if L == 0:
        L = 0.01
    h = math.asin(N)
    h = math.degrees(h)
    A = math.atan(-M/L)
    A = math.degrees(A)
    if L < 0. :
        A = A + 180.
    return [h,A]

def proper_move(RA,DC,V1,V2):   # proper monve
    T  = Cent - 1
    RA = RA + V1*T/3600000/math.cos(math.radians(DC))
    DC = DC + V2*T/3600000
    return [RA , DC]

def saisa_hosei(ad):  # 歳差補正
    t = Cent - 1
    f = 0.640616 * t + 0.0000839* t*t + 0.000005*t**3
    z = 0.640616 * t + 0.000304 * t*t + 0.00000506*t**3
    s = 0.556753 * t - 0.000119 * t*t - 0.0000116*t**3
    sF = math.sin(math.radians(f))
    cF = math.cos(math.radians(f))
    sZ = math.sin(math.radians(z))
    cZ = math.cos(math.radians(z))
    sS = math.sin(math.radians(s))
    cS = math.cos(math.radians(s))
    L = (- sZ*sF + cZ*cS*cF)*ad[0] + (- sZ*cF - cZ*cS*sF)*ad[1] - cZ*sS*ad[2]
    M = (cZ*sF + sZ*cS*cF)*ad[0] + (cZ*cF - sZ*cS*sF)*ad[1] - sZ*sS*ad[2]
    N = sS*cF*ad[0] - sS*sF*ad[1] + cS*ad[2]
    return [L, M, N]

def dispXY(hh, AA):
    dot = 480  # 画面のパラメータ　中心座標（540,375)
    r = dot * math.sin(math.radians((90-hh)/2))
    x = r * math.sin(math.radians(AA)) + 540
    y = r * math.cos(math.radians(AA)) + 375
    return [x, y]

# 太陽の位置計算
def solar_Pos():
    #print("Solar")
    sml = 280.6824 + 36000.769325 * Cent + 7.22222e-04*Cent*Cent
    sml = 360*(sml/360 - int(sml/360))
    if sml < 0:
        sml = sml + 360   # 平均黄経
    sec = 0.0167498 - 4.258e-5*Cent - 1.37e-7*Cent*Cent     # 離心率
    spl = 281.2206 + 1.717697*Cent + 4.83333e-4*Cent*Cent + 2.77777e-6*Cent*Cent*Cent
    spl = 360*(spl/360 -int(spl/360))
    if spl < 0:
        spl = spl + 360 # 近日点黄経
    sma = sml - spl
    if sma < 0:
        sma = sma + 360
    sma = math.radians(sma)  # 平均近点角
    smpg = 1.91946 * math.sin(sma) + 2.00939e-2*math.sin(2*sma) \
           - 4.78889e-3*math.sin(sma)*Cent - 1.44444e-5*math.sin(sma)*Cent*Cent
    sl = sml + smpg  # 太陽黄経
    sta = sl -spl   # 真近点角
    if sta < 0:
        sta = sta + 360
    sax = 1.00000129   # 軌道長半径
    srr = sax*(1 - sec*sec)/(1 + sec*math.cos(math.radians(sta)))  #地球-太陽距離
    ss = 0.2666/srr   # 視半径
    sx  = srr*(math.cos(math.radians(sl)))
    sy  = srr*(math.sin(math.radians(sl)))
    sz  = 0
    return [srr,sx,sy,sz,sl,ss]

#水星の軌道要素
def Mercury(C):
    #print("Mercury")
    ml  = 182.27175 + 149474.07244*C + 2.01944e-3*C*C  # 平均黄径
    if ml > 360:
        ml  = 360*(ml/360 - int(ml/360))
    pnl = 75.89717 + 1.553469*C + 3.08639e-4*C*C   # 近日点黄径
    omg = 47.144736 + 1.18476*C + 2.23194e-4*C*C  # 昇降点黄径Ω
    inc = 7.003014 + 1.73833e-3*C - 1.55555e-5*C*C  # 軌道傾斜角
    ec  = 0.20561494 + 0.0203e-3*C - 0.04e-6*C*C   # 離心率
    ax  = 0.3870984   # 軌道長半径
    return [ml,pnl,omg,inc,ec,ax]

#金星の軌道要素
def Venus(C):
    #print("Venus")
    ml = 344.36936 + 58519.2126*C + 9.8055e-4*C*C  #平均黄径
    if ml > 360:
        ml = 360*(ml/360 - int(ml/360))
    pnl = 130.14057 + 1.3723*C - 1.6472e-3*C*C   #近日点黄径
    omg = 75.7881 + 0.91403*C + 4.189e-4*C*C  #昇降点黄径Ω
    inc = 3.3936 + 1.2522e-3*C - 4.333e-6*C*C  #軌道傾斜角
    ec = 0.00681636 - 0.5384e-4*C + 0.126e-6*C*C   #離心率
    ax = 0.72333015   #軌道長半径
    return [ml,pnl,omg,inc,ec,ax]

#火星の軌道要素
def Mars(C):
    #print("Mars")
    ml = 294.26478 + 19141.69625*C + 3.15028e-4*C*C  #平均黄径
    if ml > 360:
        ml = 360*(ml/360 - int(ml/360))
    pnl = 334.21833 + 1.840394*C + 3.35917e-4*C*C   #近日点黄径
    omg = 48.78670 + 0.776944*C - 6.02778e-4*C*C  #昇降点黄径Ω
    inc = 1.85030 - 6.49028e-4*C + 2.625e-5*C*C  #軌道傾斜角
    ec = 0.0933088 + 0.095284e-3*C - 0.122e-6*C*C   #離心率
    ax = 1.5236781   #軌道長半径
    return [ml,pnl,omg,inc,ec,ax]

# 木星の軌道要素
def Jupiter(C,Y,JD):
    #print("Jupiter")
    ml  = 238.132386 + 3036.301986*C + 3.34683e-4*C*C - 1.64889e-6*C**3  #平均黄径
    if ml > 360:
        ml  = 360*(ml/360 - int(ml/360))
    T  = Y/1000
    A  = 0.42 - 0.075*T + 0.015*T*T - 0.003*T**3
    L7 = A*math.sin(math.radians((T-0.62)*360/0.925))  #摂動補正（長周期）
    eta = 86.1 + 0.033459*(JD - 1721057)
    eta = 360*(eta/360 - int(eta/360))
    if eta < 0:
        eta = eta + 360
    zeta = 89.1 + 0.04963*(JD - 1721057)
    zeta = 360*(zeta/360-int(zeta/360))
    if zeta < 0:
        zeta = zeta +360
    #print("eta = ",eta," zeta = ",zeta)  #短周期
    #L8 = input("input> L8  =")
    L8 = -.02#float(L8)
    ml = ml + L7 + L8
    pnl = 12.720972 + 1.6099617*C + 1.05627e-3*C*C - 3.4333e-6*C**3  #近日点黄径
    pnl = 360*(pnl/360 - int(pnl/360))
    if pnl < 0:
        pnl = pnl + 360
    PS7 = 0.02*math.sin(math.radians((T + 0.1)*360/0.925))
    #print(" input> PS8  ")
    #PS8 = input("=")
    PS8 = .0#float(PS8)
    PH  = 2.58 + 0.1*T
    pnl = pnl + (PS7 + PS8)/math.sin(math.radians(PH))
    ec  = 0.0483348 + 0.16418e-3*C - 0.4676e-6*C*C - 1.7e-9*C**3   # 離心率
    PH7 = 0.03*math.sin(math.radians((T + 0.36)*360/0.925))
    # print(" input> PH8  ")
    # PH8 = input("=")
    PH8 = .4 # float(PH8)
    ec  = math.sin(math.radians(PH + PH7 + PH8))
    omg = 99.443414 + 1.01053*C + 3.52222e-4*C*C - 8.351111e-6*C**3  # 昇降点黄径Ω
    inc = 1.308736 - 5.69611e-3*C + 3.88889e-6*C*C  # 軌道傾斜角
    ax  = 5.202805   # 軌道長半径
    return [ml,pnl,omg,inc,ec,ax]

# 土星の軌道要素
def Saturn(C,Y,JD):
    #print("Saturn")
    ax  = 9.554747   # 軌道長半径
    ml  = 266.597875 + 1223.50988*C + 3.24542e-4*C*C - 5.83333e-7*C**3  #平均黄径
    if ml > 360:
        ml  = 360*(ml/360 - int(ml/360))
    T  = Y/1000
    A  = 0.88 - 0.0633*T + 0.03*T*T - 0.006*T**3
    L7 = -0.5 + A*math.sin(math.radians((T-0.145)*360/0.95))  #摂動補正（長周期）
    # 短周期
    # L8 = input("input> L8=")
    L8 = .3  # float(L8)
    ml = ml + L7 + L8
    pnl = 91.09821 + 1.958416*C + 8.26361e-4*C*C + 4.61111e-6*C**3  #近日点黄径
    pnl = 360*(pnl/360 - int(pnl/360))
    if pnl < 0:
        pnl = pnl + 360
    B  = 0.1 - 0.005*T
    PS7 = -0.5 + B*math.sin(math.radians((T - 0.54)*360/0.95))
    # print(" input> PS8  ")
    # PS8 = input("=")
    PS8 = .4 # float(PS8)
    PH  = 3.56 + 0.175*T - 0.005*T*T
    pnl = pnl + (PS7 + PS8)/math.sin(math.radians(PH))
    ec  = 0.05589231 - 3.455e-4*C - 7.28e-7*C*C + 7.4e-10*C**3   # 離心率
    F   = 0.1 -0.005*T
    PH7 = -0.5 + F*math.sin(math.radians((T - 0.32)*360/0.95))
    # print(" input> PH8  ")
    # PH8 = input("=")
    PH8 = .5 # float(PH8)
    ec  = math.sin(math.radians(PH + PH7 + PH8))
    G   = 0.004 - 0.0005*T
    AX7 = -0.05 + G*math.sin(math.radians((T - 0.35)*360/0.95))
    # print(" input> AX8  ")
    # AX8 = input("=")
    AX8 = .04 # float(AX8)
    ax  = ax + AX7 + AX8
    omg = 112.790414 + 0.873195*C - 1.52181e-4*C*C - 5.30555e-6*C**3  # 昇降点黄径Ω
    inc = 2.49252 - 3.91889e-3*C - 1.54889e-5*C*C + 4.44444e-8*C**3  # 軌道傾斜角

    return [ml,pnl,omg,inc,ec,ax]

def pl_position(el):         # 惑星の位置計算
    ml = el[0] ; pnl=el[1] ; omg=el[2] ; inc=el[3] ; ec=el[4] ; ax=el[5]
    ma  = ml -pnl     # 平均近点角(Mean Anomaly)
    ma  = 360*(ma/360 - int(ma/360))
    if ma < 0:
        ma = ma + 360
    # print("  ma=",ma)
    mar = math.radians(ma)
    mpg = (2*ec-(ec*ec*ec)/4)*math.sin(mar) + 1.25*math.sin(2*mar)*ec*ec \
          + (13/12)*math.sin(3*mar)*ec**3
    mpg = math.degrees(mpg)
    # print("  ml=",ml)
    ta  = ma + mpg   # 真近点角(Ture Anomaly)
    uu  = ta + pnl - omg
    if uu < 0:
        uu = uu + 360
    aa  = math.cos(math.radians(inc))*math.tan(math.radians(uu))
    cc  = math.atan(aa)
    cc  = math.degrees(cc)
    if uu > 90 and uu < 270:
        cc = cc + 180
    if uu > 270:
        cc = cc + 360
    bb  = math.tan(math.radians(inc))*math.sin(math.radians(cc))

    ll  = cc + omg    # 日心黄径
    if ll > 360:
        ll = ll - 360
    # print("  ll =",ll)
    tb  = math.atan(bb)
    tb  = math.degrees(tb)   # 日心黄緯
    rr  = ax*(1 - ec*ec)/(1 + ec*math.cos(math.radians(ta)))  # 動径
    xx  = rr*(math.cos(math.radians(uu))*math.cos(math.radians(omg))
              - math.sin(math.radians(uu))*math.sin(math.radians(omg))*math.cos(math.radians(inc)))
    yy  = rr*(math.cos(math.radians(uu))*math.sin(math.radians(omg))
              + math.sin(math.radians(uu))*math.cos(math.radians(omg))*math.cos(math.radians(inc)))
    zz  = rr*(math.sin(math.radians(uu))*math.sin(math.radians(inc)))
    # tt  = math.sqrt(xx**2 + yy**2 + zz**2) # 太陽との距離＝動径
    # print("  rr=",rr)

    return [rr,xx,yy,zz,ll,tb]

def sekido():  # 赤道・黄道の描画
    sekiR = [0.0]*182
    A = [0.0]*182
    hh = [0.0]*182
    xl = [0.0]*182
    yl = [0.0]*182
    sekiD = [0.0]*182
    kodoD = [0.0]*182
    for i in range(0,181):
        sekiR[i] = i*2
        sekiD[i] = 0
        kodoD[i] = 23.4392*math.sin(math.radians(i*2))

    n = 0
    for i in range(182):
        ad = yogen_AD(sekiR[i],sekiD[i])
        h = horizon(ad)
        if h[0] < 0.2:
             continue
        hh[n],A[n] = h
        n += 1
    for i in range(n):
        xy= dispXY(hh[i],A[i])
        xl[i] ,yl[i]= xy

    for i in range(n-1):
        if xl[i+1] - xl[i] > 50:
            continue
        app.co_line(xl[i], yl[i], xl[i+1], yl[i+1], '#710071')
    n = 0
    for i in range(182):
        ad = yogen_AD(sekiR[i], kodoD[i])
        # ad = saisa_hosei(ad)
        h = horizon(ad)
        if h[0] < 0.2:
             continue
        hh[n],A[n] = h
        n += 1
    for i in range(n):
        xy= dispXY(hh[i],A[i])
        xl[i] ,yl[i] = xy

    for i in range(n-1):
        if xl[i+1] - xl[i] > 50 :
            continue
        app.co_line(xl[i], yl[i], xl[i+1], yl[i+1], '#969600')

def star_color(CL):    # 恒星の色　CL：color index
    if CL < -0.16:
        c = "#a09eff"
    elif CL < 0.15:
        c = "#a0d7ff"
    elif CL < 0.45:
        c = "#d7e8ff"
    elif CL < 0.68:
        c = "#ffffff"
    elif CL < 1.15:
        c = "#ffffdc"
    elif CL < 1.6:
        c = "#ffe6aa"
    else:
        c = "#ffd7b1"
    return c

def magnitude(m):    #等級を星の大きさに
    if m < 0.0:
       rd = 7
    elif m < 1.0:
       rd = 6
    elif m < 2.0:
       rd = 5
    elif m < 3.0:
       rd = 4
    elif m < 4.0:
        rd = 3
    else:
       rd = 2
    return rd

class Conline:  # 星座線クラス
    def __init__(self):
        self.lcnum = 0
        self.linRas = 0
        self.linDcs = 0
        self.linV1s = 0
        self.linV2s = 0
        self.linRae = 0
        self.linDce = 0
        self.linV1e = 0
        self.linV2e = 0

class Star:  # 星クラス
    def __init__(self):
        self.stnum = 0
        self.stV1 = 0
        self.stV2 = 0
        self.stRA = 0
        self.stDC = 0
        self.stMg = 0
        self.stCL = 0
class Constelation:  # 星座クラス
    def __init__(self):
        self.con_name = ""
        self.con_Ra = 0
        self.con_Dc = 0

class Planetarium:  # プラネタリウムクラス
    # 惑星表示のための変数
    ex = [0.0]*5
    ey = [0.0]*5
    ez = [0.0]*5
    xq = [0.0]*5
    yq = [0.0]*5
    zq = [0.0]*5
    dd = [0.0]*5
    lam = [0.0]*5
    bet = [0.0]*5
    ii = [0.0]*5
    R = [0.0]*5
    pmag = [0.0] * 5
    pl_RA = [0.0] * 5
    pl_DC = [0.0] * 5
    ph = [0.0] * 5
    pA = [0.0] * 5
    pname = [''] * 5
    pelm = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] * 5
    xp = [0.0] * 5
    yp = [0.0] * 5
    br = [0.0] * 5
    xyz = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] * 5
    plane_counter = 0
    # 星表示のための変数
    XX = [0.0] * 1000
    YY = [0.0] * 1000
    hh = [0.0] * 1000
    AA = [0.0] * 1000
    MG = [0.0] * 1000
    CLs = [0.0] * 1000
    rd = [0] * 1000
    hLs = [0.0] * 500
    hLe = [0.0] * 500
    ALs = [0.0] * 500
    ALe = [0.0] * 500
    x1 = [0.0] * 500
    y1 = [0.0] * 500
    x2 = [0.0] * 500
    y2 = [0.0] * 500
    nh = [0.0] * 60
    nA = [0.0] * 60
    xn = [0.0] * 60
    yn = [0.0] * 60
    coname = [""] * 60
    star_counter = 0
    line_counter = 0
    con_counter = 0

    def __init__(self):
        # 星、星座線リストを作る
        self.star_list = list()
        self.conline_list = list()
        self.conste_list = list()

        for i in range(1263):
            self.star_list.append(Star())

        for i in range(673):
            self.conline_list.append(Conline())

        for i in range(89):
            self.conste_list.append(Constelation())


        # データ読み込み
        with open("starData1263.csv", "r") as f:  # 恒星ファイル読み込み
            stDATA = csv.reader(f, delimiter=",")
            i = 0
            for row in stDATA:
                self.star_list[i].stnum = int(row[4])  #No.
                self.star_list[i].stV1 = float(row[1]) #固有運動RA
                self.star_list[i].stV2 = float(row[2]) #        DC
                self.star_list[i].stRA = float(row[6]) #赤経
                self.star_list[i].stDC = float(row[7]) #赤緯
                self.star_list[i].stMg = float(row[5]) #光度
                self.star_list[i].stCL = float(row[8]) #色指数
                i += 1

        with open("cons_lineData.csv", "r") as f:  #星座線ファイル読み込み
            szL=csv.reader(f,delimiter=",")
            i = 0
            for row in szL:
                self.conline_list[i].lcnum = str(row[0]) #星座コード
                self.conline_list[i].linRas = float(row[1])  #始点
                self.conline_list[i].linDcs = float(row[2])
                self.conline_list[i].linV1s = float(row[3])
                self.conline_list[i].linV2s = float(row[4])
                self.conline_list[i].linRae = float(row[5])  #終点
                self.conline_list[i].linDce = float(row[6])
                self.conline_list[i].linV1e = float(row[7])
                self.conline_list[i].linV2e = float(row[8])
                i += 1
        with open("cons_nameData.csv", "r") as f:  # 星座名ファイル読み込み
            szM=csv.reader(f,delimiter=",")
            i = 0
            for row in szM:
                self.conste_list[i].con_name = str(row[0]) # 星座名
                self.conste_list[i].con_Ra = float(int(row[1])*15+int(row[2])*0.25)
                self.conste_list[i].con_Dc = float(row[3])
                i += 1

    def star_culc(self):       # 恒星表示メソッド

        for lin in self.conline_list:  #固有運動の補正
            ads = proper_move(lin.linRas,lin.linDcs,lin.linV1s,lin.linV2s)
            lin.linRas = ads[0]
            lin.linDcs = ads[1]
            ade = proper_move(lin.linRae,lin.linDce,lin.linV1e,lin.linV2e)
            lin.linRae = ade[0]
            lin.linDce = ade[1]

        m = 0             # 星座線の地平座標計算
        for line in self.conline_list:
            ad = yogen_AD(line.linRas,line.linDcs)
            ad = saisa_hosei(ad)
            hs = horizon(ad)
            if hs[0] < 0.0:
                continue
            ad = yogen_AD(line.linRae,line.linDce)
            ad = saisa_hosei(ad)
            he = horizon(ad)
            if he[0] < 0.0:
                continue
            self.hLs[m],self.ALs[m] = hs
            self.hLe[m],self.ALe[m] = he
            m += 1
        self.line_counter = m

        i = 0
        for i in range( self.line_counter):   # 画面上の座標
            xy= dispXY(self.hLs[i],self.ALs[i])
            self.x1[i] ,self.y1[i] = xy
            xy= dispXY(self.hLe[i],self.ALe[i])
            self.x2[i] ,self.y2[i] = xy

        for star in self.star_list:  # 固有運動の補正
            ad = proper_move(star.stRA,star.stDC,star.stV1,star.stV2)
            star.stRA = ad[0]
            star.stDC = ad[1]

        n = 0              # 恒星の地平座標計算
        for star in self.star_list:
            ad = yogen_AD(star.stRA,star.stDC)
            ad = saisa_hosei(ad)
            h = horizon(ad)
            if h[0] < 0.0:
                continue
            self.hh[n],self.AA[n] = h
            self.MG[n] = star.stMg
            self.CLs[n] = star.stCL
            n += 1
        self.star_counter = n

        for i in range(self.star_counter):
            xy= dispXY(self.hh[i],self.AA[i])
            self.XX[i] ,self.YY[i] = xy


        n = 0            #星座名表示の地平座標計算
        for c in self.conste_list:
            ad = yogen_AD(c.con_Ra,c.con_Dc)
            ad = saisa_hosei(ad)
            h = horizon(ad)
            if h[0] < 0.0:
                continue
            self.nh[n] ,self.nA[n] = h
            self.coname[n] = c.con_name
            n += 1
        self.con_counter = n

        for i in range(self.con_counter):
            xy= dispXY(self.nh[i],self.nA[i])
            self.xn[i] ,self.yn[i] = xy


    def star_display(self):
        # 星座線を引く
        for i in range( self.line_counter):
            app.co_line(self.x1[i], self.y1[i], self.x2[i], self.y2[i], 'blue')

        # 星のプロット
        for i in range(self.star_counter):
            self.rd[i] = magnitude(self.MG[i])
            color = star_color(self.CLs[i])
            app.point_star(self.XX[i], self.YY[i], self.rd[i]/2, color)

        #星座名の表示
        for i in range(self.con_counter):
            app.text_in(self.xn[i], self.yn[i], self.coname[i], 'red')

    def coordinate_Planet(self):  # 惑星の位置計算
        #
        sxyz = solar_Pos()
        sx = sxyz[1] ; sy = sxyz[2] ; sz = sxyz[3] ; srr = sxyz[0] ; sl = sxyz[4]
        T = (YY - 1900)/100
        obl = 23.4523 - 1.30125e-2*T  # 黄道傾斜角
        cos = math.cos(math.radians(obl))
        sin = math.sin(math.radians(obl))
        for ip in range(5):
            if ip == 0:
                self.pelm[0] = Mercury(Cent)
                self.pname[0] ="Mercury"
            if ip == 1:
                self.pelm[1] = Venus(Cent)
                self.pname[1] ="Venus"
            if ip == 2:
                self.pelm[2] = Mars(Cent)
                self.pname[2] ="Mars"
            if ip == 3:
                self.pelm[3] = Jupiter(Cent,YY,JD)
                self.pname[3] ="Jupiter"
            if ip == 4:
                self.pelm[4] = Saturn(Cent,YY,JD)
                self.pname[4] ="Saturn"
            self.xyz = pl_position(self.pelm[ip])
            self.ex[ip] = self.xyz[1] + sx    #　黄道地心座標
            self.ey[ip] = self.xyz[2] + sy
            self.ez[ip] = self.xyz[3] + sz
            self.dd[ip] = math.sqrt(self.ex[ip]**2 + self.ey[ip]**2 + self.ez[ip]**2)  # 地心距離

        # 赤道地心座標に変換
            self.xq[ip] = self.ex[ip]
            self.yq[ip] = self.ey[ip]*cos - self.ez[ip]*sin
            self.zq[ip] = self.ey[ip]*sin + self.ez[ip]*cos
            self.R[ip] = math.sqrt(self.xq[ip]**2 + self.yq[ip]**2 + self.zq[ip]**2)
            self.pl_RA[ip] = math.degrees(math.atan(self.yq[ip] / self.xq[ip]))
            if self.xq[ip] <= 0.0:
                self.pl_RA[ip] = self.pl_RA[ip] + 180
            self.pl_DC[ip] = math.degrees(math.asin(self.zq[ip] / self.R[ip]))
        # 位相角の計算
            self.lam[ip] = self.ey[ip] / self.ex[ip]
            self.bet[ip] = self.ez[ip] / self.dd[ip]
            self.bet[ip] = math.asin(self.bet[ip])
            self.bet[ip] = math.degrees(self.bet[ip])   #地心黄緯
            self.lam[ip] = math.atan(self.lam[ip])
            self.lam[ip] = math.degrees(self.lam[ip])   #地心黄径
            if self.ex[ip] < 0:
                self.lam[ip] = self.lam[ip] + 180
            if self.ex[ip] > 0 and self.ey[ip] < 0:
                self.lam[ip] = self.lam[ip] + 360
            # print("lam = ",self.lam[ip]," bet= ",self.bet[ip])
            # elo = self.lam[ip] - sl  #太陽との離隔
            # print(" elo=",elo)
            hl = self.xyz[4] - sl
            if hl < -180:
                hl = hl + 360
            d2 = math.sqrt(self.xyz[0]**2 + srr**2 +     2*self.xyz[0]*srr*math.cos(math.radians(hl)))
            # print("d2=",d2," rr=",xyz[0])
            self.ii[ip] = (self.xyz[0]**2 + d2*d2 - srr**2)/(2*self.xyz[0]*d2)
            self.ii[ip] = math.acos(self.ii[ip])
            self.ii[ip] = math.degrees(self.ii[ip])   #位相角
            if self.ii[ip] < 0:
                self.ii[ip] = self.ii[ip] + 180
        # 惑星の明るさ（光度）
            if ip == 0:
                self.br[ip] = 1.16 + 5*math.log10(self.xyz[0]*d2) + 0.02838*abs(self.ii[ip]-50) + 1.023e-4*abs((self.ii[ip]-50)**2)
            if ip == 1:
                self.br[ip] = -4 + 5*math.log10(self.xyz[0]*d2) + 0.01322*abs(self.ii[ip]) + 0.4247e-6*abs(self.ii[ip]**3)
            if ip == 2:
                self.br[ip] = -1.3 + 5*math.log10(self.xyz[0]*d2) + 0.01486*abs(self.ii[ip])
            if ip == 3:
                self.br[ip] = -8.93 + 5*math.log10(self.xyz[0]*d2)
            if ip == 4:
                self.br[ip] = -8.68 + 5*math.log10(self.xyz[0]*d2)
            # print(" hl=",hl," ii =",self.ii[ip],"  br=",self.br[ip])

        self.plane_counter = 0            # 惑星の地平座標を計算
        for i in range(5):
            ad = yogen_AD(self.pl_RA[i],self.pl_DC[i])
            # ad = saisa_hosei(ad)
            h = horizon(ad)
            if h[0] < 0.0 :
                continue
            self.ph[self.plane_counter], self.pA[self.plane_counter] = h
            self.pname[self.plane_counter] = self. pname[i]
            self.br[self.plane_counter] = self.br[i]
            self.plane_counter += 1

        for i in range(self.plane_counter):
            self.xy= dispXY(self.ph[i],self.pA[i])
            self.xp[i], self.yp[i] = self.xy


    def planet_display(self):
        # 惑星の表示
        for i in range(self.plane_counter):
            self.br[i] = magnitude(self.br[i])
            self.br[i] = self.br[i]/2
            app.point_star(self.xp[i], self.yp[i], self.br[i], "yellow")
            app.text_in(self.xp[i]-10,self.yp[i]-8, self.pname[i], 'white')

    def solar_display(self):
        # 太陽の表示
        sxyz = solar_Pos()
        sx = sxyz[1] ; sy = sxyz[2]; sz = sxyz[3]; srr = sxyz[0]; ss = sxyz[5]
        ss = int(ss * 25)   # 視半径を画面サイズに
        obl = 23.4523 - 1.30125e-2*Cent  # 黄道傾斜角
        cos = math.cos(math.radians(obl))
        sin = math.sin(math.radians(obl))
        xq = sx
        yq = sy * cos - sz * sin
        zq = sy * sin + sz * cos
        sun_R = math.sqrt(xq**2 + yq**2 + zq**2)
        sun_RA = math.degrees(math.atan(yq / xq))
        if xq < 0.0:
            sun_RA = sun_RA + 180
        sun_DC = math.degrees(math.asin(zq / sun_R))
        ad = yogen_AD(sun_RA,sun_DC)
        # ad = saisa_hosei(ad)
        h = horizon(ad)
        if h[0] > 0.0 :
            xy= dispXY(h[0],h[1])
            app.point_star(xy[0], xy[1], ss, 'white')
            app.text_in(xy[0]-8,xy[1]-12, "Solar",  'white')

    def luna_display(self):    # 月の位置計算と表示
        # print("Luna")
        J = (JD -2378496)/36525    # Epoch A.D.1800 I 0.5 UT
        ml = 335.723436 + 481267.887361*J + 3.38888e-3*J*J + 1.83333e-6*J**3 # 平均黄径
        ml = 360*(ml/360 - int(ml/360))
        if ml < 0:
            ml = ml + 360
        # 摂動補正
        AA = 1.2949 + 413335.4078*J -7.2201e-3*J*J - 7.2305e-6*J**3
        AA = 360*(AA/360 - int(AA/360))
        BB = 111.6209 + 890534.2514*J + 6.9838e-3*J*J + 6.9778e-6*J**3
        BB = 360*(BB/360 - int(BB/360))
        CC = 180.40885 + 35999.0552*J -0.0001988*J*J
        CC = 360*(CC/360 - int(CC/360))
        DD = 0.88605 + 377336.3526*J - 7.0213e-3*J*J - 7.2305e-6*J**3
        DD = 360*(DD/360 - int(DD/360))
        EE = 111.21205 + 854535.1962*J + 7.1826e-3*J*J + 6.9778e-6*J**3
        EE = 360*(EE/360 - int(EE/360))
        HH = 169.1706 + 407332.2103*J + 5.3354e-3*J*J + 5.3292e-6*J**3
        HH = 360*(HH/360 - int(HH/360))

        A0 = 1.2408*math.sin(math.radians(AA))
        B0 = 0.5958*math.sin(math.radians(BB))
        C0 = 0.1828*math.sin(math.radians(CC))
        D0 = 0.055*math.sin(math.radians(DD))
        E0 = 0.0431*math.sin(math.radians(EE))
        H0 = 0.1453*math.sin(math.radians(HH))
        st = A0 + B0 + C0 + D0 + E0
        ml = ml + st
        pnl = 225.397325 + 4069.053805*J - 1.02869e-2*J*J - 1.22222e-5*J**3   #近日点黄径
        pnl = 360*(pnl/360 - int(pnl/360))
        ma = ml - pnl
        ec = 0.05490897   # 離心率
        ma = math.radians(ma)
        EX = ma
        SS = EX - ec*math.sin(EX) - ma
        # kepplar equation
        while abs(SS) > 1.0e-8:
            DE = SS/(1 - ec*math.cos(EX))
            EX = EX - DE
            SS = EX - ec*math.sin(EX) - ma
        TT = math.sqrt((1 + ec)/(1 - ec))*math.tan(EX/2)
        TA = 2*math.atan(TT)
        TA = math.degrees(TA)
        if TA < 0:
            TA = TA +360

        omg = 33.272936 - 1934.144694*J + 2.08028e-3*J*J + 2.08333e-6*J**3 # 昇降点黄径Ω
        omg = 360*(omg/360 - int(omg/360))
        if omg < 0:
            omg = omg + 360
        uu = pnl - omg + TA
        uu = 360*(uu/360 - int(uu/360))

        inc = 5.144433   # 軌道傾斜角
        JJ = math.cos(math.radians(inc))*math.tan(math.radians(uu))
        MM = math.atan(JJ)
        MM = math.degrees(MM)
        if math.cos(math.radians(uu)) < 0:
            MM = MM + 180
        MM  = 360*(MM/360 - int(MM/360))
        lam = MM + omg
        lam = 360*(lam/360 - int(lam/360))
        BE = math.tan(math.radians(inc))*math.sin(math.radians(MM))
        tb = math.atan(BE)
        tb = math.degrees(tb)
        tb = tb + H0          # lam tb :地心視位置（黄経，黄緯）

        lst = koseji(JD,long)
        lst = lst*15
        ax = 60.2682   # 軌道長半径(地球半径を１とする）
        RR = ax*(1 - ec*math.cos(EX))  # 地心距離
        G = 1/RR/.99
        PI = math.asin(G)
        PI = math.degrees(PI)  # 月の赤道水平視差
        obl = 23.4523 - 0.013*Cent -1.6388e-6*Cent*Cent
        A = math.cos(math.radians(obl))*math.cos(math.radians(LAT))*math.sin(math.radians(lst)) \
          + math.sin(math.radians(obl))*math.sin(math.radians(LAT))
        B = math.cos(math.radians(LAT))*math.cos(math.radians(lst))
        L = math.atan(A/B)
        L = math.degrees(L) # 観測地点の地心黄経
        if A < 0 and B < 0 :
            L = L + 180
        if A < 0 and B > 0:
            L = L +360
        if A > 0 and B < 0:
            L = L + 180
        JJ = - math.sin(math.radians(obl))*math.cos(math.radians(LAT))*math.sin(math.radians(lst))\
          + math.cos(math.radians(obl))*math.sin(math.radians(LAT))
        B = math.asin(JJ)
        B = math.degrees(B) # 観測地点の黄緯

        # 視差の計算
        PP = math.sin(math.radians(PI))*math.cos(math.radians(B))*math.sin(math.radians(L - lam))\
          /math.cos(math.radians(tb))
        lam1 = math.asin(PP)
        lam1 = -math.degrees(lam1)
        GG  = math.tan(math.radians(B))/math.cos(math.radians(L - lam))
        GA1 = math.atan(GG)
        GA1 = math.degrees(GA1)
        QQ  = math.sin(math.radians(PI))*math.sin(math.radians(B))*math.sin(math.radians(GA1-tb))\
          /math.sin(math.radians(GA1))
        tb1 = -math.asin(QQ)
        tb1 = math.degrees(tb1)
        lam2 = lam + lam1
        tb2 = tb + tb1
        obl = 23.452 - 1.30125e-2*Cent
        s = math.cos(math.radians(obl))*math.sin(math.radians(tb2)) + math.sin(math.radians(obl))*math.cos(math.radians(tb2))*math.sin(math.radians(lam2))
        luna_DC = math.asin(s)
        luna_DC = math.degrees(luna_DC)
        A = -math.sin(math.radians(obl))*math.sin(math.radians(tb2)) + math.cos(math.radians(obl))*math.cos(math.radians(tb2))*math.sin(math.radians(lam2))
        B = math.cos(math.radians(tb2))*math.cos(math.radians(lam2))
        luna_RA = math.atan(A/B)
        luna_RA = math.degrees(luna_RA)
        if A > 0 and B < 0 :
            luna_RA = luna_RA + 180
        if A < 0 and B > 0:
            luna_RA = luna_RA + 360
        if A < 0 and B < 0:
            luna_RA = luna_RA + 180
        # 視半径
        K = 0.2725*G
        ms = math.asin(K)
        ms = math.degrees(ms)
        ms = int(ms*25)

        # Moon's phase
        solar = solar_Pos()
        mp = lam2 - solar[4]
        mp = 360*(mp/360 - int(mp/360))
        if mp < 0:
            mp = mp + 360
        # Earth's shadow
        moo = lam - solar[4] - 180
        if moo < 0:
            moo = moo + 360
        bke = 1 / (60.2682*(1 - ec*math.cos(EX)))
        bke = math.degrees(bke)
        bae = 2.443e-3 /  solar[0]
        kem = bke - solar[5] + bae
        kem = int(1.02 * 12 * kem)     # 地球の本影の半径(display)
        # oek = 0.25905 / (1 - ec*math.cos(EX))　月の支直径
        # print("moo =",moo ,"kem=",kem,"oek=",oek)
        sx = solar[1] ; sy = solar[2] ; sz = solar[3]
        cos = math.cos(math.radians(obl))
        sin = math.sin(math.radians(obl))
        xq = sx
        yq = sy * cos - sz * sin
        zq = sy * sin + sz * cos
        sun_R = math.sqrt(xq**2 + yq**2 + zq**2)
        sun_RA = math.degrees(math.atan(yq / xq))
        if xq < 0.0:
            sun_RA = sun_RA + 180
        sun_DC = math.degrees(math.asin(zq / sun_R))
        sdRA = sun_RA + 180
        if sdRA >360:
            sdRA = sdRA - 360
        sdDC = - sun_DC
        ad = yogen_AD(sdRA,sdDC)  # 月食の影の描画
        # ad = saisa_hosei(ad)
        h = horizon(ad)
        if h[0] > 0.0 :
            xy= dispXY(h[0],h[1])
            app.point_eclip(xy[0], xy[1], kem, 'green')
            app.text_in(xy[0]-20, xy[1]-20, "shadow", 'gray')
        # 月の描画
        ad = yogen_AD(luna_RA,luna_DC)
        #ad = saisa_hosei(ad)
        h = horizon(ad)
        if h[0] > 0.0 :
            xy= dispXY(h[0],h[1])
            app.point_star(xy[0], xy[1], ms, 'gray')
            app.text_in(xy[0]-8, xy[1]-12, "Moon", 'white')
            # print(" 月齢　= ",round(mp*0.082,1))
        return round(mp*0.082,1)


class Time:
    def __init__(self,Y,D,lo):
        self.Ydate = Y
        self.Dtime = D
        self.LAT = 36.6
        self.JD = 0
        self.ST = 0
        self.Cent = 0
        self.YY = 0
        self.long = lo

    def Julian(self):  # （ユリウス日）の計算
        self.JD = 0
        if self.Ydate != abs(self.Ydate):
            SP1 = -1
            self.Ydate = abs(self.Ydate)
        else:
            SP1 = 1
        self.YY = int(self.Ydate/10000)
        MD = int(self.Ydate-10000*self.YY)
        MM = int(MD/100)
        DD = MD - 100 * MM
        HH = int(self.Dtime/100)
        MS = self.Dtime-100*HH
        if SP1 < 0:
            self.YY = self.YY * SP1  # +1  BC.でなく，BC1年を0年として－で入力する
        SP2 = self.YY + (MM-1)/12 + DD/365.25
        if MM <= 2 :
            MM = MM + 12
            self.YY = self.YY - 1
        if self.YY < 0:
            self.JD = math.floor(365.25*self.YY) + int(30.59*(MM-2)) + DD - self.long/360 + 1721086.5
        else:
            self.JD = int(365.25*self.YY) + int(30.59*(MM-2)) + DD - self.long/360 + 1721086.5
        if SP2 > 1582.78:  # グレゴリオ暦以降
            self.JD = self.JD + int(self.YY/400) - int(self.YY/100) + 2
        if MM > 12:
            MM = MM - 12
            self.YY = self.YY + 1
        self.JD = self.JD + HH/24 + MS/1440

        self.ST  = koseji(self.JD,self.long)*15      # ST 恒星時(度)
        self.Cent  = (self.JD - 2415021.0)/36525      # 元期1900年I.1 0.5


def Batch():
    app.refresh()
    plt.star_culc()
    plt.star_display()
    plt.coordinate_Planet()
    plt.planet_display()
    plt.solar_display()
    plt.luna_display()

def update(event):
    global LAT
    global long
    global ymd
    global ST
    global Cent
    global YY
    global JD

    gvl.getV()
    Dtime = gvl.D_time
    Dtime = float(Dtime)
    Ydate = gvl.Y_date
    Ydate = float(Ydate)
    long  = gvl.LONG
    long  = float(long)
    LAT = gvl.Lat
    LAT = float(LAT)
    tm = Time(Ydate, Dtime, long)
    tm.Julian()
    JD = tm.JD
    ST = tm.ST
    Cent = tm.Cent
    YY = tm.YY
    ymd = JDT(JD)

    Batch()

def Timeforward():
    global ST
    global JD
    global ymd
    ymd[3] = ymd[3] + 1
    ST = ST + 15
    JD = JD + (1/24)
    ymd = JDT(JD)

    Batch()

def Timeback():
    global ST
    global JD
    global ymd
    ymd[3] = ymd[3] - 1
    ST = ST - 15
    JD = JD - (1/24)
    ymd = JDT(JD)
    Batch()

def Dateforward():
    global ST
    global JD
    global ymd
    global Cent
    ST = ST + 1.002738
    JD = JD + 1
    ymd = JDT(JD)
    Cent =Cent + 0.000027379093
    Batch()

def Dateback():
    global ST
    global JD
    global ymd
    global Cent
    ST = ST - 1.002738
    JD = JD -1
    ymd = JDT(JD)
    Cent =Cent - 0.000027379093
    Batch()

class Application(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)
        master.title(u"星座早見（Small-Size バージョン3.01）")
        master.geometry("1100x750")
        self.c0 = tk.Canvas(master=None, width = 1100, height = 750, bg="#001766")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.c0.create_text(955, 570, text="その日の時刻を１時間", font=('', 12), anchor='c', fill="white")
        self.c0.create_text(955, 635, text="日付を１日", font=('', 12), anchor='c', fill='white')
        self.c0.create_text(25, 670, text="紀元前はB.C.1年を0年として計算する。入力は-１で", font=('', 10), fill='white', anchor='w')
        self.lb1 = tk.Label(text=u"観測地の緯度・経度(南緯は－，東経は＋）", fg='white', bg="#001766", anchor='w', font=('', 14)).place(x=730,
                                                                                      y=30)
        self.inputbox1 = tk.Entry(width=4, font=('', 14))
        self.inputbox1.place(x=820, y=60)
        self.inputbox1.insert(tk.END, "36.6")
        self.inputbox1.bind("<KeyPress-Return>", update)
        self.inputbox2 = tk.Entry(width=6, font=('', 14))
        self.inputbox2.place(x=900, y=60)
        self.inputbox2.insert(tk.END, "139.7")
        self.inputbox2.bind("<KeyPress-Return>", update)
        self.lb2 = tk.Label(text="日付(YYYYMMDD)  時刻(hhmm)", fg='white', bg="#001766", anchor='w', font=('', 14)).place(x=800,
                                                                                                                 y=95)
        self.inputbox3 = tk.Entry(width=10, font=('', 14))
        self.inputbox3.place(x=850, y=120)
        self.inputbox3.insert(tk.END, "20350902")
        self.inputbox3.bind("<KeyPress-Return>", update)
        self.inputbox4 = tk.Entry(width=6, font=('', 14))
        self.inputbox4.place(x=980, y=120)
        self.inputbox4.insert(tk.END, "1100")
        self.inputbox4.bind("<KeyPress-Return>", update)

        self.lb3 = tk.Label(text=u'入力→Enterで再表示します', width=25, font=('', 10), fg='#001766', bg='skyblue').place(x=870, y=165)
        self.Button1 = tk.Button(text=u'進む>>', command=Timeforward, width=10, font=('', 10)).place(x=960, y=590)
        self.Button2 = tk.Button(text=u'<<もどる', command=Timeback, width=10, font=('', 10)).place(x=860, y=590)
        self.Button3 = tk.Button(text=u'進む>', command=Dateforward, width=10, font=('', 10)).place(x=960, y=650)
        self.Button4 = tk.Button(text=u'<もどる', command=Dateback, width=10, font=('', 10)).place(x=860, y=650)

    def refresh(self):  # 再表示
        global img_moon   # create_imageに必要
        self.c0.create_oval(170, 10, 910, 745, fill="#001766", outline="#001766")
        self.c0.create_text(540, 20, text="N", font=('', 18), fill="yellow")
        self.c0.create_text(540, 730, text="S", font=('', 18), fill="yellow")
        self.c0.create_text(180, 375, text="E", font=('', 18), fill="yellow")
        self.c0.create_text(900, 375, text="W", font=('', 18), fill="yellow")
        self.c0.create_oval(200, 35, 880, 715, fill='black', outline='skyblue', width=1)
        self.c0.pack()
        iDir = os.path.abspath(os.path.dirname(__file__))
        img_moon = tk.PhotoImage(file=iDir + '\moon-phase\m' + str(int(plt.luna_display())) + '.gif')
        self.c0.create_image(140, 590, image=img_moon, anchor='sw')
        self.c0.pack()
        if ymd[0] <= 0:
            self.lb4 = tk.Label(text=f"B.C. {-ymd[0]}年　{ymd[1]}月 {ymd[2]}日   {ymd[3]} 時の星空(地方時）  　 ", fg='white', \
                           bg="#001766", anchor='w', font=('', 14))
        else:
            self.lb4 = tk.Label(text=f"A.D. {ymd[0]}年　{ymd[1]}月 {ymd[2]}日   {ymd[3]} 時の星空(地方時）  　 ", fg='white', \
                       bg="#001766", anchor='w', font=('', 14))
        self.lb4.place(x=25, y=25)
        self.lb5 = tk.Label(text=f"緯度= {LAT}°経度=　{long}°", fg='white', bg="#001766", anchor \
            ='w', font=('', 14))
        self.lb5.place(x=25, y=60)
        # self.c0.create_oval(185, 35, 1015, 865, fill='black', outline='skyblue', width=1)
        self.lb6 = tk.Label(text=f" ユリウス日は = {round(JD, 3)}　日　    ", fg='white', bg="#001766", anchor \
            ='w', font=('', 10))
        self.lb6.place(x=25, y=600)
        self.lb7 = tk.Label(text=f" 恒星時は = {round(ST / 15, 1)}  時    ", fg='white', bg="#001766", anchor \
            ='w', font=('', 10))
        self.lb7.place(x=25, y=630)
        self.lb8 = tk.Label(text=f" 月齢  =  {plt.luna_display()}    ", fg='white', bg="#001766", anchor \
            ='w', font=('', 12))
        self.lb8.place(x=25, y=570)


        sekido()

    def point_star(self, X, Y, dir, color):
        self.c0.create_oval(X-dir, Y-dir, X+dir, Y+dir, fill = color)
        self.c0.pack()

    def co_line(self, X1, Y1, X2, Y2, color):
        self.c0.create_line(X1, Y1, X2, Y2, fill = color, smooth = "True")
        self.c0.pack()

    def text_in(self, X, Y, name, color):
        self.c0.create_text(X, Y, text = name, font = ('',8), fill = color)
        self.c0.pack()

    def point_eclip(self, X, Y, dir, color):
        self.c0.create_oval(X-dir, Y-dir, X+dir, Y+dir, outline = color, )
        self.c0.pack()

class Get_Value(Application):
    def __init__(self,master=None):
        super().__init__(master)
        self.Lat = 0
        self.LONG = 0
        self.Y_date = 0
        self.D_time = 0
    def getV(self):
        self.Lat = self.inputbox1.get()
        self.LONG = self.inputbox2.get()
        self.Y_date = self.inputbox3.get()
        self.D_time = self.inputbox4.get()


plt = Planetarium()
root = tk.Tk()
root.resizable(width=False, height=False)
app = Application(master=root)   # tkinter(GUI)
gvl = Get_Value(master=root)    # 設定変更値の取得

# 日時の計算
tm = Time(20350902, 1100, 139.7) # 初期設定（年月日，時刻，経度
tm.Julian()
JD = tm.JD
ST = tm.ST
Cent = tm.Cent
YY = tm.YY
long = tm.long  # 経度
LAT = tm.LAT  # 緯度
ymd = JDT(JD)
Batch()

if __name__ == '__main__':
    app.mainloop()
