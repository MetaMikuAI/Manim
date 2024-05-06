from manimlib import *
from scipy.optimize import fsolve
import math

class ECCdemo(Scene):
    def construct(self):
# Chapter-0: 开头，标题和签名
        title = Tex(R"ECC").scale(2)
        subtitle = Tex(R"Elliptic-curve~cryptography").next_to(title,DOWN)
        MetaMiku = SVGMobject(R"E:\Desktop\MetaMikuColor.svg",stroke_opacity=0).scale(.125).next_to(subtitle,DR)
        self.play(
            Write(title)
        )
        self.play(
            Write(subtitle),
            run_time = 3
        )
        self.wait(1)
        self.play(
            Write(MetaMiku)
        )
        self.wait(1)
        self.play(
            FadeOut(VGroup(title,subtitle)),
            MetaMiku.animate.to_edge(DR)
        )
        self.wait(.5)
# Chapter-1：椭圆曲线和坐标系的绘制
        # [1.1] 建立平面直角坐标系
        axes = Axes(
            x_range = (-7, 7),
            y_range = (-6, 6),
            x_axis_config={
                "include_tip": True,
            },
            y_axis_config={
                "include_tip": True,
            }
            )
        axes.add_coordinate_labels()

        # [1.2] 设椭圆曲线
        a,b = -5,10
        curve1_func = lambda x: math.sqrt(x**3+a*x+b)
        curve2_func = lambda x:-math.sqrt(x**3+a*x+b)
        curve1 = axes.get_graph(
            curve1_func,
            x_range=(-2.905474,64),
            color=BLUE,
        )
        curve2 = axes.get_graph(
            curve2_func,
            x_range=(-2.905474,64),
            color=BLUE,
        ) 
        curve_label1 = axes.get_graph_label(curve2, R"y^2 = x^3 +ax +b")
        curve_label2 = axes.get_graph_label(curve2, R"y^2 = x^3 -5x +10")
        self.play(
            ShowCreation(curve1),
            ShowCreation(curve2),
            FadeIn(curve_label1, RIGHT),
            run_time = 1
        )
        self.wait(2)

        # [1.3] 平面直角坐标系的绘制和椭圆曲线的量化显示
        self.play(
            Write(axes, lag_ratio=0.01, run_time=2),
            ReplacementTransform(curve_label1,curve_label2)
        )
        self.wait(2)

