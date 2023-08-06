from typing import Any, Dict

import gensim
import penelope.utility as utility
import penelope.vendor.gensim as gensim_utility

from . import options

logger = utility.getLogger("")


def compute_score(id2word, model, corpus) -> float:
    try:
        dictionary = gensim_utility.create_dictionary(id2word)
        coherence_model = gensim.models.CoherenceModel(
            model=model, corpus=corpus, dictionary=dictionary, coherence='u_mass'
        )
        coherence_score = coherence_model.get_coherence()
    except Exception as ex:  # pylint: disable=broad-except
        logger.error(ex)
        coherence_score = None
    return coherence_score


def compute_scores(
    method: str,
    id2word: Dict[int, str],
    corpus: Any,
    start=10,
    stop: int = 20,
    step: int = 10,
    engine_args: Dict[str, Any] = None,
) -> Dict[str, Any]:

    algorithm_name = method.split('_')[1].upper()

    metrics = []

    dictionary = gensim_utility.create_dictionary(id2word)

    for num_topics in range(start, stop, step):

        algorithm = options.engine_options(algorithm_name, corpus, id2word, engine_args)

        engine = algorithm['engine']
        engine_options = algorithm['options']

        model = engine(**engine_options)

        coherence_score = gensim.models.CoherenceModel(
            model=model, corpus=corpus, dictionary=dictionary, coherence='u_mass'
        )

        perplexity_score = 2 ** model.log_perplexity(corpus, len(corpus))

        metric = dict(num_topics=num_topics, coherence_score=coherence_score, perplexity_score=perplexity_score)
        metrics.append(metric)

    # filename = os.path.join(target_folder, "metric_scores.json")

    # with open(filename, 'w') as fp:
    #     json.dump(model_data.options, fp)

    return metrics


# Can take a long time to run.
# model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=40, step=6)
# # Show graph
# limit=40; start=2; step=6;
# x = range(start, limit, step)
# plt.plot(x, coherence_values)
# plt.xlabel("Num Topics")
# plt.ylabel("Coherence score")
# plt.legend(("coherence_values"), loc='best')
# plt.show()
