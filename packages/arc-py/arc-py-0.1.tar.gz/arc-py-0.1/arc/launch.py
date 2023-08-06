import os

from read import parse_dir

here = os.path.dirname(__file__)

train_dir = os.path.join(here, "original", "ARC", "data", "training")
eval_dir = os.path.join(here, "original", "ARC", "data", "evaluation")

train_set = parse_dir(train_dir)
eval_set = parse_dir(eval_dir)

assert train_set, "Training set is empty - this distribution of arc utils is broken."
assert eval_set, "Evaluation set is empty - this distribution of arc utils is broken."

def describe(arc_task_set):

    number_examples = [len(x.train_pairs) for x in arc_task_set]
    number_queries = [len(x.test_pairs) for x in arc_task_set]

    from collections import Counter

    print("Train:")
    print("Number of tasks:", len(arc_task_set))
    print("Number of demonstrations per task:", Counter(number_examples))
    print("Number of tests per task:", Counter(number_queries))


if __name__ == '__main__':

    print("\nTrain")
    describe(train_set)

    print("\nEval")
    describe(eval_set)
