"""This function generates other time based features """
#data['offer_date'].values.dayofweek
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

class date_feat:
    def __init__(self,df,feature):
        self.df = df # dataframe containing the feature
        self.feature = feature  #feature to be used for engneeering other date based features.
    def gen_feat(self):
        self.df[self.feature +'_month'] = self.df[self.feature].dt.month
        self.df[self.feature +'_day'] =   self.df[self.feature].dt.day
        self.df[self.feature +"_quarter"] = self.df[self.feature].dt.quarter
        #df[feature+"_isweekend"] = (df[feature].dt.weekday < 5).astype(float)
        self.df[self.feature + '_weekend'] = (pd.DatetimeIndex(self.df[self.feature]).dayofweek).isin([5, 6]).astype(float)

        dr = self.df[self.feature]
        #cal = calendar()
        cal = USFederalHolidayCalendar()
        #holidays = cal.holidays(start=dr.min(), end=dr.max())
        holidays = cal.holidays(start=dr.min(), end=dr.max()).to_pydatetime()

        self.df[self.feature +'_holiday'] = self.df[self.feature].isin(holidays).astype(float)
        return self.df 