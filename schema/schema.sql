create table if not exists public.segments
(
    id          serial
    primary key,
    name        varchar(255) not null,
    description text
    );

alter table public.segments
    owner to root;

create table if not exists public.placersalespersons
(
    id        serial
    primary key,
    name      varchar(100) not null,
    cellphone varchar(20),
    email     varchar(255)
    );

alter table public.placersalespersons
    owner to root;

create table if not exists public.searches
(
    id          serial
    primary key,
    source      varchar(50),
    searchterm  varchar(255),
    searchdate  timestamp,
    results     text
    );

alter table public.searches
    owner to root;

create table if not exists public.companies
(
    id          serial
    primary key,
    name           varchar(255) not null,
    website        varchar(255) unique not null,
    description    text,
    relevancyscore integer,
    searchid       integer
    references public.searches,
    segmentid      integer
    references public.segments
    );

alter table public.companies
    owner to root;

create index if not exists companies_name_index
    on public.companies (name);

create table if not exists public.locations
(
    id         serial
    primary key,
    address    varchar(255),
    city       varchar(100),
    state      varchar(50),
    postalcode varchar(10),
    pobox      varchar(50),
    country    varchar(50),
    hours      varchar(255),
    companyid  integer
    references public.companies
    );

alter table public.locations
    owner to root;

create table if not exists public.leads
(
    id                  serial
    primary key,
    name                varchar(5000) not null,
    title               varchar(5000),
    email               varchar(5000),
    workphone           varchar(20),
    cellphone           varchar(20),
    locationid          integer
    references public.locations,
    companyid           integer
    references public.companies,
    placersalespersonid integer
    references public.placersalespersons
    );

alter table public.leads
    owner to root;

create index if not exists leads_name_index
    on public.leads (name);
