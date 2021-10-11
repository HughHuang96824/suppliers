'''
This file defines the model for Supplier
'''

import json
from typing import Dict, List, Set, Union
from Models.product import Product
import Exception.supplier_exception as se


class Supplier:
    '''
    Supplier model that encapsulates
    necessary info about a supplier
    '''

    def __init__(self, name: str, id: int = None,
                 email: str = "", address: str = "",
                 products: Union[List[Product], Set[Product]] = []) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the supplier
        id : int (0, 1e10), optional
            The id of the supplier (default is None).
            Its value is obtained from the DB and needs to be set eventually
        email: str, optional
            The email of the supplier (default is None)
        address: str, optional
            The address of the supplier (default is None)
        products: Union[List[Product], Set[Product]], optional
            The products of the supplier (default is [])
        """
        if id is not None:
            self._check_id(id)
        self._check_name(name)
        self._check_email(email)
        self._check_address(address)
        self._check_products(products)
        if (email == "" and address == ""):
            raise se.MissingContactInfo("At least one contact method "
                                        "(email or address) is required")

        self._id = None  # DB provides ID
        self._name = name
        self._email = email
        self._address = address
        self._products = {}
        for p in products:
            self.add_product(p)

    @property
    def id(self) -> str:
        '''id of the supplier'''
        return self._id

    @property
    def name(self) -> str:
        '''name of the supplier'''
        return self._name

    @property
    def email(self) -> int:
        '''email of the supplier'''
        return self._email

    @property
    def address(self) -> str:
        '''address of the supplier'''
        return self._address

    @property
    def products(self) -> Dict[str, Product]:
        '''products of the supplier'''
        return self._products

    @id.setter
    def id(self, id: int) -> None:
        self._check_id(id)
        self._id = str(id).zfill(10)

    @name.setter
    def name(self, name: str) -> None:
        self._check_name(name)
        self._name = name

    @email.setter
    def email(self, email: str) -> None:
        self._check_email(email)
        self._email = email

    @address.setter
    def address(self, address: str) -> None:
        self._check_address(address)
        self._address = address

    @products.setter
    def products(self, products: Union[List[Product], Set[Product]]) -> None:
        self._check_products(products)
        for p in products:
            self.add_product(p)

    def add_product(self, product: Product) -> None:
        '''add a product to the supplier'''
        self._check_product(product)
        if product.id is None:
            raise se.MissingProductId("Product %s has no id" % product.name)
        self._products[product.id] = product

    def to_json(self) -> str:
        '''convert the supplier to JSON formatted string'''
        def formatter(supplier: Supplier):
            return {k.lstrip('_'): v for k, v in vars(supplier).items()}
        return json.dumps(self, default=formatter, indent=4)

    def _check_id(self, id: int) -> None:
        '''check the type and the range of id'''
        if not isinstance(id, int):
            raise se.WrongArgType("<class 'int'> expected for id, "
                                  "got %s" % type(id))
        elif (id >= 1e10 or id <= 0):
            raise se.OutOfRange("id is not within range (0, 1e10), "
                                "got %s" % id)

    def _check_name(self, name: str) -> None:
        '''check the type of name'''
        if not isinstance(name, str):
            raise se.WrongArgType("<class 'str'> expected for name, "
                                  "got %s" % type(name))

    def _check_email(self, email: str) -> None:
        '''check the type of email'''
        # email format parser may needed
        if not isinstance(email, str):
            raise se.WrongArgType("<class 'str'> expected for email, "
                                  "got %s" % type(email))

    def _check_address(self, address: str) -> None:
        '''check the type of address'''
        if not isinstance(address, str):
            raise se.WrongArgType("<class 'str'> expected for address, "
                                  "got %s" % type(address))

    def _check_product(self, product: Product) -> None:
        '''check the type of product'''
        if not isinstance(product, Product):
            raise se.WrongArgType("class<'Product'> expected for product, "
                                  "got %s" % type(product))

    def _check_products(self, products:
                        Union[List[Product], Set[Product]]) -> None:
        '''check the type of products'''
        if not isinstance(products, (List, Set)):
            raise se.WrongArgType("class<'List'> or class<'Set'> expected "
                                  "for products, got %s" % type(products))
