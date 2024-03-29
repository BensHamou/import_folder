from .models import Setting
import psycopg2

def connect_database():
    port = Setting.objects.get(name='port').value
    host = Setting.objects.get(name='host').value
    dbname = Setting.objects.get(name='dbname').value
    user = Setting.objects.get(name='user').value
    password = Setting.objects.get(name='password').value
    conn_string = ("host="+host+" port="+port+" dbname="+dbname+" user="+user+" password="+password)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return cursor

def execute_query(query, params=None):
    with connect_database() as cursor:
        cursor.execute(query, params)
        records = cursor.fetchall()
    return records

def getFournisseurId(supplier_name):
    query = """SELECT id, name FROM res_partner WHERE name ILIKE %s AND supplier = true AND state = 'validate' LIMIT 5;"""
    params = ('%' + supplier_name.upper() + '%',)
    return execute_query(query, params)

def getProductId(product_name):
    query = """SELECT id, name, template_code FROM product_template he WHERE template_code ILIKE %s AND company_id = 8 LIMIT 5;"""
    params = ('%' + product_name.upper() + '%',)
    return execute_query(query, params)