# Chapter-2：演示P+Q运算
        # [2.1] 创建点P
        Pdot_x = -2.8
        Pdot_x_tracker = ValueTracker(Pdot_x)   # 设P的x坐标为动态
        Pdot_y = curve1_func(Pdot_x_tracker.get_value())
        Pdot = Dot(color=RED) # .move_to(axes.i2gp(Pdot_x_tracker.get_value(), curve1))
        f_always(Pdot.move_to, lambda: axes.i2gp(Pdot_x_tracker.get_value(), curve1)) # 设点P绑定到动态的P_x坐标
        Pdot_label = Tex(R"P", color=RED).next_to(Pdot, UL, buff=0.1)
        always(Pdot_label.next_to, Pdot, UL, 0.1) # 设P标签绑定到动态的点P
        self.play(
            ShowCreation(Pdot, scale=0.25),
            ShowCreation(Pdot_label),
            run_time = .5
        )

        # [2.2] 创建点Q
        Qdot_x = .5
        Qdot_x_tracker = ValueTracker(Qdot_x)   # 设Q的x坐标为动态
        Qdot_y = curve1_func(Qdot_x_tracker.get_value())
        Qdot = Dot(color=RED) # .move_to(axes.i2gp(Qdot_x_tracker.get_value(), curve1))
        f_always(Qdot.move_to, lambda: axes.i2gp(Qdot_x_tracker.get_value(), curve1)) # 设点Q绑定到动态的Q_x坐标
        Qdot_label = Tex(R"Q", color=RED) # .next_to(Qdot, DOWN, buff=0.1)
        always(Qdot_label.next_to, Qdot,DOWN,0.1) # 设Q标签绑定到动态的点Q
        self.play(
            ShowCreation(Qdot, scale=0.25),
            ShowCreation(Qdot_label),
            run_time = .5
        )

        # [2.3] 抛出问题"P+Q=?"
        latex2_1 = Tex(R"P+Q = ")
        latex2_2 = Tex(R"?")
        latex2 = VGroup(latex2_1,latex2_2).arrange(RIGHT, aligned_edge=LEFT,buff = 1.2).to_edge(UL)
        self.play(
            Write(latex2)
        )
        self.wait(2)

        # [2.4] 创建伪直线PQ
        def CalcPQlineFunc(Px:float,Qx:float,curve_func,axes)->ParametricCurve:
            Py = curve_func(Px)
            Qy = curve_func(Qx)
            dx = Px - Qx
            dy = Py - Qy
            #ds = math.sqrt(dx**2 + dy**2)
            #return lambda t: axes.c2p(dx*t/ds + Px, dy*t/ds + Py)
            return lambda x: dy/dx*(x-Px)+Py
        PQline = always_redraw(lambda: axes.get_graph(CalcPQlineFunc(Pdot_x_tracker.get_value(),Qdot_x_tracker.get_value(),curve1_func,axes),color=WHITE,x_range=[-8,8,2]))
        self.play(
            ShowCreation(PQline),
            run_time = .5
        )

        # [2.5] 创建交点R'
        def PointADD(Px:float,Qx:float,func,m:bool):
            Py = func(Px)
            Qy = func(Qx)
            k = (Py - Qy) / (Px - Qx)
            Rx = k**2 - Px - Qx
            Ry = k*(Px - Rx) -Py
            return axes.c2p(Rx,Ry if m else -Ry)
        # R_dot_x = lambda: PointADD_x(Pdot_x_tracker.get_value(),Qdot_x_tracker.get_value(),curve1_func) # R_dot_x = PQline_k**2 - Pdot_x - Qdot_x # R_dot_x = fsolve(lambda x:curve1_func(x)-PQline_func(x),2.5)
        # R_dot_y = curve1_func(R_dot_x())
        R_dot = Dot(color=ORANGE) # .move_to(axes.i2gp(R_dot_x, curve1))
        f_always(R_dot.move_to, lambda: PointADD(Pdot_x_tracker.get_value(),Qdot_x_tracker.get_value(),curve1_func,False))
        R_dot_label = Tex(R"R'", color=ORANGE) # .next_to(R_dot, DR, buff=0.1)
        always(R_dot_label.next_to, R_dot, DR, 0.1)
        self.play(
            ShowCreation(R_dot, scale=0.25),
            ShowCreation(R_dot_label),
        )

        # [2.6] 创建点R和虚线RR'
        # Rdot_x = R_dot_x
        # Rdot_y = -R_dot_y
        Rdot = Dot(color=ORANGE) # .move_to(axes.i2gp(Rdot_x, curve2))
        f_always(Rdot.move_to,lambda: PointADD(Pdot_x_tracker.get_value(),Qdot_x_tracker.get_value(),curve1_func,True))
        Rdot_label = Tex(R"R", color=ORANGE).next_to(Rdot, DL, buff=0.1)
        RR_dashedLine = always_redraw(lambda: DashedLine(R_dot.get_center(), Rdot.get_center(), color=WHITE, dash_length=0.1, dashed_ratio=0.5))
        self.play(
            ShowCreation(RR_dashedLine),
            ShowCreation(Rdot),
            ShowCreation(Rdot_label),
        )
        always(Rdot_label.next_to, Rdot, DL, 0.1)
        self.wait(1)

        # [2.7] 给出问题答案
        latex2_3 = Tex(R"R").move_to(latex2_2)
        self.play(
            ReplacementTransform(latex2_2,latex2_3),
        )
        self.wait(2)


