---
title: Thin Plate Spline
date: 2016-04-24 18:05:32
tags: 数学
---

------

# 1. Thin Plate Spline

简单来说，TPS是一种$ f: \mathbb R^K → \mathbb R^L $的座标变换。
此变换包含两部分，第一是Affine $f\_A(x)$, 第二是Kernel $f\_K(x)$。

完整的TPS如下:

$$
f(x)=f\_A(x)+f\_K(x)=\underbrace{Ax+b}\_{\text{Affine}}+\overbrace{\sum\_{n=1}^N w^{(n)} \varphi(x^{(n)}, x)}^{\text{Kernel}}
\tag{1}
$$
其中，

$x$是变换前的K维座标；$f(x)$是变换后L维新座标；$x^{(n)}$是K维控制点，总共N个；$\varphi()$是核函数。
如此，便实现了$ \mathbb R^K→ \mathbb R^L $的变换。

变换后的第$i$维$(i=1,...,L)$：

$$
f\_i(x)=\sum\_{j=1}^K A\_{ij}+b\_i+\sum\_{n=1}^N W\_{in}\varphi(x^{(n)}, x)
\tag{2}
$$

------

# 2. TPS的能量函数1

TPS的能量函数包含数据项Data和平滑项TPS：

$$
E(f) = E\_{Data} + \lambda E\_{TPS} = \underbrace{\sum\_{n=1}^N ||y^{(n)}-f(x)^{(n)}||^2}\_{\text{Data项}} + \overbrace{\lambda \int\_{\mathbb R^K} dx||D^2f(x)||\_{Frob.}}^{\text{TPS平滑项}}
\tag{3}
$$

其中，

- $\lambda$是平滑项和数据项的平衡系数。
- $y^{(n)}$是变换后的\_L\_维控制点，与变换前的\_K\_维控制点$x^{(n)}$一一对应。
- 数据项比较简单，用来表征控制点的误差。
- 平滑项比较复杂，用来表征变换后数据的平滑性。

平滑项的具体定义为TPS变换$f(x)$二次微分$[D^2f(x)]\_{ijk}$

$$
[D^2f(x)]\_{ijk} = \frac{\partial^2 f\_i(x)}{\partial x\_j \partial x\_k}
\tag{4}
$$

