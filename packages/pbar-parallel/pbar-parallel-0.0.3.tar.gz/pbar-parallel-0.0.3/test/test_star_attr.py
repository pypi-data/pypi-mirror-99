"""Code by https://gist.github.com/oakkitten/03ca8f9c1113a7e32e32135e2cf5fef9
"""

import inspect
from typing import Dict, Tuple, Optional, List, Sequence, MutableSequence, Iterable, Mapping, MutableMapping, Collection

from attr import attrib
from pytest import raises

from src._star_attr import star_attrs, star_attrib


@star_attrs
class Foo:
    foo = attrib()
    args = star_attrib()


class TestStarArgs:
    def test_no_args(self):
        with raises(TypeError):
            Foo()

    def test_unexpected_kwarg(self):
        with raises(TypeError):
            Foo(bar=1)

    def test_no_starargs(self):
        assert Foo("a").args == ()

    def test_one_stararg(self):
        assert Foo("a", "b").args == ("b",)

    def test_two_starargs(self):
        assert Foo("a", "b", "c").args == ("b", "c")

    def test_positional_specified_with_keyword(self):
        foo = Foo(foo=1)
        assert foo.foo == 1
        assert foo.args == ()

##########################################################################


@star_attrs()
class Bar:
    foo = attrib()
    kwargs = star_attrib(kw_only=True)


class TestStarKwargs:
    def test_no_args(self):
        with raises(TypeError):
            Bar()

    def test_too_many_args(self):
        with raises(TypeError):
            Bar("a", "b")

    def test_no_star_kwargs(self):
        assert Bar("a").kwargs == {}

    def test_multiple_values_for_argument(self):
        with raises(TypeError):
            assert Bar("a", foo=1)

##########################################################################


@star_attrs(frozen=True)
class Baz:
    foo = attrib()
    args = star_attrib()
    bar = attrib(kw_only=True, factory=int)
    kwargs = star_attrib(kw_only=True)


class TestStarArgsKwargs:
    def test_no_star_kwargs(self):
        bar = Baz("a")
        assert bar.bar == 0 and bar.kwargs == {}
        bar = Baz("a", bar=1)
        assert bar.bar == 1 and bar.kwargs == {}

    def test_some_kwargs(self):
        baz = Baz("a", "b", baz=1, quux=2)
        assert baz.args == ("b",)
        assert baz.kwargs == dict(baz=1, quux=2)

    def test_kwargs_with_same_names_as_stargs(self):
        assert Baz("a", args=1, kwargs=2).kwargs == dict(args=1, kwargs=2)

##########################################################################


class TestBadDefs:
    def test_default_given(self):
        with raises(ValueError):
            @star_attrs
            class Qux:      # noqa
                args = star_attrib(factory=int)

    def test_init_false(self):
        with raises(ValueError):
            @star_attrs
            class Qux:      # noqa
                args = star_attrib(init=False)

    def test_raises_bad_order(self):
        with raises(ValueError):
            @star_attrs
            class Qux:      # noqa
                args = star_attrib()
                arg = attrib()

    def test_raises_many_starargs(self):
        with raises(ValueError):
            @star_attrs
            class Qux:      # noqa
                args = star_attrib()
                args2 = star_attrib()

    def test_raises_many_star_kwargs(self):
        with raises(ValueError):
            @star_attrs
            class Qux:      # noqa
                args = star_attrib(kw_only=True)
                args2 = star_attrib(kw_only=True)

    # same as Baz, but without `kw_only=True` on the `bar` attribute
    def test_stararag_before_positional(self):
        with raises(ValueError):
            @star_attrs(frozen=True)
            class Qux:      # noqa
                foo = attrib()
                args = star_attrib()
                bar = attrib(factory=int)
                kwargs = star_attrib(kw_only=True)

##########################################################################

