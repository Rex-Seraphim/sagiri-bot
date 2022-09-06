import asyncio
from pathlib import Path
from loguru import logger

try:
    from .MockingBirdForUse.mockingbirdforuse import MockingBird
    mockingbird_available = True
except ImportError:
    mockingbird_available = False

model_path = Path.cwd() / "statics" / "models" / "mockingbird"
if not model_path.exists():
    models = []
    models_available = False
else:
    models = [i.stem for i in model_path.iterdir() if i.is_dir()]

    try:
        if mockingbird_available:
            mockingbird = MockingBird() #type: ignore
            mockingbird.load_model(
                model_path / "encoder.pt",
                model_path / "hifigan.pt"
            )
            current_model = "azusa"
            mockingbird.set_synthesizer(model_path / current_model / f"{current_model}.pt")
            generate_accuracy = 9
            models_available = True
        else:
            models_available = False
    except FileNotFoundError:
        models_available = False


def get_voice(content: str):
    return mockingbird.synthesize(
        content,
        model_path / current_model / "record.wav",
        min_stop_token=generate_accuracy
    ).getvalue()


async def set_model(model_name: str) -> bool:
    global current_model
    try:
        asyncio.get_event_loop().run_in_executor(
            None, mockingbird.set_synthesizer, model_path / model_name / f"{model_name}.pt"
        )
        current_model = model_name
        return True
    except Exception as e:
        logger.error(e)
        return False


def set_accuracy(accuracy: int):
    global generate_accuracy
    generate_accuracy = accuracy
