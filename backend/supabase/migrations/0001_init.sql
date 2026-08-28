-- Civic Resolution prototype schema.
-- All data here is synthetic/demo data for a hackathon prototype.
-- RLS is enabled with NO anon/authenticated policies: only the backend,
-- using the service_role key, can read or write. The frontend never talks
-- to Supabase directly.

create extension if not exists pgcrypto;

create table if not exists citizens (
    id uuid primary key default gen_random_uuid(),
    display_name text not null,
    persona_key text not null unique,
    phone text,
    created_at timestamptz not null default now()
);

create table if not exists authorities (
    id uuid primary key default gen_random_uuid(),
    name text not null unique,
    authority_type text not null,
    jurisdiction_area text not null,
    contact_person_name text not null,
    contact_role text not null,
    escalation_authority_id uuid references authorities(id),
    created_at timestamptz not null default now()
);

create table if not exists services (
    id uuid primary key default gen_random_uuid(),
    category text not null unique,
    display_name text not null,
    description text not null,
    default_authority_type text not null,
    required_evidence text[] not null default '{}',
    sla_days int not null,
    stage_template jsonb not null,
    created_at timestamptz not null default now()
);

create table if not exists problems (
    id uuid primary key default gen_random_uuid(),
    citizen_id uuid not null references citizens(id),
    raw_text text not null,
    location_text text,
    latitude numeric,
    longitude numeric,
    service_id uuid references services(id),
    ai_understanding jsonb,
    created_at timestamptz not null default now()
);
create index if not exists idx_problems_citizen_id on problems(citizen_id);
create index if not exists idx_problems_service_id on problems(service_id);

create table if not exists cases (
    id uuid primary key default gen_random_uuid(),
    case_number text not null unique,
    problem_id uuid not null references problems(id),
    citizen_id uuid not null references citizens(id),
    authority_id uuid not null references authorities(id),
    service_id uuid not null references services(id),
    status text not null,
    current_stage text not null,
    opened_at timestamptz not null,
    expected_resolution_date date not null,
    last_status_change_at timestamptz not null,
    resolution_verification_count int not null default 0,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);
create index if not exists idx_cases_citizen_id on cases(citizen_id);
create index if not exists idx_cases_problem_id on cases(problem_id);
create index if not exists idx_cases_case_number on cases(case_number);

create table if not exists case_timeline (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id),
    stage_name text not null,
    status text not null,
    actor_type text not null,
    actor_name text,
    note text,
    occurred_at timestamptz not null,
    sequence_order int not null
);
create index if not exists idx_case_timeline_case_id on case_timeline(case_id);

create table if not exists evidence (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id),
    uploaded_by text not null,
    file_name text not null,
    file_url text,
    description_text text,
    ai_interpretation jsonb,
    stage_context text,
    created_at timestamptz not null default now()
);
create index if not exists idx_evidence_case_id on evidence(case_id);

create table if not exists community_reports (
    id uuid primary key default gen_random_uuid(),
    problem_id uuid not null references problems(id),
    case_id uuid references cases(id),
    reporter_citizen_id uuid references citizens(id),
    confirmation_type text not null,
    comment_text text,
    created_at timestamptz not null default now()
);
create index if not exists idx_community_reports_problem_id on community_reports(problem_id);

create table if not exists escalations (
    id uuid primary key default gen_random_uuid(),
    case_id uuid not null references cases(id),
    escalated_to_authority_id uuid not null references authorities(id),
    reason_text text not null,
    payload_snapshot jsonb not null,
    status text not null default 'submitted',
    created_at timestamptz not null default now()
);
create index if not exists idx_escalations_case_id on escalations(case_id);

alter table citizens enable row level security;
alter table authorities enable row level security;
alter table services enable row level security;
alter table problems enable row level security;
alter table cases enable row level security;
alter table case_timeline enable row level security;
alter table evidence enable row level security;
alter table community_reports enable row level security;
alter table escalations enable row level security;
