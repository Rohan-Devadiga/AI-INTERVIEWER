import opensmile
import pandas as pd

smile=opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals       
)
def extract_features(audio:str)->pd.DataFrame:
    return smile.process_file(audio)

features=extract_features("answer.wav")
print(features.head())

def detect_hesitation(audio_path: str) -> bool:
    features = extract_features(audio_path)

    jitter = features["jitterLocal_sma3nz_amean"].values[0]
    loudness = features["loudness_sma3_amean"].values[0]
    pitch_var = features["F0semitoneFrom27.5Hz_sma3nz_stddevNorm"].values[0]

    # Example heuristic: high jitter or very low pitch variation → hesitation
    if jitter > 0.05 or pitch_var < 2 or loudness < -30:
        return True
    return False
