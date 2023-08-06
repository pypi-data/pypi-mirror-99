#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# Aegis is your shield to protect you on the Brave New Web

# Python Imports
import argparse
import logging
import os
import pwd
import sys

# Extern Imports
import tornado.options
from tornado.options import define, options

# Project Imports
import aegis.stdlib
import aegis.build
import aegis.config

# Load project config via VIRTUAL_ENV and naming convention, or by calling virtualenv binary directly
venv = os.environ.get('VIRTUAL_ENV')
if venv:
    # Running from within a virtualenv
    repo_dir = os.path.dirname(venv)
    src_dir = os.path.join(repo_dir, os.path.split(repo_dir)[-1])
    sys.path.insert(0, src_dir)
    import config
elif sys.argv[0] == 'virtualenv/bin/aegis':
    # Running by calling the virtualenv binary directly
    repo_dir = os.getcwd()
    src_dir = os.path.join(repo_dir, os.path.split(repo_dir)[-1])
    sys.path.insert(0, src_dir)
    import config
elif sys.argv[0] == '/usr/local/bin/aegis':
    repo_dir = os.getcwd()
    if os.path.exists(os.path.join(repo_dir, '.git')):
        src_dir = os.path.join(repo_dir, os.path.split(repo_dir)[-1])
        sys.path.insert(0, src_dir)
        import config
    else:
        logging.error("Can't detect your app dir. Be in the source root, next to .git dir.")
        sys.exit(1)


# Create a new spinoff of aegis
def create(parser):
    args = parser.parse_args()
    if not args.appname or not args.domain:
        logging.error("aegis create requires --appname and --domain")
        sys.exit()
    app_name = args.appname[0]
    domain = args.domain[0]
    aegis.stdlib.logw("AEGIS CREATE  %s  %s" % (app_name, domain))
    aegis_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    src_dir = os.path.dirname(aegis_dir)
    template_vars = {'app_name': app_name, 'aegis_domain': domain}
    create_dir = os.path.join(src_dir, app_name)
    #aegis.stdlib.logw(create_dir, "CREATE DIR")
    #if os.path.exists(create_dir):
    #    logging.error("AEGIS     Sorry that directory exists already. Exiting.")
    #    sys.exit(1)
    if not os.path.exists(create_dir):
        os.mkdir(create_dir)
    create_etc_dir = os.path.join(create_dir, 'etc')
    if not os.path.exists(create_etc_dir):
        os.mkdir(create_etc_dir)
    # Now walk tmpl/etc
    tmpl_dir = os.path.join(aegis_dir, 'aegis', 'tmpl')
    for entry in os.walk(tmpl_dir):
        basedir, subdirs, files = entry
        rebasedir = create_dir + basedir[basedir.find('aegis/tmpl')+10:]
        if rebasedir.endswith('/aegis'):
            rebasedir = rebasedir[:-6] + '/' + app_name
        if not os.path.exists(rebasedir):
            os.mkdir(rebasedir)
        for filename in files:
            filepath = os.path.join(basedir, filename)
            with open(filepath, 'r') as fd:
                # iterate a dictionary of vars and replace vars
                output = fd.read()
                for var, val in template_vars.items():
                    output = output.replace('{{%s}}' % var, val)
                rebase_filename = filename
                if filename == 'aegis.py':
                    rebase_filename = app_name + '.py'
                if filename == 'aegis.conf':
                    rebase_filename = app_name + '.conf'
                if filename == 'aegis_dev.conf':
                    rebase_filename = app_name + '_dev.conf'
                if filename == 'aegis_prod.conf':
                    rebase_filename = app_name + '_prod.conf'
                rebasepath = os.path.join(rebasedir, rebase_filename)
                with open(rebasepath, 'w') as writefd:
                    writefd.write(output)
    print ("GREAT SUCCESS!!")
    # git create and push
    # virtualenv and setup.py
    # <appname>/<appname>.py


# Diff and apply system configs to /etc and /srv
def install(parser):
    aegis.stdlib.logw(parser, "INSTALL ARG PARSER")


