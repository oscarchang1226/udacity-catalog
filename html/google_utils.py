from oauth2client import client, crypt


CLIENT_ID = "947254913299-se2f07fh8e54gvjvuvq7qt5ac0gkrits.apps.googleusercontent.com"  # NOQA
CLIENT_SECRET = "CU5BWeNxu_s6ljwPOF48dEEB"


def verify(form):
    """Verify Google authentication"""
    params = None
    try:
        if(form["token"] is None):
            raise crypt.AppIdentityError
        idinfo = client.verify_id_token(form["token"], CLIENT_ID)
        if(idinfo["iss"] not in [
            "accounts.google.com",
            "https://accounts.google.com"
        ]):
            raise crypt.AppIdentityError
        params = (True, dict(
            name=form["name"],
            img_url=form["img"],
            email="google+%s" % form["email"],
            sub=str(idinfo["sub"]),
            at_hash=str(idinfo["at_hash"])
        ))

    except crypt.AppIdentityError:
        return (False, None)
    return params