# Chapter-3：演示P+P运算
        # [3.1] 抛出问题
        latex3_1 = Tex(R"P+P= ")
        latex3_2 = Tex(R"?")
        latex3 = VGroup(latex3_1,latex3_2).arrange(RIGHT, aligned_edge=LEFT,buff = 1.2).to_edge(UL)
        self.play(
            ReplacementTransform(VGroup(latex2_1,latex2_3),latex3),
        )
        self.wait(2)

        # [3,2] 动态移动点P点Q
        self.play(
            Pdot_x_tracker.animate.set_value(-1-.00001),
            Qdot_x_tracker.animate.set_value(-1+.00001),
            run_time=3
        )
        self.wait(2)

        # [3.3] P Q重合
        self.play(
            FadeOut(Qdot),
            FadeOut(Qdot_label)
        )
        Rdot_label_2 = Tex(R"R=2P", color=ORANGE).next_to(Rdot, DL, buff=0.1)
        self.play(
            ReplacementTransform(Rdot_label,Rdot_label_2)
        )
        self.wait(1)
        Rdot_label_3 = Tex(R"2P", color=ORANGE).next_to(Rdot, DL, buff=0.1)
        latex3_3 = Tex(R"2P").move_to(latex3_2)
        self.play(
            ReplacementTransform(latex3_2,latex3_3),
            ReplacementTransform(Rdot_label_2,Rdot_label_3)
        )
        always(Rdot_label_3.next_to, Rdot, DL, 0.1)
        self.wait(1)

        # [3.4] 移动重合的点P，展示更多细节
        self.play(
            Pdot_x_tracker.animate.set_value(3-.00001),
            Qdot_x_tracker.animate.set_value(3+.00001),
            run_time=3
        )
        self.wait(.5)
        self.play(
            Pdot_x_tracker.animate.set_value(-1.58-.0000001),
            Qdot_x_tracker.animate.set_value(-1.58+.0000001),
            run_time=3
        )
        self.wait(1)

