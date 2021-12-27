# FLASK related imports
from flask import render_template,request,jsonify,flash,redirect,url_for
from flask_login import current_user
from sqlalchemy import desc,asc
from . import main
from .. import db
import json
from .. models import User,Work,Time_dimension
from datetime import datetime,time
from .forms import SelectForm


@main.route('/')
def index():
    return render_template('index.html')

def timesheet(year,month,week,user_id):
    tms = db.session.query(Time_dimension.id,
                           Time_dimension.db_date,
                           Time_dimension.day_name,
                           Work.start_time,
                           Work.lunch_duration,
                           Work.end_time,
                           Work.worked_time). \
        join(Work, Time_dimension.id == Work.td_id). \
        filter(Time_dimension.year == year,
               Time_dimension.month == month,
               Time_dimension.week == week,
               Work.user_id == user_id,
               Time_dimension.weekend_flag == 'f'). \
        order_by(asc(Time_dimension.id)).all()
    return tms


@main.route('/timesheets',methods=['POST','GET'])
@main.route('/timesheets/<int:year>/<int:month>/<int:week>',methods=['POST','GET'])
def timesheets(year = None,month=None,week=None):
    save_btn = False
    form = SelectForm()
    if request.method == 'POST':
        next = url_for('main.timesheets',
                       year=int(form.searchYear.data),
                       month = int(form.searchMonth.data),
                       week = int(form.searchWeek.data))
        return redirect(next)
    if year is not None and month is not None and week is not None:
        form.searchYear.data = year
        form.searchMonth.data = month
        form.searchWeek.data = week
        form.update_weeks(year, month)
        tms = timesheet(year,month,week,current_user.id)
    else:
        form.update_weeks(int(form.searchYear.data),int(form.searchMonth.data))
        tms = timesheet(int(form.searchYear.data),int(form.searchMonth.data),
                        int(form.searchWeek.data),current_user.id)
    save_btn = False if len(tms) <= 0 else True
    return render_template('timesheets.html',
                           form=form,time_table=tms,
                           save_btn=save_btn)

@main.route('/about')
def about():
    return render_template('about.html')

'''
    if form.validate_on_submit():
        year = form.searchYear.data
        month = form.searchMonth.data
        week = form.searchWeek.data
        tms = timesheet(year, month, week,current_user.id)
        save_btn = False if len(tms) <= 0 else True
        next = url_for('main.timesheets_show',
                   year=year,
                   month=month,
                   week=week)
        return redirect(next)
    form.update_weeks(year,month)
    form.searchYear.data = year
    form.searchMonth.data = month
    form.searchWeek.data = week
    tms = timesheet(year,month,week,current_user.id)
    return render_template('timesheets.html',
                           form=form, time_table=tms,
                           save_btn=save_btn)
'''



'''
    if request.method == "GET":
        ymw = InitYMW.ymw()
        today = datetime.now()
        tms = db.session.query(Time_dimension.id,
                                    Time_dimension.db_date,
                                    Time_dimension.day_name,
                                    Work.start_time,
                                    Work.lunch_duration,
                                    Work.end_time,
                                    Work.worked_time).\
            join(Work,Time_dimension.id == Work.td_id).\
            filter(Time_dimension.year == today.year,
                   Time_dimension.month == today.month,
                   Time_dimension.week == today.isocalendar()[1],
                   Work.user_id == current_user.id,
                   Time_dimension.weekend_flag == 'f').\
            order_by(asc(Time_dimension.id)).all()
        if len(tms)<=0:
            save_btn = False
'''
'''
    return render_template('timesheets.html',
                           years = ymw['years'],year_selected=today.year,
                           months = ymw['months'],month_selected = today.month,
                           weeks = ymw['weeks'],week_selected = str(today.isocalendar()[1]),
                           user_tms = tms,save_btn=save_btn)
'''



'''
@main.route('/on_show',methods=['POST','GET'])
def on_show():
    if request.method == "POST":
        data_sent = request.get_json()
        tms = db.session.query(Time_dimension.id,
                                    Time_dimension.db_date,
                                    Time_dimension.day_name,
                                    Work.start_time,
                                    Work.lunch_duration,
                                    Work.end_time,
                                    Work.worked_time).\
            join(Work,Time_dimension.id == Work.td_id).\
            filter(Time_dimension.year == data_sent['year'],
                   Time_dimension.month == data_sent['month'],
                   Time_dimension.week == data_sent['week'],
                   Work.user_id == current_user.id,
                   Time_dimension.weekend_flag == 'f').all()
        if len(tms) == 0:
            ins = db.session.query(Time_dimension.id). \
                filter(Time_dimension.year == data_sent['year'],
                       Time_dimension.month == data_sent['month'],
                       Time_dimension.week == data_sent['week'],
                       Time_dimension.weekend_flag == 'f').all()
            for i in ins:
                work = Work(user_id = current_user.id,
                            td_id = i[0],
                            start_time = '00:00:00',
                            lunch_duration = '00:00:00',
                            end_time = '00:00:00',
                            worked_time='00:00:00')
                db.session.add(work)
                db.session.commit()
            print(ins)
        flash('New week has been added to your timesheets.')
    return redirect(url_for('main.timesheets'))
'''

@main.route('/get_year_month',methods=['POST','GET'])
def on_year_month_data():
    sent_back = {}
    if request.method == "POST":
        data_sent = request.get_json()
        week_numbers = Time_dimension.query.filter_by(year=data_sent['year'], month=data_sent['month'])\
            .group_by(Time_dimension.week)\
            .order_by(asc(Time_dimension.week)).all()
        for w in week_numbers:
            first_date = Time_dimension.query.filter_by(year = data_sent['year'],
                                                        month=data_sent['month'],
                                                        week=w.week, weekend_flag='f') \
                .order_by(asc(Time_dimension.db_date)).first()
            last_date = Time_dimension.query.filter_by(year=data_sent['year'],
                                                       month=data_sent['month'],
                                                       week=w.week, weekend_flag='f') \
                .order_by(desc(Time_dimension.db_date)).first()
            if not first_date is None and not last_date is None:
                date_period = first_date.db_date.strftime("%m/%d/%Y") + ' - ' + last_date.db_date.strftime("%m/%d/%Y")
                sent_back[w.week] = date_period
    return jsonify(sent_back)


@main.route('/calculate_time',methods=['POST','GET'])
def calculate_time():
    sent_back = {}
    if request.method == "POST":
        d = datetime(1900, 1, 1)
        data_sent = request.get_json()
        print(data_sent)
        id = data_sent['id']
        start = datetime.strptime(data_sent['start'], '%H:%M')
        lunch = datetime.strptime(data_sent['lunch'],'%H:%M')
        end = datetime.strptime(data_sent['end'], '%H:%M')
        worked = datetime.strptime(data_sent['worked'], '%H:%M')
        end_lunch = d + (end-lunch)
        diff_days = (end_lunch - start).days
        sent_back['id'] = id
        if diff_days < 0:
            sent_back['worked'] = worked.strftime("%H:%M")
            sent_back['message'] = 'Start Time must be lower than End Time minus Lunch Duration'
        else:
            sent_back['worked'] = (d + (end_lunch - start)).strftime("%H:%M")
            sent_back['message'] = 'OK'
        print(sent_back)
    return jsonify(sent_back)
