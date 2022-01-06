from flask import render_template,request,jsonify,flash,redirect,url_for
from flask_login import current_user
from sqlalchemy import desc,asc,func
from . import main
from .. import db
from .. models import User_settings,Work,Work_notes,Time_dimension
from datetime import datetime,timedelta
from .forms import SelectForm,SettingsForm,HistoryForm



def timesheet(year,month,week,user_id):
    tms = db.session.query(Time_dimension.id,
                           Time_dimension.db_date,
                           Time_dimension.day_name,
                           Work.start_time,
                           Work.lunch_duration,
                           Work.end_time,
                           Work.worked_time,
                           Work.overtime). \
        join(Work, Time_dimension.id == Work.td_id). \
        filter(Time_dimension.year == year,
               Time_dimension.month == month,
               Time_dimension.week == week,
               Work.user_id == user_id,
               Time_dimension.weekend_flag == 'f'). \
        order_by(asc(Time_dimension.id)).all()
    return tms

def historysheet(year,month,user_id):
    tms = db.session.query(Time_dimension.id,
                           Time_dimension.db_date,
                           Time_dimension.day_name,
                           Work.start_time,
                           Work.lunch_duration,
                           Work.end_time,
                           Work.worked_time,
                           Work.overtime). \
        join(Work, Time_dimension.id == Work.td_id). \
        filter(Time_dimension.year == year,
               Time_dimension.month == month,
               Work.user_id == user_id,
               Time_dimension.weekend_flag == 'f'). \
        order_by(asc(Time_dimension.id)).all()
    return tms

def history_summary(year,month,user_id):
    hs = db.session.query(Time_dimension.id,
                           func.sec_to_time(func.sum(func.time_to_sec(Work.worked_time))),
                           func.sec_to_time(func.sum(func.time_to_sec(Work.overtime)))). \
        join(Work, Time_dimension.id == Work.td_id). \
        filter(Time_dimension.year == year,
               Time_dimension.month == month,
               Work.user_id == user_id,
               Time_dimension.weekend_flag == 'f'). \
        order_by(asc(Time_dimension.id)).all()
    if hs[0][0] is None:
        return {'tw':timedelta(0),'to':timedelta(0)}
    return {'tw':hs[0][1],'to':hs[0][2]}

def notes(year,month,week,user_id):
    nts = db.session.query(Time_dimension.id,Work_notes.notes). \
        join(Work_notes, Time_dimension.id == Work_notes.td_first_id). \
        filter(Time_dimension.year == year,
               Time_dimension.month == month,
               Time_dimension.week == week,
               Work_notes.user_id == user_id,
               Time_dimension.weekend_flag == 'f'). \
        order_by(asc(Time_dimension.id)).all()
    if len(nts) <= 0:
        return ''
    return nts[0][1]

def format_timedelta(td):
    d = datetime(1900, 1, 1)
    if td < timedelta(0):
        return '-' + format_timedelta(-td)
    else:
        return (d + td).strftime("%H:%M")


#################################### VIEW FUNCS #################################

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/timesheets',methods=['POST','GET'])
@main.route('/timesheets/<int:year>/<int:month>/<int:week>',methods=['POST','GET'])
def timesheets(year = None,month=None,week=None):
    save_btn = False
    create_btn = False
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
        nts = notes(year,month,week,current_user.id)
    else:
        form.update_weeks(int(form.searchYear.data),int(form.searchMonth.data))
        tms = timesheet(int(form.searchYear.data),int(form.searchMonth.data),
                        int(form.searchWeek.data),current_user.id)
        nts = notes(int(form.searchYear.data), int(form.searchMonth.data),
                    int(form.searchWeek.data), current_user.id)
    save_btn = False if len(tms) <= 0 else True
    create_btn = not save_btn
    return render_template('timesheets.html',
                           form=form,time_table=tms,notes_area = nts,
                           save_btn=save_btn,create_btn = create_btn)


