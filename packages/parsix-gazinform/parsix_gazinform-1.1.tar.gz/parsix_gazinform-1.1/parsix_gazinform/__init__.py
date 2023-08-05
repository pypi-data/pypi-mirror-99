import re
import sys

def parsix(input_str: str):
    try:
        input_str = input_str.strip()[::-1]
        reg_res = re.findall(r" .*=.* \|(?!\\)(.*)$", input_str) #ищем подстроки между | учитывая экранирование
        if not reg_res:
            return {}
        sub_str = re.findall(r"(.*?)\|(?!\\)", reg_res[0]+'|')
        sub_str = [k[::-1] for k in sub_str[::-1]]

        if len(sub_str) != 7:
            return {}

        key_values = re.findall(r"(.*?)(?!\\)=(.[^ =/|]+?) ", input_str) #отлично и быстро ищет пары ключ=значение. требует обратного порядка файла

        result_voc = {}

        for i, v in enumerate(sub_str):
            result_voc.update({"param_{}".format(i+1): v})

        for i in key_values[::-1]:
            result_voc.update({i[1][::-1]: i[0][::-1]})
    except Exception as e:
        print(e, file=sys.stderr)
        return {}
    return result_voc
