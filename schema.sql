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

create table if not exists public.companies
(
    id          serial
    primary key,
    name        varchar(255) not null,
    website     varchar(255),
    description text,
    segmentid   integer
    references public.segments
    );

alter table public.companies
    owner to root;

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
    companyid  integer
    references public.companies
    );

alter table public.locations
    owner to root;

create table if not exists public.leadspersons
(
    id                  serial
    primary key,
    name                varchar(100) not null,
    title               varchar(50),
    email               varchar(255),
    workphone           varchar(20),
    cellphone           varchar(20),
    locationid          integer
    references public.locations,
    companyid           integer
    references public.companies,
    placersalespersonid integer
    references public.placersalespersons
    );

alter table public.leadspersons
    owner to root;

