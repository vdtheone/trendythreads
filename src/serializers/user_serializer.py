from flask import jsonify


def user_serializer(user):
    return jsonify(
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile_no": user.mobile_no,
        }
    ).json
