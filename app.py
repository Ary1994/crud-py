from flask import render_template, request, redirect;
from flask import Flask;
from flaskext.mysql import MySQL;
from datetime import datetime;

app= Flask(__name__);
mysql = MySQL() 
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = '' 
app.config['MYSQL_DATABASE_DB'] = 'sistema22538' 
mysql.init_app(app)

@app.route('/')
def main():
    sql="SELECT * FROM empleados"
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute(sql);
    empleados=cursor.fetchall();
    #print(empleados);
    conn.commit();
    return render_template('empleados/index.html', emple = empleados);

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/storage', methods=['POST'])
def storage():
    nombre= request.form['nombreValue']
    email= request.form['emailValue']
    file=request.files['fileValue']
    nuevoNombreImg='';
    if file.filename !='':
        now=datetime.now();
        moment=now.strftime('%Y%M%S');
        nuevoNombreImg= moment +"-"+file.filename;
        file.save('uploads/'+nuevoNombreImg);


    sql="INSERT INTO `empleados` (`id`, `nombre`, `email`, `imagen`) VALUES (NULL, %s, %s, %s);";
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute(sql,(nombre,email,nuevoNombreImg));
    #print(file)
    conn.commit();
    return redirect('/');

@app.route('/destroy/<int:id>')
def destroy (id):
    sql="DELETE FROM empleados WHERE id=%s";
    conn=mysql.connect();
    cursor=conn.cursor();
    cursor.execute(sql,(id));
    conn.commit();
    return redirect('/');


if __name__=='__main__':
    app.run(debug=True);