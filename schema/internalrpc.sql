--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.12
-- Dumped by pg_dump version 9.6.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: export_archive; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE export_archive (
    id integer NOT NULL,
    gp_id integer NOT NULL,
    password character varying NOT NULL,
    url character varying NOT NULL,
    md5 character varying NOT NULL,
    map_url character varying,
    archive_date character varying,
    is_latest boolean DEFAULT false,
    build_id bigint,
    is_topgis boolean DEFAULT false
);


ALTER TABLE export_archive OWNER TO internalrpc;

--
-- Name: export_archive_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE export_archive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE export_archive_id_seq OWNER TO internalrpc;

--
-- Name: export_archive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE export_archive_id_seq OWNED BY export_archive.id;


--
-- Name: layer_statistic; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE layer_statistic (
    id integer NOT NULL,
    gp_id integer NOT NULL,
    sum_htable integer NOT NULL,
    sum_qgis_mapserv integer NOT NULL,
    sum_wms integer NOT NULL,
    sum_total integer NOT NULL
);


ALTER TABLE layer_statistic OWNER TO internalrpc;

--
-- Name: layer_statistic_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE layer_statistic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE layer_statistic_id_seq OWNER TO internalrpc;

--
-- Name: layer_statistic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE layer_statistic_id_seq OWNED BY layer_statistic.id;


--
-- Name: mapfile; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE mapfile (
    id integer NOT NULL,
    name text NOT NULL,
    gp_id integer NOT NULL,
    data jsonb NOT NULL
);


ALTER TABLE mapfile OWNER TO internalrpc;

--
-- Name: mapfile_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE mapfile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mapfile_id_seq OWNER TO internalrpc;

--
-- Name: mapfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE mapfile_id_seq OWNED BY mapfile.id;


--
-- Name: mapfile_layer; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE mapfile_layer (
    id integer NOT NULL,
    gp_id integer NOT NULL,
    layer_id integer NOT NULL,
    layer_data json NOT NULL,
    layer_name text NOT NULL,
    layer_mapfile_position integer NOT NULL,
    layer_group text NOT NULL
);


ALTER TABLE mapfile_layer OWNER TO internalrpc;

--
-- Name: mapfile_layer_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE mapfile_layer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mapfile_layer_id_seq OWNER TO internalrpc;

--
-- Name: mapfile_layer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE mapfile_layer_id_seq OWNED BY mapfile_layer.id;


--
-- Name: qgisfile; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE qgisfile (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    gp_id integer NOT NULL,
    data jsonb NOT NULL
);


ALTER TABLE qgisfile OWNER TO internalrpc;

--
-- Name: qgisfile_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE qgisfile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE qgisfile_id_seq OWNER TO internalrpc;

--
-- Name: qgisfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE qgisfile_id_seq OWNED BY qgisfile.id;


--
-- Name: reactor; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE reactor (
    id integer NOT NULL,
    name character varying NOT NULL,
    status character varying(255) DEFAULT 'created'::character varying NOT NULL,
    data json,
    options json,
    module character varying(255) DEFAULT 'test'::character varying NOT NULL
);


ALTER TABLE reactor OWNER TO internalrpc;

--
-- Name: reactor_c_module; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE reactor_c_module (
    id integer NOT NULL,
    name character varying(255) DEFAULT 'test'::character varying NOT NULL
);


ALTER TABLE reactor_c_module OWNER TO internalrpc;

--
-- Name: reactor_c_module_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE reactor_c_module_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reactor_c_module_id_seq OWNER TO internalrpc;

--
-- Name: reactor_c_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE reactor_c_module_id_seq OWNED BY reactor_c_module.id;


