"""docstring for Business Controller"""
from flask import jsonify
from .models import Business


class BusinessService(object):
    """docstring for Business Class"""
    def __init__(self, arg=0):
        self.arg = arg


    def register_business(self, user_id, business):
        """docstring for register business"""
        # fields = ["name", "category", "location"]
        # result = self.check_req_fields(business, fields)
        # if result["success"]:
        #     Business(user_id=user_id, name=business["name"], category=business["category"],
        #              location=business["location"]).register_business()
        #     return jsonify({"success":True, "message":"Business Created"}), 201
        # return jsonify(result), 422

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
        if res["success"]:
            return jsonify(res), 200
        return jsonify(res), 404