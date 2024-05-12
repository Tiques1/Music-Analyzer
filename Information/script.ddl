-- Generated by Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   at:        2024-04-30 01:25:39 YEKT
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE album (
    id    INTEGER NOT NULL,
    name  text,
    year  DATE,
    label INTEGER,
    genre INTEGER
);

ALTER TABLE album ADD CONSTRAINT album_pk PRIMARY KEY ( id );

ALTER TABLE album ADD CONSTRAINT album__un UNIQUE ( id );

CREATE TABLE album_autorship (
    album  INTEGER,
    artist INTEGER
);

CREATE TABLE artist (
    id   INTEGER NOT NULL,
    name text
);

ALTER TABLE artist ADD CONSTRAINT artist_pk PRIMARY KEY ( id );

ALTER TABLE artist ADD CONSTRAINT artist__un UNIQUE ( id );

CREATE TABLE autorship (
    track  INTEGER,
    artist INTEGER
);

CREATE TABLE genre (
    id   INTEGER NOT NULL,
    name text
);

ALTER TABLE genre ADD CONSTRAINT genre_pk PRIMARY KEY ( id );

ALTER TABLE genre ADD CONSTRAINT genre__un UNIQUE ( id );

CREATE TABLE label (
    id   INTEGER NOT NULL,
    name text
);

ALTER TABLE label ADD CONSTRAINT label_pk PRIMARY KEY ( id );

ALTER TABLE label ADD CONSTRAINT label__unv1 UNIQUE ( id );

CREATE TABLE track (
    id        INTEGER NOT NULL,
    name      text,
    album_num INTEGER,
    album     INTEGER NOT NULL
);

ALTER TABLE track ADD CONSTRAINT track_pk PRIMARY KEY ( id );

ALTER TABLE track ADD CONSTRAINT track__un UNIQUE ( id );

ALTER TABLE album_autorship
    ADD CONSTRAINT album_autorship_album_fk FOREIGN KEY ( album )
        REFERENCES album ( id );

ALTER TABLE album
    ADD CONSTRAINT album_genre_fk FOREIGN KEY ( genre )
        REFERENCES genre ( id );

ALTER TABLE album
    ADD CONSTRAINT album_label_fk FOREIGN KEY ( label )
        REFERENCES label ( id );

ALTER TABLE autorship
    ADD CONSTRAINT fk_autorship_artist FOREIGN KEY ( artist )
        REFERENCES artist ( id );

ALTER TABLE album_autorship
    ADD CONSTRAINT fk_autorship_artistv2 FOREIGN KEY ( artist )
        REFERENCES artist ( id );

ALTER TABLE autorship
    ADD CONSTRAINT fk_autorship_track FOREIGN KEY ( track )
        REFERENCES track ( id );

ALTER TABLE track
    ADD CONSTRAINT track_album_fk FOREIGN KEY ( album )
        REFERENCES album ( id );



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             7
-- CREATE INDEX                             0
-- ALTER TABLE                             17
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
