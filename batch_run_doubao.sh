#!/bin/bash

symbols=(
    # ==================== 科技巨头 ====================
    'NVDA' # 英伟达(51800)- AI芯片/半导体/数据中心
    'GOOG' # 谷歌C(46800)- 互联网/广告/云计算/AI
    'AAPL' # 苹果(45900)- 消费电子/软件生态/服务
    'MSFT' # 微软(31700)- 软件/云计算/AI/操作系统
    'AMZN' # 亚马逊(29500)- 电子商务/云计算/物流
    'TSM' # 台积电(22000)- 全球最大芯片代工
    'AVGO' # 博通(20200)- 通信半导体/AI芯片
    'TSLA' # 特斯拉(16600)- 新能源汽车/能源存储/自动驾驶
    'META' # 元宇宙平台(16100)- 社交网络/AI/元宇宙

    # ==================== 半导体 ====================
    'MU' # 美光科技(10400)- 存储芯片/DRAM/NAND
    'ASML' # 阿斯麦(6189)- 光刻机/半导体设备
    'AMD' # 超威半导体(8448)- CPU/GPU/AI芯片
    'INTC' # 英特尔(6076)- CPU/芯片制造/AI
    'KLAC' # 科磊(3977)- 半导体检测设备
    'ARM' # 安谋(3581)- 芯片IP授权
    'AMAT' # 应用材料(3570)- 半导体制造设备
    'QCOM' # 高通(2623)- 移动SoC/汽车芯片/物联网
    'SMCI' # 超微电脑(1850)- AI服务器/数据中心
    'MRVL' # 迈威尔科技(1793)- 数据中心芯片/汽车电子
    'DELL' # 戴尔(1280)- 服务器/PC/企业IT
    'APH' # 安费诺(1120)- 连接器/半导体封装
    'ALAB' # Astera Labs(599)- 高速互连芯片/AI基础设施
    'CBRS' # Cerebras Systems(522)- AI专用芯片/晶圆级引擎
    'ON' # 安森美半导体(485)- 功率半导体/汽车芯片
    'CRDO' # Credo Technology(410)- 高速互连芯片/光模块
    'VRT' # 慧与科技(426)- 服务器/IT基础设施
    'GLW' # 康宁(312)- 玻璃/半导体材料/显示面板
    'WOLF' # Wolfspeed(285)- 碳化硅功率器件
    'NOK' # 诺基亚(877)- 通信芯片/5G设备
    'AMSC' # 美国超导(12)- 超导材料/电力设备
    'PXLW' # Pixelworks(3)- 显示芯片/视频处理
    'POET' # Poet Technologies(2)- 光电子芯片/集成
    'LAES' # LAES(1)- 半导体设备

    # ==================== 人工智能 ====================
    'PLTR' # Palantir(3436)- AI数据分析/国防/企业
    'APP' # Applovin(2015)- 移动广告/AI推荐引擎
    'CRWD' # CrowdStrike(1708)- 网络安全/AI威胁检测
    'GDS' # 万国数据(180)- 数据中心/AI基础设施
    'BBAI' # BigBear.ai(15)- 国防AI/决策支持   
    'UPST' # Upstart(12)- AI信贷评估/金融科技
    'SOUN' # SoundHound(8)- AI语音识别/对话系统
    'CIFR' # Cipher Mining(5)- AI计算/加密挖矿
    'INOD' # Innodata(3)- AI数据标注/训练数据
    'VERI' # Veritone(2)- AI媒体分析/内容理解

    # ==================== 能源-核电 ====================
    'CEG' # Constellation Energy(1280)- 美国最大核电运营商
    'GEV' # GE Vernova(1120)- 核电设备/能源基础设施
    'BWXT' # BWX Technologies(183)- 核反应堆部件/国防
    'SMR' # NuScale Power(45)- 小型模块化反应堆(SMR)
    'OKLO' # Oklo(32)- 钠冷快堆/先进核能
    'LEU' # Centrus Energy(28)- 铀浓缩/核燃料
    'NNE' # Nano Nuclear Energy(12)- 微反应堆/便携式核能
    'LBRT' # Liberty Energy(18)- 能源服务/油田技术
    'USEG' # U.S. Energy Corp(5)- 传统能源/油气

    # ==================== 能源-传统 ====================
    'NRG' # NRG Energy(185)- 电力/天然气/可再生能源
    'VST' # Vistra Energy(120)- 电力/能源批发
    'AES' # AES Corp(150)- 全球电力/可再生能源

    # ==================== 能源-新能源 ====================
    'ETN' # 伊顿(1050)- 电气设备/新能源/工业自动化
    'FSLR' # 第一太阳能(294)- 光伏组件/薄膜太阳能
    'ENPH' # Enphase Energy(120)- 光伏逆变器/家用储能
    'QS' # QuantumScape(85)- 固态电池/电动汽车
    'JKS' # 晶科能源(85)- 光伏组件/太阳能电站
    'NVTS' # Novanta(120)- 精密运动控制/医疗/工业
    'BE' # Bloom Energy(45)- 燃料电池/分布式发电
    'PLUG' # Plug Power(35)- 氢能源/燃料电池
    'FLNC' # Fluence(25)- 储能系统/可再生能源
    'TMDE' # TimkenSteel(30)- 特种钢/能源设备
    'MVST' # Microvast(15)- 动力电池/商用车
    'SES' # SES AI(12)- 固态电池/锂金属
    'EOSE' # Eos Energy(8)- 长时储能/锌电池
    'VTS' # Vitesse Energy(5)- 能源开发

    # ==================== 自动驾驶与电动汽车 ====================
    'UBER' # 优步(1444)- 网约车/自动驾驶/外卖
    'STLA' # 斯特兰蒂斯(520)- 传统汽车/电动化转型
    'MBLY' # Mobileye(320)- 自动驾驶芯片/ADAS
    'RIVN' # Rivian(195)- 电动皮卡/SUV
    'AUR' # Aurora(130)- L4自动驾驶/卡车
    'LCID' # Lucid(120)- 豪华电动汽车
    'WRD' # 文远知行(45)- Robotaxi/自动驾驶
    'INVZ' # Innoviz(12)- 激光雷达/自动驾驶
    'CYN' # Cyan(5)- 自动驾驶软件
    'MVIS' # 维视图像(2)- 激光雷达/机器视觉

    # ==================== 生物医药 ====================
    'LLY' # 礼来(10600)- 制药/糖尿病/肥胖症/阿尔茨海默
    'NVO' # 诺和诺德(2016)- 制药/糖尿病/肥胖症
    'PFE' # 辉瑞(1490)- 制药/疫苗/抗感染
    'BMY' # 百时美施贵宝(1162)- 制药/肿瘤/免疫
    'ELV' # Elevance Health(1280)- 健康保险/医疗服务
    'ONC' # 百济神州(334)- 创新药/肿瘤
    'ILMN' # 因美纳(420)- 基因测序/生命科学
    'MDLN' # Madrigal Pharmaceuticals(122)- 非酒精性脂肪肝
    'CRSP' # CRISPR Therapeutics(120)- 基因编辑/遗传病
    'CELC' # Celcuity(64)- 癌症诊断/伴随诊断
    'HIMS' # Hims & Hers(120)- 数字健康/消费医疗
    'MRNA' # 莫德纳(189)- mRNA疫苗/传染病
    'RXRX' # Recursion Pharmaceuticals(45)- AI药物研发
    'TDOC' # Teladoc(35)- 远程医疗/虚拟护理
    'VKTX' # Viking Therapeutics(37)- 代谢疾病/肥胖症
    'NVAX' # Novavax(12)- 疫苗/传染病
    'AMWL' # American Well(8)- 远程医疗平台
    'WGS' # Whole Genome Sequencing(3)- 全基因组测序
    'GENB' # Genprex(2)- 基因治疗/肺癌
    'ATNM' # Actinium Pharmaceuticals(5)- 放射治疗/肿瘤
    'ATPC' # Atossa Therapeutics(1)- 乳腺癌/女性健康
    'OMDA' # Omega Diagnostics(1)- 体外诊断
    'HCTI' # Health Catalyst(1)- 医疗IT/数据分析
    'PSTV' # Positron(1)- 核医学成像
    'TEM' # Tempo Therapeutics(1)- 癌症治疗
    'SPRC' # Sparc(1)- 生物科技

    # ==================== 中国概念股 ====================
    'BABA' # 阿里巴巴(3516)- 电子商务/云计算/物流
    'PDD' # 拼多多(1616)- 社交电商/跨境电商
    'BIDU' # 百度(455)- 搜索/AI/自动驾驶
    'JD' # 京东(407)- 电子商务/物流
    'LI' # 理想汽车(320)- 智能电动汽车/增程式
    'NIO' # 蔚来(160)- 智能电动汽车/换电
    'XPEV' # 小鹏汽车(160)- 智能电动汽车/自动驾驶
    'GDS' # 万国数据(180)- 数据中心/云服务
    'BILI' # 哔哩哔哩(120)- 视频/游戏/社区
    'EDU' # 新东方(85)- 教育/培训
    'PONY' # 小马智行(80)- 自动驾驶/Robotaxi
    'KC' # 金山云(30)- 云计算/企业服务
    'NIU' # 小牛电动(25)- 智能两轮车
    'HSAI' # 禾赛科技(31)- 激光雷达/自动驾驶
    'CHA' # 喜茶(5)- 消费

    # ==================== 存储芯片 ====================
    'SNDK' # 闪迪(2431)- NAND闪存/存储解决方案
    'STX' # 希捷科技(1975)- 机械硬盘/HDD
    'WDC' # 西部数据(1831)- 机械硬盘/NAND闪存
    'RMBS' # Rambus(120)- 内存接口芯片/半导体IP
    'SIMO' # Silicon Motion(85)- 闪存控制器/SSD

    # ==================== 金属与矿产 ====================
    'FCX' # 麦克莫兰铜金(947)- 铜/金/钼矿产
    'MP' # MP Materials(37)- 稀土开采/加工
    'LAC' # Lithium Americas(18)- 锂矿/电池材料
    'CRML' # Critical Metals(18)- 锂/稀土/关键金属

    # ==================== 通信与网络 ====================
    'VZ' # 威瑞森(1680)- 电信运营商/5G
    'S' # 美国电话电报公司(1250)- 电信运营商/媒体
    'PANW' # 派拓网络(2015)- 网络安全/防火墙
    'ANET' # Arista Networks(1120)- 数据中心交换机/云网络
    'LITE' # Lumentum(702)- 光通信器件/激光
    'UI' # Ubiquiti(369)- 网络设备/无线
    'SATS' # 回声星通信(355)- 卫星通信/宽带
    'HPE' # 慧与科技(426)- 服务器/网络/企业IT
    'AAOI' # Applied Optoelectronics(153)- 光通信器件/光模块
    'ASTS' # AST SpaceMobile(39)- 卫星通信/移动网络
    'ONDS' # Ondas Holdings(5)- 无线通信/工业物联网

    # ==================== 互联网与流媒体 ====================
    'SPOT' # Spotify(1062)- 音乐流媒体/播客
    'ROKU' # Roku(194)- 流媒体设备/平台
    'RUM' # Rumble(12)- 视频平台/保守派媒体

    # ==================== 金融科技 ====================
    'NU' # Nu Holdings(593)- 拉丁美洲数字银行
    'PYPL' # 贝宝(391)- 数字支付/在线支付
    'AFRM' # Affirm(161)- 先买后付/消费金融
    'HOOD' # Robinhood(180)- 零佣金券商/加密交易
    'SOFI' # SoFi Technologies(120)- 数字银行/投资/贷款    
    'CHYM' # Chime(98)- 美国数字银行
    'STNE' # StoneCo(28)- 巴西数字支付/金融科技

    # ==================== 加密货币 ====================
    'MSTR' # MicroStrategy(531)- 比特币储备公司/企业软件
    'COIN' # Coinbase(480)- 加密货币交易所
    'TRON' # 波场(330)- 公链/去中心化应用
    'MARA' # Marathon Digital(120)- 比特币挖矿
    'RIOT' # Riot Platforms(110)- 比特币挖矿   
    'HUT' # Hut 8(85)- 比特币挖矿/AI计算
    'APLD' # Applied Digital(65)- 数据中心/加密挖矿/AI
    'IREN' # Iris Energy(45)- 比特币挖矿/可持续能源
    'BLSH' # Bullish(35)- 加密货币交易所
    'CRCL' # Circle(25)- USDC稳定币发行商
    'BTBT' # Bit Digital(7)- 比特币挖矿
    'BTDR' # Bitdeer(15)- 比特币挖矿/云算力    
    'BMNR' # BitMEX(15)- 加密衍生品交易所
    'FIG' # Figure(12)- 区块链金融/贷款
    'BKKT' # Bakkt(8)- 加密交易/机构服务
    'ABTC' # Abra(5)- 加密钱包/投资
    'NAKA' # Nakamoto(3)- 加密货币
    'BVC' # BVC(2)- 加密货币
    'BTCS' # Bitcoin Services(1)- 加密货币
    'XYZ' # XYZ(1)- 加密货币

    # ==================== 软件与SaaS ====================
    'ORCL' # 甲骨文(5859)- 企业软件/数据库/云
    'SHOP' # Shopify(1493)- 电商SaaS/中小企业
    'CRM' # 赛富时(1441)- CRM/客户关系管理
    'NOW' # ServiceNow(1074)- IT服务管理/工作流
    'SNPS' # 新思科技(920)- EDA软件/半导体设计
    'DDOG' # Datadog(802)- 可观测性/监控
    'SNOW' # Snowflake(680)- 数据仓库/云数据平台
    'DASH' # DoorDash(683)- 外卖配送/本地服务
    'RBLX' # Roblox(335)- 元宇宙游戏/用户生成内容
    'SE' # Sea(320)- 东南亚互联网/游戏/电商
    'MDB' # MongoDB(262)- NoSQL数据库
    'NET' # Cloudflare(350)- CDN/网络安全/边缘计算
    'PATH' # UiPath(180)- RPA/机器人流程自动化
    'TWLO' # Twilio(150)- 云通信/API
    'DBX' # Dropbox(120)- 云存储/文件共享
    'IOT' # Samsara(120)- 工业物联网/运营技术
    'GME' # 游戏驿站(120)- 游戏零售/电商
    'GTLB' # GitLab(80)- DevOps/代码托管
    'RDDT' # Reddit(85)- 社交媒体/论坛
    'DJT' # Trump Media(80)- 社交媒体/Truth Social
    'U' # Unity(65)- 游戏引擎/3D内容
    'FSLY' # Fastly(45)- CDN/边缘计算
    'OPEN' # Opendoor(45)- 房地产科技/在线卖房
    'DOCN' # DigitalOcean(35)- 云服务器/开发者
    'NBIS' # N-able(25)- IT管理/MSP
    'PDYN' # PagerDuty(20)- IT运维/事件响应
    'KEEL' # Keel(15)- 企业软件
    'CLSK' # CleanSpark(12)- 软件/比特币挖矿
    'AIIO' # AIIO(5)- 企业软件
    'ZENA' # Zena(3)- 企业软件
    'VIVO' # Vivo(2)- 企业软件
    'DXYZ' # DXYZ(1)- 软件

    # ==================== 航天航空与国防 ====================
    'GE' # 通用电气(3310)- 航空发动机/能源/医疗
    'RKLB' # Rocket Lab(857)- 商业火箭发射/太空服务
    'AXON' # Axon Enterprise(354)- 国防/执法技术/Tasers
    'HEI' # Heico(432)- 航空零部件/国防电子
    'AVAV' # AeroVironment(107)- 无人机/国防
    'KTOS' # Kratos(122)- 国防无人机/靶机
    'JOBY' # Joby Aviation(85)- eVTOL/空中出租车
    'ACHR' # Archer Aviation(65)- eVTOL/电动垂直起降
    'EH' # 亿航智能(45)- eVTOL/城市空中交通
    'RDW' # Redwire(25)- 太空基础设施/3D打印
    'LUNR' # Intuitive Machines(15)- 月球着陆器/太空探索
    'RCAT' # Red Cat(12)- 无人机/国防
    'SIDU' # Sidus Space(8)- 卫星/太空服务
    'MNTS' # Momentus(5)- 太空运输/轨道服务
    'DFNS' # Defense(3)- 国防技术
    'AIRO' # Airobotics(2)- 无人机/自动化
    'UMAC' # Umbra(2)- 卫星/雷达成像
    'VOYG' # Voyager Space(2)- 太空基础设施
    'KULR' # KULR Technology(1)- 热管理/航天
    'RKTO' # Rocket(3)- 火箭技术
    'MOB' # Mobilicom(1)- 通信/国防
    'DPRO' # DPRO(1)- 国防产品
    'JTAI' # JTAI(1)- AI国防

    # ==================== 量子计算 ====================
    'IONQ' # IonQ(262)- 离子阱量子计算
    'QBTS' # D-Wave(86)- 量子退火/优化
    'RGTI' # Rigetti(59)- 超导量子计算
    'QUBT' # Quantum Computing(28)- 量子软件/解决方案
    'ARQQ' # Arqit(12)- 量子加密/网络安全

    # ==================== 机器人 ====================
    'RR' # Richtech Robotics(7)- 服务机器人/餐饮
    'SERV' # Serve Robotics(6)- 配送机器人/最后一公里
    'ARBE' # Arbe Robotics(1)- 自动驾驶雷达/4D成像
    'KITT' # KITT(1)- 机器人技术

    # ==================== 其他 ====================
    'CORZ' # CoreWeave(583)- 云服务/AI计算/GPU云
    'COHR' # Coherent(120)- 激光/光电子/材料加工
    'SEI' # SEI Investments(250)- 金融服务/资产管理
    'TSEM' # Tower Semiconductor(85)- 芯片代工/模拟芯片
    'ASTC' # ASTC(1)- 科技
)
# 设置默认值
if [ -z "$1" ]; then
    period="1y"
else
    period="$1"
fi

if [ -z "$2" ]; then
    interval="1d"
else
    interval="$2"
fi

if [ -z "$3" ]; then
    save_root="/Users/chengxian/Desktop/buy_sell_images"
else
    save_root="$3"
fi

for symbol in "${symbols[@]}"
do
#    echo "$symbol"
#    python candle_dark.py --symbol $symbol --period ${period} --interval ${interval}
   python candle_dark_doubao.py --symbol $symbol --period ${period} --interval ${interval} --save_root ${save_root}
done
echo "plot end..."