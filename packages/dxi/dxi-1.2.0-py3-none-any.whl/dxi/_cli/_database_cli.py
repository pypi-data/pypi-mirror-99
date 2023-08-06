#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.database.dxi_ingest import DXIProvisionDsource
from dxi.database.dxi_ingest import DXIProvisionDsourceConstants
from dxi.database.dxi_provision import DXIVdb
from dxi.database.dxi_provision import DXIVdbConstants


@click.group()
def database():
    """
    Delphix Dsource, VDB and vFile operations
    """
    pass


# Refresh command
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to refresh",
    default=None,
)
@click.option(
    "--time_stamp",
    default="LATEST",
    help='''
        The Delphix semantic for the point in time on the source
         from which you want to refresh your VDB.
         Formats: latest point in time or snapshot: LATEST
        point in time: "YYYY-MM-DD HH24:MI:SS"
        snapshot name: "@YYYY-MM-DDTHH24:MI:SS.ZZZ"
        snapshot time from GUI: "YYYY-MM-DD HH24:MI"''',
)
@click.option(
    "--time_stamp-type",
    help="The type of timestamp you are specifying",
    default="SNAPSHOT",
    type=click.Choice(["TIME", "SNAPSHOT"]),
)
@click.option(
    "--time_flow", help="Name of the timeflow to refresh a VDB", default=None
)
@click.option("--engine", default=DXIVdbConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
def refresh(
    name,
    time_stamp_type,
    time_stamp,
    engine,
    single_thread,
    time_flow,
    poll,
    config,
    log_path,
    parallel,
):
    """
Refresh a Delphix VDB
    """

    obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        log_file_path=log_path,
        parallel=parallel,
    )

    boolean_based_system_exit(
        obj.refresh(
            name,
            time_stamp_type=time_stamp_type,
            time_stamp=time_stamp,
            time_flow=time_flow,
        )
    )


# Rewind Command
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to rewind",
    default=None,
)
@click.option(
    "--time_stamp",
    default="LATEST",
    help='''
        The Delphix semantic for the point in time on the source
        from which you want to refresh your VDB.
         Formats: latest point in time or snapshot: LATEST
        point in time: "YYYY-MM-DD HH24:MI:SS"
        snapshot name: "@YYYY-MM-DDTHH24:MI:SS.ZZZ"
        snapshot time from GUI: "YYYY-MM-DD HH24:MI"''',
)
@click.option(
    "--timestamp-type",
    help="The type of timestamp you are specifying",
    default="SNAPSHOT",
    type=click.Choice(["TIME", "SNAPSHOT"]),
)
@click.option(
    "--database_type",
    help="Type of database: oracle, mssql, ase, vfiles",
    default=None,
)
@click.option("--engine", default=DXIVdbConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
def rewind(
    name,
    timestamp_type,
    time_stamp,
    engine,
    single_thread,
    database_type,
    poll,
    config,
    log_path,
    parallel,
):
    """
Rewinds a VDB
    """

    obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        log_file_path=log_path,
        parallel=parallel,
    )
    boolean_based_system_exit(
        obj.rewind(
            name,
            time_stamp_type=timestamp_type,
            time_stamp=time_stamp,
            database_type=database_type,
        )
    )


# Delete command
@database.command()
@click.option(
    "--name",
    default=None,
    help="Name of dataset(s) in Delphix to execute against",
)
@click.option(
    "--db-type",
    default=DXIVdbConstants.TYPE,
    help="Type of the dataset to delete. vdb | dsource",
)
@click.option(
    "--force",
    is_flag=True,
    default=DXIVdbConstants.FORCE,
    help="Force delete the dataset",
)
@click.option("--engine", default=DXIVdbConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log_path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
def delete(
    name,
    db_type,
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_path,
    force,
):
    """
    Delete a Delphix dSource or VDB
    """
    obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        log_file_path=log_path,
        parallel=parallel,
    )
    boolean_based_system_exit(obj.delete(name, db_type=db_type, force=force))


#############################################
# DB Operations

# db-list
@database.command()
@click.option(
    "--engine",
    default=DXIVdbConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
def list(engine, single_thread, parallel, poll, config, log_path):
    """
    List all datasets on an engine
    """
    obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        log_file_path=log_path,
        parallel=parallel,
    )
    boolean_based_system_exit(obj.list())


# db-start
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--engine",
    default=DXIVdbConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
