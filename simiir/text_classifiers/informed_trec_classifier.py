__author__ = 'leif'

from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from simiir.text_classifiers.base_informed_trec_classifier import BaseInformedTrecTextClassifier

import logging

log = logging.getLogger('informed_trec_classifer.InformedTrecTextClassifier')


class InformedTrecTextClassifier(BaseInformedTrecTextClassifier):
    """
    A concrete implementation of BaseInformedTrecTextClassifier.

    No dice rolling here. What ever is in the judgement file is used.

    """
    def __init__(self, topic, qrel_file):
        """

        """
        super(InformedTrecTextClassifier, self).__init__(topic, qrel_file)

        log.debug("Classifier uses TREC qrels to make decision:")



    def is_relevant(self, document):
        """
        No dice rolling here. What ever is in the judgement file is used.
        """
        val = self._get_judgement(self._topic.id, document.doc_id)
        if val > 0:
            return True
        else:
            return False
