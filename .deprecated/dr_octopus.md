母公司：Apocynthion

公司名称：ArenaLabs

公司介绍：
    创始人：Lloyd Lei；fo-founder：Lucas Zhuang，Carice Waggonar，David Ding
    公司背景：Lloyd Lei拥有ucsb物理数学双学士学位，曾就职于中国bytedance担任数据工程师和波士顿动力姐妹公司RAI研究所的研究院。已获得CMU 机器人全奖phd offer，正在考虑拒绝掉offer做 physical ai 的startup。现已获得10万美金天使轮投资。

项目背景：章鱼博士（Dr.Octopus）：
    基于 openarmx 人形同构机械臂开发的9dof + ee的非人形异构机械臂，采用bci ssvep头盔和vr眼动追踪控制机械臂。目标为带着章鱼博士出席2026年谷歌I/O大会和隆重的科技盛会来提高媒体曝光和知名度，以寻求700万美金种子轮融资。

项目规划：借用实验室现有的 openarmx 机械臂进行深度改装。电机结构上，原本单边的电机序列为j1 j2 j3 j4 j5 j6 j7 ee，现在引入两组新的j3'j4'电机，因此现在单边的电机序列为j1 j2 j3' j4'j3 j4 j5 j6 j7 ee。机械结构上，为了适配 引入新的延长臂cnc结构用以连接原来的link2和link3。原本j3 j4 j5组装在同一个cnc结构件上，现在去除掉了j5的部分并且用一个L形状的连接件来接上原本的j3j4j5 cnc结构件。具体图片参照dir中image copy.png和image copy 2 png。config方便，j3' j4'均采用j3 j4的限位参数和动力学定义参数，命名为j3new j4new， 延长件命名为ext_Link,L_link（新的cnc部分应该由两部分组成）。电气方面，需要换掉原来的变压器充电线改用移动电源。外观设计上，将两只机械触手插在一个背包基座上，打造“章鱼博士”动漫人物既视感，寻求视觉上的震撼，以复刻 Ron Lee 创立cluely的融资路径。

项目现状：openarmx的ros2驱动已完善。已完成和制造外观设计。当前需要解决章鱼博士的ros2驱动问题。四个新的电机均未烧录注册。当前已有一个单臂的step file，但是需要转换成ros2需要的文件，并且还需要对mesh和完整的结构分层。这部分可以参照openarmx ws deploy里面的详情。今晚需要完成的事情，创建分层的章鱼博士mesh，然后注册成ros2，明天烧录电机然后打包成新的章鱼博士ws。（不动原本的openarmx ws）