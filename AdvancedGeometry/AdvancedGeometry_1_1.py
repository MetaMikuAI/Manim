from manimlib import *

class AdvancedGeometry_1_1(Scene):
    def construct(self):
# [0]
        # 标题
        title = Tex(R"\text{高等几何}").scale(2)
        subtitle = Tex(R"\text{第}_1\text{章：仿射坐标与仿射变换}").next_to(title,DOWN)
        subsubtitle = Tex(R"\text{§1 透视仿射对应}").scale(.5).next_to(subtitle,DOWN)
        MetaMiku = SVGMobject(R"E:\Desktop\MetaMikuColor.svg",stroke_opacity=0).scale(.125).next_to(subsubtitle,DR)
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
        # [1.1.1] 介绍单比
        # [1.1.1.1] 创建一线三点和对应的跟踪器
        pLine = Line(start=axes.c2p(-6.5,0,0),end=axes.c2p(6.5,0,0), color=WHITE)
        P1xTracker = ValueTracker(-2)
        P2xTracker = ValueTracker( 0)
        PxTracker  = ValueTracker( 2)
        P1Point = Dot(color=BLUE)
        P2Point = Dot(color=TEAL)
        PPoint = Dot(color=GREEN)
        f_always(P1Point.move_to,lambda: axes.c2p(P1xTracker.get_value(),0,-.001))
        f_always(P2Point.move_to,lambda: axes.c2p(P2xTracker.get_value(),0,.001))
        f_always( PPoint.move_to,lambda: axes.c2p( PxTracker.get_value(),0,0))
        P1PointLabel = Tex(R"P_1",color=BLUE)
        P2PointLabel = Tex(R"P_2",color=TEAL)
        PPointLabel = Tex(R"P",color=GREEN)
        always(P1PointLabel.next_to,P1Point,UP)
        always(P2PointLabel.next_to,P2Point,UP)
        always( PPointLabel.next_to, PPoint,UP)
        # [1.1.1.2] 展示直线,三点和三点的标签
        self.play(
            Write(pLine,run_time=1),
            Write(P1Point,lag_time=.5),
            Write(P2Point,lag_time=.75),
            Write(PPoint,lag_time=1),
            Write(PPointLabel,lag_time=1.25),
            Write(P1PointLabel,lag_time=1.25),
            Write(P2PointLabel,lag_time=1.25),
        )
        # [1.1.1.3] 创建各个名词及其高亮
        latex_010101 = Tex(R"(P_1P_2P)",R" = \frac{P_1P}{P_2P}").scale(1.25).to_edge(DOWN,buff=1.)
        text_010101 = TexText("单比",color = GREY_C).next_to(latex_010101,LEFT,buff=.5)
        text_010102 = TexText("有向线段",color = GREY_C)
        text_010107 = TexText("有向线段的数量",color = GREY_C)
        text_010103 = TexText("分点",color = GREY_C).next_to( PPointLabel,UP)
        text_010104 = TexText("基点",color = GREY_C).next_to(P1PointLabel,UP)
        text_010105 = TexText("基点",color = GREY_C).next_to(P2PointLabel,UP)
        text_010106 = TexText("P",color = GREY_C).next_to(P2PointLabel,UP)
        P1PointLabelHighlight = SurroundingRectangle(P1PointLabel, color=BLUE, fill_opacity=0.1)
        P2PointLabelHighlight = SurroundingRectangle(P2PointLabel, color=TEAL, fill_opacity=0.1)
        PPointLabelHighlight  = SurroundingRectangle(PPointLabel, color=GREEN, fill_opacity=0.1)
        # [1.1.1.4] 介绍"单比"定义式
        self.play(
            Write(latex_010101),
            run_time = 2,
        )
        # [1.1.1.5] 高亮提示"单比"
        latex_010102 = latex_010101.get_part_by_tex(R"(P_1P_2P)")
        latex_010102_highlight = SurroundingRectangle(latex_010102, color=GREY_C, fill_opacity=0.1)
        self.play(
            ShowCreation(latex_010102_highlight,run_time=1),
            Write(text_010101,run_time=2),
            lag_ratio = .9,
        ) 
        # [1.1.1.6] 高亮提示 "基点"
        self.play(
            ShowCreation(PPointLabelHighlight, run_time=1),
            Write(text_010103, run_time=1),
        )
        self.wait(.5)
        # [1.1.1.7] 高亮提示"分点"
        self.play(
            ShowCreation(VGroup(P1PointLabelHighlight,P2PointLabelHighlight), run_time=1),
            Write(VGroup(text_010104,text_010105), run_time=2),
        )
        self.wait(1)
        # [1.1.1.8] 创建有向线段Arrow
        P1PArrow = always_redraw(lambda: Arrow(start=P1Point,end=PPoint,color=BLUE,buff=0))
        P2PArrow = always_redraw(lambda: Arrow(start=P2Point,end=PPoint,color=TEAL,buff=0))
        # [1.1.1.9] 单独列出有向线段
        P1PArrow_ = Arrow(start=axes.c2p(3,-2,0),end=axes.c2p(4,-2,0),color=BLUE,buff=0)
        P2PArrow_ = Arrow(start=axes.c2p(3,-2.75,0),end=axes.c2p(4,-2.75,0),color=TEAL,buff=0)
        P1P2PArrowHighlight = SurroundingRectangle(VGroup(P1PArrow_,P2PArrow_),color=GREY, fill_opacity=0.1)
        latex_010103 = Tex(R"P_1P",color = BLUE).move_to(P1PArrow_)
        latex_010104 = Tex(R"P_2P",color = TEAL).move_to(P2PArrow_)
        # [1.1.1.10] 展示有向线段P_1P
        self.play(Write(P1PArrow))
        self.play(ReplacementTransform(P1PArrow,P1PArrow_))
        self.wait(1)
        self.play(Write(P2PArrow))
        self.play(ReplacementTransform(P2PArrow,P2PArrow_))
        self.wait(1)
        self.play(ShowCreation(P1P2PArrowHighlight))
        text_010102.next_to(Group(P1PArrow_,P2PArrow_),DOWN)
        text_010107.move_to(text_010102)
        self.play(Write(text_010102))
        self.wait(.5)
        self.play(
            FadeOut(P1P2PArrowHighlight),
            FadeOut(Group(text_010102,P1PArrow_,P2PArrow_)),
            FadeIn(Group(text_010107,latex_010103,latex_010104)),
        )
        self.wait(1)
        self.play(
            FadeOut(Group(text_010107,latex_010103,latex_010104)),
            FadeIn(Group(text_010102,P1PArrow_,P2PArrow_)),
        )
        self.wait(3)
        # [1.1.1.11] 淡去所有标签，恢复有向线段P_1P P_2P
        self.play(
            FadeOut(Group(text_010101,text_010102,text_010103,text_010104,text_010105)),
            FadeOut(Group(P1PointLabelHighlight,P2PointLabelHighlight,PPointLabelHighlight,latex_010102_highlight)),
            ReplacementTransform(P1PArrow_,P1PArrow),
            ReplacementTransform(P2PArrow_,P2PArrow),
            run_time=1
        )
        # [1.1.1] ended
        # latex -> latex_010104
        # text -> text_010107 

        # [1.1.2] 单比计算动态化展示
        # [1.1.2.1] 单比结果
        text_010106, number_010101 = DYNnumber_010101 = VGroup(
            Text(" = "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            )
        ).arrange(RIGHT)
        always(DYNnumber_010101.next_to,latex_010101,RIGHT)
        f_always(number_010101.set_value,lambda: (PxTracker.get_value()-P1xTracker.get_value())/(PxTracker.get_value()-P2xTracker.get_value()))
        # [1.1.2.2] P_1P,P_2P结果
        DYNnumber_010102 = DecimalNumber(0,show_ellipsis=True,num_decimal_places=2,include_sign=True)
        DYNnumber_010103 = DecimalNumber(0,show_ellipsis=True,num_decimal_places=2,include_sign=True)
        always(DYNnumber_010102.next_to,latex_010101,UR)
        always(DYNnumber_010103.next_to,latex_010101,DR)
        f_always(DYNnumber_010103.set_value,lambda: PxTracker.get_value()-P2xTracker.get_value())
        f_always(DYNnumber_010102.set_value,lambda: PxTracker.get_value()-P1xTracker.get_value())
        # [1.1.2.3] 显示动态数据
        self.play(
            Write(DYNnumber_010102),
            Write(DYNnumber_010103),
            Write(DYNnumber_010101),
        )
        self.wait(.5)
        # [1.1.2.4] 动态调整
        # [WARNING] 动态移动的时候有可能出现两点重合的情况，重合时Arrow将会NaN出错，计算单比也会NAN出错，故将先前P P1 P2的z轴进行轻微错位处理
        self.play(PxTracker.animate.set_value(5))
        self.play(PxTracker.animate.set_value(-1))
        self.play(PxTracker.animate.set_value(-5))
        self.play(PxTracker.animate.set_value(2))
        self.play(P1xTracker.animate.set_value(4),PxTracker.animate.set_value(-1))
        self.play(P1xTracker.animate.set_value(-1),P2xTracker.animate.set_value(3),PxTracker.animate.set_value(1))
        self.play(P1xTracker.animate.set_value(-2),P2xTracker.animate.set_value(0),PxTracker.animate.set_value(2))
        self.wait(1)
        # [1.1.2.5] 提示特殊情况
        latex_010105 = Tex(R"^{\text{注意：当}} P ~^{\text{与}} P_2 ~^{\text{重合时，}} (P_1P_2P) ^{\text{不存在}}").to_edge(UR)
        self.play(Write(latex_010105))
        self.wait(3)
        # [1.1.2.6] 淡出
        self.play(
            FadeOut(Group(pLine,P1Point,P2Point,PPoint,P1PointLabel,P2PointLabel,PPointLabel)),
            FadeOut(Group(DYNnumber_010101,DYNnumber_010102,DYNnumber_010103)),
            FadeOut(latex_010101),
            FadeOut(Group(P1PArrow,P2PArrow)),
            FadeOut(latex_010105),
        )
        self.wait(1)
        # [1.1.2] END
        # latex -> latex_010105 
        # text -> text_010107

        # [1.1.3]介绍仿射变换
        # [1.1.3.1]建立两个平面\pi,\pi'
        piPlanePoints = [
            [-8, 0, 0         ],
            [ 8, 0, 0         ],
            [ 8, 3, 3 * 3**0.5],
            [-8, 3, 3 * 3**0.5],
        ]
        pi_PlanePoints = [
            [-8, 0, 0],
            [ 8, 0, 0],
            [ 8, 6, 0],
            [-8, 6, 0],
        ]
        piPlane = Polygon(*piPlanePoints, color=GREY).set_fill(GREY, opacity=0.5)
        pi_Plane = Polygon(*pi_PlanePoints, color=GREY).set_fill(GREY, opacity=0.5)
        # [1.1.3.2] 建立基准点
        M  = np.array([ 6, 0,           0]) # 自对应点
        N  = np.array([1, 2, 2*3**.5]) # 直线n端点
        N_ = np.array([-4, 3,           0]) # 直线n’端点
        # [1.1.3.3] 计算平面法向量和摄像机朝向
        MN = N-M
        MN_= N_-M
        normal = np.cross(MN,MN_)
        normal /= np.linalg.norm(normal)
        phi = np.pi/2 - np.dot(normal,np.array([0,0,1]))
        theta = 1
        theta = -np.arctan2(normal[0],normal[1])
        camera.set_euler_angles(theta=theta,phi=phi,gamma=0) # [WARNING] 具体角度可能会偏差PI/2或者正负，根据实际情况调整
        MetaMiku.apply_matrix(MatrixPointingToCamera())
        # [1.1.3.4] 画线
        nLine = Line3D(start=M,end=N,color=WHITE,width=0.025)
        n_Line = Line3D(start=M,end=N_,color=WHITE,width=0.025)
        self.play(
            ShowCreation(nLine),
            ShowCreation(n_Line)
        )
        # [1.1.3.3] 创建标记点
        Mdot = Sphere(radius=.05,color=WHITE).move_to(ac2p(M))
        Adot = Sphere(radius=.05,color=BLUE).move_to(ac2p((7*M+1*N)/8))
        Bdot = Sphere(radius=.05,color=TEAL).move_to(ac2p((4*M+4*N)/8))
        Cdot = Sphere(radius=.05,color=GREEN).move_to(ac2p((2*M+6*N)/8))
        A_dot = Sphere(radius=.05,color=BLUE).move_to(ac2p((7*M+1*N_)/8))
        B_dot = Sphere(radius=.05,color=TEAL).move_to(ac2p((4*M+4*N_)/8))
        C_dot = Sphere(radius=.05,color=GREEN).move_to(ac2p((2*M+6*N_)/8))
        MdotLabel = Tex("M",color=WHITE).apply_matrix(MatrixPointingToCamera()).next_to(Mdot,np.array([0,0,-1]))
        AdotLabel = Tex("A",color=BLUE).apply_matrix(MatrixPointingToCamera()).next_to(Adot,np.array([1,0,1]))
        BdotLabel = Tex("B",color=TEAL).apply_matrix(MatrixPointingToCamera()).next_to(Bdot,np.array([1,0,1]))
        CdotLabel = Tex("C",color=GREEN).apply_matrix(MatrixPointingToCamera()).next_to(Cdot,np.array([1,0,1]))
        A_dotLabel = Tex("A'",color=BLUE).apply_matrix(MatrixPointingToCamera()).next_to(A_dot,np.array([0,0,-1]))
        B_dotLabel = Tex("B'",color=TEAL).apply_matrix(MatrixPointingToCamera()).next_to(B_dot,np.array([0,0,-1]))
        C_dotLabel = Tex("C'",color=GREEN).apply_matrix(MatrixPointingToCamera()).next_to(C_dot,np.array([0,0,-1]))
        AA_Line = Line3D(start=Adot.get_center(),end=A_dot.get_center(),color=BLUE,width=0.025)
        BB_Line = Line3D(start=Bdot.get_center(),end=B_dot.get_center(),color=TEAL,width=0.025)
        CC_Line = Line3D(start=Cdot.get_center(),end=C_dot.get_center(),color=GREEN,width=0.025)
        piPlaneLabel = Tex("\pi",color=GREY).scale(2).apply_matrix(MatrixPointingToCamera(np.pi,np.pi*2/3,0)).move_to(axes.c2p(-3,.5,1))
        pi_PlaneLabel = Tex("\pi'",color=GREY).scale(2).apply_matrix(MatrixPointingToCamera(np.pi,0,0)).move_to(axes.c2p(-1,5,0))
        nLineLabel = Tex("n",color=WHITE).apply_matrix(MatrixPointingToCamera()).next_to(ac2p((1*M+7*N)/8),OUT)
        n_LineLabel = Tex("n'",color=WHITE).apply_matrix(MatrixPointingToCamera()).move_to(ac2p((1*M+7*N_)/8),OUT)
        # [1.1.3.4] 描点
        self.play(
            ShowCreation(Mdot),
            ShowCreation(Adot),
            ShowCreation(Bdot),
            ShowCreation(Cdot),
            ShowCreation(A_dot),
            ShowCreation(B_dot),
            ShowCreation(C_dot),
            ShowCreation(VGroup(MdotLabel,AdotLabel,BdotLabel,CdotLabel,A_dotLabel,B_dotLabel,C_dotLabel))
        )
        self.wait(2)
        # [1.1.3.5] 连线
        self.play(ShowCreation(AA_Line),run_time=.5)
        self.play(ShowCreation(BB_Line),run_time=.5)
        self.play(ShowCreation(CC_Line),run_time=.5)
        self.wait(1)
        # [1.1.3.6] 几何关系必要latex和text 
        latex_010106 = Tex("AA'", "||" , "BB'" , "||", "CC'").set_color_by_tex_to_color_map({"AA'":BLUE,"BB'":TEAL,"CC'":GREEN})
        latex_010107 = Tex("A","\\leftrightarrow ","A'").set_color_by_tex_to_color_map({"A":BLUE,"A'":BLUE})
        latex_010108 = Tex("B","\\leftrightarrow ","B'").set_color_by_tex_to_color_map({"B":TEAL,"B'":TEAL})
        latex_010109 = Tex("C","\\leftrightarrow ","C'").set_color_by_tex_to_color_map({"C":TEAL,"C'":TEAL})
        latex_010110 = Tex("n","\\leftrightarrow ","n'").set_color_by_tex_to_color_map({"n":WHITE,"n'":WHITE})
        latex_010111 = Tex("\\pi","\\leftrightarrow ","\\pi'").set_color_by_tex_to_color_map({"\\pi":GREY,"\\pi'":GREY})
        latex_010112 = Tex(R"M \leftrightarrow M")
        latex_010113 = VGroup(latex_010106,latex_010112,latex_010107,latex_010108,latex_010109,latex_010110,latex_010111).arrange(direction=DOWN).to_edge(UR).apply_matrix(MatrixPointingToCamera())
        text_010109 = TexText("透视仿射对应").apply_matrix(MatrixPointingToCamera()).move_to(latex_010113)
        # [1.1.3.7] 提示几何关系 M A B C 
        self.play(Write(latex_010106),run_time=1)
        self.wait(2)
        self.play(Write(latex_010112),run_time=1)
        self.play(Write(latex_010107),run_time=1)
        self.play(Write(latex_010108),run_time=1)
        self.play(Write(latex_010109),run_time=1)
        # [1.1.3.8] 显示直线n n'的标签，并提及其几何关系
        self.play(
            Write(nLineLabel,run_time=1),
            Write(n_LineLabel,run_time=1),
        )
        self.play(Write(latex_010110),run_time=1)
        # [1.1.3.9] 展示平面\pi 和\pi' 三维旋转展示空间几何关系
        self.play(
            ShowCreation(piPlane,run_time=2),
            ShowCreation(pi_Plane,run_time=2),
            Write(piPlaneLabel,run_time=2),
            Write(pi_PlaneLabel,run_time=2),
        )
        self.play(
            camera.animate.set_euler_angles(theta=np.pi+theta,phi=60*DEGREES,gamma=0),
            run_time = 5
        )
        self.play(
            camera.animate.set_euler_angles(theta=2*np.pi+theta,phi=phi,gamma=0),
            run_time = 4
        )
        self.play(Write(latex_010111),run_time=1)
        self.wait(2)
        # [1.1.3.10] 提出"透视仿射对应"概念
        self.play(
            ReplacementTransform(latex_010113,text_010109),
        )
        self.wait(.5)
        TempDot = TexText("透视仿射对应").to_edge(DR).apply_matrix(MatrixPointingToCamera())
        self.play(
            text_010109.animate.move_to(TempDot)
        )
        # [1.1.3.11] 提出"自对应点" "透视轴"概念
        mLine = Line3D(start=np.array([8,0,0]),end=np.array([-8,0,0]),color=YELLOW,width=.05)
        mLineLabel = Tex("m",color=YELLOW).apply_matrix(MatrixPointingToCamera()).next_to(np.array([4,0,0]),np.array([0,.5,.5]))
        mLineLabel.apply_matrix(np.linalg.inv(MatrixPointingToCamera()))
        mLineLabelHighLight = SurroundingRectangle(mLineLabel, color=YELLOW, fill_opacity=0.1).move_to(axes.c2p(0,0,0)).apply_matrix(MatrixPointingToCamera())
        mLineLabel.apply_matrix(MatrixPointingToCamera())
        mLineLabelHighLight.move_to(mLineLabel)

        text_010110 = TexText("自对应点").apply_matrix(MatrixPointingToCamera()).next_to(MdotLabel,np.array([-1,0,-1]))
        text_010111 = TexText("透视轴").apply_matrix(MatrixPointingToCamera()).next_to(mLineLabel,np.array([0,0,1]))
        latex_010114 = Tex(R"M \subset m = \pi \cap \pi'").to_edge(DOWN).apply_matrix(MatrixPointingToCamera())

        MdotLabel.apply_matrix(np.linalg.inv(MatrixPointingToCamera()))
        MdotLabelHighLight = SurroundingRectangle(MdotLabel, color=WHITE, fill_opacity=0.1).move_to(axes.c2p(0,0,0)).apply_matrix(MatrixPointingToCamera())
        MdotLabel.apply_matrix(MatrixPointingToCamera())
        MdotLabelHighLight.move_to(MdotLabel)
        self.play(
            ShowCreation(mLine),
            Write(mLineLabel),
        )
        self.play(
            Write(latex_010114),
            run_time=3
        )
        self.play(
            ShowCreation(MdotLabelHighLight),
            Write(text_010110)
        )
        self.wait(1)
        self.play(
            ShowCreation(mLineLabelHighLight),
            Write(text_010111)
        )
        self.wait(3)
        self.play(
            FadeOut(VGroup(text_010110,text_010111)),
            FadeOut(VGroup(MdotLabelHighLight,mLineLabelHighLight)),
            FadeOut(latex_010114)
        )
        # [1.1.3.12] 淡去平面
        self.play(
            FadeOut(piPlane),
            FadeOut(pi_Plane),
            FadeOut(piPlaneLabel),
            FadeOut(pi_PlaneLabel)
        )
        # [1.1.3.13] 实在写不下去了，转成摄像机固定视角，几何体跟随摄像机吧，累死我了
        AllSceneNow = Group(
            nLine,n_Line,mLine,
            Adot,A_dot,Bdot,B_dot,Cdot,C_dot,Mdot,
            mLineLabel,AdotLabel,A_dotLabel,BdotLabel,B_dotLabel,CdotLabel,C_dotLabel,MdotLabel,
        )
        # AllSceneNow.apply_matrix(np.linalg.inv(MatrixPointingToCamera()))
        # camera.set_euler_angles(0,0,0)
        # 转不过去，可恶！
        # self.wait(1)
        
        # [1.1.3.14] 高亮 透视仿射对应
        text_010109.apply_matrix(np.linalg.inv(MatrixPointingToCamera()))
        text_010109HighLight = SurroundingRectangle(text_010109, color=WHITE, fill_opacity=0.1).apply_matrix(MatrixPointingToCamera())
        text_010109.apply_matrix(MatrixPointingToCamera())
        text_010109HighLight.move_to(text_010109)
        self.play(
            ShowCreation(text_010109HighLight),
        )
        self.wait(1)

        # [1.1.3.15] 介绍对应四大性质(的文本)
        text_010112 = TexText("(1)同素性")
        text_010113 = TexText(":")
        text_010114 = TexText("点对应点，直线对应直线")
        text_010121 = VGroup(text_010112,text_010113,text_010114).arrange(RIGHT)
        text_010115 = TexText("(2)结合性")
        text_010116 = TexText(":")
        latex_010115 = Tex(R"A \subset n \leftrightarrow A' \subset n'")
        text_010122 = VGroup(text_010115,text_010116,latex_010115).arrange(RIGHT)
        text_010117 = TexText("(3)单比不变")
        text_010118 = TexText(":")
        latex_010116 = Tex(R"(ABC) = (A'B'C')")
        text_010123 = VGroup(text_010117,text_010118,latex_010116).arrange(RIGHT)
        text_010119 = TexText("(4)二直线的平行性")
        text_010120 = TexText(":")
        latex_010117 = Tex(R"n || l \leftrightarrow n' || l'")
        text_010124 = VGroup(text_010119,text_010120,latex_010117).arrange(RIGHT)
        text_010125 = VGroup(text_010121,text_010122,text_010123,text_010124)#.arrange(DOWN)
        text_010125.to_edge(DL).apply_matrix(MatrixPointingToCamera())
        # [1.1.3.16] 介绍对应四大性质
        self.play(
            Write(text_010121),
            run_time = 3
        )
        self.wait(3)
        self.play(
            ReplacementTransform(text_010121,text_010122),
        )
        self.wait(3)
        self.play(
            ReplacementTransform(text_010122,text_010123),
        )
        self.wait(3)
        self.play(
            ReplacementTransform(text_010123,text_010124),
        )
        # [1.1.3.17] 临时加线，展示第四条
        L = np.array([-2,0,0])
        lLine = Line3D(start=M+L,end=N+L,color=WHITE,width=0.025)
        l_Line = Line3D(start=M+L,end=N_+L,color=WHITE,width=0.025)
        lLineLabel = Tex("l").apply_matrix(MatrixPointingToCamera()).move_to(ac2p(nLineLabel.get_center()+L))
        l_LineLabel = Tex("l'").apply_matrix(MatrixPointingToCamera()).move_to(ac2p(n_LineLabel.get_center()+L))
        self.play(
            ShowCreation(lLine),
            ShowCreation(l_Line),
            Write(lLineLabel),
            Write(l_LineLabel)
        )
        self.wait(.5)
        # [1.1.3.18] 摄像机角度刁钻，略微抬高视角
        self.play(
            camera.animate.set_euler_angles(theta=theta,phi=phi+np.pi*23/12,gamma=0),
        )
        self.play(
            camera.animate.set_euler_angles(theta=theta,phi=phi+np.pi*2,gamma=0),
        )
        self.wait(2)
        # [1.1.3.19] 小节结束，淡出全部 
        AllSceneNow = Group(
            nLine,n_Line,mLine,
            Adot,A_dot,Bdot,B_dot,Cdot,C_dot,Mdot,
            mLineLabel,AdotLabel,A_dotLabel,BdotLabel,B_dotLabel,CdotLabel,C_dotLabel,MdotLabel,
            AA_Line,BB_Line,CC_Line,nLineLabel,n_LineLabel,lLine,l_Line,lLineLabel,l_LineLabel,
            text_010124,text_010109,text_010109HighLight
        )
        self.play(
            FadeOut(AllSceneNow)
        )
        # [1.1.3] END
        # latex -> latex_010117 
        # text -> text_010125

        # [0]
        MetaMiku_ = SVGMobject(R"E:\Desktop\MetaMikuColor.svg",stroke_opacity=0).scale(.125).apply_matrix(MatrixPointingToCamera())
        self.wait(1)
        self.play(
            MetaMiku.animate.move_to(MetaMiku_).scale(2)
        )
        self.wait(3)
        self.play(
            FadeOut(MetaMiku),
        )
        self.wait(9)
        
        return
    

if __name__ == '__main__':
    from os import system
    system(f"manimgl {__file__}")
    # system(f"manimgl {__file__} AdvancedGeometry -o --uhd")