--
-- Name: reactor_c_status; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE reactor_c_status (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE reactor_c_status OWNER TO internalrpc;

--
-- Name: reactor_c_status_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE reactor_c_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reactor_c_status_id_seq OWNER TO internalrpc;

--
-- Name: reactor_c_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE reactor_c_status_id_seq OWNED BY reactor_c_status.id;


--
-- Name: reactor_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE reactor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reactor_id_seq OWNER TO internalrpc;

--
-- Name: reactor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE reactor_id_seq OWNED BY reactor.id;


--
-- Name: reactor_server_slot; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE reactor_server_slot (
    id integer NOT NULL,
    core_id integer NOT NULL,
    server_id integer NOT NULL,
    reactor_id integer
);


ALTER TABLE reactor_server_slot OWNER TO internalrpc;

--
-- Name: reactor_server_slot_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE reactor_server_slot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reactor_server_slot_id_seq OWNER TO internalrpc;

--
-- Name: reactor_server_slot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE reactor_server_slot_id_seq OWNED BY reactor_server_slot.id;


--
-- Name: server; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE server (
    id integer NOT NULL,
    hostname character varying(255) NOT NULL,
    machine_type character varying(255) NOT NULL,
    machine_id integer NOT NULL,
    machine_env character varying(255) NOT NULL,
    machine_location character varying(255) NOT NULL,
    status character varying(255) NOT NULL
);


ALTER TABLE server OWNER TO internalrpc;

--
-- Name: server_c_machine_type; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE server_c_machine_type (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE server_c_machine_type OWNER TO internalrpc;

--
-- Name: server_c_machine_type_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE server_c_machine_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE server_c_machine_type_id_seq OWNER TO internalrpc;

--
-- Name: server_c_machine_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE server_c_machine_type_id_seq OWNED BY server_c_machine_type.id;


--
-- Name: server_c_status; Type: TABLE; Schema: public; Owner: internalrpc
--

CREATE TABLE server_c_status (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE server_c_status OWNER TO internalrpc;

--
-- Name: server_id_seq; Type: SEQUENCE; Schema: public; Owner: internalrpc
--

CREATE SEQUENCE server_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE server_id_seq OWNER TO internalrpc;

--
-- Name: server_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: internalrpc
--

ALTER SEQUENCE server_id_seq OWNED BY server.id;


--
-- Name: export_archive id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY export_archive ALTER COLUMN id SET DEFAULT nextval('export_archive_id_seq'::regclass);


--
-- Name: layer_statistic id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY layer_statistic ALTER COLUMN id SET DEFAULT nextval('layer_statistic_id_seq'::regclass);


--
-- Name: mapfile id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY mapfile ALTER COLUMN id SET DEFAULT nextval('mapfile_id_seq'::regclass);


--
-- Name: mapfile_layer id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY mapfile_layer ALTER COLUMN id SET DEFAULT nextval('mapfile_layer_id_seq'::regclass);


--
-- Name: qgisfile id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY qgisfile ALTER COLUMN id SET DEFAULT nextval('qgisfile_id_seq'::regclass);


--
-- Name: reactor id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor ALTER COLUMN id SET DEFAULT nextval('reactor_id_seq'::regclass);


--
-- Name: reactor_c_module id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_c_module ALTER COLUMN id SET DEFAULT nextval('reactor_c_module_id_seq'::regclass);


--
-- Name: reactor_c_status id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_c_status ALTER COLUMN id SET DEFAULT nextval('reactor_c_status_id_seq'::regclass);


--
-- Name: reactor_server_slot id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_server_slot ALTER COLUMN id SET DEFAULT nextval('reactor_server_slot_id_seq'::regclass);


--
-- Name: server id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server ALTER COLUMN id SET DEFAULT nextval('server_id_seq'::regclass);


--
-- Name: server_c_machine_type id; Type: DEFAULT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server_c_machine_type ALTER COLUMN id SET DEFAULT nextval('server_c_machine_type_id_seq'::regclass);


--
-- Name: reactor_c_module reactor_c_module_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_c_module
    ADD CONSTRAINT reactor_c_module_id PRIMARY KEY (id);


--
-- Name: reactor_c_module reactor_c_module_name; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_c_module
    ADD CONSTRAINT reactor_c_module_name UNIQUE (name);


--
-- Name: reactor_c_status reactor_c_status_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_c_status
    ADD CONSTRAINT reactor_c_status_id PRIMARY KEY (id);


--
-- Name: reactor_c_status reactor_c_status_name; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_c_status
    ADD CONSTRAINT reactor_c_status_name UNIQUE (name);


--
-- Name: reactor reactor_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor
    ADD CONSTRAINT reactor_id PRIMARY KEY (id);


--
-- Name: reactor_server_slot reactor_server_slot_core_id_server_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_core_id_server_id UNIQUE (core_id, server_id);


--
-- Name: reactor_server_slot reactor_server_slot_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_id PRIMARY KEY (id);


--
-- Name: server_c_machine_type server_c_machine_type_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server_c_machine_type
    ADD CONSTRAINT server_c_machine_type_id PRIMARY KEY (id);


--
-- Name: server_c_machine_type server_c_machine_type_name; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server_c_machine_type
    ADD CONSTRAINT server_c_machine_type_name UNIQUE (name);


--
-- Name: server_c_status server_c_status_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server_c_status
    ADD CONSTRAINT server_c_status_id PRIMARY KEY (id);


--
-- Name: server_c_status server_c_status_name; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server_c_status
    ADD CONSTRAINT server_c_status_name UNIQUE (name);


--
-- Name: server server_id; Type: CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server
    ADD CONSTRAINT server_id PRIMARY KEY (id);


--
-- Name: reactor reactor_module_fkey; Type: FK CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor
    ADD CONSTRAINT reactor_module_fkey FOREIGN KEY (module) REFERENCES reactor_c_module(name);


--
-- Name: reactor_server_slot reactor_server_slot_reactor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_reactor_id_fkey FOREIGN KEY (reactor_id) REFERENCES reactor(id);


--
-- Name: reactor_server_slot reactor_server_slot_server_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_server_id_fkey FOREIGN KEY (server_id) REFERENCES server(id);


--
-- Name: reactor reactor_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY reactor
    ADD CONSTRAINT reactor_status_fkey FOREIGN KEY (status) REFERENCES reactor_c_status(name);


--
-- Name: server server_machine_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server
    ADD CONSTRAINT server_machine_type_fkey FOREIGN KEY (machine_type) REFERENCES server_c_machine_type(name);


--
-- Name: server server_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: internalrpc
--

ALTER TABLE ONLY server
    ADD CONSTRAINT server_status_fkey FOREIGN KEY (status) REFERENCES server_c_status(name);


--
-- PostgreSQL database dump complete
--

