from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def train_rf_shot_model(train_df,test_df):
    
    features = [
        "PERIOD",
        "MINUTES_REMAINING",
        "SECONDS_REMAINING",
        "ACTION_TYPE",
        "SHOT_TYPE",
        "SHOT_ZONE_BASIC",
        "SHOT_ZONE_AREA",
        "SHOT_ZONE_RANGE",
        "SHOT_DISTANCE",
        "LOC_X",
        "LOC_Y",
        "HTM",
        "VTM",
        "TEAM_NAME"]

    X_train = train_df[features]
    y_train = train_df["SHOT_MADE_FLAG"]

    X_test = test_df[features]
    y_test = test_df["SHOT_MADE_FLAG"]


    categorical_features = [
        "ACTION_TYPE",
        "SHOT_TYPE",
        "SHOT_ZONE_BASIC",
        "SHOT_ZONE_AREA",
        "SHOT_ZONE_RANGE",
        "HTM",
        "VTM",
        "TEAM_NAME"
    ]

    numeric_features = [
        "PERIOD",
        "MINUTES_REMAINING",
        "SECONDS_REMAINING",
        "SHOT_DISTANCE",
        "LOC_X",
        "LOC_Y"
    ]

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features)
        ]
    )

    # Model
    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", rf)
    ])

    # Train
    pipeline.fit(X_train, y_train)

    # Predict
    y_pred = pipeline.predict(X_test)

    # Metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0)
    }

    print("Model Performance:")
    for k, v in metrics.items():
        print(f"{k}: {v:.3f}")

