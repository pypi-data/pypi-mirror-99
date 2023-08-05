# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

from datetime import datetime
import warnings
from pyiron_base.generic.parameters import GenericParameters
from pyiron_base.job.generic import GenericJob
from pyiron_base.master.generic import GenericMaster
from pyiron_base.generic.util import deprecate

__author__ = "Jan Janssen"
__copyright__ = (
    "Copyright 2021, Max-Planck-Institut für Eisenforschung GmbH - "
    "Computational Materials Design (CM) Department"
)
__version__ = "1.0"
__maintainer__ = "Jan Janssen"
__email__ = "janssen@mpie.de"
__status__ = "development"
__date__ = "Jan 8, 2021"


class InteractiveWrapper(GenericMaster):
    def __init__(self, project, job_name):
        super(InteractiveWrapper, self).__init__(project, job_name)
        self._ref_job = None
        self.input = GenericParameters("parameters")

    @property
    def ref_job(self):
        """
        Get the reference job template from which all jobs within the ParallelMaster are generated.

        Returns:
            GenericJob: reference job
        """
        if self._ref_job is not None:
            return self._ref_job
        try:
            if isinstance(self[0], GenericJob):
                self._ref_job = self[0]
                return self._ref_job
            else:
                return None
        except IndexError:
            return None

    @ref_job.setter
    def ref_job(self, ref_job):
        """
        Set the reference job template from which all jobs within the ParallelMaster are generated.

        Args:
            ref_job (GenericJob): reference job
        """
        if not ref_job.server.run_mode.interactive:
            warnings.warn("Run mode of the reference job not set to interactive")
        self.append(ref_job)

    def set_input_to_read_only(self):
        """
        This function enforces read-only mode for the input classes, but it has to be implement in the individual
        classes.
        """
        self.input.read_only = True

    def validate_ready_to_run(self):
        """
        Validate that the calculation is ready to be executed. By default no generic checks are performed, but one could
        check that the input information is complete or validate the consistency of the input at this point.
        """
        self.ref_job.validate_ready_to_run()

    def check_setup(self):
        """
        Checks whether certain parameters (such as plane wave cutoff radius in DFT) are changed from the pyiron standard
        values to allow for a physically meaningful results. This function is called manually or only when the job is
        submitted to the queueing system.
        """
        try:
            self.ref_job.check_setup()
        except AttributeError:
            pass

    def ref_job_initialize(self):
        """

        """
        if len(self._job_name_lst) > 0:
            self._ref_job = self.pop(-1)
            if self._job_id is not None and self._ref_job._master_id is None:
                self._ref_job.master_id = self.job_id
                self._ref_job.server.cores = self.server.cores

    def to_hdf(self, hdf=None, group_name=None):
        """
        Store the InteractiveWrapper in an HDF5 file

        Args:
            hdf (ProjectHDFio): HDF5 group object - optional
            group_name (str): HDF5 subgroup name - optional
        """
        if self._ref_job is not None and self._ref_job.job_id is None:
            self.append(self._ref_job)
        super(InteractiveWrapper, self).to_hdf(hdf=hdf, group_name=group_name)
        with self.project_hdf5.open("input") as hdf5_input:
            self.input.to_hdf(hdf5_input)

    def from_hdf(self, hdf=None, group_name=None):
        """
        Restore the InteractiveWrapper from an HDF5 file

        Args:
            hdf (ProjectHDFio): HDF5 group object - optional
            group_name (str): HDF5 subgroup name - optional
        """
        super(InteractiveWrapper, self).from_hdf(hdf=hdf, group_name=group_name)
        with self.project_hdf5.open("input") as hdf5_input:
            self.input.from_hdf(hdf5_input)

    def collect_output(self):
        pass

    def collect_logfiles(self):
        pass

    def _db_entry_update_run_time(self):
        """

        Returns:

        """
        job_id = self.get_job_id()
        db_dict = {}
        start_time = self.project.db.get_item_by_id(job_id)["timestart"]
        db_dict["timestop"] = datetime.now()
        db_dict["totalcputime"] = (db_dict["timestop"] - start_time).seconds
        self.project.db.item_update(db_dict, job_id)

    def _finish_job(self):
        """

        Returns:

        """
        self.status.finished = True
        self._db_entry_update_run_time()
        self._logger.info(
            "{}, status: {}, monte carlo master".format(self.job_info_str, self.status)
        )
        self._calculate_successor()
        self.send_to_database()
        self.update_master()

    def __getitem__(self, item):
        """
        Get/ read data from the GenericMaster

        Args:
            item (str, slice): path to the data or key of the data object

        Returns:
            dict, list, float, int: data or data object
        """
        child_id_lst = self.child_ids
        child_name_lst = [
            self.project.db.get_item_by_id(child_id)["job"]
            for child_id in self.child_ids
        ]
        if isinstance(item, int):
            total_lst = child_name_lst + self._job_name_lst
            item = total_lst[item]
        return self._get_item_when_str(
            item=item, child_id_lst=child_id_lst, child_name_lst=child_name_lst
        )
