"""
Zemberek: Simple Classification Example
Documentation: https://bit.ly/2BNKPmP
Java Code Example: https://bit.ly/2JsoO1i
fastText Documentation: https://bit.ly/31YVBS8
"""
import subprocess
from pathlib import Path
from typing import List

from jpype import JClass, JString, java

from examples import DATA_PATH, JAVA_PATH, ZEMBEREK_PATH

__all__: List[str] = ['run']


FastTextClassifier: JClass = JClass(
    'zemberek.classification.FastTextClassifier'
)
TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')


def run(sentence: str) -> None:
    """
    News classification example. Trains a new model if there are no model
    available.

    Args:
        sentence (str): Sentence to classify.
    """
    label_data_path: Path = DATA_PATH.joinpath(
        'classification', 'news-title-category-set'
    )
    model_path: Path = label_data_path.with_suffix('.model')

    if not model_path.is_file():

        print('Could not find a model. Training a new one...')

        if not label_data_path.is_file():
            raise FileNotFoundError(
                'Could not train a model!'
                ' Please include news-title-category-set!'
            )

        subprocess.run(
            [
                JAVA_PATH,
                '-jar',
                ZEMBEREK_PATH,
                'TrainClassifier',
                '-i',
                label_data_path,
                '-o',
                model_path,
                '--learningRate',
                '0.1',
                '--epochCount',
                '50',
                '--applyQuantization',
                '--cutOff',
                '15000',
            ],
            check=True,
        )

    classifier: FastTextClassifier = FastTextClassifier.load(model_path)

    processed: str = ' '.join(
        [
            str(token)
            for token in TurkishTokenizer.DEFAULT.tokenizeToStrings(
                JString(sentence)
            )
        ]
    ).lower()

    results: java.util.ArrayList = classifier.predict(processed, 3)

    print(f'Sentence: {sentence}')

    for i, result in enumerate(results):
        print(
            f'\nItem {i + 1}: {result.item}',
            f'\nScore {i + 1}: {result.score}',
        )