def start(
    name, group, engine, single_thread, parallel, poll, config, log_path
):
    """
    Starts a virtual dataset by name and group
    """
    ops_obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        parallel=parallel,
        log_file_path=log_path,
    )
    boolean_based_system_exit(ops_obj.start(name=name, group=group))


# db-stop
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--engine",
    default=DXIVdbConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
def stop(name, group, engine, single_thread, parallel, poll, config, log_path):
    """
    Stop a virtual dataset by name and group (optional)
    """
    ops_obj = DXIVdb(
        engine=engine,
        poll=poll,
        config=config,
        parallel=parallel,
        log_file_path=log_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(ops_obj.stop(name=name, group=group))


# db-enable
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--engine",
    default=DXIVdbConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
def enable(
    name, group, engine, single_thread, parallel, poll, config, log_path
):
    """
    Enable a virtual dataset by name and group(optional)
    """
    ops_obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        parallel=parallel,
        log_file_path=log_path,
    )
    boolean_based_system_exit(ops_obj.enable(name=name, group=group))


# db-disable
@database.command()
@click.option(
    "--name",
    required=True,
    help="Name of the virtual dataset to start",
    default=None,
)
@click.option("--group", help="Group where the dataset resides", default=None)
@click.option(
    "--force",
    is_flag=True,
    help="Force disable a virtual dataset",
    default=None,
)
@click.option(
    "--engine",
    default=DXIVdbConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIVdbConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIVdbConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIVdbConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
def disable(
    name, group, force, engine, single_thread, parallel, poll, config, log_path
):
    """
    Disable a virtual dataset by name and group(optional)
    """
    ops_obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        log_file_path=log_path,
        parallel=parallel,
    )
    boolean_based_system_exit(
        ops_obj.disable(name=name, group=group, force=force)
    )


