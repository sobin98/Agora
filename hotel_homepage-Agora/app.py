

from flask import Flask, request, render_template, flash, redirect, url_for, session, current_app

import pymysql # flask에서 mysql 접속 용도

import hashlib # salting한 값을 해쉬함수에 넣어 암호화

app = Flask(__name__)
app.secret_key = b''
host_ip=''
db_passwd=''
db = pymysql.connect(host=host_ip, port=3306, user='dbadmin', passwd=db_passwd, db='hotel_db', charset='utf8')
cursor = db.cursor()

@app.route('/', methods=['GET'])
def index():
    print(session)
    username = session.get('username', None)
    
    if 'username' in session:
    	return render_template('/index.html', username=username, session=session)
	
    return render_template('/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':
		db = pymysql.connect(host=host_ip, port=3306, user='dbadmin', passwd=db_passwd, db='hotel_db', charset='utf8')
		cursor = db.cursor()
		
		# login시 입력받은 form 정보를 dict type으로 login_info에 저장
		login_info = request.form
		userid = login_info['username'] # username은 html form에서 가져온 data
		passwd = login_info['password'] # password html form에서 가져온 data
		sql = "SELECT * FROM staff_info WHERE staff_id=%s"
		rows_count = cursor.execute(sql, userid)
		print(rows_count)

		if rows_count > 0:
			user_info = cursor.fetchone()
			print("user info: ", user_info)
			is_pw_correct = bcrypt.checkpw(passwd.encode('utf-8'), user_info[1].encode('utf-8'))
			print("password check:", is_pw_correct)
			
			if not is_pw_correct:
				print("암호 틀림")
			else:
				# session을 dictionary type으로 저장한다.
				session['username'] = login_info['username']
		else:
			print('User does not exist')
		db.close()
		return redirect(url_for('index'))
	return render_template('login/login.html')

@app.route('/signout')
def signout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	return render_template('login/signup.html')

@app.route('/staff_info')
def staff_info():
	db = pymysql.connect(host=host_ip, port=3306, user='dbadmin', passwd=db_passwd, db='hotel_db', charset='utf8')
	cursor = db.cursor()
	sql = "SELECT staff_id, staff_kor_last_name, staff_kor_first_name, staff_title, staff_rank, staff_join_date, staff_birth, staff_cell_no FROM staff_info"
	cursor.execute(sql)
	data_list = cursor.fetchall()
	db.close()
	return render_template('/staff_info.html', data_list = data_list)

@app.route('/staff_Mgt', methods=['GET', 'POST'])
def staffMgt():
	db = pymysql.connect(host=host_ip, port=3306, user='dbadmin', passwd=db_passwd, db='hotel_db', charset='utf8')
	cur = db.cursor()
	sql = "SELECT staff_id, staff_kor_last_name, staff_kor_first_name FROM staff_info"
	cur.execute(sql)
	data_list = cur.fetchall()

	sql2 = "SELECT room_no FROM room"
	cur.execute(sql2)
	data_list2 = cur.fetchall()


	if request.method =='POST':
		register_info = request.form
		name = register_info['staff_name']
		room = register_info['room_name']

		sql3 = """
			INSERT INTO staff_mgt (staff_task_session, staff_rating)
			VALUES (%s, %s);
		"""
		cur.execute(sql3, (name, room))
		db.commit()


	sql4 = "SELECT staff_task_session, staff_rating FROM staff_mgt"
	cur.execute(sql4)
	data_list3 = cur.fetchall()
	db.close()
	return render_template('/staffMgt.html', data_list = data_list, data_list2 = data_list2, data_list3 = data_list3)

@app.route('/staff_register', methods=['GET', 'POST'])
def staff_register():
	if request.method == 'POST':
		db = pymysql.connect(host=host_ip, port=3306, user='dbadmin', passwd=db_passwd, db='hotel_db', charset='utf8')
		cursor = db.cursor()
		register_info = request.form
		#userid = register_info['staff_id'] # staff_id를 html form에서 가져온 data
		hashed_pw = bcrypt.hashpw(register_info['staff_id'].encode('utf-8'), bcrypt.gensalt()) # password html form에서 가져온 data를 암호화하여 변수에 저장
		sql = """
			INSERT INTO staff_info 
			(staff_id, staff_pw, staff_title, staff_rank, staff_kor_last_name, staff_kor_first_name, staff_eng_last_name, staff_eng_first_name, staff_birth, staff_join_date, staff_cell_no)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
		"""
		cursor.execute(sql, (register_info['staff_id'], hashed_pw, register_info['staff_title'], register_info['staff_rank'], register_info['staff_kor_last_name'], register_info['staff_kor_first_name'], register_info['staff_eng_last_name'], register_info['staff_eng_first_name'], register_info['staff_birth'], register_info['staff_join_date'], register_info['staff_cell_no']))
		db.commit()
		db.close()

		return render_template('login/staff_register.html')
	return render_template('login/login.html')

@app.route('/about-us')
def aboutus():
	return render_template('/about-us.html')

@app.route('/rooms')
def rooms():
	return render_template('/rooms.html')

@app.route('/news')
def news():
	return render_template('/news.html')

@app.route('/contact')
def contact():
	return render_template('/contact.html')

@app.route('/services')
def services():
	return render_template('/services.html')

@app.route('/agora')
def agora():
	username = session.get('username', None)
	if 'username' in session:
		return render_template('/agora.html', username=username, session=session)
	return render_template('/agora.html')

@app.route('/add_staff')
def add_staff():
	return render_template('/add_staff.html')

@app.route('/res_status')
def res_status():
	db = pymysql.connect(host=host_ip, port=3306, user='dbadmin', passwd=db_passwd, db='hotel_db', charset='utf8')
	cursor = db.cursor()
	sql = "SELECT * FROM reservation"
	cursor.execute(sql)
	res_list = cursor.fetchall()
	db.close()
	return render_template('res_status.html', res_list = res_list)

@app.route('/mypage')
def mypage():
    return render_template('/mypage.html')



#test용으로 미리 db에 만들어놓기 sobin987,1234
@app.route('/login',methods=['GET','POST'])
def login():
     if request.method=='POST':
        db.connect()
        sql='SELECT * FROM customer_info where cust_id=%s'
        rows_count=cursor.execute(sql,(request.form['cust_id']))
        
        if rows_count>0:
            user_info=cursor.fetchone()
            print(user_info)#확인용도
            session['cust_id'] = user_info[0]
            
        else:
            print('로그인실패')
        return redirect(url_for('chg_info'))
     return render_template('/login.html')

@app.route('/chg_info',methods=['GET','POST'])
def chg_info():
#    sql1='select * from customer_info where cust_id=%s'
 #   cursor.execute(sql1,(session['cust_id']))
    user=session['cust_id']
    db.connect()
    sql='select * from customer_info where cust_id=%s'
    rows_count=cursor.execute(sql,(user))
    if rows_count>0:
        user_info=cursor.fetchone()
    
    if request.method=='POST':
        
        db.connect()       
            
        if not request.form['cust_cell_no']:
            flash('핸드폰 번호를 입력해주세요.')
        elif not request.form['cust_pw'] :
            flash('비밀번호를 입력해주세요.')
        elif request.form['cust_pw'] != request.form['cust_pw2']:
            flash('비밀번호가 일치하지 않습니다.')
#        elif 500에러뜨면
#            flash('형식에 맞게 입력해주세요')
        else:
            sql2=''' UPDATE customer_info SET cust_pw=%s,cust_eng_first_name=%s,cust_eng_last_name=%s,cust_country=%s,cust_region=%s,
cust_cell_ccc=%s,cust_cell_no=%s,cust_card_type=%s,cust_card_no=%s,cust_card_vlddate=%s where cust_id=%s'''
            rows_count1=cursor.execute(sql2,(request.form['cust_pw'],request.form['cust_eng_first_name'],request.form['cust_eng_last_name'],
                                        request.form['cust_country'],request.form['cust_region'],request.form['cust_cell_ccc'],request.form['cust_cell_no'],
                                         request.form['cust_card_type'],request.form['cust_card_no'],request.form['cust_card_vlddate']+'-01',user))
       
        #밑에 세줄을 콘솔창에서 확인해볼려고 만들어놈
            if rows_count1>0:
                user_new_info=cursor.fetchone()
                
                db.commit()
                db.close()
            return ('개인정보 수정이 완료되었습니다.')
        return redirect(url_for('chg_info'))
    return render_template('/chg_info.html',user=user,kor_name=user_info[2]+user_info[3],efirname=user_info[5],elasname=user_info[4],
                           birthday=user_info[6],country=user_info[7],region=user_info[8],cell_no=user_info[10],
                           card_no=user_info[12],vlddate=user_info[13])#기존정보들 입력하려고 사용 html에서 변수확인
    
if __name__ == '__main__':
	app.run()
 