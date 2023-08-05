import unittest
import pytest
from bson import ObjectId
from random import randint

from mongodantic.models import MongoModel, Query
from mongodantic.types import ObjectIdStr, ObjectId
from mongodantic import init_db_connection_params
from mongodantic.aggregation import Lookup, Sum, Max, Min, Avg, Count
from mongodantic.exceptions import ValidationError

product_types = {1: 'phone', 2: 'book', 3: 'food'}


class TestAggregation(unittest.TestCase):
    def setUp(self):
        init_db_connection_params("mongodb://127.0.0.1:27017", "test")

        class Product(MongoModel):
            title: str
            cost: float
            quantity: int
            product_type: str
            config: dict

        class ProductImage(MongoModel):
            url: str
            product_id: ObjectIdStr

        Product.querybuilder.drop_collection(force=True)
        ProductImage.querybuilder.drop_collection(force=True)

        self.Product = Product
        self.ProductImage = ProductImage

    def test_aggregation_math_operation(self):
        data = [
            self.Product(
                title=str(i),
                cost=float(i),
                quantity=i,
                product_type=product_types[randint(1, 3)],
                config={'type_id': i},
            )
            for i in range(1, 5)
        ]
        self.Product.querybuilder.insert_many(data)
        max_ = self.Product.querybuilder.aggregate(aggregation=Max('cost'))
        assert max_ == {'cost__max': 4}

        min_ = self.Product.querybuilder.aggregate(aggregation=Min('cost'))
        assert min_ == {'cost__min': 1}

        sum_ = self.Product.querybuilder.aggregate(aggregation=Sum('cost'))
        assert sum_ == {'cost__sum': 10}

        avg_ = self.Product.querybuilder.aggregate(aggregation=Avg('cost'))
        assert avg_ == {'cost__avg': 2.5}

        simple_avg = self.Product.querybuilder.aggregate_sum('cost')
        assert simple_avg == 10.0

        simple_max = self.Product.querybuilder.aggregate_max('cost')
        assert simple_max == 4

        simple_min = self.Product.querybuilder.aggregate_min('cost')
        assert simple_min == 1

        simple_avg = self.Product.querybuilder.aggregate_avg('cost')
        assert simple_avg == 2.5

    def test_aggregation_multiply(self):
        data = [
            self.Product(
                title=str(i),
                cost=float(i),
                quantity=i - 1,
                product_type=product_types[2] if i != 4 else product_types[1],
                config={'type_id': 2},
            )
            for i in range(1, 5)
        ]
        self.Product.querybuilder.insert_many(data)
        result_sum = self.Product.querybuilder.aggregate(
            aggregation=[Sum('cost'), Sum('quantity')]
        )
        assert result_sum == {'cost__sum': 10.0, 'quantity__sum': 6}

        result_max = self.Product.querybuilder.aggregate(
            aggregation=[Max('cost'), Max('quantity')]
        )
        assert result_max == {'cost__max': 4.0, 'quantity__max': 3}

        result_min = self.Product.querybuilder.aggregate(
            aggregation=[Min('cost'), Min('quantity')]
        )
        assert result_min == {'cost__min': 1.0, 'quantity__min': 0}

        result_avg = self.Product.querybuilder.aggregate(
            aggregation=(Avg('cost'), Avg('quantity'))
        )
        assert result_avg == {'cost__avg': 2.5, 'quantity__avg': 1.5}

        result_multiply = self.Product.querybuilder.aggregate(
            aggregation=(Avg('cost'), Max('quantity'))
        )
        assert result_multiply == {'cost__avg': 2.5, 'quantity__max': 3}

        result_count = self.Product.querybuilder.aggregate(
            aggregation=Count('product_type')
        )
        assert result_count == {'book': {'count': 3}, 'phone': {'count': 1}}

        result_count_agg = self.Product.querybuilder.aggregate(
            aggregation=[Count('product_type'), Sum('cost')]
        )
        assert result_count_agg == {
            'book': {'cost__sum': 6.0, 'count': 3},
            'phone': {'cost__sum': 4.0, 'count': 1},
        }

        result_sum_and_avg_agg_with_group = self.Product.querybuilder.aggregate(
            aggregation=[Avg('cost'), Sum('cost')], group_by=['product_type'],
        )
        assert result_sum_and_avg_agg_with_group == {
            'phone': {'cost__avg': 4.0, 'cost__sum': 4.0},
            'book': {'cost__avg': 2.0, 'cost__sum': 6.0},
        }

        result_raw_group_by_by_inners = self.Product.querybuilder.raw_aggregate(
            data=[
                {
                    "$group": {
                        "_id": {'type_id': "$config.type_id"},
                        'count': {f'$sum': 1},
                        'names': {'$push': '$title'},
                    }
                },
            ],
        )
        assert result_raw_group_by_by_inners == [
            {'_id': {'type_id': 2}, 'count': 4, 'names': ['1', '2', '3', '4']}
        ]

        result_group_by_by_inners = self.Product.querybuilder.aggregate(
            group_by=['config.type_id'], aggregation=Count('_id')
        )
        assert result_group_by_by_inners == {'2': {'count': 4}}

        result_sum_and_avg_agg_with_group_many = self.Product.querybuilder.aggregate(
            aggregation=[Avg('cost'), Sum('cost')],
            group_by=['product_type', 'quantity'],
        )
        assert result_sum_and_avg_agg_with_group_many == {
            'book|0': {'cost__avg': 1.0, 'cost__sum': 1.0},
            'book|1': {'cost__avg': 2.0, 'cost__sum': 2.0},
            'book|2': {'cost__avg': 3.0, 'cost__sum': 3.0},
            'phone|3': {'cost__avg': 4.0, 'cost__sum': 4.0},
        }

        result_agg = self.Product.querybuilder.aggregate(
            aggregation=[Avg('cost'), Max('quantity')]
        )
        assert result_agg == {'cost__avg': 2.5, 'quantity__max': 3}

        result_not_match_agg = self.Product.querybuilder.aggregate(
            Query(title__ne='not_match') & Query(title__startswith='not'),
            aggregation=[Avg('cost'), Max('quantity')],
        )
        assert result_not_match_agg == {}

    def test_raises_invalid_field(self):
        with pytest.raises(ValidationError):
            self.Product.querybuilder.aggregate(
                title='not_match', aggregation=[Avg('cost123'), Max('quantityzzzz')]
            )

    def test_aggregate_lookup(self):
        product_inserted_id = self.Product.querybuilder.insert_one(
            title='product1',
            cost=23.00,
            quantity=23,
            product_type=product_types[randint(1, 3)],
            config={'type_id': 1},
        )
        image_inserted_id = self.ProductImage.querybuilder.insert_one(
            url='http://localhost:8000/image.png',
            product_id=ObjectId(product_inserted_id),
        )
        product = self.Product.querybuilder.aggregate_lookup(
            lookup=Lookup(
                self.ProductImage, local_field='_id', foreign_field='product_id',
            ),
            title='product1',
        ).first()

        assert str(product.productimage[0].product_id) == str(product_inserted_id)

        image = self.ProductImage.querybuilder.aggregate_lookup(
            lookup=Lookup(
                local_field='product_id',
                from_collection=self.Product,
                foreign_field='_id',
                with_unwind=True,
            )
        ).first()
        assert str(image.product._id) == str(product_inserted_id)

        product = self.Product.querybuilder.aggregate_lookup(
            lookup=Lookup(
                self.ProductImage,
                local_field='_id',
                foreign_field='product_id',
                as_='image',
                with_unwind=True,
            ),
            title='product1',
            project={'_id': 1, 'title': 1, 'cost': 1, 'image_id': '$image._id'},
        )[0]
        assert str(product['image_id']) == str(image_inserted_id)
