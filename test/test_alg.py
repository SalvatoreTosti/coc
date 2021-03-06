import os, datetime, pytest, sys

sys.path.insert(0, "../")
from backend.core.alg import *
from hypothesis import given
import hypothesis.strategies as st


@given(shares=st.integers(), price=st.integers())
def test_market_cap(shares, price):
    assert mkt_cap(shares, price) == shares * price


@given(
    eps=st.floats(min_value=-10000000, max_value=10000000),
    bvps=st.floats(min_value=-10000000, max_value=10000000),
)
def test_graham_number(eps, bvps):
    result = graham_num(eps, bvps)
    product = 22.5 * eps * bvps
    if product < 0:
        assert result < 0
        assert result == -1 * round(math.sqrt(abs(product)), 2)
    else:
        assert result >= 0
        assert result == round(math.sqrt(product), 2)


@given(sales=st.integers())
def test_good_sales(sales):
    result = good_sales(sales)
    if sales >= 700000000:
        assert result
    else:
        assert not result


@given(pe_ratio=st.floats())
def test_good_pe_ratio(pe_ratio):
    result = good_pe_ratio(pe_ratio)
    if pe_ratio < 15.0:
        assert result
    else:
        assert not result


@given(curr_ratio=st.floats())
def test_good_curr_ratio(curr_ratio):
    result = good_curr_ratio(curr_ratio)
    if curr_ratio >= 2.0:
        assert result
    else:
        assert not result


@given(eps_list=st.lists(st.floats()))
def test_good_eps(eps_list):
    if len(eps_list) < 5:
        expected = False
    else:
        expected = all(list(map(lambda x: x is not None and x >= 0, eps_list)))
    if len(eps_list) == 0:
        expected = False
    result = good_eps(eps_list)
    assert expected == result


@given(num=st.floats())
def test_abbreviate_num_floats(num):
    result = abbreviate_num(num)
    assert type(result) is str


@given(num=st.integers())
def test_abbreviate_num_ints(num):
    result = abbreviate_num(num)
    large_nums = {"T": trillion, "B": billion, "M": million}
    abbreviation = ""
    denominator = 1
    if num != None:
        for i in large_nums:
            if abs(num) >= large_nums[i]:
                denominator *= large_nums[i]
                abbreviation = i
                break
        expected = str(round((num / denominator), 2)) + abbreviation
    if abbreviation == "":
        expected = "None"
    assert type(result) is str
    assert expected == result
