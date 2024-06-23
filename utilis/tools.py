from datetime import datetime


def retime(time_str1, time_str2):
    # 将时间字符串转换为 datetime 对象
    time1 = datetime.strptime(str(time_str1), "%Y-%m-%d %H:%M:%S")
    time2 = datetime.strptime(str(time_str2), "%Y-%m-%d %H:%M:%S")
    # 计算时间差
    time_diff = time2 - time1
    # 将时间差转换为秒数
    total_seconds = time_diff.total_seconds()
    return int(total_seconds)
