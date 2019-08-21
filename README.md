# Funny-Math-Problem-by-Python3
基于Python3的趣味数学问题解决方案


**Pro1. [数独 (Sudoku)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/blob/master/Sudoku)**
>>>根据九宫格盘面上的已知数字，推理出所有剩余空格的数字，并满足每一行、每一列、每一个宫(3*3)内的数字均含1—9这9个数字。
        
**Pro2. [幻方 (Magic Square)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/blob/master/Magic%20Square)**
>>>幻方又称为魔方，方阵或厅平方。通常幻方由从1到n<sup>2</sup> 的连续整数组成，其中n为正方形的行或列的数目。将数填在纵横格数都相等的正方形图内，使得每一行、每一列和每一条对角线上的各个数之和都相等。
        
**Pro3. [24点 (24 Point)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/blob/master/24%20Point)**
>>>把4个整数通过加、减、乘、除以及括号运算，使最后的计算结果是24的一个数学游戏。
 
**Pro4. [汉诺塔 (Tower of Hanoi)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/blob/master/Tower%20of%20Hanoi)**
>>>法国数学家爱德华·卢卡斯曾编写过一个关于印度的古老传说：在世界中心贝拿勒斯的圣庙里，一块黄铜板上插着三根宝石针，印度教的主神梵天在创造世界的时候，在其中一根针上从下到上地穿好了由大到小的64片金片，这就是所谓的汉诺塔。不论白天黑夜，总有一个僧侣在按照下面的法则移动这些金片：一次只移动一片，不管在哪根针上，小片必须在大片上面。这就是汉诺塔问题。
        
**Pro5. [N皇后 (N Queens)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/blob/master/N%20Queens)**
>>>八皇后问题，是一个古老而著名的问题，是利用回溯算法求解的典型案例。该问题是国际西洋棋棋手马克斯·贝瑟尔于1848年提出：在8×8格的国际象棋上摆放八个皇后，使其不能互相攻击，即任意两个皇后都不能处同一行、同一列或同一斜线上，问有多少种摆法。之后陆续有许多数学家对其进行研究，其中包括高斯和康托，并且将其推广为N皇后问题。

**Pro6. [彩票号码优选方案 (Lottery Number)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Lottery)**
>>>彩票号码优选方案。双色球、大乐透号码的优选方案。

**Pro7. [完美迷宫 (Perfect Maze)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Perfect%20Maze)**
>>>所谓完美迷宫，就是没有回路，没有不可达区域的迷宫，并且迷宫中任意两个网格间都有唯一的路径。利用Prim算法，分别采取遍历墙和遍历网格的方法，动态展示迷宫的生成。并且利用A\*算法获得从入口到出口的最佳路径，并在迷宫中展示出来。

**Pro8. [凸包 (Convex Hull)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Convex%20Hull)**
>>>下面用比较通俗的方式，介绍下凸包：在一个二维坐标平面中，散列着一些点，将最外层的点连接起来构成的凸多边型，它能包含散列的所有的点，这个多边形就是这些点构成的点集的凸包。利用Graham Scan算法获得凸包(平面凸包)，并动态展示凸包的形成过程。

**Pro9. [一笔画完 (One Stroke)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/One_Stroke)**
>>>从起始网格开始，用一笔划过所有可以走的节点，不能遗漏，也不能重复。利用DFS(深度优先搜索)和BFS(广度优先搜索)算法找到所有的路径，在寻找路径过程中添加了优化选择的函数，加速了计算过程。最总图示所有的解。涉及到的点有Python的尾递归优化以及基于多线程的计时器。

**Pro10. [七桥 (Seven Bridge)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Seven%20Bridge)**
>>>一笔划过图形中所有的边，边不能遗漏，同时也不能重复。利用欧拉定理以及Fleury(弗洛莱)算法解决。

**Pro11. [旅行商 (Traveling Salesman)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Traveling%20Salesman)**
>>>旅行商问题(TSP)，一个旅行商要拜访N个城市，每个城市只能拜访一次，最后要回到原来出发的城市。选择的路径的路程必须是所有路径中值最小的。以全国34城市为例。城市之间的距离定义为经纬度之间的地球表面的距离。利用遗传算法(Genetic Algorithm)获得最终的方案。

**Pro12. [变态曲线 (Abnormal Curve)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Abnormal%20Curve)**
>>>由一簇具有某种规律的直线的交点构成的变态曲线，探索这条变态曲线的表达式，以及计算曲线下的面积和直线簇构成的图形的面积的误差的范围。

**Pro13. [爱因斯坦问题 (Einstein's Puzzle)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Einstein's%20Puzzle)**
>>>利用回溯算法解决爱因斯坦问题。在一条街上，有5座房子，喷了不同的5种颜色。每个房子里住着不同国籍的人。每个人喝着不同的饮料，抽不同品牌的香烟，养不同的宠物。问：谁养鱼？

**Pro14. [分形 (Fractal)](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Fractal)**
>>>分形（Fractal）一词，是由美国数学家曼德勃罗先生（Mandelbrot）创造出来的。分形几何学是一门以非规则几何形态为研究对象的几何学。按照分形几何学的观点，一切复杂的对象虽然看似杂乱无章，但他们具有相似性。简单地说，就是把复杂对象的某个局部进行放大，其形态和复杂程度与整体相似。本文给出基于复动力系统，例如Mandelbrot集合、Julia集合；基于迭代函数系统，例如Koch雪花、谢尔宾斯基三角形。

**Pro15. [八人过河（Cross River）](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/Cross%20River)**
>>>现在有8个人分别为：1个父亲，带着他的2个儿子。1个母亲，带着她的2个女儿；1个警察，带着1个犯人；开始时，8个人都是在河的左岸。现在需要过河，过河时需要注意下面5条说明：1，只有警察、父亲和母亲可以划船；2，警察如果离开犯人，犯人就会伤害其他人；3，母亲不在时，这个父亲会伤害她的女儿。4，父亲不在时，这个母亲也会伤害他的儿子；5，船上一次最多只能坐两个人。求出过河方案。利用状态空间BFS搜索算法解决，并以绘图形式给出解决方案。

**Pro15. [十五谜题（15 Puzzle）](https://github.com/Anfany/Funny-Math-Problem-by-Python3/tree/master/15%20Puzzle)**
>>>15谜题是由纽约卡纳斯托塔市的邮政局长诺伊斯·查普曼发明的。15谜题就是将编号从1到15的15个方块，放在一个有16个格子的4×4的的盒子中，其中一个格子是没有方块的。通过移动方块，使得方块的编号上左上方到右下方正好是连续的，并且右下角的格子正好没有方块。利用IDA\*算法获得移动方案。

###### 扫描二维码，关注订阅号，可获取以上谜题的详细解答，以及关于编程、机器学习等方面的文章。
![image](https://github.com/Anfany/Machine-Learning-for-Beginner-by-Python3/blob/master/pythonfan_anfany.jpg)
