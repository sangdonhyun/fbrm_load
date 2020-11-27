keys=["last_update_time","fbrm_date","ins_date_time","elapsed_seconds","message","sql_hash_value","serial","sql_id","sql_exec_id","sql_plan_hash_value","target_desc","hostname","sql_address","sid","units","sql_plan_operation","sql_plan_line_id","username","agent_ip","complete","sql_exec_","timestamp","start_time","db_name","opname","sql_plan_options","target","sofar","context","time_remaining","live_date_time","totalwork"]
vals=['2020-05-25 18:06:53','2020-05-25','2020-05-25 18:37:58','45','RMAN: incremental datafile backup: Set Count 620: 29441 out of 29441 Blocks done','0','9651','','','0','Set Count','fora_01','00','94','Blocks','','','SYS','192.168.56.130','100.0','16777440','','2020-05-25 18:06:08','UPGR','RMAN: incremental datafile backup','0','620','29441','2','0','2020-05-25 18:15:28','29441']




for i  in range(len(keys)):
    print keys[i],vals[i],len(vals[i])


