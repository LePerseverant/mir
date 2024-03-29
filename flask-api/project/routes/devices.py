from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import or_, asc, desc
import json
from ..models.device import Device 
from ..utils.utils import get_pagination_urls
from ..db import db


bp = Blueprint("devices", __name__, url_prefix="/devices")


@jwt_required()
@bp.get("/")
def get_devices():
    limit = request.args.get("limit", default=3, type=int)
    offset = request.args.get("offset", default=0, type=int)
    filters = request.args.get("filters")
    global_filter = request.args.get("global_filter")
    sorting = request.args.get("sorting")

    try:
        query = Device.query

        if filters:
            filters = json.loads(filters)
            filter_conditions = []
            for filter_obj in filters:
                id = filter_obj.get("id")
                value = filter_obj.get("value")
                column = getattr(Device, id)
                filter_conditions.append(column.ilike(f"%{value}%"))
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


@jwt_required()
@bp.post("/")
def create_device():

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "missing device data."}), 400

    device_mac_address = data.json["device_mac_address"]
    device_ip_v4_address = data.json["device_ip_v4_address"]
    device_category = data.json["device_category"]
    device_status = data.json["device_status"]

    try:
        device = Device(device_mac_address=device_mac_address, device_ip_v4_address=device_ip_v4_address, device_category=device_category, device_status=device_status)
        db.session.add(device)
        db.session.commit()
        return jsonify({'message': 'Device added successfully', 'device_id': device.device_id}), 201

    except Exception as exception:

        return jsonify({ "error": str(exception) })
