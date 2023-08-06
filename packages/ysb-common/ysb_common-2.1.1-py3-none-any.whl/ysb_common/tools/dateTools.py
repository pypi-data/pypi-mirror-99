import calendar
import time
import datetime
import calendar


class DateTools:
    # 1. 获取「今天」  2021-01-07
    today = datetime.date.today()
    # 2. 获取当前月的第一天
    first_day = today.replace(day=1)
    # 3. 减一天，得到上个月的最后一天
    last_month_last_day = first_day - datetime.timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)

    @staticmethod
    def get_today(type1=None):
        """
        获取当前时间：返回不同的格式
        :param: type:
        1返回年，2返回月，3返回日。None返回年月日yyyy-mm-dd
        :return:
        """
        if type1 is None:
            today_str = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        else:
            type2 = str(type1)
            cur = datetime.datetime.now()
            if type2 == '1':
                today_str = str(cur.year)
            elif type2 == '2':
                yf = str(cur.month)
                if int(yf) < 10:
                    today_str = "0" + yf
                else:
                    today_str = yf
            elif type2 == '3':
                today_str = cur.day

        return str(today_str)

    @staticmethod
    def get_last_month_first_day():
        """
        获取上个月的第一天
        :return:
        """
        return str(DateTools.last_month_first_day)

    @staticmethod
    def get_last_month_last_day():
        """
        获取上个月的最后一天
        :return:
        """
        return str(DateTools.last_month_last_day)

    @staticmethod
    def get_this_month_first_day():
        """
        获取本月第一天
        :return:
        """
        return str(DateTools.first_day)

    @staticmethod
    def get_this_month_last_day():
        """
        获取本月最后一天
        :return:
        """
        last_day = datetime.date.today().replace(
            day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])
        return str(last_day)

    @staticmethod
    def switch_quarter(date):
        """
        判断日期所属季度
        :param date: 格式-'2019-10-01'
        :return:
        """
        date_list = date.split('-')
        if date_list[1] == '01':
            return '1'
        elif date_list[1] == '04':
            return '2'
        elif date_list[1] == '07':
            return '3'
        elif date_list[1] == '10':
            return '4'
        else:
            return '0'

    @staticmethod
    def nsqx_dm(startDate, endDate):
        """
        根据所属日期返回月/季申报代码
        :param startDate:
        :param endDate:
        :return:
        """
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        num = (endDate - startDate).days
        if num < 60:
            return '06'  # 按月申报
        elif num < 180:
            return '08'  # 按季申报
        elif num < 300:
            return '09'  # 按半年申报
        elif num > 300:
            return '10'  # 按年申报
        elif startDate == endDate:
            return '11'  # 按次申报

    @staticmethod
    def last_month(set_date):
        """
        给定时间，返回上月月初/月末日期
        :param set_date:
        :return:
        """
        date_dict = {}
        set_day = datetime.datetime.strptime(set_date, '%Y-%m-%d')
        set_time = datetime.date(set_day.year, set_day.month, set_day.day)  # 年，月，日
        # 该月第一天
        this_month_start = datetime.date(set_time.year, set_time.month, 1)
        # 前一个月最后一天
        last_month_end = this_month_start - datetime.timedelta(days=1)
        # 前一个月第一天
        last_month_start = datetime.date(last_month_end.year, last_month_end.month, 1)
        date_dict['last_month_start'] = str(last_month_start)
        date_dict['last_month_end'] = str(last_month_end)
        return date_dict

    @staticmethod
    def last_quarter():
        """
        上一季的第一天与最后一天
        :return:
        """
        date_dict = {}
        # 当前季度
        now = datetime.datetime.now()
        month = (now.month - 1) - (now.month - 1) % 3 + 1
        this_quarter_start = datetime.datetime(now.year, month, 1)
        last_quarter_end = this_quarter_start - datetime.timedelta(days=1)
        last_quarter_start = datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)
        date_dict['last_quarter_start'] = str(last_quarter_start.date())
        date_dict['last_quarter_end'] = str(last_quarter_end.date())
        return date_dict

    @staticmethod
    def sfty(date1, date2):
        """
        判断两个日期是否同属一月份
        :param date1:
        :param date2:
        :return:
        """
        date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
        date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
        if date1.year == date2.year and date1.month == date2.month:
            return True
        else:
            return False

    @staticmethod
    def current_quarter():
        """
        获取本季第一天与最后一天
        :return:
        """
        now = datetime.datetime.now()
        month = (now.month - 1) - (now.month - 1) % 3 + 1
        this_quarter_start = datetime.datetime(now.year, month, 1)
        this_quarter_end = datetime.datetime(now.year, month, calendar.monthrange(now.year, now.month)[1])

    @staticmethod
    def is_quarter(date1, date2):
        """
        判断两个日期是否同属一个季度
        :param date1:
        :param date2:
        :return:
        """
        date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
        quarter1 = int((date1.month - 1) / 3 + 1)
        date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
        quarter2 = int((date2.month - 1)/3 + 1)
        if quarter1 == quarter2:
            return True
        else:
            return False

    @staticmethod
    def during_date(current_date, start_date, end_date):
        """
        判断日期是否在某段时间内
        :return:
        """
        current_time = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        if start_time <= current_time <= end_time:
            return True
        else:
            return False
