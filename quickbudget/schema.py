import datetime

from sqlalchemy import Column, Integer, Unicode, ForeignKey, Numeric, DateTime, Date, desc
from sqlalchemy.orm import relationship

from quickbudget.db import Base as DeclarativeBase


class ReceiptImage(DeclarativeBase):
    __tablename__ = 'recipe_image'

    #id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Unicode, primary_key=True)
    recipeId = Column(Integer, ForeignKey('recipe.id'), nullable=True)

    contentPath = Column(Unicode)
    crc = Column(Unicode)
    md5 = Column(Unicode)
    #created = Column(DateTime)

    receipt = relationship("Receipt")

    def __init__(self, uid, contentPath):
        self.uid = uid
        self.contentPath = contentPath

    @classmethod
    def get(cls, uid):
        """

        :param uid:
        :return: Loaded image
        :rtype: ReceiptImage
        """
        return cls.query.filter(cls.uid == uid).one()

    @classmethod
    def allWithoutReceipt(cls):
        return cls.query.filter(cls.receipt == None).all()


class Receipt(DeclarativeBase):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True, autoincrement=True)

    total = Column(Numeric(18, 2), nullable=False)
    date = Column(Date, nullable=True)
    note = Column(Unicode)

    expenseCategoryId = Column(Integer, ForeignKey('expense_category.id', name='expense_category'), nullable=True)

    recipeImportData = relationship("ReceiptImportData")
    image = relationship("ReceiptImage")
    #parts = relationship("RecipePart")
    expenseCategory = relationship("ExpenseCategory")

    @classmethod
    def allWithoutImage(cls):
        return cls.query.filter(cls.image == None).order_by(desc(cls.date)).all()


# class RecipePart(DeclarativeBase):
#     __tablename__ = 'recipe_part'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#
#     partTotal = Column(Numeric(18,2))
#
#     recipeId = Column(Integer, ForeignKey('recipe.id'), nullable=False)
#     expenseCategoryId = Column(Integer, ForeignKey('expense_category.id'), nullable=True)
#
#     recipe = relationship("Recipe")
#     expenseCategory = relationship("ExpenseCategory")


class ExpenseCategory(DeclarativeBase):
    __tablename__ = 'expense_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class ReceiptImportData(DeclarativeBase):
    __tablename__ = 'recipe_import_data'

    recipeId = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    bankImportId = Column(Integer, ForeignKey('bank_import_history.id'), primary_key=True)

    uid = Column(Unicode, unique=True)
    importLine = Column(Integer, nullable=False)

    receipt = relationship("Receipt")
    bankImport = relationship("BankImportHistory")

    def __init__(self, receipt, bankImport, uid, line):
        self.receipt = receipt
        self.bankImport = bankImport
        self.uid = uid
        self.importLine = line

    @classmethod
    def get(cls, uid):
        return cls.query.filter(cls.uid == uid).one()


class BankImportHistory(DeclarativeBase):
    __tablename__ = 'bank_import_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contentPath = Column(Unicode)

    type = Column(Unicode)
    status = Column(Unicode)
    date = Column(DateTime)

    crc = Column(Unicode)
    md5 = Column(Unicode)

    def __init__(self, type):
        #self.contentPath = path
        self.type = type
        self.date = datetime.datetime.now()

    @classmethod
    def findByHash(cls, md5, crc):
        return cls.query.filter(cls.crc == crc, cls.md5 == md5).one()


