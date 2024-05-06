from manimlib import *
from sympy import symbols, Eq, solve

class AdvancedGeometry_1_2(Scene):
    def construct(self):
# [0]
        # 标题
        title = Tex(R"\text{高等几何}").scale(2)
        subtitle = Tex(R"\text{第}_1\text{章：仿射坐标与仿射变换}").next_to(title,DOWN)
        subsubtitle = Tex(R"\text{§1 仿射对应与仿射变换}").scale(.5).next_to(subtitle,DOWN)
        MetaMiku = SVGMobject(R"E:\Desktop\MetaMiku\Projects\Manim\MetaMikuColor.svg",stroke_opacity=0).scale(.125).next_to(subsubtitle,DR)
        self.play(
            Write(title)
        )
        self.play(
            Write(subtitle),
            run_time = 2
        )
        self.play(
            Write(subsubtitle),
            run_time = 2
        )
        self.wait(1)
        self.play(
            Write(MetaMiku)
        )
        self.wait(3)
        self.play(
            FadeOut(Group(title,subtitle,subsubtitle)),
            MetaMiku.animate.to_edge(UL)
        )
        self.add(MetaMiku.to_edge(UL))
        # 建系
        axes = ThreeDAxes(
            x_axis_config={"include_tip": True},
            y_axis_config={"include_tip": True}
        )
        # axes.add_coordinate_labels()
        # self.add(axes)

        # 获取相机帧的引用
        camera = self.camera.frame
        camera.set_euler_angles(theta=0,phi=0,gamma=0,units=DEGREES)

        # 用于对标签初始化时指向摄像机，如：
        # oneLabel = Tex(R"P").apply_matrix(PointAtCamera()).move_to(aPoint)
        def MatrixPointingToCamera(theta=None,verphi=None,gamma=None):
            if None in [theta,verphi,gamma]:
                theta,verphi,gamma = camera.get_euler_angles()
            R1 = np.array([[math.cos(theta),-math.sin(theta), 0],
                           [math.sin(theta), math.cos(theta), 0],
                           [              0,              0 , 1]])
            R2 = np.array([[1,                0,                0],
                           [0, math.cos(verphi),-math.sin(verphi)],
                           [0, math.sin(verphi), math.cos(verphi)]])
            R3 = np.array([[math.cos(gamma),-math.sin(gamma), 0],
                           [math.sin(gamma), math.cos(gamma), 0],
                           [              0,              0 , 1]])
            R = R1 @ R2 @ R3
            return R
        def ac2p(_xyz) -> np.ndarray:
            return axes.c2p(_xyz[0],_xyz[1],_xyz[2])

