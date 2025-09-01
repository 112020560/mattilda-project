-- Insertar colegios de ejemplo
INSERT INTO schools (name, address, phone, email, is_active) VALUES
('Colegio San José', 'Avenida Central 123, San José', '2234-5678', 'info@colegiosanjose.cr', true),
('Instituto Nacional', 'Calle 15, Cartago', '2551-9876', 'contacto@institutoacional.cr', true),
('Liceo de Heredia', 'Boulevard Principal, Heredia', '2260-1234', 'admin@liceoheredia.cr', true);

-- Insertar estudiantes de ejemplo
INSERT INTO students (first_name, last_name, email, phone, student_id, enrollment_date, birth_date, school_id, is_active) VALUES
('Juan', 'Pérez', 'juan.perez@email.com', '8888-1111', 'EST001', '2024-02-01', '2008-05-15', 1, true),
('María', 'González', 'maria.gonzalez@email.com', '8888-2222', 'EST002', '2024-02-01', '2009-03-20', 1, true),
('Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '8888-3333', 'EST003', '2024-02-15', '2008-11-10', 2, true),
('Ana', 'Martínez', 'ana.martinez@email.com', '8888-4444', 'EST004', '2024-02-20', '2009-07-25', 2, true);