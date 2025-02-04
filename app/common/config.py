# coding:utf-8
from enum import Enum
import datetime
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,OptionsValidator,
                            RangeConfigItem, RangeValidator,FolderValidator)

YEAR = datetime.datetime.now().year
AUTHOR = "shiyi0x7f"
VERSION = "2.0.4"
PRODHOST = '生产服务器地址'
DEVHOST = "127.0.0.1:8000"
TESTHOST = "测试服务器地址"
HELP_URL = "https://dquyl9k1r5u.feishu.cn/docx/HdPzd8HOwoWrzRxxdM3ckoYJn6c"
FEEDBACK_URL = "https://dquyl9k1r5u.feishu.cn/docx/HdPzd8HOwoWrzRxxdM3ckoYJn6c"
Languages = {'中文': 'chinese', '繁体': 'traditional chinese','英语': 'english', '俄语': 'russian', '德语': 'german', '西班牙语': 'spanish', '荷兰语': 'dutch', '法语': 'french', '意大利语': 'italian', '葡萄牙语': 'portuguese', '巴西葡萄牙语': 'brazilian',  '波兰语': 'polish', '乌克兰语': 'ukrainian', '保加利亚语': 'bulgarian', '希腊语': 'greek', '罗马尼亚语': 'romanian', '摩尔多瓦语': 'moldavian', '土耳其语': 'turkish', '波斯语': 'persian', '阿拉伯语': 'arabic', '日语': 'japanese', '瑞典语': 'swedish', '匈牙利语': 'hungarian', '塞尔维亚语': 'serbian', '拉丁语': 'latin', '克罗地亚语': 'croatian', '捷克语': 'czech', '哈萨克语': 'kazakh', '白俄罗斯语': 'belarusian', '印度尼西亚语': 'indonesian', '马来西亚语': 'malaysian', '立陶宛语': 'lithuanian', '加泰罗尼亚语': 'catalan', '芬兰语': 'finnish', '阿塞拜疆语': 'azerbaijani', '韩语': 'korean', '孟加拉语': 'bengali', '世界语': 'esperanto', '印地语': 'hindi', '乌拉都语': 'urdu', '丹麦语': 'danish', '乌兹别克语': 'uzbek', '斯洛伐克语': 'slovak', '挪威语': 'norwegian', '越南语': 'vietnamese', '土著语': 'indigenous', '巴什基尔语': 'bashkir', '马拉提语': 'marathi', '吉尔吉斯语': 'kyrgyz', '塔吉克语': 'tajik', '鞑靼语': 'tatar', '阿尔巴尼亚语': 'albanian', '索马里语': 'somali', '冰岛语': 'icelandic', '蒙古语': 'mongolian', '拉脱维亚语': 'latvian', '格鲁吉亚语': 'georgian', '梵文': 'sanskrit', '希伯来语': 'hebrew', '斯洛文尼亚语': 'slovenian', '拉雅拉姆语': 'malayalam', '南非语': 'afrikaans', '尼泊尔语': 'nepali', '僧伽罗语': 'sinhala', '柏柏尔人': 'berber', '亚美尼亚语': 'armenian', '克里米亚鞑靼语': 'crimean', '泰米尔语': 'tamil', '奥迪亚语': 'odia', '斯瓦希里语': 'swahili', '古吉拉特语': 'gujarati', '泰卢固语': 'telugu', '卡纳达语': 'kannada', '爱沙尼亚语': 'estonian', '泰语': 'thai', '查莫罗语': 'chamorro', '加利西亚语': 'galician', '阿布哈兹语': 'abkhazian', '阿法尔语': 'afar', '阿坎语': 'akan', '阿姆哈拉语': 'amharic', '阿拉贡语': 'aragonese', '阿萨姆语': 'assamese', '阿尔瓦语': 'avaric', '阿维斯陀语': 'avestan', '艾马拉语': 'aymara', '班巴拉语': 'bambara', '巴斯克语': 'basque', '比斯拉马语': 'bislama', '波斯尼亚语': 'bosnian', '凯尔特语': 'breton', '缅甸语': 'burmese', '车臣语': 'chechen', '齐切瓦语': 'chichewa', '教会斯拉夫语': 'church_slavic', '楚瓦什语': 'chuvash', '科恩语': 'cornish', '科西嘉语': 'corsican', '克里语': 'cree', '马尔代夫语': 'divehi', '宗卡语': 'dzongkha', '埃维语': 'ewe', '法罗语 ': 'faroese', '斐济语': 'fijian', '西弗里斯兰语': 'western_frisian', '富拉尼语': 'fulah', '盖耳语\n': 'gaelic', '干达语': 'ganda', '格陵兰语': 'kalaallisut', '瓜拉尼语': 'guarani', '海地语': 'haitian', '豪萨语': 'hausa', '格列罗语': 'herero', '希里摩图语': 'hiri_motu', '伊多语': 'ido', '伊格博语': 'igbo', '国际语': 'interlingua', '西方国际语': 'occidental', '伊努伊特语': 'inuktitut', '因努伊特语': 'inupiaq', '爱尔兰语': 'irish', '爪哇语': 'javanese', '卡努里语': 'kanuri', '克什米尔语': 'kashmiri', '高棉语': 'central_khmer', '基库尤语': 'kikuyu', '基尼亚卢旺达语': 'kinyarwanda', '科米': 'komi', '刚果语': 'kongo', '库纳马语': 'kuanyama', '库尔德': 'kurdish', '老挝语': 'lao', '林堡语': 'limburgan', '林加拉语': 'lingala', '卢巴-加丹加语': 'luba-katanga', '卢森堡语': 'luxembourgish', '马其顿语': 'macedonian', '马达加斯加语': 'malagasy', '马尔他语': 'maltese', '缅因语': 'manx', '毛利语': 'maori', '马歇尔语': 'marshallese', '瑙鲁语': 'nauru', '纳瓦霍语': 'navajo', '北恩德贝勒语': 'north_ndebele', '南恩德贝勒语': 'south_ndebele', '恩东加语': 'ndonga', '书面挪威语': 'norwegian_bokmal', '尼诺斯克语': 'norwegian_nynorsk', '诺苏': 'sichuan_yi', '奥克西唐语': 'occitan', '奥吉布韦语': 'ojibwa', '奥罗莫语': 'oromo', '奥赛梯语': 'ossetian', '巴利语': 'pali', '普什图语': 'pashto', '旁遮普语': 'punjabi', '奇楚亚语': 'quechua', '罗曼什语': 'romansh', '隆迪语': 'rundi', '北萨米语': 'northern_sami', '萨摩亚语': 'samoan', '桑戈语': 'sango', '撒丁语': 'sardinian', '绍纳语': 'shona', '信德语': 'sindhi', '塞索托语': 'southern_sotho', '苏丹语': 'sundanese', '斯瓦蒂语': 'swati', '他加禄语 (Filipino)': 'tagalog', '塔希提语': 'tahitian', '西藏语': 'tibetan', '底格莱语': 'tigrinya', '汤加语': 'tonga', '聪加语': 'tsonga', '茨瓦纳语': 'tswana', '土库曼语': 'turkmen', '特维语': 'twi', '维吾尔族语': 'uighur', '文达语': 'venda', '沃拉皮尤克语': 'volapuk', '瓦龙': 'walloon', '威尔士语': 'welsh', '沃洛夫语': 'wolof', '科萨语': 'xhosa', '意地绪语': 'yiddish', '约鲁巴语': 'yoruba', '壮语': 'zhuang', '祖鲁语': 'zulu'}
SearchMode = {'默认': None, '热度': 'popular', '匹配度': 'bestmatch', '名称': 'title', '上传日期': 'date', '出版日期': 'year'}
Extensions = {'所有': None, 'txt': 'txt', 'pdf': 'pdf', 'epub': 'epub', 'mobi': 'mobi', 'azw': 'azw', 'azw3': 'azw3'}

class Config(QConfig):
    """ Config of application """

    # folders
    downloadFolder = ConfigItem("Settings", "DownloadFolder", "download", FolderValidator())
    downloadSwitch = ConfigItem("Settings",
                                "DownloadSwitch",
                                True, BoolValidator())
    reapeatFiles = ConfigItem("Settings",
                                "repeatFiles",
                                True, BoolValidator())
    searchNums = RangeConfigItem("Settings", "Nums", 50,RangeValidator(50, 200))
    language = ConfigItem("Settings", "language", 0,RangeValidator(0,len(Languages)))
    searchMode = ConfigItem("Settings", "searchMode",0, RangeValidator(0,len(SearchMode)))
    extensions = ConfigItem("Settings", "extensions", 0, RangeValidator(0,len(Extensions)))
    accurate = ConfigItem("Settings","accurate",False,BoolValidator())


    dpiScale = OptionsConfigItem("Windows",
                                 "DpiScale",
                                 "Auto",
                                 OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
                                 restart=True)

    # Update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())
    updateMode = ConfigItem("Update","updateMode",True, BoolValidator())
    latestVersion = ConfigItem("Update", "latestVersion",None)


cfg = Config()
qconfig.load('config/config.json', cfg)