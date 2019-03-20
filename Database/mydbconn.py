from Auth import app
import pymssql

# host = "201.49.223.4" # antigo
# host = "10.0.1.202" # prod local
host = "138.36.216.242" #prod 
user = "sa"
# ukey = "6wraTEK4PDe6"
ukey = "#Oc0rr3-!RupTur@*"
sche = "DADOS_TST"


def get_conn():
    return pymssql.connect(host, user, ukey, sche)

def db_execute(statement, params):
    conn = get_conn()
    with conn.cursor() as cursor:
        try:
            ret = cursor.execute(statement, params)
            conn.commit()
        except:
            return False
        finally:
            conn.close()

    return ret

def db_execute_scalar(statement, params):
    conn = get_conn()
    results = []
    with conn.cursor() as cursor:
        try:
            cursor.execute(statement, params)
            rows = cursor.fetchall()
            if rows:
                columns = [column[0].lower() for column in cursor.description]
                
                for row in rows:
                    b = []
                    for a in row:
                        if isinstance(a, str):
                            a = str(a).strip()
                        b.append(a)

                    results.append(dict(zip(columns, b)))
            
            conn.commit()
        except:
            return False
        finally:
            conn.close()

    return results
    
def error_handler(msgstate, severity, srvname, procname, line, msgtext):
    print("error_handler: msgstate = %d, severity = %d, procname = '%s', "
          "line = %d, msgtext = '%s'" % (msgstate, severity, procname,
                                         line, msgtext))