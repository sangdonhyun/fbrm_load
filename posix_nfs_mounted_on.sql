CREATE SEQUENCE fbrm.u_id_posix_nfs_mounted_on
    INCREMENT 1
    START 179866
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE fbrm.u_id_posix_nfs_mounted_on
    OWNER TO fbrmuser;





CREATE TABLE fbrm.posix_nfs_mounted_on
(
    u_id bigint NOT NULL DEFAULT nextval('fbrm.u_id_posix_filesystems'::regclass),
    check_date_time character varying(20) COLLATE pg_catalog."default",
    server_hostname character varying(50) COLLATE pg_catalog."default",
    server_ip character varying(16) COLLATE pg_catalog."default",
    filesystem character varying(50) COLLATE pg_catalog."default",
    mounted  character varying(50) COLLATE pg_catalog."default",
    mounted_bit  bool default False ,
    check_bit bool default False ,
    CONSTRAINT master_zfs_snapshots_pkey PRIMARY KEY (server_hostname, server_ip,mounted)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE fbrm.posix_nfs_mounted_on
    OWNER to webuser;




CREATE FUNCTION fbrm.merge_posix_nfs_mounted_on_trigger()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$ begin
  if exists ( select 1 from fbrm.posix_nfs_mounted_on where server_hostname = new.server_hostname and server_ip= new.server_ip and mounted = new.mounted ) then
    update fbrm.posix_nfs_mounted_on set 
		check_date_time = new.check_date_time
		check_date_time = new.check_date_time
        

      where zfs_name = new.zfs_name and zfs_default_ip= new.zfs_default_ip and zfs_service_ip = new.zfs_service_ip  ;
    return null;
    end if;
  return new;
  end; $BODY$;

ALTER FUNCTION fbrm.merge_posix_nfs_mounted_on_trigger()
    OWNER TO fbrmuser;
