import requests
from flask import Blueprint,request
from config import *

url = 'http://openapi.reb.or.kr/OpenAPI_ToolInstallPackage/service/rest/RealEstateTradingSvc' \
      '/getRealEstateTradingCountTypeSizeYear '

api = Blueprint('api',__name__)

@api.route('/api/result')
def result():
    start = request.args.get('start')
    end = request.args.get('end')
    region = request.args.get('region',default='11000')
    tradingtype = request.args.get('tradingtype',default='01')
    params = {'serviceKey': DECODING, 'startyear': start, 'endyear': end, 'region': region, 'tradingtype': tradingtype}
    response = requests.get(url,params=params)
    return response.content