@main.route('/on_save',methods=['POST','GET'])
def on_save():
    if request.method == "POST":
        data_sent = request.get_json()
        d = data_sent['data']
        n = data_sent['notes']
        works = [Work.query.filter_by(user_id=current_user.id,td_id = k).one() for k in d.keys()]
        last_td_id = 0
        for w in works:
            td_id_str = str(w.td_id)
            last_td_id = w.td_id
            w.start_time = d[td_id_str]['start']
            w.lunch_duration = d[td_id_str]['lunch']
            w.end_time = d[td_id_str]['end']
            w.worked_time = d[td_id_str]['worked']
            w.overtime = d[td_id_str]['over']
            db.session.merge(w)
            db.session.flush()
            db.session.commit()
        work_notes = Work_notes.query.filter_by(user_id=current_user.id, td_first_id=works[0].td_id).first()
        work_notes.notes = n
        db.session.merge(work_notes)
        db.session.flush()
        db.session.commit()
        td = Time_dimension.query.filter_by(id = last_td_id).first()
        next = url_for('main.timesheets',
                       year=td.year,
                       month = td.month,
                       week = td.week)
        flash('Changes have been saved.')
        return redirect(next)


@main.route('/on_create',methods=['POST','GET'])
def on_create():
    if request.method == "POST":
        data_sent = request.get_json()
        ids = Time_dimension.query.filter_by(year=data_sent['year'],
                                             month=data_sent['month'],
                                             week=data_sent['week'])\
            .order_by(asc(Time_dimension.week)).all()
        for i in ids:
            work = Work(user_id = current_user.id,
                        td_id = i.id,
                        start_time = '00:00:00',
                        lunch_duration = '00:00:00',
                        end_time = '00:00:00',
                        worked_time = '00:00:00',
                        overtime = '00:00:00')
            db.session.add(work)
            db.session.commit()
        work_notes = Work_notes(user_id = current_user.id,
                               td_first_id = ids[0].id,
                               notes='')
        db.session.add(work_notes)
        db.session.commit()
        next = url_for('main.timesheets',
                       year=int(data_sent['year']),
                       month = int(data_sent['month']),
                       week = int(data_sent['week']))
        flash('New week has been added.')
        return redirect(next)



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
                date_period = first_date.db_date.strftime("%d/%m/%Y") + ' - ' + last_date.db_date.strftime("%d/%m/%Y")
                sent_back[w.week] = date_period
    return jsonify(sent_back)


@main.route('/calculate_time',methods=['POST','GET'])
def calculate_time():
    sent_back = {}
    if request.method == "POST":
        d = datetime(1900, 1, 1)
        data_sent = request.get_json()
        id = data_sent['id']
        start = datetime.strptime(data_sent['start'], '%H:%M')
        lunch = datetime.strptime(data_sent['lunch'],'%H:%M')
        end = datetime.strptime(data_sent['end'], '%H:%M')
        worked = data_sent['worked']
        over_orig = data_sent['overtime']
        wt = User_settings.query.filter_by(user_id = current_user.id).first()
        limit = wt.working_time
        end_lunch = d + (end-lunch)
        diff_days = (end_lunch - start).days
        sent_back['id'] = id
        if diff_days < 0:
            sent_back['worked'] = worked
            sent_back['overtime'] = over_orig
            sent_back['message'] = 'Start Time must be lower than End Time minus Lunch Duration'
        else:
            diff = (end_lunch - start)
            sent_back['worked'] = (d + diff).strftime("%H:%M")
            sent_back['overtime'] = format_timedelta(diff-limit)
            sent_back['message'] = 'OK'
    return jsonify(sent_back)



@main.route('/settings',methods=['GET','POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        us = User_settings.query.filter_by(user_id=current_user.id).first()
        us.user_id = current_user.id
        us.working_time = form.workingTime.data
        db.session.merge(us)
        db.session.flush()
        db.session.commit()
        next = url_for('main.settings')
        flash('Settings have been saved')
        return redirect(next)
    wt = User_settings.query.filter_by(user_id=current_user.id).first()
    form.workingTime.data = (datetime(1900, 1, 1) + wt.working_time)
    return render_template('settings.html',form=form)


@main.route('/history',methods=['GET','POST'])
@main.route('/history/<int:year>/<int:month>',methods=['GET','POST'])
def history(year=None,month=None):
    form = HistoryForm()
    if request.method == 'POST':
        next = url_for('main.history',
                       year=int(form.historyYear.data),
                       month = int(form.historyMonth.data))
        return redirect(next)
    if year is not None and month is not None:
        form.historyYear.data = year
        form.historyMonth.data = month
        hs = historysheet(year,month,current_user.id)
        info = history_summary(year,month,current_user.id)
    else:
        hs = historysheet(int(form.historyYear.data),int(form.historyMonth.data),
                          current_user.id)
        info = history_summary(int(form.historyYear.data),int(form.historyMonth.data),
                               current_user.id)
    return render_template('history.html',form=form,
                           history_table=hs,info=info)



@main.route('/about')
def about():
    return render_template('about.html')