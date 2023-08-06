Please see https://alembic.readthedocs.org/en/latest/index.html for general documentation

To create alembic migrations use:
$ cyborg-dbsync revision --message <message_info> --autogenerate

NOTE: <message_info> is the brief information of the database script you want to upgrade.

Stamp db with most recent migration version, without actually running migrations
$ cyborg-dbsync stamp --revision head

Upgrade can be performed by:
$ cyborg-dbsync upgrade
# cyborg-dbsync upgrade --revision head
