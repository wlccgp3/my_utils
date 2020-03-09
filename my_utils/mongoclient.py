#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pymongo import MongoClient

__all__ = ['Mongo']

logger = logging.getLogger(__name__)


class Mongo(object):
    def __init__(self, uri, db_name, coll_name, connect=True, index=None, unique=False):
        self.uri = uri
        self.db_name = db_name
        self.coll_name = coll_name

        self.client = MongoClient(uri, connect=connect)
        self.db = self.client[self.db_name]
        self.coll = self.db[self.coll_name]
        if index:
            if unique:
                self.coll.create_index(index, unique=True, background=True)
            else:
                self.coll.create_index(index, unique=False, background=True)

    def find(self, *args, no_cursor_timeout=True, **kwargs):
        result = self.coll.find(*args, no_cursor_timeout=no_cursor_timeout, **kwargs)
        return result

    def find_one(self, filter=None, *args, **kwargs):
        result = self.coll.find_one(
            filter, *args, **kwargs
        )
        return result

    def insert_one(self, document, bypass_document_validation=False, session=None):
        try:
            result = self.coll.insert_one(
                document,
                bypass_document_validation=bypass_document_validation,
                session=session
            )
        except Exception as e:
            logger.warning(e)
        else:
            return result

    def insert_many(self, documents, ordered=True,
                    bypass_document_validation=False, session=None):
        try:
            result = self.coll.insert_many(
                documents, ordered=ordered,
                bypass_document_validation=bypass_document_validation,
                session=session
            )
        except Exception as e:
            logger.warning(e)
        else:
            return result

    def update_one(self, filter, update, upsert=False,
                   bypass_document_validation=False,
                   collation=None, array_filters=None,
                   session=None):
        try:
            result = self.coll.update_one(
                filter, update, upsert=upsert,
                bypass_document_validation=bypass_document_validation,
                collation=collation, array_filters=array_filters,
                session=session
            )
        except Exception as e:
            logger.warning(e)
        else:
            return result

    def update_many(self, filter, update, upsert=False, array_filters=None,
                    bypass_document_validation=False, collation=None,
                    session=None):
        try:
            result = self.coll.update_many(
                filter, update, upsert=upsert, array_filters=array_filters,
                bypass_document_validation=bypass_document_validation,
                collation=collation, session=session
            )
        except Exception as e:
            logger.warning(e)
        else:
            return result

    def replace_one(self, filter, replacement, upsert=False,
                    bypass_document_validation=False, collation=None,
                    session=None):
        try:
            result = self.coll.replace_one(
                filter, replacement, upsert=upsert,
                bypass_document_validation=bypass_document_validation,
                collation=collation, session=session
            )
        except Exception as e:
            logger.warning(e)
        else:
            return result
