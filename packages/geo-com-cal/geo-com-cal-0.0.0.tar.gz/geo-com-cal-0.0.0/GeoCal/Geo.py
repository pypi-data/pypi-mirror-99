# This Python file uses the following encoding: gbk
import math

from decimal import Decimal


class Geo:
    #类属性 赤道至纬度B子午线弧长计算（传统展开多项式方法 展开至10项）以及垂直纬度计算的辅助变量
    #此公式计算弧长结果贴合cgcs 2000 对于西安 80  北京 54 坐标系 误差稍大
    A,B,C,D,E=None,None,None,None,None
    def __init__(self):
        #Ellipsoidal parameter default:CGCS 2000
        self.setEllipsoidParameter2(6378137,1/298.257222101)
        Geo.A=1+3/4*math.pow(self.e1,2)+45/64*math.pow(self.e1,4)\
        +175/256*math.pow(self.e1,6)+11025/16384*math.pow(self.e1,8)+43659/65536*math.pow(self.e1,10)

        Geo.B=3/4*math.pow(self.e1,2)+15/16*math.pow(self.e1,4)\
        +525/512*math.pow(self.e1,6)+2205/2048*math.pow(self.e1,8)+72765/65536*math.pow(self.e1,10)

        Geo.C=15/64*math.pow(self.e1,4)+105/256*math.pow(self.e1,6)+2205/4096*math.pow(self.e1,8)\
        +10395/16384*math.pow(self.e1,10)

        Geo.D=35/512*math.pow(self.e1,6)+315/2048*math.pow(self.e1,8)+31185/131072*math.pow(self.e1,10)

        Geo.E=315/16384*math.pow(self.e1,8)+3465/65536*math.pow(self.e1,10)

        Geo.F=693/131072*math.pow(self.e1,10)

        pass

    #设置椭球参数
    #参数 a b c f e1^2 e2^2
    def setEllipsoidParameter1(self,a,b,c,f,e12,e22):
        self.a=Decimal(str(a)).quantize(Decimal("1"))
        self.b=Decimal(str(b)).quantize(Decimal("1.0000"))
        self.c=Decimal(str(c)).quantize(Decimal("1.0000"))
        self.f=Decimal(str(f)).quantize(Decimal("1.00000000000000"))
        self.e1=Decimal(str(math.sqrt(e12)))
        self.e2=Decimal(str(math.sqrt(e22)))
        #辅助函数
        self.W=None
        self.V=None
        pass

    #设置椭球参数
    #参数 a f
    def setEllipsoidParameter2(self,a,f):
        b=a-a*f
        c=a*a/b
        e1=(a**2-b**2)/(a**2)
        e2=(a**2-b**2)/(b**2)
        self.setEllipsoidParameter1(a,b,c,f,e1,e2)
        pass

    #度数（60进制）转弧度
    #参数：+-度 分 秒
    #返回Decimal类型 浮点数弧度
    def degToRad(self,d,m,s):
        d=Decimal(str(d))
        if d<0:
            d=d-Decimal(str(m))/60-Decimal(str(s))/3600
            pass
        else:
            d=d+Decimal(str(m))/60+Decimal(str(s))/3600
            pass
        return Decimal(str(math.radians(d)))

    #度数（浮点数）转60进制度数(dd°dd′dd.d+″)
    #返回d m s(Decimal类型)
    def deg_60(self,D):
        D=Decimal(str(D))
        d=None
        if D>=0:
            d=Decimal(str(math.floor(D)))
            pass
        else:
            d=Decimal(str(math.ceil(D)))
            pass
        D=Decimal(str(abs(D)))
        dt=Decimal(str(abs(d)))
        m=Decimal(str(round(math.floor((D-dt)*100)*60/100)))
        s=Decimal(str((D-dt-m/60)*3600))
        while s<0:
            m-=1
            s+=60
            pass
        return (d,m,s)

    #第一辅助函数
    #参数大地纬度 弧度
    #返回W Decimal类型
    def getW(self,B):
        bs2=Decimal(str(math.pow(math.sin(B),2)))
        return Decimal(str( math.sqrt( 1-self.e1**2*bs2 ) ))

    #第二辅助函数
    #参数大地纬度 弧度
    #返回V Decimal类型
    def getV(self,B):
        bc2=Decimal(str(math.pow(math.cos(B),2)))
        return Decimal(str(math.sqrt(1+self.e2**2*bc2)))

    #子午线弧长计算
    #展开10次幂多项式的传统求X算法
    #参数 大地纬度B(弧度) 返回子午线弧长 Decimal类型
    def getX(self,b):
        A=Geo.A
        B=Geo.B
        C= Geo.C
        D=Geo.D
        E=Geo.E
        F=Geo.F
        #B为弧度单位 公式中p可去掉
        X=self.a*(1-self.e1*self.e1)*Decimal(str((A*float(b)-B/2*math.sin(2*b)+\
        C/4*math.sin(4*b)-D/6*math.sin(6*b)+E/8*math.sin(8*b))-F/10*math.sin(10*b)))
        return X

    #获取子午线弧长
    #参数 b(大地纬度的弧度) s
    #返回值 s=0,1,2 分别返回cgcs2000, 北京 54 , 西安 80坐标系下的子午线弧长  Decimal类型
    def getX3(self,b,s):
        if s==0:
            return Decimal(str(111132.95254700*math.degrees(b)-16038.508741268*math.sin(2*b)+16.832613326622*math.sin(4*b)-\
        0.021984374201268*math.sin(6*b)+3.1141625291648e-5*math.sin(8*b)))
        elif s==1:
            return  Decimal(str(111134.8611*math.degrees(b)-16036.4803*math.sin(2*b)+16.8281*math.sin(4*b)-0.022*math.sin(6*b)))
        elif s==2:
            return Decimal(str(111133.0047*math.degrees(b)-16038.5282*math.sin(2*b)+16.8326*math.sin(4*b)-0.022*math.sin(6*b)))
        pass

    #趋近法辅助计算Bf函数
    # 参数 Bf[i-1] 弧度 ,x,A,B,C,D=0,E=0,F=0
    #返回 Bfi 单位:度
    def Bf(self,Bf,x,A,B,C,D=0,E=0,F=0):
        Bfi=(x+B*math.sin(2*Bf)-C*math.sin(4*Bf)+D*math.sin(6*Bf)-E*math.sin(8*Bf)+F*math.sin(10*Bf))/A
        return Bfi

    #返回Bf垂直维度，即y=0 x=X时，用于高斯反算
    #参数 高斯坐标 x
    #返回Bf 单位:度 Decimal类型
    def getBf(self,x):
        x=float(x)
        v=float(self.a*(1-self.e1**2))
        #Bf为度数单位 需除去度数
        A=math.radians(v*Geo.A)
        B=v*Geo.B/2
        C=v*Geo.C/4
        D=v*Geo.D/6
        E=v*Geo.E/8
        F=v*Geo.F/10
        Bf0=x/A
        Bf=self.Bf(math.radians(Bf0),x,A,B,C,D,E,F)
        while abs(Bf-Bf0)>=2.8e-7:
            Bf0=Bf
            Bf=self.Bf(math.radians(Bf0),x,A,B,C,D,E,F)
            pass
        return Decimal(str(Bf))

    #返回Bf垂直维度，即y=0 x=X时，用于高斯反算
    #参数 x s
    #返回 s=0,1,2 分别返回cgcs2000, 北京 54 , 西安 80坐标系下的Bf  Decimal类型 单位：度
    def getBf3(self,x,s):
        x=float(x)
        s=int(s)
        A,B,C,D,E=0,0,0,0,0
        if s==0:
            A=111132.95254700
            B=16038.508741268
            C=16.832613326622
            D=0.021984374201268
            E=3.1141625291648e-5
            pass
        elif s==1:
            A=111134.8611
            B=16036.4803
            C=16.8281
            D=0.0220
            pass
        else :
            A=111133.0047
            B=16038.5282
            C=16.8326
            D=0.0220
            pass
        Bf0=x/A
        Bf=self.Bf(math.radians(Bf0),x,A,B,C,D,E)
        while abs(Bf-Bf0)>=2.8e-7:
            Bf0=Bf
            Bf=self.Bf(math.radians(Bf0),x,A,B,C,D,E)
            pass
        return Decimal(str(Bf))

    #大地坐标与大地空间直角坐标正算
    #参数L B(浮点数弧度) H
    #返回X Y Z大地空间直角坐标 Decimal类型
    #精度：0.0001
    def   geoAndGeoSpatialCal(self,L,B,H):
        H=Decimal(str(H))
        W=self.getW(B)
        V=self.getV(B)
        N=self.a/W;
        X=(N+H)*Decimal(str(math.cos(B)*math.cos(L)));
        Y=(N+H)*Decimal(str(math.cos(B)*math.sin(L)));
        Z=(N*(1-self.e1*self.e1)+Decimal(str(H)))*Decimal(str(math.sin(B)))

        return (X,Y,Z)

    #大地坐标与大地空间直角坐标反算
    #参数X Y Z
    #返回L B H大地坐标  Decimal类型
    #精度：0.0001
    def   geoAndGeoSpatialInvertedCal(self,X,Y,Z):
        X=Decimal(str(X))
        Y=Decimal(str(Y))
        Z=Decimal(str(Z))
        L=Decimal(str(math.degrees(math.atan(Y/X))));
        B0=Z/Decimal(str(math.sqrt(X*X+Y*Y)));
        while True:
            Bt=Decimal(str(1/math.sqrt(X*X+Y*Y)))*(Z+(self.a*self.e1*self.e1*B0)/Decimal(str(math.sqrt(1+B0*B0-self.e1*self.e1*B0*B0))))
            if abs(Bt-B0)<(5e-10):
                B0=Bt
                break
            else:
                B0=Bt
                pass
            pass
        #正切求弧度
        B=math.atan(B0)
        W=self.getW(B)
        N=self.a/W;
        H=Decimal(str(math.sqrt(X*X+Y*Y)/math.cos(B)))-N
        B=Decimal(str(math.degrees(B)))
        return (L,B,H)

    #高斯投影正算
    #精度 0.001m
    #参数 l B(浮点数弧度) d3 bool类型 为真则3度带计算
    #返回 x y y假定 Decimal类型
    #精度：0.001
    def geoAndGuassCal(self,L,B,d3,X):
        #3度带计算
        X=Decimal(str(X))
        l=math.degrees(L)
        if d3:
            #中央子午线经度及带数
            n3=int((l-1.5)/3)+1
            l3=3*n3
            #任一点与中央子午线经差
            l=l-l3
            l=math.radians(l)
            m=math.cos(B)*l
            W=self.getW(B)
            N=float(self.a/W)
            t=math.tan(B)
            n=float(self.e2)*math.cos(B)
            x=X+Decimal(str(N*t*(1/2*m*m+1/24*(5-t*t+9*n*n+4*math.pow(n,4))*math.pow(m,4)+1/720*(61-58*t*t+math.pow(t,4))*math.pow(m,6))))
            y=Decimal(str(N*(m+1/6*(1-t*t+n*n)*math.pow(m,3)+1/120*(5-18*t*t+math.pow(t,4)+14*n*n-58*n*n*t*t)*math.pow(m,5))))
            yf=Decimal(str(n3)+str((5e+5+float(y))))
            return (x,y,yf)
        else:
            #中央子午线经度及带数
            n6=int(l/6)
            if l%6!=0:
                n6+=1
                pass
            l6=6*n6-3
            #任一点与中央子午线经差
            l=l-l6
            l=math.radians(l)
            m=math.cos(B)*l
            W=self.getW(B)
            N=float(self.a/W)
            t=math.tan(B)
            n=float(self.e2)*math.cos(B)
            x=X+Decimal(str(N*t*(1/2*math.pow(m,2)+1/24*(5-t*t+9*n*n+4*math.pow(n,4))*math.pow(m,4)+1/720*(61-58*t*t+math.pow(t,4))*math.pow(m,6))))
            y=Decimal(str(N*(m+1/6*(1-t*t+n*n)*math.pow(m,3)+1/120*(5-18*t*t+math.pow(t,4)+14*n*n-58*n*n*t*t)*math.pow(m,5))))
            yf=Decimal(str(n6)+str((5e+5+float(y))))
            return (x,y,yf)
        pass


    #高斯投影反算
    #参数 高斯坐标x,y,y假定 d3 bool类型 为真则3度带计算 垂足纬度Bf（度）
    #返回 L B (度)
    #精度 0.0001m
    def geoAndGuassInvertedCal(self,x,y,yf,d3,Bf):
        Bf=math.radians(Bf)
        Vf=float(self.getV(Bf))
        Wf=self.getW(Bf)
        Nf=float(self.a/Wf)
        tf=math.tan(Bf)
        nf=float(self.e2)*math.cos(Bf)
        ynf=float(y)/Nf
        B=math.degrees(Bf)-math.degrees(1/2*Vf*Vf*tf*(math.pow(ynf,2)-1/12*(5+3*tf*tf+nf*nf-9*nf*nf*tf*tf)*math.pow(ynf,4)+1/360*(61+90*tf*tf+\
        45*math.pow(tf,4))*math.pow(ynf,6)))
        #经差
        l=math.degrees(1/math.cos(Bf)*(ynf-1/6*(1+2*tf*tf+nf*nf)*math.pow(ynf,3)+1/120*(5+28*tf*tf+24*math.pow(tf,4)+6*nf*nf+8*nf*nf*tf*tf)*math.pow(ynf,5)))
        #带数
        band=Decimal(str((5e+5)+float(y))).quantize(Decimal("1"))
        band=len(str(band))
        yf=str(Decimal(str(yf)).quantize(Decimal("1")))
        band=int(str(yf)[0:len(yf)-band])
        #中央子午线度数
        l36=None
        if d3:
            l36=3*band
            pass
        else:
            l36=6*band-3
            pass
        L=Decimal(str(l+l36))
        B=Decimal(str(B))
        return (L,B)


    #大地问题正解
    #参数 p1点的大地坐标L1 B1(度) p1p2之间的大地线长S,及大地方位角A1(度)
    #返回 p2点的大地坐标L2 B2(度) 以及大地线在p2点的大地反方位角 A2(度) Decimal类型
    def  geoProblemPSolutionCal(self,L1,B1,S,A1):
        L1=Decimal(str(L1))
        B1=Decimal(str(B1))
        S=Decimal(str(S))
        A1=Decimal(str(A1))
        #以度数为单位，所以许多参数乘以常数p度
        def fp(p):
            return math.degrees(p)
        #椭球元素投影到球面
        u1=math.atan(math.sqrt(1-self.e1*self.e1)*math.tan(math.radians(B1)))
        #辅助变量
        m=fp(math.asin(math.cos(u1)*math.sin(math.radians(A1))))
        if m<=0:
            m+=360
            pass
        M=fp(math.atan(math.tan(u1)/math.cos(math.radians(A1))))
        if M<=0:
            M+=180
            pass

        m,M=math.radians(m),math.radians(M)
        k2=math.pow(self.e2,2)*math.pow(math.cos(m),2)

        af=fp(math.sqrt(1+self.e2**2)/float(self.a)*(1-k2/4+7/64*k2*k2-15/256*k2**3))
        bt=fp(k2/4-k2*k2/8+37/512*k2**3)
        r=fp(k2*k2/128-k2**3/128)
        st0=af*float(S)
        while True:
            st=af*float(S)+bt*math.sin(math.radians(st0))*math.cos(2*M+math.radians(st0))+\
            r*math.sin(2*math.radians(st0))*math.cos(4*M+2*math.radians(st0))
            if abs(st-st0)<0.001/3600:
                break
            st0=st
            pass
        #解算球面三角形
        A2=fp(math.atan(math.tan(m)/math.cos(M+math.radians(st))))
        if A2<=0:
            A2+=180
            pass
        if A1<=180:
            A2+=180
            pass
        u2=math.atan(-(math.cos(math.radians(A2))*math.tan(M+math.radians(st))))
        nant1=fp(math.atan(math.sin(u1)*math.tan(math.radians(A1))))
        #m,M化为度数判断
        m,M=fp(m),fp(M)
        if nant1<=0:
            nant1+=180
            pass
        if m>=180:
            nant1+=180
            pass
        nant2=fp(math.atan(math.sin(u2)*math.tan(math.radians(A2))))
        if nant2<=0:
            nant2+=180
            pass
        if m<180:
            if M+st>=180:
                nant2+=180
                pass
            pass
        else:
            if M+st<=180:
                nant2+=180
                pass
            pass
        nant=nant2-nant1
        #m,M,st化为弧度计算
        m,M,st=math.radians(m),math.radians(M),math.radians(st)

        #将球面元素换算到椭球面上
        B2=fp(math.atan(math.sqrt(1+self.e2*self.e2)*math.tan(u2)))
        et=math.pow(self.e1,2)
        k12=et*math.pow(math.cos(m),2)
        af1=(et/2+et**2/8+et**3/16)-et/16*(1+et)*k12+3/128*et*k12**2
        bt1=fp(et/16*(1+et)*k12-et/32*k12**2)
        r1=fp(et/256*k12**2)
        #经差l 单位度
        l=nant-math.sin(m)*( af1*fp(st)+bt1*math.sin(st)*math.cos(2*M+st)+\
        r1*math.sin(2*st)*math.cos(4*M+2*st) )
        L2=L1+Decimal(str(l))
        B2=Decimal(str(B2))
        A2=Decimal(str(A2))
        return (L2,B2,A2)

    #大地问题反解
    #参数 p1 p2的大地坐标(度)
    #返回 p1p2之间的大地线S S在p1的大地方位角及在p2的大地反方位角 单位m Decimal类型
    def  geoProblemISolutionCal(self,L1,B1,L2,B2):
        L1 =math.radians(L1)
        B1 =math.radians(B1)
        L2 = math.radians(L2)
        B2 =math.radians(B2)


        e12=math.pow(self.e1,2)
        e22=math.pow(self.e2,2)
        u1 = math.atan(math.sqrt(1 -e12) * math.tan(B1))
        u2 = math.atan(math.sqrt(1 - e12) * math.tan(B2))
        l = L2 - L1

        sigma0 = math.acos(math.sin(u1) * math.sin(u2) + math.cos(u1) * math.cos(u2) * math.cos(l))
        m0 = math.asin(math.cos(u1) * math.cos(u2) * math.sin(l) / math.sin(sigma0))
        Dlambda = 0.003351 * sigma0 * math.sin(m0)
        lambda0 = l + Dlambda
        Dsigma = math.sin(m0) * Dlambda
        sigma1 = sigma0 + Dsigma
        # 迭代计算sigma以及mlambda
        while True:
            m = math.asin(math.cos(u1) * math.cos(u2) * math.sin(lambda0) / math.sin(sigma1))
            A1c = math.atan(math.sin(lambda0) / (math.cos(u1) * math.tan(u2) - math.sin(u1) *math.cos(lambda0)))
            if A1c < 0:
                A1c = A1c + math.pi
                pass
            if m < 0:
                A1c = A1c + math.pi
                pass
            M = math.atan(math.sin(u1) / math.sin(m) * math.tan(A1c))
            if M < 0:
                M = M +math.pi
                pass
            k_2 = e12 * math.cos(m)**2
            e4 =e12**2
            e6 = e12**3
            k_4 = k_2**2
            alpha_ = e12/2 + e4/8 + e6/16 - e12/16*(1 + e12)*k_2 + 3/128*e12*k_4
            beta_ = e12/16*(1 + e12)*k_2 - e12/32*k_4
            gama_ = e12/256*k_4

            mlambda = l + math.sin(m) * (alpha_*sigma1 + beta_*math.sin(sigma1)*math.cos(2*M + sigma1))
            sigma = math.acos(math.sin(u1) * math.sin(u2) + math.cos(u1) * math.cos(u2) * math.cos(mlambda))
            # 设定的精度为0.001秒
            if abs(sigma - sigma1) <2.8e-7:
                sigma1 = sigma
                lambda0 = mlambda
                break
            sigma1 = sigma
            lambda0 = mlambda
            pass
        A1 = math.atan(math.sin(mlambda) / (math.cos(u1)*math.tan(u2) - math.sin(u1)*math.cos(mlambda)))
        if A1 < 0:
            A1 = A1 + math.pi
            pass
        if m < 0:
            A1 = A1 +math. pi
            pass
        A2 = math.atan(math.sin(mlambda) / (math.sin(u2)*math.cos(mlambda) - math.tan(u1)*math.cos(u2)))
        if A2 < 0:
            A2 = A2 + math.pi
            pass
        if m > 0:
            A2 = A2 + math.pi
            pass

        k2 = e22 * math.cos(m)**2
        k4 = k2**2
        k6 = k2**3
        alpha = math.sqrt(1 +e22) /float(self.a) * (1 - k2/4 + 7*k4/64 - 15*k6/256)
        beta = k2/4 - k4/8 + 37*k6/512
        gamma = k4/128 + k6/128

        S = 1/alpha * (sigma - beta*math.sin(sigma)*math.cos(2*M+sigma) - gamma*math.sin(2*sigma)*math.cos(4*M+2*sigma))

        S=Decimal(str(S))
        A1 = Decimal(str(math.degrees(A1)))
        A2 = Decimal(str(math.degrees(A2)))
        return (S,A1,A2)


    pass