def schema(parser):
    # Command line options and sanity checking
    define('dry_run', default=True, help="Dry run - make no changes", type=bool)
    config.initialize()
    if not options.hostname:
        logging.error("Please specify hostname to apply schema to, ie dev.codebug.com")
        exit(1)
    config.apply_hostname(options.hostname)
    logging.info("Running schema.py   Env: %s   Hostname: %s   Database: %s   Dry Run: %s", options.env, options.hostname, options.pg_database, options.dry_run)
    if not options.pg_database:
        logging.error("Database isn't configured for this hostname")
        exit(1)
    if not options.app_name:    # is this program_name ?
        logging.error("Please specify app_name to find sql diffs")
        exit(1)
    # Do schema
    try:
        dbnow = aegis.database.dbnow()
        logging.warning("Database Standard Time: %s", dbnow['now'])
        results = aegis.database.db().get("SELECT EXISTS ( SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'sql_diff' )")
        if not results['exists']:
            logging.warning("Creating sql_diff table since it doesn't exist yet.")
            aegis.database.SqlDiff.create_table()
    except aegis.database.OperationalError as ex:
        logging.error("Could not connect to database. Do you need to log into postgres and run:")
        logging.error("postgres=# CREATE USER %s WITH PASSWORD '%s';" % (options.pg_username, options.pg_password))
        logging.error("postgres=# CREATE DATABASE %s OWNER=%s;" % (options.pg_database, options.pg_username))
        exit(1)
    # Read sql_diffs from filesystem
    sql_dir = os.path.join(options.basedir, 'sql')
    diff_files = patch_diffs(sql_dir)
    # Read state from database, INSERT INTO sql_diff for unknown diffs
    sql_diff_rows = aegis.database.SqlDiff.scan()
    sql_diff_map = aegis.database.SqlDiff.map_items(sql_diff_rows, 'sql_diff_name')
    for diff_file in diff_files:
        if diff_file not in sql_diff_map:
            logging.warning("Inserting diff: %s", diff_file)
            aegis.database.SqlDiff.insert(diff_file)
    # Apply any unapplied diffs
    for patch in aegis.database.SqlDiff.scan_unapplied():
        filename = os.path.join(sql_dir, patch['sql_diff_name'])
        sql = open(filename).read().replace('%', '%%')
        try:
            if options.dry_run:
                logging.warning("[Dry Run] diff:  %s  from: %s" % (patch['sql_diff_name'], filename))
            else:
                logging.warning("Applying diff:  %s  from: %s" % (patch['sql_diff_name'], filename))
                query = sql
                aegis.database.db().execute(query)
                aegis.database.SqlDiff.mark_applied(patch['sql_diff_name'])
        except Exception as ex:
            logging.exception(ex)
            logging.error('Query was: %s', query)
            exit(1)
    # Globals
    def diff_sort_cmp(x, y):
        xx = int(x.split('diff')[1].split('.sql')[0])
        yy = int(y.split('diff')[1].split('.sql')[0])
        return xx - yy
    def patch_diffs(sql_dir, prefix='diff'):
        if not os.path.exists(sql_dir):
            logging.error('No patch dir found at: %s', sql_dir)
            sys.exit(1)
        patches = [g.split('/')[-1] for g in glob.glob(sql_dir + '/' + prefix + '*.sql')]
        patchnums = [patch.lstrip(prefix).rstrip('.sql') for patch in patches]
        patchnums.sort()
        diffs = ['%s%s.sql' % (prefix, patchnum) for patchnum in patchnums]
        diffs = sorted(diffs, key=functools.cmp_to_key(diff_sort_cmp))
        return diffs


def build(parser):
    # Argument Handling
    args = parser.parse_args()
    build_args = {'branch': args.branch, 'revision': args.revision, 'env': aegis.config.get('env')}
    if not aegis.config.get('env') or not(build_args['branch'] or build_args['revision']):
        logging.error("aegis build requires --env and one of --branch or --revision")
        aegis.stdlib.loge(aegis.config.get('env'), "ENV")
        aegis.stdlib.loge(build_args, "BUILD ARGS")
        sys.exit(1)
    # Require sudo to build, set real and effective uid and gid, as well as HOME for www-data user
    if not os.geteuid() == 0:
        logging.error('You need root privileges, please run it with sudo.')
        sys.exit(1)
    pw = pwd.getpwnam('www-data')
    os.putenv('HOME', pw.pw_dir)
    os.setregid(pw.pw_gid, pw.pw_gid)
    os.setreuid(pw.pw_uid, pw.pw_uid)
    # Set up build
    logging.info("Running aegis build   Env: %s   Branch: %s   Revision: %s", aegis.config.get('env'), build_args['branch'], build_args['revision'])
    new_build = aegis.build.Build()
    build_row = new_build.create(build_args)
    if build_row.get('error'):
        logging.error(build_row['error'])
        sys.exit(1)
    # Running build itself
    exit_status = new_build.build_exec(build_row)
    build_row = aegis.model.Build.get_id(build_row['build_id'])
    if exit_status:
        logging.error("Build Failed. Version: %s" % build_row['version'])
    else:
        logging.info("Build Success. Version: %s" % build_row['version'])
        logging.info("Next step:  sudo aegis deploy --env=%s --version=%s" % (aegis.config.get('env'), build_row['version']))
    sys.exit(exit_status)


