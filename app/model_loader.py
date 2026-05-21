import os
import joblib

_model_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "ml", "model.joblib")
)

try:
    model = joblib.load(_model_path)
except FileNotFoundError:
    raise RuntimeError(
        f"Model not found at {_model_path}. Run 'python ml/train.py' first."
    )
