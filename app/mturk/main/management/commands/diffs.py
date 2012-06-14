import time
import logging

from utils.sql import execute_sql, query_to_tuples

log = logging.getLogger(__name__)


def hitgroups(cid):
    r = execute_sql("select distinct group_id from hits_mv where crawl_id = %s", cid)
    return [g[0] for g in r.fetchall()]


def last_crawlids(limit=10):
    r = execute_sql("select crawl_id from hits_mv order by crawl_id desc limit %s", limit)
    return [c[0] for c in r.fetchall()]


def last_crawlid():
    return execute_sql("select crawl_id from hits_mv order by crawl_id desc limit 1;").fetchall()[0][0]


def updatehitgroup(g, cid):
    prev = execute_sql("""select hits_available from hits_mv
                where
                    crawl_id between %s and %s and
                    group_id = '%s'
                order by crawl_id desc
                limit 1;""" % (cid - 100, cid - 1, g)).fetchall()
    prev = prev[0][0] if prev else 0

    execute_sql("""update hits_mv set hits_diff = hits_available - %s where
            group_id = '%s' and crawl_id = %s;""" % (prev, g, cid))


def update_cid(cid):

    st = time.time()
    count = 0
    for i, g in enumerate(query_to_tuples("select distinct group_id from hits_mv where crawl_id = %s", cid)):
        g = g[0]
        log.info("processing %s, %s %s", i, cid,  g)
        updatehitgroup(g, cid)
        count += 1

    execute_sql("commit;")

    log.info("updated crawl in %s", time.time() - st)

    return count
