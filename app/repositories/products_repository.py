from sqlalchemy.orm import Session

from app.models import Product


def find_by_barcode(db: Session, barcode: str) -> Product | None:
    return db.query(Product).filter(Product.barcode == barcode).first()


def find_by_name(db: Session, name: str) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.name.ilike(f"%{name}%"))
        .order_by(Product.verified.desc(), Product.confidence.desc())
        .first()
    )


def create_product(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product