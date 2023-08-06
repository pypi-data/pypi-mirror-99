import numpy as np

from kolibri.evaluation.metrics import compute_at_thresholds
from kolibri.evaluation.plot.util import set_default_ax


@set_default_ax
def metrics_at_thresholds(fn, y_true, y_score, n_thresholds=10, start=0.0,
                          ax=None):
    """Plot metrics at increasing thresholds
    """
    th, m = compute_at_thresholds(fn, y_true, y_score, n_thresholds,
                                  start)

    ax.plot(th, np.array(m).T, '.--')
    ax.legend([fn_.__name__ for fn_ in fn])
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Metric value')
    ax.grid()

    return ax