# [1] 仿射坐标与仿射变换
    # [1.1] 透视放射对应
        # [1.2] 仿射对应与仿射变换
        # [1.2.1] 平面上线对线的仿射
        # [1.2.1.1] 绘图元素
        camera.set_euler_angles(theta=0,phi=0,gamma=0)

        a1LineFunc = lambda x: 1/6 * x + 17/6
        a1Line = axes.get_graph(function=a1LineFunc,x_range=[-4,1])
        a1LineLabel = Tex("a_1").next_to(axes.c2p(1,3,0),RIGHT,buff=.1)
        
        a2LineFunc = lambda x: -1/32 * x + 27/32
        a2Line = axes.get_graph(function=a2LineFunc,x_range=[-5,.2])
        a2LineLabel = Tex("a_2").next_to(axes.c2p(0,1,0),RIGHT,buff=.1)

        aiLineFunc = lambda x: 1/3 * x + 2/3
        aiLine = axes.get_graph(function=aiLineFunc,x_range=[-3.8,-.6])
        aiLineLabel = Tex("a_i").next_to(axes.c2p(-.5,.5,0),DR,buff=.1)
        
        anLineFunc = lambda x: -1/4 * x -9/4
        anLine = axes.get_graph(function=anLineFunc,x_range=[-3,2])
        anLineLabel = Tex("a_n").next_to(axes.c2p(2,-3,0),UR,buff=.1)
        self.play(
            ShowCreation(Group(a1Line,a2Line,aiLine,anLine)),
            Write(VGroup(a1LineLabel,a2LineLabel,aiLineLabel,anLineLabel))
        )
        # self.play(
        #     camera.animate.move_to(axes.c2p(2,1,0))
        # )
        def AffineFunc2D(Point:Dot,func,k:float) -> np.ndarray:
            x0,y0,_ = Point.get_center()
            x = symbols('x')
            x1 = solve(Eq(func(x),k*(x-x0)+y0), x)[0]
            y1 = func(x1)
            return axes.c2p(x1,y1,0)
        # [ERROR] 大段注释解释：
        # 本来是想做全局Tracker的，
        # 但是目前这个。。。
        # 基础的就有三个Tracker
        # 然后在此基础上每个Tracker衍生了4个Dot，4个Tex，3个Line
        # 明显感觉渲染卡顿，而且有莫名的抖动，目前很迷惑，还不如不加Tracker，反正这里也无关紧要
        """
        T1 = Tracker1 = ValueTracker(-3)
        T2 = Tracker2 = ValueTracker(-2)
        T3 = Tracker3 = ValueTracker(-1)
        A1dot = Dot(color=GREEN).scale(.75)
        B1dot = Dot(color=TEAL).scale(.75)
        C1dot = Dot(color=BLUE).scale(.75)
        f_always(A1dot.move_to, lambda: axes.c2p(T1.get_value(),a1LineFunc(T1.get_value()),0))
        f_always(B1dot.move_to, lambda: axes.c2p(T2.get_value(),a1LineFunc(T2.get_value()),0))
        f_always(C1dot.move_to, lambda: axes.c2p(T3.get_value(),a1LineFunc(T3.get_value()),0))
        A1dotLabel = Tex(R"A_1",color=GREEN).scale(.75)
        B1dotLabel = Tex(R"B_1",color=TEAL).scale(.75)
        C1dotLabel = Tex(R"C_1",color=BLUE).scale(.75)
        always(A1dotLabel.next_to, A1dot,UL,buff=.1)
        always(B1dotLabel.next_to, B1dot,UL,buff=.1)
        always(C1dotLabel.next_to, C1dot,UL,buff=.1)
        A2dot = Dot(color=GREEN).scale(.75).move_to(AffineFunc2D(A1dot,a2LineFunc,1))
        B2dot = Dot(color=TEAL).scale(.75).move_to(AffineFunc2D(B1dot,a2LineFunc,1))
        C2dot = Dot(color=BLUE).scale(.75).move_to(AffineFunc2D(B1dot,a2LineFunc,1))
        f_always(A2dot.move_to, lambda: AffineFunc2D(A1dot,a2LineFunc,1))
        f_always(B2dot.move_to, lambda: AffineFunc2D(B1dot,a2LineFunc,1))
        f_always(C2dot.move_to, lambda: AffineFunc2D(C1dot,a2LineFunc,1))
        A2dotLabel = Tex(R"A_2",color=GREEN).scale(.75)
        B2dotLabel = Tex(R"B_2",color=TEAL).scale(.75)
        C2dotLabel = Tex(R"C_2",color=BLUE).scale(.75)
        always(A2dotLabel.next_to, A2dot,UR,buff=.1)
        always(B2dotLabel.next_to, B2dot,UR,buff=.1)
        always(C2dotLabel.next_to, C2dot,UR,buff=.1)
        Aidot = Dot(color=GREEN).scale(.75).scale(.75)
        Bidot = Dot(color=TEAL).scale(.75).scale(.75)
        Cidot = Dot(color=BLUE).scale(.75).scale(.75)
        f_always(Aidot.move_to, lambda: AffineFunc2D(A2dot,aiLineFunc,-1))
        f_always(Bidot.move_to, lambda: AffineFunc2D(B2dot,aiLineFunc,-1))
        f_always(Cidot.move_to, lambda: AffineFunc2D(C2dot,aiLineFunc,-1))
        AidotLabel = Tex(R"A_i",color=GREEN).scale(.75)
        BidotLabel = Tex(R"B_i",color=TEAL).scale(.75)
        CidotLabel = Tex(R"C_i",color=BLUE).scale(.75)
        always(AidotLabel.next_to, Aidot,UL,buff=.1)
        always(BidotLabel.next_to, Bidot,UL,buff=.1)
        always(CidotLabel.next_to, Cidot,UL,buff=.1)
        Andot = Dot(color=GREEN).scale(.75)
        Bndot = Dot(color=TEAL).scale(.75)
        Cndot = Dot(color=BLUE).scale(.75)
        f_always(Andot.move_to, lambda: AffineFunc2D(Aidot,anLineFunc,-3))
        f_always(Bndot.move_to, lambda: AffineFunc2D(Bidot,anLineFunc,-3))
        f_always(Cndot.move_to, lambda: AffineFunc2D(Cidot,anLineFunc,-3))
        AndotLabel = Tex(R"A_i",color=GREEN).scale(.75)
        BndotLabel = Tex(R"B_i",color=TEAL).scale(.75)
        CndotLabel = Tex(R"C_i",color=BLUE).scale(.75)
        always(AndotLabel.next_to, Andot,DL,buff=.1)
        always(BndotLabel.next_to, Bndot,DL,buff=.1)
        always(CndotLabel.next_to, Cndot,DL,buff=.1)
        self.play(
            ShowCreation(VGroup(A1dot,B1dot,C1dot)),
            ShowCreation(VGroup(A2dot,B2dot,C2dot)),
            ShowCreation(VGroup(Aidot,Bidot,Cidot)),
            ShowCreation(VGroup(Andot,Bndot,Cndot)),
            Write(VGroup(A1dotLabel,B1dotLabel,C1dotLabel)),
            Write(VGroup(A2dotLabel,B2dotLabel,C2dotLabel)),
            Write(VGroup(AidotLabel,BidotLabel,CidotLabel)),
            Write(VGroup(AndotLabel,BndotLabel,CndotLabel)),
        )
        self.wait(3)
        self.play(T1.animate.set_value(3),run_time=3)
        """
        
        A1dot = Dot(color=GREEN).scale(.75).move_to(axes.c2p(-2.5,a1LineFunc(-2.5),0))
        B1dot = Dot(color=TEAL).scale(.75).move_to(axes.c2p(-1.2,a1LineFunc(-1.2),0))
        C1dot = Dot(color=BLUE).scale(.75).move_to(axes.c2p(.5,a1LineFunc(.5),0))
        A1dotLabel = Tex(R"A_1",color=GREEN).scale(.75).next_to(A1dot,UL,buff=.1)
        B1dotLabel = Tex(R"B_1",color=TEAL).scale(.75).next_to(B1dot,UL,buff=.1)
        C1dotLabel = Tex(R"C_1",color=BLUE).scale(.75).next_to(C1dot,UL,buff=.1)
        A2dot = Dot(color=GREEN).scale(.75).move_to(AffineFunc2D(A1dot,a2LineFunc,1))
        B2dot = Dot(color=TEAL).scale(.75).move_to(AffineFunc2D(B1dot,a2LineFunc,1))
        C2dot = Dot(color=BLUE).scale(.75).move_to(AffineFunc2D(C1dot,a2LineFunc,1))
        A2dotLabel = Tex(R"A_2",color=GREEN).scale(.75).next_to(A2dot,DL,buff=.1)
        B2dotLabel = Tex(R"B_2",color=TEAL).scale(.75).next_to(B2dot,DL,buff=.1)
        C2dotLabel = Tex(R"C_2",color=BLUE).scale(.75).next_to(C2dot,DL,buff=.1)
        Aidot = Dot(color=GREEN).scale(.75).move_to(AffineFunc2D(A2dot,aiLineFunc,-1))
        Bidot = Dot(color=TEAL).scale(.75).move_to(AffineFunc2D(B2dot,aiLineFunc,-1))
        Cidot = Dot(color=BLUE).scale(.75).move_to(AffineFunc2D(C2dot,aiLineFunc,-1))
        AidotLabel = Tex(R"A_i",color=GREEN).scale(.75).next_to(Aidot,DR,buff=.1)
        BidotLabel = Tex(R"B_i",color=TEAL).scale(.75).next_to(Bidot,DR,buff=.1)
        CidotLabel = Tex(R"C_i",color=BLUE).scale(.75).next_to(Cidot,DR,buff=.1)
        Andot = Dot(color=GREEN).scale(.75).move_to(AffineFunc2D(Aidot,anLineFunc,-3))
        Bndot = Dot(color=TEAL).scale(.75).move_to(AffineFunc2D(Bidot,anLineFunc,-3))
        Cndot = Dot(color=BLUE).scale(.75).move_to(AffineFunc2D(Cidot,anLineFunc,-3))
        AndotLabel = Tex(R"A_i",color=GREEN).scale(.75).next_to(Andot,DR,buff=.1)
        BndotLabel = Tex(R"B_i",color=TEAL).scale(.75).next_to(Bndot,DR,buff=.1)
        CndotLabel = Tex(R"C_i",color=BLUE).scale(.75).next_to(Cndot,DR,buff=.1)
        A12Line = Line(start=A1dot,end=A2dot,color=GREEN)
        B12Line = Line(start=B1dot,end=B2dot,color=TEAL)
        C12Line = Line(start=C1dot,end=C2dot,color=BLUE)
        A2iLine = Line(start=A2dot,end=Aidot,color=GREEN)
        B2iLine = Line(start=B2dot,end=Bidot,color=TEAL)
        C2iLine = Line(start=C2dot,end=Cidot,color=BLUE)
        AinLine = Line(start=Aidot,end=Andot,color=GREEN)
        BinLine = Line(start=Bidot,end=Bndot,color=TEAL)
        CinLine = Line(start=Cidot,end=Cndot,color=BLUE)
        phi1Arrow = Arrow(start=axes.c2p(-3.8,2,0),end=axes.c2p(-4.3,1.5,0),buff=0,color=PURPLE_B)
        phi2Arrow = Arrow(start=axes.c2p(-4.5,.2,0),end=axes.c2p(-4,-.3,0),buff=0,color=PURPLE_B)
        phi3Arrow = Arrow(start=axes.c2p(-3.2,-.8,0),end=axes.c2p(-3,-1.4,0),buff=0,color=PURPLE_B)
        phi1ArrowLabel = Tex(R"\varphi _{_1}",color=PURPLE_B).next_to(phi1Arrow,LEFT,buff=.1)
        phi2ArrowLabel = Tex(R"\varphi _{_2}",color=PURPLE_B).next_to(phi2Arrow,LEFT,buff=.1)
        phi3ArrowLabel = Tex(R"\varphi _{_i}",color=PURPLE_B).next_to(phi3Arrow,LEFT,buff=.1)
        #self.play(
        #    ShowCreation(VGroup(A1dot,B1dot,C1dot)),
        #    ShowCreation(VGroup(A2dot,B2dot,C2dot)),
        #    ShowCreation(VGroup(Aidot,Bidot,Cidot)),
        #    ShowCreation(VGroup(Andot,Bndot,Cndot)),
        #    Write(VGroup(A1dotLabel,B1dotLabel,C1dotLabel)),
        #    Write(VGroup(A2dotLabel,B2dotLabel,C2dotLabel)),
        #    Write(VGroup(AidotLabel,BidotLabel,CidotLabel)),
        #    Write(VGroup(AndotLabel,BndotLabel,CndotLabel)),
        #)
        self.play(
            ShowCreation(A1dot),
            ShowCreation(B1dot),
            ShowCreation(C1dot),
            Write(A1dotLabel),
            Write(B1dotLabel),
            Write(C1dotLabel),
            run_time = .5
        )
        self.play(
            Write(phi1Arrow),
            Write(phi1ArrowLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(A12Line),
            ShowCreation(B12Line),
            ShowCreation(C12Line),
            run_time = .5
        )
        self.play(
            ShowCreation(A2dot),
            ShowCreation(B2dot),
            ShowCreation(C2dot),
            Write(A2dotLabel),
            Write(B2dotLabel),
            Write(C2dotLabel),
            run_time = .5
        )
        self.play(
            Write(phi2Arrow),
            Write(phi2ArrowLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(A2iLine),
            ShowCreation(B2iLine),
            ShowCreation(C2iLine),
            run_time = .5
        )
        self.play(
            ShowCreation(Aidot),
            ShowCreation(Bidot),
            ShowCreation(Cidot),
            Write(AidotLabel),
            Write(BidotLabel),
            Write(CidotLabel),
            run_time = .5
        )
        self.play(
            Write(phi3Arrow),
            Write(phi3ArrowLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(AinLine),
            ShowCreation(BinLine),
            ShowCreation(CinLine),
            run_time = .5
        )
        self.play(
            ShowCreation(Andot),
            ShowCreation(Bndot),
            ShowCreation(Cndot),
            Write(AndotLabel),
            Write(BndotLabel),
            Write(CndotLabel),
            run_time = .5
        )
        # [] 提出仿射对应
        text_010202 = TexText("仿射对应")
        text_010201 = VGroup(
            Tex("a_1"),
            TexText("到"),
            Tex("a_n"),
            TexText("的")
        ).arrange(direction=RIGHT)
        VGroup(text_010201,text_010202).arrange(direction=RIGHT).to_edge(UR)
        latex_010201 = Tex(R"\varphi : a_{1} \to a_{n}",color=PURPLE_B).next_to(text_010201,DOWN)
        latex_010202 = Tex(R"\varphi",color=PURPLE_B)
        latex_010203 = Tex(R"=\varphi _{_{n-1}} \cdot \varphi _{_{n-2}} \cdot \cdots \cdot \varphi_{_{2}} \cdot \varphi_{_{1}}",color=PURPLE_B)
        latex_010204 = VGroup(latex_010202,latex_010203).arrange(direction=RIGHT).next_to(latex_010201,DOWN).to_edge(RIGHT)
        self.play(
            Write(VGroup(text_010201,text_010202)),
            run_time = 2
        )
        self.wait(1)
        self.play(
            TransformFromCopy(text_010201,latex_010201)
        )
        self.wait(2)
        self.play(
            TransformFromCopy(latex_010201,latex_010202)
        )
        self.wait(1)
        self.play(
            TransformFromCopy(latex_010202,latex_010203)
        )
        self.wait(3)
        text_010203 = VGroup(
            TexText("如果直线"),
            Tex("a_1"),
            TexText("与"),
            Tex("a_n"),
            TexText("重合")
        ).arrange(direction=RIGHT).next_to(latex_010204,DOWN).to_edge(RIGHT)
        self.play(
            Write(text_010203),
            run_time=2
        )
        self.wait(2)
        text_010204 = TexText("仿射变换",color=PURPLE_B).move_to(text_010202)
        text_010201_ = VGroup(
            Tex("a_1"),
            TexText("到"),
            TexText("自身"),
            TexText("的")
        ).arrange(direction=RIGHT).next_to(text_010204,LEFT)
        text_010202HighLight = SurroundingRectangle(text_010202, color=PURPLE_B, fill_opacity=0.1)
        self.play(
            ShowCreation(text_010202HighLight),
        )
        self.play(
            ReplacementTransform(text_010202,text_010204),
            ReplacementTransform(text_010201,text_010201_)
        )
        self.wait(.5)
        self.play(
            FadeOut(text_010202HighLight)
        )
        self.wait(2)
        self.play(
            FadeOut(text_010203),
        )
        self.wait(4)
        self.play(
            FadeOut(Group(A1dot,B1dot,C1dot)),
            FadeOut(Group(A2dot,B2dot,C2dot)),
            FadeOut(Group(Aidot,Bidot,Cidot)),
            FadeOut(Group(Andot,Bndot,Cndot)),
            FadeOut(Group(A1dotLabel,B1dotLabel,C1dotLabel)),
            FadeOut(Group(A2dotLabel,B2dotLabel,C2dotLabel)),
            FadeOut(Group(AidotLabel,BidotLabel,CidotLabel)),
            FadeOut(Group(AndotLabel,BndotLabel,CndotLabel)),
            FadeOut(Group(a1Line,a2Line,aiLine,anLine)),
            FadeOut(Group(a1LineLabel,a2LineLabel,aiLineLabel,anLineLabel)),
            FadeOut(Group(A12Line,B12Line,C12Line)),
            FadeOut(Group(A2iLine,B2iLine,C2iLine)),
            FadeOut(Group(AinLine,BinLine,CinLine)),
            FadeOut(Group(phi1Arrow,phi2Arrow,phi3Arrow)),
            FadeOut(Group(phi1ArrowLabel,phi2ArrowLabel,phi3ArrowLabel)),
            FadeOut(Group(text_010201_,text_010204,latex_010201,latex_010202,latex_010203))
        )
        # [1.2.2.1] 构建必要函数
        #pi1 = ["func":lambda x,y:0]
        camera.set_euler_angles(theta=15,phi=75,gamma=0,units=DEGREES)
        MetaMiku.apply_matrix(MatrixPointingToCamera())
        #self.wait(2)
        def createPlane(ABCD, pointsxy, color=GREY, opacity=.5):
            A,B,C,D = ABCD
            func = lambda x,y: (A*x + B*y + D)/(-C)
            pointsxyz = [[pointsxy[0][0],pointsxy[0][1],func(pointsxy[0][0],pointsxy[0][1])],
                         [pointsxy[1][0],pointsxy[1][1],func(pointsxy[1][0],pointsxy[1][1])],
                         [pointsxy[2][0],pointsxy[2][1],func(pointsxy[2][0],pointsxy[2][1])],
                         [pointsxy[3][0],pointsxy[3][1],func(pointsxy[3][0],pointsxy[3][1])]]
            return {'A':A,
                    'B':B,
                    'C':C,
                    'D':D,
                    'points':pointsxyz,
                    'ABCD':(A,B,C,D),
                    'func': func ,
                    'color': color ,
                    'Mobject': Polygon(*pointsxyz, color=color).set_fill(GREY, opacity=0.5)}
        def AffineFunc3D(Point:Sphere,plane,vector) -> np.ndarray:
            x0,y0,z0 = Point.get_center()
            a,b,c = vector
            A,B,C,D = plane['ABCD']
            t = - (A*x0 + B*y0 + C*z0 + D) / (A*a + B*b + C*c)
            return axes.c2p(x0 + a*t, y0 + b*t, z0 + c*t)
        pi1 = createPlane([3,5,-15,15], [[-3,-.75],[-1.5,-.75],[-1.5,.75],[-3,.75]])
        pi2 = createPlane([1,0,5,5], [[-3,-.75],[-1.5,-.75],[-1.5,.75],[-3,.75]])
        pii = createPlane([0,0,1,2], [[-2,-2],[-2,2],[2,2],[2,-2]])
        pin = createPlane([4,-3,12,-12],[[1,1],[2.5,2.5],[4.5,1],[3,-.5]])
        pi1Label = Tex(R"\pi_1",color=WHITE).apply_matrix(MatrixPointingToCamera()).move_to(ac2p(pi1['points'][0]))
        pi2Label = Tex(R"\pi_2",color=WHITE).apply_matrix(MatrixPointingToCamera()).move_to(ac2p(pi2['points'][0]))
        piiLabel = Tex(R"\pi_i",color=WHITE).apply_matrix(MatrixPointingToCamera()).move_to(ac2p(pii['points'][0]))
        pinLabel = Tex(R"\pi_n",color=WHITE).apply_matrix(MatrixPointingToCamera()).move_to(ac2p(pin['points'][0]))
        A1dot = Sphere(radius=.05,color=GREEN).move_to(axes.c2p(-2,-.2,pi1['func'](-2,-.2)))
        B1dot = Sphere(radius=.05,color=TEAL).move_to(axes.c2p(-2.5,0,pi1['func'](-2.5,0)))
        C1dot = Sphere(radius=.05,color=BLUE).move_to(axes.c2p(-1.8,.5,pi1['func'](-1.8,.5)))
        A1dotLabel = Tex(R"A_1",color=GREEN).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(A1dot,UP,buff=.5)
        B1dotLabel = Tex(R"B_1",color=TEAL).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(B1dot,UP,buff=.5)
        C1dotLabel = Tex(R"C_1",color=BLUE).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(C1dot,UP,buff=.5)
        phi1vector = [1,0,3]
        A2dot = Sphere(radius=.05,color=GREEN).move_to(AffineFunc3D(A1dot, pi2, phi1vector))
        B2dot = Sphere(radius=.05,color=TEAL).move_to(AffineFunc3D(B1dot, pi2, phi1vector))
        C2dot = Sphere(radius=.05,color=BLUE).move_to(AffineFunc3D(C1dot, pi2, phi1vector))
        A2dotLabel = Tex(R"A_2",color=GREEN).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(A2dot,UL,buff=.2)
        B2dotLabel = Tex(R"B_2",color=TEAL).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(B2dot,UL,buff=.2)
        C2dotLabel = Tex(R"C_2",color=BLUE).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(C2dot,UL,buff=.2)
        phi2vector = [4,1,-3]
        Aidot = Sphere(radius=.05,color=GREEN).move_to(AffineFunc3D(A2dot, pii, phi2vector))
        Bidot = Sphere(radius=.05,color=TEAL).move_to(AffineFunc3D(B2dot, pii, phi2vector))
        Cidot = Sphere(radius=.05,color=BLUE).move_to(AffineFunc3D(C2dot, pii, phi2vector))
        AidotLabel = Tex(R"A_i",color=GREEN).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(Aidot,DOWN,buff=.5)
        BidotLabel = Tex(R"B_i",color=TEAL).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(Bidot,DOWN,buff=.5)
        CidotLabel = Tex(R"C_i",color=BLUE).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(Cidot,DOWN,buff=.5)
        phiivector = [4,.5,3]
        Andot = Sphere(radius=.05,color=GREEN).move_to(AffineFunc3D(Aidot, pin, phiivector))
        Bndot = Sphere(radius=.05,color=TEAL).move_to(AffineFunc3D(Bidot, pin, phiivector))
        Cndot = Sphere(radius=.05,color=BLUE).move_to(AffineFunc3D(Cidot, pin, phiivector))
        AndotLabel = Tex(R"A_n",color=GREEN).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(Andot,UR,buff=.2)
        BndotLabel = Tex(R"B_n",color=TEAL).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(Bndot,UR,buff=.2)
        CndotLabel = Tex(R"C_n",color=BLUE).scale(.5).apply_matrix(MatrixPointingToCamera()).next_to(Cndot,UR,buff=.2)
        A12Line = Line3D(start=A1dot.get_center(), end=A2dot.get_center(), color = GREEN, width=.025)
        B12Line = Line3D(start=B1dot.get_center(), end=B2dot.get_center(), color = TEAL , width=.025)
        C12Line = Line3D(start=C1dot.get_center(), end=C2dot.get_center(), color = BLUE , width=.025)
        A2iLine = Line3D(start=A2dot.get_center(), end=Aidot.get_center(), color = GREEN, width=.025)
        B2iLine = Line3D(start=B2dot.get_center(), end=Bidot.get_center(), color = TEAL , width=.025)
        C2iLine = Line3D(start=C2dot.get_center(), end=Cidot.get_center(), color = BLUE , width=.025)
        AinLine = Line3D(start=Aidot.get_center(), end=Andot.get_center(), color = GREEN, width=.025)
        BinLine = Line3D(start=Bidot.get_center(), end=Bndot.get_center(), color = TEAL , width=.025)
        CinLine = Line3D(start=Cidot.get_center(), end=Cndot.get_center(), color = BLUE , width=.025)

        self.play(
            ShowCreation(pi1['Mobject']),
            Write(pi1Label),
            run_time=.5
        )
        self.play(
            ShowCreation(A1dot),
            ShowCreation(B1dot),
            ShowCreation(C1dot),
            Write(A1dotLabel),
            Write(B1dotLabel),
            Write(C1dotLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(A12Line),
            ShowCreation(B12Line),
            ShowCreation(C12Line),
            run_time=.5
        )
        self.play(
            ShowCreation(pi2['Mobject']),
            Write(pi2Label),
            run_time=.5
        )
        self.play(
            ShowCreation(A2dot),
            ShowCreation(B2dot),
            ShowCreation(C2dot),
            Write(A2dotLabel),
            Write(B2dotLabel),
            Write(C2dotLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(A2iLine),
            ShowCreation(B2iLine),
            ShowCreation(C2iLine),
            run_time=.5
        )
        self.play(
            ShowCreation(pii['Mobject']),
            Write(piiLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(Aidot),
            ShowCreation(Bidot),
            ShowCreation(Cidot),
            Write(AidotLabel),
            Write(BidotLabel),
            Write(CidotLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(AinLine),
            ShowCreation(BinLine),
            ShowCreation(CinLine),
            run_time=.5
        )
        self.play(
            ShowCreation(pin['Mobject']),
            Write(pinLabel),
            run_time=.5
        )
        self.play(
            ShowCreation(Andot),
            ShowCreation(Bndot),
            ShowCreation(Cndot),
            Write(AndotLabel),
            Write(BndotLabel),
            Write(CndotLabel),
            run_time=.5
        )
        self.wait(1)
        self.play(
            camera.animate.set_euler_angles(theta=180+15,phi=60,gamma=0,units=DEGREES),
            run_time = 4
        )
        self.play(
            camera.animate.set_euler_angles(theta=360+15,phi=75,gamma=0,units=DEGREES),
            run_time = 4
        )
        latex_010204 = VGroup(
            TexText(R"当"),
            Tex(R"\pi_1"),
            TexText(R"与"),
            Tex(R"\pi_n"),
            TexText(R"重合时，"),
            Tex(R"\varphi"),
            TexText(R"称为平面"),
            Tex(R"\pi_1"),
            TexText(R"到自身的仿射变换"),
        ).arrange(RIGHT).to_edge(DOWN).apply_matrix(MatrixPointingToCamera())
        self.play(
            Write(latex_010204),
            run_time = 2
        )
        self.wait(3)
        latex_010205 = TexText(R"仿射对应和仿射变换都是一串透视仿射对应的乘积")
        latex_010206 = TexText(R"称为")
        latex_010207 = TexText(R"透视仿射对应链",color=GREY_A)
        VGroup(latex_010205,latex_010206,latex_010207).scale(.75).arrange(RIGHT).to_edge(DOWN).apply_matrix(MatrixPointingToCamera())
        self.play(
            ReplacementTransform(latex_010204,latex_010205)
        )
        self.wait(2)
        self.play(
            TransformFromCopy(latex_010205,latex_010206) # VGroup(latex_010206,latex_010207)
        )
        self.wait(.5)
        self.play(
            TransformFromCopy(latex_010206,latex_010207)
        )
        self.wait(3)
        latex_010208 = TexText(R"透视仿射对应链",color=GREY_A)
        latex_010208.to_edge(UR).apply_matrix(MatrixPointingToCamera())
        self.play(
            ReplacementTransform(latex_010207,latex_010208),
            FadeOut(latex_010205),
            FadeOut(latex_010206)
        )
        latex_010209 = TexText(R"(1)保持同素性和结合性").to_edge(DOWN).apply_matrix(MatrixPointingToCamera())
        latex_010210 = TexText(R"(2)保持共线三点的单比不变").to_edge(DOWN).apply_matrix(MatrixPointingToCamera())
        latex_010211 = TexText(R"(3)保持直线的平行性").to_edge(DOWN).apply_matrix(MatrixPointingToCamera())
        latex_010212 = TexText(R"注意：对两个点集来讲，在仿射对应下，对应点连线不一定平行").to_edge(DOWN).apply_matrix(MatrixPointingToCamera())
        self.wait(.5)
        self.play(
            Write(latex_010209),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(latex_010209,latex_010210)
        )
        self.wait(2)
        self.play(
            ReplacementTransform(latex_010210,latex_010211)
        )
        self.wait(3)
        self.play(
            ReplacementTransform(latex_010211,latex_010212)
        )
        self.wait(2)
        self.play(
            FadeOut(latex_010212),
            FadeOut(latex_010208)
        )
        self.wait(1)
        self.play(
            FadeOut(Group(A1dot,B1dot,C1dot)),
            FadeOut(Group(A2dot,B2dot,C2dot)),
            FadeOut(Group(Aidot,Bidot,Cidot)),
            FadeOut(Group(Andot,Bndot,Cndot)),
            FadeOut(Group(A1dotLabel,B1dotLabel,C1dotLabel)),
            FadeOut(Group(A2dotLabel,B2dotLabel,C2dotLabel)),
            FadeOut(Group(AidotLabel,BidotLabel,CidotLabel)),
            FadeOut(Group(AndotLabel,BndotLabel,CndotLabel)),
            FadeOut(Group(A12Line,B12Line,C12Line)),
            FadeOut(Group(A2iLine,B2iLine,C2iLine)),
            FadeOut(Group(AinLine,BinLine,CinLine)),
            FadeOut(Group(pi1['Mobject'],pi2['Mobject'],pii['Mobject'],pin['Mobject'])),
            FadeOut(Group(pi1Label,pi2Label,piiLabel,pinLabel))
        )
        # [0]
        MetaMiku_ = SVGMobject(R"E:\Desktop\MetaMiku\Projects\Manim\MetaMikuColor.svg",stroke_opacity=0).scale(.125).apply_matrix(MatrixPointingToCamera())
        self.wait(1)
        self.play(
            MetaMiku.animate.move_to(MetaMiku_).scale(2)
        )
        self.wait(3)
        self.play(
            FadeOut(MetaMiku),
        )
        self.wait(9)
        

        
        
if __name__ == '__main__':
    from os import system
    system(f"manimgl {__file__}")