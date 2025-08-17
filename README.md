## API Endpoints (Week 2)
- POST /register/ → Create new user
- POST /login/ → Obtain token
- POST /categories/ → Create category (auth required)
- GET /categories/ → List categories (auth required)
- PUT /categories/<id>/ → Update category (auth required, owner only)
- DELETE /categories/<id>/ → Delete category (auth required, owner only)
