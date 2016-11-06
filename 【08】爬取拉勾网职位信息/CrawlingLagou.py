import requests
from openpyxl import Workbook
import time
import random

session = requests.session()


def get_json(url, page, lang_name):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Referer': 'https://www.lagou.com/jobs/list_Python%E5%B7%A5%E7%A8%8B%E5%B8%88?px=default&city=%E4%B8%8A%E6%B5%B7'
    }
    data = {'first': 'true', 'pn': page, 'kd': lang_name}
    json = session.post(url, headers=header, data=data, verify=False).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i['positionName'])  # 岗位名称
        info.append(i['companyFullName'])  # 公司名称
        info.append(i.get("education", ""))  # 学历
        info.append(i.get("salary", ""))  # 薪资
        info.append(i.get("workYear", ""))  # 工作年限
        info.append(i.get('city', ""))  # 城市
        info.append(','.join(i.get('businessZones')) if i.get('businessZones') else "无")  # 工作地址
        info.append(i.get("financeStage", ""))  # 公司上市情况
        info.append(i.get("companySize", ""))  # 公司人数规模
        info.append(i.get("industryField", ""))  # 行业类型
        info.append(i.get("positionAdvantage", ""))  # 公司文化
        info.append(','.join(i.get("companyLabelList")) if i.get("companyLabelList", "") else "无")  # 公司福利
        info_list.append(info)
    return info_list


def main():
    lang_name = input('请输入职位名称：')
    page = 1
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    info_result = []
    while True:
        time.sleep(random.randint(5, 15))
        info = get_json(url, page, lang_name)
        if not info:
            break
        info_result = info_result + info
        page += 1
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    ws1.append(["岗位名称", "公司名称", "学历", "薪资", "工作年限", "城市", "工作地址", "公司上市情况", "公司人数规模", "行业类型", "公司文化", "公司福利"])
    for row in info_result:
        ws1.append(row)
    wb.save(r'D:\职位信息.xlsx')


if __name__ == '__main__':
    main()
