--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.server DROP CONSTRAINT server_status_fkey;
ALTER TABLE ONLY public.server DROP CONSTRAINT server_machine_type_fkey;
ALTER TABLE ONLY public.reactor DROP CONSTRAINT reactor_status_fkey;
ALTER TABLE ONLY public.reactor_server_slot DROP CONSTRAINT reactor_server_slot_server_id_fkey;
ALTER TABLE ONLY public.reactor_server_slot DROP CONSTRAINT reactor_server_slot_reactor_id_fkey;
ALTER TABLE ONLY public.reactor DROP CONSTRAINT reactor_module_fkey;
ALTER TABLE ONLY public.server DROP CONSTRAINT server_id;
ALTER TABLE ONLY public.server_c_status DROP CONSTRAINT server_c_status_name;
ALTER TABLE ONLY public.server_c_status DROP CONSTRAINT server_c_status_id;
ALTER TABLE ONLY public.server_c_machine_type DROP CONSTRAINT server_c_machine_type_name;
ALTER TABLE ONLY public.server_c_machine_type DROP CONSTRAINT server_c_machine_type_id;
ALTER TABLE ONLY public.reactor_server_slot DROP CONSTRAINT reactor_server_slot_id;
ALTER TABLE ONLY public.reactor_server_slot DROP CONSTRAINT reactor_server_slot_core_id_server_id;
ALTER TABLE ONLY public.reactor DROP CONSTRAINT reactor_id;
ALTER TABLE ONLY public.reactor_c_status DROP CONSTRAINT reactor_c_status_name;
ALTER TABLE ONLY public.reactor_c_status DROP CONSTRAINT reactor_c_status_id;
ALTER TABLE ONLY public.reactor_c_module DROP CONSTRAINT reactor_c_module_name;
ALTER TABLE ONLY public.reactor_c_module DROP CONSTRAINT reactor_c_module_id;
ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.server_c_machine_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.server ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.reactor_server_slot ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.reactor_c_status ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.reactor_c_module ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.reactor ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.users_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.server_id_seq;
DROP TABLE public.server_c_status;
DROP SEQUENCE public.server_c_machine_type_id_seq;
DROP TABLE public.server_c_machine_type;
DROP TABLE public.server;
DROP SEQUENCE public.reactor_server_slot_id_seq;
DROP TABLE public.reactor_server_slot;
DROP SEQUENCE public.reactor_id_seq;
DROP SEQUENCE public.reactor_c_status_id_seq;
DROP TABLE public.reactor_c_status;
DROP SEQUENCE public.reactor_c_module_id_seq;
DROP TABLE public.reactor_c_module;
DROP TABLE public.reactor;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: reactor; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.reactor (
    id integer NOT NULL,
    name character varying NOT NULL,
    status character varying(255) DEFAULT 'created'::character varying NOT NULL,
    data json,
    options json,
    module character varying(255) DEFAULT 'test'::character varying NOT NULL
);


ALTER TABLE public.reactor OWNER TO gdt;

--
-- Name: reactor_c_module; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.reactor_c_module (
    id integer NOT NULL,
    name character varying(255) DEFAULT 'test'::character varying NOT NULL
);


ALTER TABLE public.reactor_c_module OWNER TO gdt;

--
-- Name: reactor_c_module_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.reactor_c_module_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reactor_c_module_id_seq OWNER TO gdt;

--
-- Name: reactor_c_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.reactor_c_module_id_seq OWNED BY public.reactor_c_module.id;


