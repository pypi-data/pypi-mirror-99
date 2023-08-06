from __future__ import annotations

from typing import Optional

from loguru import logger
from pandas import DataFrame, concat
from snapflow.core.data_block import DataBlock
from snapflow.core.snap import Input, Output, Snap
from snapflow.core.sql.sql_snap import Sql, SqlSnap
from snapflow.core.streams import Stream
from snapflow.core.typing.inference import conform_dataframe_to_schema
from snapflow.storage.db.utils import get_tmp_sqlite_db_url
from snapflow.testing.utils import (
    DataInput,
    produce_snap_output_for_static_input,
    str_as_dataframe,
)
from snapflow.utils.pandas import assert_dataframes_are_almost_equal
from snapflow.utils.typing import T


# @snap(module="core")
# @input("input", schema="T")
# @input("previous", schema="T", recursive_from_self=True)
@Snap(module="core", display_name="Accumulate DataFrames")
def dataframe_accumulator(
    input: Stream[T],
    this: Optional[DataBlock[T]] = None,
) -> DataFrame[T]:
    # TODO: make this return a dataframe iterator right?
    accumulated_dfs = [block.as_dataframe() for block in input]
    if this is not None:
        accumulated_dfs = [this.as_dataframe()] + accumulated_dfs
    return concat(accumulated_dfs)


# TODO: this is no-op if "this" is empty... is there a way to shortcut?
# TODO: does the bound stream thing even work?? Do we have a test somewhere?
# TODO: what if we have mixed schemas? need explicit columns
@Input("previous", schema="T", from_self=True)
@Input("new", schema="T", stream=True)
@Output(schema="T")
@SqlSnap(module="core", autodetect_inputs=False, display_name="Accumulate Tables")
def sql_accumulator():
    sql = """
    {% if input_objects.previous.bound_block %}
    select * from {{ inputs.previous }}
    union all
    {% endif %}
    {% for block in input_objects.new.bound_stream %}
    select
    * from {{ block.as_table_stmt() }}
    {% if not loop.last %}
    union all
    {% endif %}
    {% endfor %}
    """
    return sql


def test_accumulator():
    from snapflow.modules import core

    input_data_1 = """
        k1,k2,f1,f2,f3,f4
        1,2,abc,1.1,1,
        1,2,def,1.1,{"1":2},2012-01-01
        1,3,abc,1.1,2,2012-01-01
        1,4,,,"[1,2,3]",2012-01-01
        2,2,1.0,2.1,"[1,2,3]",2012-01-01
    """
    expected_1 = """
        k1,k2,f1,f2,f3,f4
        1,2,abc,1.1,1,
        1,2,def,1.1,{"1":2},2012-01-01
        1,3,abc,1.1,2,2012-01-01
        1,4,,,"[1,2,3]",2012-01-01
        2,2,1.0,2.1,"[1,2,3]",2012-01-01
    """
    input_data_2 = """
        k1,k2,f1,f2,f3,f4
        1,2,abc,1.1,1,
        1,2,def,1.1,{"1":2},2012-01-01
        1,3,abc,1.1,2,2012-01-01
        1,4,,,"[1,2,3]",2012-01-01
        2,2,1.0,2.1,"[1,2,3]",2012-01-01
        1,7,g,0,
    """
    expected_2 = """
        k1,k2,f1,f2,f3,f4
        1,2,abc,1.1,1,
        1,2,def,1.1,{"1":2},2012-01-01
        1,3,abc,1.1,2,2012-01-01
        1,4,,,"[1,2,3]",2012-01-01
        2,2,1.0,2.1,"[1,2,3]",2012-01-01
        1,7,g,0,
    """
    s = get_tmp_sqlite_db_url()
    for input_data, expected in [
        (input_data_1, expected_1),
        (input_data_2, expected_2),
    ]:
        for p in [sql_accumulator, dataframe_accumulator]:
            data_input = DataInput(input_data, schema="CoreTestSchema", module=core)
            with produce_snap_output_for_static_input(
                p, input=data_input, target_storage=s
            ) as db:
                assert db is not None
                expected_df = DataInput(
                    expected, schema="CoreTestSchema", module=core
                ).as_dataframe(db.manager.ctx.env, db.manager.sess)
                logger.debug("TEST df conversion 2")
                df = db.as_dataframe()
                assert_dataframes_are_almost_equal(
                    df, expected_df, schema=core.schemas.CoreTestSchema
                )

    # TODO: how to test `this`?
    # test_recursive_input=dict(
    #     input="""
    #         schema: CoreTestSchema
    #         k1,k2,f1,f2,f3
    #         1,2,abc,1.1,1
    #         1,2,def,1.1,{"1":2}
    #         1,3,abc,1.1,2
    #         1,4,,,"[1,2,3]"
    #         2,2,1.0,2.1,"[1,2,3]"
    #     """,
    #     this="""
    #         schema: CoreTestSchema
    #         k1,k2,f1,f2,f3
    #         1,5,abc,1.1,
    #         1,6,abc,1.1,2
    #     """,
    #     output="""
    #         schema: CoreTestSchema
    #         k1,k2,f1,f2,f3
    #         1,2,def,1.1,{"1":2}
    #         1,3,abc,1.1,2
    #         1,4,,,"[1,2,3]"
    #         2,2,1.0,2.1,"[1,2,3]"
    #         1,5,abc,1.1,
    #         1,6,abc,1.1,2
    #     """,
    #
    # ),
