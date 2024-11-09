from flask import Flask ,render_template,request,redirect,url_for,send_file

import Alg

from Alg import Algos
app = Flask(__name__,template_folder="templates")
import matplotlib as plt
import pandas as pd
import locale
import io
import xlsxwriter
import datetime
from datetime import datetime, date

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        data=request.form
        portfolio_size=request.form.get('portfolio')
        algo=request.form.get('algo')
        print("requested data",portfolio_size,algo)

        return redirect(url_for('result',portfolio_size=portfolio_size,algo=algo))
        
    return render_template("index.html")

img_src=""
data=""
name=""
@app.route("/result")
def result():
    global data,name
    portfolio_size=request.args.get('portfolio_size')
    algo=request.args.get('algo')
    Alg=Algos(int(portfolio_size))
    result,img_path=Alg.Nifty50EqualW(SaveExcel=True,Analyzer=True)
    data=result
    name="AlgoTrade"+str(date.today()).replace("-","")+str(datetime.now().time()).replace(":","")
    print("result",result)
    locale.setlocale(locale.LC_MONETARY,"en_IN")
    amount=locale.currency(int(portfolio_size), grouping=True)
    table_html = result.to_html(classes='table table-striped', index=False)
    return render_template('results.html',portfolio_size=amount,algo=algo,img=img_path,table=table_html)


@app.route("/download")
def download():
    df=data
    print(df)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    output.seek(0)  # Rewind the buffer
    
    # Send the Excel file as a download
    return send_file(output, as_attachment=True, download_name=f'{name}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route("/test")
def test():
    return render_template("index_test.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)