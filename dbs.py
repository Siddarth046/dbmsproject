from os import name
from MySQLdb import cursors
from MySQLdb.cursors import Cursor
import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'GDSiddu@3858'
app.config['MYSQL_DB'] = 'emp'
mysql = MySQL(app)


@app.route("/")
def f1():
    return render_template('home.html')


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        req = request.form
        username = req['username']
        password = req['password']
        email = req['email']
        cursor = mysql.connection.cursor()
        cursor.execute('select * from user where username=%s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exist'
        else:
            cursor.execute(
                "INSERT INTO user(username,password,email) VALUES (%s, %s,%s)", (username, password, email))
            mysql.connection.commit()
            msg = 'Successfully registerd'
            cursor.close()
            return redirect('/')
    elif request.method == 'POST':
        msg = 'Please fill out the form hg'
    return render_template('sign_up.html', msg=msg)


@app.route("/login", methods=['GET', 'POST'])
def f4():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        req = request.form
        username = req['username']
        password = req['password']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'select * from user where username=%s and password=%s', (username, password,))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Logged in successfully'
            return redirect('/')
        else:
            msg = 'Incorrect username/password'
            return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)


@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method =='POST' and 'username' in request.form and 'password' in request.form:
        req = request.form
        username = req['username']
        password = req['password']
        if(username=="Admin" and password=="12345"):
           return redirect('/add_data')
        else:
            msg="Incorrect Username/Password"
            return render_template('admin_login.html',msg=msg)
    return render_template('admin_login.html')

