
        
        
--DROP TABLE fbrm.mon_rman_backup_list_y20m05d09;

CREATE TABLE fbrm.mon_rman_backup_list_y20m05d09
(
    -- Inherited from table fbrm.mon_rman_backup_list: u_id bigint NOT NULL DEFAULT nextval('fbrm.u_id_mon_rman_backup_list'::regclass),
    -- Inherited from table fbrm.mon_rman_backup_list: hostname character varying(50) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: agent_ip character varying(16) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: zfs_name character varying(50) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: zfs_ip character varying(50) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: fbrm_date date NOT NULL,
    -- Inherited from table fbrm.mon_rman_backup_list: db_key numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: db_name character varying(8) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: session_key numeric NOT NULL,
    -- Inherited from table fbrm.mon_rman_backup_list: session_recid numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: session_stamp numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: command_id character varying(33) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: start_time character varying(19) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: end_time character varying(19) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: input_bytes numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: output_bytes numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: status_weight numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: optimized_weight character varying(30) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: input_type_weight character varying(30) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: output_device_type character varying(17) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: autobackup_count numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: backed_by_osb character varying(3) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: autobackup_done character varying(3) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: status character varying(23) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: input_type character varying(13) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: optimized character varying(3) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: elapsed_seconds character varying(30) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: compression_ratio character varying(30) COLLATE pg_catalog."default",
    -- Inherited from table fbrm.mon_rman_backup_list: input_bytes_per_sec numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: output_bytes_per_sec numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: input_bytes_display numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: output_bytes_display numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: input_bytes_per_sec_display numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: output_bytes_per_sec_display numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: time_taken_display numeric,
    -- Inherited from table fbrm.mon_rman_backup_list: collect_time date,
    CONSTRAINT y20m05d09 CHECK (fbrm_date >= '2020-05-09'::date)
)
    INHERITS (fbrm.mon_rman_backup_list)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.mon_rman_backup_list_y20m05d09
    OWNER to fbrmuser;




-- FUNCTION: fbrm.merge_mon_rman_backup_list_trigger()

-- DROP FUNCTION fbrm.merge_mon_rman_backup_list_trigger();

CREATE OR REPLACE FUNCTION fbrm.merge_mon_rman_backup_list_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$ begin
  if exists ( select 1 from fbrm.mon_rman_backup_list_y20m05d09 where session_key = new.session_key  ) then
    update fbrm.mon_rman_backup_list_y20m05d09 set 
      
        session_stamp = new.session_stamp,
        command_id =new.command_id ,
        start_time = new.start_time ,
        end_time = new.end_time, 
        input_bytes = new.input_bytes ,
        output_bytes = new.output_bytes ,
        status_weight = new.status_weight ,
        optimized_weight  = new.optimized_weight,
        input_type_weight = new.input_type_weight ,
        output_device_type  = new.output_device_type,
        autobackup_count = new.autobackup_count,
        backed_by_osb = new.backed_by_osb,
        autobackup_done = new.autobackup_done,
        status = new.status,
        input_type = new.input_type,
        optimized = new.optimized,
        elapsed_seconds = new.elapsed_seconds,
        compression_ratio = new.compression_ratio,
        input_bytes_per_sec = new.input_bytes_per_sec,
        output_bytes_per_sec = new.output_bytes_per_sec,
        input_bytes_display = new.input_bytes_display,
        output_bytes_display =new.output_bytes_display,
        input_bytes_per_sec_display = new.input_bytes_per_sec_display ,
        output_bytes_per_sec_display =new.output_bytes_per_sec_display,
        time_taken_display = new.time_taken_display,
        collect_time =collect_time 

      where session_key = new.session_key   ;
    return null;
    end if;
  return new;
  end; $BODY$;

ALTER FUNCTION fbrm.merge_mon_rman_backup_list_trigger()
    OWNER TO fbrmuser;


CREATE OR REPLACE FUNCTION fbrm.backup_list_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF ( NEW.fbrm_date = DATE '2020-05-09') THEN
    INSERT INTO fbrm.mon_rman_backup_list_y20m05d09 VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE 'td_1') THEN
    INSERT INTO fbrm.mon_rman_backup_list_y2020m05d10 VALUES (NEW.*);
ELSIF ( NEW.fbrm_date = DATE '2020-05-11') THEN
    INSERT INTO fbrm.mon_rman_backup_list_y2020m05d11 VALUES (NEW.*);
ELSE
RAISE EXCEPTION 'Date out of range.  Fix the insert_mon_rman_backup_list_trigger() function!';
END IF;
RETURN NULL;
END;
$BODY$;

ALTER FUNCTION fbrm.backup_list_trigger()
    OWNER TO fbrmuser;
	


CREATE TRIGGER merge_mon_rman_backup_list_trigger
    BEFORE INSERT
    ON fbrm.mon_rman_backup_list_y20m05d09
    FOR EACH ROW
    EXECUTE PROCEDURE fbrm.merge_mon_rman_backup_list_trigger();
