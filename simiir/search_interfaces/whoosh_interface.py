import os
from whoosh.index import open_dir
from search_interfaces import Document
from ifind.search.engines.whooshtrec import Whooshtrec
from search_interfaces.base_interface import BaseSearchInterface
import logging

log = logging.getLogger('simuser.search_interfaces.whoosh_interface')


class WhooshSearchInterface(BaseSearchInterface):
    """
    A search interface making use of the Whoosh indexing library - and the ifind search components.

    Set model = 0 for TFIDIF
    Set model = 1 for BM25 (defaults to b=0.75), set pval to change b.
    Set model = 2 for PL2 (defaults to c=10.), set pval to change c.

    """
    def __init__(self, whoosh_index_dir, model=2, implicit_or=True, pval=None):
        super(WhooshSearchInterface, self).__init__()
        log.debug("Whoosh Index to open: {0}".format(whoosh_index_dir))
        self.__index = open_dir(whoosh_index_dir)
        self.__reader = self.__index.reader()


        self.__engine = Whooshtrec(whoosh_index_dir=whoosh_index_dir,model=model,implicit_or=implicit_or)

        if pval:
            self.__engine.set_model(model, pval)
    
    def issue_query(self, query, top=100):
        """
        Allows one to issue a query to the underlying search engine. Takes an ifind Query object.
        """
        query.top = top
        response = self.__engine.search(query)
        
        self._last_query = query
        self._last_response = response
        
        return response
    
    def get_document(self, document_id):
        """
        Retrieves a Document object for the given document specified by parameter document_id.
        """
        fields = self.__reader.stored_fields(int(document_id))
        
        title = fields['title']
        content = fields['content']
        document_num = fields['docid']
        document_date = fields['timedate']
        document_source = fields['source']
        
        document = Document(id=document_id, title=title, content=content)
        document.date = document_date
        document.doc_id = document_num
        document.source = document_source
        
        return document
        
