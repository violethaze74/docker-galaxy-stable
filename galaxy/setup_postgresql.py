import os
import shutil
import argparse
import subprocess


def pg_ctl(database_path, database_version, mod='start'):
    """
        Start/Stop PostgreSQL with variable data_directory.
        mod = [start, end, restart, reload]
    """
    pg_conf = f'/etc/postgresql/{database_version}/main/postgresql.conf'
    new_data_directory = f"'{database_path}'"
    cmd = f'sed -i "s|data_directory = .*|data_directory = {new_data_directory}|g" {pg_conf}'
    subprocess.call(cmd, shell=True)
    subprocess.call(f'service postgresql {mod}', shell=True)


def set_pg_permission(database_path):
    """
        Set the correct permissions for a newly created PostgreSQL data_directory.
    """
    subprocess.call(f'chown -R postgres:postgres {database_path}', shell=True)
    subprocess.call(f'chmod -R 0700 {database_path}', shell=True)


def create_pg_db(user, password, database, database_path, database_version):
    """
        Initialize PostgreSQL Database, add database user und create the Galaxy Database.
    """
    pg_bin = f"/usr/lib/postgresql/{database_version}/bin/"
    os.makedirs(database_path)
    set_pg_permission(database_path)
    # initialize a new postgres database
    subprocess.call(
        f"su - postgres -c '{os.path.join(pg_bin, 'initdb')} "
        f"--auth=trust --encoding UTF8 --pgdata={database_path}'",
        shell=True
    )

    shutil.copy('/etc/ssl/certs/ssl-cert-snakeoil.pem', os.path.join(database_path, 'server.crt'))
    shutil.copy('/etc/ssl/private/ssl-cert-snakeoil.key', os.path.join(database_path, 'server.key'))
    set_pg_permission(os.path.join(database_path, 'server.crt'))
    set_pg_permission(os.path.join(database_path, 'server.key'))

    # change data_directory in postgresql.conf and start the service with the new location
    pg_ctl(database_path, database_version, 'start')

    subprocess.call(f"""su - postgres -c "psql --command \\"CREATE USER {user} WITH SUPERUSER PASSWORD '{password}'\\";"
                    """, shell=True)

    subprocess.call(f"su - postgres -c 'createdb -O {user} {database}'", shell=True)
    subprocess.call('service postgresql stop', shell=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Initializing a complete Galaxy Database with Tool Shed Tools.')

    parser.add_argument("--dbuser", required=True,
                        help="Username of the Galaxy Database Administrator. That name will be specified in the "
                             "galaxy.yml file.")

    parser.add_argument("--dbpassword", required=True,
                        help="Password of the Galaxy Database Administrator. That name will be specified in the "
                             "galaxy.yml file.")

    parser.add_argument("--db-name", dest='db_name', required=True,
                        help="Galaxy Database name. That name will be specified in the galaxy.yml file.")

    parser.add_argument("--dbpath",
                        help="Galaxy Database path.")

    parser.add_argument("--dbversion", default='15',
                        help="Postgresql server major version.")

    options = parser.parse_args()

    """
        Initialize the Galaxy Database + adding an Admin user.
        This database is the default one, created by the Dockerfile. 
        The user can set a volume (-v /path/:/export/) to get a persistent database.
    """
    create_pg_db(options.dbuser, options.dbpassword, options.db_name, options.dbpath, options.dbversion)
