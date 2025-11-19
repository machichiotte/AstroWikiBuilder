# tests/unit/test_utils/test_directory_utils.py
"""
Tests pour le module directory_utils.
"""

import os

from src.utils.directory_utils import create_output_directories


class TestDirectoryUtils:
    """Tests des utilitaires de gestion de répertoires."""

    def test_create_output_directories(self, tmp_path):
        """Test de création des répertoires de sortie."""
        output_dir = str(tmp_path / "output")
        drafts_dir = str(tmp_path / "drafts")
        consolidated_dir = str(tmp_path / "consolidated")

        # Vérifier que les répertoires n'existent pas
        assert not os.path.exists(output_dir)
        assert not os.path.exists(drafts_dir)
        assert not os.path.exists(consolidated_dir)

        # Créer les répertoires
        create_output_directories(output_dir, drafts_dir, consolidated_dir)

        # Vérifier qu'ils existent maintenant
        assert os.path.exists(output_dir)
        assert os.path.exists(drafts_dir)
        assert os.path.exists(consolidated_dir)

    def test_create_output_directories_without_consolidated(self, tmp_path):
        """Test sans le répertoire consolidated."""
        output_dir = str(tmp_path / "output2")
        drafts_dir = str(tmp_path / "drafts2")

        create_output_directories(output_dir, drafts_dir)

        assert os.path.exists(output_dir)
        assert os.path.exists(drafts_dir)

    def test_create_output_directories_already_exist(self, tmp_path):
        """Test quand les répertoires existent déjà."""
        output_dir = str(tmp_path / "output3")
        drafts_dir = str(tmp_path / "drafts3")

        # Créer une première fois
        create_output_directories(output_dir, drafts_dir)

        # Créer une deuxième fois (ne devrait pas échouer)
        create_output_directories(output_dir, drafts_dir)

        # Vérifie qu'ils existent toujours
        assert os.path.exists(output_dir)
        assert os.path.exists(drafts_dir)