--
-- Name: reactor_c_status; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.reactor_c_status (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.reactor_c_status OWNER TO gdt;

--
-- Name: reactor_c_status_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.reactor_c_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reactor_c_status_id_seq OWNER TO gdt;

--
-- Name: reactor_c_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.reactor_c_status_id_seq OWNED BY public.reactor_c_status.id;


--
-- Name: reactor_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.reactor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reactor_id_seq OWNER TO gdt;

--
-- Name: reactor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.reactor_id_seq OWNED BY public.reactor.id;


--
-- Name: reactor_server_slot; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.reactor_server_slot (
    id integer NOT NULL,
    core_id integer NOT NULL,
    server_id integer NOT NULL,
    reactor_id integer
);


ALTER TABLE public.reactor_server_slot OWNER TO gdt;

--
-- Name: reactor_server_slot_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.reactor_server_slot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reactor_server_slot_id_seq OWNER TO gdt;

--
-- Name: reactor_server_slot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.reactor_server_slot_id_seq OWNED BY public.reactor_server_slot.id;


--
-- Name: server; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.server (
    id integer NOT NULL,
    hostname character varying(255) NOT NULL,
    machine_type character varying(255) NOT NULL,
    machine_id integer NOT NULL,
    machine_env character varying(255) NOT NULL,
    machine_location character varying(255) NOT NULL,
    status character varying(255) NOT NULL
);


ALTER TABLE public.server OWNER TO gdt;

--
-- Name: server_c_machine_type; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.server_c_machine_type (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.server_c_machine_type OWNER TO gdt;

--
-- Name: server_c_machine_type_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.server_c_machine_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.server_c_machine_type_id_seq OWNER TO gdt;

--
-- Name: server_c_machine_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.server_c_machine_type_id_seq OWNED BY public.server_c_machine_type.id;


--
-- Name: server_c_status; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.server_c_status (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.server_c_status OWNER TO gdt;

--
-- Name: server_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.server_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.server_id_seq OWNER TO gdt;

--
-- Name: server_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.server_id_seq OWNED BY public.server.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: gdt
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying NOT NULL,
    md5_password character varying NOT NULL,
    email character varying NOT NULL,
    superadmin boolean DEFAULT false NOT NULL
);


ALTER TABLE public.users OWNER TO gdt;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: gdt
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO gdt;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gdt
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: reactor id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor ALTER COLUMN id SET DEFAULT nextval('public.reactor_id_seq'::regclass);


--
-- Name: reactor_c_module id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_c_module ALTER COLUMN id SET DEFAULT nextval('public.reactor_c_module_id_seq'::regclass);


--
-- Name: reactor_c_status id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_c_status ALTER COLUMN id SET DEFAULT nextval('public.reactor_c_status_id_seq'::regclass);


--
-- Name: reactor_server_slot id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_server_slot ALTER COLUMN id SET DEFAULT nextval('public.reactor_server_slot_id_seq'::regclass);


--
-- Name: server id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server ALTER COLUMN id SET DEFAULT nextval('public.server_id_seq'::regclass);


--
-- Name: server_c_machine_type id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server_c_machine_type ALTER COLUMN id SET DEFAULT nextval('public.server_c_machine_type_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: reactor; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.reactor (id, name, status, data, options, module) FROM stdin;
3	amazfit	running	{"mac":"E5:2F:5A:BE:DC:CA"}	\N	test
4	miband2	running	{"mac":"FF:BD:87:9D:70:7C"}	\N	test
2	test	ready	{"mac":"d8:ec:bf:c7:8c:8b"}	{"mac":"d8:ec:bf:c7:8c:8b"}	test
\.


--
-- Data for Name: reactor_c_module; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.reactor_c_module (id, name) FROM stdin;
1	test
\.


--
-- Name: reactor_c_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.reactor_c_module_id_seq', 1, true);


--
-- Data for Name: reactor_c_status; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.reactor_c_status (id, name) FROM stdin;
1	ready
2	running
3	done
\.


--
-- Name: reactor_c_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.reactor_c_status_id_seq', 3, true);


--
-- Name: reactor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.reactor_id_seq', 4, true);


--
-- Data for Name: reactor_server_slot; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.reactor_server_slot (id, core_id, server_id, reactor_id) FROM stdin;
\.


--
-- Name: reactor_server_slot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.reactor_server_slot_id_seq', 268, true);


--
-- Data for Name: server; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.server (id, hostname, machine_type, machine_id, machine_env, machine_location, status) FROM stdin;
\.


--
-- Data for Name: server_c_machine_type; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.server_c_machine_type (id, name) FROM stdin;
1	labrat
\.


--
-- Name: server_c_machine_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.server_c_machine_type_id_seq', 1, true);


--
-- Data for Name: server_c_status; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.server_c_status (id, name) FROM stdin;
1	registered
2	online
\.


--
-- Name: server_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.server_id_seq', 110, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: gdt
--

COPY public.users (id, name, md5_password, email, superadmin) FROM stdin;
1	admin	d8578edf8458ce06fbc5bb76a58c5ca4	krutma@seznam.cz	t
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gdt
--

SELECT pg_catalog.setval('public.users_id_seq', 15, true);


--
-- Name: reactor_c_module reactor_c_module_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_c_module
    ADD CONSTRAINT reactor_c_module_id PRIMARY KEY (id);


--
-- Name: reactor_c_module reactor_c_module_name; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_c_module
    ADD CONSTRAINT reactor_c_module_name UNIQUE (name);


--
-- Name: reactor_c_status reactor_c_status_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_c_status
    ADD CONSTRAINT reactor_c_status_id PRIMARY KEY (id);


--
-- Name: reactor_c_status reactor_c_status_name; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_c_status
    ADD CONSTRAINT reactor_c_status_name UNIQUE (name);


--
-- Name: reactor reactor_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor
    ADD CONSTRAINT reactor_id PRIMARY KEY (id);


--
-- Name: reactor_server_slot reactor_server_slot_core_id_server_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_core_id_server_id UNIQUE (core_id, server_id);


--
-- Name: reactor_server_slot reactor_server_slot_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_id PRIMARY KEY (id);


--
-- Name: server_c_machine_type server_c_machine_type_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server_c_machine_type
    ADD CONSTRAINT server_c_machine_type_id PRIMARY KEY (id);


--
-- Name: server_c_machine_type server_c_machine_type_name; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server_c_machine_type
    ADD CONSTRAINT server_c_machine_type_name UNIQUE (name);


--
-- Name: server_c_status server_c_status_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server_c_status
    ADD CONSTRAINT server_c_status_id PRIMARY KEY (id);


--
-- Name: server_c_status server_c_status_name; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server_c_status
    ADD CONSTRAINT server_c_status_name UNIQUE (name);


--
-- Name: server server_id; Type: CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server
    ADD CONSTRAINT server_id PRIMARY KEY (id);


--
-- Name: reactor reactor_module_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor
    ADD CONSTRAINT reactor_module_fkey FOREIGN KEY (module) REFERENCES public.reactor_c_module(name);


--
-- Name: reactor_server_slot reactor_server_slot_reactor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_reactor_id_fkey FOREIGN KEY (reactor_id) REFERENCES public.reactor(id);


--
-- Name: reactor_server_slot reactor_server_slot_server_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor_server_slot
    ADD CONSTRAINT reactor_server_slot_server_id_fkey FOREIGN KEY (server_id) REFERENCES public.server(id);


--
-- Name: reactor reactor_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.reactor
    ADD CONSTRAINT reactor_status_fkey FOREIGN KEY (status) REFERENCES public.reactor_c_status(name);


--
-- Name: server server_machine_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server
    ADD CONSTRAINT server_machine_type_fkey FOREIGN KEY (machine_type) REFERENCES public.server_c_machine_type(name);


--
-- Name: server server_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gdt
--

ALTER TABLE ONLY public.server
    ADD CONSTRAINT server_status_fkey FOREIGN KEY (status) REFERENCES public.server_c_status(name);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

