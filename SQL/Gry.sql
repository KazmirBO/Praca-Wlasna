CREATE TABLE gry (
    id     INTEGER PRIMARY KEY AUTO_INCREMENT,
    nazwa  VARCHAR(50) NOT NULL
);


CREATE TABLE kto (
    id        INTEGER PRIMARY KEY AUTO_INCREMENT,
    imie      VARCHAR(30) NOT NULL,
    nazwisko  VARCHAR(30) NOT NULL,
    telefon   VARCHAR(9) NOT NULL
);


CREATE TABLE wyp (
    id       INTEGER PRIMARY KEY AUTO_INCREMENT,
    gry_id   INTEGER NOT NULL,
    kto_id   INTEGER NOT NULL,
    datawyp  DATE NOT NULL,
    czywyp   BOOLEAN NOT NULL
);

ALTER TABLE wyp
    ADD CONSTRAINT wyp_gry_fk FOREIGN KEY ( gry_id )
        REFERENCES gry ( id );

ALTER TABLE wyp
    ADD CONSTRAINT wyp_kto_fk FOREIGN KEY ( kto_id )
        REFERENCES kto ( id );

--- UPDATE kto SET imie='',nazwisko='',telefon= WHERE id=;
