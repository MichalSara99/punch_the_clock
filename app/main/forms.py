from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField
from datetime import datetime
from sqlalchemy import desc,asc
from ..models import Time_dimension


class SelectForm(FlaskForm):
    searchYear = SelectField("",coerce=int,default=datetime.now().year)
    searchMonth = SelectField("",coerce=int,default=datetime.now().month)
    searchWeek = SelectField("",coerce=int,default=datetime.now().isocalendar()[1])
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
                date_period = first_date.db_date.strftime("%m/%d/%Y") + ' - ' + last_date.db_date.strftime("%m/%d/%Y")
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
                date_period = first_date.db_date.strftime("%m/%d/%Y") + ' - ' + last_date.db_date.strftime("%m/%d/%Y")
                weeks[w.week] = date_period
        self.searchWeek.choices = [(k, v) for k,v in weeks.items()]