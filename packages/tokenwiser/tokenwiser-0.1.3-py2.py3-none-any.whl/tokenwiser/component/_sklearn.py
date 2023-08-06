from spacy.language import Language


def attach_sklearn_categoriser(nlp, pipe_name, estimator):
    """
    This function will attach a scikit-learn compatible estimator to
    the pipeline which will feed predictions to the `.cats` property.

    This is useful if you're interesting in added a pre-trained sklearn
    model to the pipeline. This is **not** useful if you're interested
    in training a new model via spaCy, check out the `tokenwiser.model`
    submodule for that.

    Usage:

    ```python
    import spacy

    from sklearn.pipeline import make_pipeline
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression

    from tokenwiser.component import attach_sklearn_categoriser

    X = [
        "i really like this post",
        "thanks for that comment",
        "i enjoy this friendly forum",
        "this is a bad post",
        "i dislike this article",
        "this is not well written"
    ]

    y = ["pos", "pos", "pos", "neg", "neg", "neg"]

    # Note that we're training a pipeline here via a single-batch `.fit()` method
    pipe = make_pipeline(CountVectorizer(), LogisticRegression()).fit(X, y)

    nlp = spacy.load("en_core_web_sm")
    # This is where we attach our pre-trained model as a pipeline step.
    attach_sklearn_categoriser(nlp, pipe_name="silly_sentiment", estimator=pipe)

    assert nlp.pipe_names[-1] == "silly_sentiment"
    assert nlp("this post i really like").cats["pos"] > 0.5
    ```
    """

    @Language.component(pipe_name)
    def my_component(doc):
        pred = estimator.predict([doc.text])[0]
        proba = estimator.predict_proba([doc.text]).max()
        doc.cats[pred] = proba
        return doc

    nlp.add_pipe(pipe_name)
