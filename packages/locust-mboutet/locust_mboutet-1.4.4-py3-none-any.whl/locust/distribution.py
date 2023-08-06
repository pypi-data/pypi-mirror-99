import math
from itertools import combinations_with_replacement
from operator import attrgetter
from typing import (
    Dict,
    List,
    Type,
)

from locust import User


def weight_users(
    user_classes: List[Type[User]],
    number_of_users: int,
) -> Dict[str, int]:
    """
    Compute the desired state of users using the weight of each user class.

    If `number_of_users` is less than `len(user_classes)`, at most one user of each user class
    is chosen. User classes with higher weight are chosen first.

    If `number_of_users` is greater than or equal to `len(user_classes)`, at least one user of each
    user class will be chosen. The greater `number_of_users` is, the better the actual distribution
    of users will match the desired one (as dictated by the weight attributes).

    :param user_classes: the list of user class
    :param number_of_users: total number of users
    :return: the set of users to run
    """
    assert number_of_users >= 0

    if len(user_classes) == 0:
        return {}

    user_classes = sorted(user_classes, key=lambda u: u.__name__)

    user_class_occurrences = {user_class.__name__: 0 for user_class in user_classes}

    if number_of_users <= len(user_classes):
        user_class_occurrences.update(
            {
                user_class.__name__: 1
                for user_class in sorted(
                    user_classes,
                    key=lambda user_class: user_class.weight,
                    reverse=True,
                )[:number_of_users]
            }
        )
        return user_class_occurrences

    weights = list(map(attrgetter("weight"), user_classes))
    user_class_occurrences = {
        user_class.__name__: round(relative_weight * number_of_users) or 1
        for user_class, relative_weight in zip(user_classes, (weight / sum(weights) for weight in weights))
    }

    if sum(user_class_occurrences.values()) == number_of_users:
        return user_class_occurrences

    else:
        return _find_ideal_users_to_add_or_remove(
            user_classes,
            number_of_users - sum(user_class_occurrences.values()),
            user_class_occurrences.copy(),
        )


def _find_ideal_users_to_add_or_remove(
    user_classes: List[Type[User]],
    number_of_users_to_add_or_remove: int,
    user_class_occurrences: Dict[str, int],
) -> Dict[str, int]:
    sign = -1 if number_of_users_to_add_or_remove < 0 else 1

    number_of_users_to_add_or_remove = abs(number_of_users_to_add_or_remove)

    user_class_occurrences_candidates: Dict[float, Dict[str, int]] = {}

    for user_classes_combination in combinations_with_replacement(user_classes, number_of_users_to_add_or_remove):
        user_class_occurrences_candidate = {
            user_class.__name__: user_class_occurrences[user_class.__name__]
            + sign * sum(1 for user_class_ in user_classes_combination if user_class_.__name__ == user_class.__name__)
            for user_class in user_classes
        }
        distance = distance_from_desired_distribution(
            user_classes,
            user_class_occurrences_candidate,
        )
        if distance not in user_class_occurrences_candidates:
            user_class_occurrences_candidates[distance] = user_class_occurrences_candidate.copy()

    return user_class_occurrences_candidates[min(user_class_occurrences_candidates.keys())]


def distance_from_desired_distribution(
    user_classes: List[Type[User]],
    user_class_occurrences: Dict[str, int],
) -> float:
    user_class_2_actual_percentage = {
        user_class: 100 * occurrences / sum(user_class_occurrences.values())
        for user_class, occurrences in user_class_occurrences.items()
    }

    user_class_2_expected_percentage = {
        user_class.__name__: 100 * user_class.weight / sum(map(attrgetter("weight"), user_classes))
        for user_class in user_classes
    }

    differences = [
        user_class_2_actual_percentage[user_class] - expected_percentage
        for user_class, expected_percentage in user_class_2_expected_percentage.items()
    ]

    return math.sqrt(math.fsum(map(lambda x: x ** 2, differences)))
