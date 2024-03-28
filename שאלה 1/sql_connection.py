import sqlite3
import patients
import corona_information
#this function creates client and files tables
def create():
    try:
        f = open('corona.db')
    except:
        conn = sqlite3.connect('corona.db')
        c = conn.cursor()
        c.execute('CREATE TABLE patients (name txet, id text, address text, bdate date, tel text, phone text, primary key(id))')
        c.execute('CREATE TABLE vaccination (id txet, first_vacc date, first_prod text, second_vacc date, second_prod text, third_vacc date, third_prod text, fourth_vacc date, fourth_prod text, pos_res date, recovery_date, primary key(id))')
        conn.close()

def empty(data):
    return data == ""

def not_valid_id(data: str):
    return len(data) != 9 or not data.isnumeric()

def not_number(data):
    return not data.isnumeric()

#this function insert new client with new uuid, name, and last_seen
def insert_patient(name, id0, address, bdate, tel, phone):
    if empty(name) or not_valid_id(id0) or empty(address) or empty(bdate) or not_number(tel) or not_number(phone):
        return 1
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    p1 = find_patient(id0)
    if p1 != 0:
        return 0
    p = patients.Patient(name, id0, address, bdate, tel, phone)
    patient = [(name, id0, address, bdate, tel, phone)]
    c.executemany("INSERT INTO patients VALUES(?, ?, ?, ?, ?, ?)", patient)
    conn.commit()
    c.close()
    conn.close()
    return p

def find_patient(id) -> patients.Patient:
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    query = c.execute("SELECT * FROM patients WHERE id = ?", (id, ))
    try:
        results = query.fetchall().__getitem__(0)
    except:
        return 0
    c.close()
    conn.close()
    p = patients.Patient(results.__getitem__(0), results.__getitem__(1), results.__getitem__(2), results.__getitem__(3), results.__getitem__(4), results.__getitem__(5))
    return p


def find_corona_info(id) -> corona_information.Corona_info:
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    query = c.execute("SELECT * FROM vaccination WHERE id = ?", (id, ))
    try:
        results = query.fetchall().__getitem__(0)
        v = corona_information.Corona_info(results.__getitem__(0),
                                           [results.__getitem__(1), results.__getitem__(2), results.__getitem__(3),
                                            results.__getitem__(4), results.__getitem__(5), results.__getitem__(6),
                                            results.__getitem__(7), results.__getitem__(8)], results.__getitem__(9), results.__getitem__(10))
    except:
        v = 0
    c.close()
    conn.close()
    return v


def set_patient_sql(name, id0, address, bdate, tel, phone):
    if empty(name) or not_valid_id(id0) or empty(address) or empty(bdate) or not_number(tel) or not_number(phone):
        return 1
    p = find_patient(id0)
    if not p:
        return 2
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    c.execute("UPDATE patients "
                        "SET name = ?, "
                            "address = ?, "
                            "bdate = ?, "
                            "tel = ?, "
                            "phone = ? "
                        "WHERE id = ?", (name, address, bdate, tel, phone, id0))
    conn.commit()
    c.close()
    conn.close()
    p = patients.Patient(name, id0, address, bdate, tel, phone)
    return p


def delete_p(id0):
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    c.execute("DELETE from vaccination WHERE id = ?", (id0, ))
    conn.commit()
    c.close()
    conn.close()


def delete_v(id0):
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    c.execute("DELETE from patients WHERE id = ?", (id0,))
    conn.commit()
    c.close()
    conn.close()


def create_vacc_list(list_info, id):
    vacc_list = []
    len_t = len(list_info)
    i = 0
    empty = 0
    if len_t > 2:
        vacc_list.append(list_info.__getitem__(i))
        vacc_list.append(list_info.__getitem__(i + 1))
        if len_t > 4:
            i += 2
            vacc_list.append(list_info.__getitem__(i))
            vacc_list.append(list_info.__getitem__(i + 1))
            if len_t > 6:
                i += 2
                vacc_list.append(list_info.__getitem__(i))
                vacc_list.append(list_info.__getitem__(i + 1))
                if len_t > 8:
                    i += 2
                    vacc_list.append(list_info.__getitem__(i))
                    vacc_list.append(list_info.__getitem__(i + 1))
                else:
                    empty = 2
            else:
                empty = 4
        else:
            empty = 6
        i += 2
    else:
        empty = 8
    j = 0
    while j < empty:
        vacc_list.append('')
        j += 1
    v = corona_information.Corona_info(id, vacc_list, list_info.__getitem__(i), list_info.__getitem__(i + 1))
    return vacc_list, v

#this function insert new file with id of client, file name and file path
def set_vaccination(id, *vacc_info):
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    list_info = []
    if len(vacc_info) > 1:
        list_info = vacc_info.__getitem__(0)
    else:
        list_info.append('')
        list_info.append('')
    vacc_list, v = create_vacc_list(list_info, id)
    vacc_list.append(v.pos_res)
    vacc_list.append(v.recovery_date)
    vacc_list.append(id)
    corona = [tuple(vacc_list)]
    c.execute("UPDATE vaccination "
                        "SET first_vacc = ?, "
                            "first_prod = ?, "
                            "second_vacc = ?, "
                            "second_prod = ?, "
                            "third_vacc = ?, "
                            "third_prod = ?, "
                            "fourth_vacc = ?, "
                            "fourth_prod = ?, "
                            "pos_res = ?, "
                            "recovery_date = ?"
                        "WHERE id = ?", (vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0)))
    conn.commit()
    c.close()
    conn.close()
    return v


def insert_vaccination(id, *vacc_info):
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    list_info = vacc_info.__getitem__(0)
    if len(list_info) == 0:
        list_info.append('')
        list_info.append('')
    vacc_list, v = create_vacc_list(list_info, id)
    vacc_list.insert(0, id)
    vacc_list.append(v.pos_res)
    vacc_list.append(v.recovery_date)
    c.execute("UPDATE vaccination "
                        "SET first_vacc = ?, "
                            "first_prod = ?, "
                            "second_vacc = ?, "
                            "second_prod = ?, "
                            "third_vacc = ?, "
                            "third_prod = ?, "
                            "fourth_vacc = ?, "
                            "fourth_prod = ?, "
                            "pos_res = ?, "
                            "recovery_date = ?"
                        "WHERE id = ?", (vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0), vacc_list.pop(0)))
    conn.commit()
    c.close()
    conn.close()
    return v


#this function execute all clients (to insert them to client_list)
def execute_patients():
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    query = c.execute("SELECT * FROM patients")
    results = query.fetchall()
    c.close()
    conn.close()
    return results

#this function execute all files (to insert them to file_list)
def execute_files():
    conn = sqlite3.connect('corona.db')
    c = conn.cursor()
    query = c.execute("SELECT * FROM files")
    results = query.fetchall()
    c.close()
    conn.close()
    return results