# Provision dSource
#
@database.command()
@click.option(
    "--source-name", required=True, help="Name of the dSource to create"
)
@click.option(
    "--single-thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db-type", help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option(
    "--db-passwd", help="Password for db_user", required=True, default=False
)
@click.option(
    "--db-user",
    help="Username of the dSource DB",
    required=True,
    default=False,
)
@click.option(
    "--group", help="Group name for this dSource", required=True, default=False
)
@click.option(
    "--env-name",
    help="Name of the Delphix environment",
    required=True,
    default=False,
)
@click.option(
    "--ip-addr", help="IP Address of the dSource", required=True, default=False
)
@click.option(
    "--db-type",
    help="dSource type. mssql, sybase, oracle or oramt",
    required=True,
    default=None,
)
@click.option("--logsync", help="Enable or disable logsync", default=True)
@click.option(
    "--envinst",
    help="Location of the installation path of the DB",
    required=True,
    default=None,
)
@click.option("--source-user", help="Environment username", default="delphix")
@click.option("--sync-mode", help="sync mode", default="UNDEFINED")
@click.option(
    "--rman-channels",
    help="Configures the number of Oracle RMAN Channels",
    default=2,
)
@click.option(
    "--files-per-set",
    help="Configures how many files per set for Oracle RMAN",
    default=5,
)
@click.option(
    "--num-connections",
    help="Number of connections for Oracle RMAN",
    default=5,
)
@click.option(
    "--port-num", help="Port number for the Oracle Listener", default=5
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.", type=click.INT
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIProvisionDsourceConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIProvisionDsourceConstants.LOG_FILE_PATH,
)
@click.option(
    "--version",
    help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True,
)
@click.option("--source-user", help="Environment username", default="delphix")
@click.option("--stage-user", help="Stage username", default="delphix")
@click.option("--stage-repo", help="Stage repository", default="delphix")
@click.option(
    "--stage-instance", help="Name of the PPT instance", default=None
)
@click.option("--stage-env", help="Name of the PPT server", default=None)
@click.option(
    "--backup-user-pwd",
    help="Password of the shared backup path",
    default=None,
)
@click.option(
    "--backup-user", help="User of the shared backup path", default=None
)
@click.option(
    "--use-recent-backup",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=True,
)
@click.option(
    "--validated-sync-mode",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default="TRANSACTION_LOG",
)
@click.option(
    "--delphix-managed",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=True,
)
@click.option(
    "--initial-load-type",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=None,
)
@click.option(
    "--backup-path", help="Path to the ASE/MSSQL backups", default=None
)
@click.option("--engine", default=DXIProvisionDsourceConstants.ENGINE_ID)
def ingest(
    engine,
    ip_addr,
    env_name,
    group,
    source_name,
    db_user,
    db_passwd,
    envinst,
    db_type,
    num_connections,
    log_path,
    logsync,
    single_thread,
    files_per_set,
    rman_channels,
    port_num,
    sync_mode,
    source_user,
    parallel,
    poll,
    config,
    version,
    stage_user,
    stage_repo,
    stage_instance,
    stage_env,
    backup_user_pwd,
    backup_user,
    use_recent_backup,
    initial_load_type,
    validated_sync_mode,
    delphix_managed,
    backup_path,
):
    """
    Provision a Delphix dSource
    """
    obj = DXIProvisionDsource(
        engine=engine,
        single_thread=single_thread,
        parallel=parallel,
        poll=poll,
        config=config,
        version=version,
        log_file_path=log_path,
    )
    obj.ingest(
        ip_addr=ip_addr,
        env_name=env_name,
        dx_group=group,
        dsource_name=source_name,
        db_user=db_user,
        db_passwd=db_passwd,
        db_install_path=envinst,
        db_type=db_type,
        num_connections=num_connections,
        logsync=logsync,
        files_per_set=files_per_set,
        rman_channels=rman_channels,
        port_num=port_num,
        sync_mode=sync_mode,
        source_user=source_user,
        stage_user=stage_user,
        stage_repo=stage_repo,
        stage_instance=stage_instance,
        stage_env=stage_env,
        backup_loc_passwd=backup_user_pwd,
        backup_loc_user=backup_user,
        load_from_backup=use_recent_backup,
        initial_load_type=initial_load_type,
        validated_sync_mode=validated_sync_mode,
        delphix_managed=delphix_managed,
        backup_path=backup_path,
    )


# MSSQL dSource
@database.command()
@click.option("--dsource_name", help="Name of the dSource to create")
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db_type", help="The type of VDB. oracle, oramt, mssql, ase or vfiles"
)
@click.option("--db_passwd", help="Password for db_user", default=False)
@click.option("--db_user", help="Username of the dSource DB", default=False)
@click.option(
    "--dx_group",
    help="Delphix group name of where the dSource will be linked",
    default=False,
)
@click.option(
    "--env-name", help="Name of the Delphix environment", default=False
)
@click.option(
    "--envinst",
    help="The identifier of the instance in Delphix. ex. LINUXTARGET",
    default=False,
)
@click.option(
    "--db_type",
    help="dSource type. mssql, sybase, oracle or oramt",
    default=None,
)
@click.option("--logsync", help="Enable or disable logsync", default=True)
@click.option(
    "--backup-path", help="Path to the ASE/MSSQL backups", default=None
)
@click.option(
    "--sync_mode",
    help="\bMSSQL validated sync mode \n"
    "TRANSACTION_LOG|FULL_OR_DIFFERENTIAL|FULL|NONE",
    default="FULL",
)
@click.option("--source_user", help="Environment username", default="delphix")
@click.option("--stage-user", help="Stage username", default="delphix")
@click.option("--stage-repo", help="Stage repository", default="delphix")
@click.option(
    "--stage-instance", help="Name of the PPT instance", default=None
)
@click.option("--stage-env", help="Name of the PPT server", default=None)
@click.option(
    "--backup-user-pwd",
    help="Password of the shared backup path",
    default=None,
)
@click.option(
    "--backup-user", help="User of the shared backup path", default=None
)
@click.option(
    "--use-recent-backup",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=True,
)
@click.option(
    "--validated_sync_mode",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default="TRANSACTION_LOG",
)
@click.option(
    "--delphix_managed",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=True,
)
@click.option(
    "--initial_load_type",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=None,
)
@click.option("--logsync_mode", help="logsync mode", default=None)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.", type=click.INT
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIProvisionDsourceConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIProvisionDsourceConstants.LOG_FILE_PATH,
)
@click.option(
    "--version",
    help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True,
)
@click.option(
    "--initial_load_type",
    help="Delphix will try to load the most recent backup. MSSQL only",
    default=None,
)
@click.option(
    "--version",
    help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True,
)
@click.option("--engine", default=DXIProvisionDsourceConstants.ENGINE_ID)
def link_mssql(
    engine,
    env_name,
    dx_group,
    dsource_name,
    db_user,
    db_passwd,
    db_type,
    logsync,
    single_thread,
    backup_path,
    source_user,
    stage_user,
    stage_repo,
    stage_instance,
    logsync_mode,
    stage_env,
    backup_user_pwd,
    backup_user,
    delphix_managed,
    use_recent_backup,
    initial_load_type,
    envinst,
    parallel,
    poll,
    config,
    validated_sync_mode,
    version,
    log_path,
):
    """
    Provision a Delphix MSSQL dSource
    """
    obj = DXIProvisionDsource(
        engine=engine,
        single_thread=single_thread,
        parallel=parallel,
        poll=poll,
        config=config,
        version=version,
        log_file_path=log_path,
    )
    obj.ingest(
        env_name=env_name,
        dx_group=dx_group,
        dsource_name=dsource_name,
        db_user=db_user,
        db_passwd=db_passwd,
        db_type=db_type,
        logsync=logsync,
        backup_path=backup_path,
        source_user=source_user,
        stage_user=stage_user,
        stage_repo=stage_repo,
        stage_instance=stage_instance,
        stage_env=stage_env,
        logsync_mode=logsync_mode,
        backup_loc_passwd=backup_user_pwd,
        backup_loc_user=backup_user,
        load_from_backup=use_recent_backup,
        validated_sync_mode=validated_sync_mode,
        delphix_managed=delphix_managed,
        initial_load_type=initial_load_type,
        envinst=envinst,
    )


