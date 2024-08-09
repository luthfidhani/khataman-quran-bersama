-- Tabel member
CREATE TABLE member (
    id VARCHAR PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    is_delete BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabel period
CREATE TABLE period (
    id VARCHAR PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    can_update BOOLEAN NOT NULL DEFAULT FALSE,
    can_lock BOOLEAN NOT NULL DEFAULT FALSE,
    is_done BOOLEAN NOT NULL DEFAULT FALSE
);

-- Tabel checklist
CREATE TABLE checklist (
    id VARCHAR PRIMARY KEY,
    member_id VARCHAR NOT NULL,
    period_id VARCHAR NOT NULL,
    juz VARCHAR[] NOT NULL,
    checklist BOOLEAN[] NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (member_id) REFERENCES member(id),
    FOREIGN KEY (period_id) REFERENCES period(id)
);