class TestSignature:
    def test_stararg(self):
        assert str(inspect.signature(Foo)) == "(foo, *args) -> None"

    def test_starkwarg(self):
        assert str(inspect.signature(Bar)) == "(foo, **kwargs) -> None"

    def test_stararg_kwarg(self):
        assert str(inspect.signature(Baz)) == "(foo, *args, bar=NOTHING, **kwargs) -> None"

    def test_kw_only_and_kwargs(self):
        @star_attrs
        class Corge:
            foo = attrib(kw_only=True)
            bar = attrib()
            kwargs = star_attrib(kw_only=True)

        assert str(inspect.signature(Corge)) == "(bar, *, foo, **kwargs) -> None"

    def test_typing_convert_strips_off_typing(self):
        @star_attrs
        class Corge:
            args: Tuple[str, ...] = star_attrib(converter=list)

        assert str(inspect.signature(Corge)) == "(*args) -> None"

    def test_weird_order_1(self):
        @star_attrs
        class Baz1:
            kwargs = star_attrib(kw_only=True)
            foo = attrib()
            args = star_attrib()
            bar = attrib(kw_only=True, factory=int)

        assert str(inspect.signature(Baz1)) == "(foo, *args, bar=NOTHING, **kwargs) -> None"

    def test_weird_order_2(self):
        @star_attrs
        class Baz2:
            kwargs = star_attrib(kw_only=True)
            kwarg = attrib(kw_only=True)
            foo = attrib()
            args = star_attrib()

        assert str(inspect.signature(Baz2)) == "(foo, *args, kwarg, **kwargs) -> None"

    def test_weird_order_3(self):
        @star_attrs
        class Baz3:
            kwarg1 = attrib(kw_only=True)
            foo = attrib()
            kwargs = star_attrib(kw_only=True)
            bar = attrib()
            args = star_attrib()
            kwarg2 = attrib(kw_only=True)

        assert str(inspect.signature(Baz3)) == "(foo, bar, *args, kwarg1, kwarg2, **kwargs) -> None"

    class TestTyping:
        def test_expected_tuple_dict(self):
            @star_attrs
            class Corge:
                kwargs: Dict[str, int] = star_attrib(kw_only=True)
                foo: Optional[str] = attrib()
                args: Tuple[str, ...] = star_attrib()
                bar: int = attrib(kw_only=True, factory=int)

            assert str(inspect.signature(Corge)) == "(foo: Union[str, NoneType], *args: str, bar: int = NOTHING, **kwargs: int) -> None"

        def test_expected_sequence_mapping(self):
            @star_attrs
            class Corge:
                args: Sequence[str] = star_attrib()
                kwargs: Mapping[str, int] = star_attrib(kw_only=True)

            assert str(inspect.signature(Corge)) == "(*args: str, **kwargs: int) -> None"

        def test_expected_iterable_mutable_mapping(self):
            @star_attrs
            class Corge:
                args: Iterable[str] = star_attrib()
                kwargs: MutableMapping[str, int] = star_attrib(kw_only=True)

            assert str(inspect.signature(Corge)) == "(*args: str, **kwargs: int) -> None"

        # we wouldn't be getting anything other than `Tuple[?, ...]` and `Dict[str, ?]` from attrs, unless there's a
        # converter. attrs strip type information when the converter is present. we follow the same principle here
        def test_unexpected_list_mistyped_dict(self):
            @star_attrs
            class Corge:
                kwargs: Dict[int, str] = star_attrib(kw_only=True)
                foo: Optional[str] = attrib()
                args: List[str] = star_attrib()
                bar: int = attrib(kw_only=True, factory=int)

            assert str(inspect.signature(Corge)) == "(foo: Union[str, NoneType], *args, bar: int = NOTHING, **kwargs) -> None"

        def test_unexpected_mutable_sequence_collection(self):
            @star_attrs
            class Corge:
                args: MutableSequence[str] = star_attrib()
                kwargs: Collection[int] = star_attrib(kw_only=True)

            assert str(inspect.signature(Corge)) == "(*args, **kwargs) -> None"

        def test_unexpected_non_container_types(self):
            @star_attrs
            class Corge:
                args: str = star_attrib()
                kwargs: int = star_attrib(kw_only=True)

            assert str(inspect.signature(Corge)) == "(*args, **kwargs) -> None"

        def test_unexpected_non_variadic_tuple_one(self):
            @star_attrs
            class Corge:
                args: Tuple[str] = star_attrib()

            assert str(inspect.signature(Corge)) == "(*args) -> None"

        def test_forward_ref(self):
            @star_attrs
            class Corge:
                args: 'Tuple[str, ...]' = star_attrib()

            assert str(inspect.signature(Corge)) == "(*args: str) -> None"

        def test_forward_ref_inside(self):
            @star_attrs
            class Corge:
                args: Tuple['str', ...] = star_attrib()

            assert str(inspect.signature(Corge)) == "(*args: str) -> None"

        def test_forward_ref_broken(self):
            @star_attrs
            class Corge:
                args: 'Zuple[str, ...]' = star_attrib()

            assert str(inspect.signature(Corge)) == "(*args) -> None"

        def test_forward_ref_preserves_broken(self):
            @star_attrs
            class Corge:
                foo: 'Scooby Doo' = attrib()
                args: 'Tuple[str, ...]' = star_attrib()

            assert str(inspect.signature(Corge)) == "(foo: 'Scooby Doo', *args: str) -> None"

##########################################################################

def validator(_self, _attribute, value):
    if value['hello'] < 0:
        raise ValueError


@star_attrs(eq=False)
class Quux:
    foo = attrib()
    args = star_attrib(converter=" ".join)
    bar = attrib(kw_only=True, factory=int)
    kwargs = star_attrib(kw_only=True, validator=validator)