def deploy(parser):
    # Argument Handling
    args = parser.parse_args()
    version = args.version
    env = args.env
    if not version or not env:
        aegis.stdlib.logw(version, "VERSION")
        aegis.stdlib.logw(env, "ENV")
        logging.error("aegis deploy requires --version and --env")
        sys.exit()
    # Require sudo to build, set real and effective uid and gid, as well as HOME for www-data user
    if not os.geteuid() == 0:
        logging.error('You need root privileges, please run it with sudo.')
        sys.exit(1)
    pw = pwd.getpwnam('www-data')
    os.putenv('HOME', pw.pw_dir)
    os.setregid(pw.pw_gid, pw.pw_gid)
    os.setreuid(pw.pw_uid, pw.pw_uid)
    # Make it so
    logging.info("Running aegis deploy   Version: %s   Env: %s", version, env)
    build = aegis.build.Build()
    message = None
    while not message:
        message = input(aegis.stdlib.cstr('Type in release notes for the deploy notification:\n', 'white'))
    # Save the user message and start the deploy/revert
    build_row = aegis.model.Build.get_version(version)
    build_row.set_message(message, 'deploy')
    build_row = aegis.model.Build.get_version(version)
    aegis.build.Build.start_deploy(build_row, os.getenv('SUDO_USER'))
    build.deploy(version, env=env)


def revert(parser):
    # Argument Handling
    args = parser.parse_args()
    env = args.env
    if not env:
        aegis.stdlib.logw(env, "ENV")
        logging.error("aegis revert requires --env")
        sys.exit()
    # Require sudo to build, set real and effective uid and gid, as well as HOME for www-data user
    if not os.geteuid() == 0:
        logging.error('You need root privileges, please run it with sudo.')
        sys.exit(1)
    pw = pwd.getpwnam('www-data')
    os.putenv('HOME', pw.pw_dir)
    os.setregid(pw.pw_gid, pw.pw_gid)
    os.setreuid(pw.pw_uid, pw.pw_uid)
    # Make it so
    logging.info("Running aegis revert   Env: %s", env)
    build = aegis.build.Build()
    message = None
    while not message:
        message = input(aegis.stdlib.cstr('Type in release notes for the deploy notification:\n', 'white'))
    # Save the user message and start the deploy/revert
    build_row = aegis.model.Build.get_live_build(env)
    build_row.set_message(message, 'revert')
    build_row = aegis.model.Build.get_id(build_row['build_id'])
    aegis.build.Build.start_revert(build_row, os.getenv('SUDO_USER'))
    build_row = aegis.model.Build.get_id(build_row['build_id'])
    build_row.set_output('revert', '')
    build.revert(build_row)


def initialize():
    # if branch, revision, version, env don't exist, add them
    if not aegis.config.get('branch'):
        define('branch', default=None, help='git branch name', type=str)
    if not aegis.config.get('revision'):
        define('revision', default=None, help='git revision hash', type=str)
    if not aegis.config.get('version'):
        define('version', default=None, help='git version name', type=str)
    try:
        config.initialize(args=sys.argv[1:])
    except Exception as ex:
        # No config, such as during aegis create shell command
        logging.exception(ex)
        remaining = tornado.options.parse_command_line()


def main():
    parser = argparse.ArgumentParser(description='Create your shield.')
    parser.add_argument('cmd', metavar='<command>', type=str, nargs=1, help='What to do: [create, install, schema, build, deploy, revert]')
    parser.add_argument('--branch', metavar='<branch>', type=str, help='git branch name')
    parser.add_argument('--revision', metavar='<revision>', type=str, help='git revision hash')
    parser.add_argument('--env', metavar='<env>', type=str, help='primary environment name')
    parser.add_argument('--version', metavar='<version>', type=str, help='program version tag')
    parser.add_argument('--appname', metavar='<appname>', type=str, nargs=1, help='code name for application')
    parser.add_argument('--domain', metavar='<domain>', type=str, nargs=1, help='domain to create application')
    args = parser.parse_args()
    cmd = args.cmd[0]
    # Do something
    if cmd == 'create':
        return create(parser)
    elif cmd == 'install':
        return install(parser)
    elif cmd == 'schema':
        return schema(parser)
    elif cmd == 'build':
        return build(parser)
    elif cmd == 'deploy':
        return deploy(parser)
    elif cmd == 'revert':
        return revert(parser)
    else:
        logging.error("NOT IMPLEMENTED... YET")
        return 127


if __name__ == "__main__":
    # Called from repository checkout, for example ./aegis/aegis_.py
    initialize()
    retval = main()
    sys.exit(retval)
elif __name__ == 'aegis.aegis_':
    # Called from entry point, likely from setup.py installation
    initialize()
    retval = main()
    sys.exit(retval)
else:
    # Not entirely sure how it was called
    initialize()
    aegis.stdlib.logw(__name__, "Called by __name__")
    sys.exit(126)
