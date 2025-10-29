from sqlalchemy.orm import Session
from sqlalchemy import exc
from . import models, schemas


def get_products(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Product).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        raise e


def get_product(db: Session, product_id: int):
    try:
        return db.query(models.Product).filter(models.Product.id == product_id).first()
    except exc.SQLAlchemyError as e:
        raise e


def create_product(db: Session, product: schemas.ProductCreate):
    try:
        db_product = models.Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise e


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            return None

        update_data = product.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)

        db.commit()
        db.refresh(db_product)
        return db_product
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise e


def delete_product(db: Session, product_id: int):
    try:
        db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not db_product:
            return False

        db.delete(db_product)
        db.commit()
        return True
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise e