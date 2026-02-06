from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.config import get_google_client_id, get_google_client_secret

router = APIRouter()

oauth = OAuth()

def register_oauth():
    oauth.register(
        name='google',
        client_id=get_google_client_id(),
        client_secret=get_google_client_secret(),
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        authorize_params=None,
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        client_kwargs={
            'scope': 'openid email profile',
            'timeout': 30.0
        }
    )

register_oauth()

@router.get("/auth/google")
async def login_google(request: Request):
    google = oauth.create_client('google')
    redirect_uri = request.url_for('auth_callback')
    return await google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        google = oauth.create_client('google')
        token = await google.authorize_access_token(request)
        user = token.get('userinfo')
        if not user:
            # Fallback if userinfo is not in token (depends on provider/scope)
            user = await google.userinfo(token=token)
            
        request.session['user'] = dict(user)
        return RedirectResponse(url='/')
    except Exception as e:
        print(f"OAuth Error details: {repr(e)}")
        # In production, handle errors more gracefully (log them, show error page)
        raise HTTPException(status_code=400, detail=f"OAuth failed: {repr(e)}")

@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/auth/google')
