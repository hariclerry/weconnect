"""docstring for Business Controller"""
from flask import jsonify
from ..models import Business


class BusinessService(object):
    """docstring for Business Class"""
    def __init__(self, arg=0):
        self.arg = arg


    # paginante businesses
    @staticmethod
    def get_businesses(page, limit, search_string, location, category):
        """docstring for paginating through the business"""
        filters = {}
        # generate filters
        if location is not None:
            filters["location"] = location
        if category is not None:
            filters["category"] = category
        res = Business.get_businesses(page, limit, search_string, filters)
        if res["status"]:
            return jsonify(res), 200
        return jsonify(res), 404