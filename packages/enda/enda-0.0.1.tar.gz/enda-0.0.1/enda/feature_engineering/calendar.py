import pandas as pd
import datetime
from enda.feature_engineering.datetime_features import DatetimeFeature

try:
    import unidecode
    from jours_feries_france import JoursFeries
    from vacances_scolaires_france import SchoolHolidayDates
except ImportError:
    raise ImportError("unidecode, jours_feries_france, vacances_scolaires_france are required if you want to use "
                      "enda's FrenchHolidays and FrenchCalendar classes. "
                      "Try: pip install jours-feries-france vacances-scolaires-france Unidecode")


class FrenchHolidays:

    @staticmethod
    def get_public_holidays(year_list=None, orientation='rows'):

        if year_list is None:
            year_list = range(2000, 2051)

        result = pd.DataFrame()
        for year in year_list:
            try:
                res = JoursFeries.for_year(year)
                df_res = pd.DataFrame.from_dict(res, orient='index')
                df_res.index = df_res.index.map(lambda x: unidecode.unidecode(x))
                result = result.append(df_res.T, ignore_index=True)
            except Exception as e:
                raise ValueError("Missing french public holidays : {}".format(e))

        if orientation is not 'columns':
            result = result.stack().reset_index(level=0, drop=True)
            result.index.name = 'nom_jour_ferie'
            result = result.to_frame('date')
            result = result.reset_index(drop=False)
            result = result[['date', 'nom_jour_ferie']]

        return result

    @staticmethod
    def get_school_holidays(year_list=None):

        if year_list is None:
            current_year = datetime.datetime.utcnow().year
            year_list = range(2000, current_year + 1)

        d = SchoolHolidayDates()
        result = pd.DataFrame()
        for year in year_list:
            try:
                res = d.holidays_for_year(year)
                df_res = pd.DataFrame.from_dict(res, orient='index')
                df_res['nom_vacances'] = df_res['nom_vacances'].map(lambda x: unidecode.unidecode(x))
                df_res = df_res.reset_index(drop=True)
                result = result.append(df_res, ignore_index=True)
            except Exception as e:
                raise ValueError("Missing french school holidays : {}".format(e))

        return result


class Calendar:

    def __init__(self, country='FR'):
        self.country = country

    def get_french_lockdown(self):
        """
        Return a dataframe from 2000-01-01 to 2050-12-25 indicating for each day if national lockdown was ongoing.
        So far, the main lockdown period goes from 2020-03-17 to 2020-05-11.
        """

        if self.country is not 'FR':
            raise NotImplementedError("Public holidays in {} unknown".format(self.country))

        start_lockdown_date = pd.to_datetime('2020-03-17')
        end_lockdown_date = pd.to_datetime('2020-05-11')
        lockdown_period = pd.date_range(start_lockdown_date, end_lockdown_date)

        df_lockdown = pd.DataFrame(index=lockdown_period, columns=['lockdown'], data=1)
        df_lockdown.index.name = 'date'

        result = df_lockdown.reindex(pd.date_range('2000-01-01', '2050-12-25'))
        result = result.fillna(0)

        return result

    def get_public_holidays(self):
        """
        Return a dataframe from 2000-01-01 to 2050-12-25 indicating for each day
        whether it is a public holiday (denoted by a 1) or not (denoted by a 0)
        """

        if self.country is 'FR':
            public_holidays = FrenchHolidays.get_public_holidays()
        else:
            raise NotImplementedError("Public holidays in {} unknown".format(self.country))

        public_holidays = public_holidays.set_index('date')
        public_holidays.index = pd.to_datetime(public_holidays.index)
        public_holidays = public_holidays[~public_holidays.index.duplicated(keep='first')]  # 2008-05-01

        public_holidays['public_holiday'] = 1
        public_holidays = public_holidays.asfreq('D')
        public_holidays = public_holidays.fillna(0)

        return public_holidays[['public_holiday']]

    def get_school_holidays(self):
        """
        Return a dataframe from 2000-01-01 to as far as possible (2021-08-29) indicating for each day
        the number of school areas (zone A, B et C) in vacation (either 0, 1, 2 or 3)
        """

        if self.country is 'FR':
            school_holidays = FrenchHolidays.get_school_holidays()
        else:
            raise NotImplementedError("School holidays in {} unknown".format(self.country))

        school_holidays = school_holidays.set_index('date')
        school_holidays.index = pd.to_datetime(school_holidays.index)
        school_holidays = school_holidays.drop('nom_vacances', 1)

        school_holidays['nb_school_areas_off'] = school_holidays.sum(axis=1)
        school_holidays = school_holidays.asfreq('D')
        school_holidays = school_holidays.fillna(0)

        return school_holidays[['nb_school_areas_off']]

    def get_extra_long_weekend(self):
        """
        Return a dataframe from 2000-01-01 to 2050-12-25 indicating for each day
        - if the previous (resp. the next day) is a public holiday
        AND
        - if the current day is a tuesday (resp. a thursday)
        If both conditions are fulfilled then the day is denoted by a 1 (0 otherwise)
        """

        public_holidays = self.get_public_holidays()
        public_holidays = DatetimeFeature.split_datetime(public_holidays, split_list=['dayofweek'], index=True)

        public_holidays['is_yesterday_day_off'] = public_holidays['public_holiday'].shift()
        public_holidays['is_tomorrow_day_off'] = public_holidays['public_holiday'].shift(-1)
        public_holidays['extra_long_weekend'] = 0

        mondays = public_holidays[public_holidays['dayofweek'] == 0]
        mondays_off = mondays[mondays['is_tomorrow_day_off'] == 1].index

        fridays = public_holidays[public_holidays['dayofweek'] == 4]
        fridays_off = fridays[fridays['is_yesterday_day_off'] == 1].index

        extra_long_weekend_index = mondays_off.append(fridays_off)
        extra_long_weekend_index = sorted(extra_long_weekend_index)

        public_holidays.loc[extra_long_weekend_index, 'extra_long_weekend'] = 1

        return public_holidays[['extra_long_weekend']]

    @staticmethod
    def interpolate_daily_to_subdaily_data(df, freq, method='ffill', tz='Europe/Paris'):
        """
        Interpolate daily data in a dataframe (with a DatetimeIndex) to subdaily data using a given method.
        :param df: pd.DataFrame
        :param freq: a frequency < 'D' (e.g. 'H', '30min', '15min', etc)
        :param method: how are data interpolated between two consecutive dates (e.g. 'ffill', 'linear', etc)
        :param tz: timezone ('Europe/Paris')
        :return: pd.DataFrame
        """
        if df.index.tzinfo is None:
            df.index = pd.to_datetime(df.index).tz_localize(tz)

        new_end_date = df.index.max() + datetime.timedelta(days=1)
        extra_row = df.iloc[[-1]].reindex([new_end_date])

        result = df.append(extra_row, ignore_index=False)
        result = result.resample(freq).interpolate(method=method)
        result = result.drop(new_end_date)

        result.index.name = 'time'

        return result

    @staticmethod
    def get_french_special_days(freq='30min'):

        lockdown = Calendar().get_french_lockdown()
        public_holidays = Calendar().get_public_holidays()
        school_holidays = Calendar().get_school_holidays()
        extra_long_weekend = Calendar().get_extra_long_weekend()

        result = pd.concat([lockdown, public_holidays, school_holidays, extra_long_weekend], 1, 'inner')
        result = Calendar().interpolate_daily_to_subdaily_data(result, freq=freq)

        return result
