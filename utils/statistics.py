from database import *
import datetime as datecalc
from matplotlib import pyplot
import pandas
import seaborn


def get_users_statistics(type : str) -> dict:
    """
    forming statistics about users by every type [hour/day/]

    :return: dict(key=iso_format, value=database.User)
    """

    result = dict()
    available_types = ['day', 'hour']
    if type not in available_types:
        raise Exception(f"{type} type is not available (allowed types: [{available_types}])")

    users = sorted(get_users(), key=lambda x : x.auth_date)
    for k in range(len(users)):
        date_ = datecalc.datetime.fromtimestamp(users[k].auth_date)

        # iso string without minutes and seconds/milliseconds
        split_sign = ':'
        if type == 'day':
            split_sign = 'T'

        iso = date_.isoformat().split(split_sign)[0]

        if iso not in result:
            result[iso] = list()

        result[iso].append(users[k])

    return result


def get_parsed_users_stats(users_stat: dict):
    """
    :return: dict(key=iso_format, value=count of users)
    """

    result = dict()
    for key in users_stat:
        result[key] = len(users_stat[key])

    return result

def get_pandas_users_stats(users_stat : dict):
    result = list()
    for key in users_stat:
        result.append({
            'day' : key,
            'count' : len(users_stat[key])
        })


    return pandas.DataFrame.from_dict(result)


def show_users_stats_pyplot():
    users_stat = get_parsed_users_stats(get_users_statistics('day'))

    x = list(users_stat.keys())
    y = list(users_stat.values())

    pyplot.plot(x, y, color='green', linestyle='dashed', linewidth=3,
                marker='o', markerfacecolor='blue', markersize=12)

    pyplot.ylim(0, max(y) + 5)

    pyplot.xlabel('Days')
    pyplot.ylabel('Count of users')

    pyplot.title("Users table statistic")

    pyplot.show()


def show_users_stats_seaborn():
    dataframe = get_pandas_users_stats(get_users_statistics('day'))

    # seaborn.set_context("notebook", font_scale = 1)
    # seaborn.histplot(data = dataframe)

    fig, axes = pyplot.subplots(1, 2, figsize=(15, 5))

    ax1 = seaborn.histplot(data = dataframe, bins = 3, ax=axes[0])
    ax2 = seaborn.histplot(data = dataframe, element='step', ax=axes[1])

    axes[0].set_title("Too few bins!")
    axes[1].set_title("Too many bins!")

    pyplot.show()