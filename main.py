from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import user, product, cart 
from routers import product as product_router
from auth.routes import router as auth_router
from routers.order import router as order_router
from routers import cart
from routers import wishlist
from routers import admin as admin_router  
from routers import admin_product
from routers import admin_order
from routers import order
from routers import review 
from routers import admin_review
from routers import qna
from routers import admin_qna
from dotenv import load_dotenv
load_dotenv()


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001","http://139.59.63.32:3000", "http://primetask.duckdns.org"], 
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
app.include_router(cart.router)
app.include_router(wishlist.router, prefix="/api", tags=["Wishlist"])
app.include_router(admin_router.router, prefix="/api", tags=["Admin"]) 
app.include_router(admin_product.router, tags=["Admin Products"])
app.include_router(admin_order.router)
app.include_router(order.router)
app.include_router(review.router, prefix="/api", tags=["Reviews"])
app.include_router(admin_review.router, prefix="/api", tags=["Admin Reviews"])
app.include_router(qna.router, prefix="/api", tags=["Q&A"])
app.include_router(admin_qna.router,  tags=["Admin QnA"])
