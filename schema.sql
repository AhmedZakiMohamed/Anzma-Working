-- Reference tables

CREATE TABLE locations (
    id          SERIAL PRIMARY KEY,
    building    VARCHAR(50)  NOT NULL,
    floor       INT          NOT NULL,
    zone        VARCHAR(50)  NOT NULL,
    UNIQUE (building, floor, zone)
);

CREATE TABLE systems (
    id    SERIAL PRIMARY KEY,
    type  VARCHAR(20) NOT NULL UNIQUE
          CHECK (type IN ('HVAC','NETWORK','ACCESS','CCTV','FIRE_ALARM'))
);

CREATE TABLE assets (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    system_id    INT NOT NULL REFERENCES systems(id),
    location_id  INT NOT NULL REFERENCES locations(id),
    model        VARCHAR(100),
    status       VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
                 CHECK (status IN ('ACTIVE','INACTIVE','MAINTENANCE','FAULT')),
    installed_at DATE
);

-- Events (main fact table)

CREATE TABLE events (
    id          BIGSERIAL PRIMARY KEY,
    asset_id    INT NOT NULL REFERENCES assets(id),
    ts          TIMESTAMPTZ NOT NULL,
    event_type  VARCHAR(50) NOT NULL,
    severity    VARCHAR(10) NOT NULL DEFAULT 'INFO'
                CHECK (severity IN ('INFO','WARNING','CRITICAL')),
    value       DOUBLE PRECISION,
    unit        VARCHAR(20),
    details     JSONB
);

-- Indexes (TO better search)

CREATE INDEX idx_events_ts          ON events (ts);
CREATE INDEX idx_events_asset_ts    ON events (asset_id, ts);
CREATE INDEX idx_events_type        ON events (event_type);
CREATE INDEX idx_assets_system      ON assets (system_id);
CREATE INDEX idx_assets_location    ON assets (location_id);