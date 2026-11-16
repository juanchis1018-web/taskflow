-- TaskFlow - export de la base de datos
-- Generado: 2026-11-14 08:38:19
-- Origen: taskflow_demo.sqlite

CREATE DATABASE IF NOT EXISTS taskflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE taskflow;

DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(20)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('user','admin') NOT NULL DEFAULT 'user',
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE tasks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priority    ENUM('baja','media','alta') NOT NULL DEFAULT 'media',
    done        TINYINT(1) NOT NULL DEFAULT 0,
    due_date    DATE NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_tasks_user (user_id)
) ENGINE=InnoDB;

INSERT INTO users (id, username, email, password_hash, role, created_at) VALUES
  (1, 'admin', 'admin@taskflow.local', 'scrypt:32768:8:1$gLs3y3GH2jJOQUSc$16b0bb5bfc40d1521eb23ed9b08f24e78d9583f8c19545a5328b5bc6251c6c43015085364c7dcc45bb94b370755993faae12dee52d55958451c91a750eca1b2d', 'admin', '2026-11-14 13:38:18'),
  (2, 'jsmunoz', 'juan.munoz@taskflow.local', 'scrypt:32768:8:1$CIvB9efkAYq56HwR$08f10b52c744959c799648e5065b906af900a46515fcf6ca7b3eed934c52b93c028f7d9e4f73abc4469986f377ce0b8b836d46eb00f2e104dff26a89c72f1ef6', 'user', '2026-11-14 13:38:18'),
  (3, 'lgarcia', 'laura.garcia@taskflow.local', 'scrypt:32768:8:1$idJUBB0DcBOKA21W$d6c6df8f0c445d3ef984321d74d0fd56b0bceee7a6ae42b7f315cc06b2c8820fbb85833f35d86c2f0060bac9d4460d9d86c47aef0517f444939b3dfb982fcf6c', 'user', '2026-11-14 13:38:18'),
  (4, 'cperez', 'carlos.perez@taskflow.local', 'scrypt:32768:8:1$Fw9XoiiFDgolsX0z$5154cca676b39e2d4f59bc00c58204aa312a35c403ded9c15562ce0b85d8eed6b6a999f2955ba4d53203a1f639456a1752697390bd47c774a827ac1f6fdb788d', 'user', '2026-11-14 13:38:19');

INSERT INTO tasks (id, user_id, title, description, priority, done, due_date, created_at) VALUES
  (1, 2, 'Especificar requerimientos funcionales', 'Documento IEEE 29148 del proyecto', 'alta', 1, '2026-10-05', '2026-11-14 13:38:19'),
  (2, 2, 'Diseñar modelo de base de datos', 'Tablas users y tasks con integridad referencial', 'alta', 1, '2026-10-08', '2026-11-14 13:38:19'),
  (3, 2, 'Implementar API REST de tareas', 'Endpoints GET/POST/PUT/DELETE /api/tasks', 'alta', 1, '2026-10-15', '2026-11-14 13:38:19'),
  (4, 2, 'Automatizar pruebas con pytest y Playwright', 'Unitarias, integración, seguridad y E2E', 'media', 1, '2026-10-18', '2026-11-14 13:38:19'),
  (5, 2, 'Elaborar diagrama de despliegue UML', 'Nodos cliente, servidor web, aplicación y BD', 'media', 1, '2026-11-10', '2026-11-14 13:38:19'),
  (6, 2, 'Configurar despliegue con Docker y Nginx', 'docker-compose con proxy inverso', 'media', 0, '2026-11-14', '2026-11-14 13:38:19'),
  (7, 2, 'Grabar video de avance del proyecto', '10 minutos en español', 'alta', 0, '2026-11-16', '2026-11-14 13:38:19'),
  (8, 3, 'Diseñar interfaz gráfica de usuario', 'Mapa de navegación y vistas', 'alta', 1, '2026-10-10', '2026-11-14 13:38:19'),
  (9, 3, 'Validar diseño adaptable en celular', 'Pruebas en 375 px y 768 px de ancho', 'media', 0, '2026-11-12', '2026-11-14 13:38:19'),
  (10, 3, 'Revisar accesibilidad de formularios', 'Etiquetas, foco visible y contraste', 'baja', 0, '2026-11-20', '2026-11-14 13:38:19'),
  (11, 4, 'Medir métricas ISO/IEC 25023', 'Cobertura, tiempos de respuesta, defectos', 'media', 1, '2026-11-11', '2026-11-14 13:38:19'),
  (12, 4, 'Preparar plan de pruebas de aceptación', 'Escenarios con el cliente', 'media', 0, '2026-11-18', '2026-11-14 13:38:19');

