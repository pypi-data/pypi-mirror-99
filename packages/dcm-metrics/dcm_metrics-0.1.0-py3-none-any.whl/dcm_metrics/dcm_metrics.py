import logging
import time
from typing import Any, Callable

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
    measure_func: Callable[[], Any],
    connection_string: str,
    interval: float = 1.0,
):
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
        measurement = measure_func()
        _LOGGER.info('%s: %.2f', name, measurement)
        mmap.measure_float_put(measure, measurement)
        mmap.record()
        time.sleep(interval)