# Provision a Dephix VDB
@database.command()
@click.option(
    "--group",
    required=True,
    help="The group into which Delphix will place the VDB",
)
@click.option("--source-name", required=True, help="The source database")
@click.option(
    "--db-name", required=True, help="The name you want to give the database"
)
@click.option(
    "--env-name",
    required=True,
    help="The name of the Target environment in Delphix",
)
@click.option(
    "--single_thread",
    help="Run as a single thread. False if running multiple threads.",
    default=False,
    type=click.BOOL,
)
@click.option(
    "--db-type",
    required=True,
    help="The type of VDB. oracle, oramt, mssql, ase or vfiles",
)
@click.option(
    "--prerefresh", help="Pre-Hook commands before a refresh", default=False
)
@click.option(
    "--postrefresh", help="Post-Hook commands after a refresh", default=False
)
@click.option(
    "--prerollback", help="Pre-Hook commands before a rollback", default=False
)
@click.option(
    "--postrollback", help="Post-Hook commands after a rollback", default=False
)
@click.option(
    "--configure_clone", help="Configure Clone commands", default=False
)
@click.option(
    "--envinst",
    help="The identifier of the instance in Delphix.",
    default=None,
)
@click.option(
    "--timestamp-type",
    help="The type of timestamp you are specifying. TIME or SNAPSHOT",
    default="SNAPSHOT",
)
@click.option(
    "--timestamp",
    help="\bThe Delphix semantic for the point in time\n "
    "from which you want to ingest your VDB.",
    default="LATEST",
)
@click.option(
    "--mntpoint",
    help="The identifier of the instance in Delphix.",
    default="/mnt/ingest",
)
@click.option(
    "--parallel", help="Limit number of jobs to maxjob.", type=click.INT
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=10,
    type=click.INT,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIVdbConstants.CONFIG,
)
@click.option(
    "--log-path",
    help="The path to the logfile you want to use.",
    default=DXIVdbConstants.LOG_FILE_PATH,
)
@click.option(
    "--version",
    help="Show version.",
    type=click.BOOL,
    is_flag=True,
    default=True,
)
@click.option("--engine", default=DXIVdbConstants.ENGINE_ID)
def provision(
    engine,
    source_name,
    db_name,
    db_type,
    group,
    mntpoint,
    env_name,
    timestamp,
    timestamp_type,
    prerefresh,
    postrefresh,
    prerollback,
    postrollback,
    configure_clone,
    envinst,
    single_thread,
    parallel,
    poll,
    config,
    log_path,
    version,
):
    """
    Provision a Delphix VDB
    """
    obj = DXIVdb(
        engine=engine,
        single_thread=single_thread,
        poll=poll,
        config=config,
        log_file_path=log_path,
        parallel=parallel,
    )
    obj.provision(
        group,
        source_name,
        db_name,
        db_type,
        env_name,
        timestamp=timestamp,
        timestamp_type=timestamp_type,
        prerefresh=prerefresh,
        postrefresh=postrefresh,
        prerollback=prerollback,
        postrollback=postrollback,
        configure_clone=configure_clone,
        envinst=envinst,
        mntpoint=mntpoint,
    )


if __name__ == "__main__":
    provision()
