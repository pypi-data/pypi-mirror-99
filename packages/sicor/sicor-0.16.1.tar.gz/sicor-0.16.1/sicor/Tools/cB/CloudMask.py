from .cB import S2cB
from .classical_bayesian import ClassicalBayesian, ToClassifierDef, get_clf_functions
from .classical_bayesian import read_classical_bayesian_from_hdf5_file
from pkg_resources import resource_filename, Requirement, DistributionNotFound
from os.path import dirname, join, isfile
import logging
import numpy as np
import json
import pickle
import gdown
import h5py


class CloudMask(S2cB):
    def __init__(self, persistence_file=None, processing_tiles=10,
                 novelty_detector=None, logger=None):
        """ Get Cloud Detection based on classical Bayesian approach

        :param persistence_file: if None, use internal file, else give file name to persistence file
        :param processing_tiles: in order so save memory, the processing can be done in tiles
        :param logger: None or logger instance
        :return: CloudMask instance
        """
        from sklearn.svm import OneClassSVM  # import here to avoid static TLS ImportError

        logger = logger or logging.getLogger(__name__)

        if persistence_file is None:
            persistence_file = "data/cld_mask_20160321_s2.h5"
            try:
                fn = resource_filename(Requirement.parse("sicor"), persistence_file)
            except DistributionNotFound:
                fn = join(dirname(__file__), persistence_file)
                if isfile(fn) is False:
                    raise FileNotFoundError(persistence_file)
            else:
                if isfile(fn) is False:
                    fn = join(dirname(__file__), persistence_file)
                    if isfile(fn) is False:
                        raise FileNotFoundError(persistence_file)
            self.persistence_file = fn
        else:
            self.persistence_file = persistence_file

        data = read_classical_bayesian_from_hdf5_file(filename=self.persistence_file)
        cb_clf = ClassicalBayesian(logger=logger, mk_clf=ToClassifierDef(
            clf_functions=get_clf_functions(), **data["kwargs_mk_clf"]), **data["kwargs_cb"])

        if novelty_detector is not None:
            file_ext = novelty_detector.split(".")[-1]
            if file_ext == "json":
                with open(novelty_detector, "r") as fl:
                    nvc, ncv_clf = (lambda nvc_data: (
                        OneClassSVM(**nvc_data["params"]).fit(np.array(nvc_data["data"], dtype=float)),
                        nvc_data["clf"]
                    ))(json.load(fl))
            elif file_ext == "pkl":
                try:
                    with open(novelty_detector, "rb") as fl:
                        nvc = pickle.load(fl)
                        ncv_clf = pickle.load(fl)
                except (ModuleNotFoundError, AttributeError, KeyError):
                    # download training data base for novelty detector from google drive
                    logger.info("Novelty detector has to be updated with a newer version of scikit-learn.")
                    logger.info("Download training data base from google drive.")
                    url = "https://drive.google.com/uc?export=download&id=1PlJ84GGbQXM5NNSmkOn2Mg3WMy1UbPgI"
                    db_nv_fn = "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.h5"
                    db_nv_path = novelty_detector.split("noclear")[0] + db_nv_fn
                    gdown.download(url, db_nv_path, quiet=False)

                    # retrain novelty detector
                    logger.info("Retrain novelty detector with updated version of scikit-learn.")
                    from sklearn.ensemble import RandomForestClassifier

                    with h5py.File(db_nv_path, "r") as h5f:
                        nv = RandomForestClassifier(**dict(h5f["xx"].attrs.items()))
                        nv.fit(X=h5f["xx"], y=h5f["yy"])
                        bf = json.loads(h5f.attrs["clf"])

                        with open(novelty_detector, "wb") as fl:
                            pickle.dump(nv, fl)
                            pickle.dump({"id": [tuple(ids) for ids in bf["id"]], "fk": [str(ids) for ids in bf["fk"]]},
                                        fl)

                    # reload novelty detector
                    with open(novelty_detector, "rb") as fl:
                        nvc = pickle.load(fl)
                        ncv_clf = pickle.load(fl)
            else:
                raise ValueError("Novelty detector file type not implemented")

            test_1 = ncv_clf["fk"] == cb_clf.mk_clf.classifiers_fk
            test_2 = [list(ll) for ll in ncv_clf["id"]] == [list(ll) for ll in cb_clf.mk_clf.classifiers_id]
            if test_1 is not True or test_2 is not True:
                raise ValueError(
                    "The novelty detection in %s is not compatible with the classifier." % novelty_detector)
            else:
                cb_clf.nvc = nvc

        super().__init__(cb_clf=cb_clf,
                         mask_legend=data["mask_legend"],
                         clf_to_col=data["clf_to_col"],
                         processing_tiles=processing_tiles,
                         logger=logger)