# Chapter-4: 演示nP运算，并提出结合律
        # [4.1] 抛出问题 P+P+P+P+P+P-?
        latex4_1 = Tex(R"P+P+P+P+P+P=").scale(.75).to_edge(UL)
        latex4_2 = Tex(R"?").scale(.75).next_to(latex4_1)
        latex4_3 = VGroup(latex4_1,latex4_2)
        self.play(
            ReplacementTransform(VGroup(latex3_1,latex3_3),VGroup(latex4_1,latex4_2)),
        )
        self.wait(2)

        # [4.2] 连续展示3P,4P,5P,6P
        def PointADD_xy(x1,y1,x2,y2):
            if x1==x2 and y1==y2:
                k = (3*x1**2+a)/(2*y1)
            else:
                k = (y1-y2)/(x1-x2)
            x3 = k**2-x1-x2
            y3 = k*(x1-x3)-y1
            return x3,y3
            
        x1 = Pdot_x_tracker.get_value()
        y1 = curve1_func(x1)
        x2,y2 = PointADD_xy(x1,y1,x1,y1)
        x3,y3 = PointADD_xy(x2,y2,x1,y1)
        x4,y4 = PointADD_xy(x3,y3,x1,y1)
        x5,y5 = PointADD_xy(x4,y4,x1,y1)
        x6,y6 = PointADD_xy(x5,y5,x1,y1)
        _3Pdot = Dot(color = YELLOW).move_to(axes.c2p(x3,y3))
        _4Pdot = Dot(color = GREEN ).move_to(axes.c2p(x4,y4))
        _5Pdot = Dot(color = BLUE_A).move_to(axes.c2p(x5,y5))
        _6Pdot = Dot(color = PURPLE).move_to(axes.c2p(x6,y6))
        _3P_dot = Dot(color = YELLOW).move_to(axes.c2p(x3,-y3))
        _4P_dot = Dot(color = GREEN ).move_to(axes.c2p(x4,-y4))
        _5P_dot = Dot(color = BLUE_A).move_to(axes.c2p(x5,-y5))
        _6P_dot = Dot(color = PURPLE).move_to(axes.c2p(x6,-y6))
        _3Pdot_label = Tex(R"3P", color=YELLOW).next_to(_3Pdot, UL, buff=0.1)
        _4Pdot_label = Tex(R"4P", color=GREEN ).next_to(_4Pdot, UL, buff=0.1)
        _5Pdot_label = Tex(R"5P", color=BLUE_A).next_to(_5Pdot, UL, buff=0.1)
        _6Pdot_label = Tex(R"6P", color=PURPLE).next_to(_6Pdot, UL, buff=0.1)
        hLine3,vLine3 = Line(start=Rdot,end=Pdot,color=WHITE),DashedLine(start=_3P_dot,end=_3Pdot,color=WHITE)
        self.play(ShowCreation(VGroup(hLine3,vLine3,_3Pdot,_3Pdot_label)),run_time=.5)
        self.wait(.5)
        hLine4,vLine4 = Line(start=_3Pdot,end=Pdot,color=WHITE),DashedLine(start=_4P_dot,end=_4Pdot,color=WHITE)
        self.play(ShowCreation(VGroup(hLine4,vLine4,_4Pdot,_4Pdot_label)),FadeOut(VGroup(hLine3,vLine3)),run_time=.5)
        self.wait(.5)
        hLine5,vLine5 = Line(start=Pdot,end=_5P_dot,color=WHITE),DashedLine(start=_5P_dot,end=_5Pdot,color=WHITE)
        self.play(ShowCreation(VGroup(hLine5,vLine5,_5Pdot,_5Pdot_label)),FadeOut(VGroup(hLine4,vLine4)),run_time=.5)
        self.wait(.5)
        hLine6,vLine6 = Line(start=_5Pdot,end=_6P_dot,color=WHITE),DashedLine(start=_6P_dot,end=_6Pdot,color=WHITE)
        self.play(ShowCreation(VGroup(hLine6,vLine6,_6Pdot,_6Pdot_label)),FadeOut(VGroup(hLine5,vLine5)),run_time=.5)
        self.wait(.5)
        self.play(FadeOut(VGroup(hLine6,vLine6)),run_time=.5)
        self.wait(2)

        # [4.3] 回答问题P+P+P+P+P+P=6P
        latex4_4 = Tex(R"6P").scale(.75).move_to(latex4_2)
        self.play(
            ReplacementTransform(latex4_2,latex4_4),
        )
        self.wait(2)

        # [4.4] 提出问题2P+2P+2P=?
        latex4_5 = Tex(R"2P+2P+2P=").scale(.75).next_to(latex4_1,DOWN).to_edge(LEFT)
        latex4_6 = Tex(R"?").scale(.75).next_to(latex4_5,RIGHT)
        latex4_7 = VGroup(latex4_5,latex4_6)
        self.play(
            TransformFromCopy(latex4_3,latex4_7),
        )
        self.wait(2)

        # [4.5] 演示2P+2P+2P
        hLine7,vLine7 = Line(start=Rdot,end=_4P_dot,color=WHITE), vLine4
        self.play(ShowCreation(VGroup(hLine7,vLine7)),run_time=.5)
        self.wait(1)
        hLine8,vLine8 = Line(start=Rdot,end=_6P_dot,color=WHITE), vLine6
        self.play(ShowCreation(VGroup(hLine8,vLine8)),FadeOut(VGroup(hLine7,vLine7)),run_time=.5)
        self.wait(1)
        self.play(FadeOut(VGroup(hLine8,vLine8)),run_time=.5)

        # [4.6] 回答问题2P+2P+2P=3(2P)=6P
        latex4_8 = Tex(R"3(2P)").scale(.75).next_to(latex4_5,RIGHT)
        self.play(
            ReplacementTransform(latex4_6,latex4_8)
        )
        self.wait(2)
        latex4_9 = Tex(R"=6P").scale(.75).next_to(latex4_8,RIGHT)
        self.play(
            TransformFromCopy(latex4_8,latex4_9)
        )
        self.wait(.5)

        # [4.8] 提出问题3P+3P=?
        latex4_10 = Tex(R"3P+3P=").scale(.75).next_to(latex4_5,DOWN).to_edge(LEFT)
        latex4_11 = Tex(R"?").scale(.75).next_to(latex4_10,RIGHT)
        latex4_12 = VGroup(latex4_10,latex4_11)
        self.play(
            TransformFromCopy(latex4_7,latex4_12),
        )
        self.wait(2)
        
        # [4.9] 演示3P+3P
        hLine9,vLine9 = Line(start=_3Pdot,end=_6P_dot,color=WHITE), vLine6
        self.play(ShowCreation(VGroup(hLine9,vLine9)),run_time=.5)
        self.wait(1)
        self.play(FadeOut(VGroup(hLine9,vLine9)),run_time=.5)
        self.wait(1)

        # [4.10] 回答问题3P+3P=2(3P)=6P
        latex4_13 = Tex(R"2(3P)").scale(.75).next_to(latex4_10,RIGHT)
        self.play(
            ReplacementTransform(latex4_11,latex4_13)
        )
        self.wait(2)
        latex4_14 = Tex(R"=6P").scale(.75).next_to(latex4_13,RIGHT)
        self.play(
            TransformFromCopy(latex4_13,latex4_14)
        )
        self.wait(2)

        # [4.11] 引出交换律a(bP) = b(aP) = (ab)P
        latex4_15 = Tex(R"a(bP) = b(aP) = (ab)P").to_edge(UL)
        latex4_17 = VGroup(latex4_1,latex4_4,latex4_5,latex4_8,latex4_9,latex4_10,latex4_13,latex4_14)
        self.play(
            ReplacementTransform(latex4_17,latex4_15)
        )
        self.wait(3)

        # [4.12] 淡出
        self.play(
            FadeOut(latex4_15),
            FadeOut(VGroup(_3Pdot,_4Pdot,_5Pdot,_6Pdot)),
            FadeOut(VGroup(_3Pdot_label,_4Pdot_label,_5Pdot_label,_6Pdot_label)),
            FadeOut(VGroup(Rdot,R_dot,Rdot_label_3,R_dot_label,RR_dashedLine)),
            FadeOut(PQline),
        )

