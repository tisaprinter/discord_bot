from utils import db
from cfg import DATABASE



db.cmd(F"CREATE DATABASE IF NOT EXISTS {DATABASE['NAME']}", database=None)


db.cmd("""CREATE TABLE IF NOT EXISTS conversations(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name TEXT,
    messages JSON,
    PRIMARY KEY (id))
    """)


db.cmd("""CREATE TABLE IF NOT EXISTS channels(
           channel_id VARCHAR(128) PRIMARY KEY
    )
       """)



db.cmd("""
       CREATE TABLE IF NOT EXISTS config(
           name VARCHAR(32),
           value VARCHAR(128)
       )
       """)


if not db.get_value("value", "config", "name", "status"):
    db.cmd("INSERT INTO config VALUES(%s, %s)", value=("status", "off"))
    
    
if not db.get_value("value", "config", "name", "token1"):
    db.cmd("INSERT INTO config VALUES(%s, %s)", value=("token1", None))


if not db.get_value("value", "config", "name", "token2"):
    db.cmd("INSERT INTO config VALUES(%s, %s)", value=("token2", None))


if not db.get_value("value", "config", "name", "token3"):
    db.cmd("INSERT INTO config VALUES(%s, %s)", value=("token3", None))


if not db.get_value("value", "config", "name", "token4"):
    db.cmd("INSERT INTO config VALUES(%s, %s)", value=("token4", None))


if not db.get_value("value", "config", "name", "token5"):
    db.cmd("INSERT INTO config VALUES(%s, %s)", value=("token5", None))
