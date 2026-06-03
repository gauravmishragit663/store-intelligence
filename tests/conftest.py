# PROMPT:
# Generate pytest fixtures for FastAPI testing.

# CHANGES MADE:
# Modified fixtures to support project-specific endpoints
# and test data requirements.

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)