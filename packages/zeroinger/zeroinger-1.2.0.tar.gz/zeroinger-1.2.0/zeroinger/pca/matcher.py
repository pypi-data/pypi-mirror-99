from typing import List
from zeroinger.text import TextFile
from zeroinger.file import PathUtil
import ahocorasick
from collections import defaultdict
from logzero import logger
from .area import Area, AreaPrediction
from .adcode_loader import AdcodeLoader


class AliasBuilder:
    def __init__(self):
        # 特殊的简写,主要是几个少数民族自治区
        self.special_abbre = {
            "内蒙古自治区": "内蒙古",
            "广西壮族自治区": "广西",
            "西藏自治区": "西藏",
            "新疆维吾尔自治区": "新疆",
            "宁夏回族自治区": "宁夏",
            "香港特别行政区": "香港",
            "澳门特别行政区": "澳门"
        }
        self.nations = TextFile.load_lines(PathUtil.path_relative_to_code(__file__, 'nations.txt'))
        self.prov_list = '北京@天津@河北@山西@内蒙古@辽宁@吉林@黑龙江@上海@江苏@浙江省@安徽@福建@江西@山东@河南@湖北@湖南@广东@广西@海南@重庆@四川@贵州@云南@西藏@陕西@甘肃省@青海@宁夏@新疆@台湾@香港特别行政区@澳门@香港@'.split(
            '@')

        self.black_alias = {'互助'}

        pass

    def build_alias(self, area: Area) -> List[str]:
        """
        生成区域简称
        1.特别行政区 + 自治区
        2.省份、城市  直接去除后缀
        3.区县 不去除后缀，因为太容易重名
        4.自治县、盟
        :param area:
        :return:
        """
        name, level = self._find_name(area)
        ret = []
        # 原始名称加入
        ret.append(name)
        # 几个省级自治区 + 特别行政区
        if name in self.special_abbre:
            ret.append(self.special_abbre[name])
        else:
            mark = False
            for k in ['自治', '盟', '旗']:
                if k in name:
                    mark = True
            if mark:
                ret.extend(self._build4nation(name))
        if name.endswith('省') or name.endswith('市'):
            ret.append(name.strip('省').strip('市'))
        new_ret = []
        # 删除过短的名称
        for x in ret:
            if len(x) == 1:
                continue
            if x in self.black_alias:
                continue
            new_ret.append(x)
        # if '互助' in ret:
        #     print(ret, area, new_ret, self.black_alias)
        return list(set(new_ret))

        pass

    def _build4nation(self, name) -> List[str]:
        """
        少数民族处理
        1. AB族自治X
        2. XX盟
        :param name:
        :return:
        """
        ret = []
        if name.endswith('自治县') or name.endswith('自治州'):
            text = name[:-3]
            new_text = text
            while True:
                for x in self.nations:
                    if new_text.endswith(x):
                        new_text = new_text[:-len(x)]
                if text == new_text:
                    break
                text = new_text
            ret.append(text)
            if len(text) > 1:
                ret.append(text + name[-3:])
                ret.append(text + name[-1:])

            pass

        if name.endswith('盟'):
            ret.append(name[:-1])
        for x in ret:
            if x in self.prov_list:
                ret.remove(x)
        return ret

        pass

    def _find_name(self, area: Area) -> (str, int):
        if not self.is_empty(area.area):
            return area.area, 3
        if not self.is_empty(area.city):
            return area.city, 2
        return area.prov, 1

    def is_empty(self, text: str):
        return text is None or text == ''


