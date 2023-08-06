#
# Copyright (c) 2021 by Delphix. All rights reserved.
#
from dxi._lib import dx_logging as log
from dxi._lib.dxi_constants import VirtualOps
from dxi.database._mixins._dxi_db_operations import _DBOperationsMixin
from dxi.database._mixins._dxi_delete import _DeleteMixin
from dxi.database._mixins._dxi_provision_vdb import _ProvisionVDBMixin
from dxi.database._mixins._dxi_refresh import _RefreshMixin
from dxi.database._mixins._dxi_rewind import _RewindMixin
from dxi.dxi_tool_base import DXIBase


class DXIVdbConstants(object):
    """
    Define constants for DXIVDB class
    """

    SINGLE_THREAD = False
    POLL = 20
    CONFIG = "../../dxi-data/config/dxtools.conf"
    LOG_FILE_PATH = "../../dxi-data/logs/"
    ENGINE_ID = "default"
    TIME_STAMP_TYPE = "SNAPSHOT"
    TIME_STAMP = "LATEST"
    TIME_FLOW = None
    PARALLEL = 5
    FORCE = False
    TYPE = "vdb"
    DB_TYPE = None


class DXIVdb(
    DXIBase,
    _RefreshMixin,
    _DeleteMixin,
    _RewindMixin,
    _ProvisionVDBMixin,
    _DBOperationsMixin,
):
    """
    Implement operations for vdb datasets
    """

    def __init__(
        self,
        engine=DXIVdbConstants.ENGINE_ID,
        single_thread=DXIVdbConstants.SINGLE_THREAD,
        poll=DXIVdbConstants.POLL,
        config=DXIVdbConstants.CONFIG,
        log_file_path=DXIVdbConstants.LOG_FILE_PATH,
        parallel=DXIVdbConstants.PARALLEL,
    ):
        """
          :param engine: An Identifier of Delphix engine in dxtools.conf.
          :type engine: `str`
          :param single_thread: Run as a single thread.
                 False if running multiple threads.
          :type single_thread: `bool`
          :param poll: The number of seconds to wait between job polls
          :type poll: `int`
          :param config: The path to the dxtools.conf file
          :type config: `str`
          :param log_file_path: The path to the logfile you want to use.
          :type log_file_path: `str`
          :param all_dbs: Run against all database objects
          :type all_dbs: `bool`
        """
        super().__init__(
            poll=poll,
            config=config,
            log_file_path=log_file_path,
            single_thread=single_thread,
            engine=engine,
            module_name=__name__,
            parallel=parallel,
        )
        self.vdb = ""
        self.time_stamp_type = ""
        self.time_stamp = ""
        self.time_flow = ""
        self.name = ""
        self.force = ""
        self.type = ""
        self.db_type = ""
        self.source_db = ""
        self.group = ""
        self.db_type = ""
        self.env_name = ""
        self.mntpoint = ""
        self.timestamp = ""
        self.timestamp_type = ""
        self.pre_refresh = ""
        self.post_refresh = ""
        self.pre_rollback = ""
        self.post_rollback = ""
        self.configure_clone = ""
        self.envinst = ""
        self.action = ""

    def refresh(
        self,
        name,
        time_stamp_type=DXIVdbConstants.TIME_STAMP_TYPE,
        time_stamp=DXIVdbConstants.TIME_STAMP,
        time_flow=DXIVdbConstants.TIME_FLOW,
    ):
        """
        Refresh a Delphix VDB

        :param name: VDBs name
        :type name: `str`
        :param time_stamp_type: Either SNAPSHOT or TIME
        :type time_stamp_type: `str`
        :param time_stamp: The Delphix semantic for the point in time on
            the source from which you want to refresh your VDB.
        :type time_stamp: `str`
        :param time_flow: Name of the timeflow to refresh a VDB
        """
        try:
            self.vdb = name
            self.time_stamp_type = time_stamp_type
            self.time_stamp = time_stamp
            self.time_flow = time_flow
            self._execute_operation(self._refresh_helper)
            return True
        except (Exception, BaseException):
            return False

    def delete(self, name, db_type="vdb", force=False):
        """
        Deletes a VDB or a list of VDBs from an engine

        :param name: Colon[:] separated names of the VDBs/dSources to delete.
        :type name: `str`
        :param db_type: Type of object being deleted. vdb | dsource
        :type db_type: `str`
        :param force: To force delete the objects
        :type force: `bool`
        """
        try:
            self.name = name
            self.force = force
            self.db_type = db_type
            self._execute_operation(self._delete_main_workflow)
            return True
        except (Exception, BaseException):
            return False

    def rewind(
        self,
        name,
        time_stamp_type=DXIVdbConstants.TIME_STAMP_TYPE,
        time_stamp=DXIVdbConstants.TIME_STAMP,
        database_type=None,
    ):
        """
        Rewind the given vdb

        :param name: VDBs name
        :type name: `str`
        :param time_stamp_type: Either SNAPSHOT or TIME
        :type time_stamp_type: `str`
        :param time_stamp: The Delphix semantic for the point in time on
                the source from which you want to refresh your VDB.
          :type time_stamp: `str`
          :param database_type: Type of database: oracle, mssql, ase, vfiles
          :type database_type: `str`
        """
        self.vdb = name
        self.time_stamp_type = time_stamp_type
        self.time_stamp = time_stamp
        self.db_type = database_type
        try:
            self._execute_operation(self._rewind_helper)
            return True
        except Exception:
            print("here")
            return False

    def provision(
        self,
        target_grp,
        source_db,
        db,
        db_type,
        env_name,
        prerefresh=False,
        postrefresh=False,
        prerollback=False,
        postrollback=False,
        configure_clone=False,
        timestamp_type="SNAPSHOT",
        timestamp="LATEST",
        mntpoint="/mnt/ingest",
        envinst=None,
    ):
        """
        To ingest vdb
        """

        self.source_db = source_db
        self.name = db
        self.group = target_grp
        self.db_type = db_type
        self.env_name = env_name
        self.mntpoint = mntpoint
        self.timestamp = timestamp
        self.timestamp_type = timestamp_type
        self.pre_refresh = prerefresh
        self.post_refresh = postrefresh
        self.pre_rollback = prerollback
        self.post_rollback = postrollback
        self.configure_clone = configure_clone
        self.envinst = envinst
        try:
            self._execute_operation(self._provision_vdb_helper)
            return True
        except Exception:
            return False

    def list(self):
        """
        List datasets on an engine
        """
        self.action = VirtualOps.LIST
        try:
            self._execute_operation(self._db_operation_helper)
            log.print_debug("End of Execution")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"listing the datasets: {repr(err)}"
            )
            return False

    def start(self, name, group=None):
        """
        Start a Virtual dataset by name
        """
        self.action = VirtualOps.START
        self.name = name
        self.group = group
        try:
            self._execute_operation(self._db_operation_helper)
            log.print_debug("End of Execution")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"starting the virtual dataset: {repr(err)}"
            )
            return False

    def stop(self, name, group=None):
        """
        Stop a Virtual dataset by name
        """
        self.action = VirtualOps.STOP
        self.name = name
        self.group = group
        try:
            self._execute_operation(self._db_operation_helper)
            log.print_debug("End of Execution")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"stoping the virtual dataset: {repr(err)}"
            )
            return False

    def enable(self, name, group=None):
        """
        Enable a Virtual dataset by name
        """
        self.action = VirtualOps.ENABLE
        self.name = name
        self.group = group
        try:
            self._execute_operation(self._db_operation_helper)
            log.print_debug("End of Execution")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"enabling the virtual dataset: {repr(err)}"
            )
            return False

    def disable(self, name, group=None, force=False):
        """
        Disable a Virtual dataset by name
        """
        self.action = VirtualOps.DISABLE
        self.name = name
        self.group = group
        self.force = force
        try:
            self._execute_operation(self._db_operation_helper)
            log.print_debug("End of Execution")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"disabling the virtual dataset: {repr(err)}"
            )
            return False
