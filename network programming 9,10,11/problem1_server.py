from flask import Flask, request
import csv
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def definition():
    data = request.get_data().decode('utf-8')
    definition = ''
    with open('problem1_csv.csv', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            key = line.split(",")[0]
            value = (',').join(line.split(",")[1:])
            if(key == data):
                definition = value
    f.close()
    return definition

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)