import logging
import time
from typing import Any, Callable, List

from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
ch.setFormatter(formatter)
_LOGGER.addHandler(ch)

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder


def measure_to_azure(
    name: str,
    device_id: str,
    connection_string: str,
    measure_func: Callable[[], Any],
    measure_interval: float = 60.,
    aggregation_size: int = 1,
    aggregation_func: Callable[[List[float]], float] = lambda v: v[-1],
):
    """Retrieve measurements from measure_func and send them as metrics
    to Azure.

    :param name: name of the measurements - used for metric name
    :type name: str
    :param device_id: id of the device - used for metric name
    :type device_id: str
    :param connection_string: connection string to the Azure App Insights
    :type connection_string: str
    :param measure_func: a function that returns a single measurement
    :type measure_func: Callable[[], Any]
    :param measure_interval: interval between two measurements, defaults to 60.
    :type measure_interval: float, optional
    :param aggregation_size: how many measurements to aggregate before
     sending to App Insights, if set to 1 no aggregation occurs, defaults to 1
    :type aggregation_size: int
    :param aggregation_func: an aggregation function to use for aggregating
     measurement, defaults to lambda m: m[-1] (select last value)
    :type aggregation_func: Optional[Callable[[List[float]], float]], optional
    """
    if not isinstance(aggregation_size, int) or aggregation_size < 1:
        raise ValueError(
            f'aggregation_size must either an integer greater than one 1'
            f' or None, got {aggregation_size}'
        )

    if aggregation_size > 1 and aggregation_func is None:
        raise ValueError(
            'aggregation_func must not be None when'
            ' aggregation_size is > 1'
        )

    metric_name = f'{name}_{device_id}'

    measure = measure_module.MeasureFloat(
        name=metric_name,
        description="",
    )
    view = view_module.View(
        name=metric_name,
        description="",
        columns=[],
        measure=measure,
        aggregation=aggregation_module.LastValueAggregation(),
    )

    exporter = metrics_exporter.new_metrics_exporter(
        connection_string=connection_string,
        export_interval=1,
    )
    view_manager.register_exporter(exporter)

    view_manager.register_view(view)
    mmap = stats_recorder.new_measurement_map()

    while True:
        measurements = []
        for _ in range(aggregation_size):
            measurement = measure_func()
            _LOGGER.info('Measured %s: %.2f', name, measurement)
            measurements.append(measurement)
            time.sleep(measure_interval)
        _LOGGER.info(f'Aggregating {len(measurements)} measurements...')
        aggregated_value = aggregation_func(measurements)
        _LOGGER.info(
            'Sending aggregated value to AppInsights: %.2f...',
            aggregated_value,
        )
        mmap.measure_float_put(measure, aggregated_value)
        mmap.record()