class TestMisc:
    def test_converter(self):
        assert Quux("a", "b", "c", hello=1).args == "b c"

    def test_validator(self):
        Quux("a", "b", "c", hello=1)

        with raises(ValueError):
            Quux("a", "b", "c", hello=-1)

    # `kw_only=True` is ignored if `init=False` is given
    def test_no_init(self):
        @star_attrs
        class Corge:
            foo = attrib(init=False)
            args = star_attrib()
            bar = attrib(init=False, factory=int)
            kwargs = star_attrib(kw_only=True)

        corge = Corge("a", "b", c=1)

        with raises(AttributeError):
            corge.foo  # noqa
        assert corge.args == ("a", "b")
        assert corge.bar == 0
        assert corge.kwargs == dict(c=1)

        assert str(inspect.signature(Corge)) == "(*args, **kwargs) -> None"

    def test_auto_attribs(self):
        @star_attrs(auto_attribs=True)
        class Corge:
            foo: int
            args: Collection[int] = star_attrib()
            kwargs: Dict[str, int] = star_attrib(kw_only=True)

        assert str(inspect.signature(Corge)) == "(foo: int, *args: int, **kwargs: int) -> None"

    def test_partial(self):
        from functools import partial
        star_frozen = partial(star_attrs, frozen=True)

        @star_frozen
        class Corge:
            args = star_attrib()

        assert Corge("a", "b").args == ("a", "b")

        @star_frozen()
        class Corge:
            args = star_attrib()

        assert Corge("a", "b").args == ("a", "b")

##########################################################################

@star_attrs
class Pos:
    pos = attrib()


@star_attrs
class Kwonly:
    kwonly = attrib(kw_only=True)


@star_attrs
class Args:
    args = star_attrib()


@star_attrs
class Kwargs:
    kwargs = star_attrib(kw_only=True)


class TestSubclassing:
    def test_pos_args(self):
        @star_attrs
        class PosArgs(Pos, Args):
            pass

        pos_args = PosArgs("a", "b", "c")
        assert pos_args.pos == "a"
        assert pos_args.args == ("b", "c")

    def test_pos_kwargs(self):
        @star_attrs
        class PosKwargs(Pos, Kwargs):
            pass

        with raises(TypeError):
            PosKwargs("a", "b")
        pos_kwargs = PosKwargs("a", b=1)
        assert pos_kwargs.pos == "a"
        assert pos_kwargs.kwargs == dict(b=1)

    def test_kwonly_args(self):
        @star_attrs
        class KwonlyArgs(Kwonly, Args):
            pass

        kwonly_args = KwonlyArgs("a", "b", kwonly=1)
        assert kwonly_args.args == ("a", "b")
        assert kwonly_args.kwonly == 1

    def test_kwonly_kwargs(self):
        @star_attrs
        class KwonlyKwargs(Kwonly, Kwargs):
            pass

        kwonly_kwargs = KwonlyKwargs(a=1, b=2, kwonly=1)
        assert kwonly_kwargs.kwargs == dict(a=1, b=2)
        assert kwonly_kwargs.kwonly == 1

    def test_pos_added_kwargs(self):
        @star_attrs
        class PosArgsPlus(Pos, Args):
            kwargs = star_attrib(kw_only=True)

        pos_args_plus = PosArgsPlus("a", b=1)
        assert pos_args_plus.pos == "a"
        assert pos_args_plus.args == ()
        assert pos_args_plus.kwargs == dict(b=1)

    def test_all_together(self):
        @star_attrs
        class PosArgsKwargsKwonly(Pos, Args, Kwargs, Kwonly):
            pass

        all_together = PosArgsKwargsKwonly("a", "b", c=1, kwonly=7)
        assert all_together.pos == "a"
        assert all_together.args == ("b",)
        assert all_together.kwargs == dict(c=1)
        assert all_together.kwonly == 7

        with raises(TypeError):
            PosArgsKwargsKwonly("a")

    def test_overwriting_star_args(self):
        @star_attrs
        class PosArgs(Pos, Args):
            args = star_attrib()
        assert PosArgs("a").args == ()

    def test_multiple_star_attrib(self):
        with raises(ValueError):
            @star_attrs
            class PosArgs(Pos, Args):           # noqa
                boop = star_attrib()

    def test_multiple_star_keyword_attrib(self):
        with raises(ValueError):
            @star_attrs
            class PosKwargs(Pos, Kwargs):       # noqa
                boop = star_attrib(kw_only=True)

    def test_bad_class_order(self):
        with raises(ValueError):
            @star_attrs
            class ArgsPos(Args, Pos):           # noqa
                pass

    def test_sub_subclassing(self):
        @star_attrs
        class Zoo(Pos):
            zoo = attrib()

        @star_attrs
        class Moo(Kwonly):
            moo = star_attrib()

        @star_attrs
        class Poo(Zoo, Moo):
            poo = attrib(kw_only=True)

        @star_attrs
        class Woo(Poo):
            woo = star_attrib(kw_only=True)

        assert str(inspect.signature(Woo)) == "(pos, zoo, *moo, kwonly, poo, **woo) -> None"