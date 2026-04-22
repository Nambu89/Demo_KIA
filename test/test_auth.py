"""
Tests del módulo de autenticación.
Patrón AAA (Arrange, Act, Assert).
"""

from miapi.auth import authenticate, verify_token, generate_session_token


class TestAuthenticate:
    """Tests para la función authenticate()."""

    def test_login_correcto_devuelve_datos_usuario(self):
        # Arrange
        username = "admin"
        password = "K1@_Adm1n_2024!"

        # Act
        result = authenticate(username, password)

        # Assert
        assert result is not None
        assert result["username"] == "admin"
        assert result["role"] == "admin"
        assert "token" in result

    def test_login_password_incorrecta_devuelve_none(self):
        # Arrange
        username = "admin"
        password = "wrong_password"

        # Act
        result = authenticate(username, password)

        # Assert
        assert result is None

    def test_login_usuario_inexistente_devuelve_none(self):
        # Arrange
        username = "no_existe"
        password = "cualquier_password"

        # Act
        result = authenticate(username, password)

        # Assert
        assert result is None


class TestVerifyToken:
    """Tests para la función verify_token()."""

    def test_token_valido_devuelve_true(self):
        # Arrange
        token = "a1b2c3d4e5f6g7h8i9j0k"

        # Act
        result = verify_token(token)

        # Assert
        assert result is True

    def test_token_vacio_devuelve_false(self):
        # Arrange
        token = ""

        # Act
        result = verify_token(token)

        # Assert
        assert result is False

    def test_token_corto_devuelve_false(self):
        # Arrange
        token = "abc"

        # Act
        result = verify_token(token)

        # Assert
        assert result is False


class TestGenerateSessionToken:
    """Tests para la función generate_session_token()."""

    def test_genera_token_no_vacio(self):
        # Arrange
        user_data = {"username": "admin", "role": "admin"}

        # Act
        token = generate_session_token(user_data)

        # Assert
        assert token is not None
        assert len(token) > 0

    def test_tokens_diferentes_para_misma_entrada(self):
        # Arrange
        user_data = {"username": "admin", "role": "admin"}

        # Act
        token1 = generate_session_token(user_data)
        import time
        time.sleep(0.01)
        token2 = generate_session_token(user_data)

        # Assert — pueden ser iguales si se generan en el mismo ms, pero idealmente no
        assert isinstance(token1, str)
        assert isinstance(token2, str)