# Chapter-5: 简略证明无穷发散
        # [5.1] 绘制直线和辅助点
        P_dot = Dot(color=RED)
        f_always(P_dot.move_to,lambda: axes.c2p(Pdot_x_tracker.get_value(),curve2_func(Pdot_x_tracker.get_value())))
        P_dot_label = Tex(R"P'",color=RED)
        always(P_dot_label.next_to, P_dot, DL, 0.1)
        Pudot = Dot()
        f_always(Pudot.move_to,lambda: axes.c2p(Pdot_x_tracker.get_value(),512))
        Pddot = Dot()
        f_always(Pddot.move_to,lambda: axes.c2p(Pdot_x_tracker.get_value(),-512))
        pline = always_redraw(lambda: Line(start=Pudot,end=Pddot))
        self.play(
            ShowCreation(VGroup(P_dot,P_dot_label,pline,Pudot,Pddot)),
            run_time=.5
        )
        self.wait(.5)
        self.play(
            Pdot_x_tracker.animate.set_value(1),
            runtime=2
        )
        self.play(
            Pdot_x_tracker.animate.set_value(-2),
            runtime=2
        )

        # [5.2] 提出问题 趋于无穷
        latex5_1 = Tex(R"\lim_{x \to \infty} \frac{\mathrm{d}y}{\mathrm{d}x} = ").move_to(axes.c2p(-7,-2)).to_edge(LEFT)
        latex5_2 = Tex(R"?").next_to(latex5_1,RIGHT)
        self.play(
            Write(latex5_1),
            Write(latex5_2)
        )
        self.play(
            Pdot_x_tracker.animate.set_value(3),
            runtime=3
        )
        self.wait(2)

        # [5.3] 开始推导
        latex5_3 = Tex(R"y^2 = x^3 +ax +b").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            TransformFromCopy(curve_label2,latex5_3),
        )
        self.wait(1.5)
        latex5_4 = Tex(R"2y\mathrm{d}y = 3x^2\mathrm{d}x +a\mathrm{d}x").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_3,latex5_4),
        )
        self.wait(1.5)
        latex5_5 = Tex(R"2y\mathrm{d}y = (3x^2+a)\mathrm{d}x").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_4,latex5_5)
        )
        self.wait(1.5)
        latex5_6 = Tex(R"\frac{\mathrm{d}y}{\mathrm{d}x} = \frac{3x^2+a}{2y}").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_5,latex5_6)
        )
        self.wait(1.5)
        latex5_7 = Tex(R"k = \frac{3x^2+a}{2y}").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_6,latex5_7)
        )
        self.wait(1.5)
        latex5_8 = Tex(R"k^2 = \frac{9x^4+6ax^2+a^2}{4y^2}").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_7,latex5_8)
        )
        self.wait(1.5)
        latex5_9 = Tex(R"k^2 = \frac{9x^4+6ax^2+a^2}{4(x^3+ax+b)}").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_8,latex5_9)
        )
        self.wait(1.5)
        latex5_10 = Tex(R"k^2 = \frac{9x^4+6ax^2+a^2}{4x^3+4ax+4b}").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_9,latex5_10)
        )
        self.wait(1.5)
        latex5_11 = Tex(R"\lim_{x \to \infty}k^2 =\lim_{x \to \infty} \frac{9x^4+6ax^2+a^2}{4x^3+4ax+4b}").scale(.75).next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_10,latex5_11)
        )
        self.wait(1.5)
        latex5_12 = Tex(R"\lim_{x \to \infty}k^2 =\infty").next_to(latex5_1,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(latex5_11,latex5_12)
        )
        self.wait(.5)
        latex5_13 = Tex(R"\infty").move_to(latex5_2)
        self.play(
            ReplacementTransform(VGroup(latex5_12,latex5_2),latex5_13)
        )
        self.wait(3)
        self.play(
            FadeOut(VGroup(latex5_1,latex5_13))
        )
        self.wait(1)


