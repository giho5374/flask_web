from flask import Blueprint,render_template,request,redirect
import pandas as pd

est_app = Blueprint('est_app',__name__)

@est_app.route('/search', methods = ['POST','GET'])
def search():
    if request.method == 'POST':
        city = request.form['city']
        date = request.form['date'].replace('-','')
        return redirect(f'/api/apartment_trade?LAWD_CD={city}&DEAL_YMD={date}')
    city_list = list(pd.read_csv('static/region_code.csv',index_col=0).index)
    return render_template('search.html',city_list = sorted(city_list))