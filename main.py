from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import user, product  # 👈 ensures tables are created
from routers import product as product_router  # 👈 new import
from auth.routes import router as auth_router
from routers import cart as cart_router
from routers import wishlist

# Create DB tables
Base.metadata.create_all(bind=engine)

# Init app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
def root():
    return {"message": "Backend running 🎉"}

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(product_router.router, prefix="/api", tags=["Products"])
app.include_router(cart_router.router, prefix="/api", tags=["Cart"]) 
app.include_router(wishlist.router, prefix="/api", tags=["Wishlist"])