# Chapter-6: 演示无穷远点和无穷远直线
        # [6.2] 提出问题P+P'
        question6_1 = Tex(R"P+").to_edge(UL)
        question6_2 = Tex(R"P'").next_to(question6_1,RIGHT)
        question6_3 = Tex(R"=").next_to(question6_2,RIGHT)
        question6_4 = Tex(R"?").next_to(question6_3,RIGHT)
        self.play(
            Write(VGroup(question6_1,question6_2,question6_3,question6_4)),
        )
        self.wait(2)
 
        # [6.3] 绘制无穷远直线[0:0:0]
        the_line_at_inf = Circle(radius=256, color=GREY).move_to(axes.c2p(0, 0))
        self.play(
            Write(the_line_at_inf),
        )
 
        # [6.3] 缩小全局
        AllTheSceneNow = VGroup(
            axes,curve1,
            curve2,curve_label2,
            pline,
            question6_1,question6_2,question6_3,question6_4,
            MetaMiku
        )
        self.play(  # 点和点标签的缩放似乎会存在未知原因bug，只能舍掉
            FadeOut(VGroup(Pdot,Pdot_label,P_dot,P_dot_label)),
            run_time = .1
        )
        matrix1 = [[1/2560,0],[0,1/80]] # 变换矩阵，椭圆曲线发散的有点慢，就只能用压缩x轴的方法体现视觉效果
        self.play(
            ApplyMatrix(matrix=matrix1,mobject=AllTheSceneNow),
            the_line_at_inf.animate.scale(1/80),
            run_time = 7
        )
 
        # [6.4] 展示无穷远直线[0:0:0]和无穷远点(0:1:0)
        the_line_at_inf_label = Tex(R"\mathrm{The ~ line ~ at ~ infinity}",color=GREY).scale(.75).to_edge(RIGHT)
        self.play(
            ShowCreation(the_line_at_inf_label)
        )
        self.wait(2)
        Pudot_label = Tex(R"O",color=GREY).next_to(Pudot,UR)
        Pddot_label = Tex(R"O",color=GREY).next_to(Pddot,DL)
        Pudot_label_comment = Tex(R"\mathrm{~~A ~ point ~ at ~ infinity}",color=GREY).next_to(Pudot_label,RIGHT)
        Pddot_label_comment = Tex(R"\mathrm{~~A ~ point ~ at ~ infinity}",color=GREY).next_to(Pddot_label,RIGHT)
        self.play(
            Write(Pudot_label),
            Write(Pddot_label),
        )
        self.play(
            Write(VGroup(Pudot_label_comment,Pddot_label_comment))
        )
        self.wait(3)
        self.play(
            FadeOut(Pudot_label_comment),
            FadeOut(Pddot_label_comment),
        )
        self.wait(3)
 
        # [6.5] 放大全局
        self.play(
            ApplyMatrix(matrix=np.linalg.inv(matrix1),mobject=VGroup(AllTheSceneNow,Pudot_label,Pddot_label)),
            VGroup(the_line_at_inf,the_line_at_inf_label).animate.scale(80),
            run_time = 5
        )
 
        # [6.6] 给出答案P+P'=O,P+(-P)=O 
        question6_5 = Tex(R"O").move_to(question6_4)
        self.play(
            ReplacementTransform(question6_4,question6_5),
            ShowCreation(VGroup(Pdot,Pdot_label,P_dot,P_dot_label))    
        )
        self.wait(2)
        question6_6 = Tex(R"(-P)").next_to(question6_1,RIGHT)
        P_dot_label_new = Tex(R"-P",color=RED).next_to(P_dot,direction=DL,buff=.1)
        self.play(
            ReplacementTransform(question6_2,question6_6),
            ReplacementTransform(P_dot_label,P_dot_label_new),
            VGroup(question6_3,question6_5).animate.next_to(question6_6),
        )
        self.wait(3)
        self.play(
            FadeOut(VGroup(question6_1,question6_6,question6_3,question6_5)),
            FadeOut(VGroup(Pdot,Pdot_label,P_dot,P_dot_label_new,pline,Pudot,Pddot)),
            FadeOut(VGroup(curve1,curve2,curve_label2)),
        )
        self.play(
            FadeOutToPoint(axes,axes.c2p(0,0))
        )
        self.wait(1)

