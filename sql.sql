create table user_account (
	id serial primary key,
	username text not null unique,
	password text not null,
	discord_id text,
	role text not null default 'user',
	emails text[],
	unique(discord_id)
	-- emails text[],
	-- is_deleted boolean default false
);


create table jwt_token (
	token text,
	meta json,
	user_account_id int references user_account(id) on delete cascade
);


create table recovery_token (
	token text,
	user_account_id int references user_account(id) on delete cascade,
	expire_at timestamptz default now() + interval '30 minutes'
);

create table discord_state (
	state text,
	user_account_id int references user_account(id) on delete cascade,
	expire_at timestamptz default now() + interval '10 minutes'
);


