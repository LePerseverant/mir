from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_, asc, desc
import json
from project.models.device import Device
from ..models.customer import Customer
from ..utils.utils import get_pagination_urls
from ..db import db


bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.get("/")
@jwt_required()
def get_customers():
    limit = request.args.get("limit", default=3, type=int)
    offset = request.args.get("offset", default=0, type=int)
    filters = request.args.get("filters")
    global_filter = request.args.get("global_filter")
    sorting = request.args.get("sorting")

    try:
        query = Customer.query

        if filters:
            filters = json.loads(filters)
            filter_conditions = []
            for filter_obj in filters:
                id = filter_obj.get("id")
                value = filter_obj.get("value")
                column = getattr(Customer, id)
                filter_conditions.append(column.ilike(f"%{value}%"))
            query = query.filter(or_(*filter_conditions))

        if global_filter:
            global_filter_conditions = []
            for column in Customer.__table__.columns:
                global_filter_conditions.append(column.ilike(f"%{global_filter}%"))
            query = query.filter(or_(*global_filter_conditions))

        if sorting:
            sort_fields = json.loads(sorting)
            for sort_field in sort_fields:
                field = sort_field.get("id")
                order = sort_field.get("order")
                column = getattr(Customer, field)
                if order == "asc":
                    query = query.order_by(asc(column))
                elif order == "desc":
                    query = query.order_by(desc(column))

        results = query.limit(limit=limit).offset(offset=offset)
        total_count = query.count()
        previous_page, next_page = get_pagination_urls(limit, offset, total_count)
        customers = [customer.to_dict() for customer in results]

        return jsonify({ "data": { "count": total_count, "next": next_page, "previous": previous_page, "results": customers } })

    except Exception as exception:

        return jsonify({ "error": str(exception) })

# @jwt_required()
@bp.get("/customer/<int:customer_id>/devices")
def get_customer_devices(customer_id):
    limit = request.args.get("limit", default=3, type=int)
    offset = request.args.get("offset", default=0, type=int)
    filters = request.args.get("filters")
    global_filter = request.args.get("global_filter")
    sorting = request.args.get("sorting")

    try:
        query = Device.query.filter(Device.customer_id == customer_id)

        if filters:
            filters = json.loads(filters)
            filter_conditions = []
            for filter_obj in filters:
                id = filter_obj.get("id")
                value = filter_obj.get("value")
                column = getattr(Device, id)
                filter_conditions.append(column.ilike(f"%{value}%"))
                print("##########")
                print(filter_conditions)
                print("##########")
            query = query.filter(or_(*filter_conditions))

        if global_filter:
            global_filter_conditions = []
            for column in Device.__table__.columns:
                global_filter_conditions.append(column.ilike(f"%{global_filter}%"))
            query = query.filter(or_(*global_filter_conditions))

        if sorting:
            sort_fields = json.loads(sorting)
            for sort_field in sort_fields:
                field = sort_field.get("id")
                order = sort_field.get("order")
                column = getattr(Device, field)
                if order == "asc":
                    query = query.order_by(asc(column))
                elif order == "desc":
                    query = query.order_by(desc(column))

        results = query.limit(limit=limit).offset(offset=offset)
        total_count = query.count()
        previous_page, next_page = get_pagination_urls(limit, offset, total_count)
        devices = [device.to_dict() for device in results]

        return jsonify({ "data": { "count": total_count, "next": next_page, "previous": previous_page, "results": devices } })

    except Exception as exception:

        return jsonify({ "error": str(exception) })

@bp.get("/customer/<int:customer_id>")
def get_customer(customer_id: int):
    try:
        customer = Customer.query.get(customer_id)
        if customer is None:
            return jsonify({ "error": "customer not found."}), 404
        return jsonify({ "data": customer })
    except Exception as exception:
        return jsonify({ "error": str(exception) })


@bp.post("/customer/<int:customer_id>/devices")
def assign_device_to_customer(customer_id: int):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({ "error": "customer not found."}), 404
    data = request.get_json()
    if data is None:
        return jsonify({ "error": "missing device data."}), 400

    device_mac_address = data.get("device_mac_address")
    device_ip_v4_address = data.get("device_ip_v4_address", None)
    device_category = data.get("device_category")
    device_status = data.get("device_status")

    device = Device(
        device_mac_address=device_mac_address,
        device_ip_v4_address=device_ip_v4_address,
        device_category=device_category,
        device_status=device_status,
        customer=customer
    )

    try:
        db.session.add(device)
        db.session.commit()
    except Exception as exception:
            db.session.rollback()
            return jsonify({ "error": f"failed to add device: {str(exception)}" }), 500

    return jsonify({ "message": "device added successfully" }), 201


@bp.post("/")
def create_customer():

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "missing customer data."}), 400

    try:
        customer_name = data.get("customer_name")
        customer = Customer(customer_name=customer_name)
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'customer created.', "data": customer }), 201

    except Exception as exception:
        return jsonify({ "error": str(exception) })