# Chapter-7: 演示加减密逻辑
        # [7.1] 创建Alice和Bob
        Alice = Tex(R"\pi",color=BLUE_C).scale(4).move_to(axes.c2p(-5,0)).to_edge(UP)
        Bob = Tex(R"\pi",color=BLUE_D).scale(4).move_to(axes.c2p(4,0)).to_edge(UP)
        self.play(
            ShowCreation(VGroup(Alice,Bob))
        )
        Alice_label = Tex(R"Alice",color=BLUE_C).next_to(Alice,DR)
        Bob_label = Tex(R"Bob",color=BLUE_D).next_to(Bob,DR)
        self.play(
            Write(VGroup(Alice_label,Bob_label))
        )

        # [7.2] Alice生成G，发送给Bob
        G_alice = Tex(R"G",color = BLUE_A).next_to(Alice,DOWN)
        public = Tex(R"public:").move_to(axes.c2p(-4,0)).to_edge(DOWN)
        self.play(
            Write(public),
            Write(G_alice)
        )
        G_bob = Tex(R"G",color = BLUE_A).next_to(Bob,DOWN)
        G_public = Tex(R"G",color = BLUE_A).next_to(public,RIGHT)
        self.play(
            TransformFromCopy(G_alice,VGroup(G_public,G_bob))
        )
        self.wait(1)

        # [7.3] Alice生成p，Bob生成q
        p_alice = Tex(R"p",color = GREEN_E).next_to(G_alice,DOWN)
        q_bob = Tex(R"q",color = YELLOW_E).next_to(G_bob,DOWN)
        self.play(
            Write(VGroup(p_alice,q_bob)),
        )
        self.wait(1)

        # [7.4] Alice计算A = pG,Bob计算B=qG
        A_alice1 = Tex(R"A",color=GREEN_A).next_to(p_alice,DL)
        A_alice2 = Tex(R"=",color=GREY).next_to(A_alice1,RIGHT)
        A_alice3 = Tex(R"p",color=GREEN_E).next_to(A_alice2,RIGHT)
        A_alice4 = Tex(R"G",color=YELLOW).next_to(A_alice3,RIGHT)
        B_bob1 = Tex(R"B",color=YELLOW_A).next_to(q_bob,DL)
        B_bob2 = Tex(R"=",color=GREY).next_to(B_bob1,RIGHT)
        B_bob3 = Tex(R"q",color=YELLOW_E).next_to(B_bob2,RIGHT)
        B_bob4 = Tex(R"G",color=YELLOW).next_to(B_bob3,RIGHT)
        self.play(
            TransformFromCopy(p_alice,A_alice3),
            TransformFromCopy(G_alice,A_alice4),
            TransformFromCopy(q_bob,B_bob3),
            TransformFromCopy(G_bob,B_bob4),
        )
        self.wait(.5)
        self.play(
            Write(VGroup(A_alice2,B_bob2))
        )
        self.play(
            Write(VGroup(A_alice1,B_bob1))
        )
        self.wait(1)

        # [7.5] Alice，Bob交换A,B
        A_bob = Tex(R"A",color=GREEN_A).next_to(B_bob2,DOWN)
        A_public = Tex(R"A",color=GREEN_A).next_to(G_public,RIGHT)
        B_alice = Tex(R"B",color=YELLOW_A).next_to(A_alice2,DOWN)
        B_public = Tex(R"B",color=YELLOW_A).next_to(A_public,RIGHT)
        self.play(
            TransformFromCopy(A_alice1,A_bob),
            TransformFromCopy(A_alice1,A_public),
            TransformFromCopy(B_bob1,B_alice),
            TransformFromCopy(B_bob1,B_public),
        )
        self.wait(2)

        # [7.5] 生成key
        key_alice1 = Tex(R"key",color=RED).next_to(B_alice,DL)
        key_alice2 = Tex(R"=",color=GREY).next_to(key_alice1,RIGHT)
        key_alice3 = Tex(R"p",color=GREEN_E).next_to(key_alice2,RIGHT)
        key_alice4 = Tex(R"B",color=YELLOW_A).next_to(key_alice3,RIGHT)
        key_alice5 = Tex(R"=p(qG)",color=GREY).scale(.75).next_to(key_alice4,RIGHT)
        key_bob1 = Tex(R"key",color=RED).next_to(A_bob,DL)
        key_bob2 = Tex(R"=",color=GREY).next_to(key_bob1,RIGHT)
        key_bob3 = Tex(R"q",color=YELLOW_E).next_to(key_bob2,RIGHT)
        key_bob4 = Tex(R"A",color=GREEN_A).next_to(key_bob3,RIGHT)
        key_bob5 = Tex(R"=q(pG)",color=GREY).scale(.75).next_to(key_bob4,RIGHT)
        self.play(
            TransformFromCopy(p_alice,key_alice3),
            TransformFromCopy(q_bob,key_bob3),
            TransformFromCopy(B_alice,key_alice4),
            TransformFromCopy(A_bob,key_bob4),
        )
        self.play(
            TransformFromCopy(VGroup(key_alice3,key_alice4),key_alice5),
            TransformFromCopy(VGroup(key_bob3,key_bob4),key_bob5),
        )
        self.wait(2)
        self.play(
            TransformFromCopy(VGroup(key_alice3,key_alice4,key_alice5),key_alice1),
            TransformFromCopy(VGroup(key_bob3,key_bob4,key_bob5),key_bob1),
            Write(VGroup(key_alice2,key_bob2))
        )
        self.wait(2)

        # [7.6] 比对key
        equal = Tex(R"=")
        self.play(
            key_alice1.animate.next_to(equal,LEFT),
            key_bob1.animate.next_to(equal,RIGHT)
        )
        self.play(
            Write(equal)
        )
        self.wait(1)

