"""
Tests del módulo de base de datos.
Patrón AAA (Arrange, Act, Assert).
"""

from miapi.database import get_connection, create_user, find_user, search_users, delete_user


class TestGetConnection:
    """Tests para get_connection()."""

    def test_devuelve_conexion_valida(self):
        # Arrange & Act
        conn = get_connection()

        # Assert
        assert conn is not None
        conn.close()

    def test_tablas_creadas_correctamente(self):
        # Arrange & Act
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        # Assert
        assert "users" in tables
        assert "audit_log" in tables
        conn.close()


class TestCreateUser:
    """Tests para create_user()."""

    def test_crea_usuario_devuelve_id(self):
        # Arrange
        username = "test_user"
        password = "test_password"
        email = "test@example.com"

        # Act
        user_id = create_user(username, password, email)

        # Assert
        assert isinstance(user_id, int)
        assert user_id > 0


class TestFindUser:
    """Tests para find_user()."""

    def test_usuario_no_existente_devuelve_none(self):
        # Arrange
        username = "inexistente"

        # Act
        result = find_user(username)

        # Assert
        assert result is None


class TestSearchUsers:
    """Tests para search_users()."""

    def test_busqueda_sin_resultados_devuelve_lista_vacia(self):
        # Arrange
        search_term = "xyz_no_existe"

        # Act
        results = search_users(search_term)

        # Assert
        assert isinstance(results, list)
        assert len(results) == 0


class TestDeleteUser:
    """Tests para delete_user()."""

    def test_eliminar_usuario_inexistente_devuelve_false(self):
        # Arrange
        user_id = 99999

        # Act
        result = delete_user(user_id)

        # Assert
        assert result is False
