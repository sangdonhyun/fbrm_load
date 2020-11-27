str="""       SID,   SERIAL#,OPNAME                                                          ,TARGET                                                          ,TARGET_DESC                     ,     SOFAR, TOTALWORK,UNITS                           ,START_TIM,LAST_UPDA,TIMESTAMP,TIME_REMAINING,ELAPSED_SECONDS,   CONTEXT,MESSAGE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ,USERNAME                      ,SQL_ADDRESS     ,SQL_HASH_VALUE,SQL_ID       ,SQL_PLAN_HASH_VALUE,SQL_EXEC_,SQL_EXEC_ID,SQL_PLAN_LINE_ID,SQL_PLAN_OPERATION            ,SQL_PLAN_OPTIONS              ,     QCSID
"""
for s in str.split(','):
    print s.strip()

print len(str.split(','))


"""
sid
serial#
opname
target
target_desc
sofar
totalwork
units
start_tim
last_upda
timestamp
time_remaining
elapsed_seconds
context
message
username
sql_address
sql_hash_value
sql_id
sql_plan_hash_value
sql_exec_
sql_exec_id
sql_plan_line_id
sql_plan_operation
sql_plan_options
qcsid
"""
