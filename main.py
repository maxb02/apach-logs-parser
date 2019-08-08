from collections import Counter
import re
from flask import Flask
from flask import render_template
from flask import request



app = Flask(__name__)

###############################################
DEFAULT_ADDRESSES_QUANTITY = 10
DEFAULT_REQUEST_QUANTITY = 100
###############################################

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        addresses_quantity = int(request.form['addresses_quantity'])
        requests_quantity = int(request.form['requests_quantity'])
        file = request.files['file'].read()
        txt = str(file.decode('utf-8'))

        pattern = r'\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}'
        ip_addresses = re.findall(pattern, txt)

        result = Counter(ip_addresses).most_common(addresses_quantity)
        ban = []

        for ip, requests_number in result:
            if requests_number >= requests_quantity:
                ban.append({'ip': ip, 'requests_number': requests_number})

        return render_template('index.html',
                               ip_addresses=ban,
                               addresses_quantity=addresses_quantity,
                               requests_quantity=requests_quantity)
    else:
        return render_template('index.html',
                               addresses_quantity=DEFAULT_ADDRESSES_QUANTITY,
                               requests_quantity=DEFAULT_REQUEST_QUANTITY)


if __name__ == '__main__':
    app.run(debug=True)