的[Frobenius范数](http://mathworld.wolfram.com/FrobeniusNorm.html)累加和$||D^2f(x)||\_{Frob.}$

$$
||D^2f(x)||\_{Frob.} = \sum\_{i=1}^L \sum\_{j=1}^K \sum\_{k=1}^K |\frac{\partial^2}{\partial x\_j \partial x\_k}f\_i(x)|^2
\tag{5}
$$

在原始K维空间中的积分$\int\_{\mathbb R^K} dx||D^2f(x)||\_{Frob.}$。具体的计算见下节。

------

# 3. 基于核函数的TPS平滑项
首先定义一下核函数:

$$
\varphi(x, x^,) =
\begin{cases}
r^4-Klnr & \text{(K为基数)} \\\\
r^4-K & \text{(K为偶数)}
\end{cases} \\\\
\tag{6}
$$

其中$r=||x-x^,||$。
接着处理原始K维空间中的积分$\int\_{\mathbb R^K} dx||D^2f(x)||\_{Frob.}$：

$$
E\_{TPS}=\int\_{\mathbb R^K}dx||D^2f(x)||\_{Frob.}=\int\_{\mathbb R^K}dx\sum\_{i=1}^L\sum\_{j=1}^K\sum\_{k=1}^K|\frac {\partial^2} {\partial x\_j \partial x\_k} f\_i (x)|^2
\tag{7}
$$

$$
=\int\_{\mathbb R^K}dx\sum\_{i=1}^L\sum\_{j=1}^K\sum\_{k=1}^K|\frac {\partial^2} {\partial x\_j \partial x\_k} \sum\_{n=1}^N W\_{in} \varphi(x^{(n)}, x) |^2
\tag{8}
$$

$$
= \mathbf Tr( \mathbf {W \phi W^T}) = \sum\_{i=1}^L \sum\_{n=1}^N \sum\_{m=1}^N W\_{in} \phi\_{mn} W\_{im}
\tag{9}
$$

其中$\phi\_{mn}=\varphi(||x^{(n)}-x^{(m)}||)$。

# 4. TPS能量函数2

把式(1)，式(9)，以及核函数的定义带入能量函数(3):

$$
E(f)=E\_{Data}+\lambda E\_{TPS}
\tag{10}
$$

$$
= \sum\_{n=1}^N || y^{(n)} - Ax^{(n)} - b - \sum\_{m=1}^Nw^{(m)}\varphi(||x^{(n)}-x^{(m)}||)||^2 + \lambda \mathbf Tr( \mathbf {W \phi W^T})
\tag{11}
$$

$$
= \sum\_{n=1}^N || y^{(n)} - Ax^{(n)} - b - \sum\_{m=1}^Nw^{(m)}\varphi(||x^{(n)}-x^{(m)}||)||^2 + \lambda \sum\_{i=1}^L \sum\_{n=1}^N \sum\_{m=1}^N W\_{in} \phi\_{mn} W\_{im}
\tag{12}
$$

其中，

- $Y\_{in}$ 是变换后的第n个控制点的第i维(共L维)。
- $X\_{jn}$ 是变换前的第n个控制点的第j维(共K维)。

如式(12)所示，TPS的能量函数最终归结为关于三个变量$A\_{ij}, b\_i, W\_{in}$的二次函数。

- 第一项$E\_{Data}$明显是关于变量($A\_{ij}, b\_i$)下突二次函数。
- 第二项$E\_{TPS}$可以看作关于变量$W$的正系数($\mathbf \phi$)连加下突二次($W\_{in}W\_{im}$)函数。

两项都下突，TPS能量函数的最小值就可能存在解析解。

# 5. 能量函数最小值

首先对三个变量$A\_{ij}, b\_i, W\_{in}$分别求偏导:

$$
\frac {\partial E(f)} {\partial A\_{ij}} = -2 \sum\_{n=1}^K (Y\_{in} - \sum\_{k=1}^K A\_{ik}X\_{kn} - b\_i - \sum\_{l=1}^N W\_{il} \phi\_{ln}) X\_{jn}
\tag{13}
$$

$$
\frac {\partial E(f)} {\partial b\_i} = -2 \sum\_{n=1}^K (Y\_{in} - \sum\_{k=1}^K A\_{ik}X\_{kn} - b\_i - \sum\_{l=1}^N W\_{il} \phi\_{ln})
\tag{14}
$$

$$
\frac {\partial E(f)} {\partial W\_{im}} = -2 \sum\_{n=1}^K (Y\_{in} - \sum\_{k=1}^K A\_{ik}X\_{kn} - b\_i - \sum\_{l=1}^N W\_{il} \phi\_{ln}) \phi\_{mn} + \lambda \sum\_{n=1}^N (W\_{in} \phi\_{mn} + \phi\_{nm} W\_{in})
\tag{15}
$$

令$\partial E(f) = 0$，并利用核函数$\phi\_{mn}=\phi\_{nm}$的对称性，可得:

$$
\sum\_{n=1}^K (Y\_{in} - \sum\_{k=1}^K A\_{ik}X\_{kn} - b\_i - \sum\_{l=1}^N W\_{il} \phi\_{ln}) X\_{jn} = 0 \\
(i=1,...,L, j=1,...,K)
\tag{16}
$$

$$
\sum\_{n=1}^K (Y\_{in} - \sum\_{k=1}^K A\_{ik}X\_{kn} - b\_i - \sum\_{l=1}^N W\_{il} \phi\_{ln}) = 0 \\
(i=1,...,L)
\tag{17}
$$

$$
\sum\_{n=1}^K (Y\_{in} - \sum\_{k=1}^K A\_{ik}X\_{kn} - b\_i - \sum\_{l=1}^N W\_{il} \phi\_{ln} - \lambda W\_{in}) \phi\_{mn} = 0 \\
(i=1,...,L, m=1,...,N)
\tag{18}
$$

进一步整理可得($i,m,n$取值范围同上，下略):

$$
\sum\_{n=1}^N \sum\_{k=1}^K X\_{kn} X\_{jn} A\_{ik} + \sum\_{n=1}^N X\_{jn}b\_i + \sum\_{n=1}^N \sum\_{l=1}^N X\_{jn} \phi\_{ln} W\_{il} = \sum\_{n=1}^N Y\_{in} X\_{jn}
\tag{19}
$$

$$
\sum\_{n=1}^N \sum\_{k=1}^K X\_{kn} A\_{ik} + Nb\_i + \sum\_{n=1}^N \sum\_{l=1}^N \phi\_{ln} W\_{il} = \sum\_{n=1}^N Y\_{in}
\tag{20}
$$

$$
\sum\_{n=1}^N \sum\_{k=1}^K X\_{kn} \phi\_{mn} A\_{ik} + \sum\_{n=1}^N \phi\_{mn}b\_i + \sum\_{l=1}^N (\sum\_{n=1}^N \phi\_{ln} \phi\_{mn} + \lambda \phi\_{ml}) W\_{il} = \sum\_{n=1}^N Y\_{in} \phi\_{mn}
\tag{21}
$$

上式中各项可通过矩阵表示:

- 变换前的K维控制点$X\_{kn}$用$K*N$矩阵表示$\mathbf X$。
- 变换后的L维控制点$Y\_{ln}$用$L*N$矩阵表示$\mathbf Y$。
- 变形系数$W\_{ln}$可以表示为$L*N$矩阵$\mathbf W$。
- Affine变换系数$A\_{lk}$可以表示为$L*K$矩阵$\mathbf A$。
- Affine变换系数$b\_{l}$可以表示为$L*1$矩阵$\mathbf b$。
- 把所有控制点带入核函数$\phi\_{mn}(||x^{(n)-x^{(m)}}||)$，可得$N*N$核矩阵$\mathbf \phi$。

将上述矩阵带入:

$$
\sum\_{k=1}^K A\_{ik}[\mathbf X \mathbf X^T]\_{kj} + bi[\sum\_{n=1}^N X\_{jn}] + \sum\_{l=1}^N[\mathbf X \phi^T]\_{jl}W\_{il} = [\mathbf Y \mathbf X^T]\_{ij}
\tag{22}
$$

$$
\sum\_{k=1}^K A\_{ik}[\sum\_{n=1}^N X\_{kn}] + Nb\_i + \sum\_{l=1}^N[\sum\_{n=1}^N \phi\_{ln}]W\_{il} = [\sum\_{n=1}^N Y\_{in}]
\tag{23}
$$

$$
\sum\_{k=1}^K A\_{ik}[\mathbf X \mathbf \phi^T]\_{km} + b\_i[\sum\_{n=1}^N \phi\_{mn}] + \sum\_{l=1}^N[\mathbf \phi(\mathbf \phi^T + \lambda \mathbf I)]\_ml W\_{il} = [\mathbf Y \mathbf \phi^T]\_{im}
\tag{24}
$$

引入$N*1$的列向量$\mathbf 1$:

$$
[\mathbf A \mathbf X \mathbf X^T]\_{ij} + [\mathbf b(\mathbf X \mathbf 1)^T]\_{ij} + [\mathbf W \mathbf \phi \mathbf X^T]\_{ij} = [\mathbf Y \mathbf X^T]\_{ij}
\tag{25}
$$

$$
[\mathbf A(\mathbf X \mathbf 1)]\_i + [(\mathbf 1^T \mathbf 1)\mathbf b]\_i + [\mathbf W \mathbf \phi \mathbf 1]\_i = [\mathbf Y \mathbf 1]\_i
\tag{26}
$$

$$
[\mathbf A \mathbf X \mathbf \phi^T]\_{im} + [\mathbf b (\mathbf 1^T \mathbf \phi^T)]\_{im} + [\mathbf W (\mathbf \phi^T+\lambda \mathbf I)^T \mathbf \phi^T]\_(im) = [\mathbf  Y \mathbf \phi^T]\_im
\tag{27}
$$

去掉上式中的所有的索引$i,j$，并转置:

$$
\mathbf X^T \mathbf X \mathbf A^T + \mathbf X \mathbf 1 \mathbf b^T + \mathbf X \mathbf \phi^T \mathbf W^T = \mathbf X \mathbf Y^T
\tag{28}
$$

$$
\mathbf 1^T \mathbf X^T \mathbf A^T + \mathbf 1^T \mathbf 1 \mathbf b^T + \mathbf 1^T \mathbf \phi^T \mathbf W^T = \mathbf 1^T \mathbf Y^T
\tag{29}
$$

$$
\mathbf \phi \mathbf X^T \mathbf A^T + \mathbf \phi \mathbf 1 \mathbf b^T + \mathbf \phi(\mathbf \phi^T + \lambda \mathbf I)\mathbf W^T = \mathbf \phi \mathbf Y^T
\tag{30}
$$

至此，已得到关于未知矩阵$\mathbf A，\mathbf b，\mathbf W$的三个方程。
进一步将上述方程组的系数和未知数分离(注意这里系数核未知数都是矩阵，不是常量):

$$
\begin{bmatrix}
\mathbf X^T \mathbf X & \mathbf X \mathbf 1 & \mathbf X \mathbf \phi^T \\\\
\mathbf 1^T \mathbf X^T & \mathbf 1^T \mathbf 1 & \mathbf 1^T \mathbf \phi^T \\\\
\mathbf \phi \mathbf X^T & \mathbf \phi \mathbf 1 & \mathbf \phi(\mathbf \phi^T + \lambda \mathbf I)
\end{bmatrix}
\begin{bmatrix}
\mathbf A^T \\\\
\mathbf b^T \\\\
\mathbf W^T
\end{bmatrix}
=
\begin{bmatrix}
\mathbf X \mathbf Y^T \\\\
\mathbf 1^T \mathbf Y \\\\
\mathbf \phi \mathbf Y^T
\end{bmatrix}
\tag{31}
$$

继续整理:

$$
\begin{bmatrix}
\mathbf \phi(\mathbf \phi^T + \lambda \mathbf I) & \mathbf \phi \mathbf X^T & \mathbf \phi \mathbf 1 \\\\
\mathbf X \mathbf \phi^T & \mathbf X^T \mathbf X & \mathbf X \mathbf 1 \\\\
\mathbf 1^T \mathbf \phi \mathbf 1^T & \mathbf 1 ^T \mathbf X^T & \mathbf 1^T \mathbf 1
\end{bmatrix}
\begin{bmatrix}
\mathbf W^T \\\\
\mathbf A^T \\\\
\mathbf b^T
\end{bmatrix}
=
\begin{bmatrix}
\mathbf \phi \\\\
\mathbf X \\\\
\mathbf 1^T
\end{bmatrix}
\mathbf Y^T
\tag{32}
$$

接着将数据项和平滑项相关矩阵分离:

$$
\left(
\begin{bmatrix}
\mathbf \phi \\\\
\mathbf X \\\\
\mathbf 1^T
\end{bmatrix}
\begin{bmatrix}
\mathbf \phi^T & \mathbf X^T & \mathbf 1
\end{bmatrix} + \lambda
\begin{bmatrix}
\mathbf \phi & \mathbf 0 & \mathbf 0 \\\\
\mathbf 0 & \mathbf 0 & \mathbf 0 \\\\
\mathbf 0 & \mathbf 0 & \mathbf 0
\end{bmatrix}
\right)
\begin{bmatrix}
\mathbf W^T \\\\
\mathbf A^T \\\\
\mathbf b^T
\end{bmatrix} =
\begin{bmatrix}
\mathbf \phi \\\\
\mathbf X \\\\
\mathbf 1^T
\end{bmatrix}
\mathbf Y^T
\tag{33}
$$

最后将未知矩阵放左边，其余部分放右边:

$$
\begin{bmatrix}
\mathbf W^T \\\\
\mathbf A^T \\\\
\mathbf b^T
\end{bmatrix} =
\left(
\begin{bmatrix}
\mathbf \phi \\\\
\mathbf X \\\\
\mathbf 1^T
\end{bmatrix}
\begin{bmatrix}
\mathbf \phi^T & \mathbf X^T & \mathbf 1
\end{bmatrix} + \lambda
\begin{bmatrix}
\mathbf \phi & \mathbf 0 & \mathbf 0 \\\\
\mathbf 0 & \mathbf 0 & \mathbf 0 \\\\
\mathbf 0 & \mathbf 0 & \mathbf 0
\end{bmatrix}
\right)^{-1}
\begin{bmatrix}
\mathbf \phi \\\\
\mathbf X \\\\
\mathbf 1^T
\end{bmatrix}
\mathbf Y^T
\tag{34}
$$

式(34)的计算结果，即为TPS能量函数最小值的参数。
得到此参数后，便可通过(1)式对任意K维座标$x$进行变换，得到新的L维座标$f(x)$。

# References

[1]. Thin plate spline (Wikipedia).
[2]. Chui, Haili, and Anand Rangarajan. “A new point matching algorithm for non-rigid registration.”Computer Vision and Image Understanding 89.2 (2003): 114-141.
[3]. Wood, Simon N. “Thin plate regression splines.” Journal of the Royal Statistical Society: Series B (Statistical Methodology) 65.1 (2003): 95-114.

# 附录(变量索引)

- (知) K: 变换前控制点$X\_{kn}$的维数。
- (知) L: 变换后控制点$Y\_{ln}$的维数。
- (知) $\mathbf x^{(n)}$: 变换前的K维控制点(K*1)。
- (知) $\mathbf y^{(n)}$: 变换后的L维控制点(L*1)。
- (知) $\mathbf X$: 变换前的所有控制点的$K*N$矩阵表示。
- (知) $\mathbf Y$: 变换后的所有控制点的$L*N$矩阵表示。
- (知) $\mathbf \phi$: 所有控制点带入核函数$\phi\_{mn}(||x^{(n)-x^{(m)}}||)$所得$N*N$核矩阵。
- (未) $\mathbf W$: 变形系数$W\_{ln}$的$L*N$矩阵表示。
- (未) $\mathbf A$: Affine变换系数$A\_{lk}$的$L*K$矩阵表示。
- (未) $\mathbf b$: Affine变换系数$b\_{l}$的$L*1$矩阵表示。