class PcaMatcher:
    ac = None

    def __init__(self):
        self.ac = None
        self.alias_builder = AliasBuilder()
        self._overall_build()
        pass

    def _overall_build(self):

        if PcaMatcher.ac is None:
            logger.info("PcaMatcher|build ac|start")
            PcaMatcher.ac = ahocorasick.Automaton()
            loader = AdcodeLoader()
            area_list = loader.load()
            self._build(area_list)
            logger.info("PcaMatcher|build ac|end")
            pass
        self.ac = PcaMatcher.ac

    def _build(self, area_list: List[Area]):
        name2area_list = defaultdict(list)
        for area in area_list:
            name_list = self.alias_builder.build_alias(area)
            for name in name_list:
                name2area_list[name].append(area)
        for k, v in name2area_list.items():
            PcaMatcher.ac.add_word(k, (k, v))
        PcaMatcher.ac.make_automaton()

    def _match_without_comb(self, text: str) -> List[AreaPrediction]:
        """
        给定一个文本预测其结果
        1. 去除其中重叠的预测结果，序列中靠前的优先级高
        2. 从前向后组合可能的地址
        :param text:
        :return:
        """
        list_ret = []
        for end_index, value in self.ac.iter(text):
            list_ret.append([end_index - len(value[0]) + 1, end_index, value[0], value[1]])
        list_ret = self._process_overlap(text, list_ret)
        ret = []
        for item in list_ret:
            start, end, name, ent_list = item
            pred = AreaPrediction()
            pred.set_prediction(ent_list)
            level = ent_list[0].level()
            if level == 'AREA':
                pred.set_raw_info(area_text=name, area_pos=start)
            if level == 'CITY':
                pred.set_raw_info(city_text=name, city_pos=start)
            if level == 'PROV':
                pred.set_raw_info(prov_text=name, prov_pos=start)
            ret.append(pred)
        return ret

    def match(self, text: str, enable_comb: bool = True) -> List[AreaPrediction]:
        pred_list = self._match_without_comb(text)
        if enable_comb:
            return self._process_comb(text, pred_list)
        else:
            return pred_list

    def _process_overlap(self, text: str, list_ret: list) -> list:
        """
        处理重叠的问题
        1.完全包含的关系，保留最长的
        2.不完全重叠，保留靠前的
        :param text:
        :param list_ret:
        :return:
        """
        # 删除完全被包含的元素
        overlap_cache = []
        for i in range(len(list_ret)):
            start = list_ret[i][0]
            end = list_ret[i][1]
            skip_mark = False
            for j in range(len(list_ret)):
                if i == j:
                    continue
                if start >= list_ret[j][0] and end <= list_ret[j][1]:
                    skip_mark = True
                    break
            if not skip_mark:
                overlap_cache.append(list_ret[i])
                # print(list_ret[i])
        # 删除和前面元素重叠的部分
        ret = []
        for i in range(len(overlap_cache)):
            # 如果我是第一个直接跳过
            if len(ret) == 0:
                ret.append(overlap_cache[i])
                continue
            if overlap_cache[i][0] > ret[-1][1]:
                ret.append(overlap_cache[i])
            else:
                continue
        return ret

        pass

    def _process_comb(self, text: str, pred_list: List[AreaPrediction]) -> List[AreaPrediction]:
        """
        对地址序列进行组装
        0. 数据结构转换为预测结果类型
        1. 对相邻的前后两个列表进行组合枚举
        2. 判断每一个枚举是否能够形成组合关系，
        :param text:
        :param pred_list:
        :return:
        """
        ret = []
        if len(pred_list) <= 1:
            return pred_list
        last_pred = pred_list[0]
        for i in range(1, len(pred_list)):
            cur_pred = pred_list[i]
            if self._can_merge4text(last_pred, cur_pred):
                area_can = False
                for j in range(len(last_pred.area_list)):
                    if area_can:
                        break
                    area_a = last_pred.area_list[j]
                    for k in range(len(cur_pred.area_list)):
                        area_b = cur_pred.area_list[k]
                        can, area_new = self._can_merge4area(area_a, area_b)
                        if can:
                            area_can = True
                            last_pred.area_list = [area_new]
                            break
                    if area_can:
                        break
                if area_can:
                    if self._is_empty(last_pred.prov_text):
                        last_pred.prov_text = cur_pred.prov_text
                        last_pred.prov_pos = cur_pred.prov_pos
                    if self._is_empty(last_pred.city_text):
                        last_pred.city_text = cur_pred.city_text
                        last_pred.city_pos = cur_pred.city_pos
                    if self._is_empty(last_pred.area_text):
                        last_pred.area_text = cur_pred.area_text
                        last_pred.area_pos = cur_pred.area_pos
                    continue
            ret.append(last_pred)
            last_pred = cur_pred
        ret.append(last_pred)
        return ret

    def _is_empty(self, text: str) -> bool:
        return text is None or text == ''

    def _can_merge4area(self, area_a: Area, area_b: Area):
        """
        判断两个区域信息是否可以合并
        :param area_a:
        :param area_b:
        :return:
        """
        text_a = '{}{}{}'.format(area_a.prov, area_a.city, area_a.area)
        text_b = '{}{}{}'.format(area_b.prov, area_b.city, area_b.area)

        if text_a in text_b:
            return True, area_b
        if text_b in text_a:
            return True, area_a
        return False, None

    def _can_merge4text(self, pred_a: AreaPrediction, pred_b: AreaPrediction):
        """
        判断省市区的描述信息是否重复，比如都描述了xx省，则不适宜合并
        :param pred_a:
        :param pred_b:
        :return:
        """
        if not self._is_empty(pred_a.prov_text) and not self._is_empty(pred_b.prov_text):
            return False
        if not self._is_empty(pred_a.city_text) and not self._is_empty(pred_b.city_text):
            return False
        if not self._is_empty(pred_a.area_text) and not self._is_empty(pred_b.area_text):
            return False
        return True
        pass


def test_alias_builder():
    loader = AdcodeLoader()
    area_list = loader.load()
    alias_builder = AliasBuilder()
    for area in area_list:
        text, level = alias_builder._find_name(area)
        mark = False
        for k in ['自治', '盟', '旗']:
            if k in text:
                mark = True
        if mark:
            print(area, alias_builder.build_alias(area))
