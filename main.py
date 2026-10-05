import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
	GradientBoostingClassifier,
	RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
	accuracy_score,
	classification_report,
	confusion_matrix,
	roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

STAGE_NAMES = {
	'2': 'Fountain',
	'3': 'Stadium',
	'8': 'Story',
	'28': 'Dreamland',
	'31': 'Battlefield',
	'32': 'Final Destination',
}
# https://gamefaqs.gamespot.com/boards/516492-super-smash-bros-melee/68128269
CHARACTER_NAMES = [
	'Mario',
	'Fox',
	'C.Falcon',
	'Donkey Kong',
	'Kirby',
	'Bowser',
	'Link',
	'Sheik',
	'Ness',
	'Peach',
	'Popo',
	'Nana',
	'Pikachu',
	'Samus',
	'Yoshi',
	'Jigglypuff',
	'Mewtwo',
	'Luigi',
	'Marth',
	'Zelda',
	'Young Link',
	'Dr. Mario',
	'Falco',
	'Pichu',
	'Mr. Game & Watch',
	'Ganondorf',
	'Roy',
]

df = pd.read_csv('games.csv')

# cleaning

df = df[df['player total damage'] != 0]
df = df[df['opponent total damage'] != 0]
df = df[(df['player stocks'] == 0) | (df['opponent stocks'] == 0)]

# define target + features

TARGET = 'win'
features = [
	'player character',
	'opponent character',
	'player total damage',
	'opponent total damage',
	'player openings',
	'opponent openings',
	'player neutral wins',
	'opponent neutral wins',
	'total neutral breaks',
	'stage',
	'match length',
]
X = df[features]
y = df[TARGET]

# identify categorical and numeric columns

categorical_features = [
	'player character',
	'opponent character',
	'stage',
]
numeric_features = [
	'player total damage',
	'opponent total damage',
	'player openings',
	'opponent openings',
	'player neutral wins',
	'opponent neutral wins',
	'total neutral breaks',
	'match length',
]

# preprocessing

numeric_pipeline = Pipeline([
	('imputer', SimpleImputer(strategy='median')),
	('scaler', StandardScaler()),
])
categorical_pipeline = Pipeline([
	('imputer', SimpleImputer(strategy='most_frequent')),
	('onehot', OneHotEncoder(handle_unknown='ignore')),
])
preprocessor = ColumnTransformer([
	('numeric', numeric_pipeline, numeric_features),
	('categorical', categorical_pipeline, categorical_features),
])

# creating the model

models = {
	'Gradient Boosting': GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        min_samples_split=5,
        random_state=42,
	),
	'Logistic Regression': LogisticRegression(
		max_iter=1000,
		class_weight='balanced',
		random_state=42,
	),
    'Random Forest': RandomForestClassifier(
		n_estimators=300,
		max_depth=None,
		min_samples_split=5,
		random_state=42,
		class_weight='balanced',
		n_jobs=-1,
	),
}

# test/train split of data

X_train, X_test, y_train, y_test = train_test_split(
	X, y,
	test_size=0.20,
	# 42 is an excellent number
	random_state=42,
	stratify=y,
)
print('Training examples:', len(X_train))
print('Testing examples:', len(X_test))

for name, model in models.items():
	print('RUNNING: ' + name)
	pipeline = Pipeline([
		('preprocessor', preprocessor),
		('model', model),
	])

	# training
	pipeline.fit(X_train, y_train)

	# evaluating the model

	predictions = pipeline.predict(X_test)
	probabilities = pipeline.predict_proba(X_test)[:, 1]

	accuracy = accuracy_score(y_test, predictions)
	auc = roc_auc_score(y_test, probabilities)

	print(f'Accuracy: {accuracy:.4f}')
	print(f'ROC-AUC:  {auc:.4f}')

	print('\nClassification Report:')
	print(classification_report(y_test, predictions))

	print('\nConfusion Matrix:')
	print(confusion_matrix(y_test, predictions))

	# predicting a new match

	new_match = pd.DataFrame([{
		'player character': CHARACTER_NAMES.index('Sheik'),
		'opponent character': CHARACTER_NAMES.index('Fox'),
		'player total damage': 320,
		'opponent total damage': 350,
		'player openings': 30,
		'opponent openings': 24,
		'player neutral wins': 11,
		'opponent neutral wins': 10,
		'total neutral breaks': 21,
		'stage': 3,
		'match length': 8400,
	}])

	prediction = pipeline.predict(new_match)[0]
	win_probability = pipeline.predict_proba(new_match)[0][1]

	if prediction == 1:
		print('Player Wins')
	else:
		print('Opponent Wins')
	print(f'Player win probability: {win_probability:.2%}')