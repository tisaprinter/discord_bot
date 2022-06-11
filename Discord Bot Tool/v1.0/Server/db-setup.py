from utils import db
from cfg import DATABASE



db.cmd(F"CREATE DATABASE IF NOT EXISTS {DATABASE['NAME']}", database=None)


db.cmd("""CREATE TABLE IF NOT EXISTS conversations(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name TEXT,
    messages JSON,
    PRIMARY KEY (id))
    """)


db.cmd("""
       CREATE TABLE IF NOT EXISTS bots(
           id BIGINT NOT NULL AUTO_INCREMENT,
           name TEXT,
           account1_token TEXT,
           account2_token TEXT,
           channel_id BIGINT,
           PRIMARY KEY (id)
       )
       """)



db.cmd("""
       CREATE TABLE IF NOT EXISTS options(
           name VARCHAR(32),
           value VARCHAR(32)
       )
       """)


if not db.get_value("value", table="options", search_filter="name", value="status"):
    db.cmd("INSERT INTO options VALUES(%s, %s)", value=("status", "off"))