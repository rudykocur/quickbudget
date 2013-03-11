import os

from sqlalchemy import Column, Integer, Unicode, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship

from quickbudget.db import Base as DeclarativeBase

class RecipeImage(DeclarativeBase):
    __tablename__ = 'recipe_image'

    #id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Unicode, primary_key=True)
    recipeId = Column(Integer, ForeignKey('recipe.id'), nullable=True)

    contentPath = Column(Unicode)
    crc = Column(Unicode)
    md5 = Column(Unicode)
    #created = Column(DateTime)

    recipe = relationship("Recipe")

    def __init__(self, uid, contentPath):
        self.uid = uid
        self.contentPath = contentPath

class Recipe(DeclarativeBase):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True, autoincrement=True)

    total = Column(Numeric(18,2), nullable=False)
    date = Column(DateTime, nullable=True)
    vendor = Column(Unicode, nullable=True)

    expenseCategoryId = Column(Integer, ForeignKey('expense_category.id'), nullable=True)

    image = relationship("RecipeImage")
    parts = relationship("RecipePart")
    expenseCategory = relationship("ExpenseCategory")

class RecipePart(DeclarativeBase):
    __tablename__ = 'recipe_part'

    id = Column(Integer, primary_key=True, autoincrement=True)

    partTotal = Column(Numeric(18,2))

    recipeId = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    expenseCategoryId = Column(Integer, ForeignKey('expense_category.id'), nullable=True)

    recipe = relationship("Recipe")
    expenseCategory = relationship("ExpenseCategory")

class ExpenseCategory(DeclarativeBase):
    __tablename__ = 'expense_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode)

