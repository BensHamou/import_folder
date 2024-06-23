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
    # query = """SELECT pt.id, pt.name, pt.template_code 
    #             FROM product_template pt
    #             LEFT JOIN product_template_company_allowed_rel ptc on pt.id = ptc.template_id
    #             WHERE pt.template_code ILIKE %s AND (pt.company_id = 8 OR ptc.company_id = 8) LIMIT 5;"""
    query = """SELECT pp.id, pp.name_template, pp.default_code 
                FROM product_product pp
                LEFT JOIN product_template pt on pt.id = pp.product_tmpl_id
                LEFT JOIN product_template_company_allowed_rel ptc on pt.id = ptc.template_id
                WHERE pp.default_code ILIKE %s AND (pt.company_id = 8 OR ptc.company_id = 8) LIMIT 5;"""
    params = ('%' + product_name.upper() + '%',)
    return execute_query(query, params)
