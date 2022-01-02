from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField,TimeField
from datetime import datetime,timedelta
from sqlalchemy import desc,asc
from ..models import Time_dimension


class SettingsForm(FlaskForm):
    workingTime = TimeField("",default=datetime(1900,1,1,8,0,0))
    settingsSubmit = SubmitField("Save")


class HistoryForm(FlaskForm):
    historyYear = SelectField("",coerce=int,default=datetime.now().year)
    historyMonth = SelectField("",coerce=int,default=datetime.now().month)
    historySubmit = SubmitField("Show")

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args,**kwargs)
        self.historyYear.choices = [(td.year,td.year) for td in Time_dimension.query.group_by(Time_dimension.year).all()]
        self.historyMonth.choices = [(td.month, td.month_name) for td in
                                   Time_dimension.query.group_by(Time_dimension.month, Time_dimension.month_name).all()]

def get_propper_week():
    today = datetime.now()
    w = today.isocalendar()
    if w[2] == 6:
        next_day = today + timedelta(days=2)
        return next_day.isocalendar()[1]
    elif w[2] == 7:
        next_day = today + timedelta(days=1)
        return next_day.isocalendar()[1]
    return w[1]


class SelectForm(FlaskForm):
    searchYear = SelectField("",coerce=int,default=datetime.now().year)
    searchMonth = SelectField("",coerce=int,default=datetime.now().month)
    searchWeek = SelectField("",coerce=int,default=get_propper_week())
    searchSubmit = SubmitField("Show")

    def __init__(self, *args, **kwargs):
        super(SelectForm, self).__init__(*args,**kwargs)
        today = datetime.now()
        weeks = {}
        self.searchYear.choices = [(td.year,td.year) for td in Time_dimension.query.group_by(Time_dimension.year).all()]
        self.searchMonth.choices = [(td.month, td.month_name) for td in
                                   Time_dimension.query.group_by(Time_dimension.month, Time_dimension.month_name).all()]
        week_numbers = Time_dimension.query.filter_by(year=today.year, month=today.month).group_by(Time_dimension.week)\
            .order_by(asc(Time_dimension.week)).all()
        for w in week_numbers:
            first_date = Time_dimension.query.filter_by(year = today.year, month=today.month, week=w.week, weekend_flag='f') \
                .order_by(asc(Time_dimension.db_date)).first()
            last_date = Time_dimension.query.filter_by(year=today.year, month=today.month, week=w.week, weekend_flag='f') \
                .order_by(desc(Time_dimension.db_date)).first()
            if not first_date is None and not last_date is None:
                date_period = first_date.db_date.strftime("%d/%m/%Y") + ' - ' + last_date.db_date.strftime("%d/%m/%Y")
                weeks[w.week] = date_period
        self.searchWeek.choices = [(k, v) for k,v in weeks.items()]

    def update_weeks(self, year,month):
        weeks = {}
        week_numbers = Time_dimension.query.filter_by(year=year, month=month).group_by(Time_dimension.week)\
            .order_by(asc(Time_dimension.week)).all()
        for w in week_numbers:
            first_date = Time_dimension.query.filter_by(year = year, month=month, week=w.week, weekend_flag='f') \
                .order_by(asc(Time_dimension.db_date)).first()
            last_date = Time_dimension.query.filter_by(year=year, month=month, week=w.week, weekend_flag='f') \
                .order_by(desc(Time_dimension.db_date)).first()
            if not first_date is None and not last_date is None:
                date_period = first_date.db_date.strftime("%d/%m/%Y") + ' - ' + last_date.db_date.strftime("%d/%m/%Y")
                weeks[w.week] = date_period
        self.searchWeek.choices = [(k, v) for k,v in weeks.items()]