# Chapter-8: 结尾动画
        # [8.1] 淡出无用元素
        self.play(
            FadeOut(VGroup(
                Alice,Alice_label,
                G_alice,
                p_alice,
                A_alice1,A_alice2,A_alice3,A_alice4,
                B_alice,
                key_alice2,key_alice3,key_alice4,key_alice5
            )),
            FadeOut(VGroup(
                Bob,Bob_label,
                G_bob,
                q_bob,
                B_bob1,B_bob2,B_bob3,B_bob4,
                A_bob,
                key_bob2,key_bob3,key_bob4,key_bob5
            )),
            FadeOut(VGroup(
                public,G_public,A_public,B_public
            )),
        )
        self.wait(2)

        # [8.2] 放大
        AllTheSceneEnd = VGroup(key_alice1,key_bob1,equal,MetaMiku)
        Thanks = Tex(R"Thanks ~ for ~ watching")
        self.play(
            AllTheSceneEnd.animate.scale(128,about_point=axes.c2p(0,0)),
            FadeInFromPoint(Thanks,axes.c2p(0,0)),
            run_time = 5
        )

        # [8.3] MetaMiku
        MetaMiku_ = SVGMobject(R"E:\Desktop\MetaMikuColor.svg",stroke_opacity=0).scale(.125)
        
        MetaMiku_.next_to(Thanks,DR)
        self.play(
            Write(MetaMiku_),
            run_time = 1
        )
        self.wait(3)

        # [8.4] fadeout
        self.play(
            FadeOut(Thanks),
            FadeOut(MetaMiku_)
        )
        self.wait(9)
        

        