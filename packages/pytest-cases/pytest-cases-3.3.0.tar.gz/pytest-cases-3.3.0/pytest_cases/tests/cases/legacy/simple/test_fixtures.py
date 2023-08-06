# Authors: Sylvain MARIE <sylvain.marie@se.com>
#          + All contributors to <https://github.com/smarie/python-pytest-cases>
#
# License: 3-clause BSD, <https://github.com/smarie/python-pytest-cases/blob/master/LICENSE>
from distutils.version import LooseVersion
import pytest
from ..simple import test_main_cases

from pytest_cases import unfold_expected_err, cases_fixture, cases_data, fixture
from pytest_cases.common_pytest_marks import PYTEST3_OR_GREATER

from ..example_code import super_function_i_want_to_test


@cases_fixture(module=test_main_cases)
def my_case_fixture_legacy(case_data, request):
    """Getting data will now be executed BEFORE the test (outside of the test duration)"""
    return case_data.get()


def test_with_cases_decorated_legacy(my_case_fixture_legacy):
    """ Example unit test that is automatically parametrized with @cases_data """

    # 1- Grab the test case data
    i, expected_o, expected_e = my_case_fixture_legacy

    # 2- Use it
    if expected_e is None:
        # **** Nominal test ****
        outs = super_function_i_want_to_test(**i)
        assert outs == expected_o

    else:
        # **** Error test ****
        # First see what we need to assert
        err_type, err_ptrn, err_inst, err_checker = unfold_expected_err(expected_e)

        # Run with exception capture and type check
        with pytest.raises(err_type) as err_info:
            super_function_i_want_to_test(**i)

        # Optional - Additional Exception instance check
        if err_inst is not None:
            assert err_info.value == err_inst

        # Optional - Additional exception instance check
        if err_checker is not None:
            err_checker(err_info.value)


if PYTEST3_OR_GREATER:
    @fixture
    @cases_data(module=test_main_cases)
    @pytest.mark.parametrize('a', [True])
    def my_case_fixture(case_data, a, request):
        """Getting data will now be executed BEFORE the test (outside of the test duration)"""
        return case_data.get()
else:
    # we cant double-parametrize with pytest 2.x: the ids get messed up
    @fixture
    @cases_data(module=test_main_cases)
    # @pytest.mark.parametrize('a', [True])
    def my_case_fixture(case_data, request):
        """Getting data will now be executed BEFORE the test (outside of the test duration)"""
        return case_data.get()


def test_with_cases_decorated(my_case_fixture):
    """ Example unit test that is automatically parametrized with @cases_data """

    # 1- Grab the test case data
    i, expected_o, expected_e = my_case_fixture

    # 2- Use it
    if expected_e is None:
        # **** Nominal test ****
        outs = super_function_i_want_to_test(**i)
        assert outs == expected_o

    else:
        # **** Error test ****
        # First see what we need to assert
        err_type, err_ptrn, err_inst, err_checker = unfold_expected_err(expected_e)

        # Run with exception capture and type check
        with pytest.raises(err_type) as err_info:
            super_function_i_want_to_test(**i)

        # Optional - Additional Exception instance check
        if err_inst is not None:
            assert err_info.value == err_inst

        # Optional - Additional exception instance check
        if err_checker is not None:
            err_checker(err_info.value)
