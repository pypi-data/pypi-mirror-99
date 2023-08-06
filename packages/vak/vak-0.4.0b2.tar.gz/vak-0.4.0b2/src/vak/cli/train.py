from pathlib import Path
import shutil

from .. import config
from .. import core
from .. import logging
from ..paths import generate_results_dir_name_as_path
from ..timenow import get_timenow_as_str


def train(toml_path):
    """train models using training set specified in config.toml file.
    Function called by command-line interface.

    Parameters
    ----------
    toml_path : str, Path
        path to a configuration file in TOML format.

    Returns
    -------
    None

    Trains models, saves results in new directory within root_results_dir specified
    in config.toml file, and adds path to that new directory to config.toml file.
    """
    toml_path = Path(toml_path)
    cfg = config.parse.from_toml_path(toml_path)

    if cfg.train is None:
        raise ValueError(
            f'train called with a config.toml file that does not have a TRAIN section: {toml_path}'
        )

    # ---- set up directory to save output -----------------------------------------------------------------------------
    results_path = generate_results_dir_name_as_path(cfg.train.root_results_dir)
    results_path.mkdir(parents=True)
    # copy config file into results dir now that we've made the dir
    shutil.copy(toml_path, results_path)

    # ---- set up logging ----------------------------------------------------------------------------------------------
    logger = logging.get_logger(log_dst=results_path,
                                caller='train',
                                timestamp=get_timenow_as_str(),
                                logger_name=__name__)
    logger.info('Logging results to {}'.format(results_path))

    model_config_map = config.models.map_from_path(toml_path, cfg.train.models)

    core.train(model_config_map,
               cfg.train.csv_path,
               cfg.prep.labelset,
               cfg.dataloader.window_size,
               cfg.train.batch_size,
               cfg.train.num_epochs,
               cfg.train.num_workers,
               results_path=results_path,
               spect_key=cfg.spect_params.spect_key,
               timebins_key=cfg.spect_params.timebins_key,
               normalize_spectrograms=cfg.train.normalize_spectrograms,
               shuffle=cfg.train.shuffle,
               val_step=cfg.train.val_step,
               ckpt_step=cfg.train.ckpt_step,
               patience=cfg.train.patience,
               device=cfg.train.device,
               logger=logger,
               )
