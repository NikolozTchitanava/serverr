from flask import Flask, jsonify, render_template
import random
import time
import threading

app = Flask(__name__)

data_storage = {
    'numbers': [],
    'timestamps': [],
    'averages': []
}

def calculate_averages(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def generate_numbers():
    while True:
        number = random.randint(1,10)
        timestamp = time.strftime('%H:%M:%S', time.localtime()) 
        data_storage['numbers'].append(number)
        data_storage['timestamps'].append(timestamp)

        if len(data_storage['numbers']) > 50:
            data_storage['numbers'].pop(0)
            data_storage['timestamps'].pop(0)
            
    
        last_six_numbers = data_storage['numbers'][-6:]
        current_average = calculate_averages(last_six_numbers)
        data_storage['averages'].append(current_average)

        time.sleep(5)

threading.Thread(target=generate_numbers).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
  
    overall_average = calculate_averages(data_storage['averages'])
    return jsonify({
        'numbers': data_storage['numbers'],
        'timestamps': data_storage['timestamps'],
        'current_average': data_storage['averages'][-1] if data_storage['averages'] else 0,
        'overall_average': overall_average
    })

if __name__ == '__main__':
    app.run(debug=True)
