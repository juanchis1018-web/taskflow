-- TaskFlow - export de la base de datos
-- Generado: 2026-11-14 08:38:19
-- Origen: taskflow_demo.sqlite

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    priority    TEXT    NOT NULL DEFAULT 'media' CHECK (priority IN ('baja', 'media', 'alta')),
    done        INTEGER NOT NULL DEFAULT 0,
    due_date    TEXT,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "tasks" VALUES(1,2,'Especificar requerimientos funcionales','Documento IEEE 29148 del proyecto','alta',1,'2026-10-05','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(2,2,'Diseñar modelo de base de datos','Tablas users y tasks con integridad referencial','alta',1,'2026-10-08','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(3,2,'Implementar API REST de tareas','Endpoints GET/POST/PUT/DELETE /api/tasks','alta',1,'2026-10-15','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(4,2,'Automatizar pruebas con pytest y Playwright','Unitarias, integración, seguridad y E2E','media',1,'2026-10-18','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(5,2,'Elaborar diagrama de despliegue UML','Nodos cliente, servidor web, aplicación y BD','media',1,'2026-11-10','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(6,2,'Configurar despliegue con Docker y Nginx','docker-compose con proxy inverso','media',0,'2026-11-14','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(7,2,'Grabar video de avance del proyecto','10 minutos en español','alta',0,'2026-11-16','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(8,3,'Diseñar interfaz gráfica de usuario','Mapa de navegación y vistas','alta',1,'2026-10-10','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(9,3,'Validar diseño adaptable en celular','Pruebas en 375 px y 768 px de ancho','media',0,'2026-11-12','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(10,3,'Revisar accesibilidad de formularios','Etiquetas, foco visible y contraste','baja',0,'2026-11-20','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(11,4,'Medir métricas ISO/IEC 25023','Cobertura, tiempos de respuesta, defectos','media',1,'2026-11-11','2026-11-14 13:38:19');
INSERT INTO "tasks" VALUES(12,4,'Preparar plan de pruebas de aceptación','Escenarios con el cliente','media',0,'2026-11-18','2026-11-14 13:38:19');
CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "users" VALUES(1,'admin','admin@taskflow.local','scrypt:32768:8:1$gLs3y3GH2jJOQUSc$16b0bb5bfc40d1521eb23ed9b08f24e78d9583f8c19545a5328b5bc6251c6c43015085364c7dcc45bb94b370755993faae12dee52d55958451c91a750eca1b2d','admin','2026-11-14 13:38:18');
INSERT INTO "users" VALUES(2,'jsmunoz','juan.munoz@taskflow.local','scrypt:32768:8:1$CIvB9efkAYq56HwR$08f10b52c744959c799648e5065b906af900a46515fcf6ca7b3eed934c52b93c028f7d9e4f73abc4469986f377ce0b8b836d46eb00f2e104dff26a89c72f1ef6','user','2026-11-14 13:38:18');
INSERT INTO "users" VALUES(3,'lgarcia','laura.garcia@taskflow.local','scrypt:32768:8:1$idJUBB0DcBOKA21W$d6c6df8f0c445d3ef984321d74d0fd56b0bceee7a6ae42b7f315cc06b2c8820fbb85833f35d86c2f0060bac9d4460d9d86c47aef0517f444939b3dfb982fcf6c','user','2026-11-14 13:38:18');
INSERT INTO "users" VALUES(4,'cperez','carlos.perez@taskflow.local','scrypt:32768:8:1$Fw9XoiiFDgolsX0z$5154cca676b39e2d4f59bc00c58204aa312a35c403ded9c15562ce0b85d8eed6b6a999f2955ba4d53203a1f639456a1752697390bd47c774a827ac1f6fdb788d','user','2026-11-14 13:38:19');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('users',4);
INSERT INTO "sqlite_sequence" VALUES('tasks',12);
COMMIT;
