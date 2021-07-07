import base64
import io
import urllib.parse

import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import mplcyberpunk

def get_graph():
    buffer = io.BytesIO()
    fig = plt.gcf()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    string = base64.b64encode(buffer.read())
    uri = urllib.parse.quote(string)
    buffer.close()
    return uri


def get_plot_cake(*, name="", **kwargs):
    plt.style.use("cyberpunk")
    plt.clf()
    list_of_values = list(kwargs.values())
    if len(list_of_values) == 0:
        return get_graph()
    if max(list_of_values) == 0:
        return get_graph()
    slices = list(kwargs.values())
    labels = list(kwargs.keys())
    explode = [0.03 for _ in range(len(slices))]
    plt.pie(slices, labels=labels, wedgeprops={'edgecolor': 'black'},
            explode=explode, shadow=True)
    plt.title(name)
    plt.tight_layout()
    return get_graph()


def get_plot_normal(dates, *, name="", xlabel='Datum',
                    ylabel='Odpracované hodiny',
                    **kwargs):
    for i in kwargs.values():
        assert len(i) == len(dates)
    plt.clf()
    plt.style.use("cyberpunk")

    legend = []
    for k in kwargs:
        plt.plot_date(dates, [ i//60 for i in kwargs[k]], linestyle='solid')
        legend.append(k)

    plt.title(name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    date_format = mpl_dates.DateFormatter('%d. %m. %Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()

    plt.legend(legend)
    plt.tight_layout()

    graph = get_graph()
    return graph


def days_minutes(td):
    return td.seconds // 3600 + td.days * 24, (td.seconds // 60) % 60
