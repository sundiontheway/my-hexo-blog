title: GO语言 | 要点总结
date: 2015-02-01
categories: 学习笔记
tags: go
---

Go语言的学习笔记。

<!--more-->

### 特点：
并发，垃圾回收，头文件简单


### 安装：
源码，标准包，第三方工具
标准包—一键安装，一键配置环境变量
查看环境变量：go env
bin：编译后生成的可执行文件
pkg：编译后生成的包文件
src：存放源码
配置gopath环境变量

### go命令：

    go get 获取远程包：git，hg
    go run：直接运行
    go build：编译
    go fmt：一般不用
    go install：编译包文件，编译主程序
    go test：运行测试文件
    go doc：查看文档

### 建立一个本地说明文档：
godoc -http=:8080
访问localhost:8080 查看文档

### 程序一般结构
由package来组织程序，只有名称为main的包可以包含main函数

    import  导入的包名（或 import { 包名 }）
    const PI = 3.14  // 定义常量
    var name = "gopher" // 全局变量
    type newType int //类型定义
    type gopher struct {
    }  // 定义结构
    type golang interface{} // 定义接口
    func main(){
    } //main函数


package要放在非注释的第一行
main函数和main包必须同时在一个文件里
调用包中的函数 pkgname.funcname

package别名的设置  import newname "fmt"
package省略调用 import . "fmt" 调用时候就可以省略（不推荐使用）
*省略调用和别名不可以同时使用*

### 可见性规则
使用大小写来决定是否可以被外部包调用


### 变量
声明多个变量、全局变量和一般类型的方法:类似import多个包。(变量组的声明不能放在函数体内)

### Go基本类型：
布尔型：bool 1字节 不能和数字比较
整型： int uint
8位整型 int8 uint8
字节型：byte 实际是uint8的别名
16位整型：int16 uint16
32位整型：int32(rune) uint32
64位整型：int64 uint64
浮点型 float32 float64 (注意没有double型)
复数
数组、结构、字符串
切片、map、chan
接口类型
函数类型

类型0值：类型声明的默认值，布尔型默认false，string是空字符串


检查是否类型溢出 math.MaxInt32 就是int32的最大值
go语言不存在隐式转换，必须人为强制转换

类型推断：
var b = 1 这时b的类型判定为整型
省略var关键字和类型 b := 1（全局变量不可以省略）

在函数体内多个变量的声明：

    func main(){
         var a,b,c,d int = 1,2,3,4 // a,b,c,d := 1,2,3,4
    }

空白符号(一般用在函数有多个返回值的时候)

    a,_,b,c = 1,2,3,4

变量的类型转换
不存在隐式转换，所有类型必须显式转换
*转换只能发生在相互兼容的类型之间*
格式：

    var a float32 = 100.1
    b := int(a) //此时b为100

定义常量：等号右侧必须是常量或者常量表达式

iota定义枚举（iota的值只和变量的位置有关，并且遇到const之后就置回0）

运算符：
从左到右结合


指针：不支持指针运算。
使用.
`&`取变量地址，用`*`访问变量对象，默认nil

`++`和`--`不是表达式，而是语句（只能当成语句放在单独的一行，而且只能放在变量的右边）

    if 1<2 // 不加括号
    if a:=1; a > 1 //先初始化a，a只能作用在if内部（如果外部也定义了a，那if内部的a会暂时隐藏外部的a）


循环语句只有for 没有while
for支持三种形式：

    for {
        a++
        if a > 3 {
            break
        }
    }

    for a <= 3 {
        a++
    }

    for i:=0 ;i<3; i++ {
       a++
    }

switch 不需要break，如果想继续运行需要fallthrough

    switch a >0 {
    case 0:
    case 1:
    default:
    }

    switch {
    case a=0 :
        fallthrough
    case a=1:
        fallthrough
    default:
    }

    switch a:=1; { // a只在switch语句内部有效
    }

跳转语句 goto break continue
三个语句都可以配合标签的使用，例如跳出多层循环
标签名区分大小写

    LABEL1：
     for {
        for {
            break LABEL1
        }
    } // 跳出到LABEL1所在层次

    LABEL1：
     for i:=0;i<10;i++ {
        for {
             continue LABEL1
       }
    } // 跳过无限循环，继续外部有限循环


### 数组
数组并不是统一的类型，长度不同的数组，是不同的类型，不能直接赋值

    var a [2]int 
    var b [1]int
    var c [2]int

    b = a //非法
    c = a //合法


    a := [20]int{19:1} // 索引号为19的元素赋值1，其他都默认0
    a := [...]int{1,2,3,4,5}
    a := [...]int{0:1, 1:2, 2:3} //输出1,2,3
    a := [...]int{2:3} //输出0,0,3


Go支持多维数组
Go中的数组都是值类型，不是引用类型（引用类型可以参考切片）


### 切片Slice
本身并不是数组，底层指向数组
作为变长数组的替代方案。可以关联底层数组的局部或者全部
引用类型
可以直接创建或从底层数组获取生成
len()获取元素个数，cap()获取容量
make()创建

    var s1 []int //创建，无数组大小的slice类型

    a := [10]int{}
    s1 := a[9] //s1为0(取索引值为9的元素)
    s2 :=a[5:10] //a[5 6 7 8 9]


    s1 := make([]int, 3, 10) // make(数组类型，元素个数，分配的容量)

切片的索引相对于被切片的数组为准，超出数组的长度就会越界。

append追加元素

    s1 = append(s1, 1,2,3)

多个slice指向同一个数组的元素，任何一个slice修改了该元素，其他slice中也会改变
（某个切片超出容量，继续添加元素时，会重新分配空间并把之前的值拷贝过去，这时候其他切片修改底层数组就不影响该切片了）

    copy(s1,s2) //将s2复制到s1中
如果s1比s2元素少，则拷贝后只有s2中的部分元素覆盖了s1中的元素

### map

    var m := map[int]string
map的key必须是能够进行等号等操作的，也就是说slice，map等不可以用作key
map可以嵌套，就是用map类型作map的value
例如：

    m := make(map[int]map[int]string)
    m[1] = make(map[int]string) // 每一级的map都需要单独初始化，否则运行时会出错
    a := m[2][1]

用迭代操作map,slice

    for i,v:=range slice1 { // i=索引，v=slice1的i元素的值 *v是拷贝值，对v赋值不会影响slice里的值
    }
    for k,v:=range map1{ // k=key v = value *v是一个拷贝值，任何操作都不影响map里的值
    }

map存储是无序的！

    m = map[int]string{1:"a", 2:"b", 3:"c"} //输出为乱序

如何让它有序排列？

    import sort
    sort.Ints(s)




