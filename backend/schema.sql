CREATE TABLE IF NOT EXISTS items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    filename    TEXT NOT NULL,
    original    TEXT NOT NULL,
    annotated   TEXT NOT NULL,
    garment     TEXT,
    colour      TEXT,
    confidence  REAL,
    uploaded_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS outfits (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS outfit_items (
    outfit_id  INTEGER REFERENCES outfits(id) ON DELETE CASCADE,
    item_id    INTEGER REFERENCES items(id)   ON DELETE CASCADE,
    PRIMARY KEY (outfit_id, item_id)
);