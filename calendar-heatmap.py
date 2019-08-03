# ----------------------------------------------------------------------------
# Author:  Nicolas P. Rougier
# License: BSD
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from datetime import datetime
from dateutil.relativedelta import relativedelta


def calmap(ax, year, data):
    ax.tick_params('x', length=0, labelsize="medium", which='major')
    ax.tick_params('y', length=0, labelsize="x-small", which='major')

    # Month borders
    xticks, labels = [], []
    start = datetime(year,1,1).weekday()
    for month in range(1,13):
        first = datetime(year, month, 1)
        last = first + relativedelta(months=1, days=-1)

        y0 = first.weekday()
        y1 = last.weekday()
        x0 = (int(first.strftime("%j"))+start-1)//7
        x1 = (int(last.strftime("%j"))+start-1)//7

        P = [ (x0,   y0), (x0,    7),  (x1,   7),
              (x1,   y1+1), (x1+1,  y1+1), (x1+1, 0),
              (x0+1,  0), (x0+1,  y0) ]
        xticks.append(x0 +(x1-x0+1)/2)
        labels.append(first.strftime("%b"))
        poly = Polygon(P, edgecolor="black", facecolor="None",
                       linewidth=1, zorder=20, clip_on=False)
        ax.add_artist(poly)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(labels)
    ax.set_yticks(0.5 + np.arange(7))
    ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    ax.set_title("{}".format(year), weight="semibold")
    
    # Clearing first and last day from the data
    valid = datetime(year, 1, 1).weekday()
    data[:valid,0] = np.nan
    valid = datetime(year, 12, 31).weekday()
    # data[:,x1+1:] = np.nan
    data[valid+1:,x1] = np.nan

    # Showing data
    ax.imshow(data, extent=[0,53,0,7], zorder=10, vmin=-1, vmax=1,
              cmap="RdYlBu", origin="lower", alpha=.75)


fig = plt.figure(figsize=(8,4.5), dpi=100)
X = np.linspace(-1,1, 53*7)

ax = plt.subplot(311, xlim=[0,53], ylim=[0,7], frameon=False, aspect=1)
I = 1.2 - np.cos(X.ravel()) + np.random.normal(0,.2, X.size)
calmap(ax, 2017, I.reshape(53,7).T)

ax = plt.subplot(312, xlim=[0,53], ylim=[0,7], frameon=False, aspect=1)
I = 1.1 - np.cos(X.ravel()) + np.random.normal(0,.2, X.size)
calmap(ax, 2018, I.reshape(53,7).T)

ax = plt.subplot(313, xlim=[0,53], ylim=[0,7], frameon=False, aspect=1)
I = 1.0 - np.cos(X.ravel()) + np.random.normal(0,.2, X.size)
calmap(ax, 2019, I.reshape(53,7).T)


plt.tight_layout()
plt.savefig("calendar-heatmap.png", dpi=300)
plt.savefig("calendar-heatmap.pdf", dpi=600)
plt.show()

