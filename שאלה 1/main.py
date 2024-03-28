from flask import Flask, request, render_template
import patients
import vaccination_info
import corona_information
from sql_connection import *

app = Flask('main', template_folder='')

def update_corona_info(data, id0, flag):
    t = []
    if 'vacc1' in data:
        t.append(data["vacc1"])
        t.append(data["prod1"])
        if 'vacc2' in data:
            t.append(data["vacc2"])
            t.append(data["prod2"])
            if 'vacc3' in data:
                t.append(data["vacc3"])
                t.append(data["prod3"])
                if 'vacc4' in request.values:
                    t.append(data["vacc4"])
                    t.append(data["prod4"])
        t.append(data["pos_res"])
        t.append(data["recovery"])
    for i in t:
        if i == '':
            return 1
    if flag:
        v = insert_vaccination(id0, t)
    else:
        v = set_vaccination(id0, t)
    return 0


@app.route('/create_new_patient', methods=['POST'])
def create_new_patient():
    p = insert_patient(request.values["name"],
                       request.values["id"],
                       request.values["address"],
                       request.values["bdate"],
                       request.values["tel"],
                       request.values["phone"])
    res = update_corona_info(request.values, p.id, True)
    if p == 0:
        return 'לקוח בעל תעודת זהות זהה כבר קיים'
    if p == 1 or res == 1:
        return 'אחד או יותר מהנתונים לא תקינים'
    return f'{p.name}, {p.id}'

@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    string_patient = request.values.__getitem__('textarea1')
    start_id = string_patient.rfind(' ') + 1
    id0 = string_patient[start_id:len(string_patient)]
    delete_p(id0)
    delete_v(id0)
    return "לקוח הוסר בהצלחה"


@app.route('/set_patient', methods=['POST'])
def set_patient():
    id0 = request.values["id"]
    p = set_patient_sql(request.values["name"],
                       id0,
                       request.values["address"],
                       request.values["bdate"],
                       request.values["tel"],
                       request.values["phone"])
    res = update_corona_info(request.values, id0, False)
    if p == 1 or res == 1:
        return 'אחד או יותר מהנתונים לא תקינים'
    if p == 2:
        return 'תעודת זהות לא זהה לתעודת זהות של הפציינט אותו ברצונך לעדכן'
    return f'{p.name}, {p.id}'


def create_str(v):
    flag = False
    corona_str = '<br/>נתוני קורונה:'
    i = 1
    while v.vacc_list.__getitem__(0) != '':
        flag = True
        date = v.vacc_list.pop(0)
        prod = v.vacc_list.pop(0)
        corona_str += f'<br/>מועד חיסון {i}: {date}<br/>יצרן חיסון {i}: {prod}<br/>'
        i += 1
    if flag:
        corona_str += f'<br/>מועד תוצאה חיובית: {v.pos_res}<br/>מועד החלמה: {v.recovery_date}<br/>'
    else:
        corona_str = ''
    return corona_str

@app.route('/show_data', methods=['POST', 'GET'])
def show_data():
    string_patient = request.values.__getitem__('textarea1')
    start_id = string_patient.rfind(' ') + 1
    id0 = string_patient[start_id:len(string_patient)]
    p = find_patient(id0)
    v = find_corona_info(id0)
    print('v', v == 0)
    if v != 0:
        print('v', v.vacc_list)
        corona_str = create_str(v)
    else:
        corona_str = ''
    return (f'פרטי פציינט:<br/>שם: {p.name}<br/> תעודת זהות: {p.id}'
            f'<br/>כתובת: {p.address}<br/>תאריך לידה: {p.bdate}'
            f'<br/> טלפון: {p.tel}<br/>פלאפון: {p.phone}') + corona_str




# Decorator defines a route
# http://localhost:5000/
@app.route('/')
def index():
    patient_list = execute_patients()
    new_list = []
    count = 0
    for r in patient_list:
        count += 1
        new_list.append({'id': count, 'info': f'{r.__getitem__(0)}, '
                                              f'{r.__getitem__(1)}'})
    return render_template('index.html', to_send=new_list)

if __name__ == '__main__':
    create()
    app.run()
