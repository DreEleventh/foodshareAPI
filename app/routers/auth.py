from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..databaseConn import get_db
from .. import models, schemas, utills, oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/donor_login", response_model=schemas.Token)
def donor_login(donor_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Handle donor login and token generation.

    Args:
        donor_credentials (schemas.DonorLogin): The donor's login credentials.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token and its type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    donor = db.query(models.DonorCredentials).filter(models.DonorCredentials.username
                                                     == donor_credentials.username).first()

    if not donor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if not utills.verify_passcode(donor_credentials.password, donor.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(payload={"donor_id": donor.donor_id})
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/donor_logout", status_code=status.HTTP_200_OK)
# def donor_logout(current_donor: models.DonorCredentials = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
#     token = request.headers.get("Authorization").split(" ")[1]
#
#     # Decode the token to get the "jti" (JWT ID) claim
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     jti = payload.get("jti")
#
#     # Store the revoked "jti" in the DonorCredentials model
#     current_donor.revoked_tokens.append(jti)
#     db.commit()
#
#     return {"message": "Logout successful"}
#
#
# @router.post("/logout")
# async def logout(current_user: schemas.User = Depends(oauth2.get_current_user),
#                   blacklist_service: BlacklistService = Depends()):
#     """
#     Handle user logout and invalidate the current token.
#
#     Args:
#         current_user (schemas.User): The currently logged-in user information (obtained from the dependency).
#         blacklist_service (BlacklistService): Dependency providing blacklist functionality.
#
#     Raises:
#         HTTPException: If there's an issue with logout logic.
#     """
#
#     if not current_user:
#         return {"message": "User already logged out"}  # Informative message
#
#     try:
#         # Add the current user's token to the blacklist
#         await blacklist_service.add_to_blacklist(current_user.access_token)
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Logout failed: {str(e)}")
#
#     return {"message": "Successfully logged out"}

