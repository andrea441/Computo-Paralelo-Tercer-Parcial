CREATE TABLE sucursal (
    idsucursal      VARCHAR2(5),
    nombresucursal  VARCHAR2(15),
    ciudadsucursal  VARCHAR2(15),
    activos         NUMBER,
    region          VARCHAR2(2),
    PRIMARY KEY (idsucursal)
);

CREATE TABLE prestamo (
    noprestamo  VARCHAR2(15),
    idsucursal  VARCHAR2(5),
    cantidad    NUMBER,
    PRIMARY KEY (noprestamo)
);

CREATE TABLE log_replicacion (
    tabla           VARCHAR2(20),
    operacion       VARCHAR2(10),
    datos           CLOB,
    fecha_registro  TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE OR REPLACE TRIGGER trg_log_sucursal
AFTER INSERT ON sucursal
FOR EACH ROW
BEGIN
    INSERT INTO log_replicacion (tabla, operacion, datos)
    VALUES (
        'sucursal',
        'insert',
        '{"idsucursal":"'
        || :NEW.idsucursal || '", "nombresucursal":"'
        || :NEW.nombresucursal || '", "ciudadsucursal":"'
        || :NEW.ciudadsucursal || '", "activos":'
        || :NEW.activos || ', "region":"'
        || :NEW.region || '"}'
    );
END;
/


CREATE OR REPLACE TRIGGER trg_log_prestamo
AFTER INSERT ON prestamo
FOR EACH ROW
BEGIN
    INSERT INTO log_replicacion (tabla, operacion, datos)
    VALUES (
        'prestamo',
        'insert',
        '{"noprestamo":"'
        || :NEW.noprestamo || '", "idsucursal":"'
        || :NEW.idsucursal || '", "cantidad":'
        || :NEW.cantidad || '}'
    );
END;
/

CREATE OR REPLACE TRIGGER trg_log_sucursal_delete
AFTER DELETE ON sucursal
FOR EACH ROW
BEGIN
    INSERT INTO log_replicacion (tabla, operacion, datos)
    VALUES (
        'sucursal',
        'delete',
        '{"idsucursal":"'||:OLD.idsucursal||'"}'
    );
END;
/

CREATE OR REPLACE TRIGGER trg_log_prestamo_delete
AFTER DELETE ON prestamo
FOR EACH ROW
BEGIN
    INSERT INTO log_replicacion (tabla, operacion, datos)
    VALUES (
        'prestamo',
        'delete',
        '{"noprestamo":"'||:OLD.noprestamo||'"}'
    );
END;
/

CREATE OR REPLACE TRIGGER trg_log_sucursal_update
AFTER UPDATE ON sucursal
FOR EACH ROW
BEGIN
    INSERT INTO log_replicacion (tabla, operacion, datos)
    VALUES (
        'sucursal',
        'update',
        '{"idsucursal":"'||:NEW.idsucursal||'", "nombresucursal":"'||:NEW.nombresucursal||'", "ciudadsucursal":"'||:NEW.ciudadsucursal||'", "activos":'||:NEW.activos||', "region":"'||:NEW.region||'"}'
    );
END;
/

CREATE OR REPLACE TRIGGER trg_log_prestamo_update
AFTER UPDATE ON prestamo
FOR EACH ROW
BEGIN
    INSERT INTO log_replicacion (tabla, operacion, datos)
    VALUES (
        'prestamo',
        'update',
        '{"noprestamo":"'||:NEW.noprestamo||'", "idsucursal":"'||:NEW.idsucursal||'", "cantidad":'||:NEW.cantidad||'}'
    );
END;
/