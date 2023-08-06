from cifsdk.client.http import HTTP as Client
from confuse import Subview
from multiprocessing import JoinableQueue
from queue import Empty
import threatbus
from threatbus_cif3.message_mapping import map_to_cif
from typing import Callable, List


"""CIFv3 application plugin for Threat Bus"""

plugin_name = "cif3"
workers: List[threatbus.StoppableWorker] = list()


class CIFPublisher(threatbus.StoppableWorker):
    """
    Reports / publishes Indicators to the given CIF endpoint.
    """

    def __init__(self, indicator_q: JoinableQueue, cif: Client, config: Subview):
        """
        @param indicator_q Publish all indicators from this queue to CIF
        @param cif The CIF client to use
        @config the plugin config
        """
        super(CIFPublisher, self).__init__()
        self.indicator_q = indicator_q
        self.cif = cif
        self.config = config

    def run(self):
        global logger
        if not self.cif:
            logger.error("CIF is not properly configured. Exiting.")
            return
        confidence = self.config["confidence"].as_number()
        if not confidence:
            confidence = 5
        tags = self.config["tags"].get(list)
        tlp = self.config["tlp"].get(str)
        group = self.config["group"].get(str)

        while self._running():
            try:
                indicator = self.indicator_q.get(block=True, timeout=1)
            except Empty:
                continue
            if not indicator:
                self.indicator_q.task_done()
                continue
            cif_mapped_intel = map_to_cif(
                indicator, confidence, tags, tlp, group, logger
            )
            if not cif_mapped_intel:
                self.indicator_q.task_done()
                continue
            try:
                logger.debug(f"Adding indicator to CIF {cif_mapped_intel}")
                self.cif.indicators_create(cif_mapped_intel)
            except Exception as err:
                logger.error(f"Error adding indicator to CIF {err}")
            finally:
                self.indicator_q.task_done()


def validate_config(config: Subview):
    assert config, "config must not be None"
    config["tags"].get(list)
    config["tlp"].get(str)
    config["confidence"].as_number()
    config["group"].get(str)
    config["api"].get(dict)
    config["api"]["host"].get(str)
    config["api"]["ssl"].get(bool)
    config["api"]["token"].get(str)


@threatbus.app
def run(
    config: Subview,
    logging: Subview,
    inq: JoinableQueue,
    subscribe_callback: Callable,
    unsubscribe_callback: Callable,
):
    global logger, workers
    logger = threatbus.logger.setup(logging, __name__)
    config = config[plugin_name]
    try:
        validate_config(config)
    except Exception as e:
        logger.fatal("Invalid config for plugin {}: {}".format(plugin_name, str(e)))

    remote, token, ssl = (
        config["api"]["host"].get(),
        config["api"]["token"].get(),
        config["api"]["ssl"].get(),
    )
    cif = None
    try:
        cif = Client(remote=remote, token=token, verify_ssl=ssl)
        cif.ping()
    except Exception as err:
        logger.error(
            f"Cannot connect to CIFv3 at {remote}, using SSL: {ssl}. Exiting plugin. {err}"
        )
        return

    indicator_q = JoinableQueue()
    topic = "stix2/indicator"
    subscribe_callback(topic, indicator_q)

    workers.append(CIFPublisher(indicator_q, cif, config))
    for w in workers:
        w.start()

    logger.info("CIF3 plugin started")


@threatbus.app
def stop():
    global logger, workers
    for w in workers:
        if not w.is_alive():
            continue
        w.stop()
        w.join()
    logger.info("CIF3 plugin stopped")