@app.route('/delete_data',methods=['GET', 'POST'])
def delete_data():
    if request.method=='POST':
        delete=request.form
        p_fname=delete['P_fname']
        p_lname=delete['P_lname']
        select_table=delete['select_table']
        cur=mysql.connection.cursor()
        # msg=''
        if(select_table=="PlayerInformation"):
            cur.execute('delete from player_information where p_fname=%s',(p_fname,))

        if(select_table=="BattingCareer"):
            cur.execute('delete from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s)',(p_fname,p_lname,))       
            
        if(select_table=="BattingCareerInTest"):
            cur.execute('delete from batt_test where bat_id=(select bat_id from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))
        
        if(select_table=="BattingCareerInOdi"):
            cur.execute('delete from batt_odi where bat_id=(select bat_id from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))

        if(select_table=="BattingCareerInT20"):
            cur.execute('delete from batt_t20 where bat_id=(select bat_id from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))
        
        if(select_table=="BattingCareerInIPL"):
            cur.execute('delete from batt_ipl where bat_id=(select bat_id from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))
        
        if(select_table=="BowlingCareer"): 
            cur.execute('delete from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s)',(p_fname,p_lname,))
        
        if(select_table=="BowlingCareerInTest"):
            cur.execute('delete from bowl_test where bowl_id=(select bowl_id from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))
        
        if(select_table=="BowlingCareerInOdi"):
            cur.execute('delete from bowl_odi where bowl_id=(select bowl_id from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))
        
        if(select_table=="BowlingCareerInT20"):
            cur.execute('delete from bowl_t20 where bowl_id=(select bowl_id from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))

        if(select_table=="BowlingCareerInIPL"):
            cur.execute('delete from bowl_ipl where bowl_id=(select bowl_id from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(p_fname,p_lname,))
        
        mysql.connection.commit()
        cur.close()
        return render_template('delete.html')
    return render_template('delete.html')

@app.route('/update_data',methods=['GET','POST'])
def update_data():
    if request.method=='POST':
        req=request.form
        select_table1=req['select_table1']
        pfname=req['P_fname']
        plname=req['P_lname']
        matches=req['matches']
        innings=req['Innings']
        runs=req['runs']
        wickets=req['wickets']
        Runsg=req['Runsg']
        Average=req['Average']
        cur=mysql.connection.cursor()
        if(select_table1=='Allrounder'):
            cur.execute('UPDATE batt_test SET matches = %s,innings=%s,runs=%s WHERE bat_id=(select bat_id from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(matches,innings,runs,pfname,plname,))
            cur.execute('UPDATE bowl_test SET matches=%s,innings=%s, wickets = %s,runs=%s,average=%s WHERE bowl_id=(select bowl_id from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(matches,innings,wickets,Runsg,Average,pfname,plname,))
        
        if(select_table1=='BattingCareerInTest'):
            cur.execute('UPDATE batt_test SET matches = %s,innings=%s,runs=%s WHERE bat_id=(select bat_id from batting where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(matches,innings,runs,pfname,plname,))
        
        if(select_table1=='BowlingCareerInTest'):
            cur.execute('UPDATE bowl_test SET matches=%s,innings=%s, wickets = %s,runs=%s,average=%s WHERE bowl_id=(select bowl_id from bowling where Pid=(select Pid from player_information where p_fname=%s and p_lname=%s))',(matches,innings,wickets,Runsg,Average,pfname,plname,))  
        
        mysql.connection.commit()
        cur.close()
    return render_template('update.html')

@app.route("/contacts")
def f2():
    return render_template('Contact_Us.html')


@app.route("/rankings")
def f3():
    return render_template('Batting_rankings.html')


@app.route("/odi")
def odi():
    return render_template('odi_ranking.html')


@app.route("/t20")
def t20():
    return render_template('t20_ranking.html')


@app.route("/B_rankings")
def branking():
    return render_template('bowling_ranking.html')


@app.route("/B_odi")
def b_odi():
    return render_template('B_odi.html')


@app.route("/B_t20")
def b_t20():
    return render_template('B_t20.html')


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    
    if request.method == 'POST' :#and 'P_fname' in request.form and 'P_lname' in request.form and 'Pid' in request.form and 'Dob' in request.form and 'Bplace' in request.form and 'Country' in request.form and 'Bat_id' in request.form and 'Bowl_id' in request.form:
        addplayer = request.form
        #PLAYER INFORMATION
        P_fname = addplayer['P_fname']
        P_lname = addplayer['P_lname']
        Pid = addplayer['Pid']
        Dob = addplayer['Dob']
        Birth_place = addplayer['Bplace']
        Country = addplayer['Country']
        Bat_id = addplayer['Bat_id']
        Bowl_id = addplayer['Bowl_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO player_information(P_fname,P_lname,Pid,dob,bplace,country) VALUES (%s,%s,%s,%s,%s,%s)",
                    (P_fname, P_lname, Pid, Dob, Birth_place, Country))
        cur.execute(
            'INSERT INTO batting(Pid,Bat_id) VALUES(%s,%s)', (Pid, Bat_id))
        cur.execute(
            'INSERT INTO bowling(Pid,Bowl_id) VALUES(%s,%s)', (Pid, Bowl_id))
        # CAREER
        # Pid = 545
        # Bat_id = 1000
        # Bowl_id = 2000
        # Debut_id = 5
        Player_role = addplayer['Player_role']
        Total_runs = addplayer['Total_runs']
        Debut_id = addplayer['Debut_id']
        cur.execute(
            'INSERT INTO career(Pid, prole,total_runs,debut_id) VALUES(%s,%s,%s,%s)', (Pid, Player_role, Total_runs, Debut_id))
        # DEBUT
        Test_debut = addplayer['Test_debut']
        Odi_debut = addplayer['Odi_debut']
        T20_debut = addplayer['T20_debut']
        cur.execute('INSERT INTO debut(debut_id,test_debut,odi_debut,t20_debut) VALUES(%s,%s,%s,%s)',
                    (Debut_id, Test_debut, Odi_debut, T20_debut))
        # BATTING TEST CAREER
        T_Matches = addplayer['T_Matches']
        T_Innings = addplayer['T_Innings']
        Test_Runs = addplayer['Test_Runs']
        T_Hundreds = addplayer['T_Hundreds']
        T_Double_hundreds = addplayer['T_Double_hundreds']
        T_Fifties = addplayer['T_Fifties']
        T_Four = addplayer['T_Four']
        T_sixes = addplayer['T_sixes']
        T_Highest_score = addplayer['T_Highest_score']
        T_Average = addplayer['T_Average']
        if T_Matches and T_Innings and Test_Runs and T_Hundreds and T_Double_hundreds and T_Fifties and T_Four and T_sixes and T_Highest_score and T_Average:
            cur.execute('INSERT INTO batt_test(bat_id,matches,innings,runs,hundreds,double_hundreds,fifties,fours,sixes,highest_score,average) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                Bat_id, T_Matches, T_Innings, Test_Runs, T_Hundreds, T_Double_hundreds, T_Fifties, T_Four, T_sixes, T_Highest_score, T_Average))
        # BATTING ODI CAREER
        O_Matches = addplayer['O_Matches']
        O_Innings = addplayer['O_Innings']
        Odi_Runs = addplayer['Odi_Runs']
        O_Hundreds = addplayer['O_Hundreds']
        O_Double_hundreds = addplayer['O_Double_hundreds']
        O_Fifties = addplayer['O_Fifties']
        O_Four = addplayer['O_Four']
        O_sixes = addplayer['O_sixes']
        O_Highest_score = addplayer['O_Highest_score']
        O_Average = addplayer['O_Average']
        if O_Matches and O_Innings and Odi_Runs and O_Hundreds and O_Double_hundreds and O_Fifties and O_Four and O_sixes and O_Highest_score and O_Average:
            cur.execute('INSERT INTO batt_odi(bat_id,matches,innings,runs,hundreds,double_hundreds,fifties,fours,sixes,highest_score,average) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                Bat_id, O_Matches, O_Innings, Odi_Runs, O_Hundreds, O_Double_hundreds, O_Fifties, O_Four, O_sixes, O_Highest_score, O_Average))
        # BATTING T20 CAREER
        T20_Matches = addplayer['T20_Matches']
        T20_Innings = addplayer['T20_Innings']
        T20_Test_Runs = addplayer['T20_Test_Runs']
        T20_Hundreds = addplayer['T20_Hundreds']
        T20_Fifties = addplayer['T20_Fifties']
        T20_Four = addplayer['T20_Four']
        T20_sixes = addplayer['T20_sixes']
        T20_Highest_score = addplayer['T20_Highest_score']
        T20_Average = addplayer['T20_Average']
        if T20_Matches and T20_Average and T20_Fifties and T20_Innings and T20_Test_Runs and T20_Hundreds and T20_Four and T20_sixes and T20_Highest_score:
            cur.execute('INSERT INTO batt_t20(bat_id,matches,innings,runs,hundreds,fifties,fours,sixes,highest_score,average) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                Bat_id, T20_Matches, T20_Innings, T20_Test_Runs, T20_Hundreds, T20_Fifties, T20_Four, T20_sixes, T20_Highest_score, T20_Average))
        # BOWLING TEST CAREER
        BT_Matches = addplayer['BT_Matches']
        BT_Innings = addplayer['BT_Innings']
        BT_balls = addplayer['BT_balls']
        BTest_Runs = addplayer['BTest_Runs']
        BT_totalwickets = addplayer['BT_totalwickets']
        BT_5wickets = addplayer['BT_5wickets']
        BT_10wickets = addplayer['BT_10wickets']
        BT_strikerate = addplayer['BT_strikerate']
        BT_economy = addplayer['BT_economy']
        BT_average = addplayer['BT_average']
        if BT_Matches and BT_Innings and BT_balls and BTest_Runs and BT_totalwickets and BT_5wickets and BT_10wickets and BT_strikerate and BT_economy and BT_average:
            cur.execute('INSERT INTO bowl_test(bowl_id,matches,innings,runs,balls,wickets,average,strike_rate,economy,five_wickets,ten_wickets) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (Bowl_id, BT_Matches, BT_Innings, BTest_Runs, BT_balls, BT_totalwickets, BT_average, BT_strikerate, BT_economy, BT_5wickets, BT_10wickets))
        # BOWLING ODI CAREER
        BO_Matches = addplayer['BO_Matches']
        BO_Innings = addplayer['BO_Innings']
        BO_balls = addplayer['BO_balls']
        BOdi_Runs = addplayer['BOdi_Runs']
        BO_totalwickets = addplayer['BO_totalwickets']
        BO_5wickets = addplayer['BO_5wickets']
        # BO_10wickets = addplayer['BO_10wickets']
        BO_average = addplayer['BO_average']
        BO_strikerate = addplayer['BO_strikerate']
        BO_economy = addplayer['BO_economy']
        if BO_Matches and BO_Innings and BO_balls and BOdi_Runs and BO_totalwickets and BO_5wickets and BO_average and BO_strikerate and BO_economy:
            cur.execute('INSERT INTO bowl_odi(bowl_id,matches,innings,runs,balls,wickets,average,strike_rate,economy,five_wickets) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (Bowl_id, BO_Matches, BO_Innings, BOdi_Runs, BO_balls, BO_totalwickets, BO_average, BO_strikerate, BO_economy, BO_5wickets))

        # # BOWLING T2O CAREER
        Bt20_Matches = addplayer['Bt20_Matches']
        Bt20_Innings = addplayer['Bt20_Innings']
        Bt20_balls = addplayer['Bt20_balls']
        Bt20_Runs = addplayer['Bt20_Runs']
        Bt20_totalwickets = addplayer['Bt20_totalwickets']
        Bt20_5wickets = addplayer['Bt20_5wickets']
        Bt20_average = addplayer['Bt20_average']
        Bt20_strikerate = addplayer['Bt20_strikerate']
        Bt20_economy = addplayer['Bt20_economy']
        if Bt20_Matches and Bt20_Innings and Bt20_balls and Bt20_Runs and Bt20_totalwickets and Bt20_5wickets and Bt20_average and Bt20_strikerate and Bt20_economy:
            cur.execute('INSERT INTO bowl_t20(bowl_id,matches,innings,runs,balls,wickets,average,strike_rate,economy,five_wickets) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (Bowl_id, Bt20_Matches, Bt20_Innings, Bt20_Runs, Bt20_balls, Bt20_totalwickets, Bt20_average, Bt20_strikerate, Bt20_economy, Bt20_5wickets))
        # #BATTING IPL CAREER
        ipl_Matches = addplayer['ipl_Matches']
        ipl_Innings = addplayer['ipl_Innings']
        ipl_Runs = addplayer['ipl_Runs']
        ipl_Hundreds = addplayer['ipl_Hundreds']
        ipl_Fifties = addplayer['ipl_Fifties']
        ipl_Four = addplayer['ipl_Four']
        ipl_sixes = addplayer['ipl_sixes']
        ipl_Highest_score = addplayer['ipl_Highest_score']
        ipl_Average = addplayer['ipl_Average']
        if ipl_Matches and ipl_Average and ipl_Fifties and ipl_Innings and ipl_Runs and ipl_Hundreds and ipl_Four and ipl_sixes and ipl_Highest_score: 
            cur.execute('INSERT INTO batt_ipl(bat_id,matches,innings,runs,hundreds,fifties,fours,sixes,highest_score,average) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                Bat_id, ipl_Matches, ipl_Innings, ipl_Runs, ipl_Hundreds, ipl_Fifties, ipl_Four, ipl_sixes, ipl_Highest_score, ipl_Average))
        #BOWLING IPL CAREER
        Bipl_Matches = addplayer['Bipl_Matches']
        Bipl_Innings = addplayer['Bipl_Innings']
        Bipl_balls = addplayer['Bipl_balls']
        Bipl_Runs = addplayer['Bipl_Runs']
        Bipl_totalwickets = addplayer['Bipl_totalwickets']
        Bipl_5wickets = addplayer['Bipl_5wickets']
        Bipl_average = addplayer['Bipl_average']
        Bipl_economy = addplayer['Bipl_economy']
        Bipl_strikerate = addplayer['Bipl_strikerate']
        if Bipl_Matches and Bipl_Innings and Bipl_balls and Bipl_Runs and Bipl_totalwickets and Bipl_5wickets and Bipl_average and Bipl_strikerate and Bipl_economy:
            cur.execute('INSERT INTO bowl_ipl(bowl_id,matches,innings,runs,balls,wickets,average,strike_rate,economy,five_wickets) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (Bowl_id, Bipl_Matches, Bipl_Innings, Bipl_Runs, Bipl_balls, Bipl_totalwickets, Bipl_average, Bipl_strikerate, Bipl_economy, Bipl_5wickets))

        mysql.connection.commit()
        cur.close()
        return render_template('add_data.html')

    return render_template('add_data.html')


@app.route('/playersearch', methods=['GET', 'POST'])
def playersearch():
    msg = ''
    if request.method == 'POST' and 'search' in request.form:
        search = request.form['search']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM player_information WHERE P_fname = %s', (search,))
        playername = cursor.fetchall()
        if playername:
            msg = 'player information is displayed'
            return render_template('display.html', playername=playername)
        else:
            msg = 'no data'
    return render_template('playersearch.html', msg=msg)


@app.route("/Player_details")
def Pdetails():
    return render_template('playersearch.html')


app.run(debug=True)
