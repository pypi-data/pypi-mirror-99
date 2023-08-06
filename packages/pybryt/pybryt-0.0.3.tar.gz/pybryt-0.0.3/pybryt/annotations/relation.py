"""Relational annotations for asserting conditions on other annotations"""

__all__ = [
    "RelationalAnnotation", "BeforeAnnotation", "AndAnnotation", "OrAnnotation", "XorAnnotation", 
    "NotAnnotation"
]

from abc import abstractmethod
from typing import Any, List, Tuple

from .annotation import Annotation, AnnotationResult


class RelationalAnnotation(Annotation):
    """
    Abstract base class for annotations that assert some kind of condition (temporal or boolean)
    on one or more other annotations.

    All relational annotations should inherit from this class, which defines a constructor that
    takes in a list of annotations and any necessary keyword arguments and populates the fields 
    needed for tracking child annotations.

    Args:
        *annotations (:py:class:`Annotation<pybryt.Annotation>`): the child annotations being 
            operated on
        **kwargs: additional keyword arguments passed to the 
            :py:class:`Annotation<pybryt.Annotation>` constructor
    """

    _annotations: List['Annotation']
    """the child annotations that this annotation operates on"""

    def __init__(self, *annotations, **kwargs):
        self._annotations = annotations
        for ann in self._annotations:
            if not isinstance(ann, Annotation):
                raise ValueError("One of the arguments is not an annotation")

        super().__init__(**kwargs)

    @property
    def children(self):
        """
        ``list[Annotation]``: the child annotations that this annotation operates on
        """
        return self._annotations

    @abstractmethod
    def check(self, observed_values: List[Tuple[Any, int]]) -> "AnnotationResult":
        ...


class BeforeAnnotation(RelationalAnnotation):
    """
    Annotation for asserting that one annotation occurs before another.

    When being :py:meth:`check<pybryt.BeforeAnnotation.check>` is called, ensures that all child 
    annotations are satisfied and then checks that for the :math:`i^\\text{th}` annotation the
    :math:`(i+1)^\\text{th}` annotation has a timestamp greater than or equal to its own. 
    Annotations must be passed to the constructor in the order in which they are expected to appear.

    Args:
        *annotations (:py:class:`Annotation<pybryt.Annotation>`): the child annotations being 
            operated on
        **kwargs: additional keyword arguments passed to the 
            :py:class:`Annotation<pybryt.Annotation>` constructor
    """

    def check(self, observed_values: List[Tuple[Any, int]]) -> "AnnotationResult":
        """
        Checks that all child annotations are satisfied by the values in ``observed_values`` and
        that the timestamps of the satisfying values occur in non-decreasing order.

        Args:
            observed_values (``list[tuple[object, int]]``): a list of tuples of values observed
                during execution and the timestamps of those values
        
        Returns:
            :py:class:`AnnotationResult`: the results of this annotation based on 
            ``observed_values``
        """
        results = []
        for ann in self._annotations:
            results.append(ann.check(observed_values))

        if all(res.satisfied for res in results):
            before = []
            for i in range(len(self._annotations) - 1):
                before.append(results[i].satisfied_at < results[i + 1].satisfied_at)
            
            return AnnotationResult(all(before), self, children = results)
        
        else:
            return AnnotationResult(False, self, children = results)


class AndAnnotation(RelationalAnnotation):
    """
    Annotation for asserting that a series of annotations are **all** satisfied.

    Args:
        *annotations (:py:class:`Annotation<pybryt.Annotation>`): the child annotations being 
            operated on
        **kwargs: additional keyword arguments passed to the 
            :py:class:`Annotation<pybryt.Annotation>` constructor
    """

    def check(self, observed_values: List[Tuple[Any, int]]) -> "AnnotationResult":
        """
        Checks that all child annotations are satisfied by the values in ``observed_values``.

        Args:
            observed_values (``list[tuple[object, int]]``): a list of tuples of values observed
                during execution and the timestamps of those values
        
        Returns:
            :py:class:`AnnotationResult`: the results of this annotation based on 
            ``observed_values``
        """
        results = []
        for ann in self._annotations:
            results.append(ann.check(observed_values))

        return AnnotationResult(all(res.satisfied for res in results), self, children = results)


class OrAnnotation(RelationalAnnotation):
    """
    Annotation for asserting that, of a series of annotations, **any** are satisfied.

    Args:
        *annotations (:py:class:`Annotation<pybryt.Annotation>`): the child annotations being 
            operated on
        **kwargs: additional keyword arguments passed to the 
            :py:class:`Annotation<pybryt.Annotation>` constructor
    """

    def check(self, observed_values: List[Tuple[Any, int]]) -> "AnnotationResult":
        """
        Checks that any of the child annotations are satisfied by the values in ``observed_values``.

        Args:
            observed_values (``list[tuple[object, int]]``): a list of tuples of values observed
                during execution and the timestamps of those values
        
        Returns:
            :py:class:`AnnotationResult`: the results of this annotation based on 
            ``observed_values``
        """
        results = []
        for ann in self._annotations:
            results.append(ann.check(observed_values))

        return AnnotationResult(any(res.satisfied for res in results), self, children = results)


class XorAnnotation(RelationalAnnotation):
    """
    Annotation for asserting that, of two annotations, one is satisfied and the other is not.

    Args:
        *annotations (:py:class:`Annotation<pybryt.Annotation>`): the child annotations being 
            operated on
        **kwargs: additional keyword arguments passed to the 
            :py:class:`Annotation<pybryt.Annotation>` constructor
    """

    def __init__(self, *annotations):
        super().__init__(*annotations)
        assert len(self._annotations) == 2, "Cannot use xor with more than two annotations"

    def check(self, observed_values: List[Tuple[Any, int]]) -> "AnnotationResult":
        """
        Checks that one child annotation is satisfied and one is not by the values in 
        ``observed_values``.

        Args:
            observed_values (``list[tuple[object, int]]``): a list of tuples of values observed
                during execution and the timestamps of those values
        
        Returns:
            :py:class:`AnnotationResult`: the results of this annotation based on 
            ``observed_values``
        """
        results = []
        for ann in self._annotations:
            results.append(ann.check(observed_values))

        sats = [res.satisfied for res in results]
        return AnnotationResult(sats[0] ^ sats[1], self, children = results)


class NotAnnotation(RelationalAnnotation):
    """
    Annotation for asserting that a single annotation should **not** be satisfied.

    Args:
        *annotations (:py:class:`Annotation<pybryt.Annotation>`): the child annotation being 
            operated on
        **kwargs: additional keyword arguments passed to the 
            :py:class:`Annotation<pybryt.Annotation>` constructor
    """

    def check(self, observed_values: List[Tuple[Any, int]]) -> "AnnotationResult":
        """
        Checks that the child annotation is not satisfied by the values in ``observed_values``.

        Args:
            observed_values (``list[tuple[object, int]]``): a list of tuples of values observed
                during execution and the timestamps of those values
        
        Returns:
            :py:class:`AnnotationResult`: the results of this annotation based on 
            ``observed_values``
        """
        results = []
        for ann in self._annotations:
            results.append(ann.check(observed_values))

        return AnnotationResult(all(not res.satisfied for res in results), self, children = results)
