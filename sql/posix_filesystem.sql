-- DROP TABLE fbrm.posix_filesystem;

CREATE TABLE fbrm.posix_filesystem_realtime
(
    u_id bigint NOT NULL DEFAULT nextval('fbrm.u_id_posix_filesystems'::regclass),
    fbrm_date date NOT NULL,
    live_date_time character varying(20) COLLATE pg_catalog."default",
    hostname character varying(50) COLLATE pg_catalog."default",
    agent_ip character varying(16) COLLATE pg_catalog."default",
    filesystem character varying(50) COLLATE pg_catalog."default",
    blocks numeric,
    used numeric,
    available numeric,
    used_capacity character varying(4) COLLATE pg_catalog."default",
    mounted character varying(50) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.posix_filesystem
    OWNER to webuser;





CREATE TABLE fbrm.posix_filesystem_realtime_y2020m05d19
(
   
    CONSTRAINT y2020m05d19 CHECK (fbrm_date >= '2020-05-19'::date)
)
    INHERITS (fbrm.posix_filesystem_realtime)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.posix_filesystem_realtime_y2020m05d19
    OWNER to fbrmuser;