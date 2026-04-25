import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

import pytest
from fastapi.testclient import TestClient
from main import app  # ajuste se seu app estiver em outro arquivo

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
