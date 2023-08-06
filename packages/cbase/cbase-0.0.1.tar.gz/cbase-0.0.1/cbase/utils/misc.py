def gen_uid():
    """
    Generate UID
    """

    import uuid

    return {'return':0,
            'uid':uuid.uuid4().hex[:16]}
