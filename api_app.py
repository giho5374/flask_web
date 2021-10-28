import requests
from flask import Blueprint,request,url_for
from config import *
import xmltodict,json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

api = Blueprint('api',__name__)
region_code = pd.read_csv('static/region_code.csv',encoding = 'utf-8',index_col=0)
region_dict = region_code.to_dict()['법정동코드']
@api.route('/api/statics_search_service')
def statics_search_service():
    url = 'http://openapi.reb.or.kr/OpenAPI_ToolInstallPackage/service/rest/RealEstateTradingSvc' \
          '/getRealEstateTradingCountTypeSizeYear '
    start = request.args.get('start')
    end = request.args.get('end')
    region = request.args.get('region',default='11000')
    tradingtype = request.args.get('tradingtype',default='01')
    params = {'serviceKey': DECODE, 'startyear': start, 'endyear': end, 'region': region, 'tradingtype': tradingtype}
    response = requests.get(url,params=params)
    return response.content

@api.route('/api/apartment_trade')
def apartment_trade():
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
    lawd_cd = request.args.get('LAWD_CD')# 지역코드
    if not lawd_cd.isdecimal():
        lawd_cd = region_dict[lawd_cd]
    deal_ymd = request.args.get('DEAL_YMD') #월단위
    params = {'serviceKey': DECODE, 'LAWD_CD': lawd_cd, 'DEAL_YMD': deal_ymd}
    response = requests.get(url,params=params)
    result = json.loads(json.dumps(xmltodict.parse(response.text), ensure_ascii=False))['response']['body']['items']
    if result:
        result = pd.DataFrame().from_dict(result['item'])
        result['일'] = result['일'].astype('int')
        result.sort_values('일',inplace=True)
        style_res = result.style.set_properties(**{'background-color':'white','border':'0.1px solid black','font-size':'15px'})
        return f'''<a href='{url_for("api.apartment_trade")}?LAWD_CD={lawd_cd}&DEAL_YMD={(datetime.strptime(deal_ymd,"%Y%m")-relativedelta(months=1)).strftime("%Y%m")}'>이전</a>
        <a href='{url_for("api.apartment_trade")}?LAWD_CD={lawd_cd}&DEAL_YMD={(datetime.strptime(deal_ymd,"%Y%m")+relativedelta(months=1)).strftime("%Y%m")}'>다음</a>
               ''' + style_res.hide_index().render()

    return '<h1>There is No trade in that month</h1>'\
           f'''<a href='{url_for("api.apartment_trade")}?LAWD_CD={lawd_cd}&DEAL_YMD={(datetime.strptime(deal_ymd,"%Y%m")-relativedelta(months=1)).strftime("%Y%m")}'>이전</a>
        <a href='{url_for("api.apartment_trade")}?LAWD_CD={lawd_cd}&DEAL_YMD={(datetime.strptime(deal_ymd,"%Y%m")+relativedelta(months=1)).strftime("%Y%m")}'>다음</a>
               '''


