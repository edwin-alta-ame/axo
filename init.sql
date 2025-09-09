    CREATE TABLE roles (
      id SERIAL PRIMARY KEY,
      nombre_rol VARCHAR(50) UNIQUE NOT NULL,
      descripcion TEXT
    );
    CREATE TABLE usuarios (
      id SERIAL PRIMARY KEY,
      nombre VARCHAR(100) NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      contrasena VARCHAR(255) NOT NULL,
      rol_id SERIAL NOT NULL,
      fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      CONSTRAINT fk_rol
        FOREIGN KEY(rol_id) 
        REFERENCES roles(id)
        ON DELETE RESTRICT
    );
    CREATE TABLE permisos (
      id SERIAL PRIMARY KEY,
      nombre_permiso VARCHAR(100) UNIQUE NOT NULL,
      descripcion TEXT
    );
    CREATE TABLE roles_permisos (
      rol_id SERIAL NOT NULL,
      permiso_id SERIAL NOT NULL,
      PRIMARY KEY (rol_id, permiso_id),
      FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE CASCADE,
      FOREIGN KEY (permiso_id) REFERENCES permisos(id) ON DELETE CASCADE
    );
    INSERT INTO roles (nombre_rol, descripcion) VALUES
    ('admin', 'Rol para administradores con acceso total.'),
    ('usuario', 'Rol para usuarios básicos.');

    -- Insertar permisos iniciales
    INSERT INTO permisos (nombre_permiso, descripcion) VALUES
    ('ApiGetUser.post', 'Permite ver la lista de usuarios.'),
    ('ApiSignUp.post', 'Permite agregar un usuario.');

    -- Asignar permisos al rol de admin
    INSERT INTO roles_permisos (rol_id, permiso_id)
    SELECT
        (SELECT id FROM roles WHERE nombre_rol = 'admin'),
        id
    FROM permisos;

    -- Asignar permisos al rol de usuario básico
    INSERT INTO roles_permisos (rol_id, permiso_id)
    SELECT
        (SELECT id FROM roles WHERE nombre_rol = 'usuario'),
        id
    FROM permisos
    WHERE nombre_permiso IN ('ApiGetUser.post');

    -- Insertar un usuario admin de ejemplo
    INSERT INTO usuarios (nombre, email, contrasena, rol_id)
    VALUES (
        'Administrador',
        'axo@email.com',
        '1dc239777b3a67de263c96c560f2948d13aa89be92820984d9615881bcde838e', -- hash de 'axopass'
        (SELECT id FROM roles WHERE nombre_rol = 'admin')
    );
    -- Insertar un usuario regular de ejemplo
    INSERT INTO usuarios (nombre, email, contrasena, rol_id)
    VALUES (
        'Usuario',
        'usuario@email.com',
        '1dc239777b3a67de263c96c560f2948d13aa89be92820984d9615881bcde838e', -- hash de 'axopass'
        (SELECT id FROM roles WHERE nombre_rol = 'usuario')
    );
